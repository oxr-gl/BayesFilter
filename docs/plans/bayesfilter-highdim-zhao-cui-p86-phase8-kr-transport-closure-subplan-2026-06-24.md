# P86 Phase 8 Subplan: KR And Transport Closure

Date: 2026-06-24

Status: `DRAFT_BLOCKED_PENDING_PHASE7`

## Phase Objective

Replace, certify, or keep blocked the diagnostic KR/transport route for the
author algebraic `Lagrangep` SIR lane.

## Entry Conditions Inherited From Previous Phase

- Phase 7 correctness bridge status is recorded.
- Current metadata and code route for KR/transport proposal correction are
  inventoried.
- Any production metadata change requires reviewed evidence and owner approval
  if it changes product claims.

## Required Artifacts

- KR/transport closure manifest or blocker.
- Focused tests for monotonicity, inversion residuals, mass checks, and route
  identity if repaired.
- Phase 8 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase8-kr-transport-closure-result-2026-06-24.md`
- Updated execution ledger and refreshed Phase 9 subplan.

## Required Checks / Tests / Reviews

- Inventory:
  `production_kr_closure`, `conditional_cdf_route_class`,
  `numerical_grid_trapezoid_bisection`, `eval_pdf_on_local_samples`, and
  `proposal_density_backend`.
- Confirm proposal correction remains through `eval_pdf` on local samples if
  that is the reviewed route.
- CPU-hidden focused tests where feasible.
- Claude read-only bounded review before changing KR/transport status.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the author-route KR conditional/inversion and transport path be certified for production scope, or must it remain diagnostic? |
| Baseline/comparator | P83/P84 KR metadata, author source route, Phase 7 bridge scope, and any reviewed KR replacement. |
| Primary criterion | Production KR/transport manifest and tests pass, or blocker preserves diagnostic status and forbidden claims. |
| Veto diagnostics | Base-density proposal shortcut; unreviewed metadata flip; non-monotone CDF; inversion failure; missing source anchors; route mismatch. |
| Explanatory diagnostics | CDF monotonicity, inversion residuals, mass checks, proposal correction ranges, runtime. |
| Not concluded | No production readiness without derivative/HMC/comparator/scale/final decision gates. |
| Artifact | KR/transport result and manifest. |

## Forbidden Claims / Actions

- Do not set `production_kr_closure=True` without reviewed evidence.
- Do not replace `eval_pdf` correction with base-density-only correction unless
  explicitly reviewed and approved.
- Do not claim production readiness from KR closure alone.

## Exact Next-Phase Handoff Conditions

Phase 9 may begin only if:

- KR/transport status is explicitly pass, blocked, or out of final production
  scope by reviewed owner direction;
- derivative/HMC scope is refreshed with exact approval needs.

## Stop Conditions

Stop if:

- KR/transport semantics cannot be certified or bounded;
- metadata change would alter product claims without owner approval;
- Claude and Codex do not converge after five review rounds.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 8 result / close record;
3. draft or refresh the Phase 9 subplan;
4. review the Phase 9 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
