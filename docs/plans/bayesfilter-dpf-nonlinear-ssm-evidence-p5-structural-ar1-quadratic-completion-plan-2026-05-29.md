# P5 Plan: Structural AR(1) Quadratic Completion

Date: 2026-05-29

## Decision

`ACCEPTED_BY_CLAUDE_REVIEW_ITERATION_1`

## Evidence Contract

Question: can the DPF lane test the ch18b exogenous/endogenous structural split
with a non-DSGE toy model and differentiable estimation evidence?

Model:
`m_t = rho m_{t-1} + sigma eps_t`,
`k_t = a k_{t-1} + b m_t + c m_t^2 + d m_{t-1} m_t`,
`x_t = (m_t, k_t)`,
`y_t = k_t + lambda m_t + eta_t`.

Comparator: differentiable TF/TFP CUT4 structural filter integrating over
`eps_t` only and deterministically completing `k_t`.

Pass criterion: result records same-scalar value/gradient, one-parameter
bounded MLE/SE diagnostics, deterministic residuals near zero for structural
paths, and an optional wrong full-state noisy diagnostic labelled invalid if
implemented.

Veto diagnostics: deterministic residual not recorded, independent noise added
to `k_t` as valid model, DSGE/NAWM drift, non-finite gradient, or invalid
Hessian SE.

## Inputs

- ch18b read-only.
- P3 CUT4 component.
- Existing LEDH-PF-PF-OT implementation.

## Outputs

- `experiments/dpf_implementation/tf_tfp/fixtures/structural_ar1_quadratic_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/cut4_structural_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_structural_ar1_cut4_ledh_gradient_mle_tf.py`
- `experiments/dpf_implementation/reports/dpf-nonlinear-ssm-structural-ar1-gradient-mle-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_nonlinear_ssm_structural_ar1_gradient_mle_2026-05-29.json`
- `docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p5-structural-ar1-quadratic-completion-result-2026-05-29.md`

## Allowed Write Set

Listed outputs and DPF nonlinear-SSM plan/result artifacts.

## Forbidden Write Set

Production code, tests, monograph chapters, vendored code, high-dimensional
lane, DSGE/NAWM files, NumPy implementation.

## Skeptical Audit Checklist

Use the master checklist.  Pay special attention to DSGE/NAWM drift and
structural residuals.

## Stop Conditions

Stop if the DPF path cannot preserve deterministic completion, if residuals are
not measurable, or if CUT4/DPF scalar mismatch occurs.

## Verification Commands

- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_ar1_cut4_ledh_gradient_mle_tf`
- `... --validate-only`
- `... --check-reproducibility`

## Claude Review Protocol

Use exact Claude command and loop.

## What Must Not Be Concluded

No DSGE/NAWM validation, production readiness, HMC readiness, posterior
correctness, banking/model-risk claim, or monograph claim.
