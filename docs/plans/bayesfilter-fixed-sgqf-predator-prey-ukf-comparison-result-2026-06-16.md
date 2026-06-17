# Fixed-SGQF Predator-Prey UKF Comparison Result

metadata_date: 2026-06-16
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-predator-prey-ukf-comparison-plan-2026-06-16.md`
status: EXECUTION_COMPLETE

## Question

On the same predator-prey lower-rung target, how do fixed SGQF and UKF compare
against the dense same-target reference for value, and how should their
gradients be compared under the current repo infrastructure?

## Implemented changes

Updated:
- `tests/highdim/test_p47_predator_prey_filtering.py`

Added / tightened:
1. same-target UKF value diagnostic row,
2. same-target UKF vs dense full-path value row,
3. same-target fixed-SGQF vs UKF direct value row,
4. parameterized predator-prey structural closure helper for UKF value rows.

## Verification run

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p47_predator_prey_filtering.py \
  tests/highdim/test_p44_predator_prey_diagnostic.py \
  tests/highdim/test_p51_predator_prey_production_tuning.py
```

Observed:
- `27 passed, 2 warnings`

## What the new comparison establishes

### Value side
The predator-prey lower-rung test file now has:
- dense same-target reference,
- Zhao-Cui same-target lower-rung value row,
- CUT4 same-target structural closure diagnostic row,
- fixed-SGQF same-target value diagnostics,
- UKF same-target value diagnostics,
- direct SGQF-vs-UKF value row.

Current lower-rung value gaps against the dense same-target reference are:

| Quantity | Dense | Fixed-SGQF | UKF | SGQF abs gap | UKF abs gap | SGQF rel gap | UKF rel gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Total log-likelihood | `-16.4158538691` | `-65.1112692344` | `-65.1087560933` | `48.6954153653` | `48.6929022242` | `2.9663650611` | `2.9662119688` |
| Step-0 log increment | `-9.1672314059` | `-54.1268728053` | `-54.1249555921` | `44.9596413994` | `44.9577241862` | `4.9043860037` | `4.9041768660` |
| Step-1 log increment | `-7.2486224632` | `-10.9843964291` | `-10.9838005012` | `3.7357739659` | `3.7351780380` | `0.5153770920` | `0.5152948794` |

Path diagnostics versus the dense same-target reference:

| Quantity | Fixed-SGQF max gap | UKF max gap |
| --- | ---: | ---: |
| Filtered mean error (prey) | `17.7804582104` | `17.7799353700` |
| Filtered mean error (predator) | `0.4973272000` | `0.4973632500` |
| Filtered covariance entry error (full path max) | `2.2301276249` | `2.2301812075` |

Interpretation:
- SGQF and UKF are extremely close to **each other** on this tested lower-rung
  predator-prey closure,
- but both are far from the dense same-target reference,
- so the current result is a same-target deterministic comparison row, not a
  dense-equality success row for either SGQF or UKF.

### Gradient side
Current repo support is still asymmetric:
- fixed-SGQF has explicit accepted-branch centered-FD gradient checks on the same
  SGQF scalar,
- the predator-prey CUT4 diagnostic file already contains stronger local
  autodiff-vs-FD calibration style checks,
- but we did **not** promote a direct benchmark-grade SGQF-vs-UKF gradient row in
  this pass because the current infrastructure still does not provide a clean
  same-target reference-gradient comparator for UKF on this predator-prey row.

So the correct interpretation is:
- value comparison row exists,
- gradient comparison remains local-route diagnostic rather than promoted
  cross-method truth.

## Comparison scope summary

| Comparator | Current predator-prey same-target status |
| --- | --- |
| dense lower-rung reference | primary value anchor |
| Zhao-Cui lower-rung route | tight same-target value comparator |
| fixed SGQF | same-target value and accepted-branch local gradient diagnostics |
| UKF | same-target value diagnostic comparator |
| CUT4 | same-target value diagnostic comparator |

## Supported claims
1. Predator-prey now has an explicit same-target value comparison row for fixed
   SGQF vs UKF vs dense lower-rung reference.
2. The SGQF-vs-UKF value comparison is anchored to the dense same-target
   predator-prey reference, not to one another alone.
3. The current gradient comparison scope remains intentionally narrower and more
   honest than the value comparison scope.

## Not supported by this pass
1. No benchmark-grade SGQF-vs-UKF predator-prey gradient ranking claim.
2. No production predator-prey SGQF or UKF claim.
3. No HMC readiness or nonlinear-preconditioning usefulness claim.

## Interpretation

This pass successfully adds the missing predator-prey lower-rung same-target UKF
comparison on the value side. It also makes the scope asymmetry explicit:
- value comparison across dense / Zhao-Cui / SGQF / UKF is now real,
- gradient comparison remains route-local and diagnostic under the current
  infrastructure.

That is the correct scope boundary at the moment.
