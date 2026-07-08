# Experiment plan: exact-transformed-sv-fixed-sgqf-broader-precursor-ladder

metadata_date: 2026-06-26
program_id: exact-transformed-sv-fixed-sgqf-broader-precursor-ladder
status: DRAFT_READY_FOR_EXECUTION
master_context:
- `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-source-scope-sgqf-unlocks-reset-memo-2026-06-24.md`
- `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-precursor-result-2026-06-26.md`

## Question
Does the current
`exact_transformed_sv_independent_panel_fixed_sgqf_filter(...)` route remain a
numerically controlled **same-target, independent-panel, value-only precursor**
when we broaden beyond the single current tiny fixture to a small nearby ladder
of exact-transformed SV cases?

What decision will this inform?
- whether the precursor evidence should remain “single tiny fixture only”,
- or whether it is strong enough to support a slightly broader internal
  exact-transformed precursor ladder before the program pivots back to the
  augmented-noise-first source-scope unlock path.

## Mechanism being tested
The mechanism is the existing internal exact-transformed SV SGQF wrapper in
`bayesfilter/highdim/sv_mixture_cut4.py`:
- `exact_transformed_sv_independent_panel_fixed_sgqf_filter(...)`

This plan does **not** test a generic non-Gaussian SGQF core. It tests whether
that specific independent-panel wrapper continues to match the same-target dense
exact-transformed reference under a modest ladder expansion:
- nearby parameter settings,
- slightly longer horizons,
- sparse-level sensitivity on the same target.

## Scope
- Variant: broader precursor ladder for the internal exact-transformed SV SGQF
  wrapper
- Objective: broaden same-target value-only evidence without changing target
  identity or claiming analytical score support
- Seed(s): deterministic in-repo fixtures only
- Training steps: N/A
- HMC/MCMC settings: none
- XLA/JIT mode: none required
- Expected runtime: focused CPU-only test pass under a few minutes

Planned ladder axes:
1. **Parameter-neighborhood ladder**
   - retain dims `1, 2, 3`
   - add a small set of nearby `(gamma, beta, sigma)` fixtures around the current
     p41 values
2. **Horizon ladder**
   - retain the current short horizon
   - add one slightly longer exact-transformed horizon that still permits the
     same-target dense reference on CPU
3. **Sparse-level ladder**
   - compare `sparse_level in {1, 2, 3}` as explanatory evidence only
   - do not make monotone refinement a promotion criterion unless the behavior is
     clearly stable across the tested cases

## Baseline / comparator
Primary same-target comparator:
- `highdim.exact_transformed_sv_independent_panel_dense_reference(...)`

Secondary explanatory comparator:
- the already recorded single-fixture precursor result in
  `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-precursor-result-2026-06-26.md`

What is explicitly **not** a comparator for promotion in this plan:
- KSC Gaussian-mixture surrogate routes,
- UKF or CUT4 approximation routes,
- source-scope runner/leaderboard emission,
- generic `tf_fixed_sgqf_filter(...)` non-Gaussian support.

## Evidence contract
Scientific / engineering question:
- Is the existing internal exact-transformed SGQF wrapper stable enough across a
  small nearby ladder to justify calling it a broader internal precursor rather
  than a one-fixture curiosity?

Exact baseline:
- same-target dense exact-transformed SV reference on each tested ladder point

Primary promotion criterion:
- across the tested ladder, SGQF remains finite and within declared dense
  reference tolerances for:
  - total log-likelihood,
  - per-time log normalizers,
  - filtered mean path,
  - filtered covariance path.

Diagnostics that can veto:
- non-finite outputs,
- dense-reference disagreement beyond declared thresholds,
- covariance structure inconsistent with the independent-panel design,
- instability that appears only when the horizon is modestly extended,
- behavior suggesting the current single-fixture tolerances were accidental.

Diagnostics that are explanatory only:
- how gaps change with sparse level,
- whether level 2 or level 3 improves a given case,
- runtime or point-count observations.

What will not be concluded even if the ladder passes:
- no analytical-score admission,
- no generic non-Gaussian SGQF core support,
- no source-faithful Zhao-Cui source-row admission,
- no generalized-SV or spatial-SIR unlock,
- no HMC or production-readiness claim.

Artifact that will preserve the result:
- a result note under `docs/plans/` tied to this plan,
- plus focused regression coverage in `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`.

## Success criteria
Primary:
- Each ladder case returns finite SGQF and dense-reference values.
- The worst-case gaps across the ladder stay within declared tolerances, or any
  necessary tolerance widening is small, justified by measured behavior, and
  recorded explicitly.
- The route remains clearly independent-panel and value-only in diagnostics and
  non-claims.

Secondary:
- The current single-fixture result remains reproducible under the expanded test
  file.
- The ladder reveals whether the current evidence is robust enough to justify a
  broader internal precursor label.

Sanity checks:
- no silent fallthrough to KSC surrogate code paths,
- non-scalar cloud rejection remains enforced,
- dim-1 wrapper bookkeeping remains consistent with scalar dense reference,
- diagonal covariance structure remains preserved on the factorized fixture.

## Diagnostics
Primary:
- max absolute SGQF-vs-dense `log_likelihood` gap across the ladder
- max absolute SGQF-vs-dense per-step `log_normalizers` gap across the ladder
- max absolute SGQF-vs-dense `mean_path` gap across the ladder
- max absolute SGQF-vs-dense diagonal `covariance_path` gap across the ladder
- max off-diagonal covariance leakage across the ladder

Secondary:
- sparse-level sensitivity on representative cases
- whether the longer-horizon case degrades materially relative to the current
  two-step fixture

Sanity checks:
- public export status remains unchanged unless explicitly reviewed later
- exact-transformed route diagnostics retain narrow non-claims

## Expected failure modes
- The current agreement may deteriorate quickly once the horizon is extended by a
  few steps.
- Nearby parameter settings may expose a sensitivity hidden by the original
  fixture.
- Sparse-level behavior may be non-monotone, making a simple “higher level is
  better” story invalid.
- A broader ladder may show that the current precursor should stay classified as
  a single-fixture result only.

## Pre-mortem
How the run could pass while misleading us:
- The added ladder points might still be too close to the original fixture,
  giving a false sense of breadth.
- Loose tolerances could let the broader ladder pass without demonstrating real
  robustness.

How the run could fail for implementation/tuning rather than scientific reasons:
- The dense reference might become numerically heavy on a slightly longer
  horizon, making the comparison look worse for computational rather than
  algorithmic reasons.
- A sparse-level choice that is too small for one ladder point could make the
  wrapper look weaker than it is.

Cheap diagnostic to distinguish those explanations:
- inspect whether failures cluster only at one sparse level or only at the
  longer horizon while the shorter nearby-parameter cases remain stable.

## Skeptical audit execution note
Audit pass recorded before execution on 2026-06-26.

Why the audit passes:
- the baseline remains the same-target dense exact-transformed reference for
  every ladder point;
- the proposed ladder is still small enough to stay in the “focused diagnostic”
  regime rather than silently becoming a benchmark ladder used for row
  promotion;
- the plan does not use runtime, sparse-level improvement, or any approximation
  comparator as a promotion oracle;
- the plan preserves explicit stop conditions: if the broadened ladder fails,
  the claim ceiling stays at the current single-fixture precursor result rather
  than broadening scope by narration.

Execution note:
- proceed with deterministic CPU-only ladder probes first;
- tighten or widen tolerances only from measured same-target gaps, and record
  any widening explicitly in the result note.

## What would change our mind
- If the broader ladder passes cleanly, we can upgrade the wording from
  “single tiny fixture precursor” to “small internal precursor ladder” while
  still keeping the route value-only and internal.
- If the ladder shows large or unstable gaps, keep the current narrower result as
  the correct ceiling and do not broaden the claim.
- If the longer horizon is the only failure point, treat that as a boundary of
  current evidence rather than as evidence for generic non-Gaussian SGQF failure.

## Files likely to modify
Primary tests:
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`

Possible supporting artifact:
- `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-broader-precursor-ladder-result-2026-06-26.md`

No implementation-file changes are planned in the first pass.
In particular, this plan does **not** require edits to:
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `bayesfilter/highdim/__init__.py`

## Execution order
1. Add deterministic nearby-parameter fixtures and one slightly longer-horizon
   exact-transformed case to the p41 ladder test file.
2. Add explanatory sparse-level checks for representative cases.
3. Run focused CPU-only compile and pytest checks.
4. Record the observed worst-case gaps and decide whether the precursor claim can
   be broadened or must stay at the current single-fixture boundary.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m compileall -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py -k "fixed_sgqf or exact_transformed"
```

## Interpretation rule
- If the broader ladder remains finite and within reasonable same-target dense
  tolerances, then record a broader **internal value-only precursor ladder**
  result and keep the route internal.
- If only the original current fixture passes cleanly, retain the existing
  single-fixture precursor result as the honest ceiling.
- If the broader ladder fails materially, do not interpret that as failure of the
  whole SGQF family program; interpret it as a limit of this specific exact-
  transformed precursor wrapper and pivot back to the augmented-noise-first path.
