# P0 Result: Governance And LEDH-PFPF-OT Evidence Quarantine

Date: 2026-06-10

## Status

`PASS_P0_QUARANTINE_MANIFEST_READY_FOR_P1`

## Decision

`PASS_P0_QUARANTINE_MANIFEST_READY_FOR_P1`

All previous `LEDH-PFPF-OT`, `ledh_pfpf`, and auxiliary-flow-only
`source-faithful repair` artifacts are quarantined for source-faithful
Li-Coates Algorithm 1 method evidence.

They are not deleted.  They remain historical lineage, regression symptoms,
implementation scaffolding, and old-comparison context.  They must not be cited
as evidence that BayesFilter implements Li-Coates Algorithm 1 until P1-P4 of the
new program pass and P5-P6 publish replacement results.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we make the old LEDH-PFPF-OT evidence impossible to accidentally cite as source-faithful method evidence before rebuilding Algorithm 1? |
| Baseline/comparator | Existing LEDH-PFPF-OT plans, reports, JSON files, runner code, and P8/P44 amendments. |
| Primary pass criterion | A quarantine manifest and supersession note identify old LEDH-PFPF-OT artifacts and state that none may support source-faithful LEDH-PFPF claims. |
| Veto diagnostics | No deletion; no overwriting old result files; the 2026-06-10 auxiliary-flow-only repair is not labelled final source-faithful Algorithm 1 evidence; known artifacts are listed or grouped with explanation. |
| Explanatory diagnostics | Artifact counts and route identifiers only. |
| Not concluded | P0 does not decide the new implementation design and does not run numerical tests. |

## Supersession Rule

Effective for this program:

1. Old LEDH-PFPF-OT rows are discarded for source-faithful method claims.
2. Old rows may be used only as historical lineage, regression symptoms,
   scaffolding candidates, or old-comparison context.
3. New replacement tables must use route identifiers that include all of:
   - `method_generation = li_coates_algorithm1_ukf_covariance_lifecycle`;
   - `flow_source_route = li_coates_2017_algorithm1_ledh_pfpf`;
   - `covariance_route = per_particle_ukf_prediction_update`;
   - `previous_ledh_pfpf_ot_evidence_status = quarantined`.
4. Any future artifact that cites an old LEDH-PFPF-OT row as Algorithm 1
   evidence fails the P4/P6 gates.

## Quarantine Manifest

### Required Explicit Quarantine Items

| Artifact | Role | P0 status | Allowed future use |
| --- | --- | --- | --- |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-plan-2026-06-10.md` | Prior repair plan for auxiliary-flow/determinant topology | `QUARANTINED_AS_INCOMPLETE_ALGORITHM1_EVIDENCE` | Historical diagnosis; source of known failure modes |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-result-2026-06-10.md` | Prior result that called auxiliary-flow repair source-faithful | `SUPERSEDED_FOR_METHOD_EVIDENCE` | Historical lineage; old-vs-new delta only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p8-m3-ledh-pfpf-source-faithful-amendment-2026-06-10.md` | P8 amendment using the auxiliary-flow-only repair route | `SUPERSEDED_FOR_METHOD_EVIDENCE` | Historical amendment; regression symptom |
| `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_source_faithful_repair_tf.py` | Prior auxiliary-flow-only repair runner | `QUARANTINED_AS_SCAFFOLDING_ONLY` | May be read as scaffolding; cannot be final Algorithm 1 path |
| `experiments/dpf_implementation/reports/dpf-ledh-pfpf-source-faithful-repair-2026-06-10.md` | Prior repair report | `SUPERSEDED_FOR_METHOD_EVIDENCE` | Historical lineage; old-vs-new comparison context |
| `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_source_faithful_repair_2026-06-10.json` | Prior repair JSON | `SUPERSEDED_FOR_METHOD_EVIDENCE` | Old-vs-new diagnostic delta only |

### Historical LEDH-PFPF-OT Plan Family

All `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*2026-05-29.md` artifacts are
quarantined as pre-Algorithm-1 historical plans/results.  They include:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-master-program-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p0-scope-default-architecture-plan-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p0-scope-default-architecture-result-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p1-ledh-math-contract-plan-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p1-ledh-math-contract-result-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p2-affine-lgssm-edh-parity-plan-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p2-affine-lgssm-edh-parity-result-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p3-nonlinear-local-linearization-plan-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p3-nonlinear-local-linearization-result-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p4-pfpf-correction-logdet-plan-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p4-pfpf-correction-logdet-result-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p5-tf-tfp-ledh-flow-implementation-plan-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p5-tf-tfp-ledh-flow-implementation-result-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p6-integrated-ledh-pfpf-ot-runner-plan-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p6-integrated-ledh-pfpf-ot-runner-result-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p7-gradient-tape-contract-plan-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p7-gradient-tape-contract-result-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p8-lgssm-validation-plan-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p8-lgssm-validation-result-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p9-range-bearing-validation-plan-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p9-range-bearing-validation-result-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p10-final-audit-handoff-plan-2026-05-29.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p10-final-audit-handoff-result-2026-05-29.md`

Allowed future use: historical lineage and scaffolding inspection only.

### DPF V2 LEDH-PFPF-OT Same-Contract Comparison Family

All `dpf-v2-ledh-pfpf-ot` contract/value/gradient artifacts from 2026-06-07 are
quarantined for source-faithful Algorithm 1 claims.  They may still document
old BayesFilter/FilterFlow same-contract agreement.

| Artifact group | P0 status | Allowed future use |
| --- | --- | --- |
| `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-*2026-06-07.md` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical same-contract contract lane only |
| `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-*2026-06-07.md` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical same-contract value lane only |
| `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-*2026-06-07.md` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical fixed-branch same-contract gradient lane only |
| `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-contracts-2026-06-07.md` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical same-contract context |
| `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-values-2026-06-07.md` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical same-contract context |
| `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-gradients-2026-06-07.md` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical same-contract context |
| `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_contracts_2026-06-07.json` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical same-contract context |
| `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_values_2026-06-07.json` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical same-contract context |
| `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_gradients_2026-06-07.json` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical same-contract context |

### Filter-Oracle Comparison Family With Historical `dpf_ledh_pfpf_ot` Rows

Claude review iteration 1 identified this family as an accidental-citation
risk.  It contains promoted or diagnostic rows with method id
`dpf_ledh_pfpf_ot`, including P44/P8 closure and P6 amended-display artifacts.
Those rows are now explicitly quarantined for source-faithful Algorithm 1
claims.

| Artifact | P0 status | Allowed future use |
| --- | --- | --- |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-subplan-2026-06-08.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical comparison context only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-result-2026-06-08.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical comparison context only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-amended-with-p8-dpf-metrics-2026-06-09.md` | `SUPERSEDED_FOR_LEDHPFPF_METHOD_EVIDENCE` | Old display table only; cannot support Algorithm 1 claims |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p8-p44-dpf-blocker-closure-plan-2026-06-09.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical blocker-closure context only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p8-p44-dpf-blocker-closure-result-2026-06-09.md` | `SUPERSEDED_FOR_LEDHPFPF_METHOD_EVIDENCE` | Historical blocker-closure context only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p8-m3-ledh-pfpf-source-faithful-amendment-2026-06-10.md` | `SUPERSEDED_FOR_LEDHPFPF_METHOD_EVIDENCE` | Historical amendment only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p8-claude-review-ledger-2026-06-09.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical review trail only |
| `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-2026-06-08.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical comparison context only |
| `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p8-p44-dpf-blocker-closure-2026-06-09.md` | `SUPERSEDED_FOR_LEDHPFPF_METHOD_EVIDENCE` | Historical blocker-closure context only |
| `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p8_p44_dpf_blocker_closure_2026-06-09.json` | `SUPERSEDED_FOR_LEDHPFPF_METHOD_EVIDENCE` | Historical old-row data only |
| `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p8_p44_dpf_blocker_closure_review_brief_2026-06-09.json` | `SUPERSEDED_FOR_LEDHPFPF_METHOD_EVIDENCE` | Historical old-row review brief only |
| `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p8_p44_dpf_blocker_closure_tf.py` | `QUARANTINED_AS_OLD_RUNNER_WHERE_LEDHPFPF_ROUTE_APPEARS` | Scaffolding only after audit; not final Algorithm 1 path |

Any table row in this family with method id `dpf_ledh_pfpf_ot` is discarded for
Algorithm 1 method claims, even if that row was previously marked promoted,
diagnostic, repaired, or blocked-closure.  The old row status is not a
source-faithfulness status under the new program.

Claude review iteration 2 showed that the P6/P8/P44 scope above was still too
narrow because P7 closeout artifacts and P6/P7 JSON payloads also surface
historical `dpf_ledh_pfpf_ot` rows.  Therefore the controlling quarantine rule
for this family is broadened:

> Every `docs/plans`, report, JSON output, review ledger, reset memo, and runner
> in the filter-oracle comparison family is quarantined for Algorithm 1
> LEDH-PFPF claims wherever it contains `dpf_ledh_pfpf_ot`, `LEDH-PFPF`, or
> `ledh_pfpf`.  The old filter-oracle program may remain valid for its original
> scoped comparisons, but not as evidence of Li-Coates Algorithm 1
> source-faithful LEDH-PFPF.

Additional explicitly covered filter-oracle artifacts include:

| Artifact | P0 status | Allowed future use |
| --- | --- | --- |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-master-program-2026-06-08.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical filter-oracle program context only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-gated-execution-runbook-2026-06-08.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical execution context only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical execution context only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-reset-memo-2026-06-08.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical reset context only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-result-2026-06-08.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical statistical-closeness context only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-integration-closeout-subplan-2026-06-08.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical closeout context only |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-integration-closeout-result-2026-06-08.md` | `SUPERSEDED_FOR_LEDHPFPF_METHOD_EVIDENCE` | Historical closeout only; cannot summarize Algorithm 1 evidence |
| `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-claude-review-ledger-2026-06-08.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical review trail only |
| `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-2026-06-08.md` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical report only |
| `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p7-integration-closeout-2026-06-08.md` | `SUPERSEDED_FOR_LEDHPFPF_METHOD_EVIDENCE` | Historical closeout report only |
| `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p5_dpf_statistical_closeness_2026-06-08.json` | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` | Historical JSON only |
| `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json` | `SUPERSEDED_FOR_LEDHPFPF_METHOD_EVIDENCE` | Historical JSON only |
| `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p7_integration_closeout_2026-06-08.json` | `SUPERSEDED_FOR_LEDHPFPF_METHOD_EVIDENCE` | Historical closeout JSON only |
| `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf.py` | `QUARANTINED_AS_OLD_RUNNER_WHERE_LEDHPFPF_ROUTE_APPEARS` | Scaffolding only after audit |
| `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf.py` | `QUARANTINED_AS_OLD_RUNNER_WHERE_LEDHPFPF_ROUTE_APPEARS` | Scaffolding only after audit |
| `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p7_integration_closeout.py` | `QUARANTINED_AS_OLD_RUNNER_WHERE_LEDHPFPF_ROUTE_APPEARS` | Scaffolding only after audit |

Inventory broadening command:

```bash
rg --files docs/plans experiments/dpf_implementation/reports experiments/dpf_implementation/reports/outputs experiments/dpf_implementation/tf_tfp/runners | rg -i 'filter-oracle-comparison|dpf_filter_oracle_comparison|run_filter_oracle_comparison'
rg -l "dpf_ledh_pfpf_ot|LEDH-PFPF|ledh_pfpf" docs/plans experiments/dpf_implementation/reports experiments/dpf_implementation/reports/outputs experiments/dpf_implementation/tf_tfp/runners | rg -i 'filter-oracle-comparison|dpf_filter_oracle_comparison|run_filter_oracle_comparison'
rg -n "dpf_ledh_pfpf_ot|LEDH-PFPF|ledh_pfpf" docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-integration-closeout-result-2026-06-08.md experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p7_integration_closeout_2026-06-08.json
```

### Historical Runner And Report Scaffolding

| Artifact | P0 status | Allowed future use |
| --- | --- | --- |
| `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py` | `QUARANTINED_AS_OLD_IMPLEMENTATION_PATH` | Scaffolding only after audit; not final Algorithm 1 path |
| `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_ledh_pfpf_ot_tf.py` | `QUARANTINED_AS_OLD_RUNNER` | Fixture/reference scaffolding only |
| `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_multiseed_ledh_pfpf_ot_tf.py` | `QUARANTINED_AS_OLD_RUNNER` | Fixture/reference scaffolding only |
| `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_ledh_pfpf_ot_tf.py` | `QUARANTINED_AS_OLD_RUNNER` | Fixture/reference scaffolding only |
| `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_stress_ledh_pfpf_ot_tf.py` | `QUARANTINED_AS_OLD_RUNNER` | Fixture/reference scaffolding only |
| `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_gradient_checks_tf.py` | `QUARANTINED_AS_OLD_RUNNER` | Gradient-check scaffolding only |
| `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_annealed_transport_lgssm_tf.py` | `QUARANTINED_AS_OLD_RUNNER` | Historical comparison only |
| `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_matched_ledh_pfpf_ot_tf.py` | `QUARANTINED_AS_OLD_RUNNER` | FilterFlow-side old comparison only |
| `experiments/dpf_implementation/tf_tfp/runners/run_v2_ledh_pfpf_ot_contracts_tf.py` | `QUARANTINED_AS_OLD_RUNNER` | Old same-contract context only |
| `experiments/dpf_implementation/tf_tfp/runners/run_v2_ledh_pfpf_ot_values_tf.py` | `QUARANTINED_AS_OLD_RUNNER` | Old same-contract context only |
| `experiments/dpf_implementation/tf_tfp/runners/run_v2_ledh_pfpf_ot_gradients_tf.py` | `QUARANTINED_AS_OLD_RUNNER` | Old same-contract context only |
| `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-lgssm-result-2026-05-29.md` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical result only |
| `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-range-bearing-result-2026-05-29.md` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical result only |
| `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-gradient-check-result-2026-05-29.md` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical result only |
| `experiments/dpf_implementation/reports/dpf-ledh-pfpf-annealed-transport-lgssm-2026-05-31.md` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical result only |
| `experiments/dpf_implementation/reports/dpf-filterflow-matched-ledh-pfpf-ot-2026-05-31.md` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical FilterFlow context only |

Corresponding JSON outputs under
`experiments/dpf_implementation/reports/outputs/` with names beginning
`dpf_ledh_pfpf_`, `dpf_filterflow_matched_ledh_pfpf_ot`, or
`dpf_v2_ledh_pfpf_ot` are also quarantined for Algorithm 1 claims.

### New Li-Coates Algorithm 1 Program Artifacts

The newly created `li-coates-alg1-ukf-source-faithful` master program, runbook,
subplans, review ledger, execution plan, execution ledger, and this P0 result
are not quarantined.  They are the active replacement program.  They do not yet
constitute implementation or performance evidence until their phase gates pass.

## Inventory Commands

Commands run visibly in the current dialogue:

```bash
sed -n '1,180p' docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-subplan-2026-06-10.md
sed -n '1,260p' docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-gated-overnight-execution-plan-2026-06-10.md
git status --short
rg -n "LEDH-PFPF|ledh_pfpf|dpf_ledh_pfpf_ot|dpf-v2-ledh-pfpf-ot|source_faithful_scalar_auxiliary_ledh_pfpf|li_coates_2017_algorithm_pf_pf_ledh_auxiliary_flow" docs/plans experiments/dpf_implementation tests scripts
rg --files docs/plans | rg -i 'ledh.*pfpf|pfpf.*ledh|dpf-v2.*ledh|filter-oracle.*ledh|li-coates-alg1'
rg --files experiments/dpf_implementation | rg -i 'ledh.*pfpf|pfpf.*ledh|dpf_v2_ledh|filterflow_matched_ledh|source_faithful_repair'
rg --files tests scripts | rg -i 'ledh.*pfpf|pfpf.*ledh|dpf_v2.*ledh'
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
rg --files docs/plans experiments/dpf_implementation/reports experiments/dpf_implementation/reports/outputs | rg -i 'filter-oracle-comparison.*(p6|p8|p44)|dpf_filter_oracle_comparison_p8_p44|p8-p44-dpf-blocker|p6-amended-with-p8'
rg -n "dpf_ledh_pfpf_ot|LEDH-PFPF|ledh_pfpf" docs/plans/bayesfilter-dpf-filter-oracle-comparison-p8-p44-dpf-blocker-closure-result-2026-06-09.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-amended-with-p8-dpf-metrics-2026-06-09.md experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p8_p44_dpf_blocker_closure_review_brief_2026-06-09.json experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p8_p44_dpf_blocker_closure_2026-06-09.json
```

## Run Manifest

| Field | Value |
| --- | --- |
| git branch | `main` |
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| phase | `P0` |
| execution mode | visible current-dialogue execution |
| detached execution | `False` |
| CPU/GPU status | no TensorFlow/GPU command run |
| random seeds | `N/A` |
| output artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-result-2026-06-10.md` |
| execution ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md` |
| plan | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-subplan-2026-06-10.md` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `P0_QUARANTINE_MANIFEST_READY_FOR_REVIEW` | quarantine manifest and supersession rule written | no deletion, no overwrite, old repair explicitly superseded | inventory is broad and grouped; future P6 should re-check before closeout | Claude read-only P0 review | no new implementation, no numerical rerun, no Algorithm 1 faithfulness pass |

## Claude Review

Iteration 1 returned `VERDICT: REVISE` because the filter-oracle comparison
family with historical `dpf_ledh_pfpf_ot` rows was not explicitly quarantined.
This revision adds that family and broadens the row-level supersession rule.

Iteration 2 returned `VERDICT: REVISE` because the filter-oracle quarantine was
still too narrow and missed P6 JSON and P7 closeout artifacts.  This revision
adds a controlling family-wide quarantine rule and explicitly covers P5/P6/P7
filter-oracle artifacts and runners where `dpf_ledh_pfpf_ot` appears.

Send this revised result artifact to Claude read-only review and continue only
after `VERDICT: AGREE`, or repair under the visible repair loop.

Iteration 3 returned `VERDICT: AGREE`.  P0 passes and the execution can advance
to P1.
