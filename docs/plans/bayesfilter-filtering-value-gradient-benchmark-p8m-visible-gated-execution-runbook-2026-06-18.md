# P8m Visible Gated Execution Runbook

Date: 2026-06-18

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

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-claude-review-ledger-2026-06-18.md`

Execution ledger:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-visible-execution-ledger-2026-06-18.md`

Stop handoff:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-visible-stop-handoff-2026-06-18.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and generic boundary contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase0-governance-boundary-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase0-governance-boundary-result-2026-06-18.md` |
| 1 | Transport instrumentation design | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase1-instrumentation-design-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase1-instrumentation-design-result-2026-06-18.md` |
| 2 | Generic microbenchmark implementation | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-microbenchmark-implementation-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-microbenchmark-implementation-result-2026-06-18.md` |
| 3 | Trusted GPU chunk ladder | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-gpu-chunk-ladder-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-gpu-chunk-ladder-result-2026-06-18.md` |
| 4 | Exact implementation optimization decision | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase4-exact-optimization-decision-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase4-exact-optimization-decision-result-2026-06-18.md` |
| 5 | Exact implementation repair, if justified | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase5-exact-implementation-repair-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase5-exact-implementation-repair-result-2026-06-18.md` |
| 6 | Sinkhorn/epsilon validation contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase6-sinkhorn-validation-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase6-sinkhorn-validation-result-2026-06-18.md` |
| 7 | Administrative boundary closeout | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase7-cross-fixture-closeout-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase7-administrative-boundary-closeout-result-2026-06-18.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generic TensorFlow batched DPF transport core be profiled and optimized without SIR-specific shortcuts or scientific overclaims? |
| Baseline/comparator | Current streaming entropic OT transport route, with P8l actual-SIR d18 profile as stress evidence only. |
| Primary pass criterion | Every phase either passes its declared gate with artifacts and review, or writes a blocker. |
| Veto diagnostics | SIR-specific hidden optimization, runtime proxy promoted to adequacy, GPU outside trusted context, changed default without review, lower-iteration promotion without validation, missing local checks. |
| Explanatory diagnostics | Runtime, compile time, memory, finite values, configuration metadata, chunk sizes, residuals if available. |
| Not concluded | Particle adequacy, leaderboard completion, exact nonlinear likelihood, gradients, HMC/NUTS, production default. |
| Artifacts | Master program, subplans, result files, Claude ledger, execution ledger, stop handoff, JSON/markdown benchmark outputs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| SIR d18 as stress fixture only | P8l result | It exposed transport cost at high `N`, but is not representative of every model. | SIR-specific shortcuts creep into generic code. | Phase 0 text checks and Claude review. | hypothesis |
| Exact implementation separated from tuning | P8l iteration sensitivity | Lower iterations changed values. | Runtime win mistaken for exact optimization. | Phase 6 validation boundary. | reviewed-by-plan |
| Trusted GPU only for GPU evidence | AGENTS.md GPU policy | Sandbox can hide GPU access. | False GPU failure/success. | Escalated `nvidia-smi` and GPU runs. | required |

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
