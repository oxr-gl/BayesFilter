# Phase Result: Two-Lane Comparison P1 Low-Dimensional Lane Eligibility

metadata_date: 2026-06-24
plan_reference: `docs/plans/bayesfilter-two-lane-filter-comparison-p1-lowdim-lane-eligibility-subplan-2026-06-24.md`
master_program: `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
status: PASS_P1_LOWDIM_LANE_ELIGIBILITY_FROZEN

## Phase Objective

Freeze the low-dimensional same-target leaderboard lane and classify candidate
rows as rankable, diagnostic-only, or excluded from the rankable lowdim table.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | answered: the low-dimensional lane now has an explicit rankable row set and explicit exclusions |
| Primary criterion status | satisfied |
| Veto diagnostic status | no actual-vs-surrogate SV mixing; no CUT4 leakage beyond lowdim; no diagnostic-only row promoted |
| Main uncertainty | later execution still needs a durable lowdim timing harness that covers the intended algorithms honestly |
| Next justified action | freeze the high-dimensional lane in P2 |
| What is not concluded | no numeric lowdim leaderboard yet |

## Frozen Low-Dimensional Rankable Rows

Rankable low-dimensional rows:
- `lgssm_exact_kalman_dim_1_2_3`
- `p44_cubic_additive_gaussian_dim_1_2_3`
- `p44_quadratic_observation_dim_1_2_3`
- `p44_nonlinear_transition_h2_dim_1_2_3`
- `sv_ksc_gaussian_mixture_surrogate_dim_1_2_3`

Diagnostic-only low-dimensional row:
- `p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3`

Explicit non-rankable low-dimensional row:
- `sv_exact_transformed_actual_nongaussian_dim_1_2_3`

## Allowed Low-Dimensional Algorithms

- `fixed_sgqf`
- `ukf`
- `cut4`
- `zhao_cui_scalar_or_multistate`

## Audit Of Result Just Produced

P1 passes the skeptical audit because it preserves same-target rankability, does
not use actual transformed SV as a surrogate for KSC evidence, and leaves the
H4 nonlinear-transition row diagnostic-only.

## Next-Phase Review

P2 may proceed unchanged. The high-dimensional lane still needs explicit
row-by-row blocker preservation and CUT4 exclusion.

## Nonclaims

- No low-dimensional timing result is produced yet.
- No low-dimensional winner is claimed.
