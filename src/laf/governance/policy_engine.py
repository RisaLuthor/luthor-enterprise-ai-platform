from __future__ import annotations

from typing import List, Tuple

from laf.governance.models import EvaluateRequest, Violation
from laf.governance.pii_detect import detect_pii, redact_pii

def _risk_score(classification: str, findings: List[str]) -> int:
    base = 5 if classification.upper() == "INTERNAL" else 10
    bump = 20 * len(findings)
    score = min(100, base + bump)
    return score

def evaluate(req: EvaluateRequest) -> Tuple[bool, int, List[Violation], List[str], str, List[str]]:
    text = req.input_text or ""
    classification = (req.data_classification or "INTERNAL").upper()

    audit: List[str] = []
    findings = detect_pii(text)
    audit.append(f"findings={findings}")

    sanitized, redactions = redact_pii(text)
    if redactions:
        audit.append(f"redactions={redactions}")

    violations: List[Violation] = []

    # Always record that findings were detected if any PII-like pattern exists
    if findings:
        violations.append(
            Violation(
                code="FINDINGS_DETECTED",
                message="Potential sensitive findings detected.",
                severity="MEDIUM",
                rule="pii",
            )
        )

    allowed = True
    # For RESTRICTED, block if any PII findings
    if classification == "RESTRICTED" and findings:
        allowed = False
        violations.append(
            Violation(
                code="POLICY_BLOCK",
                message="RESTRICTED inputs containing PII are not allowed.",
                severity="HIGH",
                rule="pii",
            )
        )
        audit.append("blocked=policy_block")

    risk = _risk_score(classification, findings)
    audit.append(f"risk={risk}")

    return allowed, risk, violations, redactions, sanitized, audit
