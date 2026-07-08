# Claude Read-Only Review Bundle

Date: 2026-07-06
Review name: `minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review the Phase 0/Phase 1 planning boundary for the minimal scalar SSL-LSTM
`zhaocui_fixed` HMC ladder.

## Artifacts To Inspect

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-master-program-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-governance-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-governance-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase1-target-adapter-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-visible-gated-overnight-execution-plan-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-reset-memo-2026-07-06.md`
- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py`
- `docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase7.py`
- `bayesfilter/inference/hmc.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the minimal scalar `zhaocui_fixed` HMC ladder correctly scoped and safe to execute after approval? |
| Baseline/comparator | Completed minimal smoke artifact and existing Phase 7 SSL-LSTM HMC launch-smoke pattern. |
| Primary criterion | Plans preserve scalar fixture, HMC hard-veto evidence class, artifact requirements, checks, approvals, and evidence boundaries. |
| Veto diagnostics | Wrong fixture dimensions, hidden target autodiff/NumPy, unapproved HMC/GPU/long/detached launch, LEDH leakage, unsupported HMC convergence/posterior/ranking/source-faithful/default claim, missing stop condition, or hidden authority transfer. |
| Explanatory diagnostics | Numeric-default provenance, planned artifact paths, review/repair loop clarity, and approval boundaries. |
| Numeric provenance | Dimensions and observations are inherited from completed minimal smoke; HMC canary settings are inherited from existing Phase 7 launch smoke and are debug conveniences/hypotheses. |
| Not concluded | No target adapter pass, HMC canary pass, posterior correctness, HMC convergence, ranking, method superiority, source-faithful parity, GPU/XLA readiness, default readiness, or LEDH result. |

## Review Questions

1. Is there a material correctness or boundary issue in the master program,
   Phase 0 subplan, Phase 1 subplan, or runbook?
2. Is the evidence contract internally consistent?
3. Are required artifacts and checks sufficient for the stated planning and
   target-adapter phases?
4. Are there unsupported claims or hidden authority transfers?
5. Are there unsupported numeric defaults that were invented, inherited, or
   overcommitted without provenance?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
