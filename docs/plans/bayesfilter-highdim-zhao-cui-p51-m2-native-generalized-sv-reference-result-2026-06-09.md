# P51-M2 Result: Native Generalized SV Reference

metadata_date: 2026-06-09
phase: P51-M2
status: PASS_P51_M2_NATIVE_GENERALIZED_SV_REFERENCE
supervisor: Codex
reviewer: Claude Code read-only

## Decision

P51-M2 closes the native generalized SV reference gap at low dimension by
adding a dense same-target raw-observation reference for

```text
y_t = beta s_t + exp(h_t / 2) epsilon_t,    x_t = (s_t, h_t).
```

The reference is implemented in TensorFlow/TFP with tensor-product Legendre
quadrature over the two latent state coordinates.  Gradients are obtained by
TensorFlow autodiff through the same dense reference.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | We can construct a defensible low-dimensional same-target reference for native generalized SV. |
| Baseline/comparator | P50-M5 native generalized SV blocker, P45 target registry, and P51-M2 subplan. |
| Primary criterion | Passed for a declared low-dimensional native raw-y fixture by refinement of dense value and gradient. |
| Veto diagnostics | Passed: transformed residual, moment-matched Kalman, KSC mixture, CUT4, and Zhao-Cui proxies are not treated as exact native same-target evidence. |
| Not concluded | No CUT4 same-target equality. No Zhao-Cui same-target equality. No HMC readiness. No production generalized SV readiness. |

## Implementation

Added:

- `bayesfilter.highdim.NativeGeneralizedSVSSM`
- `bayesfilter.highdim.NativeGeneralizedSVDenseReferenceResult`
- `bayesfilter.highdim.native_generalized_sv_dense_reference`

The model state is `(s_t, h_t)`, with independent stationary AR(1) state laws
and raw-y observation density with mean `beta s_t` and variance `exp(h_t)`.
The TensorFlow implementation uses the equivalent scale `exp(h_t/2)`.  The
parameterization is

```text
theta = (atanh(rho_s), atanh(rho_h), log(sigma_s), log(sigma_h), log(beta)).
```

## Validation

Focused validation actually run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p51_native_generalized_sv_reference.py tests/highdim/test_p50_sv_generalized_sv_ladder.py tests/highdim/test_p45_generalized_sv_comparison_blocker.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/native_generalized_sv.py bayesfilter/highdim/__init__.py tests/highdim/test_p51_native_generalized_sv_reference.py
git diff --check -- bayesfilter/highdim/native_generalized_sv.py bayesfilter/highdim/__init__.py tests/highdim/test_p51_native_generalized_sv_reference.py docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-manifest-2026-06-09.json docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p51-visible-execution-ledger-2026-06-09.md
```

Results:

- `13 passed, 2 warnings` for the focused pytest command.  The warnings were
  TensorFlow Probability deprecation warnings from the local environment.
- `compileall` passed.
- `git diff --check` passed.

## Nonclaims

- No CUT4 same-target equality.
- No Zhao-Cui same-target equality.
- No HMC readiness.
- No production generalized SV readiness.
- No GPU readiness.
- No source-faithful adaptive TT/SIRT filtering.
- No S&P 500 reproduction.
