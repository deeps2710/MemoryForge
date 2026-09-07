# Fast-weight associative memory

MemoryForge | One-page concept summary

## Central claim and design pressure

**Temporary associations can change while every long-term encoder parameter stays fixed.** MemoryForge tests this claim in a CPU learning lab: teach arbitrary digit symbols, query unseen images, inject a wrong label, then clear memory. The contribution is a reproducible teaching substrate, not a new architecture. [5]

A conventional Transformer also responds to context without retraining: attention matches queries against token keys and combines values. [1] Fast-weight memory instead accumulates associations into writable state. Compression can bound state size, but associations can interfere. [2] The distinction concerns which state changes and how it is read.

## Mechanism and what actually learns

MemoryForge trains a 64-32-16 encoder and digit-classification head on 1,347 images; 450 are held out. Each episode randomly maps three digit identities to ALPHA, BETA and GAMMA. Demonstrations and queries use distinct held-out rows. The digit head never predicts these symbols: the encoder recognizes familiar categories while memory learns their temporary names. [5]

For a demonstration, k is a unit-length, 16-component embedding and v is its three-component one-hot symbol. S stores key sums; c counts writes by symbol. A query supplies another unit vector q:

```equation
S <- S + v k^T       c <- c + v
M[i] = S[i] / c[i]   when c[i] > 0
scores = M q
```

The outer product adds k to one row; division by c averages its demonstrations. Class means are not renormalized. The highest written-label score wins; empty memory abstains. Scores are similarities, not calibrated probabilities. No optimizer runs during adaptation. Actual matrices, scores, truth and exact encoder-tensor comparisons are visible. Reset removes associations, preserving pretrained representations. [5]

All 650 evaluated conditions replay exactly, with encoder delta zero. [5]

<!-- column -->

## Evidence and its scope

Across 50 seeds with fixed queries per seed, clean mean accuracy is 94.07% at one demonstration per class and 98.07% at ten; population standard deviations are 6.37 and 2.67 percentage points. Three appended wrong-label writes reduce those means to 84.47% and 97.27%. Chance is 33.33%. [5]

The 19,500 query outcomes reuse images; they are not independent trials. These are reproducible developer measurements, not an external evaluation or deployment. Random labels test association learning, not discovery of visual concepts. [5]

## Research connections, without equivalence

| System | Changing state |
|---|---|
| DeltaNet [2] | Matrix updated through retrieval-error correction. |
| BDH [3] | Hebbian synaptic state; fixed graph connections. |
| BDH-CQ [4] | Context memory, then a separate reasoning workspace. |

BDH motivates separating learned structure from associative state. BDH-CQ adds iterative query computation; MemoryForge has no such workspace. CQ's exact updates and dimensions remain proprietary. Neither system is implemented by this toy or needed to derive its class-average rule. [3] [4]

DeltaNet reports MAD In-Context Recall of 100% (Transformer: 94.1%), but Memorize of 52.8% (85.2%). Table 1 uses baseline scores from prior work. This developer-reported synthetic benchmark supports task-specific trade-offs, not independent reproduction or deployment. [2]

## Most important missing evidence

Transfer to unfamiliar categories, larger memories or language remains untested. Small digits, targeted repeated-key corruption and overlapping episodes constrain the result. The next scientific question is how memory capacity and update choice affect interference under broader, controlled evaluations. MemoryForge establishes an inspectable state update, not general reasoning performance. [5]

<!-- references -->

## Primary sources and continuation

[1] Vaswani et al. *Attention Is All You Need* (2017), section 3.2. arXiv:1706.03762v7.

[2] Yang et al. *DeltaNet* (NeurIPS 2024), sections 2.2, 4.1; Table 1. arXiv:2406.06484v3.

[3] Kosowski et al. *The Dragon Hatchling* (2025 preprint), sections 1.2, 2.2. arXiv:2509.26507v1.

[4] Engdahl et al. *BDH-CQ: In-Context Learning with Recurrent Latent Reasoning* (2026 report), section 3. arXiv:2608.09888v1.

[5] MemoryForge, implementation f3ec52e: source, raw evaluation and technical walkthrough at github.com/deeps2710/MemoryForge.

[1]: https://arxiv.org/html/1706.03762v7
[2]: https://arxiv.org/html/2406.06484v3
[3]: https://arxiv.org/html/2509.26507v1
[4]: https://arxiv.org/html/2608.09888v1
[5]: https://github.com/deeps2710/MemoryForge/tree/f3ec52e60c999d60f8ea89c2f7c243eaa89c1bac
