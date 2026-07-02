# Phase 1 Subplan: SIR Gradient Evidence Contract

Date: 2026-06-30

Status: `DRAFT_PENDING_PHASE0`

## Phase Objective

Define a SIR-specific HMC-direction evidence contract that adapts the LGSSM
directional gate without pretending that SIR has an exact Kalman oracle.

## Entry Conditions Inherited From Previous Phase

- Phase 0 route inventory passed.
- Active SIR scripts and manual-score tests are syntactically valid.
- Material route is GPU/XLA/TF32 manual reverse, with regression FD as a
  fixed-randomness comparator.

## Required Artifacts

- Phase result: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-result-2026-06-30.md`
- Updated execution ledger.
- Refreshed Phase 2 subplan.

## Required Checks, Tests, And Reviews

Local checks:

```bash
rg -n "manual-reverse|regression_slope_standard_error|standard_error_of_batch_mean|row_residual|expect-device-kind|tf32-mode" docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
```

Review:

- Claude read-only review is required because this phase defines the numerical
  pass/fail contract.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What SIR-specific gate can classify the manual reverse score as HMC-direction useful without overclaiming exact correctness? |
| Baseline/comparator | Same fixed-randomness 13-point regression FD in raw theta directions, with slope SE and regression diagnostics. |
| Primary criterion | A written gate that separates route validity, fixed-randomness derivative agreement, seed-gradient MCSE, relative-error screen, and residual vetoes. |
| Veto diagnostics | Treating FD as exact truth; hiding row residuals; using CPU route; omitting MCSE; omitting slope SE; changing thresholds after seeing Phase 4 results. |
| Explanatory diagnostics | FD R2, plateau, score decomposition, N ladder, Sinkhorn budget ladder. |
| Not concluded | Exact SIR gradient proof, posterior correctness, global nonlinear validation, or HMC/NUTS readiness. |

## Candidate Gate To Review

For each raw theta direction, after route checks pass, classify the comparison
against regression FD using the combined uncertainty scale

```text
combined_se = sqrt(regression_slope_standard_error^2
                   + standard_error_of_batch_mean^2)
```

where `standard_error_of_batch_mean` is the seed-gradient MCSE for the same
theta component.  Define

```text
direction_scale = max(abs(regression_fd_slope), abs(manual_score), 1.0)
precision_pass = (2 * combined_se <= 0.25 * direction_scale)
```

The `precision_pass` threshold is a predeclared HMC-direction diagnostic floor:
if the uncertainty band is wider than this, the result is classified as
`inconclusive_precision_veto`, not as positive evidence.  A direction may be
classified as `direction_pass` only if the route checks, row-residual checks,
finite objective/score checks, finite FD slope-SE checks, finite MCSE checks,
and `precision_pass` all pass, and then at least one of the following two pass
arms holds:

1. `abs(manual_score - regression_fd_slope) <= 2 * combined_se`;
2. `abs(manual_score - regression_fd_slope) <= 4 * combined_se` and a
   separate N/budget ladder certificate shows decreasing MCSE or decreasing row
   residual with no worsening of the gap, while `precision_pass` remains true;

Supportive labels are reported separately and do not create `direction_pass`.
The direction is marked `near_equal_supportive` when relative error to the
regression FD slope is below `1%` using `max(abs(regression_fd_slope), 1.0)` as
the scale.

For non-negligible directions, the manual score and FD slope must also have the
same sign.  A direction is non-negligible if either absolute value exceeds
`2 * combined_se`.  If both are within `2 * combined_se` of zero, sign is not a
veto, but the direction is reported as `near_zero_direction` in addition to its
pass/inconclusive status.

The gate must additionally require finite objective, finite score, finite
per-seed MCSE, manual reverse score route, XLA compiler metadata for material
runs, GPU tensor device evidence, TF32 enabled, no dense/full transport
autodiff, and predeclared row residual thresholds.

The relative-error screen is therefore explanatory/supportive for SIR.  It can
help explain an HMC-direction result, but it cannot by itself promote a
direction because the regression FD slope is not an exact nonlinear oracle.
The MCSE term is not merely recorded: it enters `combined_se`, and a nonfinite
or missing MCSE vetoes the direction classification.

## Forbidden Claims And Actions

- Do not claim exact-gradient correctness from FD agreement.
- Do not change thresholds after seeing Phase 4 material results.
- Do not define a gate that can pass without route metadata.
- Do not use FD relative error alone as a pass condition.
- Do not use finite MCSE as a sufficient MCSE check; MCSE must enter the
  comparison uncertainty or veto classification.
- Do not convert a large uncertainty band into positive evidence; failure of
  `precision_pass` is an inconclusive precision veto, not a pass.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- the gate is written with explicit route checks and numerical screens;
- Claude returns `VERDICT: AGREE`, or revisions converge within five rounds;
- Phase 2 knows exactly which diagnostic fields or tests must be added.

## Stop Conditions

- Claude and Codex cannot converge on a non-overclaiming gate.
- The current diagnostics cannot expose required fields without a larger design
  change.
- A human decision is needed to alter default policy or scientific criteria.

## End-Of-Phase Close Protocol

1. Run required local checks.
2. Write the Phase 1 result.
3. Refresh Phase 2 subplan.
4. Review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
