import subprocess
import sys
from pathlib import Path

def test_cli_run_generates_reports(tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    (work / "scenarios").mkdir()

    # create dummy scenario yaml file
    scenario_dir = work / "scenarios" / "examples"
    scenario_dir.mkdir(parents=True)
    (scenario_dir / "example.yaml").write_text("email: test@example.com\n", encoding="utf-8")

    r = subprocess.run(
        [sys.executable, "-m", "laf", "run", str(scenario_dir)],
        cwd=work,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr

    reports = work / "reports"
    assert reports.exists()
    assert any(p.suffix == ".json" for p in reports.iterdir())
