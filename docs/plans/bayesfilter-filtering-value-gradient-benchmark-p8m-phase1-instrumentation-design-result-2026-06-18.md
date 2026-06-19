# P8m Phase 1 Result: Transport Instrumentation Design

metadata_date: 2026-06-18
status: PASS_GENERIC_MICROBENCHMARK_DESIGN
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Use a generic synthetic transport microbenchmark as the first instrumentation surface.  Do not add SIR callbacks or side-effect timers inside differentiable compiled math in Phase 2. |
| Primary criterion status | Passed.  The result names concrete Phase 2 artifacts, commands, metadata fields, and checks. |
| Veto diagnostic status | No SIR-specific route selected; no implementation was performed in Phase 1. |
| Main uncertainty | The microbenchmark will time exact streaming transport as a callable unit; deeper split between softmin, potential updates, column normalization, and final application may require a later optional instrumentation phase. |
| Next justified action | Implement a small generic benchmark under `docs/benchmarks` plus focused CPU tests. |
| What is not concluded | No speedup, optimization, accepted Sinkhorn iteration count, production readiness, or scientific adequacy. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the smallest generic instrumentation surface that can profile transport-core bottlenecks? |
| Baseline/comparator | Current streaming transport functions and P8l whole-call evidence. |
| Primary criterion | Design result names concrete artifacts, commands, fields, and tests for Phase 2 without requiring SIR-specific code. |
| Veto diagnostics | SIR-only data path, intrusive timing inside differentiable math, hidden semantic change, or inability to test finite/matched outputs. |
| Explanatory diagnostics | Code anchors, proposed benchmark shapes, timing fields. |
| Not concluded | No speedup, no optimization, no accepted iteration count. |

## Code Anchor Inventory

Generic streaming transport path:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  - `_filterflow_streaming_softmin`;
  - `_filterflow_streaming_sinkhorn_potentials`;
  - `_filterflow_streaming_column_log_normalizer`;
  - `_filterflow_streaming_transport_from_potentials`;
  - `_filterflow_streaming_transport`.
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  - `batched_annealed_transport_core_tf`, which calls
    `_filterflow_streaming_transport` under `transport_plan_mode="streaming"`.

The selected Phase 2 benchmark should call the generic transport core through
`batched_annealed_transport_core_tf` first.  That preserves the public
experimental transport surface and exercises the same fixed-mask behavior used
by the streaming DPF engine.

## Selected Instrumentation Route

Implement a new generic benchmark:

- `docs/benchmarks/benchmark_p8m_transport_core_tf.py`

Inputs:

- synthetic stateless particles with shape `[B, N, D]`;
- synthetic normalized log weights with shape `[B, N]`;
- fixed resampling mask policy:
  - `active-all`;
  - `no-resampling` for lower-bound smoke only;
- dtype:
  - `float32` default;
  - optional `float64` if needed for CPU reference;
- transport settings:
  - plan mode `streaming`;
  - gradient mode `raw`;
  - Sinkhorn iterations;
  - epsilon;
  - row/col chunk sizes;
  - optional seed.

Outputs:

- JSON and optional markdown artifact;
- finite output flags;
- output devices;
- compile plus first call seconds;
- warm-call timings and summary;
- memory counters when GPU is visible;
- shape/configuration metadata;
- row residual and column residual from `BatchedAnnealedTransportTensors`;
- log-weight normalization check;
- nonclaims.

Optional later instrumentation:

- if Phase 3 shows chunk tuning alone is insufficient, add a reviewed Phase 4
  or Phase 5 design for direct microbenchmarks of private helpers
  `_filterflow_streaming_sinkhorn_potentials` and
  `_filterflow_streaming_transport_from_potentials`.  Do not start there
  because private-helper timing would create more brittle test surfaces.

## Phase 2 Required Checks

Expected implementation checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8m_transport_core_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8m_transport_core_tf.py --device-scope cpu --expect-device-kind cpu --batch-size 2 --num-particles 64 --state-dim 3 --sinkhorn-iterations 3 --row-chunk-size 32 --col-chunk-size 32 --warmups 0 --repeats 1 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-transport-core-cpu-smoke-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-transport-core-cpu-smoke-2026-06-18.md
python - <<'PY'
import json
from pathlib import Path
path = Path("docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-transport-core-cpu-smoke-2026-06-18.json")
data = json.loads(path.read_text())
assert data["finite_output"]
assert data["transport"]["plan_mode"] == "streaming"
assert data["transport"]["gradient_mode"] == "raw"
assert data["shape"]["model_family"] == "synthetic_transport_core"
print("P8M_PHASE2_CPU_SMOKE_ASSERTIONS_PASS")
PY
git diff --check -- docs/benchmarks/benchmark_p8m_transport_core_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-*
```

Focused test file is optional in Phase 2 if the benchmark CPU smoke plus JSON
assertions cover the initial generic instrumentation contract.  Add a pytest
only if implementation logic grows beyond CLI/build/run/report plumbing.

## Phase 2 Evidence Boundary

Phase 2 may prove only that the generic benchmark exists, runs, and reports
metadata correctly on a small CPU smoke.  It may not claim GPU speedup,
particle adequacy, cross-model generality, or default readiness.

## Handoff

Phase 2 may proceed with implementation of
`docs/benchmarks/benchmark_p8m_transport_core_tf.py` after Claude review of
this result and the Phase 2 subplan.
