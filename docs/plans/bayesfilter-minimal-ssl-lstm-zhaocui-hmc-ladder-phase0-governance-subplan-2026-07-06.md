# Phase 0 Subplan: Governance, Fixture Freeze, And Review Setup

Date: 2026-07-06

Status: `DRAFT_PENDING_LOCAL_CHECKS_AND_REVIEW`

## Phase Objective

Freeze the scalar HMC ladder scope, create the visible execution scaffolding,
and prepare bounded review before running material HMC, GPU, long, detached, or
external reviewer commands.

## Entry Conditions Inherited From Previous Phase

- The minimal scalar SSL-LSTM smoke program completed.
- `zhaocui_fixed` has a CPU-hidden debug smoke artifact with finite
  deterministic value/score and finite-difference subset agreement.
- Current scope is HMC mechanics for the scalar clean-room fixed adaptation,
  not posterior correctness, GPU/XLA production readiness, LEDH, or
  source-faithful Zhao-Cui/TTSIRT work.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-master-program-2026-07-06.md`
- Visible gated overnight execution plan:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-visible-gated-overnight-execution-plan-2026-07-06.md`
- Execution ledger:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-visible-execution-ledger-2026-07-06.md`
- Stop handoff:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-visible-stop-handoff-2026-07-06.md`
- Compact review bundle:
  `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-review-bundle-2026-07-06.md`
- Phase 0 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-governance-result-2026-07-06.md`
- Dedicated Phase 1 subplan.

## Required Checks, Tests, And Reviews

- Required artifact existence check.
- `git diff --check`.
- Forbidden-claim scan over new HMC-ladder planning/review artifacts.
- Confirm completed minimal smoke artifact exists.
- Bounded Claude review gate after approval, or recorded local Codex substitute
  review if external Claude review is unavailable or denied.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the scalar `zhaocui_fixed` HMC ladder correctly scoped and ready for target-adapter implementation planning? |
| Baseline/comparator | Completed minimal smoke artifact and existing Phase 7 SSL-LSTM HMC launch-smoke pattern. |
| Primary pass criterion | Master program, all phase subplans, runbook, ledger, handoff, and review bundle exist and preserve evidence boundaries. |
| Veto diagnostics | Wrong fixture dimensions, unsupported claim, missing stop condition, hidden HMC/GPU/long/detached launch, LEDH leakage, source-faithful parity claim, or invalid review authority transfer. |
| Explanatory diagnostics | Worktree status, planned approvals, numeric-default provenance, and review availability. |
| Not concluded | No target adapter pass, HMC canary pass, posterior correctness, HMC convergence, ranking, GPU/XLA readiness, default readiness, source-faithful parity, or LEDH result. |

## Forbidden Claims And Actions

- Do not claim the HMC target adapter works.
- Do not claim HMC convergence, posterior correctness, method superiority,
  source-faithful parity, GPU/XLA production readiness, default readiness, or
  LEDH result.
- Do not run HMC, GPU, long, detached, package-install, network, or external
  reviewer commands before the relevant gate.
- Do not modify public APIs, model files, package metadata, or unrelated dirty
  files.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only when:

- Phase 0 result exists;
- Phase 1 target-adapter subplan exists;
- local doc checks pass;
- review path is completed or explicitly substituted and recorded;
- anticipated approvals have been requested/recorded.

## Stop Conditions

Stop if fixture scope cannot stay scalar/minimal, if executing would require
unapproved HMC/GPU/long/detached/external-review commands, if review does not
converge after five rounds for the same blocker, or if a required fix would
broaden into LEDH/source-faithful/default-policy work.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write Phase 0 result/close record.
3. Draft or refresh Phase 1 subplan.
4. Review Phase 1 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
