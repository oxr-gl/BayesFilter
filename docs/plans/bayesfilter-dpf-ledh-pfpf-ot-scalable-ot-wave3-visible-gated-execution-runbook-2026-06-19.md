# Wave 3 Visible Gated Execution Runbook

Date: 2026-06-19

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_NOT_YET_REVIEWED`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook does not launch detached agents, `codex exec`, detached
supervisors, backgrounded phase runners, or copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-master-program-2026-06-19.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-launch-review-packet-2026-06-19.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-claude-review-ledger-2026-06-19.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-visible-execution-ledger-2026-06-19.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-visible-stop-handoff-2026-06-19.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| W3-0 | Launch Packet And Review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p00-launch-review-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p00-launch-review-result-2026-06-19.md` |
| W3-1 | Artifact Audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p01-artifact-audit-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p01-artifact-audit-result-2026-06-19.md` |
| W3-2 | Common Downstream Smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p02-downstream-smoke-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p02-downstream-smoke-result-2026-06-19.md` |
| W3-3 | Closeout And Next Decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p03-closeout-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-result-2026-06-19.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Wave 3 audit artifacts and run a common downstream smoke without hard vetoes or unsupported ranking/default claims? |
| Baseline/comparator | Wave 2 final merge, Wave 2 JSON artifacts, and shared deterministic fixtures. |
| Primary pass criterion | W3-0 review passes; W3-1 artifact audit passes; W3-2 smoke passes or writes a blocker under hard-veto rules; W3-3 records non-ranking closeout. |
| Veto diagnostics | Missing/invalid artifacts, nonfinite outputs, shape/log-weight failures, unsupported claim, shared/default/public boundary crossing, or nonconvergent review. |
| Explanatory diagnostics | Moment deltas, wall time, residual metadata, fixture coverage. |
| Not concluded | No ranking, speedup, posterior correctness, HMC/API/production/default readiness, dense equivalence, or broad scalable-OT selection. |
| Artifacts | Phase results, JSON/Markdown diagnostics, review ledger, final result. |

## Approval Record

The user requested creation, Claude review, visible runbook, approval request,
and launch.  Current permitted command classes for this visible run:

- local file writes under `docs/plans`, `docs/benchmarks`, and `tests`;
- local `python -m py_compile`;
- local focused `pytest -q`;
- CPU-scoped TensorFlow diagnostics with `CUDA_VISIBLE_DEVICES=-1`;
- Claude read-only review through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh`.

Not approved by this runbook:

- package installation;
- network fetches other than Claude Code reviewer access through the approved
  wrapper;
- GPU evidence or benchmarks;
- public API/default/export changes;
- destructive filesystem/git operations;
- detached overnight execution.

## Skeptical Plan Audit

Before each phase, Codex checks for wrong baselines, proxy metrics promoted to
criteria, missing stop conditions, unfair comparisons, hidden assumptions,
stale context, environment mismatch, and commands whose artifacts would not
answer the phase question.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan and verify prerequisites.
2. `EXECUTE_MINIMAL`: run only scoped visible commands.
3. `ASSESS_GATE`: compare outputs to evidence contract and write result.
4. `PASS_REVIEW`: use Claude read-only review for material planning/claim
   issues.
5. `REPAIR_LOOP`: patch Wave-3-owned files, rerun focused checks, retry review
   up to five rounds for same blocker.
6. `ADVANCE_OR_STOP`: continue only after gate passes.
