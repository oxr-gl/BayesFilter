# P75 Visible Gated Execution Runbook

Date: 2026-06-17

## Status

`PHASE10_CLAUDE_AGREE_READY_FOR_PHASE11`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

Claude review is performed through the foreground wrapper
`/home/chakwong/python/claudecodex/scripts/claude_worker.sh` when a material
phase requires it.  That wrapper is a bounded read-only review mechanism, not
an executor, supervisor, detached phase runner, or authority to advance gates.
Codex must inspect the returned review in this conversation, patch or block
visibly, and record the outcome in the ledgers.

The foreground `claude_worker.sh` read-only reviewer is the only allowed
cross-agent mechanism in this runbook.  It is not a phase executor and must be
run synchronously, with Codex waiting for and inspecting the review output in
the current conversation.  Non-escalated Claude hangs or network/auth errors
are sandbox evidence only until a minimal trusted-context probe is retried.

This runbook must not launch a detached or nested execution agent.  Do not
use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

"Overnight" means the phase ladder may contain long visible commands that
Codex monitors and records.  It does not mean hidden autonomous execution.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p75-claude-review-ledger-2026-06-17.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-stop-handoff-2026-06-17.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Planning and objective-boundary review | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-result-2026-06-17.md` |
| 1 | Mathematical pilot design contract | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-result-2026-06-17.md` |
| 2 | Implementation surface and test plan | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-result-2026-06-17.md` |
| 3 | Opt-in implementation and unit tests | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-result-2026-06-17.md` |
| 4 | Bounded pilot run | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-result-2026-06-17.md` |
| 5 | Result decision and next handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-result-2026-06-17.md` |
| 6 | Guided warm-start mechanism smoke | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-result-2026-06-18.md` |
| 7 | UKF/source-guided initializer design | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-design-result-2026-06-18.md` |
| 8 | Source-guided square-root prefit implementation and tiny test | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-result-2026-06-18.md` |
| 9 | Guided prefit decision and larger-pilot handoff | to be drafted at Phase 8 close | to be drafted at Phase 8 close |
| 10 | Bounded capacity/sample/prefit ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-result-2026-06-18.md` |
| 11 | Negative ladder decision and redesign handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase11-negative-ladder-decision-subplan-2026-06-18.md` | to be drafted at Phase 10 close |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P75 implement and run a bounded stochastic differentiable density-training pilot for the fixed variant without overclaiming? |
| Baseline/comparator | P73 Phase 5 blocked diagnostic and Phase 6 handoff. |
| Primary pass criterion | Each phase produces its required result, local checks pass, material Claude review converges, the next subplan exists, and exact handoff conditions are met. |
| Veto diagnostics | Source-faithfulness overclaim, audit holdout used for training, pilot loss promoted to validation, threshold changes after outputs, downstream validation/HMC/scaling/rank promotion, unapproved GPU claims. |
| Explanatory diagnostics | Loss curves, gradient norms, log-normalizer estimates, fresh audit residuals, line gates, runtime, memory. |
| Not concluded | No repaired lower gate unless frozen gates pass; no adaptive Zhao--Cui parity; no validation/HMC/scaling readiness; no final rank/sample policy. |
| Artifacts | Master program, runbook, execution ledger, review ledger, phase subplans/results, implementation diffs if launched, pilot JSONs, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| P73 blocked diagnostic is the baseline | P73 Phase 6 closeout | It is the actual current failure. | Comparing against stale schema/smoke or old ALS-only result. | Phase 0 artifact checks. | reviewed predecessor |
| P75 is an extension/invention | Zhao--Cui governance and P73 closeout | Stochastic KL training is not author source-route behavior. | Source-faithfulness overclaim. | Phase 0 boundary ledger. | planned |
| Start CPU-only unless explicitly escalated | AGENTS GPU policy and bounded pilot scope | Avoids false GPU evidence and approval churn. | Long pilot too slow or sandbox GPU confusion. | Phase 1/4 runtime gate. | planned |
| Pilot loss is not validation | Scientific evidence policy | Avoids proxy metric promotion. | Declaring success from training loss only. | Phase 1 evidence contract. | planned |

## Anticipated Approvals And Boundaries

The reviewed runbook approval covers visible execution of ordinary reviewed
phase transitions.  After a phase gate passes, Codex continues to the next
reviewed subplan without asking for another routine launch approval.  Codex
asks the user only when a human-required boundary below is reached.

Covered by the reviewed visible runbook:

- Claude Code read-only reviews through
  `/home/chakwong/python/claudecodex/scripts/claude_worker.sh` with Opus max
  effort, run in the foreground and used only for review;
- local documentation writes under `docs/plans`;
- visible source-code edits on implementation surfaces explicitly authorized
  by a reviewed phase subplan only;
- CPU-only Python/pytest diagnostics with `CUDA_VISIBLE_DEVICES=-1`;
- bounded CPU-only pilot or diagnostic runs explicitly authorized by a
  reviewed phase subplan.

Not approved by this runbook:

- destructive git or filesystem actions;
- package installation or dependency downloads;
- network fetches, credentials, or outside-repo writes;
- detached/background execution except the foreground synchronous
  `claude_worker.sh` read-only reviewer described above;
- threshold changes after outputs;
- downstream validation, HMC, scaling, or rank promotion;
- escalated GPU, network, package-install, or outside-repo commands unless a
  later reviewed phase explicitly needs them and the user approves the
  boundary.

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and,
for material phases, in the execution ledger.

Check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
4. `DRAFT_NEXT`
   - Draft or refresh the next phase subplan.
   - Ensure the current result explicitly produces next-phase entry
     conditions.
5. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude through the foreground read-only review wrapper.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
6. `REPAIR_LOOP`
   - For fixable blockers, patch the same artifact visibly.
   - Rerun focused checks.
   - Rereview material fixes.
   - Stop after five Claude review rounds for the same blocker.
7. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Continue automatically to the next reviewed subplan after the gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- downstream validation, HMC, scaling, or rank promotion;
- continuing after Claude and Codex do not converge after five review rounds.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests/benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
