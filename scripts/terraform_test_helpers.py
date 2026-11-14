"""Mutation test helper: preserve semantics across official `terraform fmt` spacing changes."""
from __future__ import annotations
import re


def replace_mutation(source: str, before: str, after: str) -> str:
    if before in source:
        return source.replace(before, after, 1)
    # Compare token sequences separated by any whitespace. Reject ambiguity.
    tokens = before.split()
    if not tokens:
        raise AssertionError("Empty mutation selector")
    pattern = re.compile(r"\s+".join(map(re.escape, tokens)), re.MULTILINE)
    matches = list(pattern.finditer(source))
    if len(matches) != 1:
        raise AssertionError(f"Mutation selector expected once, found {len(matches)}: {before!r}")
    match = matches[0]
    return source[:match.start()] + after + source[match.end():]
