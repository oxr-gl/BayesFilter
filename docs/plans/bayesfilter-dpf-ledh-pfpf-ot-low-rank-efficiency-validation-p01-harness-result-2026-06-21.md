# P01 Common Efficiency Harness And Small Sanity Checks Result

Timestamp: 2026-06-21T04:19:30+08:00

Status: `P01_PASSED`

## Objective

Create the lane-owned common harness and validate small CPU route execution,
finite outputs, route-fired evidence, sentinel transport shapes, metadata
coverage, and bounded output-comparability fields.

## Artifacts

- Harness: `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
- Tests: `tests/test_low_rank_ledh_pfpf_efficiency.py`
- Small JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-small-2026-06-21.json`
- Small Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-small-2026-06-21.md`

## Local Checks

Passed:

- `python -m py_compile docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_pfpf_efficiency.py -q`
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode small --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-small-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-small-2026-06-21.md`
- JSON inspection for route status, route invocations, sentinel shapes,
  factor residuals, log-weight normalization, and comparability status.

## Evidence Summary

Small CPU artifact status: `PASS`.

Rows:

- Streaming row: `PASS`; transport invocations `2`; active mask count `2`;
  transport matrix materialized `False`; final log-weight normalization
  residual `0.0`.
- Low-rank row: `PASS`; low-rank invocations `2`; active mask count `2`;
  transport matrix materialized `False`; max factor residual
  `2.8604135608734094e-08`; final log-weight normalization residual `0.0`.
- Bounded output comparability: `PASS`.

## Decision

P01 passes.  The harness can emit the fields needed by P02: route, particle
count, physical/logical device metadata, `CUDA_VISIBLE_DEVICES`, TF32 state,
timeout status, finite output, output-comparability summaries, warm-call
timings, GPU memory before/after/reset status, and low-rank route-fired
evidence.

## Non-Claims

The small CPU run does not establish efficiency, speedup, posterior
correctness, HMC readiness, public API readiness, production/default readiness,
dense Sinkhorn equivalence, or broad scalable-OT selection.

## Next Subplan Review

P02 remains the next phase.  Before executing P02, run a trusted GPU preflight
and skeptical plan audit.  P02 must use one physical GPU for all paired claim
rows, prefer GPU1 via `CUDA_VISIBLE_DEVICES=1`, preserve TF32 enabled parity,
and stop streaming upward only at the first fixed timeout/OOM/failure.
