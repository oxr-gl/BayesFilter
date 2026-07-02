# Phase R2 Subplan: Contract E Reset VJP Decision

Date: 2026-06-29

Status: `DRAFT_HANDOFF_FROM_R1`

## Phase Objective

Isolate the Contract E reset map and decide whether its derivative boundary can
be implemented manually, must be deliberately stopped with bias/nonclaims, or
must remain blocked.

## Entry Conditions Inherited From R1

- R1 design and route manifest exist.
- Every Contract E reset sub-boundary is listed individually.
- Material Phase 3 remains blocked by
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.

## Required Artifacts

- Local reset map derivation note.
- Tiny local reset VJP diagnostic or blocker.
- Updated route manifest section for Contract E reset policy with one row for
  each E01-E14 reset sub-boundary.
- Per-sub-boundary decision table recording terminal classification, evidence
  artifact, FD parity requirement/status, fixed-rank/interior-only scope, and
  nonclaim or blocker text.
- R2 result.

## Required Checks, Tests, And Reviews

- Claude bounded read-only review before implementation.
- Local finite-difference parity check for any proposed manual reset VJP.
- Static check that no generic score autodiff or reset autodiff fallback is
  introduced.
- Static check that updated route manifest still records
  `material_gate_authorized=false`,
  `material_blocker_code=PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`,
  and the rule that R2 cannot unblock material mode.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the Contract E reset derivative be represented safely without generic autodiff? |
| Baseline/comparator | Local same-map finite differences on tiny fixtures. |
| Primary pass criterion | Each gradient-bearing reset sub-boundary E01-E13 has an explicit terminal classification: `manual_vjp_implemented`, `stop_gradient_by_design`, or `blocked`; E14 remains `non_gradient_monitor`. |
| Veto diagnostics | Nonfinite local VJP, hidden `GradientTape`, hidden eigensystem autodiff, missing reset sub-boundary. |
| Not concluded | Full Phase 3 LGSSM gradient correctness or material readiness. |

## Decision-Type Evidence Requirements

- `manual_vjp_implemented`: requires a local same-map FD parity check on a tiny
  deterministic fixture, with explicit slope/error reporting and finite VJP
  values.
- `stop_gradient_by_design`: requires a bias/nonclaim rationale explaining
  which derivative contribution is omitted and why this cannot be promoted as
  the full Contract E gradient without later evidence.
- `blocked`: requires an exact unresolved-boundary blocker statement naming the
  sub-boundary and why the derivative is unsafe, unjustified, or not yet
  derived.
- `non_gradient_monitor`: allowed only for diagnostics that do not feed the
  material score route, currently E14.

## Spectral-Boundary Safety Rule

Any manual VJP claim touching E05, E07, E10, E11, or another eigensystem-derived
quantity must be explicitly scoped to a fixed local spectral class:

- retained rank and projector branch must be unchanged in the local fixture;
- no eigenvalue may cross the spectral floor in the tested perturbation range;
- floor/rank-switch cases must be classified as `blocked` or
  `stop_gradient_by_design` with a nonclaim ledger;
- TensorFlow autodiff through `eigh`, eigenvector branches, square roots, or
  pseudo-inverse square roots is not an acceptable hidden fallback.

## Forbidden Claims And Actions

- Do not remove or weaken the material Phase 3 blocker in R2.
- Do not run material Phase 3.
- Do not claim gradient correctness from a local reset check.
- Do not classify E14 as gradient-bearing unless a later reviewed plan changes
  the material route to use diagnostic monitors in the score, which R2 does not
  authorize.

## Exact Next-Phase Handoff Conditions

Advance to R3 only if the reset policy is reviewed, each E01-E14 row has
per-sub-boundary evidence, and the material blocker is still in force in the
updated manifest.  R3 must implement the full manual likelihood reverse scan
and then pass route audit before material mode can be considered.

## Stop Conditions

Stop if any reset sub-boundary cannot be classified, if a proposed reset VJP
requires hidden generic autodiff, if a spectral/rank-switch boundary is treated
as smooth without evidence, or if the updated manifest weakens the material
blocker.
