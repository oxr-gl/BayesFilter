# P8m Phase 3 Result: Trusted GPU Chunk Ladder

metadata_date: 2026-06-18
status: PASS_CHUNK_LADDER_1024_MEMORY_CANDIDATE
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | In the generic synthetic transport-core benchmark, chunk size 1024 is the best current candidate: it matches 2048 runtime within noise while using much less reported peak GPU memory.  Chunk size 4096 is rejected for this shape. |
| Primary criterion status | Passed.  All trusted-GPU rungs are finite, GPU-backed, metadata-complete, and use matched exact transport settings. |
| Veto diagnostic status | No CPU fallback, OOM, nonfinite output, SIR-specific route, Sinkhorn/epsilon tuning, or `N=50000` run. |
| Main uncertainty | This is a synthetic transport-core benchmark, not a full model benchmark.  It identifies a generic candidate setting and memory behavior, not a cross-model default. |
| Next justified action | Phase 4 should decide whether to treat 1024 as a configurable candidate and whether exact implementation changes are needed. |
| What is not concluded | No default change, particle adequacy, leaderboard completion, exact likelihood correctness, DPF gradient correctness, HMC/NUTS readiness, production readiness, or cross-model performance claim. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which generic chunk sizes reduce exact streaming transport runtime or memory without changing outputs? |
| Baseline/comparator | Phase 2 benchmark at current chunk size 2048/2048 and Sinkhorn 10. |
| Primary criterion | Trusted-GPU finite artifacts with matched exact settings and comparable outputs; result identifies candidate chunk settings or rejects chunk tuning. |
| Veto diagnostics | CPU fallback, OOM, nonfinite output, changed outputs under exact settings, missing metadata, or treating runtime as statistical adequacy. |
| Explanatory diagnostics | Runtime, memory counters, compile time, chunk sizes, residuals. |
| Not concluded | No default change, no particle adequacy, no HMC readiness. |

## Trusted GPU Preflight

Command:

```bash
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
```

Observed:

- NVIDIA GeForce RTX 4080 SUPER, 16376 MiB, driver 591.86.

## Commands Run

All benchmark rungs were run in trusted/escalated context.

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8m_transport_core_tf.py --batch-size 5 --num-particles 10000 --state-dim 18 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 1024 --col-chunk-size 1024 --warmups 1 --repeats 2 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk1024-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk1024-2026-06-18.md
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8m_transport_core_tf.py --batch-size 5 --num-particles 10000 --state-dim 18 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --warmups 1 --repeats 2 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk2048-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk2048-2026-06-18.md
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8m_transport_core_tf.py --batch-size 5 --num-particles 10000 --state-dim 18 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 4096 --col-chunk-size 4096 --warmups 1 --repeats 2 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk4096-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk4096-2026-06-18.md
```

Artifact assertions:

```bash
python - <<'PY'
import json
from pathlib import Path
for path in sorted(Path('docs/plans').glob('bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk*.json')):
    data = json.loads(path.read_text())
    assert data['finite_output'], path
    assert data['expect_device_kind'] == 'gpu', path
    assert any('GPU' in device.upper() for device in data['output_devices']), path
    assert data['shape']['model_family'] == 'synthetic_transport_core', path
    assert data['transport']['plan_mode'] == 'streaming', path
    assert data['transport']['gradient_mode'] == 'raw', path
print('P8M_PHASE3_GPU_CHUNK_ASSERTIONS_PASS')
PY
```

Result:

- `P8M_PHASE3_GPU_CHUNK_ASSERTIONS_PASS`

## Artifacts

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk1024-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk1024-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk2048-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk2048-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk4096-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk4096-2026-06-18.md`

## Result Table

| Chunk | Warm timings seconds | Warm mean seconds | Compile + first seconds | Peak GPU memory counter bytes | Max row residual |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1024 | `[0.289488, 0.296639]` | 0.293063 | 5.137230 | 84433920 | 0.0000411868 |
| 2048 | `[0.288934, 0.302516]` | 0.295725 | 5.234393 | 211000320 | 0.0000411272 |
| 4096 | `[0.811105, 0.807255]` | 0.809180 | 5.885975 | 715791360 | 0.0000411272 |

Interpretation:

- 1024 and 2048 have effectively tied warm runtime for this synthetic shape.
- 1024 uses about 40 percent of the 2048 reported peak memory counter.
- 4096 is slower and uses much more reported peak memory.
- Row residuals are comparable across rungs.

## Boundary

This is a generic synthetic transport-core benchmark.  It is not SIR d18
evidence, not a full-filter benchmark, and not a cross-model default claim.

Sinkhorn iterations and epsilon were held fixed.  This phase does not evaluate
tuning.

No `N=50000` run was launched.

## Handoff

Phase 4 should decide:

- whether 1024 should become the preferred benchmark candidate for future
  generic transport-core profiling;
- whether any exact implementation repair is justified now;
- whether additional internal instrumentation is needed before implementation
  repair.

Do not change defaults from this result alone.
