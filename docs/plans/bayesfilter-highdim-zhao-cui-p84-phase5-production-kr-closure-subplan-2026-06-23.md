# P84 Phase 5 Subplan: Production KR Closure

Date: 2026-06-23

Status: `DRAFT_BLOCKED_PENDING_PHASE4`

## Phase Objective

Replace, certify, or keep blocked the current diagnostic grid-CDF KR route.

## Entry Conditions Inherited From Previous Phase

- Current metadata still states `production_kr_closure=False`.
- Proposal correction must remain through `eval_pdf` on local samples.

## Required Artifacts

- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase5-production-kr-closure-result-2026-06-23.md`
- KR closure manifest and tests if repaired.
- Updated execution ledger and Phase 6 subplan.

## Required Checks / Tests / Reviews

```bash
rg -n "production_kr_closure|conditional_cdf_route_class|numerical_grid_trapezoid_bisection|eval_pdf_on_local_samples|proposal_density_backend" \
  bayesfilter/highdim \
  tests/highdim \
  docs/plans -S
```

Claude review is required before changing production KR metadata.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the KR conditional/inversion route be certified as production, or must it remain diagnostic? |
| Baseline/comparator | P83 metadata, author source route, and any reviewed KR replacement. |
| Primary criterion | Production KR manifest and tests pass, or blocker preserves `production_kr_closure=False`. |
| Veto diagnostics | Base-density proposal shortcut, unreviewed metadata flip, non-monotone CDF, missing source anchors. |
| Explanatory diagnostics | CDF monotonicity, inversion residuals, mass checks, proposal correction ranges. |
| Not concluded | No production readiness without all later gates. |
| Artifact | KR result and manifest. |

## Forbidden Claims / Actions

- Do not set `production_kr_closure=True` without reviewed evidence.
- Do not replace `eval_pdf` correction with base-density-only correction.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if KR status is explicitly pass or blocked.

## Stop Conditions

Stop if KR production semantics cannot be certified.
