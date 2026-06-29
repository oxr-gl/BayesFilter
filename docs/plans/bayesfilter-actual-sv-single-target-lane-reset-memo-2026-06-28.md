# Reset memo: actual-sv-single-target-lane-reset

## Date
2026-06-28

## Context
The recent actual-SV work introduced a Lane A / Lane B comparison and then used
that framing to build documentation, code wrappers, tests, and benchmark
artifacts.  That work was useful diagnostically, but the framing drifted away
from the target the user intended.

The user clarified the governing rule repeatedly:
- there is **one** likelihood function for this problem,
- both Lane A and Lane B must approximate that **same**
  \(\log p(y_{1:T}\mid\theta)\),
- Zhao--Cui is a same-target comparator regardless of lane,
- an augmented-noise method should not introduce a different surrogate scalar or
  require the KSC mixture approximation when the goal is the actual-SV
  likelihood.

That means the current so-called Lane B Gaussian-closure route is not merely a
weaker approximation.  It is a misdefined target for the intended inference
problem.

## Decision / policy
Future sessions should assume the following unless a newer reviewed artifact
supersedes it:

1. **There is one likelihood target.**
   For actual SV, Lane A, Lane B, and Zhao--Cui are allowed to differ only in how
   they approximate the same cumulative log likelihood
   \(\ell_T(\theta)=\log p(y_{1:T}\mid\theta)\).

2. **The current Gaussian-closure Lane B is invalid as an inference lane.**
   The current augmented-noise Gaussian-closure implementation computes a
   different scalar from the Lane-A exact-target route.  It must not be treated
   as a co-equal same-target likelihood approximation for MLE/HMC.

3. **Zhao--Cui is same-target, not lane-owned.**
   Zhao--Cui is conceptually applicable to both Lane A and Lane B because it is a
   same-target comparator, not because it belongs to one lane's numerical
   mechanism.

4. **Current Lane-B artifacts become diagnostic / negative evidence.**
   The recent dense/SGQF/UKF Lane-B comparison remains useful only as evidence
   that the Gaussian-closure definition drifted away from the single-target
   actual-SV likelihood.

5. **Restart from a corrected single-target plan.**
   The next correct task is to define Lane B as an augmented-noise route to the
   same actual likelihood as Lane A, not as a separate Gaussian-closure scalar.

## What changed
The recent work produced the following useful but now reclassified artifacts:

- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex`
- `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
- `docs/chapters/ch28_nonlinear_ssm_validation.tex`
- `docs/chapters/ch18b_structural_deterministic_dynamics.tex`
  - These chapter edits currently encode a lane split that should be reread with
    the single-target correction in mind.  They may need revision in the next
    pass.

- `bayesfilter/highdim/sv_mixture_cut4.py`
  - Added current Lane-A wrappers and current Lane-B Gaussian-closure wrappers.
  - The Lane-A pieces remain useful.
  - The current Lane-B Gaussian-closure pieces should now be treated as
    diagnostic-only scaffolding, not target-correct inference lanes.

- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/test_actual_sv_two_lane_benchmark_script.py`
  - These tests remain useful, but the Lane-B assertions should be interpreted as
    validating the current diagnostic scalar, not the intended final actual-SV
    target.

- `docs/benchmarks/benchmark_actual_sv_two_lane_comparison.py`
- `docs/benchmarks/actual_sv_two_lane_comparison_2026-06-27.json`
- `docs/benchmarks/actual_sv_two_lane_comparison_2026-06-27.md`
- `docs/plans/bayesfilter-actual-sv-two-lane-value-gradient-comparison-plan-2026-06-27.md`
- `docs/plans/bayesfilter-actual-sv-two-lane-value-gradient-comparison-result-2026-06-27.md`
  - These are now diagnostic artifacts showing that the current Lane-B
    Gaussian-closure route is numerically different from the same-target Lane-A
    route and should not be promoted as the intended inference target.

## Bugs / blockers resolved
- Resolved the ambiguity about whether there are multiple target likelihoods.
  There are not.
- Resolved the question of whether Zhao--Cui belongs only to Lane A.  It does
  not; it is a same-target comparator.
- Resolved the interpretation of the large Lane-A / Lane-B dense-reference gap:
  it is evidence of target mismatch, not acceptable lane variation.

## Verification already run
The following targeted checks passed for the current diagnostic implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_actual_sv_two_lane_benchmark_script.py
```

Observed:
- the current Lane-A and current diagnostic Lane-B wrappers execute,
- the benchmark script emits reproducible artifacts,
- but those passing tests do **not** certify that current Lane B targets the
  intended single actual-SV likelihood.

## Current policy
- Treat Lane A as the current same-target truth-anchor route.
- Treat the current Gaussian-closure Lane B as diagnostic-only scaffolding.
- Do not use the current Lane-B dense / SGQF / UKF comparisons as evidence about
  the intended actual-SV likelihood target.
- Restart from the corrected single-target plan before further inference-facing
  interpretation.

## Known limitations / cautions
- Some of the recent documentation now uses Lane A / Lane B language that may
  need tightening or partial rollback.
- The current benchmark script is still useful, but only as a reproducible record
  of the diagnostic mismatch.
- The current Lane-B SGQF > UKF finding is only evidence about the current
  Gaussian-closure surrogate scalar, not about a corrected same-target Lane-B
  route.

## Suggested next steps
1. Start a fresh session from this reset memo and the corrected single-target
   plan:
   - `docs/plans/bayesfilter-actual-sv-single-target-lane-correction-plan-2026-06-28.md`
2. Re-derive Lane B under the rule that it must approximate the same actual-SV
   likelihood function as Lane A.
3. Reclassify Zhao--Cui explicitly as a same-target comparator for both lanes.
4. Only after that derivation should Lane B be reimplemented and rebenchmarked.
