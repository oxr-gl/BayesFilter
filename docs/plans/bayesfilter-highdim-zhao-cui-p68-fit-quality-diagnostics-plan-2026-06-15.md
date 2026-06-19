# P68 Plan: Fixed-TTSIRT Fit-Quality Diagnostics

metadata_date: 2026-06-15
status: DRAFT_FOR_REVIEW
parent_result: docs/plans/bayesfilter-highdim-zhao-cui-p67-adjacent-ladder-execution-result-2026-06-15.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Objective

Repair the P67 evidence gap by exposing fixed-TTSIRT fit-quality diagnostics in
the P59/P67 artifacts, then rerun the same adjacent ladder without changing
rows, thresholds, or nonclaim boundaries.

P68 does not change the fixed branch algorithm.  It only preserves diagnostics
already computed by the fixed TT fit layer, and records whether holdout-style
diagnostics are absent.

## Entry Conditions

- P67 executed the adjacent ladder and returned
  `P67_ADJACENT_FIXED_BUDGET_SCREEN_INCONCLUSIVE`.
- Every P67 row assembled and passed source invariants, with no defensive-only
  row and no near-zero TT core collapse.
- Every P67 row was budget-unresolved because the row artifacts did not expose
  condition-number, holdout-residual, or fit-residual diagnostics.
- The P67 degree ladder exceeded the declared delta thresholds; P68 must not
  hide or relax those failures.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does exposing fixed-TTSIRT fit-quality diagnostics remove the row-level diagnostic-missing blocker from P67, and what does the unchanged adjacent ladder report afterward? |
| Baseline | P67 JSON/status with missing fit-resolution diagnostics and unchanged thresholds. |
| Primary criterion | P59/P67 row artifacts expose fit status, per-core condition numbers and warning/veto thresholds, fit residuals, and explicit holdout availability/status for each step fit. |
| Veto diagnostics | Missing exposed fit diagnostics after implementation; non-OK fit status; nonfinite fit residual; condition-number veto or warning not recorded; source-invariant drift; defensive-only row; near-zero core collapse; unauthorized ladder difference; threshold failures. |
| Explanatory diagnostics | Condition-number summaries, per-core update records, fit residuals, holdout absent/present status, ladder deltas, runtime events. |
| Not concluded | No structural rank/degree convergence proof, no d18 correctness, no d50/d100 scaling, no adaptive Zhao--Cui parity, no HMC readiness.  A small fit residual is not a correctness proof. |
| Artifacts | Updated code/tests, P68 result note, refreshed P67-style JSON or a P68 JSON path if the runner name changes. |

## Implementation Scope

Expose diagnostics from existing `FixedTTFitResult` objects:

- `status`;
- `termination_reason`;
- `stop_condition_triggered`;
- `fit_residual`;
- `holdout_residual`;
- `holdout_available`;
- per-core update records containing condition numbers and condition thresholds;
- condition-number summaries such as max finite condition number and whether any
  condition warning/veto appeared.

The narrow source route is:

1. Add a helper in `bayesfilter/highdim/source_route.py` to build a JSON-ready
   fit-quality diagnostic payload from a `FixedTTFitResult`.
2. Return that payload from `_p59_fixed_ttsirt_transport_from_values` alongside
   transport and branch hashes.
3. Add step-level fit-quality diagnostics to the P59-9b manifest.
4. Add P59-9a fit-quality diagnostics for its existing preparation fit.
5. Update `scripts/p67_author_sir_adjacent_ladder_diagnostics.py` so a row is
   no longer budget-limited merely because diagnostics were absent; it must
   inspect the newly exposed diagnostics and mark unresolved only when the
   diagnostics are missing, non-OK, nonfinite, condition-vetoed, or explicitly
   holdout-unavailable under the P68 contract.

P68 may record holdout-unavailable as an unresolved diagnostic.  It must not
invent a holdout set or change the fitting samples without a separate reviewed
plan.

## Required Checks

Before execution:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  scripts/p67_author_sir_adjacent_ladder_diagnostics.py
```

Focused tests:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p59_author_sir_step_spec_assembly.py \
  tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
```

Rerun unchanged adjacent ladder:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python \
  scripts/p67_author_sir_adjacent_ladder_diagnostics.py \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p68-fit-quality-adjacent-ladder-diagnostics-2026-06-15.json
```

Self-check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python \
  scripts/p67_author_sir_adjacent_ladder_diagnostics.py \
  --check-only \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p68-fit-quality-adjacent-ladder-diagnostics-2026-06-15.json
```

## Skeptical Audit

- Wrong baseline: P68 compares against the P67 evidence gap, not against the
  old P60 low/high sentinel.
- Proxy metrics: fit residuals and condition numbers can explain or veto; they
  cannot prove filtering correctness or structural convergence.
- Hidden assumption: holdout diagnostics are currently absent.  P68 records
  this explicitly rather than fabricating holdout evidence.
- Threshold discipline: P68 does not change the P67 delta thresholds after
  seeing data.
- Artifact fitness: the rerun JSON must show whether diagnostics are present
  and why a row is passable, inconclusive, or blocked.

## Stop Conditions

- Claude plan review returns material `VERDICT: REVISE` not fixed within five
  rounds.
- The implementation would require changing the fixed branch algorithm, fit
  samples, thresholds, or ladder rows.
- Diagnostics cannot be exposed without destabilizing existing P59/P66 tests.
- The rerun produces threshold failures; record them, do not tune around them.

## Review Protocol

Claude is read-only.  It may review this plan, the implementation diff, and the
result artifact.  It cannot authorize scientific overclaims or post-hoc
threshold changes.
