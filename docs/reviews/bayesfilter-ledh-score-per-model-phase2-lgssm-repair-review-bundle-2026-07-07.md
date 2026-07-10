# Phase 2 LGSSM Repair Review Bundle

metadata_date: 2026-07-07
review_scope: `score_phase2_lgssm_repair`

## Role Contract

Claude is read-only reviewer only.

Do not edit files, run experiments, launch agents, approve policy boundaries,
or change state.

Codex remains supervisor and executor.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

## Objective

Review the Phase 2 LGSSM blocker result and repair subplan before Codex changes
the full LGSSM score execution path.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-phase2-lgssm-full-run-blocker-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase2-lgssm-repair-subplan-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase2-lgssm-subplan-2026-07-07.md`
- `bayesfilter/highdim/ledh_score_contract.py`
- `tests/highdim/test_ledh_lgssm_score_phase2_contract.py`

Do not review the whole repo.

## Current State

Phase 2 preflight passed:

- active full-row identity is now N=10000;
- stale N=1000 raw evidence is rejected;
- full-mode dispatch reaches total-VJP code despite a legacy CLI constant name;
- raw score fixtures normalize into the Phase 1 score schema.

The full T=50,N=10000 raw runner was launched after preflight. It produced no
JSON artifact in a bounded visible window and was interrupted. The log showed
execution inside the compact JVP finite-Sinkhorn softmin loop.

Older LGSSM score-memory evidence is not admissible because it used T=2, while
the current admitted value artifact is T=50,N=10000.

## Proposed Repair

Build a bounded full-row score artifact path that:

- computes the compact T=50,N=10000 score once;
- may use a predeclared same-scalar directional finite-difference diagnostic as
  explanatory evidence only;
- still requires coordinate-wise same-scalar finite differences, an
  exact/reference all-parameter score check, or proof-backed reviewed tests for
  full admission;
- validates the final score artifact with
  `validate_ledh_score_artifact(..., require_admitted=True)`;
- does not admit old T=2 or stale N=1000 evidence.

## Review Questions

1. Is the blocker correctly classified as fixable execution-plan failure, not
   score target failure?
2. Does the revised repair correctly keep directional FD diagnostic-only and
   require all-parameter correctness for full admission?
3. Does the repair subplan sufficiently forbid admitting old T=2 evidence and
   stale N=1000 evidence?
4. Are the stop conditions sufficient before Phase 3 fixed-SIR handoff?

## Pass Criteria

Return `VERDICT: AGREE` only if the repair subplan is safe to execute before
LGSSM score admission.

Return `VERDICT: REVISE` if directional FD is too weak without additional
conditions, if the schema extension is unsafe, or if any boundary is missing.
