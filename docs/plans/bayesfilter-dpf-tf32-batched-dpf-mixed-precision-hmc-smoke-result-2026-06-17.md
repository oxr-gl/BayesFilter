# Mixed-Precision HMC Smoke Result - 2026-06-17

## Status

`MIXED_PRECISION_HMC_SMOKE_PASSED`

## Objective

Test the mixed-precision boundary where HMC state, step size, leapfrog
bookkeeping, and MH diagnostics remain FP64, while the experimental
LEDH-PFPF-OT DPF target computes value/score internally in FP32/TF32 and
returns FP64-compatible tensors to TFP HMC.

This result does not establish HMC readiness, posterior correctness, chain
convergence, production readiness, public API readiness, TF32 superiority, or
full FP32 HMC mechanics.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Engineering question | Can FP64 HMC consume a DPF target that computes internally in FP32/TF32 and returns FP64-compatible value/score tensors? |
| Baseline/comparator | Phase 5 CPU FP64 mechanics smoke and the previous GPU TF32 failure caused by dtype plumbing. |
| Primary criterion | Passed: CPU FP32-no-TF32 and trusted GPU0 FP32/TF32 mixed-precision HMC smokes exited 0 with finite hard-veto diagnostics. |
| Veto diagnostics | No non-finite initial value/score, samples, target log prob, or log accept ratios; MH trace present; GPU tensors placed on GPU0. |
| Explanatory diagnostics | Acceptance rate was `1.0` on the tiny short smoke; runtime and trace values are explanatory only. |
| What will not be concluded | No HMC readiness, posterior correctness, convergence, TF32 superiority, production/default readiness, or full FP32 HMC mechanics. |
| Artifact preserving result | This result plus the JSON/Markdown/log artifacts below. |

## Skeptical Audit

- Wrong baseline: this run answers the mixed-precision target-boundary question,
  not the full FP32 HMC-state question.
- Proxy metric risk: acceptance rate, target trace values, and runtime are not
  promotion criteria.
- Missing stop condition: non-finite value/score, samples, target log prob, log
  accept ratio, missing MH trace, or wrong GPU placement would block passage.
- Unfair comparison: no speed, accuracy, or precision ranking is made.
- Hidden assumption: HMC sees FP64-compatible value/score tensors; the adapter
  owns internal DPF computation dtype.
- Environment mismatch: GPU evidence was run through the trusted GPU wrapper.
- Artifact adequacy: JSON records `hmc_state_dtype`, target computation dtype,
  TF32 mode, device placement, hard-veto flags, and nonclaims.

## What Changed

- `bayesfilter/inference/hmc.py`
  - promotes incoming HMC initial state tensors with `tf.cast(..., tf.float64)`
    instead of failing when a tensor is already `float32`;
  - records top-level `initial_state_shape` and `initial_state_dtype` metadata.
- `bayesfilter/inference/batched_value_score.py`
  - casts adapter-returned value/score tensors to the requested HMC target dtype
    after conversion, allowing FP32/TF32 target internals to feed FP64 HMC.
- `docs/benchmarks/run_experimental_batched_ledh_pfpf_ot_hmc_mechanics_smoke.py`
  - makes the FP64-HMC/target-internal-DPF-dtype boundary explicit;
  - casts initial HMC state to FP64;
  - records a `mixed_precision_contract` in output artifacts.
- `scripts/run_hmc_gpu_smoke.sh`
  - adds a narrow GPU0 mixed-precision DPF TF32 smoke wrapper to avoid long
    inline trusted-command approval paths.

## Gate Evidence

| Check | Artifact or log | Status |
| --- | --- | --- |
| Focused dtype tests | pytest: `tests/test_batched_value_score.py::test_reviewed_value_score_target_casts_adapter_outputs_to_hmc_dtype` and `tests/test_nonlinear_ssm_phase4_full_chain_hmc.py::test_phase4_full_chain_hmc_promotes_float32_initial_state_to_fp64_state` | Passed: `2 passed` |
| CPU mixed-precision smoke | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-mixed-precision-hmc-smoke-fp32-notf32-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.json` | Passed: `overall_passed=true`, hard veto passed |
| Trusted GPU0 mixed-precision smoke | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-mixed-precision-hmc-smoke-fp32-tf32-gpu0-b1-t3-np8-d2-m2-active-odd-2026-06-17.json` | Passed: `overall_passed=true`, hard veto passed, GPU placement verified |
| GPU full log | `docs/benchmarks/logs/mixed-precision-hmc-smoke-fp32-tf32-gpu0-b1-t3-np8-d2-m2-active-odd-2026-06-17.log` | Written |
| Diff hygiene | `git diff --check` | Passed before result write |

## Mixed-Precision Contract Observed

The trusted GPU0 artifact records:

| Field | Value |
| --- | --- |
| HMC state dtype | `float64` |
| Target computation dtype | `float32` |
| Target return dtype seen by HMC | `float64` |
| TF32 execution enabled | `true` |
| Boundary | `FP64 HMC state -> adapter casts to DPF dtype -> value/score cast back to HMC state dtype by reviewed target wrapper` |

Hard-veto diagnostics:

- finite samples: `true`;
- finite log accept ratios: `true`;
- finite target log prob: `true`;
- nonfinite log accept count: `0`;
- trace keys included `is_accepted`, `log_accept_ratio`, and
  `target_log_prob`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit at run time | `70ab32644cedeb95d4b56e096448f3bb2c908763` |
| Repository | `/home/ubuntu/python/BayesFilter` |
| Python/env | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| TensorFlow | GPU artifact recorded TensorFlow `2.20.0` |
| GPU | Trusted GPU0, NVIDIA RTX 4080 SUPER visible as `/device:GPU:0` |
| Shape | `B=1,T=3,N=8,D=2,M=2`, active-odd transport |
| Plan file | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-mixed-precision-hmc-smoke-subplan-2026-06-17.md` |
| Result file | This file |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Accept mixed FP64-HMC/FP32-TF32-target smoke as passed on tiny fixture | Passed | No hard veto fired | Tiny fixture and short chain only | Add larger replicated mixed-precision HMC-facing diagnostics before any readiness claim | HMC readiness, posterior correctness, convergence, TF32 superiority, full FP32 HMC mechanics |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for CPU FP32-no-TF32 and trusted GPU0 FP32/TF32 mixed smokes. |
| Statistically supported ranking | Not established. |
| Descriptive-only differences | Acceptance, runtime, and trace values are descriptive only. |
| Default-readiness | Not established. |
| Next evidence needed | Larger replicated score/target fixtures and longer HMC diagnostics with declared posterior/reference criteria. |

## Post-Run Red-Team Note

The strongest alternative explanation is that the tiny fixture and short chain
are too small to expose energy error, target nondeterminism, or larger-shape
precision pathologies. The result would be weakened by larger mixed-precision
runs where target values, scores, log accept ratios, or samples become
non-finite, or where TF32 score drift becomes comparable to PF Monte Carlo
variability. This result resolves the immediate dtype-plumbing blocker for the
mixed architecture; it does not validate posterior sampling.
