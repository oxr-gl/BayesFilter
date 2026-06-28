# P03 Medium CPU Filter-Scale Validation Result

Timestamp: 2026-06-20T16:51:14+08:00

Status: `P03_PASSED`

## Objective

Run the selected P02 low-rank setting through larger CPU-hidden filter-loop rows
before trusted GPU scale, verifying that the actual integration path still
passes hard diagnostics without dense transport materialization and with
low-rank route-execution evidence.

## Artifacts

- JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-medium-cpu-2026-06-20.json`
- Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-medium-cpu-2026-06-20.md`
- Log:
  `docs/benchmarks/logs/low-rank-ledh-pfpf-integration-p03-medium-cpu.log`

## Command

```bash
timeout 1200 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py --mode medium-cpu --rank 16 --assignment-epsilon 0.015625 --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-medium-cpu-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-medium-cpu-2026-06-20.md
```

## Evidence

| N | Status | Invocations | Active count | Transport shapes | Factor residual | Row residual | Column residual |
| ---: | --- | ---: | ---: | --- | ---: | ---: | ---: |
| 4096 | `PASS` | `2` | `2` | `[[1, 0, 0], [1, 0, 0]]` | `1.341104507446289e-07` | `1.4901161193847656e-06` | `1.7881393432617188e-06` |
| 8192 | `PASS` | `2` | `2` | `[[1, 0, 0], [1, 0, 0]]` | `1.6391277313232422e-07` | `1.2516975402832031e-06` | `1.6689300537109375e-06` |

Hard vetoes: `[]`

Runtime and memory were recorded only as explanatory diagnostics.

## Decision

P03 passed.  The selected setting remained viable in the actual filter-shaped
loop at medium CPU scale with route-execution evidence and nonmaterialized
transport sentinel shapes.

## Next Handoff

Proceed to P04 trusted GPU scale with:

- `rank=16`
- `assignment_epsilon=0.015625`
- `particle_counts=[50000, 100000]`
- `--conditional-100k`
- trusted/elevated GPU context.

No speedup, ranking, posterior correctness, HMC readiness, public API
readiness, production/default readiness, dense Sinkhorn equivalence, broad
scalable-OT selection, or TF32-help is concluded.

