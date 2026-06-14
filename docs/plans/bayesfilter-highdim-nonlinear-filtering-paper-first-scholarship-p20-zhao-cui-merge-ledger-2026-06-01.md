# P20 Zhao--Cui Merge Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P18 true annotated Zhao--Cui companion note and ledgers.
- P19 chair-readable fixed-branch gradient note and ledgers.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross/rank/pivot/domain
  choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No empirical validation on BayesFilter target models.

## Merge Decision

Decision: `P18_SPINE_PRESERVED_P19_GRADIENT_IMPORTED`.

P20 uses P18 as the source-order annotated Zhao--Cui spine.  It preserves P18
through the fixed-branch filtering recursion and replaces only the compressed
P18 derivative/diagnostic/minimal-example/conclusion tail beginning at
`Same-Scalar Analytical Derivative`.  The imported P19 body has `P19-`
equation-tag prefixes to prevent collisions.

## P18 Carry-Forward Map

| P18 block | P20 destination | Status |
|---|---|---|
| Reader Contract And Notation | Same titled section | `PRESERVED_IN_ORDER` |
| What Problem Is Being Solved? | Same titled section | `PRESERVED_IN_ORDER` |
| State-Space Model And BayesFilter Notation | Same titled section | `PRESERVED_IN_ORDER` |
| The Four Marginal Learning Problems | Same titled section | `PRESERVED_IN_ORDER` |
| The Exact Recursive Bottleneck | Same titled section | `PRESERVED_IN_ORDER` |
| Tensor Trains From First Principles | Same titled section | `PRESERVED_IN_ORDER` |
| Why TT Marginalization Is Cheap Once The Representation Exists | Same titled section | `PRESERVED_IN_ORDER` |
| Zhao--Cui Algorithm 1, Fully Annotated | Same titled section | `PRESERVED_IN_ORDER` |
| Why Nonnegativity Fails And Why Square-Root TT Repairs It | Same titled section | `PRESERVED_IN_ORDER` |
| Squared-TT Density, Defensive Reference, And Normalizer | Same titled section | `PRESERVED_IN_ORDER` |
| Squared-TT Marginalization And Mass Matrices | Same titled section | `PRESERVED_IN_ORDER` |
| Conditional Densities And KR Maps From Marginal Ratios | Same titled section | `PRESERVED_IN_ORDER` |
| Zhao--Cui Algorithm 2, Fully Annotated | Same titled section | `PRESERVED_IN_ORDER` |
| Forward Conditional Map And Particle-Filter Correction | Same titled section | `PRESERVED_IN_ORDER` |
| Backward Conditional Map, Path Estimation, And Smoothing | Same titled section | `PRESERVED_IN_ORDER` |
| Error Propagation: What It Proves And What It Does Not Prove | Same titled section | `PRESERVED_IN_ORDER` |
| Preconditioning | Same titled section including Algorithm 5 bridge | `PRESERVED_IN_ORDER` |
| End of Zhao--Cui Annotation and Start of BayesFilter Fixed-Branch Extension | Same titled boundary section | `PRESERVED_IN_ORDER` |
| Implementable Fixed-Branch Objects And Data Structures | Same titled section | `PRESERVED_IN_ORDER` |
| One Concrete Branch, Fully Instantiated | Same titled section | `PRESERVED_IN_ORDER` |
| Fixed-Branch TT Filtering Recursion | Same titled section | `PRESERVED_IN_ORDER` |
| Source Coverage Summary appendix | Same titled appendix | `PRESERVED` |

Codex checked that these are substantive carried sections, not summary
placeholders.  They appear in the same order as P18 before the integrated P19
gradient expansion.

## P19 Import Checklist

| Accepted P19 component | P20 destination | Status |
|---|---|---|
| Motivation and same-scalar problem | `Chair-Readable Fixed-Branch Gradient: Motivation` | `IMPORTED` |
| Fixed-branch structural-choice rule | Integrated bridge and motivation | `IMPORTED` |
| Warmup 1: normalizer derivative | Same titled warmup | `IMPORTED` |
| Warmup 2: squared approximation | Same titled warmup | `IMPORTED` |
| Warmup 3: rank-one TT | Same titled warmup | `IMPORTED` |
| Warmup 4: rank-\(R\) TT | Same titled warmup | `IMPORTED` |
| Warmup 5: fixed linear solve | Same titled warmup | `IMPORTED` |
| Forward object table | `The Fixed-Branch Forward Pass` | `IMPORTED` |
| Derivative object table | `The Fixed-Branch Derivative Pass` | `IMPORTED` |
| Positivity-floor same-scalar clarification | Eq. `P19-53a` | `IMPORTED` |
| Entrywise design-row derivation | Eqs. `P19-53b`--`P19-53h` | `IMPORTED` |
| Full mass-contraction derivative | Eqs. `P19-66`--`P19-72` | `IMPORTED` |
| Carried-marginal contraction derivative | Eqs. `P19-74a`--`P19-74d` | `IMPORTED` |
| Normalized approximate-filter proposition | `Proposition 1` section | `IMPORTED` |
| Same-scalar derivative proposition | `Proposition 2` section | `IMPORTED` |
| Limitations | `What This Does Not Prove` | `IMPORTED` |
| Same-branch finite differences | `Finite-Difference Test` | `IMPORTED` |
| Structural choices frozen, cores recomputed | Eqs. `P19-94`--`P19-101` | `IMPORTED` |
| Minimal runnable example | Same titled section | `IMPORTED` |
| Closing summary | `Integrated Reader-Facing Conclusion` | `IMPORTED` |

## Reader Bridge

P20 adds a reader-facing bridge before the imported gradient section.  It
distinguishes:

- \(\theta\): a random static parameter coordinate in Zhao--Cui joint
  state/parameter learning;
- \(\beta\): the external parameter argument differentiated by the fixed-branch
  BayesFilter likelihood lane.

The bridge also states that branch choices are frozen while fitted cores remain
parameter-dependent outputs of the same fixed fitting equations.
