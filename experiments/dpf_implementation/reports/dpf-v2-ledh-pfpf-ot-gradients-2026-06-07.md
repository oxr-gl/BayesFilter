# DPF V2 Algorithm Full Comparison P7 LEDH-PFPF-OT Gradients Result

metadata_date: 2026-06-07
visible_execution_timestamp: `2026-06-08T17:20:00+08:00`
phase: P7
execution_route: `VISIBLE_IN_DIALOGUE`
status: `PASS_P7_LEDH_PFPF_OT_GRADIENTS_READY_FOR_P8`

## Question

Do BayesFilter and BayesFilter-owned FilterFlow-side adapters match LEDH-PFPF-OT fixed-branch AD gradients for all P5-required physical knobs after the reviewed P6 value pass?

## Evidence Contract

Primary criterion:

- for every P5-included physical knob, BayesFilter and the BayesFilter-owned FilterFlow-side adapter consume the same frozen P5 LEDH-PFPF-OT contract;
- scalar values match within declared tolerance on the deterministic fixed branch;
- AD gradients through the LEDH proposal, PF-PF correction, and deterministic OT transform match within declared tolerance;
- `spatial_sir_j3_rk4` remains a predeclared no-physical-knob exclusion, not a failed row.

Veto diagnostics:

- nonfinite scalar or AD gradient for an included knob;
- BF/FF scalar mismatch;
- BF/FF AD-gradient mismatch;
- missing or changed required knob after P5;
- missing SIR predeclared exclusion;
- P5 checksum/digest or P6 digest drift;
- finite differences promoted to a gradient gate;
- value agreement used to excuse derivative mismatch;
- `.localsource/filterflow` mutation, student command, oracle framing, or unsupported full-comparison/P8 success claim.

Non-claims:

- P7 does not establish gradients through stochastic resampling distributions or random/discrete branch selection.
- P7 does not prove BayesFilter, FilterFlow, or adapter implementation correctness.
- P7 does not make a student implementation claim.
- P7 does not make a GPU, scalability, deployment, production-readiness, full-comparison, or P8 success claim.

## Local Skeptical Phase Audit

Audit status: `PASS_LOCAL_PHASE_AUDIT`.

Wrong-baseline risk: controlled. P7 rejects drift from the reviewed P5 contract bundle and reviewed P6 value digest.

Proxy-metric risk: controlled. FD ladders, AD-vs-FD deltas, gradient norms, and runtime are explanatory only.

Missing stop-condition risk: controlled. P7 stops on included-knob nonfinite or mismatched AD gradients, P5/P6 drift, missing SIR exclusion, or governance vetoes.

Unfair-comparison risk: controlled. Both adapters consume identical contract bytes, branch masks, OT settings, scalar definition, and included knob list.

Environment-mismatch risk: controlled. TensorFlow was run CPU-only with pre-import `CUDA_VISIBLE_DEVICES=-1`; no GPU claim is made.

Audit decision: reviewed local pass; final Claude read-only synthesis returned VERDICT: AGREE.

## Result

- Decision: `PASS_P7_LEDH_PFPF_OT_GRADIENTS_READY_FOR_P8`
- JSON artifact: `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_gradients_2026-06-07.json`
- Markdown report: `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-gradients-2026-06-07.md`
- Phase result: `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-result-2026-06-07.md`
- P5 contract bundle checksum: `20b7cb9a05a2de41bbf139a90bff8c8465f7bda7e4fd84fe6b83ee48a09c39f4`
- P5 reproducibility digest: `6770ce953db079fe003d62e631e8a379cf68e6889006d583b39d70e6f5139661`
- P6 reproducibility digest: `890a07f12bd2fcc35e6bc747578455bc04c418948058b07d3f5d2f62b955fe24`
- P7 reproducibility digest: `d9d6f691c00171e287971b89b461b151ee2dd8d8e1c1804c45421bfa7dc94f14`

## Gradient Cells

| Model id | Status | Knobs | Scalar delta | Max AD gradient delta |
|---|---|---|---:|---:|
| `lgssm_2d_h25_rich` | MATCHED | `['transition_matrix_scale', 'observation_noise_scale']` | 0.0 | 0.0 |
| `sv_1d_h18_rich` | MATCHED | `['mu', 'phi', 'sigma']` | 0.0 | 1.7763568394002505e-15 |
| `range_bearing_4d_h20_rich` | MATCHED | `['sigma_range', 'sigma_bearing']` | 0.0 | 0.0 |
| `structural_ar1_quadratic_h16` | MATCHED | `['rho', 'sigma', 'c']` | 0.0 | 1.7763568394002505e-15 |
| `spatial_sir_j3_rk4` | PREDECLARED_EXCLUDED | `excluded: ['sir_physical_knobs']` | N/A | N/A |
| `predator_prey_rk4` | MATCHED | `['r']` | 0.0 | 1.7763568394002505e-15 |

## Primary Criterion Fields

- included_gradient_knobs: `{'lgssm_2d_h25_rich': ['transition_matrix_scale', 'observation_noise_scale'], 'sv_1d_h18_rich': ['mu', 'phi', 'sigma'], 'range_bearing_4d_h20_rich': ['sigma_range', 'sigma_bearing'], 'structural_ar1_quadratic_h16': ['rho', 'sigma', 'c'], 'spatial_sir_j3_rk4': [], 'predator_prey_rk4': ['r']}`
- excluded_gradient_knobs: `{'lgssm_2d_h25_rich': [], 'sv_1d_h18_rich': [], 'range_bearing_4d_h20_rich': [], 'structural_ar1_quadratic_h16': [], 'spatial_sir_j3_rk4': ['sir_physical_knobs'], 'predator_prey_rk4': []}`
- total_included_physical_knobs: `11`
- predeclared_excluded_rows: `['spatial_sir_j3_rk4']`
- all_included_knobs_executed: `True`
- all_gradient_rows_matched_or_predeclared_excluded: `True`
- all_adapter_input_checksums_preserved: `True`
- all_adapter_input_checksums_match_between_adapters: `True`
- finite_difference_promotion_gate: `False`

## Veto Diagnostics

- missing_v2_row: `False`
- row_order_mismatch: `False`
- p5_contract_checksum_changed: `False`
- p5_reproducibility_digest_changed: `False`
- p6_value_pass_missing_or_changed: `False`
- gradient_knob_changed_after_p5: `False`
- sir_predeclared_exclusion_missing_or_failed: `False`
- scalar_mismatch: `False`
- ad_gradient_mismatch: `False`
- nonfinite_scalar_or_gradient: `False`
- unclassified_gradient_mismatch: `False`
- disconnected_gradient: `False`
- adapter_input_checksum_mismatch: `False`
- value_agreement_used_to_excuse_derivative_mismatch: `False`
- finite_difference_promoted_to_gradient_gate: `False`
- localsource_filterflow_mutated: `False`
- student_command_or_metric: `False`
- oracle_framing: `False`
- unsupported_full_comparison_or_p8_success_claim: `False`

## Explanatory Only Fields

- status_counts: `{'MATCHED': 5, 'PREDECLARED_EXCLUDED': 1}`
- max_abs_scalar_delta: `0.0`
- max_abs_gradient_delta: `1.7763568394002505e-15`
- max_abs_bayesfilter_ad_vs_fd_delta: `0.3314773285976411`
- max_abs_filterflow_ad_vs_fd_delta: `0.3314773285976429`
- finite_difference_policy: `FD diagnostics are recorded per side but do not promote or fail P7.`
- gradient_norm_policy: `Gradient norms explain scale only and are not a pass criterion.`
- runtime_policy: `runtime is explanatory only.`

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
| dirty status | full repo dirty state is recorded in JSON run manifest; unrelated dirty work is not interpreted as P7 evidence |
| command | `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_ot_gradients_tf` |
| validation commands | `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_gradients_2026-06-07.json`; `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_ot_gradients_tf --validate-only`; `git diff --check` on P7 files |
| environment | `/home/chakwong/BayesFilter`; Python `3.11.14`; TensorFlow `2.19.1`; TFP `0.25.0` |
| CPU/GPU status | CPU-only TensorFlow run; pre-import `CUDA_VISIBLE_DEVICES=-1`; visible GPUs `[]` |
| random seeds | no RNG consumed in P7; frozen particles, observations, transition innovations, and masks from P5 |
| dtype | `tf.float64` / JSON dtype `float64` |
| output artifacts | `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_gradients_2026-06-07.json`; `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-gradients-2026-06-07.md`; `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-result-2026-06-07.md` |

## Review State

review_round: 5 final Claude synthesis returned VERDICT: AGREE

open_material_blockers: none identified locally

repair_amendment_required: false

next_allowed_action: begin P8 PRECHECK visibly in current dialogue

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| `PASS_P7_LEDH_PFPF_OT_GRADIENTS_READY_FOR_P8` | all included LEDH-PFPF-OT AD gradients matched locally; SIR was predeclared excluded | all local P7 veto diagnostics clear | shared adapter defects remain possible outside the fixed-branch comparator | begin P8 PRECHECK visibly in the current dialogue | no stochastic-gradient correctness, implementation proof, student claim, GPU claim, production readiness, full-comparison success, or P8 success |

## Post-Run Red Team

Strongest alternative explanation: because the FilterFlow-side adapter is BayesFilter-owned, P7 can miss a shared defect in the contract-formula or shared LEDH/OT path.

What would overturn the local decision: any reviewer finding that an included P5 knob was omitted, that the BayesFilter model side did not depend on the parameterized knob, that the SIR exclusion was not predeclared, or that finite differences were used as a pass gate.

Weakest part of the evidence: P7 is fixed-branch AD-gradient evidence only and does not test stochastic resampling distributions or gradients through discrete branch decisions.
