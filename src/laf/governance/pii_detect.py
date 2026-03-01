from __future__ import annotations

import re
from typing import List

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b")

def detect_pii(text: str) -> List[str]:
    findings: List[str] = []
    if EMAIL_RE.search(text):
        findings.append("PII_EMAIL")
    if PHONE_RE.search(text):
        findings.append("PII_PHONE")
    return findings

def redact_pii(text: str) -> tuple[str, List[str]]:
    redactions: List[str] = []
    out = text

    if EMAIL_RE.search(out):
        out = EMAIL_RE.sub("[REDACTED:EMAIL]", out)
        redactions.append("EMAIL")

    if PHONE_RE.search(out):
        out = PHONE_RE.sub("[REDACTED:PHONE]", out)
        redactions.append("PHONE")

    return out, redactions
