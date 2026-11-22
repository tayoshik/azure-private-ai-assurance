#!/usr/bin/env python3
"""Offline-only REST data-plane fixture-contract checks for three Azure services.

NO HTTP transport, credential loading, Azure SDK, Terraform or network I/O.
These are narrow, versioned synthetic example contracts, not live acceptance.
"""
from __future__ import annotations

import json
import re

SCHEMA = "azure-data-plane-mock-contract/v1"
SERVICES = frozenset({"azure_openai", "ai_search", "cosmos_nosql"})
SAFE_NAME = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}\Z")
SEARCH_PATH = re.compile(r"/indexes\('([a-zA-Z0-9_-]{1,64})'\)/docs/search\.post\.search\Z")
COSMOS_PATH = re.compile(r"/dbs/([a-zA-Z0-9_-]{1,64})/colls/([a-zA-Z0-9_-]{1,64})/docs\Z")
COSMOS_QUERY = "SELECT TOP 1 c.id FROM c WHERE c.id = @id"
MAX_FIXTURE_BYTES = 65_536


class ContractError(ValueError):
    """Invalid synthetic contract; errors intentionally avoid payload disclosure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def bounded_json(value: object) -> None:
    try:
        raw = json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, OverflowError) as exc:
        raise ContractError("fixture is not finite JSON") from exc
    require(len(raw) <= MAX_FIXTURE_BYTES, "fixture exceeds bounded size")


def _str(value: object, limit: int = 256) -> bool:
    return isinstance(value, str) and bool(value) and len(value) <= limit


def validate_request(service: str, request: dict) -> None:
    require(service in SERVICES, "unsupported service")
    require(isinstance(request, dict) and set(request) ==
            {"method", "path", "api_version", "auth_mode", "headers", "body"},
            "request envelope fields invalid")
    require(request["method"] == "POST", "only approved query/sample methods permitted")
    require(request["auth_mode"] == "entra_bearer_placeholder",
            "only a credential-free Entra auth placeholder is permitted")
    path = request["path"]
    require(isinstance(path, str) and len(path) <= 256 and
            "?" not in path and "#" not in path and
            "://" not in path and "%" not in path and ".." not in path,
            "request must use a literal relative path")
    headers = request["headers"]
    require(isinstance(headers, dict) and all(
            isinstance(k, str) and isinstance(v, str) for k, v in headers.items()),
            "request header metadata invalid")
    require(len(headers) == len({k.lower() for k in headers}),
            "case-insensitive duplicate headers are forbidden")
    normalized = {k.lower(): v for k, v in headers.items()}
    require("authorization" not in normalized and "api-key" not in normalized and
            "x-ms-date" not in normalized and "x-ms-continuation" not in normalized,
            "credential, signed header or continuation value forbidden")
    body = request["body"]
    require(isinstance(body, dict), "request body invalid")

    if service == "azure_openai":
        require(path == "/openai/v1/chat/completions" and
                request["api_version"] == "v1",
                "OpenAI v1 endpoint/version mismatch")
        require(normalized == {"content-type": "application/json"},
                "OpenAI header contract mismatch")
        require(set(body) == {"model", "messages", "stream"} and
                _str(body["model"], 64) and
                SAFE_NAME.fullmatch(body["model"]) and
                body["stream"] is False, "OpenAI request shape invalid")
        messages = body["messages"]
        require(isinstance(messages, list) and len(messages) == 1 and
                isinstance(messages[0], dict) and
                set(messages[0]) == {"role", "content"} and
                messages[0]["role"] == "user" and
                messages[0]["content"] == "synthetic-request",
                "OpenAI test prompt must be fixed and synthetic")
    elif service == "ai_search":
        require(bool(SEARCH_PATH.fullmatch(path)) and
                request["api_version"] == "2025-09-01",
                "AI Search path/version mismatch")
        require(normalized == {"content-type": "application/json"},
                "AI Search header contract mismatch")
        require(set(body) == {"search", "count", "top"} and
                body["search"] == "synthetic" and
                body["count"] is True and
                type(body["top"]) is int and 1 <= body["top"] <= 20,
                "AI Search example request must be a bounded synthetic query")
    else:
        require(bool(COSMOS_PATH.fullmatch(path)) and
                request["api_version"] == "2018-12-31",
                "Cosmos NoSQL query path/version mismatch")
        require(normalized == {
            "content-type": "application/query+json",
            "x-ms-documentdb-isquery": "true",
            "x-ms-version": "2018-12-31",
        }, "Cosmos NoSQL query header contract mismatch")
        require(set(body) == {"query", "parameters"} and
                body["query"] == COSMOS_QUERY and
                isinstance(body["parameters"], list) and
                len(body["parameters"]) == 1 and
                type(body["parameters"][0]) is dict and
                body["parameters"][0] == {"name": "@id", "value": "synthetic-doc"},
                "Cosmos query must be fixed and parameterized")


def validate_success(service: str, body: dict) -> str:
    require(isinstance(body, dict), "success body must be an object")
    if service == "azure_openai":
        require(_str(body.get("id")) and
                isinstance(body.get("choices"), list) and
                len(body["choices"]) == 1, "OpenAI choices/id malformed")
        choice = body["choices"][0]
        require(isinstance(choice, dict) and
                type(choice.get("index")) is int and choice["index"] == 0 and
                choice.get("finish_reason") == "stop" and
                isinstance(choice.get("message"), dict) and
                choice["message"].get("role") == "assistant" and
                _str(choice["message"].get("content"), 4_096),
                "OpenAI synthetic assistant response malformed")
        if "usage" in body:
            u = body["usage"]
            require(isinstance(u, dict) and all(
                type(u.get(k)) is int and u[k] >= 0 for k in
                ("prompt_tokens", "completion_tokens", "total_tokens")) and
                u["prompt_tokens"] + u["completion_tokens"] == u["total_tokens"],
                "OpenAI usage accounting malformed")
    elif service == "ai_search":
        value = body.get("value")
        require(isinstance(value, list) and len(value) <= 20 and
                all(isinstance(doc, dict) and
                    _str(doc.get("id"), 128) for doc in value),
                "AI Search synthetic result list malformed")
        count = body.get("@odata.count")
        require(type(count) is int and count >= len(value),
                "AI Search synthetic count malformed")
        if "@odata.nextLink" in body or "@search.nextPageParameters" in body:
            return "OFFLINE_CONTINUATION_NOT_FOLLOWED"
    else:
        documents = body.get("Documents")
        require(isinstance(documents, list) and len(documents) <= 20 and
                all(isinstance(doc, dict) and
                    _str(doc.get("id"), 128) for doc in documents),
                "Cosmos NoSQL synthetic documents malformed")
        require(type(body.get("_count")) is int and
                body["_count"] == len(documents),
                "Cosmos NoSQL synthetic count malformed")
    return "OFFLINE_RESPONSE_CONTRACT_MATCH_ONLY"


def evaluate_fixture(service: str, fixture: dict) -> dict:
    """No I/O. Return only classification and metadata, never payload or secrets."""
    require(isinstance(fixture, dict) and
            set(fixture) == {"schema", "execution_class", "request", "response"} and
            fixture["schema"] == SCHEMA and
            fixture["execution_class"] == "OFFLINE_MOCK_ONLY",
            "not an approved synthetic fixture envelope")
    bounded_json(fixture)
    validate_request(service, fixture["request"])
    response = fixture["response"]
    require(isinstance(response, dict) and
            set(response) == {"status", "headers", "body"} and
            type(response["status"]) is int and
            isinstance(response["headers"], dict) and
            isinstance(response["body"], dict),
            "response envelope invalid")
    require(all(isinstance(k, str) and isinstance(v, str)
                for k, v in response["headers"].items()),
            "response header metadata invalid")
    require(len(response["headers"]) == len(
            {k.lower() for k in response["headers"]}),
            "duplicate response header names")
    headers = {k.lower(): v for k, v in response["headers"].items()}
    status = response["status"]
    if status == 200:
        classification = validate_success(service, response["body"])
    elif status in (401, 403):
        classification = "OFFLINE_DENIAL_NOT_ISOLATION_EVIDENCE"
    elif status in (429, 503):
        retry = headers.get("retry-after")
        if service == "cosmos_nosql":
            retry = headers.get("x-ms-retry-after-ms", retry)
        require(retry is not None and retry.isdigit() and
                0 <= int(retry) <= 120_000, "retry interval invalid or absent")
        classification = "OFFLINE_RETRY_HINT_NOT_EXECUTED"
    elif status in (400, 404, 500, 502, 504):
        classification = "OFFLINE_ERROR_OBSERVATION_ONLY"
    else:
        raise ContractError("unexpected HTTP status in synthetic fixture")
    return {
        "schema": SCHEMA,
        "service": service,
        "execution_class": "OFFLINE_MOCK_ONLY",
        "classification": classification,
        "http_status": status,
        "network_requests": 0,
        "scope_approval": "PENDING_SCOPE_CHANGE_APPROVAL",
        "api_unit_contract_evaluated": True,
        "verified_azure_live_passes": 0,
        "release_decision": "NO_GO",
    }
