# Phase 0 Result: Coordinate And Mass Convention Audit

Date: 2026-07-08

## Status

`REPAIR_REQUIRED_BEFORE_PHASE_1`

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Which coordinate space does each precision/covariance live in, and what must be passed to HMC geometry initialization? |
| Baseline/comparator | Existing minimal Phase 5 low-rank path and `initialize_hmc_kernel_geometry` contract. |
| Primary criterion | Partially passed: the coordinate mapping is established, but the reusable initializer needs a theta-coordinate mass repair before Phase 1 can use it as an HMC geometry artifact. |
| Veto diagnostics | Triggered for Phase 1 as currently written: untransformed whitened precision would be treated as original-coordinate precision if passed directly from the reusable initializer with nontrivial `scale`. |
| Explanatory diagnostics | The `1.57` trajectory heuristic remains explanatory only until Phase 2 predeclares a geometry criterion. |
| Not concluded | No initializer quality, HMC readiness, posterior correctness, sampler convergence, default readiness, or Zhao-Cui source-faithfulness claim. |

## Source-Anchored Findings

- `fit_low_rank_spd_quadratic_geometry` evaluates the target in original
  coordinates but fits the quadratic in whitened local coordinates:
  `theta = center + scale*z`
  (`bayesfilter/inference/quadratic_geometry.py:200-205`,
  `bayesfilter/inference/quadratic_geometry.py:259-266`).
- The fitted score data are also transformed into `z` coordinates by
  multiplying original-coordinate scores by `scale`
  (`bayesfilter/inference/quadratic_geometry.py:246-247`,
  `bayesfilter/inference/quadratic_geometry.py:296-299`).
- Therefore `geometry.precision` and `geometry.covariance` are `z`-coordinate
  objects when `scale` is not all ones
  (`bayesfilter/inference/quadratic_geometry.py:332-334`,
  `bayesfilter/inference/quadratic_geometry.py:444-452`).
- The old minimal Phase 5 path already transforms the whitened precision back
  to original theta coordinates before HMC:
  `P_theta = diag(1/scale) @ P_z @ diag(1/scale)`
  (`docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py:589-600`).
- `initialize_hmc_kernel_geometry` requires `negative_hessian` to be
  `-d2 log p(theta)` in the same unconstrained coordinates as
  `initial_position`
  (`bayesfilter/inference/hmc_kernel_tuning.py:4158-4173`).
- The HMC geometry hint report records this same convention as
  `parameterization = same as initial_position`
  (`bayesfilter/inference/hmc_kernel_tuning.py:7868-7902`).
- The HMC mass artifact stores covariance and validates that its Cholesky-style
  factor reconstructs covariance as `factor @ factor.T`
  (`bayesfilter/inference/hmc.py:49-56`, `bayesfilter/inference/hmc.py:80-111`).

## Required Coordinate Rule

For HMC geometry initialization, the position, precision, and covariance must
all be in the same original unconstrained theta coordinates.

If the quadratic geometry is fitted with

```text
theta = center + scale * z
```

then the coordinate transforms are:

```text
P_theta = diag(1 / scale) @ P_z @ diag(1 / scale)
C_theta = diag(scale) @ C_z @ diag(scale)
```

The HMC handoff must use `P_theta` as `negative_hessian` or `C_theta` as
`initial_covariance`.

## Repair Finding

The reusable initializer currently passes `geometry.precision` directly into
`covariance_from_precision`
(`bayesfilter/inference/quadratic_map_covariance.py:254-287`). Because
`geometry.precision` is in `z` coordinates when `scale` is supplied, the
initializer's returned `precision`, `covariance`, and `mass_matrix` are not
safe to feed directly to HMC in original theta coordinates.

This is a repairable implementation issue, not evidence against the quadratic
initializer approach.

## Decision Table

| Decision | Status |
| --- | --- |
| Phase 0 coordinate audit | Passed with repair required. |
| Primary criterion status | Coordinate mapping established with line-anchored evidence. |
| Veto diagnostic status | Phase 1 blocked until the reusable initializer returns or explicitly labels theta-coordinate mass. |
| Main uncertainty | Whether the repaired initializer artifact will pass finite/SPD checks on the minimal target. |
| Next justified action | Patch `estimate_quadratic_map_covariance` so accepted `precision`/`covariance` are original-coordinate theta objects when `scale` is supplied; preserve geometry payload as whitened-fit provenance. |
| What is not being concluded | HMC readiness, posterior correctness, convergence, default readiness, or Zhao-Cui source-faithfulness. |

## Phase 1 Handoff Condition

Phase 1 may start only after focused tests show that:

- with `scale=None` or all-one scale, the result remains unchanged;
- with nontrivial `scale`, `result.precision` equals the original-coordinate
  precision and `result.covariance` equals the original-coordinate covariance
  on a known Gaussian target within the preexisting diagnostic tolerance;
- the payload records that geometry fitting was whitened but mass output is in
  original theta coordinates.

