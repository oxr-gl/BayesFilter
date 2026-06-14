# P25 Zhao--Cui Five-Gap Closure Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- P24 Zhao--Cui human-facing companion note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No adaptive global differentiability claim.
- No production implementation claim.
- No empirical validation claim.

## Gap Closures

| Gap | P25 section/control | Status |
|---|---|---|
| Chair Bayesian-to-TT plausibility bridge | `From Bayesian Filtering To A Tensor-Train Approximation Family`; Eqs. `p25-bridge-1`--`p25-bridge-20`, plus anti-overclaim wording after Eq. `p25-bridge-16` | `CLOSED_AFTER_BOUNDED_CLAUDE_REVIEW` |
| One observation-step coordinate walkthrough | `One Observation Step Through All Coordinate Systems`; Eqs. `p25-walk-1`--`p25-walk-17`, plus Eq. `p25-walk-measure-bookkeeping` | `CLOSED_AFTER_BOUNDED_CLAUDE_REVIEW` |
| Gradient teaching layer before Proposition 2 | `Gradient Teaching Layer: What Is Differentiated`; Eqs. `p25-gradteach-1`--`p25-gradteach-11` | `CLOSED_LOCALLY` |
| Less-toy numerical trace | `A Less-Toy Two-Point Basis Trace`; Eqs. `p25-trace2-1`--`p25-trace2-20`, plus verification Eqs. `p25-trace2-9a`, `p25-trace2-12a`, and `p25-trace2-residual-check` | `CLOSED_AFTER_BOUNDED_CLAUDE_REVIEW` |
| Consolidated fixed least-squares implementation and derivative protocol | `Consolidated Fixed Least-Squares Lane`; Eqs. `p25-ls-1`--`p25-ls-23`, shape/flattening/mass-contract Eqs. `p25-ls-shape-ledger`--`p25-ls-mass-contract`, and failure table | `CLOSED_AFTER_BOUNDED_CLAUDE_REVIEW` |

## Preservation Guardrail

- P25 was created by copying the P24 TeX source and inserting expansion blocks.
- P24 was not edited.
- P25 line/page count must be no shorter than P24 at validation.

Decision: `P25_FIVE_GAP_CLOSURE_PATCHED_AFTER_BOUNDED_CLAUDE_REVIEW`.
