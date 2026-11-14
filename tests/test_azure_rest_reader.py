import importlib.util
from pathlib import Path
import io
import json
import unittest
from urllib.error import HTTPError

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('azure_rest_reader',ROOT/'scripts/azure_rest_reader.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
SID='01234567-89ab-4def-8123-0123456789ab'
RID=f'/subscriptions/{SID}/resourceGroups/rg-test/providers/Microsoft.Web/sites/web-demo'
class FakeResponse:
    def __init__(self,payload,status=200):self.payload=json.dumps(payload).encode();self.status=status
    def read(self,n):return self.payload[:n]
    def __enter__(self):return self
    def __exit__(self,*args):return False

class ClientTests(unittest.TestCase):
    def client(self,handler=None,*,enabled=True,sleep=None,attempts=3):
        return a.AzureReadOnlyClient([SID],lambda:'TEST_TOKEN',read_enabled=enabled,
              transport=handler or (lambda req,timeout:FakeResponse({'id':RID})),
              sleeper=sleep or (lambda s:None),max_attempts=attempts)
    def test_opt_in_required(self):
        with self.assertRaises(a.NotReadyError):self.client(enabled=False).get_resource(RID,'2024-04-01')
    def test_unauthorized_target_scope(self):
        with self.assertRaises(ValueError):self.client().get_resource(RID.replace(SID,'11111111-1111-4111-8111-111111111111'),'2024-04-01')
    def test_bad_api_version(self):
        with self.assertRaises(ValueError):self.client().get_resource(RID,'latest')
    def test_get_safe_and_observed_not_pass(self):
        c=self.client()
        result=c.get_resource(RID,'2024-04-01')
        self.assertEqual(result['state'],'OBSERVED_NOT_ACCEPTED')
        self.assertEqual(len(result['evidence_sha256']),64)
    def test_no_write_methods(self):
        with self.assertRaises(ValueError):self.client()._send('DELETE','/subscriptions/x')
    def test_no_arbitrary_post(self):
        with self.assertRaises(ValueError):self.client()._send('POST','/subscriptions/x',{'a':1})
    def test_no_redirect_leak(self):
        self.assertIsNone(a._NoRedirect().redirect_request(None,None,302,'',{},'https://evil.example'))
    def test_403_not_ready(self):
        def t(req,timeout):raise HTTPError(req.full_url,403,'forbidden',{},None)
        with self.assertRaises(a.NotReadyError):self.client(t).get_resource(RID,'2024-04-01')
    def test_404_not_ready_not_pass(self):
        def t(req,timeout):raise HTTPError(req.full_url,404,'missing',{},None)
        with self.assertRaises(a.NotReadyError):self.client(t).get_resource(RID,'2024-04-01')
    def test_429_retry_after(self):
        calls=[];wait=[]
        def t(req,timeout):
            calls.append(1)
            if len(calls)==1:raise HTTPError(req.full_url,429,'throttle',{'Retry-After':'2'},None)
            return FakeResponse({'id':RID})
        self.client(t,sleep=wait.append).get_resource(RID,'2024-04-01')
        self.assertEqual(len(calls),2);self.assertEqual(wait,[2.0])
    def test_429_exhausted_not_ready(self):
        def t(req,timeout):raise HTTPError(req.full_url,429,'throttle',{'Retry-After':'0'},None)
        with self.assertRaises(a.NotReadyError):self.client(t,attempts=2).get_resource(RID,'2024-04-01')
    def test_200_unexpected_shape(self):
        def t(req,timeout):return FakeResponse({'unexpected':True})
        with self.assertRaises(a.NotReadyError):self.client(t).get_resource(RID,'2024-04-01')
    def test_graph_pagination(self):
        calls=[]
        def t(req,timeout):
            calls.append(json.loads(req.data))
            item={'id':RID,'type':'microsoft.web/sites','subscriptionId':SID}
            return FakeResponse({'data':[item],'$skipToken':'next'}) if len(calls)==1 else FakeResponse({'data':[item]})
        result=self.client(t).resource_graph_inventory(['microsoft.web/sites'])
        self.assertEqual(result['page_count'],2)
        self.assertEqual(len(result['rows']),2)
        self.assertEqual(calls[1]['options']['$skipToken'],'next')
    def test_graph_out_of_scope_rejected(self):
        def t(req,timeout):return FakeResponse({'data':[{'subscriptionId':'11111111-1111-4111-8111-111111111111','type':'microsoft.web/sites'}]})
        with self.assertRaises(a.NotReadyError):self.client(t).resource_graph_inventory(['microsoft.web/sites'])
    def test_graph_truncation_without_token(self):
        def t(req,timeout):return FakeResponse({'data':[], 'resultTruncated': True})
        with self.assertRaises(a.NotReadyError):self.client(t).resource_graph_inventory(['microsoft.web/sites'])
    def test_graph_repeated_token(self):
        def t(req,timeout):return FakeResponse({'data':[], '$skipToken':'dup'})
        with self.assertRaises(a.NotReadyError):self.client(t).resource_graph_inventory(['microsoft.web/sites'])
    def test_graph_unsupported_type(self):
        with self.assertRaises(ValueError):self.client().resource_graph_inventory(['microsoft.authorization/roleassignments'])
    def test_oidc_must_be_configured(self):
        from unittest.mock import patch
        with patch.dict('os.environ',{},clear=True):
            with self.assertRaises(a.NotReadyError):a.workload_identity_token_provider()
    def test_not_ready_on_large_response(self):
        class Large(FakeResponse):
            def read(self,n):return b'x' * n
        with self.assertRaises(a.NotReadyError):self.client(lambda req,timeout:Large({})).get_resource(RID,'2024-04-01')

if __name__=='__main__':unittest.main()
