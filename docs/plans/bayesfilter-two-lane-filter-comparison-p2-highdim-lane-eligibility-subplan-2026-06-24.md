# Phase P2 Subplan: High-Dimensional Lane Eligibility

metadata_date: 2026-06-24
status: DRAFT_PENDING_P1_CLOSEOUT
master_program: docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md
phase: P2
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Freeze the high-dimensional / source-scope comparison lane and classify each row
as rankable, status-only, or blocked for the leaderboard program.

The key purpose of P2 is to prevent high-dimensional tables from becoming a
misleading mixed roster where CUT4 leaks in or blocked SGQF rows appear to be
fairly ranked.

## Entry Conditions Inherited From Previous Phase

- P1 result must exist and freeze the low-dimensional lane cleanly.
- The source-paper scope contract remains the governing row list for the
  high-dimensional lane.

## Required Artifacts

- Phase P2 result:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p2-highdim-lane-eligibility-result-2026-06-24.md`
- Refreshed Phase P3 subplan:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p3-artifact-schema-and-emitter-subplan-2026-06-24.md`

## Required Checks, Tests, And Reviews

Focused artifact checks:

```bash
rg -n "source_scope_row_ids|excluded_algorithm_ids|cut4|blocked_fixed_sgqf|actual_and_surrogate_sv_must_remain_separate" \
  docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json \
  docs/plans/bayesfilter-filtering-value-gradient-benchmark-gradient-semantics-2026-06-10.json \
  docs/plans/bayesfilter-two-lane-filter-comparison-p2-highdim-lane-eligibility-subplan-2026-06-24.md -S
```

Focused machine-check tests when phase work is implemented:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py \
  tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which source-scope rows are honestly comparable in the high-dimensional lane, and which must remain blocked or status-only? |
| Baseline/comparator | Source-paper scope contract, gradient semantics policy, and row-specific route/readiness constraints. |
| Primary pass criterion | The high-dimensional lane has an explicit comparison roster without CUT4, with actual-vs-surrogate SV separation, and with blocked SGQF rows preserved visibly. |
| Veto diagnostics | CUT4 appears in the high-dimensional comparison lane, actual transformed SV is merged with KSC surrogate SV, or blocked SGQF rows disappear into omission. |
| Explanatory diagnostics | Route-readiness status, source-scope row list, blocker row list, and focused test outcomes. |
| Not concluded | No numeric ranking yet, no source-paper superiority claim, no SGQF broad family admission. |
| Artifact preserving result | P2 result and refreshed P3 subplan. |

## Required High-Dimensional Row Review

Source-scope rows:
- `benchmark_lgssm_exact_oracle_m3_T50`
- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
- `zhao_cui_spatial_sir_austria_j9_T20`
- `zhao_cui_predator_prey_T20`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

Blocked-by-default SGQF high-dimensional rows unless a new reviewed same-target route exists:
- actual transformed SV
- spatial SIR
- predator-prey
- generalized SV

## Stop Conditions

Stop with a blocked P2 result if the high-dimensional lane still implies CUT4
eligibility or if actual and surrogate SV cannot be kept separated in the
planned tables.
