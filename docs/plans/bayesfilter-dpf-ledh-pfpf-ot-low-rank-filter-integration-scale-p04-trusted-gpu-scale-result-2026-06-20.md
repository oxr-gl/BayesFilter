# P04 Trusted GPU 50k/100k Scale Ladder Result

Timestamp: 2026-06-20T16:53:47+08:00

Status: `P04_PASSED_DIAGNOSTIC_ONLY`

## Objective

Run the selected low-rank filter-integration route in trusted GPU context at
50k particles and conditionally 100k particles, preserving diagnostic-only
interpretation, nonmaterialized transport, and explicit route-execution
evidence.

## Artifacts

- JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-gpu-scale-2026-06-20.json`
- Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-gpu-scale-2026-06-20.md`
- Log:
  `docs/benchmarks/logs/low-rank-ledh-pfpf-integration-p04-gpu-scale.log`

## Command

```bash
timeout 1800 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py --mode gpu-scale --rank 16 --assignment-epsilon 0.015625 --conditional-100k --tf32-mode enabled --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-gpu-scale-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-gpu-scale-2026-06-20.md
```

The command was run in trusted/elevated context.

## Evidence

| N | Status | Invocations | Active count | Transport shapes | Factor residual | Row residual | Column residual | Wall time role |
| ---: | --- | ---: | ---: | --- | ---: | ---: | ---: | --- |
| 50000 | `PASS` | `1` | `1` | `[[1, 0, 0]]` | `1.4901161193847656e-08` | `1.1920928955078125e-06` | `1.5497207641601562e-06` | explanatory |
| 100000 | `PASS` | `1` | `1` | `[[1, 0, 0]]` | `2.9802322387695312e-08` | `1.1920928955078125e-06` | `1.3709068298339844e-06` | explanatory |

Hard vetoes: `[]`

Device evidence:

- Device scope: `visible`
- Device request: `/GPU:0`
- Physical GPUs recorded:
  `['/physical_device:GPU:0', '/physical_device:GPU:1']`
- TF32 execution recorded: `True`

Runtime, memory, and TF32 status are explanatory only.

## Decision

P04 passed as a diagnostic scale screen.  The selected low-rank route fired
inside the filter-shaped loop at both 50k and 100k particles and preserved
nonmaterialized sentinel transport shapes.

No speedup, ranking, posterior correctness, HMC readiness, public API
readiness, production/default readiness, dense Sinkhorn equivalence, broad
scalable-OT selection, or TF32-help is concluded.

## Next Handoff

Proceed to P05 final closeout and non-claim audit.

