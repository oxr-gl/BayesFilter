# BayesFilter NeuTra c603 Integration Phase 4 Subplan

Date: 2026-07-06

## Phase Objective

Generalize lessons from the c603-loaded artifact boundary into a documented
BayesFilter interface pattern for nonlinear SSM targets, BayesFilter filter
programs, frozen NeuTra transports, and mechanics/HMC-gate separation.

## Entry Conditions Inherited From Previous Phase

- Phase 3 mechanics-only checks pass or have a documented blocker that still
  informs interface design.
- c603 adapter limitations are explicitly recorded, including the synthetic
  base-adapter boundary used in the mechanics smoke.
- No scientific or production claims have been promoted from import/mechanics
  evidence.

## Required Artifacts

- Interface design note or API brief under `docs/plans/` that names the
  concrete target surfaces already in the repo:
  `SSMTargetContract`, `FilterProgram`, `FrozenTransportBinding`,
  `GenericSSMPosteriorAdapter`, and `FixedTransportValueScoreAdapter`.
- Optional code skeleton only if required by the reviewed result.
- Phase 4 result note:
  `docs/plans/bayesfilter-neutra-c603-integration-phase4-generic-interface-result-2026-07-06.md`.

## Required Checks, Tests, Reviews

- Text checks for required interface fields, artifact boundaries, and
  nonclaims.
- Review of the design note for hidden authority transfers, unsupported
  generality claims, and any accidental promotion of import/mechanics evidence
  into HMC or product claims.
- If code skeleton is added, focused import/API tests.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What generic BayesFilter interfaces are justified by c603 import/mechanics evidence, and what remains future work? |
| Baseline/comparator | Existing `SSMTargetContract`, `FilterProgram`, `FrozenTransportBinding`, dense-IAF loader, fixed-transport mechanics, and c603 adapter behavior. |
| Primary criterion | Design separates target identity, filter authority, transport payload, mechanics binding, and scientific/HMC validation gates. |
| Veto diagnostics | Claims that c603 proves arbitrary nonlinear SSM readiness, hidden default-policy changes, missing evidence gates, or conflating import with inference validity. |
| Explanatory diagnostics | Interface diagrams/tables, API candidates, test gap list. |
| Not concluded | No universal nonlinear SSM support, no production HMC readiness, no default policy change. |
| Artifact | Phase 4 result note and design artifact. |

## Forbidden Claims/Actions

- Do not claim support for any nonlinear SSM unless the interface states the
  exact required contracts.
- Do not claim a filter is HMC-ready without a reviewed value/score authority
  and separate HMC evidence plan.
- Do not make product/default changes.

## Exact Next-Phase Handoff Conditions

This is the final planned phase. Handoff is complete only if:

- result note lists completed phases, tests, reviews, unresolved blockers,
  concrete interface boundaries, and nonclaims;
- any next implementation program is explicitly separated from this c603
  integration program.

## Stop Conditions

Stop if:

- the design would require unreviewed scientific claims;
- material API decisions require user direction;
- review does not converge after five rounds for the same material blocker.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 4 result;
3. update final visible handoff;
4. review final decision for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
