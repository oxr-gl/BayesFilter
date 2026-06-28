# LR-TF32-2 Subplan: Medium CPU No-Dense Smoke

Date: 2026-06-20
Owner: peer agent

## Status

`P02_AMENDED_INVALID_AS_ROUTE_REJECTION_PLANNING_USAGE_ERROR`

## Phase Objective

Run a CPU-hidden medium particle-count smoke to catch accidental dense
materialization, shape/memory mistakes, and downstream moment-screen failures
before trusted GPU 50k/100k execution.

The frozen medium screen is `fixture_id=bounded_smooth_v1`, `B=2`,
`N in {4096, 8192}`, `D=8`, `rank=64`, `assignment_epsilon=0.5`,
`dtype=float32`, CPU hidden, and `timeout=300s`.

Amendment: after this phase ran, the user identified the missing tuning phase
as a planning/usage error.  Therefore this subplan remains the record for the
initial untuned medium screen, but its failure is not a route-family rejection
or a final lane stop.

## Entry Conditions Inherited From Previous Phase

- P01 harness and small invariants passed.
- Diagnostic script and focused tests exist.
- Thresholds remain unchanged.

## Required Artifacts

- Medium CPU JSON/Markdown:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.json`
  and `.md`
  The JSON must include the top-level `run_manifest` object defined by the
  master program.
- Log:
  `docs/benchmarks/logs/low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.log`
- P02 result/close record.

## Required Checks, Tests, And Reviews

- CPU-hidden medium diagnostic command, quiet logged with the exact fixed
  command shape:
  `timeout 300 env CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py --mode medium-cpu --particle-counts 4096 8192 --batch-size 2 --state-dim 8 --rank 64 --dtype float32 --fixture-id bounded_smooth_v1`.
- JSON parse and summary check.
- Scan JSON for no dense scale matrix materialization.
- Local forbidden-claim/action scan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the low-rank resampling harness run at the fixed medium CPU screen, `N=4096` and `N=8192`, without dense transport materialization or invalid downstream moments? |
| Baseline/comparator | Exact weighted input moments are the downstream reference; naive uniform no-transport is explanatory only. |
| Primary pass criterion | Medium CPU-hidden diagnostic exits 0 within `300s`, JSON includes the embedded run manifest and the fixed fixture/run fields, hard vetoes are empty, factors/particles are finite and valid, output weights normalize, residuals and moment errors pass thresholds, and scale rows report no dense matrix materialization.  If only the untuned downstream moment screen fails while no-dense/factor validity holds, the amended interpretation is a tuning trigger rather than route rejection. |
| Veto diagnostics | Diagnostic failure, timeout, invalid JSON, fixture/run mismatch, dense scale materialization, nonfinite/invalid factors or particles, residual/moment threshold failure, missing embedded run manifest, or unsupported claim.  Under the amendment, residual/moment failure in this untuned screen is a hard veto only against the untuned setting, not against the low-rank solver-route family. |
| Explanatory diagnostics | Runtime, memory proxy, rank, projection iterations, factor minima, candidate-vs-naive deltas. |
| Not concluded | No 50k/100k feasibility, GPU feasibility, TF32 help, speedup, ranking, readiness, or dense equivalence. |

## Forbidden Claims And Actions

- Do not infer GPU or TF32 feasibility from CPU-hidden medium results.
- Do not change thresholds after seeing results.
- Do not change fixture scale, dimensions, ranks, dtype, particle counts, or
  timeout after seeing results.
- Do not compare against positive-feature.

## Exact Next-Phase Handoff Conditions

Advance directly to LR-TF32-3 only if P02 passes.  If P02 fails only as an
untuned moment-preservation screen while no-dense/factor validity holds, advance
to the user-approved tuning amendment path: LR-TF32-2A, then LR-TF32-2B,
then LR-TF32-2C before any trusted GPU scale.

## Stop Conditions

Stop with `LOW_RANK_TF32_SCALE_MEDIUM_CPU_BLOCKED` if medium no-dense smoke
fails in a way that cannot be repaired lane-locally or if GPU scale execution
would no longer answer the stated question.  Do not stop on an untuned moment
failure that the planned/user-approved tuning phases are designed to repair.
