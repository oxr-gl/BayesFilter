# BayesFilter Highdim Zhao-Cui Leaderboard Completion Visible Gated Overnight Runbook

Date: 2026-07-01

## Status

`REVISED_PENDING_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only.

This visible overnight runbook must not launch a detached or nested agent. Do
not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution is needed later, stop and write a separate
detached-supervisor plan.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-master-program-2026-07-01.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-claude-review-ledger-2026-07-01.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-visible-execution-ledger-2026-07-01.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-visible-stop-handoff-2026-07-01.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Launch inventory and fail-closed Zhao-Cui contract | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase0-launch-inventory-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase0-launch-inventory-result-2026-07-01.md` |
| 1 | Actual-SV and KSC Zhao-Cui analytical score repair | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase1-sv-ksc-score-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase1-sv-ksc-score-result-2026-07-01.md` |
| 2 | Predator-prey T20 Zhao-Cui evaluator adapter | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase2-predator-prey-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase2-predator-prey-result-2026-07-01.md` |
| 3 | Generalized-SV exact source-row Zhao-Cui evaluator | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase3-generalized-sv-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase3-generalized-sv-result-2026-07-01.md` |
| 4 | Spatial SIR d18 full observed-data/filtering route | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase4-sir-full-filtering-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase4-sir-full-filtering-result-2026-07-01.md` |
| 5 | Batched, GPU/XLA, and score-at-true calibration ladder | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase5-batch-gpu-calibration-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase5-batch-gpu-calibration-result-2026-07-01.md` |
| 6 | Final leaderboard regeneration and closeout | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase6-final-regeneration-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase6-final-regeneration-result-2026-07-01.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining Zhao-Cui leaderboard cells be completed or precisely blocked under an analytical-score-only admission contract? |
| Baseline/comparator | Exact artifacts `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`, `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`, `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase1-route-protocol-inventory-result-2026-06-22.md`, and `docs/plans/bayesfilter-highdim-zhao-cui-p91-reset-memo-2026-06-29.md`; source-faithfulness claims additionally require exact paper/source anchors recorded in the phase result. |
| Primary pass criterion | Final Zhao-Cui cells are either admitted with finite value plus manual analytical score, or blocked with exact target/evaluator/derivative gap. Batch/GPU/XLA and score-at-true results are recorded as separate readiness/diagnostic statuses rather than silent row-admission gates. |
| Veto diagnostics | Autodiff/tape/FD admitted as analytical score; source-faithfulness without anchors; score without theta; local complete-data SIR promoted to full filtering; GPU/XLA claim from untrusted context; SGQF lane mixed into Zhao-Cui admission. |
| Explanatory diagnostics | FD consistency, score norm, timing, CPU-only smokes, trusted GPU/XLA compiles. Expected-score calibration is required where simulator/truth support exists and may veto scientific-consistency/readiness wording, but it does not prove exact likelihood or posterior correctness. |
| Not concluded | Exact nonlinear likelihood, posterior correctness, HMC convergence, universal GPU speedup, release readiness, default-policy changes. |
| Artifacts | Phase results, regenerated leaderboard, Claude review ledger, execution ledger, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Analytical score excludes `GradientTape` and `ForwardAccumulator` | User directive and prior P82/P91 ledgers | Leaderboard benchmarks analytical gradient accuracy | Diagnostic gradient sneaks into admitted cell | Provenance scan and tests | binding |
| SGQF is out of scope | User says another agent is fixing SGQF | Avoid cross-agent lane collision | Accidentally overwriting SGQF work | Row filter limited to Zhao-Cui algorithm id | binding |
| Score-at-true is expectation-based | User correction | High-dimensional models lack gradient oracle | Per-dataset zero-score myth | Multi-seed mean and uncertainty artifact | binding |
| GPU/XLA requires trusted context | `AGENTS.md` | Sandbox can hide GPU devices | False GPU failure or false GPU claim | Escalated device/framework probe | policy |

## Skeptical Plan Audit

Before executing each phase, Codex must record a skeptical audit in chat and in
the execution ledger.

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
4. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after two focused code repair iterations for the same row/blocker.
   - A narrow local-check or Claude-requested patch may be applied only inside
     those two iterations; it does not extend the iteration count.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Read-Only Review Template

Default first prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: <one path>. Do not edit, run commands, launch agents, or review the whole repo. Question: <one question>. Check wrong baseline, proxy metrics promoted to pass criteria, missing stop condition, unfair comparison, hidden assumption, stale context, environment mismatch, unsupported claim, and artifact mismatch. Findings first. End with exactly VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, run a tiny read-only probe. If the probe responds,
redesign the prompt to a smaller exact path.

Claude availability stop rule:

- A silent/no-output Claude call counts as a no-response event after two
  consecutive polls of at least 60 seconds each.
- For the same artifact, after two no-response events and a successful tiny
  probe, Codex must redesign the prompt once to a smaller exact path.
- If the redesigned prompt also has two no-response events, write a blocker
  entry in the execution ledger and stop for human direction.
- If the tiny probe itself fails in trusted context, write a blocker entry and
  stop for human direction.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing a GPU/XLA readiness phase after a required trusted GPU device
  probe, framework probe, or row-specific compile cannot be run; in that case
  write the phase result as a GPU/XLA blocker instead of proceeding;
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
