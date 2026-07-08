# Claude Read-Only Review Bundle

Date: 2026-07-06
Review name: `minimal-ssl-lstm-zhaocui-phase0-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review the Phase 0/Phase 1 planning boundary for the minimal scalar SSL-LSTM
`zhaocui_fixed` smoke program.

## Artifacts To Inspect

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-master-program-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase0-governance-fixture-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase1-harness-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-visible-gated-execution-runbook-2026-07-06.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-reset-memo-2026-07-05.md`
- `tests/test_ssl_lstm_zhaocui_fixed_adapter.py`
- `bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the minimal scalar SSL-LSTM smoke program correctly scoped and safe to execute after approval? |
| Baseline/comparator | Existing minimal `zhaocui_fixed` adapter test fixture and July 5 reset memo. |
| Primary criterion | Plans preserve scalar fixture, artifact requirements, checks, and evidence boundaries. |
| Veto diagnostics | Wrong fixture dimensions, hidden target autodiff, unapproved Claude/GPU/long launch, LEDH leakage, unsupported HMC/posterior/ranking/source-faithful claim, or missing stop condition. |
| Explanatory diagnostics | Numeric-default provenance, planned artifact paths, and review/repair loop clarity. |
| Numeric provenance | Dimensions are user-requested; horizon/observations/FD subset are inherited from existing minimal tests and are smoke conveniences. |
| Not concluded | No mechanics pass, posterior correctness, HMC convergence, ranking, method superiority, source-faithful parity, GPU/XLA readiness, default readiness, or LEDH result. |

## Review Questions

1. Is there a material correctness or boundary issue in the master program,
   Phase 0 subplan, Phase 1 subplan, or runbook?
2. Is the evidence contract internally consistent?
3. Are required artifacts and checks sufficient for the stated planning and
   harness phases?
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
