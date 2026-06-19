# P8i Visible Gated Execution Runbook

Date: 2026-06-16

## Status

`PLANNING_REVIEWED_READY_FOR_PHASE0`

## Role Contract

Codex in the current conversation is supervisor and executor.

Claude is a read-only reviewer only. Claude must not edit files, run
experiments, launch agents, authorize GPU execution, or change state.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- overnight launcher scripts;
- `setsid`, `nohup`, detached `tmux`, or background supervisors;
- copied-workspace execution.

This is visible, recoverable execution inside the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-remaining-gap-master-program-2026-06-16.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-claude-review-ledger-2026-06-16.md`

Execution ledger:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-visible-execution-ledger-2026-06-16.md`

Stop handoff:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-visible-stop-handoff-2026-06-16.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| 0 | Governance and gap ledger | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase0-governance-gap-ledger-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase0-governance-gap-ledger-result-2026-06-16.md` |
| 1 | Longer-prefix particle and value ladder | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-result-2026-06-16.md` |
| 2 | Longer-horizon OT gradient ladder | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-result-2026-06-16.md` |
| 3 | GPU scaling profile | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-result-2026-06-16.md` |
| 4 | HMC Tier-1 and Tier-2 diagnostics | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-tier2-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-tier2-result-2026-06-16.md` |
| 5 | NUTS readiness decision | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase5-nuts-readiness-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase5-nuts-readiness-result-2026-06-16.md` |
| 6 | Stochastic-gradient and likelihood boundary | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase6-gradient-likelihood-boundary-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase6-gradient-likelihood-boundary-result-2026-06-16.md` |
| 7 | Scope, ranking, and default-policy decision | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase7-ranking-policy-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase7-ranking-policy-result-2026-06-16.md` |
| 8 | Closeout, artifact index, and repo boundary | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase8-closeout-boundary-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase8-closeout-boundary-result-2026-06-16.md` |

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the P8h route be advanced from short-prefix/Tier-0 feasibility toward longer-horizon filtering and sampler diagnostics without overclaiming scientific or production readiness? |
| Baseline/comparator | Closed P8h Phase 10/11 boundary plus P8h Phase 5-8 reviewed artifacts. |
| Primary pass criterion | Each phase passes its gate and writes a result, or stops with a blocker result and handoff. |
| Veto diagnostics | Using Stage 0 as full-horizon adequacy; unsupported stochastic-gradient, exact-likelihood, NUTS, production-HMC, ranking, or default-policy claims; untrusted GPU execution; Claude used as executor. |
| Explanatory diagnostics | Ledger entries, local checks, Claude reviews, value ladders, gradient checks, GPU profiles, HMC/NUTS diagnostics, boundary audits. |
| Not concluded | Any remaining P8h nonclaim unless the corresponding P8i phase explicitly passes. |

## Skeptical Plan Audit

Before executing any material phase, Codex must record a skeptical audit in
chat and in the execution ledger. Check wrong baselines, proxy metrics as
promotion criteria, missing stop conditions, unfair comparisons, hidden
assumptions, stale context, environment mismatch, and commands whose artifacts
would not answer the phase question.

## Visible State Machine

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run visible commands only, starting with the smallest
   diagnostic.
3. `ASSESS_GATE`: compare against primary and veto diagnostics, write result.
4. `PASS_REVIEW`: use Claude read-only review for material phase results or
   next subplans.
5. `REPAIR_LOOP`: patch fixable issues visibly, rerun focused checks, stop
   after five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the current gate passes.

## Claude Read-Only Review Template

```text
READ-ONLY REVIEW ONLY.
Do not edit files, run experiments, launch agents, or change state.
Read these local repo files only as needed:
- <paths>
Review for consistency, correctness, feasibility, artifact coverage, boundary
safety, unsupported claims, missing stop conditions, stale P8h/P8g assumptions,
and scientific-claim promotion risk.
Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch,
credentials, destructive filesystem/git action, changing pass/fail criteria
after seeing results, changing default policy beyond this reviewed plan,
modifying unrelated dirty user work, untrusted GPU execution, or continuing
after five non-convergent Claude review rounds. Stop before commit or push if
the P8i file set cannot be separated from unrelated Zhao-Cui, monograph, P8h,
or user worktree changes.
