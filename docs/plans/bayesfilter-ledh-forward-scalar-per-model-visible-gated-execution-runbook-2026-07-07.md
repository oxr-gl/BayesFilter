# LEDH Forward Scalar Per-Model Visible Gated Execution Runbook

Date: 2026-07-07

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

Execution is visible and staged. Launch Phase 0 only after the launch package
passes local checks and read-only review. Later phases may proceed only through
their handoff gates.

## Quiet Visible Execution Pattern

Full stdout/stderr for long TensorFlow, CUDA, benchmark, sampler, or Claude
commands is an artifact, not chat content.

Required pattern:

1. Predeclare log path and structured artifact path in the subplan or ledger.
2. Redirect full stdout/stderr to logs for long commands.
3. Prefer commands that write JSON/Markdown/result artifacts directly.
4. Print only bounded summaries: exit status, artifact paths, pass/fail fields,
   and at most the last 20-40 log lines on failure.
5. Treat excessive stdout/stderr as an execution-flow defect.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`

Source amendment:

- `docs/plans/bayesfilter-ledh-same-target-forward-scalar-per-model-amendment-plan-2026-07-06.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-visible-execution-ledger-2026-07-07.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-visible-stop-handoff-2026-07-07.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Baseline and admission guard | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase0-baseline-guard-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase0-baseline-guard-result-2026-07-07.md` |
| 1 | Shared runner schema | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase1-runner-schema-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase1-runner-schema-result-2026-07-07.md` |
| 2 | LGSSM | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase2-lgssm-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase2-lgssm-result-2026-07-07.md` |
| 3 | Fixed SIR | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase3-fixed-sir-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase3-fixed-sir-result-2026-07-07.md` |
| 4 | Predator-prey | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-result-2026-07-07.md` |
| 5 | Actual SV | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-result-2026-07-07.md` |
| 6 | Generalized SV | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase6-generalized-sv-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase6-generalized-sv-result-2026-07-07.md` |
| 7 | KSC SV | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase7-ksc-sv-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase7-ksc-sv-result-2026-07-07.md` |
| 8 | Value integration | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase8-integration-subplan-2026-07-07.md` | `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase8-integration-result-2026-07-07.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can each intended high-dimensional LEDH row produce an executable same-target observed-data log likelihood estimator artifact? |
| Target scalar | `observed_data_log_likelihood_estimator`, reported as `log_likelihood`. |
| Baseline/comparator | July 6 Phase 3 admitted/blocked result, July 6 per-model amendment plan, current forward contract metadata, row datasets, and row-specific reference checks where available. |
| Primary pass criterion | A row is value-admitted only when a validated executable artifact reports finite `log_likelihood` values from the row target correction at the required row scale. |
| Veto diagnostics | Metadata-only admission; callback-only admission; proposal/flow objective used as likelihood; wrong row target; actual-SV/KSC artifact borrowing; score implementation before scalar admission; runtime/memory/finite output promoted as correctness. |
| Explanatory diagnostics | Runtime, compile time, memory, ESS, Monte Carlo standard error, tiny-prefix checks, old blocked evidence, and non-LEDH references. |
| Not concluded | Score correctness, score admission, HMC readiness, posterior correctness, scientific superiority, and fair runtime ranking. |
| Artifacts | Master program, runbook, ledger, stop handoff, phase subplans/results, review bundles, logs, checks, and final value leaderboard artifacts. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Forward-scalar-only scope | User request and amendment plan | Score work previously polluted scalar admission | Score code runs before value target is proven | Phase 0 and all subplans forbid score work | baseline |
| One phase per model | User request and amendment plan | Model dependencies differ and bundled Phase 3 failed | Metadata/callback evidence overpromoted | Phase index separates every row | baseline |
| KSC last | Amendment plan | KSC lacks LEDH route and must not borrow actual-SV route | Actual-SV/KSC target mixing | Phase 7 guard tests | baseline |
| Visible execution | Template policy | Recoverable current-conversation gating | Detached work hides blockers | Runbook forbids detached agents | baseline |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the execution ledger.

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
   - Apply the plain-language gate before accepting the result artifact.
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
- avoids unsupported soft language such as `surrogate`, `proxy`, `stabilized`,
  `contract`, `reasonable`, `practical`, or `approximately correct`;
- labels unsupported claims as `unsupported` or `not checked`;
- labels mismatches as `wrong relative to the stated target`;
- states what remains unproved or unevaluated.

## Claude Review Protocol

Use Claude only as read-only reviewer. Bounded review prompts must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review only the cited fixed paths or packet excerpts.

End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

If Claude does not respond, run a tiny probe. If the probe succeeds, narrow the
prompt. If Claude is unavailable or policy-blocked, replace the review with a
fresh Codex read-only review.

## Launch Rule

After the master program, runbook, ledger, stop handoff, Phase 0 subplan, and
launch review bundle are written and reviewed, launch Phase 0 only. Continue to
later phases only through the gated handoff conditions.
