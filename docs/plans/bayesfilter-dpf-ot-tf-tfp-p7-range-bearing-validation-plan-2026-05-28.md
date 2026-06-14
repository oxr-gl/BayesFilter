# P7 Plan: Range-Bearing Validation

Date: 2026-05-28

## Evidence Contract

Question: on the fixed TF/TFP Gaussian range-bearing fixture, do UKF, TF
bootstrap PF, and TF finite-Sinkhorn OT-DPF produce finite smoke diagnostics?

Primary criterion: finite UKF/PF/OT rows, finite Sinkhorn residuals, shared
fixture/model/observation checksums, reproducibility digest, and explicit UKF
approximate-reference caveat.

Explanatory-only diagnostics: PF/OT-DPF RMSE to UKF, latent RMSE to simulated
states, observation proxy RMSE, ESS summaries, runtime, and resampling count.
They may explain the smoke result but cannot validate posterior correctness or
make UKF ground truth.

Veto diagnostics: non-finite values, invalid UKF covariance, missing caveat,
mismatched checksums, malformed JSON, missing CPU-only manifest, or NumPy import
in `tf_tfp`.

What must not be concluded: UKF is not ground truth; proxy RMSE is not posterior
correctness, production readiness, HMC readiness, or monograph validation.

## Inputs

- P1-P5 results.

## Outputs

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p7-range-bearing-validation-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-range-bearing-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_range_bearing_2026-05-28.json`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p7-*-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-range-bearing-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_range_bearing_2026-05-28.json`

## Forbidden Write Set

Production `bayesfilter/`, tests, monograph chapters, vendored code, highdim
lane, and existing NumPy prototype modules.

## Skeptical Audit Checklist

Check stale context, wrong backend, NumPy drift, proxy overclaim, missing stop
conditions, hidden production drift, monograph drift, vendored contamination,
highdim contamination, and artifact fitness.

## Stop Conditions

Stop if the targeted range-bearing runner fails or if results would overclaim
UKF/proxy evidence.

If a stop condition fires, write the P7 result artifact with decision
`P7_STRUCTURED_BLOCKER` and do not update the markdown report as a pass.

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ot_dpf_tf --validate-only
test -f experiments/dpf_implementation/reports/dpf-ot-tf-tfp-range-bearing-result-2026-05-28.md
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_range_bearing_2026-05-28.json >/dev/null
rg -n '"pre_import_cuda_visible_devices": "-1"|"decision"|"model_checksum"|"observation_checksum"|"reproducibility_digest"|"UKF is approximate' experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_range_bearing_2026-05-28.json
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or max
5 iterations.
