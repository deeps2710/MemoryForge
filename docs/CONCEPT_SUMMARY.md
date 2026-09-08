# MemoryForge

Associative Memory & Fast Weights
DataForge 2026 / PS-1 - Pathway / Team BitWise

## The claim and the problem

**Temporary associations can change while every long-term encoder parameter remains fixed.** MemoryForge tests this claim through teaching, held-out queries, contradictory labels and reset. A changed prediction alone cannot identify what learned; the CPU lab exposes the changing state and audits the frozen tensors. [5]

Fast associative memory compresses key-value relationships into writable state. Compared with retaining token keys and values for attention, fixed-size state can bound storage but introduce interference. The update rule determines how associations accumulate or compete. [3]

## Mechanism and contribution

A 64-32-16 encoder trains on 1,347 digit images, then freezes. Episodes draw distinct supports and queries from 450 held-out images, randomly mapping three familiar digit identities to ALPHA, BETA and GAMMA. The digit head never predicts these temporary names. [5]

For unit keys k and q, one-hot label v, key sums S and counts c:

```equation
S <- S + v k^T
c <- c + v
M[i] = S[i]/c[i] if c[i]>0, else 0
scores = Mq
```

M holds class means without renormalization. The largest written-label score wins; empty memory abstains. Adaptation runs no optimizer. The contribution is a reproducible teaching substrate with actual writes, scores, before/after states and exact encoder comparisons. [5]

<!-- column -->

## Evidence and interpretation

Public seed 1000 shows encoder delta **0** and fast-memory delta **1.73205** from the empty matrix. Teaching a second support per class changes accuracy from 23/30 to 27/30. One wrong-label write gives 26/30 with five changed predictions. Reset restores abstention. [5]

Across 50 fixed seeds, clean mean accuracy is 94.07% at one support per class and 98.07% at ten. Three wrong-label writes give 84.47% and 97.27%. Encoder delta stays zero in all 650 conditions. The 19,500 outcomes reuse images: developer measurements, not independent trials or external evaluation. [5]

## The research connection

BDH separates fixed connections from dynamic Hebbian synaptic state. MemoryForge illustrates that distinction, without implementing BDH's graph or sequence architecture. [1] BDH-CQ adds iterative computation in a separate query workspace; its exact updates and dimensions remain proprietary. The lab has no such workspace. [2]

DeltaNet corrects retrieval error rather than merely adding associations. [3] Titans optimizes a neural memory at test time. [4] These alternatives show why the identity of the writable state and its update matter; their results cannot be transferred to this class-mean toy.

## The main missing evidence

Unfamiliar categories, larger memories, learner benefit and concurrent-session capacity remain untested. Repeated-key corruption changes the noise fraction across shot counts. Next studies should compare update rules at fixed corruption rates and assess whether learners can explain the state change. [5]

<!-- references -->

[1] Kosowski et al. *The Dragon Hatchling* (2025), sections 1.2, 2.2. arXiv:2509.26507v1.
[2] Engdahl et al. *BDH-CQ* (2026), sections 3.2-3.3. arXiv:2608.09888v1.
[3] Yang et al. *Parallelizing Linear Transformers with the Delta Rule over Sequence Length* (2024), sections 1-2. arXiv:2406.06484v3.
[4] Behrouz et al. *Titans: Learning to Memorize at Test Time* (2024/25), section 3. arXiv:2501.00663v1.
[5] MemoryForge source, raw evidence and walkthrough, revision 3751264. github.com/deeps2710/MemoryForge.
