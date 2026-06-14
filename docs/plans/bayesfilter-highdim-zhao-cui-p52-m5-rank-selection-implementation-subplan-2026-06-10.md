# P52-M5 Subplan: Rank Selection Implementation And Tests

metadata_date: 2026-06-10
phase: P52-M5
status: PLAN_REVIEW_CONVERGED

## Objective

Implement the fixed-rank selection protocol that combines memory preflight, UKF
scouting, lower-rung references, and rank-ladder self-convergence.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter choose a fixed rank before HMC using declared memory and calibration rules? |
| Baseline/comparator | P52-M2 rank ceilings, P52-M3 UKF scout outputs, P52-M4 route metadata, lower-rung dense references, and higher-rank deterministic references where feasible. |
| Primary pass criterion | The implementation selects or blocks a rank from `{2, 4, 8, 16, 32}` with recorded memory forecasts, value/gradient diagnostics, nonclaim labels, and the explicit stop rules from the P52 master program. |
| Veto diagnostics | Rank chosen after seeing HMC samples; adaptive rank changes inside likelihood; rank grows above `r_max`; no failure classification when ranks do not stabilize. |
| Not concluded | Rank selection does not prove exact posterior correctness or HMC readiness. |

## Planned Work

1. Add a rank-selection protocol object:
   - inputs: dimension, horizon, memory budget, UKF scout, route metadata,
     candidate ranks, tolerances;
   - outputs: selected rank or blocker, frozen design metadata, diagnostics.
2. Define comparison classes:
   - low-dimensional dense reference;
   - same-target dense reference when feasible;
   - higher-rank deterministic reference;
   - UKF scout sanity check;
   - rank self-convergence.
3. Track value error per observation, gradient relative error where available,
   directional gradient cosine where available, filtered mean/covariance
   discrepancies, memory forecast, and wall time.
4. Require deterministic replay of selected rank and branch metadata.
5. Add tests for no adaptive rank mutation during likelihood evaluation.

## Required Stop Rules

The implementation must enforce these rules before any model row can pass:

- remove all candidate ranks above `r_max` before evaluating the row;
- block with `BLOCK_P52_RANK_BUDGET_EMPTY` if no candidate remains;
- with a dense/exact reference, select the smallest passing rank and block with
  `BLOCK_P52_RANK_REFERENCE_MISMATCH` if none pass;
- without dense/exact reference, require a strictly higher feasible rank as the
  same-route comparator and block with
  `BLOCK_P52_HIGHER_RANK_REFERENCE_MISSING` if none exists;
- block after two consecutive nonfinite, memory-failing, or clearly worsening
  rank increases;
- reject any rank choice that changes during likelihood evaluation.

The default tolerance bundle is inherited from the master program unless this
phase writes stricter tolerances before executing tests.

## Higher-Rank Reference Definition

A higher-rank deterministic reference is not an external truth.  It is a
same-target, same-route run with:

- identical observations, parameters, centers, scales, basis family,
  contraction path, route metadata, and random seeds if any;
- only the fixed rank cap increased;
- memory forecast below the same single-step cap;
- deterministic replay metadata matching the candidate row.

If those conditions fail, the row has no higher-rank reference and must use a
different comparator class or block.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p52-m5-rank-selection-implementation-result-2026-06-10.md`

Required token:

`PASS_P52_M5_RANK_SELECTION_IMPLEMENTATION` or
`BLOCK_P52_M5_RANK_SELECTION_IMPLEMENTATION`
