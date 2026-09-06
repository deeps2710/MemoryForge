# MemoryForge

**Interactive Few-Shot Learning with Fast-Weight Associative Memory**

> A neural system can rapidly learn new associations by updating temporary
> fast-weight memory while keeping its long-term model parameters unchanged.

MemoryForge makes this claim testable with real CPU computation. A small neural
encoder learns digit representations once. Demonstrations then teach temporary,
randomly assigned labels such as ALPHA, BETA and GAMMA using an associative
memory. New held-out images query that memory. Encoder tensors are checked for
exact equality before and after adaptation.

**Phase 1: verified ML core. Phase 2: not started.** The interactive Streamlit
experience is the next gated phase; there is no app or deployment yet.
MemoryForge is an educational fast-weight associative-memory model used to
demonstrate the concept. It does not implement or reproduce BDH or BDH-CQ.

[Repository](https://github.com/deeps2710/MemoryForge) ·
[Phase status](docs/PHASE_STATUS.md) · [Completion report](docs/PHASE_1_REPORT.md) ·
[Requirement evidence](docs/REQUIREMENTS_MATRIX.md)

## Audience and learning objectives

For early ML learners and data scientists familiar with basic neural networks,
vectors, classification and embeddings. The intended learning experience teaches
learners to distinguish frozen slow weights from writable temporary memory;
create and inspect an association; query an unseen image; test the effects of
more demonstrations, conflicting labels and reset; and explain why temporary
adaptation is useful but differs from permanent training. The sourced research
connection to BDH and learner-facing activities belong to later phases.

## Run the verified core

Python 3.11-compatible source and numerical dependency pins; tested on Windows
with Python 3.12.14 and CPU PyTorch. Start in the repository root. A Python
installation must be available as `python` (or substitute its executable path).

```sh
python -m venv .venv
```

Activate with `.venv\Scripts\Activate.ps1` in PowerShell, or
`source .venv/bin/activate` on macOS/Linux. If PowerShell activation is restricted,
replace `python` below with `.\.venv\Scripts\python.exe`; activation is optional.

```sh
# Windows/Linux CPU wheel; install this first to avoid unnecessary GPU packages.
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python -m pip check

# The small checked-in checkpoint can be loaded immediately.
python scripts/smoke_test.py
python scripts/evaluate_core.py
python -m pytest -q

# Reproduce training explicitly; never triggered by evaluation or import.
python scripts/train_encoder.py

# Run the entire default benchmark twice and compare all recorded evidence.
python scripts/verify_replay.py
```

On macOS, install `torch==2.6.0` from the default PyPI index instead of the CPU
wheel index; this project still places every tensor on CPU. macOS/Linux and an
actual Python 3.11 runtime are not verified in this Phase 1 report.

Dependency installation needs network access. Digits is bundled in scikit-learn;
training, evaluation and tests make no dataset/API network requests and require
no API keys. Missing weights produce an actionable error instructing you to run
the training script, with no automatic retraining.

Optional episode settings:

```sh
python scripts/evaluate_core.py --episodes 50 --n-way 3 --shots 5 --queries 10 --seed 1000
python scripts/evaluate_core.py --shots 1 --output artifacts/replay-one-shot.json
python scripts/train_encoder.py --seed 42 --split-seed 42 --output artifacts/encoder.pt
```

The split seed must match the checkpoint. For an encoder trained with another
split seed, also pass `--split-seed` to `evaluate_core.py`. Select 2–10 labels and
positive shot/query counts that fit the chosen classes' held-out pools; invalid
or impossible requests fail clearly.

## Mechanism

1. Load 1,797 bundled 8×8 digits; divide pixels by 16. Stratify original row IDs
   into 1,347 training and 450 held-out images using split seed 42.
2. Train `64 → Linear(32) → ReLU → Linear(16)` plus a ten-digit classification
   head for 100 fixed epochs using training rows only. Freeze the encoder.
3. Select three digit classes and separately permute their arbitrary episode
   labels. Support and query images are distinct, drawn only from held-out rows.
4. Use normalized encoder embeddings as keys and one-hot episode labels as values.
5. Write support keys to temporary memory, query new keys, inject one wrong-label
   support association, and clear memory. Record real states and predictions.

The outer-product rule with explicit class-wise averaging is:

```text
S ← S + v kᵀ
c ← c + v
M[i] = S[i] / c[i] if c[i] > 0, else 0
scores = M q
```

Here `k` and `q` are unit embeddings, `v` is a one-hot episode label, `S` stores
sums, `c` counts writes, and `M` is the actual retrieval matrix. The ordinary digit
head is retained only for sanity evaluation; it never predicts episode labels.

`FastMemory` exposes `reset`, `write`, `write_batch`, `query`, `state_snapshot`,
`memory_delta` and `statistics`. Snapshots include raw sums, counts and the exact
retrieval matrix. Empty memory abstains (`prediction = -1`); the analytic `1/N`
chance baseline is the expected accuracy of uniform random guessing. Softmax
display scores are not calibrated probabilities. Unwritten labels cannot win;
exact ties among written labels use the first label index and are flagged.

## Measured Phase 1 evidence

Default checkpoint and seeds 1000–1049; 3-way, 5 shots/class, 10 queries/class:

| Measurement | Result |
|---|---:|
| Held-out ordinary digit sanity accuracy | 97.11% (437/450) |
| Mean episode accuracy | 97.53% |
| Episode population standard deviation | 3.11 percentage points |
| Chance reference | 33.33% |
| Evaluated queries | 1,500 across 50 episodes |
| Maximum encoder parameter delta | **0**, exact tensor equality |
| Minimum / mean clean memory delta | 1.51549 / 1.59116 |
| Accuracy after one wrong-label write per episode | 97.00% |
| Predictions changed by conflicts | 19/1,500 |

These are measured internal validation results, not competition thresholds.
Episodes may reuse held-out images and are not independent dataset draws.
The conflict can improve, worsen or leave a particular episode's accuracy
unchanged; the engine logs its actual effect.

`artifacts/encoder.pt` is locally trained, not an external pretrained model.
`encoder.training.json` records training seeds/configuration and sanity accuracy.
`evaluation.json` contains every mapping, sample ID, embedding, memory state,
query score, prediction and ground truth. `reproducibility.json` records two-run
exact comparison. `environment.json` and `verification.json` record the verified
environment and executed commands. No charts or scripted predictions are used.

## Project layout

```text
src/          independent data, encoder, episodes, memory and evaluation modules
scripts/      explicit train, evaluate, smoke and replay commands
tests/        handcrafted math, unit, integration and deterministic replay tests
artifacts/    small checkpoint and actual reproducible evidence
docs/         architecture, decisions, phase gate, requirements and disclosures
```

The pre-existing unrelated `html` file is preserved and is not an application
entry point. See [architecture](docs/ARCHITECTURE.md) for equations and data flow,
and [decisions](docs/PROJECT_DECISIONS.md) for reasons and alternatives.

## Scope, sources and ownership

The encoder has already learned these digit identities. Fast adaptation learns
temporary label assignments, not visual categories from scratch. The small data
and simple class-mean memory do not establish claims about large models, memory
capacity or continual learning. See [limitations](docs/LIMITATIONS.md).

Data: Alpaydin and Kaynak's *Optical Recognition of Handwritten Digits* via the
scikit-learn bundled subset. Its original UCI page lists CC BY 4.0; attribution,
modifications and license evidence are in [provenance](docs/PROVENANCE.md).
The team has not yet selected licenses for project code and generated weights.

Codex assisted implementation, tests, evaluation and documentation; see
[AI assistance](docs/AI_ASSISTANCE.md). Team review and technical ownership remain
required. Recent primary papers and BDH claims will be verified in Phase 3;
[research handoff](docs/RESEARCH_NOTES.md) contains the evidence TODOs.

This project targets DataForge 2026's Pathway Track according to the supplied
brief. The actual organizer PDF/portal has not been independently verified.
Public deployment and submission PDFs belong to Phase 4. Whether a blog PDF is
separate from the one-page concept summary remains an explicit unresolved item.
See the [gated roadmap](docs/FUTURE_ROADMAP.md) and
[full supplied development brief](docs/DEVELOPMENT_BRIEF.md).

Further phases require explicit user instruction. No next phase starts automatically.
