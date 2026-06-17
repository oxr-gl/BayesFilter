# BayesFilter DPF LEDH-PFPF-OT TF32 Default Policy Result - 2026-06-15

## Decision

Default TF32 for the experimental LEDH-PFPF-OT GPU/performance lane is now
implemented as `float32` tensors with TensorFlow TF32 execution enabled.

This is a scoped default. It does not change the global BayesFilter numerical
policy, and it does not remove FP64 reference or FP32-no-TF32 comparison lanes.

## What Changed

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  now exposes the scoped default policy:
  - `DEFAULT_DTYPE = tf.float32`
  - `DEFAULT_TF32_MODE = "enabled"`
  - `precision_policy_metadata()`
- The experimental batched LEDH-PFPF-OT module synchronizes shared transport
  helper dtype at the experimental transport entry point.
- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`
  now defaults to `--dtype float32 --tf32-mode enabled`.
- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_lgssm_scale.py`
  now has explicit precision flags and defaults to `float32` with TF32 enabled.
- `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_gradient_structure.py`
  now defaults to the TF32 candidate for ad hoc runs, while aggregate precision
  scripts still launch explicit FP64/FP32/TF32 arms.
- Correctness/reference paths are pinned to FP64:
  - `docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_correctness.py`
  - `docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py`
  - `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_cpu_gpu.py`
  - `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`
- The shared `annealed_transport_tf.py` standalone default remains FP64 to
  avoid changing older FilterFlow/reference lanes.

## Verification

Syntax check passed:

```bash
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_lgssm_scale.py \
  docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_cpu_gpu.py \
  docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_correctness.py \
  docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py \
  docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_gradient_structure.py \
  docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_pf_mc_error_vs_precision.py \
  tests/test_experimental_batched_ledh_pfpf_ot_tf.py
```

Trusted GPU default smoke passed:

```bash
timeout 180 /home/ubuntu/anaconda3/envs/tfgpu/bin/python \
  docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  --device-scope visible --cuda-visible-devices 0 --device /GPU:0 \
  --expect-device-kind gpu --batch-size 1 --time-steps 2 \
  --num-particles 4 --state-dim 2 --obs-dim 2 \
  --transport-policy active-odd --sinkhorn-iterations 2 \
  --row-chunk-size 2 --col-chunk-size 2 --particle-chunk-size 2 \
  --warmups 0 --repeats 1 \
  --output /tmp/bayesfilter_ledh_tf32_default_smoke.json \
  --markdown-output /tmp/bayesfilter_ledh_tf32_default_smoke.md
```

Observed metadata:

```json
{
  "active_dtype": "float32",
  "default_dtype": "float32",
  "default_tf32_mode": "enabled",
  "dtype": "float32",
  "precision_default_policy": "experimental_ledh_pfpf_ot_gpu_tf32",
  "scope": "experimental_batched_ledh_pfpf_ot_gpu_performance_lane",
  "tf32_execution_enabled": true,
  "tf32_mode": "enabled",
  "tf_dtype": "float32"
}
```

The smoke was finite, GPU placed, and XLA compiled.

FP64 streaming correctness smoke passed:

```bash
timeout 180 /home/ubuntu/anaconda3/envs/tfgpu/bin/python \
  docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py \
  --device-scope cpu --device /CPU:0 --expect-device-kind cpu \
  --batch-size 2 --time-steps 2 --num-particles 3 \
  --transport-policy no-resampling --sinkhorn-iterations 2 \
  --row-chunk-size 2 --col-chunk-size 2 --particle-chunk-size 2 \
  --skip-score-fd \
  --output /tmp/bayesfilter_ledh_fp64_streaming_correctness_smoke.json \
  --markdown-output /tmp/bayesfilter_ledh_fp64_streaming_correctness_smoke.md
```

The FP64 smoke reported `overall_passed: true`. TensorFlow emitted a CUDA init
warning during the CPU run, but the artifact reported `CUDA_VISIBLE_DEVICES=-1`,
CPU tensor placement, and no GPU devices.

## Decision Table

| Field | Status |
| --- | --- |
| Default-policy decision | Adopted for experimental LEDH-PFPF-OT GPU/performance lane only. |
| Primary criterion | Passed. Default benchmark precision is `float32` with TF32 enabled and metadata records the policy. |
| Veto diagnostics | No syntax failure. GPU default smoke finite/JIT/GPU placed. FP64 correctness smoke still passes. |
| Main uncertainty | HMC score path is still not fully JIT-ready; downstream HMC energy/acceptance impact remains untested. |
| Next justified action | Use TF32 by default for performance runs; keep FP64/FP32-no-TF32 arms in precision and correctness comparisons. |
| What is not concluded | No production-wide dtype policy, no HMC correctness claim, no posterior validity claim. |

## Inference Status

| Evidence class | Interpretation |
| --- | --- |
| Hard veto screen | No hard veto fired for this scoped default change. |
| Statistically supported ranking | None. The prior six-seed MC comparison was descriptive. |
| Descriptive-only differences | Prior result showed TF32 value drift at about `1.06%` of PF value SD and score L2 drift at about `6.51%` of FP64 PF score-SD norm. |
| Default-readiness | Ready as a scoped experimental GPU/performance default, not as a global production default. |
| Next evidence needed | Larger-shape MC-noise comparison after JIT-safe score work, plus HMC energy/acceptance diagnostics. |

## Post-Run Red-Team Note

- Strongest alternative explanation: the small MC-noise fixture may understate
  TF32 accumulation effects in larger `T,N,D`, sharper likelihoods, or more
  Sinkhorn iterations.
- Result that would overturn the scoped default: TF32 score drift near or above
  one PF MC SD on a realistic JIT-safe fixture, or HMC diagnostics showing
  persistent energy error or degraded acceptance.
- Weakest evidence: the HMC-relevant score path still needs JIT-safe validation.
- Guardrail: all correctness/reference scripts touched here retain explicit
  FP64 controls.
