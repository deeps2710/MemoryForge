import numpy as np
import pytest
import torch

from scripts.smoke_test import run_smoke
from src.config import EpisodeConfig, SeedConfig
from src.encoder import parameter_delta, parameter_snapshot, parameters_equal
from src.evaluation import evaluate_core, run_episode


def test_episode_preserves_actual_parameters_and_changes_fast_state(encoder, data):
    before = parameter_snapshot(encoder)
    record = run_episode(encoder, data, EpisodeConfig(), 1000)
    assert parameters_equal(encoder, before) and parameter_delta(encoder, before) == 0
    assert record["encoder_parameters_equal"] and record["encoder_parameter_delta"] == 0
    assert record["clean"]["memory_delta_from_empty"] > 0
    assert record["empty"]["query"]["predictions"] == [-1] * 30
    assert record["reset"]["query"] == record["empty"]["query"]
    assert record["reset"]["statistics"]["writes"] == 0
    # Reconstruct the actual reported scores from recorded state and query keys.
    matrix = torch.tensor(record["clean"]["state"]["matrix"], dtype=torch.float64)
    keys = torch.tensor(record["query_keys"], dtype=torch.float64)
    normalized = keys / torch.linalg.vector_norm(keys, dim=1, keepdim=True)
    assert torch.allclose(normalized @ matrix.T, torch.tensor(record["clean"]["query"]["scores"], dtype=torch.float64))


def test_multiepisode_measured_accuracy_and_baseline(trained_artifact):
    report = evaluate_core(trained_artifact, episodes=20)
    summary = report["summary"]
    # Broad regression margin, declared explicitly as engineering health only.
    assert summary["mean_accuracy"] > summary["chance"] + 0.1
    assert summary["chance"] == 1 / 3
    assert summary["all_encoder_parameters_equal"]
    assert summary["encoder_parameter_delta_max"] == 0
    assert summary["queries_total"] == 600
    actual = []
    for record in report["episodes"]:
        truth = np.asarray(record["episode"]["query_labels"])
        predicted = np.asarray(record["clean"]["query"]["predictions"])
        measured = float((truth == predicted).mean())
        assert record["clean"]["query"]["accuracy"] == measured
        actual.append(measured)
    assert summary["mean_accuracy"] == float(np.mean(actual))


def test_conflict_uses_support_only_and_records_actual_effect(encoder, data):
    record = run_episode(encoder, data, EpisodeConfig(), 1000)
    conflict = record["conflict"]
    assert conflict["support_id"] in record["episode"]["support_ids"]
    assert conflict["support_id"] not in record["episode"]["query_ids"]
    assert conflict["original_label"] != conflict["injected_wrong_label"]
    assert conflict["memory_delta_from_clean"] > 0
    assert conflict["scores_delta_l2"] > 0
    assert conflict["statistics"]["writes"] == record["clean"]["statistics"]["writes"] + 1
    before = np.asarray(record["clean"]["query"]["predictions"])
    after = np.asarray(conflict["query"]["predictions"])
    assert conflict["predictions_changed"] == int((before != after).sum())
    # No forced decrease: actual conflict accuracy is recomputed against original truth.
    assert conflict["query"]["accuracy"] == float((after == record["episode"]["query_labels"]).mean())


def test_end_to_end_smoke(trained_artifact):
    result = run_smoke(trained_artifact)
    assert result["status"] == "PASS" and all(result["checks"].values())


def test_new_episode_has_fresh_memory(encoder, data):
    a = run_episode(encoder, data, EpisodeConfig(), 1000)
    b = run_episode(encoder, data, EpisodeConfig(), 1001)
    assert a["empty"]["state"] == b["empty"]["state"]
    assert b["clean"]["statistics"]["writes"] == 15


def test_wrong_split_seed_and_empty_evaluation_rejected(trained_artifact):
    with pytest.raises(ValueError, match="split seed"):
        evaluate_core(trained_artifact, seeds=SeedConfig(split=99), episodes=1)
    with pytest.raises(ValueError, match="episodes"):
        evaluate_core(trained_artifact, episodes=0)
