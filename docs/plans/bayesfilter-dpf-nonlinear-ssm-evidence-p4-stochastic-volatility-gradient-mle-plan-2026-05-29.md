# P4 Plan: Stochastic Volatility Gradient/MLE

Date: 2026-05-29

## Decision

`ACCEPTED_BY_CLAUDE_REVIEW_ITERATION_1`

## Evidence Contract

Question: on a bounded one-parameter SV fixture, do TF/TFP CUT4 and
LEDH-PF-PF-OT produce comparable differentiable likelihood, gradient, and MLE
diagnostics on the estimation scale?

Model:
`h_t = mu + phi (h_{t-1} - mu) + sigma eta_t`,
`y_t | h_t ~ Normal(0, exp(h_t))`.

Primary comparator: differentiable TF/TFP CUT4, not ground truth.

Pass criterion: result records same-scalar value, GradientTape gradients,
finite-difference self-check where bounded, one-parameter bounded MLEs for
`mu`, comparator Hessian SE, `z = |mu_DPF - mu_CUT4| / SE_CUT4`, and DPF seed
variability.  Final tolerances remain calibration outputs.

Veto diagnostics: DPF/CUT4 scalar mismatch, non-finite gradient, invalid Hessian
SE, value-only overclaim, or CUT4 ground-truth language.

## Inputs

- P3 CUT4 component.
- Existing LEDH-PF-PF-OT flow/filter implementation.

## Outputs

- `experiments/dpf_implementation/tf_tfp/fixtures/stochastic_volatility_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/cut4_sv_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_sv_cut4_ledh_gradient_mle_tf.py`
- `experiments/dpf_implementation/reports/dpf-nonlinear-ssm-sv-gradient-mle-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_nonlinear_ssm_sv_gradient_mle_2026-05-29.json`
- `docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p4-stochastic-volatility-gradient-mle-result-2026-05-29.md`

## Allowed Write Set

Listed outputs and DPF nonlinear-SSM plan/result artifacts.

## Forbidden Write Set

Production code, tests, monograph chapters, vendored code, high-dimensional
lane, DSGE/NAWM files, NumPy implementation.

## Skeptical Audit Checklist

Use the master checklist.  Pay special attention to estimation/gradient evidence
and uncalibrated-threshold risk.

## Stop Conditions

Stop if SV LEDH-PF-PF cannot state a valid proposal/target density path, if
CUT4 is non-differentiable, or if MLE/Hessian diagnostics are invalid.

## Verification Commands

- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_sv_cut4_ledh_gradient_mle_tf`
- `... --validate-only`
- `... --check-reproducibility`

## Claude Review Protocol

Use exact Claude command and loop.

## What Must Not Be Concluded

No production, HMC, posterior, DSGE/NAWM, banking/model-risk, or monograph
claim; CUT4 is comparator, not ground truth.
