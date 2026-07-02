# SIR Gradient Reparameterization Root-Cause Visible Stop Handoff

Date: 2026-07-01

Status: `COMPLETED`

## Current State

Master program and visible runbook are drafted and reviewed.  Phase 0 passed.
Phase 1 regional kappa expansion passed after a seed-microbatch route repair.
Claude review iteration 2 agreed. Phase 2 regional kappa/nu rho/tau diagnostic
passed. Phase 3 RK4 sensitivity audit passed after focused Claude review of
the Phase 3 subplan patch. Phase 4 transport-adjoint / stopped-scale-key audit
passed after Claude review of the refreshed Phase 4 subplan. Phase 5 synthesis
passed final Claude review.

## Final Phase Reached

Phase 5

## Result Artifacts

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase0-scope-route-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-budget10-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-budget10-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase5-synthesis-result-2026-07-01.md`

## Claude Review Trail

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-claude-review-ledger-2026-07-01.md`

## Tests Or Benchmarks Actually Run

- `rg` heading/path checks for root-cause plan artifacts.
- `rg` code-anchor inventory for SIR gradient code.
- `python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
- `python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_regional_kappa_gradient_decomposition.py`
- `bash -n scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh`
- `pytest -q tests/test_p8p_regional_kappa_gradient_decomposition.py`
- `pytest -q tests/test_ledh_pfpf_ot_p7_manual_score.py`
- `bash scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh`
- `python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_regional_orthogonal_gradient_decomposition.py`
- `bash -n scripts/run_sir_gradient_reparam_rootcause_phase2_regional_orthogonal_budget10.sh`
- `pytest -q tests/test_p8p_regional_orthogonal_gradient_decomposition.py`
- `pytest -q tests/test_p8p_regional_kappa_gradient_decomposition.py`
- `bash scripts/run_sir_gradient_reparam_rootcause_phase2_regional_orthogonal_budget10.sh`
- `python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/diagnose_p8p_sir_rk4_sensitivity_vjp.py`
- `pytest -q tests/test_p8p_sir_rk4_sensitivity_vjp.py`
- `python docs/benchmarks/diagnose_p8p_sir_rk4_sensitivity_vjp.py --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-2026-07-01.json`
- `python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/diagnose_p8p_sir_transport_adjoint_vjp.py`
- `pytest -q tests/test_p8p_sir_transport_adjoint_vjp.py`
- `python docs/benchmarks/diagnose_p8p_sir_transport_adjoint_vjp.py --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-2026-07-01.json`

## Unresolved Blockers

None. The current program is complete.

## Nonclaims

- No SIR gradient correctness claim.
- No HMC readiness claim.
- No posterior correctness claim.
- No production default change.
- No global reparameterization proof.

## Safest Next Human Decision

Safest next action is a new governed tiny full-route score-assembly parity
plan before any new material GPU/TF32 SIR ladder.
