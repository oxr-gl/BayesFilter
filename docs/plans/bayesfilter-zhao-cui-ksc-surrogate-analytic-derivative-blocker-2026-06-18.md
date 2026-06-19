# Zhao-Cui KSC Surrogate Analytic-Derivative Blocker Note

metadata_date: 2026-06-18
issue_id: zhaocui-ksc-surrogate-analytic-derivative-blocker
status: BLOCKED_PENDING_FOLLOWUP
owner: handoff_to_new_agent

## Context

While correcting the KSC-surrogate Fixed-SGQF wrapper so that it is **value-only**
unless a true analytical outer score exists, we re-ran a broader focused test
suite and discovered that the current Zhao-Cui KSC-surrogate score evidence is
still going through autodiff-based wrapper tests.

This exposed a concrete failure and indicates that the current Zhao-Cui
KSC-surrogate score path should not be treated as analytically settled.

## Problem summary

The failing path is the Zhao-Cui KSC-surrogate wrapper used in
`tests/highdim/test_p47_generalized_sv_equality.py`.

The test differentiates through the wrapper value function via `_value_and_score(...)`
using `tf.GradientTape`, rather than using a dedicated analytical Zhao-Cui score
API.

During the verification run, that autodiff path failed with:

- `ValueError: Gradient not defined for fast=False`

coming from TensorFlow’s gradient for `MatrixSolveLs`.

## Reproduction

### Command that exposed the problem

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p47_generalized_sv_equality.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py \
  tests/highdim/test_filtering_value_gradient_benchmark_reference_oracles.py \
  tests/test_fixed_sgqf_scores_tf.py \
  tests/test_fixed_sgqf_branch_contract_tf.py
```

### Failing tests observed

The failures came from Zhao-Cui KSC-surrogate score-style tests in:
- `tests/highdim/test_p47_generalized_sv_equality.py`
  - `test_p47_m3_zhaocui_matches_dense_on_same_ksc_mixture_target_value_and_score[...]`
  - `test_p47_m3_cut4_and_zhaocui_direct_gap_is_bounded_on_ksc_target[...]`

## Relevant code anchors

### Wrapper/value route currently under test
- `bayesfilter/highdim/sv_mixture_cut4.py`
  - `independent_panel_sv_mixture_zhaocui_tt_filter(...)`

### Current score-style helper being used in tests
- `tests/highdim/test_p47_generalized_sv_equality.py`
  - `_value_and_score(...)`
  - `_zhaocui_value(...)`

### Experimental autodiff score API used elsewhere for Zhao-Cui style evidence
- `bayesfilter/highdim/score_api.py`
  - `evaluate_experimental_score_api(...)`

### Important nonclaim already present on current value paths
- `bayesfilter/highdim/filtering.py`
  - fixed-design TT value paths include `"derivative_correctness"` in
    `what_is_not_claimed`

## Interpretation

This is enough evidence to treat Zhao-Cui analytical derivative status as
**unresolved / blocked** for the KSC-surrogate wrapper.

We should not assume that because highdim TT derivative primitives exist,
there is already a fully implemented and admitted analytical Zhao-Cui wrapper
score route.

At minimum, the current test evidence shows:
- the active score-style path is wrapper autodiff,
- that path can fail in TensorFlow internals,
- and the value-path manifests still explicitly disclaim derivative correctness.

## Decision

For now:
- leave Zhao-Cui analytical derivative / score work **out of scope** for the
  SGQF correction pass,
- keep the current SGQF wrapper correction focused on value-only status,
- hand this Zhao-Cui issue to a separate agent for dedicated investigation.

## What the follow-up agent should determine

1. Is there already an unexposed analytical Zhao-Cui score route built from the
   highdim derivative primitives in `bayesfilter/highdim/derivatives.py`?
2. If not, what exact layer is missing?
   - analytical wrapper score aggregation,
   - branch/replay contract,
   - TT fit derivative wiring,
   - retained-filter quotient derivative plumbing,
   - or something else.
3. Should the existing Zhao-Cui KSC-surrogate score tests be demoted to
   value-only until that route exists?
4. Is the TensorFlow `MatrixSolveLs(fast=False)` gradient failure only a symptom
   of using the wrong testing path, or part of the actual blocker?

## Suggested next actions for the follow-up agent

- Inspect `tests/highdim/test_p47_generalized_sv_equality.py` and replace the
  current assumption that `_value_and_score(...)` is acceptable Zhao-Cui score
  evidence.
- Audit `bayesfilter/highdim/derivatives.py` and the fixed-design TT fitting
  stack to determine whether an analytical Zhao-Cui score path is partially
  implemented but not exposed.
- Decide whether the immediate safe move is:
  - demote Zhao-Cui KSC-surrogate score claims to value-only, or
  - implement and certify a real analytical Zhao-Cui score route.

## Nonclaims

This note does **not** conclude that Zhao-Cui analytical derivatives are
impossible. It only records that the currently exercised KSC-surrogate
score-testing path is not reliable enough to count as resolved analytical score
support.
