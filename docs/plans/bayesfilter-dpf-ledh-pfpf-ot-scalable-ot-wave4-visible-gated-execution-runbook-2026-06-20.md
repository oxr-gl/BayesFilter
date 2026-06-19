# Wave 4 Visible Gated Execution Runbook

Date: 2026-06-20

## Status

`VISIBLE_EXECUTION_LAUNCHED_STOPPED_WAITING_FOR_PEER_LOW_RANK_ARTIFACTS`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook does not launch detached agents, `codex exec`, detached
supervisors, backgrounded phase runners, or copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-master-program-2026-06-20.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-launch-review-packet-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-claude-review-ledger-2026-06-20.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-visible-execution-ledger-2026-06-20.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-visible-stop-handoff-2026-06-20.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| W4-0 | Launch Packet And Review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p00-launch-review-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p00-launch-review-result-2026-06-20.md` |
| W4-1 | Peer Low-Rank Lane Handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p01-peer-low-rank-handoff-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p01-peer-low-rank-handoff-result-2026-06-20.md` |
| W4-2 | Current Positive-Feature Lane | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p02-current-positive-feature-validation-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-positive-feature-result-2026-06-20.md` |
| W4-3 | Final Merge And Inference Status | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p03-final-merge-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-final-merge-result-2026-06-20.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can each Wave 4 lane pass a replicated downstream resampling hard screen while preserving independent-lane and no-ranking boundaries? |
| Baseline/comparator | Exact weighted input estimates for each fixture; naive uniform-no-transport is explanatory only. |
| Primary pass criterion | W4-0 review passes; W4-1 peer handoff is written; W4-2 current lane passes or writes a blocker; W4-3 final merge runs only after peer lane artifacts exist. |
| Veto diagnostics | Missing/invalid artifacts, nonfinite outputs, shape/log-weight failures, residual or moment screen failures, unsupported claim, shared/default/public boundary crossing, peer artifact absence for final merge, or nonconvergent review. |
| Explanatory diagnostics | Runtime, naive baseline errors, candidate-vs-naive deltas, per-fixture/per-seed summaries, and residual magnitudes. |
| Not concluded | No ranking, speedup, posterior correctness, HMC/API/production/default readiness, dense equivalence, broad scalable-OT selection, or scientific superiority. |
| Artifacts | Phase results, JSON/Markdown diagnostics, peer task note, review ledger, final merge or stop handoff. |

## Approval Record

The user requested creation, Claude review, visible runbook, and launch.  Current
permitted command classes for this visible run:

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
- detached overnight execution;
- current-agent execution of the peer low-rank algorithm lane.

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
5. `REPAIR_LOOP`: patch Wave-4-owned files, rerun focused checks, retry review
   up to five rounds for same blocker.
6. `ADVANCE_OR_STOP`: continue only after gate passes.

## Claude Prompt Recovery

If Claude does not respond, Codex runs a tiny read-only probe.  If the probe
responds, Codex redesigns the compact review prompt and retries.  If Claude
does not converge after five rounds for the same material blocker, Codex writes
a blocker result and stops.
