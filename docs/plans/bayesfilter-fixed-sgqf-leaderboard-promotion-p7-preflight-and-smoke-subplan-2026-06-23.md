# Phase P7 Subplan: Preflight And Smoke Refresh

metadata_date: 2026-06-23
status: DRAFT_PENDING_P6_HANDOFF_AND_LOCAL_CHECKS
master_program: docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
phase: P7
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Refresh preflight/smoke governance artifacts after the P6 machine-readable SGQF
integration so the SGQF roster and KSC tiny-scope score qualifier remain
consistent before any later runner/numeric phases.

## Entry Conditions Inherited From Previous Phase

- P6 result status is
  `PASS_P6_FIXED_SGQF_MATRIX_INTEGRATION_COMPLETE` or a reviewed equivalent pass
  token.
- P6 added `fixed_sgqf` to the preflight frozen roster and aligned the KSC row
  across deterministic coverage, smoke payloads, and preflight semantics.
- The visible execution ledger and visible stop handoff were updated through P6.
- Any P6 bounded-review findings were patched and the P6 packet rechecked.

## Required Artifacts

- Phase P7 result / close record:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p7-preflight-and-smoke-result-2026-06-23.md`
- Refreshed Phase P8 subplan:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p8-numeric-ledger-and-runner-subplan-2026-06-23.md`
- Visible execution ledger entry
- Review-ledger entry
- Visible stop handoff update

## Required Checks, Tests, And Reviews

Local checks:
```bash
git diff --check -- docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p7-preflight-and-smoke-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p7-preflight-and-smoke-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p8-numeric-ledger-and-runner-subplan-2026-06-23.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-smoke-payloads-2026-06-10.json
```

Required review:
- bounded read-only review on the exact P7 packet after the P7 result and P8
  subplan are written.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the preflight and smoke artifacts now carry the SGQF roster and KSC tiny-scope analytical-score qualifier consistently, while remaining non-performance evidence? |
| Baseline/comparator | The P6 result, preflight matrix artifact, deterministic smoke payload artifact, and preflight-matrix tests. |
| Primary pass criterion | P7 records that the refreshed preflight/smoke artifacts remain internally consistent, preserve non-performance-evidence status, and keep the KSC tiny-scope qualifier visible without widening it. |
| Veto diagnostics | widened KSC score scope, loss of no-silent-holes discipline, or any preflight/smoke artifact drifting into performance-evidence wording. |
| Explanatory diagnostics | preflight roster status, smoke payload consistency, nonclaims, review verdict. |
| Not concluded | No numeric benchmark execution yet, no runner-matrix completion yet, no broad family-score expansion beyond KSC. |
| Artifact preserving result | P7 result, visible execution ledger, review ledger, visible stop handoff, refreshed P8 subplan. |

## Forbidden Claims And Actions

- Do not treat preflight or smoke artifacts as performance evidence.
- Do not widen the KSC analytical-score scope beyond the tiny declared surrogate fixture.
- Do not run numeric benchmark ladders in P7.

## Exact Next-Phase Handoff Conditions

Advance to P8 only if:
- the refreshed P7 result records preflight/smoke consistency,
- the KSC tiny-scope qualifier remains explicit,
- non-performance-evidence wording remains intact,
- P8 subplan exists,
- bounded review agrees or is repaired within the P7 loop.

## Stop Conditions

Stop if preflight/smoke wording now overclaims performance evidence, if the KSC
scope is widened silently, or if review finds an unpatchable governance mismatch.

## End-Of-Phase Protocol

1. Run focused local checks.
2. Write the P7 result.
3. Draft/refresh the P8 subplan.
4. Update ledgers/handoff.
5. Run bounded review.
6. Patch and rerun if needed.
7. Advance only if handoff conditions hold.
