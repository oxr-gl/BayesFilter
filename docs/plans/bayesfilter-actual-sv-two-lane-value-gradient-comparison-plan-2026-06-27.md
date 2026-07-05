# Experiment plan: actual-sv-two-lane-value-gradient-comparison

metadata_date: 2026-06-27
program_id: actual-sv-two-lane-value-gradient-comparison
status: DRAFT_READY_FOR_EXECUTION
master_context:
- `docs/plans/bayesfilter-actual-transformed-sv-sgqf-value-semantics-bug-fix-plan-2026-06-26.md`
- `docs/plans/bayesfilter-actual-transformed-sv-sgqf-planning-error-reset-memo-2026-06-26.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json`

## Question
Across actual-SV and related benchmark rows, how do direct likelihood quadrature
(Lane A) and augmented-noise Gaussian closure (Lane B) compare in value and
gradient approximation quality?

What decision will this experiment inform?
- whether Lane B provides a competitive approximate-likelihood lane relative to
  the exact-target Lane-A baseline;
- whether Lane-B UKF or Lane-B SGQF is the stronger Gaussian-closure actual-SV
  approximation on tiny deterministic fixtures;
- whether either lane is numerically stable enough to support later MLE/HMC work
  under the declared same-scalar contract.

## Mechanism being tested
This experiment compares two distinct cumulative log-likelihood constructions for
actual SV:

- **Lane A**: same-target direct likelihood quadrature on the exact-transformed
  actual-SV target;
- **Lane B**: augmented-noise Gaussian-closure approximate likelihood accumulated
  over time.

The comparison isolates both value approximation and gradient approximation.
Lane-local comparisons are same-scalar comparisons. Cross-lane comparisons are
approximation-gap evidence only.

## Scope
- Variant: actual-SV two-lane value/gradient comparison
- Objective: compare Lane-A and Lane-B approximation behavior without mixing
  their scalar semantics
- Seed(s): deterministic tiny fixtures only in the first pass
- Training steps: N/A
- HMC/MCMC settings: none
- XLA/JIT mode: eager-only diagnostic path
- Expected runtime: compile/tests and tiny comparisons under several minutes

Out of scope:
- production HMC admission,
- generalized-SV promotion,
- KSC surrogate-to-actual transfer claims,
- shared-core SGQF genericization.

## Baseline / comparator
### Lane A same-target comparators
- `highdim.exact_transformed_sv_independent_panel_dense_reference(...)`
- `highdim.exact_transformed_sv_independent_panel_fixed_sgqf_filter(...)`
- `highdim.exact_transformed_sv_independent_panel_fixed_sgqf_score(...)`
- `highdim.exact_transformed_sv_independent_panel_zhaocui_tt_filter(...)`
- `highdim.exact_transformed_sv_independent_panel_zhaocui_tt_score(...)`

### Lane B same-scalar comparators
- `highdim.actual_transformed_sv_independent_panel_augmented_noise_dense_gaussian_closure_reference(...)`
- `highdim.actual_transformed_sv_independent_panel_augmented_noise_fixed_sgqf_filter(...)`
- `highdim.actual_transformed_sv_independent_panel_augmented_noise_fixed_sgqf_score(...)`
- `highdim.actual_transformed_sv_independent_panel_augmented_noise_ukf_filter(...)`
- `highdim.actual_transformed_sv_independent_panel_augmented_noise_ukf_score(...)`

### Cross-lane comparators
- Lane-B dense reference versus Lane-A dense exact-target reference
- Lane-B score versus Lane-A score only as approximation-gap evidence

### Separate surrogate family
- existing KSC transformed-SV rows remain separate and are explanatory only.

## Success criteria
Primary:
- Lane-A SGQF and TT scores match Lane-A finite-difference or dense references
  at planned tiny-fixture tolerances;
- Lane-B SGQF and Lane-B UKF scores match centered finite differences of their
  own declared Lane-B scalar at planned tiny-fixture tolerances;
- Lane-B dense reference, Lane-B SGQF, and Lane-B UKF all remain finite and
  branch-valid on the tiny deterministic fixtures.

Secondary:
- the documentation, code diagnostics, and tests use the same Lane-A / Lane-B
  names and do not claim cross-lane same-target equality;
- existing KSC and exact-transformed tests remain interpretable.

Sanity checks:
- KSC surrogate rows stay separate from actual-SV rows;
- Lane-B diagnostics explicitly say it is not direct actual-SV likelihood
  quadrature;
- cross-lane differences are nonzero on at least one row, confirming the lanes
  are not accidentally collapsing to the same scalar.

## Diagnostics
Primary:
- within-lane log-likelihood gap,
- within-lane per-step log-normalizer gap,
- within-lane gradient finite-difference gap,
- branch-validity / finite-value / finite-gradient status.

Secondary:
- Lane-B UKF vs Lane-B SGQF value gap,
- Lane-B UKF vs Lane-B SGQF score gap,
- Lane-B versus Lane-A value/score gap,
- point-count diagnostics for SGQF/UKF.

Sanity checks:
- off-diagonal covariance drift on diagonal panel fixtures,
- nonzero cross-lane gap,
- no mislabeling of Lane-B as same-target actual-SV evidence.

## Expected failure modes
- Lane-B augmented-noise Gaussian closure may be too crude for some actual-SV
  rows and show larger gaps than expected;
- Lane-B SGQF or UKF score paths may expose derivative-contract bugs around the
  augmented-noise state;
- Lane-A GradientTape score may be slower or more fragile than analytical score
  wrappers on larger fixtures;
- dense Lane-B reference may need smaller order/radius than expected for stable
  tiny-fixture diagnostics.

## What would change our mind
- If Lane-B dense/UKF/SGQF comparisons are unstable or branch-invalid even on the
  tiny fixture, stop and treat Lane B as blocked for now.
- If Lane-B gradients are stable and significantly closer to their dense Lane-B
  reference than Lane-A approximations are to Lane-A references on relevant rows,
  that is evidence for Lane-B usefulness as an approximate-likelihood lane.
- If Lane A remains clearly better against the exact-target reference while Lane B
  is only smoother, keep Lane A as the truth-anchor lane and document Lane B as a
  separate engineering approximation.

## Skeptical audit
Wrong-baseline risk:
- do not judge Lane B only against Lane A; Lane B has its own dense same-scalar
  reference in this plan.

Proxy-promotion risk:
- smoother gradients or easier optimization do not prove closer agreement to the
  exact actual-SV likelihood.

Artifact-answer mismatch risk:
- any result note that reports Lane-B success as same-target actual-SV admission
  fails this plan.

Audit verdict:
- proceed with lane-local comparisons first, then cross-lane approximation-gap
  reporting only.

## Files likely to modify
Primary implementation:
- `bayesfilter/highdim/sv_mixture_cut4.py`

Primary tests:
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`

Primary documentation:
- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex`
- `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
- `docs/chapters/ch28_nonlinear_ssm_validation.tex`
- `docs/chapters/ch18b_structural_deterministic_dynamics.tex`

Likely result artifact:
- `docs/plans/bayesfilter-actual-sv-two-lane-value-gradient-comparison-result-2026-06-27.md`

## Execution order
1. Compile the modified modules and tests.
2. Run targeted p41 ladder tests for Lane-A and Lane-B value behavior.
3. Run targeted p43 value/gradient tests for Lane-A, Lane-B, and KSC separation.
4. Record within-lane value and gradient evidence.
5. Record cross-lane approximation gaps as explanatory-only evidence.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m compileall -q \
  bayesfilter/highdim/sv_mixture_cut4.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

## Interpretation rule
- If Lane-A and Lane-B within-lane checks both pass, report both as working
  declared scalars and compare them only through explicit approximation gaps.
- If Lane A passes but Lane B fails, keep Lane B blocked and preserve Lane A as
  the exact-target truth anchor.
- If Lane B passes but is materially different from Lane A, report that as
  expected semantic separation rather than a bug by itself.
- If both lanes fail branch-validity or finite-gradient checks, stop and record
  the specific blocker before broader model comparisons.
