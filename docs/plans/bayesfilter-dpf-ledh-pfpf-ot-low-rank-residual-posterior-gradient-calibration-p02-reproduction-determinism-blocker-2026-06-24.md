# P02 Reproduction And Determinism Blocker

Date: 2026-06-24

Status: `BLOCKED_RUNTIME_ESCALATION_REJECTED_AGAIN`

## Phase Objective

Run trusted GPU/XLA reproduction for seeds `91001,91002,91003`, both streaming
and low-rank routes, and three repeats with the P01 value/gradient harness.

## What Passed Before The Blocker

- P01 instrumentation passed local checks and Claude read-only review.
- P02 subplan passed Claude read-only review.
- Trusted GPU precheck with `nvidia-smi` passed:
  - GPU 0 visible with 32760 MiB total memory and moderate existing load;
  - GPU 1 visible with 32760 MiB total memory and minimal existing load.

## Blocker

The P02 reproduction command was submitted exactly as planned with
`sandbox_permissions=require_escalated` because BayesFilter GPU/CUDA policy and
the P02 subplan require trusted GPU runtime for evidence. The escalation
reviewer rejected the action:

```text
This is a bounded, user-authorized local GPU benchmark, but the planned action
explicitly requests escalated execution via `sandbox_permissions":"require_escalated"`,
which is disallowed in the current environment. The agent must not attempt to
achieve the same outcome via workaround, indirect execution, or policy
circumvention. Proceed only with a materially safer alternative, or if the user
explicitly approves the action after being informed of the risk. Otherwise,
stop and request user input.
```

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Not answered; P02 runtime did not start. |
| Baseline/comparator | Exact Kalman value/gradient and streaming/low-rank routes remain planned. |
| Primary criterion | Not assessed. |
| Veto diagnostics | Runtime escalation rejection fired before benchmark execution. |
| Explanatory diagnostics | GPU precheck passed, but benchmark launch was rejected by environment approval review. |
| Not concluded | No reproduction result, no residual/value/gradient jitter finding, no threshold calibration, no holdout validation, no posterior correctness, no HMC readiness, no default readiness. |

## Stop Condition

P02 stop condition fired: trusted GPU runtime is unavailable under the current
approval state.

## Required Human Direction

To continue P02, the user must explicitly approve the exact trusted GPU/XLA
benchmark launch after being informed that it runs TensorFlow/CUDA code with
elevated permissions and writes the P02 JSON/Markdown/log artifacts under
`docs/benchmarks` and `docs/logs`.

The exact command requiring approval is:

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
  --device /GPU:0 \
  --expect-device-kind gpu \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.md \
  --quiet
```

No workaround, indirect execution, or non-trusted GPU run should be used to
replace this evidence.

## Second Attempt After User Approval

Date: 2026-06-25

After the user replied `I approve`, Codex reran the trusted GPU precheck:

- `nvidia-smi` passed.
- GPU 0 was visible with 32760 MiB total memory, about 1564 MiB in use, 89 C,
  and 85% utilization.
- GPU 1 was visible with 32760 MiB total memory, about 18 MiB in use, 36 C,
  and 0% utilization.

Codex then submitted the exact P02 command again with
`sandbox_permissions=require_escalated`, using the approved TensorFlow/CUDA
runtime and planned artifact paths. The escalation reviewer rejected it again:

```text
The benchmark is a bounded, user-approved local GPU run, but it still
explicitly requires escalated execution via `sandbox_permissions":"require_escalated"`,
which is disallowed in the current environment.
The agent must not attempt to achieve the same outcome via workaround, indirect
execution, or policy circumvention. Proceed only with a materially safer
alternative, or if the user explicitly approves the action after being informed
of the risk. Otherwise, stop and request user input.
```

P02 remains unexecuted. The blocker is now specifically that the current
environment's escalation reviewer rejected the elevated GPU benchmark even
after a user approval response.

## Owner Trust Directive Resolution

Date: 2026-06-25

The user then clarified: `non-elevated GPU runs are trusted`.

Codex interpreted this as a BayesFilter owner directive for the managed session:
visible non-elevated GPU runs are trusted BayesFilter GPU evidence when the
artifact records GPU/XLA/TF32 provenance and states the trust basis as
`owner_designated_managed_session_visible_gpu_trusted`.

This resolves the runtime escalation blocker for P02 without weakening the
scientific evidence contract.  P02 may proceed as a visible non-elevated GPU/XLA
run.  The output still may not claim threshold calibration, holdout validation,
posterior correctness, HMC readiness, default readiness, statistical
superiority, or scientific validity.

## Non-Elevated Visible GPU Runtime Failure

Date: 2026-06-25

Codex patched the P02 docs and harness to record the owner-designated managed
session GPU trust basis, reran compile/focused tests, and launched the visible
non-elevated GPU command.  The process started but exited nonzero before
writing the P02 JSON/Markdown artifacts.

Diagnostics:

- Non-elevated `nvidia-smi` passed and showed both GPUs.
- Non-elevated TensorFlow reported `built_with_cuda=True` but
  `tf.config.list_physical_devices("GPU") == []`.
- Non-elevated checks with `CUDA_VISIBLE_DEVICES=0` and
  `CUDA_VISIBLE_DEVICES=1` also returned no TensorFlow GPUs.
- `/dev/nvidiactl`, `/dev/nvidia0`, `/dev/nvidia1`, and `/dev/nvidia-uvm` are
  absent inside the non-elevated sandbox.
- The failed benchmark log is:
  `docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/p02-reproduction-gpu.log`.
- The log shows TensorFlow failed CUDA initialization with
  `CUDA_ERROR_NO_DEVICE`; the compiled route then fell back to XLA CPU JIT and
  failed on an unsupported `FakeParam` op inside a route `tf.cond`.

Updated blocker:

- The owner trust directive resolved the evidence-labeling question, but the
  non-elevated sandbox still does not expose CUDA device files to TensorFlow.
- P02 remains unexecuted as a GPU/XLA reproduction run.
- CPU or non-GPU XLA output cannot replace P02 evidence and, in this attempt,
  the CPU XLA fallback was technically invalid for the route.

Required environment-level fix:

- Run the exact P02 command in a session/process where TensorFlow can see
  `/dev/nvidia*` and `tf.config.list_physical_devices("GPU")` is nonempty; or
- update the execution harness approval policy so the exact elevated local
  TensorFlow/CUDA benchmark can run.
