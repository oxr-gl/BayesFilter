# P70 Phase 6h Result: Root-Cause Probes For Residual And Conditioning Failures

metadata_date: 2026-06-17
status: PHASE6H_EXECUTED_CLAUDE_AGREE_PHASE7_BLOCKED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-subplan-2026-06-17.md
json_artifact: docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-2026-06-17.json

## Evidence Contract

Question: which mechanism best explains the row-A holdout/replay residual
explosion and row-B condition veto: support/effective-support mismatch,
off-cloud TT growth, normalized-metric amplification, hidden design
conditioning, or target/shift/frame mismatch?

Baseline/comparator: saved Phase 6f/6g failed evidence and unchanged P70 row
definitions.  Phase 6h is diagnostic only.

Primary criterion: produce a finite JSON artifact and classify every declared
hypothesis using the predeclared signatures, without changing thresholds,
fitting policy, row specs, or Phase 6 gate outcomes.

Nonclaims: no repair, no fixed-variant success, no d18 correctness, no
rank/degree promotion, no scaling claim, no HMC readiness, no adaptive
Zhao--Cui parity, and no source-faithfulness closure.

## Run Manifest

Before running the diagnostic, Codex revised only the Phase 6h diagnostic
script to bring it into line with the already-reviewed subplan: median
nearest-neighbor summaries are used for the predeclared support rule; the
leave-one-out diagonal is formed without a `0 * inf` artifact; row-B
last/failing systems are reconstructed by locally replaying core updates; and
both target-RMS and density-normalizer residual scales are preserved.  No
production algorithm files were changed during Phase 6h.

Command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6h_root_cause_probes.py --output docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-2026-06-17.json
```

The command exited `0` and wrote
`docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-2026-06-17.json`.
This was a deliberate CPU-only run with `CUDA_VISIBLE_DEVICES=-1`.
TensorFlow printed CUDA plugin/cuInit startup messages, but no GPU run was
intended or used for the artifact.

Local checks:

- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p70_phase6h_root_cause_probes.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6h_root_cause_probes.py --output ...`: exited `0`.
- `python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-2026-06-17.json`: passed.
- `git diff --check -- scripts/p70_phase6h_root_cause_probes.py docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-subplan-2026-06-17.md`: passed.

## Result Table

| Hypothesis | Classification | Evidence |
| --- | --- | --- |
| H2/H6 support or effective-support mismatch | unresolved | Step 1 has fit leave-one-out median `0.0`, so the predeclared median-ratio test degenerates.  Diagnostic nearest-neighbor medians are large (`3.588` holdout, `3.532` replay) and clipping is near but below the `0.25` threshold (`0.230`, `0.242`).  Step 2 ratios and clipping do not meet the support threshold. |
| H4 off-cloud square-root TT growth | supported | Line probes grow by orders of magnitude.  Step 1 farthest holdout line reaches `2.053e10`; step 2 farthest line reaches `8.987e7`.  These exceed `1e6` times fit-target RMS in the predeclared rule. |
| H7 normalized-metric amplification | weakened | The raw holdout/replay residuals are already enormous relative to fit-target RMS: step 1 holdout `1.678e10`, replay `4.827e11`; step 2 holdout `4.000e8`, replay `8.299e6`.  The failure is not explained by a small denominator alone. |
| H8/H3 design conditioning | supported | Row B replay reconstructs the condition veto with last accepted scaled condition `1.040e13` and failing scaled condition `1.305e14 > 1e14`; both have unscaled normal condition `inf` and effective-rank ratio `0.889`.  Row A sampled-core audits do not show a condition warning, so the support is mainly for row B. |
| H5 target/shift/frame mismatch | weakened | Recomputed frame hashes match saved hashes.  Diagnostic shift constants match manifests.  Target min/max summaries match manifests.  Fit-side shift matching is not directly testable from the manifest because the fit manifest does not store a shift constant; this absence is recorded rather than treated as positive shift-match evidence. |

## Main Interpretation

The strongest row-A explanation is off-cloud evaluator growth: the fitted
degree-1, rank-2 square-root TT has small fit residuals but grows explosively
along deterministic line segments from fit points toward holdout points.  The
row-A problem is therefore not merely a reporting scale artifact.  Support
mismatch remains plausible, but the predeclared support rule cannot cleanly
classify it because the step-1 fit cloud contains duplicate points and the fit
leave-one-out median is zero.

The row-B problem is a real conditioning failure in the fixed ALS system.  The
diagnostic replay reconstructs last-accepted and failing systems with singular
spectra.  The failing scaled augmented matrix has singular-value minimum
`1.925e-14`, singular-value maximum `2.512`, scaled condition `1.305e14`, and
unscaled normal condition `inf`.

Phase 7 remains blocked.  The next justified phase is a Phase 6i repair-design
subplan that targets off-cloud growth and rank-3 conditioning without changing
claims or validation scope.
