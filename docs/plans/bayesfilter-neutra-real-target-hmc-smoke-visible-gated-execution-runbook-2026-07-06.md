# BayesFilter NeuTra Real Target HMC Smoke Visible Gated Execution Runbook

Date: 2026-07-06

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use `codex
exec`, detached supervisors, backgrounded phase runners, or copied-workspace
execution.

## Quiet Visible Execution Pattern

Full command output is an artifact, not chat content. For noisy commands,
predeclare logs, preserve them, and report bounded summaries only.

## Program

Master program:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-master-program-2026-07-06.md`

Execution ledger:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-visible-execution-ledger-2026-07-06.md`

Stop handoff:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-visible-stop-handoff-2026-07-06.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Launch Contract Freeze | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase0-launch-contract-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase0-launch-contract-result-2026-07-06.md` |
| 1 | Target Authority Inventory | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase1-target-authority-inventory-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase1-target-authority-inventory-result-2026-07-06.md` |
| 2 | Real Target Adapter Boundary | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase2-real-target-adapter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase2-real-target-adapter-result-2026-07-06.md` |
| 3 | c603 Real-Target Mechanics | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase3-real-target-mechanics-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase3-real-target-mechanics-result-2026-07-06.md` |
| 4 | Tiny Fixed-Kernel HMC Smoke | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase4-tiny-hmc-smoke-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase4-tiny-hmc-smoke-result-2026-07-06.md` |
| 5 | Closeout | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase5-closeout-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase5-closeout-result-2026-07-06.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter replace the c603 synthetic mechanics base adapter with a reviewed real target/value-score boundary, then run mechanics and at most a tiny fixed-kernel HMC smoke without overclaiming? |
| Baseline/comparator | Closed c603 import/mechanics fixture program plus existing SSM target-builder/fixed-transport/HMC surfaces. |
| Primary pass criterion | A reviewed real target adapter boundary is either implemented and tested, or the exact missing authority is recorded fail-closed; no HMC smoke is run until that boundary passes. |
| Veto diagnostics | Missing real value/score authority, target-signature mismatch, nonfinite target values/scores, hidden fallback promotion, GPU/training/long-HMC launch, or unsupported claims. |
| Explanatory diagnostics | Adapter metadata, finite probes, manifest hashes, target signature, review status, tiny-smoke diagnostics if reached. |
| Not concluded | Posterior correctness, HMC convergence, sampler ranking, production readiness, or support for arbitrary nonlinear SSMs. |
| Artifacts | Ledger, phase results, review records, logs, tests. |

## Skeptical Plan Audit

Before executing each phase, Codex must record a skeptical audit in the ledger:
wrong baselines, proxy metrics, stop conditions, hidden assumptions, stale
context, environment mismatch, and artifact mismatch.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract.
2. `EXECUTE_MINIMAL`: run the smallest visible work needed.
3. `ASSESS_GATE`: compare result to primary criterion and veto diagnostics.
4. `PASS_REVIEW`: use Claude only as read-only reviewer for material gates.
5. `REPAIR_LOOP`: patch fixable blockers visibly; rerun focused checks; stop
   after five review rounds for the same material blocker.
6. `ADVANCE_OR_STOP`: advance only after the current phase gate passes.

## Human-Required Stop Conditions

Stop before package installation, network fetch not already authorized,
credentials, environment setup, destructive git/filesystem actions, GPU/CUDA
jobs, training, long HMC, default-policy changes, modifying unrelated dirty
work, or unsupported scientific/product claims.

## Claude Review Protocol

Use `~/python/claudecodex/scripts/claude_review_gate.sh` with bounded bundles
under `docs/reviews/`. If Claude does not respond, run a tiny probe. If the
probe succeeds, revise the prompt. If the probe fails, record reviewer
unavailability and substitute a fresh Codex review.

Claude cannot authorize human, runtime, model-file, funding, product,
default-policy, or scientific-claim boundaries.

## Final Visible Handoff

When execution completes or stops, update:

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-visible-stop-handoff-2026-07-06.md`
