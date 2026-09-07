# PHASE 3 COMPLETION REPORT

Overall status: **PASS**. Phase 3 = **COMPLETE**. Phase 4 = **NOT STARTED**.
Verified 2026-09-07 on Windows, Python 3.12.14 and PyTorch 2.6.0+cpu.

## 1. Implemented

- Integrated Research & evidence: live episode context, BDH/BDH-CQ learning
  module, source boundaries, DeltaNet/Titans comparison and immediate check.
- Four verified recent primary papers/reports plus pinned official BDH code;
  one versioned claim ledger supplies nearby UI citations and limitations.
- Actual key/value outer-product and count-normalized retrieval derivation.
- Paired 50-seed, five-shot-count, clean/corrupted evidence, actual Plotly chart,
  numeric results and downloadable raw observations.
- Reusable evidence/replay and robustness scripts, 19 new tests, technical
  ownership walkthrough, updated limitations, provenance and phase records.

## 2. Architecture decisions

The existing encoder, memory rule, data split and lab session protocol remain
unchanged. The new research layer inspects live state without writing to it.
It derives S += v k^T, counts c += v and M[i] = S[i]/c[i], then scores = Mq.
It matches the memory's float64 re-normalization of input keys and queries.

Evidence fixes each seed's mapping, 10-support/class pool and 30 held-out
queries, then compares nested clean prefixes with 0, 1 or 3 appended wrong-label
writes. Timing is outside the deterministic report. Only loaded evidence and
frozen resources are cached globally; temporary memory stays session-local.
Summary disagreement or a mismatched live encoder produces an explicit warning.

Published claims are separated from local measurements. BDH-CQ's proprietary
updates/dimensions are not inferred, and its latent workspace is not implemented.
Titans' memory-parameter updates do not imply that all test-time learners freeze
every parameter. Details and alternatives are in PROJECT_DECISIONS.md.

## 3. Files created/modified

Created: src/evidence.py, src/research.py; scripts/evaluate_suite.py and
verify_robustness.py; tests/test_evidence.py and test_research.py;
artifacts/phase3_{evidence,replay,robustness,verification}.json;
docs/research_sources.json, TECHNICAL_WALKTHROUGH.md, PHASE_3_WALKTHROUGH.md and
this report.

Updated: app.py, src/ui.py, README.md, docs/ARCHITECTURE.md,
PROJECT_DECISIONS.md, REQUIREMENTS_MATRIX.md, PHASE_STATUS.md, LIMITATIONS.md,
PROVENANCE.md, RESEARCH_NOTES.md, AI_ASSISTANCE.md and FUTURE_ROADMAP.md.
Earlier ML modules, tests, checkpoint, evidence, dependency pins and the unrelated
html file are preserved. Local environments/logs remain ignored under .local.

## 4. ML verification

Every condition has 30 queries. Each table row aggregates 50 episode accuracies.
Deviation is population standard deviation (ddof=0); pp means percentage points.
Changed predictions are paired against the same seed/shot count's clean result.

| Clean shots/class | Extra wrong-label writes | Mean accuracy | Population deviation | Changed predictions |
|---|---:|---:|---:|---:|
| 0 | 0 | 0.00% | 0.00 pp | 0 |
| 1 | 0 | 94.07% | 6.37 pp | 0 |
| 1 | 1 | 89.73% | 9.35 pp | 104 |
| 1 | 3 | 84.47% | 11.50 pp | 189 |
| 2 | 0 | 95.67% | 5.26 pp | 0 |
| 2 | 1 | 94.87% | 6.64 pp | 40 |
| 2 | 3 | 86.87% | 11.34 pp | 168 |
| 5 | 0 | 96.93% | 4.51 pp | 0 |
| 5 | 1 | 96.60% | 5.27 pp | 17 |
| 5 | 3 | 94.20% | 7.42 pp | 55 |
| 10 | 0 | 98.07% | 2.67 pp | 0 |
| 10 | 1 | 97.80% | 3.03 pp | 8 |
| 10 | 3 | 97.27% | 3.57 pp | 22 |

There are **650 conditions and 19,500 query outcomes**. All measured encoder
deltas are **0**, all exact tensor comparisons pass, all resets are empty, and
every nonempty condition changes memory from empty (minimum norm
1.29948555). Chance is 33.33%; zero-shot accuracy is zero because memory
abstains. Original row IDs, mappings, keys, writes, raw sums/counts/matrices,
scores, predictions, ties and deltas are retained.

Two complete reports match exactly. Canonical report SHA-256:
`2a50066a46766a3ebe5e3ffda33e009200b5c15206104d10aa368d3bdd322eab`.
The final recorded first pass took 1.43s on CPU after imports/resource
loading; it includes recording and excludes browser rendering. This is a local
scoped measurement. Independent NumPy reconstruction also passed for all 650
saved conditions, beyond the separate boundary-seed pytest fixture.

Fresh regeneration reproduced every encoder tensor exactly. Re-evaluating that
checkpoint reproduced all Phase 1 report fields except the deliberately excluded
environment inventory: 97.53% mean accuracy over 1,500 queries and unchanged
encoder parameters. The ordinary digit sanity score remains 437/450.

## 5. Tests and checks executed

| Command/check | Observed result |
|---|---|
| Phase 3 entry suite | 105 passed in 8.80s; prior-phase behavior retained |
| Fresh isolated venv + CPU torch + requirements | Installation succeeded; include-system-site-packages=false |
| python scripts/verify_robustness.py | PASS: pip check, all tests, smoke, separate encoder regeneration and core replay |
| Full suite inside robustness run | 124 passed in 16.81s |
| Final full suite after navigation-label edit | **124 passed in 8.16s** |
| python scripts/evaluate_suite.py | 50 seeds, 650 conditions, complete two-run equality; default output overwrite succeeded |
| Independent saved-row reconstruction | All 650 delivered rows match NumPy sums/counts/matrices/scores/predictions/deltas |
| Live browser | Cold startup, citations, equation/chart inspection, mobile tabs, feedback and preserved state |
| Repository/document audit | Recorded in phase3_verification.json; Git delivery recorded below |

The test runtime is .local/phase3-clean/Scripts/python.exe. To reproduce the
robustness run, install requirements in a fresh venv and run the script. It
creates its workspace-local scratch parent before invoking pytest. Missing model
behavior, unusual shots, repeated reset/conflicts, no-connection app actions with
fresh caches, and all 105 earlier tests are included.

Harness issues were resolved without changing app behavior: legacy pytest
folders were inaccessible, so checks use fresh local scratch paths. One manual
final command omitted its scratch parent and produced 75 passes/49 fixture setup
errors (WinError 3); creating the parent yielded the 124-pass final result.
An earlier OneDrive report overwrite failed; a subsequent default-path run
succeeded and its digest matches the delivered artifact. No failed run is
counted as passing. Full successful robustness commands and package versions
are recorded in phase3_robustness.json.

## 6. Individual requirement checklist

| Requirement ID | Status | Evidence |
|---|---|---|
| P3-01 | PASS | research_sources.json: four papers/reports, first dates 2024–2026, versioned primary full text and exact locators |
| P3-02 | PASS | BDH v1, BDH-CQ v1 and official Pathway baseline at commit 2b0d7a45b058d4309c84a10e0768d541fe18bdc2 |
| P3-03 | PASS | One shared claim ledger feeds nearby UI citations; RESEARCH_NOTES.md maps local claims to code/tests |
| P3-04 | PASS | Research & evidence starts from the live episode; source connections, role comparison and immediate learning check; AppTest/browser verified |
| P3-05 | PASS | Explicit architecture boundaries in UI, source ledger and LIMITATIONS.md; proprietary CQ details are not inferred |
| P3-06 | PASS | S += outer(v,k), c += v, M = S/c, scores = Mq; float64 normalized-key reconstruction and read-only derivation tests |
| P3-07 | PASS | scripts/evaluate_suite.py: two complete 50-seed reports exactly equal; phase3_replay.json |
| P3-08 | PASS | phase3_evidence.json: 650 conditions, keys/IDs/mappings, writes, matrices, scores, predictions, deltas and resets |
| P3-09 | PASS | test_evidence_plot_uses_saved_observations_and_population_std; summary validation and full saved-row reconstruction |
| P3-10 | PASS | LIMITATIONS.md and nearby UI limits: pretrained representations, simple digits, interference, dependent trials, uncalibrated scores and architecture scope |
| P3-11 | PASS | TECHNICAL_WALKTHROUGH.md covers data flow, training, math, actions, evidence, visualizations, limits and 12 judge questions |
| P3-12 | PASS | 124 tests, fresh isolated CPU installation, pip check, smoke, exact regeneration/core replay; phase3_robustness.json and phase3_verification.json |
| P3-13 | PASS | REQUIREMENTS_MATRIX.md: all 13 Phase 3 gates individually evidenced; Phase 4 remains gated |

## 7. Known limitations

The encoder learned familiar digit identities beforehand; fast adaptation binds
temporary symbols. Small digits, fixed 3-way episodes and targeted repeated-key
corruption limit generalization. Conditions share images, so the 19,500 outcomes
are not independent trials. Population deviations are descriptive, not confidence
intervals; three conflicts represent different contamination fractions by shot
count. Additional demonstrations need not improve every seed.

Scores are uncalibrated, memory is temporary, and the toy does not establish
BDH/CQ architecture, language-model, capacity, biological or reasoning results.
Primary reports/code inspection are not independent research reproductions.
Execution was Windows/CPU/Python 3.12.14; installation and opening citations need
network. Full cross-platform, accessibility, human-learning and public-load
validation remain outside this evidence. See LIMITATIONS.md for full details.

## 8. Unresolved items

No Phase 3 acceptance blocker remains. Phase 4 retains deployment, final PDFs,
code/generated-weight license choices, final provenance and submission audits,
organizer portal verification and the blog-versus-concept-summary distinction.
No public application URL or submission readiness is claimed.

## 9. Git status / commit

Target: deeps2710/MemoryForge, branch main. Phase 3 baseline:
`320a327f59cdb39321a1b6a500e577a135d2121c`.
Implementation commit: `383d141e158be6067e9fc0d5a1c7ae2daceb20ad`
(`feat: add sourced research and reproducible Phase 3 evidence`).
Push to origin/main succeeded. On 2026-09-07, git ls-remote confirmed this exact
hash and the working tree was clean. This record is included in a following
documentation commit; the final response identifies the final verified remote HEAD.

## 10. Phase gate

Phases 1, 2 and 3 = **COMPLETE**. Phase 4 = **NOT STARTED**.

Stopped after Phase 3 as instructed. Awaiting explicit instruction to initiate the next phase.
