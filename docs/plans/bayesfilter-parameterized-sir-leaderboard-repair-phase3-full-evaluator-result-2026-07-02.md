# Phase 3 Result: Full Observed-Data Evaluator

Date: 2026-07-02

Status: `BLOCK_PHASE3_FULL_EVALUATOR_COMPLEXITY_GATE`

## Owner-Directive Amendment

The route tested here,
`bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_score_path`,
is now demoted to diagnostic/historical retained-grid evidence.  It is no
longer the production candidate for Zhao-Cui leaderboard wiring.  The preserved
complexity blocker remains useful as a record of why the generic full
tensor-product retained-grid route should not be repaired as the production
path.

The production-admissible Zhao-Cui direction is the fixed-variant source-route
path.  Future leaderboard repair should select or wire that fixed variant,
not revive the generic retained-grid candidate tested in this Phase 3 result.

## Objective

Determine whether the reviewed parameterized SIR row can compute a full
observed-data/filtering value and analytical/manual score through the Phase 1
candidate Zhao-Cui route.

## Entry Evidence

- Phase 2 generated
  `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`.
- The row has `truth_theta_coordinate = sir_log_scale_theta` and
  `truth_theta = [0.0, 0.0, 0.0]`.
- Phase 2 did not admit any score.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the parameterized SIR row compute full observed-data/filtering value and analytical/manual score? |
| Baseline/comparator | Phase 2 row contract and existing local SIR score components. |
| Primary pass criterion | Finite full-row value and finite analytical/manual score for the declared row at truth theta. |
| Veto diagnostics | Nonfinite outputs, branch mismatch, target mismatch, complexity gate, autodiff/FD score provenance, or missing semantic binding. |
| Not concluded | No exactness claim, no rank sufficiency claim, no HMC/GPU readiness claim. |

## Checks Run

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p81_analytical_sir_score.py::test_multistate_fixed_design_tt_score_path_runs_on_sir_d18_horizon0_observation_term \
  tests/highdim/test_p81_analytical_sir_score.py::test_multistate_fixed_design_tt_score_path_blocks_sir_d18_two_row_all_grid_transition
```

Exit status: 0. Result: `2 passed, 2 warnings` in 66.10 seconds.

Interpretation:

- Horizon-0 observation-only SIR `d=18` score path runs and returns finite
  value/score under the current candidate route.
- The two-row transition rung is an expected complexity blocker under the
  current full-grid multistate route.

## Blocker Artifact

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-blocker-2026-07-02.json`

The blocker records:

- minimum retained grid size for SIR `d=18`: `2^18 = 262144` points;
- default streaming chunks for transition fallback:
  `current_chunk_size = 512`, `previous_chunk_size = 64`,
  `max_chunk_products = 8192`;
- required chunk products at minimum retained order:
  `512 * 4096 = 2097152`, which exceeds the current gate;
- total pair count per transition at minimum retained order:
  `262144^2 = 68719476736`;
- current route is blocked by retained full-grid transition complexity, not by
  dataset-row theta metadata.

## Route Boundary

The existing P8p manual no-autodiff SIR score code was inspected as a possible
repair clue. It is a LEDH-PFPF-OT diagnostic route, not the Zhao-Cui
fixed-design TT/SIRT evaluator bound by Phase 1. Using it here would silently
change the algorithm under test, so it is not admitted as a Phase 3 shortcut.

## Gate Assessment

Primary criterion: failed.

Veto diagnostic: `complexity_gate`.

Phase 4 cannot start because no finite full-row value and analytical/manual
score exists for the reviewed parameterized SIR row.

## Required Repair Before Resuming

Implement or select a reviewed full observed-data parameterized SIR Zhao-Cui
evaluator that avoids the current full tensor-product retained transition grid
while preserving analytical/manual score provenance.

Any such route must be classified before implementation under the Zhao-Cui
source-anchor gate:

- `source_faithful`;
- `fixed_hmc_adaptation`;
- `extension_or_invention`.

The repair should be planned as a new governed subprogram before Phase 4 is
attempted.

## Environment

- CPU-only by explicit `CUDA_VISIBLE_DEVICES=-1`.
- `MPLCONFIGDIR=/tmp`.
- TensorFlow emitted usual CPU-only CUDA plugin/cuInit warnings; no GPU claim
  is made.
- No package installation, network fetch, or GPU benchmark was run.

## Nonclaims

- This is not evidence against the Phase 2 dataset repair.
- This is not evidence against the local analytical SIR score hooks.
- This is not proof that Zhao-Cui SIR inference is impossible.
- This is not permission to use LEDH-PFPF-OT as a Zhao-Cui leaderboard score.
- This is not HMC or GPU production readiness evidence.

## Next Handoff

Stop the current runbook before Phase 4 for the generic retained-grid route.
The next safe action is to supersede this candidate and wire the fixed-variant
Zhao-Cui source-route evaluator under a reviewed leaderboard repair plan.
