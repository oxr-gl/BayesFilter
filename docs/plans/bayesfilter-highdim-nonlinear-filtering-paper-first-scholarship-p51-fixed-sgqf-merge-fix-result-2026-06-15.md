# Fixed-SGQF Merge-Fix Result

metadata_date: 2026-06-15
plan_reference: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p50-fixed-sgqf-merge-fix-plan-2026-06-15.md`
status: EXECUTION_COMPLETE

## Question

Did a source-faithful merge fix restore higher-level SGQF clouds, and do the
previous higher-level `carried_covariance` failures persist after the fix?

## Code changes made

### Primary implementation fix
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`

Narrow changes:
1. Replaced the old bucket scaling in `_merge_key(...)` with a simpler tolerance
   grid key based directly on the declared absolute tolerance.
2. Added `_find_merged_point(...)` to search existing merged nodes and merge only
   when the declared sup-norm tolerance actually passes.
3. Updated `tf_fixed_sgqf_cloud(...)` so weight accumulation uses the real
   tolerance check rather than the old magnitude-scaled bucket shortcut.

### Test updates
- `tests/test_fixed_sgqf_tf.py`
  - added higher-level cloud regressions:
    - 1D level-3 cloud keeps the full 5-point GHQ rule,
    - 2D level-3 cloud matches the Jia 17-point construction and covariance.
- `tests/test_fixed_sgqf_values_tf.py`
  - updated higher-level scalar tests to reflect the corrected cloud behavior;
  - added a level-4 dense-reference match row.
- `tests/test_fixed_sgqf_scores_tf.py`
  - updated the previous carried-covariance failure expectation for level-3;
  - after the fix, the score row remains accepted and returns the expected zero
    derivative for the zero-derivative fixture.

## Verification commands
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_tf.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_audit_tf.py tests/test_fixed_sgqf_testing_integration_tf.py tests/test_fixed_sgqf_verification_tf.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_tf.py tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_verification_tf.py tests/test_fixed_sgqf_audit_tf.py tests/test_fixed_sgqf_testing_integration_tf.py
```

## Final suite status
- `41 passed, 2 warnings`

## Focused probe results after the fix

### 1D higher-level clouds
After the fix:
- 1D level 3 cloud point count = 5
- 1D level 4 cloud point count = 7
- 1D level 5 cloud point count = 9

This now matches the fixed GHQ family declared in p47.

### 2D level-3 cloud
After the fix:
- 2D level-3 cloud point count = 17
- weight total = 1.0
- covariance matches the identity target within floating-point tolerance

This now matches the Jia 2D level-3 construction instead of the previous
collapsed 9-point artifact.

### Scalar quadratic sparse-level ladder
After the fix:
- level 1 remains weak on the selected scalar quadratic row;
- level 2 matches the dense reference;
- level 3 matches the dense reference;
- level 4 matches the dense reference;
- level 5 matches the dense reference.

So the previous interpretation “higher levels fail at carried covariance” is no
longer supported on this tested row.

### Multistep score row
The multistep score row remains accepted after the fix.
The accepted-branch multi-parameter score path is still intact.

### 3D affine level-3 probe
After the fix:
- 3D affine level 2 still matches exact Kalman;
- 3D affine level 3 now also matches exact Kalman to floating-point tolerance.

So the previous affine level-3 block also disappears after the cloud repair.

## Diagnostics summary
| Item | Before fix | After fix | Interpretation |
|---|---:|---:|---|
| 1D level-3 cloud point count | 3 | 5 | distinct GHQ nodes no longer collapse |
| 2D level-3 cloud point count | 9 | 17 | Jia source construction restored |
| 2D level-3 covariance error | ~0.4 | ~0 | cloud artifact removed |
| scalar level-3/4/5 carried-covariance block | present | absent on tested row | prior failure was cloud-bug-driven on this row |
| 3D affine level-3 carried-covariance block | present | absent | prior affine level-3 block was cloud-bug-driven on this row |
| final SGQF suite | 38 passed | 41 passed | stronger higher-level coverage after repair |

## Interpretation

### What changed
The merge fix restored the higher-level clouds to match the source-level point
structure implied by Jia 2012 and the local p47 fixed-GHQ specialization.

### What this means for the earlier suspicion
The earlier interpretation from the audit can now be sharpened:

- the suspicious higher-level failures were **not** good evidence against the
  original SGQF method;
- on the tested rows, they were artifacts of the higher-level cloud merge bug;
- after repairing the cloud, the previously suspicious higher-level level-3+
  behavior disappears on the tested scalar and affine probes.

### What is still not concluded
This fix does **not** prove:
- universal higher-level SGQF correctness,
- general convergence,
- production-default readiness,
- or that every future nonlinear high-level row will pass.

It does show that the previously reported higher-level failures should be
reinterpreted: they were caused by an implementation bug in cloud construction,
not by the source-authoritative SGQF method on the tested rows.

## Final verdict

The merge-fix execution succeeded.

### Main conclusion
The higher-level fixed-SGQF failures that motivated the source-authority audit
were primarily caused by a **real merge bug** in cloud construction.  After the
fix, the higher-level clouds become source-consistent and the previously observed
level-3 `carried_covariance` failures disappear on the tested scalar and affine
rows.

### Recommended next step
- Update any prior result notes or mental model that treated higher-level SGQF as
  inherently failing on those tested rows.
- Treat the current lane as repaired at the cloud-construction level, with the
  usual remaining nonclaims about broader scope.
