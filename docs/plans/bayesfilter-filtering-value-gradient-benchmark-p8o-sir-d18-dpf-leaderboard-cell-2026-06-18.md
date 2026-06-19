# P8o SIR d18 DPF Leaderboard Cell Note

metadata_date: 2026-06-18
status: SELECT_N10000_VALUE_CELL_READY

## Cell

- Row: `zhao_cui_spatial_sir_austria_j9_T20`
- Algorithm cell: `ledh_pfpf_alg1_ukf_current` value evidence, implemented through the current experimental batched TF32/GPU LEDH-PFPF-OT streaming adapter.
- Selected particle count: `N=10000`
- Adjacent checked rung: `N=50000`
- Seeds: `81120,81121,81122,81123,81124`
- Transport: `active-all`, Sinkhorn 10, epsilon 1.0, chunks `1024/1024/1024`

## Evidence

| N | Mean log likelihood | MC SE | MC SE threshold | Warm seconds | Min ESS | Pass |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 10000 | -902.830151 | 0.208222 | 2.257075 | 8.629159 | 6432.781738 | True |
| 50000 | -902.837939 | 0.101975 | 2.257095 | 140.195284 | 31872.621094 | True |

Adjacent stability:

- absolute mean delta: `0.0077880859375909495`
- combined MC SE: `0.2318521150120367`
- threshold: `1.4637042300240735`
- adjacent pass: `True`

## Decision

Select `N=10000` for the SIR d18 value-only DPF leaderboard cell under the current batched TF32/GPU route.

## Nonclaims

- No exact nonlinear likelihood correctness claim.
- No DPF gradient, HMC, NUTS, posterior convergence, or production/default readiness claim.
- No Zhao-Cui TT/SIRT source-faithfulness or MATLAB parity claim.
