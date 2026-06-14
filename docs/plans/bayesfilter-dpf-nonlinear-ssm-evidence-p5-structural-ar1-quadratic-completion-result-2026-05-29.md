# P5 Result: Structural AR(1) Quadratic Completion

Date: 2026-05-29

## Decision

`DPF_NONLINEAR_SSM_STRUCTURAL_AR1_EXECUTED_WITH_ESTIMATION_CALIBRATION_WARNING`

## Evidence Contract Result

The structural toy model tested an endogenous/exogenous split without DSGE or
NAWM code:

- `m_t = rho m_{t-1} + sigma eps_t`
- `k_t = a k_{t-1} + b m_t + c m_t^2 + d m_{t-1} m_t`
- `y_t = k_t + lambda m_t + eta_t`

CUT4 integrates over `eps_t` only.  The DPF path samples and flows the
exogenous/current `m` coordinate, applies finite-Sinkhorn relaxed resampling to
the declared stochastic/current and structural-context coordinates, and then
recomputes `k_t` from the deterministic completion map.

## Metrics

| Diagnostic | CUT4 | DPF | Role |
| --- | ---: | ---: | --- |
| value at true `b=0.65` | 1.69561538766999 | 1.058876457208914 | same-scalar smoke |
| GradientTape gradient at true `b` | -0.7587319463437616 | 3.8927855675004146 | gradient smoke |
| grid MLE `b` | 0.65 | 0.35 median over seeds | estimation smoke |

Comparator observed-information SE for `b`: 0.2507523019954904.  The
standard-error scaled grid-MLE distance was 1.196399784219709.  DPF seed grid
MLEs were `[0.35, 0.5, 0.35]`.

## Deterministic Residual Veto

| Diagnostic | Value |
| --- | ---: |
| max post-flow deterministic residual | 0.0 |
| max post-resample deterministic residual | 0.0 |
| max structural residual | 0.0 |
| max Sinkhorn residual | 1.0485329271503474e-09 |

## Verification

- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_ar1_cut4_ledh_gradient_mle_tf`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_ar1_cut4_ledh_gradient_mle_tf --validate-only`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_ar1_cut4_ledh_gradient_mle_tf --check-reproducibility`: passed.

JSON: `experiments/dpf_implementation/reports/outputs/dpf_nonlinear_ssm_structural_ar1_gradient_mle_2026-05-29.json`.

## Interpretation

The structural residual veto passed exactly at smoke scale, so the relaxed
resampling path did not silently turn the deterministic endogenous coordinate
into an independently noisy state.  The DPF and CUT4 estimation diagnostics are
not identical; the grid-MLE difference and gradient difference are a structured
calibration warning.  This phase passes the structural-residual and finite
same-scalar GradientTape smoke checks, but it does not pass estimator-equivalence
evidence.

## Caveats

This is a toy non-DSGE structural fixture.  No DSGE/NAWM validation, posterior
correctness, HMC readiness, production readiness, banking/model-risk claim, or
monograph claim is concluded.
