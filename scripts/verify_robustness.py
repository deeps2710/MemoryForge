"""Run Phase 3 robustness checks in the invoking (preferably freshly installed) environment."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from time import perf_counter
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import ROOT, DEFAULT_ARTIFACT
from src.encoder import load_encoder, parameter_snapshot, parameters_equal
from src.reproducibility import save_json, environment_info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "phase3_robustness.json")
    args = parser.parse_args()
    scratch = ROOT / ".local" / ("robustness-" + uuid.uuid4().hex[:10])
    scratch.mkdir(parents=True)
    commands = []
    def run(arguments):
        start = perf_counter()
        result = subprocess.run([sys.executable, *arguments], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        entry = {"arguments": arguments, "exit_code": result.returncode,
                 "elapsed_seconds": perf_counter()-start, "stdout": result.stdout, "stderr": result.stderr}
        commands.append(entry)
        print(f'{arguments[:3]}: exit {result.returncode}', flush=True)
        if result.returncode:
            save_json(args.output, {"status": "FAIL", "commands": commands})
            raise RuntimeError(result.stdout + result.stderr)
        return result
    run(["-m","pip","check"])
    run(["-m","pytest","-q","--basetemp",str(scratch / "pytest"),
         "-o",f"cache_dir={scratch / 'cache'}"])
    run(["scripts/smoke_test.py"])
    regenerated = scratch / "regenerated.pt"
    run(["scripts/train_encoder.py","--output",str(regenerated)])
    original, _ = load_encoder(DEFAULT_ARTIFACT)
    regenerated_model, _ = load_encoder(regenerated)
    equal = parameters_equal(regenerated_model, parameter_snapshot(original))
    if not equal:
        raise RuntimeError("Regenerated encoder differs from checked-in encoder")
    run(["scripts/evaluate_core.py","--artifact",str(regenerated),"--output",str(scratch / "core.json")])
    core = json.loads((scratch / "core.json").read_text())
    baseline = json.loads((ROOT / "artifacts" / "evaluation.json").read_text())
    # Numerical core evidence is compared separately from the environment inventory.
    equal_keys = [key for key in baseline if key != "environment"]
    core_equal = all(core[key] == baseline[key] for key in equal_keys)
    if not core_equal:
        raise RuntimeError("Regenerated artifact's core evidence changed")
    packages = json.loads(run(["-m","pip","list","--format=json"]).stdout)
    save_json(args.output, {
        "status":"PASS", "verified_at_utc":datetime.now(timezone.utc).isoformat(),
        "python_executable":sys.executable, "environment":environment_info(),
        "isolated_environment":sys.prefix != sys.base_prefix,
        "installed_packages":packages, "commands":commands[:-1],
        "regenerated_encoder_exactly_equal":equal,
        "regenerated_core_evidence_equal_excluding_environment":core_equal,
        "offline_scope":"test_research denies socket connect/connect_ex/create_connection with fresh Streamlit caches, then opens and operates lab and research page. Does not modify system network settings.",
        "limits":"Windows CPU/Python 3.12.14 only; installer requires network; no cross-platform or public deployment claim."
    })
    print(f"Robustness PASS: {args.output}")


if __name__ == "__main__":
    main()
