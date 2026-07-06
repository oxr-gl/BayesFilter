# BayesFilter LGSSM-First NeuTra/HMC Visible Gated Execution Runbook

Date: 2026-07-06

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch detached or nested execution. Do not use `codex
exec`, `overnight_gated_launch.sh`, detached supervisors, backgrounded phase
runners, or copied-workspace execution.

## Quiet Visible Execution Pattern

Full command output is an artifact, not chat content. For noisy commands,
predeclare logs, preserve them, and report bounded summaries only.

## Program

Master program:

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-master-program-2026-07-06.md`

Execution ledger:

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-execution-ledger-2026-07-06.md`

Stop handoff:

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-stop-handoff-2026-07-06.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Scope Reset And Launch | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase0-scope-reset-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase0-scope-reset-result-2026-07-06.md` |
| 1 | Interface Inventory And Gap Map | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase1-interface-inventory-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase1-interface-inventory-result-2026-07-06.md` |
| 2 | LGSSM Exact Target Adapter | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase2-lgssm-target-adapter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase2-lgssm-target-adapter-result-2026-07-06.md` |
| 3 | Plain HMC Mechanics Smoke | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-result-2026-07-06.md` |
| 4 | LGSSM Posterior Reference Validation | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-result-2026-07-06.md` |
| 5 | Frozen Transport Binding | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase5-frozen-transport-binding-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase5-frozen-transport-binding-result-2026-07-06.md` |
| 6 | LGSSM NeuTra Training And Freeze | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-result-2026-07-06.md` |
| 7 | First Simple Nonlinear SSM | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase7-simple-nonlinear-ssm-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase7-simple-nonlinear-ssm-result-2026-07-06.md` |
| 8 | Same Target Multiple Filters | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase8-multifilter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase8-multifilter-result-2026-07-06.md` |
| 9 | DSGE/c603 Stress Target | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-dsge-stress-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-dsge-stress-result-2026-07-06.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter build a generic Bayesian SSM target adapter and NeuTra/HMC mechanics path from an exact LGSSM base before moving to nonlinear SSMs and later DSGE stress targets? |
| Baseline/comparator | Existing SSM contracts, QR Kalman LGSSM code, fixed transport mechanics, and opt-in QR static LGSSM HMC smoke harness. |
| Primary pass criterion | Each phase either produces a reviewed artifact for its boundary or records an exact blocker without overclaiming. |
| Veto diagnostics | DSGE/c603 as foundation, smoke promoted to readiness, finite probes promoted to posterior correctness, unapproved GPU/training/long-HMC/package/git actions. |
| Explanatory diagnostics | Signatures, manifests, finite probes, reference residuals, review status. |
| Not concluded | Posterior convergence, sampler ranking, production readiness, broad nonlinear SSM validity, DSGE/c603 readiness. |
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
jobs, NeuTra training, long HMC, detached execution, default-policy changes,
modifying unrelated dirty work, live DSGE/c603 runtime work, or unsupported
scientific/product claims.

## Claude Review Protocol

Use `~/python/claudecodex/scripts/claude_review_gate.sh` with bounded bundles
under `docs/reviews/`. If Claude does not respond, run a tiny trusted probe. If
the probe succeeds, revise the prompt. If the probe fails or cannot be run,
record reviewer unavailability and substitute a fresh Codex review.

Claude cannot authorize human, runtime, model-file, funding, product,
default-policy, or scientific-claim boundaries.

## Final Visible Handoff

When execution completes or stops, update:

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-stop-handoff-2026-07-06.md`
