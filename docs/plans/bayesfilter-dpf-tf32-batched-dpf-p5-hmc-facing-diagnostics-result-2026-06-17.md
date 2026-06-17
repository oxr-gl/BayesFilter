# Phase 5 Result - HMC-Facing Diagnostics - 2026-06-17

## Status

`PHASE_5_HMC_FACING_DIAGNOSTICS_PASSED_WITH_GPU_HMC_TF32_LIMITATION`

## Objective

Run bounded HMC-facing diagnostics after the streaming active-transport score
path became JIT-safe. The phase tested value/gradient precision relative to a
small PF Monte Carlo variability proxy and ran a tiny HMC mechanics smoke.

This result does not establish HMC readiness, posterior correctness, chain
convergence, production readiness, public API readiness, or TF32 superiority.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are TF32/FP32 value and gradient errors small relative to PF Monte Carlo variability on bounded fixtures, and do tiny HMC mechanics checks avoid hard vetoes? |
| Baseline/comparator | FP64 score/JIT reference lane; FP32-no-TF32 lane; rerun three-seed FP64 PF variability proxy. |
| Primary criterion | No hard veto; TF32/FP32 drift small relative to FP64 seed-to-seed variability on the tested fixture; tiny mechanics smoke finite with MH/log-accept diagnostics. |
| Criterion status | Passed for CPU/GPU value-score precision and CPU FP64 HMC mechanics; GPU TF32 full-chain HMC mechanics was not run because the generic HMC runner currently hard-casts initial state to FP64. |
| Veto diagnostics | No non-finite value/gradient in required score/JIT/precision artifacts; no CPU FP64 mechanics non-finite; trusted GPU value/score placement passed. |
| Explanatory diagnostics | Runtime and acceptance are descriptive only; short-chain acceptance rate is not a promotion criterion. |
| Not concluded | No posterior correctness, no chain convergence, no production/default readiness, no superiority ranking, no 100k-particle score scalability proof. |

## Skeptical Audit

- Wrong baseline: the previous PF MC artifact from 2026-06-15 had failed, so
  Phase 5 reran a fresh three-seed PF MC-vs-precision comparator instead of
  reusing invalid evidence.
- Proxy metric risk: acceptance rate, runtime, and compile time are explicitly
  explanatory only.
- Missing stop condition: non-finite values, non-finite gradients, failed
  score/JIT guardrail, missing FP64 reference, wrong GPU placement, or missing
  MC comparator would stop interpretation.
- Unfair comparison: dense transport is a tiny reference where used; no method
  superiority or speed ranking is claimed.
- Hidden assumption: CPU TF32 is effectively not GPU tensor-core TF32, so a
  trusted GPU value/score precision run was required and was executed.
- Environment mismatch: GPU value/score evidence ran in trusted GPU context;
  GPU full-chain HMC mechanics could not be executed without changing shared
  HMC runtime dtype semantics.
- Artifact adequacy: JSON/Markdown artifacts preserve FP64 guardrail,
  CPU/GPU precision-vs-MC diagnostics, and CPU HMC mechanics smoke.

## What Changed

- Added `--child-jit-compile` to
  `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_pf_mc_error_vs_precision.py`
  so Phase 5 precision-vs-MC child score runs can be JIT compiled.
- Added
  `docs/benchmarks/run_experimental_batched_ledh_pfpf_ot_hmc_mechanics_smoke.py`
  for a tiny fixed-kernel HMC mechanics smoke over the repaired streaming DPF
  value/score adapter.

No BayesFilter public API was changed. No default precision policy was changed.

## Gate Evidence

| Check | Artifact or log | Status |
| --- | --- | --- |
| FP64 active-odd score/JIT guardrail | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p5-guardrail-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.json` | Passed: `overall_passed=true`, `finite_all=true`, `structure_passed=true` |
| CPU JIT PF MC-vs-precision | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p5-pf-mc-error-vs-precision-cpu-jit-b1-t3-np8-d2-m2-seeds3-active-odd-2026-06-17.json` | Passed |
| GPU0 JIT PF MC-vs-precision | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p5-pf-mc-error-vs-precision-gpu0-jit-b1-t3-np8-d2-m2-seeds3-active-odd-2026-06-17.json` | Passed in trusted GPU context |
| CPU FP64 HMC mechanics smoke | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p5-hmc-mechanics-smoke-fp64-cpu-b1-t3-np8-d2-m2-active-odd-rerun-2026-06-17.json` | Passed: finite samples, finite target log prob, finite log accept ratios, MH trace present |
| GPU TF32 HMC mechanics smoke | `docs/benchmarks/logs/p5-hmc-mechanics-smoke-fp32-tf32-gpu0-b1-t3-np8-d2-m2-active-odd-2026-06-17.log` | Not a sampler veto; script/runtime dtype mismatch because generic HMC runner hard-casts initial state to FP64 |
| Final py_compile | `docs/benchmarks/logs/p5-final-pycompile-2026-06-17.log` | Passed |
| Diff hygiene | `git diff --check` | Passed |

## Precision Vs PF Variability

The GPU0 JIT three-seed active-odd diagnostic reported:

| Precision arm | Max value RMS / FP64 sample SD | Max score RMS / FP64 sample SD | Evidence class |
| --- | ---: | ---: | --- |
| FP32 no TF32 | `2.5213270905237544e-05` | `1.896581015148424e-05` | descriptive viability screen |
| FP32 with TF32 | `9.623909211576227e-05` | `0.0009484052802509225` | descriptive viability screen |

On this tiny fixture, TF32 value drift was below `0.01%` of the FP64
seed-to-seed value SD and TF32 score drift was below `0.1%` of the FP64
seed-to-seed score SD. This supports continued TF32 diagnostics on bounded
fixtures. It is not a statistical ranking and not a production default claim.

## HMC Mechanics Smoke

The CPU FP64 mechanics smoke used a tiny fixed-kernel TFP HMC run with:

- shape `B=1,T=3,N=8,D=2,M=2`;
- active-odd transport;
- `num_results=6`, `num_burnin_steps=2`, `num_leapfrog_steps=2`;
- fixed step size `0.002`;
- no sampler adaptation;
- no full-chain XLA claim.

It passed hard veto checks:

- initial value/score finite;
- samples finite;
- target log probability trace finite;
- log accept ratio trace finite;
- MH acceptance trace present;
- nonfinite log accept count `0`.

The observed acceptance rate was `1.0`, which is explanatory only for this very
short smoke.

## Limitation

The generic BayesFilter HMC runner currently converts `initial_state` to
`tf.float64` internally. That is compatible with the CPU FP64 mechanics smoke
but blocks a direct FP32/TF32 full-chain HMC mechanics smoke without a broader,
reviewed HMC-runtime dtype change. Phase 5 therefore treats GPU TF32 evidence
as value/score precision evidence, not full-chain TF32 HMC mechanics evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit at run time | `70ab32644cedeb95d4b56e096448f3bb2c908763` |
| Conda/env | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| TensorFlow version | Recorded in JSON artifacts; mechanics smoke used TensorFlow `2.20.0` |
| GPU | GPU0 trusted value/score precision run, NVIDIA RTX 4080 SUPER |
| Primary fixture | `B=1,T=3,N=8,D=2,M=2`, active-odd, three seeds for precision-vs-MC |
| Plan file | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p5-hmc-facing-diagnostics-subplan-2026-06-17.md` |
| Result file | This file |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 5 as passed with GPU TF32 full-chain mechanics limitation | Passed for score/JIT, CPU/GPU precision-vs-MC, and CPU FP64 mechanics smoke | No hard veto fired in completed gates | Tiny fixture and short chain only; no GPU TF32 full-chain HMC mechanics due to HMC runner FP64 cast | Phase 6 closeout/guardrails and optional reviewed HMC runtime dtype subplan | HMC readiness, posterior correctness, convergence, production/default readiness, TF32 superiority |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for completed score/JIT, precision, and CPU mechanics gates. |
| Statistically supported ranking | Not established. |
| Descriptive-only differences | TF32/FP32 drift ratios, runtime, and acceptance are descriptive only. |
| Default-readiness | Not established. |
| Next evidence needed | Larger replicated fixtures; reviewed HMC runtime dtype policy if direct FP32/TF32 full-chain mechanics is required; longer HMC diagnostics with uncertainty and convergence checks. |

## Post-Run Red-Team Note

The strongest alternative explanation is that the tiny fixture understates
precision and HMC mechanics issues that could appear at larger `T`, `N`, or
state dimension. The result would be weakened by a larger replicated fixture
where TF32 score drift becomes comparable to PF seed-to-seed variability, or by
a reviewed FP32/TF32 full-chain HMC mechanics run that produces non-finite
energy/log-accept diagnostics. The weakest part of the evidence is scale and
chain length; Phase 5 is a bounded viability screen, not a sampler validation.
