# Reset Memo: Fixed-SGQF Repaired Lane

metadata_date: 2026-06-15
status: REPAIRED_LANE_CONFIRMED

## Date
2026-06-15

## Context
Before this pass, the fixed-SGQF lane had completed its original testing program
and a source-authority audit, but higher-level SGQF behavior on tested scalar and
affine rows looked suspicious. In particular, level-3+ clouds could collapse and
some higher-level rows blocked at `carried_covariance`. The source-authority
audit traced that suspicion to a likely bug in higher-level cloud merge logic,
not to a source-authoritative SGQF limitation.

## Decision / policy
Future sessions should assume the following unless new evidence contradicts it:

- The earlier pre-fix higher-level failure story on the tested scalar and affine
  rows is superseded.
- The repaired fixed-SGQF lane is the current governing implementation surface.
- The higher-level merge bug was real and was the primary cause of the old
  suspicious level-3 behavior on the tested rows.
- Current result notes and closeout have been reconciled to the repaired lane.

## What changed
- File: `bayesfilter/nonlinear/fixed_sgqf_tf.py`
  - Repaired higher-level cloud merge behavior.
  - Replaced the old magnitude-scaled bucket shortcut with a real sup-norm
    tolerance merge check over existing merged nodes.
- File: `tests/test_fixed_sgqf_tf.py`
  - Added higher-level cloud regressions:
    - 1D level-3 cloud keeps the full 5-point GHQ rule,
    - 2D level-3 cloud matches the Jia 17-point construction and covariance.
- File: `tests/test_fixed_sgqf_values_tf.py`
  - Updated higher-level scalar expectations to reflect the repaired cloud.
  - Added a level-4 dense-reference match row.
- File: `tests/test_fixed_sgqf_scores_tf.py`
  - Updated the old carried-covariance failure expectation for level-3.
- Files under `docs/plans/`
  - Wrote the source-authority audit and merge-fix results.
  - Reconciled the original P1/P3/P7/P8 fixed-SGQF result notes with the
    repaired-lane evidence.

## Bugs / blockers resolved
- Symptom:
  - Higher-level clouds collapsed distinct GHQ nodes and produced suspicious
    level-3+ failures on tested rows.
- Root cause:
  - The cloud merge helper could merge distinct higher-level GHQ nodes into the
    same bucket.
- Resolution:
  - Implemented a real sup-norm tolerance-based duplicate search before merging
    weights, then reran higher-level cloud/value/score probes.

## Verification already run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_tf.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_audit_tf.py tests/test_fixed_sgqf_testing_integration_tf.py tests/test_fixed_sgqf_verification_tf.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_tf.py tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_verification_tf.py tests/test_fixed_sgqf_audit_tf.py tests/test_fixed_sgqf_testing_integration_tf.py
```

Observed:
- Final repaired SGQF suite status: `41 passed, 2 warnings`
- 1D higher-level cloud point counts now match the GHQ family:
  - level 3 = 5
  - level 4 = 7
  - level 5 = 9
- 2D level-3 cloud now has 17 points and correct covariance behavior.
- Scalar level-3/4/5 rows no longer fail on the tested row.
- 3D affine level-3 now matches exact Kalman on the tested row.

## Current policy
- Treat current fixed-SGQF result notes as reconciled to the repaired merged-
  cloud implementation.
- Keep both implementation fixes in force:
  1. rank-safe `_symmetrize(...)` for derivative-path tensors;
  2. source-faithful higher-level cloud merge repair.
- Read post-fix result claims as local tested evidence, not as universal SGQF
  guarantees.

## Known limitations / cautions
- No universal SGQF superiority claim.
- No general sparse-level convergence claim.
- No production-default recommendation.
- No claim that every future higher-level nonlinear row will pass.
- Later-time deterministic failure coverage (`time_index > 0`) is still not fully
  closed.

## Suggested next steps
1. If needed, write a short human-readable final SGQF status summary for paper or
   internal note use.
2. Only extend to broader higher-level nonlinear rows if a concrete consumer
   needs them.
3. Preserve the repaired-lane framing in any future baseline or documentation
   updates.
