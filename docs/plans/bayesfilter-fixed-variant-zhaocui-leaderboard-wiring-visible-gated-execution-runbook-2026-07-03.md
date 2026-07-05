# Visible Gated Execution Runbook: Fixed-Variant Zhao-Cui Leaderboard Wiring

Date: 2026-07-03

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_PENDING_CLAUDE_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This is a visible, recoverable execution plan. The word "launch" means Codex
starts Phase 0 in the current conversation after local checks and bounded
Claude review pass.

## Program

Master program:

- `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-master-program-2026-07-03.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-claude-review-ledger-2026-07-03.md`

Execution ledger:

- `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-visible-execution-ledger-2026-07-03.md`

Stop handoff:

- `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-visible-stop-handoff-2026-07-03.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Launch Boundary Freeze | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase0-launch-boundary-freeze-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase0-launch-boundary-freeze-result-2026-07-03.md` |
| 1 | Fixed-Variant Entry Point Inventory | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase1-entrypoint-inventory-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase1-entrypoint-inventory-result-2026-07-03.md` |
| 2 | Row Scope And Evidence Contract | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase2-row-scope-contract-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase2-row-scope-contract-result-2026-07-03.md` |
| 3 | Runner Wiring And Guards | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase3-runner-wiring-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase3-runner-wiring-result-2026-07-03.md` |
| 4 | Regeneration And Validation | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase4-regeneration-validation-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase4-regeneration-validation-result-2026-07-03.md` |
| 5 | Closeout And Handoff | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase5-closeout-subplan-2026-07-03.md` | `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase5-closeout-result-2026-07-03.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the highdim leaderboard report the Zhao-Cui SIR fixed-variant route without using or repairing the demoted retained-grid route and without overclaiming full observed-data filtering readiness? |
| Baseline/comparator | Current July highdim leaderboard artifacts, P91 fixed-variant SIR artifacts, and owner retained-grid demotion directive. |
| Primary pass criterion | The affected Zhao-Cui SIR row is regenerated with fixed-variant route metadata, analytical/manual score provenance if a score is emitted, retained-grid exclusion metadata, and explicit scope/nonclaim fields. |
| Veto diagnostics | Retained-grid route selected for production; autodiff/FD score admitted; full observed-data filtering score identity claimed without closing preserved blockers; stale fixed/no-free-theta row treated as the parameterized score row; nonfinite value/score; missing result artifacts; Claude review `VERDICT: REVISE` not resolved within five rounds. |
| Explanatory diagnostics | Runtime, sidecar P91 GPU/XLA timing, P91 score-at-true tables, row summary readiness, and leaderboard markdown formatting. |
| Not concluded | No exact likelihood proof, no posterior correctness, no convergence claim, no universal GPU speed superiority, no production default change beyond route admission metadata, and no source-faithful claim without paper/source anchors. |
| Artifacts | Master program, phase subplans/results, visible runbook, execution ledger, review ledger, regenerated leaderboard JSON/MD, and stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Fixed variant is production direction | Owner directive and `AGENTS.md` route boundary | Avoids historical retained-grid path | Overclaims local component as full filtering | Phase 1/2 scope contract | pending |
| Retained-grid remains callable for diagnostics | Existing tests and code | Preserve lower-rung evidence | Accidentally selected for production row | Route metadata tests | pending |
| CPU-only for runner checks | Current highdim leaderboard script hides CUDA | Avoid untrusted GPU claims | Missing GPU evidence | Cite trusted P91 artifacts only | pending |
| Claude read-only review | User request and local policy | Independent boundary review | Prompt stalls or broad disclosure | One-path prompts and probe ladder | pending |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and in
the execution ledger for material phases.

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
2. `EXECUTE_MINIMAL`
3. `ASSESS_GATE`
4. `PASS_REVIEW`
5. `REPAIR_LOOP`
6. `ADVANCE_OR_STOP`

Codex must update the execution ledger at each material state transition.

## Repair Loop

If a review or check finds a fixable problem:

1. Patch the same subplan/result visibly.
2. Rerun focused checks.
3. Rerun bounded Claude review only for material issues.
4. Stop after five review rounds for the same blocker.

## Human-Required Stop Conditions

Stop if continuing would require:

- redefining the leaderboard scientific target;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Launch Command Discipline

No detached launcher is allowed under this visible runbook. Claude calls require
trusted/escalated execution. GPU/CUDA commands require trusted/escalated
execution and are not planned unless Phase 4 explicitly needs fresh GPU
evidence.

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
