# P38-C4 Subplan: CUT4 Stress-Row Feasibility Guard

metadata_date: 2026-06-06
phase: P38-C4

Question: can CUT4 feasibility be recorded for small stress rows without
promoting stress diagnostics into correctness or scalability claims?

Comparator:

- CUT4 point-count/resource feasibility, not truth.

Audit design:

- declare augmented dimension, point count `2d+2^d`, wall-time/resource
  interpretation, and one-axis stress boundary;
- first gate uses only small rows already exercised by C0, C2, and C3;
- no paper-model reproduction or scalability promotion.

Equivalence criterion:

- none unless a row also has a same-model candidate and comparator from C0.

Vetoes:

- missing point-count cap;
- interpreting stress feasibility as correctness;
- GPU/HMC/DSGE/scalability overclaim;
- simultaneous unplanned axis changes.

Artifact:

- manifest tests in `tests/highdim/test_p30_cut4_statistical_comparators.py`.

Non-claims:

- no CUT4-as-ground-truth claim;
- no candidate-vs-CUT4 statistical-equivalence claim unless the row also
  passes a dedicated equivalence gate;
- no paper-model reproduction claim;
- no correctness claim from stress feasibility;
- no production scalability claim;
- no GPU/HMC/DSGE readiness claim;
- no stable public API or end-to-end score API claim.
