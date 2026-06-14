# P8 Plan: LGSSM Validation

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: does TF/TFP LEDH-PF-PF-OT produce finite bounded smoke diagnostics on
the LGSSM fixture against Kalman, bootstrap PF, and bootstrap OT-DPF
comparators?

Baseline/comparator: exact Kalman reference, TF bootstrap PF, and existing
TF/TFP bootstrap OT-DPF.

Pass criterion: finite rows, finite corrected weights, finite log-det, finite
Sinkhorn residuals, reproducibility digest, and median LEDH RMSE/loglik smoke
caps not exceeded.

Veto diagnostics: non-finite row, max Sinkhorn residual above `1e-5`,
non-finite corrected-weight diagnostics, missing CPU-only manifest, or missing
caveats.

Not concluded: scientific validation, posterior correctness, HMC readiness,
production readiness, NAWM-scale readiness.

## Inputs

- P6 integrated runner.
- LGSSM fixture and Kalman reference.

## Outputs

- `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-lgssm-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_ot_tf_tfp_lgssm_2026-05-29.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p8-lgssm-validation-result-2026-05-29.md`

## Allowed Write Set

- listed output files;
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`

## Forbidden Write Set

Production code, vendored code, monograph chapters, high-dimensional lane
artifacts, and NumPy algorithm paths.

## Skeptical Audit Checklist

Check stale context, wrong default architecture, bootstrap-proposal overclaim,
OT-resampling overclaim, missing stop conditions, hidden production drift,
monograph drift, vendored-code contamination, high-dimensional-lane
contamination, and artifact fitness.

## Stop Conditions

Stop or write blocker if LGSSM runner fails, Kalman reference is unavailable,
corrected weights are invalid, or smoke caps make the artifact misleading.

## Verification Commands

- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ledh_pfpf_ot_tf`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ledh_pfpf_ot_tf --validate-only`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ledh_pfpf_ot_tf --check-reproducibility`
- `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_ot_tf_tfp_lgssm_2026-05-29.json`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to max five
iterations with Codex audit.

## What Must Not Be Concluded

No production, HMC, posterior, NAWM-scale, public API, or monograph claim.
