import numpy as np
import pytest
import torch

from src.lab import LabSession, MAX_SHOTS, load_lab_resources


@pytest.fixture(scope="module")
def resources(trained_artifact):
    return load_lab_resources(trained_artifact)


def test_preset_is_real_and_images_are_heldout(resources):
    lab = LabSession(resources)
    view = lab.state_view()
    assert view["shots"] == 1 and view["statistics"]["writes"] == 3
    assert view["memory_delta"] > 0 and view["encoder_delta"] == 0
    assert view["prediction"] == int(lab.memory.query(lab.query_keys[lab.query_position]).predictions[0])
    assert view["truth"] == lab.episode.query_labels[lab.query_position]
    assert not set(lab.episode.support_ids) & set(lab.episode.query_ids)
    assert not set(lab.episode.support_ids) & set(resources.data.train_ids)
    assert not set(lab.episode.query_ids) & set(resources.data.train_ids)
    with pytest.raises(KeyError):
        resources.keys(resources.data.train_ids[:1])


def test_shots_use_nested_support_and_unchanged_queries(resources):
    lab = LabSession(resources)
    original_query_ids = lab.episode.query_ids.copy()
    original_mapping = lab.episode.digit_to_label.copy()
    one_shot = {w["sample_id"] for w in lab.last_transition.writes}
    lab.set_shots(5)
    five_shot = {w["sample_id"] for w in lab.last_transition.writes}
    assert one_shot < five_shot and len(five_shot) == 15
    assert np.array_equal(original_query_ids, lab.episode.query_ids)
    assert original_mapping == lab.episode.digit_to_label
    assert lab.shot_accuracies[5] == lab.accuracy()
    lab.set_shots(1)
    assert {w["sample_id"] for w in lab.last_transition.writes} == one_shot


def test_teach_writes_three_actual_embeddings_without_gradients(resources):
    lab = LabSession(resources)
    before = lab.memory.state_snapshot()
    lab.teach_round()
    assert lab.shots == 2 and lab.memory.statistics()["writes"] == 6
    assert lab.memory.memory_delta(before) > 0
    assert len(lab.last_transition.writes) == 3
    for write in lab.last_transition.writes:
        assert sum(write["value"]) == 1
        key = torch.tensor(write["key"], dtype=torch.float32)
        assert torch.equal(key, lab.support_keys[write["support_position"]])
    assert lab.audit() == 0


def test_conflict_reset_and_reteach(resources):
    lab = LabSession(resources)
    truth = lab.episode.query_labels.copy()
    for count in range(1, 4):
        lab.inject_conflict()
        transition = lab.last_transition
        assert lab.conflicts == count and lab.memory.statistics()["writes"] == 3 + count
        assert not torch.equal(transition.before.matrix, transition.after.matrix)
        assert not torch.equal(transition.before_query.scores, transition.after_query.scores)
        assert transition.writes[0]["true_label"] != transition.writes[0]["written_label"]
        assert np.array_equal(truth, lab.episode.query_labels)
    lab.clear()
    lab.clear()
    assert lab.shots == lab.conflicts == lab.memory.statistics()["writes"] == 0
    assert lab.state_view()["prediction"] == -1
    assert lab.state_view()["memory_delta"] == 0
    assert lab.audit() == 0
    lab.teach_round()
    assert lab.shots == 1 and lab.state_view()["prediction"] >= 0


def test_change_shots_clears_conflicts_but_preserves_evidence(resources):
    lab = LabSession(resources)
    lab.inject_conflict()
    conflict_state = lab.snapshots["After conflict"].as_dict()
    lab.set_shots(3)
    assert lab.conflicts == 0 and lab.memory.statistics()["writes"] == 9
    assert lab.snapshots["After conflict"].as_dict() == conflict_state


def test_queries_never_write_and_cycle_through_distinct_rows(resources):
    lab = LabSession(resources)
    before = lab.memory.state_snapshot().as_dict()
    seen = set()
    for _ in range(30):
        seen.add(lab.state_view()["query_id"])
        lab.next_query()
    assert len(seen) == 30 and lab.query_cursor == 0
    assert lab.memory.state_snapshot().as_dict() == before
    assert lab.audit() == 0


def test_sessions_share_only_frozen_resources(resources):
    first, second = LabSession(resources), LabSession(resources)
    before = second.memory.state_snapshot().as_dict()
    first.inject_conflict()
    first.clear()
    assert second.memory.state_snapshot().as_dict() == before
    assert second.shots == 1 and second.conflicts == 0
    other = LabSession(resources, seed=1001)
    assert other.episode.description() != second.episode.description()
    assert other.memory.statistics()["writes"] == 3


def test_seed_replay_and_clean_shots_path_agree(resources):
    first, second = LabSession(resources), LabSession(resources)
    first.teach_round()
    first.teach_round()
    second.set_shots(3)
    assert first.episode.description() == second.episode.description()
    assert first.memory.state_snapshot().as_dict() == second.memory.state_snapshot().as_dict()


@pytest.mark.parametrize("shots", [-1, 11, True, 2.5])
def test_invalid_shots_rejected_without_mutation(resources, shots):
    lab = LabSession(resources)
    before = lab.memory.state_snapshot().as_dict()
    with pytest.raises(ValueError):
        lab.set_shots(shots)
    assert before == lab.memory.state_snapshot().as_dict()


def test_empty_conflict_and_exhausted_teaching_are_rejected(resources):
    lab = LabSession(resources, preset_shots=0)
    with pytest.raises(ValueError, match="Teach"):
        lab.inject_conflict()
    lab.set_shots(MAX_SHOTS)
    with pytest.raises(ValueError, match="already taught"):
        lab.teach_round()


def test_encoder_corruption_is_detected_before_a_write(trained_artifact):
    resources = load_lab_resources(trained_artifact)
    lab = LabSession(resources)
    before = lab.memory.state_snapshot().as_dict()
    with torch.no_grad():
        next(resources.encoder.parameters()).flatten()[0] += 0.1
    with pytest.raises(RuntimeError, match="integrity"):
        lab.teach_round()
    assert before == lab.memory.state_snapshot().as_dict()
