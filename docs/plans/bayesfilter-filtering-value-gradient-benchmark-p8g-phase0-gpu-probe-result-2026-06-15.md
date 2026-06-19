# P8g-G0 Result: Trusted GPU Device And Backend Gate

Date: 2026-06-15

Status: `PASS_P8G_G0_GPU_TRUSTED_PROBE_REVIEWED`

## Phase Objective

Establish the trusted GPU/CUDA/TensorFlow/XLA baseline required before any
serious P8g GPU implementation, tuning, or gradient claim.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the trusted GPU backend usable for P8g serious execution? |
| Baseline/comparator | Local CPU-only P8e diagnostics plus local GPU policy. |
| Primary criterion | Trusted GPU probe sees at least one usable GPU and TensorFlow can run a tiny GPU matmul and XLA probe. |
| Veto diagnostics | Non-escalated GPU failure used as evidence; no GPU visible in trusted context; TensorFlow GPU probe fails; XLA probe fails without reviewed exception; artifact lacks command/environment manifest. |
| Explanatory diagnostics | Driver/CUDA versions, memory, TensorFlow device placement, XLA details. |
| Not concluded | Algorithm speedup, correctness, value accuracy, gradient correctness, or HMC readiness. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `eae3f22fb8fe4a7740d7dc67066522303aaaf083` |
| Worktree state | Dirty before G0; unrelated Zhao-Cui/SGQF/P8 plan/code/doc changes and untracked P8g planning artifacts were preserved. |
| Repo root | `/home/chakwong/BayesFilter` |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| Python version | `3.11.14` |
| Platform | `Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.35` |
| GPU trust context | Trusted/escalated Codex command execution, per repo GPU policy. |
| CPU/GPU status | GPU visible and used for TensorFlow matmul and XLA probe. |
| Data version | N/A |
| Random seeds | N/A |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-subplan-2026-06-15.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md` |

## Commands Run

Non-GPU local checks:

```bash
git rev-parse HEAD
git status --short
git diff --check
```

Trusted GPU checks:

```bash
nvidia-smi
python - <<'PY'
import json
import os
import platform
import sys
import time

result = {
    "python": sys.version,
    "executable": sys.executable,
    "platform": platform.platform(),
    "cwd": os.getcwd(),
}
try:
    import tensorflow as tf
    import tensorflow_probability as tfp
    result["tensorflow_version"] = tf.__version__
    result["tfp_version"] = tfp.__version__
    result["built_with_cuda"] = bool(tf.test.is_built_with_cuda())
    result["physical_gpus"] = [d.name for d in tf.config.list_physical_devices("GPU")]
    result["logical_gpus"] = [d.name for d in tf.config.list_logical_devices("GPU")]
    result["visible_devices"] = [d.name for d in tf.config.get_visible_devices()]
    with tf.device("/GPU:0"):
        a = tf.constant([[1.0, 2.0], [3.0, 4.0]], dtype=tf.float64)
        b = tf.matmul(a, a)
        result["matmul_device"] = b.device
        result["matmul_value"] = b.numpy().tolist()
        @tf.function(jit_compile=True)
        def tiny_xla(x):
            return tf.linalg.matmul(x, x) + tf.eye(tf.shape(x)[0], dtype=x.dtype)
        start = time.time()
        c = tiny_xla(a)
        result["xla_device"] = c.device
        result["xla_value"] = c.numpy().tolist()
        result["xla_wall_seconds"] = time.time() - start
    result["status"] = "PASS"
except Exception as exc:
    result["status"] = "FAIL"
    result["error_type"] = type(exc).__name__
    result["error"] = str(exc)
print(json.dumps(result, indent=2, sort_keys=True))
if result.get("status") != "PASS":
    raise SystemExit(1)
PY
```

## Probe Results

`git diff --check`: passed.

`nvidia-smi` trusted probe:

- NVIDIA-SMI: `590.57`
- Driver version: `591.86`
- CUDA version reported by driver: `13.1`
- GPU: `NVIDIA GeForce RTX 4080 SUPER`
- GPU memory: `3498 MiB / 16376 MiB` at probe time
- Temperature/power at probe time: `48C`, `40W / 320W`
- Compute mode: `Default`

TensorFlow/TFP trusted probe:

```json
{
  "built_with_cuda": true,
  "executable": "/home/chakwong/anaconda3/envs/tf-gpu/bin/python",
  "logical_gpus": [
    "/device:GPU:0"
  ],
  "matmul_device": "/job:localhost/replica:0/task:0/device:GPU:0",
  "matmul_value": [
    [
      7.0,
      10.0
    ],
    [
      15.0,
      22.0
    ]
  ],
  "physical_gpus": [
    "/physical_device:GPU:0"
  ],
  "status": "PASS",
  "tensorflow_version": "2.19.1",
  "tfp_version": "0.25.0",
  "visible_devices": [
    "/physical_device:CPU:0",
    "/physical_device:GPU:0"
  ],
  "xla_device": "/job:localhost/replica:0/task:0/device:GPU:0",
  "xla_value": [
    [
      8.0,
      10.0
    ],
    [
      15.0,
      23.0
    ]
  ],
  "xla_wall_seconds": 0.16100072860717773
}
```

TensorFlow startup emitted duplicate cuFFT/cuDNN/cuBLAS factory registration
messages and AutoGraph source-code warnings for the inline probe. These did not
block GPU device creation, GPU matmul, or XLA compilation. TensorFlow reported
GPU device creation with `13495 MB` memory and compute capability `8.9`.

## Gate Assessment

Decision: `PASS_P8G_G0_GPU_TRUSTED_PROBE_REVIEWED`.

| Criterion | Status | Evidence |
|---|---|---|
| Trusted GPU visible | Pass | `nvidia-smi` sees RTX 4080 SUPER; TensorFlow lists `/physical_device:GPU:0` and `/device:GPU:0`. |
| TensorFlow built with CUDA | Pass | `built_with_cuda: true`. |
| Tiny GPU matmul | Pass | Matmul ran on `/device:GPU:0` and returned expected value. |
| Tiny GPU XLA probe | Pass | XLA service initialized for CUDA, compiled a cluster, and output tensor ran on `/device:GPU:0`. |
| Local formatting check | Pass | `git diff --check` returned clean. |
| Artifact manifest | Pass | This result records commit, dirty summary, environment, commands, GPU, TensorFlow, TFP, XLA, and nonclaims. |
| Review gate | Pass | Claude read-only review returned `VERDICT: AGREE` and is recorded in the canonical review ledger. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Pass G0 probe after required review | Trusted GPU, TensorFlow GPU matmul, XLA GPU probe, and G0 review gate pass. | No G0 veto fired in trusted context. | Later P8g code may still have device fallback, vectorization, parity, tuning, gradient, or HMC failures. | Refresh/execute G1 only through its subplan and command/artifact contract. | No speedup, algorithm correctness, particle-count adequacy, gradient correctness, HMC readiness, callback closure, stochastic PF marginal validity, or filter ranking. |

## Next-Phase Handoff

G0 handoff conditions are met:

1. Claude read-only review of this G0 result converged with `VERDICT: AGREE`;
2. the review is recorded in
   `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-execution-ledger-2026-06-15.md`;
3. this result status is
   `PASS_P8G_G0_GPU_TRUSTED_PROBE_REVIEWED`;
4. the G1 subplan cites this result as its trusted GPU manifest.

No G1 profiling, G2 implementation, G4 tuning, or G6 HMC command is launched by
this result.
