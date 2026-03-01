from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

def log_evaluation(
    *,
    input_text: str,
    data_classification: str,
    allowed: bool,
    risk_score: int,
    violations: List[Dict[str, Any]],
    redactions_applied: List[str],
    sanitized_text: str,
    audit_trail: List[str],
) -> None:
    out_dir = Path("audit_logs")
    out_dir.mkdir(parents=True, exist_ok=True)

    rec = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "data_classification": data_classification,
        "allowed": allowed,
        "risk_score": risk_score,
        "violations": violations,
        "redactions_applied": redactions_applied,
        "sanitized_text": sanitized_text,
        "audit_trail": audit_trail,
        "input_preview": (input_text or "")[:200],
    }

    path = out_dir / "evaluations.jsonl"
    path.open("a", encoding="utf-8").write(json.dumps(rec) + "\n")
