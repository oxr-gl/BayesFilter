# P70 Phase 2 Result: Current-Code Gap Audit

metadata_date: 2026-06-16
status: PHASE2_PASSED_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Scope

Phase 2 audits the current BayesFilter code against the Phase 1 fixed-branch
contract.  It is read-only with respect to algorithmic code and p50.  The
question is:

> Which current code surfaces already implement the fixed-branch objects and
> predicates, which are partial, and which are missing before a UKF-guided
> branch-builder design can be written?

The answer is: the current code has source-route localization, fixed-rank TT
fitting infrastructure, square-root-density normalizer accounting, UKF scout
metadata, and post-fit holdout/replay diagnostics.  It does not yet have the
P70 UKF-guided branch builder, does not pass UKF scout information into the
source-route fit construction, and still realizes the P59/P69 fixed source
route through constant-path initialization and one forward ALS sweep.

## Skeptical Audit

The Phase 2 plan survived the pre-run skeptical audit.

| Risk checked | Phase 2 disposition |
| --- | --- |
| Wrong baseline | Baseline is the current P59/P69 constant-path one-sweep fixed-TTSIRT route, not an adaptive Zhao--Cui run. |
| Proxy metric promoted to gate | Fit residual, holdout residual, replay residual, UKF summaries, and low/high deltas are treated only as diagnostics. |
| Missing stop condition | Phase 2 stops if a code surface cannot be inspected, if code anchors are ambiguous, or if Phase 3 would require implementation evidence. |
| Unfair comparison | No repaired diagnostic or ladder is run, so no comparison result is promoted. |
| Hidden assumption | The UKF remains scout evidence only; it is not an oracle for rank, domain, correctness, or HMC readiness. |
| Environment mismatch | No GPU, HMC, network, or long-running diagnostic command is required. |
| Artifact mismatch | The required artifact is a code-gap ledger and a Phase 3 subplan, not a repair. |

The dirty worktree is broad and includes unrelated code, document, and result
artifacts.  Phase 2 treats those as existing user/other-lane state and changes
only P70 plan/result/ledger artifacts.

## Source And Claim Boundary

The following classifications govern this audit.

| Operation | Phase 2 classification | Anchors | Consequence |
| --- | --- | --- | --- |
| Zhao--Cui adjacent-state TT square-root density, squared-density nonnegativity, marginalization, KR maps, and normalizer spine | `source_faithful` at the mathematical route level | P18 claim ledger lines 22--32; P16 equation ledger lines 35--63; P18 source ledger line 20 | May support the mathematical route, but not a claim that the current fixed branch reproduces the adaptive implementation. |
| Author SIR benchmark source route: pushed samples, weighted localization, resampling, TTSIRT construction, and log-normalizer update | author-source anchored; fixed BayesFilter implementation remains a fixed adaptation | `eg3_sir/mainscript.m:14-17`, `:39-56`; `models/full_sol.m:21-43`, `:46-124`; `models/computeL.m:24-47` | Supports the current source-route ancestry.  It does not supply a UKF-guided branch builder. |
| BayesFilter fixed branch with frozen samples, deterministic resampling, fixed ranks, fixed basis, fixed sweep schedule, and replayable manifests | `fixed_hmc_adaptation` | `source_route.py:2361-2488`, `source_route.py:3190-3303`, `fitting.py:573-608` | May be designed for differentiable/HMC use, but cannot be called adaptive Zhao--Cui parity. |
| UKF-guided branch construction | not `source_faithful`; P70 design target | `ukf_scout.py:13-22`, `rank_budget.py:328-365`; Phase 1 contract lines 31 and 135--142 | Phase 3 must keep this as scout-guided fixed adaptation or explicitly quarantine any stronger extension claim. |

## Gap Ledger: Branch Objects

| Phase 1 object | Current code surface | Status | Gap for P70 |
| --- | --- | --- | --- |
| \(\mu_t\) | `SourceRouteCoordinateFrame.mu` stores a finite center, and `source_route_recenter` computes it as a weighted empirical mean (`source_route.py:211-256`, `source_route.py:6589-6661`).  The P59 source-fit builder calls this on pushed weighted samples (`source_route.py:2396-2409`). | partial | Present for the empirical source route.  Missing a UKF-guided rule \(G_t\) that freezes \(\mu_t\) from UKF scout output or from a documented UKF/source hybrid. |
| \(L_t\) | `SourceRouteCoordinateFrame.matrix` stores a nonsingular affine matrix (`source_route.py:215-247`).  `source_route_recenter` forms a weighted covariance, Cholesky factor, optional quantile stretch, and expansion factor (`source_route.py:6633-6656`). | partial | Present for author-style weighted localization.  Missing a UKF-guided covariance-orientation and scale policy, eigenvalue/jitter policy, and manifest fields tying \(L_t\) to the scout. |
| \(\Omega_t\) | The P59/P69 fixed-TTSIRT route constructs a product Legendre basis on `BoundedInterval(-1.0, 1.0)` (`source_route.py:3205-3211`; also `source_route.py:2057-2064`). | partial | The local cube exists as an implementation convention, but the branch identity does not yet expose a P70 domain policy derived from UKF scale bounds. |
| \(\mathcal D_t\) | `_p59_author_sir_source_fit_data_for_step` returns `local_fit_points` and `fit_weights=tf.ones([n])` after deterministic weighted resampling (`source_route.py:2410-2422`, `source_route.py:2479-2488`). | partial | Present as source-route fit rows.  Missing a UKF-guided design-measure rule or a declared hybrid rule that separates scout guidance from empirical source-route rows. |
| \(c_t\) | The fit-data builder sets `shift = tf.reduce_min(local_negative_log)` and records it as `shift_constant` (`source_route.py:2442-2448`, `source_route.py:2482-2486`).  Diagnostic data reuse the fitted shift (`source_route.py:2491-2619`). | present-for-current-route | Present for the current route.  Phase 3 must decide whether \(c_t\) remains the fit-row minimum or is frozen by another predeclared branch rule. |
| \(B_t\) branch identity | `FixedTTFitter` records ranks, ridge, sweep order, max sweeps, initial-core hash, initialization rule, update records, fitted cores, and nonclaims in a `BranchManifest` (`fitting.py:573-608`).  Density identity and source-route step manifests carry hashes (`source_route.py:3253-3270`, `source_route.py:2996-3045`). | partial | Current branch identity records the realized fixed fit, but not UKF scout inputs, branch-builder thresholds, channel-activity predicates, or the Phase 3 \(G_t\) rule. |

## Gap Ledger: Initialization, Sweeps, And Channels

| Required surface | Current code surface | Status | Gap for P70 |
| --- | --- | --- | --- |
| Nondegenerate initialization | `_source_route_constant_path_initial_cores` sets only entry `[0,0,0]` in every core (`source_route.py:3606-3628`).  P59/P69 callers pass this as the supplied initial cores (`source_route.py:2078-2095`, `source_route.py:3231-3248`). | gap | This guarantees a positive constant path, but it does not give declared higher-rank channels an initial nonzero path.  Phase 4 must design an initialization with a mathematical opportunity for declared channels to activate. |
| Multi-sweep fitting mechanism | `FixedTTFitter.fit` supports configurable `max_sweeps` and `sweep_order` (`fitting.py:25-79`, `fitting.py:223-260`). | present-in-fitter | The source-route P59/P69 callers hard-code `max_sweeps=1` and forward coordinate order (`source_route.py:2065-2077`, `source_route.py:3212-3224`). |
| One-sweep current source route | `_p59_fixed_ttsirt_transport_from_values` constructs `FixedTTFitConfig(... max_sweeps=1, sweep_order=tuple(range(target_dim)))` (`source_route.py:3212-3224`). | present-current-baseline | This is the baseline to repair, not the P70 target. |
| Channel-activity predicates | The P69 diagnostic script defines rank-channel summaries and extra-channel activity measurements (`scripts/p69_phase5c_rank_activity_degree_normalizer_diagnostic.py:149-234`). | diagnostic-only | No integrated fitter/source-route predicate currently gates a branch on declared-channel activity.  Phase 4 must define such predicates before Phase 6 observes repaired diagnostics. |
| Gauge-aware channel interpretation | Current diagnostics inspect literal core-channel norms in the P69 script. | missing | Phase 4 must decide whether literal channel norms are enough under the chosen initialization/gauge, or whether an additional gauge-aware diagnostic is needed. |
| Degree/rank policy for fixed route | `fit_degree` and `fit_rank` are passed into current source-route helpers and recorded in manifests (`source_route.py:3033-3038`). | partial | No current policy prevents in-sample residual improvement from being promoted despite normalizer/holdout/replay instability.  Phase 4/6 must freeze structural and normalizer predicates first. |

## Gap Ledger: Normalizer, Holdout, Replay

| Predicate or diagnostic | Current code surface | Status | Gap for P70 |
| --- | --- | --- | --- |
| Fixed shifted normalizer \(\log \zeta_t^B-c_t\) | `SourceRouteNormalizerContribution.log_increment()` computes `log_transport_normalizer - shift_constant` (`source_route.py:293-327`), and `source_route_log_normalizer_update` wraps that rule (`source_route.py:6703-6715`). | present | This supports the Phase 1 scalar convention, but it does not by itself prove a stable fitted branch. |
| Squared-density normalizer decomposition | `_p64_normalizer_terms_by_step` records square-root, defensive, mixture, log-transport, shift, and increment terms when a squared density is available (`source_route.py:4307-4350`). | diagnostic-present | P69 found degree-normalizer sensitivity.  Phase 6 must use predeclared finite/bounded thresholds before observing repaired output. |
| Fitter-internal holdout residual | `FixedTTFitSampleBatch` accepts holdout tensors and `FixedTTFitter.fit` can veto nonfinite or too-large holdout residuals (`fitting.py:82-124`, `fitting.py:277-291`). | present-in-fitter | `_p59_fixed_ttsirt_transport_from_values` does not pass holdout tensors into `FixedTTFitSampleBatch`; P69 deliberately uses post-fit diagnostics instead (`source_route.py:3236-3248`). |
| Post-fit holdout/replay diagnostics | `_p69_post_fit_holdout_replay_diagnostics` and `_p69_post_fit_diagnostic_channel` compute diagnostic residuals and record nonclaims (`source_route.py:3306-3429`, `source_route.py:3432-3507`). | diagnostic-only | The diagnostics preserve branch identity but are not correctness, validation, or Phase 6 pass criteria unless thresholds are declared before the run. |
| Fit-quality diagnostics | `_p59_fixed_ttsirt_fit_quality_diagnostics` records residuals, update statuses, condition-number summaries, and nonclaims (`source_route.py:3538-3586`). | diagnostic-only | Fit residual and condition numbers are explanatory.  They cannot replace rank-channel and normalizer predicates. |
| Historical low/high deltas | Older adjacent-ladder code reports normalizer-increment deltas and threshold exceedances (`source_route.py:4162-4186`). | historical-diagnostic | P70 must not require low and high branches to be close.  For this model they may legitimately differ; the repaired gate should ask whether the repaired branch is structurally active and numerically bounded under predeclared predicates. |

## Existing Tests And Scripts

| Surface | Existing coverage | Phase 2 conclusion |
| --- | --- | --- |
| Generic `FixedTTFitter` behavior | `tests/highdim/test_fixed_branch_fit.py` covers configurable sweeps, rank changes, deterministic branch hashes, and holdout veto behavior. | Useful for Phase 5 focused tests, but not proof that the P59/P69 source-route helper uses those features. |
| UKF scout nonclaims | `tests/highdim/test_p52_ukf_scout.py` checks scout claim class and nonclaims. | Confirms scout-only boundary.  Does not implement branch construction. |
| P69 rank/normalizer diagnostic | `scripts/p69_phase5c_rank_activity_degree_normalizer_diagnostic.py` and result artifacts record rank-channel collapse and degree-normalizer sensitivity. | Historical evidence only.  Phase 2 did not rerun the diagnostic. |
| Public exports | `bayesfilter/highdim/__init__.py` exports `FixedTTFitConfig`, `FixedTTFitter`, `UKFScoutConfig`, and `UKFScoutResult` (`__init__.py:51-55`, `__init__.py:337-342`, `__init__.py:568-569`). | Phase 5 can use public surfaces, but Phase 3 should design before implementation. |

## Surfaces Phase 3 May Design Against

Phase 3 may design against these existing surfaces:

- UKF scout outputs and nonclaims: `bayesfilter/highdim/ukf_scout.py:13-22`,
  `ukf_scout.py:49-87`, `ukf_scout.py:87-130`.
- UKF rank-policy guardrails: `bayesfilter/highdim/rank_budget.py:328-365`.
- Affine coordinate-frame type and manifest payload:
  `bayesfilter/highdim/source_route.py:211-256`.
- Empirical source-route localization helper:
  `bayesfilter/highdim/source_route.py:6589-6661`.
- P59/P69 fit-data route for pushed samples, local points, weights, and shifts:
  `bayesfilter/highdim/source_route.py:2361-2488`.
- Post-fit diagnostic data construction that reuses a fitted frame and shift:
  `bayesfilter/highdim/source_route.py:2491-2619`.
- Current fixed-TTSIRT transport helper:
  `bayesfilter/highdim/source_route.py:3190-3303`.
- Fixed TT fitter configuration, sweep loop, branch manifest, and diagnostics:
  `bayesfilter/highdim/fitting.py:25-79`, `fitting.py:223-291`,
  `fitting.py:573-646`.
- Normalizer accounting and decompositions:
  `bayesfilter/highdim/source_route.py:293-327`,
  `source_route.py:4307-4350`, `source_route.py:6703-6715`.

## Surfaces Phase 3 Must Not Touch

Phase 3 is a design phase.  It must not edit or execute:

- `bayesfilter/highdim/source_route.py`;
- `bayesfilter/highdim/fitting.py`;
- `bayesfilter/highdim/ukf_scout.py`;
- `bayesfilter/highdim/rank_budget.py`;
- p50 LaTeX or generated PDFs;
- `scripts/p69_phase5c_rank_activity_degree_normalizer_diagnostic.py`;
- tests that run repaired diagnostics or ladder comparisons.

Design notes may name these files as future implementation surfaces, but no
implementation change belongs to Phase 3.

## Phase 3 Handoff

Phase 3 may start after Claude agrees with this Phase 2 result and the Phase 3
subplan.  The exact entry products are:

- gap ledger for \(\mu_t,L_t,\Omega_t,\mathcal D_t,c_t\);
- gap ledger for nondegenerate initialization, sweep policy, and
  channel-activity predicates;
- gap ledger for normalizer, holdout, and replay predicates;
- exact surfaces Phase 3 may design against;
- exact surfaces Phase 3 must not touch;
- refreshed Phase 3 design subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase3-ukf-guided-branch-builder-design-subplan-2026-06-16.md`.

Claude returned `VERDICT: AGREE` for this result and the refreshed Phase 3
subplan.  The only residual review notes were presentation-level: Phase 3
should repeat direct Zhao--Cui paper section/equation anchors inline where it
uses `source_faithful`, and Phase 3 local `rg` checks are smoke checks rather
than proof of design adequacy.

## Not Concluded

- No repaired branch was implemented.
- No p50 prose was edited.
- No P69 Phase 5c diagnostic or repaired diagnostic was run.
- No rank, degree, normalizer, holdout, or replay threshold was chosen after
  seeing repaired output.
- No UKF correctness, rank truth, d18 validation, scaling, HMC readiness,
  adaptive Zhao--Cui parity, or author-code failure claim is made.
