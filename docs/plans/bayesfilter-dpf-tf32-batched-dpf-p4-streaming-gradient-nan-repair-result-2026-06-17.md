# Phase 4 Result - Streaming Transport NaN Gradient Repair - 2026-06-17

## Status

`PHASE_4_STREAMING_GRADIENT_NAN_REPAIR_PASSED`

## Objective

Repair the non-finite raw TensorFlow gradient in the memory-efficient
streaming active transport path, while preserving active transport values and
without claiming HMC, posterior, production, default-policy, or public API
readiness.

## Entry Conditions

- Phase 0 through Phase 3 had passed.
- Phase 4 no-resampling score/JIT repair had passed.
- Active-odd dense transport score arms were finite and matched.
- Active-odd streaming transport value arms were finite and matched dense
  values.
- Active-odd streaming transport score arms were non-finite before this repair.

## Skeptical Audit

- Wrong baseline: the comparator remained the tiny dense transport arm and the
  prior active-odd artifact with NaN streaming scores, not a speed or HMC
  metric.
- Proxy metric risk: compile time and warm time were explanatory only.
- Missing stop condition: non-finite score, value mismatch, JIT failure, or
  no-resampling regression would stop the phase.
- Unfair comparison: dense transport was used only as a tiny reference arm, not
  as a scalable competitor.
- Hidden assumption: exact-chunk streaming success did not imply padded-chunk
  success, so a dedicated oversized-chunk localization was required.
- Environment mismatch: CPU-only FP64 gates intentionally hid GPU devices and
  do not support GPU performance claims.
- Artifact adequacy: localization, active-odd, and no-resampling artifacts
  directly answer the phase question.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the active streaming transport score path be finite under JIT on the tiny active-odd fixture without changing active transport values? |
| Baseline/comparator | Dense transport tiny reference plus prior active-odd NaN artifact. |
| Primary criterion | Active-odd FP64 gradient-structure harness exits 0, all arms finite, JIT compile true, and streaming scores match dense within tolerance. |
| Criterion status | Passed. |
| Veto diagnostics | No non-finite scores; no value drift; no JIT failure; no no-resampling regression. |
| Explanatory diagnostics | NaN localized to padded streaming column log normalizer backward pass; exact chunks passed; oversized chunks passed after repair. |
| Not concluded | No HMC readiness, no posterior validity, no production/default/public API readiness, no 100k-particle score proof, no GPU performance claim. |

## What Changed

- Added a finite log-zero sentinel for padded streaming log-domain entries in
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
- Replaced padded `-inf` entries in streaming softmin, column normalizer, and
  transport application with that finite sentinel where padding participates in
  differentiable log-domain reductions.
- Normalized TensorFlow `while_loop` `loop_vars` container types from lists to
  tuples where loop bodies returned tuples, fixing eager-mode structure
  mismatches exposed by focused tests.
- Added a focused localization script:
  `docs/benchmarks/localize_experimental_batched_ledh_pfpf_ot_streaming_gradient_nan.py`.

The repair route is raw streaming gradient stabilization. It is not a dense
gradient hybrid and not a custom-gradient route.

## Localization Evidence

| Artifact | Result |
| --- | --- |
| `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-streaming-gradient-nan-localization-2026-06-17.md` | Oversized chunks before repair: dense, streaming softmin, and streaming Sinkhorn potentials finite; first non-finite gradient in streaming column log normalizer. |
| `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-streaming-gradient-nan-localization-exact-chunks-2026-06-17.md` | Exact chunk sizes passed, isolating the issue to padding/backward behavior rather than the streaming equations. |
| `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-streaming-gradient-nan-localization-repaired-rerun-2026-06-17.md` | Oversized chunks passed after repair with all probe outputs and gradients finite under JIT. |

## Gate Evidence

| Check | Artifact or log | Status |
| --- | --- | --- |
| Python compile | `docs/benchmarks/logs/p4-pycompile-nan-repair-rerun-2026-06-17.log` | Passed |
| Focused streaming tests | `docs/benchmarks/logs/p4-streaming-pytest-nan-repair-rerun-2026-06-17.log` | Passed: 8 passed |
| Active-odd FP64 score/JIT | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-nan-repair-rerun-2026-06-17.json` | Passed: `overall_passed=true`, `finite_all=true`, `structure_passed=true` |
| No-resampling FP64 regression | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-nan-repair-rerun-2026-06-17.json` | Passed: `overall_passed=true`, `finite_all=true`, `structure_passed=true` |
| Diff hygiene | `git diff --check` | Passed |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit at run time | `70ab32644cedeb95d4b56e096448f3bb2c908763` |
| Conda/env | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| Device scope | CPU-only gates with `CUDA_VISIBLE_DEVICES=-1` |
| TensorFlow version | Recorded in JSON artifacts; active rerun used TensorFlow `2.20.0` |
| Primary shape | `B=1,T=3,N=8,D=2,M=2` |
| Precision | FP64 reference gates, TF32 disabled |
| Seeds | Benchmark harness default seed `20260615` |
| Plan file | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-streaming-gradient-nan-repair-subplan-2026-06-17.md` |
| Result file | This file |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 4 streaming-gradient NaN repair as passed | Passed | No veto fired | Only tiny deterministic CPU FP64 score/JIT fixture covered | Draft Phase 5 HMC-facing diagnostics subplan | HMC readiness, posterior validity, production/default readiness, GPU-scale score proof |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the scoped tiny active-odd and no-resampling score/JIT gates. |
| Statistically supported ranking | Not applicable; deterministic structure checks only. |
| Descriptive-only differences | Compile and warm timings are recorded but not interpreted as speed evidence. |
| Default-readiness | Not established. |
| Next evidence needed | Phase 5 must test HMC-facing value/gradient precision and energy/acceptance diagnostics under a separate evidence contract. |

## Post-Run Red-Team Note

The strongest alternative explanation is that the tiny fixture is too small to
expose a remaining instability in larger active transport score paths. The
repair would be weakened by any future larger-shape active score/JIT artifact
that produces non-finite gradients or value/score drift against an appropriate
reference. The weakest part of the evidence is scale: this phase establishes a
JIT-safe tiny active score path, not a 100k-particle score proof.
