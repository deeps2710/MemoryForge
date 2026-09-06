"""Replay the Phase 2 preset and save real states, writes and predictions."""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import ROOT
from src.lab import LabSession, load_lab_resources
from src.reproducibility import save_json


def record(lab: LabSession, action: str) -> dict:
    view = lab.state_view()
    view["query_result"] = view["query_result"].as_dict()
    del view["last_action_ms"]  # Timing has its own measured artifact.
    transition = lab.last_transition
    return {
        "action": action, "view": view,
        "memory": lab.memory.state_snapshot().as_dict(),
        "writes": list(transition.writes) if transition and action != "query" else [],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "phase2_demo.json")
    args = parser.parse_args()
    lab = LabSession(load_lab_resources())
    records = [record(lab, "preset")]
    for action, operation in (
        ("teach", lab.teach_round), ("query", lab.next_query),
        ("conflict", lab.inject_conflict), ("clear", lab.clear),
        ("five_shots", lambda: lab.set_shots(5)),
        ("ten_shots", lambda: lab.set_shots(10)),
    ):
        operation()
        records.append(record(lab, action))
    save_json(args.output, {
        "protocol": "Phase 2: seed 1000, fixed 10-support/class pool, 30 disjoint fixed queries; nested support prefixes. Different sampling from the Phase 1 five-shot benchmark.",
        "encoder_sha256": lab.resources.encoder_sha256,
        "episode": lab.episode.description(),
        "query_truth": lab.episode.query_labels.tolist(),
        "records": records,
    })
    for item in records:
        view = item["view"]
        print(f'{item["action"]}: writes={view["statistics"]["writes"]}, accuracy={view["accuracy"]:.6f}, encoder_delta={view["encoder_delta"]}, memory_delta={view["memory_delta"]:.6f}')
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
