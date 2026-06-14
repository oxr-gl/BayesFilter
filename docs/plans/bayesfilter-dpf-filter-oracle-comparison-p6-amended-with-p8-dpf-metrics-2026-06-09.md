# P6 Amended Display With P8 DPF Metrics

metadata_date: 2026-06-09
status: PASS_P8_P44_DPF_BLOCKER_CLOSURE_READY_FOR_REVIEW

This file amends the historical P6 display only; it does not overwrite the original P6 result artifact.

- P8 JSON: `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p8_p44_dpf_blocker_closure_2026-06-09.json`
- P8 result: `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p8-p44-dpf-blocker-closure-result-2026-06-09.md`
- P8 M2 dim-1 gate: `PASS_P8_M2_DIM1_ADAPTER_GATE`

## Filled P44 DPF Cells

| Historical P6 target | DPF method | Dim | Final particles | Filled value cell | Filled gradient cell | P8 row decision |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `p44_m2_cubic_additive_gaussian_panel` | `dpf_bootstrap_ot` | 1 | 256 | value RMSE/obs `0.0198161` | mean relative score `0.0463665` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m2_cubic_additive_gaussian_panel` | `dpf_ledh_pfpf_ot` | 1 | 512 | value RMSE/obs `0.0031074` | mean relative score `0.0227353` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m2_cubic_additive_gaussian_panel` | `dpf_bootstrap_ot` | 2 | 512 | value RMSE/obs `0.00895122` | mean relative score `0.027133` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m2_cubic_additive_gaussian_panel` | `dpf_ledh_pfpf_ot` | 2 | 512 | value RMSE/obs `0.00319505` | mean relative score `0.0329506` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m2_cubic_additive_gaussian_panel` | `dpf_bootstrap_ot` | 3 | 512 | value RMSE/obs `0.00892343` | mean relative score `0.0308123` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m2_cubic_additive_gaussian_panel` | `dpf_ledh_pfpf_ot` | 3 | 512 | value RMSE/obs `0.00558933` | mean relative score `0.0544305` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m3_quadratic_observation_panel` | `dpf_bootstrap_ot` | 1 | 256 | value RMSE/obs `0.00826516` | mean relative score `0.0353553` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m3_quadratic_observation_panel` | `dpf_ledh_pfpf_ot` | 1 | 512 | value RMSE/obs `0.248276` | mean relative score `0.371019` | `DIAGNOSTIC_ONLY_MEASURED` |
| `p44_m3_quadratic_observation_panel` | `dpf_bootstrap_ot` | 2 | 512 | value RMSE/obs `0.00596884` | mean relative score `0.0192512` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m3_quadratic_observation_panel` | `dpf_ledh_pfpf_ot` | 2 | 512 | value RMSE/obs `0.25736` | mean relative score `0.430345` | `DIAGNOSTIC_ONLY_MEASURED` |
| `p44_m3_quadratic_observation_panel` | `dpf_bootstrap_ot` | 3 | 512 | value RMSE/obs `0.00601149` | mean relative score `0.0129603` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m3_quadratic_observation_panel` | `dpf_ledh_pfpf_ot` | 3 | 512 | value RMSE/obs `0.286888` | mean relative score `0.450967` | `DIAGNOSTIC_ONLY_MEASURED` |
| `p44_m4_nonlinear_transition_h2_panel` | `dpf_bootstrap_ot` | 1 | 512 | value RMSE/obs `0.01921` | mean relative score `0.0391226` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m4_nonlinear_transition_h2_panel` | `dpf_ledh_pfpf_ot` | 1 | 512 | value RMSE/obs `4.75274e-05` | mean relative score `0.000408852` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m4_nonlinear_transition_h2_panel` | `dpf_bootstrap_ot` | 2 | 512 | value RMSE/obs `0.0150133` | mean relative score `0.0402967` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m4_nonlinear_transition_h2_panel` | `dpf_ledh_pfpf_ot` | 2 | 256 | value RMSE/obs `0.000105854` | mean relative score `0.00113916` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m4_nonlinear_transition_h2_panel` | `dpf_bootstrap_ot` | 3 | 512 | value RMSE/obs `0.0134747` | mean relative score `0.0426034` | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| `p44_m4_nonlinear_transition_h2_panel` | `dpf_ledh_pfpf_ot` | 3 | 512 | value RMSE/obs `2.65008e-05` | mean relative score `0.000387676` | `PROMOTED_EXACT_TARGET_CLOSENESS` |

## Interpretation

Rows marked `PROMOTED_EXACT_TARGET_CLOSENESS` satisfy the reviewed P8 promotion bands at the final reported particle count. Rows marked `DIAGNOSTIC_ONLY_MEASURED` fill the historical `N/A` cells with finite measured value and fixed-branch gradient metrics, but they do not satisfy all promotion bands.

The amended cells use fixed-branch AD score metrics only. They do not claim full stochastic-resampling score correctness, HMC readiness, production readiness, GPU readiness, or universal DPF superiority.
