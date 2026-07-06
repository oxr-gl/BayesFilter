# Actual-SIR Nystrom N8192 Paired-Drift Diagnostic Visible Gated Execution Runbook

Date: 2026-06-23

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested execution agent. The only
allowed cross-agent action is bounded read-only Claude review through
`bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh` when a subplan
requires it.

## Quiet Visible Execution Pattern

Full stdout/stderr is an artifact, not chat content. Predeclare log and
structured artifact paths, redirect full output to logs, and summarize only
bounded status and JSON fields in chat.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-master-program-2026-06-23.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-claude-review-ledger-2026-06-23.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-visible-execution-ledger-2026-06-23.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-visible-stop-handoff-2026-06-23.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance and review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p00-governance-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p00-governance-result-2026-06-23.md` |
| P01 | Fixed-policy replay and seed replication | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p01-fixed-policy-replay-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p01-fixed-policy-replay-result-2026-06-23.md` |
| P02 | Repair candidate selection | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p02-repair-selection-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p02-repair-selection-result-2026-06-23.md` |
| P03 | Focused repair test | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p03-focused-repair-test-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p03-focused-repair-test-result-2026-06-23.md` |
| P04 | Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p04-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p04-closeout-result-2026-06-23.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the `N=8192` paired mean drift reproducible, stochastic/inconclusive, a harness issue, or repairable? |
| Baseline/comparator | Compiled streaming TF32 actual-SIR route in the same artifact. |
| Primary pass criterion | P01 classifies replay/replication before any repair; P02/P03 run only if P01 justifies repair. |
| Veto diagnostics | Missing artifact, GPU/TF32 evidence missing, fixed-policy metadata drift in P01, nonfinite outputs, residual hard veto, runtime timeout, unsupported claim. |
| Explanatory diagnostics | Paired deltas, route log likelihoods, residuals, factor/scaling diagnostics, runtime, memory. |
| Not concluded | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness, no broad robustness. |
| Artifacts | Runbook, ledgers, subplans/results, benchmark JSON/Markdown/logs. |

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only commands needed for the phase.
3. `ASSESS_GATE`: compare artifacts to hard criteria and write phase result.
4. `PASS_REVIEW`: use Claude read-only review only when required by the active
   subplan.
5. `ADVANCE_OR_STOP`: advance only after phase gate passes; stop on stated
   continuation vetoes.

## Human-Required Stop Conditions

Stop if continuing would require default-policy changes, package installation,
network fetch beyond Claude review, destructive actions, criteria changes after
seeing results, or tuning before a reviewed P02 repair-selection phase.
