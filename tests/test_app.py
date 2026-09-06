"""Exercise rendered Streamlit state and user controls, not just callback internals."""

import json

import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

from src.config import ROOT
from src.learning import QUIZ


def start_app() -> AppTest:
    return AppTest.from_file(ROOT / "app.py", default_timeout=20).run()


def assert_healthy(app: AppTest) -> None:
    assert not app.exception, [item.value for item in app.exception]
    assert not app.error, [item.value for item in app.error]


def metrics(app: AppTest) -> dict:
    return {item.label: item.value for item in app.metric}


def test_app_opens_on_real_preset_with_truth_and_deltas(monkeypatch):
    import src.training
    monkeypatch.setattr(src.training, "train_encoder", lambda *a, **k: pytest.fail("UI must not train"))
    app = start_app()
    assert_healthy(app)
    lab = app.session_state.lab
    assert "Same neural weights" in app.title[0].value
    assert "without changing its neural-network weights" in " ".join(x.value for x in app.markdown)
    values = metrics(app)
    assert values["Encoder parameter delta"] == "0"
    assert float(values["Fast-memory delta"]) > 0
    assert values["Actual memory writes"] == "3"
    view = lab.state_view()
    assert values["Prediction"] == lab.episode.label_names[view["prediction"]]
    assert values["Ground truth"] == lab.episode.label_names[view["truth"]]


def test_buttons_teach_query_conflict_clear_and_reteach():
    app = start_app()
    original_id = app.session_state.lab.state_view()["query_id"]
    app.button(key="teach").click().run()
    assert_healthy(app)
    assert metrics(app)["Actual memory writes"] == "6"
    app.button(key="query").click().run()
    assert app.session_state.lab.state_view()["query_id"] != original_id
    assert metrics(app)["Actual memory writes"] == "6"
    for _ in range(3):
        app.button(key="conflict").click().run()
        assert_healthy(app)
    assert metrics(app)["Actual memory writes"] == "9"
    assert any("Conflicting write" in warning.value for warning in app.warning)
    app.button(key="clear").click().run()
    assert_healthy(app)
    assert metrics(app)["Prediction"] == "Abstaining"
    assert metrics(app)["Fast-memory delta"] == "0.00000"
    assert app.button(key="conflict").disabled
    app.button(key="clear").click().run()
    app.button(key="teach").click().run()
    assert_healthy(app)
    assert metrics(app)["Actual memory writes"] == "3"
    assert not app.button(key="conflict").disabled


def test_playground_slider_preserves_queries_and_clears_conflicts():
    app = start_app()
    before_ids = app.session_state.lab.episode.query_ids.copy()
    app.radio(key="workspace").set_value("Playground").run()
    app.button(key="conflict").click().run()
    app.slider(key="shots_slider").set_value(5).run()
    assert_healthy(app)
    assert metrics(app)["Actual memory writes"] == "15"
    assert app.session_state.lab.conflicts == 0
    assert np.array_equal(before_ids, app.session_state.lab.episode.query_ids)
    app.slider(key="shots_slider").set_value(10).run()
    assert app.button(key="teach").disabled
    app.slider(key="shots_slider").set_value(0).run()
    assert metrics(app)["Prediction"] == "Abstaining"
    app.button(key="teach").click().run()
    assert app.slider(key="shots_slider").value == 1


def test_new_episode_does_not_keep_old_memory_or_conflicts():
    app = start_app()
    original = app.session_state.lab.episode.description()
    app.button(key="conflict").click().run()
    app.button(key="new").click().run()
    assert_healthy(app)
    lab = app.session_state.lab
    assert lab.seed == 1001 and lab.conflicts == 0 and lab.shots == 1
    assert lab.episode.description() != original
    assert metrics(app)["Actual memory writes"] == "3"
    assert "After conflict" not in lab.snapshots


def test_chart_payloads_match_actual_current_and_historical_matrices():
    app = start_app()
    app.button(key="teach").click().run()
    for label in ["Current", "Before teaching", "Before latest action", "After teaching"]:
        app.selectbox(key="matrix_view").select(label).run()
        assert_healthy(app)
        chart = json.loads(app.get("plotly_chart")[0].proto.spec)
        lab = app.session_state.lab
        snapshot = lab.memory.state_snapshot() if label == "Current" else lab.snapshots[label]
        assert np.array_equal(chart["data"][0]["z"], snapshot.matrix.numpy())
    app.button(key="clear").click().run()
    assert app.selectbox(key="matrix_view").value == "Current"
    chart = json.loads(app.get("plotly_chart")[0].proto.spec)
    assert np.count_nonzero(chart["data"][0]["z"]) == 0


def test_rendered_score_chart_and_table_agree_with_query():
    app = start_app()
    app.button(key="query").click().run()
    view = app.session_state.lab.state_view()
    expected = view["query_result"].scores[view["query_position"]].tolist()
    chart = json.loads(app.get("plotly_chart")[1].proto.spec)
    assert chart["data"][0]["x"] == expected
    assert app.table[0].value["Raw score"].tolist() == expected


def test_quiz_feedback_and_return_preserve_experiment():
    app = start_app()
    app.button(key="teach").click().run()
    before = app.session_state.lab.memory.state_snapshot().as_dict()
    app.radio(key="workspace").set_value("60-second check").run()
    assert_healthy(app)
    assert app.title[0].value == "What actually learned?"
    for i, question in enumerate(QUIZ):
        wrong = next(option for option in question["options"] if option != question["answer"])
        app.radio(key=f"quiz_{i}").set_value(wrong).run()
        assert any("Try that reasoning again" in info.value for info in app.info)
        app.radio(key=f"quiz_{i}").set_value(question["answer"]).run()
    assert len(app.success) == 3
    app.radio(key="workspace").set_value("Guided lab").run()
    assert before == app.session_state.lab.memory.state_snapshot().as_dict()


def test_rerun_preserves_state_and_fresh_session_resets():
    app = start_app()
    app.button(key="teach").click().run()
    before = app.session_state.lab.memory.state_snapshot().as_dict()
    app.run()
    assert before == app.session_state.lab.memory.state_snapshot().as_dict()
    fresh = start_app()
    assert_healthy(fresh)
    assert fresh.session_state.lab.shots == 1
    fresh.button(key="clear").click().run()
    assert before == app.session_state.lab.memory.state_snapshot().as_dict()


def test_missing_artifact_shows_actionable_message_without_training(monkeypatch, tmp_path):
    import src.config
    monkeypatch.setattr(src.config, "DEFAULT_ARTIFACT", tmp_path / "missing.pt")
    app = start_app()
    assert not app.exception
    assert any("python scripts/train_encoder.py" in error.value for error in app.error)
    assert not app.button
