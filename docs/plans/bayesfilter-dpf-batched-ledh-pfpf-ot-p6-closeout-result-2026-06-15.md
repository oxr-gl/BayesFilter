# Phase 6 Result: Closeout And Promotion Boundary

Date: 2026-06-15

## Status

`COMPLETE_EXPERIMENTAL_OPT_IN`

## Safe Conclusion

The gated program produced an experimental TensorFlow implementation of
batched LEDH-PFPF-OT over independent model-parameter rows, plus a
TensorFlow-autodiff value+score wrapper for the fixed relaxed objective.

It is safe to treat this as an experimental opt-in implementation with focused
correctness, row-locality, compile, and descriptive benchmark evidence. It is
not yet a production default or public API feature.

## Decision Table

| Area | Status | Evidence | Remaining Gap | What Is Not Concluded |
| --- | --- | --- | --- | --- |
| Shape/API contract | Passed | Phase 1 shape-contract tests and no public export drift | Public API design and migration plan | Production/default readiness |
| Batched flow/transport core | Passed | Phase 2 focused CPU tests and graph smoke | Larger-dimensional and model-family coverage | General DPF correctness |
| Batched value recursion | Passed | B=1 and B=20 scalar-stack parity, row permutation, identical-row tests | Larger fixture parity and application fixtures | Posterior validity |
| Value+score wrapper | Passed with boundary repair | No-resampling finite differences, active-transport finite/row-local score tests | Active annealed-transport gradient contract remains separate | Classical particle-filter likelihood score |
| Compiled benchmark | Passed descriptive gate | CPU/GPU `tf.function(jit_compile=True)` artifacts with device metadata | Larger realistic DPF dimensions and repeated statistical benchmarking | Universal GPU speedup |
| HMC/NeuTra boundary | Not in scope | No HMC tests or blockers used as gates | N/A for filtering-lane promotion | HMC/NeuTra readiness |

## Benchmark Summary

Warm-call median seconds, compile time excluded:

| Mode | Transport | B | CPU | GPU | Boundary |
| --- | --- | ---: | ---: | ---: | --- |
| value | active raw OT | 20 | 0.0004247 | 0.0011840 | descriptive only |
| value | active raw OT | 256 | 0.0036069 | 0.0012761 | descriptive only |
| value | active raw OT | 4096 | 0.0336660 | 0.0016139 | descriptive only |
| value+score | no resampling/raw | 20 | 0.0014570 | 0.0017820 | descriptive only |
| value+score | no resampling/raw | 256 | 0.0099436 | 0.0018915 | descriptive only |

B=20 active value parity against a scalar compiled value loop passed with max
absolute delta `2.220446049250313e-16`.

## Checks

- Phase 6 artifact existence check: all required Phase 0-5 artifacts present.
- Benchmark artifact metadata check: all expected JSON artifacts present,
  finite, and `jit_compile=true`.
- Focused value/score test: `20 passed`.
- Focused benchmark harness test: `8 passed`.
- `git diff --check`: passed for touched implementation, tests, plans, and
  DPF benchmark artifacts.
- `git status --short --branch`: recorded in the execution ledger. Unrelated
  modified HMC files are present and were not touched by this closeout.

## Production Promotion Gaps

- Realistic DPF fixtures: current benchmark fixture is tiny
  (`T=3`, `N=4`, `D=1`), so production needs larger `T`, particle counts, and
  nonlinear/application fixtures.
- Active transport score semantics: active annealed transport has intentional
  stopped-gradient/custom-gradient boundaries; its gradient contract needs a
  separate reviewed plan before production score claims.
- Public API and default policy: no export or default integration has been made.
- Broader parity: B=20 active value parity passed; production should add larger
  scalar-stack samples where feasible and more model routes.
- Benchmark robustness: Phase 5 timings are single-shape descriptive evidence,
  not statistically replicated performance evidence.

## Final Human Decision Boundary

Recommended status: keep as experimental opt-in and use it to drive the next
production-hardening program. Do not promote to production default until the
remaining gaps above are closed by dedicated gates.

## Nonclaims

- No production default.
- No public API promotion.
- No classical particle-filter likelihood score.
- No posterior correctness.
- No HMC/NeuTra readiness.
- No universal GPU speedup.
