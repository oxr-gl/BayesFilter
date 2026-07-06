# BayesFilter LGSSM-First NeuTra/HMC Phase 6 Subplan

Date: 2026-07-06

## Phase Objective

Prepare the LGSSM NeuTra training gate after prior target, reference, and
fixed-transport mechanics gates pass. This phase may request or record explicit
training approval, but it must not train unless approval is already present.

## Entry Conditions Inherited From Previous Phase

- Phase 5 fixed-transport binding passed.
- Phase 5 review passed or a fixable blocker was visibly repaired.
- Explicit approval for training and any GPU use has not been assumed.

## Required Artifacts

- Approval/request result if training approval is absent:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-approval-request-2026-07-06.md`
- If explicit approval is later granted, a separate training execution subplan
  must be written before any training command.
- Phase 6 result:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-result-2026-07-06.md`
- Refreshed Phase 7 subplan.

## Required Checks/Tests/Reviews

- Check whether explicit training/GPU approval exists in the current user
  instruction.
- If absent, write approval request/stop result and do not run training.
- If present, write a separate reviewed training execution subplan with budget,
  seed, environment, CPU/GPU status, artifact paths, frozen artifact load check,
  downstream mechanics/reference check, and review before nonlinear SSM phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is BayesFilter authorized and prepared to train/freeze a NeuTra transport for LGSSM after mechanics gates passed? |
| Baseline/comparator | Phase 5 fixed transports and Phase 4 LGSSM reference target. |
| Primary criterion | If approval is absent, write a clear approval request and stop before training; if approval is present, write a reviewed execution subplan before training. |
| Veto diagnostics | Any training command without explicit approval, GPU use without trusted approval, missing budget/artifact paths, or training loss promoted to posterior correctness. |
| Explanatory diagnostics | Proposed budget, runtime target, seeds, artifact paths, CPU/GPU choice. |
| Not concluded | Sampler superiority, broad nonlinear SSM validity, production readiness. |
| Artifact | Phase 6 result and approval/request artifact; later training artifacts only after approval. |

## Forbidden Claims/Actions

- Do not train without explicit approval.
- Do not use GPU without trusted approval.
- Do not claim training loss proves correctness.
- Do not use DSGE/c603 material.
- Do not continue to nonlinear SSM phases by treating synthetic fixed transports
  as learned NeuTra training evidence.

## Exact Next-Phase Handoff Conditions

Phase 7 may begin only after either:

- LGSSM NeuTra training is explicitly approved, executed under a reviewed
  subplan, frozen, loaded, and checked; or
- the master program is intentionally amended to skip learned NeuTra training
  for now under explicit human direction.

## Stop Conditions

Stop if approval is absent, if a training execution plan is not reviewed, if
artifacts are invalid, if target signatures mismatch, or if review does not
converge after five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 6 result;
3. draft or refresh Phase 7 subplan;
4. review Phase 7 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
