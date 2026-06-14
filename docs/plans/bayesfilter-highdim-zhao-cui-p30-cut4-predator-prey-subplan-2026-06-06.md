# P38-C3 Subplan: Predator-Prey CUT4 Feasibility Diagnostic

metadata_date: 2026-06-06
phase: P38-C3

Question: can a clean-room BayesFilter additive-Gaussian closure inspired by
the P30 predator-prey model contract be evaluated by CUT4 on a small
diagnostic row, while blocking native predator-prey filtering and
nonlinear-preconditioning usefulness claims?

Comparator:

- `tf_svd_cut4_filter` on a clean-room structural predator-prey-inspired
  additive-Gaussian closure model.

Audit design:

- 2-state predator-prey fixture at the declared true parameter vector;
- additive Gaussian process noise and identity Gaussian observation closure;
- fixed observations from a replayable short simulation;
- CUT4 point count capped by augmented dimension 4;
- no highdim candidate equivalence because current BayesFilter predator-prey
  evidence is model-contract and comparison-schema evidence only;
- traceability status is `BAYESFILTER_EXTENSION`, not source-matched native
  Zhao--Cui/MATLAB predator-prey filtering behavior.

Equivalence criterion:

- none in this phase.  Passing row is diagnostic-only.

Vetoes:

- nonfinite ODE/state/value;
- theta outside P30 parameter box;
- unmatched comparison budgets;
- nonlinear preconditioning usefulness, paper-scale, or candidate-vs-CUT4
  equivalence claims.

Artifact:

- `tests/highdim/test_p30_cut4_statistical_comparators.py`.

Non-claims:

- no CUT4-as-ground-truth claim;
- no candidate-vs-CUT4 statistical-equivalence claim;
- no nonlinear preconditioning usefulness claim;
- no matched linear/nonlinear comparison success claim;
- no paper-scale predator-prey result;
- no adaptive MATLAB behavior claim;
- no high-dimensional scalability claim;
- no GPU/HMC/DSGE readiness claim;
- no stable public API or end-to-end score API claim.
