# P38-C2 Subplan: Spatial SIR CUT4 Feasibility Diagnostic

metadata_date: 2026-06-06
phase: P38-C2

Question: can a clean-room BayesFilter additive-Gaussian closure inspired by
the P30 spatial SIR model contract be evaluated by CUT4 on a small diagnostic
row, and can the result be recorded without claiming native SIR or
candidate-filter equivalence?

Comparator:

- `tf_svd_cut4_filter` on a clean-room structural SIR-inspired
  additive-Gaussian closure model.

Audit design:

- small `J=1` row with state `(S_1, I_1)` and additive process noise;
- one or two fixed observations from the clean-room SIR fixture;
- CUT4 point count capped by augmented dimension 4;
- no highdim candidate equivalence because current BayesFilter SIR evidence is
  first-gate model-contract evidence only;
- traceability status is `BAYESFILTER_EXTENSION`, not source-matched native
  Zhao--Cui/MATLAB SIR filtering behavior.

Equivalence criterion:

- none in this phase.  Passing row is diagnostic-only: finite CUT4 value,
  residual diagnostics, and explicit non-claims.

Vetoes:

- nonfinite CUT4 value;
- silent negative-population clipping;
- point-count cap exceeded;
- claiming TT/SIRT SIR filtering, paper-scale `J=9`, or candidate-vs-CUT4
  equivalence.

Artifact:

- `tests/highdim/test_p30_cut4_statistical_comparators.py`.

Non-claims:

- no CUT4-as-ground-truth claim;
- no candidate-vs-CUT4 statistical-equivalence claim;
- no production TT/SIRT SIR filtering claim;
- no paper-scale `J=9` accuracy or scalability claim;
- no adaptive MATLAB behavior claim;
- no GPU/HMC/DSGE readiness claim;
- no stable public API or end-to-end score API claim.
