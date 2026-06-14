# P49-M2 Result: Retained TT/SIRT Object Skeleton

metadata_date: 2026-06-09
phase: P49-M2
status: PASS
supervisor: Codex
reviewer: Claude Code read-only

PASS_P49_M2_RETAINED_TRANSPORT_OBJECT

## Decision Table

| Field | Result |
| --- | --- |
| Decision | PASS |
| Primary criterion status | PASS: a minimal clean-room retained-object skeleton passes shape, metadata, branch, and no-all-grid checks. |
| Veto diagnostic status | PASS: source-faithful retained objects reject all-grid tensor-product storage and pairwise-grid propagation; fixed-branch grid retention remains separately labeled as a gradient-bearing adaptation. |
| Main uncertainty | This is an interface/invariant skeleton, not a complete adaptive TT/SIRT transport implementation. |
| Next justified action | Submit M2 to Claude read-only review, then advance to P49-M3 only if Claude returns `VERDICT: AGREE`. |
| What is not concluded | No adaptive TT-cross production quality, filtering accuracy, ESS/proposal correctness, recentering correctness, smoothing support, or HMC readiness. |

## Implementation Summary

Added:

- `bayesfilter/highdim/source_route.py`
- `tests/highdim/test_p49_source_route_retained_object.py`

Exported through the experimental `bayesfilter.highdim` subpackage only:

- `SOURCE_FAITHFUL_ROUTE_LABEL`
- `GRADIENT_ADAPTATION_ROUTE_LABEL`
- `SourceRouteCoordinateFrame`
- `SourceRouteSampleDiagnostics`
- `SourceRouteNormalizerContribution`
- `SourceRouteRetainedObject`
- `effective_sample_size_from_log_weights`
- `source_route_retained_object_identity`

## Contract Coverage

The M2 skeleton carries:

- retained transport object metadata;
- affine coordinate frame `mu`, `L`, expansion factor, and `log_abs_det`;
- retained samples and log weights;
- sample count and ESS diagnostics;
- normalizer terms `log_transport_normalizer`, `shift_constant`, and determinant policy;
- route label;
- storage-kind and transition-interface labels;
- mandatory transport `manifest_payload()` metadata;
- canonical branch identity.

For `source_faithful_filtering`, the skeleton rejects:

- `scalar_dense_grid`;
- `scalar_tt_grid`;
- `multistate_tt_grid`;
- `all_axes_tensor_product_grid`;
- `pairwise_grid_transition`;
- `all_grid_pairwise_transition`;
- `multistate_grid_pairwise_transition`.

The same grid labels remain admissible under `gradient_bearing_adaptation`, so
existing fixed-branch retained grids are preserved under their proper route
label.

## Repair Note

The first focused test run failed because direct dataclass equality on
`BranchIdentity` recursed into TensorFlow tensor-valued manifest payloads.  The
fix compares canonical branch-hash values instead, which is the intended branch
identity invariant for these objects.

## Validation

Commands:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p49_source_route_retained_object.py tests/highdim/test_public_api_highdim.py tests/highdim/test_phase0_contracts.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p49_source_route_retained_object.py tests/highdim/test_phase0_contracts.py
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p49_source_route_retained_object.py tests/highdim/test_phase0_contracts.py docs/plans/bayesfilter-highdim-zhao-cui-p49-m2-retained-transport-object-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p49-visible-execution-ledger-2026-06-09.md
```

Result:

- `29 passed, 2 warnings`
- compileall passed
- diff check passed

The warnings are TensorFlow Probability deprecation warnings unrelated to M2.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d`; worktree is dirty with unrelated existing files. |
| Commands | Focused CPU-only pytest including the backend-policy static test, compileall, diff check, static reads of retained-filter code and tests. |
| Environment | Local shell, `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`. |
| CPU/GPU status | CPU-only by explicit environment. |
| Random seeds | N/A. |
| Output artifacts | This result file; source-route retained skeleton code; focused tests; visible execution ledger update. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m2-retained-transport-object-subplan-2026-06-09.md` |

## Post-Run Red-Team Note

Strongest alternative explanation: the skeleton could be too permissive because
it validates labels and metadata, not actual transport map behavior.  P49-M3
and P49-M4 must test proposal correction, ESS, recentering, determinant, and
normalizer math before any filtering claim.

What would overturn this M2 pass: a source-faithful retained object can be
constructed with all-grid tensor-product storage or pairwise-grid propagation,
or the object can omit coordinate-frame/normalizer/sample metadata while still
passing tests.

Weakest part of the evidence: no adaptive TT/SIRT fit object exists yet.
