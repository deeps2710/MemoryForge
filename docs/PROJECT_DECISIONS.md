# Project decisions

Central claim: “A neural system can rapidly learn new associations by updating
temporary fast-weight memory while keeping its long-term model parameters unchanged.”

Scope: DataForge 2026 Pathway Track, Associative Memory and Fast Weights.
MemoryForge is an educational fast-weight associative-memory model used to
demonstrate the concept. It is not an implementation or reproduction of BDH.
Competition constraints are captured from the supplied development brief; the
actual organizer PDF/portal has not been provided or independently verified.

## D-01 — Dataset and split
Decision: bundled sklearn digits, float32 inputs divided by 16, stratified
75% train / 25% held-out split with seed 42. Preserve original dataset row IDs.
Reason: tiny CPU experiment without a dataset download; explicit leakage checks.
Alternatives considered: MNIST, Omniglot, random unstratified splits.
Consequences: digit identities occur in training and evaluation; held-out images
are unseen, not novel visual classes. Demo and query rows are distinct within
each episode; different episodes may reuse held-out rows.
Phase introduced: 1.

## D-02 — Slow encoder
Decision: Linear(64,32), ReLU, Linear(32,16); train with a Linear(16,10) head
using cross entropy and Adam, CPU, fixed epochs and seeded shuffling.
Reason: matches the brief and keeps computation explainable.
Alternatives considered: CNN, pretrained external model, handcrafted embeddings.
Consequences: supervised digit representations precede fast adaptation. Retain
head tensors only in the checkpoint for sanity evaluation; episodic code uses
only the frozen encoder. No early stopping or tuning on held-out queries.
Phase introduced: 1.

## D-03 — Memory and normalization
Decision: normalize nonzero keys and queries to unit L2 length. Store raw sums
S <- S + v k^T and class counts c <- c + v. Retrieval matrix M_i = S_i / c_i
when c_i > 0, otherwise zero. Query scores = M q.
Reason: transparent Hebbian accumulation with fair scaling for multiple shots.
Alternatives considered: unnormalized sums, attention, learned update rules.
Consequences: class-mean vectors are not renormalized. Snapshots expose raw sums,
counts AND the exact retrieval matrix. Softmax is a display score, not calibrated
probability. Unwritten classes are masked; empty memory abstains (prediction -1),
returns zero raw scores and uniform display scores. Exact score ties choose the
first written label by index and expose a tie flag.
Phase introduced: 1.

## D-04 — Episodes and evidence
Decision: default 3-way, 5 shots/class, 10 queries/class, arbitrary randomly
permuted ALPHA/BETA/GAMMA labels. Evaluate 50 fixed seeds starting at 1000.
Reason: test temporary label associations separately from ordinary digit labels.
Alternatives considered: fixed digit-label assignments; extra baselines.
Consequences: chance reference is analytic 1/N; overlapping episodes are not
independent dataset draws. Record all row IDs, mappings, predictions, states,
scores and exact tensor deltas. Conflict repeats one support key with a wrong
episode label once; measure the effect without requiring accuracy to fall.
Phase introduced: 1.

## D-05 — Phase boundary and dependencies
Decision: Python core, NumPy, sklearn, PyTorch, pytest only in Phase 1. Streamlit
and Plotly remain planned for Phase 2. No secrets or external service needed.
Reason: verified core first, per explicit user phase gate.
Alternatives considered: building UI concurrently, React/FastAPI, paid APIs.
Consequences: no app.py or empty UI stubs, no research module, PDFs or deployment.
Phase introduced: 1.

## D-06 — Runtime compatibility and verification evidence
Decision: execute in an isolated Windows Python 3.12.14 environment; retain
Python 3.11-compatible syntax and pin SciPy 1.15.3, joblib 1.4.2 and threadpoolctl
3.6.0 alongside the direct dependencies. Record the installed environment.
Reason: the machine has no Python on PATH; unconstrained SciPy resolved to a
Python 3.12+ build, so pin the numerical stack compatible with 3.11 as well.
Alternatives considered: requiring 3.12 everywhere, modifying the shared runtime.
Consequences: actual 3.11 execution remains unverified; deterministic claims apply
to the tested environment. Repeat final training/evaluation/tests after pinning.
Phase introduced: 1.
