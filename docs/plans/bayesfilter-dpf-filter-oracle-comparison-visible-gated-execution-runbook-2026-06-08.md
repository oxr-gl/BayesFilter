# Visible Gated Execution Runbook: DPF Filter Oracle Comparison

Date: 2026-06-08

## Status

`PASS_P7_FILTER_COMPARISON_CLOSEOUT`

## Role Contract

Codex in this dialogue is the supervisor and executor.

Claude is a read-only critical reviewer only.  Claude must not edit files, run
experiments, launch agents, or change state.

This visible runbook must not launch a detached or nested supervisor.  Do not
use `codex exec`, `overnight_gated_launch.sh`, `setsid`, `nohup`, detached
`tmux`, backgrounded phase runners, or copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-master-program-2026-06-08.md`

Plan review ledger:

- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-claude-review-ledger-2026-06-08.md`

Visible execution ledger:

- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-stop-handoff-2026-06-08.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P0 | Target-route registry | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p0-target-route-registry-subplan-2026-06-08.md` | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p0-target-route-registry-result-2026-06-08.md` |
| P1 | LGSSM exact oracle | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p1-lgssm-exact-oracle-subplan-2026-06-08.md` | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p1-lgssm-exact-oracle-result-2026-06-08.md` |
| P2 | Tiny nonlinear dense oracle | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-subplan-2026-06-08.md` | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-result-2026-06-08.md` |
| P3 | Conditional Gaussian mixture | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-subplan-2026-06-08.md` | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-result-2026-06-08.md` |
| P4 | Zhao-Cui route classification | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-subplan-2026-06-08.md` | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-result-2026-06-08.md` |
| P5 | DPF statistical closeness | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-subplan-2026-06-08.md` | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-result-2026-06-08.md` |
| P6 | Cross-filter calibration | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-subplan-2026-06-08.md` | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-result-2026-06-08.md` |
| P7 | Integration closeout | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-integration-closeout-subplan-2026-06-08.md` | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-integration-closeout-result-2026-06-08.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can DPF value and gradient evidence be fairly compared against exact, approximation, diagnostic, and blocked filter routes without promoting non-oracles? |
| Baseline/comparator | P0 registry first; later phases may use only P0-P4 approved references. |
| Primary pass criterion | Each phase writes reviewed result or blocker artifacts with claim class separation. |
| Veto diagnostics | Wrong target, missing tolerance, missing gradient statistic, missing manifest, unreviewed runner, unsupported oracle claim, or Claude/Codex disagreement after five rounds. |
| Explanatory diagnostics | Runtime, route availability, point count, ESS, residuals, and local smoothness checks. |
| Not concluded | No numerical comparison, DPF correctness, HMC readiness, production readiness, GPU readiness, or paper-scale claim from P0. |
| Artifacts | Phase JSON/result/review ledgers plus this visible execution ledger. |

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, restate evidence contract, audit baselines and stop
   conditions.
2. `EXECUTE_MINIMAL`: run only commands visible in this dialogue.
3. `ASSESS_GATE`: compare artifacts against phase criteria and vetoes.
4. `PASS_REVIEW`: run Claude read-only review up to five iterations.
5. `ADVANCE_OR_STOP`: advance only after a reviewed pass; otherwise write a
   blocker or stop handoff.

## Current Phase

Closed.

Latest completed phase: P7 integration closeout exited
`PASS_P7_FILTER_COMPARISON_CLOSEOUT` after Claude read-only review iteration 3.
No required phase work remains in this visible gated run.

Closeout scope: no DPF correctness, stochastic-score correctness, universal DPF
superiority, global ranking, HMC readiness, production readiness, GPU readiness,
public API readiness, paper-scale claim, or default-policy change is claimed.
