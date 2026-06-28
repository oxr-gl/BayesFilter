# P03 Large-N Low-Rank Executable-Envelope Ladder Result

Timestamp: 2026-06-21T05:38:52+08:00

Status: `P03_PASSED_LOW_RANK_LARGE_N_ENVELOPE_ONLY`

## Objective

Run low-rank-only trusted GPU1 rows at large particle counts to test whether
the candidate extends the executable LEDH/PFPF-OT envelope beyond the last
completed paired streaming comparison, without making unpaired speed or
superiority claims.

## Entry Conditions

P02 produced a reviewed paired result:

- bounded speed-screen support on feasible paired rows through `N=16384`;
- direct route-fired streaming timeout sidecar at `N=32768`;
- low-rank `PASS` at `N=32768`;
- no memory-improvement claim;
- no streaming superiority claim at unpaired `N=50000/100000`.

P03 inherited GPU1 selection via `CUDA_VISIBLE_DEVICES=1` and TF32 enabled
state.

## Artifacts

- Large-N JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.json`
- Large-N Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.md`
- Row artifacts:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21-row-low_rank-n50000.json`
  and matching Markdown;
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21-row-low_rank-n100000.json`
  and matching Markdown.

## Command And Environment

GPU preflight:

- GPU0: NVIDIA GeForce RTX 4080 SUPER, 1188 MiB used, 32760 MiB total, 36% utilization.
- GPU1: NVIDIA GeForce RTX 4080 SUPER, 18 MiB used, 32760 MiB total, 0% utilization.
- Selected GPU: GPU1.

Official command:

`timeout 3000 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode large-n --cuda-visible-devices 1 --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.md --quiet`

Environment:

- `CUDA_VISIBLE_DEVICES=1`
- TF32 recorded: `True`
- Device scope: `visible`
- Row subprocess timeouts: `True`
- P03 row timeout: `1200s`
- Routes: low-rank only

## Local Checks

Passed:

- `python -m json.tool docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.json`
- JSON inspection confirmed aggregate `status: PASS`, `phase:
  LOW_RANK_LEDH_EFFICIENCY_P03`, `mode: large-n`, `routes: low-rank`,
  `CUDA_VISIBLE_DEVICES: 1`, `tf32_execution_recorded: true`, one physical GPU,
  and no aggregate hard vetoes.
- Row inspection confirmed both rows were route-fired subprocess completions,
  completed within `1200s`, had finite outputs, no materialized transport
  matrix, matching active transport invocation count, and factor residuals
  below `5.0e-3`.

## Evidence Summary

| N | Status | Warm median seconds | Peak memory delta bytes | ESS fraction min | Max factor residual | Transport materialized |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 50000 | `PASS` | 8.957678684964776 | 81125888 | 0.9999864101409912 | 1.4901161193847656e-08 | false |
| 100000 | `PASS` | 19.56813136092387 | 86015744 | 0.9999861717224121 | 1.4901161193847656e-08 | false |

## Decision

P03 supports low-rank executable-envelope evidence at `N=50000` and
`N=100000` under the P03 large-N contract.

This evidence is low-rank-only.  It does not establish speedup or superiority
over streaming at `N=50000` or `N=100000`, because streaming was not paired at
those sizes after the predeclared `N=32768` streaming timeout boundary.

## Non-Claims

This does not establish posterior correctness, HMC readiness, public API
readiness, production/default readiness, dense Sinkhorn equivalence, broad
scalable-OT selection, statistical ranking, memory improvement, or streaming
superiority at unpaired `N=50000/100000` rows.

## Next Subplan Review

P04 may start.  P04 must combine:

- P02 reviewed bounded speed-screen support through feasible paired rows;
- P02 direct executable-envelope support at `N=32768`;
- P03 low-rank-only large-N envelope evidence at `N=50000` and `N=100000`;
- non-claims and limitations.
