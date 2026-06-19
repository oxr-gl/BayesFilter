# Wave 2 Visible Gated Execution Runbook

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

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-coordinator-master-program-2026-06-19.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-launch-review-packet-2026-06-19.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-claude-review-ledger-2026-06-19.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-visible-execution-ledger-2026-06-19.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-visible-stop-handoff-2026-06-19.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| W2-0 | Coordinator Launch Packet And Review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p00-coordinator-launch-packet-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p00-coordinator-launch-packet-result-2026-06-19.md` |
| W2-1 | Current-Agent Positive-Feature Execution | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p01-current-positive-feature-execution-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p01-current-positive-feature-execution-result-2026-06-19.md` |
| W2-2 | Final Coordinator Merge | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p02-final-merge-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-final-merge-result-2026-06-19.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Wave 2 execute current-agent positive-feature Sinkhorn to closeout while preserving independent peer-agent low-rank closeout and final-only merge? |
| Baseline/comparator | Wave 2 master program, positive-feature source/Phase 5 context, peer-agent final low-rank status, Phase 1/Phase 3 shared contracts. |
| Primary pass criterion | W2-0 review converges, W2-1 positive-feature diagnostics pass or block under contract, W2-2 merge records both lane final statuses without ranking. |
| Veto diagnostics | Shared contract conflict, write-set collision, unsupported claim, missing final lane status, nonconvergent material review, or unapproved boundary crossing. |
| Explanatory diagnostics | Runtime/logs, dense-reference semantic deltas, Claude findings, existing peer-agent low-rank status. |
| Not concluded | No speedup, ranking, posterior correctness, HMC/API/production/default readiness, dense equivalence, or broad scalable-OT selection. |
| Artifacts | Phase results, lane results/statuses, diagnostics, review ledger, final merge. |

## Approval Record

The user requested execution of the prompt and explicitly included Claude Opus
max-effort read-only review plus launch after the execution plan is written.
Current permitted command classes for this visible run:

- local file writes under `docs/plans`, `docs/benchmarks`, and `tests`;
- local `python -m py_compile`;
- local `pytest -q` focused tests;
- CPU-scoped TensorFlow diagnostics with `CUDA_VISIBLE_DEVICES=-1`;
- Claude read-only review through the approved
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh` wrapper.

Not approved by this runbook:

- package installation;
- network fetches other than Claude Code reviewer access through the approved
  wrapper;
- GPU evidence or benchmarks;
- public API/default/export changes;
- destructive filesystem/git operations;
- detached overnight execution.

## Quiet Visible Execution Pattern

Full TensorFlow and Claude output should be redirected to log files when large.
The session should report bounded summaries: exit status, artifact paths,
pass/fail fields, and short failure tails.

## Skeptical Plan Audit

Before each phase, Codex checks for wrong baselines, proxy metrics promoted to
criteria, missing stop conditions, unfair comparisons, hidden assumptions,
stale context, environment mismatch, and commands whose artifacts would not
answer the phase question.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, verify prerequisites, restate evidence contract.
2. `EXECUTE_MINIMAL`: run only visible scoped commands.
3. `ASSESS_GATE`: compare outputs against criteria and write result artifact.
4. `PASS_REVIEW`: use Claude read-only review for material planning/claim
   issues.
5. `REPAIR_LOOP`: patch lane/coordinator-owned files, rerun focused checks,
   and retry review up to five rounds for the same blocker.
6. `ADVANCE_OR_STOP`: continue only after the gate passes.

## Final Visible Handoff

At completion or stop, write final phase reached, status, result artifacts,
Claude review trail, tests/diagnostics run, unresolved blockers, non-claims,
and safest next human decision.
