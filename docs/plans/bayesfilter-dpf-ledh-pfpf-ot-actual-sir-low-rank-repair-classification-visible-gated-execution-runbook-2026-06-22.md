# Actual-SIR Low-Rank Repair Classification Visible Gated Execution Runbook

Date: 2026-06-22
Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

This visible runbook is adapted from
`/home/ubuntu/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.
Codex is the supervisor and executor. Claude Opus max effort is a read-only
reviewer only.

## Role Contract

This runbook must not launch detached or nested execution. Bounded foreground
Claude review through
`/home/ubuntu/python/claudecodex/scripts/claude_worker.sh` is allowed only for
read-only review because it is part of the supervised review loop, not an
execution authority.

Do not use `codex exec`, `overnight_gated_launch.sh`, `setsid`, `nohup`,
detached `tmux`, backgrounded phase runners, or copied-workspace execution.

## Quiet Visible Execution Pattern

Full stdout/stderr is an artifact, not chat content. For noisy commands:

1. Predeclare log and structured artifact paths in the phase subplan.
2. Redirect full stdout/stderr to the log file.
3. Prefer commands that write JSON/Markdown/result artifacts directly.
4. After completion, report exit status, artifact paths, pass/fail fields, and
   at most the last 40 log lines on failure.
5. Poll bounded status rather than streaming large output.
6. Treat excessive stdout/stderr as an execution-flow defect.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-master-program-2026-06-22.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-visible-execution-ledger-2026-06-22.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-claude-review-ledger-2026-06-22.md`

Visible stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-visible-stop-handoff-2026-06-22.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| ---: | --- | --- | --- |
| 0 | Governance and launch audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p00-governance-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p00-governance-result-2026-06-22.md` |
| 1 | P03 artifact classifier | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p01-artifact-classifier-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p01-artifact-classifier-result-2026-06-22.md` |
| 2 | Code-path classifier | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p02-code-path-classifier-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p02-code-path-classifier-result-2026-06-22.md` |
| 3 | Conditional microprobe | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p03-conditional-microprobe-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p03-conditional-microprobe-result-2026-06-22.md` |
| 4 | Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p04-closeout-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-result-2026-06-22.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is P03 no-freeze best explained by route-performance repair, tuning/comparability/ESS repair, or both? |
| Baseline/comparator | P03 paired artifacts comparing low-rank route with compiled streaming actual-SIR TF32/GPU route. |
| Primary pass criterion | A bounded repair classifier and next handoff are written without crossing into implementation or promotion claims. |
| Veto diagnostics | Missing artifacts, stale source anchors, unsupported claims, route-internal edits, proxy metrics treated as promotion, or optional GPU probe without trusted context. |
| Explanatory diagnostics | Candidate labels, timing ratios, log-likelihood deltas, ESS hard vetoes, source timing asymmetry, and eager/host-sync anchors. |
| Not concluded | No speedup, candidate freeze, held-out support, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, or statistical ranking. |
| Artifacts | Phase results, execution ledger, Claude review ledger, optional microprobe artifacts, closeout, and stop handoff if needed. |

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, record skeptical audit.
2. `EXECUTE_MINIMAL`: run the smallest local command or inspection.
3. `ASSESS_GATE`: compare evidence against the phase contract.
4. `WRITE_RESULT`: write phase result or blocker result.
5. `PASS_REVIEW`: use Claude read-only review for material plans/results.
6. `REPAIR_LOOP`: patch same subplan for fixable blockers, rerun focused checks,
   and rerun Claude review up to five rounds.
7. `ADVANCE_OR_STOP`: advance only after gate passes; otherwise write handoff.

## Human-Required Stop Conditions

Stop if continuing requires package installation, network fetch, credentials,
destructive git/filesystem action, default-policy change, public API change,
criteria changes after seeing results, unrelated dirty-worktree modification,
route-internal implementation before a reviewed implementation subplan, or
continuing after five unresolved Claude review rounds for the same blocker.

## Claude Read-Only Review Prompt Shape

The prompt must be path-only and say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the named paths only:
- <path>

Check wrong baseline, proxy metrics promoted to pass criteria, missing stop
condition, unfair comparison, hidden assumption, stale context, environment
mismatch, unsupported claim, artifact mismatch, consistency, feasibility,
artifact coverage, boundary safety, and whether fixable repair issues continue
through the planned repair loop.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Final Visible Handoff

When execution completes or stops, write final phase reached, final status,
result artifacts, Claude review trail, tests/checks actually run, unresolved
blockers, what was not concluded, and safest next decision.
