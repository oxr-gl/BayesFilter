# P65 Visible Gated Execution Runbook

Date: 2026-06-14

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch detached or autonomous agents.  The only allowed
cross-agent command is a foreground, bounded, read-only Claude worker invocation
for review, with exact file paths, line spans, and questions, and with the output
preserved in the review ledger.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution is needed later, stop and write a separate
detached-supervisor plan.  This runbook is for visible, recoverable execution in
the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p65-fixed-branch-rank-capacity-master-program-2026-06-14.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p65-claude-review-ledger-2026-06-14.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p65-visible-execution-ledger-2026-06-14.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p65-visible-stop-handoff-2026-06-14.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, baseline, and launch readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase0-governance-baseline-subplan-2026-06-14.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase0-governance-baseline-result-2026-06-14.md` |
| 1 | One-factor rank/capacity diagnostic | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase1-rank-capacity-diagnostic-subplan-2026-06-14.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase1-rank-capacity-diagnostic-result-2026-06-14.md` |
| 2 | Bounded implementation repair | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase2-implementation-repair-subplan-2026-06-14.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase2-implementation-repair-result-2026-06-14.md` |
| 3 | Bug-test closeout and handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase3-bug-test-closeout-subplan-2026-06-14.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase3-bug-test-closeout-result-2026-06-14.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P65 implement and test a source-preserving fixed-branch repair for the P60 d=18 high-rank defensive-only collapse bug? |
| Baseline/comparator | P64 current P60 failing comparator and result artifact, pinned to `sample_count=1`, `fit_sample_count=2`, low `(degree=0, rank=1)`, high `(degree=1, rank=2)`; Phase 0 must restate and probe this full tuple before execution. |
| Primary pass criterion | Final repaired focused comparator has no high defensive-only steps, high fitted square-root mass is nonzero at both steps, focused P59/P60 tests pass, and no source/threshold/target invariants are changed. |
| Veto diagnostics | Defensive-only high branch; changed target/order/axes; artificial fit data; defensive tau removal/rescale outside derivation; threshold weakening; hidden adaptive reselection; nonfinite density/normalizer; unsupported claims. |
| Explanatory diagnostics | Fit sample count, retained sample count, clipping, target value ranges, ESS, correction ranges, normalizer decomposition, log marginal deltas, rank/degree/ridge. |
| Not concluded | No d=18 correctness unless explicitly supported by Phase 3; no d=50/d=100; no adaptive parity; no paper-scale reproduction; no HMC readiness. |
| Artifacts | Master program, phase subplans/results, Claude review ledger, visible execution ledger, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| CPU-only execution | AGENTS GPU/CUDA policy | P65 tests rank/capacity logic, not GPU behavior. | CUDA chatter may be misread. | Set `CUDA_VISIBLE_DEVICES=-1`. | baseline |
| Current P64 result as baseline | P64 result | It localizes the actual bug. | Stale local state. | Phase 0 JSON probe. | to verify |
| Visible current-conversation execution | User request and template | Keeps supervisor/executor role explicit. | Long tests consume time. | Run smallest diagnostics first. | planned |
| Bounded Claude prompts | User request | Avoids oversized approval/prompt failures. | Missing context. | Give exact anchors and questions. | planned |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and in
the execution ledger for material phases.

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
- artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.  This template permits only the foreground bounded reviewer
path; it does not permit autonomous, detached, editing, or execution-authority
Claude roles.

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
