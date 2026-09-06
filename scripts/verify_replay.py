"""Repeat the complete fixed benchmark and compare every evidence field."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import DEFAULT_ARTIFACT, ROOT
from src.evaluation import evaluate_core
from src.reproducibility import save_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--episodes", type=int, default=50)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "reproducibility.json")
    args = parser.parse_args()
    try:
        first = evaluate_core(args.artifact, episodes=args.episodes)
        second = evaluate_core(args.artifact, episodes=args.episodes)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Replay failed: {error}\n")
    canonical_first = json.dumps(first, sort_keys=True, allow_nan=False).encode()
    canonical_second = json.dumps(second, sort_keys=True, allow_nan=False).encode()
    result = {
        "status": "PASS" if first == second else "FAIL", "episodes_per_run": args.episodes,
        "runs": 2, "exact_report_equality": first == second,
        "first_report_sha256": hashlib.sha256(canonical_first).hexdigest(),
        "second_report_sha256": hashlib.sha256(canonical_second).hexdigest(),
        "compared": ["seeds", "mappings", "sample_ids", "metrics", "parameter_deltas", "keys", "memory_tensors", "query_scores", "predictions", "conflicts", "resets"],
        "environment": first["environment"], "encoder_sha256": first["encoder_sha256"],
    }
    save_json(args.output, result)
    print(json.dumps(result, indent=2))
    if first != second:
        parser.exit(1, "Deterministic evaluation replay differed\n")


if __name__ == "__main__":
    main()
