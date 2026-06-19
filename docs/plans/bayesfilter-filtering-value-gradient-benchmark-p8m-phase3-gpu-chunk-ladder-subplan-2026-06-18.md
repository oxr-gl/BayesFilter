# P8m Phase 3 Subplan: Trusted GPU Chunk Ladder

metadata_date: 2026-06-18
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md
phase: 3

## Phase Objective

Run a trusted-GPU chunk-size ladder on generic transport instrumentation to
identify exact implementation bottlenecks and safe candidate configurations.

## Entry Conditions Inherited From Previous Phase

- Phase 2 generic benchmark/instrumentation passes focused checks.
- GPU commands are approved and must be trusted/escalated.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-gpu-chunk-ladder-result-2026-06-18.md`
- JSON/markdown benchmark artifacts for executed rungs.

## Required Checks/Tests/Reviews

Trusted GPU preflight:

```bash
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
```

Expected chunk ladder, adjusted by Phase 2 benchmark interface:

Baseline and candidate rungs, all trusted/escalated:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8m_transport_core_tf.py --batch-size 5 --num-particles 10000 --state-dim 18 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 1024 --col-chunk-size 1024 --warmups 1 --repeats 2 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk1024-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk1024-2026-06-18.md
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8m_transport_core_tf.py --batch-size 5 --num-particles 10000 --state-dim 18 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --warmups 1 --repeats 2 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk2048-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk2048-2026-06-18.md
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8m_transport_core_tf.py --batch-size 5 --num-particles 10000 --state-dim 18 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 4096 --col-chunk-size 4096 --warmups 1 --repeats 2 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk4096-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk4096-2026-06-18.md
```

Artifact assertions after any executed rungs:

```bash
python - <<'PY'
import json
from pathlib import Path
for path in sorted(Path("docs/plans").glob("bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk*.json")):
    data = json.loads(path.read_text())
    assert data["finite_output"], path
    assert data["expect_device_kind"] == "gpu", path
    assert any("GPU" in device.upper() for device in data["output_devices"]), path
    assert data["shape"]["model_family"] == "synthetic_transport_core", path
    assert data["transport"]["plan_mode"] == "streaming", path
    assert data["transport"]["gradient_mode"] == "raw", path
print("P8M_PHASE3_GPU_CHUNK_ASSERTIONS_PASS")
PY
```

Claude review is required before launching high-cost rungs.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which generic chunk sizes reduce exact streaming transport runtime or memory without changing outputs? |
| Baseline/comparator | Phase 2 benchmark at current chunk size 2048/2048 and Sinkhorn 10 unless Phase 1 defines another exact baseline. |
| Primary criterion | Trusted-GPU finite artifacts with matched exact settings and comparable outputs; result identifies candidate chunk settings or rejects chunk tuning. |
| Veto diagnostics | CPU fallback, OOM, nonfinite output, changed outputs under exact settings, missing metadata, or treating runtime as statistical adequacy. |
| Explanatory diagnostics | Runtime, memory counters, compile time, chunk sizes, residuals if available. |
| Not concluded | No default change, no particle adequacy, no HMC readiness. |

## Forbidden Claims/Actions

- Do not run `N=50000` unless separately reviewed.
- Do not change Sinkhorn iteration or epsilon in this phase.
- Do not claim cross-model speedup from a single fixture.

## Exact Next-Phase Handoff Conditions

Phase 4 may proceed if Phase 3 identifies a concrete exact implementation
optimization candidate or shows chunk tuning is enough.

## Stop Conditions

Stop on GPU unavailability, OOM, nonfinite output, mismatched outputs, or no
actionable generic bottleneck.
