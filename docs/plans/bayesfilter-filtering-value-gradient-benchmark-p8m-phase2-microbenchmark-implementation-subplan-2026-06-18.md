# P8m Phase 2 Subplan: Generic Microbenchmark Implementation

metadata_date: 2026-06-18
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md
phase: 2

## Phase Objective

Implement the reviewed generic transport microbenchmark or instrumentation
surface from Phase 1.

## Entry Conditions Inherited From Previous Phase

- Phase 1 design passed local checks and Claude review.
- Implementation route is generic and does not depend on SIR d18.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-microbenchmark-implementation-result-2026-06-18.md`
- New or updated benchmark/test files named in the Phase 1 result.

## Required Checks/Tests/Reviews

Minimum required checks from the reviewed Phase 1 design:

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

Claude review is required for material implementation diffs.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the generic microbenchmark/instrumentation run locally and preserve transport semantics under small focused checks? |
| Baseline/comparator | Existing transport functions under matched synthetic particles/log weights. |
| Primary criterion | pycompile and focused CPU checks pass; output metadata records shape, chunk sizes, iterations, dtype, and nonclaims. |
| Veto diagnostics | SIR-specific dependency, nonfinite outputs, mismatched exact output under a small reference check, GPU-only correctness path, or changed default behavior. |
| Explanatory diagnostics | CPU smoke timing, metadata fields, finite checks. |
| Not concluded | No GPU speedup, no production readiness, no scientific adequacy. |

## Forbidden Claims/Actions

- Do not claim optimization from a smoke test.
- Do not change default transport behavior.
- Do not add broad dependency or package installation requirements.
- Do not add SIR callbacks, SIR-only data paths, SIR state-layout assumptions,
  or disease-model-specific inputs.
- Do not add side-effect timers or other instrumentation inside differentiable
  compiled transport math.
- Do not make semantic changes to the transport algorithm in Phase 2.

## Exact Next-Phase Handoff Conditions

Phase 3 planning may proceed if the generic benchmark passes the reviewed CPU
smoke and metadata assertions and the Phase 2 result records the GPU-rung
interface needed for later trusted execution.  Phase 2 does not itself prove
GPU readiness or performance.

## Stop Conditions

Stop if focused checks fail or the instrumentation cannot be kept generic.
