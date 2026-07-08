# Phase 5 Result: Nonlinear Adapter Admission Inventory

Date: 2026-07-03

Status: `ALL_NONLINEAR_ROWS_BLOCKED_OR_TARGET_MISMATCHED`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | No nonlinear row is adapter-ready for same-target LEDH score repair. |
| Primary criterion status | Failed: each nonlinear row is blocked, target-mismatched, or only scoped-diagnostic. |
| Veto diagnostic status | No scoped diagnostic was promoted to a full observed-data/filtering leaderboard score row. |
| Main uncertainty | Whether any future same-target LEDH adapter can be built for these rows without changing the target or using a blocked route. |
| Next justified action | Mark Phase 6 as skipped/blocked unless a new adapter target is explicitly approved. |
| Not concluded | No nonlinear LEDH score admission, no HMC readiness, no source-faithfulness claim, no scientific superiority. |

## Row Classification

| Row | Classification | Reason |
| --- | --- | --- |
| `zhao_cui_sv_actual_nongaussian_T1000` | `adapter_missing` | The current LEDH-inclusive leaderboard marks the LEDH route blocked because no reviewed current GPU/XLA adapter proves the exact requested target. |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `target_mismatch` | The row is explicitly a KSC Gaussian-mixture surrogate target, not exact native SV likelihood. |
| `zhao_cui_predator_prey_T20` | `adapter_missing` | The current fixed-SGQF/LEDH surfaces do not provide a reviewed same-target T20 observed-data adapter. |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `adapter_missing` | The exact source-row evaluator is missing; native-oracle, precursor, auxiliary, actual-SV, and KSC evidence are not admission evidence. |

## Evidence

Actual SV:

- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`
  records the LEDH row as blocked:
  `value_status = blocked_no_reviewed_current_gpu_xla_ledh_row_adapter`.

KSC SV:

- The leaderboard treats it as a declared KSC Gaussian-mixture surrogate row,
  not an exact native SV likelihood row.
- The parameterized SIR scoped component row is separate and must not be used
  as evidence for this SV target.

Predator-prey:

- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py` records the LEDH
  route as blocked because no reviewed current GPU/XLA adapter proves the exact
  requested target.
- The fixed-SGQF route is blocked by target alignment.

Generalized SV:

- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py` records the row as
  blocked because no reviewed exact-row evaluator exists and native-oracle or
  precursor evidence is not admission evidence.

## Plain Scientific Classification

None of the nonlinear rows can be advanced to LEDH score admission on the
current evidence.  In particular:

- actual SV needs a reviewed same-target LEDH adapter;
- KSC is a surrogate target and not the exact native SV target;
- predator-prey lacks a reviewed same-target adapter;
- generalized SV lacks an exact source-row evaluator.

## Checks Run

- Inspected the July 3 LEDH-inclusive leaderboard row status JSON.
- Inspected the row-admission ledger and leaderboard implementation for the
  four nonlinear rows.
- Preserved the Phase 3 LGSSM blocker and Phase 4 fixed SIR classification.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded for this audit-only classification. |
| Commands | `rg`, `python` JSON inspection, `nl`, `sed`. |
| Environment | Local repository audit; no GPU or TensorFlow execution required. |
| CPU/GPU status | GPU not used. |
| Output artifacts | This result file; refreshed Phase 6 subplan. |
| Plan file | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase6-nonlinear-score-repair-subplan-2026-07-03.md` |

## Phase 6 Handoff

Phase 6 should be marked skipped or blocked unless a new, explicitly reviewed
same-target adapter is approved.  The current program should carry forward:

- Phase 3 LGSSM score blocker:
  `blocked_total_transport_vjp_needs_no_tape_repair`;
- Phase 4 fixed SIR classification:
  `no_free_theta_value_only`;
- Phase 5 nonlinear classification:
  all four nonlinear rows blocked, target-mismatched, or scoped-only.
