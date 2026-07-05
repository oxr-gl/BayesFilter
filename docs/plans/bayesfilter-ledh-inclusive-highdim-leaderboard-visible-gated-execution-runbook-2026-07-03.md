# LEDH-Inclusive Highdim Leaderboard Visible Gated Execution Runbook

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

This is a visible, recoverable execution plan. Commands that need GPU or Claude
must be run in trusted or escalated context.

## Quiet Visible Execution Pattern

Full stdout/stderr is an artifact, not chat content.

For large commands:

1. predeclare the log path and structured artifact path;
2. redirect full stdout/stderr to the log path;
3. print only exit status, artifact paths, key pass/fail fields, and at most
   the last 40 log lines on failure;
4. preserve logs under `docs/plans/logs/`.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-master-program-2026-07-03.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-claude-review-ledger-2026-07-03.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-visible-execution-ledger-2026-07-03.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-visible-stop-handoff-2026-07-03.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Launch Boundary Freeze | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase0-launch-boundary-freeze-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase0-launch-boundary-freeze-result-2026-07-03.md` |
| 1 | Row Admission And Adapter Inventory | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-adapter-inventory-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-adapter-inventory-result-2026-07-03.md` |
| 2 | Runner And Artifact Schema | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase2-runner-schema-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase2-runner-schema-result-2026-07-03.md` |
| 3 | Tiny GPU/XLA Value And Score Gates | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tiny-gpu-xla-gates-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tiny-gpu-xla-gates-result-2026-07-03.md` |
| 4 | LEDH Particle Ladders | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-result-2026-07-03.md` |
| 5 | Merge And Cross-Algorithm Comparison | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-merge-comparison-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-merge-comparison-result-2026-07-03.md` |
| 6 | Closeout And Reset Memo | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-result-2026-07-03.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can LEDH-PFPF-OT be added to the highdim leaderboard across all existing model rows with target status, value status, and score status stated plainly? |
| Baseline/comparator | July 3 non-LEDH highdim leaderboard and row-specific exact or finite-difference references where valid. |
| Primary pass criterion | New LEDH-inclusive leaderboard artifact exists, or a blocker result states exactly why it cannot be produced. |
| Veto diagnostics | Wrong target, missing GPU/XLA evidence for LEDH execution, missing MCSE, missing total derivative check for claimed scores, hidden failed row. |
| Explanatory diagnostics | runtime, compile time, ESS, memory, particle trend, per-seed dispersion. |
| Not concluded | HMC readiness, posterior correctness, and scientific superiority are not concluded by this leaderboard alone. |
| Artifacts | Phase results, raw LEDH JSON/MD, merged JSON/MD, logs, review ledger. |

Comparator mode is `frozen_non_ledh_baseline_plus_fresh_ledh` unless a reviewed
phase changes it before results are seen. Runtime ranking across LEDH and
non-LEDH rows is forbidden in this mode.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| LEDH uses GPU/XLA/TF32 route | `AGENTS.md` default execution target | Matches project default for DPF transport work | CPU run misrepresented as production | Trusted GPU probe in Phase 3 | planned |
| July 3 highdim leaderboard is baseline | Existing artifact | It is the latest non-LEDH highdim artifact | Hidden mutation of baseline rows | Phase 0 freeze and Phase 5 diff check | planned |
| Frozen baseline plus fresh LEDH | This runbook | Avoids rerunning unrelated expensive rows while preserving provenance | Runtime comparisons become unfair | Disable runtime ranking unless all algorithms rerun | planned |
| Score is total derivative | User direction and recent debugging result | MLE/HMC need derivative of log likelihood target | Partial derivative admitted as score | Phase 3 score gate and row status fields | planned |
| Value MCSE is required | Monte Carlo LEDH values | Single seed value is not enough | Stable-looking single seed used as evidence | Phase 4 batched seeds `81120..81124` and default `N=1000,10000` ladder | planned |

## Skeptical Plan Audit

Before executing each phase, Codex must record the phase evidence contract and
check for:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If this audit finds a material flaw, revise the plan or write a blocker before
running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, append ledger entry.
2. `EXECUTE_MINIMAL`: run the smallest command or edit that answers the phase.
3. `ASSESS_GATE`: compare artifacts to phase evidence contract.
4. `PASS_REVIEW`: use Claude read-only review for material phase transitions.
5. `REPAIR_LOOP`: patch fixable defects, rerun focused checks, review again,
   at most five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the current gate passes.

## Claude Read-Only Review Template

Use Claude only as reviewer. Prompts must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review exact paths only:
- <paths>

Check:
- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch;
- evasive scientific language;
- mismatch between stated target and computed quantity.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Human-Required Stop Conditions

Stop if continuing would require:

- changing pass/fail criteria after seeing results;
- new package installation or network data fetch;
- destructive git or filesystem action;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU results without trusted execution;
- continuing after five unresolved Claude review rounds for the same blocker.
