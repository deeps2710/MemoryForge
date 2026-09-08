# Future scope and sustainability options

Prepared for the user's requested DataForge 2026 presentation redesign on
2026-09-08. This document proposes work; it does not initiate implementation or
report existing services, customers, revenue, partnerships or production readiness.

The current contribution is a working CPU teaching prototype with an inspectable
fast-memory rule, exact encoder audits, a guided UI and reproducible evidence.
The intended educational benefit is mechanistic understanding. No learner study
has yet measured whether the app improves that understanding.

## Research and scale

- Compare additive class means with alternative update rules at a fixed label-noise fraction.
- Vary label count and embedding dimension; measure interference and capacity.
- Evaluate unfamiliar categories using a disclosed training/evaluation protocol.
- Test learning outcomes and concurrent classroom sessions before claiming broader utility.

The present core stores S of shape 3 x 16 and c of shape 3 in float64:
(3*16+3)*8 = 408 raw bytes. For C labels and d features, sums/counts require
O(Cd) storage and the dense read/write operations grow with C and d. This excludes
encoder storage, cached keys, derived matrices, transition snapshots and Python
objects. It does not imply 408 bytes of total app memory or validated deployment
capacity. The [full DFD](DATA_FLOW.md) describes all stores.

## Potential sustainability

Keep the educational core openly available under its scoped license. Test demand
for paid workshops, course integration support or managed classroom hosting.
A viable offering would need learner evidence, facilitator time, hosting and
support cost estimates, reliability checks and clear data/privacy handling for
any future classroom features. Pricing would follow those studies.

The prototype currently has no implemented billing, classroom account system or
commercial service. The proposal assigns no market size or revenue forecast.
The detailed [limitations](LIMITATIONS.md) and [gated roadmap](FUTURE_ROADMAP.md)
remain the boundaries of the actual project.
