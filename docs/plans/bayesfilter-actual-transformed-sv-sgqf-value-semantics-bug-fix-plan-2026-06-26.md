# Experiment plan: actual-transformed-sv-sgqf-value-semantics-bug-fix

metadata_date: 2026-06-26
program_id: actual-transformed-sv-sgqf-value-semantics-bug-fix
status: DRAFT_READY_FOR_EXECUTION
master_context:
- `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-actual-transformed-sv-augmented-noise-sgqf-next-step-result-2026-06-26.md`
- `docs/plans/bayesfilter-actual-transformed-sv-augmented-noise-sgqf-precursor-improvement-plan-2026-06-26.md`

## Question
What is the correct fix for the actual-transformed SV SGQF lane now that we have
identified a value-semantics bug: the current augmented-noise route computes a
Gaussian-closure surrogate objective instead of an SGQF likelihood approximation
for the intended lane?

What decision will this plan inform?
- whether to repair the SGQF core with a true non-Gaussian update branch, or
- whether to implement a dedicated direct-quadrature actual-SV value path,
- before any further value-quality tuning, precursor promotion, or analytical-
  gradient work is attempted.

## Mechanism being tested
The mechanism under review is the value computation itself.

The specific bug diagnosis is:
- the current actual-transformed augmented-noise route in
  `bayesfilter/highdim/sv_mixture_cut4.py` routes through the Gaussian
  innovation-closure SGQF core in `bayesfilter/nonlinear/fixed_sgqf_tf.py`;
- therefore the scalar value it computes is not the intended SGQF-style direct
  likelihood quadrature for this lane;
- therefore treating the route as a precursor candidate for value promotion or
  analytical-gradient admission was a planning error.

This plan isolates the semantic repair problem, not score work.

## Scope
- Variant: actual-transformed SV value-semantics repair
- Objective: correct the SGQF value computation target before any further score
  or admission work
- Seed(s): deterministic tiny fixture only in the first pass
- Training steps: N/A
- HMC/MCMC settings: none
- XLA/JIT mode: none required
- Expected runtime: focused compile/test diagnostics under a few minutes for the
  first repair pass

Out of scope:
- analytical-score implementation,
- runner/leaderboard row promotion,
- source-row admission claims,
- generalized-SV follow-on work.

## Baseline / comparator
Primary truth anchor:
- `highdim.exact_transformed_sv_independent_panel_dense_reference(...)`

Implementation baseline for bug diagnosis:
- the current route in
  `bayesfilter/highdim/sv_mixture_cut4.py`
  - `actual_transformed_sv_independent_panel_augmented_noise_fixed_sgqf_filter(...)`
- the Gaussian innovation-closure path in
  `bayesfilter/nonlinear/fixed_sgqf_tf.py`

Reference pattern for what the lane should resemble semantically:
- direct pointwise likelihood reweighting pattern already used by
  `exact_transformed_sv_independent_panel_fixed_sgqf_filter(...)`

## Success criteria
Primary:
- identify and document the exact semantic mismatch between the intended SGQF
  likelihood approximation and the current Gaussian-closure implementation;
- choose one repair path:
  1. true non-Gaussian SGQF core branch, or
  2. dedicated direct-quadrature actual-SV value path;
- implement the smallest repair that makes the value function itself the right
  object for the lane.

Secondary:
- keep the repair local enough that existing SGQF/KSC tests remain interpretable;
- preserve target-identity and non-claim discipline.

Sanity checks:
- no score API is added during the value-semantics repair pass;
- no runner/leaderboard artifact is promoted during the repair pass.

## Diagnostics
Primary:
- whether the corrected value path uses direct pointwise observation likelihood
  evaluation rather than Gaussian innovation closure,
- gap versus exact-transformed dense reference on the deterministic tiny fixture,
- same-target interpretation of the repaired scalar value.

Secondary:
- implementation complexity tradeoff of core repair vs dedicated value path,
- whether the corrected route can reuse branch/diagnostic infrastructure cleanly.

Sanity checks:
- KSC surrogate route remains separate,
- actual-transformed route no longer relies on mislabeled Gaussian closure for
  its SGQF value computation.

## Expected failure modes
- the non-Gaussian core branch may be only partially scaffolded and need deeper
  repair than expected;
- a dedicated direct-quadrature value path may duplicate too much logic if the
  core is close to repairable;
- the fix may expose that the current augmented-noise route is unnecessary if a
  direct exact-transformed SGQF value path already answers the narrow lane need.

## What would change our mind
- If the SGQF core can be repaired cleanly with a true non-Gaussian update path,
  prefer that over another lane-specific wrapper.
- If the core repair is too invasive for the immediate need, prefer a dedicated
  actual-SV direct-quadrature value path as the smallest honest correction.
- If neither repair path is clean enough on the tiny fixture, stop and record the
  row as blocked by value-semantics mismatch rather than continuing score work.

## Skeptical audit
Wrong-baseline risk:
- do not compare only against the previous augmented-noise precursor; the dense
  exact-transformed reference remains the truth anchor.

Proxy-promotion risk:
- a repaired value path is still not automatic score admission.

Artifact-answer mismatch risk:
- any plan/result language that resumes talking about score readiness before the
  value semantics are corrected fails this plan.

Audit verdict:
- proceed by treating the issue as a value-side semantic bug first.

## Files likely to modify
Primary implementation candidates:
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `bayesfilter/highdim/sv_mixture_cut4.py`

Primary tests:
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`

Likely result artifact:
- `docs/plans/bayesfilter-actual-transformed-sv-sgqf-value-semantics-bug-fix-result-2026-06-26.md`

## Execution order
1. Write down the exact scalar objective the current route computes and the exact
   scalar objective the lane is supposed to compute.
2. Confirm the mismatch at the code-path level.
3. Choose core repair vs dedicated direct-quadrature path.
4. Implement the smallest honest repair.
5. Re-run focused p41/p43/source-scope verification.
6. Only after the value semantics are corrected should any analytical-gradient
   planning restart.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m compileall -q \
  bayesfilter/nonlinear/fixed_sgqf_tf.py \
  bayesfilter/highdim/sv_mixture_cut4.py \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

## Interpretation rule
- If we can correct the value semantics cleanly, then restart later score work
  from that repaired route only.
- If we cannot correct the value semantics cleanly, keep the row blocked and do
  not resume analytical-gradient work for this lane.
