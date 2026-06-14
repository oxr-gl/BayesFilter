# P1 Plan: LGSSM Multiseed Regression

Date: 2026-05-29

## Decision

`ACCEPTED_BY_CLAUDE_REVIEW_ITERATION_1`

## Evidence Contract

Question: does TF/TFP LEDH-PF-PF-OT remain finite and stable across a bounded
LGSSM seed ladder against exact Kalman?

Comparator: exact Kalman, plus bootstrap PF and bootstrap OT-DPF diagnostics.

Pass criterion: result records multi-seed finite rows, RMSE/log-normalizer
diagnostics, corrected-weight/log-det/Sinkhorn diagnostics, and DPF variability.

Veto diagnostics: non-finite row, invalid Sinkhorn residual, missing CPU-only
manifest, or treating RMSE as estimation validation.

## Inputs

- Existing LGSSM fixture, Kalman reference, LEDH-PF-PF-OT runner.

## Outputs

- `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_multiseed_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/reports/dpf-nonlinear-ssm-lgssm-multiseed-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_nonlinear_ssm_lgssm_multiseed_2026-05-29.json`
- `docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p1-lgssm-multiseed-regression-result-2026-05-29.md`

## Allowed Write Set

Listed outputs and DPF nonlinear-SSM plan/result artifacts.

## Forbidden Write Set

Production code, tests, monograph chapters, vendored code, high-dimensional
lane, DSGE/NAWM files.

## Skeptical Audit Checklist

Use the master checklist.  Pay special attention to value-only overclaim.

## Stop Conditions

Stop if existing LEDH runner artifacts are missing, Kalman reference is invalid,
or CPU-only discipline cannot be recorded.

## Verification Commands

- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_multiseed_ledh_pfpf_ot_tf`
- `... --validate-only`
- `... --check-reproducibility`

## Claude Review Protocol

Use exact Claude command and loop.

## What Must Not Be Concluded

No nonlinear, posterior, HMC, production, DSGE/NAWM, or monograph claim.
