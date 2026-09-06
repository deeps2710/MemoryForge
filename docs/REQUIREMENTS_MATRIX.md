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
| COMP-01 | Interactive artifact, few meaningful controls, guide then sandbox | Brief sections 3–5, 13 | 2 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-02 | Genuine computation tied to the central claim | Brief sections 3–5, 13 | 1 | P1-10 through P1-19 | PASS | Real core computation verified |
| COMP-03 | One precise falsifiable claim and explicit audience/objectives | Brief sections 3–5, 13 | 1 | README; PROJECT_DECISIONS | PASS | Central claim, audience and intended learning objectives explicit |
| COMP-04 | Visible frozen parameters, memory and retrieval | Brief sections 3–5, 13 | 2 | Phase 1 core and docs evidence | PARTIAL | Core support exists; remaining UI/final audit deferred |
| COMP-05 | Truth beside prediction | Brief sections 3–5, 13 | 2 | Phase 1 core and docs evidence | PARTIAL | Core support exists; remaining UI/final audit deferred |
| COMP-06 | Measured feedback approximately under 1 second after load | Brief sections 3–5, 13 | 2 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-07 | Substantial sourced BDH/BDH-CQ learning module; no equivalence | Brief sections 3–5, 13 | 3 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-08 | At least 3 primary papers dated 2022–2026 beside claims | Brief sections 3–5, 13 | 3 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-09 | Public artifact accessible without sign-in | Brief sections 3–5, 13 | 4 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-10 | Public source repository | Brief sections 3–5, 13 | 4 | Unauthenticated GitHub API private=false; implementation commit f46ae98 pushed, remote main hash verified | PASS | Source repository delivery complete; this does not imply deployment/submission readiness |
| COMP-11 | Complete README and reproduction instructions | Brief sections 3–5, 13 | 4 | Phase 1 core and docs evidence | PARTIAL | Core support exists; remaining UI/final audit deferred |
| COMP-12 | Verified data/code/weights/assets/licenses provenance | Brief sections 3–5, 13 | 4 | Phase 1 core and docs evidence | PARTIAL | Core support exists; remaining UI/final audit deferred |
| COMP-13 | AI disclosure and technical ownership | Brief sections 3–5, 13 | 4 | Phase 1 core and docs evidence | PARTIAL | Core support exists; remaining UI/final audit deferred |
| COMP-14 | One-page concept summary PDF | Brief sections 3–5, 13 | 4 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-15 | Blog/written PDF; resolve whether separate from summary | Brief sections 3–5, 13 | 4 | Requirement-specific phase audit | NOT STARTED | Portal clarification required |
| COMP-16 | Learning check, accessible presentation, genuine failure/reset | Brief sections 3–5, 13 | 2 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-17 | Multi-seed, varying-shot, clean/corrupted evidence and charts | Brief sections 3–5, 13 | 3 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-18 | Technical walkthrough, primary-source claim ledger | Brief sections 3–5, 13 | 3 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-19 | Clean install, public deployment, demo script and rubric audit | Brief sections 3–5, 13 | 4 | Requirement-specific phase audit | NOT STARTED | No early completion claim |
| COMP-20 | Honest limitations, CPU only, reproducibility | Brief sections 3–5, 13 | 4 | Phase 1 core and docs evidence | PARTIAL | Core support exists; remaining UI/final audit deferred |
