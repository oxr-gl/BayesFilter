# P10 Result: Final Audit And Handoff

Date: 2026-05-29

## Decision

`P10_LEDH_PFPF_OT_EXPERIMENTAL_HANDOFF_ACCEPTED`

## Phase Status

| Phase | Status | Result |
| --- | --- | --- |
| P0 | pass | `P0_SCOPE_DEFAULT_ARCHITECTURE_ACCEPTED` |
| P1 | pass | `P1_LEDH_MATH_CONTRACT_ACCEPTED` |
| P2 | pass | `P2_AFFINE_LGSSM_EDH_PARITY_ACCEPTED` |
| P3 | pass | `P3_RANGE_BEARING_LOCAL_LINEARIZATION_ACCEPTED` |
| P4 | pass | `P4_PFPF_CORRECTION_LOGDET_ACCEPTED` |
| P5 | pass | `P5_TF_TFP_LEDH_FLOW_IMPLEMENTATION_ACCEPTED` |
| P6 | pass | `P6_INTEGRATED_LEDH_PFPF_OT_RUNNER_ACCEPTED` |
| P7 | pass | `P7_GRADIENT_TAPE_CONTRACT_PASSED` |
| P8 | pass | `P8_LGSSM_VALIDATION_PASSED` |
| P9 | pass | `P9_RANGE_BEARING_VALIDATION_PASSED` |

## Implemented Variant

`TF/TFP LEDH-PF-PF with finite-budget entropic OT/Sinkhorn relaxed resampling`.

The PF-PF correction uses bootstrap transition `q0`, local frozen-affine LEDH
flow, forward log determinant, transition target density, observation target
density, corrected log weights, and finite Sinkhorn relaxed resampling after
correction.  Bootstrap OT-DPF is now comparator/component baseline only.

## Result Summary

| Result | Decision | Key evidence |
| --- | --- | --- |
| LGSSM | `DPF_LEDH_PFPF_OT_TF_TFP_LGSSM_PASSED` | median LEDH RMSE to Kalman `0.06830431164955209`; max Sinkhorn residual `5.427581322575703e-08` |
| Range-bearing | `DPF_LEDH_PFPF_OT_TF_TFP_RANGE_BEARING_PASSED` | median LEDH state RMSE to UKF `0.07742171157461389`; max Sinkhorn residual `6.661338147750939e-16` |
| Gradient | `DPF_LEDH_PFPF_OT_TF_TFP_GRADIENT_CHECK_PASSED` | GradientTape `1.0815014757961667`; finite difference `1.08150132739393`; abs error `1.484022367215232e-07` |

## Claude Review Record

- Plan bundle iteration 1: `ACCEPT`.
- Claude minor caution: direct raw `claude -p --model claude-opus-4-7 --effort max`
  is stricter than a wrapper-script preference.  Codex audit: non-blocking
  because the user explicitly required that exact command.

## Verification Commands

- `python -m py_compile` over touched TF/TFP files: pass.
- `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp`: no matches.
- `rg -n "student|vendored|highdim|ch33|ch34|ch35|ch36|ch37" experiments/dpf_implementation/tf_tfp`: no matches.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ledh_pfpf_ot_tf`: pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ledh_pfpf_ot_tf`: pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_gradient_checks_tf`: pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ledh_pfpf_ot_tf --validate-only`: pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ledh_pfpf_ot_tf --validate-only`: pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_gradient_checks_tf --validate-only`: pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ledh_pfpf_ot_tf --check-reproducibility`: pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ledh_pfpf_ot_tf --check-reproducibility`: pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_gradient_checks_tf --check-reproducibility`: pass.
- `python -m json.tool` over the three new JSON outputs: pass.

TensorFlow emitted CUDA plugin/cuInit warnings despite CPU hiding.  The runners
set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import and JSON manifests record
no visible GPU devices.  This is recorded as environment noise, not GPU use.

## Files Changed

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-master-program-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p*-2026-05-29.md`
- `experiments/dpf_implementation/tf_tfp/flows/`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_gradient_checks_tf.py`
- `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-*-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_ot_tf_tfp_*.json`

## Caveats

- Experimental evidence only; not production `bayesfilter/` code.
- No public API readiness.
- No HMC readiness.
- No posterior correctness.
- No NAWM-scale readiness; that requires separate scaling evidence.
- UKF is approximate and not ground truth for range-bearing.
- Finite Sinkhorn is relaxed finite-budget OT, not exact categorical PF
  equivalence or exact unregularized OT.
- Frozen local-affine LEDH log-det is the first-rung PF-PF convention; full
  state-dependent nonlinear-map Jacobian validation is deferred.
- No banking/model-risk claim.
- No monograph claim without separate review.

## Unresolved Risks

- The evidence is a bounded smoke/proxy ladder on LGSSM and moderate
  range-bearing only.
- The frozen local-affine log-det convention is auditable and fast, but a future
  nonlinear-map Jacobian audit is needed before stronger claims.
- Multi-seed uncertainty is small but still smoke-scale.

## Next Recommended Action

Create a reviewed multi-seed/stress ladder for LEDH-PF-PF-OT, then a separate
production-boundary/API plan only if the ladder remains stable.
