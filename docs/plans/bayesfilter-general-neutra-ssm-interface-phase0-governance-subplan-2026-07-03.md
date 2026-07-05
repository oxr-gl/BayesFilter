# Phase 0 Subplan: Governance, Scope, And Artifact Boundary

Date: 2026-07-03

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Freeze the master-program boundary, create the visible execution runbook and
review ledgers, verify that all phase subplans exist with required fields, and
record the artifact-reuse boundary before any implementation begins.

## Entry Conditions Inherited From Previous Phase

Phase 0 has no predecessor. It inherits only the current user request and the
BayesFilter governance policy:

- Codex is supervisor and executor.
- Claude is read-only reviewer only.
- GPU is the default execution target for NeuTra training.
- CPU-only runs must be explicit and must not be represented as training or
  performance evidence.
- Existing dirty worktree changes must be preserved.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-master-program-2026-07-03.md`
- Visible runbook:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-gated-execution-runbook-2026-07-03.md`
- Execution ledger:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-execution-ledger-2026-07-03.md`
- Claude review ledger:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-claude-review-ledger-2026-07-03.md`
- Stop handoff:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-stop-handoff-2026-07-03.md`
- Phase 0 result:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-result-2026-07-03.md`
- Phase subplans:
  - `docs/plans/bayesfilter-general-neutra-ssm-interface-phase0-governance-subplan-2026-07-03.md`
  - `docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-subplan-2026-07-03.md`
  - `docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-subplan-2026-07-03.md`
  - `docs/plans/bayesfilter-general-neutra-ssm-interface-phase3-filter-registry-subplan-2026-07-03.md`
  - `docs/plans/bayesfilter-general-neutra-ssm-interface-phase4-neutra-artifacts-subplan-2026-07-03.md`
  - `docs/plans/bayesfilter-general-neutra-ssm-interface-phase5-hmc-binding-subplan-2026-07-03.md`
  - `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-reuse-subplan-2026-07-03.md`
  - `docs/plans/bayesfilter-general-neutra-ssm-interface-phase7-validation-closeout-subplan-2026-07-03.md`

## Required Checks, Tests, And Reviews

Local checks:

- Verify every master-program phase has a subplan path.
- Verify every phase subplan contains all required headings.
- Verify the visible runbook contains role contract, state machine, evidence
  contract, repair loop, and human-required stop conditions.
- Verify no planned Phase 0 command launches training, HMC, detached execution,
  or package installation.

Authoritative required subplan headings for the Phase 0 local check:

- `## Phase Objective`;
- `## Entry Conditions Inherited From Previous Phase`;
- `## Required Artifacts`;
- `## Required Checks, Tests, And Reviews`;
- `## Evidence Contract`;
- `## Forbidden Claims And Actions`;
- `## Exact Next-Phase Handoff Conditions`;
- `## Stop Conditions`.

Review:

- Claude read-only review of this Phase 0 subplan.
- Claude read-only review of the Phase 1 subplan before crossing to Phase 1.
- Maximum five review rounds for the same blocker.

Repair loop:

- Trigger: any local check failure, Claude `VERDICT: REVISE`, missing artifact,
  missing required heading, boundary mismatch, or unsupported claim.
- Owner: Codex is the only repair executor.
- Repair artifact: patch the same subplan or planning artifact that contains
  the defect, and record the patch in the execution ledger.
- Focused check: rerun only the local check that can falsify the repaired
  defect, then rerun the bounded Claude review for material review blockers.
- Re-review condition: any material subplan or next-phase handoff changed by the
  repair must be reviewed again by Claude unless the review command itself is
  blocked by a human-required boundary.
- Escalation condition: after five Claude review rounds for the same blocker,
  write a blocker result and stop.
- Blocker write-up path: use the current phase result path and the visible stop
  handoff path listed under Required Artifacts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the generic NeuTra SSM interface program boundary, phase artifacts, and review loop complete enough to begin Phase 1 implementation safely? |
| Baseline/comparator | User-requested protocode plus local visible-gated execution template. |
| Primary pass criterion | Required artifacts exist, subplan required-section check passes, Claude review returns `VERDICT: AGREE` for Phase 0 and Phase 1 boundary or a documented blocker is written. |
| Veto diagnostics | Missing required subplan section, missing runbook state machine, absent stop conditions, Claude role drift, plan authorizes CPU-hidden training, plan authorizes detached execution without separate approval, or plan treats review as execution authority. |
| Explanatory diagnostics | File counts, line anchors, review round count, and local check output. |
| Not concluded | No interface implementation, no target correctness, no HMC readiness, no NeuTra training readiness, no artifact reuse success. |
| Artifacts | Phase 0 result, execution ledger, Claude review ledger, Phase 1 subplan. |

## Forbidden Claims And Actions

- Do not implement production code in Phase 0.
- Do not launch NeuTra training or HMC.
- Do not run GPU/CUDA probes in Phase 0 unless a later reviewed subplan requires
  them.
- Do not call Claude an execution authority.
- Do not claim posterior validity, HMC convergence, default readiness, or
  generic all-filter support.
- Do not paste whole files into Claude prompts.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- Phase 0 result is written with `PHASE0_GATE_PASSED`;
- master program and visible runbook exist;
- all phase subplans exist and contain required fields;
- Claude review of Phase 0 subplan returns `VERDICT: AGREE`;
- Claude review of Phase 1 subplan returns `VERDICT: AGREE`;
- no human-required stop condition fired.

## Stop Conditions

Stop and write a blocker result if:

- Claude review and Codex do not converge after five rounds for the same Phase 0
  or Phase 1 subplan blocker;
- continuing requires detached execution approval;
- continuing requires package installation, network fetch, or destructive git
  action;
- a required artifact path cannot be written without touching unrelated dirty
  work.

Minimum stop-handoff contents:

- current phase and state;
- blocker classification;
- last local check run and result;
- last Claude review target, round count, and verdict if any;
- artifacts created;
- exact next action requiring user or environment change;
- forbidden claims preserved while stopped.

## Phase Execution Steps

1. Create or refresh all required planning artifacts.
2. Run local section and path checks.
3. Run Claude bounded read-only review.
4. Patch fixable plan issues and rerun focused checks.
5. Write Phase 0 result.
6. Refresh and review Phase 1 subplan.
7. If any stop condition fires, update the visible stop handoff with the minimum
   contents listed above before sending the final status to the user.

## End-Of-Subplan Closeout Requirements

At Phase 0 close:

- local checks are recorded;
- review round count and verdicts are recorded;
- Phase 0 result exists;
- Phase 1 subplan review status is recorded;
- execution ledger is updated.
