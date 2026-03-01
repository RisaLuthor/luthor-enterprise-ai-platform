from __future__ import annotations

import argparse
import sys
from pathlib import Path

from laf.governance.models import EvaluateRequest
from laf.governance.policy_engine import evaluate as eval_policy


def run_scenarios(path: str) -> int:
    p = Path(path)
    if not p.exists():
        print(f"Path not found: {p}", file=sys.stderr)
        return 2

    files = []
    if p.is_dir():
        files = sorted(list(p.glob("*.yaml")) + list(p.glob("*.yml")))
    else:
        files = [p]

    out_dir = Path("reports")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Minimal: evaluate each file as plain text content (placeholder).
    # You can evolve this into real scenario YAML parsing later.
    for f in files:
        text = f.read_text(encoding="utf-8")
        req = EvaluateRequest(input_text=text, data_classification="INTERNAL", policy_profile="default")
        allowed, risk, violations, redactions, sanitized, audit = eval_policy(req)

        report = {
            "file": str(f),
            "allowed": allowed,
            "risk_score": risk,
            "violations": [v.model_dump() for v in violations],
            "redactions_applied": redactions,
            "sanitized_text": sanitized,
            "audit_trail": audit,
        }

        report_path = out_dir / f"{f.stem}.report.json"
        report_path.write_text(__import__("json").dumps(report, indent=2), encoding="utf-8")

    print(f"Wrote {len(files)} report(s) to {out_dir}/")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="laf", description="Luthor AI Systems Framework CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    runp = sub.add_parser("run", help="Run scenarios from a path (file or directory)")
    runp.add_argument("path", help="Scenario YAML file or directory containing YAML files")

    args = parser.parse_args(argv)

    if args.cmd == "run":
        return run_scenarios(args.path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
