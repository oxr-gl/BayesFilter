# P49-M4 Recentring, Jacobian, And Normalizer Result

metadata_date: 2026-06-09
phase: P49-M4
status: PASS_P49_M4_RECENTERING_NORMALIZER

## Decision Table

| Field | Decision |
| --- | --- |
| Gate decision | Pass M4 for scoped source-route recentering, affine-Jacobian, shifted-target, and normalizer accounting. |
| Primary criterion status | Passed: focused tests cover weighted empirical recentering, determinant/Jacobian addition, shift-invariant log-normalizer update, and normalizer manifest fields. |
| Veto diagnostic status | Passed: `log(abs(det(L)))` is explicit; target shift cancels through `log(z) - const`; the recentering rule is fixed as weighted mean/covariance with expansion factor before larger model phases. |
| Main uncertainty | This is an accounting/helper gate, not production target tuning or adaptive TT/SIRT fitting. |
| Next justified action | Advance to M5 preconditioned predator-prey route repair. |
| Not concluded | No paper-scale filtering accuracy, preconditioner quality, HMC readiness, smoothing support, or full source-route completion. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are coordinate transforms and normalizers accounted for exactly in the source-faithful lane? |
| Baseline/comparator | M1 source operation contract plus analytic affine and shifted-target identities. |
| Primary pass criterion | Focused affine and nonlinear one-step tests pass moment, determinant, and log-normalizer checks. |
| Diagnostics that can veto | Missing determinant term; target shift changes final likelihood; recentering chosen after result inspection. |
| Explanatory diagnostics | CPU-only pytest, compileall, static diff whitespace check. |
| What will not be concluded | Production target tuning, adaptive TT/SIRT fit correctness, or full filtering accuracy. |
| Artifact preserving result | This file plus `tests/highdim/test_p49_source_route_recenter_normalizer.py`. |

## Implemented Scope

M4 added minimal TensorFlow source-route accounting primitives in
`bayesfilter/highdim/source_route.py`:

- `source_route_recenter` computes a deterministic weighted empirical mean and
  covariance from sample log weights, applies optional jitter, and stores a
  Cholesky scale multiplied by the expansion factor in
  `SourceRouteCoordinateFrame`.
- `source_route_reference_log_density_from_physical` adds
  `log(abs(det(L)))` when converting physical log density into local reference
  coordinates.
- `source_route_shifted_negative_log_target` applies the source-style
  stability shift to a negative-log target.
- `source_route_log_normalizer_update` returns the source-style
  `log_transport_normalizer - shift_constant` increment.

The highdim subpackage exports were updated for these M4 helpers.  No top-level
`bayesfilter` API export was added.

## Local Validation

Commands run CPU-only with `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`:

```text
pytest -q tests/highdim/test_p49_source_route_recenter_normalizer.py tests/highdim/test_p49_source_route_sample_proposal.py tests/highdim/test_p49_source_route_retained_object.py tests/highdim/test_public_api_highdim.py tests/highdim/test_phase0_contracts.py
```

Result:

```text
42 passed, 2 TensorFlow Probability deprecation warnings
```

```text
python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p49_source_route_recenter_normalizer.py tests/highdim/test_p49_source_route_sample_proposal.py tests/highdim/test_p49_source_route_retained_object.py
```

Result: passed.

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p49_source_route_recenter_normalizer.py docs/plans/bayesfilter-highdim-zhao-cui-p49-visible-execution-ledger-2026-06-09.md
```

Result: passed.

## Interpretation

The M4 gate establishes that the clean-room source-route lane has auditable
affine recentering and normalizer-accounting primitives.  The determinant term
is first-class through `SourceRouteCoordinateFrame.log_abs_det()`, and the
shift-invariance test verifies that changing the numerical stability constant
does not change the final log-likelihood increment.

M4 deliberately does not tune targets, fit transports, choose preconditioners,
or claim full source-route filtering quality.
