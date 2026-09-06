"""Deterministic critical path; never silently train a missing artifact."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import DEFAULT_ARTIFACT
from src.evaluation import evaluate_core


def run_smoke(artifact: str | Path = DEFAULT_ARTIFACT) -> dict:
    report = evaluate_core(artifact, episodes=5)
    summary = report["summary"]
    checks = {
        "above_chance": summary["mean_accuracy"] > summary["chance"],
        "encoder_unchanged": summary["encoder_parameter_delta_max"] == 0 and summary["all_encoder_parameters_equal"],
        "memory_updated": summary["memory_delta_min"] > 0,
        "conflict_changes_state": summary["conflict_memory_delta_min"] > 0,
        "reset_clears_memory": summary["reset_all_empty"],
    }
    if not all(checks.values()):
        raise RuntimeError(f"Smoke checks failed: {checks}")
    return {"status": "PASS", "checks": checks, "summary": summary}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    args = parser.parse_args()
    try:
        result = run_smoke(args.artifact)
    except (ValueError, OSError, RuntimeError) as error:
        parser.exit(1, f"Smoke test failed: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
