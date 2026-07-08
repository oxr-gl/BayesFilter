# Phase 4 Subplan: Manual No-Tape Score Implementation

metadata_date: 2026-07-06
status: DRAFT_AFTER_PHASE3_PARTIAL_ADMISSION
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 4

## Phase Objective

Implement or confirm analytical/manual total-derivative scores only for rows
whose same-target forward likelihood scalar was admitted in Phase 3.

## Entry Conditions Inherited From Previous Phase

- Phase 3 admitted value rows:
  - `benchmark_lgssm_exact_oracle_m3_T50`
  - `zhao_cui_spatial_sir_austria_j9_T20`
- Phase 3 blocked value rows:
  - `zhao_cui_sv_actual_nongaussian_T1000`
  - `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
  - `zhao_cui_predator_prey_T20`
  - `zhao_cui_generalized_sv_synthetic_from_estimated_values`
- Score work is forbidden for Phase 3 blocked rows.
- Fixed SIR score must use the amended 3D `sir_log_scale_theta` contract.
- Scoped parameterized-SIR diagnostic score may be used only as a diagnostic
  reference; it must not substitute for fixed full-row score admission.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-ledh-same-target-forward-score-phase4-manual-score-implementation-result-2026-07-06.md`
- Fixed-SIR score repair notes or blocker result.
- Static no-autodiff audit result.
- Tiny same-scalar finite-difference artifacts.
- Refreshed Phase 5 per-model score/memory test subplan listing only rows
  whose tiny no-tape score checks passed.

## Row Order

1. LGSSM:
   - confirm existing compact forward-sensitivity no-autodiff score remains the
     default route;
   - do not reopen historical manual-reverse route as default.
2. Fixed SIR:
   - adapt the no-tape total VJP from the scoped parameterized SIR diagnostic
     to the full fixed SIR row and amended `sir_log_scale_theta`;
   - ensure value and score use the same target scalar and same LEDH transport
     algorithm;
   - no `GradientTape`, `ForwardAccumulator`, or hidden autodiff.

## Required Checks/Tests/Reviews

- Static audit that admitted score helpers do not use:
  - `GradientTape`
  - `ForwardAccumulator`
  - `gradient`
  - `jacobian`
  - `batch_jacobian`
  - `watch`
- Runtime no-autodiff sentinel on score paths.
- Tiny same-scalar centered finite-difference check for each admitted score
  row.
- For fixed SIR, explicit checks that score components include all total
  derivative channels:
  - observation density covariance;
  - LEDH flow observation covariance;
  - transition mean from transition density;
  - transition mean from LEDH flow prior;
  - transition mean from pre-flow/process path.
- Claude read-only implementation review for material score diffs.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the implemented scores derivatives of the exact Phase 3 admitted finite-`N` LEDH likelihood scalars? |
| Baseline/comparator | Phase 3 admitted value scalars, LGSSM existing compact score tests, fixed-SIR same-scalar finite differences, and scoped SIR diagnostic only as non-admission reference. |
| Primary criterion | Tiny no-tape score matches same-scalar finite difference within row-specific tolerance and passes static/runtime no-autodiff audits. |
| Veto diagnostics | Autodiff use; missing total-VJP terms; stop-gradient masking; derivative of proposal objective; derivative of a different random path; scoped SIR diagnostic promoted as fixed full-row evidence. |
| Explanatory diagnostics | Runtime, memory, conditioning, FD noise, and component decomposition. |
| Not concluded | `N=10000` memory correctness, full leaderboard readiness, HMC readiness, posterior correctness, or scientific superiority. |

## Forbidden Claims/Actions

- Do not score Phase 3 blocked rows.
- Do not use tape gradient as admitted score evidence.
- Do not use finite difference as the implementation.
- Do not use stop-gradient as a mathematical repair.
- Do not use finite-difference agreement against the wrong scalar.
- Do not claim scoped parameterized SIR diagnostic evidence as fixed full-row
  score admission.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only with:

- explicit list of rows whose tiny no-tape score checks passed;
- explicit list of rows still score-blocked;
- static and runtime no-autodiff evidence;
- Phase 5 subplan that creates one N=10000 correctness/memory test per score
  row and an integration test for admitted rows only.

## Stop Conditions

Stop for a row if the manual score cannot be made the derivative of the
admitted scalar without new mathematics, human direction, or changing the row
target. Continue to the other admitted row only if independence is explicit.
