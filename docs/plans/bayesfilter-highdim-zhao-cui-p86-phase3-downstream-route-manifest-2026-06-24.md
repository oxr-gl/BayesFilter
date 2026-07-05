# P86 Phase 3 Downstream Route Manifest

Date: 2026-06-24

Status: `PASS_P86_PHASE3_DOWNSTREAM_AUTHOR_ROUTE_WIRING_REVIEWED`

## Scope

This manifest records no-fit downstream consumer disposition for the author
`Lagrangep(4,8)` plus `AlgebraicMapping(1)` route after P86 Phases 1 and 2.

It does not approve fitting, optimizer steps, transport execution, GPU/HMC/LEDH,
scale, correctness, KR closure, or production readiness.

## Route

| Field | Value |
|---|---|
| Basis family | `lagrangep` |
| Basis order/elements | `order=4`, `num_elems=8` |
| Basis dimension | `33` per axis |
| Domain map | `algebraic`, `scale=1` |
| Density/mass convention | `REFERENCE_MEASURE` / `REFERENCE_MEASURE` |
| Test route dimension | `2` |
| Runtime posture | CPU-hidden local smoke only |

## Consumer Disposition

| Consumer | Disposition | Reason | Evidence |
|---|---|---|---|
| `bayesfilter/highdim/tt.py` | `smoked` | `FunctionalTT.integrate_all` consumes `integral_vector(REFERENCE_MEASURE)` on author `Lagrangep` axes. | `tests/highdim/test_p86_downstream_author_route_wiring.py::test_p86_functional_tt_integrate_all_consumes_author_lagrangep_basis` |
| `bayesfilter/highdim/squared_tt.py` | `smoked` | `SquaredTTDensity.sqrt_square_normalizer`, `normalizer`, and retained marginal values consume author-route mass and convention. | `tests/highdim/test_p86_downstream_author_route_wiring.py::test_p86_squared_tt_normalizer_and_marginal_consume_author_lagrangep_basis` |
| `bayesfilter/highdim/stochastic_density_training.py` | `smoked` | `TrainableFunctionalTT.normalizer` consumes author-route mass without optimizer/training steps. | `tests/highdim/test_p86_downstream_author_route_wiring.py::test_p86_trainable_tt_normalizer_consumes_author_lagrangep_basis_without_training` |
| `bayesfilter/highdim/derivatives.py` | `smoked` | `squared_tt_normalizer_derivative` consumes author-route mass for fixed bases. | `tests/highdim/test_p86_downstream_author_route_wiring.py::test_p86_squared_tt_normalizer_derivative_consumes_author_lagrangep_basis` |
| `bayesfilter/highdim/ukf_initializer.py` | `deferred_not_on_phase3_path` | The current UKF initializer projection assumes bounded-domain basis fields `.length`, `.left`, and `.right`; author algebraic initializer adaptation is not required for Phase 3 no-fit downstream smoke. | `bayesfilter/highdim/ukf_initializer.py:319-321`; no code path executed. |

## Nonclaims

- No fit quality evidence.
- No posterior correctness evidence.
- No KR production closure.
- No HMC readiness.
- No LEDH comparison.
- No d=50/d=100 scale evidence.
- No production readiness.

## Local Check

Exact CPU-hidden test command:

```text
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p86_downstream_author_route_wiring.py tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p86_algebraic_measure_contract.py
```

Result:

```text
15 passed, 2 warnings in 7.10s
```

Warnings:

```text
TensorFlow Probability distutils Version deprecation warnings only.
```
