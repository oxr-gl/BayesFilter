# P49-M3 Subplan: Sample Propagation, ESS, And Proposal Correction

metadata_date: 2026-06-09
phase: P49-M3
status: PLAN_REVIEW_CONVERGED

## Objective

Repair R3 and R4 by implementing or specifying the source-style propagation
loop: propagate samples, compute weights, assess ESS, enhance/resample when
needed, construct the new target, sample from the retained transport, and
apply proposal correction.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the source-faithful lane use sample/ESS/proposal correction instead of pairwise retained-grid transition density? |
| Baseline/comparator | Source `full_sol.solve`, `full_sol.reapprox`, `pre_sol.solve`, `pre_sol.reapprox`; exact one-step references. |
| Primary pass criterion | One-step and tiny-horizon tests verify ESS accounting, proposal correction, and no pairwise-grid fallback. |
| Veto diagnostics | ESS omitted; correction ratio omitted; all-grid pairwise propagation used as source-faithful path. |
| Not concluded | No paper-scale accuracy or HMC readiness. |

## Planned Work

1. Create focused one-step propagation tests.
2. Add ESS and enhanced-sampling invariants.
3. Add proposal-correction normalizer checks against dense references.
4. Record Monte Carlo uncertainty for stochastic tests.

## Repair Loop

Failed numerical checks must be classified as implementation bug, tolerance
issue, Monte Carlo uncertainty, or design mismatch.  Fix implementation bugs;
do not loosen tolerances after seeing results without a reviewed amendment.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p49-m3-sample-ess-proposal-result-2026-06-09.md`
