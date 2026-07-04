# Phase 1 Result: Row Admission And Adapter Inventory

Date: 2026-07-03

Status: `PASSED_PHASE1_LEDGER_READY_PENDING_CLAUDE_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Admit only the LGSSM LEDH value arm and fixed spatial SIR LEDH value arm as initial execution candidates; keep all LEDH score arms blocked until total-derivative gates pass, and keep all other requested rows explicit as scoped or blocked until a reviewed same-target adapter exists. |
| Primary criterion | Passed: every requested row appears in the row admission ledger with value status, score status, target status, and next action. |
| Veto diagnostics | Passed locally: no requested row is silently omitted; parameterized SIR remains scoped; no row is marked `executed_value_score`; legacy callback existence is not treated as current GPU/XLA leaderboard admission. |
| Main uncertainty | Whether Phase 2 should implement more row adapters now or emit blocked rows first and run the executable LGSSM/SIR subset. |
| Next justified action | Phase 2 should implement the LEDH-inclusive runner schema with all rows emitted and only LGSSM/SIR in the initial executable scope. |
| Not concluded | No LEDH value correctness, score correctness, all-model readiness, runtime superiority, HMC readiness, posterior correctness, or scientific superiority. |

## Ledger

Row admission ledger:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json`

## Row Summary

| Row | LEDH Phase 1 decision | Value status | Score status |
| --- | --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | in scope for later full value+score only after gates | candidate value arm; needs Phase 2 runner wiring and Phase 3 value gate | blocked until Kalman or same-target FD gate |
| `zhao_cui_sv_actual_nongaussian_T1000` | blocked | no reviewed current GPU/XLA LEDH row adapter | blocked |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | blocked | no reviewed KSC LEDH row adapter | blocked |
| `zhao_cui_spatial_sir_austria_j9_T20` | fixed spatial SIR value arm candidate only | existing P8j/P8o streaming GPU/TF32 value route; must be carried forward explicitly or rerun in Phase 4 | blocked for full leaderboard score |
| `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` | scoped component row | diagnostic/scoped only | diagnostic/scoped only, not full observed-data score |
| `zhao_cui_predator_prey_T20` | blocked | no reviewed current GPU/XLA LEDH row adapter | blocked |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | blocked | no reviewed same-target LEDH row adapter | blocked |

## Evidence Used

- The July 3 highdim leaderboard excludes LEDH/PFPF-OT and DPF rows.
- The current highdim runner row set is the requested row set.
- `benchmark_p8j_tf32_batched_actual_sir.py` contains the current streaming
  fixed SIR LEDH value route for the fixed spatial SIR observed-data value arm,
  not the parameterized SIR component row.
- The P8o SIR d18 cell selects `N=10000` as value-only evidence and explicitly
  forbids gradient/HMC/posterior claims.
- `benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py` and the
  P8d LGSSM callbacks show a viable LGSSM value route, but Phase 2 must wire the
  actual highdim row before execution.
- Legacy P8d callbacks exist for actual SV, predator-prey, and generalized SV,
  but Phase 1 does not admit them as current GPU/XLA LEDH leaderboard rows
  without a reviewed same-target adapter.

## Phase 2 Handoff

Phase 2 must build a separate LEDH-inclusive runner that:

- emits every requested row;
- preserves `full`, `scoped`, and `blocked` statuses;
- uses comparator mode `frozen_non_ledh_baseline_plus_fresh_ledh`;
- disables runtime cross-ranking against frozen non-LEDH rows;
- initially wires only the LGSSM value dry-run/tiny value arm and fixed spatial
  SIR value arm unless Phase 2 adds and reviews further same-target adapters
  before execution;
- emits explicit blocked/scoped reasons for every non-executed row and every
  non-executed score arm;
- keeps score admission separate from value admission.

## Checks Run

- JSON parse check for the ledger: passed.
- Row coverage check against the requested seven-row set: passed.
- Comparator mode check: passed, `runtime_cross_ranking_allowed=false`.
- Required status field check for every row: passed.
- `git diff --check` on Phase 1 ledger/result and Phase 2 subplan: passed.
- Phase 2 subplan refresh: completed.
- Claude read-only review of Phase 1 result and Phase 2 handoff: pending.
