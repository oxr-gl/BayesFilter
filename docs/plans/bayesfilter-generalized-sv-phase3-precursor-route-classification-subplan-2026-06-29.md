# Phase 3 Subplan: Precursor Route Design And Classification

Date: 2026-06-29

## Status

`REVIEWED_ROUTE_CLASSIFICATION_SUBPLAN_CLOSED`

## Phase Objective

Classify the current Generalized-SV SGQF route as precursor, admitted,
diagnostic, or blocked, and make explicit what it may and may not claim before
any same-target promotion gate.

## Entry Conditions Inherited From Previous Phase

- Phase 2 has reviewed and frozen the row identity, target family,
  truth/test-point convention, and oracle/evaluator split.
- The active benchmark row remains
  `zhao_cui_generalized_sv_synthetic_from_estimated_values`.
- The current source-row SGQF evaluator is not yet admitted by any reviewed
  artifact.
- The native generalized-SV dense reference remains oracle-only evidence.
- Any current executable generalized-SV approximation route must be classified
  without promoting precursor evidence into admission evidence.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-result-2026-06-29.md`
- Refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-generalized-sv-phase4-short-prefix-same-target-value-gate-subplan-2026-06-29.md`
- Visible execution ledger:
  `docs/plans/bayesfilter-generalized-sv-visible-execution-ledger-2026-06-29.md`
- Claude review ledger:
  `docs/plans/bayesfilter-generalized-sv-claude-review-ledger-2026-06-29.md`
- Governing contract:
  `docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md`
- Source-scope SGQF unlock plan:
  `docs/plans/bayesfilter-generalized-sv-source-scope-sgqf-unlock-plan-2026-06-24.md`
- SGQF admission ledger:
  `docs/plans/bayesfilter-source-scope-sgqf-admission-ledger-2026-06-24.md`
- Source-row numeric runner:
  `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- Highdim leaderboard harness:
  `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- Native dense-reference implementation:
  `bayesfilter/highdim/native_generalized_sv.py`
- Source-scope emitter/spec anchors:
  `scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py`
  `scripts/filtering_value_gradient_benchmark_emit_generalized_sv_spec.py`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f docs/plans/bayesfilter-source-scope-sgqf-admission-ledger-2026-06-24.md
test -f scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py
test -f docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py
test -f bayesfilter/highdim/native_generalized_sv.py
test -f scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py
test -f scripts/filtering_value_gradient_benchmark_emit_generalized_sv_spec.py
rg -n "blocked_missing_value_route|blocked_missing_analytical_route|no reviewed SGQF source-scope generalized-SV evaluator is wired|augmented_noise|generalized_sv_augmented|native_generalized_sv_dense_reference|reviewed_evaluator_pending" docs/plans/bayesfilter-source-scope-sgqf-admission-ledger-2026-06-24.md docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py bayesfilter/highdim/native_generalized_sv.py scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py scripts/filtering_value_gradient_benchmark_emit_generalized_sv_spec.py
git diff --check -- docs/plans/bayesfilter-generalized-sv*.md
```

Required read-only Claude reviews:

- Phase 3 result,
- refreshed Phase 4 subplan.

No implementation, new evaluator wiring, runtime, benchmark, leaderboard
mutation, score, derivative, HMC, GPU/CUDA, package/network, release, CI, or
default-policy command is authorized in Phase 3. This phase is a read-only
classification and blocker/precursor determination.

## Skeptical Plan Audit

| Risk Checked | Phase 3 Control |
| --- | --- |
| Wrong baseline | Classification must distinguish the source-row SGQF evaluator question from existing UKF/SVD/CUT4 augmented-noise execution and from the native dense oracle. |
| Proxy metric promoted | The existence of an augmented-noise runner branch or blocked row metadata does not admit a same-target SGQF evaluator. |
| Missing stop condition | If no distinct source-row SGQF evaluator is wired, Phase 3 must classify the route as blocked pending source-scope evaluator rather than force a promotional handoff. |
| Unfair comparison | No transformed, KSC, or augmented-noise approximation may be relabeled as same-target generalized-SV admission evidence without a reviewed gate. |
| Hidden assumption | Native dense-reference existence does not imply source-row evaluator availability. UKF/SVD/CUT4 execution does not imply SGQF execution. |
| Stale context | Historical unlock plans and ledgers are supporting evidence only; the reviewed Phase 2 contract controls route-class vocabulary. |
| Environment mismatch | Phase 3 is code/document inspection only; no evaluator runtime is authorized. |
| Artifact-answer mismatch | Phase 3 must close with an explicit route class and preserved nonclaims, not just a narrative summary. |

Audit status: passed if classification is anchored to existing implementation
and artifact surfaces without promoting unwired or approximate routes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the correct current route class for the Generalized-SV SGQF source-row path, given the actual implementation, runner, leaderboard, and governing artifacts? |
| Baseline/comparator | reviewed Phase 2 contract, SGQF admission ledger, source-row runner, leaderboard harness, source-scope emitters/spec artifacts, and native dense-reference implementation. |
| Primary criterion | Phase 3 writes a reviewed classification that names whether the SGQF source-row path is `BLOCKED_PENDING_SOURCE_SCOPE_EVALUATOR`, `PRECURSOR_VALUE_ONLY`, `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE`, or, only if reviewed evidence truly supports it, another governed route class, with exact evidence for what is and is not wired today. |
| Veto diagnostics | claiming a distinct SGQF source-row evaluator exists when it does not, treating augmented-noise UKF/SVD/CUT4 execution as SGQF admission, treating native dense reference as source-row execution, or promoting precursor evidence as admission. |
| Explanatory diagnostics | runner provenance strings, blocked-row ledger text, leaderboard row statuses, and source-scope emitter notes. |
| Not concluded | No same-target value pass, no SGQF source-row admission, no score admission, no HMC readiness, no production readiness, and no leaderboard promotion. |
| Artifact | reviewed Phase 3 classification result and refreshed Phase 4 subplan. |

## Forbidden Claims/Actions

- Do not claim a distinct SGQF source-row evaluator is wired unless an exact
  implementation entry point exists and is admitted by reviewed evidence.
- Do not relabel UKF/SVD/CUT4 augmented-noise execution as SGQF same-target
  admission.
- Do not relabel native dense-reference evidence as source-row execution.
- Do not run implementation, runtime, benchmark, evaluator, score, derivative,
  HMC, GPU/CUDA, package/network, release, CI, or default-policy commands.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only if:

- the Phase 3 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 4 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records one of the following reviewed class-to-handoff
  mappings:
  - `PRECURSOR_VALUE_ONLY` -> Phase 4 may be refreshed as an executable
    precursor/oracle-agreement scope only.
  - `BLOCKED_PENDING_SOURCE_SCOPE_EVALUATOR` -> Phase 4 is blocker-only pending
    a missing source-scope evaluator.
  - `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE` -> Phase 4 remains diagnostic-only
    with no promotional advancement authority.
  - `SOURCE_ROW_SAME_TARGET_ADMITTED` is not expected from current known
    evidence; it would require separate explicit reviewed authority and must not
    be inferred from this subplan alone.

## Stop Conditions

- Inspection shows no distinct source-row SGQF evaluator and no reviewed
  precursor route suitable for a Phase 4 oracle-agreement gate.
- Artifact/code evidence is inconsistent enough that route class cannot be
  stated honestly without new implementation or new authority.
- Local document/source checks fail and cannot be repaired within document
  scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require implementation, runtime, benchmark, evaluator,
  GPU/CUDA, package/network, release, CI, default-policy, destructive
  git/filesystem, or unrelated dirty worktree changes.

## End-Of-Phase Requirements

1. Run the required code/document inspection checks.
2. Write the Phase 3 classification result.
3. Refresh Phase 4 according to the reviewed class-to-handoff mapping above:
   `PRECURSOR_VALUE_ONLY` -> executable precursor/oracle-agreement scope only;
   `BLOCKED_PENDING_SOURCE_SCOPE_EVALUATOR` -> blocker-only; and
   `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE` -> diagnostic-only with no
   promotional advancement authority.
4. Review the Phase 3 result and refreshed Phase 4 subplan.
5. Update the execution ledger and Claude review ledger.
