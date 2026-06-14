# P44-M6 Result: Predator-Prey Diagnostic Closure

metadata_date: 2026-06-08
phase: P44-M6
run_id: `p44-codex-supervised-20260608-013203`
Status: `PASS_P44_M6_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | M6 predator-prey diagnostic closure passed final read-only Claude code/governance review. |
| Primary criterion status | Passed locally as diagnostic-only: predator-prey model-contract anchor, domain diagnostic, finite CUT4 value and parameter score, CUT4 metadata boundary, executable no-Zhao--Cui equality route, and fair-comparison manifest blockers. |
| Veto diagnostic status | No unmatched-budget, ODE-domain, nonfinite-likelihood, proxy-promotion, diagnostic-overclaim, point-cap, or compile veto fired. |
| Main uncertainty | This is not a fair linear-vs-nonlinear preconditioning comparison and not a native Zhao--Cui predator-prey equality result. |
| Next justified action | Run the P44-M6 executable phase gate, then proceed to P44-M7 if the gate passes. |
| Not concluded | No nonlinear preconditioning usefulness, no matched linear/nonlinear comparison success, no CUT4-vs-Zhao--Cui equality, no paper-scale predator-prey validation, no adaptive MATLAB behavior, no HMC readiness, and no score API readiness. |

## Evidence Contract

Question: for the existing two-state predator-prey fixture, can CUT4 evaluate a
finite additive-Gaussian closure value and diagnostic parameter score while
preserving the blocked nonlinear-preconditioning usefulness boundary?

Baseline/comparator:

- Governing baseline: predator-prey model-contract tests from
  `PredatorPreySSM`, including parameter box, RK4 source anchors, observation
  convention, and domain diagnostics.
- CUT4 diagnostic closure: `tf_svd_cut4_filter` on a clean-room
  additive-Gaussian structural closure with horizon 2, augmented dimension 4,
  point count 24, and the six physical predator-prey parameters.
- Zhao--Cui route: no matched non-scalar predator-prey equality target exists
  in this phase; the fixed-branch highdim value route rejects the non-scalar
  model, and this is recorded as diagnostic-only nonclaim evidence.
- Fair-comparison schema: `P30PredatorPreyComparisonManifest` is used only to
  check matched-settings and proxy-promotion blockers.

Primary promotion criterion:

- `PredatorPreySSM` source/model-contract metadata is present;
- domain failures are surfaced by diagnostics;
- CUT4 closure value and diagnostic TensorFlow autodiff parameter score are
  finite;
- CUT4 metadata records diagnostic closure, point count, polynomial degree, and
  no innovation-floor events;
- the absence of a matched Zhao--Cui equality route is executable;
- fair-comparison manifest rejects unmatched budgets and cost-free ESS
  promotion.

Veto diagnostics:

- unmatched budgets or parameter settings;
- ODE domain failure or nonfinite likelihood;
- cost-free ESS promotion;
- diagnostic closure described as paper-scale predator-prey validation;
- CUT4-vs-Zhao--Cui equality claimed without a matched shared closure target;
- finite diagnostic score promoted as production score API readiness.

Explanatory-only diagnostics:

- TensorFlow warning logs, wall time, CUT4 point count, polynomial degree,
  diagnostic score norm, and manifest schema checks.

Nonclaims:

- no nonlinear preconditioning usefulness;
- no matched linear/nonlinear comparison success;
- no CUT4-vs-Zhao--Cui equality;
- no paper-scale predator-prey validation;
- no adaptive MATLAB behavior;
- no GPU readiness;
- no HMC readiness;
- no DSGE readiness;
- no stable public API or score API readiness.

Artifact preserving the result:

- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase6-predator-prey-diagnostic-result-2026-06-07.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase6-predator-prey-diagnostic-evidence-manifest-p44-codex-supervised-20260608-013203.json`
- Command logs:
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M6-command0.log`
  and
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M6-command1.log`

## Skeptical Audit

Status: `PASS_P44_M6_CODE_GOVERNANCE`.

- Wrong-baseline risk: there is no same-target dense or Zhao--Cui comparator
  in M6; the phase is therefore explicitly diagnostic-only.
- Proxy-metric risk: finite CUT4 value, finite score, raw ESS, wall time, and
  trajectory metrics are not promoted to preconditioning usefulness.
- Target-mismatch risk: the test records that the current highdim fixed-branch
  route rejects non-scalar predator-prey, so no equality row is run.
- Fairness risk: manifest schema blocks unmatched comparison settings and
  proxy-only promotion.
- Resource risk: fixture is two-state, horizon 2, CPU-only, augmented
  dimension 4, and point count 24, within the phase cap.
- Hidden-assumption risk: the closure is named and labeled as additive-Gaussian
  diagnostic closure, not paper-scale predator-prey validation.

## Local Evidence

Commands:

1. `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q -s tests/highdim/test_p44_predator_prey_diagnostic.py`
2. `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p44_predator_prey_diagnostic.py`

Observed result:

- Focused pytest: `5 passed`, exit code 0.
- Compile check: exit code 0.
- CUT4 diagnostic value: `-1.442440e+02`.
- CUT4 diagnostic score norm: `4.194142e+02`.
- CPU-only mode was deliberate; no GPU evidence is claimed. TensorFlow emitted
  CUDA initialization warnings despite `CUDA_VISIBLE_DEVICES=-1`; these are
  treated as explanatory-only because the phase is CPU-only.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `N/A - dirty worktree preserved; command manifest captures current files` |
| Command environment | CPU-only via `CUDA_VISIBLE_DEVICES=-1` and `MPLCONFIGDIR=/tmp` |
| Data version | deterministic in-test observations |
| Random seeds | deterministic fixture only; no stochastic run promotion |
| Wall time | tiny local validation only |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase6-predator-prey-diagnostic-subplan-2026-06-07.md` |
| Test file | `tests/highdim/test_p44_predator_prey_diagnostic.py` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase6-predator-prey-diagnostic-result-2026-06-07.md` |

## Gate Markers

p44_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase6-predator-prey-diagnostic-evidence-manifest-p44-codex-supervised-20260608-013203.json`
p44_local_evidence_run: `COMPLETE`
p44_evidence_audit: `COMPLETE`
p44_result_note_substance: `COMPLETE`
p44_traceability_or_nonclaim: `COMPLETE`
p44_command_count: `2`
p44_long_run_used: `false`
