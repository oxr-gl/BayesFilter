# P70 Visible Gated Execution Runbook

Date: 2026-06-16

## Status

`VISIBLE_EXECUTION_PHASE6F_BLOCKED_LOWER_GATE_FAILURE_AND_RANK3_CONDITION_VETO_CLAUDE_AGREE_PHASE7_BLOCKED`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

When this runbook is launched later, it must be run visibly inside the current
Codex conversation.  Do not ask another agent to execute the runbook.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p70-claude-review-ledger-2026-06-16.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-execution-ledger-2026-06-16.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-stop-handoff-2026-06-16.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and source-anchor reset | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase0-governance-source-anchor-reset-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase0-governance-source-anchor-reset-result-2026-06-16.md` |
| 1 | Mathematical fixed-branch contract audit | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase1-mathematical-fixed-branch-contract-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase1-mathematical-fixed-branch-contract-result-2026-06-16.md` |
| 2 | Current-code gap audit | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase2-current-code-gap-audit-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase2-current-code-gap-audit-result-2026-06-16.md` |
| 3 | UKF-guided branch-builder design | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase3-ukf-guided-branch-builder-design-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase3-ukf-guided-branch-builder-design-result-2026-06-16.md` |
| 4 | Nondegenerate initialization and multi-sweep fitting design | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase4-nondegenerate-fitting-design-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase4-nondegenerate-fitting-design-result-2026-06-16.md` |
| 5 | Focused implementation and unit tests | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase5-focused-implementation-tests-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase5-focused-implementation-tests-result-2026-06-16.md` |
| 6 | Bounded rank-channel and normalizer diagnostic rerun | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-result-2026-06-16.md` |
| 6b | Condition-veto diagnostic capture blocker repair | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6b-condition-veto-capture-repair-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6b-condition-veto-capture-repair-result-2026-06-16.md` |
| 7 | Rank/degree ladder rerun gate | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase7-rank-degree-ladder-gate-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase7-rank-degree-ladder-gate-result-2026-06-16.md` |
| 8 | Sequential source-route recursion audit | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase8-sequential-source-route-recursion-audit-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase8-sequential-source-route-recursion-audit-result-2026-06-16.md` |
| 9 | Documentation and ledger refresh | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase9-documentation-ledger-refresh-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase9-documentation-ledger-refresh-result-2026-06-16.md` |
| 10 | d18 validation planning decision | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase10-d18-validation-planning-decision-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase10-d18-validation-planning-decision-result-2026-06-16.md` |

Only Phase 0 may begin after explicit user launch approval.  Each later phase
requires its own current subplan and review before execution.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the UKF-guided fixed-branch repair be executed visibly, phase by phase, without overclaiming source faithfulness, validation, scaling, or HMC readiness? |
| Baseline/comparator | Current P59/P69 constant-path one-sweep fixed-TTSIRT path, P69 Phase 5c diagnostics, p50 fixed-branch mathematics, and Zhao--Cui author source anchors. |
| Primary pass criterion | A phase advances only when its result artifact exists, local checks pass, Claude review converges when required, and the next phase's exact entry conditions are produced. |
| Veto diagnostics | Wrong baseline; UKF as truth; proxy residuals used as correctness; missing stop conditions; unfair rank/degree comparisons; hidden source-anchor gaps; detached execution; threshold changes after seeing results. |
| Explanatory diagnostics | Branch identities, UKF scout summaries, channel norms, sweep diagnostics, normalizer terms, holdout/replay residuals, condition numbers, source-anchor coverage. |
| Not concluded | No adaptive Zhao--Cui parity, no d18 correctness, no scaling, no HMC readiness, no paper or author-code failure claim. |
| Artifacts | Master program, runbook, visible execution ledger, Claude review ledger, phase subplans/results, stop handoff. |

## Executable Diagnostic Approval Gate

Phase 0 and Phase 1 do not authorize a repaired diagnostic run.  The first
executable repaired diagnostic is Phase 6, and it requires:

- Phase 5 implementation and focused-test result;
- reviewed Phase 6 subplan;
- frozen Phase 6 evidence contract with exact baseline/comparator, primary
  pass criterion, veto diagnostics, explanatory diagnostics, nonclaims, and
  result artifacts;
- explicit user approval for the visible run.

Phase 7 requires an explicit Phase 6 lower-gate pass and its own reviewed
evidence contract before any ladder command is executed.  If a threshold or
promotion criterion is missing before a diagnostic or ladder run, the phase
blocks rather than setting the value after seeing results.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| UKF guides branch design only | p50 UKF scout section; `ukf_scout.py:13-22`; `rank_budget.py:330-365` | UKF moments can give centers/scales/covariance but not correctness. | UKF promoted to oracle. | Phase 0 source-anchor ledger and Phase 3 branch-builder nonclaims. | planned |
| Fixed-HMC adaptation target | p50 fixed-branch section and AGENTS source gate | HMC differentiability requires frozen branch choices. | Adaptive parity overclaim. | Every phase classifies behavior as `source_faithful`, `fixed_hmc_adaptation`, or `extension_or_invention`. | planned |
| Rank-channel activation as repair target | P69 Phase 5c result | Current declared higher-rank channels are exactly zero in realized fits. | Treating collapse as proof rank 1 suffices. | Phase 4/6 channel-activity gates. | planned |
| Degree/normalizer stabilization as separate target | P69 Phase 5c result | Degree 2 improved fit residual but destabilized normalizer/holdout/replay. | In-sample residual becomes proxy for validity. | Phase 6/7 normalizer and holdout/replay vetoes. | planned |
| Visible execution only | User prompt and runbook template | User asked for visible plan and no detached launch. | Accidental background launch. | Runbook forbids detached/nested execution. | planned |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the execution ledger.

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

1. `PRECHECK`
   - Read the current phase subplan.
   - Confirm entry conditions inherited from the previous phase.
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
4. `DRAFT_NEXT`
   - Draft or refresh the next phase subplan.
   - Ensure the current result explicitly produces the next phase entry
     conditions.
5. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
6. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker.
7. `ADVANCE_OR_STOP`
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

Use Claude only as a reviewer.  The prompt must say:

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
- source-anchor gap;
- human readability for mathematical prose when documents are reviewed.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

If Claude does not respond, run a tiny read-only probe.  If the probe responds,
redesign the original prompt and retry with a smaller bounded review scope.

## Human-Required Stop Conditions

Stop if continuing would require:

- launching this runbook without explicit user approval;
- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- using Claude as executor or authority rather than read-only reviewer;
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
