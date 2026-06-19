# Master Program: Fixed-SGQF Broader Nonlinear Comparison

metadata_date: 2026-06-16
program_id: fixed-sgqf-broader-nonlinear-comparison
status: EXECUTION_READY

## Date

2026-06-16

## Status

`EXECUTION_READY`

## Purpose

This program governs the placement of the repaired fixed-SGQF lane into the
broader repo-wide nonlinear comparison ecosystem, using the existing target
registries, deterministic-coverage matrices, preflight matrix, and numeric
result ledgers as the backbone.

The goal is not to create a parallel benchmark stream. The goal is to say
exactly where fixed SGQF belongs in the existing repo-wide deterministic
comparison roster, where it is admitted, where it is blocked, and why.

## Governing Registries

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json`

## Existing Broader Comparison Backbone

For eventual literature-facing leaderboard studies, this program inherits the
repo's **source-paper scope contract** rather than the older 12-row diagnostic
roster.

That means the promoted literature-backed family set is:
- `benchmark_lgssm_exact_oracle_m3_T50`
- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
- `zhao_cui_spatial_sir_austria_j9_T20`
- `zhao_cui_predator_prey_T20`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

The following rows remain available only as engineering/debugging evidence and
are **not** part of the final literature-backed leaderboard scope:
- `p44_cubic_additive_gaussian_dim_1_2_3`
- `p44_quadratic_observation_dim_1_2_3`
- `p44_nonlinear_transition_h2_dim_1_2_3`
- `p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3`

The fixed-SGQF lane should therefore be evaluated against the literature-backed
roster first, while keeping the P44 rows available only as local debugging or
engineering fixtures.

## Fixed-SGQF Admission Rules

### Admit exact
Allowed when:
- the family is same-target compatible with the current fixed-SGQF lane,
- fixed SGQF can evaluate the declared value scalar exactly within its own lane
  semantics,
- reference policy remains consistent with the existing registry.

### Admit dense-reference only
Allowed when:
- fixed SGQF is same-target compatible with a row family that already uses a
  dense numerical reference policy,
- the row is clearly labeled as dense-reference only, not exact.

### Diagnostic-only
Allowed when:
- fixed SGQF can be run in a way that is informative but not benchmark-ranked.

### Blocked
Required when:
- the family would require a richer state+innovation SGQF lane,
- or target semantics differ from the current additive-state lane.

## Evidence Contract

Question:

Where does the repaired fixed-SGQF lane fit into the broader repo-wide nonlinear
comparison ecosystem, and which model families can it enter honestly under the
current lane semantics?

Primary pass criterion:
- fixed SGQF is admitted into the broader deterministic comparison backbone only
  where same-target compatible,
- blocked families are explicit rather than silently omitted,
- result artifacts show a truthful repo-wide placement for fixed SGQF.

Veto diagnostics:
- a blocked family is admitted without same-target justification,
- exact/dense/diagnostic semantics are mixed in one row family,
- broader result notes imply universal compatibility.

Explanatory-only diagnostics:
- number of admitted families,
- number of blocked families,
- which registry artifacts were updated,
- where fixed SGQF remains outside scope.

## Phase Map

| Phase | Subplan | Purpose | Required outcome token |
| --- | --- | --- | --- |
| P0 | `docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-p0-governance-and-target-scan-subplan-2026-06-16.md` | inventory repo-wide model families and classify SGQF admission candidates | `PASS_P0_FIXED_SGQF_BROADER_SCAN_COMPLETE` |
| P1 | `docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-p1-deterministic-lane-admission-subplan-2026-06-16.md` | thread fixed SGQF into the broader deterministic admission logic | `PASS_P1_FIXED_SGQF_DETERMINISTIC_LANE_CLASSIFIED` |
| P2 | `docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-p2-p44-lowdim-value-panel-subplan-2026-06-16.md` | decide and, if admissible, place fixed SGQF into low-dimensional deterministic P44 rows | `PASS_P2_FIXED_SGQF_P44_SCOPE_CLASSIFIED` |
| P3 | `docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-p3-lgssm-and-affine-anchor-subplan-2026-06-16.md` | anchor repo-wide admission on LGSSM / affine exact rows | `PASS_P3_FIXED_SGQF_AFFINE_ANCHOR_CONFIRMED` |
| P4 | `docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-p4-blocked-family-ledger-subplan-2026-06-16.md` | write explicit blocked-family reasons for incompatible families | `PASS_P4_FIXED_SGQF_BLOCKED_FAMILY_LEDGER_WRITTEN` |
| P5 | `docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-p5-closeout-subplan-2026-06-16.md` | summarize where fixed SGQF is admitted repo-wide and where it is not | `PASS_P5_FIXED_SGQF_BROADER_COMPARISON_CLOSEOUT` |

## Artifact Contract

The program should prefer updating or extending the existing broader registry and
coverage artifacts rather than creating a disconnected scoreboard.

At minimum it must write:
- this master program,
- the phase subplans,
- a closeout artifact that explicitly lists admitted and blocked families.

## Stop Rules

Stop if:
1. a family cannot be admitted without changing target semantics;
2. fixed SGQF would have to be described as exact where it is only diagnostic or
   approximate;
3. a blocked family reason cannot be expressed clearly.

## Exit Criteria

The program exits successfully only if:
- fixed SGQF’s repo-wide placement is explicit,
- admitted families have same-target justification,
- blocked families have stable reasons,
- and no artifact implies broader compatibility than the evidence supports.
