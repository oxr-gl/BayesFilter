# LGSSM Paper-Table Smoke Residual Localization

## Decision

`lgssm_table_smoke_residual_shared_filterflow_state`

## First Failing State

| Field | Value |
| --- | ---: |
| time index | `1` |
| active rows | `20` |
| failing rows | `3` |
| failing global indices | `[7, 9, 11]` |
| active log-weight min | `-114.82133411103732` |
| active log-weight max | `-0.5430073149890857` |

## Residuals

| Probe | max row residual | max column residual | max residual |
| --- | ---: | ---: | ---: |
| BayesFilter | `0.00048593625368886784` | `5.329070518200751e-15` | `0.00048593625368886784` |
| FilterFlow same state | `0.00048593625368886784` | `5.329070518200751e-15` | `0.00048593625368886784` |

## Transport Delta

| Metric | Value |
| --- | ---: |
| transport matrix max abs delta | `4.440892098500626e-16` |
| transported particles max abs delta | `4.440892098500626e-16` |
| residual delta | `0.0` |

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No general nonlinear-SSM validity is concluded.
- No claim that finite relaxed OT is categorical PF is concluded.
- No claim that patched filterflow is untouched upstream code is concluded.
