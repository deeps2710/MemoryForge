"""Generate and exactly replay the Phase 3 paired evidence suite."""
import argparse
from pathlib import Path
import sys
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import DEFAULT_ARTIFACT, ROOT, require_int
from src.evidence import DEFAULT_EVIDENCE, evaluate_suite, report_digest
from src.lab import load_lab_resources
from src.reproducibility import save_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--output", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--replay-output", type=Path, default=ROOT / "artifacts" / "phase3_replay.json")
    parser.add_argument("--episodes", type=int, default=50)
    parser.add_argument("--seed", type=int, default=1000)
    args = parser.parse_args()
    require_int("episodes", args.episodes, 1, 1000)
    resources = load_lab_resources(args.artifact)
    started = perf_counter()
    first = evaluate_suite(resources, seeds=range(args.seed, args.seed + args.episodes))
    elapsed = perf_counter() - started
    second = evaluate_suite(resources, seeds=range(args.seed, args.seed + args.episodes))
    if first != second:
        raise RuntimeError("Complete evidence replay differs")
    save_json(args.output, first)
    save_json(args.replay_output, {"complete_reports_equal": True, "sha256": report_digest(first),
        "episodes": args.episodes, "conditions": sum(len(e["conditions"]) for e in first["episodes"]),
        "first_run_seconds": elapsed, "timing_scope": "CPU suite after imports/resource loading; includes recording, excludes browser."})
    for row in first["summary"]:
        print(f'shots={row["shots"]}, conflicts={row["conflicts"]}: {row["mean_accuracy"]:.4%} +/- {row["std_accuracy_population"]:.4%}; encoder delta={row["encoder_parameter_delta_max"]}')
    print(f"Exact replay PASS; {elapsed:.2f}s first run; {args.output}")


if __name__ == "__main__":
    main()
