# LR-TF32-3 Subplan: Trusted GPU FP32/TF32 Scale Smoke

Date: 2026-06-20
Owner: peer agent

## Status

`COMPLETED_TUNED_GPU_SCALE_DIAGNOSTIC_ONLY`

## Phase Objective

Run trusted GPU FP32/TF32 scale smokes at `N=50k` and conditionally `N=100k`
for the tuned low-rank resampling component on LEDH/PFPF-shaped particle
clouds.

The frozen GPU scale screen is `fixture_id=bounded_smooth_v1`, `B=2`, `D=8`,
`rank=64`, `assignment_epsilon=0.015625`, `dtype=float32`, `N=50000`, and
conditional `N=100000` only after the 50k row passes without hard vetoes.

## Entry Conditions Inherited From Previous Phase

- P02C tuned medium CPU no-dense validation passed with `rank=64` and
  `assignment_epsilon=0.015625`.
- Trusted GPU/TF32 execution is approved by the user/tool approval flow.
- The diagnostic command records device, TF32, memory, and manifest metadata.
- 100k is attempted only if 50k passes without hard vetoes.

## Required Artifacts

- Tuned GPU scale JSON/Markdown:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.json`
  and `.md`
  The JSON must include the top-level `run_manifest` object defined by the
  master program.
- Logs:
  `docs/benchmarks/logs/low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.log`
  A separate GPU-probe log is optional when the trusted GPU diagnostic command
  itself records the device/TF32 manifest fields required by the evidence
  contract.
- P03 result/close record.

## Required Checks, Tests, And Reviews

- Trusted GPU availability evidence through `nvidia-smi`, TensorFlow device
  metadata, or the diagnostic run manifest.
- Trusted GPU diagnostic with `--mode gpu-scale --particle-counts 50000 100000
  --conditional-100k --batch-size 2 --state-dim 8 --rank 64
  --assignment-epsilon 0.015625 --dtype float32 --fixture-id
  bounded_smooth_v1`.
- JSON parse and summary check.
- Verify 50k row status; verify 100k attempted only if 50k passed.
- Local forbidden-claim/action scan.
- Claude read-only review may be used for the P03 result if a material
  interpretation or blocker appears.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the low-rank resampling component run at 50k, and conditionally 100k, particles on trusted GPU FP32/TF32 without OOM, dense materialization, or invalid numerical artifacts? |
| Baseline/comparator | Exact weighted input moments are the downstream reference. Naive uniform no-transport is explanatory only. No dense OT baseline and no positive-feature comparator. |
| Primary pass criterion | 50k GPU row exits with empty hard vetoes, JSON includes the embedded run manifest and the fixed fixture/run fields, finite valid factors/particles, normalized uniform output weights, residual/moment thresholds pass, no dense matrix materialization, and the manifest records visible trusted GPU plus TF32 metadata. 100k pass is additional evidence only if attempted after 50k pass. |
| Veto diagnostics | GPU probe failure, untrusted/sandbox GPU evidence, diagnostic failure, OOM, invalid JSON, fixture/run mismatch, nonfinite/invalid factors or particles, residual/moment threshold failure, dense matrix materialization, missing embedded run manifest, threshold change, unsupported claim. |
| Explanatory diagnostics | Wall time, memory info, rank, projection iterations, factor minima, device metadata, TF32 enabled flag, 100k row if attempted. |
| Not concluded | No speedup, ranking, TF32-help claim, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or full solver fidelity. |

## Forbidden Claims And Actions

- Do not run GPU scale without trusted approval.
- Do not treat GPU runtime or memory as speedup evidence.
- Do not claim TF32 helps; only record the TF32 execution flag.
- Do not continue to 100k if 50k hard vetoes fire.
- Do not use dense `[B,N,N]` materialization in scale rows.
- Do not change fixture scale, dimensions, tuned setting, dtype, particle
  counts, or thresholds after seeing results.

## Exact Next-Phase Handoff Conditions

Advance to LR-TF32-4 if P03 writes a pass, fail, or blocker result with the
scale evidence preserved and no unresolved interpretation ambiguity remains.

## Stop Conditions

Stop with `LOW_RANK_TF32_GPU_SCALE_BLOCKED` if trusted GPU approval is missing,
GPU is unavailable in trusted context, 50k OOMs/fails with no lane-local repair,
or completing the phase requires package/network/public/default/shared edits.

Current status: `COMPLETED_TUNED_GPU_SCALE_DIAGNOSTIC_ONLY`.  P03 executed only
after the user-approved tuning amendment, P02B focused tuning, and P02C tuned
medium CPU validation.
