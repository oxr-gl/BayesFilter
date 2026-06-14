# P8 Result: TF/TFP OT-DPF Final Audit And Handoff

Date: 2026-05-28

## Decision

`P8_TF_TFP_OT_DPF_EXPERIMENTAL_HANDOFF_ACCEPTED`

## Phase Status

| Phase | Status | Result |
| --- | --- | --- |
| P0 | pass | `P0_SCOPE_IMPORT_GATE_ACCEPTED` |
| P1 | pass | `P1_LGSSM_TF_KALMAN_ACCEPTED` |
| P2 | pass | `P2_RANGE_BEARING_TF_UKF_ACCEPTED` |
| P3 | pass | `P3_SINKHORN_TF_RESAMPLER_ACCEPTED` |
| P4 | pass | `P4_INTEGRATED_TF_RUNNERS_ACCEPTED` |
| P5 | pass | `P5_GRADIENT_TAPE_SAME_SCALAR_PASSED` |
| P6 | pass | `P6_LGSSM_TF_VALIDATION_PASSED` |
| P7 | pass | `P7_RANGE_BEARING_TF_VALIDATION_PASSED` |

## Skeptical Final Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | Backend correction, rewrite plan, and NumPy prototype caveats were reread. |
| wrong backend | pass | Implementation under `tf_tfp/` uses TF/TFP and no NumPy imports. |
| NumPy implementation drift | pass | `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp` returned no matches. |
| proxy overclaim | pass | LGSSM/range-bearing/gradient notes preserve smoke/proxy caveats. |
| missing stop conditions | pass | Plans and result notes include structured blocker conditions. |
| hidden production drift | pass | No `bayesfilter/` files were edited. |
| monograph drift | pass | No `docs/chapters/` or `docs/references.bib` edits were made. |
| vendored-code contamination | pass | No vendored/student imports or edits were used. |
| high-dimensional-lane contamination | pass | No high-dimensional lane artifacts were used as authority or edited. |
| artifact fitness | pass | TF/TFP implementation, LGSSM, range-bearing, and gradient artifacts answer the lane question. |

## Implemented Variant

`bootstrap proposal + stable log weights + finite-budget entropic OT/Sinkhorn
barycentric relaxed resampling + equal post-resampling weights`, implemented in
TensorFlow / TensorFlow Probability under `experiments/dpf_implementation/tf_tfp/`.

This is a relaxed finite-budget OT path, not categorical PF equivalence and not
exact unregularized OT.

## Result Summary

| Result | Decision | Key evidence |
| --- | --- | --- |
| LGSSM | `DPF_OT_TF_TFP_LGSSM_PASSED` | median OT-DPF RMSE to Kalman `0.04777780918669452`; max Sinkhorn residual `4.3050919044940184e-08` |
| Range-bearing | `DPF_OT_TF_TFP_RANGE_BEARING_PASSED` | median OT-DPF state RMSE to UKF `0.06459801669123823`; max Sinkhorn residual `4.440892098500626e-16` |
| Gradient | `DPF_OT_TF_TFP_GRADIENT_CHECK_PASSED` | GradientTape `0.3591554456487759`; finite difference `0.35915332758218455`; absolute error `2.118066591338952e-06` |

## Resolved Implementation Issue

The first reproducibility check failed because the digest included
`created_at_utc`.  The runners were patched to exclude timestamp, manifest, and
digest fields from reproducibility digests.  After the patch, LGSSM,
range-bearing, and gradient reproducibility checks passed.

## Verification Commands Run

- `claude -p --model claude-opus-4-7 --effort max` plan review: iteration 1
  `REJECT`, iteration 2 `REJECT`, iteration 3 `ACCEPT`.
- `CUDA_VISIBLE_DEVICES=-1 python -c "import os; pre=os.environ.get('CUDA_VISIBLE_DEVICES'); assert pre == '-1'; import tensorflow as tf; import tensorflow_probability as tfp; assert pre == '-1'; print(...)"`
  passed with TensorFlow `2.19.1`, TFP `0.25.0`.
- `python -m py_compile` over touched TF/TFP Python files: pass.
- `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp`:
  no matches.
- `rg -n "experiments\\.dpf_implementation\\.(fixtures|filters|references|resampling|runners)(\\.| import)|student|vendored|highdim" experiments/dpf_implementation/tf_tfp`:
  no matches.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ot_dpf_tf`:
  pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ot_dpf_tf`:
  pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_gradient_checks_tf`:
  pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ot_dpf_tf --validate-only`:
  pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ot_dpf_tf --validate-only`:
  pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_gradient_checks_tf --validate-only`:
  pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ot_dpf_tf --check-reproducibility`:
  pass after digest patch.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ot_dpf_tf --check-reproducibility`:
  pass after digest patch.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_gradient_checks_tf --check-reproducibility`:
  pass after digest patch.
- `python -m json.tool` over the three TF/TFP JSON outputs: pass.
- CPU-only manifest/decision/checksum/digest `rg` checks over JSON outputs:
  pass; visible GPU list recorded as `[]`.

## Claude Result Review

- Iteration 1: `ACCEPT`.
- Claude finding: the implementation stayed within the accepted TF/TFP lane
  boundary, `tf_tfp/` has no NumPy/JAX/Torch imports, CPU-only manifests are
  explicit and consistent, LGSSM/range-bearing/gradient evidence artifacts are
  internally consistent, and caveats prevent production/posterior/HMC/monograph
  overclaim.
- Unresolved reviewer risks: validate-only checks are lighter than the prose
  verification claims because they do not deeply validate full JSON schema or
  every caveat string; shared reports output directory contains adjacent non-TF
  artifacts with similar names, which could confuse future broad greps.
- Codex audit: agreed; risks are non-blocking for this experimental handoff.

TensorFlow emitted CUDA plugin/cuInit warnings even with CPU-only hiding.  This
is recorded as environment noise, not GPU use; output manifests record
`pre_import_cuda_visible_devices=-1` and no visible GPU devices.

## Artifacts

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-master-program-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p0-scope-import-gate-result-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p1-lgssm-fixture-kalman-result-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p2-range-bearing-ukf-result-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p3-sinkhorn-resampler-result-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p4-integrated-dpf-runner-result-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p5-gradient-tape-contract-result-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p6-lgssm-validation-result-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p7-range-bearing-validation-result-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p8-final-audit-handoff-result-2026-05-28.md`
- `experiments/dpf_implementation/tf_tfp/`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-lgssm-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-range-bearing-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-gradient-check-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_lgssm_2026-05-28.json`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_range_bearing_2026-05-28.json`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_gradient_check_2026-05-28.json`

## Caveats

- Experimental evidence only; not production `bayesfilter/` code.
- No public API readiness.
- No HMC readiness.
- No posterior correctness.
- No learned/neural OT promotion.
- No banking/model-risk claim.
- No monograph claim without separate review.
- LGSSM smoke caps are run-validity checks, not scientific validation.
- Range-bearing UKF is approximate and not ground truth.
- Finite GradientTape agreement is for one named proxy scalar only.

## Next Recommended Action

Run a reviewed small multi-seed uncertainty ladder and then decide whether to
draft a separate production-boundary/API plan.
