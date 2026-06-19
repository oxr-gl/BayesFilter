# P76 Visible Gated Execution Runbook

Date: 2026-06-18

## Status

`PHASE10_CLAUDE_AGREE_CLOSED_READY_FOR_PHASE11_SUBPLAN`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

Claude review is performed through the foreground wrapper
`/home/chakwong/python/claudecodex/scripts/claude_worker.sh` when a material
phase requires it.  That wrapper is a bounded read-only review mechanism, not
an executor, supervisor, detached phase runner, or authority to advance gates.

This runbook must not launch a detached or nested execution agent.  Do not
use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

"Overnight" means the phase ladder may contain long visible commands that
Codex monitors and records.  It does not mean hidden autonomous execution.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md`

P75 closeout erratum:

- `docs/plans/bayesfilter-highdim-zhao-cui-p75-closeout-erratum-ukf-hypothesis-untested-2026-06-18.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Closeout and boundary reset | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase0-closeout-boundary-reset-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase0-closeout-boundary-reset-result-2026-06-18.md` |
| 1 | Mathematical UKF initializer contract | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase1-mathematical-ukf-initializer-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase1-mathematical-ukf-initializer-result-2026-06-18.md` |
| 2 | Implementation surface and test plan | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase2-implementation-surface-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase2-implementation-surface-result-2026-06-18.md` |
| 3 | Opt-in UKF initializer implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-result-2026-06-18.md` |
| 4 | Tiny UKF-initializer smoke | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-result-2026-06-18.md` |
| 5 | Mini-batch training pilot decision | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-result-2026-06-18.md` |
| 6 | Bounded UKF-frame mini-batch pilot | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-result-2026-06-18.md` |
| 6b | Corrected evidence contract | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-result-2026-06-18.md` |
| 7 | Fit-diagnostic protocol v2 | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-result-v2-2026-06-18.md` |
| 8 | Corrected heldout metric surface | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-subplan-2026-06-18.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-result-2026-06-18.md` |
| 9 | Corrected heldout metric smoke | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-subplan-2026-06-19.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-result-2026-06-19.md` |
| 10 | Generated corrected-metric diagnostic | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-subplan-2026-06-19.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-result-2026-06-19.md` |

## Phase 6b Corrective Interlock

Phase 6 is now mechanics-only evidence.  The original Phase 7 subplan is
superseded and must not be executed:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md`

The executable successor is Phase 7 v2:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md`

Future fit-quality interpretation must use target-only heldout density
cross-entropy as primary, with train/validation/audit separation and
predeclared tuning.  Raw or sign/scale-adjusted square-root residuals are
secondary diagnostics only.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a true UKF-informed initializer provide usable geometry for subsequent mini-batch density training in the fixed variant? |
| Baseline/comparator | Historical P75 failures: random, calibrated constant, and source-route prefit. |
| Primary pass criterion | Each phase produces required artifacts, preserves UKF-as-scout boundaries, forbids failed-method ladders as live repairs, and hands off to the next reviewed subplan. |
| Veto diagnostics | Source-route prefit substituted for UKF initialization; UKF promoted to truth/validation/HMC readiness; audit leakage; large-pilot launch; proxy metric promoted to lower-gate repair. |
| Explanatory diagnostics | UKF moment finiteness, covariance conditioning, initializer residuals, mini-batch losses, gradients, audit residuals, line residuals, runtime. |
| Not concluded | No lower-gate repair, validation readiness, HMC readiness, scaling, source-faithfulness, final rank/sample policy, or large-pilot authorization. |
| Artifacts | P75 erratum, P76 master program, runbook, execution ledger, review ledger, phase subplans/results, JSON diagnostics. |

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
- accidental re-entry into the failed P75 source-prefit route.

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
