# Phase 1 Result: Regional Kappa Expansion

Date: 2026-07-01

Status: `PASSED_WITH_PHASE2_HANDOFF`

## Decision

Phase 1 passes as a diagnostic gate.  The regional kappa expansion reconstructs
the current scalar manual `log_kappa_scale` score exactly under the repaired
seed-microbatch route, so scalar aggregation is not the root cause.

The discrepancy remains dynamic and regional: the regional finite-difference
sum is much more negative than the regional manual-score sum.  Phase 2 should
therefore test whether the mismatch is better explained by regional
infection-vs-recovery geometry, not by global scalar aggregation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does decomposing global `log_kappa_scale` into per-region log-kappa scores localize the mismatch or reveal an aggregation bug? |
| Baseline/comparator | GPU/TF32 budget-10 SIR route with seeds `81120..81124`, `T=3`, `N=64`, active-all transport, seed microbatch size `1`, theta `(0.02,-0.01,0.01)`. |
| Primary criterion | Regional manual scores sum to the current scalar manual `log_kappa_scale` score within tolerance, and regional FD evidence is reported. |
| Veto diagnostics | CPU material route, TF32 disabled, missing regional FD, changed seeds/theta/budget, nonfinite value/score, or unexplained chain-rule failure. |
| Nonclaims | No SIR gradient correctness, HMC readiness, posterior correctness, production regional model, or default-policy change. |

## Commands Run

Local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_regional_kappa_gradient_decomposition.py
bash -n scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh
pytest -q tests/test_p8p_regional_kappa_gradient_decomposition.py
pytest -q tests/test_ledh_pfpf_ot_p7_manual_score.py
```

Material GPU/TF32 run:

```bash
bash scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh
```

Focused score-parity check:

```bash
python - <<'PY'
import argparse
import tensorflow as tf
from docs.benchmarks import benchmark_p8p_parameterized_sir_gradient as p8p
from docs.benchmarks import benchmark_p8p_regression_fd_reparameterization as p8p_reg

args = argparse.Namespace(
    batch_seeds=[81120,81121,81122,81123,81124],
    time_steps=3,
    num_particles=64,
    theta_values=[0.02,-0.01,0.01],
    transport_policy='active-all',
    sinkhorn_iterations=10,
    sinkhorn_epsilon=1.0,
    annealed_scaling=0.9,
    annealed_convergence_threshold=1.0e-3,
    transport_plan_mode='streaming',
    transport_gradient_mode=p8p.core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE,
    transport_ad_mode='stabilized',
    row_chunk_size=64,
    col_chunk_size=64,
    particle_chunk_size=64,
    dtype='float32',
    tf32_mode='enabled',
    device='/GPU:0',
    device_scope='visible',
    cuda_visible_devices='0',
    expect_device_kind='gpu',
    seed_microbatch_size=1,
)
p8p._configure_precision(args)
p8p._configure_gpus()
contexts, _ = p8p_reg._build_microbatch_contexts(args)
plain = p8p_reg._manual_gradient_diagnostic_for_contexts(
    contexts,
    args.theta_values,
    compiler='eager',
    return_score_decomposition=False,
)
decomp = p8p_reg._manual_gradient_diagnostic_for_contexts(
    contexts,
    args.theta_values,
    compiler='eager',
    return_score_decomposition=True,
)
print('plain objective', float(plain['objective'].numpy()))
print('plain gradient', plain['gradient_tensor'].numpy().tolist())
print('decomp objective', float(decomp['objective'].numpy()))
print('decomp gradient', decomp['gradient_tensor'].numpy().tolist())
print('diff', (decomp['gradient_tensor'] - plain['gradient_tensor']).numpy().tolist())
PY
```

## Artifacts

- Diagnostic code:
  `docs/benchmarks/benchmark_p8p_regional_kappa_gradient_decomposition.py`
- Tests:
  `tests/test_p8p_regional_kappa_gradient_decomposition.py`
- Wrapper:
  `scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh`
- Material JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-budget10-2026-07-01.json`

## Route

The material run used:

- device `/GPU:0`;
- `float32`;
- TF32 enabled;
- streaming transport;
- manual streaming finite Sinkhorn stopped-scale-key gradient;
- seed microbatch size `1`;
- seeds `81120,81121,81122,81123,81124`;
- `T=3`, `N=64`;
- Sinkhorn iterations `10`.

The run produced `status=pass`. This Phase 1 artifact records GPU and TF32
evidence, but it does not record explicit XLA compiler status; therefore
Phase 1 claims only the GPU/TF32 streaming route evidenced in the JSON.

## Main Numbers

| Quantity | Value |
| --- | ---: |
| Objective | `-125.47383880615234` |
| Scalar manual `log_kappa_scale` | `-205.1933135986328` |
| Sum regional manual `log_kappa` | `-205.1933135986328` |
| Chain-rule absolute delta | `0.0` |
| Chain-rule tolerance | `1.0e-4` |
| Regional FD sum | `-263.2179145812988` |
| Regional FD sum minus scalar manual | `-58.024600982666016` |

Current same-context parity check:

| Route | Manual gradient |
| --- | --- |
| Plain manual score | `[-205.193603515625, 84.62638092041016, 47.33308792114258]` |
| Decomposed manual score | `[-205.1933135986328, 84.62630462646484, 47.33308792114258]` |
| Difference | `[0.0002899169921875, -0.0000762939453125, 0.0]` |

Thus the regional/decomposition hook is not changing the current manual score.

## Regional Table

| Region | Manual mean | MCSE | FD slope | FD - manual |
| ---: | ---: | ---: | ---: | ---: |
| 0 | `-44.518055` | `10.455665` | `-57.128902` | `-12.610847` |
| 1 | `-56.402557` | `4.219496` | `-67.394257` | `-10.991699` |
| 2 | `-17.691551` | `3.393065` | `-17.532349` | `0.159203` |
| 3 | `-21.114342` | `4.446944` | `-14.621734` | `6.492608` |
| 4 | `-6.481490` | `4.224358` | `-14.793395` | `-8.311905` |
| 5 | `-12.401180` | `4.472942` | `-16.429901` | `-4.028721` |
| 6 | `-15.134489` | `3.397395` | `-24.223326` | `-9.088837` |
| 7 | `-15.616262` | `3.490962` | `-26.935575` | `-11.319313` |
| 8 | `-15.833391` | `2.105026` | `-24.158476` | `-8.325085` |

Classification:

- `aggregation_failure`: ruled out by exact chain-rule reconstruction.
- `localized_region`: not supported as a single-region explanation.
- `shared_across_regions`: supported, with largest absolute gaps in regions
  `0`, `1`, `6`, `7`, `8`, and region `4` also notable.
- `inconclusive_due_to_mcse_or_runtime`: not the main classification, though
  MCSE remains explanatory and Phase 2 must keep uncertainty visible.

## Baseline Caveat

The prior budget-10 artifact
`docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.json`
contains manual `log_kappa_scale = -143.36988830566406`, while the repaired
current-code same-context manual route gives about `-205.1936`.

This is not caused by the Phase 1 regional decomposition: current plain and
decomposed manual scores match to about `3e-4`.  The older manual score should
therefore be treated as superseded for current-code decisions.  Its FD slope
for `log_kappa_scale`, `-263.1854553222656`, remains consistent with the
repaired regional FD sum, `-263.2179145812988`, but its manual score is not a
valid current-code scalar baseline.

## Skeptical Audit

- Wrong baseline: repaired by adding `--seed-microbatch-size 1` to the Phase 1
  wrapper and by using context aggregation matching the frozen budget route.
- Proxy metrics: regional FD gaps are diagnostic only, not promotion evidence
  for correctness or HMC readiness.
- Missing stop conditions: none triggered; chain-rule passed and no route veto
  fired.
- Unfair comparison: current regional manual and FD use the same seed groups,
  seeds, theta, budget, chunks, and transport route.
- Hidden assumption: the older `-143` manual score is not used as current
  truth after same-context parity established current plain/decomposed scores.
- Environment mismatch: material route was GPU/TF32. Explicit XLA compiler
  status was not captured in the Phase 1 JSON and is not claimed here.
- Artifact mismatch: material JSON now records `seed_microbatch_size=1` and
  `seed_microbatch_count=5`.

## Phase 2 Handoff

Advance to Phase 2 with this target:

- Preserve the same seed-microbatch route.
- Expose regional `log_kappa_j` and `log_nu_j` manual scores.
- Report regional
  `rho_j = (log_kappa_j - log_nu_j)/sqrt(2)` and
  `tau_j = (log_kappa_j + log_nu_j)/sqrt(2)` manual-vs-FD diagnostics.
- Focus interpretation on whether the Phase 1 mismatch is infection-vs-recovery
  contrast, common-rate direction, both, or neither.

Phase 2 must not claim Fisher orthogonality or production reparameterization.

## Nonclaims

- No SIR gradient correctness claim.
- No HMC readiness claim.
- No posterior correctness claim.
- No production regional model.
- No default-policy change.
