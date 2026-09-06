You are acting as the lead software engineer, ML engineer, research engineer,
QA engineer, and technical documentation maintainer for a time-critical
DataForge 2026 hackathon project.

Read this ENTIRE prompt before making any changes.

This prompt defines:
- the complete project vision;
- the competition requirements;
- the ML methodology;
- the architecture;
- the development standards;
- the implementation roadmap;
- the testing requirements;
- the documentation requirements;
- the final submission requirements;
- and strict phase-gating rules.

IMPORTANT:
You are NOT allowed to build the whole project immediately.

You must understand the entire roadmap first, but on this first invocation you
must execute PHASE 1 ONLY.

After Phase 1:
1. implement everything required by Phase 1;
2. test it;
3. verify every Phase 1 requirement individually;
4. produce a detailed Phase 1 completion report;
5. update the persistent project status documentation;
6. STOP;
7. wait for the user's explicit instruction such as:

   "Initiate the next phase"

Only after receiving that instruction may you begin Phase 2.

The same rule applies between every later phase.

===============================================================================
SECTION 1 — PROJECT IDENTITY
===============================================================================

Project working name:

MemoryForge

Subtitle:

Interactive Few-Shot Learning with Fast-Weight Associative Memory

Competition:

DataForge 2026 — Pathway Track

Selected approved topic:

Associative Memory and Fast Weights

Primary project category:

Machine Learning / AI Research Education / Interactive ML Visualization

Primary objective:

Build a technically correct, interactive machine-learning experience that
teaches how a neural system can rapidly acquire new associations using
temporary fast-weight / associative memory while its long-term neural-network
parameters remain unchanged.

This is NOT supposed to be:
- a generic chatbot;
- a RAG application;
- an LLM wrapper;
- a paper summarizer;
- a static educational website;
- an animation pretending to be model computation;
- a dashboard full of unrelated metrics;
- a fake implementation of BDH;
- or a broad explanation of the entire field.

The ML mechanism itself must be central to the product.

===============================================================================
SECTION 2 — THE CENTRAL LEARNING CLAIM
===============================================================================

The entire project should revolve around ONE precise, falsifiable claim:

"A neural system can rapidly learn new associations by updating temporary
fast-weight memory while keeping its long-term model parameters unchanged."

Every major:
- experiment,
- chart,
- control,
- visualization,
- explanation,
- metric,
- and BDH connection

must support this claim.

Do not add features merely because they look impressive.

If a feature does not help the learner understand, test, reproduce, challenge,
or contextualize this claim, it should probably not exist.

===============================================================================
SECTION 3 — TARGET LEARNER
===============================================================================

Primary learner:

An undergraduate ML/data-science student or early ML practitioner who already
understands:
- basic classification;
- vectors;
- neural networks at a basic level;
- training versus inference;
- and the basic concept of embeddings;

but does NOT yet understand:
- fast weights;
- associative key-value memory;
- temporary inference-time state;
- Hebbian-style updates;
- or how such memory differs from permanent model weights.

The project must explicitly state:

Audience:
Early ML learners / data scientists.

Prerequisites:
Basic neural networks, vectors, classification, embeddings.

Learning objectives:

By the end of the experience the learner should be able to:

1. distinguish permanent model weights from temporary fast memory;
2. explain how demonstration examples can create temporary associations;
3. observe a real memory update;
4. use that memory to make an unseen prediction;
5. understand that the encoder can remain frozen while the temporary state
   changes;
6. experimentally observe the effect of more demonstrations;
7. experimentally observe a failure mode such as conflicting/mislabeled
   demonstrations;
8. explain why temporary fast memory is useful but not equivalent to permanent
   training;
9. understand the conceptual connection to recent architectures such as BDH,
   without falsely claiming that MemoryForge itself implements BDH.

===============================================================================
SECTION 4 — COMPETITION REQUIREMENTS THAT MUST SHAPE THE PROJECT
===============================================================================

Treat the following as hard requirements derived from the Pathway challenge.

A. INTERACTIVITY

A static article, poster, slide deck, or recorded video alone is insufficient.

The artifact must allow the learner to alter something meaningful, such as:
- an example;
- a parameter;
- a state;
- a demonstration count;
- a corruption condition;
- or an assumption;

and observe a meaningful consequence.

B. REAL COMPUTATION

At least one important part of the artifact must contain genuine computation.

Animations must either:
- correspond to actual computation;
OR
- be clearly labelled as a teaching simplification.

Never present a scripted animation as actual model behavior.

C. ONE CENTRAL CLAIM

Avoid explaining an entire field.

A focused artifact that creates one reliable moment of understanding is
preferred over a broad dashboard.

D. VISIBLE STATE

The important internal state should be visible.

For this project, that includes:
- frozen model parameters being unchanged;
- fast-memory contents changing;
- retrieved associations;
- confidence/logit behavior where useful;
- prediction versus ground truth.

E. TRUTH BESIDE ESTIMATE

Whenever possible show:
- model prediction;
AND
- correct/expected answer

next to each other.

F. FAST FEEDBACK

Interactive controls should respond quickly.

Target:
under approximately one second for normal memory update/query interactions
after the app and encoder have loaded.

Do not sacrifice correctness to meet this target.

G. FEW MEANINGFUL CONTROLS

Controls must correspond to actual ML variables.

Avoid decorative sliders.

H. GUIDE THEN SANDBOX

The application should initially guide the learner through the central
mechanism.

After the learner understands it, expose a playground/sandbox.

I. HONEST LIMITATIONS

All important caps, simplifications, assumptions, precomputation,
synthetic components, toy models, and unsupported claims must be disclosed.

J. BDH / BDH-CQ

The project must contain a substantial, technically correct learning section
connecting the chosen concept to BDH or BDH-CQ.

Do NOT tack this on as a random final paragraph.

Integrate it naturally into the learning journey.

Use primary sources where possible.

MemoryForge must NEVER be labelled:
- "BDH";
- "BDH-CQ";
- "an implementation of BDH";
- or "a reproduction of BDH"

unless that becomes factually true, which is not currently the project plan.

Instead label it explicitly as:

"An educational fast-weight associative-memory model used to demonstrate the
concept."

Then separately explain how published BDH research relates to the concept.

K. RESEARCH SOURCING

At least three recent PRIMARY research papers from 2022–2026 that:
- use;
- extend;
- test;
- or rely on

the selected concept must be cited beside relevant technical claims in the
final submission.

BDH / BDH-CQ primary sources should also be used for claims about those
systems.

Do not fabricate papers, authors, dates, results, benchmarks, quotations, or
citations.

If primary sources cannot be accessed during a phase:
- create an explicit TODO;
- identify what evidence is still required;
- do NOT fill gaps using made-up information.

L. AI ASSISTANCE

AI-assisted:
- coding;
- writing;
- research;
- and design

are allowed by the competition.

However:
- the team must understand every major component;
- AI-generated work must be disclosed;
- reused or forked work must be disclosed;
- technical ownership must remain with the team.

Maintain an AI assistance disclosure.

M. SUBMISSION COMPONENTS

The final project should be prepared to provide:

1. public artifact URL accessible without sign-in;
2. public source-code repository;
3. complete README;
4. setup/reproduction instructions;
5. written PDF deliverable(s);
6. at least three recent primary papers from 2022–2026;
7. code/data/weights/assets/license provenance;
8. AI-assistance disclosure;
9. concept summary PDF;
10. any additional written/blog PDF required by the actual submission portal.

IMPORTANT AMBIGUITY:

The supplied Pathway PDF mentions "the blog as a PDF" and subsequently defines
a required "one-page concept summary".

Do NOT invent requirements that were not specified.

Maintain these as potentially separate deliverables until the actual portal or
organizer instructions confirm whether they are separate.

Flag this in documentation as an unresolved submission-check item rather than
silently assuming an answer.

===============================================================================
SECTION 5 — JUDGING PRIORITIES
===============================================================================

Optimize the project around the official scoring priorities:

1. Technical correctness and depth — 25 points
2. Technical ownership and live defense — 15 points
3. Learning effectiveness — 15 points
4. Interactive substrate and honesty — 15 points
5. BDH / BDH-CQ integration and evidence discipline — 10 points
6. Craft, robustness, accessibility, provenance — 10 points
7. One-page concept summary — 10 points

Use these priorities when deciding whether a feature is worth implementing.

Correct ML + explainability + interactivity are more important than
unnecessary software complexity.

===============================================================================
SECTION 6 — DEVELOPMENT PHILOSOPHY
===============================================================================

The deadline is extremely close.

Therefore:

PRIORITIZE:
- working ML;
- reproducibility;
- interactivity;
- presentability;
- scientific honesty;
- simplicity;
- reliability;
- fast iteration.

AVOID:
- unnecessary microservices;
- unnecessary databases;
- authentication;
- user accounts;
- React unless genuinely unavoidable;
- FastAPI unless genuinely unavoidable;
- cloud infrastructure complexity;
- asynchronous architecture that provides no direct benefit;
- external paid APIs;
- GPU dependencies;
- giant datasets;
- model training that takes hours;
- unnecessary LLM APIs;
- premature optimization;
- complex animations;
- scope creep.

Default stack:

Python
PyTorch
NumPy
Scikit-learn
Pandas where useful
Plotly
Streamlit
Pytest

The entire application should be capable of running on CPU.

===============================================================================
SECTION 7 — CORE ML EXPERIMENT
===============================================================================

The central live experiment will use:

sklearn.datasets.load_digits()

Reasons:
- bundled with scikit-learn;
- no external dataset download required;
- tiny;
- visually understandable;
- 8×8 handwritten digit images;
- extremely fast;
- appropriate for CPU;
- good for live demonstration.

-------------------------------------------------------------------------------
7.1 PRETRAINED / SLOW COMPONENT
-------------------------------------------------------------------------------

Build a small neural encoder in PyTorch.

Suggested architecture:

Input:
64 features from an 8×8 digit image

Example:

64
→ Linear(64, 32)
→ ReLU
→ Linear(32, 16)

The exact architecture may be adjusted if justified.

During encoder training only, attach a classification head for digit
classification.

Example:

16
→ Linear(16, 10)

Train on a deterministic training split of the digits dataset.

After training:
- retain the encoder;
- discard or ignore the ordinary classification head for the main MemoryForge
  task;
- FREEZE every encoder parameter.

The application must verify programmatically that the encoder remains frozen
during episodic fast-memory learning.

Do not merely trust `requires_grad=False`.

Also test that actual parameter tensors do not change before versus after a
fast-memory episode.

Precompute embeddings for held-out examples where beneficial for UI latency.

-------------------------------------------------------------------------------
7.2 EPISODIC TASK
-------------------------------------------------------------------------------

The main task is NOT normal digit classification.

Instead create temporary random mappings per episode.

Example:

Digit 2 → ALPHA
Digit 5 → BETA
Digit 8 → GAMMA

Another episode might become:

Digit 2 → GAMMA
Digit 5 → ALPHA
Digit 8 → BETA

This random mapping is important.

It demonstrates that the permanent model cannot simply memorize the arbitrary
episode label assignment.

Default episode:

3-way classification

Example:
choose 3 digit identities;
assign 3 arbitrary symbolic labels.

Prefer accessible labels such as:
ALPHA
BETA
GAMMA

Optional colors may visually accompany labels, but do NOT make color the sole
carrier of information because of accessibility.

The demonstrations contain:
- image;
- actual digit identity;
- episode-specific arbitrary label.

Queries use new held-out images of one of the selected digit classes.

The prediction target is the EPISODE LABEL, not the normal digit number.

-------------------------------------------------------------------------------
7.3 FAST-WEIGHT ASSOCIATIVE MEMORY
-------------------------------------------------------------------------------

Implement a small, interpretable associative key-value memory.

Use normalized encoder embeddings as keys.

Represent episode labels as one-hot values.

A simple pedagogically useful form is a Hebbian-style outer-product memory:

M ← M + v k^T

where:
- k is an embedding/key;
- v is a one-hot label/value;
- M is temporary associative memory.

For a query embedding q:

scores = M q

Then convert scores to suitable normalized confidence-like values when
appropriate.

If multiple demonstrations per class are used, handle scale fairly.

For example:
- class-wise normalization;
- averaging;
- or another clearly documented mechanism.

Do NOT silently introduce a complicated method solely to improve scores.

Clarity matters.

If implementation changes materially from the formula above:
- document why;
- retain conceptual correspondence;
- update equations;
- update tests;
- disclose simplification.

The memory object must support at least:

reset()
write(key, value)
write_batch(...)
query(...)
state_snapshot()
memory_delta(...)
statistics()

The memory should be TEMPORARY.

Starting a fresh episode or pressing Clear Memory must reset it.

-------------------------------------------------------------------------------
7.4 CRITICAL SCIENTIFIC DISTINCTION
-------------------------------------------------------------------------------

Permanent encoder:
slow/frozen weights.

Fast memory:
temporary, changing state.

The UI and tests must demonstrate:

Encoder parameter delta after memory writes = 0.

Fast memory delta after demonstrations > 0.

This distinction is central to the entire project.

-------------------------------------------------------------------------------
7.5 BASELINES
-------------------------------------------------------------------------------

At minimum include a random/chance baseline in evaluation.

For an N-way episode:

chance = 1/N.

Optional later baseline:
nearest demonstration / prototype classifier.

Do not add multiple baselines in Phase 1 unless they help validate the ML
implementation.

Avoid bloating scope.

-------------------------------------------------------------------------------
7.6 REPRODUCIBILITY
-------------------------------------------------------------------------------

All experiments must support deterministic random seeds.

Record:
- Python seed;
- NumPy seed;
- PyTorch seed;
- train/test split seed;
- episode seed.

Create a single reproducibility utility.

No hidden randomness.

===============================================================================
SECTION 8 — CORE USER EXPERIENCE
===============================================================================

The final experience should roughly follow this learning journey:

STEP 1 — HOOK

Show a preset episode immediately.

Do NOT open with an empty page requiring the user to click "Run".

Opening message:

"Can an AI learn a new association without changing its neural-network
weights?"

Immediately show demonstrations and a current prediction.

-------------------------------------------------------------------------------

STEP 2 — SEE THE PERMANENT MODEL

Show:

Neural Encoder
Status: FROZEN

Explain briefly:
the encoder has learned a representation of digit images beforehand.

Do not overwhelm the learner with architecture details immediately.

-------------------------------------------------------------------------------

STEP 3 — TEACH A NEW ASSOCIATION

Display something like:

Digit 2 → ALPHA
Digit 5 → BETA
Digit 8 → GAMMA

Allow learner to add demonstrations.

As each demonstration is written:
- show which embedding is written;
- show its label/value;
- update the memory visualization.

-------------------------------------------------------------------------------

STEP 4 — SEE FAST MEMORY CHANGE

Display the fast-memory matrix as a heatmap or another truthful visualization.

Before:
near-zero / empty memory.

After:
changed memory.

Never fabricate the heatmap.

It must visualize the actual memory tensor being used for prediction.

-------------------------------------------------------------------------------

STEP 5 — QUERY THE SYSTEM

Show a held-out query image.

Show:

Prediction: BETA
Ground truth: BETA
Confidence/scores
Correct / Incorrect

Truth and model output must appear side by side.

-------------------------------------------------------------------------------

STEP 6 — WHAT CHANGED?

Display:

Encoder parameter delta: 0
Fast-memory delta: > 0

This should be one of the strongest moments in the demo.

-------------------------------------------------------------------------------

STEP 7 — EXPERIMENT

Expose only meaningful controls such as:

- demonstrations per class;
- random episode;
- perhaps selected digit classes;
- perhaps controlled input noise;
- conflicting demonstration injection.

Avoid unnecessary controls.

-------------------------------------------------------------------------------

STEP 8 — BREAK THE MEMORY

Provide a deliberate failure experiment.

Preferred MVP:

"Inject conflicting demonstration"

Example:

Existing:
Digit 7 → BETA

Conflict:
Digit 7 → GAMMA

Then evaluate before and after.

Show the effect of conflicting information on:
- predictions;
- scores;
- memory;
- and aggregate accuracy.

This is more scientifically defensible than inventing an arbitrary "memory
capacity" slider unless capacity is explicitly implemented and measured.

-------------------------------------------------------------------------------

STEP 9 — RESET

Provide:

CLEAR MEMORY

When clicked:
- memory returns to initial state;
- encoder remains unchanged;
- previously learned episode associations disappear;
- predictions revert appropriately.

This should be visually obvious.

-------------------------------------------------------------------------------

STEP 10 — BDH CONNECTION

After the learner has understood:
slow weights versus temporary memory,

introduce the research connection.

Do not lead with BDH jargon.

Use the project experiment as conceptual scaffolding.

-------------------------------------------------------------------------------

STEP 11 — 60-SECOND CHECK

Add a short learning test.

Example question:

"A model receives demonstrations. Its permanent weights remain identical, but
its temporary memory changes. Which component carried the adaptation?"

Provide immediate feedback.

The quiz should test the central claim, not trivia.

===============================================================================
SECTION 9 — EXPECTED PROJECT STRUCTURE
===============================================================================

Use a clean structure similar to:

memoryforge/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example              # only if actually needed
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── reproducibility.py
│   ├── data.py
│   ├── encoder.py
│   ├── training.py
│   ├── episodes.py
│   ├── fast_memory.py
│   ├── evaluation.py
│   └── visualization.py
│
├── scripts/
│   ├── train_encoder.py
│   ├── evaluate_core.py
│   └── smoke_test.py
│
├── artifacts/
│   └── encoder.pt
│
├── tests/
│   ├── test_data.py
│   ├── test_encoder.py
│   ├── test_fast_memory.py
│   ├── test_episode.py
│   ├── test_reproducibility.py
│   └── ...
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PROJECT_DECISIONS.md
│   ├── REQUIREMENTS_MATRIX.md
│   ├── PHASE_STATUS.md
│   ├── RESEARCH_NOTES.md
│   ├── LIMITATIONS.md
│   ├── PROVENANCE.md
│   ├── AI_ASSISTANCE.md
│   └── FUTURE_ROADMAP.md
│
└── submission/
    ├── concept_summary.md
    ├── research_sources.md
    ├── demo_script.md
    └── ...

Adjust only when there is a concrete reason.

Do not create dozens of empty files just to mimic this structure.

Every created file should have a purpose.

===============================================================================
SECTION 10 — PERSISTENT PROJECT MANAGEMENT FILES
===============================================================================

Because development occurs over multiple Codex sessions/phases, maintain the
following files carefully.

-------------------------------------------------------------------------------
10.1 docs/PROJECT_DECISIONS.md
-------------------------------------------------------------------------------

Record important decisions.

For every significant decision include:

Decision:
Reason:
Alternatives considered:
Consequences:
Phase introduced:

Examples:
- why sklearn digits was used;
- why Streamlit was chosen;
- exact encoder architecture;
- exact memory formula;
- normalization method;
- default episode size.

Do not rewrite history unnecessarily.

-------------------------------------------------------------------------------
10.2 docs/PHASE_STATUS.md
-------------------------------------------------------------------------------

Persistent phase ledger.

Include:

Current phase:
Completed phases:
Current status:
Last verification:
Known issues:
Unresolved requirements:
Next permitted phase:

At the end of Phase 1 it must clearly say:

Phase 1: COMPLETE / INCOMPLETE
Phase 2: NOT STARTED
Awaiting user instruction.

-------------------------------------------------------------------------------
10.3 docs/REQUIREMENTS_MATRIX.md
-------------------------------------------------------------------------------

Create stable requirement IDs.

Examples:

COMP-01 Interactive artifact
COMP-02 Real computation
COMP-03 One central claim
COMP-04 Visible state
COMP-05 Truth beside estimate
COMP-06 Fast feedback
COMP-07 BDH integration
COMP-08 3+ recent primary papers
COMP-09 Public artifact URL
COMP-10 Public repository
COMP-11 README
COMP-12 Provenance/licenses
COMP-13 AI disclosure
COMP-14 Concept summary PDF

ML-01 Frozen encoder
ML-02 Random episode mapping
ML-03 Associative memory update
ML-04 Memory reset
ML-05 Parameter delta zero
ML-06 Memory delta nonzero
ML-07 Reproducibility
...

For every requirement track:

ID
Requirement
Source/category
Target phase
Verification method
Current status
Evidence / file / test
Notes

Never claim PASS without evidence.

-------------------------------------------------------------------------------
10.4 docs/AI_ASSISTANCE.md
-------------------------------------------------------------------------------

Record meaningful AI-assisted development.

Include:
- Codex used for implementation;
- areas assisted;
- tests/review performed;
- team responsibility for verification.

Do not pretend AI wasn't used.

===============================================================================
SECTION 11 — CODING STANDARDS
===============================================================================

General:

- Python 3.11-compatible unless repository environment requires otherwise.
- Type hints for important interfaces.
- Small focused functions.
- Docstrings on non-obvious ML functions.
- No giant app.py containing the entire ML implementation.
- UI calls modules; ML logic remains independently testable.
- Avoid global mutable state where possible.
- No secrets committed.
- No unnecessary abstraction.
- No unnecessary design patterns.
- CPU-safe.
- deterministic when requested.
- reasonable error handling.
- meaningful names.

ML:

- no data leakage between train/test splits;
- no fitting on query examples;
- freeze encoder correctly;
- no hidden training during demo;
- no fake accuracy values;
- no hard-coded successful predictions;
- no hard-coded charts pretending to be experiments.

Metrics shown to users must originate from actual computation.

===============================================================================
SECTION 12 — TESTING PHILOSOPHY
===============================================================================

Tests are not optional.

Each phase must include:

1. unit tests;
2. integration tests where appropriate;
3. deterministic smoke test;
4. manual verification for UI when applicable;
5. requirement-level verification.

A phase CANNOT be marked complete merely because the code "looks right".

If a test cannot be performed:
mark it UNVERIFIED and explain why.

Do not say "all requirements satisfied" if something was not verified.

After code changes always run the relevant complete test suite.

At minimum by project completion:

pytest must pass.

Also provide a simple command such as:

python scripts/smoke_test.py

that validates the critical application path.

===============================================================================
SECTION 13 — PHASE EXECUTION RULES
===============================================================================

There are ONLY FOUR major phases.

This small number is deliberate because the deadline is close.

You must NEVER start the next phase automatically.

During the initial execution:
PHASE 1 ONLY.

When the user says:

"Initiate the next phase"

then:
- read docs/PHASE_STATUS.md;
- inspect docs/PROJECT_DECISIONS.md;
- inspect docs/REQUIREMENTS_MATRIX.md;
- rerun the existing test suite;
- verify previous phase assumptions still hold;
- then begin exactly one next phase.

Do not reinitialize the repo.
Do not discard working implementation.
Do not replace stable modules unless there is a concrete technical reason.

Prefer incremental extensions.

If changing a previous decision:
1. explain why;
2. update PROJECT_DECISIONS;
3. preserve compatibility where practical;
4. rerun affected tests;
5. explicitly report the change.

===============================================================================
PHASE 1 — CORE ML FOUNDATION AND VERIFIED MVP ENGINE
===============================================================================

GOAL:

Produce a scientifically defensible, deterministic, independently testable
ML core before building the polished UI.

DO NOT build the final Streamlit experience yet.

Phase 1 must accomplish ALL of the following.

-------------------------------------------------------------------------------
PHASE 1A — REPOSITORY AUDIT
-------------------------------------------------------------------------------

Before coding:

1. inspect the repository;
2. understand existing files;
3. preserve useful existing work;
4. check Git status;
5. identify Python environment;
6. inspect dependency configuration;
7. avoid deleting unrelated user work.

If repository is empty:
initialize the project cleanly.

Do not create unnecessary placeholder files.

-------------------------------------------------------------------------------
PHASE 1B — REQUIREMENT CAPTURE
-------------------------------------------------------------------------------

Create/update:

docs/PROJECT_DECISIONS.md
docs/PHASE_STATUS.md
docs/REQUIREMENTS_MATRIX.md
docs/AI_ASSISTANCE.md
docs/LIMITATIONS.md

Record the project's central claim, scope and competition constraints.

Phase 1 status must initially be IN PROGRESS.

-------------------------------------------------------------------------------
PHASE 1C — DATA PIPELINE
-------------------------------------------------------------------------------

Implement loading of sklearn digits.

Requirements:

- deterministic split;
- explicit train/test separation;
- normalize input consistently;
- expose dataset metadata;
- avoid leakage;
- query/demo samples used during episodes should come from the held-out portion
  intended for evaluation;
- tests verify shapes/ranges/split behavior.

Document dataset source and license/provenance information if available from
the installed package/documentation.

If license details are uncertain:
do not guess;
record as research TODO.

-------------------------------------------------------------------------------
PHASE 1D — ENCODER
-------------------------------------------------------------------------------

Implement the small PyTorch encoder.

Train classification head on training split.

Requirements:

- deterministic training;
- CPU compatible;
- save artifact;
- allow loading artifact without retraining every app run;
- report actual held-out digit-classification performance for sanity;
- no invented performance target.

Recommended sanity expectation:
performance should be comfortably better than chance.

If performance is unexpectedly poor:
investigate before proceeding.

After training:
freeze encoder.

Test:
- all encoder `requires_grad` values false where intended;
- encoder weights identical before and after memory episode;
- loading saved model reproduces embeddings.

-------------------------------------------------------------------------------
PHASE 1E — EPISODE GENERATOR
-------------------------------------------------------------------------------

Implement deterministic episodic task creation.

Minimum functionality:

generate_episode(
    n_way,
    shots_per_class,
    queries_per_class,
    seed
)

Episode must:
- select digit classes;
- create a random mapping to episode labels;
- choose demonstration images;
- choose distinct query images;
- avoid accidental duplication where inappropriate;
- preserve ground truth;
- support deterministic replay from seed.

Test:
same seed → same episode.

Different seed → generally different mapping/selection.

-------------------------------------------------------------------------------
PHASE 1F — FAST-WEIGHT MEMORY
-------------------------------------------------------------------------------

Implement associative memory using a simple transparent mathematical update.

Requirements:

- memory begins empty;
- writes alter memory;
- query uses actual memory state;
- reset clears it;
- state snapshot available;
- memory norm/delta measurable;
- input validation;
- no gradient update to frozen encoder;
- multiple demonstrations handled correctly.

Test the math with tiny handcrafted vectors where expected answer can be
calculated manually.

This is essential.

Do not rely solely on dataset-level tests.

-------------------------------------------------------------------------------
PHASE 1G — END-TO-END ML EVALUATION
-------------------------------------------------------------------------------

Create an evaluation script.

Example:

python scripts/evaluate_core.py

It should:

1. load encoder;
2. run multiple deterministic unseen episodes;
3. write demonstrations to fast memory;
4. query held-out images;
5. calculate actual accuracy;
6. calculate chance baseline;
7. measure encoder parameter delta;
8. measure memory delta;
9. report results.

Engineering acceptance target:

The system should demonstrably perform above chance across a deterministic
multi-episode validation set.

Do not fabricate a required competition accuracy because the PDF does not
specify one.

Suggested internal health target:
mean episode accuracy should exceed random chance by a meaningful margin.

If results are poor:
debug the representation/memory design before Phase 1 can pass.

Do NOT hardcode desired results.

-------------------------------------------------------------------------------
PHASE 1H — CONFLICT TEST
-------------------------------------------------------------------------------

Implement a simple reproducible conflicting-demonstration experiment at the ML
level, even if UI is Phase 2.

Example:
- run clean episode;
- inject a wrong label association;
- rerun;
- record how memory/predictions change.

Do not require that accuracy always decreases on every seed.

Instead demonstrate and log the actual effect.

The purpose is to establish the failure-analysis mechanism.

-------------------------------------------------------------------------------
PHASE 1I — REPRODUCIBILITY
-------------------------------------------------------------------------------

Implement central seed control.

Run the same evaluation twice.

Verify equal:
- episode mappings;
- metrics where deterministic;
- parameter deltas;
- memory state where expected.

Document any unavoidable nondeterminism.

-------------------------------------------------------------------------------
PHASE 1J — TEST SUITE
-------------------------------------------------------------------------------

Minimum Phase 1 tests should cover:

- dataset loading;
- deterministic split;
- encoder output shape;
- encoder freeze;
- encoder persistence;
- episode determinism;
- no support/query leakage within an episode where prohibited;
- arbitrary-label mapping;
- memory write;
- memory query;
- memory reset;
- handcrafted memory math;
- parameter immutability;
- memory-state change;
- reproducible evaluation;
- end-to-end smoke path.

Run full pytest.

Run scripts/smoke_test.py.

Run scripts/evaluate_core.py.

-------------------------------------------------------------------------------
PHASE 1K — PHASE 1 ACCEPTANCE GATE
-------------------------------------------------------------------------------

PHASE 1 MAY ONLY BE MARKED COMPLETE IF:

[ ] repo is structurally clean;
[ ] core dependencies install/import;
[ ] digits data loads;
[ ] deterministic train/test split exists;
[ ] encoder trains and loads;
[ ] encoder produces embeddings;
[ ] encoder is frozen for episode adaptation;
[ ] arbitrary episode label mappings work;
[ ] demonstrations and queries are distinct as designed;
[ ] fast memory writes actual state;
[ ] query uses actual memory;
[ ] reset works;
[ ] frozen encoder parameter delta is exactly zero within numerical equality;
[ ] fast memory delta is nonzero after valid writes;
[ ] evaluation runs across multiple episodes;
[ ] actual metrics are reported;
[ ] chance baseline is reported;
[ ] conflicting demonstration experiment runs;
[ ] deterministic replay works;
[ ] pytest passes;
[ ] smoke test passes;
[ ] limitations are documented;
[ ] no claims falsely identify MemoryForge as BDH;
[ ] requirements matrix has been updated with evidence.

If any item fails:
PHASE 1 IS NOT COMPLETE.

Fix it or report the blocker.

-------------------------------------------------------------------------------
PHASE 1L — REQUIRED COMPLETION REPORT
-------------------------------------------------------------------------------

At the end output:

================================
PHASE 1 COMPLETION REPORT
================================

Overall status:
PASS / FAIL / PARTIAL

1. Implemented
- ...

2. Architecture decisions
- ...

3. Files created/modified
- ...

4. ML verification
- encoder accuracy:
- episode configuration:
- memory behavior:
- chance baseline:
- episode accuracy:
- parameter delta:
- memory delta:
- conflict-test outcome:

5. Tests executed
Command:
Result:
...

6. Requirement checklist
Requirement ID | Status | Evidence

7. Known limitations
- ...

8. Unresolved items
- ...

9. Git status / commit
- ...

10. Phase gate
Phase 1 = COMPLETE / INCOMPLETE
Phase 2 = NOT STARTED

FINAL SENTENCE:

"Stopped after Phase 1 as instructed. Awaiting explicit instruction to initiate
the next phase."

Then STOP.

===============================================================================
PHASE 2 — INTERACTIVE EDUCATIONAL PRODUCT AND LIVE DEMO
===============================================================================

DO NOT EXECUTE PHASE 2 UNTIL USER EXPLICITLY ASKS.

GOAL:

Turn the verified ML engine into an excellent interactive Streamlit learning
experience suitable for a live DataForge demonstration.

-------------------------------------------------------------------------------
PHASE 2A — STREAMLIT EXPERIENCE
-------------------------------------------------------------------------------

Build the Streamlit UI while keeping ML code in src/.

Suggested structure:

1. Hero / central claim
2. Guided explanation
3. Current episode
4. Demonstrations
5. Fast-memory visualization
6. Query/prediction
7. What changed?
8. Playground
9. Break the memory
10. Clear memory
11. Research/BDH transition placeholder or preliminary section
12. 60-second learner test

The initial page must open with a meaningful preset already running.

Avoid:
blank screen + "Run experiment".

-------------------------------------------------------------------------------
PHASE 2B — PRESENTATION-FIRST UX
-------------------------------------------------------------------------------

The app must be usable by a presenter without typing code.

Important interactions should be one click.

Provide:
- New Episode
- Add/Teach Demonstrations
- Test Query
- Inject Conflict
- Clear Memory

Keep controls minimal.

Use clear visual hierarchy.

The live-demo path should be obvious even to someone seeing it for the first
time.

-------------------------------------------------------------------------------
PHASE 2C — FAST MEMORY VISUALIZATION
-------------------------------------------------------------------------------

Visualize the actual memory tensor.

Prefer Plotly heatmap or similarly truthful visualization.

Show:
- before;
- after demonstrations;
- after conflict;
- after reset.

Use the real tensor.

Never use a decorative fake matrix.

-------------------------------------------------------------------------------
PHASE 2D — EMBEDDING / RETRIEVAL VISUALIZATION
-------------------------------------------------------------------------------

Show enough information to understand retrieval without overwhelming user.

Possible:
- similarity/scores by episode label;
- embedding vector summary;
- retrieved association strengths.

Use actual values.

Do not imply calibrated probabilities unless they really are calibrated.

If scores are normalized only for display, label them accurately.

-------------------------------------------------------------------------------
PHASE 2E — WHAT CHANGED PANEL
-------------------------------------------------------------------------------

Show prominently:

PERMANENT ENCODER
Parameter delta: 0
Status: Frozen

FAST MEMORY
Memory delta: <actual value>
Status: Updated

This must be backed by real calculations.

-------------------------------------------------------------------------------
PHASE 2F — DEMONSTRATION COUNT EXPERIMENT
-------------------------------------------------------------------------------

Allow meaningful adjustment of shots per class.

Learner should observe:
- changed memory;
- changed model results;
- actual measured accuracy if enough evaluation samples exist.

Do not prewrite an expected accuracy curve.

-------------------------------------------------------------------------------
PHASE 2G — CONFLICT FAILURE MODE
-------------------------------------------------------------------------------

Interactive action:

Inject conflicting demonstration.

Show:
- conflict;
- memory change;
- before/after prediction or aggregate result;
- limitation explanation.

This should explicitly teach that rapidly writable memory can also rapidly
accept incorrect associations.

-------------------------------------------------------------------------------
PHASE 2H — RESET EXPERIMENT
-------------------------------------------------------------------------------

Clear memory.

Verify:
- memory reset;
- encoder unchanged;
- episodic associations removed.

Visually demonstrate it.

-------------------------------------------------------------------------------
PHASE 2I — ACCESSIBILITY AND DESIGN
-------------------------------------------------------------------------------

Do not encode meaning by color alone.

Use:
- text labels;
- icons where useful;
- adequate contrast;
- readable fonts;
- responsive layout;
- concise prose.

Avoid giant paragraphs.

Avoid excessive animations.

-------------------------------------------------------------------------------
PHASE 2J — PERFORMANCE
-------------------------------------------------------------------------------

Precompute held-out embeddings if necessary.

Measure actual interaction latency.

Target:
normal memory interactions approximately <1 second after load on development
hardware.

Record measurements honestly.

Do not claim universal latency.

-------------------------------------------------------------------------------
PHASE 2K — LEARNING TEST
-------------------------------------------------------------------------------

Implement a brief interactive quiz or prediction activity.

It should verify understanding of:
- frozen weights;
- changing fast state;
- temporary versus permanent adaptation;
- failure case.

Provide immediate feedback.

-------------------------------------------------------------------------------
PHASE 2L — UI TESTING
-------------------------------------------------------------------------------

Test:
- clean startup;
- preset works;
- new episode;
- changing shots;
- teach;
- query;
- conflict;
- reset;
- repeat interaction;
- invalid states;
- app reload;
- no crashes;
- no hidden model retraining;
- visualizations match underlying tensors.

Add automated tests where practical.

Perform manual smoke walkthrough.

-------------------------------------------------------------------------------
PHASE 2 ACCEPTANCE GATE
-------------------------------------------------------------------------------

Cannot pass until:

[ ] app starts successfully;
[ ] preset appears immediately;
[ ] core claim visible;
[ ] live demonstrations can be added;
[ ] real fast memory visualized;
[ ] query gives real model output;
[ ] ground truth shown;
[ ] parameter delta shown;
[ ] memory delta shown;
[ ] shots experiment works;
[ ] conflict experiment works;
[ ] reset works;
[ ] learner quiz works;
[ ] normal path is presentation-ready;
[ ] feedback performance measured;
[ ] all Phase 1 tests still pass;
[ ] Phase 2 tests pass;
[ ] requirement matrix updated.

Then produce the same formal phase report and STOP.

===============================================================================
PHASE 3 — RESEARCH INTEGRATION, BDH MODULE, EVIDENCE AND ROBUSTNESS
===============================================================================

DO NOT EXECUTE UNTIL USER EXPLICITLY ASKS.

GOAL:

Transform the working prototype into a scientifically grounded competition
submission.

-------------------------------------------------------------------------------
PHASE 3A — PRIMARY RESEARCH
-------------------------------------------------------------------------------

Identify and verify at least three primary research papers from 2022–2026
directly relevant to:
- associative memory;
- fast weights;
- fast-weight memory;
- inference-time associative state;
- related modern architectures.

Also obtain primary BDH resources where possible:
- Dragon Hatchling paper;
- BDH-CQ technical report where relevant;
- official toy implementation where relevant;
- other official Pathway research material where primary/authoritative.

DO NOT use blogs as the sole basis for technical claims when primary sources
exist.

For every technical claim record:
Claim
Source
Evidence type
Publication date
Primary/secondary
Limitations

Do not fabricate inaccessible evidence.

-------------------------------------------------------------------------------
PHASE 3B — BDH LEARNING MODULE
-------------------------------------------------------------------------------

Integrate BDH naturally.

Suggested flow:

"What you just observed"

Frozen slow representation
+
rapidly changing associative state

↓

"How does this connect to frontier architectures?"

Explain the connection supported by primary sources.

Clearly distinguish:

MemoryForge:
educational toy associative-memory system.

BDH:
published architecture with its own mathematical/computational design.

Do not claim architectural equivalence.

Explain:
- what part of the concept genuinely connects;
- what MemoryForge simplifies;
- what cannot be demonstrated using this toy system.

BDH-CQ should only be discussed where directly relevant and supported.

If BDH-CQ does not have a direct role in a specific statement, say so.

-------------------------------------------------------------------------------
PHASE 3C — TECHNICAL EXPLANATION
-------------------------------------------------------------------------------

Include a concise derivation/visual:

Demonstration:
(k, v)

Hebbian-style memory write:
M ← M + v k^T

Query:
scores = Mq

Explain:
- k;
- v;
- M;
- q;
- normalization;
- multiple-shot handling.

Every equation must match actual implementation.

-------------------------------------------------------------------------------
PHASE 3D — EVIDENCE SUITE
-------------------------------------------------------------------------------

Create reproducible experiments across:
- multiple random seeds;
- varying shots;
- clean episodes;
- corrupted demonstrations.

Record:
- mean accuracy;
- standard deviation;
- chance baseline;
- memory delta;
- parameter delta;
- latency where useful.

Save raw results in a reproducible data format.

Charts must be generated from those results.

No invented numbers.

-------------------------------------------------------------------------------
PHASE 3E — LIMITATIONS
-------------------------------------------------------------------------------

Explicitly disclose at least:

- encoder learned digit representations during ordinary supervised training;
- fast memory learns episode-specific associations, not visual concepts from
  scratch;
- sklearn digits is small/simple;
- MemoryForge is an educational demonstration;
- no claim that it reproduces BDH;
- temporary memory is cleared between episodes unless intentionally retained;
- label score normalization may not represent calibrated probability;
- conflicting demonstrations can interfere;
- conclusions should not be generalized to large language models without
  evidence.

Add any newly discovered limitations.

-------------------------------------------------------------------------------
PHASE 3F — TECHNICAL OWNERSHIP DOCUMENT
-------------------------------------------------------------------------------

Create something like:

docs/TECHNICAL_WALKTHROUGH.md

Explain:
- full data flow;
- encoder;
- training;
- embeddings;
- memory equations;
- episode mapping;
- retrieval;
- metrics;
- visualizations;
- limitations;
- likely judge questions.

Goal:
team should be able to defend every major component.

-------------------------------------------------------------------------------
PHASE 3G — RESEARCH CITATIONS IN APP
-------------------------------------------------------------------------------

Technical claims shown in UI must have nearby citations or source references.

Do not clutter the teaching flow.

Use expandable source sections where useful.

-------------------------------------------------------------------------------
PHASE 3H — ROBUSTNESS
-------------------------------------------------------------------------------

Test:
- clean install;
- cold startup;
- missing model artifact behavior;
- regenerate artifact;
- multiple random seeds;
- unusual shot counts;
- repeated reset;
- repeated conflicts;
- no network;
- CPU-only run.

All earlier tests must remain green.

-------------------------------------------------------------------------------
PHASE 3 ACCEPTANCE GATE
-------------------------------------------------------------------------------

Cannot pass until:

[ ] 3+ qualifying recent primary papers verified;
[ ] BDH primary sources recorded;
[ ] technical claims sourced;
[ ] BDH module integrated;
[ ] no false equivalence with MemoryForge;
[ ] equations match code;
[ ] reproducible evidence suite exists;
[ ] experiment results stored;
[ ] charts use actual data;
[ ] limitations comprehensive;
[ ] technical walkthrough exists;
[ ] all tests pass;
[ ] requirements matrix updated.

Then report and STOP.

===============================================================================
PHASE 4 — SUBMISSION HARDENING, DEPLOYMENT AND FINAL AUDIT
===============================================================================

DO NOT EXECUTE UNTIL USER EXPLICITLY ASKS.

GOAL:

Produce a submission-ready artifact and documentation package.

-------------------------------------------------------------------------------
PHASE 4A — README
-------------------------------------------------------------------------------

README must include:

1. project title;
2. one-sentence claim;
3. problem;
4. learner/audience;
5. prerequisites;
6. learning objectives;
7. architecture;
8. ML methodology;
9. fast-memory equation;
10. how arbitrary episode mappings work;
11. app features;
12. installation;
13. run instructions;
14. encoder training/reproduction;
15. evaluation reproduction;
16. live versus precomputed components;
17. data source;
18. model artifact source;
19. research sources;
20. BDH connection;
21. limitations;
22. AI assistance;
23. licenses/provenance;
24. deployment URL;
25. repository URL;
26. credits.

README claims must be defensible.

-------------------------------------------------------------------------------
PHASE 4B — PROVENANCE
-------------------------------------------------------------------------------

Create/update docs/PROVENANCE.md.

Track:
- sklearn digits;
- PyTorch;
- NumPy;
- Streamlit;
- Plotly;
- code;
- data;
- model weights;
- images;
- icons;
- fonts;
- research figures if reused;
- any external assets.

For each:
Source
License
Modification
Location

Never guess a license.

If uncertain:
mark unresolved before final submission.

-------------------------------------------------------------------------------
PHASE 4C — AI DISCLOSURE
-------------------------------------------------------------------------------

Complete docs/AI_ASSISTANCE.md.

Be transparent but concise.

Mention that Codex assisted development.

Describe team review/testing/ownership.

-------------------------------------------------------------------------------
PHASE 4D — CONCEPT SUMMARY
-------------------------------------------------------------------------------

Prepare a one-page concept summary source and PDF.

Target approximately:
500–950 words.

It must be:
- self-contained;
- technically correct;
- accessible to an average data scientist;
- information dense;
- free of promotional filler.

It should include:
- central claim;
- problem/design pressure;
- mechanism;
- relation to conventional alternatives;
- MemoryForge experiment;
- BDH connection;
- representative systems/research;
- evidence;
- trade-offs;
- limitations;
- maturity/evidence distinctions;
- primary references.

Do NOT produce:
- AI slop;
- buzzword padding;
- a list of papers with no synthesis;
- unsupported benchmark claims.

Every sentence should contribute meaning.

-------------------------------------------------------------------------------
PHASE 4E — BLOG PDF AMBIGUITY
-------------------------------------------------------------------------------

Check actual submission instructions if available.

The provided Pathway PDF refers to a blog PDF but does not fully define a
separate blog format in the supplied text.

Do not silently invent one.

If portal requirements clarify it:
produce exactly what is required.

Otherwise:
prepare a clearly labelled draft and flag it for human confirmation.

-------------------------------------------------------------------------------
PHASE 4F — DEPLOYMENT
-------------------------------------------------------------------------------

Target a simple public deployment such as Streamlit Community Cloud or another
compatible service.

Requirements:

- URL opens without sign-in;
- no secrets;
- stable dependencies;
- app cold-start behavior acceptable;
- model artifact available;
- public link tested.

If Codex does not have credentials or permission to deploy:
do NOT pretend deployment happened.

Instead:
- prepare deployment files;
- verify locally;
- provide exact human steps;
- mark URL requirement UNVERIFIED until user completes it.

-------------------------------------------------------------------------------
PHASE 4G — DEMO SCRIPT
-------------------------------------------------------------------------------

Prepare a concise competition demo.

Ideal flow:

1. state claim;
2. show random episode mapping;
3. show frozen encoder;
4. teach demonstrations;
5. show memory changing;
6. query unseen image;
7. prediction vs truth;
8. parameter delta = 0;
9. memory delta > 0;
10. add more demonstrations;
11. inject conflict;
12. show failure;
13. clear memory;
14. connect to BDH;
15. state limitation.

The central claim should be reproducible within roughly one minute.

-------------------------------------------------------------------------------
PHASE 4H — FINAL REQUIREMENTS AUDIT
-------------------------------------------------------------------------------

Audit every competition requirement and every project requirement.

For each requirement:
PASS
FAIL
UNVERIFIED
NOT APPLICABLE

and evidence.

Never convert UNVERIFIED to PASS because the deadline is close.

-------------------------------------------------------------------------------
PHASE 4I — JUDGING RUBRIC AUDIT
-------------------------------------------------------------------------------

Evaluate submission against:

Technical correctness — /25
Technical ownership — /15
Learning effectiveness — /15
Interactive substrate/honesty — /15
BDH integration/evidence — /10
Craft/robustness/provenance — /10
Concept summary — /10

For each:
- strengths;
- weaknesses;
- evidence;
- last-minute fix if worthwhile.

Do not invent a guaranteed score.

-------------------------------------------------------------------------------
PHASE 4J — FINAL CLEANUP
-------------------------------------------------------------------------------

Check:
- dead code;
- unused assets;
- broken links;
- TODOs;
- secrets;
- cached files;
- unnecessary binaries;
- temporary debugging outputs;
- notebook garbage;
- dependency pins;
- README links;
- app startup;
- tests;
- model artifact;
- source references.

Do NOT delete something merely because it seems unfamiliar.

-------------------------------------------------------------------------------
PHASE 4K — FINAL TEST
-------------------------------------------------------------------------------

From a clean environment where practical:

install
train/load
evaluate
test
start app

Verify end-to-end.

-------------------------------------------------------------------------------
PHASE 4L — FINAL REPORT
-------------------------------------------------------------------------------

Produce:

DATAFORGE SUBMISSION READINESS REPORT

Overall readiness:
READY / NOT READY / READY WITH MANUAL ACTIONS

Public artifact:
status

Repository:
status

Tests:
status

Research sources:
status

BDH module:
status

Concept summary:
status

Blog/written deliverable:
status

Provenance:
status

AI disclosure:
status

Known limitations:
...

Manual actions still required:
...

Competition requirement matrix:
...

Then STOP.

===============================================================================
SECTION 14 — FUTURE RESUME ROADMAP
===============================================================================

Because this project should remain valuable after DataForge, maintain:

docs/FUTURE_ROADMAP.md

DO NOT implement these before the deadline unless all competition-critical work
is already complete.

Potential post-hackathon extensions:

- Omniglot few-shot learning;
- Fashion-MNIST;
- CIFAR embeddings;
- modern Hopfield networks;
- learnable memory rules;
- attention versus associative memory comparison;
- meta-learning;
- prototypical networks;
- memory consolidation;
- continual learning;
- larger embedding models;
- interference/capacity experiments;
- memory retrieval benchmarking;
- GPU support;
- richer research visualizations;
- packaged Python library.

Keep deadline build intentionally narrow.

===============================================================================
SECTION 15 — PROHIBITED BEHAVIORS
===============================================================================

Never:

- skip phases;
- automatically begin next phase;
- claim tests passed when they were not run;
- invent benchmark results;
- invent citations;
- invent licenses;
- invent deployment URLs;
- invent BDH behavior;
- claim MemoryForge is BDH;
- hard-code successful predictions;
- create fake charts;
- silently use query samples for training;
- allow model parameters to update during fast-memory adaptation;
- replace functioning previous-phase code without justification;
- expose secrets;
- hide known limitations;
- prioritize aesthetics over correctness;
- add broad features merely to appear impressive.

===============================================================================
SECTION 16 — FIRST EXECUTION INSTRUCTION
===============================================================================

You have now been given the COMPLETE development roadmap.

Read and understand ALL FOUR phases.

However:

YOU MUST NOW EXECUTE PHASE 1 ONLY.

Do not:
- implement Streamlit final UI;
- implement Phase 2;
- implement research integration;
- implement Phase 3;
- prepare final submission PDFs;
- deploy;
- execute Phase 4.

You may create planning placeholders required for continuity, but do not perform
future-phase implementation.

Proceed in this order:

1. inspect repository;
2. summarize your understanding internally;
3. inspect existing implementation;
4. establish Phase 1 requirement matrix;
5. implement Phase 1;
6. test Phase 1;
7. fix failures;
8. rerun tests;
9. verify each Phase 1 acceptance criterion individually;
10. update persistent docs;
11. provide Phase 1 completion report;
12. STOP.

If anything prevents Phase 1 completion:
explain exactly what remains and why.

Do not weaken requirements simply to mark the phase complete.

After the completion report your final line must be:

"Stopped after Phase 1 as instructed. Awaiting explicit instruction to initiate
the next phase."