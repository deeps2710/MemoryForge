"""Evaluate fixed unseen-image episodes, conflicts and reset; save actual evidence."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import DEFAULT_ARTIFACT, ROOT, EpisodeConfig, SeedConfig
from src.evaluation import evaluate_core
from src.reproducibility import save_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "evaluation.json")
    parser.add_argument("--episodes", type=int, default=50)
    parser.add_argument("--n-way", type=int, default=3)
    parser.add_argument("--shots", type=int, default=5)
    parser.add_argument("--queries", type=int, default=10)
    parser.add_argument("--seed", type=int, default=1000, help="First episode seed")
    parser.add_argument("--split-seed", type=int, default=42)
    args = parser.parse_args()
    try:
        report = evaluate_core(
            args.artifact, EpisodeConfig(args.n_way, args.shots, args.queries), args.episodes,
            SeedConfig(split=args.split_seed, episode=args.seed),
        )
        save_json(args.output, report)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Evaluation failed: {error}\n")
    print(json.dumps(report["summary"], indent=2))
    print(f"Evidence: {args.output}")


if __name__ == "__main__":
    main()
