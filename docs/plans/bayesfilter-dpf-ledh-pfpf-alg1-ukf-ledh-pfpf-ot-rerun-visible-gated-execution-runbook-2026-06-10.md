# Visible Gated Execution Runbook: Algorithm 1 UKF Rerun Of LEDH-PFPF-OT Tests

Date: 2026-06-10

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- overnight launch scripts;
- `setsid`, `nohup`, detached `tmux`, or backgrounded phase runners;
- copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-master-program-2026-06-10.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-claude-review-ledger-2026-06-10.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-visible-execution-ledger-2026-06-10.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-visible-stop-handoff-2026-06-10.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P0 | Inventory And Rerun Registry | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p0-inventory-registry-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p0-inventory-registry-result-2026-06-10.md` |
| P1 | Direct LGSSM, Range-Bearing, Gradient Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p1-direct-lgssm-range-bearing-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p1-direct-lgssm-range-bearing-result-2026-06-10.md` |
| P2 | V2 Algorithm 1 Contract Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p2-v2-contracts-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p2-v2-contracts-result-2026-06-10.md` |
| P3 | V2 Algorithm 1 Value Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p3-v2-values-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p3-v2-values-result-2026-06-10.md` |
| P4 | V2 Algorithm 1 Gradient Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p4-v2-gradients-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p4-v2-gradients-result-2026-06-10.md` |
| P5 | Filter-Oracle Statistical Closeness Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p5-filter-oracle-statistical-closeness-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p5-filter-oracle-statistical-closeness-result-2026-06-10.md` |
| P6 | Cross-Filter Calibration Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p6-cross-filter-calibration-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p6-cross-filter-calibration-result-2026-06-10.md` |
| P7 | P44/P8 Blocker Closure Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p7-p44-blocker-closure-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p7-p44-blocker-closure-result-2026-06-10.md` |
| P8 | FilterFlow, Annealed, And Historical Regression Classification | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p8-filterflow-annealed-historical-regression-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p8-filterflow-annealed-historical-regression-result-2026-06-10.md` |
| P9 | Integration Closeout And Supersession Ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p9-closeout-supersession-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p9-closeout-supersession-result-2026-06-10.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the old LEDH-PFPF-OT-related tests be redone visibly with Algorithm 1 UKF, or classified without overclaiming? |
| Baseline/comparator | Old LEDH-PFPF-OT tests define coverage only.  Current comparators are exact or valid approximation routes declared per model. |
| Primary pass criterion | All old LEDH-PFPF-OT lanes receive a reviewed new status and no old row remains usable as Algorithm 1 evidence. |
| Veto diagnostics | Old implementation used as current evidence; missing Algorithm 1 route ids; unsupported model/filter pair ranked; missing MC uncertainty; nonfinite numerics; hidden detached execution. |
| Explanatory diagnostics | Runtime, ESS, value and gradient errors, covariance spectra, determinant ranges, old-vs-new deltas. |
| Not concluded | No production default, HMC readiness, universal superiority, or OT-as-source-Algorithm-1 claim. |
| Artifacts | Phase results, JSON/Markdown reports, visible ledger, Claude review ledger, closeout. |

## Required Row Fields

Every visible phase that emits Algorithm 1 rows must preserve:

- mandatory Algorithm 1 route fields from the master program;
- `evidence_route_class`, separating source core from BayesFilter extension;
- predeclared value and gradient tolerances or `N/A` reasons;
- seed count, particle ladder, and uncertainty columns for stochastic rows;
- per-row run-manifest link.

## Visible State Machine

For each phase:

1. `PRECHECK`: read the subplan, restate the evidence contract, confirm
   prerequisites, and append a ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands in this conversation.
3. `ASSESS_GATE`: compare outputs to primary and veto criteria.
4. `WRITE_RESULT`: write the result artifact and any JSON/Markdown reports.
5. `PASS_REVIEW`: send the result to Claude Opus max effort as read-only
   reviewer and continue only on `VERDICT: AGREE`.
6. `REPAIR_LOOP`: if fixable, repair visibly and repeat review up to five
   iterations.
7. `ADVANCE_OR_STOP`: advance only after gate pass; otherwise write a handoff.

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
- old LEDH-PFPF-OT evidence accidentally revived;
- missing Algorithm 1 UKF covariance lifecycle route identifiers;
- OT resampling treated as source Li-Coates Algorithm 1;
- missing MC uncertainty for stochastic rows;
- missing full run manifest for serious runs.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and verify that Claude stayed
read-only.

## Human-Required Stop Conditions

Stop if continuing would require:

- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing BayesFilter default policy;
- modifying unrelated dirty user work;
- interpreting GPU/CUDA results without trusted-context evidence;
- continuing after five unresolved Claude review iterations.
