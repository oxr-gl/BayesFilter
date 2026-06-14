# LEDH-PFPF Source-Faithful Repair Result

metadata_date: 2026-06-10
status: PASS_LEDH_PFPF_SOURCE_FAITHFUL_REPAIR_READY_FOR_REVIEW

## Review Gate

- plan review: `PLAN_REVIEW_CONVERGED_VERDICT_AGREE_ITERATION_2`
- plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-plan-2026-06-10.md`
- ledger: `docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-claude-review-ledger-2026-06-10.md`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PASS_LEDH_PFPF_SOURCE_FAITHFUL_REPAIR_READY_FOR_REVIEW` | 9 repaired M3 rows; 3 promoted, 6 diagnostic, 0 failed numeric bands | no structural vetoes | Auxiliary-flow LEDH/PF-PF is source-faithful to Li-Coates but still a finite-particle nonlinear approximation. | run Claude read-only result review and then decide whether to amend P8/P6 tables | no production, HMC, universal superiority, or exact nonlinear filtering claim |

## Source Route

- source route: `li_coates_2017_algorithm_pf_pf_ledh_auxiliary_flow`
- determinant route: `sum_log_abs_det_one_plus_epsilon_a_i_j`
- collapsed shortcut used: `False`
- exact Jacobian of collapsed shortcut used: `False`

## P44 M3 Repaired Rows

| Dim | Particles | Seeds | Value RMSE/obs | Mean relative score error | Row decision |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 128 | 5 | 0.0203213 | 0.0711824 | `DIAGNOSTIC_ONLY_MEASURED` |
| 1 | 256 | 5 | 0.00864287 | 0.0362252 | `DIAGNOSTIC_ONLY_MEASURED` |
| 1 | 512 | 5 | 0.00452798 | 0.0202737 | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| 2 | 128 | 5 | 0.00784323 | 0.0423792 | `DIAGNOSTIC_ONLY_MEASURED` |
| 2 | 256 | 5 | 0.00830028 | 0.0249235 | `DIAGNOSTIC_ONLY_MEASURED` |
| 2 | 512 | 5 | 0.0056339 | 0.0163674 | `PROMOTED_EXACT_TARGET_CLOSENESS` |
| 3 | 128 | 5 | 0.00716804 | 0.039708 | `DIAGNOSTIC_ONLY_MEASURED` |
| 3 | 256 | 5 | 0.00898721 | 0.0307261 | `DIAGNOSTIC_ONLY_MEASURED` |
| 3 | 512 | 5 | 0.00629505 | 0.0204727 | `PROMOTED_EXACT_TARGET_CLOSENESS` |

## Extra Dim-1 Ladder

| Particles | Seeds | Value RMSE/obs | Mean relative score error | Row decision |
| ---: | ---: | ---: | ---: | --- |
| 1024 | 5 | 0.00364298 | 0.0174921 | `DIAGNOSTIC_ONLY_MEASURED` |
| 2048 | 5 | 0.00217098 | 0.00990912 | `DIAGNOSTIC_ONLY_MEASURED` |

## Determinant Diagnostics

- max old collapsed-shortcut frozen-vs-true logdet discrepancy: `0.540237`
- max source-faithful accumulated-vs-finite-difference logdet discrepancy: `1.10888e-11`

## Run Manifest

- command: `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-ledh-repair-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_source_faithful_repair_tf`
- git branch: `main`
- git commit: `26485010c28e11b3591da59b7ca375d4764c3d8d`
- CPU/GPU status: CPU-only, `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import
- visible GPU devices: `[]`
- seeds: `[101, 202, 303, 404, 505]`
- particle counts: `[128, 256, 512]`
- extra particle counts: `[1024, 2048]`
- pseudo-time step count: `29`
- pseudo-time ratio: `1.2`
- JSON: `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_source_faithful_repair_2026-06-10.json`
- report: `experiments/dpf_implementation/reports/dpf-ledh-pfpf-source-faithful-repair-2026-06-10.md`
- result: `docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-result-2026-06-10.md`
- wall time seconds: `24.134698729030788`

## Nonclaims

- Historical P8 artifacts are not overwritten.
- This repair invalidates the old collapsed-shortcut M3 LEDH-PFPF interpretation but does not prove universal LEDH-PFPF superiority.
- Rows use fixed-branch AD gradients, not full stochastic-resampling scores.
- No HMC, production, public API, GPU, or default-policy readiness is concluded.
- Li-Coates auxiliary-flow LEDH/PF-PF remains an approximation for nonlinear observations.
