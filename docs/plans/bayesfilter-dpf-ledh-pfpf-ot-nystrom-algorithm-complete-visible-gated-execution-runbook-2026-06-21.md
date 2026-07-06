# Nystrom Algorithm-Complete Visible Gated Execution Runbook

Date: 2026-06-21

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested execution supervisor. Do not
use `codex exec`, detached `tmux`, `nohup`, `setsid`, copied workspaces, or
backgrounded phase runners.

## Quiet Visible Execution Pattern

Full command output is an artifact, not chat content. Long TensorFlow/GPU and
Claude commands must write logs under `docs/benchmarks/logs/` or be captured by
the Claude wrapper. Chat receives only exit status, artifact paths, pass/fail
fields, and bounded tails on failure.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-master-program-2026-06-21.md`

Review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-claude-review-ledger-2026-06-21.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-visible-execution-ledger-2026-06-21.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-visible-stop-handoff-2026-06-21.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance and source lock | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p00-governance-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p00-governance-result-2026-06-21.md` |
| P01 | Implementation and harness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p01-implementation-harness-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p01-implementation-harness-result-2026-06-21.md` |
| P02 | Small dense-reference validation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p02-small-reference-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p02-small-reference-result-2026-06-21.md` |
| P03 | Downstream LEDH smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p03-downstream-smoke-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p03-downstream-smoke-result-2026-06-21.md` |
| P04 | Trusted GPU scale envelope | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p04-gpu-scale-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p04-gpu-scale-result-2026-06-21.md` |
| P05 | Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p05-closeout-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-result-2026-06-21.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the Nystrom candidate become a real leaderboard-ready diagnostic candidate? |
| Baseline/comparator | Small dense-reference TensorFlow transport, downstream LEDH smoke, and GPU scale envelope; streaming default only as operational context. |
| Primary pass criterion | P00-P05 complete required gates and final closeout records no hard vetoes for required phases. |
| Veto diagnostics | Missing artifacts, failed tests/checks, nonfinite output, residual failure, CPU fallback in GPU phase, dense materialization, wrong baseline, unsupported claim. |
| Explanatory diagnostics | Runtime, memory, dense-reference drift, ranks, landmarks, GPU metadata. |
| Not concluded | No default change, final ranking, posterior correctness, HMC readiness, public API readiness, or statistical superiority. |
| Artifacts | Paths listed in master program and subplans. |

## Skeptical Plan Audit Requirement

Before every material phase, Codex records a skeptical audit against wrong
baselines, proxy metrics, stop conditions, unfair comparisons, hidden
assumptions, stale context, environment mismatch, and artifact mismatch.

## Visible State Machine

For each phase:

1. `PRECHECK`: read the phase subplan, confirm prerequisites, restate evidence
   contract, append ledger entry.
2. `EXECUTE_MINIMAL`: run only necessary visible commands, preserving unrelated
   dirty worktree changes.
3. `ASSESS_GATE`: compare artifacts to primary criteria and veto diagnostics.
4. `PASS_REVIEW`: use Claude as read-only reviewer for material plan/result
   changes.
5. `REPAIR_LOOP`: patch visibly, rerun focused checks, and retry review up to
   five rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after gate pass; otherwise write blocker or
   handoff.

## Claude Read-Only Review Template

Use compact prompts with paths and summaries, not pasted full files. The prompt
must ask Claude to check wrong baseline, proxy metric promotion, missing stop
condition, unfair comparison, hidden assumption, stale context, environment
mismatch, unsupported claim, and artifact mismatch. Claude must end with exactly
`VERDICT: AGREE` or `VERDICT: REVISE`.
