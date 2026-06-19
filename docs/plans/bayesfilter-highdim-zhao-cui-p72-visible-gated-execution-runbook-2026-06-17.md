# P72 Visible Gated Execution Runbook

Date: 2026-06-17

## Status

`READY_FOR_USER_LAUNCH_APPROVAL_CLAUDE_AGREE`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

"Overnight" means the phase ladder may contain long visible commands that
Codex monitors and records.  It does not mean hidden autonomous execution.
If a long command is needed, Codex launches it visibly in this conversation,
polls it, records the command and output artifact, and stops only at real
phase gates or human-required boundaries.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-stop-handoff-2026-06-17.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Mathematical repair-note closeout and governance reset | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase0-repair-note-closeout-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase0-repair-note-closeout-result-2026-06-17.md` |
| 1 | Source and literature boundary audit | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-result-2026-06-17.md` |
| 2 | Guard-cloud, line-probe, and conditioning design contract | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md` |
| 3 | Implementation surface audit and focused test plan | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md` |
| 4 | Focused implementation and unit tests | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-result-2026-06-17.md` |
| 5 | Bounded repaired lower-gate diagnostic | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md` |
| 6 | Result review and downstream validation-planning decision | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase6-downstream-validation-decision-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase6-downstream-validation-decision-result-2026-06-17.md` |
| 7 | Administrative closeout, ledgers, and stop handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase7-administrative-closeout-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase7-administrative-closeout-result-2026-06-17.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the support-certified fixed-fit repair be designed, implemented, and bounded-diagnosed visibly enough to decide whether the P70 Phase 6h lower gate is repaired? |
| Baseline/comparator | P70 Phase 6h failed evidence and P72 mathematical repair note. |
| Primary pass criterion | A phase advances only when its result artifact exists, required local checks pass, material Claude review converges, the next subplan exists, and exact handoff conditions are met. |
| Veto diagnostics | Fit residual promoted to success; missing finite guard/max/line/conditioning gates; source-faithfulness overclaim; thresholds changed after output; downstream validation ladder launched before Phase 6 decision; missing serious-run manifest for the decisive diagnostic; detached execution; GPU sandbox result interpreted without trusted context. |
| Explanatory diagnostics | Fit/guard/audit residuals, max residuals, line probes, singular spectra, condition numbers, effective ranks, normalizers, support distances, clipping, branch hashes, run manifests. |
| Not concluded | No original Zhao--Cui failure claim, no adaptive parity, no d18 accuracy, no scaling, no HMC readiness, no source-faithfulness closure for guard additions. |
| Artifacts | Master program, runbook, execution ledger, stop handoff, phase subplans/results, review ledger, PDF note, diagnostic JSONs, implementation diffs if launched. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Finite diagnostic certificate | P72 repair note and Claude R2 review | The observed failure is finite holdout/replay/line explosion; continuum claims would overreach. | Guard set passes but real support still fails. | Phase 2 support-distance and audit-cloud design. | reviewed note |
| Guard additions are not source-faithful by default | AGENTS.md Zhao-Cui gate and P72 note | Prevents fixed-variant repair from being misrepresented as author algorithm. | Source-faithfulness overclaim. | Phase 1 classification ledger. | planned |
| Fit residual is not a pass criterion | Phase 6h failure and P72 note | Fit residual already passed while off-cloud behavior failed. | Same bug returns under new name. | Phase 2/5 gate requires max residual and line probes. | planned |
| Column scaling/effective-rank convention is predeclared | Phase 6h row-B condition failure | Conditioning results depend on scaling and rank convention. | Threshold gaming. | Phase 2 contract freezes convention before implementation. | planned |
| Visible execution only | User instruction and template | Keeps phase state inspectable. | Hidden blocker or silent detached state. | Runbook forbids detached execution. | planned |

## Anticipated Approvals And Boundaries

Before launch, request or confirm approval for:

- Claude Code read-only reviews through
  `/home/chakwong/python/claudecodex/scripts/claude_worker.sh` with Opus max
  effort;
- local documentation writes under `docs/plans`;
- visible source-code edits on implementation surfaces explicitly authorized
  by reviewed Phase 3 and Phase 4 subplans only; unrelated dirty user work must
  be preserved;
- local read-only shell checks (`sed`, `rg`, `git status`, `git diff`,
  `latexmk` log inspection);
- CPU-only Python/pytest checks for focused implementation phases, with
  `CUDA_VISIBLE_DEVICES=-1` recorded when used;
- trusted/escalated GPU commands only if a later reviewed phase explicitly
  requires GPU evidence;
- any command that writes outside the repository, needs network access, or
  performs package installation must stop for explicit approval.

Not approved by this runbook:

- destructive git or filesystem actions;
- package installation or dependency downloads;
- changing thresholds after seeing outputs;
- detached/background execution;
- any downstream validation ladder or d18 validation during this P72 program.

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and,
for material phases, in the execution ledger.

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
before running the phase.  Execution begins only after the phase survives this
audit.

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
4. `DRAFT_NEXT`
   - Draft or refresh the next phase subplan.
   - Ensure the current result explicitly produces next-phase entry
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
- source-governance overclaim.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

If Claude does not respond, run a tiny probe.  If the probe responds, redesign
the prompt.  Do not treat a prompt stall as Claude unavailability.

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
