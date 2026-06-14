# Visible Gated Execution Runbook: Li-Coates Algorithm 1 LEDH-PFPF UKF

Date: 2026-06-10

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_FOR_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-master-program-2026-06-10.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-claude-review-ledger-2026-06-10.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-execution-ledger-2026-06-10.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-stop-handoff-2026-06-10.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P0 | Governance and Evidence Quarantine | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-result-2026-06-10.md` |
| P1 | LaTeX Documentation Rewrite | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-result-2026-06-10.md` |
| P2 | UKF Covariance Lifecycle Design | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-result-2026-06-10.md` |
| P3 | Algorithm 1 Implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md` |
| P4 | Faithfulness Audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-result-2026-06-10.md` |
| P5 | Test Rerun And Comparisons | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-result-2026-06-10.md` |
| P6 | Supersession Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-result-2026-06-10.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current dialogue visibly replace the old LEDH-PFPF-OT evidence with a Li-Coates Algorithm 1, UKF-covariance-lifecycle implementation and rerun all relevant comparisons? |
| Baseline/comparator | Li-Coates Algorithm 1 source anchors; existing BayesFilter docs; prior LEDH-PFPF-OT artifacts only as quarantined historical lineage. |
| Primary pass criterion | P4 faithfulness passes and P5 rerun artifacts report finite, reviewed value and gradient comparisons for the new Algorithm 1 implementation. |
| Veto diagnostics | Missing per-particle covariance lifecycle, unsupported doc claims, old implementation path used as replacement, non-finite numerical state, failed Claude convergence, hidden detached execution. |
| Explanatory diagnostics | Runtime, ESS, MC intervals, old-vs-new deltas, filter rankings on compatible models. |
| Not concluded | No production default, HMC readiness, universal superiority, or source-faithful status for OT resampling itself. |
| Artifacts | This runbook, phase result files, visible execution ledger, Claude review ledger, comparison JSON/Markdown outputs, final stop handoff if needed. |

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
4. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Ledger Entry Template

```markdown
### <timestamp> - Phase <N> - <STATE>

Evidence contract:

- Question:
- Baseline/comparator:
- Primary criterion:
- Veto diagnostics:
- Non-claims:

Actions:

- <commands/edits/reviews>

Artifacts:

- <paths>

Gate status:

- <PASSED/BLOCKED/FAILED/IN_PROGRESS>

Next action:

- <next visible step>
```

## Claude Read-Only Review Template

Use Claude only as a reviewer. The prompt must say:

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
- artifact mismatch;
- missing Li-Coates Algorithm 1 covariance lifecycle obligation.
- insufficient quarantine or supersession of previous LEDH-PFPF-OT evidence;
- any wording that treats UKF as paper-mandated rather than a permitted,
  requested Algorithm 1 covariance option;
- any wording that treats OT resampling as source Li-Coates Algorithm 1 rather
  than a BayesFilter extension;
- missing full run manifest for serious implementation or comparison runs.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

## Human-Required Stop Conditions

Stop if continuing would require:

- deleting historical artifacts rather than superseding them;
- changing pass/fail criteria after seeing results;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing BayesFilter default policy;
- modifying unrelated dirty user work;
- interpreting GPU/CUDA results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests/benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
