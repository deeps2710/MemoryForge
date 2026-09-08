# Requirements matrix

Sources: the supplied MemoryForge development brief (2026-09-06), the inspected
14-page Pathway organizer PDF and the live Unstop submission form. See
SUBMISSION_INSTRUCTIONS_AUDIT.md for physical page locators and portal details.
PASS requires evidence. Earlier phase rows preserve their historical verification;
the competition and Phase 4 rows record current release readiness.

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
| COMP-06 | Measured feedback approximately under 1 second after load | Brief sections 3–5, 13 | 2 | P2-15; artifacts/phase2_latency.json | PASS | Local measurements plus public single-action observations 952–1,017ms including overhead; no universal guarantee |
| COMP-07 | Substantial sourced BDH/BDH-CQ learning module; no equivalence | Brief sections 3–5, 13 | 3 | P3-02–05; research module and primary claim ledger | PASS | BDH/CQ connections and architectural limits verified |
| COMP-08 | At least 3 primary papers dated 2022–2026 beside claims | Brief sections 3–5, 13 | 3 | P3-01 and P3-03; four versioned primary papers/reports | PASS | 2022–2026 requirement satisfied; citations beside claims |
| COMP-09 | Public artifact accessible without sign-in | Organizer p12; Phase 4F | 4 | phase4_deployment.json: anonymous public demo at https://memoryforge.streamlit.app/ | PASS | Python 3.12.14; real operations and restart checked 2026-09-08 |
| COMP-10 | Public source repository | Brief sections 3–5, 13 | 4 | Unauthenticated GitHub API private=false; implementation commit f46ae98 pushed, remote main hash verified | PASS | Source repository delivery complete; this does not imply deployment/submission readiness |
| COMP-11 | Complete README and reproduction instructions | Organizer p12; Phase 4A | 4 | README and all 26 items below; verified deployment and package commands | PASS | Local verification and separate public Linux browser checks |
| COMP-12 | Data/code/weights/assets/licenses source record | Organizer p12; Phase 4B | 4 | PROVENANCE.md; scoped MIT owner choice; dependency_provenance.json; exact dependency, Streamlit and PDF font notices | PASS | Records separate logo/html reuse uncertainty; no legal ownership certification or uninspected Linux-wheel equivalence claimed |
| COMP-13 | AI disclosure and technical ownership | Organizer p11–12; Phase 4C | 4 | AI_ASSISTANCE.md; TECHNICAL_WALKTHROUGH.md; DEMO_SCRIPT.md | UNVERIFIED | Disclosure complete; human comprehension/live defense cannot be certified by agent tests |
| COMP-14 | One-page concept summary PDF | Brief sections 3–5, 13; explicit standalone document request | 4 | output/pdf/MemoryForge_OnePage_Summary.pdf; pdf_verification.json: one page, 526 words including references | PASS | Redesigned at user request after Phase 4; visual/content checks recorded in PDF_DELIVERY.md |
| COMP-15 | Blog/written PDF; separate format clarification | Organizer p12–14; explicit blog request | 4 | Four-page blog delivered; organizer PDF and ZIP form inspected; SUBMISSION_INSTRUCTIONS_AUDIT.md | UNVERIFIED | No separate format specified; included as a labelled submission-format draft alongside the distinct concept summary |
| COMP-16 | Learning check, accessible presentation, genuine failure/reset | Brief sections 3–5, 13 | 2 | P2-11–14; PHASE_2_WALKTHROUGH.md | PASS | Quiz, labelled responsive UI and real conflict/reset; no full WCAG claim |
| COMP-17 | Multi-seed, varying-shot, clean/corrupted evidence and charts | Brief sections 3–5, 13 | 3 | P3-07–09; phase3_evidence.json and chart payload tests | PASS | 50 seeds, varying shots and paired corruption; actual mean/population deviation |
| COMP-18 | Technical walkthrough, primary-source claim ledger | Brief sections 3–5, 13 | 3 | P3-03 and P3-11; technical walkthrough and source ledger | PASS | Mechanism, evidence and limitations explained for team ownership |
| COMP-19 | Clean install, public deployment, demo script and rubric audit | Phase 4F/G/I/K | 4 | phase4_final_robustness.json: 124 tests, exact train/core replay; phase4_deployment.json; DEMO_SCRIPT.md; RUBRIC_AUDIT.md | PASS | Public cold rebuild and real anonymous demo checked; no universal latency guarantee |
| COMP-20 | Honest limitations, CPU only, reproducibility | Organizer p7–14; Phase 4 | 4 | LIMITATIONS.md; live versus saved labels; phase4_robustness.json; unchanged historical evidence | PASS | No unverified performance, deployment, ownership or architecture-equivalence claim |
| COMP-21 | Pathway selection and solution ZIP | Inspected live submission form | 4 | scripts/build_submission.py; source/byte manifest and CRC checks | UNVERIFIED | ZIP preparation and extracted run verified; actual Pathway selection/upload/submission not performed |


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


## Phase 4 acceptance audit

Statuses use PASS, FAIL, UNVERIFIED or NOT APPLICABLE. No scheduled or future
extension is part of this release. A PASS for a document means its contents were
reviewed; it does not imply that the human actions it describes have occurred.

| ID | Requirement | Evidence | Status |
|---|---|---|---|
| P4-A | README covers the 26 specified items | All 26 items below; verified public URL in README | PASS |
| P4-B | Source/license/modification/location record for all material | PROVENANCE.md and exact notices; scoped MIT approval | PASS |
| P4-C | Honest AI and reuse disclosure | AI_ASSISTANCE.md; README credits; no claimed human defense | PASS |
| P4-C2 | Team understands and can defend the submission | Walkthrough and rehearsal supplied; no observed team review | UNVERIFIED |
| P4-D | Readable one-page 500–950-word concept summary | One A4 page, 526 extracted words, source/visual checks; redesigned 2026-09-08 | PASS |
| P4-E | Check blog ambiguity and label unresolved format | Organizer p12–14 and live ZIP field inspected; blog marked submission-format draft | PASS |
| P4-F1 | Correct public deployment inputs, dependencies, checkpoint and no secrets | DEPLOYMENT.md; checked-in CPU artifact; pinned versions; no secret-pattern hits | PASS |
| P4-F2 | Usable public URL without owner authentication | phase4_deployment.json: real app operated in anonymous browser | PASS |
| P4-F3 | Public cold start and interaction checks | Fresh reboot usable within 130s; real actions observed at 952–1,017ms including overhead; phase4_deployment.json | PASS |
| P4-G | Concise reproducible demonstration | DEMO_SCRIPT.md; measured seed-1000 protocol; roughly one-minute target labelled | PASS |
| P4-H | Requirement-by-requirement honest audit | This matrix, organizer/portal audit and readiness report | PASS |
| P4-I | Seven-criterion rubric review | RUBRIC_AUDIT.md: weights, strengths, weaknesses, evidence and useful final actions; no promised score | PASS |
| P4-J | Code/assets/links/TODOs/secrets/caches/binaries/pins cleanup | phase4_cleanup.json: syntax/local-link/pattern scan, 45 protected prior files unchanged; only relevant release files added | PASS |
| P4-K1 | Clean install, train/load, evaluate and tests | Initial fresh install and final constraints: phase4_final_installation.json / phase4_final_robustness.json; 124 tests in 15.76s, smoke, exact encoder/core replay | PASS |
| P4-K2 | Start and operate final app end to end | Anonymous hosted demo, research, credits and post-reboot teaching; phase4_deployment.json | PASS |
| P4-L | Final readiness report and stop | Final SUBMISSION_READINESS_REPORT.md: READY WITH MANUAL ACTIONS; stop after Phase 4 | PASS |
| P4-ZIP | Portal package byte integrity, source manifest and run after extraction | Builder CRC/byte/SHA manifest checks; extracted smoke and app tests in phase4_package_smoke.json | PASS |
| P4-SUBMIT | Actual competition submission | No final form submission authorized or performed | UNVERIFIED |
| P4-EXT | Implement post-hackathon extensions | Excluded by phase scope | NOT APPLICABLE |

### README item coverage

| Item | Required content | Location in README | Status |
|---|---|---|---|
| 1 | Project title | Opening heading | PASS |
| 2 | One-sentence claim | Opening quote | PASS |
| 3 | Problem | The problem | PASS |
| 4 | Intended learner | Audience and learning objectives | PASS |
| 5 | Prerequisites | Audience and learning objectives | PASS |
| 6 | Learning objectives | Audience and learning objectives | PASS |
| 7 | Architecture | Mechanism; architecture link and project layout | PASS |
| 8 | ML methodology | Mechanism and measured evidence; linked training config | PASS |
| 9 | Memory equation | Explicit S/c/M update and scores | PASS |
| 10 | Arbitrary episode mapping | Opening, Use the lab and Mechanism | PASS |
| 11 | App features | Use the lab and Research | PASS |
| 12 | Installation | Python 3.12 venv, requirements and pip check | PASS |
| 13 | Run instructions | streamlit run app.py | PASS |
| 14 | Training/reproduction | Explicit train_encoder.py commands | PASS |
| 15 | Evaluation reproduction | Core, replay, suite and robustness commands | PASS |
| 16 | Live/precomputed distinction | Cached embeddings, live actions, saved evidence; no scripted model animation | PASS |
| 17 | Data source | Scope, sources and ownership | PASS |
| 18 | Model source | Locally trained encoder, checkpoint and metadata | PASS |
| 19 | Primary research | Research section and adjacent source links | PASS |
| 20 | BDH connection | Research module and explicit implementation boundary | PASS |
| 21 | Limitations | Scope and linked LIMITATIONS.md | PASS |
| 22 | AI disclosure | Credits and AI_ASSISTANCE.md | PASS |
| 23 | Licenses/provenance | Scoped MIT and separate notice links | PASS |
| 24 | Verified deployment URL | Opening live link; deployment evidence section | PASS |
| 25 | Repository URL | Opening links and deployment coordinates | PASS |
| 26 | Credits | Scope, sources and ownership | PASS |
