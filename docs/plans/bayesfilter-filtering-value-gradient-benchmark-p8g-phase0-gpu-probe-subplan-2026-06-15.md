# P8g-G0 Subplan: GPU Device And Backend Gate

Date: 2026-06-15

Status: `DRAFT_PENDING_REVIEW`

## Phase Objective

Establish the trusted GPU/CUDA/TensorFlow/XLA baseline required before any
serious P8g GPU implementation, tuning, or gradient claim.

## Entry Conditions

- P8g master program exists and is reviewed or under active review.
- Local GPU policy requires escalation for all GPU/CUDA/NVIDIA commands.
- No P8g serious GPU artifact exists yet; this phase creates the root GPU
  manifest that later artifacts must cite.

## Required Artifacts

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md`
- GPU probe command transcript or summarized output in the result artifact.
- G0 manifest fields: git commit, dirty summary, environment, driver, CUDA,
  TensorFlow, TFP, XLA, GPU name, GPU memory, visible devices, probe commands,
  and CPU/GPU status.

## Required Checks/Tests/Reviews

- Escalated `nvidia-smi`.
- Escalated TensorFlow GPU device probe.
- Escalated tiny TensorFlow matmul on GPU.
- Escalated tiny `tf.function(jit_compile=True)` probe on GPU.
- Local `git diff --check`.
- Claude read-only review of the G0 result before any G1 advance, because G0 is
  the root GPU trust gate for every later serious artifact.

## Planned Command And Artifact Contract

Repository root: `/home/chakwong/BayesFilter`.

Environment assumptions:

- active Python environment is the project default environment;
- all GPU/CUDA/NVIDIA commands require trusted/escalated execution;
- CPU-only checks must set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.

Exact planned commands:

- local formatting check, non-GPU:
  `git diff --check`
- trusted GPU device check:
  `nvidia-smi`
- trusted TensorFlow GPU probe:
  `python - <<'PY'` with a bounded probe that imports TensorFlow and TensorFlow
  Probability, prints versions, lists physical/logical GPU devices, runs a tiny
  GPU matmul under `tf.device('/GPU:0')`, and runs a tiny
  `tf.function(jit_compile=True)` on the same device.

Phase-local output paths:

- required phase result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md`;
- optional raw transcript if needed:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-transcript-2026-06-15.txt`.

Approval boundary:

- do not run `nvidia-smi` or the TensorFlow GPU probe until the user approves
  the exact trusted commands for G0 launch;
- no long run, tuning, implementation, or HMC command is authorized by this
  subplan.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the trusted GPU backend usable for P8g serious execution? |
| Baseline/comparator | Local CPU-only P8e diagnostics plus local GPU policy. |
| Primary criterion | Trusted GPU probe sees at least one usable GPU and TensorFlow can run a tiny GPU matmul and XLA probe. |
| Veto diagnostics | Non-escalated GPU failure used as evidence; no GPU visible in trusted context; TensorFlow GPU probe fails; XLA probe fails without reviewed exception; artifact lacks command/environment manifest. |
| Explanatory diagnostics | Driver/CUDA versions, memory, TensorFlow device placement, XLA details. |
| Not concluded | Algorithm speedup, correctness, value accuracy, gradient correctness, or HMC readiness. |

## Forbidden Claims/Actions

- Do not diagnose GPU health from non-escalated failures.
- Do not launch tuning or implementation from G0.
- Do not claim GPU speed or algorithm readiness from device probes.

## Next-Phase Handoff Conditions

Advance to G1 only if the G0 result is `PASS_P8G_G0_GPU_TRUSTED_PROBE` and the
result artifact path is recorded for downstream citation. The G0 result must
also receive read-only Claude review, with the review round recorded in the
canonical `Review Loop Ledger`, before G1 execution starts.

## Stop Conditions

- Trusted GPU probe fails.
- GPU commands require approval not granted.
- TensorFlow/XLA environment is missing or unusable.
