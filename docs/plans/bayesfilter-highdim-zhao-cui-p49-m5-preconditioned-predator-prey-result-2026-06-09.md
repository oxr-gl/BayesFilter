# P49-M5 Preconditioned Predator-Prey Result

metadata_date: 2026-06-09
phase: P49-M5
status: PASS_P49_M5_PRECONDITIONED_PREDATOR_PREY

## Decision Table

| Field | Decision |
| --- | --- |
| Gate decision | Pass M5 for route-separated predator-prey ladder scaffolding and exact preconditioner/residual target-decomposition checks. |
| Primary criterion status | Passed for scoped repair: tests distinguish P47 M5b fixed-design accuracy tuning from source-route preconditioner evidence, exact fixtures verify `full = preconditioner + residual` in negative-log convention, and manifest guards reject identity-only production-token emission. |
| Veto diagnostic status | Passed: P47 fixed-design failure is not interpreted as source-route failure; preconditioner target identity is checked; no tolerance, horizon, rank, or window was loosened after results. |
| Main uncertainty | The full source-style preconditioned predator-prey filter remains unimplemented; only the route contract, manifest guard, and target-decomposition identity are tested. |
| Next justified action | Advance to M6 smoothing boundary and keep production predator-prey claims blocked unless a separate ladder passes. |
| Not concluded | No paper-scale predator-prey production token, nonlinear preconditioning usefulness claim, adaptive TT/SIRT fit quality, or full source-route filtering accuracy. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does a source-style full/preconditioned route repair the predator-prey gap relative to fixed-design BayesFilter? |
| Baseline/comparator | P47 M5b fixed-design blocker plus M1 source preconditioner/residual operation roles. |
| Primary pass criterion | A ladder scaffold separates route mismatch, fixed-design tuning failure, and source-route preconditioner evidence; exact target-decomposition checks cover the implemented M5 source-route evidence. |
| Diagnostics that can veto | P47 fixed-design failure interpreted as source failure; preconditioner/residual target equality unchecked; tolerances loosened after results. |
| Explanatory diagnostics | CPU-only pytest, compileall, static diff whitespace check, exact target-decomposition identity. |
| What will not be concluded | Production predator-prey readiness or source-route preconditioned filter completion. |
| Artifact preserving result | This file plus `tests/highdim/test_p49_source_route_preconditioned_predator_prey.py`. |

## Implemented Scope

M5 added minimal TensorFlow/source-route contract primitives in
`bayesfilter/highdim/source_route.py`:

- `SourceRoutePreconditionerContract` records source-route full,
  preconditioner, or residual target metadata with coefficient, reference
  density, and forward/inverse map labels.
- `source_route_residual_negative_log_target` computes the residual
  negative-log target as `full_negative_log_target -
  preconditioner_negative_log_target`.
- `source_route_preconditioned_target_identity_error` returns the max absolute
  error in the identity `full = preconditioner + residual`.
- `SourceRoutePredatorPreyLadderRow` and
  `SourceRoutePredatorPreyLadderManifest` record route-separated ladder rows
  and reject unearned production-token emission unless a future source-faithful
  row emits `PASS_SOURCE_PRECONDITIONED_FILTERING`.

The highdim subpackage exports were updated for these M5 helpers.  No top-level
`bayesfilter` API export was added.

## Route-Separation Interpretation

The P47 M5b result remains a fixed-design accuracy/tuning blocker.  It is not
evidence that source-style Zhao--Cui preconditioning fails.  M5 repairs the
claim boundary by making the ladder scaffold explicit:

| Row | Route | Status | Interpretation |
| --- | --- | --- | --- |
| P47 M5b fixed-design row | `gradient_bearing_adaptation` | blocked fixed-design accuracy/tuning | Does not decide source-route preconditioning. |
| P49 source preconditioner identity row | `source_faithful_filtering` | target identity only | Confirms the full/preconditioner/residual accounting invariant on exact fixtures. |
| Future source preconditioned filter row | `source_faithful_filtering` | not implemented in M5 | Must emit `PASS_SOURCE_PRECONDITIONED_FILTERING` before any predator-prey production claim. |

## Local Validation

Commands run CPU-only with `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`:

```text
pytest -q tests/highdim/test_p49_source_route_preconditioned_predator_prey.py tests/highdim/test_p49_source_route_recenter_normalizer.py tests/highdim/test_p49_source_route_sample_proposal.py tests/highdim/test_p49_source_route_retained_object.py tests/highdim/test_public_api_highdim.py tests/highdim/test_phase0_contracts.py
```

Result:

```text
48 passed, 2 TensorFlow Probability deprecation warnings
```

```text
python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p49_source_route_preconditioned_predator_prey.py tests/highdim/test_p49_source_route_recenter_normalizer.py tests/highdim/test_p49_source_route_sample_proposal.py tests/highdim/test_p49_source_route_retained_object.py
```

Result: passed.

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p49_source_route_preconditioned_predator_prey.py docs/plans/bayesfilter-highdim-zhao-cui-p49-visible-execution-ledger-2026-06-09.md
```

Result: passed.

## Interpretation

The M5 gate establishes an honest predator-prey repair boundary: P47 M5b is a
fixed-design route blocker, while source-route preconditioning requires its own
full/preconditioner/residual target identity checks and later filtering
implementation.  M5 passes as a route-separation scaffold and target-accounting
gate, not as a completed horizon/ablation ladder or predator-prey production
result.
