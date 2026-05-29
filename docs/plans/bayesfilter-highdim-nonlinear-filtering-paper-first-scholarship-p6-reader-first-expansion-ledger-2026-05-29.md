# P6 Reader-First Expansion Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U/P2R/P3/P4/P5 high-dimensional nonlinear
filtering ledgers and results, P6 plan, `ch33`--`ch37`,
`docs/references.bib`, `docs/main.tex`, `docs/main.log`, `docs/main.pdf`, and
the scholarly literature audit policy.

what_is_not_concluded: P6 does not conclude production readiness, NAWM
readiness, posterior accuracy, HMC convergence, tensor-method validation,
transport-method validation, GPU/XLA readiness, default readiness, exhaustive
literature coverage, or machine-certified chapter correctness.

## Scope

P6 is a pedagogical readability pass.  It does not introduce a new broad
orientation chapter and does not expand literature claims beyond the existing
checked support ledgers.  The baseline is the P5 chapter state.

## Chapter Edits

| chapter | reader-first additions | source-support status |
|---|---|---|
| `ch33` | running quadratic-observation cell, object/role table, checkpoints after exact recursion and likelihood-gradient derivation, fixed export table | project derivation and existing checked sources only |
| `ch34` | running-cell Gaussian projection explanation, object table, wrappers for affine projection and exactness-not-accuracy, checkpoint, fixed export table | project derivation and existing checked sources only |
| `ch35` | running-cell interpretation for particles/transports/tensors, representation table, wrappers for particle collapse and covariance factor gate, checkpoint, fixed export table | project derivation and existing checked sources only |
| `ch36` | running-cell HMC scalar-target explanation, exact/approximate-gradient table, wrapper for HMC gradient contract, checkpoint, fixed export table | project derivation and existing checked sources only |
| `ch37` | running-cell synthesis paragraph, imports-from-chapters table, explicit scalar-to-macro stress-cell bridge, checkpoint before final synthesis propositions | project synthesis/nonclaim using prior chapter exports |

## Proposition Pedagogy

P6 added compact wrappers for these propositions:

- `prop:bf-hd-affine-projection`;
- `prop:bf-hd-exactness-not-accuracy`;
- `prop:bf-hd-pf-collapse`;
- `prop:bf-hd-factor-gate`;
- `prop:bf-hd-hmc-gradient-contract`.

The wrappers use the P6 template: plain-English claim, object, assumptions,
approximation step, failure if assumptions break, and industrial
interpretation.

Existing P4/P5 derivations remain the main derivation support for the other
propositions.  P6 did not convert every proposition into a textbook proof
because the plan required a reader-first expansion, not a full proof appendix.

## Method Survey Versus Synthesis Boundary

P6 keeps `ch33`--`ch36` as mechanism chapters.  Cross-method promotion and
architecture-level decision synthesis remain in `ch37`.

Each of `ch33`--`ch36` now exports:

`object | exact target | approximation site | failure mode | diagnostic/veto | cost variable | promotion gate | citation/derivation anchor`

`ch37` now imports these fields explicitly before using them in its defect
calculus.

## Decision

`P6_READER_FIRST_EXPANSION_READY_FOR_HOSTILE_REVIEW`.
