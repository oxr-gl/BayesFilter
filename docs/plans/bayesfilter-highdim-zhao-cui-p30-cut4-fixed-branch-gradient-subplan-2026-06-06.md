# P38-C5 Subplan: CUT4 Smooth-Branch Score Comparator

metadata_date: 2026-06-06
phase: P38-C5

Question: where a smooth structural branch exists, can CUT4 first-order score
sanity comparisons be recorded without claiming production Hessians or a
stable end-to-end highdim score API?

Comparator:

- production `tf_svd_cut4_score` compared against the testing-only autodiff
  oracle or finite differences on small smooth structural fixtures.

Audit design:

- use only certified smooth branches with no active floors and separated
  spectra;
- record score paired errors with a statistical/equivalence manifest;
- keep this as a CUT4 score sanity row, not a highdim end-to-end score API
  claim;
- the end-to-end fixed-branch score API remains `BLOCKED_UNVALIDATED` in the
  traceability ledger.

Equivalence criterion:

- paired score errors lie inside a declared CI band;
- Hessian remains `deferred` / testing-only.

Vetoes:

- active floor;
- weak spectral gap;
- nonfinite score;
- production Hessian claim;
- stable score API, HMC, or DSGE readiness claim.

Promotable claim:

- first-order CUT4 score sanity on small smooth structural fixtures only.

Non-claims:

- no production CUT4 Hessian claim;
- no highdim end-to-end score API claim;
- no stable public API claim;
- no HMC/DSGE/GPU readiness claim;
- no adaptive Zhao--Cui derivative support claim;
- no paper-scale validation claim.

Artifact:

- focused tests in `tests/highdim/test_p30_cut4_statistical_comparators.py`
  plus existing score tests under `tests/test_nonlinear_sigma_point_scores_tf.py`.
