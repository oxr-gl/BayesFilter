# P71 Phase 4c Subplan: Objective-Preserving Scaled ALS Implementation

metadata_date: 2026-06-16
status: CLAUDE_R2_AGREE_IMPLEMENTATION_AUTHORIZED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 4c
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement the reviewed Phase 4b objective-preserving column-scaled weighted
ridge ALS repair for `FixedTTFitter`, repair the ignored P59 ridge argument,
and run focused local checks.  Phase 4c may run only implementation and focused
diagnostics needed to decide whether the repair is eligible for a later P71
Phase 4 structural-ladder rerun.

Phase 4c is not an accuracy phase and cannot launch Phase 5.

## Entry Conditions Inherited From Previous Phase

- P71 Phase 4 remains blocked with Claude agreement:
  `PHASE4_BLOCKED_CLAUDE_REVIEW_AGREE_STOPPED_BEFORE_PHASE5`.
- P70 Phase 6c has Claude agreement and identifies unscaled ALS
  design/normal-equation conditioning as the proximate first-row blocker.
- Phase 4b has Claude agreement for the objective-preserving scaled solve:
  \(A_s=A S^{-1}\), \(c=S^{-1}z\), and
  \((A_s^\top W A_s+\rho S^{-2})z=A_s^\top Wy\).
- Isotropic ridge in scaled coordinates is not authorized.
- Phase 5 remains blocked until a rerun Phase 4 admits exactly one d18
  configuration.

## Allowed Files

Implementation may touch only:

- `bayesfilter/highdim/fitting.py`;
- `bayesfilter/highdim/source_route.py`;
- `tests/highdim/test_fixed_branch_fit.py`;
- focused P71/P70 docs under `docs/plans`.

If another file appears necessary, stop and patch this subplan or ask for
direction before editing it.

## Required Implementation Details

### FixedTTFitter Scaled Solve

Add a deterministic objective-preserving column scaling path to core updates:

1. Build the existing design \(A\), weights \(W\), target \(y\), and ridge
   \(\rho\).
2. Compute fixed column scales
   \(s_j=\max(\lVert A_{\cdot j}\rVert_2,s_{\min})\), with a documented
   positive floor.
3. Let \(S={\rm diag}(s)\), \(A_s=A S^{-1}\), and solve
   \[
     (A_s^\top W A_s+\rho S^{-2})z=A_s^\top Wy.
   \]
4. Unscale with \(c=S^{-1}z\), then reshape \(c\) into the core.
5. Apply condition warning/veto thresholds to the transformed system actually
   solved.
6. Record the original unscaled normal-equation condition as diagnostic-only.

The implementation must not use \((A_s^\top W A_s+\rho I)\) for this first
repair.

### Manifest And Diagnostics

Update per-core update records, fit diagnostics, and branch manifest payloads
to include:

- `solver_backend`;
- `stabilization_policy`;
- `objective_preserving_column_scaling`;
- column scale summary and column scale hash;
- transformed-system condition number;
- original unscaled normal-equation condition number;
- ridge metric summary;
- enough branch-hash payload material so stabilization policy changes alter
  branch identity.

### Ridge Argument Cleanup

Make `_p59_fixed_ttsirt_transport_from_values(..., ridge=...)` pass the
supplied `ridge` argument into `FixedTTFitConfig`.  This cleanup is not the
observed P70 Phase 6c root cause because the diagnostic supplied
`P70_FIT_RIDGE`, but it is a real implementation mismatch and should be closed
while touching the fit configuration surface.

The cleanup must update every source-route artifact surface that reports the
fixed-fit ridge/policy, including:

- the `FixedTTFitConfig` construction in
  `_p59_fixed_ttsirt_transport_from_values`;
- the failed-fit `P70FixedFitDiagnosticError` payload emitted by the same
  helper;
- `_p70_fixed_fitting_policy_payload`;
- any manifest/result payload that would otherwise still report
  `P70_FIT_RIDGE` after a caller supplied a different ridge.

## Required Checks/Tests/Reviews

Before edits:

```bash
rg -n "def _normal_equations|def _fit_core_update|stabilization_choices|solver_backend|def _p59_fixed_ttsirt_transport_from_values|ridge=P70_FIT_RIDGE" bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py
```

After implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py tests/highdim/test_fixed_branch_fit.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py
git diff --check -- bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py tests/highdim/test_fixed_branch_fit.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4c-objective-preserving-scaled-als-implementation-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-runbook-claude-review-ledger-2026-06-16.md
```

Focused tests must cover:

- objective-preserving scaled solve matches the original weighted ridge
  solution on a controlled problem with nontrivial column-scale imbalance,
  nonuniform weights, and materially nonzero ridge.  The fixture must be able
  to fail if isotropic ridge in scaled coordinates is used by mistake;
- transformed-system condition can be admissible on a controlled ill-scaled
  design while the original unscaled normal condition remains recorded;
- manifests and branch hashes change when stabilization policy changes,
  including changes to policy fields that may not affect realized scales on a
  particular matrix;
- `_p59_fixed_ttsirt_transport_from_values` honors a nondefault supplied
  `ridge` in the fit config, failed-fit payload, fixed-fitting policy payload,
  and manifest/result surfaces;
- failed-fit payloads preserve the new stabilization diagnostics through the
  structured `P70FixedFitDiagnosticError` path;
- condition-veto failures still fail closed when the transformed system is
  nonfinite or beyond the unchanged veto threshold.

After focused tests, Phase 4c may run a first-row diagnostic rerun only if the
result note first records the exact evidence contract, command, commit/branch
hash, dirty-worktree status, CPU-only environment declaration, output artifact
path, fit/density branch hashes, and interpretation boundary.  Phase 4c may
not rerun the whole P71 Phase 4 ladder until the implementation result has
passed local checks and Claude review.

Claude implementation review is required before any Phase 4 rerun.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the objective-preserving scaled ALS implementation repair the numerical solve surface without changing thresholds, target, rank, degree, row budgets, initializer, or Phase 5 boundary? |
| Baseline/comparator | Current unscaled `FixedTTFitter` normal-equation solve, Phase 4b design, and focused tests over controlled well-conditioned and ill-scaled designs. |
| Primary criterion | Focused implementation tests pass; manifests record stabilization policy and diagnostics; failed fits still fail closed; no unauthorized files or thresholds change. |
| Veto diagnostics | Isotropic scaled ridge, threshold relaxation, rank/degree/row retuning, source-route drift, nonfinite transformed solve, branch-hash omission, missing ridge cleanup, Phase 5 launch, or d18 accuracy claim. |
| Explanatory diagnostics | Original unscaled condition, transformed condition, column-scale summaries, fit residuals, branch hashes, first-row diagnostic rerun if authorized after implementation. |
| Not concluded | No P71 Phase 4 pass, no d18 accuracy, no rank/degree convergence, no five-seed robustness, no scaling, no HMC readiness. |
| Artifact | Phase 4c result note, local test output summary, and any authorized focused diagnostic JSON. |

## Exact Next-Phase Handoff Conditions

If Phase 4c implementation passes local checks and Claude review, the next
phase is a refreshed Phase 4 structural-ladder rerun subplan.  That subplan
must restate the Phase 4 evidence contract and may not start Phase 5 unless
the rerun admits exactly one d18 configuration.

If implementation or tests fail, write a Phase 4c blocker result and stop for
repair design.

## Forbidden Claims/Actions

- Do not launch Phase 5.
- Do not run the whole Phase 4 structural ladder from this subplan before
  implementation review.
- Do not use isotropic ridge in scaled coordinates.
- Do not change `P70_CONDITION_NUMBER_WARNING` or
  `P70_CONDITION_NUMBER_VETO`.
- Do not change fit row counts, rank, degree, sweep order, initializer, or
  source-route semantics.
- Do not claim source-faithfulness, d18 accuracy, rank convergence, scaling, or
  HMC readiness.

## Required Stabilization Policy Fields

Phase 4c implementation must record the stabilization policy independently of
realized matrix values.  At minimum, branch manifests, diagnostics, and
policy payloads must include:

- `stabilization_policy_id`;
- `solver_backend`;
- `objective_preserving_column_scaling: true`;
- `column_scale_floor`;
- transformed-ridge rule, stated as `rho_times_S_inverse_squared`;
- condition-number gate target, stated as transformed solved system;
- original unscaled normal-equation condition role, stated as diagnostic-only.

These fields must be part of branch identity even if no column scale hits the
floor in a particular fit.

## Stop Conditions

Stop if:

- objective-preserving scaling cannot be implemented without broader route
  changes;
- tests show the transformed solve is not algebraically equivalent to the
  original weighted ridge objective on the required nontrivial-scale,
  nonuniform-weight, nonzero-ridge fixture;
- branch manifests cannot preserve stabilization policy;
- the ridge cleanup requires changing public API semantics beyond honoring the
  existing argument;
- Claude review returns `VERDICT: REVISE` and the blocker cannot be patched
  within five rounds.

## Skeptical Plan Audit

This plan targets the measured numerical root cause while avoiding threshold
retuning and Phase 5 leakage.  It does not use P70 Phase 6c explanatory probes
as proof of repair.  It requires controlled unit tests before any first-row or
Phase 4 rerun and preserves the distinction between implementation correctness,
structural ladder readiness, and scientific validation.
