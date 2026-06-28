# Visible Gated Execution Runbook: Low-Rank LEDH/PFPF-OT Filter Integration Scale

Date: 2026-06-20

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

## Quiet Visible Execution Pattern

Full stdout/stderr is an artifact, not chat content.  Commands that may produce
large TensorFlow/CUDA/Claude output must write logs under
`docs/benchmarks/logs/` and the session should inspect bounded summaries only.

Required pattern:

1. Predeclare log and structured artifact paths before running.
2. Redirect full stdout/stderr to the log file.
3. Prefer commands that write JSON/Markdown artifacts directly.
4. After the command, report exit status, artifact paths, pass/fail fields, and
   at most the last 40 log lines on failure.
5. Do not hide failures; logs and structured artifacts must be referenced from
   phase results.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-master-program-2026-06-20.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-claude-review-ledger-2026-06-20.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-visible-execution-ledger-2026-06-20.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-visible-stop-handoff-2026-06-20.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance/source/plan review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p00-governance-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p00-governance-result-2026-06-20.md` |
| P01 | Harness/small CPU invariants | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p01-harness-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p01-harness-result-2026-06-20.md` |
| P02 | CPU tuning and focused repair | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p02-tuning-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p02-tuning-result-2026-06-20.md` |
| P03 | Medium CPU filter-scale | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p03-medium-cpu-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p03-medium-cpu-result-2026-06-20.md` |
| P04 | Trusted GPU 50k/100k scale | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p04-trusted-gpu-scale-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p04-trusted-gpu-scale-result-2026-06-20.md` |
| P05 | Final closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p05-closeout-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-result-2026-06-20.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the tuned low-rank coupling route survive an actual LEDH/PFPF-OT filter-shaped TensorFlow loop at medium CPU scale and trusted GPU 50k/conditional 100k scale? |
| Baseline/comparator | Existing LEDH/PFPF-OT LGSSM fixture mechanics and low-rank component seed setting; dense Sinkhorn is not a scale comparator. |
| Primary pass criterion | Required active-resampling phase rows prove low-rank route execution inside the filter loop, pass hard finite/nonnegative/factor/log-weight/no-dense diagnostics, and all required artifacts exist. |
| Veto diagnostics | Crash/OOM/timeout, missing/zero low-rank route invocation evidence, invocation count mismatch, nonfinite output, invalid factor, residual threshold failure, missing artifact, dense transport materialized at scale, shared contract/default/public export edit, unsupported claim, or trusted GPU unavailable for P04. |
| Explanatory diagnostics | Runtime, memory, ESS, moment deltas, selected rank, selected assignment epsilon, TF32 status, GPU visibility. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or TF32-help claim. |
| Artifacts | Phase JSON/Markdown/results, logs, execution ledger, final result. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Lane-owned integration harness | User lane boundaries | Avoids public/default/shared changes | Harness not representative | Small no-resampling and active-resampling checks | pending |
| Tuned seed `rank=64`, `assignment_epsilon=0.015625` | Closed component lane | Seed only | Does not transfer | P02 tuning grid | pending |
| Runtime/memory explanatory | Evidence discipline | No fair comparison | Proxy promotion | Non-claim checks | pending |
| Trusted GPU for P04 | GPU policy | Avoid sandbox false negatives | GPU unavailable | Escalated command/result blocker | pending |

## Fixed Diagnostic Thresholds

The master program fixes hard thresholds before execution.  These values may
not be widened after seeing results:

- active rows require `low_rank_resampling_invocations > 0`;
- active rows require `low_rank_resampling_invocations == active_resampling_mask_count`;
- `max_factor_marginal_residual <= 5.0e-3`;
- `max_induced_row_residual <= 5.0e-3`;
- `max_induced_column_residual <= 5.0e-3`;
- `output_log_weight_normalization_residual <= 1.0e-6`;
- P01 tiny invariant rows require `tiny_materialized_apply_parity <= 1.0e-10`;
- filter outputs must be finite;
- scale rows must preserve sentinel `transport_matrix_shape == [B, 0, 0]`.

## Skeptical Plan Audit

Before executing each phase, Codex must record a skeptical audit in chat and in
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

1. `PRECHECK`: read the subplan, confirm prerequisites, restate evidence contract, append a ledger entry.
2. `EXECUTE_MINIMAL`: run only visible current-conversation commands.
3. `ASSESS_GATE`: compare outputs against hard criteria and write result.
4. `PASS_REVIEW`: use Claude as read-only reviewer for material results.
5. `REPAIR_LOOP`: patch fixable blockers, rerun focused checks, stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the current phase gate passes or write stop handoff.

## Claude Read-Only Review Template

Prompts must be path-only and include:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review these paths:
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
- shared-contract/public-default boundary safety.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```
