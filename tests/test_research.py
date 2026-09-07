"""Verify citations, mathematical inspection and live research-page integration."""
from datetime import date
import json
import socket

import numpy as np
import pytest
import torch
from streamlit.testing.v1 import AppTest

from src.config import ROOT
from src.evidence import DEFAULT_EVIDENCE, load_evidence
from src.lab import LabSession, load_lab_resources
from src.research import evidence_figure, sources, write_decomposition


def test_primary_sources_have_version_dates_evidence_and_limits():
    catalog = sources()
    papers = [s for s in catalog.values() if s["qualifying_paper"]]
    assert len(papers) >= 3
    for item in papers:
        assert 2022 <= date.fromisoformat(item["first_public_date"]).year <= 2026
        assert item["reviewed_version"].startswith("arXiv:") and "v" in item["reviewed_version"]
        assert item["url"].startswith("https://arxiv.org/abs/")
        assert all(item[k] for k in ("authors","claim","locator","limits","evidence_type"))
    assert catalog["titans"]["first_public_date"] == "2024-12-31"
    assert "proprietary" in catalog["bdh-cq"]["limits"]


def test_derivation_matches_real_float64_normalized_memory(trained_artifact):
    lab = LabSession(load_lab_resources(trained_artifact))
    lab.teach_round()
    lab.inject_conflict()
    before = lab.memory.state_snapshot().as_dict()
    data = write_decomposition(lab, 0)
    expected = lab.memory.query(lab.query_keys[lab.query_position]).scores[0]
    torch.testing.assert_close(data["scores"], expected, rtol=0, atol=1e-14)
    torch.testing.assert_close(data["contributions"].sum(dim=1), expected, rtol=0, atol=1e-14)
    assert torch.count_nonzero(data["outer"].any(dim=1)) == 1
    assert before == lab.memory.state_snapshot().as_dict()


def test_evidence_plot_uses_saved_observations_and_population_std():
    report = load_evidence()
    fig = evidence_figure(report["summary"])
    for trace, corruption in zip(fig.data, [0,1,3]):
        rows = [r for r in report["summary"] if r["conflicts"] == corruption]
        assert list(trace.x) == [r["shots"] for r in rows]
        assert list(trace.y) == [100*r["mean_accuracy"] for r in rows]
        assert list(trace.error_y.array) == [100*r["std_accuracy_population"] for r in rows]


def test_research_navigation_preserves_memory_and_displays_sources():
    app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
    app.button(key="teach").click().run()
    before = app.session_state.lab.memory.state_snapshot().as_dict()
    app.radio(key="workspace").set_value("Research & evidence").run()
    assert not app.exception and not app.error
    assert app.title[0].value == "From a writable matrix to research"
    text = " ".join(m.value for m in app.markdown)
    for item in sources().values():
        assert item["full_text"] in text
    for answer in ("Yes","No"):
        app.radio(key="research_check").set_value(answer).run()
        assert not app.exception
    assert any("shared separation" in x.value for x in app.success)
    app.radio(key="workspace").set_value("Guided lab").run()
    assert before == app.session_state.lab.memory.state_snapshot().as_dict()


def test_evidence_page_handles_missing_report_without_running_experiments(monkeypatch, tmp_path):
    import src.research as research
    monkeypatch.setattr(research, "DEFAULT_EVIDENCE", tmp_path / "absent.json")
    app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
    app.radio(key="workspace").set_value("Research & evidence").run()
    assert not app.exception and not app.error
    assert any("Saved evidence is unavailable" in x.value for x in app.warning)


def test_offline_app_and_experiments_need_no_socket_connections(monkeypatch):
    import streamlit as st
    st.cache_resource.clear()
    st.cache_data.clear()
    attempts = []
    def deny(*args, **kwargs):
        attempts.append("connection")
        raise AssertionError("Network connection attempted in offline test")
    monkeypatch.setattr(socket.socket, "connect", deny)
    monkeypatch.setattr(socket.socket, "connect_ex", deny)
    monkeypatch.setattr(socket, "create_connection", deny)
    app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
    for action in ("teach","query","conflict","clear","teach"):
        app.button(key=action).click().run()
    app.radio(key="workspace").set_value("Research & evidence").run()
    assert not app.exception and not app.error
    assert attempts == []


def test_evidence_mismatched_encoder_is_labelled(monkeypatch):
    import src.research as research
    report = load_evidence()
    report["encoder_sha256"] = "different"
    monkeypatch.setattr(research, "cached_evidence", lambda *args: report)
    app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
    app.radio(key="workspace").set_value("Research & evidence").run()
    assert not app.exception
    assert any("different encoder" in x.value for x in app.warning)
