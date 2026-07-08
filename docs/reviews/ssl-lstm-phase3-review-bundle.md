# Claude Read-Only Review Bundle

Date: 2026-07-04
Review name: `ssl-lstm-phase3-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review whether Phase 3 material is internally consistent and boundary-safe
enough to advance to Phase 4.

## Artifacts To Inspect

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase3-sgqf-ukf-analytic-adapters-result-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase4-zhaocui-fixed-analytic-adapter-subplan-2026-07-04.md`
- `bayesfilter/nonlinear/ssl_lstm_sgqf_ukf_adapters.py`
- `tests/test_ssl_lstm_sgqf_ukf_adapters.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Phase 3 advance to Phase 4 without a boundary or correctness issue? |
| Baseline/comparator | Phase 2 protocol, Phase 1 SSL-LSTM target, and the existing analytic SGQF/UKF score modules. |
| Primary criterion | Local checks passed, artifacts are schema-valid, and no unsupported claim or hidden authority transfer is present. |
| Veto diagnostics | Missing artifact, hidden autodiff target path, unsupported sufficiency claim, broken phase handoff, or source-anchor confusion. |
| Explanatory diagnostics | Finite-difference residual magnitudes, runtime labels, and debug/reference artifact metadata. |
| Not concluded | SGQF/UKF sufficiency, HMC convergence, production readiness, or method ranking. |

## Review Questions

1. Is there a material correctness or boundary issue?
2. Is the evidence contract internally consistent?
3. Are required artifacts and checks sufficient for the stated phase?
4. Are there unsupported claims or hidden authority transfers?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
