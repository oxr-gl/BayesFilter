# P9 Plan: Range-Bearing Validation

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: does TF/TFP LEDH-PF-PF-OT produce finite bounded proxy diagnostics on
the range-bearing fixture against UKF, bootstrap PF, and bootstrap OT-DPF
comparators?

Baseline/comparator: TF/TFP UKF approximate reference, TF bootstrap PF, and
existing TF/TFP bootstrap OT-DPF.

Pass criterion: finite rows, finite local Jacobians, finite corrected weights,
finite log-det diagnostics, finite Sinkhorn residuals, reproducibility digest,
and explicit UKF/proxy caveats.

Veto diagnostics: non-finite row, UKF caveat missing, corrected weights invalid,
max Sinkhorn residual above `1e-5`, or local Jacobian instability on fixture.

Not concluded: UKF ground truth, nonlinear correctness, production readiness,
HMC readiness, NAWM-scale readiness.

## Inputs

- P6 integrated runner.
- Range-bearing fixture and UKF reference.

## Outputs

- `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-range-bearing-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_ot_tf_tfp_range_bearing_2026-05-29.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p9-range-bearing-validation-result-2026-05-29.md`

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

Stop or write blocker if runner fails, UKF is unavailable, angle residuals are
not wrapped, corrected weights are invalid, or the artifact would overclaim
proxy RMSE.

## Verification Commands

- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ledh_pfpf_ot_tf`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ledh_pfpf_ot_tf --validate-only`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ledh_pfpf_ot_tf --check-reproducibility`
- `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_ot_tf_tfp_range_bearing_2026-05-29.json`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to max five
iterations with Codex audit.

## What Must Not Be Concluded

No UKF ground truth, production, HMC, posterior, NAWM-scale, public API, or
monograph claim.
