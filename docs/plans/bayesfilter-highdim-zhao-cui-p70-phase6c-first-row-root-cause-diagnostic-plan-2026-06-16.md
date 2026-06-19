# P70 Phase 6c Plan: First-Row Condition-Veto Root-Cause Diagnostic

metadata_date: 2026-06-16
status: DRAFT_PENDING_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 6c
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Identify the most likely root cause of the first-row
`HighDimStatus.CONDITION_NUMBER_VETO` observed in Phase 6 for
`rank_candidate_1_2_fit36`, without changing the fixed branch, thresholds,
row count, rank, degree, ridge, sweep order, initializer, or source-route
semantics.

Phase 6c is a microscope on the already-failed row.  It is not a repaired
four-row Phase 6 rerun and cannot unblock Phase 7.

## Entry Conditions Inherited From Phase 6b

Phase 6c may begin only because Phase 6b produced:

- `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6b-condition-veto-capture-repair-result-2026-06-16.md`;
- focused tests showing failed fixed-TTSIRT fits are captured as failed
  diagnostic payloads rather than treated as admissible transports;
- Claude `VERDICT: AGREE` on the Phase 6b execution review;
- the standing prohibition on rerunning the four-row Phase 6 diagnostic without
  a new reviewed subplan and explicit user approval.

## Hypotheses To Test

Let \(x_j\in[-1,1]^D\) denote the local fit row after affine recentering,
deterministic resampling, and clipping.  For core \(k\), the ALS design has
entries
\[
  A_k[j,(a,\ell,b)]
  =
  L_{j,k-1,a}\,\psi_{k,\ell}(x_{j,k})\,R_{j,k+1,b},
\]
and the fitted normal equation is
\[
  N_k = A_k^\top W A_k + \rho I,\qquad d_k=A_k^\top W y,
  \quad \rho=10^{-10}.
\]
The veto fires if \(\kappa(N_k)>10^{14}\).

The diagnostic will test:

1. Coordinate-frame fragility: the weighted covariance used to build the local
   frame is nearly singular or jitter-dominated at \(n_{\rm fit}=D=36\).
2. Effective-row collapse: deterministic resampling produces many duplicate
   source samples or very low effective sample size before fitting.
3. Clipping/saturation: many coordinates hit \(\pm1\), making degree-1
   Legendre columns nearly collinear or binary with too little variation.
4. Initial-core channel imbalance: the seeded extra channels, with
   \(\epsilon=10^{-6}\), create TT environments whose columns differ by many
   orders of magnitude.
5. Normal-equation amplification: \(N=A^\top W A+\rho I\) squares the
   condition of \(A\), and an absolute ridge \(\rho=10^{-10}\) is too small
   relative to the design scale.
6. Raw row adequacy is not the whole issue: \(36\) rows can exceed the local
   core column count for degree \(1\), rank \(2\), yet still be numerically
   rank-deficient after resampling, clipping, and environment scaling.
7. Implementation smell: `_p59_fixed_ttsirt_transport_from_values(..., ridge=...)`
   currently constructs `FixedTTFitConfig(ridge=P70_FIT_RIDGE)` instead of using
   the supplied `ridge` argument.  Phase 6c records this but does not repair it.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Why does the first P70 repaired fixed branch, `rank_candidate_1_2_fit36`, hit a condition-number veto before any Phase 6 row can complete? |
| Baseline/comparator | The Phase 6 first-row failure with degree \(1\), rank \(2\), \(n_{\rm fit}=36\), seeded-channel initialization, canonical repeated sweep order, ridge \(10^{-10}\), and condition veto \(10^{14}\). |
| Primary criterion | Produce a JSON and result note that rank the candidate root causes using directly measured first-row quantities: frame spectrum, ESS/resampling duplicates, clipping/saturation, local-point rank, target scale, initial-core/channel scales, per-core design singular values, actual normal-equation condition numbers, and the captured failing fit status. |
| Veto diagnostics | Any run that modifies thresholds, row/rank/degree/ridge/sweep/initializer policy, emits a transport from a failed fit, runs the four-row Phase 6 diagnostic, treats explanatory probes as repairs, or claims Phase 7 readiness. |
| Explanatory-only diagnostics | Column-normalized design condition numbers; trace-scaled ridge condition numbers; hypothetical ridge/normalization summaries; target residual scales; raw design singular values.  These may suggest a later repair plan but are not pass criteria and do not change the fitted branch. |
| Not concluded | No fixed-variant repair, no Phase 6 pass, no validation, no rank/degree promotion, no scaling claim, no HMC readiness, no adaptive Zhao--Cui parity, no source-faithfulness closure for seeded initialization. |
| Artifact preserving result | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-2026-06-16.json` and `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-result-2026-06-16.md`. |

## Required Artifacts

- Diagnostic plan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-plan-2026-06-16.md`.
- Diagnostic script:
  `scripts/p70_phase6c_first_row_root_cause_diagnostic.py`.
- JSON diagnostic:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-2026-06-16.json`.
- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-result-2026-06-16.md`.
- Updated P70 visible execution ledger.
- Updated P70 Claude review ledger.

## Exact Diagnostic Scope

The diagnostic command is:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6c_first_row_root_cause_diagnostic.py
```

The script must reconstruct only:

- label: `rank_candidate_1_2_fit36`;
- time index: `1`;
- degree: `1`;
- rank: `2`;
- fit sample count: `36`;
- model simulation seed: `5901`;
- source fit-data construction used by `_p59_author_sir_source_fit_data_for_step`;
- the same seeded-channel initial cores and `FixedTTFitConfig` constants used by
  `_p59_fixed_ttsirt_transport_from_values`.

The script must not call the P70 Phase 6 four-row wrapper.  It may call the
fitter directly on the first-row data and must preserve the failed status.

## Required Measurements

The JSON diagnostic must include:

- run manifest: command, git state, CPU-only environment, seeds, elapsed time;
- row identity and fixed policy constants;
- source-data manifest fields already produced by the fit-data helper;
- weighted ESS from the push, resampling duplicate count, unique resampled row
  count, and max duplicate multiplicity;
- local coordinate-frame singular values, condition number, log determinant,
  and a lower-bound diagnostic showing whether the frame is jitter-dominated;
- local unclipped and clipped point summaries, including clip fraction,
  per-axis boundary counts, all-clipped row/axis indicators, and local design
  row rank;
- target-value scale summary;
- initial-core norm and channel-scale diagnostics, including extra-channel to
  constant-channel scale ratios where defined;
- for every core in the first sweep order, the design matrix shape, singular
  values, numerical rank under a fixed relative tolerance, column norms,
  column-norm spread, \(\kappa(A)\), actual \(\kappa(A^\top W A+\rho I)\), and
  status against the existing warning/veto thresholds;
- explanatory-only condition numbers after column normalization and after a
  trace-scaled ridge, clearly marked as non-branch probes;
- captured `P70FixedFitDiagnosticError` payload from the actual helper or an
  equivalent direct `FixedTTFitter` call showing where the first veto occurs.

## Required Checks/Tests/Reviews

Before running the diagnostic:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p70_phase6c_first_row_root_cause_diagnostic.py
```

If focused tests are added:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p70_phase6c_root_cause_diagnostic_script.py
```

After the diagnostic and result note:

```bash
git diff --check -- scripts/p70_phase6c_first_row_root_cause_diagnostic.py docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-plan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-result-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-claude-review-ledger-2026-06-16.md
```

Claude plan review must check that Phase 6c:

- is not a four-row Phase 6 rerun;
- cannot unblock Phase 7;
- distinguishes actual-branch diagnostics from explanatory what-if probes;
- has enough measurements to rank the hypotheses above;
- preserves the failed-fit semantics and source-anchor boundary.

Claude execution review must check:

- the diagnostic followed the plan;
- measured evidence supports the root-cause ranking;
- nonclaims are preserved;
- any proposed next action is a new plan, not an unapproved repair.

## Forbidden Claims/Actions

- Do not run `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py`.
- Do not run a P69/P70 four-row diagnostic.
- Do not change threshold, row, rank, degree, ridge, sweep, initializer, or
  model policy.
- Do not treat column-normalization or trace-scaled ridge probes as successful
  repairs.
- Do not emit or accept a transport from a failed fit.
- Do not proceed to Phase 7.
- Do not claim source-faithfulness for seeded-channel initialization beyond
  already documented fixed-HMC adaptation scope.

## Exact Next-Phase Handoff Conditions

Phase 6c closes only after:

- local compile/check commands pass or failures are recorded;
- the one-row diagnostic artifact exists;
- the result note ranks root-cause hypotheses and separates evidence from
  speculation;
- Claude reviews the execution/result;
- the visible execution ledger and Claude review ledger are updated.

The only possible next phases are:

- a focused implementation-repair plan if the root cause is an implementation
  bug or missing scale normalization;
- a mathematical/design revision plan if the fixed-variant method itself needs
  a different stable ALS formulation;
- a blocker handoff if the evidence remains ambiguous.

No next phase may run a repaired four-row diagnostic without a new reviewed
subplan and explicit user approval.

## Stop Conditions

Stop and write a blocker if:

- the first-row data cannot be reconstructed without running the four-row
  diagnostic;
- the direct diagnostic would need to change the branch policy to observe the
  failure;
- the diagnostic cannot serialize its JSON artifact;
- Claude and Codex do not converge after five material review rounds;
- the output is too ambiguous to rank root causes without a further plan.

## Skeptical Plan Audit

This plan does not use a proxy metric as a promotion criterion.  It answers a
root-cause question about one known failed row.  The actual fitted branch and
its condition veto remain binding.  Column normalization and scaled-ridge
calculations are explicitly explanatory-only; they can motivate a later repair
plan but cannot make the current failed branch admissible.  The plan avoids the
wrong baseline risk by comparing all measurements against the exact Phase 6
first-row settings rather than against the P69 diagnostic or an easier toy row.
