# Phase P8 Subplan: Numeric Ledger And Runner Refresh

metadata_date: 2026-06-23
status: DRAFT_PENDING_P7_HANDOFF_AND_LOCAL_CHECKS
master_program: docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
phase: P8
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Refresh the runner/numeric-ledger governance artifacts so the SGQF KSC row is
represented consistently in downstream status/numeric matrices, without turning
preflight or smoke evidence into benchmark ranking claims.

P8 remains a governance/runner-artifact phase unless a later reviewed artifact
opens a real numeric benchmark execution path.

## Entry Conditions Inherited From Previous Phase

- P7 result status is
  `PASS_P7_FIXED_SGQF_PREFLIGHT_COMPLETE` or a reviewed equivalent pass token.
- P7 preserved the KSC tiny-scope qualifier and non-performance-evidence wording
  through preflight/smoke artifacts.
- The visible execution ledger and visible stop handoff were updated through P7.
- Any P7 bounded-review findings were patched and the P7 packet rechecked.

## Required Artifacts

- Phase P8 result / close record:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p8-numeric-ledger-and-runner-result-2026-06-23.md`
- Refreshed Phase P9 subplan:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p9-closeout-subplan-2026-06-23.md`
- Visible execution ledger entry
- Review-ledger entry
- Visible stop handoff update

## Required Checks, Tests, And Reviews

Local checks:
```bash
git diff --check -- docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p8-numeric-ledger-and-runner-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p8-numeric-ledger-and-runner-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p9-closeout-subplan-2026-06-23.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json
```

Required review:
- bounded read-only review on the exact P8 packet after the P8 result and P9
  subplan are written.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the downstream runner/numeric-ledger governance artifacts represent the SGQF KSC row consistently with the refreshed deterministic/preflight stack, without implying that a new numeric benchmark execution occurred? |
| Baseline/comparator | The existing P8 runner-matrix artifact, the P7 result, and the refreshed deterministic/preflight SGQF artifacts. |
| Primary pass criterion | P8 updates downstream SGQF status/numeric-ledger artifacts so the KSC row no longer contradicts the deterministic/preflight stack, while preserving explicit nonclaims that no new numeric benchmark execution occurred. |
| Veto diagnostics | any widened KSC scope, any implication that a new numeric benchmark was run when it was not, or any runner artifact that silently drops SGQF again. |
| Explanatory diagnostics | changed SGQF runner cells, unchanged no-performance-evidence status, review verdict. |
| Not concluded | No new numeric benchmark execution, no benchmark ranking, no broad family-score expansion beyond KSC. |
| Artifact preserving result | P8 result, refreshed runner artifact(s), visible execution ledger, review ledger, visible stop handoff, refreshed P9 subplan. |

## Forbidden Claims And Actions

- Do not claim that a new numeric benchmark execution occurred unless it actually did.
- Do not widen the KSC tiny-scope analytical-score admission.
- Do not turn runner-matrix status refresh into benchmark ranking.

## Exact Next-Phase Handoff Conditions

Advance to P9 only if:
- the runner/numeric-ledger artifacts no longer contradict the refreshed SGQF
  deterministic/preflight stack,
- the KSC tiny-scope qualifier remains explicit,
- explicit nonclaims about no new numeric execution remain intact,
- P9 subplan exists,
- bounded review agrees or is repaired within the P8 loop.

## Stop Conditions

Stop if the downstream runner artifact cannot be reconciled honestly without
claiming an unrun benchmark, if the KSC scope is widened silently, or if review
finds an unpatchable governance mismatch.

## End-Of-Phase Protocol

1. Run focused local checks.
2. Write the P8 result.
3. Draft/refresh the P9 subplan.
4. Update ledgers/handoff.
5. Run bounded review.
6. Patch and rerun if needed.
7. Advance only if handoff conditions hold.
