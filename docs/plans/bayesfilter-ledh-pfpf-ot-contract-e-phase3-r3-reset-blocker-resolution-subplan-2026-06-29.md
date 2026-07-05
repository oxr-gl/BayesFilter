# Phase R3 Subplan: Contract E Reset Blocker Resolution

Date: 2026-06-29

Status: `DRAFT_HANDOFF_FROM_R2`

## Phase Objective

Resolve the R2 Contract E reset VJP blocker before any material Phase 3 route is
implemented or unblocked.  R3 must choose and justify exactly one reset
derivative policy:

- `fixed_rank_manual_vjp`: derive and implement the reset VJP for E01-E13 under
  a fixed local spectral class, then pass local same-map FD parity; or
- `reviewed_stop_gradient_policy`: deliberately stop selected reset derivative
  contributions with explicit bias/nonclaim text and owner-visible limitations.

If neither policy converges, R3 must close as blocked.

R3 is still a local reset-policy phase.  It does not authorize GPU runs,
full-filter finite differences, Kalman comparisons, material Phase 3 execution,
or production gradient evidence.  Any numerical check in R3 must be a local
tiny reset-fixture check unless a later reviewed subplan explicitly changes
scope.

## Entry Conditions Inherited From R2

- R2 decision note and manifest exist.
- E01-E13 are classified as `blocked`.
- E14 is classified as `non_gradient_monitor`.
- Material Phase 3 remains blocked by
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.
- R2 did not authorize a reset VJP, stop-gradient policy, GPU run, full-filter
  FD, Kalman comparison, or material gradient evidence.

## Required Artifacts

- Reset derivative policy design note.
- If choosing `fixed_rank_manual_vjp`:
  - derivation of E01-E13 adjoints;
  - fixed spectral-class assumptions for E05, E07, E10, E11;
  - local reset-map implementation;
  - local same-map FD parity artifact.
- If choosing `reviewed_stop_gradient_policy`:
  - exact stopped boundaries;
  - omitted-derivative bias ledger;
  - forbidden-claim ledger;
  - explicit statement that the resulting route is not the full Contract E
    gradient.
- Updated route manifest.
- R3 result / close record.
- R4 handoff subplan only if R3 produces a reviewed, test-backed reset policy.

## Required Checks, Tests, And Reviews

- Claude bounded read-only review of the R3 policy design before code changes.
- Static route audit preventing generic `tf.GradientTape`, Jacobian,
  `ForwardAccumulator`, or `transport_ad_mode=full` from entering the reset
  path, eigensystem boundary, or material score route.
  The audit scope is the reset path, eigensystem boundary, or material score route.
- For `fixed_rank_manual_vjp`, local same-map FD parity on deterministic tiny
  reset fixtures.
- For spectral boundaries, checks that retained rank, projector branch, and
  floor decisions are unchanged on the parity fixture.
- For `reviewed_stop_gradient_policy`, tests that the manifest records the
  stopped boundaries and nonclaims.
- JSON parse check for the updated manifest.
- `git diff --check` on touched artifacts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can Contract E reset have a safe differentiable policy for the manual likelihood reverse scan? |
| Baseline/comparator | Local same-map finite differences for fixed-rank manual VJP, or explicit bias/nonclaim ledger for stop-gradient policy. |
| Primary pass criterion | One reset policy is selected, reviewed, represented in the manifest, and backed by its required local evidence. |
| Veto diagnostics | Hidden generic autodiff, missing E01-E13 boundary, spectral rank/floor crossing treated as smooth, nonfinite local VJP, or any weakening of the material blocker. |
| Explanatory diagnostics | Conditioning, rank margins, covariance residuals, and reset sensitivity magnitudes. |
| Not concluded | Full Phase 3 LGSSM gradient correctness, nonlinear-model validity, HMC readiness, or production readiness. |
| Artifact preserving result | R3 result note plus updated manifest under `docs/plans`. |

## Forbidden Claims And Actions

- Do not remove or weaken the material Phase 3 blocker in R3.
- Do not run material Phase 3 before the reset policy is reviewed and local
  checks pass.
- Do not run GPU jobs in R3.
- Do not run full-filter finite differences in R3.
- Do not use anything larger than local tiny reset-fixture checks in R3.
- Do not use TensorFlow autodiff through eigensystems as a hidden material VJP.
- Do not claim Kalman, SIR, SV, HMC, or production correctness from a local
  reset-map check.
- Do not classify a stop-gradient policy as the full Contract E gradient.

## Exact Next-Phase Handoff Conditions

Advance to R4 only if R3 produces a reviewed reset policy, all required local checks pass, and the material blocker remains in force.  R4 may then plan the full manual likelihood reverse scan integration.  If R3 closes as blocked, no R4 implementation phase is authorized without human direction.

## Stop Conditions

Stop if the reset derivative policy requires hidden generic autodiff, if
spectral branch assumptions cannot be stated or checked, if local FD parity
fails for a claimed manual VJP, if stop-gradient bias cannot be bounded or
clearly documented, or if any artifact weakens the material blocker.
