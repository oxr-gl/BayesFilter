# Low-Rank Residual Posterior-Gradient Calibration Reset Memo

Date: 2026-06-25

Status: `RESET_RECOMMENDED_RUNTIME_BOUNDARY_INCONSISTENCY`

## Why This Memo Exists

The P02 GPU/XLA reproduction phase is blocked by an execution-boundary
inconsistency, not by a BayesFilter algorithm result.

Earlier BayesFilter runs in this same workspace successfully executed
TensorFlow GPU/XLA benchmarks.  For example, the N3072 second-candidate
actual-SIR low-rank validation artifact records:

- command used `--cuda-visible-devices 1 --device /GPU:0`;
- TensorFlow physical GPUs:
  `PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')`;
- TensorFlow logical GPUs:
  `LogicalDevice(name='/device:GPU:0', device_type='GPU')`;
- `jit_compile=True`;
- row status `PASS`;
- hard vetoes `[]`.

Artifact:
`docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23-b2-t20-n3072-r16-eps0p125-a1em08-it120-seed81137_81138-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float-h63fd5ec16a683262.json`

Current P02 attempts in the active Codex command context show different
effective runtime access:

- `nvidia-smi` can see GPUs;
- ordinary Python/TensorFlow sees no GPUs:
  `tf.config.list_physical_devices("GPU") == []`;
- TensorFlow is CUDA-capable: `tf.test.is_built_with_cuda() == True`;
- `/dev/nvidiactl`, `/dev/nvidia0`, `/dev/nvidia1`, and `/dev/nvidia-uvm`
  are absent inside the non-elevated sandbox;
- elevated Python benchmark launch was rejected twice by the environment
  approval reviewer;
- non-elevated visible-GPU launch started but failed before artifact creation
  with `CUDA_ERROR_NO_DEVICE`, then XLA CPU fallback failed on an unsupported
  `FakeParam` op.

Captured failure log:
`docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/p02-reproduction-gpu.log`

## Current Program State

P00 governance: passed.

P01 instrumentation: passed.

- Harness:
  `docs/benchmarks/benchmark_low_rank_ledh_posterior_gradient_calibration.py`
- Tests:
  `tests/test_low_rank_ledh_posterior_gradient_calibration.py`
- Result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p01-instrumentation-result-2026-06-24.md`
- Claude review:
  `VERDICT: AGREE`

P02 reproduction: not executed successfully.

- No valid P02 GPU/XLA JSON/Markdown result exists.
- No residual/value/gradient jitter conclusion exists.
- No threshold calibration exists.
- No posterior correctness, HMC readiness, default readiness, statistical
  superiority, public API readiness, or scientific-validity claim exists.

## Owner Directive Recorded

The user clarified on 2026-06-25 that visible non-elevated GPU runs are trusted
for BayesFilter in this managed session when provenance is recorded.

Policy update made:
`AGENTS.md` now contains `Managed-Session GPU Trust`, with trust basis:
`owner_designated_managed_session_visible_gpu_trusted`.

The P02 harness was patched to record this trust basis for visible GPU artifacts.
That patch passed compile and focused tests.  This resolved the evidence-label
question but did not make CUDA devices visible to TensorFlow in the current
sandbox.

## Reset Recommendation

Start a fresh Codex/VS Code execution context and run these checks before
resuming P02:

```bash
ls -l /dev/nvidiactl /dev/nvidia0 /dev/nvidia1 /dev/nvidia-uvm
CUDA_VISIBLE_DEVICES=1 python -c "import tensorflow as tf; print(tf.test.is_built_with_cuda()); print(tf.config.list_physical_devices('GPU'))"
```

Resume P02 only if TensorFlow reports at least one GPU.  Prefer GPU1, matching
successful recent BayesFilter GPU runs.

If TensorFlow still reports no GPUs, do not treat CPU/non-GPU XLA output as P02
evidence.  The environment needs either:

- a command context where `/dev/nvidia*` is mounted for Python/TensorFlow; or
- approval-policy support for the exact elevated local TensorFlow/CUDA
  benchmark command.

## Exact P02 Resume Command

Once TensorFlow sees a GPU, use GPU1 as visible `/GPU:0`:

```bash
python docs/benchmarks/benchmark_low_rank_ledh_posterior_gradient_calibration.py \
  --case-ids lgssm_small_exact_ref \
  --seeds 91001,91002,91003 \
  --route both \
  --num-particles 1024 \
  --time-steps 12 \
  --low-rank-rank 16 \
  --low-rank-assignment-epsilon 0.25 \
  --low-rank-alpha 1.0e-8 \
  --low-rank-max-projection-iterations 120 \
  --particle-chunk-size 64 \
  --warmups 0 \
  --repeats 3 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.md \
  --quiet
```

Capture stdout/stderr to:
`docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/p02-reproduction-gpu.log`

## Non-Claims

- This memo does not change the algorithm verdict.
- This memo does not certify a threshold.
- This memo does not claim posterior correctness, HMC readiness, statistical
  superiority, default readiness, package readiness, public API readiness, or
  scientific validity.
- This memo does not invalidate prior GPU artifacts that recorded TensorFlow
  GPU provenance.
