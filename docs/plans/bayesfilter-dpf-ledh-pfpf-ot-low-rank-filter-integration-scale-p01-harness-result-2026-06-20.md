# P01 Harness Implementation And Small CPU Invariants Result

Timestamp: 2026-06-20T16:47:36+08:00

Status: `P01_PASSED`

## Objective

Create a lane-owned TensorFlow benchmark harness that embeds the low-rank
solver route inside an LEDH/PFPF-OT filter-shaped loop and validate small CPU
invariants with route-execution evidence.

## Artifacts

- Harness:
  `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py`
- Tests:
  `tests/test_low_rank_ledh_pfpf_integration_smoke.py`
- JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-small-2026-06-20.json`
- Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-small-2026-06-20.md`
- Log:
  `docs/benchmarks/logs/low-rank-ledh-pfpf-integration-p01-small.log`

## Checks Run

| Check | Status |
| --- | --- |
| `python -m py_compile docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py` | PASS |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_pfpf_integration_smoke.py -q` | PASS, 3 tests |
| `timeout 300 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py --mode small ...` | PASS |

## Evidence

| Diagnostic | Value | Role |
| --- | ---: | --- |
| Status | `PASS` | hard gate |
| Hard vetoes | `[]` | hard gate |
| Low-rank resampling invocations | `2` | hard route-execution evidence |
| Active resampling mask count | `2` | hard route-execution comparator |
| Transport matrix shapes | `[[2, 0, 0], [2, 0, 0]]` | hard no-dense sentinel |
| Tiny materialized apply parity | `2.7755575615628914e-17` | P01 tiny invariant |
| Max factor marginal residual | `7.251428655458136e-08` | hard threshold |
| Max induced row residual | `2.3204571693025144e-06` | hard threshold |
| Max induced column residual | `2.1324625882890302e-06` | hard threshold |

## Decision

P01 passed.  The harness proves that the low-rank solver route fired inside the
filter-shaped loop for the active row.  This does not establish scale viability,
speedup, ranking, posterior correctness, HMC readiness, public API readiness,
production/default readiness, dense Sinkhorn equivalence, broad scalable-OT
selection, or TF32-help.

## Next Handoff

Proceed to P02 CPU tuning grid with the predeclared grid:

- `particle_counts=[512]`
- `batch_size=1`
- `time_steps=2`
- `state_dim=6`
- `obs_dim=4`
- `tuning_ranks=[16, 32, 64, 128]`
- `tuning_assignment_epsilons=[0.0625, 0.03125, 0.015625]`
- at most two focused reruns if the initial grid has no viable row and no
  harness-validity veto fires.
