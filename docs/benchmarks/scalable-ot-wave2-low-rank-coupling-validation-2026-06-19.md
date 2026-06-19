# Wave 2 Low-Rank Coupling Validation Diagnostics

- Status: `PASS`
- Wave 2 status: `LOW_RANK_COUPLING_VALIDATION_PASSED_DIAGNOSTIC_ONLY`
- Owner: `peer_agent`
- Algorithm family: `low_rank_coupling_solver_route_validation`
- Entry context status: `LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY`
- Semantic class: `semantic_replacement`
- Source route: `extension_or_invention`
- Validity pass: `True`
- Hard vetoes: `[]`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| max factor marginal residual | `1.144962e-07` | hard veto |
| max induced row residual | `5.267489e-07` | hard veto |
| max induced column residual | `5.724812e-07` | hard veto |
| max materialized tiny apply parity | `1.110223e-16` | hard veto |
| max projection error | `5.906869e-07` | explanatory |
| max projection floor hits | `0.000000e+00` | explanatory |
| min Q | `5.593962e-03` | explanatory |
| min R | `2.539576e-03` | explanatory |
| min g | `2.839796e-01` | explanatory |
| total wall time seconds | `1.717574e-01` | explanatory |

## Rows

| Fixture | Rank | Valid | Factor residual | Row residual | Column residual | Apply parity |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| tiny_manual | 3 | `True` | `1.144962e-07` | `5.267489e-07` | `5.724812e-07` | `2.775558e-17` |
| small_batch | 3 | `True` | `4.448633e-08` | `2.224317e-07` | `2.181370e-07` | `1.110223e-16` |
| wider_state | 3 | `True` | `3.761063e-08` | `2.039595e-07` | `2.256638e-07` | `5.551115e-17` |

## Source-Route Classification

| Component | Classification |
| --- | --- |
| `factored_coupling_parameterization` | `source_faithful` |
| `low_rank_lazy_apply` | `source_faithful` |
| `factor_marginal_diagnostics` | `source_faithful` |
| `dykstra_style_projection` | `source_faithful` |
| `deterministic_initialization` | `fixed_hmc_adaptation` |
| `fixed_iteration_schedule` | `fixed_hmc_adaptation` |
| `phase1_scaled_transport_adapter` | `fixed_hmc_adaptation` |
| `cost_nudged_assignment_kernel` | `extension_or_invention` |

## Non-Claims

- Wave 2 peer-agent low-rank coupling validation only
- semantic replacement, not dense Sinkhorn equivalence
- no full low-rank Sinkhorn solver-fidelity claim for extension components
- no speedup claim
- no ranking claim
- no production default change
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no broad scalable-OT selection claim
