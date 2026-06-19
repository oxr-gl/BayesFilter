# P77 Visible Gated Execution Runbook

Date: 2026-06-19

## Status

`PHASE6_LOCAL_CHECKS_PASS_PENDING_CLAUDE_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

Claude review is performed through the foreground wrapper
`/home/chakwong/python/claudecodex/scripts/claude_worker.sh` when a material
phase requires it.  That wrapper is a bounded read-only review mechanism, not
an executor, supervisor, detached phase runner, or authority to advance gates.

This runbook must not launch a detached or nested execution agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

"Overnight" means the phase ladder may contain long visible commands that
Codex monitors and records.  It does not mean hidden autonomous execution.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md`

Predecessor closeout:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-result-2026-06-19.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | P76 closeout and P77 boundary reset | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase0-boundary-reset-subplan-2026-06-19.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase0-boundary-reset-result-2026-06-19.md` |
| 1 | Objective, split, and leakage contract | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-subplan-2026-06-19.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md` |
| 2 | Parameter-count, budget, and tuning protocol | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md` |
| 3 | Implementation surface for budgeted training | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-result-2026-06-19.md` |
| 4 | Tiny training mechanics smoke | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-subplan-2026-06-19.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-result-2026-06-19.md` |
| 5 | Proper budgeted training diagnostic design | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-subplan-2026-06-19.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md` |
| 6 | Budgeted corrected-metric training diagnostic | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-subplan-2026-06-19.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-result-2026-06-19.md` |
| 7 | Decision and next-scale boundary | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase7-decision-boundary-subplan-2026-06-19.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase7-decision-boundary-result-2026-06-19.md` |

Only Phase 0 may execute after the initial plan review converges.  Later
subplans must be drafted or refreshed at the previous phase close before any
execution.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does UKF-warm-started mini-batch training improve corrected target-only heldout density CE under enough fresh training samples and clean train/eval separation? |
| Baseline/comparator | UKF-initialized untrained TT candidate on the same corrected metric and same validation/replay/audit roles. |
| Primary pass criterion | A proper training run may pass only if \(N_{\rm train}\ge20P_\theta\), train/validation/replay/audit roles are disjoint, corrected validation CE improves against the UKF-initialized untrained baseline under a predeclared rule, and veto diagnostics pass. |
| Veto diagnostics | Under-budget evidence run, audit leakage, source-prefit revival, proxy metric promoted to fit quality, nonfinite numerical quantities, bridge/tieout failure, seed overlap, unapproved GPU/network/package/default/large-run action. |
| Explanatory diagnostics | Training loss, gradient norm, raw square-root residuals, centered log-shape RMS, alpha ESS, rho range, normalizer, runtime, and mechanics-smoke values. |
| Not concluded | No source-faithful Zhao--Cui claim, no lower-gate repair, no validation/HMC readiness, no production/default policy, no final rank/sample policy, and no scaling claim. |
| Artifacts | P77 master program, runbook, execution ledger, review ledger, stop handoff, phase subplans/results, JSON diagnostics. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| New P77 lane | P76 Phase 10 closeout | P76 repaired metric plumbing but did not govern a proper training evidence run. | Treating P76 as training evidence. | Phase 0 boundary reset. | draft |
| Corrected heldout CE primary | P76 Phases 8-10 | Avoids contaminated \(\tau q_0\) helper alpha and residual proxy overclaim. | Training loss or residuals become promotion criteria. | Phase 1 contract. | active |
| \(N_{\rm train}\ge20P_\theta\) | User direction | Enforces enough fresh data for fixed-branch regression evidence. | Tiny smoke promoted as evidence. | Phase 2 budget manifest. | active |
| UKF initializer comparator | P76 initializer and Phase 10 metric diagnostic | Training must improve the actual starting candidate. | Comparing only to weak historical baselines. | Phase 1 comparator check. | active |
| Audit final-only | Scientific coding policy | Prevents hidden tuning. | Hyperparameters selected on audit. | Phase 1 split manifest. | active |

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
- commands whose artifacts would not answer the phase question;
- accidental training-evidence claims from under-budget mechanics smokes.

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

## Scoped Code-Edit Governance

Scoped implementation-code edits do not require separate human approval when
all of the following hold:

- the edits are explicitly named in a reviewed phase subplan;
- the edits are limited to the files and behavioral surface named there;
- Claude has reviewed the subplan and remains read-only;
- Codex executes visibly in this session;
- focused local checks are run and recorded;
- no training-evidence run, GPU/CUDA use, network/package operation, default
  change, destructive filesystem/git action, detached agent, or large
  diagnostic is involved.

This applies to every P77 phase, not only Phase 3.  If a later
Claude-reviewed subplan explicitly names implementation-code edits and those
edits remain inside the named files, named behavior, reviewed checks, and
forbidden-action boundary, Codex may perform the edits visibly without asking
for another human approval.  Claude remains a reviewer, not an executor or
authority to cross the stop conditions below.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- running any training-evidence command, including `1024 x 40`, without
  separate reviewed subplan and explicit approval;
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
