# P47-M3 Result: Generalized SV Same-Target Equality

metadata_date: 2026-06-08
phase: P47-M3
status: `PASS_P47_M3_GENERALIZED_SV_EQUALITY`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | M3 passed local evidence and Claude read-only review as a lower-rung same-target value/gradient gate for the independent-panel KSC finite-mixture transformed-SV approximation target. |
| Primary criterion status | `PASS_LOCAL`: focused M3 tests pass for value and gradient on dimensions 1, 2, and 3, including direct CUT4--Zhao--Cui gap checks under the declared lower-rung KSC mixture target. |
| Veto diagnostic status | The target manifest keeps native/generalized-SV and KSC-mixture targets separate, preserves the M1 documented-deviation route label, and forbids HMC/native/paper-scale promotion. |
| Main uncertainty | This is a reviewed approximation target, not native generalized SV or CNS estimation. |
| Next justified action | Run local M3 gates, then Claude read-only review for `PASS_P47_M3_GENERALIZED_SV_EQUALITY`. |
| Not concluded | No exact native SV likelihood, no native generalized-SV/CNS estimator, no HMC readiness, no production score API, no adaptive MATLAB TT-cross/SIRT reproduction, no paper-scale validation, and no S&P 500 reproduction. |

## Evidence Contract Outcome

M3 freezes the promoted equality target as the lower-rung independent-panel KSC
finite-mixture transformed-SV approximation.  CUT4 is compared against the
component-enumerated Kalman mixture and dense scalar quadrature on the same
target.  Zhao--Cui is compared against dense scalar quadrature on the same
target through a factorized fixed-design TT route.  CUT4 and Zhao--Cui are also
directly compared against each other with a declared lower-rung tolerance.  All
comparisons use the same unconstrained parameterization.

The phase does not claim that CUT4 and Zhao--Cui are native generalized-SV
filters, nor that the KSC approximation is exact native SV.

## Skeptical Phase Audit

Status: `PASS_TO_LOCAL_M3_GATES`.

- Wrong baseline risk: CUT4 is not used as truth for Zhao--Cui; Kalman and
  dense references anchor the same declared KSC mixture target.
- Target-mismatch risk: the target manifest states that native generalized SV,
  exact transformed SV, and KSC mixture SV are distinct.
- Proxy-metric risk: finite values, fit residuals, and tiny fixture agreement
  do not promote HMC readiness or production score API.
- Hidden-assumption risk: the Zhao--Cui route is a factorized fixed-design
  substitute, not adaptive MATLAB TT-cross/SIRT and not coupled multivariate
  TT.

## Artifacts

- Target manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-generalized-sv-equality-target-manifest-2026-06-08.json`
- Code:
  `bayesfilter/highdim/sv_mixture_cut4.py`
- Focused test:
  `tests/highdim/test_p47_generalized_sv_equality.py`

## Local Commands

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p47-generalized-sv-equality-target-manifest-2026-06-08.json
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_generalized_sv_equality.py
```

Result: 13 passed, 2 TensorFlow Probability deprecation warnings.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_generalized_sv_equality.py
```

Result: passed.

```bash
git diff --check -- bayesfilter/highdim/sv_mixture_cut4.py bayesfilter/highdim/__init__.py tests/highdim/test_p47_generalized_sv_equality.py docs/plans/bayesfilter-highdim-zhao-cui-p47-generalized-sv-equality-target-manifest-2026-06-08.json docs/plans/bayesfilter-highdim-zhao-cui-p47-phase3-generalized-sv-equality-result-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase3-generalized-sv-equality-claude-review-ledger-2026-06-08.md
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_target_registry.py tests/highdim/test_p47_adaptive_route.py tests/highdim/test_p47_paper_scale_readiness.py tests/highdim/test_p47_generalized_sv_equality.py tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py tests/highdim/test_p40_sv_kalman_cut4_zhaocui.py tests/highdim/test_p39_sv_mixture_cut4.py tests/highdim/test_p45_generalized_sv_comparison_blocker.py
```

Result: 68 passed, 2 TensorFlow Probability deprecation warnings.

## Claude Review

Iteration 1 returned:

```text
PASS_P47_M3_GENERALIZED_SV_EQUALITY
```

Claude accepted the gate only under the intended scope: lower-rung same-target
value/gradient equality for the declared independent-panel KSC transformed-SV
approximation target.  The review explicitly did not accept a stronger native
generalized-SV, CNS, HMC, production score API, adaptive MATLAB TT-cross/SIRT,
coupled multivariate TT, paper-scale, or S&P 500 claim.
