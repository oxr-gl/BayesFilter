# Highdim Leaderboard Blocker-By-Blocker Visible Gated Execution Runbook

Date: 2026-07-04

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

Codex may invoke Claude Code only as a bounded, foreground, read-only review
process for an exact path and exact question. Claude must not edit files, run
commands, launch agents, approve boundaries, or make execution decisions.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-master-program-2026-07-04.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-claude-review-ledger-2026-07-04.md`
- `docs/reviews/bayesfilter-highdim-leaderboard-blocker-by-blocker-plan-review-bundle-2026-07-04.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-visible-execution-ledger-2026-07-04.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-visible-stop-handoff-2026-07-04.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Baseline freeze and launch gate | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase0-baseline-freeze-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase0-baseline-freeze-result-2026-07-04.md` |
| 1 | Full-row LGSSM GPU/XLA score gate | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase1-lgssm-full-row-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase1-lgssm-full-row-result-2026-07-04.md` |
| 2 | Actual-SV current LEDH adapter repair | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase2-actual-sv-ledh-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase2-actual-sv-ledh-result-2026-07-04.md` |
| 3 | KSC current LEDH adapter repair | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase3-ksc-ledh-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase3-ksc-ledh-result-2026-07-04.md` |
| 4 | Generalized-SV exact source-row evaluator | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase4-generalized-sv-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase4-generalized-sv-result-2026-07-04.md` |
| 5 | Spatial SIR full observed-data/filtering route | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase5-spatial-sir-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase5-spatial-sir-result-2026-07-04.md` |
| 6 | Predator-prey T20 source-scope adapter | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase6-predator-prey-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase6-predator-prey-result-2026-07-04.md` |
| 7 | UKF analytical-score cleanup | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase7-ukf-cleanup-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase7-ukf-cleanup-result-2026-07-04.md` |
| 8 | Final regeneration and closeout | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase8-final-regeneration-closeout-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase8-final-regeneration-closeout-result-2026-07-04.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining highdim leaderboard blockers be repaired into honest value plus analytical/manual score rows, or else preserved as precise blockers? |
| Baseline/comparator | `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json` and `.md`; the remaining-blockers ledger; phase-local target contracts. |
| Primary pass criterion | Each targeted cell is finite value plus finite same-target analytical/manual score with theta coordinates and no autodiff/FD score provenance, or is precisely blocked by target/evaluator/derivative/readiness gap. |
| Veto diagnostics | Autodiff/FD/tape score admission; wrong target reported as row; local component or lower-rung evidence reported as full row; source-faithful claim without paper/source anchors; GPU/XLA claim from non-trusted context. |
| Explanatory diagnostics | FD consistency, score norm, runtime, score-at-true calibration, CPU-only smoke, trusted GPU/XLA compile/timing, and batch parity. |
| Not concluded | Exact nonlinear likelihood correctness, posterior correctness, HMC convergence, GPU superiority, release readiness, default-policy change. |
| Artifacts | This runbook, master program, review ledger, execution ledger, stop handoff, phase results, regenerated leaderboard artifacts `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-04.json` and `.md` if Phase 8 regenerates, and final closeout/reset memo `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-reset-memo-2026-07-04.md` if reached. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Start with LGSSM full-row gate | user-requested blocker-by-blocker repair order | It is the clearest remaining LEDH blocker and already has a local tiny-prefix score route. | CPU-only prefix mistakenly treated as full-row admission. | Phase 1 trusted-row gate requirement. | `review_pending` |
| Defer actual-SV and KSC to separate phases | current leaderboard blockers separate those rows | Their blockers are adapter-specific and should not be mixed. | accidental cross-row reuse without reviewed same-target proof. | Phase 2/3 target freeze. | `review_pending` |
| Keep GPU/XLA in readiness and full-row gates | repo GPU policy and user HMC-facing concern | Hardware claims need trusted execution and row-specific manifests. | CPU-only artifact misread as GPU readiness. | Phase 1 and Phase 5 trusted-context prechecks. | `review_pending` |

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

Phase 0 is a hard launch gate. No Phase 1 or later execution may begin until
`docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase0-baseline-freeze-result-2026-07-04.md`
exists and explicitly certifies the candidate phase list against
`docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-execution-ledger-2026-07-02.md`.

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
   - If the same blocker reaches five Claude review rounds, write a blocker
     result, update the stop handoff, and stop.
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

If Claude does not respond to a bounded foreground read-only review, do not
launch a detached, nested, broader, or autonomous Claude process under this
runbook. First redesign the pending review prompt to a smaller one-path
question and retry once. If that retry also produces no review, write a
visible stop/handoff that records the prompt, path, timeout, and next proposed
narrower review. Continue only after human direction.

## Artifact Ownership

- The visible execution ledger is appended at each phase start/end.
- The review ledger records every material Claude review round.
- The stop handoff is written if the runbook stops early or after the final
  closeout.
- The final closeout/reset note is written only in Phase 8.

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
