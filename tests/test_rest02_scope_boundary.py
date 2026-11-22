"""REST02 defense-in-depth regression: offline fake transports, no cloud SDK/network."""
from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "azure_rest_reader_boundaries", ROOT / "scripts/azure_rest_reader.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

SID = "01234567-89ab-4def-8123-0123456789ab"
OTHER = "11111111-1111-4111-8111-111111111111"
RID = f"/subscriptions/{SID}/resourceGroups/rg-test/providers/Microsoft.Web/sites/web-demo"
OTHER_RID = RID.replace(SID, OTHER)
VERSION = "2024-04-01"
GRAPH_TYPE = "microsoft.web/sites"


class Response:
    status = 200

    def __init__(self, value):
        self.bytes = json.dumps(value).encode("utf-8")

    def read(self, limit):
        return self.bytes[:limit]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class REST02Boundaries(unittest.TestCase):
    def setUp(self):
        self.transport_calls = 0
        self.token_calls = 0
        self.waits = []

    def send(self, fn, timeout=15):
        self.transport_calls += 1
        self.assertEqual(fn.full_url.split("?", 1)[0].startswith(m.ARM_HOST), True)
        self.assertEqual(timeout, 15)
        return Response({"id": RID})

    def token(self):
        self.token_calls += 1
        return "synthetic-token-never-send-to-Azure"

    def client(self, transport=None, attempts=3, token_provider=None):
        return m.AzureReadOnlyClient(
            [SID], token_provider or self.token, read_enabled=True,
            transport=transport or self.send, sleeper=self.waits.append,
            max_attempts=attempts)

    def test_out_of_scope_get_transport_denied_before_token(self):
        with self.assertRaisesRegex(ValueError, "outside approved scope"):
            self.client()._send("GET", OTHER_RID + "?api-version=" + VERSION)
        self.assertEqual((self.token_calls, self.transport_calls), (0, 0))

    def test_fake_subscriptions_and_unsafe_uris_rejected_before_token(self):
        cases = (
            RID + "/../other?api-version=" + VERSION,
            RID + "/./child?api-version=" + VERSION,
            RID + "?api-version=" + VERSION + "&other=yes",
            RID + "?api-version=latest",
            RID + "?api-version=" + VERSION + "#evil",
            RID + "/%2e%2e?api-version=" + VERSION,
            "https://unapproved.example/subscriptions/" + SID + "/resources?api-version=" + VERSION,
            "/subscriptions/" + SID + "/resourceGroups/rg-test?api-version=" + VERSION,
            RID,
            RID + "?x=1",
        )
        for path in cases:
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    self.client()._send("GET", path)
        self.assertEqual((self.token_calls, self.transport_calls), (0, 0))

    def test_get_does_not_allow_dot_segments(self):
        for resource_id in (RID + "/../other", RID + "/./other"):
            with self.subTest(resource_id=resource_id):
                with self.assertRaises(ValueError):
                    self.client().get_resource(resource_id, VERSION)
        self.assertEqual((self.token_calls, self.transport_calls), (0, 0))

    def test_unsafe_http_methods_and_get_body_denied(self):
        for method in ("PUT", "DELETE", "PATCH", "HEAD"):
            with self.subTest(method=method):
                with self.assertRaises(ValueError):
                    self.client()._send(method, RID + "?api-version=" + VERSION)
        with self.assertRaises(ValueError):
            self.client()._send("GET", RID + "?api-version=" + VERSION, {"mutation": True})
        self.assertEqual((self.token_calls, self.transport_calls), (0, 0))

    def test_valid_get_is_observation_not_cloud_acceptance(self):
        result = self.client().get_resource(RID, VERSION)
        self.assertEqual(result["state"], "OBSERVED_NOT_ACCEPTED")
        self.assertEqual(result["resource_id"], RID)
        self.assertEqual(len(result["evidence_sha256"]), 64)
        self.assertNotIn("synthetic-token", json.dumps(result))
        self.assertEqual((self.token_calls, self.transport_calls), (1, 1))

    @staticmethod
    def graph_row(**changes):
        row = {"id": RID, "type": GRAPH_TYPE, "subscriptionId": SID}
        row.update(changes)
        return row

    def graph(self, row):
        return self.client(lambda req, timeout: Response({"data": [row]})).resource_graph_inventory([GRAPH_TYPE])

    def test_graph_mismatched_id_subscription_rejected(self):
        with self.assertRaisesRegex(m.NotReadyError, "scope/type"):
            self.graph(self.graph_row(id=OTHER_RID))

    def test_graph_row_missing_id_rejected(self):
        with self.assertRaisesRegex(m.NotReadyError, "invalid resource ID"):
            self.graph(self.graph_row(id=None))

    def test_graph_row_id_type_does_not_match_reported_type(self):
        with self.assertRaisesRegex(m.NotReadyError, "scope/type"):
            self.graph(self.graph_row(id=RID.replace("Microsoft.Web/sites", "Microsoft.Search/searchServices")))

    def test_graph_id_path_traversal_rejected(self):
        with self.assertRaisesRegex(m.NotReadyError, "invalid resource ID"):
            self.graph(self.graph_row(id=RID + "/../other"))

    def test_graph_valid_scope_observation_not_pass(self):
        result = self.graph(self.graph_row())
        self.assertEqual(result["state"], "OBSERVED_NOT_ACCEPTED")
        self.assertEqual(result["page_count"], 1)
        self.assertTrue(result["complete_pages"])
        self.assertEqual(len(result["evidence_sha256"]), 64)
        self.assertNotIn("PASS", json.dumps(result))

    def test_invalid_json_response_fails_closed(self):
        class Broken(Response):
            def __init__(self):
                self.bytes = b"{not-json"
        with self.assertRaisesRegex(m.NotReadyError, "invalid JSON"):
            self.client(lambda req, timeout: Broken()).get_resource(RID, VERSION)

    def test_bad_token_short_circuits_transport(self):
        def denied():
            raise RuntimeError("credential failure")
        with self.assertRaisesRegex(m.NotReadyError, "OIDC authentication"):
            self.client(token_provider=denied).get_resource(RID, VERSION)
        self.assertEqual(self.transport_calls, 0)

    def test_empty_token_short_circuits_transport(self):
        with self.assertRaisesRegex(m.NotReadyError, "OIDC token unavailable"):
            self.client(token_provider=lambda: "").get_resource(RID, VERSION)
        self.assertEqual(self.transport_calls, 0)

    def test_401_does_not_retry_and_redacts_token(self):
        def unauthorized(req, timeout):
            self.transport_calls += 1
            raise HTTPError(req.full_url, 401, "secret must not echo", {}, None)
        with self.assertRaisesRegex(m.NotReadyError, "ARM status 401") as ctx:
            self.client(unauthorized).get_resource(RID, VERSION)
        self.assertNotIn("synthetic-token", str(ctx.exception))
        self.assertEqual(self.transport_calls, 1)
        self.assertEqual(self.waits, [])

    def test_503_retries_and_recovers(self):
        def temporarily_unavailable(req, timeout):
            self.transport_calls += 1
            if self.transport_calls < 3:
                raise HTTPError(req.full_url, 503, "unavailable", {"Retry-After": "1"}, None)
            return Response({"id": RID})
        result = self.client(temporarily_unavailable).get_resource(RID, VERSION)
        self.assertEqual(result["state"], "OBSERVED_NOT_ACCEPTED")
        self.assertEqual(self.transport_calls, 3)
        self.assertEqual(self.waits, [1.0, 1.0])

    def test_network_failure_exhausts_retry_to_not_ready(self):
        def network_failure(req, timeout):
            self.transport_calls += 1
            raise URLError("synthetic broken network")
        with self.assertRaisesRegex(m.NotReadyError, "network unavailable"):
            self.client(network_failure, attempts=2).get_resource(RID, VERSION)
        self.assertEqual(self.transport_calls, 2)
        self.assertEqual(self.waits, [1.0])

    def test_read_disabled_prevents_network_and_token(self):
        c = m.AzureReadOnlyClient([SID], self.token, read_enabled=False, transport=self.send)
        with self.assertRaisesRegex(m.NotReadyError, "explicit approved opt-in"):
            c.get_resource(RID, VERSION)
        self.assertEqual((self.token_calls, self.transport_calls), (0, 0))


if __name__ == "__main__":
    unittest.main()
