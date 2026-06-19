# P71 Phase 4c Result: Objective-Preserving Scaled ALS Implementation

metadata_date: 2026-06-16
status: CLAUDE_R2_AGREE_PHASE4_RERUN_SUBPLAN_READY_TO_DRAFT
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4c-objective-preserving-scaled-als-implementation-subplan-2026-06-16.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the Phase 4c implementation add objective-preserving column-scaled weighted ridge ALS and close the stale ridge/policy surfaces without changing thresholds, target, rank, degree, row budgets, initializer, sweep order, or Phase 5 boundary? |
| Baseline/comparator | The prior `FixedTTFitter` unscaled normal-equation solve, Phase 4b objective-preserving equation, and focused tests over controlled direct, ill-scaled, policy, and failed-fit cases. |
| Primary criterion | Focused implementation checks pass; manifests record stabilization policy and diagnostics; source-route helper honors nondefault ridge; failed fits still fail closed with structured diagnostics. |
| Veto diagnostics | Isotropic scaled ridge, missing branch-hash policy fields, stale `P70_FIT_RIDGE` reporting for supplied ridge, missing failed-fit stabilization diagnostics, threshold/row/rank/degree/sweep/initializer drift, Phase 5 launch, or d18 accuracy claim. |
| Explanatory diagnostics | Transformed-system condition, original unscaled normal condition, column-scale summaries/hash, ridge metric summary, fit residuals, and branch hashes. |
| Not concluded | No Phase 4 rerun pass, no d18 accuracy, no rank/degree convergence, no five-seed robustness, no scaling claim, no HMC readiness, and no Zhao-Cui source-faithfulness claim for this stabilization. |

## Implementation Summary

Scoped files edited:

- `bayesfilter/highdim/fitting.py`
- `bayesfilter/highdim/source_route.py`
- `tests/highdim/test_fixed_branch_fit.py`

Implemented:

- `FixedTTFitter` now solves core updates through objective-preserving column-scaled augmented weighted ridge ALS.
- The solved system uses \(A_s = A S^{-1}\), ridge rows \(\sqrt{\rho} S^{-1}\), and unscales the solved variable by \(c=S^{-1}z\).
- Condition warning/veto applies to the transformed augmented system actually solved.
- Original unscaled normal-equation condition is preserved as diagnostic-only.
- Branch manifest, fit diagnostics, and per-core records include stabilization policy ID, solver backend, objective-preserving scaling flag, column scale floor/rule, transformed ridge rule `rho_times_S_inverse_squared`, condition gate target, unscaled condition role, column-scale summaries/hash, and ridge metric summary.
- Fit-level diagnostics now include `stabilization_diagnostics_summary`, derived from per-core records, with transformed condition, original unscaled condition, column-scale hashes/spread, and ridge-metric summary.
- `_p59_fixed_ttsirt_transport_from_values(..., ridge=...)` now passes the supplied ridge into `FixedTTFitConfig`.
- Source-route fixed-fit policy and failed-fit `P70FixedFitDiagnosticError` payloads now report the supplied ridge, stabilization policy, and stabilization diagnostics summary.

## Local Check Results

| Check | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py tests/highdim/test_fixed_branch_fit.py` | PASS |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py` | PASS: 34 passed, 2 TensorFlow Probability deprecation warnings |
| `git diff --check -- bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py tests/highdim/test_fixed_branch_fit.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4c-objective-preserving-scaled-als-implementation-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-runbook-claude-review-ledger-2026-06-16.md` | PASS |

## Claude R1 Implementation Review

Claude R1 returned `VERDICT: REVISE`.

Accepted material blocker:

- Fit-level `FixedTTFitResult.diagnostics` lacked the full stabilized-fit
  diagnostic summary, even though per-core records had the data.
- Source-route policy and failed-fit diagnostic payloads therefore exposed only
  partial stabilization diagnostics.
- Focused tests did not assert those fit-level/source-route summary fields.

Repair:

- Added `stabilization_diagnostics_summary` to `FixedTTFitResult.diagnostics`.
- Propagated the same summary into `_p70_fixed_fitting_policy_payload` and the
  `P70FixedFitDiagnosticError` payload.
- Added tests asserting fit-level diagnostics, policy payload diagnostics, and
  failed-fit diagnostic summary fields.
- Preserved `"inf"` in fit-level summaries for failed singular transformed
  systems.

R1 repair checks:

- PASS: `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py tests/highdim/test_fixed_branch_fit.py`
- PASS: `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py`
  - Output summary: `34 passed, 2 warnings`.
- PASS: `git diff --check -- bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py tests/highdim/test_fixed_branch_fit.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4c-objective-preserving-scaled-als-implementation-result-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-runbook-claude-review-ledger-2026-06-16.md`

## Claude R2 Implementation Review

Claude R2 returned `VERDICT: AGREE`.

Claude agreed that:

- fit-level `stabilization_diagnostics_summary` exposes transformed
  solved-system condition, original unscaled normal condition, column-scale
  summaries/hashes, and ridge-metric extrema;
- the objective-preserving scaled ridge ALS route is preserved;
- source-route ridge and stabilization diagnostics propagate through
  `_p70_fixed_fitting_policy_payload` and `P70FixedFitDiagnosticError`;
- focused tests cover the repaired surfaces and isotropic-ridge leakage;
- Phase 4 rerun, Phase 5, and scientific-claim boundaries remain closed.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 4c and draft refreshed Phase 4 rerun subplan. | PASS locally after R1 repair; Claude R2 `VERDICT: AGREE`. | No unresolved local or Claude veto. | The repaired solver has not yet been exercised by the full Phase 4 ladder. | Draft refreshed Phase 4 structural-ladder rerun subplan with the original admission boundary. | No Phase 4 repair success, no d18 admissibility, no Phase 5 launch. |

## Run Manifest

| Field | Value |
| --- | --- |
| Branch | `fix/fixed-sgqf-merge-audit` |
| Commit | `94069066a70df6f1f0f2b53d32b9d452bd67f891` |
| Worktree | Dirty before and after; scoped implementation files modified plus unrelated dirty/untracked repo work existed before this close record. |
| Environment | CPU-only deliberate checks with `CUDA_VISIBLE_DEVICES=-1`; `MPLCONFIGDIR=/tmp`. |
| GPU status | N/A for local checks; no GPU command was run in Phase 4c implementation checks. |
| Random seeds | N/A for focused deterministic unit tests. |
| Data version | N/A; no Phase 4 ladder or d18 scientific run executed. |
| Output artifacts | This result note and the focused pytest output summarized above. |

## Boundary Notes

- Phase 5 remains blocked.
- The whole P71 Phase 4 structural ladder was not rerun.
- No thresholds, target, rank, degree, row counts, sweep order, or initializer were intentionally changed.
- This is an engineering repair gate, not a scientific validation gate.

## Closeout

Phase 4c is closed as an engineering implementation gate.  The next allowed
action is to draft the refreshed Phase 4 structural-ladder rerun subplan.  The
full ladder may not run until that subplan states the evidence contract,
checks, artifacts, stop conditions, and boundary rules.
