"""Paired, deterministic shot/conflict experiments using the real lab engine."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path

import numpy as np

from src.config import ROOT, require_int
from src.lab import LabResources, LabSession, MAX_SHOTS
from src.reproducibility import environment_info

DEFAULT_EVIDENCE = ROOT / "artifacts" / "phase3_evidence.json"


def report_digest(report: dict) -> str:
    return hashlib.sha256(json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def summarize(episodes: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for episode in episodes:
        for row in episode["conditions"]:
            groups[(row["shots"], row["conflicts"])].append(row)
    result = []
    for (shots, conflicts), rows in sorted(groups.items()):
        accuracies = np.array([row["accuracy"] for row in rows])
        result.append({
            "shots": shots, "conflicts": conflicts, "episodes": len(rows),
            "queries_total": sum(len(row["predictions"]) for row in rows),
            "mean_accuracy": float(accuracies.mean()),
            "std_accuracy_population": float(accuracies.std(ddof=0)),
            "mean_accuracy_change_from_clean": float(np.mean([r["accuracy_change_from_clean"] for r in rows])),
            "predictions_changed": sum(r["predictions_changed_from_clean"] for r in rows),
            "memory_delta_min": min(r["memory_delta"] for r in rows),
            "mean_memory_delta": float(np.mean([r["memory_delta"] for r in rows])),
            "mean_conflict_memory_delta": float(np.mean([r["conflict_memory_delta"] for r in rows])),
            "encoder_parameter_delta_max": max(r["encoder_delta"] for r in rows),
            "all_encoder_parameters_equal": all(r["encoder_parameters_equal"] for r in rows),
            "chance": 1 / 3,
        })
    return result


def evaluate_suite(resources: LabResources, seeds=range(1000, 1050),
                   shots=(0, 1, 2, 5, 10), conflicts=(0, 1, 3)) -> dict:
    seeds, shots, conflicts = list(seeds), list(shots), list(conflicts)
    for name, values, maximum in (("seed", seeds, 2**32-1), ("shots", shots, MAX_SHOTS), ("conflicts", conflicts, 100)):
        if not values or len(set(values)) != len(values):
            raise ValueError(f"{name} must be a nonempty unique sequence")
        for value in values:
            require_int(name, value, 0, maximum)
    if 0 not in conflicts:
        raise ValueError("Include zero conflicts for a paired clean baseline")
    episodes = []
    for seed in seeds:
        lab = LabSession(resources, seed=seed, preset_shots=0)
        conditions = []
        for count in sorted(shots):
            lab.set_shots(count)
            clean = lab.query_all()
            clean_memory = lab.memory.state_snapshot()
            clean_accuracy = lab.accuracy(clean)
            for n_conflicts in sorted(conflicts):
                if count == 0 and n_conflicts:
                    continue  # No taught support exists to corrupt.
                while lab.conflicts < n_conflicts:
                    lab.inject_conflict()
                view = lab.state_view()
                query = view["query_result"]
                conditions.append({
                    "shots": count, "conflicts": n_conflicts,
                    "support_positions": lab.support_grid[:, :count].T.flatten().tolist(),
                    "corrupt_support_position": 0 if n_conflicts else None,
                    "corrupt_written_label": (int(lab.episode.support_labels[0]) + 1) % 3 if n_conflicts else None,
                    "memory": lab.memory.state_snapshot().as_dict(),
                    "scores": query.scores.tolist(), "predictions": query.predictions.tolist(),
                    "ties": query.ties.tolist(), "has_memory": query.has_memory,
                    "accuracy": view["accuracy"],
                    "accuracy_change_from_clean": view["accuracy"] - clean_accuracy,
                    "predictions_changed_from_clean": int((query.predictions != clean.predictions).sum()),
                    "memory_delta": view["memory_delta"],
                    "conflict_memory_delta": lab.memory.memory_delta(clean_memory),
                    "encoder_delta": view["encoder_delta"],
                    "encoder_parameters_equal": view["encoder_parameters_equal"],
                })
        lab.clear()
        episodes.append({
            "episode": lab.episode.description(),
            "support_keys": lab.support_keys.tolist(), "query_keys": lab.query_keys.tolist(),
            "conditions": conditions,
            "reset": {"writes": lab.memory.statistics()["writes"],
                      "memory_delta": lab.state_view()["memory_delta"], "encoder_delta": lab.audit()},
        })
    return {
        "schema_version": 1, "environment": environment_info(),
        "encoder_sha256": resources.encoder_sha256,
        "dataset_fingerprint": resources.data.metadata["fingerprint_sha256"],
        "protocol": {
            "seeds": seeds, "shots": sorted(shots), "conflicts": sorted(conflicts),
            "n_way": 3, "support_pool_per_class": 10, "queries_per_class": 10,
            "corruption": "Append the first taught key under the next cyclic label for each configured conflict count; original truth unchanged.",
            "pairing": "Same mapping, nested support prefixes and identical 30 queries within each seed.",
            "zero_shots": "Only the clean abstention condition; no corruption without demonstrations.",
            "scope": "Descriptive fixed-seed evidence, no tuning; episodes may reuse held-out images. Not independent datasets.",
        },
        "episodes": episodes, "summary": summarize(episodes),
    }


def load_evidence(path: str | Path = DEFAULT_EVIDENCE) -> dict:
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    if report.get("schema_version") != 1 or not report.get("episodes"):
        raise ValueError("Unsupported or empty evidence report")
    if summarize(report["episodes"]) != report["summary"]:
        raise ValueError("Evidence summary disagrees with recorded observations")
    return report
