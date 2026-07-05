# Phase 5 Result: Generic Code-Wiring Implementation

Date: 2026-07-01

Status: `GENERIC_NSSM_PHASE5_LOCAL_PASS_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 5 implements the narrow structural-adapter refresh authorized by the executable refresh. The structural adapter now exposes explicit reviewed-admission metadata, supports affine structural models as exact-eligible SGQF adapter routes, reclassifies model C as approximate-eligible, and keeps model B explicitly ineligible under the current adapter. |
| Primary criterion status | Met locally: the reviewed contracts were implemented in the narrow seam set without widening target semantics, genericity claims, or API scope. |
| Veto diagnostic status | Passed locally: no silent model-specific fallback was promoted as generic support, no exact-target overclaim was introduced for model C, no top-level/HMC/API widening occurred, and no direct-likelihood SGQF wiring claim was introduced. |
| Main uncertainty | This refresh does not yet wire the generic non-Gaussian direct-likelihood SGQF runtime path or admit any gradient lane. Those remain for later phases. |
| Next justified action | Execute Phase 6 value validation for the reviewed structural-admission categories and the newly explicit affine-exact / model-C-approximate structural SGQF adapter split. |
| What is not being concluded | No value-gate pass yet, no gradient-gate pass, no HMC readiness, no top-level API promotion, and no production/default claim. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the reviewed contracts be implemented across the structural/nonlinear seam without silent semantic fallback? |
| Baseline/comparator | reviewed contracts from Phases 1-4 and the current implementation seams. |
| Primary criterion | Passed locally: the structural adapter now exposes exact/approximate/ineligible admission metadata and the focused tests pass without overclaiming generic nonlinear support. |
| Veto diagnostics | Passed locally: no hidden target drift, no unreviewed API-scope widening, and no silent model-specific fallback disguised as generic support. |
| Explanatory diagnostics | CPU-only focused pytest, compile checks, and adapter metadata inspection. |
| Not concluded | No value validation pass, no gradient admission, no HMC readiness, and no top-level/production promotion. |
| Artifact | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-code-wiring-result-2026-07-01.md` and refreshed `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-subplan-2026-07-01.md`. |

## Implemented Changes

### Structural adapter metadata

Updated [bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py](bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py) to add explicit reviewed-admission metadata on `TFFixedSGQFStructuralAdapterResult`:

- `admission_status`
- `target_scope`
- `nonclaims`
- convenience properties:
  - `exact_eligible`
  - `approximate_eligible`

### Affine structural exact-eligible adapter

`tf_structural_to_fixed_sgqf_model(...)` now supports affine structural models
through `TFFixedSGQFAffineModel`, with:

- `admission_status="exact_eligible"`
- `target_scope="exact_affine_structural_lane"`

### Model-C reclassification

The existing autonomous nonlinear-growth structural adapter path remains
implemented, but is now explicitly classified as:

- `admission_status="approximate_eligible"`
- `target_scope="declared_structural_gaussian_projection_model_c_adapter"`

This prevents silent exact-target overclaim.

### Model-B fail-closed ineligibility

The nonlinear accumulation structural fixture remains ineligible under the
current adapter, but the ineligibility reason and status are now more explicit
and aligned with the reviewed structural-admission contract.

## Focused Tests Updated

Updated focused tests to reflect the reviewed admission semantics:

- [tests/test_nonlinear_benchmark_models_tf.py](tests/test_nonlinear_benchmark_models_tf.py)
  - model B asserted ineligible
  - model C asserted approximate-eligible, not exact-eligible
  - affine structural model asserted exact-eligible

- [tests/test_fixed_sgqf_values_tf.py](tests/test_fixed_sgqf_values_tf.py)
  - model C structural adapter test now asserts approximate-eligible metadata
  - added affine structural adapter parity test to exact Kalman reference

## Local Checks

Commands actually run:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_nonlinear_benchmark_models_tf.py \
  tests/test_fixed_sgqf_values_tf.py \
  tests/test_fixed_sgqf_integration_tf.py
```

```bash
python -m compileall -q \
  bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py \
  tests/test_nonlinear_benchmark_models_tf.py \
  tests/test_fixed_sgqf_values_tf.py
```

```bash
git diff --check -- \
  bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py \
  tests/test_nonlinear_benchmark_models_tf.py \
  tests/test_fixed_sgqf_values_tf.py
```

Outcome:

- Focused CPU-only pytest passed: `23 passed, 2 warnings in 3.80s`.
- `compileall` passed.
- Diff hygiene passed.
- Warnings were TensorFlow Probability deprecation warnings only.

## Skeptical Plan Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided: only the reviewed structural-adapter seam was modified. |
| Proxy metric promoted | Avoided: compile/test success is recorded as implementation correctness evidence only, not value/gradient/HMC admission. |
| Missing stop condition | Avoided: model B remains fail-closed ineligible and model C remains approximate-eligible only. |
| Unfair comparison | Avoided: affine-exact, model-C-approximate, and model-B-ineligible statuses are now explicit. |
| Hidden assumption | Avoided: the implementation does not claim generic direct-likelihood SGQF runtime wiring. |
| Stale context | Avoided: changed files align with the reviewed Phase 5 executable refresh. |
| Environment mismatch | Avoided: focused checks were CPU-only with explicit GPU hiding. |
| Artifact-answer mismatch | Avoided: the result records the exact seam modified and the exact checks actually run. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745` |
| Worktree status | Dirty pre-existing research/doc worktree; unrelated dirty changes preserved. |
| Execution target | Narrow structural-adapter implementation refresh. |
| CPU/GPU status | CPU-only TensorFlow test run with `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA command was run. |
| Commands | See Local Checks commands above. |
| Data version | `N/A` (unit tests / no dataset mutation) |
| Random seeds | `N/A` (deterministic fixture/unit-test focus) |
| Wall time | `N/A` (no dedicated benchmark timing artifact for Phase 5) |
| Plan | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-code-wiring-subplan-2026-07-01.md` |
| Executable refresh | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-executable-refresh-2026-07-01.md` |
| Result | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-code-wiring-result-2026-07-01.md` |
| Refreshed Phase 6 subplan | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-subplan-2026-07-01.md` |

## Phase 6 Handoff

Phase 6 may start only after the ledgers record that:

- affine structural SGQF adaptation is exact-eligible and tested against exact Kalman reference;
- model C structural SGQF adaptation is approximate-eligible only;
- model B structural SGQF adaptation remains ineligible under the current adapter;
- the Phase 5 result is reviewed `AGREE`;
- the refreshed Phase 6 subplan is reviewed `AGREE`.

Phase 6 must validate value paths only. It must not admit gradients, HMC
readiness, top-level API promotion, production readiness, or default-policy
change.
