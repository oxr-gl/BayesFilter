# P8 Amendment: M3 LEDH-PFPF Source-Faithful Replacement Rows

Date: 2026-06-10

## Decision

`P8_M3_LEDH_PFPF_SOURCE_FAITHFUL_AMENDMENT_READY_FOR_REVIEW`

This note amends, without overwriting, the historical P8 interpretation of
`dpf_ledh_pfpf_ot` on `p44_m3_quadratic_observation_panel`.

## Superseded Interpretation

The historical P8 M3 LEDH-PFPF rows used a collapsed local-affine shortcut:

- coefficients were computed from the same pre-flow proposal value;
- the forward log determinant was the frozen local-affine determinant;
- the auxiliary-flow / actual-particle separation from Li-Coates PF-PF(LEDH)
  was absent.

Those rows should no longer be interpreted as evidence about LEDH-PF-PF.  They
are evidence that the collapsed shortcut was not source-faithful for nonlinear
particle-dependent LEDH.

## Replacement Artifact

Replacement result:
`docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-result-2026-06-10.md`

Replacement JSON:
`experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_source_faithful_repair_2026-06-10.json`

Source route:
`li_coates_2017_algorithm_pf_pf_ledh_auxiliary_flow`

Determinant route:
`sum_log_abs_det_one_plus_epsilon_a_i_j`

## Replacement Rows

| Target | Method | Dim | Particles | Value RMSE/obs | Mean relative score error | Replacement decision |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `p44_m3_quadratic_observation_panel` | `dpf_ledh_pfpf_ot` | 1 | 512 | 0.00452798 | 0.0202737 | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m3_quadratic_observation_panel` | `dpf_ledh_pfpf_ot` | 2 | 512 | 0.0056339 | 0.0163674 | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m3_quadratic_observation_panel` | `dpf_ledh_pfpf_ot` | 3 | 512 | 0.00629505 | 0.0204727 | `PROMOTED_EXACT_TARGET_CLOSENESS` |

## Determinant Diagnostic

- Old collapsed-shortcut frozen-vs-true logdet max discrepancy: `0.540237`.
- Source-faithful accumulated-vs-finite-difference logdet max discrepancy:
  `1.10888e-11`.

## Nonclaims

- This amendment does not overwrite historical P8 files.
- This amendment does not prove LEDH-PFPF universal superiority.
- This amendment does not claim full stochastic-resampling score correctness.
- This amendment does not establish HMC, production, public API, GPU, or default
  readiness.
