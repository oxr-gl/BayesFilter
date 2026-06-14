# P2 Result: V2 Algorithm 1 UKF Contract Replacement

metadata_date: 2026-06-10
phase: P2
status: PASS_P2_V2_ALG1_UKF_CONTRACTS_PENDING_CLAUDE_REVIEW

## Skeptical Plan Audit

Status: `PASS_FOR_CONTRACT_FREEZE_ONLY`.

Old V2 LEDH-PFPF-OT contracts define coverage only.  P2 does not use old values, gradients, or OT route identifiers as Algorithm 1 evidence.

P2 records no value, gradient, ESS, or runtime performance metrics.  Threshold fields are frozen as diagnostic-only or adapter-blocked before execution.

P3/P4 must consume this frozen contract.  Rows with missing callback contracts are blocked rather than run.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the old V2 LEDH-PFPF-OT contract lane be replaced with Algorithm 1 UKF contracts for every V2 model row? |
| Baseline/comparator | Old V2 contracts define coverage.  Current contract rows bind Algorithm 1 route fields, callbacks, scalar definitions, seeds, particle ladders, pseudo-time schedule, UKF parameters, and diagnostic-only threshold policy. |
| Primary criterion | Exactly six V2 rows are frozen in order with status RUNNABLE_ALG1, N_A_NOT_APPLICABLE, or BLOCKED_REQUIRES_ADAPTER. |
| Threshold policy | Noise scale, horizon, nonlinearity, and particle count alter Monte Carlo error.  P2 therefore freezes diagnostic execution contracts instead of inventing global error thresholds. |
| Not concluded | P2 freezes contracts only; it does not execute Algorithm 1 values.; P2 does not execute gradients or validate gradient correctness.; P2 does not set calibrated numerical value or gradient thresholds.; P2 does not rank filters or compare performance.; OT and annealed transport are not part of the source Algorithm 1 core.; Blocked rows are adapter work items, not negative scientific evidence.; P2 does not establish production readiness, HMC readiness, GPU performance, or broad model superiority. |

## Contract Rows

| Model | Status | Comparator | Value tolerance | Gradient tolerance | Missing adapter items |
| --- | --- | --- | --- | --- | --- |
| `lgssm_2d_h25_rich` | `RUNNABLE_ALG1` | `exact_kalman_for_lgssm` | `N/A_DIAGNOSTIC_ONLY_IN_P3_P4` | `N/A_DIAGNOSTIC_ONLY_IN_P3_P4` | none |
| `sv_1d_h18_rich` | `BLOCKED_REQUIRES_ADAPTER` | `N/A_BLOCKED_REQUIRES_ADAPTER` | `N/A_BLOCKED_REQUIRES_ADAPTER` | `N/A_BLOCKED_REQUIRES_ADAPTER` | reviewed observation_mean_fn and observation_covariance_fn for true or surrogate SV likelihood; explicit source-core versus extension classification for log-square surrogate; target observation_log_density_fn matching the chosen scalar; same-scalar value and gradient comparator policy |
| `range_bearing_4d_h20_rich` | `RUNNABLE_ALG1` | `diagnostic_only_no_exact_oracle_in_P3` | `N/A_DIAGNOSTIC_ONLY_IN_P3_P4` | `N/A_DIAGNOSTIC_ONLY_IN_P3_P4` | none |
| `structural_ar1_quadratic_h16` | `BLOCKED_REQUIRES_ADAPTER` | `N/A_BLOCKED_REQUIRES_ADAPTER` | `N/A_BLOCKED_REQUIRES_ADAPTER` | `N/A_BLOCKED_REQUIRES_ADAPTER` | reviewed stochastic-coordinate transition_sample and transition_log_density; deterministic k-completion carried consistently through post-flow state; PSD covariance lifecycle for singular completion without false full-state density; same-scalar gradient parameterization for structural knobs |
| `spatial_sir_j3_rk4` | `RUNNABLE_ALG1` | `diagnostic_only_no_exact_oracle_in_P3` | `N/A_DIAGNOSTIC_ONLY_IN_P3_P4` | `N/A_DIAGNOSTIC_ONLY_IN_P3_P4` | none |
| `predator_prey_rk4` | `RUNNABLE_ALG1` | `diagnostic_only_no_exact_oracle_in_P3` | `N/A_DIAGNOSTIC_ONLY_IN_P3_P4` | `N/A_DIAGNOSTIC_ONLY_IN_P3_P4` | none |

## Route Fields

| Field | Value |
| --- | --- |
| `method_generation` | `li_coates_algorithm1_ukf_covariance_lifecycle` |
| `flow_source_route` | `li_coates_2017_algorithm1_ledh_pfpf` |
| `covariance_route` | `per_particle_ukf_prediction_update` |
| `flow_anchor_route` | `zero_noise_transition` |
| `resampling_route` | `none` |
| `previous_ledh_pfpf_ot_evidence_status` | `quarantined` |
| `prediction_covariance_route` | `ukf_prediction_per_particle_covariance` |
| `update_covariance_route` | `ukf_update_per_particle_covariance` |
| `core_resampling_route` | `none` |
| `extension_resampling_route` | `none` |
| `evidence_route_class` | `SOURCE_ALGORITHM1_CORE` |

## Veto Diagnostics

| Diagnostic | Status |
| --- | --- |
| `row_count_mismatch` | `False` |
| `contract_status_invalid` | `False` |
| `old_ledh_pfpf_ot_runtime_module_imported` | `False` |
| `old_route_used_as_current_algorithm1_evidence` | `False` |
| `missing_mandatory_algorithm1_route_field` | `False` |
| `ot_labelled_as_algorithm1_core` | `False` |
| `blocked_row_missing_adapter_items` | `False` |
| `runnable_row_has_missing_adapter_items` | `False` |
| `scalar_or_gradient_object_unspecified` | `False` |
| `threshold_missing_without_reason` | `False` |
| `value_or_gradient_executed_in_p2` | `False` |
| `finite_only_promotion_allowed` | `False` |

## Summary

- contract bundle checksum: `47c57943037100b853cea5d3d862b839d23b012b433b006b51902bfd984672ce`
- status counts: `{'BLOCKED_REQUIRES_ADAPTER': 2, 'N_A_NOT_APPLICABLE': 0, 'RUNNABLE_ALG1': 4}`
- runnable models: `['lgssm_2d_h25_rich', 'range_bearing_4d_h20_rich', 'spatial_sir_j3_rk4', 'predator_prey_rk4']`
- blocked models: `['sv_1d_h18_rich', 'structural_ar1_quadratic_h16']`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PASS_P2_V2_ALG1_UKF_CONTRACTS_PENDING_CLAUDE_REVIEW` | six V2 contracts frozen in order with diagnostic-only thresholds | `{'row_count_mismatch': False, 'contract_status_invalid': False, 'old_ledh_pfpf_ot_runtime_module_imported': False, 'old_route_used_as_current_algorithm1_evidence': False, 'missing_mandatory_algorithm1_route_field': False, 'ot_labelled_as_algorithm1_core': False, 'blocked_row_missing_adapter_items': False, 'runnable_row_has_missing_adapter_items': False, 'scalar_or_gradient_object_unspecified': False, 'threshold_missing_without_reason': False, 'value_or_gradient_executed_in_p2': False, 'finite_only_promotion_allowed': False}` | P3/P4 still must implement and validate callback adapters | Claude P2 read-only review, then P3 values consume frozen contracts | no value, gradient, performance, OT-extension, or production claim |

## Post-Run Red-Team Note

Strongest alternative explanation: a row marked runnable may still fail in P3 because the declared callback route has not yet been executed.

Result that would overturn the local decision: P3/P4 or Claude finds a missing callback, an old-route leak, a row-order mismatch, or an implicit numerical threshold.

Weakest part of the evidence: P2 is declarative contract freeze only; it deliberately does not execute Algorithm 1 values or gradients.

## Run Manifest

- command: `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_alg1_ukf_contracts_tf`
- git branch: `main`
- git commit: `26485010c28e11b3591da59b7ca375d4764c3d8d`
- CPU/GPU status: CPU-only, `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import
- visible GPU devices: `[]`
- value seeds: `[101, 202, 303, 404, 505]`
- value particle counts: `[8, 16, 32]`
- gradient seeds: `[101, 202, 303]`
- gradient particle counts: `[4, 8, 16]`
- pseudo-time steps: `[0.5, 0.5]`
- UKF parameters: `{'alpha': 1.0, 'beta': 2.0, 'kappa': 0.0}`
- plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p2-v2-contracts-subplan-2026-06-10.md`
- registry: `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-registry-2026-06-10.json`
- P1 JSON: `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_alg1_ukf_direct_replacements_2026-06-10.json`
- review ledger: `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-claude-review-ledger-2026-06-10.md`
- JSON: `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_alg1_ukf_contracts_2026-06-10.json`
- report: `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-alg1-ukf-contracts-2026-06-10.md`
- result: `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p2-v2-contracts-result-2026-06-10.md`
- wall time seconds: `0.776638220064342`

## Nonclaims

- P2 freezes contracts only; it does not execute Algorithm 1 values.
- P2 does not execute gradients or validate gradient correctness.
- P2 does not set calibrated numerical value or gradient thresholds.
- P2 does not rank filters or compare performance.
- OT and annealed transport are not part of the source Algorithm 1 core.
- Blocked rows are adapter work items, not negative scientific evidence.
- P2 does not establish production readiness, HMC readiness, GPU performance, or broad model superiority.

## Gate Status

P2 is pending Claude read-only review.
