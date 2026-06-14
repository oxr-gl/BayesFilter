# P2 Plan: Range-Bearing Stress

Date: 2026-05-29

## Decision

`ACCEPTED_BY_CLAUDE_REVIEW_ITERATION_1`

## Evidence Contract

Question: do TF/TFP LEDH-PF-PF-OT nonlinear local-linearization diagnostics
remain finite under a bounded range-bearing stress ladder?

Comparator: UKF approximate, bootstrap PF, bootstrap OT-DPF.

Pass criterion: result records finite stress rows, angle wrapping, Jacobian
singular values, corrected weights, Sinkhorn residuals, and proxy labels.

Veto diagnostics: missing UKF caveat, non-finite row, invalid Jacobian/log-det,
invalid Sinkhorn residual, or proxy RMSE overclaim.

## Inputs

- Existing range-bearing fixture, UKF reference, LEDH-PF-PF-OT runner.

## Outputs

- `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_stress_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/reports/dpf-nonlinear-ssm-range-bearing-stress-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_nonlinear_ssm_range_bearing_stress_2026-05-29.json`
- `docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p2-range-bearing-stress-result-2026-05-29.md`

## Allowed Write Set

Listed outputs and DPF nonlinear-SSM plan/result artifacts.

## Forbidden Write Set

Production code, tests, monograph chapters, vendored code, high-dimensional
lane, DSGE/NAWM files.

## Skeptical Audit Checklist

Use the master checklist.  Pay special attention to UKF/proxy caveats.

## Stop Conditions

Stop if stress fixture cannot stay bounded, UKF caveat is missing, or local
Jacobian diagnostics fail.

## Verification Commands

- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_stress_ledh_pfpf_ot_tf`
- `... --validate-only`
- `... --check-reproducibility`

## Claude Review Protocol

Use exact Claude command and loop.

## What Must Not Be Concluded

No UKF ground truth, nonlinear posterior correctness, HMC, production,
DSGE/NAWM, or monograph claim.
