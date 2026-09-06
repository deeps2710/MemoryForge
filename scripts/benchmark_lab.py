"""Measure CPU lab operations and Streamlit reruns; neither includes browser paint."""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from streamlit.testing.v1 import AppTest

from src.config import ROOT
from src.lab import LabSession, load_lab_resources
from src.reproducibility import environment_info, save_json


def summarize(values: list[float]) -> dict:
    return {"samples_ms": values, "median_ms": float(np.median(values)), "p95_ms": float(np.percentile(values, 95)), "max_ms": max(values)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "phase2_latency.json")
    args = parser.parse_args()
    load_start = perf_counter()
    resources = load_lab_resources()
    load_ms = (perf_counter() - load_start) * 1000
    timings = {name: [] for name in ("teach", "query", "conflict", "clear", "shots", "new_episode")}
    for i in range(30):
        for name in timings:
            lab = LabSession(resources, seed=1000 + i)
            operation = {"teach": lab.teach_round, "query": lab.next_query, "conflict": lab.inject_conflict, "clear": lab.clear,
                         "shots": lambda: lab.set_shots(10), "new_episode": lambda: LabSession(resources, seed=1001 + i)}[name]
            start = perf_counter()
            result = operation()
            (result if isinstance(result, LabSession) else lab).state_view()
            timings[name].append((perf_counter() - start) * 1000)
    start = perf_counter()
    app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
    initial_app_ms = (perf_counter() - start) * 1000
    if app.exception or app.error:
        raise RuntimeError("Initial app run failed")
    ui_times = {name: [] for name in ("clear", "teach", "query", "conflict", "new")}
    for _ in range(10):
        for name in ui_times:
            start = perf_counter()
            app.button(key=name).click().run()
            if app.exception or app.error:
                raise RuntimeError(f"App rerun failed: {name}")
            ui_times[name].append((perf_counter() - start) * 1000)
    result = {
        "measured_at_utc": datetime.now(timezone.utc).isoformat(), "environment": environment_info(),
        "resource_load_after_imports_ms": load_ms, "initial_apptest_run_ms": initial_app_ms,
        "core_operations_including_view": {k: summarize(v) for k, v in timings.items()},
        "streamlit_apptest_reruns": {k: summarize(v) for k, v in ui_times.items()},
        "limitations": "Local Windows CPU measurements. Resource load excludes process/import startup. AppTest reruns exclude network transport and browser rendering. No universal latency guarantee.",
    }
    save_json(args.output, result)
    print(f"Resource load after imports: {load_ms:.2f} ms; initial AppTest run: {initial_app_ms:.2f} ms")
    for section in ("core_operations_including_view", "streamlit_apptest_reruns"):
        for name, stats in result[section].items():
            print(f'{section}/{name}: median {stats["median_ms"]:.2f} ms, p95 {stats["p95_ms"]:.2f} ms, max {stats["max_ms"]:.2f} ms')
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
