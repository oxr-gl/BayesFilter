# P4 Result: Stochastic Volatility Gradient/MLE

Date: 2026-05-29

## Decision

`DPF_NONLINEAR_SSM_SV_GRADIENT_MLE_PASSED_SMOKE`

## Evidence Contract Result

The stochastic-volatility fixture used
`h_t = mu + phi (h_{t-1} - mu) + sigma eta_t` and
`y_t | h_t ~ Normal(0, exp(h_t))`.  CUT4 and LEDH-PF-PF-OT both evaluated the
same scalar `sv_negative_log_normalizer_mu_parameter_tf` on fixed observations.

## Metrics

| Diagnostic | CUT4 | DPF | Role |
| --- | ---: | ---: | --- |
| value at true `mu=-0.7` | 10.487929153656978 | 11.99560198815757 | same-scalar smoke |
| GradientTape gradient at true `mu` | 1.7779230445717429 | 2.953948063339272 | gradient smoke |
| grid MLE `mu` | -1.0 | -1.0 median over seeds | estimation smoke |

Comparator observed-information SE for `mu`: 1.330552082344847.  The
standard-error scaled grid-MLE distance was 0.0.  DPF seed grid MLEs were
`[-1.0, -1.0, -1.0]`.

## Verification

- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_sv_cut4_ledh_gradient_mle_tf`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_sv_cut4_ledh_gradient_mle_tf --validate-only`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_sv_cut4_ledh_gradient_mle_tf --check-reproducibility`: passed.

JSON: `experiments/dpf_implementation/reports/outputs/dpf_nonlinear_ssm_sv_gradient_mle_2026-05-29.json`.

## Interpretation

At bounded smoke scale, CUT4 and DPF choose the same coarse-grid MLE for `mu`
and both expose finite same-scalar gradients.  The value and gradient differ,
so this is not equality of filters; it is calibrated evidence that the DPF path
is differentiable and estimation-scale comparison is feasible.

## Caveats

CUT4 is a comparator, not ground truth.  No final universal threshold,
posterior correctness, HMC readiness, production readiness, DSGE/NAWM
validation, or monograph claim is concluded.
