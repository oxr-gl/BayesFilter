# Phase 1 Subplan: Regional Kappa Expansion

Date: 2026-07-01

Status: `DRAFT_PENDING_PHASE0`

## Phase Objective

Introduce a diagnostic-only regional `log_kappa_region[j]` expansion and test
the exact chain-rule identity that the scalar global kappa score equals the sum
of regional kappa scores on the diagonal submanifold.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed and froze baseline route/artifacts.
- Current scalar parameters are confirmed as
  `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`.
- Phase 1 implementation targets are limited to diagnostic harness code and
  tests, not production defaults.

## Required Artifacts

- Diagnostic harness:
  `docs/benchmarks/benchmark_p8p_regional_kappa_gradient_decomposition.py`
- Unit/smoke tests:
  `tests/test_p8p_regional_kappa_gradient_decomposition.py`
- Material wrapper:
  `scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh`
- Material JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-budget10-2026-07-01.json`
- Phase 1 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-result-2026-07-01.md`

## Required Checks, Tests, Reviews

- Local compile/syntax checks for touched Python files.
- Focused unit test that regional score sum reconstructs scalar score on a tiny
  fixed-seed diagnostic.
- Material GPU/XLA/TF32 budget-10 run only after local checks pass.
- Claude read-only review for material implementation diff or result if a
  scientific decision is made.

Exact local command templates:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_regional_kappa_gradient_decomposition.py
pytest -q tests/test_ledh_pfpf_ot_p7_manual_score.py tests/test_p8p_regional_kappa_gradient_decomposition.py
bash -n scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh
```

Exact material command:

```bash
bash scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh
```

The material wrapper must use visible GPU/XLA/TF32, fixed seeds
`81120,81121,81122,81123,81124`, `T=3`, `N=64`, Sinkhorn iterations 10, and
seed microbatch size `1`, matching the entry budget-10 diagnostics unless a
phase result explicitly records a narrower smoke-only debug command.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does decomposing global `log_kappa_scale` into per-region log-kappa scores localize the mismatch or reveal an aggregation bug? |
| Baseline/comparator | Scalar `log_kappa_scale` manual score and FD slope from `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.md` and JSON `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.json`. |
| Primary pass criterion | On the diagonal, `sum_j score(log_kappa_region_j)` reconstructs scalar manual `log_kappa_scale` within stated numerical tolerance, and regional FD/all-ones FD are reported. |
| Veto diagnostics | Chain-rule reconstruction failure without explanation, CPU material route, missing per-region FD, changed seeds/theta/budget, nonfinite objective/gradient. |
| Explanatory diagnostics | Per-region manual scores, per-region FD slopes, region-wise MCSE, sum-vs-global residual, all-ones directional FD. |
| Not concluded | No production regional model, no HMC readiness, no posterior correctness. |

## Forbidden Claims And Actions

- Do not claim regional parameters are the final model.
- Do not change the baseline scalar SIR semantics.
- Do not hide failed regions by reporting only sums.
- Do not use whitening as a production preconditioner.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 if:

- Regional score sum reconstructs scalar score, or the reconstruction failure is
  written as a Phase 1 blocker with a focused next repair.
- Per-region FD evidence classifies the mismatch as one of:
  `localized_region`, `shared_across_regions`, `aggregation_failure`, or
  `inconclusive_due_to_mcse_or_runtime`.
- Phase 2 subplan is refreshed using Phase 1 findings.

## Stop Conditions

- Regional expansion cannot be added diagnostically without invasive production
  changes.
- Material run exits 137 twice under the reviewed route and no smaller exact
  aggregation repair is available.
- Chain-rule semantics cannot be stated unambiguously.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write Phase 1 result / close record.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
