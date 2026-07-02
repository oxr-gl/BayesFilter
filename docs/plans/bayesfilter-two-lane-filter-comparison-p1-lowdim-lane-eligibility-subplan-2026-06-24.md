# Phase P1 Subplan: Low-Dimensional Lane Eligibility

metadata_date: 2026-06-24
status: DRAFT_PENDING_P0_CLOSEOUT
master_program: docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md
phase: P1
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Freeze the low-dimensional comparison lane as a same-target leaderboard lane and
classify each candidate row as rankable, diagnostic-only, or blocked/status-only.

The key purpose of P1 is to ensure that low-dimensional accuracy/time tables are
honest before any numeric comparison is interpreted.

## Entry Conditions Inherited From Previous Phase

- P0 result status must freeze the leaderboard contract.
- The two-lane master program remains the governing artifact.
- Low-dimensional lane metadata in the target registry and related governance
  JSONs remains available.

## Required Artifacts

- Phase P1 result:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p1-lowdim-lane-eligibility-result-2026-06-24.md`
- Refreshed Phase P2 subplan:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p2-highdim-lane-eligibility-subplan-2026-06-24.md`

## Required Checks, Tests, And Reviews

Focused artifact checks:

```bash
rg -n "comparison_lane_role|lowdim_same_target|cut4|surrogate|diagnostic_only" \
  docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json \
  docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json \
  docs/plans/bayesfilter-two-lane-filter-comparison-p1-lowdim-lane-eligibility-subplan-2026-06-24.md -S
```

Required machine-check checks after P1 implementation work is proposed:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py \
  tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which low-dimensional rows are honest same-target leaderboard rows for SGQF/UKF/CUT4/Zhao-Cui, and which must remain diagnostic-only or blocked? |
| Baseline/comparator | Target registry, deterministic coverage matrix, reference-oracle manifest, and existing low-dimensional row tests. |
| Primary pass criterion | Every candidate low-dimensional row has a durable lane classification and CUT4 appears only where the row is actually allowed and same-target. |
| Veto diagnostics | Low-dimensional row mixes target identity, diagnostic-only row is promoted to rankable, actual transformed SV is merged with KSC surrogate SV, or SGQF score admissibility relies on autodiff-only provenance. |
| Explanatory diagnostics | Existing deterministic coverage statuses, row-class metadata, and focused test outcomes. |
| Not concluded | No high-dimensional claim, no overall repo-wide leaderboard, no family-wide SGQF admission outside the declared low-dimensional rows. |
| Artifact preserving result | P1 result and refreshed P2 subplan. |

## Required Low-Dimensional Row Review

Candidate rankable rows:
- `lgssm_exact_kalman_dim_1_2_3`
- `p44_cubic_additive_gaussian_dim_1_2_3`
- `p44_quadratic_observation_dim_1_2_3`
- `p44_nonlinear_transition_h2_dim_1_2_3`
- `sv_ksc_gaussian_mixture_surrogate_dim_1_2_3`

Required diagnostic-only review row:
- `p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3`

Rows that must not silently enter the low-dimensional rankable table:
- `sv_exact_transformed_actual_nongaussian_dim_1_2_3`
- lower-rung/project-fixture rows that are replaced by high-dimensional source-scope rows

## Stop Conditions

Stop with a blocked P1 result if any candidate row lacks same-target clarity or
if CUT4 eligibility depends on ambiguous target semantics.
