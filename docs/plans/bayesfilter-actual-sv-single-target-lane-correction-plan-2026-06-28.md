# Experiment plan: actual-sv-single-target-lane-correction

metadata_date: 2026-06-28
program_id: actual-sv-single-target-lane-correction
status: DRAFT_READY_FOR_EXECUTION
master_context:
- `docs/plans/bayesfilter-actual-sv-single-target-lane-reset-memo-2026-06-28.md`
- `docs/plans/bayesfilter-actual-transformed-sv-sgqf-value-semantics-bug-fix-plan-2026-06-26.md`
- `docs/plans/bayesfilter-actual-sv-two-lane-value-gradient-comparison-result-2026-06-27.md`

## Question
How should BayesFilter redefine and implement Lane B so that Lane A, Lane B, and
Zhao--Cui are all approximating the **same** actual-SV cumulative log likelihood
\(\log p(y_{1:T}\mid\theta)\)?

What decision will this experiment inform?
- whether an augmented-noise route can be made same-target for actual SV;
- whether the corrected Lane B is numerically distinct but same-target, or
  effectively equivalent to Lane A at the tested scales;
- whether the current Gaussian-closure Lane-B scaffolding should be deleted,
  retained only as a diagnostic, or repurposed under a corrected same-target
  derivation.

## Mechanism being tested
The corrected mechanism is a **single-target** actual-SV likelihood comparison.

- **Lane A** remains a same-target direct likelihood quadrature route.
- **Lane B** must be redefined as an augmented-noise route to that same
  likelihood, not as a Gaussian-closure surrogate scalar.
- **Zhao--Cui** remains a same-target comparator independent of lane labels.

The key mechanism under review is therefore not “which surrogate scalar is
better,” but “whether two different numerical approximations to one common
likelihood target agree.”

## Scope
- Variant: actual-SV single-target lane correction
- Objective: replace the current multi-scalar lane framing with a same-target
  actual-SV comparison
- Seed(s): deterministic tiny fixtures first
- Training steps: N/A
- HMC/MCMC settings: none
- XLA/JIT mode: eager-only diagnostic path first
- Expected runtime: focused compile/tests and small numerical comparisons under a
  few minutes initially

Out of scope:
- production HMC admission,
- generalized-SV promotion,
- KSC surrogate-to-actual transfer,
- large-model benchmarking before the same-target derivation is settled.

## Baseline / comparator
### Common target
- `\ell_T(\theta)=\log p(y_{1:T}\mid\theta)` for actual SV

### Same-target comparators
- Lane-A dense exact-transformed actual-SV reference
- Lane-A SGQF direct-likelihood route
- corrected Lane-B augmented-noise same-target route
- Zhao--Cui TT actual-SV route

### Diagnostic-only comparators
- the current Gaussian-closure Lane-B artifacts remain diagnostic-only and should
  not be promoted as same-target evidence in this plan.

## Success criteria
Primary:
- write down one common actual-SV likelihood target that Lane A, Lane B, and
  Zhao--Cui are all meant to approximate;
- identify exactly where the current Lane-B Gaussian-closure route deviates from
  that target;
- implement or sketch the smallest corrected Lane-B route that preserves the same
  likelihood target;
- verify on tiny deterministic fixtures that Lane A, corrected Lane B, and
  Zhao--Cui can be compared as same-target value and gradient approximations.

Secondary:
- reduce or eliminate the current dense-reference mismatch that arose from using a
  different scalar in Lane B;
- preserve target-language discipline in docs, tests, and benchmark artifacts.

Sanity checks:
- Zhao--Cui is treated as same-target for both lanes;
- KSC rows remain separate surrogate evidence;
- any remaining differences are numerical approximation gaps, not scalar-identity
  mismatches.

## Diagnostics
Primary:
- same-target value gap against a single dense actual-SV reference,
- same-target gradient gap against that same reference,
- branch-validity / finite-value / finite-gradient checks.

Secondary:
- whether corrected Lane B materially differs from Lane A after restoring the
  common target,
- whether the corrected Lane B reduces to a numerically similar route to Lane A,
- implementation complexity of preserving same-target semantics under
  augmentation.

Sanity checks:
- nonzero KSC-vs-actual gap remains expected,
- cross-lane value/gradient differences shrink to same-target approximation-scale
  behavior rather than multi-scalar behavior.

## Expected failure modes
- the augmented-noise route may, once forced onto the same target, collapse to a
  route that is numerically almost identical to Lane A and therefore not justify a
  separate lane label;
- the current augmented-noise wrapper machinery may be too entangled with
  Gaussian-closure assumptions and need partial replacement rather than patching;
- Zhao--Cui may require explicit target-language updates in artifacts even if its
  implementation is already same-target.

## What would change our mind
- If the corrected derivation shows that augmented-noise and direct quadrature are
  mathematically the same value computation under the current setup, then Lane B
  should be demoted from a distinct lane to an implementation variant.
- If a corrected augmented-noise route can be made same-target and still gives a
  numerically distinct approximation, keep it as a legitimate alternative lane.
- If no corrected same-target augmented-noise route is cleanly implementable,
  drop the current Lane-B inference framing and retain only Lane A plus Zhao--Cui.

## Skeptical audit
Wrong-baseline risk:
- do not preserve the current Lane-B dense Gaussian-closure reference as if it
  were a same-target baseline.

Proxy-promotion risk:
- self-consistent gradients of the wrong scalar do not count as evidence about the
  correct likelihood target.

Artifact-answer mismatch risk:
- any result that continues to compare different scalars as if they were same-
  target fails this plan.

Audit verdict:
- restart from the single-target derivation before any further interpretation of
  Lane B as an inference route.

## Files likely to modify
Primary documentation:
- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex`
- `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
- `docs/chapters/ch28_nonlinear_ssm_validation.tex`
- `docs/chapters/ch18b_structural_deterministic_dynamics.tex`

Primary implementation candidates:
- `bayesfilter/highdim/sv_mixture_cut4.py`
- possibly `bayesfilter/nonlinear/fixed_sgqf_tf.py` only if a same-target
  augmented-noise route really needs shared-core support

Primary tests/artifacts:
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `docs/benchmarks/benchmark_actual_sv_two_lane_comparison.py`

Likely result artifact:
- `docs/plans/bayesfilter-actual-sv-single-target-lane-correction-result-2026-06-28.md`

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m compileall -q \
  bayesfilter/highdim/sv_mixture_cut4.py \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

## Interpretation rule
- If the corrected Lane B now compares to the same dense actual-SV target as Lane
  A and Zhao--Cui, then continue with same-target value/gradient benchmarking.
- If the corrected derivation shows Lane B is not a distinct same-target route,
  merge or demote the lane label rather than preserving a misleading distinction.
- If a same-target augmented-noise route cannot be implemented cleanly, keep Lane
  A and Zhao--Cui as the valid inference-facing routes and retire the current
  Lane-B inference framing.
