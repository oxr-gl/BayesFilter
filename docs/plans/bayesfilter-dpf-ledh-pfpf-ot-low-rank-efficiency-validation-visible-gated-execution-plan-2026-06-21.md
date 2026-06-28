# Visible Gated Execution Runbook: Low-Rank LEDH/PFPF-OT Efficiency Validation

Date: 2026-06-21

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_ROUND_2`

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

Full stdout/stderr is an artifact, not chat content.  TensorFlow/CUDA and
Claude commands must write logs under `docs/benchmarks/logs/`; the session
should inspect bounded summaries only.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-master-program-2026-06-21.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-claude-review-ledger-2026-06-21.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-visible-execution-ledger-2026-06-21.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-visible-stop-handoff-2026-06-21.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance/review/GPU preflight | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p00-governance-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p00-governance-result-2026-06-21.md` |
| P01 | Common harness and small sanity | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p01-harness-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p01-harness-result-2026-06-21.md` |
| P02 | Paired feasible-N GPU screen | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p02-paired-gpu-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p02-paired-gpu-result-2026-06-21.md` |
| P03 | Large-N low-rank envelope | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p03-large-n-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p03-large-n-result-2026-06-21.md` |
| P04 | Final closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p04-closeout-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-result-2026-06-21.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the low-rank route make LEDH/PFPF-OT TF32 more efficient for large particle counts? |
| Baseline/comparator | Existing streaming TF32 route on the same fixture, same physical GPU, same `CUDA_VISIBLE_DEVICES`, same TF32 state, and same fixed timeout; large-N low-rank-only rows are unpaired envelope evidence only. |
| Primary pass criterion | Low-rank passes validity, TF32, same-GPU, and bounded output-comparability gates and meets predeclared memory/speed paired screen on at least two adjacent paired sizes, or supports executable-envelope improvement where streaming fails under fixed timeout/OOM/failure and low-rank passes that same row. |
| Veto diagnostics | Validity failure, output-comparability failure for a claimed efficiency row, missing route evidence, invalid comparator artifact, GPU not trusted, TF32 mismatch/off for TF32 claim, mixed physical GPU in one paired claim, missing timing/memory fields, unsupported claim, or shared/default edit. |
| Explanatory diagnostics | Runtime, memory, ESS after validity gates, GPU selection, large-N completion, and dense materialization byte estimates. |
| Not concluded | No posterior correctness, dense Sinkhorn equivalence, HMC readiness, public API readiness, production/default readiness, or broad scalable-OT selection. |
| Artifacts | Phase JSON/Markdown/results, logs, execution ledger, final result. |

## Fixed Criteria

- low-rank active route invocations must be `> 0` and equal active mask count;
- low-rank sentinel transport shape must be `[B, 0, 0]`;
- all outputs must be finite;
- low-rank factor residuals must be `<= 5.0e-3`;
- output log-weight normalization must be `<= 1.0e-6`;
- TF32 state must be enabled and identical for both paired routes;
- one physical GPU must be used for all rows contributing to one paired claim;
- paired ladder is `[1024, 2048, 4096, 8192, 16384, 32768, 50000, 100000]`;
- P02 per-route row timeout is `900s`;
- P03 low-rank row timeout is `1200s`;
- bounded output comparability is a hard gate for rows used in an efficiency
  claim: same shapes, finite summaries, normalized log weights, ESS fraction
  `>= 0.01`, and low-rank-vs-streaming state-mean proxy relative L2 `<= 0.5`
  or absolute L2 `<= 1.0`;
- memory improvement screen requires at least `2x` lower low-rank peak allocator delta on at least two adjacent feasible sizes;
- speed improvement screen requires at least `1.25x` lower low-rank warm-call median on at least two adjacent feasible sizes;
- large-N low-rank-only rows do not by themselves establish speedup or
  superiority over streaming at that `N`.

## GPU Selection

Prefer GPU1 via `CUDA_VISIBLE_DEVICES=1`; use GPU0 only if GPU1 is busy,
unavailable, or unsuitable, and record the fallback reason.  If GPU fallback
is needed mid-phase, paired rows already collected for that phase are invalid
for a paired claim until the phase is restarted on one physical GPU.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract, append ledger entry.
2. `EXECUTE_MINIMAL`: run visible current-conversation commands only.
3. `ASSESS_GATE`: compare outputs to hard criteria and write result.
4. `PASS_REVIEW`: use Claude as read-only reviewer for material plans/results.
5. `REPAIR_LOOP`: patch fixable blockers, rerun focused checks, stop after five Claude rounds for same blocker.
6. `ADVANCE_OR_STOP`: advance only after phase gate passes or write stop handoff.

## Claude Read-Only Review Template

Use path-only review:

```text
READ-ONLY REVIEW ONLY.
Do not edit files, run experiments, launch agents, or change state.
Review this single absolute master-program path and only same-prefix docs/plans
paths named inside it: <path>.
Findings first. End with exactly VERDICT: AGREE or VERDICT: REVISE.
```
