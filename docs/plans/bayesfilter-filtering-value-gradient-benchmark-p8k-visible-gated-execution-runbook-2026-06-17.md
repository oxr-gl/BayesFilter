# P8k Visible Gated Execution Runbook

Date: 2026-06-17

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-claude-review-ledger-2026-06-17.md`

Execution ledger:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-execution-ledger-2026-06-17.md`

Stop handoff:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-stop-handoff-2026-06-17.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and optimization contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase0-governance-optimization-contract-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase0-governance-optimization-contract-result-2026-06-17.md` |
| 1 | Generic configuration surface contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase1-config-surface-contract-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase1-config-surface-contract-result-2026-06-17.md` |
| 2 | Benchmark harness plumbing | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-benchmark-harness-plumbing-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-benchmark-harness-plumbing-result-2026-06-17.md` |
| 3 | Value-only diagnostics fast path | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-value-only-diagnostics-fastpath-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-value-only-diagnostics-fastpath-result-2026-06-17.md` |
| 4 | Inactive-transport skip path | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase4-inactive-transport-skip-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase4-inactive-transport-skip-result-2026-06-17.md` |
| 5 | Generic GPU profiling ladder | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-gpu-profiling-ladder-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-gpu-profiling-ladder-result-2026-06-17.md` |
| 6 | Generic linear-observation and transition-cache design | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase6-linear-observation-transition-cache-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase6-linear-observation-transition-cache-result-2026-06-17.md` |
| 7 | Closeout and next-lane boundary | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase7-closeout-boundary-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase7-closeout-boundary-result-2026-06-17.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the batched TF32/GPU DPF engine be made faster or more configurable through generic opt-in controls without crossing scientific boundaries? |
| Baseline/comparator | Current LGSSM streaming benchmark behavior plus current P8j experimental streaming adapter behavior.  P8j `N=10000` and `N=50000` actual-SIR artifacts are reference evidence and stress-case motivation, not promotion baselines or particle-adequacy evidence. |
| Primary pass criterion | Every phase either passes its declared gate with artifacts and review, or writes a blocker. |
| Veto diagnostics | SIR-only hidden optimization, runtime proxy promoted to particle adequacy, GPU outside trusted context, changed default without review, missing local checks. |
| Explanatory diagnostics | Runtime, compile time, memory, ESS when requested, finite values, configuration metadata. |
| Not concluded | Particle adequacy, leaderboard completion, exact likelihood, gradients, HMC/NUTS, production default. |
| Artifacts | Master program, subplans, result files, Claude ledger, execution ledger, stop handoff, JSON/markdown benchmark outputs. |

## Skeptical Plan Audit

Before each phase, Codex must check for wrong baselines, proxy metrics promoted
to pass criteria, missing stop conditions, unfair comparisons, hidden
assumptions, stale context, environment mismatch, and commands whose artifacts
would not answer the phase question.

If a material flaw is found, revise the plan or write a blocker before running
the phase.

## Visible State Machine

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run visible commands in the current conversation.
3. `ASSESS_GATE`: compare outputs against criteria and write result.
4. `PASS_REVIEW`: use Claude read-only review for material plans/results/diffs.
5. `REPAIR_LOOP`: patch visibly, rerun focused checks, stop after five Claude
   rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after gate pass, otherwise write handoff.

## Claude Read-Only Review Template

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review:
- <phase result / blocker plan / implementation diff / final decision>

Check:
- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch,
credentials, destructive git/filesystem action, changing pass criteria after
results, changing defaults, modifying unrelated dirty work, running any
GPU/CUDA/TensorFlow GPU command without trusted/escalated context, interpreting
GPU results without trusted evidence, or continuing after five failed review
rounds.

## Final Visible Handoff

When execution completes or stops, write final phase reached, final status,
result artifacts, Claude review trail, tests/benchmarks actually run,
unresolved blockers, nonclaims, and safest next action.
