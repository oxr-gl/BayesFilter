# Phase 2 Subplan: Generic Derivation Audit

Date: 2026-07-01

Status: DRAFT_SUBPLAN

## Phase Objective

Audit the generic SR-UKF derivation with MathDevMCP and bounded Claude review
until convergence or a documented blocker.

## Entry Conditions Inherited From Previous Phase

- Phase 1 generic derivation exists with labels.
- Phase 1 result records local checks and any Claude findings.

## Required Artifacts

- MathDevMCP audit transcript or summarized result entries for each material
  label.
- Claude review ledger entries.
- Phase 2 result.
- Refreshed Phase 3 adapter derivation subplan.

## Required Checks/Tests/Reviews

- MathDevMCP `latex_label_lookup`, `typed_obligation_label`,
  `audit_derivation_v2_label`, and targeted equality checks where applicable.
- Claude read-only review of exactly the generic derivation path/section.
- Local `rg` checks that nonclaims and forbidden routes remain explicit.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the generic derivation survive formal/local audit for dimensions, factor reconstruction, derivative flow, and boundary safety? |
| Baseline/comparator | Phase 1 derivation and existing factor derivative contracts. |
| Primary criterion | No material MathDevMCP obligation or Claude `REVISE` remains unresolved. |
| Veto diagnostics | Unresolved dimension mismatch, missing derivative object, unsupported factor reconstruction, or route drift. |
| Explanatory diagnostics | Minor notation requests and nonblocking clarity improvements. |
| Not concluded | Actual-SV adapter and implementation remain unaudited. |
| Artifact | Phase 2 audit result and review ledger. |

## Forbidden Claims/Actions

- Do not implement code.
- Do not promote the generic derivation to actual-SV readiness.
- Do not use Claude as execution authority.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if MathDevMCP and Claude converge or remaining issues
are explicitly classified as nonblocking notation issues.

## Stop Conditions

- Same material audit blocker persists after five Claude review rounds or
  focused repair attempts.
- Same material MathDevMCP audit blocker persists after five focused repair
  attempts.
- MathDevMCP cannot locate labels needed to audit the derivation.

## End-Of-Phase Procedure

1. Run required local and MathDevMCP checks.
2. Write Phase 2 result/close record.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
