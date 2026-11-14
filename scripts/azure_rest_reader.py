#!/usr/bin/env python3
"""REST02: fail-closed, read-only ARM/Resource Graph client.

No Azure connections occur on import. An approved runner must opt in with
read_enabled=True and a scoped WorkloadIdentityCredential. No Terraform apply,
ARM PUT/PATCH/DELETE, generic REST POST, or CLI login is provided.
"""
from __future__ import annotations
import hashlib
import json
import os
import re
import time
from urllib import request, error
from uuid import UUID
from typing import Callable

ARM_HOST = "https://management.azure.com"
ARM_SCOPE = ARM_HOST + "/.default"
GRAPH_PATH = "/providers/Microsoft.ResourceGraph/resources?api-version=2022-10-01"
MAX_RESPONSE_BYTES = 2_097_152
APPROVED_TYPES = frozenset({
    "microsoft.web/sites", "microsoft.cognitiveservices/accounts",
    "microsoft.search/searchservices", "microsoft.documentdb/databaseaccounts",
    "microsoft.network/privateendpoints", "microsoft.network/applicationgateways",
    "microsoft.keyvault/vaults", "microsoft.network/virtualnetworks",
})
RESOURCE_RE = re.compile(r"^/subscriptions/([^/]+)/resourceGroups/([^/]+)/providers/([a-zA-Z0-9.]+)/([a-zA-Z0-9_./-]+)$", re.I)
VERSION_RE = re.compile(r"^20\d\d-\d\d-\d\d(?:-preview)?$")

class NotReadyError(Exception):
    """Missing permission, environment, evidence or complete observation."""

class RestFailure(Exception):
    """Unexpected HTTP status or invalid read-only response."""

class _NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def workload_identity_token_provider() -> Callable[[], str]:
    """Explicit OIDC credential; no fall back to local CLI or shared secrets."""
    keys = ("AZURE_CLIENT_ID", "AZURE_TENANT_ID", "AZURE_FEDERATED_TOKEN_FILE")
    if any(not os.environ.get(k) for k in keys):
        raise NotReadyError("approved workload identity environment is incomplete")
    if not os.path.isfile(os.environ["AZURE_FEDERATED_TOKEN_FILE"]):
        raise NotReadyError("federated token file is unavailable")
    try:
        from azure.identity import WorkloadIdentityCredential
    except ImportError as exc:
        raise NotReadyError("approved azure-identity package is unavailable") from exc
    credential = WorkloadIdentityCredential()
    return lambda: credential.get_token(ARM_SCOPE).token


def _uuid(value: str) -> str:
    try:
        parsed = UUID(str(value))
    except (ValueError, TypeError) as exc:
        raise ValueError("subscription ID must be a UUID") from exc
    return str(parsed)


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


class AzureReadOnlyClient:
    def __init__(self, subscriptions: list[str], token_provider: Callable[[], str], *,
                 read_enabled: bool = False, transport=None, sleeper=time.sleep,
                 max_attempts: int = 3):
        if not subscriptions:
            raise ValueError("explicit subscription scope required")
        self.subscriptions = tuple(_uuid(s) for s in subscriptions)
        if len(set(self.subscriptions)) != len(self.subscriptions):
            raise ValueError("duplicate subscription scope")
        if not 1 <= max_attempts <= 5:
            raise ValueError("max_attempts must be 1..5")
        self.token_provider = token_provider
        self.read_enabled = bool(read_enabled)
        self.transport = transport or request.build_opener(_NoRedirect()).open
        self.sleeper = sleeper
        self.max_attempts = max_attempts

    def _send(self, method: str, path: str, body: dict | None = None) -> dict:
        if not self.read_enabled:
            raise NotReadyError("live REST reads require explicit approved opt-in")
        if method == "GET":
            if body is not None or not path.startswith("/subscriptions/"):
                raise ValueError("GET only permits scoped ARM resource paths")
        elif method == "POST":
            if path != GRAPH_PATH or not isinstance(body, dict):
                raise ValueError("POST permitted only for fixed read-only Resource Graph query")
        else:
            raise ValueError("HTTP method is not allowlisted")
        try:
            token = self.token_provider()
        except Exception as exc:
            raise NotReadyError("OIDC authentication unavailable") from exc
        if not isinstance(token, str) or not token:
            raise NotReadyError("OIDC token unavailable")
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = request.Request(ARM_HOST + path, data=data, method=method,
                              headers={"Authorization": f"Bearer {token}",
                                       "Accept": "application/json", "Content-Type": "application/json"})
        for attempt in range(self.max_attempts):
            try:
                with self.transport(req, timeout=15) as res:
                    code = res.status
                    if code != 200:
                        raise RestFailure(f"non-200 response: {code}")
                    raw = res.read(MAX_RESPONSE_BYTES + 1)
                    if len(raw) > MAX_RESPONSE_BYTES:
                        raise NotReadyError("response exceeds bounded size")
                    try:
                        result = json.loads(raw)
                    except (ValueError, UnicodeDecodeError) as exc:
                        raise NotReadyError("invalid JSON response") from exc
                    if not isinstance(result, dict):
                        raise NotReadyError("unexpected response shape")
                    return result
            except error.HTTPError as exc:
                status = exc.code
                if status in (401, 403, 404):
                    raise NotReadyError(f"ARM status {status}: missing identity, permission or target") from None
                if status not in (429, 500, 502, 503, 504):
                    raise RestFailure(f"ARM HTTP status {status}") from None
                if attempt + 1 == self.max_attempts:
                    raise NotReadyError("transient ARM failure after bounded retries") from None
                delay = min(30.0, 2.0**attempt)
                header = exc.headers.get("Retry-After") if exc.headers else None
                if header is not None:
                    try:
                        delay = min(30.0, max(0.0, float(header)))
                    except ValueError:
                        pass
                self.sleeper(delay)
            except (TimeoutError, error.URLError) as exc:
                if attempt + 1 == self.max_attempts:
                    raise NotReadyError("ARM network unavailable after bounded retries") from None
                self.sleeper(min(30.0, 2.0**attempt))
        raise AssertionError("unreachable")

    def get_resource(self, resource_id: str, api_version: str) -> dict:
        """Fetch a single resource, but never claim PASS for its configuration."""
        match = RESOURCE_RE.fullmatch(resource_id)
        if not match or _uuid(match[1]) not in self.subscriptions:
            raise ValueError("resource ID is invalid or outside approved subscription")
        if not VERSION_RE.fullmatch(api_version):
            raise ValueError("pinned API version required")
        data = self._send("GET", resource_id + "?api-version=" + api_version)
        actual = str(data.get("id", ""))
        if actual.lower() != resource_id.lower():
            raise NotReadyError("returned resource ID does not match approved target")
        return {"state": "OBSERVED_NOT_ACCEPTED", "resource_id": resource_id,
                "evidence_sha256": _digest(data), "observation": data}

    def resource_graph_inventory(self, resource_types: list[str], *, max_pages: int = 20, page_size: int = 200) -> dict:
        """Query only curated resource types in explicitly scoped subscriptions."""
        types = sorted({str(t).lower() for t in resource_types})
        if not types or any(t not in APPROVED_TYPES for t in types):
            raise ValueError("unsupported resource type")
        if not 1 <= max_pages <= 100 or not 1 <= page_size <= 1000:
            raise ValueError("unsafe page count/size")
        quoted_types = ", ".join("'" + t + "'" for t in types)
        query = ("Resources | where type in~ (" + quoted_types + ") "
                 "| project id,name,type,location,resourceGroup,subscriptionId | order by id asc")
        base = {"subscriptions": list(self.subscriptions), "query": query,
                "options": {"$top": page_size}}
        seen_tokens = set()
        rows = []
        for page in range(max_pages):
            response = self._send("POST", GRAPH_PATH, base)
            data = response.get("data")
            if not isinstance(data, list):
                raise NotReadyError("Resource Graph response data is not a list")
            for item in data:
                if not isinstance(item, dict):
                    raise NotReadyError("Resource Graph row is invalid")
                try:
                    scope = _uuid(item.get("subscriptionId", ""))
                except ValueError as exc:
                    raise NotReadyError("out-of-scope or incomplete Resource Graph row") from exc
                if scope not in self.subscriptions or str(item.get("type", "")).lower() not in types:
                    raise NotReadyError("Resource Graph returned unexpected scope/type")
                rows.append(item)
            token = response.get("$skipToken")
            if not token:
                if str(response.get("resultTruncated", "false")).lower() == "true":
                    raise NotReadyError("Graph result truncated without continuation token")
                return {"state": "OBSERVED_NOT_ACCEPTED", "rows": rows,
                        "page_count": page+1, "evidence_sha256": _digest(rows),
                        "complete_pages": True}
            if not isinstance(token, str) or token in seen_tokens:
                raise NotReadyError("invalid or repeated Graph continuation token")
            seen_tokens.add(token)
            base["options"]["$skipToken"] = token
        raise NotReadyError("Resource Graph page limit reached before completion")
