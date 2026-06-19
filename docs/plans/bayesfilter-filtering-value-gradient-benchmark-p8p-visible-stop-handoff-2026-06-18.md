# P8p Visible Stop Handoff

Date: 2026-06-18

Status: `STOPPED_BLOCKED_AT_PHASE3_AD_FD_RESIDUAL`

## Current State

P8p has been launched as the DPF/SIR d18 parameterized gradient and
HMC-mechanics readiness lane.  Phases 0, 1, and 2 passed.  Phase 3 blocked on
AD/FD residuals exceeding the predeclared tolerance.

## Final Phase Reached

Phase 3 blocked.  Do not proceed to Phase 4 full-horizon gradient probing until
a focused Phase 3 repair plan is reviewed and passes.

## Result Artifacts

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase0-governance-target-boundary-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-2026-06-18.json`

## Claude Review Trail

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-claude-review-ledger-2026-06-18.md`

## Tests Or Benchmarks Actually Run

- `python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`
- `python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- `git diff --check` over P8p plan artifacts
- `rg` checks for P8o status, streaming hooks, zero-filled connectivity caveat,
  and revised P8p boundary language
- CPU-only P8p Phase 2 implementation smoke
- Trusted GPU P8p Phase 2 gradient smoke
- Programmatic Phase 2 JSON gate validation
- Trusted GPU P8p Phase 3 finite-difference validation
- Programmatic Phase 3 AD/FD residual gate check

## Unresolved Blockers

Active blocker:

- Phase 3 AD/FD residuals exceeded predeclared tolerance for
  `log_kappa_scale` and `log_obs_noise_scale`.

## What Is Not Concluded

No P8p artifact currently establishes stochastic PF marginal-gradient
correctness, exact nonlinear likelihood correctness, posterior convergence,
NUTS readiness, tuned HMC readiness, production/default readiness, Zhao-Cui
TT/SIRT parity, MATLAB parity, filter ranking, or cross-model default policy.
