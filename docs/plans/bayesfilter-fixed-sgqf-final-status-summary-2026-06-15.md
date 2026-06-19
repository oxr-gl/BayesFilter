# Fixed-SGQF Final Status Summary

## Current status
The fixed-SGQF lane is currently in a **repaired and audited** state.

What changed:
- a source-authority audit found that the earlier suspicious higher-level SGQF
  failures were caused by a real cloud merge bug,
- the cloud merge logic was repaired,
- the original result notes and closeout were reconciled to the repaired lane.

Current suite status:
- **41 passed, 2 warnings**

## What is now strongly supported

### 1. Exact-reference affine rows
Fixed-SGQF matches exact Kalman on tested affine Gaussian rows:
- 1D,
- 2D,
- 3D,
including the repaired 3D level-3 row.

### 2. Dense-reference nonlinear row
On the selected scalar quadratic fixture, fixed-SGQF matches a recursive dense
numerical reference through three observations.

### 3. Higher-level clouds on tested rows
The repaired cloud builder now preserves the expected higher-level structure on
tested rows:
- 1D level-3/4/5 clouds keep the full GHQ point counts,
- 2D level-3 cloud matches the Jia 17-point construction and covariance.

### 4. Score evidence
The fixed-branch score lane remains intact and has a multistep, multi-parameter,
accepted-branch FD parity row.

### 5. Selected-fixture baseline positioning
On the tested scalar quadratic row, fixed-SGQF is closer to the dense reference
than UKF or cubature.

## What was wrong before
The earlier higher-level failure story on the tested scalar and affine rows was
caused by a higher-level cloud merge bug. Distinct GHQ nodes were being merged
incorrectly, which corrupted higher-level clouds and produced misleading
`carried_covariance` failures.

That interpretation is now superseded.

## What is still not established
- No universal SGQF superiority claim.
- No general sparse-level convergence claim.
- No production-default recommendation.
- No paper-scale high-dimensional readiness claim.
- No claim that every future higher-level nonlinear row will pass.
- No full closure yet on all later-time deterministic failure modes.

## Practical takeaway
If future work needs a summary in one sentence, use this:

> BayesFilter’s fixed-SGQF lane is now repaired, source-audited, and locally
> well-supported on tested affine, scalar nonlinear, cloud-construction, and
> fixed-branch score rows; the earlier higher-level failure story on the tested
> scalar and affine rows was a merge-bug artifact, not evidence against the
> SGQF method itself.
