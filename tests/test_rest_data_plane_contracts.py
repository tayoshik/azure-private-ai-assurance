"""Offline fixture contracts for Azure OpenAI, AI Search and Cosmos DB.

No external I/O or Azure credentials. A green mock test cannot certify Azure.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import rest_data_plane_contracts as contracts


REQUESTS = {
    "azure_openai": {
        "method": "POST",
        "path": "/openai/v1/chat/completions",
        "api_version": "v1",
        "auth_mode": "entra_bearer_placeholder",
        "headers": {"Content-Type": "application/json"},
        "body": {
            "model": "synthetic-model",
            "messages": [{"role": "user", "content": "synthetic-request"}],
            "stream": False,
        },
    },
    "ai_search": {
        "method": "POST",
        "path": "/indexes('synthetic-index')/docs/search.post.search",
        "api_version": "2025-09-01",
        "auth_mode": "entra_bearer_placeholder",
        "headers": {"Content-Type": "application/json"},
        "body": {"search": "synthetic", "count": True, "top": 2},
    },
    "cosmos_nosql": {
        "method": "POST",
        "path": "/dbs/syntheticdb/colls/syntheticcoll/docs",
        "api_version": "2018-12-31",
        "auth_mode": "entra_bearer_placeholder",
        "headers": {
            "Content-Type": "application/query+json",
            "x-ms-documentdb-isquery": "true",
            "x-ms-version": "2018-12-31",
        },
        "body": {
            "query": contracts.COSMOS_QUERY,
            "parameters": [{"name": "@id", "value": "synthetic-doc"}],
        },
    },
}
BODIES = {
    "azure_openai": {
        "id": "chatcmpl-synthetic",
        "choices": [{
            "index": 0,
            "finish_reason": "stop",
            "message": {"role": "assistant", "content": "synthetic response"},
        }],
        "usage": {"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
    },
    "ai_search": {
        "@odata.count": 1,
        "value": [{"id": "synthetic-doc"}],
    },
    "cosmos_nosql": {
        "_count": 1,
        "Documents": [{"id": "synthetic-doc"}],
    },
}


def fixture(service):
    return {
        "schema": contracts.SCHEMA,
        "execution_class": "OFFLINE_MOCK_ONLY",
        "request": deepcopy(REQUESTS[service]),
        "response": {"status": 200, "headers": {}, "body": deepcopy(BODIES[service])},
    }


class ServiceContracts(unittest.TestCase):
    def good(self, service):
        result = contracts.evaluate_fixture(service, fixture(service))
        self.assertEqual(result["classification"], "OFFLINE_RESPONSE_CONTRACT_MATCH_ONLY")
        self.assertEqual(result["execution_class"], "OFFLINE_MOCK_ONLY")
        self.assertEqual(result["scope_approval"], "PENDING_SCOPE_CHANGE_APPROVAL")
        self.assertEqual(result["verified_azure_live_passes"], 0)
        self.assertEqual(result["network_requests"], 0)
        self.assertEqual(result["release_decision"], "NO_GO")
        self.assertTrue(result["api_unit_contract_evaluated"])
        self.assertNotIn("synthetic response", json.dumps(result))
        return result

    def rejects(self, service, change):
        f = fixture(service)
        change(f)
        with self.assertRaises(contracts.ContractError):
            contracts.evaluate_fixture(service, f)

    def test_openai_valid_nonstreaming_synthetic_response(self):
        self.good("azure_openai")

    def test_search_valid_synthetic_query_response(self):
        self.good("ai_search")

    def test_cosmos_valid_parameterized_synthetic_query_response(self):
        self.good("cosmos_nosql")

    def test_no_other_profiles(self):
        for service in ("storage", "custom_endpoint", "azure_openai_alt"):
            with self.subTest(service=service):
                with self.assertRaises(contracts.ContractError):
                    contracts.evaluate_fixture(service, fixture("azure_openai"))

    def test_schema_and_execution_class_must_be_explicit(self):
        for key, value in (("schema", "v2"), ("execution_class", "LIVE_APPROVED")):
            with self.subTest(key=key):
                self.rejects("azure_openai", lambda f: f.__setitem__(key, value))

    def test_no_extra_envelope_fields(self):
        self.rejects("azure_openai", lambda f: f.__setitem__("azure_token", "secret"))

    def test_requests_deny_write_or_get_methods(self):
        for service in REQUESTS:
            for method in ("GET", "PUT", "PATCH", "DELETE", "HEAD"):
                with self.subTest(service=service, method=method):
                    self.rejects(service, lambda f: f["request"].update(method=method))

    def test_url_must_be_pinned_relative_path(self):
        for path in (
            "https://attacker.example/openai/v1/chat/completions",
            "/openai/v1/chat/completions?api-version=latest",
            "/openai/v1/../chat/completions",
            "/openai/v1/%2e%2e/chat/completions",
            "/openai/v1/chat/completions#fragment",
        ):
            with self.subTest(path=path):
                self.rejects("azure_openai", lambda f: f["request"].update(path=path))

    def test_azure_openai_version_must_not_be_latest(self):
        self.rejects("azure_openai", lambda f: f["request"].update(api_version="latest"))

    def test_search_exact_post_endpoint_and_version(self):
        for key, val in (("path", "/indexes('synthetic-index')/docs"),
                         ("api_version", "2026-08-01-preview")):
            with self.subTest(key=key):
                self.rejects("ai_search", lambda f: f["request"].update(**{key: val}))

    def test_cosmos_exact_query_endpoint_and_version(self):
        for key, val in (("path", "/dbs/db/colls/coll/docs/id"),
                         ("api_version", "latest")):
            with self.subTest(key=key):
                self.rejects("cosmos_nosql", lambda f: f["request"].update(**{key: val}))

    def test_actual_auth_or_api_key_values_not_accepted(self):
        for key in ("authorization", "api-key"):
            with self.subTest(key=key):
                self.rejects("azure_openai", lambda f:
                    f["request"]["headers"].update({key: "Bearer real-token-secret"}))
        self.rejects("azure_openai", lambda f:
                     f["request"].update(auth_mode="actual_bearer_token"))

    def test_duplicate_headers_case_insensitive(self):
        self.rejects("azure_openai", lambda f:
                     f["request"]["headers"].update({"content-type": "application/json"}))

    def test_openai_messages_must_be_fixed_synthetic(self):
        self.rejects("azure_openai", lambda f:
                     f["request"]["body"]["messages"][0].update(content="real user prompt"))
        self.rejects("azure_openai", lambda f:
                     f["request"]["body"]["messages"][0].update(role="system"))

    def test_openai_streaming_not_covered(self):
        self.rejects("azure_openai", lambda f:
                     f["request"]["body"].update(stream=True))

    def test_openai_model_name_cannot_be_url(self):
        self.rejects("azure_openai", lambda f:
                     f["request"]["body"].update(model="https://example.net"))

    def test_openai_wrong_choice_shape(self):
        self.rejects("azure_openai", lambda f:
                     f["response"]["body"]["choices"][0]["message"].update(role="user"))
        self.rejects("azure_openai", lambda f:
                     f["response"]["body"].update(choices=[]))

    def test_openai_wrong_usage_accounting(self):
        self.rejects("azure_openai", lambda f:
                     f["response"]["body"]["usage"].update(total_tokens=999))
        self.rejects("azure_openai", lambda f:
                     f["response"]["body"]["usage"].update(total_tokens=True))

    def test_search_query_bounded_and_synthetic(self):
        self.rejects("ai_search", lambda f:
                     f["request"]["body"].update(top=True))
        self.rejects("ai_search", lambda f:
                     f["request"]["body"].update(top=1000))
        self.rejects("ai_search", lambda f:
                     f["request"]["body"].update(search="*"))

    def test_search_missing_value_or_bad_count(self):
        self.rejects("ai_search", lambda f:
                     f["response"]["body"].pop("value"))
        self.rejects("ai_search", lambda f:
                     f["response"]["body"].update(**{"@odata.count": True}))
        self.rejects("ai_search", lambda f:
                     f["response"]["body"].update(**{"@odata.count": 0}))

    def test_search_continuation_is_not_followed(self):
        f = fixture("ai_search")
        f["response"]["body"]["@odata.nextLink"] = "https://untrusted.example/next"
        result = contracts.evaluate_fixture("ai_search", f)
        self.assertEqual(result["classification"], "OFFLINE_CONTINUATION_NOT_FOLLOWED")
        self.assertEqual(result["network_requests"], 0)
        self.assertNotIn("untrusted.example", json.dumps(result))

    def test_cosmos_query_must_be_parameterized(self):
        self.rejects("cosmos_nosql", lambda f:
                     f["request"]["body"].update(query="SELECT * FROM c"))
        self.rejects("cosmos_nosql", lambda f:
                     f["request"]["body"].update(parameters=[]))
        self.rejects("cosmos_nosql", lambda f:
                     f["request"]["body"]["parameters"][0].update(value="' OR 1=1 --"))

    def test_cosmos_query_required_header_values(self):
        self.rejects("cosmos_nosql", lambda f:
                     f["request"]["headers"].update(**{"Content-Type": "application/json"}))
        self.rejects("cosmos_nosql", lambda f:
                     f["request"]["headers"].update(**{"x-ms-documentdb-isquery": "false"}))

    def test_cosmos_document_count_must_match(self):
        self.rejects("cosmos_nosql", lambda f:
                     f["response"]["body"].update(_count=2))
        self.rejects("cosmos_nosql", lambda f:
                     f["response"]["body"].update(_count=True))
        self.rejects("cosmos_nosql", lambda f:
                     f["response"]["body"].update(Documents=[{"not-id": "bad"}]))

    def test_explicit_denial_not_security_pass(self):
        for service in REQUESTS:
            for status in (401, 403):
                with self.subTest(service=service, status=status):
                    f = fixture(service)
                    f["response"] = {
                        "status": status,
                        "headers": {},
                        "body": {"error": {"message": "mock secret should not echo"}},
                    }
                    r = contracts.evaluate_fixture(service, f)
                    self.assertEqual(r["classification"], "OFFLINE_DENIAL_NOT_ISOLATION_EVIDENCE")
                    self.assertEqual(r["verified_azure_live_passes"], 0)
                    self.assertNotIn("secret", json.dumps(r))

    def test_429_retry_hint_never_performs_retry(self):
        for service in ("azure_openai", "ai_search"):
            with self.subTest(service=service):
                f = fixture(service)
                f["response"] = {"status": 429, "headers": {"Retry-After": "2"},
                                 "body": {"error": {"code": "throttled"}}}
                r = contracts.evaluate_fixture(service, f)
                self.assertEqual(r["classification"], "OFFLINE_RETRY_HINT_NOT_EXECUTED")
                self.assertEqual(r["network_requests"], 0)

    def test_cosmos_429_millisecond_hint(self):
        f = fixture("cosmos_nosql")
        f["response"] = {"status": 429,
                         "headers": {"x-ms-retry-after-ms": "1000"},
                         "body": {}}
        r = contracts.evaluate_fixture("cosmos_nosql", f)
        self.assertEqual(r["classification"], "OFFLINE_RETRY_HINT_NOT_EXECUTED")

    def test_503_with_retry_metadata_is_only_mock(self):
        f = fixture("azure_openai")
        f["response"] = {"status": 503, "headers": {"Retry-After": "1"}, "body": {}}
        r = contracts.evaluate_fixture("azure_openai", f)
        self.assertEqual(r["classification"], "OFFLINE_RETRY_HINT_NOT_EXECUTED")

    def test_invalid_retry_hint_fails_closed(self):
        for retry in (None, "-1", "NaN", "120001"):
            with self.subTest(retry=retry):
                f = fixture("azure_openai")
                h = {} if retry is None else {"Retry-After": retry}
                f["response"] = {"status": 429, "headers": h, "body": {}}
                with self.assertRaises(contracts.ContractError):
                    contracts.evaluate_fixture("azure_openai", f)

    def test_404_and_500_are_only_error_observations(self):
        for status in (400, 404, 500, 502, 504):
            with self.subTest(status=status):
                f = fixture("ai_search")
                f["response"] = {"status": status, "headers": {}, "body": {}}
                r = contracts.evaluate_fixture("ai_search", f)
                self.assertEqual(r["classification"], "OFFLINE_ERROR_OBSERVATION_ONLY")
                self.assertEqual(r["release_decision"], "NO_GO")

    def test_unrecognized_success_status_cannot_be_mock_pass(self):
        for status in (201, 204, 302, 418):
            with self.subTest(status=status):
                f = fixture("cosmos_nosql")
                f["response"]["status"] = status
                with self.assertRaises(contracts.ContractError):
                    contracts.evaluate_fixture("cosmos_nosql", f)

    def test_duplicate_response_header_rejected(self):
        self.rejects("ai_search", lambda f:
                     f["response"]["headers"].update({"Retry-After": "1", "retry-after": "1"}))

    def test_fixture_size_bound_and_finite_json(self):
        self.rejects("ai_search", lambda f:
                     f["response"]["body"].update(huge="x" * 66000))
        self.rejects("ai_search", lambda f:
                     f["response"]["body"].update(nonfinite=float("nan")))

    def test_missing_response_shape_rejected(self):
        self.rejects("cosmos_nosql", lambda f: f["response"].pop("status"))
        self.rejects("cosmos_nosql", lambda f: f["response"].update(status=True))


if __name__ == "__main__":
    unittest.main()
