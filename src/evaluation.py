"""Deterministic real-computation evidence for frozen weights and temporary memory."""

from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
import torch

from src.config import DEFAULT_ARTIFACT, EpisodeConfig, SeedConfig, require_int
from src.data import DigitsData, load_digits_data
from src.encoder import (
    DigitEncoder, assert_frozen, embed, load_encoder, parameter_delta,
    parameter_snapshot, parameters_equal, validate_checkpoint_data,
)
from src.episodes import generate_episode
from src.fast_memory import FastMemory, QueryResult
from src.reproducibility import environment_info, seed_everything, tensor_digest


def _result_record(result: QueryResult, truth: np.ndarray) -> dict[str, Any]:
    record = result.as_dict()
    correct = result.predictions.numpy() == truth
    record.update({"correct": correct.tolist(), "accuracy": float(correct.mean())})
    return record


def run_episode(
    encoder: DigitEncoder, data: DigitsData, config: EpisodeConfig, seed: int,
) -> dict[str, Any]:
    """Write support only; query disjoint rows; append one conflict; then clear.

    Caller must pair encoder and data via validate_checkpoint_data (evaluate_core
    does so). No head or optimizer is accessible on this path.
    """
    assert_frozen(encoder)
    before_parameters = parameter_snapshot(encoder)
    episode = generate_episode(**asdict(config), seed=seed, data=data)
    support_keys = embed(encoder, episode.support_images)
    query_keys = embed(encoder, episode.query_images)
    memory = FastMemory(encoder.embedding_dim, config.n_way)
    empty_state = memory.state_snapshot()
    empty_result = memory.query(query_keys)
    values = torch.nn.functional.one_hot(torch.from_numpy(episode.support_labels), config.n_way)
    memory.write_batch(support_keys, values)
    clean_state = memory.state_snapshot()
    clean_result = memory.query(query_keys)
    clean_delta = memory.memory_delta(empty_state)
    clean_stats = memory.statistics()

    # Conflict uses a support key, never a query key, preserving ground truth.
    original_label = int(episode.support_labels[0])
    wrong_label = (original_label + 1) % config.n_way
    wrong_value = torch.nn.functional.one_hot(torch.tensor(wrong_label), config.n_way)
    memory.write(support_keys[0], wrong_value)
    conflict_result = memory.query(query_keys)
    conflict_state = memory.state_snapshot()
    conflict_delta = memory.memory_delta(clean_state)
    conflict_stats = memory.statistics()
    memory.reset()
    reset_result = memory.query(query_keys)
    reset_stats = memory.statistics()
    delta = parameter_delta(encoder, before_parameters)
    identical = parameters_equal(encoder, before_parameters)
    if not identical or delta != 0:
        raise RuntimeError("Frozen encoder parameters changed during memory adaptation")
    assert_frozen(encoder)

    return {
        "episode": episode.description(), "chance": 1 / config.n_way,
        "encoder_parameter_delta": delta, "encoder_parameters_equal": identical,
        "support_keys": support_keys.tolist(), "query_keys": query_keys.tolist(),
        "empty": {"query": _result_record(empty_result, episode.query_labels), "state": empty_state.as_dict()},
        "clean": {
            "query": _result_record(clean_result, episode.query_labels), "state": clean_state.as_dict(),
            "statistics": clean_stats, "memory_delta_from_empty": clean_delta,
        },
        "conflict": {
            "support_id": int(episode.support_ids[0]), "original_label": original_label,
            "injected_wrong_label": wrong_label, "writes_added": 1,
            "query": _result_record(conflict_result, episode.query_labels), "state": conflict_state.as_dict(),
            "statistics": conflict_stats, "memory_delta_from_clean": conflict_delta,
            "scores_delta_l2": float(torch.linalg.vector_norm(conflict_result.scores - clean_result.scores)),
            "predictions_changed": int((conflict_result.predictions != clean_result.predictions).sum()),
        },
        "reset": {"query": _result_record(reset_result, episode.query_labels), "statistics": reset_stats},
    }


def evaluate_core(
    artifact_path: str | Path = DEFAULT_ARTIFACT,
    config: EpisodeConfig = EpisodeConfig(), episodes: int = 50,
    seeds: SeedConfig = SeedConfig(),
) -> dict[str, Any]:
    require_int("episodes", episodes, 1)
    require_int("last episode seed", seeds.episode + episodes - 1, 0, 2**32 - 1)
    seed_everything(seeds)
    encoder, checkpoint = load_encoder(artifact_path)
    data = load_digits_data(checkpoint["data"]["split_seed"], checkpoint["data"]["test_size"])
    validate_checkpoint_data(checkpoint, data)
    if seeds.split != data.metadata["split_seed"]:
        raise ValueError("Evaluation split seed must match the trained checkpoint")
    records = [run_episode(encoder, data, config, seeds.episode + i) for i in range(episodes)]
    accuracies = np.asarray([r["clean"]["query"]["accuracy"] for r in records])
    conflict_accuracies = np.asarray([r["conflict"]["query"]["accuracy"] for r in records])
    summary = {
        "episodes": episodes, "queries_total": episodes * config.n_way * config.queries_per_class,
        "mean_accuracy": float(accuracies.mean()), "std_accuracy_population": float(accuracies.std(ddof=0)),
        "chance": 1 / config.n_way, "margin_over_chance": float(accuracies.mean() - 1 / config.n_way),
        "min_episode_accuracy": float(accuracies.min()), "max_episode_accuracy": float(accuracies.max()),
        "encoder_parameter_delta_max": max(r["encoder_parameter_delta"] for r in records),
        "all_encoder_parameters_equal": all(r["encoder_parameters_equal"] for r in records),
        "memory_delta_min": min(r["clean"]["memory_delta_from_empty"] for r in records),
        "memory_delta_mean": float(np.mean([r["clean"]["memory_delta_from_empty"] for r in records])),
        "conflict_mean_accuracy": float(conflict_accuracies.mean()),
        "conflict_mean_accuracy_change": float((conflict_accuracies - accuracies).mean()),
        "conflict_predictions_changed": sum(r["conflict"]["predictions_changed"] for r in records),
        "conflict_memory_delta_min": min(r["conflict"]["memory_delta_from_clean"] for r in records),
        "reset_all_empty": all(r["reset"]["statistics"]["writes"] == 0 and not r["reset"]["query"]["has_memory"] for r in records),
    }
    return {
        "format_version": 1, "config": asdict(config), "seeds": asdict(seeds),
        "training_seeds": checkpoint["training_report"]["seeds"], "environment": environment_info(),
        "encoder_sha256": tensor_digest(*encoder.state_dict().values()), "data": data.metadata,
        "encoder_heldout_classification_accuracy": checkpoint["training_report"]["heldout_classification_accuracy"],
        "protocol": "Fixed held-out pool; disjoint support/query per episode. Episodes may reuse rows. No tuning on evaluation outcomes.",
        "score_interpretation": "Class-mean unit-key dot products; softmax display scores are not calibrated probabilities.",
        "summary": summary, "episodes": records,
    }
