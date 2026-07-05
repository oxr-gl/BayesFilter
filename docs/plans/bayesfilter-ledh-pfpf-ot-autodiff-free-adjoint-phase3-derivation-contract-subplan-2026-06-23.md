# Phase 3 Subplan: Derivation Contract

status: DRAFT_READY_FOR_REVIEW_AFTER_P2
date: 2026-06-23
phase: P3-DERIVATION-CONTRACT

## Phase Objective

Write the full filter-level manual adjoint contract: forward checkpoints,
reverse-time recursion, primitive adjoint interfaces, and proof obligations.
This phase is documentation/derivation only. It inherits the reviewed master
program and visible runbook constraints and may not widen scope, reinterpret
phase boundaries, weaken the P2 audit contract, or treat derivation text as an
implementation, GPU, FD, or scientific-validity result.

## Entry Conditions

- P2 audit tooling exists and blocks current leaking route.
- No implementation phase may bypass the audit.
- P2 audit result decision is `FAIL_CURRENT_ROUTE`, as expected for the
  negative control.
- P3 must not redefine audit pass/fail criteria; it must consume the audit
  contract and specify manual adjoints that can later satisfy it.

## Required Artifacts

- Derivation contract:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-derivation-contract-2026-06-23.md`.
- Optional LaTeX crosswalk anchors to `docs/chapters/ch32c2_ledh_pfpf_ot_custom_gradient.tex`.
- P3 result artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase3-derivation-contract-result-2026-06-23.md`.
- Refreshed P4/P5/P6 subplans.
- Audit-contract crosswalk mapping P1/P2 leak classes to derivation
  obligations.

The derivation contract must contain mandatory sections for:

- outer filter objective adjoint replacing P1-L001/P1-L003;
- log-weight normalization and particle-weight adjoints;
- LEDH proposal/flow/log-Jacobian adjoints;
- transport/Sinkhorn/blockwise adjoints replacing P1-L013/P1-L015;
- forward checkpoint inventory and memory ownership;
- reverse-time recursion boundaries and primitive adjoint interfaces;
- leak-to-obligation crosswalk with audit requirements;
- unresolved proof, implementation, and validation questions.

The P3 result artifact must include a decision table, inspection/run manifest
for the doc-only checks, nonclaims, unresolved uncertainties, and exact next
phase gates. The refreshed P4/P5/P6 subplans must inherit the no-production
autodiff invariant, P2 audit contract, and P3 leak-to-obligation crosswalk.

## Required Checks/Tests/Reviews

- Local search for relevant LaTeX labels/sections.
- MathDevMCP or local derivation-audit tool where applicable.
- Bounded Claude review focused on completeness and boundary safety.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the manual adjoint specified enough to implement without autodiff? |
| Baseline/comparator | P0 contract, P1 leak ledger, P2 audit. |
| Primary criterion | Every primitive needed by the filter backward pass has an owner, input/output adjoint shape, stop condition, and audit requirement that would eliminate or block the corresponding P1/P2 leak. |
| Veto diagnostics | Missing outer filter objective adjoint replacing P1-L001/P1-L003; missing log-weight normalization adjoint; missing LEDH flow adjoint; missing transport adjoint replacing P1-L013/P1-L015; hidden autodiff fallback. |
| Explanatory only | Tiny autodiff parity obligations for later tests. |
| Not concluded | No implementation correctness. |
| Preserved artifact | Derivation contract and P3 result artifact paths listed above. |

## Forbidden Claims/Actions

- Do not claim mathematical proof without derivation or anchored citation.
- Do not permit autodiff fallback in production route.
- Do not run GPU/FD.
- Do not edit production route code in P3.
- Do not run FD, actual-gradient, HMC, posterior-correctness, or performance
  validation.
- Do not claim that a written adjoint contract certifies no-autodiff execution;
  certification remains gated by later implementation and audit phases.

## Exact Next-Phase Handoff Conditions

Advance to P4 only if the P3 result and derivation contract explicitly provide:

- forward checkpoint inventory and memory ownership sufficient for later
  implementation phases;
- reverse-time recursion boundaries and primitive adjoint interfaces;
- mandatory adjoint sections for the outer objective, log weights, LEDH flow,
  and transport/Sinkhorn/blockwise transport;
- a leak-to-obligation crosswalk covering P1-L001/P1-L003 and P1-L013/P1-L015;
- exact P4 analytical SIR derivative obligations and acceptance boundaries;
- unresolved proof-vs-implementation questions that must remain blockers
  rather than hidden autodiff fallbacks.

## Stop Conditions

- Derivation gaps prevent implementation boundary definition.
- Claude/Math review does not converge.
- Any required P1/P2 leak class has no derivation owner.
- Any hidden autodiff dependency remains unassignable on paper.
- Completing P3 would require production code repair, GPU execution, FD
  evidence, actual-gradient validation, or broad repository review.
- The P3 scope conflicts with the reviewed master program, visible runbook, P0
  contract, P1 leak ledger, or P2 audit contract.
