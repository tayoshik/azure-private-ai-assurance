#!/usr/bin/env python3
"""Validate the shape of an external Playwright implementation contract OFFLINE.

Even a perfect document is an untrusted, self-reported proposal, not approval,
a successful browser run, verified Azure isolation, or permission to deploy.
This tool intentionally ALWAYS exits 2. Never commit actual identities/secrets.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

KIND_BY_ID = {
    "AZ-T64-01": "internal_https_response",
    "AZ-T64-03": "tls_chain_and_hostname",
    "AZ-T64-05": "authorized_sign_in",
    "AZ-T64-07": "authenticated_health_status",
    "AZ-T64-09": "verified_dom_render",
    "AZ-T64-11": "synthetic_search_result",
    "AZ-T64-13": "safe_chat_and_redaction",
    "AZ-T64-15": "expired_or_revoked_session_rejected",
    "AZ-T64-17": "protected_data_absent_on_error",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
IDENTITY_REF = re.compile(r"^(?:vault|protected-environment):[A-Za-z0-9_./-]{3,128}$")
SUSPICIOUS_KEYS = {
    "password", "client_secret", "access_token", "refresh_token",
    "id_token", "private_key", "api_key", "cookie", "connection_string",
}
PLACEHOLDER = re.compile(r"(?i)^(?:todo|tbd|placeholder|unknown|not_ready|example|dummy|none|n/a)$")


def _required(data, dotted, errors):
    node = data
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            errors.append(f"missing field: {dotted}")
            return None
        node = node[part]
    if not isinstance(node, str) or not node.strip() or PLACEHOLDER.fullmatch(node.strip()):
        errors.append(f"invalid field: {dotted}")
        return None
    if len(node) > 512:
        errors.append(f"field too long: {dotted}")
        return None
    return node.strip()


def _forbidden_keys(node, errors, prefix=""):
    if isinstance(node, dict):
        for key, val in node.items():
            label = str(key)
            if label.lower() in SUSPICIOUS_KEYS:
                errors.append(f"embedded credential key forbidden: {prefix}{label}")
            _forbidden_keys(val, errors, prefix + label + ".")
    elif isinstance(node, list):
        for x in node:
            _forbidden_keys(x, errors, prefix)


def _url_valid(raw):
    try:
        url = urlsplit(raw)
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            return False
        if url.query or url.fragment or url.path not in ("", "/"):
            return False
        host = url.hostname.lower().rstrip(".")
        if host in {"localhost", "example.com", "example.org", "example.net"}:
            return False
        if host.endswith((".example.com", ".example.org", ".example.net", ".localhost")):
            return False
        try:
            ipaddress.ip_address(host)
            return False   # require reviewed hostname/TLS certificate, not a raw IP
        except ValueError:
            pass
        if "." not in host or any(not label for label in host.split(".")):
            return False
        port = url.port
        if port is not None and port not in (443, 8443):
            return False
        return True
    except (ValueError, TypeError):
        return False


def validate(doc):
    errors = []
    if not isinstance(doc, dict):
        doc = {}
        errors.append("root must be an object")
    _forbidden_keys(doc, errors)
    if doc.get("schema") != "azure-private-ai-playwright-contract/v1":
        errors.append("unsupported or missing schema")

    source_repo = _required(doc, "application.source_repo", errors)
    commit = _required(doc, "application.commit_sha", errors)
    artifact = _required(doc, "application.artifact_sha256", errors)
    private_url = _required(doc, "application.private_base_url", errors)
    health = _required(doc, "application.health_path", errors)
    login = _required(doc, "application.login_path", errors)
    tls_host = _required(doc, "network.tls_hostname", errors)
    inside = _required(doc, "network.internal_runner_group", errors)
    outside = _required(doc, "network.external_runner_group", errors)
    _required(doc, "network.dns_owner", errors)
    auth = _required(doc, "identity.auth_type", errors)
    identity = _required(doc, "identity.protected_identity_ref", errors)
    _required(doc, "identity.session_revocation_method", errors)
    _required(doc, "ui.synthetic_test_data_id", errors)
    _required(doc, "evidence.authorization_ticket", errors)
    evidence_sha = _required(doc, "evidence.approved_baseline_sha256", errors)
    _required(doc, "evidence.retention_policy_ref", errors)

    if source_repo and not REPOSITORY.fullmatch(source_repo):
        errors.append("invalid application source_repo")
    if commit and not COMMIT.fullmatch(commit):
        errors.append("invalid immutable application commit")
    if artifact and not SHA256.fullmatch(artifact):
        errors.append("invalid application artifact sha256")
    if evidence_sha and not SHA256.fullmatch(evidence_sha):
        errors.append("invalid approved baseline digest")
    if private_url and not _url_valid(private_url):
        errors.append("private_base_url must be a reviewed HTTPS hostname without credentials")
    if private_url and tls_host and _url_valid(private_url) and urlsplit(private_url).hostname != tls_host.lower():
        errors.append("TLS hostname must match private URL host")
    for item, value in (("health_path", health), ("login_path", login)):
        if value is not None and (not value.startswith("/") or
                                  value.startswith("//") or "?" in value or "#" in value or
                                  ".." in value):
            errors.append("invalid application " + item)
    if inside and outside and inside == outside:
        errors.append("internal and external runner groups must differ")
    if auth and auth != "EntraOIDC":
        errors.append("authentication mode must be EntraOIDC for this version")
    if identity and not IDENTITY_REF.fullmatch(identity):
        errors.append("identity must be a protected secret-location reference, never a credential")

    selectors = doc.get("ui", {}).get("selectors") if isinstance(doc.get("ui"), dict) else None
    expected_sel = ("main", "search_input", "search_result", "chat_input", "chat_result", "error_container")
    if not isinstance(selectors, dict):
        errors.append("ui.selectors must map the six reviewed UI contracts")
    else:
        for key in expected_sel:
            val = selectors.get(key)
            if not isinstance(val, str) or not val.strip() or len(val) > 256 or PLACEHOLDER.fullmatch(val.strip()):
                errors.append("missing real UI selector: " + key)

    reviewers = doc.get("evidence", {}).get("reviewer_roles") if isinstance(doc.get("evidence"), dict) else None
    if not isinstance(reviewers, list) or len(reviewers) < 2 or not all(
        isinstance(x, str) and x.strip() and not PLACEHOLDER.fullmatch(x.strip()) for x in reviewers
    ) or len(set(reviewers)) < 2:
        errors.append("two independent reviewer roles required (not approval evidence)")

    scenarios = doc.get("scenarios")
    if not isinstance(scenarios, dict) or set(scenarios) != set(KIND_BY_ID):
        errors.append("scenarios must cover exactly nine AZ-T64 positive IDs")
    else:
        for key, kind in KIND_BY_ID.items():
            case = scenarios[key]
            if not isinstance(case, dict) or case.get("assertion_kind") != kind:
                errors.append("incorrect case-specific assertion_kind: " + key)
            elif not isinstance(case.get("criterion_reference"), str) or not case["criterion_reference"].strip():
                errors.append("missing criterion_reference: " + key)

    # No approval is derived from user-provided JSON or a successful parser.
    return {
        "schema": "azure-private-ai-playwright-contract-check/v1",
        "result": "NOT_READY" if errors else "CONTRACT_STRUCTURE_VALID_EXTERNAL_VERIFICATION_REQUIRED",
        "errors": errors,
        "required_journey_count": len(KIND_BY_ID),
        "independent_approval_verified": False,
        "app_source_verified_against_repo": False,
        "private_runner_execution_verified": False,
        "browser_tests_executed": 0,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True,
                        help="approved-owner candidate in restricted storage; NEVER commit credentials")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    try:
        doc = json.loads(args.contract.read_text(encoding="utf-8"))
        result = validate(doc)
    except (OSError, ValueError, UnicodeError):
        result = validate(None)
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    print(output, end="")
    # Always exit 2: independent app/runner/evidence approval is outside this script.
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
