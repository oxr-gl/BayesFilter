# P70 Phase 6h Subplan: Root-Cause Probes For Residual And Conditioning Failures

metadata_date: 2026-06-17
status: DRAFT_FOR_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run a bounded diagnostic to discriminate the remaining Phase 6 failures:

- `rank_candidate_1_2_fit36` has tiny fit residuals but huge holdout/replay
  normalized residuals;
- `rank_stronger_1_3_fit36` hits a scaled augmented condition-number veto.

Phase 6h will test support/generalization, weight/effective-support,
off-cloud evaluator growth, target/shift/frame consistency, and design
conditioning hypotheses.  It will not repair the algorithm, loosen gates,
rerun the full four-row Phase 6 diagnostic, or advance Phase 7.

## Entry Conditions Inherited From Phase 6g

Phase 6h may begin only after:

- Phase 6g result exists and Claude accepted it with `VERDICT: AGREE`;
- Phase 6g fixed only reporting/schema and did not claim fixed-variant success;
- saved Phase 6f/6g evidence still fails by the true blockers:
  first-row holdout/replay residual veto and second-row condition veto;
- Phase 7 remains blocked.

## Hypotheses Under Test

| ID | Hypothesis | Expected Evidence If True |
| --- | --- | --- |
| H2/H6 | Fit and diagnostic clouds differ in support or effective weighted support. | Holdout/replay have large nearest-neighbor distances to fit points, high clipping/saturation, or very small effective support under fit weights. |
| H4 | Fitted square-root TT grows explosively off the selected fit cloud. | Prediction quantiles/maxima or line probes from fit points toward diagnostic points blow up before reaching diagnostic points. |
| H7 | Normalized residuals are amplified by target-scale choice. | Raw residuals are large but normalized values are additionally inflated by a small denominator; this explains scale only, not pass/fail. |
| H8/H3 | Design conditioning is already weak in row A and fatal in row B. | Row A singular spectra/effective ranks are marginal; row B spectra show near-null directions and condition growth before the veto. |
| H5 | Target/shift/frame bookkeeping mismatch contributes to residuals. | Diagnostic target hashes or recomputed target summaries conflict with the declared reused frame/shift route. |

The result is inconclusive, not successful, if any hypothesis lacks the
required measurements needed for classification.

## Required Artifacts

- this Phase 6h subplan;
- diagnostic script:
  `scripts/p70_phase6h_root_cause_probes.py`;
- optional focused tests if script helpers are nontrivial;
- JSON diagnostic output:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-2026-06-17.json`;
- result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-result-2026-06-17.md`;
- updates to the P70 execution and Claude review ledgers.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which mechanism best explains the row-A residual explosion and row-B condition veto: support/effective-support mismatch, off-cloud TT growth, normalized-metric amplification, hidden design conditioning, or target/shift/frame mismatch? |
| Baseline/comparator | Saved Phase 6f/6g failed evidence and unchanged P70 row definitions. |
| Primary criterion | Produce a finite JSON artifact and a hypothesis classification table that marks every declared hypothesis `supported`, `weakened`, or `unresolved` using the predeclared signatures below, without changing thresholds, fitting policy, row specs, or Phase 6 gate outcomes. |
| Veto diagnostics | Any repair/tuning, threshold change, row/rank/degree/ridge/sweep/initializer/model change, full Phase 6 diagnostic rerun, Phase 7 command, fixed-variant success claim, or source-faithfulness closure. |
| Explanatory only | Nearest-neighbor distances, clipping fractions, ESS/effective support, raw prediction quantiles, line-probe growth, singular spectra, effective ranks, residual decompositions. |
| Not concluded | No algorithmic fix, no fixed-variant success, no d18 correctness, no rank/degree promotion, no scaling claim, no HMC readiness, no adaptive Zhao--Cui parity, no author-code failure claim. |
| Artifact preserving result | Phase 6h JSON and result note. |

## Required Diagnostic Contents

The Phase 6h JSON must include:

- run manifest with command, git state, CPU-only status, and nonclaims;
- row-A support audit for each time step:
  nearest-neighbor distances from holdout/replay points to fit points,
  clipping/saturation summaries, fit/holdout/replay target and weight
  summaries, coordinate-frame/shift hashes;
- row-A raw output audit:
  fit/holdout/replay target summaries, prediction summaries, raw residuals,
  normalized residuals, and normalizer summaries;
- row-A line-stability probe:
  values along short line segments from selected fit points toward diagnostic
  points, with maximum absolute prediction and growth ratios;
- row-A design-conditioning audit:
  singular spectra/effective rank/condition summaries for exact core indices
  `0`, `target_dim // 2`, and `target_dim - 1` at the initial row-A state and
  the final fitted row-A state for each time step;
- row-B conditioning audit:
  accepted condition trajectory before veto, failing update details, scale
  spread, unscaled condition, and singular/effective-rank summaries for the
  last accepted and failing design systems.  If those systems cannot be
  reconstructed without running the full Phase 6 wrapper or changing production
  code, Phase 6h must stop as a blocker.

Line-stability bounds:

- select at most three deterministic fit/diagnostic pairs per time step:
  nearest, median-distance, and farthest holdout point relative to the fit cloud;
- evaluate at fixed fractions `(0.0, 0.25, 0.5, 0.75, 1.0)` only;
- use holdout points only for the line probe, with replay reserved for raw
  output and support summaries;
- do not adaptively add more pairs or fractions after seeing output.

Predeclared hypothesis signatures:

- H2/H6 supported if holdout/replay nearest-neighbor distances or clipping
  fractions are large by the following fixed rules: median diagnostic-to-fit
  nearest-neighbor distance is at least `2.0` times median fit leave-one-out
  nearest-neighbor distance, or diagnostic clipping fraction is at least `0.25`,
  or effective support size is less than `0.5 * n_fit`.  Weakened if all three
  tests fail for both holdout and replay.
- H4 supported if raw predictions or line-probe values grow by orders of
  magnitude away from fit points before or at diagnostic endpoints: maximum
  absolute holdout/replay prediction or line-probe prediction is at least
  `1e6` times the fit-target RMS, or at least `1e6` times the maximum absolute
  fit prediction.  Weakened if both ratios are below `1e3` for holdout, replay,
  and line probes.
- H7 supported only as an explanatory amplifier if raw residuals are moderate
  but normalized residuals become huge due to a small target-scale denominator:
  raw residual is below `100 * fit_target_rms` while normalized residual exceeds
  the frozen veto `10`.  Weakened if raw residual is at least
  `1e6 * fit_target_rms`.
- H8/H3 supported if singular spectra show near-null directions, very small
  effective rank, condition growth near veto, or row-A marginal conditioning:
  any audited condition number exceeds the warning threshold `1e10`, any
  effective-rank ratio is below `0.5`, or row-B last/failing systems reproduce
  a condition above `1e14` or an infinite unscaled normal condition.  Weakened
  only if all audited systems have condition below `1e8` and effective-rank
  ratio at least `0.75`.
- H5 supported if recomputed target/frame/shift hashes or summaries mismatch
  the saved route: coordinate-frame hash mismatch, shift mismatch above
  `1e-10`, or recomputed target summary relative difference above `1e-8`.
  Weakened if all hashes match and all scalar summaries are within those
  tolerances.

## Required Checks And Reviews

Before execution:

- skeptical plan audit recorded here;
- Claude read-only review of this subplan;
- syntax check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p70_phase6h_root_cause_probes.py
```

Execution command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6h_root_cause_probes.py --output docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-2026-06-17.json
```

After execution:

```bash
git diff --check -- scripts/p70_phase6h_root_cause_probes.py docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-subplan-2026-06-17.md
```

Then write the result note and ask Claude for read-only execution/result review.

## Forbidden Claims And Actions

- Do not rerun `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py`.
- Do not run Phase 7.
- Do not change thresholds or row definitions.
- Do not modify `bayesfilter/highdim/fitting.py` or
  `bayesfilter/highdim/source_route.py` during Phase 6h.
- Do not claim the fixed variant works.
- Do not treat any explanatory metric as promotion evidence.

## Stop Conditions

Stop and write a blocker if:

- Claude rejects the subplan for a material evidence-contract problem that
  cannot be patched locally;
- the diagnostic would require changing production code or thresholds;
- the diagnostic cannot reconstruct row-A or row-B inputs without rerunning the
  full Phase 6 wrapper;
- the JSON is nonfinite or missing required sections;
- the output contradicts saved Phase 6f/6g gate outcomes.

## Next-Phase Handoff Conditions

Phase 6h may close only after:

- the diagnostic JSON is written;
- result note classifies every declared hypothesis as supported, weakened, or
  unresolved using the predeclared signatures;
- Claude execution review returns `VERDICT: AGREE`, or a blocker is recorded.

The next phase, if Phase 6h succeeds, must be a new Phase 6i repair-design
subplan.  Phase 7 remains blocked.

## Skeptical Plan Audit

This plan uses failed Phase 6f/6g evidence as the baseline.  It does not treat
new local diagnostics as pass/fail promotion criteria.  The probes are designed
to separate mechanisms before repair: support mismatch, off-cloud growth,
metric amplification, hidden conditioning, and target/shift/frame mismatch.
No tuning, threshold movement, or Phase 7 action is authorized.
