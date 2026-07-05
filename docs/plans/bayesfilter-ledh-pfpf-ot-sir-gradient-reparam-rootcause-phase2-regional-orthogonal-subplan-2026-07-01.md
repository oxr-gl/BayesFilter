# Phase 2 Subplan: Regional Orthogonal Kappa/Nu Coordinates

Date: 2026-07-01

Status: `REFRESHED_AFTER_PHASE1_PENDING_REVIEW`

## Phase Objective

Test regional epidemic-growth and time-scale coordinates after regional kappa
chain-rule diagnostics:

```text
rho_j = (log_kappa_j - log_nu_j) / sqrt(2)
tau_j = (log_kappa_j + log_nu_j) / sqrt(2)
```

## Entry Conditions Inherited From Previous Phase

- Phase 1 passed the regional kappa chain-rule check under the GPU/TF32
  seed-microbatch route.
- Phase 1 ruled out scalar aggregation failure and classified the mismatch as
  shared across regions with notable gaps in regions `0`, `1`, `4`, `6`, `7`,
  and `8`.
- Any regional implementation is diagnostic-only and preserves scalar baseline
  semantics on the diagonal.
- Phase 2 inherits the current-code scalar manual score from Phase 1, not the
  superseded older `-143.36988830566406` manual score in the prior budget
  artifact.

## Required Artifacts

- Diagnostic harness:
  `docs/benchmarks/benchmark_p8p_regional_orthogonal_gradient_decomposition.py`
- Unit/smoke tests:
  `tests/test_p8p_regional_orthogonal_gradient_decomposition.py`
- Material wrapper:
  `scripts/run_sir_gradient_reparam_rootcause_phase2_regional_orthogonal_budget10.sh`
- Phase 2 diagnostic JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-budget10-2026-07-01.json`
- Phase 2 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-result-2026-07-01.md`
- Refreshed Phase 3 subplan.

## Required Checks, Tests, Reviews

- Local algebra tests for regional rho/tau chain-rule mapping.
- Syntax/compile checks for touched Python files.
- Material GPU/TF32 budget-10 diagnostic if Phase 1 handoff allows. If the
  Phase 2 implementation uses explicit `tf.function(jit_compile=True)`, record
  that compiler status in the JSON; otherwise do not claim XLA.
- Claude read-only review if Phase 2 changes the Phase 3 target.

Exact local command templates:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_regional_orthogonal_gradient_decomposition.py
pytest -q tests/test_p8p_regional_orthogonal_gradient_decomposition.py
bash -n scripts/run_sir_gradient_reparam_rootcause_phase2_regional_orthogonal_budget10.sh
```

Exact material command:

```bash
bash scripts/run_sir_gradient_reparam_rootcause_phase2_regional_orthogonal_budget10.sh
```

The material wrapper must use visible GPU/TF32, fixed seeds
`81120,81121,81122,81123,81124`, `T=3`, `N=64`, Sinkhorn iterations `10`,
theta `(0.02,-0.01,0.01)`, active-all transport, streaming manual transport
gradient, and seed microbatch size `1`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the problematic direction better described as regional infection-vs-recovery geometry rather than kappa alone? |
| Baseline/comparator | Phase 1 regional kappa result, using current-code scalar manual score and seed-microbatch route; global physics/whitened artifacts remain explanatory only. |
| Primary pass criterion | Regional rho/tau diagnostics classify whether the mismatch is concentrated in infection-vs-recovery contrast, common-rate direction, both, or neither, while preserving chain-rule reconstruction to kappa/nu controls. |
| Veto diagnostics | Missing regional mapping, CPU material route, changed baseline seeds/theta/budget, nonfinite diagnostic, unsupported production claim. |
| Explanatory diagnostics | Per-region kappa/nu/rho/tau manual-vs-FD table, projected MCSE, direction concentration, Phase 1 high-gap region labels. Relation to the prior whitened direction may be discussed only with an explicit citation to `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-2026-07-01.json`. |
| Not concluded | No global orthogonal parameterization proof and no HMC readiness. |

## Forbidden Claims And Actions

- Do not call the basis Fisher-orthogonal unless Fisher cross-information is
  actually estimated and checked.
- Do not promote regional rho/tau as production.
- Do not change threshold rules after seeing results.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 if:

- Phase 2 identifies transition/RK4 derivative terms as plausible, or Phase 1
  already showed kappa regional mismatches need transition-level audit.
- Phase 2 result states whether infection-vs-recovery contrast, common-rate
  direction, both, neither, or MCSE/FD curvature explains the observed pattern.
- If Phase 2 is inconclusive, the result must state whether inconclusiveness is
  caused by MCSE, FD curvature, runtime/memory, or implementation scope.
- Phase 3 subplan states exact local sensitivity equations/checks.

## Stop Conditions

- Phase 1 shows the problem is unrelated to regional kappa/nu dynamic
  parameters.
- Orthogonal mapping cannot be tested without broad production rewrites.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write Phase 2 result / close record.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
