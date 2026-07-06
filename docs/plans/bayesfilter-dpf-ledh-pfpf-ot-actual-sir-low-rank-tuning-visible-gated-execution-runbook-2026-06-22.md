# Actual-SIR Low-Rank Tuning Visible Gated Execution Runbook

Date: 2026-06-22
Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

This is the visible, foreground runbook adapted from
`/home/ubuntu/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.
It is suitable for overnight-style gated progress inside the current
conversation, with Codex as supervisor/executor and Claude as read-only reviewer.

## Role Contract

Codex in this conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use `codex exec`,
`overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`, backgrounded
phase runners, or copied-workspace execution. If detached execution becomes
necessary, stop and write a separate detached-supervisor plan.

## Quiet Visible Execution Pattern

Full stdout/stderr is an artifact, not chat content. For TensorFlow/CUDA,
benchmark, long test, and Claude review commands:

1. Predeclare log and structured artifact paths in the phase subplan.
2. Redirect full stdout/stderr to the log file.
3. Prefer commands that write JSON/Markdown/result artifacts directly.
4. After completion, report only exit status, artifact paths, pass/fail fields,
   and at most the last 40 log lines on failure.
5. Poll bounded status rather than streaming large output.
6. Treat excessive stdout/stderr as an execution-flow defect and write a stop
   handoff if quiet execution fails.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-master-program-2026-06-22.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-visible-execution-ledger-2026-06-22.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-claude-review-ledger-2026-06-22.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-visible-stop-handoff-2026-06-22.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| ---: | --- | --- | --- |
| 0 | Governance and review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p00-governance-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p00-governance-result-2026-06-22.md` |
| 1 | Harness/grid readiness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p01-harness-grid-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p01-harness-grid-result-2026-06-22.md` |
| 2 | Tiny tuning smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p02-tiny-smoke-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p02-tiny-smoke-result-2026-06-22.md` |
| 3 | Tuning screen | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p03-tuning-screen-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p03-tuning-screen-result-2026-06-22.md` |
| 4 | Candidate freeze | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p04-candidate-freeze-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p04-candidate-freeze-result-2026-06-22.md` |
| 5 | Held-out support | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p05-heldout-support-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p05-heldout-support-result-2026-06-22.md` |
| 6 | Large-N envelope | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p06-large-n-envelope-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p06-large-n-envelope-result-2026-06-22.md` |
| 7 | Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p07-closeout-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-result-2026-06-22.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can tuned low-rank settings pass actual-SIR d18 validity/comparability screens and then support bounded efficiency or envelope claims? |
| Baseline/comparator | Existing compiled streaming actual-SIR TF32/GPU route through the owned validation harness. |
| Primary pass criterion | Frozen candidate passes held-out paired support rows with hard validity, comparability, same GPU UUID, TF32 provenance, and warm-time support. |
| Veto diagnostics | Hard validity failures, paired comparability failures, same-GPU provenance failure, missing artifacts, trusted GPU unavailable for GPU evidence, or boundary-crossing changes. |
| Explanatory diagnostics | Runtime, memory, first-call time, warm-call spread, ESS, projection iterations, and factor residual magnitudes. |
| Not concluded | No posterior correctness, HMC readiness, default/public API readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or statistical ranking. |
| Artifacts | Phase results, JSON/Markdown benchmark artifacts, logs, execution ledger, Claude review ledger, stop handoff. |

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, state evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible current-conversation commands.
3. `ASSESS_GATE`: compare artifacts against hard vetoes and pass criteria.
4. `PASS_REVIEW`: use Claude read-only review for material plans/results.
5. `REPAIR_LOOP`: patch same subplan for fixable blockers, rerun focused
   checks, and rerun Claude review up to five rounds.
6. `ADVANCE_OR_STOP`: advance only after gate passes; otherwise write handoff.

## Human-Required Stop Conditions

Stop if continuing requires package installation, network fetch, credentials,
destructive git/filesystem action, default-policy change, public API change,
criteria changes after seeing results, unrelated dirty-worktree modification, or
continuing after five unresolved Claude review rounds for the same blocker.

## Claude Read-Only Review Prompt Shape

The prompt must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the named paths only:
- <path>

Check wrong baseline, proxy metrics promoted to pass criteria, missing stop
condition, unfair comparison, hidden assumption, stale context, environment
mismatch, unsupported claim, artifact mismatch, consistency, feasibility, and
boundary safety.

Also check correctness, artifact coverage, and whether fixable tuning failures
continue through the planned repair loop instead of stopping without a valid
continuation veto.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Final Visible Handoff

When execution completes or stops, write final phase reached, final status,
result artifacts, Claude review trail, tests/benchmarks actually run,
unresolved blockers, what was not concluded, and safest next human decision.
