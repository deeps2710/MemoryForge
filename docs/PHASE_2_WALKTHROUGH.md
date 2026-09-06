# Phase 2 browser verification

Verified by Codex through the local browser, 2026-09-07. This records actual UI
observations; it is not a human learner study or public deployment check.

| Step | Observed outcome |
|---|---|
| Start/reload local app | Real seed 1000 preset, 3 writes, ALPHA beside ALPHA truth; 23/30 (76.7%) |
| Teach demonstrations | 6 writes, 2 shots/class, 27/30 (90.0%), encoder delta 0 |
| Test Query | Different held-out image, no extra write; displayed truth GAMMA |
| Inject Conflict | Actual digit 1 → BETA despite ALPHA truth; 7 writes, 90.0% → 86.7%; 5/30 predictions changed; score delta about 0.55931 |
| Clear Memory | 0 writes, zero current matrix/delta, Abstaining; encoder delta 0; conflict disabled |
| Teach after clear | 3 actual writes restored |
| Playground keyboard arrows | Shot counts changed through intermediate values to 10; 30 writes; Teach disabled at cap |
| New Episode | Seed 1001; 3 fresh writes, no conflicts; BETA prediction beside BETA truth |
| Slider to zero | Abstaining, zero writes, Inject Conflict disabled |
| Quiz wrong answer | Immediate explanation that memory changed while encoder tensors stayed unchanged |
| Quiz correct answer | Immediate Correct feedback |
| Return to lab | Seed 1001 zero-shot/abstaining state preserved |
| Final reload | Fresh seed 1000 real preset restored |

Automated AppTest additionally covers all three quiz questions and both outcomes,
repeat conflicts, repeated reset, missing weights, independent sessions, reload,
fixed query IDs under shot changes, and exact current/historical chart payloads.

## Visual and interaction checks

Desktop screenshots were reviewed at 1280×720 and the app's available desktop
viewport. Main actions, frozen-state panel, labelled images, raw-score bars and
heatmap were inspected. Numeric matrix/score alternatives are available in
expanders. After fixing chart margins, all class labels and scales were visible.

At 390×844, controls wrap, metrics stack and both main panels occupy approximately
353 px each in a single column. The document width was 390 px (no page overflow).
The memory heatmap, rotated dimension labels, query image, prediction and truth
were visually inspected. The sidebar can collapse to reveal the full content.
Native arrow keys changed shots; the quiz and navigation preserve the experiment.
The temporary viewport override was reset after testing.

Earlier failures corrected before sign-off: a third nested Streamlit column level,
clipped Plotly margins and a CSS selector that initially failed to stack the
main panels on mobile. No claim of complete screen-reader/WCAG certification is
made; that would require broader assistive-technology testing.

## Local feedback observations

Measured click-to-visible-result observations for Teach, Test Query and Inject
Conflict were 443, 335 and 338 ms respectively. These three observations include
browser automation overhead and are not a distribution or deployment guarantee.
The repeatable benchmark records 30 CPU samples/action and 10 AppTest
samples/action in `artifacts/phase2_latency.json`; those scopes exclude browser
rendering/network. See the Phase 2 report for the final summary.
