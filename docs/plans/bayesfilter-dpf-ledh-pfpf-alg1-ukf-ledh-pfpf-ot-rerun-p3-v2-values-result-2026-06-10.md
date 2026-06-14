# P3 Result: V2 Algorithm 1 UKF Value Replacement

metadata_date: 2026-06-10
phase: P3
status: LOCAL_PASS_P3_V2_ALG1_UKF_VALUES_DIAGNOSTIC_ONLY_PENDING_CLAUDE_REVIEW

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | For V2 rows declared runnable in P2, do Algorithm 1 UKF value runs execute finitely and preserve Monte Carlo uncertainty? |
| Baseline/comparator | P2 frozen contracts; exact Kalman on LGSSM; bootstrap no-flow PF as a baseline comparator.  Other rows have no exact oracle in P3 and remain diagnostic-only. |
| Primary criterion | Every P2 row appears with a reviewed status; every P2 runnable row is executed or explicitly downgraded; P2-blocked rows may carry forward only with adapter reasons; finite runnable rows include uncertainty, route fields, and no promotion claim. |
| Threshold policy | P2 froze diagnostic-only thresholds because Monte Carlo error depends on model noise, horizon, dimension, nonlinearity, and particle count. |
| Not concluded | P3 value rows are diagnostic-only and do not certify numerical closeness.; P3 value rows do not imply gradient correctness.; P3 does not use OT or annealed transport.; P3 does not establish stochastic-resampling correctness.; P3 blocked rows are adapter work items, not negative scientific evidence.; P3 does not establish production readiness, HMC readiness, GPU performance, or broad model superiority. |

## Cells

| Model | P2 status | P3 status | Rows | Finite rows | Comparator | Reason |
| --- | --- | --- | ---: | ---: | --- | --- |
| `lgssm_2d_h25_rich` | `RUNNABLE_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `30` | `30` | `exact_kalman_for_lgssm` | finite diagnostic value rows only; no calibrated promotion band |
| `sv_1d_h18_rich` | `BLOCKED_REQUIRES_ADAPTER` | `BLOCKED_REQUIRES_ADAPTER` | `0` | `0` | `N/A_BLOCKED_REQUIRES_ADAPTER` | The current V2 stochastic-volatility row has a non-Gaussian observation likelihood.  A log-square Gaussian surrogate may be a BayesFilter extension, but it is not frozen here as source Algorithm 1 evidence. |
| `range_bearing_4d_h20_rich` | `RUNNABLE_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `30` | `30` | `diagnostic_only_no_exact_oracle_in_P3` | finite diagnostic value rows only; no calibrated promotion band |
| `structural_ar1_quadratic_h16` | `BLOCKED_REQUIRES_ADAPTER` | `BLOCKED_REQUIRES_ADAPTER` | `0` | `0` | `N/A_BLOCKED_REQUIRES_ADAPTER` | The structural row uses stochastic m dynamics plus deterministic k completion.  A reviewed singular-completion Algorithm 1 adapter is required before source-core execution. |
| `spatial_sir_j3_rk4` | `RUNNABLE_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `30` | `30` | `diagnostic_only_no_exact_oracle_in_P3` | finite diagnostic value rows only; no calibrated promotion band |
| `predator_prey_rk4` | `RUNNABLE_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `30` | `30` | `diagnostic_only_no_exact_oracle_in_P3` | finite diagnostic value rows only; no calibrated promotion band |

## Veto Diagnostics

| Diagnostic | Status |
| --- | --- |
| `p2_contract_absent_or_not_passed` | `False` |
| `row_count_or_order_mismatch` | `False` |
| `runnable_row_missing_value_rows` | `False` |
| `old_ledh_pfpf_ot_runtime_module_imported` | `False` |
| `old_route_used_as_current_algorithm1_evidence` | `False` |
| `algorithm1_route_fields_missing` | `False` |
| `missing_monte_carlo_uncertainty` | `False` |
| `unclassified_execution_failure` | `False` |
| `unsupported_comparator_ranked` | `False` |
| `finite_only_promoted` | `False` |
| `value_used_to_promote_gradient` | `False` |
| `algorithm1_gradients_computed` | `False` |
| `ot_or_annealed_transport_used` | `False` |

## Value Summaries

### lgssm_2d_h25_rich

| Method | Particles | Seeds | Finite | Mean value | SE | RMSE vs reference | Min ESS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bootstrap_pf_no_resampling_tf` | 8 | `5` | `5` | `-2.2380364702306967` | `0.2042068013971282` | `0.5090640213177533` | `2.0335887561577626` |
| `bootstrap_pf_no_resampling_tf` | 16 | `5` | `5` | `-2.5789591776403613` | `0.16158196193478447` | `0.32527973625279566` | `3.0344589710535725` |
| `bootstrap_pf_no_resampling_tf` | 32 | `5` | `5` | `-2.8760650306352935` | `0.18820547064609247` | `0.5033277858709079` | `5.853064121834346` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 8 | `5` | `5` | `-2.385044473335046` | `0.26150468671406357` | `0.5460296492923338` | `1.7022406872178886` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 16 | `5` | `5` | `-2.488133304958704` | `0.22739998304309836` | `0.45796931675642605` | `3.048355758891817` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 32 | `5` | `5` | `-2.467853404191689` | `0.20582366822077328` | `0.41825736258132357` | `3.056368736456337` |

### predator_prey_rk4

| Method | Particles | Seeds | Finite | Mean value | SE | RMSE vs reference | Min ESS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bootstrap_pf_no_resampling_tf` | 8 | `5` | `5` | `-16.554527638635992` | `0.39841031322168924` | `None` | `1.2441231502509633` |
| `bootstrap_pf_no_resampling_tf` | 16 | `5` | `5` | `-16.48573134863107` | `0.2816804246852498` | `None` | `2.144621736875749` |
| `bootstrap_pf_no_resampling_tf` | 32 | `5` | `5` | `-15.97042842731928` | `0.25509453498076223` | `None` | `2.2217543199718386` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 8 | `5` | `5` | `-15.49250581224249` | `0.13173341111037257` | `None` | `5.25830066443997` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 16 | `5` | `5` | `-15.419884404707068` | `0.0920296256699032` | `None` | `6.530837369261795` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 32 | `5` | `5` | `-15.28323655914166` | `0.07581189616226446` | `None` | `8.622173630187634` |

### range_bearing_4d_h20_rich

| Method | Particles | Seeds | Finite | Mean value | SE | RMSE vs reference | Min ESS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bootstrap_pf_no_resampling_tf` | 8 | `5` | `5` | `-6.074211899692977` | `2.8066756451358676` | `None` | `1.000005930814993` |
| `bootstrap_pf_no_resampling_tf` | 16 | `5` | `5` | `1.5974905689199326` | `2.0342998761200697` | `None` | `1.0000001413120023` |
| `bootstrap_pf_no_resampling_tf` | 32 | `5` | `5` | `2.9884302961004585` | `0.8337306326759887` | `None` | `1.0095236102109288` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 8 | `5` | `5` | `-2.9564240995257682` | `2.0123283981866087` | `None` | `1.001843832953691` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 16 | `5` | `5` | `1.797271544183196` | `0.5039957061912675` | `None` | `1.0008572195483814` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 32 | `5` | `5` | `2.7475727341346894` | `0.7908012028888805` | `None` | `1.037538818611937` |

### spatial_sir_j3_rk4

| Method | Particles | Seeds | Finite | Mean value | SE | RMSE vs reference | Min ESS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bootstrap_pf_no_resampling_tf` | 8 | `5` | `5` | `-34.81021395458376` | `0.17306370295014756` | `None` | `3.3305766844286673` |
| `bootstrap_pf_no_resampling_tf` | 16 | `5` | `5` | `-34.762585873752855` | `0.11413042596831165` | `None` | `7.045390280326577` |
| `bootstrap_pf_no_resampling_tf` | 32 | `5` | `5` | `-34.77005168583207` | `0.006381122624373871` | `None` | `13.645092709598442` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 8 | `5` | `5` | `-38.03784109869083` | `0.7517062354948472` | `None` | `1.0123711593306748` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 16 | `5` | `5` | `-38.02390589471675` | `0.4857966760223286` | `None` | `1.1200733495210617` |
| `ledh_pfpf_alg1_ukf_no_resampling_tf` | 32 | `5` | `5` | `-37.33258148667472` | `0.38796876526950913` | `None` | `2.2192517585908202` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `LOCAL_PASS_P3_V2_ALG1_UKF_VALUES_DIAGNOSTIC_ONLY_PENDING_CLAUDE_REVIEW` | every P2 row appears; P2 runnable rows executed or explicitly downgraded; P2-blocked rows remain visible with adapter reasons; finite rows carry uncertainty | `{'p2_contract_absent_or_not_passed': False, 'row_count_or_order_mismatch': False, 'runnable_row_missing_value_rows': False, 'old_ledh_pfpf_ot_runtime_module_imported': False, 'old_route_used_as_current_algorithm1_evidence': False, 'algorithm1_route_fields_missing': False, 'missing_monte_carlo_uncertainty': False, 'unclassified_execution_failure': False, 'unsupported_comparator_ranked': False, 'finite_only_promoted': False, 'value_used_to_promote_gradient': False, 'algorithm1_gradients_computed': False, 'ot_or_annealed_transport_used': False}` | non-LGSSM rows have no exact oracle in P3 | Claude P3 read-only review, then P4 gradients consume frozen contracts | no gradient, stochastic-resampling, OT-extension, performance, or production claim |

## Gate Definition

- Local decision semantics: LOCAL_PASS means the locally generated P3 artifact satisfies the pre-Claude gate and remains pending read-only Claude review.  It is not an unconditional phase pass.
- P2 blocked carry-forward allowed: `True`
- P2 blocked carry-forward rule: Rows blocked in P2 may remain BLOCKED_REQUIRES_ADAPTER in P3 with row visibility, zero value rows, N/A comparator route, missing adapter items, and status reason preserved.  P3 does not require those rows to execute values.
- P2 runnable rule: Rows marked RUNNABLE_ALG1 in P2 must execute value rows or be explicitly downgraded with failure diagnostics.
- Promotion rule: P3 value evidence is diagnostic-only.  Finite values, ESS, and particle-ladder trends cannot promote correctness.

## Post-Run Red-Team Note

Strongest alternative explanation: finite non-LGSSM values demonstrate execution only, not correctness, because P3 lacks exact nonlinear oracles.

Result that would overturn the local decision: Claude finds old-route leakage, missing P2 consumption, missing uncertainty, or a finite-only promotion.

Weakest part of the evidence: P3 is diagnostic-only by design and does not calibrate thresholds.

## Run Manifest

- command: `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_alg1_ukf_values_tf`
- git branch: `main`
- git commit: `26485010c28e11b3591da59b7ca375d4764c3d8d`
- CPU/GPU status: CPU-only, `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import
- visible GPU devices: `[]`
- P2 JSON: `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_alg1_ukf_contracts_2026-06-10.json`
- P2 contract checksum: `47c57943037100b853cea5d3d862b839d23b012b433b006b51902bfd984672ce`
- value seeds: `[101, 202, 303, 404, 505]`
- value particle counts: `[8, 16, 32]`
- pseudo-time steps: `[0.5, 0.5]`
- UKF parameters: `{'alpha': 1.0, 'beta': 2.0, 'kappa': 0.0}`
- JSON: `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_alg1_ukf_values_2026-06-10.json`
- report: `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-alg1-ukf-values-2026-06-10.md`
- result: `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p3-v2-values-result-2026-06-10.md`
- wall time seconds: `141.36719137709588`

## Nonclaims

- P3 value rows are diagnostic-only and do not certify numerical closeness.
- P3 value rows do not imply gradient correctness.
- P3 does not use OT or annealed transport.
- P3 does not establish stochastic-resampling correctness.
- P3 blocked rows are adapter work items, not negative scientific evidence.
- P3 does not establish production readiness, HMC readiness, GPU performance, or broad model superiority.

## Gate Status

P3 is pending Claude read-only review.
