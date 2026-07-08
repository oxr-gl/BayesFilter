# Phase 6 Result: Value Validation Gate

Date: 2026-07-01

Status: `GENERIC_NSSM_PHASE6_VALUE_GATE_LOCAL_PASS_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 6 passes the narrow structural value gate for the reviewed structural-admission categories. The affine structural SGQF adapter is validated as exact-eligible against exact Kalman recovery, model C is validated only as a declared Gaussian-projection approximate lane against the dense Gaussian-projection comparator, and model B remains blocked/ineligible rather than being silently promoted into a value lane. |
| Primary criterion status | Met locally: each reviewed lane was compared only against the exact or declared scalar it is authorized to approximate, with no target drift. |
| Veto diagnostic status | Passed locally: no wrong-scalar tieout, no surrogate promoted as exact-target evidence, no affine recovery failure, no fixed-cloud oracle failure, and no branch-invalid comparison were observed in the focused scope. |
| Main uncertainty | Gradient admission remains ahead. The current generic non-Gaussian direct-likelihood SGQF runtime seam remains unwired and was not promoted by this phase. |
| Next justified action | Execute Phase 7 for same-branch gradient validation only on the lanes whose value gate now passes. |
| What is not being concluded | No gradient admission yet, no HMC readiness, no top-level API promotion, and no production/default claim. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Do the implemented value paths reproduce the exact or declared scalar they are authorized to compute at the intended claim level? |
| Baseline/comparator | reviewed Phase 5 implementation and the exact/declared comparators frozen in earlier phases. |
| Primary criterion | Passed locally in the reviewed narrow scope: the affine structural lane cleared its exact Kalman comparator, model C cleared its declared Gaussian-projection comparator, and model B remained correctly blocked rather than silently promoted. |
| Veto diagnostics | Passed locally: no wrong-scalar tieout, no surrogate promoted as exact-target evidence, no affine recovery failure, and no branch-invalid comparison in the focused value scope. |
| Explanatory diagnostics | focused CPU-only runtime outputs, admitted-lane category checks, and comparator interpretation notes. |
| Not concluded | No gradient admission, no HMC readiness, and no top-level/production promotion. |
| Artifact | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-result-2026-07-01.md` and refreshed `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-subplan-2026-07-01.md`. |

## Reviewed Lanes And Comparator Outcomes

### 1. Affine structural exact-eligible lane

- reviewed admission status: `exact_eligible`
- comparator: exact Kalman recovery
- outcome: passed

Evidence used:

- [tests/test_nonlinear_benchmark_models_tf.py](tests/test_nonlinear_benchmark_models_tf.py)
  confirms affine structural models are now exact-eligible under the structural
  adapter.
- [tests/test_fixed_sgqf_values_tf.py](tests/test_fixed_sgqf_values_tf.py)
  confirms the affine structural adapter path matches exact Kalman log
  likelihood, filtered means, and filtered covariances.

Interpretation:

- This is exact-target structural value evidence for the reviewed affine SGQF
  adapter lane only.

### 2. Model-C approximate-eligible structural lane

- reviewed admission status: `approximate_eligible`
- comparator: dense Gaussian-projection first-step reference
- outcome: passed for the declared approximate lane

Evidence used:

- [tests/test_nonlinear_benchmark_models_tf.py](tests/test_nonlinear_benchmark_models_tf.py)
  confirms model C is approximate-eligible, not exact-eligible.
- [tests/test_fixed_sgqf_values_tf.py](tests/test_fixed_sgqf_values_tf.py)
  confirms the structural adapter result is intentionally compared against a
  dense Gaussian-projection first-step reference and preserves the explicit
  mismatch band that prevents silent exact-target overclaim.

Interpretation:

- This is declared Gaussian-projection approximate value evidence only.
- It must not be relabeled as exact-target support.

### 3. Model-B ineligible lane

- reviewed admission status: `ineligible`
- comparator: none admitted
- outcome: passed as fail-closed ineligibility

Evidence used:

- [tests/test_nonlinear_benchmark_models_tf.py](tests/test_nonlinear_benchmark_models_tf.py)
  confirms model B remains structurally ineligible under the current adapter.

Interpretation:

- Model B remaining blocked is a pass of the admission contract, not a missing
  test.

## Local Checks

Commands actually run:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_nonlinear_benchmark_models_tf.py \
  tests/test_fixed_sgqf_values_tf.py \
  tests/test_fixed_sgqf_integration_tf.py
```

```bash
git diff --check -- \
  docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-result-2026-07-01.md \
  docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-subplan-2026-07-01.md
```

Outcome:

- Focused CPU-only pytest passed: `23 passed, 2 warnings in 6.41s`.
- Diff hygiene for the Phase 6 result / Phase 7 handoff artifacts passed.
- Warnings were TensorFlow Probability deprecation warnings only.

## Skeptical Plan Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided: each lane was compared only to the exact or declared scalar it is reviewed to approximate. |
| Proxy metric promoted | Avoided: passing tests are recorded as value-gate evidence only, not gradient/HMC/API authority. |
| Missing stop condition | Avoided: model B remained blocked rather than being pushed through a value gate. |
| Unfair comparison | Avoided: the exact-target affine lane and the declared-surrogate model-C lane were not mixed into one pass claim. |
| Hidden assumption | Avoided: no generic direct-likelihood SGQF runtime value claim was inferred from this phase. |
| Stale context | Avoided: validation remained constrained to the reviewed Phase 5 implementation and Phase 1-4 contracts. |
| Environment mismatch | Avoided: runtime was CPU-only with explicit GPU hiding. |
| Artifact-answer mismatch | Avoided: the result yields a value-gate decision only, not a derivative or production decision. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745` |
| Worktree status | Dirty pre-existing research/doc worktree; unrelated dirty changes preserved. |
| Execution target | Narrow structural value-gate validation. |
| CPU/GPU status | CPU-only TensorFlow test run with `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA command was run. |
| Commands | See Local Checks commands above. |
| Data version | `N/A` (fixture/unit-test validation only) |
| Random seeds | `N/A` (deterministic fixture/unit-test focus) |
| Wall time | `N/A` (no dedicated benchmark timing artifact for Phase 6) |
| Plan | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-subplan-2026-07-01.md` |
| Executable refresh | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-executable-refresh-2026-07-01.md` |
| Result | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-result-2026-07-01.md` |
| Refreshed Phase 7 subplan | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-subplan-2026-07-01.md` |

## Phase 7 Handoff

Phase 7 may start only after the ledgers record that:

- the affine structural SGQF lane passed the exact-target value gate;
- the model-C structural SGQF lane passed only the declared Gaussian-projection
  approximate value gate;
- model B remains blocked/ineligible and is excluded from score-admission work;
- the Phase 6 result is reviewed `AGREE`;
- the refreshed Phase 7 subplan is reviewed `AGREE`.

Phase 7 may validate gradients only for lanes whose value gate has passed at the
reviewed claim level. It must not claim HMC readiness, top-level API promotion,
production readiness, or default-policy change.
