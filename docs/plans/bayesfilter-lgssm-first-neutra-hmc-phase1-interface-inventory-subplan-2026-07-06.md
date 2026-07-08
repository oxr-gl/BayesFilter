# BayesFilter LGSSM-First NeuTra/HMC Phase 1 Subplan

Date: 2026-07-06

## Phase Objective

Inventory current BayesFilter generic SSM target, LGSSM Kalman, transport, and
HMC surfaces, then decide the smallest safe Phase 2 implementation boundary for
an exact LGSSM target adapter.

## Entry Conditions Inherited From Previous Phase

- Phase 0 has passed launch review.
- DSGE/c603 is explicitly deferred to Phase 9 stress only.
- No HMC, GPU, training, or package/environment mutation has been run.

## Required Artifacts

- Phase 1 inventory result:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase1-interface-inventory-result-2026-07-06.md`
- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase2-lgssm-target-adapter-subplan-2026-07-06.md`
- Phase 1 review bundle:
  `docs/reviews/bayesfilter-lgssm-first-neutra-hmc-phase1-review-bundle-2026-07-06.md`

## Required Checks/Tests/Reviews

- Read-only inventory of:
  - `bayesfilter/ssm/contracts.py`;
  - `bayesfilter/ssm/target_builder.py`;
  - `bayesfilter/linear/kalman_qr_tf.py`;
  - `bayesfilter/linear/kalman_qr_derivatives_tf.py`;
  - `bayesfilter/inference/fixed_transport_hmc.py`;
  - `bayesfilter/testing/tf_hmc_readiness.py`;
  - relevant tests.
- Local text checks that inventory result classifies each surface as
  `reuse`, `patch_needed`, or `blocked`.
- Bounded read-only review of the inventory and Phase 2 handoff.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What existing BayesFilter surfaces can be reused for an LGSSM-first target adapter and what gaps must Phase 2 close? |
| Baseline/comparator | Current `SSMTargetContract`, `GenericSSMPosteriorAdapter`, QR Kalman code, fixed-transport mechanics, and QR static LGSSM HMC smoke harness. |
| Primary criterion | Inventory classifies reusable surfaces and defines an exact Phase 2 implementation/test boundary without DSGE/c603 dependency. |
| Veto diagnostics | Treating opt-in HMC smoke as readiness, ignoring exact Kalman reference needs, hidden DSGE dependency, missing target-signature policy, or unreviewed GPU/training/HMC execution. |
| Explanatory diagnostics | File/symbol anchors, existing tests, target signature surfaces, gap table. |
| Not concluded | No new implementation correctness, no LGSSM posterior validation, no HMC readiness, no NeuTra readiness. |
| Artifact | Phase 1 result and refreshed Phase 2 subplan. |

## Forbidden Claims/Actions

- Do not edit algorithm code in Phase 1 unless the review loop explicitly
  patches planning artifacts.
- Do not run HMC, NeuTra training, GPU/CUDA, package installation, or git
  commit/push.
- Do not claim current QR static LGSSM smoke is a generic BayesFilter HMC
  solution.
- Do not bring DSGE/c603 back into Phase 2 except as a deferred-stress note.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if Phase 1:

- identifies the exact LGSSM target adapter boundary;
- lists required tests/checks;
- preserves CPU-only and nonclaim boundaries;
- passes review or records a fixable blocker that has been repaired.

## Stop Conditions

Stop if current surfaces cannot support a scoped LGSSM target adapter without
major redesign, if target signature or batch value/score authority is unclear,
if review does not converge after five rounds, or if proceeding requires
unapproved HMC/GPU/training/package/git work.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 1 result;
3. draft or refresh Phase 2 subplan;
4. review Phase 2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
