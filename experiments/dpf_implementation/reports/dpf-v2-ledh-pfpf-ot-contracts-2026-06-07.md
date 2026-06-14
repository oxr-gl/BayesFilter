# DPF V2 Algorithm Full Comparison P5 LEDH-PFPF-OT Contracts Result

metadata_date: 2026-06-07
visible_execution_timestamp: `2026-06-08T15:05:00+08:00`
phase: P5
execution_route: `VISIBLE_IN_DIALOGUE`
status: `PASS_P5_LEDH_PFPF_OT_CONTRACTS_READY_FOR_P6`

## Question

Can executable LEDH-PFPF-OT comparison contracts be frozen for all six V2 rows before LEDH-PFPF-OT value or gradient execution?

## Evidence Contract

Primary criterion:

- one frozen LEDH-PFPF-OT contract per V2 row in exact order;
- each contract records pre-flow transition proposal, LEDH linearization, Jacobian route, affine map, forward logdet convention, proposal density, target transition density, observation density, PF-PF correction, fixed ESS trigger mask, OT settings, gradient knobs, dtype, tolerances, and checksums;
- BayesFilter and FilterFlow-side adapters consume the same contract checksum.

Veto diagnostics:

- row disappearance or row-order mismatch;
- P0/P1/P4 preflight drift;
- missing LEDH-specific proposal, density, logdet, correction, branch, OT, or gradient field;
- value or gradient result execution before contract freeze;
- runtime Boolean ESS trigger decisions in the primary fixed-branch contract;
- `.localsource/filterflow` mutation, student command, oracle framing, or finite differences promoted to a gradient gate.

Non-claims:

- P5 freezes contracts only; it does not validate LEDH-PFPF-OT values or gradients.

## Local Skeptical Phase Audit

Audit status: `PASS_LOCAL_PHASE_AUDIT`.

Wrong-baseline risk: controlled. P5 requires visible P0/P1/P4 pass artifacts and freezes a new LEDH contract bundle for P6/P7.

Proxy-metric risk: controlled. P5 records no LEDH value, gradient, ESS, RMSE, runtime, or finite-difference promotion metric.

Missing stop-condition risk: controlled. Missing LEDH fields, stale preflight artifacts, unsafe branch sources, or any value/gradient execution remain vetoes.

Unfair-comparison risk: controlled. Both later consumers are bound to identical contract checksums.

Environment-mismatch risk: controlled. TensorFlow was imported only for fixture serialization with `CUDA_VISIBLE_DEVICES=-1`; no GPU claim is made.

Audit decision: local pass pending Claude read-only review.

## Result

- Decision: `PASS_P5_LEDH_PFPF_OT_CONTRACTS_READY_FOR_P6`
- JSON artifact: `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_contracts_2026-06-07.json`
- Markdown report: `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-contracts-2026-06-07.md`
- Phase result: `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-result-2026-06-07.md`
- Contract bundle checksum: `20b7cb9a05a2de41bbf139a90bff8c8465f7bda7e4fd84fe6b83ee48a09c39f4`
- Reproducibility digest: `6770ce953db079fe003d62e631e8a379cf68e6889006d583b39d70e6f5139661`

## V2 Contract Rows

| Model id | Horizon | Particles | Fixed ESS mask | LEDH flow route | Included AD knobs | P7 readiness | Contract checksum |
|---|---:|---:|---|---|---|---|---|
| `lgssm_2d_h25_rich` | 3 | 3 | `[False, True, False]` | `ledh_flow_batch_tf` | `['transition_matrix_scale', 'observation_noise_scale']` | `READY_FOR_P7_AFTER_P6_VALUE_PASS` | `8a446b5418992b28a481de4b7e0f1fa0a7ad76be6ac69c4adead70bbd5bc64af` |
| `sv_1d_h18_rich` | 3 | 3 | `[False, True, False]` | `v2_scalar_sv_ledh_flow_to_be_executed_in_p6` | `['mu', 'phi', 'sigma']` | `READY_FOR_P7_AFTER_P6_VALUE_PASS` | `1f22704ef1c671c57f0fa158f76b16ca81e8c40b3f0050c73dfd095566159bf4` |
| `range_bearing_4d_h20_rich` | 3 | 3 | `[False, True, False]` | `ledh_flow_batch_tf` | `['sigma_range', 'sigma_bearing']` | `READY_FOR_P7_AFTER_P6_VALUE_PASS` | `b78733ff083e6fb352d55eb6279cd76e04b2640f4b5077e5f568efdc3a66cff7` |
| `structural_ar1_quadratic_h16` | 3 | 3 | `[False, True, False]` | `v2_structural_split_scalar_ledh_flow_to_be_executed_in_p6` | `['rho', 'sigma', 'c']` | `READY_FOR_P7_AFTER_P6_VALUE_PASS` | `40318a66d23651948e2e1b4af81a7d085297620465a0a1e28b121b74db1434cf` |
| `spatial_sir_j3_rk4` | 3 | 3 | `[False, True, False]` | `v2_autodiff_ledh_flow_to_be_executed_in_p6` | `[]` | `PREDECLARED_EXCLUDED_NO_PHYSICAL_KNOB` | `c8c42fde066d780301aa8a4dd4faeb03fd14a6380d98e83f0cae50e35a228453` |
| `predator_prey_rk4` | 3 | 3 | `[False, True, False]` | `v2_autodiff_ledh_flow_to_be_executed_in_p6` | `['r']` | `READY_FOR_P7_AFTER_P6_VALUE_PASS` | `54edee5a7bffc9b3e3e2cac70c6ab64139e1d2cce176c04c4c05c5cc24c43888` |

## Frozen LEDH Semantics

- Pre-flow proposal: fixed transition innovations before LEDH flow.
- PF-PF correction: `log_weights + target_transition + target_observation - pre_flow_log_density + forward_log_det`.
- Forward logdet convention: `log_abs_det(d post_flow / d pre_flow)`, added in the correction.
- Branch source: fixed ESS trigger masks from the V2 contract, not runtime Boolean ESS decisions.
- FilterFlow support: BayesFilter-owned adapter-hosted route; `.localsource/filterflow` is read-only.

## LEDH-PFPF-OT Settings

| Field | Value |
|---|---|
| transport method | `annealed_transport` |
| resampling method | `filterflow_style_annealed_transport_tf` |
| epsilon | `0.5` |
| iterations | `80` |
| tolerance | `1e-07` |
| annealed scaling | `0.9` |
| annealed convergence threshold | `0.001` |
| transport gradient mode | `filterflow_clipped` |
| application mode | `active_rows_only` |
| LEDH covariance jitter | `1e-09` |
| primary branch decision | `fixed_ess_trigger_mask_from_contract` |

## Primary Criterion Fields

- six_v2_rows_in_exact_order: `PASS`
- one_contract_per_row: `PASS`
- all_contracts_record_pre_flow_transition_proposal: `PASS`
- all_contracts_record_ledh_linearization_and_jacobian: `PASS`
- all_contracts_record_affine_map_and_forward_logdet: `PASS`
- all_contracts_record_density_routes: `PASS`
- all_contracts_record_pfpf_correction: `PASS`
- all_contracts_record_fixed_ess_trigger_mask: `PASS`
- all_contracts_record_ot_settings: `PASS`
- all_contracts_record_gradient_knobs: `PASS`
- all_contracts_record_dtype_tolerances_and_checksums: `PASS`
- bf_and_ff_consume_same_contract_checksum: `PASS`
- no_ledh_value_or_gradient_execution: `PASS`

## Veto Diagnostics

- missing_v2_row: `PASS`
- row_order_mismatch: `PASS`
- p0_p1_p4_preflight_drift: `PASS`
- ledh_value_result_inspected_or_computed: `PASS`
- ledh_gradient_result_inspected_or_computed: `PASS`
- missing_ledh_specific_field: `PASS`
- bootstrap_contract_copied_without_ledh_fields: `PASS`
- ambiguous_proposal_density_or_logdet: `PASS`
- runtime_boolean_ess_trigger_in_primary_contract: `PASS`
- stochastic_sampling_left_unfrozen: `PASS`
- missing_tolerance_or_gradient_knob: `PASS`
- localsource_filterflow_mutated: `PASS`
- student_command_or_metric: `PASS`
- oracle_framing: `PASS`
- finite_difference_promoted_to_gradient_gate: `PASS`

## Command Manifest

| Field | Value |
|---|---|
| git commit | `137f6ba5a03ebab199c8ab4699354d50bd560123` |
| git branch | `main` |
| P5 touched paths | `experiments/dpf_implementation/tf_tfp/runners/run_v2_ledh_pfpf_ot_contracts_tf.py; experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_contracts_2026-06-07.json; experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-contracts-2026-06-07.md; docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-result-2026-06-07.md; docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-visible-execution-ledger-2026-06-08.md` |
| dirty status | full repo dirty state is recorded in JSON run manifest; unrelated dirty work is not interpreted as P5 evidence |
| command | `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_ot_contracts_tf` |
| validation commands | `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_contracts_2026-06-07.json`; `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_ot_contracts_tf --validate-only`; `git diff --check` on P5 files |
| environment | `/home/chakwong/BayesFilter`; Python `3.11.14`; TensorFlow `2.19.1`; TFP `0.25.0` |
| CPU/GPU status | CPU-only TensorFlow serialization; pre-import `CUDA_VISIBLE_DEVICES=-1`; visible GPUs `[]` |
| random seeds | no RNG used in P5; fixed V2 path particles and innovations are serialized from fixtures |
| dtype | `tf.float64` / JSON dtype `float64` |
| output artifacts | `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_contracts_2026-06-07.json`; `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-contracts-2026-06-07.md`; `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-result-2026-06-07.md` |

## Review State

review_round: 0 pending Claude P5 contract review

open_material_blockers: none identified locally

repair_amendment_required: false

next_allowed_action: begin P6 PRECHECK visibly in current dialogue

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| `PASS_P5_LEDH_PFPF_OT_CONTRACTS_READY_FOR_P6` | six same-checksum LEDH-PFPF-OT contracts frozen | all local P5 veto diagnostics pass | Claude may find LEDH contract adequacy gaps before P6 | run chunked Claude P5 read-only review | no value match, gradient match, filtering correctness, stochastic resampling claim, or production readiness |

## Post-Run Red Team

Strongest alternative explanation: the frozen contracts may still be insufficient for P6/P7 implementation if a later adapter needs a more precise per-row LEDH flow field.

Result that would overturn the local decision: Claude or P6/P7 finds a missing proposal, Jacobian, density, logdet, branch, OT, tolerance, or gradient field needed to execute the same contract on both sides.

Weakest evidence link: P5 serializes contract data but does not execute the LEDH value or gradient paths.

## Non-Claims

- P5 freezes LEDH-PFPF-OT contracts only.
- P5 does not validate BayesFilter LEDH-PFPF-OT values.
- P5 does not validate FilterFlow-side adapter LEDH-PFPF-OT values.
- P5 does not validate LEDH-PFPF-OT gradients.
- P5 does not establish filtering correctness.
- P5 does not establish stochastic resampling distribution correctness.
- P5 does not make a student implementation claim.
- P5 does not make a GPU, scalability, deployment, or production-readiness claim.
