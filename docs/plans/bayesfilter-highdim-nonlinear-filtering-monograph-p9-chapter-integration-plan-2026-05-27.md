# P9 Monograph Chapter Integration Plan

## Question

Do the chapter drafts form a coherent, reviewer-grade nonlinear filtering block?

## Evidence Contract

Baseline:

- P1-P8 outputs.
- Existing BayesFilter chapter conventions.

Primary criterion:

- The draft chapters are self-contained, use BayesFilter notation, include
  assumptions, algorithms, derivations, evidence boxes, limitations, and claim
  ledgers.
- Every chapter includes a per-claim source/evidence ledger, theorem or lemma
  provenance where applicable, unresolved-claim register, and "what is not
  concluded" section.

Veto diagnostics:

- Chapters rely on undefined production readiness.
- Chapters cite nonexistent BayesFilter evidence.
- Chapters introduce unsupported mathematical or empirical claims.

Explanatory diagnostics:

- Source-map entries and MathDevMCP derivation audits, after mandatory gates are
  satisfied.

Non-implications:

- Passing P9 does not mean the chapters are publication-final.

Artifacts:

- Chapter drafts `ch33` through `ch37`.
- `docs/source_map.yml` entry.

## Chapter Gates

Each chapter must have:

- scoped chapter claim;
- assumptions;
- definitions and notation where needed;
- at least one algorithm or decision table when algorithmic content is present;
- source/evidence ledger;
- unresolved-claim register;
- "what is not concluded" section;
- explicit connection to P8 diagnostics only where the P8 chapter-use
  restriction allows it.

## Stop Rules

Stop P9 with a blocker if any chapter lacks the chapter gates or contains a
claim that cannot be source-supported, derived, or downgraded.

## Exit Label

`P9_CHAPTERS_ACCEPTED` if the block is coherent and conservative.
