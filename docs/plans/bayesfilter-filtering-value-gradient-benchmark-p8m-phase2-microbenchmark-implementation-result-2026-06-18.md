# P8m Phase 2 Result: Generic Microbenchmark Implementation

metadata_date: 2026-06-18
status: PASS_GENERIC_TRANSPORT_BENCHMARK_CPU_SMOKE
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Implemented a generic synthetic transport-core benchmark that calls the existing `batched_annealed_transport_core_tf` streaming route. |
| Primary criterion status | Passed.  pycompile, CPU-only smoke, JSON metadata assertions, and `git diff --check` passed. |
| Veto diagnostic status | No active veto.  The benchmark has no SIR callbacks/data paths and does not change transport algorithm semantics or defaults. |
| Main uncertainty | Phase 2 proves CPU smoke and metadata correctness only; it does not prove GPU readiness or performance. |
| Next justified action | Review the implementation diff/result with Claude, then plan Phase 3 trusted-GPU chunk ladder if review agrees. |
| What is not concluded | No GPU speedup, production readiness, scientific adequacy, particle adequacy, leaderboard completion, exact likelihood correctness, DPF gradient correctness, or HMC/NUTS readiness. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the generic microbenchmark/instrumentation run locally and preserve transport semantics under small focused checks? |
| Baseline/comparator | Existing transport functions under matched synthetic particles/log weights. |
| Primary criterion | pycompile and focused CPU checks pass; output metadata records shape, chunk sizes, iterations, dtype, and nonclaims. |
| Veto diagnostics | SIR-specific dependency, nonfinite outputs, mismatched exact output under a small reference check, GPU-only correctness path, or changed default behavior. |
| Explanatory diagnostics | CPU smoke timing, metadata fields, finite checks. |
| Not concluded | No GPU speedup, no production readiness, no scientific adequacy. |

## Implementation

Added:

- `docs/benchmarks/benchmark_p8m_transport_core_tf.py`

The benchmark:

- builds synthetic stateless particles and normalized log weights;
- calls `core_tf.batched_annealed_transport_core_tf`;
- uses `transport_plan_mode="streaming"` and `transport_gradient_mode="raw"`;
- records timing, output devices, memory counters, residuals, shape, transport
  configuration, precision metadata, and nonclaims;
- writes JSON and optional markdown artifacts;
- deliberately avoids SIR callbacks, SIR data paths, SIR state-layout
  assumptions, and side-effect timers inside differentiable transport math.

## Checks Run

```bash
python -m py_compile docs/benchmarks/benchmark_p8m_transport_core_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8m_transport_core_tf.py --device-scope cpu --expect-device-kind cpu --batch-size 2 --num-particles 64 --state-dim 3 --sinkhorn-iterations 3 --row-chunk-size 32 --col-chunk-size 32 --warmups 0 --repeats 1 --device /CPU:0 --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-transport-core-cpu-smoke-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-transport-core-cpu-smoke-2026-06-18.md
python - <<'PY'
import json
from pathlib import Path
path = Path('docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-transport-core-cpu-smoke-2026-06-18.json')
data = json.loads(path.read_text())
assert data['finite_output']
assert data['transport']['plan_mode'] == 'streaming'
assert data['transport']['gradient_mode'] == 'raw'
assert data['shape']['model_family'] == 'synthetic_transport_core'
print('P8M_PHASE2_CPU_SMOKE_ASSERTIONS_PASS')
PY
git diff --check -- docs/benchmarks/benchmark_p8m_transport_core_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-*
```

Results:

- pycompile: passed;
- CPU-only smoke: passed;
- JSON assertions: `P8M_PHASE2_CPU_SMOKE_ASSERTIONS_PASS`;
- `git diff --check`: passed.

The CPU smoke intentionally used `CUDA_VISIBLE_DEVICES=-1` and output devices
were CPU devices.  TensorFlow printed a CUDA initialization warning before
settling on host XLA, but the artifact records `physical_gpus: []`,
`logical_gpus: []`, CPU output devices, and unavailable GPU memory info.

## CPU Smoke Artifact

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-transport-core-cpu-smoke-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-transport-core-cpu-smoke-2026-06-18.md`

Key fields:

- `finite_output`: true;
- `shape.model_family`: `synthetic_transport_core`;
- `transport.plan_mode`: `streaming`;
- `transport.gradient_mode`: `raw`;
- `device_scope`: `cpu`;
- `cuda_visible_devices`: `-1`;
- `output_devices`: CPU.

## Boundary

No transport algorithm code was changed.  No defaults were changed.  No GPU
performance claim is made from Phase 2.

## Handoff

Phase 3 planning may proceed after Claude review of this result and the
implementation diff.  Phase 3 must run any GPU/CUDA/TensorFlow GPU command in
trusted/escalated context and must not treat Phase 2 as GPU-readiness or
performance evidence.
