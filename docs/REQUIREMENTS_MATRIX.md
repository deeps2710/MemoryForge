# Requirements matrix

Source: user-supplied MemoryForge development brief (2026-09-06), not an independently
verified organizer document. PASS requires recorded evidence. P1 IDs cover every
Phase 1K acceptance item; competition requirements span later phases.

| ID | Requirement | Source/category | Target phase | Verification method / evidence | Current status | Notes |
|---|---|---|---|---|---|---|
| P1-01 | Clean repository structure | Phase 1A | 1 | Git audit: base fd433b4; existing html preserved; .venv/caches ignored | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-02 | Core dependencies install and import | Phase 1A | 1 | artifacts/verification.json: pip check and all core imports succeeded | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-03 | Digits loading, metadata, normalized shapes/ranges | Phase 1C | 1 | tests/test_data.py::test_dataset_shapes_ranges_and_metadata | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-04 | Deterministic, disjoint stratified train/test split | Phase 1C | 1 | tests/test_data.py::test_split_deterministic_disjoint_and_complete | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-05 | CPU deterministic encoder training and saved artifact loading | Phase 1D | 1 | train_encoder.py succeeded; tests/test_reproducibility.py::test_training_replay_reproduces_weights_losses_and_metrics | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-06 | Encoder embeddings have correct shape and normalization | Phase 1D | 1 | tests/test_encoder.py::test_encoder_shape_normalization_freeze_and_no_grad | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-07 | All episodic encoder parameters frozen | Phase 1D | 1 | tests/test_encoder.py::test_encoder_shape_normalization_freeze_and_no_grad | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-08 | Random arbitrary episode label bijection | Phase 1E | 1 | tests/test_episode.py::test_label_permutation_changes_independently_of_selected_digits | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-09 | Distinct held-out support/query rows; no training leakage | Phase 1E | 1 | tests/test_episode.py::test_support_query_train_disjoint_and_ground_truth_preserved (5 seeds) | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-10 | Real memory writes, validation, snapshots and multi-shot handling | Phase 1F | 1 | tests/test_fast_memory.py: batch atomicity, snapshots and multi-shot checks | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-11 | Query uses exact matrix; handcrafted expected math | Phase 1F | 1 | tests/test_fast_memory.py::test_handcrafted_outer_product_and_class_averaging; test_evaluation score reconstruction | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-12 | Reset clears associations and counts | Phase 1F | 1 | tests/test_fast_memory.py::test_empty_abstention_then_identity_retrieval_and_reset | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-13 | Encoder tensors exactly unchanged through adaptation | Phase 1D/1G | 1 | artifacts/evaluation.json: all tensor comparisons true, max parameter delta 0 | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-14 | Nonzero fast-memory delta after demonstrations | Phase 1F/1G | 1 | artifacts/evaluation.json: minimum effective matrix delta 1.5154881739946258 | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-15 | Deterministic multi-episode evaluation above chance | Phase 1G | 1 | artifacts/evaluation.json: 50 episodes, 1500 queries, mean 0.9753333333333333 | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-16 | Actual held-out classification and episode metrics | Phase 1D/1G | 1 | artifacts/encoder.training.json: 437/450; evaluation.json: real per-query records | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-17 | Analytic 1/N chance baseline reported | Phase 1G | 1 | artifacts/evaluation.json: chance 0.3333333333333333 | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-18 | Reproducible wrong-label conflict experiment | Phase 1H | 1 | artifacts/evaluation.json: 19 changed predictions, conflict mean 0.97; original truth preserved | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-19 | Two evaluation runs match mappings, metrics, deltas and state | Phase 1I | 1 | artifacts/reproducibility.json: complete 50-episode reports exactly equal, identical SHA-256 | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-20 | Full pytest suite passes | Phase 1J | 1 | artifacts/verification.json: 77 passed in 6.26s (final full suite) | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-21 | Deterministic end-to-end smoke path passes | Phase 1J | 1 | artifacts/verification.json: smoke PASS, all 5 critical checks true | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-22 | Limitations and provenance uncertainty documented | Phase 1B/1C | 1 | docs/LIMITATIONS.md and PROVENANCE.md: measured limits, original dataset attribution and license TODOs | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-23 | No false BDH equivalence | Phase 1B/1K | 1 | README, ARCHITECTURE, LIMITATIONS and RESEARCH_NOTES explicitly distinguish MemoryForge from BDH | PASS | Verified 2026-09-06; see Phase 1 report |
| P1-24 | Requirement evidence, decisions, disclosure, ledger and completion report | Phase 1B/1L | 1 | docs/PHASE_1_REPORT.md, PHASE_STATUS.md, PROJECT_DECISIONS.md, AI_ASSISTANCE.md and this matrix | PASS | Verified 2026-09-06; see Phase 1 report |

| ID | Requirement | Source/category | Target phase | Verification method | Current status | Notes |
|---|---|---|---|---|---|---|
| COMP-01 | Interactive artifact, few meaningful controls, guide then sandbox | Brief sections 3–5, 13 | 2 | P2-01–04, P2-10 and guided/playground browser walkthrough | PASS | Guided interaction and meaningful controls verified locally |
| COMP-02 | Genuine computation tied to the central claim | Brief sections 3–5, 13 | 1 | P1-10 through P1-19 | PASS | Real core computation verified |
| COMP-03 | One precise falsifiable claim and explicit audience/objectives | Brief sections 3–5, 13 | 1 | README; PROJECT_DECISIONS | PASS | Central claim, audience and intended learning objectives explicit |
| COMP-04 | Visible frozen parameters, memory and retrieval | Brief sections 3–5, 13 | 2 | P2-05, P2-08 and P2-09 | PASS | Actual memory, scores and exact frozen-weight audit visible |
| COMP-05 | Truth beside prediction | Brief sections 3–5, 13 | 2 | P2-07; test_app.py | PASS | Prediction and truth displayed together |
| COMP-06 | Measured feedback approximately under 1 second after load | Brief sections 3–5, 13 | 2 | P2-15; artifacts/phase2_latency.json | PASS | Local measurements with scope limits; no universal guarantee |
| COMP-07 | Substantial sourced BDH/BDH-CQ learning module; no equivalence | Brief sections 3–5, 13 | 3 | P3-02–05; research module and primary claim ledger | PASS | BDH/CQ connections and architectural limits verified |
| COMP-08 | At least 3 primary papers dated 2022–2026 beside claims | Brief sections 3–5, 13 | 3 | P3-01 and P3-03; four versioned primary papers/reports | PASS | 2022–2026 requirement satisfied; citations beside claims |
| COMP-09 | Public artifact accessible without sign-in | Brief sections 3–5, 13 | 4 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-10 | Public source repository | Brief sections 3–5, 13 | 4 | Unauthenticated GitHub API private=false; implementation commit f46ae98 pushed, remote main hash verified | PASS | Source repository delivery complete; this does not imply deployment/submission readiness |
| COMP-11 | Complete README and reproduction instructions | Brief sections 3–5, 13 | 4 | Phase 1 core and docs evidence | PARTIAL | Phases 1–3 implementation documented; remaining final submission audit deferred |
| COMP-12 | Verified data/code/weights/assets/licenses provenance | Brief sections 3–5, 13 | 4 | Phase 1 core and docs evidence | PARTIAL | Phases 1–3 implementation documented; remaining final submission audit deferred |
| COMP-13 | AI disclosure and technical ownership | Brief sections 3–5, 13 | 4 | Phase 1 core and docs evidence | PARTIAL | Phases 1–3 implementation documented; remaining final submission audit deferred |
| COMP-14 | One-page concept summary PDF | Brief sections 3–5, 13 | 4 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-15 | Blog/written PDF; resolve whether separate from summary | Brief sections 3–5, 13 | 4 | Requirement-specific phase audit | NOT STARTED | Portal clarification required |
| COMP-16 | Learning check, accessible presentation, genuine failure/reset | Brief sections 3–5, 13 | 2 | P2-11–14; PHASE_2_WALKTHROUGH.md | PASS | Quiz, labelled responsive UI and real conflict/reset; no full WCAG claim |
| COMP-17 | Multi-seed, varying-shot, clean/corrupted evidence and charts | Brief sections 3–5, 13 | 3 | P3-07–09; phase3_evidence.json and chart payload tests | PASS | 50 seeds, varying shots and paired corruption; actual mean/population deviation |
| COMP-18 | Technical walkthrough, primary-source claim ledger | Brief sections 3–5, 13 | 3 | P3-03 and P3-11; technical walkthrough and source ledger | PASS | Mechanism, evidence and limitations explained for team ownership |
| COMP-19 | Clean install, public deployment, demo script and rubric audit | Brief sections 3–5, 13 | 4 | P3-12; fresh install, complete tests and artifact regeneration | PARTIAL | Public deployment, final demo and rubric audit remain Phase 4 |
| COMP-20 | Honest limitations, CPU only, reproducibility | Brief sections 3–5, 13 | 4 | Phase 1 core and docs evidence | PARTIAL | Phases 1–3 implementation documented; remaining final submission audit deferred |


## Phase 2 acceptance

Authorized by the user's explicit next-phase instruction on 2026-09-06.

| ID | Requirement | Source/category | Target phase | Verification method | Current status | Evidence / notes |
|---|---|---|---|---|---|---|
| P2-01 | App starts successfully | Brief Phase 2 gate | 2 | AppTest startup and live browser | PASS | AppTest startup, missing-artifact handling; live localhost browser |
| P2-02 | Real preset appears immediately | Brief Phase 2 gate | 2 | Preset session state, real matrices and query | PASS | test_app_opens_on_real_preset_with_truth_and_deltas; phase2_demo.json |
| P2-03 | Central claim visible | Brief Phase 2 gate | 2 | Rendered UI and content assertion | PASS | Rendered hero and central-claim assertion in test_app.py |
| P2-04 | Live demonstrations can be added | Brief Phase 2 gate | 2 | Teach action, real keys and one-hot values | PASS | Teach callback and 3-to-6 real writes; test_lab.py write reconstruction |
| P2-05 | Actual fast-memory state is visualized | Brief Phase 2 gate | 2 | Plotly z values match snapshots; visual check | PASS | test_chart_payloads_match_actual_current_and_historical_matrices; browser |
| P2-06 | Query gives actual model output | Brief Phase 2 gate | 2 | Displayed values match FastMemory.query | PASS | test_rendered_score_chart_and_table_agree_with_query |
| P2-07 | Ground truth shown beside prediction | Brief Phase 2 gate | 2 | UI integration and browser check | PASS | AppTest metrics equal real prediction/truth; desktop/mobile screenshots reviewed |
| P2-08 | Measured encoder parameter delta shown | Brief Phase 2 gate | 2 | Exact tensor audit; UI values | PASS | Exact tensor audit each action/view; all recorded encoder deltas zero |
| P2-09 | Measured memory delta shown | Brief Phase 2 gate | 2 | Snapshot delta; UI values | PASS | Real snapshot norms in UI; reset zero; phase2_demo.json |
| P2-10 | Demonstration-count experiment works | Brief Phase 2 gate | 2 | Nested support, fixed queries, real scores | PASS | Fixed query IDs and nested supports; keyboard 0–10; observed-only chart |
| P2-11 | Conflict experiment works | Brief Phase 2 gate | 2 | Actual wrong-label write and before/after comparison | PASS | Real wrong-label write; 5/30 predictions changed; 90.0% to 86.7% |
| P2-12 | Reset clears associations | Brief Phase 2 gate | 2 | Zero matrix, abstention, unchanged encoder | PASS | Zero sums/counts/matrix, abstention, repeat clear and reteach tests |
| P2-13 | Learner quiz gives immediate feedback | Brief Phase 2 gate | 2 | Correct/incorrect feedback for central concepts | PASS | All 3 questions correct/incorrect AppTest; live immediate-feedback check |
| P2-14 | Presentation path is accessible and usable | Brief Phase 2 gate | 2 | Live desktop/mobile browser walkthrough | PASS | PHASE_2_WALKTHROUGH.md; desktop and 390×844; labelled controls and numeric views |
| P2-15 | Feedback performance measured | Brief Phase 2 gate | 2 | Repeated core + app rerun timing; browser observation | PASS | phase2_latency.json; 30 core and 10 AppTest samples/action; scoped browser timings |
| P2-16 | All Phase 1 tests still pass | Brief Phase 2 gate | 2 | Complete pytest suite | PASS | All 77 unchanged Phase 1 tests pass; complete 50-episode report exactly equal |
| P2-17 | Phase 2 tests pass | Brief Phase 2 gate | 2 | Lab state, charts, AppTest, repeat/invalid/reload/isolation | PASS | 28 new lab/chart/AppTest checks pass; full suite 105 passed in 13.85s |
| P2-18 | Requirement evidence and phase ledger updated | Brief Phase 2 gate | 2 | Report, matrix, decisions, limitations, disclosure | PASS | Phase 2 report, matrix, ledger, README, architecture, decisions, limits and provenance |

## Phase 3 acceptance

Authorized by the user's explicit next-phase instruction on 2026-09-07.

| ID | Requirement | Source/category | Target phase | Verification method / evidence | Current status | Notes |
|---|---|---|---|---|---|---|
| P3-01 | 3+ qualifying recent primary papers verified | Brief Phase 3 gate | 3 | research_sources.json: four papers/reports, first dates 2024–2026, versioned primary full text and exact locators | PASS | Verified 2026-09-07 |
| P3-02 | BDH primary sources recorded | Brief Phase 3 gate | 3 | BDH v1, BDH-CQ v1 and official Pathway baseline at commit 2b0d7a45b058d4309c84a10e0768d541fe18bdc2 | PASS | Verified 2026-09-07 |
| P3-03 | Technical claims sourced | Brief Phase 3 gate | 3 | One shared claim ledger feeds nearby UI citations; RESEARCH_NOTES.md maps local claims to code/tests | PASS | Verified 2026-09-07 |
| P3-04 | BDH module integrated | Brief Phase 3 gate | 3 | Research & evidence starts from the live episode; source connections, role comparison and immediate learning check; AppTest/browser verified | PASS | Verified 2026-09-07 |
| P3-05 | No false equivalence with MemoryForge | Brief Phase 3 gate | 3 | Explicit architecture boundaries in UI, source ledger and LIMITATIONS.md; proprietary CQ details are not inferred | PASS | Verified 2026-09-07 |
| P3-06 | Equations match code | Brief Phase 3 gate | 3 | S += outer(v,k), c += v, M = S/c, scores = Mq; float64 normalized-key reconstruction and read-only derivation tests | PASS | Verified 2026-09-07 |
| P3-07 | Reproducible evidence suite exists | Brief Phase 3 gate | 3 | scripts/evaluate_suite.py: two complete 50-seed reports exactly equal; phase3_replay.json | PASS | Verified 2026-09-07 |
| P3-08 | Experiment results stored | Brief Phase 3 gate | 3 | phase3_evidence.json: 650 conditions, keys/IDs/mappings, writes, matrices, scores, predictions, deltas and resets | PASS | Verified 2026-09-07 |
| P3-09 | Charts use actual data | Brief Phase 3 gate | 3 | test_evidence_plot_uses_saved_observations_and_population_std; summary validation and full saved-row reconstruction | PASS | Verified 2026-09-07 |
| P3-10 | Limitations comprehensive | Brief Phase 3 gate | 3 | LIMITATIONS.md and nearby UI limits: pretrained representations, simple digits, interference, dependent trials, uncalibrated scores and architecture scope | PASS | Verified 2026-09-07 |
| P3-11 | Technical walkthrough exists | Brief Phase 3 gate | 3 | TECHNICAL_WALKTHROUGH.md covers data flow, training, math, actions, evidence, visualizations, limits and 12 judge questions | PASS | Verified 2026-09-07 |
| P3-12 | All tests pass | Brief Phase 3 gate | 3 | 124 tests, fresh isolated CPU installation, pip check, smoke, exact regeneration/core replay; phase3_robustness.json and phase3_verification.json | PASS | Verified 2026-09-07 |
| P3-13 | Requirements matrix updated | Brief Phase 3 gate | 3 | REQUIREMENTS_MATRIX.md: all 13 Phase 3 gates individually evidenced; Phase 4 remains gated | PASS | Verified 2026-09-07 |
