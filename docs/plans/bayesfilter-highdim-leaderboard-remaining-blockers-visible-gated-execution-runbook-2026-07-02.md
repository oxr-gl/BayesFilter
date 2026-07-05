# Highdim Leaderboard Remaining Blockers Visible Gated Execution Runbook

Date: 2026-07-02

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-master-program-2026-07-02.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-claude-review-ledger-2026-07-02.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-execution-ledger-2026-07-02.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-stop-handoff-2026-07-02.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Baseline freeze and launch gate | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase0-baseline-freeze-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase0-baseline-freeze-result-2026-07-02.md` |
| 1 | Predator-prey T20 Zhao-Cui evaluator and analytical score | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-result-2026-07-02.md` |
| 2 | Generalized-SV exact source-row evaluator and analytical score | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-result-2026-07-02.md` |
| 3 | Spatial SIR full observed-data/filtering route | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-result-2026-07-02.md` |
| 4 | UKF analytical-score cleanup for remaining value-only rows | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-score-cleanup-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-score-cleanup-result-2026-07-02.md` |
| 5 | Batch/GPU/XLA readiness and score-at-true calibration | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-readiness-calibration-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-readiness-calibration-result-2026-07-02.md` |
| 6 | Final regeneration and closeout | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase6-final-regeneration-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase6-final-regeneration-result-2026-07-02.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining highdim leaderboard blockers be repaired into honest value plus analytical/manual score rows, or else preserved as precise blockers? |
| Baseline/comparator | `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json` and `.md`; phase-local target contracts. |
| Primary pass criterion | Each targeted cell is finite value plus finite analytical/manual score with theta coordinates and no autodiff/FD score provenance, or is precisely blocked by target/evaluator/derivative/readiness gap. |
| Veto diagnostics | Autodiff/FD/tape score admission; wrong target reported as row; local complete-data SIR sidecar reported as full filtering row; source-faithful claim without anchors; GPU/XLA claim from non-trusted context. |
| Explanatory diagnostics | FD consistency, score norm, runtime, score-at-true calibration, CPU-only smoke, trusted GPU/XLA compile/timing, and batch parity. |
| Not concluded | Exact nonlinear likelihood correctness, posterior correctness, HMC convergence, GPU superiority, release readiness, default-policy change. |
| Artifacts | This runbook, master program, review ledger, execution ledger, stop handoff, phase results, regenerated leaderboard. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Start with predator-prey T20 | User-requested one-by-one repair plan | It is the clearest missing Zhao-Cui evaluator adapter after SV/KSC repair. | Accidentally report P47 lower-rung fixture as T20. | Phase 1 target freeze and alignment tests. | `review_pending` |
| Defer SIR full filtering until after predator/generalized | Baseline blocker distinguishes P91 local sidecar from full row | SIR requires full observed-data/filtering route, not just local component. | P91 evidence promoted too far. | Phase 3 boundary tests. | `review_pending` |
| Keep GPU/XLA in readiness phase | Repo GPU policy and user HMC-facing concern | Hardware claims need trusted execution and row-specific manifests. | CPU-only artifact misread as GPU readiness. | Phase 5 trusted-context precheck. | `review_pending` |

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
   - Run visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Apply the plain-language gate before accepting the result artifact.
   - Write or update the required phase result artifact.
4. `PASS_REVIEW`
   - Send material phase subplans/results/repairs to Claude as read-only
     review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch visibly.
   - Rerun focused checks.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Plain-Language Gate

Before accepting a phase result, blocker result, or final decision, Codex must
verify that the artifact:

- states the claimed target and computed quantity separately;
- uses direct classifications such as `correct`, `wrong relative to the stated
  target`, `unsupported`, `not checked`, or `heuristic only`;
- labels unsupported claims as `unsupported` or `not checked`;
- labels mismatches as `wrong relative to the stated target`;
- states what remains unproved or unevaluated.

## Claude Review Prompt Rule

Use the smallest exact path that can answer the gate:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond to a bounded review, do not launch an additional
Claude subprocess under this runbook. First redesign the pending review prompt
to a smaller one-path question and retry once. If that retry also produces no
review, write a visible stop/handoff that records the prompt, path, timeout,
and next proposed narrower review. Continue only after human direction.

## Human-Required Stop Conditions

Stop if continuing would require:

- project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
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
