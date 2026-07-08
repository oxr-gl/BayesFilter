# SIR Gradient HMC-Direction Visible Gated Overnight Execution Runbook

Date: 2026-06-30

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_PENDING_LOCAL_CHECK_AND_CLAUDE_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook is "overnight" only in the sense of a resumable visible program.
It must not launch a detached or nested agent.  Do not use:

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

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-master-program-2026-06-30.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-claude-review-ledger-2026-06-30.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-execution-ledger-2026-06-30.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-stop-handoff-2026-06-30.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | SIR route inventory and governance freeze | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase0-route-inventory-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase0-route-inventory-result-2026-06-30.md` |
| 1 | SIR gradient evidence contract | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-result-2026-06-30.md` |
| 2 | Diagnostic reporting and test hooks | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase2-diagnostic-reporting-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase2-diagnostic-reporting-result-2026-06-30.md` |
| 3 | GPU/XLA/TF32 route smoke | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-result-2026-06-30.md` |
| 4 | Material SIR gradient diagnostic | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-result-2026-06-30.md` |
| 5 | Repair loop and discriminating ladders | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-result-2026-06-30.md` |
| 6 | Closeout and next handoff | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase6-closeout-subplan-2026-06-30.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase6-closeout-result-2026-06-30.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the P8p SIR d18 LEDH-PFPF-OT manual reverse score be route-validated and classified by an HMC-direction diagnostic, and what is the smallest supported explanation if it fails? |
| Baseline/comparator | Same fixed-randomness objective with 13-point local regression FD.  LGSSM exact-Kalman logic is not reused as an exact SIR oracle. |
| Primary pass criterion | All executed phases satisfy their subplan gates, or stop with a reviewed blocker/root-cause classification and next discriminating action. |
| Veto diagnostics | Material CPU route, untrusted GPU evidence, XLA disabled, TF32 disabled, dense/full transport autodiff, nonfinite values/scores, missing FD SE or MCSE, row residual violation when used for evidence, unsupported scientific claim. |
| Explanatory diagnostics | Runtime, memory, row residuals, FD R2 and plateau, per-seed MCSE/covariance, score decomposition, N ladder, budget ladder, no-resampling isolation. |
| Not concluded | Exact SIR gradient correctness, HMC/NUTS readiness, posterior validity, production default change, or global nonlinear model validation. |
| Artifacts | Master program, subplans/results, ledger, review ledger, stop handoff, JSON/Markdown diagnostics. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| GPU/XLA/TF32 for material LEDH evidence | `AGENTS.md` and owner directive | This is the repo default production route for LEDH-PFPF-OT. | Sandbox hides GPU or CPU result is mistaken for production evidence. | Escalated GPU probe and tensor-device validation before material claims. | frozen |
| Manual reverse score route | Existing P8p scripts and manual-score tests | Avoids dense/full autodiff transport path. | Raw autodiff or full transport sneaks in. | Route metadata, compiler metadata, audit sentinel tests. | frozen |
| Regression FD comparator | Existing P8p FD diagnostic | SIR lacks an exact gradient oracle; same fixed-randomness FD is the local comparator. | FD SE treated as exact truth. | Phase 1 gate explicitly distinguishes comparator from proof. | planned |
| Seed-gradient MCSE | Existing P8p MC noise summary | Calibrates estimator variability for HMC-direction usefulness. | MCSE used to hide a fixed-randomness derivative defect. | Report separately from FD slope SE and relative error. | planned |
| Row residual veto | Existing Sinkhorn budget diagnostic | Transport under-convergence can mimic gradient failure. | Residual threshold tuned after results. | Threshold declared in phase command and result. | planned |
| Visible runbook | Template `/home/chakwong/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md` | Keeps execution recoverable and auditable in this conversation. | User expects detached execution. | This runbook states no detached launch is authorized. | frozen |

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

At the end of each phase, Codex must:

1. run the required local checks;
2. write a phase result or close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

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

Review exact paths only:
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
remained read-only.  If Claude does not respond, Codex first runs a small
read-only probe.  If the probe responds, the prompt is presumed problematic and
must be redesigned before retrying the review.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- detached overnight execution;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Launch Protocol

After this runbook and the master program pass local checks and bounded Claude
review, Codex launches Phase 0 visibly in this conversation.  "Launch" means:

1. append the first execution-ledger entry;
2. perform Phase 0 prechecks and local route inventory;
3. write the Phase 0 result or blocker;
4. refresh/review the Phase 1 subplan before advancing.

No detached overnight supervisor is authorized by this visible runbook.

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
