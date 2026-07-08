# SIR Gradient Reparameterization Root-Cause Visible Gated Execution Runbook

Date: 2026-07-01

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

Bounded foreground calls to `bash scripts/claude_worker.sh ...` are allowed
only for read-only Claude review in the current visible conversation.  Such
calls must be run with trusted/escalated permissions by repo policy, must not
launch phase execution, and must be recorded in the Claude review ledger.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-master-program-2026-07-01.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-claude-review-ledger-2026-07-01.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-visible-execution-ledger-2026-07-01.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-visible-stop-handoff-2026-07-01.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Scope and route freeze | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase0-scope-route-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase0-scope-route-result-2026-07-01.md` |
| 1 | Regional kappa expansion | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-result-2026-07-01.md` |
| 2 | Regional orthogonal kappa/nu | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-result-2026-07-01.md` |
| 3 | RK4 sensitivity audit | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-result-2026-07-01.md` |
| 4 | Transport adjoint and stopped-scale-key audit | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-result-2026-07-01.md` |
| 5 | Synthesis and handoff | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase5-synthesis-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase5-synthesis-result-2026-07-01.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which part of the SIR dynamic-parameter score explains the budget-10 manual-score vs FD mismatch? |
| Baseline/comparator | Existing raw, physics, and whitened budget-10 GPU/XLA/TF32 artifacts with fixed seeds `81120..81124`, `T=3`, `N=64`, Sinkhorn budget 10. |
| Primary pass criterion | Each phase produces a result or blocker artifact that preserves the phase evidence contract and narrows the root-cause target without route drift. |
| Veto diagnostics | CPU-only material route, non-XLA material route, TF32 disabled, missing chain-rule checks, unsupported scientific claim, changed seeds/theta/budget without documentation, exit 137 without blocker record. |
| Explanatory diagnostics | Per-region score/FD tables, projected MCSE, component decompositions, regional rho/tau geometry, RK4 sensitivity residuals, non-centered route deltas, runtime/memory traces. |
| Not concluded | HMC readiness, posterior correctness, SIR gradient correctness, production default, global reparameterization. |
| Artifacts | This runbook, phase subplans/results, visible ledger, Claude review ledger, JSON diagnostics. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| GPU/XLA/TF32 material route | `AGENTS.md` owner directive | Matches repo default for LEDH-PFPF-OT | CPU shortcut would be misleading | Escalated GPU run metadata | Required |
| Budget-10 first | Existing completed raw/physics/whitened artifacts | Keeps route comparable and avoids known budget-100 memory blocker | Budget-10 may be too noisy | Projected MCSE and regional localization | Baseline |
| Regional expansion first | Chain rule | Lowest-risk diagnostic for scalar aggregation | May expose score bug but not solve it | Sum regional score to scalar score | Hypothesis |
| Whitening diagnostic is not production | 2026-07-01 whitening result | Score covariance may be wrong if score is wrong | False confidence from bad preconditioner | Treat whitening as explanatory only | Required |

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
