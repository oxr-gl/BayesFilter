# P02 Feasible-N Paired GPU Efficiency Screen Subplan

Status: `DRAFT_AFTER_P01_ROUND_2`

## Phase Objective

Run paired trusted GPU measurements for streaming and low-rank routes over an
upward particle-count ladder to decide whether bounded resource-proxy
efficiency support exists, and to identify the first predeclared streaming
timeout/OOM/failure boundary if one appears.

## Entry Conditions Inherited From Previous Phase

P01 must pass.  GPU1 is preferred unless busy/unavailable.  The selected
physical GPU, `CUDA_VISIBLE_DEVICES`, and TF32 state must remain unchanged for
all rows used in one paired claim.  Validity and bounded output-comparability
vetoes must be evaluated before interpreting runtime or memory.

## Required Artifacts

- Paired GPU JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.json`
- Paired GPU Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p02-paired-gpu-result-2026-06-21.md`
- Log:
  `docs/benchmarks/logs/low-rank-ledh-pfpf-efficiency-p02-paired-gpu.log`

## Required Checks, Tests, And Reviews

- Trusted/elevated GPU command with `CUDA_VISIBLE_DEVICES=1` unless preflight
  records fallback to GPU0 before phase start.
- Paired ladder `[1024, 2048, 4096, 8192, 16384, 32768, 50000, 100000]`.
- Fixed per-route row timeout: `900s` wall time for every P02 row.
- Streaming attempts continue upward until the first predeclared
  timeout/OOM/failure; rows beyond that boundary are unpaired unless streaming
  is explicitly completed for that row under the same timeout.
- JSON inspection for validity, TF32 parity, same-GPU parity, timeout status,
  and bounded output-comparability vetoes before efficiency interpretation.
- Claude review if the result supports an efficiency claim or has material
  comparator failure.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does low-rank show bounded resource-proxy efficiency support against streaming as particle count increases, and where does streaming stop under fixed timeout/resource rules? |
| Baseline/comparator | Existing streaming LEDH/PFPF-OT TF32 route on the same harness shapes, same physical GPU, same `CUDA_VISIBLE_DEVICES`, same TF32 state, same seeds/fixture, and same `900s` per-route row timeout. |
| Primary pass criterion | At least two adjacent paired sizes pass validity, TF32 parity, same-GPU parity, and bounded output-comparability for both routes and meet either `>=2x` lower low-rank peak allocator delta or `>=1.25x` lower low-rank warm-call median; or streaming fails/OOM/times out at a predeclared size where low-rank passes, supporting executable-envelope improvement for that row only. |
| Veto diagnostics | Low-rank validity failure, output-comparability failure for a row used in an efficiency claim, comparator artifact invalid, missing TF32/GPU/timeout/timing/memory fields, GPU not trusted, TF32 mismatch, mixed physical GPU in one claim, no paired feasible sizes, or post-hoc threshold/timeout changes. |
| Explanatory diagnostics | Compile time, full timings, memory before/after, ESS/output previews after comparability gate, and rows beyond the first streaming failure boundary. |
| Not concluded | No posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, statistical ranking beyond the paired screen, or streaming superiority at unpaired large-N rows. |
| Artifact | P02 JSON/Markdown/result/log. |

## Forbidden Claims And Actions

- Do not claim speedup from one size or from compile time.
- Do not rank methods beyond the predeclared paired efficiency screen.
- Do not treat failed validity rows as efficiency evidence.
- Do not treat output-incomparable rows as efficiency evidence.
- Do not switch GPUs mid-phase for rows used in a paired claim; if fallback is
  needed mid-phase, invalidate/restart P02 or write a blocker.
- Do not treat low-rank-only 50k/100k completion as streaming superiority.

## Exact Next-Phase Handoff Conditions

P03 may start if P02 writes a valid paired result or a bounded failure result.
If P02 does not support efficiency but low-rank validity passes, P03 may still
test large-N executable envelope, with final claims limited accordingly.

## Stop Conditions

- `LOW_RANK_LEDH_EFFICIENCY_BLOCKED_GPU_UNAVAILABLE`
- `LOW_RANK_LEDH_EFFICIENCY_BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`
- Invalid harness/comparator artifacts that cannot be repaired.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the P02 result/close record.
3. Draft or refresh P03 subplan.
4. Review P03 for consistency, correctness, feasibility, artifact coverage, and boundary safety.
