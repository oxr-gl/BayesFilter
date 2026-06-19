# P69 Visible Gated Execution Runbook

Date: 2026-06-15

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution is needed later, stop and write a separate
detached-supervisor plan.  This runbook is for visible, recoverable execution
inside the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p69-claude-review-ledger-2026-06-15.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p69-visible-execution-ledger-2026-06-15.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p69-visible-stop-handoff-2026-06-15.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and claim-boundary baseline | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase0-governance-claim-boundary-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase0-governance-claim-boundary-result-2026-06-15.md` |
| 1 | Holdout/replay diagnostic design | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase1-holdout-replay-design-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase1-holdout-replay-design-result-2026-06-15.md` |
| 2 | Holdout/replay implementation and focused tests | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase2-holdout-replay-implementation-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase2-holdout-replay-implementation-result-2026-06-15.md` |
| 3 | Adjacent ladder rerun with holdout/replay evidence | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-rerun-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-rerun-result-2026-06-15.md` |
| 4 | Rank-channel activity and degree-instability diagnosis | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase4-structural-diagnosis-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase4-structural-diagnosis-result-2026-06-15.md` |
| 5 | Fixed-variant repair decision or adaptive-reproduction fork | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5-route-decision-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5-route-decision-result-2026-06-15.md` |
| 6 | d18 paper-scale SIR validation ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase6-d18-sir-validation-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase6-d18-sir-validation-result-2026-06-15.md` |
| 7 | d50/d100 scaling-route design and preflight | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase7-scaling-route-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase7-scaling-route-result-2026-06-15.md` |
| 8 | Fixed-branch derivative and HMC-readiness diagnostics | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase8-hmc-readiness-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase8-hmc-readiness-result-2026-06-15.md` |
| 9 | p50, source-ledger, and closeout refresh | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase9-document-closeout-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase9-document-closeout-result-2026-06-15.md` |

Only Phase 0 is authorized at initial launch.  Each later phase requires a
dedicated subplan and review before execution.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining Zhao--Cui fixed-HMC adaptation work be governed phase by phase without overclaiming source faithfulness, d18 correctness, scaling, or HMC readiness? |
| Baseline/comparator | P50 fixed-branch document, P65--P68 result artifacts, Zhao--Cui paper, author source snapshot, and source-governance charter. |
| Primary pass criterion | The master program, runbook, Phase 0 result, and Phase 1 subplan converge under skeptical and Claude review, with all remaining gaps classified and no forbidden claim emitted. |
| Veto diagnostics | Wrong target lane; adaptive parity language without anchors; missing holdout/replay gap; rank zero-delta promoted to convergence; degree-ladder failure ignored; missing stop conditions; detached/background execution. |
| Explanatory diagnostics | Source-anchor inventories, P65--P68 statuses, fit diagnostics, existing adjacent-ladder deltas, MathDevMCP verification boundary, dirty-worktree scope. |
| Not concluded | No implementation repair, no new validation pass, no d18 correctness, no d50/d100 scaling, no HMC readiness, no adaptive source-faithful reproduction. |
| Artifacts | P69 master program, runbook, ledger, review ledger, stop handoff, Phase 0 result, Phase 1 subplan. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Fixed-HMC adaptation as current target | P50/P65--P68 and AGENTS source-anchor gate | Current implementation freezes branch choices for differentiability. | Adaptive parity accidentally claimed. | Phase 0 claim taxonomy check. | hypothesis pending review |
| CPU-only Phase 0 checks | Phase 0 is governance/documentary | No GPU/HMC work occurs in Phase 0. | TensorFlow GPU chatter misread as evidence. | Set CPU-only only for any framework import; otherwise use read-only text checks. | planned |
| P68 as immediate predecessor | Latest adjacent-ladder result | P68 closed diagnostic-exposure gap but left holdout/replay and degree instability open. | Stale result if artifacts changed. | Phase 0 inspect current files and status. | to verify |
| Claude as read-only reviewer | User prompt and governance policy | Additional skeptical review without delegating authority. | Claude treated as executor or authority. | Prompts state READ-ONLY REVIEW ONLY and verdict format. | planned |

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
- artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
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
