# Phase 1 Result: Row Score Inventory

Date: 2026-07-03

Status: `PASS_INVENTORY`

## Decision

Phase 1 passes.  The row inventory is written, and no LEDH score row is
promoted.

The first valid score-repair target is:

- `benchmark_lgssm_exact_oracle_m3_T50`

because it already has same-target LEDH value evidence and an exact Kalman
value/score comparator.

## Inventory Artifact

- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase1-row-score-inventory-2026-07-03.json`

## Row Classifications

| Row | Current LEDH value status | Current LEDH score status | Phase 1 classification | Next action |
| --- | --- | --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | `executed_same_target_value` | `blocked_score_same_target_total_derivative_not_implemented` | `ready_for_score_repair` | Phase 2 same-target LGSSM total-derivative score repair. |
| `zhao_cui_sv_actual_nongaussian_T1000` | `blocked_no_reviewed_current_gpu_xla_ledh_row_adapter` | `blocked_score` | `needs_adapter` | Phase 5 same-target adapter admission. |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `blocked_no_ledh_ksc_row_adapter` | `blocked_score` | `needs_adapter` | Phase 5 KSC adapter admission. |
| `zhao_cui_spatial_sir_austria_j9_T20` | `executed_fixed_sir_value_only` | `blocked_score_for_full_leaderboard_row` | `no_free_theta` | Phase 4 target decision; do not invent a score. |
| `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` | `scoped_or_diagnostic_only` | `scoped_score_diagnostic_not_full_observed_data_score` | `scoped_diagnostic_only` | Keep scoped unless a separate reviewed target changes the row. |
| `zhao_cui_predator_prey_T20` | `blocked_no_reviewed_current_gpu_xla_ledh_row_adapter` | `blocked_score` | `needs_adapter` | Phase 5 same-target adapter admission. |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked_no_reviewed_same_target_ledh_row_adapter` | `blocked_score` | `needs_adapter` | Phase 5 same-target adapter admission. |

## LGSSM Phase 2 Handoff

The Phase 2 target is the actual leaderboard row:

- row id: `benchmark_lgssm_exact_oracle_m3_T50`;
- state dimension: `3`;
- observation dimension: `3`;
- time steps: `50`;
- dataset seed: `81100`;
- theta: `[0.72, 0.55, 0.35, 0.35, 0.45]`;
- exact total log likelihood: `-136.0759748579247`;
- exact average log likelihood: `-2.721519497158494`;
- exact score:
  `[5.655446876369503, -3.83505645148858, 0.3023616684162056, -1.9171806685717399, 4.354265155260018]`.

Contract E remains forbidden as same-target leaderboard score evidence because
it is a different LGSSM target.

## Evidence Contract Result

| Field | Status |
| --- | --- |
| Question | Which rows have enough target definition and comparator evidence to begin LEDH score repair? |
| Primary criterion | Passed: every highdim row has a score-target classification. |
| Veto diagnostics | No missing row; no diagnostic row promoted; no value-only evidence promoted to score. |
| Explanatory diagnostics | Existing LEDH value MCSE and adapter blockers are preserved in the source leaderboard. |
| Not concluded | No score implementation correctness, no new score admission, no HMC readiness. |

## Local Checks

JSON parse and row-count check:

```text
phase1_inventory_json_ok rows=7
```

Source leaderboard content check:

```text
source_leaderboard_ledh_rows_ok rows=7
```

Phase 2 handoff check:

```text
phase2_handoff_ok
```

## Review Of Phase 2 Subplan

Codex reviewed the Phase 2 subplan against the Phase 1 inventory.

Result: `PASS_LOCAL_SUBPLAN_REVIEW`.

Phase 2 has the right target metadata, requires exact Kalman comparison, blocks
Contract E, requires trusted GPU/XLA/TF32 evidence for material runs, and keeps
tiny smokes separate from leaderboard admission.

## Next-Phase Handoff

Advance to Phase 2 with this boundary:

- implement or locate a same-target LEDH score route for
  `benchmark_lgssm_exact_oracle_m3_T50`;
- compare the total derivative against the exact Kalman score;
- do not claim score admission from Contract E, a CPU-only diagnostic, a tiny
  smoke alone, or a stopped partial derivative.

## Nonclaims

- Phase 1 does not change the leaderboard.
- Phase 1 does not admit any LEDH score row.
- Phase 1 does not prove any nonlinear adapter exists.
- Phase 1 does not certify HMC readiness.
