# P02 CPU Tuning Grid And Focused Repair Loop Result

Timestamp: 2026-06-20T16:49:32+08:00

Status: `P02_PASSED_INITIAL_GRID`

## Objective

Run an actual filter-loop CPU tuning grid so that low-rank route parameters are
validated in the integration context before medium or GPU scale execution.

## Artifacts

- JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-tuning-cpu-2026-06-20.json`
- Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-tuning-cpu-2026-06-20.md`
- Log:
  `docs/benchmarks/logs/low-rank-ledh-pfpf-integration-p02-tuning-cpu.log`

## Command

```bash
timeout 900 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py --mode tuning-cpu --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-tuning-cpu-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-tuning-cpu-2026-06-20.md
```

## Evidence

| Diagnostic | Value | Role |
| --- | ---: | --- |
| Status | `PASS` | hard gate |
| Hard vetoes | `[]` | hard gate |
| Grid rows | `12` | bounded tuning |
| Viable rows | `12` | hard gate |
| Focused reruns used | `0` | bounded repair evidence |
| Selected rank | `16` | next-phase setting |
| Selected assignment epsilon | `0.015625` | next-phase setting |
| Selected route invocations | `2` | hard route-execution evidence |
| Selected active mask count | `2` | hard route-execution comparator |
| Selected max factor residual | `1.4901161193847656e-08` | hard threshold |
| Selected max induced row residual | `1.430511474609375e-06` | hard threshold |
| Selected max induced column residual | `1.5497207641601562e-06` | hard threshold |

## Decision

P02 passed on the initial grid.  All grid rows were viable under the hard
diagnostics, and every row recorded low-rank route invocation count equal to
active resampling mask count.  The selected P03/P04 setting is:

- `rank=16`
- `assignment_epsilon=0.015625`

The selection is a predeclared representative viable setting, not a ranking or
speed claim.

## Next Handoff

Proceed to P03 medium CPU filter-scale validation with:

- `rank=16`
- `assignment_epsilon=0.015625`
- `particle_counts=[4096, 8192]`
- CPU-hidden TensorFlow execution.

No speedup, ranking, posterior correctness, HMC readiness, public API
readiness, production/default readiness, dense Sinkhorn equivalence, broad
scalable-OT selection, or TF32-help is concluded.
