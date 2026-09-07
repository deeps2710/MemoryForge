"""Independently reconstruct every reported score from recorded keys and labels."""
import copy
import json

import numpy as np
import pytest

from src.evidence import evaluate_suite, load_evidence, report_digest, summarize
from src.lab import load_lab_resources
from src.reproducibility import save_json


@pytest.fixture(scope="module")
def suite(trained_artifact):
    return evaluate_suite(load_lab_resources(trained_artifact),
                          seeds=[0, 1000, 2**32-1], shots=[0, 1, 5, 10], conflicts=[0, 1, 3])


def test_raw_evidence_independently_reconstructs_memory_queries_and_deltas(suite):
    for episode in suite["episodes"]:
        description = episode["episode"]
        supports = np.array(episode["support_keys"], dtype=np.float64)
        supports /= np.linalg.norm(supports, axis=1, keepdims=True)
        queries = np.array(episode["query_keys"], dtype=np.float64)
        queries /= np.linalg.norm(queries, axis=1, keepdims=True)
        truth = np.array(description["query_labels"])
        assert not set(description["support_ids"]) & set(description["query_ids"])
        clean = {}
        for row in episode["conditions"]:
            sums = np.zeros((3,16), dtype=np.float64)
            counts = np.zeros(3, dtype=np.float64)
            for pos in row["support_positions"]:
                label = description["support_labels"][pos]
                sums[label] += supports[pos]
                counts[label] += 1
            for _ in range(row["conflicts"]):
                label = row["corrupt_written_label"]
                sums[label] += supports[0]
                counts[label] += 1
            matrix = np.divide(sums, counts[:, None], out=np.zeros_like(sums), where=counts[:, None] > 0)
            scores = queries @ matrix.T
            predictions = scores.argmax(axis=1) if row["shots"] else np.full(30, -1)
            np.testing.assert_allclose(sums, row["memory"]["sums"], rtol=0, atol=1e-14)
            np.testing.assert_array_equal(counts, row["memory"]["counts"])
            np.testing.assert_allclose(matrix, row["memory"]["matrix"], rtol=0, atol=1e-14)
            np.testing.assert_allclose(scores, row["scores"], rtol=0, atol=1e-14)
            np.testing.assert_array_equal(predictions, row["predictions"])
            assert row["accuracy"] == float(np.mean(predictions == truth))
            assert row["encoder_delta"] == 0 and row["encoder_parameters_equal"]
            assert row["memory_delta"] == pytest.approx(np.linalg.norm(matrix))
            if not row["conflicts"]:
                clean[row["shots"]] = row
            base = clean[row["shots"]]
            assert row["accuracy_change_from_clean"] == row["accuracy"] - base["accuracy"]
            assert row["predictions_changed_from_clean"] == int(np.sum(predictions != base["predictions"]))
            assert row["conflict_memory_delta"] == pytest.approx(np.linalg.norm(matrix - np.array(base["memory"]["matrix"])))
        assert episode["reset"] == {"writes": 0, "memory_delta": 0, "encoder_delta": 0}


def test_summary_population_std_and_pairs_match_raw_records(suite):
    assert summarize(suite["episodes"]) == suite["summary"]
    for group in suite["summary"]:
        rows = [r for e in suite["episodes"] for r in e["conditions"]
                if (r["shots"], r["conflicts"]) == (group["shots"], group["conflicts"])]
        values = np.array([r["accuracy"] for r in rows])
        assert group["mean_accuracy"] == values.mean()
        assert group["std_accuracy_population"] == values.std(ddof=0)
        assert group["episodes"] == 3 and group["queries_total"] == 90
        assert group["chance"] == 1/3


def test_complete_suite_replays_without_timing_fields(suite, trained_artifact):
    replay = evaluate_suite(load_lab_resources(trained_artifact),
                            seeds=[0,1000,2**32-1], shots=[0,1,5,10], conflicts=[0,1,3])
    assert replay == suite
    assert report_digest(replay) == report_digest(suite)


@pytest.mark.parametrize("settings", [
    {"seeds":[]}, {"seeds":[1,1]}, {"seeds":[-1]}, {"shots":[11]},
    {"shots":[True]}, {"conflicts":[-1]}, {"conflicts":[1]}, {"shots":[]},
])
def test_invalid_suite_settings_fail_before_running(trained_artifact, settings):
    with pytest.raises(ValueError):
        evaluate_suite(load_lab_resources(trained_artifact), **settings)


def test_saved_summary_corruption_is_rejected(suite, tmp_path):
    altered = copy.deepcopy(suite)
    altered["summary"][0]["mean_accuracy"] = .5
    path = tmp_path / "bad.json"
    save_json(path, altered)
    with pytest.raises(ValueError, match="disagrees"):
        load_evidence(path)
