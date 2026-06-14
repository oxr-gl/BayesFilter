# P6 Plan: LGSSM Validation

Date: 2026-05-28

## Evidence Contract

Question: on the fixed TF/TFP LGSSM fixture, do TF bootstrap PF and TF
finite-Sinkhorn OT-DPF produce finite smoke diagnostics against the Kalman
reference?

Primary criterion: finite rows, finite weights, finite Sinkhorn residuals,
shared fixture/model/observation checksums, reproducibility digest, and exact
LGSSM smoke caps to Kalman:

- median bootstrap filtered-mean RMSE to Kalman <= `0.50`;
- median OT-DPF filtered-mean RMSE to Kalman <= `0.75`;
- median bootstrap absolute log-normalizer delta to Kalman <= `5.0`;
- median OT-DPF absolute log-normalizer delta to Kalman <= `8.0`;
- max OT Sinkhorn marginal or total-mass residual <= `1e-5`.

These are run-validity smoke caps only, not scientific promotion criteria.

Explanatory-only diagnostics: bootstrap-vs-Kalman RMSE, OT-DPF-vs-Kalman RMSE,
log-normalizer proxy deltas, ESS summaries, runtime, and resampling count.  They
may explain the smoke result but do not establish production or scientific
validity.

Veto diagnostics: non-finite values, missing Kalman reference, mismatched
checksums, malformed JSON, missing CPU-only manifest, or NumPy import in
`tf_tfp`.

What must not be concluded: no nonlinear validation, exact DPF likelihood
validity, posterior correctness, HMC readiness, production readiness, or
monograph claim.

## Inputs

- P1-P5 results.

## Outputs

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p6-lgssm-validation-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-lgssm-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_lgssm_2026-05-28.json`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p6-*-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-lgssm-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_lgssm_2026-05-28.json`

## Forbidden Write Set

Production `bayesfilter/`, tests, monograph chapters, vendored code, highdim
lane, and existing NumPy prototype modules.

## Skeptical Audit Checklist

Check stale context, wrong backend, NumPy drift, proxy overclaim, missing stop
conditions, hidden production drift, monograph drift, vendored contamination,
highdim contamination, and artifact fitness.

## Stop Conditions

Stop if the targeted LGSSM runner fails or if results would overclaim beyond
bounded smoke evidence.

If a stop condition fires, write the P6 result artifact with decision
`P6_STRUCTURED_BLOCKER` and do not update the markdown report as a pass.

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ot_dpf_tf --validate-only
test -f experiments/dpf_implementation/reports/dpf-ot-tf-tfp-lgssm-result-2026-05-28.md
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_lgssm_2026-05-28.json >/dev/null
rg -n '"pre_import_cuda_visible_devices": "-1"|"decision"|"model_checksum"|"observation_checksum"|"reproducibility_digest"' experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_lgssm_2026-05-28.json
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or max
5 iterations.
