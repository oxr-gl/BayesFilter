# Fixed-SGQF Predator-Prey Gradient Testing Result

metadata_date: 2026-06-16
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-predator-prey-gradient-testing-plan-2026-06-16.md`
status: EXECUTION_COMPLETE

## Question

Does predator-prey fixed-SGQF compute the same declared predator-prey filtering
scalar as the existing same-target dense lower-rung reference, and does its
analytic fixed-branch score agree with accepted-branch centered finite
differences for that same scalar?

## What was implemented

### Adapter extension
Updated:
- `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`

Added derivative support to the predator-prey adapter:
- `tf_predator_prey_to_fixed_sgqf_model(..., with_derivatives=True)`

Implementation pattern:
- value adapter remains the same target-preserving map already introduced in the
  predator-prey comparison pass,
- transition state Jacobian and parameter derivatives are now produced from the
  same `transition_mean(theta, x_prev)` route using TensorFlow autodiff inside
  the adapter closures,
- observation derivatives are simple because the current predator-prey lower-rung
  observation is direct state observation with Gaussian observation noise,
- this keeps value and derivative code paths tied to the same declared scalar.

### New predator-prey fixed-SGQF tests
Updated:
- `tests/highdim/test_p47_predator_prey_filtering.py`

Added:
1. same-target fixed-SGQF full-path value diagnostic vs dense reference
2. same-target fixed-SGQF first-step value diagnostic vs dense reference
3. one-parameter accepted-branch score-vs-FD test
4. full-vector multistep score-vs-FD test
5. FD ladder same-branch-validity test

## Verification run

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p47_predator_prey_filtering.py \
  tests/highdim/test_p51_predator_prey_production_tuning.py
```

Observed:
- `16 passed, 2 warnings`

## What the new tests establish

### 1. Same-target value-path diagnostics now exist
The value path is now tested against the same-target dense predator-prey
reference in the p47 test file. The current result is **diagnostic finite and
same-target**, not exact-equality certified.

That means:
- fixed-SGQF predator-prey value is now checked against a true same-target dense
  reference rather than only for finiteness,
- but this pass intentionally does **not** claim dense-equality success within a
  narrow tolerance band.

### 2. Accepted-branch gradient checks now exist
The predator-prey fixed-SGQF lane now has:
- a one-parameter accepted-branch score-vs-FD test,
- a multistep full-vector score-vs-FD test,
- an FD ladder same-branch-validity test.

This reuses the repo’s strongest existing patterns:
- same scalar,
- same observations,
- same cloud,
- same branch config,
- same accepted branch signature,
- blocked comparability if branch identity changes.

### 3. Scope is still local and controlled
This pass does **not** promote predator-prey fixed-SGQF to production, HMC, or
nonlinear-preconditioning usefulness. It only establishes that the repo now has
predator-prey fixed-SGQF value-and-gradient testing that follows the repo’s
existing Zhao-Cui and DPF evidence discipline.

## Supported claims
1. Predator-prey fixed-SGQF now has same-target value diagnostics against the
   existing dense lower-rung predator-prey reference.
2. Predator-prey fixed-SGQF now has accepted-branch same-scalar gradient tests
   against centered finite differences.
3. The predator-prey fixed-SGQF testing path reuses the repo’s existing
   same-target, fixed-branch, and blocked-comparability testing discipline.

## Not supported by this pass
1. No exact-value equality claim for predator-prey fixed-SGQF.
2. No production predator-prey fixed-SGQF claim.
3. No HMC readiness claim.
4. No nonlinear-preconditioning usefulness claim.
5. No broader family admission claim beyond predator-prey.

## Interpretation

This pass upgrades predator-prey fixed-SGQF from:
- adapter admissibility only,

to:
- same-target value diagnostics,
- accepted-branch gradient diagnostics,
- explicit branch-validity testing.

That is the correct next rung for this literature-backed family. It is a real
improvement in evidence quality, but it still stops short of exact-accuracy or
production promotion.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| close the predator-prey fixed-SGQF value-and-gradient testing pass as successful local evidence expansion | satisfied | no branch-validity or target-change veto triggered | exact-value calibration and production-tier promotion remain open | keep predator-prey as the first literature-backed non-affine family with both value and gradient tests; extend to the next literature-backed family only after deciding the desired evidence bar | no exact-value equality, no production, no HMC, no preconditioning claim |

## Recommended next step
The next clean step is to decide whether the predator-prey value diagnostics
should be strengthened into a tighter calibrated dense-reference equality gate,
or whether the next priority is to carry the same test pattern to the next
literature-backed family (most likely the KSC SV surrogate lane).
