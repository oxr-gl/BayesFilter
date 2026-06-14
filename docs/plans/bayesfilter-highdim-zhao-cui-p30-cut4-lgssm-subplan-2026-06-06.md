# P38-C0 Subplan: LGSSM CUT4 Statistical Comparator

metadata_date: 2026-06-06
phase: P38-C0

Question: on small affine LGSSM fixtures, does the highdim exact value path
agree with CUT4 in a paired statistical-equivalence sense while preserving
exact Kalman as the primary exact reference?

Comparator:

- primary exact reference: exact Kalman;
- secondary comparator: `tf_svd_cut4_filter` on the same affine structural
  model.

Audit design:

- fixed 2-state, 2-innovation affine LGSSM so CUT4-G has augmented dimension
  4 and is feasible;
- fixed observation audit set with at least four paired rows;
- highdim candidate: `FixedBranchSquaredTTFilter` with no TT artifacts;
- CUT4 comparator: structural affine TensorFlow model with the same transition,
  process covariance, observation matrix, and observation covariance.

Equivalence criterion:

- paired CI for `candidate_loglik - cut4_loglik` lies inside `[-1e-8, 1e-8]`;
- max absolute paired error is at most `1e-7`;
- exact Kalman difference is also at most `1e-8`.

Vetoes:

- nonfinite value;
- CUT4 point count not equal to `2d+2^d`;
- deterministic/support residual above `1e-10`;
- exact Kalman mismatch;
- any claim that CUT4 replaces exact Kalman.

Non-claims:

- not full Zhao--Cui LGSSM reproduction grid;
- no derivative claim;
- no paper-scale scalability claim.

Artifact:

- `tests/highdim/test_p30_cut4_statistical_comparators.py`
- P38 result ledger.
