# Phase 2 Result - Single-GPU Batched Value Runner - 2026-06-16

## Status

`PHASE_2_PASSED`

## Objective

Verify a single-GPU runner for independent-row batched streaming
LEDH-PFPF-OT value evaluation using the current TF32 performance default.

This phase was value-only. No score path or HMC readiness was promoted.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the current streaming value path evaluate independent batch rows on one GPU under the scoped TF32 performance policy with bounded correctness guardrails? |
| Baseline/comparator | Used the streaming correctness gate with fixed-branch tiny parity, plus a tiny FP32-no-TF32 reference-lane artifact. |
| Primary pass criterion | Passed. The bounded single-GPU TF32 value artifact is finite, JIT-compiled, GPU-placed in trusted context, records precision metadata, and the tiny correctness/JIT guardrail passed. |
| Veto diagnostics | No active veto. No non-finite value, missing JIT metadata, wrong GPU device, missing precision metadata, score/HMC claim, or production/public API claim. |
| Explanatory diagnostics | Compile and warm-call timings, memory metadata, and preview values are descriptive only. They are not speed superiority evidence. |
| Not concluded | No speed superiority, no HMC readiness, no score correctness, no production default, no public API readiness, no single-filter multi-GPU particle sharding. |

## Commands And Artifacts

Tiny streaming correctness/JIT guardrail:

```bash
timeout 180 /home/ubuntu/anaconda3/envs/tfgpu/bin/python \
  docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --batch-size 2 \
  --time-steps 3 \
  --num-particles 4 \
  --transport-policy active \
  --sinkhorn-iterations 3 \
  --skip-score-fd \
  --output /tmp/bayesfilter_dpf_tf32_p2_streaming_correctness_cpu.json \
  --markdown-output /tmp/bayesfilter_dpf_tf32_p2_streaming_correctness_cpu.md
```

Artifact:

- `/tmp/bayesfilter_dpf_tf32_p2_streaming_correctness_cpu.json`

Result:

- `overall_passed: true`
- finite outputs: passed
- streaming versus fixed-branch baseline parity: passed
- likelihood-only history omission: passed
- CPU device placement: passed
- JIT compile smoke: passed
- source diagnostic: uses `tf.while_loop`, no Python time loop, no Python
  history lists, `return_history=False` default, streaming transport default.

Bounded single-GPU TF32 value run:

```bash
timeout 300 /home/ubuntu/anaconda3/envs/tfgpu/bin/python \
  docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --batch-size 4 \
  --time-steps 20 \
  --num-particles 256 \
  --state-dim 10 \
  --obs-dim 10 \
  --transport-policy active-odd \
  --proposal-mode callback \
  --sinkhorn-iterations 3 \
  --row-chunk-size 256 \
  --col-chunk-size 256 \
  --particle-chunk-size 128 \
  --warmups 0 \
  --repeats 1 \
  --dtype float32 \
  --tf32-mode enabled \
  --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p2-single-gpu-tf32-value-gpu0-b4-t20-np256-d10-m10-callback-2026-06-16.json \
  --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p2-single-gpu-tf32-value-gpu0-b4-t20-np256-d10-m10-callback-2026-06-16.md
```

Artifacts:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p2-single-gpu-tf32-value-gpu0-b4-t20-np256-d10-m10-callback-2026-06-16.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p2-single-gpu-tf32-value-gpu0-b4-t20-np256-d10-m10-callback-2026-06-16.md`

Key metadata:

- finite output: `true`
- JIT compiled: `true`
- output device: `/device:GPU:0`
- dtype: `float32`
- TF32 execution enabled: `true`
- output shape: `[4]`
- return history: `false`
- proposal mode: `callback`
- stores full pre-flow particles: `false`
- dense transport matrix materialized: `false`

Descriptive timings:

- compile plus first call: `10.665356416022405` seconds
- single warm-call timing: `0.09592609317041934` seconds

Tiny FP32-no-TF32 reference-lane artifact:

```bash
timeout 180 /home/ubuntu/anaconda3/envs/tfgpu/bin/python \
  docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --batch-size 2 \
  --time-steps 3 \
  --num-particles 4 \
  --state-dim 1 \
  --obs-dim 1 \
  --transport-policy active-odd \
  --proposal-mode callback \
  --sinkhorn-iterations 3 \
  --row-chunk-size 4 \
  --col-chunk-size 4 \
  --particle-chunk-size 4 \
  --warmups 0 \
  --repeats 1 \
  --dtype float32 \
  --tf32-mode disabled \
  --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p2-reference-fp32-notf32-value-cpu-b2-t3-np4-d1-m1-callback-2026-06-16.json \
  --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p2-reference-fp32-notf32-value-cpu-b2-t3-np4-d1-m1-callback-2026-06-16.md
```

Artifacts:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p2-reference-fp32-notf32-value-cpu-b2-t3-np4-d1-m1-callback-2026-06-16.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p2-reference-fp32-notf32-value-cpu-b2-t3-np4-d1-m1-callback-2026-06-16.md`

Key metadata:

- finite output: `true`
- JIT compiled: `true`
- output device: `/device:CPU:0`
- dtype: `float32`
- TF32 execution enabled: `false`
- return history: `false`
- dense transport matrix materialized: `false`

## Repairs During Phase

Two malformed tiny correctness commands were attempted before the successful
guardrail:

- first used `--transport-policy active-odd`, which belongs to the benchmark
  harness but not the correctness gate;
- second used `--state-dim`, which the correctness gate does not accept.

Both failed before algorithm execution via argument parsing. The successful
guardrail used the correctness gate's valid options.

## Statistical And Scientific Interpretation

This is engineering evidence only. It supports that the current streaming value
path can run a small independent-row batch on one GPU with TF32, JIT, callback
proposal mode, likelihood-only output, and no dense transport matrix
materialization.

The timing numbers are descriptive. They do not establish speed superiority,
scaling law, precision ranking, HMC validity, posterior correctness, or
production readiness.

## Phase 3 Handoff

Phase 3 may begin. Exact handoff conditions are satisfied:

- Phase 2 result records `PHASE_2_PASSED`.
- Bounded single-GPU TF32 value artifact exists and records finite output, JIT,
  GPU placement, and precision metadata.
- Tiny correctness/JIT guardrail passed.
- A tiny FP32-no-TF32 reference-lane artifact exists.
- Phase 3 subplan exists and limits multi-GPU work to independent row
  splitting.
- No human-required stop condition is active.

Start Phase 3 from:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p3-two-gpu-row-splitting-subplan-2026-06-16.md`
