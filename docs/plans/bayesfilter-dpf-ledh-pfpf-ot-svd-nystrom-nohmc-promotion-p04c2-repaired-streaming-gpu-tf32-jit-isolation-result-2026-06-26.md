# P04C2 Repaired Result: Streaming GPU TF32/JIT Isolation

Date: 2026-06-26

Status: `P04C2_GPU_DEVICE_STREAMING_INVALID`

## Phase Objective

Disentangle the P04C1 seed `84101` streaming comparator nonfinite diagnostic by
isolating GPU device execution, TF32, and JIT/XLA factors for the streaming
route only.

This repaired rerun used the P04C2A opt-in exception-capture harness repair so
route exceptions are serialized as structured hard-veto artifacts rather than
missing JSON/Markdown artifacts.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `P04C2_GPU_DEVICE_STREAMING_INVALID` |
| Primary criterion status | MET for isolation classification: all three P04C2 repaired row artifacts were produced and parsed. |
| Veto diagnostic status | GPU no-TF32/no-JIT seed `84101` streaming row failed with structured `route_exception`; P04C1 CPU no-TF32/no-JIT seed `84101` control passed. |
| Main uncertainty | P04C2 identifies GPU/device execution as sufficient for streaming invalidity on this seed, but does not repair the streaming route or determine whether jitter/solve stabilization would restore validity. |
| Next justified action | Draft and review a P04C3 streaming comparator robustness diagnostic/repair subplan before any P04C calibration continuation. |
| What is not concluded | No threshold freeze, no P04C resume, no seed exclusion, no SVD-Nystrom rejection, no P05 launch, no promotion/default/scientific/HMC claim, no posterior correctness claim, and no statistical superiority claim. |

## Evidence Contract Outcome

| Field | Contract Outcome |
| --- | --- |
| Question | Answered diagnostically: GPU/device execution is sufficient to invalidate the seed `84101` streaming comparator, because GPU no-TF32/no-JIT fails while P04C1 CPU no-TF32/no-JIT passed. |
| Baseline/comparator | P04C1 GPU/TF32/JIT-on seed `84101` streaming failure and P04C1 CPU/no-JIT/TF32-disabled seed `84101` streaming pass. |
| Primary criterion | Met: exact row artifacts were produced and parsed after P04C2A repaired exception artifact capture. |
| Veto diagnostics | No malformed P04C2 repaired artifacts. Runtime hard vetoes fired in all GPU streaming rows. |
| Explanatory diagnostics | Route exceptions, nonfinite route outputs, TF32/JIT/GPU toggles, log likelihood, ESS, and timing. |
| Not concluded | No calibrated threshold, no repaired P04C panel, no seed handling decision, no P05 launch, and no promotion/default/scientific/HMC claim. |
| Artifact | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-summary-2026-06-26.json` |

## Repaired Diagnostic Rows

Trusted GPU preflight selected GPU1 under the owner rule "GPU1 if available,
otherwise GPU0":

| GPU | Memory used | Total memory | Utilization |
| ---: | ---: | ---: | ---: |
| 0 | 1226 MiB | 32760 MiB | 40% |
| 1 | 18 MiB | 32760 MiB | 0% |

All rows used seed `84101`, route `streaming`, range-bearing fixture, `T=20`,
`N=4096`, `float32`, active-all transport, and `--capture-route-exceptions`.

| Row | Device / mode | Status | Route hard vetoes | Structured exception |
| --- | --- | --- | --- | --- |
| `gpu-tf32-nojit-84101` | GPU1, TF32 enabled, JIT off | `FAIL` | `route_exception` | TensorFlow `InvalidArgumentError`, `MatrixInverse`, `Input is not invertible` |
| `gpu-notf32-jit-84101` | GPU1, TF32 disabled, JIT on | `FAIL` | `nonfinite_log_likelihood`, `nonfinite_filtered_means`, `nonfinite_filtered_variances`, `nonfinite_ess_by_time` | None |
| `gpu-notf32-nojit-84101` | GPU1, TF32 disabled, JIT off | `FAIL` | `route_exception` | TensorFlow `InvalidArgumentError`, `MatrixInverse`, `Input is not invertible` |

## Artifacts

- Aggregate summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-summary-2026-06-26.json`
- `gpu-tf32-nojit-84101` JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-tf32-nojit-seed84101-2026-06-26.json`
- `gpu-tf32-nojit-84101` Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-tf32-nojit-seed84101-2026-06-26.md`
- `gpu-tf32-nojit-84101` log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c2-gpu-tf32-nojit-seed84101.log`
- `gpu-notf32-jit-84101` JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-jit-seed84101-2026-06-26.json`
- `gpu-notf32-jit-84101` Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-jit-seed84101-2026-06-26.md`
- `gpu-notf32-jit-84101` log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-jit-seed84101.log`
- `gpu-notf32-nojit-84101` JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-nojit-seed84101-2026-06-26.json`
- `gpu-notf32-nojit-84101` Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-nojit-seed84101-2026-06-26.md`
- `gpu-notf32-nojit-84101` log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-nojit-seed84101.log`

## Interpretation

The P04C2 repaired panel rules out a pure TF32 explanation and a pure JIT/XLA
explanation under the predeclared row logic. The discriminating row is
`gpu-notf32-nojit-84101`: it failed on GPU even with TF32 and JIT disabled,
while the P04C1 CPU/no-TF32/no-JIT control passed for the same seed.

The closest source-level diagnostic target is the streaming comparator LEDH
flow core: the route exceptions occur at TensorFlow `MatrixInverse` in the
posterior covariance inverse inside
`experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`.
This is explanatory context only. P04C2 does not authorize changing the flow
core, tuning jitter, or resuming calibration.

This result does not show that SVD-Nystrom failed. P04C1 already showed the
locked SVD-Nystrom route passed on seed `84101` in the both-route reproduction
while the streaming comparator failed.

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | GPU streaming comparator invalidity is supported for seed `84101`; P04C calibration remains blocked because the comparator is invalid. |
| Statistically supported ranking | NO |
| Descriptive-only differences | Runtime, route exception form, and nonfinite-output details are diagnostic only. |
| Default-readiness | NO |
| Next evidence needed | Reviewed P04C3 streaming comparator robustness diagnostic/repair plan. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Conda/Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| TensorFlow | `2.20.0` |
| GPU preflight | GPU1 selected: 18 MiB used, 0% utilization |
| Seeds | `84101` |
| Shape | Range-bearing fixture, `T=20`, `N=4096`, `float32` |
| Harness repair | P04C2A `--capture-route-exceptions` enabled |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-subplan-2026-06-26.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-repaired-streaming-gpu-tf32-jit-isolation-result-2026-06-26.md` |

## Post-Run Red-Team Note

Strongest alternative explanation: the CPU pass and GPU failure may reflect a
known numerical sensitivity in the LEDH posterior covariance inverse rather
than a generic GPU defect. A later P04C3 diagnostic should distinguish
implementation fragility, insufficient jitter, and a more fundamental
streaming-comparator validity problem.

Weakest part of the evidence: P04C2 isolates execution factors on one seed only
and does not test a repaired streaming route. It should block calibration but
not be overinterpreted as broad method failure.

## Handoff

`P04C2_GPU_DEVICE_STREAMING_INVALID`

Draft and review P04C3 before changing the streaming route or resuming P04C.
Do not run remaining P04C calibration seeds, do not drop seed `84101`, do not
count it as a non-exceedance, do not launch P05, and do not freeze a nonlinear
threshold.
