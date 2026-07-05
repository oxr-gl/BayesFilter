# Phase 6 Result: Nonlinear Score Repair Skipped

Date: 2026-07-03

Status: `SKIPPED_NO_ADMITTED_NONLINEAR_ROWS`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Do not run nonlinear LEDH score repair in this program. |
| Primary criterion status | Passed as a skip/block decision: Phase 5 admitted no nonlinear same-target adapter-ready rows. |
| Veto diagnostic status | No nonlinear score row was promoted; no scoped component diagnostic was used as a full observed-data score. |
| Main uncertainty | Whether future same-target LEDH adapters can be built for actual SV, predator-prey, or generalized SV without changing the target. |
| Next justified action | Run Phase 7 as a no-op leaderboard merge that preserves all existing LEDH score blockers. |
| Not concluded | No nonlinear LEDH score correctness, no HMC readiness, no source-faithfulness claim, no scientific superiority. |

## Evidence Contract Result

Question:

- Can Phase 6 run nonlinear LEDH score repair under the current evidence?

Answer:

- No.  Phase 5 classified every nonlinear row as blocked, target-mismatched, or
  scoped-only.  Therefore there is no admissible nonlinear row for Phase 6 to
  execute.

## Carried-Forward Row Statuses

| Row | Phase 6 status | Reason |
| --- | --- | --- |
| `zhao_cui_sv_actual_nongaussian_T1000` | `blocked_adapter_missing` | No reviewed current GPU/XLA LEDH adapter proves the exact requested actual-SV row target. |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `blocked_target_mismatch` | The row is a KSC Gaussian-mixture surrogate target, not the exact native SV likelihood. |
| `zhao_cui_predator_prey_T20` | `blocked_adapter_missing` | No reviewed same-target T20 observed-data LEDH adapter is available. |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked_adapter_missing` | The exact source-row evaluator is missing; adjacent SV evidence is not source-row admission evidence. |

## Preserved Prior Statuses

- LGSSM remains blocked for score admission by
  `blocked_total_transport_vjp_needs_no_tape_repair`.
- Fixed spatial SIR main row remains `no_free_theta_value_only`.
- Parameterized SIR log-scale row remains scoped component evidence only, not a
  full observed-data filtering score row.

## Checks Run

- Phase 5 adapter-admission JSON check: passed.
- Phase 6 skipped-subplan content check: passed.
- `git diff --check` for Phase 5/6 touched artifacts: passed before this
  result was written.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded for this audit-only skipped phase. |
| Commands | `python` JSON/content checks, `rg`, `sed`, `git diff --check`. |
| Environment | Local repository audit; no TensorFlow/GPU execution. |
| CPU/GPU status | GPU not used because Phase 6 has no admitted row to run. |
| Data version | July 3 LEDH-inclusive leaderboard plus Phase 5 adapter-admission ledger. |
| Random seeds | N/A. |
| Wall time | N/A. |
| Output artifacts | This result file; refreshed Phase 7 subplan. |
| Plan file | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase6-nonlinear-score-repair-subplan-2026-07-03.md` |

## Post-Run Red-Team Note

Strongest alternative explanation:

- One might argue that a blocked nonlinear row should still be attempted as an
  exploratory diagnostic.  That would not answer the leaderboard score question
  because the phase lacks a same-target adapter-ready row.

What would overturn this blocker:

- A reviewed same-target LEDH adapter for a nonlinear row, followed by a new
  subplan with exact or same-scalar finite-difference score evidence.

Weakest part of the evidence:

- Phase 6 does not test new nonlinear code.  It only enforces the admission
  boundary from Phase 5.

## Phase 7 Handoff

Phase 7 should be a no-op merge.  The existing July 3 LEDH-inclusive leaderboard
already reflects the correct score state:

- no LEDH score row is admitted;
- LGSSM and fixed SIR are value-only for LEDH;
- nonlinear LEDH rows remain blocked or scoped-only.
