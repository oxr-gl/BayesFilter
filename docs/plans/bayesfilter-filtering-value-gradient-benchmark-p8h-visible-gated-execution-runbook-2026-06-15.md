# P8h Visible Gated Execution Runbook

Date: 2026-06-15

## Status

`CLOSED_PHASE10_BOUNDARY_REVIEWED`

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

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-ot-resampled-alg1-ledh-master-program-2026-06-15.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-claude-review-ledger-2026-06-15.md`

Execution ledger:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-visible-execution-ledger-2026-06-15.md`

Stop handoff:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-visible-stop-handoff-2026-06-15.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| 0 | LaTeX documentation and governance correction | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase0-latex-governance-correction-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase0-latex-governance-correction-result-2026-06-15.md` |
| 1 | Governance reset | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase1-governance-reset-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase1-governance-reset-result-2026-06-15.md` |
| 2 | Algorithm and evidence contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase2-algorithm-design-contract-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase2-algorithm-design-contract-result-2026-06-15.md` |
| 3 | Scalar-SV GPU OT implementation | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase3-scalar-sv-gpu-ot-implementation-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase3-scalar-sv-gpu-ot-implementation-result-2026-06-15.md` |
| 4 | Local checks and integration diagnostics | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-local-checks-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-local-checks-result-2026-06-15.md` |
| 5 | Value/filtering tuning | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-result-2026-06-15.md` |
| 6 | OT gradient checks | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-result-2026-06-16.md` |
| 7 | GPU performance and scaling | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-result-2026-06-16.md` |
| 8 | Tier-0 HMC execution smoke | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-diagnostic-tiers-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-result-2026-06-16.md` |
| 9 | Closeout and artifact refresh | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase9-closeout-artifact-refresh-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase9-closeout-artifact-refresh-result-2026-06-16.md` |
| 10 | Repo hygiene and commit-boundary review | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase10-repo-hygiene-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase10-repo-hygiene-result-2026-06-16.md` |
| 11 | Closure status sync | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase11-closure-sync-subplan-2026-06-16.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase11-closure-sync-result-2026-06-16.md` |

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the P8h repair execute visibly and replace no-resampling P8g as the serious GPU/gradient LEDH route? |
| Baseline/comparator | P8g no-resampling scalar-SV artifacts, historical LEDH-PFPF-OT/Sinkhorn artifacts, and current Algorithm 1 UKF covariance lifecycle implementation. |
| Primary pass criterion | Each phase passes its gate and writes a result, or stops with a blocker result and handoff. |
| Veto diagnostics | Detached launch; untrusted GPU execution; Claude used as executor; missing result artifacts; no-resampling route promoted as serious filter; HMC overclaim. |
| Explanatory diagnostics | Ledger entries, local checks, Claude reviews, LaTeX build, OT residuals, value tuning, gradient diagnostics, GPU profiles, HMC smoke diagnostics. |
| Not concluded | Production readiness, stochastic PF marginal-gradient correctness, categorical-resampling gradient correctness, exact nonlinear likelihood correctness, generic high-dimensional LEDH readiness, or final filter ranking. |
| Artifacts | Master program, phase subplans/results, Claude review ledger, execution ledger, stop handoff, refreshed matrices/results, and final P8h commit-boundary manifest. |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and in
the execution ledger for material phases. Check wrong baselines, proxy metrics
as promotion criteria, missing stop conditions, unfair comparisons, hidden
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
safety, unsupported claims, missing stop conditions, and stale P8g assumptions.
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
the P8h file set cannot be separated from unrelated Zhao-Cui, monograph, or
user worktree changes.
