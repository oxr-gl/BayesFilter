# P0 Subplan: Inventory And Rerun Registry

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which old LEDH-PFPF-OT-related tests, runners, result files, and table rows must be rerun, replaced, or classified? |
| Baseline/comparator | P0 quarantine result from the Algorithm 1 source-faithful program plus fresh repository search. |
| Primary pass criterion | A machine-readable rerun registry lists every old lane with `planned_disposition`, required adapters, command template, result paths, and non-claim status. |
| Veto diagnostics | Missing old runner family; old result treated as current evidence; no result path; no route id requirement; no blocked/adapted/N/A vocabulary. |
| Explanatory diagnostics | File counts, old artifact groups, route-id occurrences, and stale result dates. |
| Not concluded | No numerical rerun and no implementation adequacy conclusion. |

## Required Inventory

At minimum, the registry must cover:

- `tests/test_ledh_pfpf_alg1_ukf_tf.py`;
- `run_lgssm_ledh_pfpf_ot_tf.py`;
- `run_lgssm_multiseed_ledh_pfpf_ot_tf.py`;
- `run_range_bearing_ledh_pfpf_ot_tf.py`;
- `run_range_bearing_stress_ledh_pfpf_ot_tf.py`;
- `run_ledh_pfpf_gradient_checks_tf.py`;
- `run_ledh_pfpf_annealed_transport_lgssm_tf.py`;
- `run_filterflow_matched_ledh_pfpf_ot_tf.py`;
- `run_v2_ledh_pfpf_ot_contracts_tf.py`;
- `run_v2_ledh_pfpf_ot_values_tf.py`;
- `run_v2_ledh_pfpf_ot_gradients_tf.py`;
- `run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf.py`;
- `run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf.py`;
- `run_filter_oracle_comparison_p7_integration_closeout.py`;
- `run_filter_oracle_comparison_p8_p44_dpf_blocker_closure_tf.py`;
- `run_ledh_pfpf_source_faithful_repair_tf.py`;
- `scripts/dpf_v2_algorithm_full_comparison_live_gate.py`;
- `run_v2_algorithm_full_comparison_closeout.py`;
- `run_filter_oracle_comparison_p1_lgssm_exact_oracle_tf.py`;
- any other script, gate, closeout, runner, JSON, Markdown report, or plan
  containing `dpf_ledh_pfpf_ot`, `LEDH-PFPF-OT`, `ledh_pfpf_ot`, or
  `ledh_pfpf`;
- JSON/report artifacts beginning `dpf_ledh_pfpf_`,
  `dpf_v2_ledh_pfpf_ot`, or `dpf_filterflow_matched_ledh_pfpf_ot`;
- filter-oracle JSON/report/table rows containing `dpf_ledh_pfpf_ot`.

## Registry Schema Requirements

Each registry row must include:

- `old_lane_id`;
- `old_artifact_paths`;
- `old_route_ids_detected`;
- `planned_disposition`;
- `replacement_phase`;
- `replacement_runner`;
- `planned_result_paths`;
- `required_algorithm1_route_fields`;
- `evidence_route_class`;
- `core_resampling_route`;
- `extension_resampling_route`;
- `comparator_route`;
- `claim_class`;
- `value_scalar`;
- `gradient_scalar`;
- `value_normalization`;
- `gradient_normalization`;
- `value_tolerance`;
- `gradient_tolerance`;
- `certification_band`;
- `minimum_seed_count`;
- `particle_ladder`;
- `primary_promote_statistic`;
- `veto_diagnostics`;
- `allowed_final_statuses`;
- `required_run_manifest_fields`;
- `non_claims`.

Rows without predeclared tolerances or explicit `N/A` reasons cannot be
promoted in P1-P9.

## Planned Commands

Search and registry construction are read-only except for writing the new P0
result and registry artifact.

```bash
rg -n "LEDH-PFPF-OT|dpf_ledh_pfpf_ot|ledh_pfpf_ot|ledh_pfpf" tests experiments scripts docs/plans
rg --files tests experiments/dpf_implementation/tf_tfp/runners experiments/dpf_implementation/reports experiments/dpf_implementation/reports/outputs docs/plans | rg -i "ledh.*pfpf|pfpf.*ledh|dpf_v2_ledh|filterflow_matched_ledh|source_faithful_repair|filter_oracle_comparison_p[5678]|filter-oracle-comparison-p[5678]"
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q
```

Required artifact:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-registry-2026-06-10.json`

## Exit Criteria

P0 passes when the registry is reviewed, the Algorithm 1 guardrail test is
rerun, every old lane has exactly one planned disposition, and no later phase
may add or drop a lane without a reviewed amendment.
