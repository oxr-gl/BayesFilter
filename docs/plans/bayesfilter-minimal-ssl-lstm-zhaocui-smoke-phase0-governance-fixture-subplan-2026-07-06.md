# Phase 0 Subplan: Governance, Fixture Freeze, And Review Setup

Date: 2026-07-06

Status: `DRAFT_PENDING_LOCAL_CHECKS_AND_REVIEW`

## Phase Objective

Freeze the minimal one-dimensional SSL-LSTM smoke fixture, create the visible
execution scaffolding, and prepare bounded review without running material
Claude/GPU/long commands yet.

## Entry Conditions Inherited From Previous Phase

- The Zhao-Cui-first program completed and recorded
  `zhaocui_fixed` as an admitted clean-room fixed adapter.
- The user approved the minimal scalar design and asked to operationalize it.
- Current scope is a new minimal smoke program, not longer HMC evidence,
  production GPU evidence, LEDH, or source-faithful Zhao-Cui/TTSIRT work.

## Required Artifacts

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-master-program-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-visible-gated-execution-runbook-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-visible-execution-ledger-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-visible-stop-handoff-2026-07-06.md`
- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase0-review-bundle-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase0-governance-fixture-result-2026-07-06.md`
- Draft Phase 1 subplan.

## Required Checks, Tests, And Reviews

- Local doc existence check for master/runbook/ledger/handoff/review bundle.
- `git diff --check`.
- Forbidden-claim scan over Phase 0 planning artifacts.
- Bounded Claude review gate only after user approval.
- If Claude approval is not granted, use a recorded Codex substitute review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the minimal scalar SSL-LSTM smoke program correctly scoped, frozen, and ready for Phase 1 harness work? |
| Baseline/comparator | Existing minimal `zhaocui_fixed` adapter test fixture and July 5 reset memo. |
| Primary pass criterion | Master program, runbook, ledger, handoff, review bundle, and Phase 1 subplan exist and preserve scope/evidence boundaries. |
| Veto diagnostics | Wrong fixture dimensions, unsupported claim, missing stop condition, hidden long/GPU/Claude launch, LEDH leakage, or source-faithful parity claim. |
| Explanatory diagnostics | Worktree status, planned checks, review availability, and numeric-default provenance. |
| Not concluded | No mechanics pass, posterior correctness, HMC convergence, ranking, source-faithful parity, GPU/XLA readiness, default readiness, or LEDH result. |

## Forbidden Claims And Actions

- Do not claim that planning proves the minimal model works.
- Do not claim posterior correctness, HMC convergence, method superiority,
  source-faithful parity, GPU/XLA production readiness, or default readiness.
- Do not run Claude review, GPU checks, long tests, or detached/overnight
  execution before explicit approval.
- Do not modify public APIs, model files, package metadata, or unrelated dirty
  files.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only when:

- Phase 0 result exists;
- Phase 1 harness subplan exists;
- local doc checks pass;
- review path is either approved and completed or explicitly recorded as
  pending/substituted;
- anticipated approvals have been requested.

## Stop Conditions

Stop if fixture scope cannot stay scalar/minimal, if executing would require
unapproved Claude/GPU/long/detached commands, if review does not converge after
five rounds for the same blocker, or if a required fix would broaden into
LEDH/source-faithful/default-policy work.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write Phase 0 result/close record.
3. Draft or refresh Phase 1 subplan.
4. Review Phase 1 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
