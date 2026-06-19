# P8h Phase 2 Subplan: Algorithm And Evidence Contract

Date: 2026-06-15

Status: `PASS_REVIEWED`

## Phase Objective

Specify route identifiers, OT trigger policy, transport diagnostics, Algorithm 1
covariance auxiliary-state carry, gradient contract, and forbidden claims before
code changes.

## Entry Conditions

- Phase 1 governance reset passed.

## Required Artifacts

- Phase 2 design contract JSON/Markdown under `docs/plans` naming exact
  implementation entry points for Algorithm 1 covariance carry, OT
  trigger/resampler hookup, and PF-PF correction attachment.
- Phase 2 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase2-algorithm-design-contract-result-2026-06-15.md`.

## Required Checks, Tests, Reviews

- `git diff --check`.
- Search/code inspection showing existing OT/Sinkhorn APIs, Algorithm 1
  covariance fields, and PF-PF correction entry points are cited.
- Claude read-only review of the design contract.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the OT-resampled Algorithm 1 LEDH route sufficiently specified before implementation? |
| Baseline/comparator | Algorithm 1 UKF implementation, Corenflos/Sinkhorn components, historical LEDH-PFPF-OT tests. |
| Primary criterion | Design states route IDs, exact implementation entry points, state carry, OT trigger/resampler hookup, PF-PF correction attachment, diagnostics, gradient semantics, and stop rules. |
| Veto diagnostics | Missing covariance carry; undefined OT trigger; unsupported gradient/HMC claims; ambiguous artifacts. |
| Explanatory diagnostics | API inspection and reviewer notes. |
| Not concluded | No implementation pass, value adequacy, performance conclusion, gradient correctness, GPU scaling, HMC readiness, stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, generic high-dimensional readiness, production readiness, or filter ranking. |

## Forbidden Claims And Actions

- Do not implement before this design contract passes review.
- Do not classify OT auxiliary-state carry as source-faithful Li-Coates unless
  explicitly limited to the Algorithm 1 covariance lifecycle plus Corenflos
  integration.
- Do not promote no-resampling/fixed-randomness artifacts beyond historical
  diagnostics.
- Do not treat classical categorical resampling as a pathwise-gradient route;
  it remains an ESS/debug comparator in this lane.
- Do not claim the OT-resampled route is validated because the design contract
  names implementation entry points.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 only after the design contract is reviewed and names exact
implementation entry points for Algorithm 1 covariance carry, OT
trigger/resampler hookup, and PF-PF correction attachment.

## Stop Conditions

- The covariance carry rule cannot be specified without a new scientific claim
  requiring human decision.
