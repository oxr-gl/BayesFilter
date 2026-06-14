# DPF V2 Algorithm Full Comparison P6 LEDH-PFPF-OT Values Result

metadata_date: 2026-06-07
visible_execution_timestamp: `2026-06-08T16:04:00+08:00`
phase: P6
execution_route: `VISIBLE_IN_DIALOGUE`
status: `PASS_P6_LEDH_PFPF_OT_VALUES_READY_FOR_P7`

## Question

Do BayesFilter and BayesFilter-owned FilterFlow-side adapters match LEDH-PFPF-OT fixed-contract values and ledgers for all six V2 rows?

## Evidence Contract

Primary criterion:

- for every V2 row, BayesFilter and the BayesFilter-owned FilterFlow-side adapter consume the same frozen P5 LEDH-PFPF-OT contract;
- scalar values match within declared tolerance;
- required ledgers match, including pre-flow proposals, LEDH affine parameters, post-flow particles, pre-flow proposal log density, forward logdet, target transition density, observation density, PF-PF corrected log weights, frozen ESS trigger masks, OT transport matrix checksums, post-transport particles, incremental log normalizers, and final scalar.

Veto diagnostics:

- nonfinite proposal, logdet, corrected weight, scalar, or transport field;
- runtime branch mask differs from frozen P5 mask;
- transport settings differ from P5;
- PF-PF correction equation mismatch;
- BF/FF value delta exceeds tolerance;
- unclassified ledger mismatch;
- `.localsource/filterflow` mutation, student command, oracle framing, or finite differences promoted to a gradient gate.

Non-claims:

- P6 does not establish LEDH-PFPF-OT gradient agreement, LEDH proposal optimality, or stochastic resampling distribution correctness.
- P6 does not prove BayesFilter, FilterFlow, or adapter implementation correctness.
- P6 does not make a student implementation claim.
- P6 does not make a GPU, scalability, deployment, or production-readiness claim.
- P6 is not full-comparison success and does not establish P7 or P8 success.

## Local Skeptical Phase Audit

Audit status: `PASS_LOCAL_PHASE_AUDIT`.

Wrong-baseline risk: controlled. P6 uses the reviewed P5 contract bundle checksum and digest as the baseline and rejects drift.

Proxy-metric risk: controlled. ESS, runtime, LEDH diagnostics, and transport residuals are explanatory unless they trigger explicit finite or ledger-veto checks.

Missing stop-condition risk: controlled. P6 stops on row disappearance, mask drift, transport setting drift, PF-PF mismatch, value/ledger mismatch, nonfinite values, or stale P5 checksum/digest.

Unfair-comparison risk: controlled. Both adapters consume identical P5 contract bytes and the same frozen mask.

Environment-mismatch risk: controlled. TensorFlow was run CPU-only with pre-import `CUDA_VISIBLE_DEVICES=-1`; no GPU claim is made.

Audit decision: local pass pending Claude read-only review.

## Result

- Decision: `PASS_P6_LEDH_PFPF_OT_VALUES_READY_FOR_P7`
- JSON artifact: `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_values_2026-06-07.json`
- Markdown report: `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-values-2026-06-07.md`
- Phase result: `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-result-2026-06-07.md`
- P5 contract bundle checksum: `20b7cb9a05a2de41bbf139a90bff8c8465f7bda7e4fd84fe6b83ee48a09c39f4`
- P5 reproducibility digest: `6770ce953db079fe003d62e631e8a379cf68e6889006d583b39d70e6f5139661`
- P6 reproducibility digest: `890a07f12bd2fcc35e6bc747578455bc04c418948058b07d3f5d2f62b955fe24`

## Path Cells

| Model id | Status | Scalar delta | Max ledger delta | Fixed mask | Resampling count |
|---|---|---:|---:|---|---:|
| `lgssm_2d_h25_rich` | MATCHED | 0.0 | 0.0 | `[False, True, False]` | 1 |
| `sv_1d_h18_rich` | MATCHED | 0.0 | 0.0 | `[False, True, False]` | 1 |
| `range_bearing_4d_h20_rich` | MATCHED | 0.0 | 0.0 | `[False, True, False]` | 1 |
| `structural_ar1_quadratic_h16` | MATCHED | 0.0 | 0.0 | `[False, True, False]` | 1 |
| `spatial_sir_j3_rk4` | MATCHED | 0.0 | 0.0 | `[False, True, False]` | 1 |
| `predator_prey_rk4` | MATCHED | 0.0 | 0.0 | `[False, True, False]` | 1 |

## Primary Criterion Fields

- primary_ledger_fields: `['ancestors', 'prior_mean', 'pre_flow_particles', 'ledh_local_posterior_means', 'ledh_local_posterior_covariances', 'post_flow_particles', 'pre_flow_log_density', 'forward_log_det', 'target_transition_log_density', 'target_observation_log_density', 'pfpf_corrected_log_weights', 'normalized_log_weights', 'incremental_log_normalizer', 'fixed_ess_trigger', 'resampling_applied', 'transport_matrix', 'transport_matrix_checksum', 'post_transport_particles', 'post_transport_log_weights']`
- transport_fields: `['transport_matrix', 'transport_matrix_summary', 'transport_matrix_checksum', 'transport_diagnostics', 'post_transport_particles', 'post_transport_log_weights']`
- all_rows_matched: `True`
- all_contract_checksums_preserved: `True`
- all_adapter_input_checksums_preserved: `True`
- all_adapter_input_checksums_match_between_adapters: `True`
- all_fixed_masks_preserved: `True`

## Veto Diagnostics

- missing_v2_row: `False`
- row_order_mismatch: `False`
- p5_contract_checksum_changed: `False`
- p5_reproducibility_digest_changed: `False`
- runtime_branch_mask_differs_from_p5: `False`
- transport_settings_differ_from_p5: `False`
- pfpf_correction_equation_mismatch: `False`
- value_delta_exceeds_tolerance: `False`
- ledger_delta_exceeds_tolerance: `False`
- nonfinite_scalar_or_ledger: `False`
- adapter_input_checksum_mismatch: `False`
- unclassified_ledger_mismatch: `False`
- localsource_filterflow_mutated: `False`
- student_command_or_metric: `False`
- oracle_framing: `False`
- finite_difference_promoted_to_gradient_gate: `False`

## Explanatory Only Fields

- status counts: `{'MATCHED': 6}`
- max abs delta: `0.0`
- ESS policy: `ESS is reported as ledger context only; fixed P5 masks are the branch source.`
- runtime policy: `runtime is explanatory only`
- transport residual policy: `transport residuals can veto nonfinite or mismatched ledger fields but do not promote correctness`

## Governance Evidence

- source_artifacts: `{'p0_visible_governance_json': 'experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p0_visible_governance_2026-06-08.json', 'p1_architecture_json': 'experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p1_architecture_2026-06-07.json', 'p5_ledh_contract_json': 'experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_contracts_2026-06-07.json'}`
- localsource_filterflow_not_mutated: `True`
- student_commands_absent: `True`
- oracle_framing_forbidden: `True`
- finite_differences_diagnostic_only: `True`
- p1_ledh_filterflow_adapter_is_bayesfilter_owned: `True`
- p5_contract_forbids_runtime_branch_redecision: `True`

## Command Manifest

| Field | Value |
|---|---|
| git commit | `137f6ba5a03ebab199c8ab4699354d50bd560123` |
| git branch | `main` |
| dirty status | full repo dirty state is recorded in JSON run manifest; unrelated dirty work is not interpreted as P6 evidence |
| command | `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_ot_values_tf` |
| validation commands | `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_values_2026-06-07.json`; `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_ot_values_tf --validate-only`; `git diff --check` on P6 files |
| environment | `/home/chakwong/BayesFilter`; Python `3.11.14`; TensorFlow `2.19.1`; TFP `0.25.0` |
| CPU/GPU status | CPU-only TensorFlow run; pre-import `CUDA_VISIBLE_DEVICES=-1`; visible GPUs `[]` |
| random seeds | no RNG consumed in P6; frozen particles, observations, transition innovations, and masks from P5 |
| dtype | `tf.float64` / JSON dtype `float64` |
| output artifacts | `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_values_2026-06-07.json`; `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-values-2026-06-07.md`; `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-result-2026-06-07.md` |

## Review State

review_round: 5 final Claude synthesis returned VERDICT: AGREE

open_material_blockers: none identified locally

repair_amendment_required: false

next_allowed_action: begin P7 PRECHECK visibly in current dialogue

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| `PASS_P6_LEDH_PFPF_OT_VALUES_READY_FOR_P7` | all six LEDH-PFPF-OT value ledgers matched locally | all local P6 veto diagnostics clear | Claude may find adapter or artifact adequacy gaps | run chunked Claude P6 read-only review | no gradient agreement, stochastic resampling correctness, implementation proof, student claim, GPU claim, scalability, deployment, production readiness, full-comparison success, or P7/P8 success |

## Post-Run Red Team

Strongest alternative explanation: because both adapters are BayesFilter-owned, P6 can miss a defect shared by the contract-formula adapter and the BayesFilter model surface.

What would overturn the local decision: any reviewer finding that the FilterFlow-side adapter is not the P1/P5-frozen adapter surface, that a required LEDH ledger field is omitted, that P5 masks/settings changed, or that the same-contract identity is broken.

Weakest part of the evidence: P6 is fixed-contract value evidence only and does not test gradient correctness or stochastic resampling distribution behavior.
