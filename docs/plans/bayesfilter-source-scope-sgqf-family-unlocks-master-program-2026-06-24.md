# Master Program: Source-Scope SGQF Family Unlocks And Analytical-Gradient Gates

metadata_date: 2026-06-24
program_id: source-scope-sgqf-family-unlocks
status: DRAFT_PENDING_IMPLEMENTATION

## Purpose

This master program governs the next family-level expansion of SGQF across the
high-dimensional / source-scope leaderboard after the first two-lane reference
packets were emitted.

Its job is to coordinate the row-by-row SGQF unlock work under one durable
program rather than leaving the remaining blocked families as separate untracked
plans.

The target rows are:
- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
- `zhao_cui_spatial_sir_austria_j9_T20`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

The program also adds the missing **analytical-gradient / analytical-score gate**
for any unlocked SGQF family, because the current family-unlock plans are mostly
value-first and do not yet unify when a row becomes:
- value-only,
- analytical-score admitted,
- diagnostic-score only,
- or still blocked.

## Why one master program is the right move

Yes — these plans should be governed under a single master program.

Reason:
- they touch overlapping benchmark runners, row-contract tests, and leaderboard
  artifacts,
- they need one consistent admission ledger for SGQF across all source-scope
  rows,
- and the analytical-gradient evidence bar must be applied consistently across
  families rather than being reinvented per row.

Without a master program, the repo risks:
- inconsistent row states across artifacts,
- unlocking value rows without a consistent score policy,
- and stale blocked/admitted language drifting between plans.

## Governing artifacts

### Existing leaderboard / lane governance
- `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-two-lane-filter-comparison-p7-closeout-and-leaderboard-result-2026-06-24.md`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.json`

### Family-specific unlock plans already written
- `docs/plans/bayesfilter-generalized-sv-source-scope-sgqf-unlock-plan-2026-06-24.md`
- `docs/plans/bayesfilter-actual-transformed-sv-source-scope-sgqf-unlock-plan-2026-06-24.md`
- `docs/plans/bayesfilter-spatial-sir-source-scope-sgqf-unlock-plan-2026-06-24.md`

### Existing SGQF analytical-gradient governance examples
- `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md`
- `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-result-2026-06-23.md`
- `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md`
- `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-result-2026-06-23.md`

## Core policy

1. **Value unlock and analytical-score unlock are separate gates.**
   A family may become SGQF value-executed before it becomes an analytical-score
   family.

2. **No target substitution.**
   Actual transformed SV, KSC surrogate SV, generalized SV, and spatial SIR must
   each keep their own target identity. A surrogate or approximation route cannot
   unlock a different row by renaming.

3. **Analytical-score claims require explicit reviewed derivative routes.**
   Autodiff remains diagnostic-only unless a reviewed family-specific exception is
   written explicitly.

4. **Blocked rows must remain explicit.**
   If a family lacks a same-target SGQF route, or lacks an analytical-score
   route, it must remain blocked/status-only rather than silently omitted.

## Why the analytical-gradient tests are missing today

The current source-scope family unlock plans are value-first because that is the
smallest honest unlock target for most of the blocked rows.

This is why analytical-gradient tests are missing in those family plans:
- KSC source-scope T1000 is only clearly ready for SGQF value promotion today,
  while source-scope score promotion still needs its own reviewed gate.
- Actual transformed SV and generalized SV do not yet even have the same-target
  SGQF **value** evaluator unlocked, so score promotion would be premature.
- Spatial SIR is still blocked at the route/value stage, so an analytical-score
  gate would be upstream of a missing value route.

So the gap is not accidental; it reflects the current unlock order. But now that
multiple family plans exist, the repo needs one explicit analytical-gradient
master gate so the score policy is coherent.

## Program structure

### P0 — unified SGQF source-scope admission ledger
Purpose:
- write one row-by-row SGQF admission ledger for all source-scope families,
  including separate columns for:
  - value status,
  - score status,
  - blocker reason,
  - target identity,
  - current implementation entry points.

### P1 — KSC surrogate T1000 evaluator promotion
Purpose:
- promote SGQF value execution on the source-scope KSC surrogate row through the
  runner and leaderboard path.

### P2 — actual transformed SV augmented-noise SGQF precursor route
Purpose:
- build an augmented-noise SGQF execution path for the actual transformed SV
  family as the first engineering unlock,
- while keeping the source-scope actual-transformed row blocked for same-target
  admission until a later reviewed promotion gate passes.

### P3 — generalized SV augmented-noise SGQF precursor route
Purpose:
- build an augmented-noise SGQF execution path for the generalized-SV source
  family as the first engineering unlock,
- while keeping the source-scope generalized-SV row blocked for same-target
  admission until a later reviewed promotion gate passes.

### P4 — same-target admission gate for augmented-noise precursor rows
Purpose:
- decide, family by family, whether any augmented-noise SGQF precursor route can
  be promoted beyond engineering/diagnostic status,
- or whether the row must remain blocked at the source-scope admission level.

### P5 — spatial SIR route-development gate
Purpose:
- classify whether the source-scope spatial SIR row can move beyond route-value
  blocking, or remains blocked pending factorized/streamed transition work.

### P6 — analytical-gradient / analytical-score family gate
Purpose:
- add one explicit family-by-family analytical-gradient gate after the value
  routes exist.
- classify each source-scope SGQF row as one of:
  - `value_only_executed`
  - `analytical_score_admitted`
  - `diagnostic_score_only`
  - `blocked_missing_analytical_route`

### P7 — runner / leaderboard integration
Purpose:
- re-emit the source-scope runner and highdim leaderboard so all family states are
  consistent with the unified ledger.

### P8 — documentation phase for augmented-noise SGQF on non-Gaussian models
Purpose:
- fully document the augmented-noise SGQF idea for non-Gaussian models in the
  manuscript,
- place the discussion in the most appropriate high-dimensional SGQF chapter,
- and make the relationship between precursor routes and same-target admission
  explicit.

### P9 — `docs/main.tex` compile / integration check
Purpose:
- compile the manuscript after the new SGQF documentation lands,
- verify that `docs/main.tex` includes the updated chapter set cleanly,
- and treat a successful compile as a required program-level verification gate.

### P10 — closeout and next-step packet
Purpose:
- summarize which SGQF families are now value-executed,
- which are analytical-score-admitted,
- which remain blocked,
- what the documentation now claims,
- and what the next justified action is.

## Analytical-gradient unblock plan needed under this program

Yes — we should create a separate plan under `docs/plans` for the analytical-
gradient / analytical-score gate itself.

Reason:
- the family unlock plans currently solve “can SGQF value run on this row?”
- they do not yet solve “what evidence is required before SGQF score claims are
  allowed on this row?”

That analytical-gradient plan should:
- inventory existing SGQF analytical-score support by family,
- identify where only autodiff/finite-difference diagnostics exist,
- define the promotion rule for source-scope score claims,
- and set the verification matrix for family-specific score admission.

## Expected files to modify across the program

Core implementation:
- `bayesfilter/highdim/sv_mixture_cut4.py`
- `bayesfilter/highdim/native_generalized_sv.py`
- `bayesfilter/highdim/transition_route.py`
- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/rank_budget.py`

Runner / leaderboard:
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- `docs/main.tex`
- relevant highdim SGQF documentation chapter(s) under `docs/chapters/`

Contracts / tests:
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p47_generalized_sv_equality.py`
- `tests/highdim/test_p47_predator_prey_filtering.py`
- `tests/highdim/test_p51_native_generalized_sv_reference.py`
- `tests/highdim/test_p51_spatial_sir_route_preflight.py`
- `tests/highdim/test_p52_factorized_transition_route.py`
- `tests/highdim/test_p53_lower_rung_streaming_route.py`

## Skeptical plan audit

Wrong-baseline risk:
- Avoid treating “some SGQF code exists” as equivalent to “same-target source-
  scope value and score routes are admitted.”

Proxy-promotion risk:
- Avoid letting value execution silently become score admission.

Hidden-assumption risk:
- KSC tiny-fixture score support does not automatically imply source-scope T1000
  analytical-score admission.

Artifact-answer mismatch risk:
- Family unlocks and score-policy changes must be reflected in the runner,
  leaderboard, and contract tests together.

Audit verdict:
- proceed under one master program with a separate analytical-gradient gate plan.
