# Phase 4 Subplan: Adapter Derivation Audit

Date: 2026-07-01

Status: DRAFT_SUBPLAN

## Phase Objective

Audit the actual-SV augmented-noise adapter derivation with MathDevMCP and
bounded Claude review.

## Entry Conditions Inherited From Previous Phase

- Phase 3 adapter derivation exists with labels.
- Phase 3 local checks passed or blockers were repaired.
- Phase 3 Claude review agreed the adapter derivation is boundary-safe, with a
  Phase 4 caveat to clarify whether the implementation-facing handoff consumes
  the stationary initial variance law or the scalar factor derivative.

## Required Artifacts

- MathDevMCP audit results for adapter labels.
- Claude review ledger entries.
- Phase 4 result.
- Refreshed Phase 5 implementation subplan.
- Implementation-facing derivative handoff note that lists the audited labels:
  `eq:bf-hd-actual-sv-srukf-augmented-variable`,
  `eq:bf-hd-actual-sv-srukf-augmented-law`,
  `eq:bf-hd-actual-sv-srukf-transition-map`,
  `eq:bf-hd-actual-sv-srukf-observation-map`,
  `eq:bf-hd-actual-sv-srukf-transition-derivatives`,
  `eq:bf-hd-actual-sv-srukf-observation-state-derivative`,
  `eq:bf-hd-actual-sv-srukf-observation-parameter-derivatives`,
  `eq:bf-hd-actual-sv-srukf-initial-law`,
  `eq:bf-hd-actual-sv-srukf-initial-derivatives`,
  `eq:bf-hd-actual-sv-srukf-initial-factor-derivatives`,
  `eq:bf-hd-actual-sv-srukf-surrogate-loglik`,
  `eq:bf-hd-actual-sv-srukf-score-handoff`,
  `eq:bf-hd-actual-sv-srukf-collapsed-law-equivalence`, and
  `eq:bf-hd-actual-sv-srukf-nonclaims`.

## Required Checks/Tests/Reviews

- MathDevMCP label lookup, typed obligation, and derivation audit checks.
- Claude read-only review of exactly the adapter derivation path/section.
- Local `rg` checks for forbidden claims and score-admission boundaries.
- Focused check that the initial handoff explicitly distinguishes the variance
  derivative
  `d sigma^2/(1-gamma^2)` from any scalar factor derivative needed by the
  factor-propagating backend.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the actual-SV adapter derivation survive audit for target law, dimensions, derivatives, and nonclaim boundaries? |
| Baseline/comparator | Phase 3 derivation and existing `ch18b` structural UKF law. |
| Primary criterion | No material MathDevMCP or Claude audit blocker remains unresolved. |
| Veto diagnostics | Wrong augmented variable, missing derivative, dimension mismatch, unclarified variance-vs-factor initial derivative handoff, exact-likelihood claim, or hidden autodiff/SVD/principal-root dependency. |
| Explanatory diagnostics | Notation improvements and implementation hints. |
| Not concluded | Implementation and numerical tests remain pending. |
| Artifact | Phase 4 audit result and review ledger. |

## Skeptical Plan Audit Before Execution

- Wrong baseline risk: the audit must compare against the declared raw
  Gaussian-closure surrogate and structural UKF law, not against the exact
  transformed actual-SV target as if they were the same scalar.
- Proxy-promotion risk: MathDevMCP structural consistency, Claude agreement,
  and local `rg` checks are audit evidence only; none can admit code,
  leaderboard rows, HMC readiness, or exact-likelihood claims.
- Missing stop-condition risk: stale MathDevMCP caches may produce fallback
  context; fallback is acceptable as diagnostic evidence only if the Phase 4
  result records it and does not overclaim formal proof.
- Fair-comparison risk: historical SVD, strict-SPD principal-root, and
  `GradientTape` routes may be mentioned only as excluded diagnostic routes.
- Hidden-assumption risk: the initial variance derivative must be reconciled
  with any scalar factor derivative required by the implementation handoff.
- Artifact-answer risk: a Phase 4 result must list exact labels audited and
  unresolved proof-backend limitations; otherwise it does not answer the
  stated audit question.

Audit status before execution:

- PASSED_FOR_PHASE_4_START. The subplan has explicit target boundary, vetoes,
  local/MathDevMCP/Claude checks, label artifacts, and the
  variance-vs-factor caveat inherited from Phase 3.

## Forbidden Claims/Actions

- Do not implement code.
- Do not admit leaderboard rows.
- Do not treat Claude agreement as scientific proof.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if adapter audit converges and Phase 5 implementation
scope is refreshed to exactly match the audited derivation.

## Stop Conditions

- Same material adapter blocker persists after five review rounds.
- Same material MathDevMCP audit blocker persists after five focused repair
  attempts.
- MathDevMCP cannot audit the required labels.

## End-Of-Phase Procedure

1. Run required checks.
2. Write Phase 4 result/close record.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 5 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
