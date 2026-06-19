# P12 Low-Rank Coupling Solver Route Diagnostics

- Status: `PASS`
- Phase 12 status: `LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY`
- Semantic class: `semantic_replacement`
- Implementation scope: `solver_route_dykstra_projection_diagnostic`
- Validity pass: `True`
- Hard vetoes: `[]`

## Summary

| Metric | Value |
| --- | ---: |
| max factor marginal residual | `1.144962e-07` |
| max induced row residual | `5.267489e-07` |
| max induced column residual | `5.724812e-07` |
| max materialized tiny apply parity | `1.110223e-16` |
| max dense-reference particle error, explanatory | `4.657416e-01` |
| max dense-reference RMS error, explanatory | `1.723903e-01` |

## Rows

| Fixture | Rank | Valid | Factor residual | Row residual | Column residual | Apply parity | Max dense error, explanatory |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| tiny_manual_solver | 3 | `True` | `1.144962e-07` | `5.267489e-07` | `5.724812e-07` | `2.775558e-17` | `3.783889e-01` |
| small_batch_solver | 3 | `True` | `4.448633e-08` | `2.224317e-07` | `2.181370e-07` | `1.110223e-16` | `4.657416e-01` |

## Non-Claims

- Agent C P12 low-rank coupling solver-route diagnostics only
- semantic replacement, not dense Sinkhorn equivalence
- no full low-rank Sinkhorn solver-fidelity claim for extension components
- no speedup claim
- no ranking claim
- no production default change
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
