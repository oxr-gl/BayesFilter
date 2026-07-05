# Reset memo: KSC surrogate analytical score lane restart

## Date
2026-06-21

## Context
This pass was working on the KSC Gaussian-mixture surrogate stochastic-volatility
analytical score lane. The intended scope was to move the lane from:
- Kalman mixture value anchor only,
- SGQF value-only,
- UKF adapter ambiguity,
- Zhao-Cui autodiff placeholder comparisons,

to a governed same-target analytical comparison lane for:
- Fixed-SGQF,
- UKF,
- Zhao-Cui,

all measured against the declared KSC surrogate target and its Kalman-mixture
enumeration anchor.

The work progressed through several debugging phases. By the end of this pass,
the key remaining blocker narrowed to the UKF analytical wrapper’s 1D
`probit_gamma` derivative contract.

## Decision / policy
Future sessions should assume the following unless new evidence explicitly
contradicts it:

1. **Kalman-mixture enumeration is the correct value truth anchor** for the
   declared KSC surrogate row because the target is a conditionally
   linear-Gaussian finite-mixture model after the transformed-observation
   construction.

2. **Autodiff is not admissible as the SGQF score itself.**
   It may only be used as a validation oracle for an already-implemented
   analytical gradient.

3. **UKF mismatch claims must be checked against a true centered finite
   difference baseline first.**
   A prior blocker report was invalidated because the purported FD comparator was
   not a real FD method. Use the corrected FD policy from the reset memo below
   before reopening any UKF bug hunt.

4. **Analytical Zhao-Cui score routes now exist in branch** and should be used
   instead of autodiff-based Zhao-Cui comparisons for this lane.

5. **The remaining active blocker is the UKF 1D `probit_gamma` derivative
   mismatch** against the corrected centered-FD baseline. SGQF is no longer the
   active blocker in the 1D reproducer.

## Governing plans / notes
Primary program artifacts for the next agent to read first:
- `docs/plans/bayesfilter-ksc-surrogate-analytic-score-master-program-2026-06-21.md`
- `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-analytic-score-plan-2026-06-18.md`
- `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-analytic-score-derivative-carry-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-ukf-fd-baseline-reset-memo-2026-06-21.md`
- `docs/plans/bayesfilter-zhao-cui-ksc-surrogate-analytic-derivative-blocker-2026-06-18.md`

## What changed
- File: `bayesfilter/highdim/sv_mixture_cut4.py`
  - Added same-target SGQF wrapper value route earlier in the program.
  - Added analytical score wrapper scaffolding for SGQF and UKF.
  - Split the KSC helper so UKF no longer reuses the CUT4-style padded helper.
  - Added UKF-specific minimal-innovation structural helper.
  - Added score aggregation helpers and derivative-carry collapse logic.
  - Current state is partially implemented and should be re-audited carefully
    against the working tree before trusting it.

- File: `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
  - Extended SGQF score result to expose carry state:
    `filtered_mean`, `filtered_covariance`, `d_filtered_mean`,
    `d_filtered_covariance`.

- File: `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`
  - Extended derivative result trace so wrapper code can recover carry-state
    derivatives from the UKF path.

- File: `bayesfilter/highdim/__init__.py`
  - Export surface updated to expose the new analytical score routes:
    `independent_panel_sv_mixture_fixed_sgqf_score`,
    `independent_panel_sv_mixture_ukf_score`,
    and the new analytical Zhao-Cui score routes.

- File: `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
  - Added true centered finite-difference helper and UKF-centered-FD checks.
  - Added time-0 and two-observation UKF FD comparators.
  - Uses analytical Zhao-Cui score helpers rather than wrapper autodiff for the
    Zhao-Cui score comparisons.

- File: `tests/highdim/test_p47_generalized_sv_equality.py`
  - Switched Zhao-Cui KSC score comparisons to `_zhaocui_score(...)`.
  - SGQF remained value-only there pending full analytical lane promotion.

- File: `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-result-2026-06-18.md`
  - Corrected to say the KSC surrogate SGQF wrapper is value-only until a true
    analytical outer score contract is in place.

- File: `docs/plans/bayesfilter-ukf-fd-baseline-reset-memo-2026-06-21.md`
  - Installed the corrected FD-baseline policy.

- File: `docs/plans/bayesfilter-zhao-cui-ksc-surrogate-analytic-derivative-blocker-2026-06-18.md`
  - Earlier blocker note about Zhao-Cui analytical derivative work.
  - This is partially superseded by the fact that analytical Zhao-Cui score
    routes are now present in branch.

- File: `docs/plans/bayesfilter-ukf-ksc-surrogate-time0-gamma-derivative-blocker-2026-06-21.md`
  - Focused blocker note for the unresolved UKF gamma derivative contract.

- File: `docs/plans/bayesfilter-ksc-surrogate-analytic-score-master-program-2026-06-21.md`
  - Consolidated phase-based master program for this lane.

## Bugs / blockers resolved
- Symptom:
  - SGQF wrapper analytical score previously disagreed badly with 1D FD in both
    coordinates.
- Root cause:
  - incorrect wrapper-side gamma/covariance derivative handling and incorrect
    beta contribution in the SGQF analytical wrapper construction.
- Resolution:
  - 1D SGQF analytical wrapper score now matches centered FD in both
    `probit_gamma` and `log_beta`.

- Symptom:
  - earlier UKF blocker notes reported a gamma mismatch against a supposed FD
    baseline.
- Root cause:
  - the comparator path was not a true FD baseline in the earlier reproducer.
- Resolution:
  - replaced with a true centered-FD policy and explicit centered-FD helper;
    the old blocker claim should not be revived without a current FD-based
    reproducer.

## Current active blocker
- Symptom:
  - UKF analytical wrapper score executes, but in the 1D KSC surrogate smoke
    case the `probit_gamma` coordinate still disagrees with the corrected
    centered-FD baseline, while `log_beta` matches.
- Current evidence:
  - SGQF analytical score: `[0.22851775, -1.47752226]`
  - UKF analytical score: `[0.31245209, -1.47752226]`
  - centered FD: `[0.22851775, -1.47752226]`
- Interpretation:
  - the lane is now blocked specifically on the UKF 1D `probit_gamma`
    derivative contract.

## Verification already run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py -k "centered_finite_difference"
```

```bash
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
# 1D SGQF vs UKF vs centered-FD smoke reproducer
PY
```

Observed:
- corrected UKF FD baseline note reports centered-FD agreement for the current
  accepted UKF reproducer path under the corrected comparator setup;
- later direct 1D smoke checks during this pass established that:
  - SGQF now matches centered FD in both coordinates,
  - UKF still differs from FD in `probit_gamma` while matching in `log_beta`.

Treat the current state as: **UKF gamma derivative blocker remains active until
re-derived or revalidated under the current exact command path.**

## Current policy
- Do not use autodiff as the SGQF score.
- Use analytical Zhao-Cui routes instead of autodiff Zhao-Cui routes for this
  lane.
- Treat the UKF 1D gamma coordinate as the only active blocker until a new pass
  proves otherwise with the current exact reproducer.
- Do not promote the lane to full SGQF/UKF/Zhao-Cui analytical comparison until
  the UKF gamma derivative is settled.

## Known limitations / cautions
- The branch has a large amount of unrelated uncommitted / untracked work. A
  fresh agent should re-check the working tree before trusting any inferred file
  state.
- The earlier “UKF is wrong” story is partially invalidated by the FD reset
  memo, but the current exact reproducer still left a gamma-coordinate mismatch.
  The next agent must reconcile these carefully rather than assuming one note
  fully dominates the other.
- The current working state in `bayesfilter/highdim/sv_mixture_cut4.py` likely
  contains partial implementation attempts and should be audited before further
  edits.

## Suggested next steps
1. Start from the master program:
   - `docs/plans/bayesfilter-ksc-surrogate-analytic-score-master-program-2026-06-21.md`
2. Re-audit the exact current code in:
   - `bayesfilter/highdim/sv_mixture_cut4.py`
   - `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
   - `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`
3. Reproduce the UKF 1D `probit_gamma` mismatch with the exact current command
   path before editing more code.
4. Only after the UKF gamma derivative is resolved should the next agent move on
   to dims 2/3 and the full three-way SGQF / UKF / Zhao-Cui analytical suite.
