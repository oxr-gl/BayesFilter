# P50 Value And Gradient Calibration Rules

metadata_date: 2026-06-09
phase: P50-M4
status: PREDECLARED_FOR_P50_M5_M6

## Purpose

These rules define how P50 compares deterministic HMC-facing filter values and
gradients before running the SV, generalized SV, spatial SIR, and predator-prey
ladders.

They explicitly address the user's concern that long or high-dimensional data
can make both autodiff and finite differences numerically fragile.  The policy
is therefore not "finite differences are truth" and not "autodiff is truth by
construction."  Instead, P50 requires a paired same-data comparison, separate
value and gradient evidence, deterministic replay, finite diagnostics, and
scale reporting.

## Required Metrics

Every promoted same-target comparison must report:

- value absolute error: `abs(candidate_value - reference_value)`;
- value relative error: absolute error divided by `max(1, abs(reference_value))`;
- value per-step error: absolute error divided by the number of observations
  when a sequential likelihood is tested;
- gradient absolute norm error:
  `||candidate_gradient - reference_gradient||_2`;
- gradient relative norm error:
  `||candidate_gradient - reference_gradient||_2 / max(1, ||reference_gradient||_2)`;
- directional residuals on a fixed deterministic direction set containing
  coordinate directions and mixed directions;
- directional cosine between candidate and reference gradient, when both norms
  are nonzero;
- finite diagnostics for all compared values and gradients;
- branch/replay diagnostics for deterministic filter branches where applicable.

Value agreement never implies gradient agreement.  Gradient agreement can pass
only when both norm-level and directional diagnostics pass.

## Default Same-Target Tolerances

These tolerances are predeclared before P50-M5 and P50-M6 model-ladder results.
They are defaults for small float64 same-target tests with exact, dense, Kalman,
or otherwise reviewed references.  A later phase may use stricter tolerances.
It may not loosen them after seeing target results unless the phase blocks and
records a new human-approved criterion.

| Metric | Default gate |
| --- | --- |
| Value absolute error | `<= 1e-6` |
| Value relative error | `<= 1e-8` |
| Value per-step error | `<= 1e-7` |
| Gradient relative norm error | `<= 1e-5` |
| Directional scaled residual | `<= 1e-5` |
| Directional cosine | `>= 0.999999` when defined |

Approximation-to-approximation comparisons, such as a Gaussian-mixture SV
approximation against an exact transformed SV likelihood, cannot pass as
same-target correctness evidence.  They can be reported as approximation
diagnostics only unless the target equality has been explicitly derived and
reviewed.

## Likelihood Variability Policy

Generated-data likelihood variability is explanatory scale only.  For data
replicates generated at the same parameter, P50 may report:

- replicate mean and standard deviation of the reference log likelihood;
- standard error of the mean when multiple replicates are used;
- paired same-data algorithm gaps for each replicate;
- the ratio of paired algorithm gap to replicate standard deviation.

This variability does not excuse systematic same-data bias.  A candidate whose
same-data value or gradient error fails the predeclared gate does not pass
because the gap is small relative to cross-dataset likelihood variation.

## Finite Difference Policy

Finite differences are diagnostics, not sole truth.  They are useful for
detecting gross autodiff disconnections and sign errors, but they are fragile
for long horizons, high dimensions, stiff models, nonsmooth guards, and
ill-conditioned likelihoods.

When finite differences are used:

- use float64;
- use at least four step sizes before claiming a stable window;
- use centered differences or a documented higher-order alternative;
- keep the deterministic branch identity fixed or mark the row invalid;
- fit or inspect a stability window across step sizes instead of trusting a
  single step;
- classify nonfinite values, branch mismatch, measure mismatch, and complexity
  vetoes separately;
- treat disagreement without a stable window as inconclusive, not as proof that
  autodiff is wrong.

Finite differences may veto a gradient claim only when the finite-difference
window is stable, branch-compatible, finite, and inconsistent with the analytic
or autodiff gradient by the predeclared diagnostic threshold.

## Autodiff Fragility Policy

Autodiff gradients still require evidence.  P50 must check:

- all value and gradient entries are finite;
- no hidden `stop_gradient`, nondifferentiable branch switch, stochastic
  resampling, or unreviewed clipping enters the tested gradient path;
- deterministic replay reproduces branch identity where the branch is fixed;
- per-step accumulation is numerically stable enough to interpret the total;
- the gradient is compared to an exact, dense, Kalman, CUT4, or independently
  derived reference when a promoted same-target claim is made.

## Pass Classes

| Class | Meaning |
| --- | --- |
| `PASS_SAME_TARGET_VALUE_AND_GRADIENT` | Same target, paired data, value metrics pass, gradient metrics pass, and veto diagnostics pass. |
| `PASS_VALUE_ONLY_DIAGNOSTIC` | Value behavior is useful diagnostic evidence but cannot support gradient or HMC claims. |
| `PASS_GRADIENT_LOCAL_DIAGNOSTIC` | Gradient entries are finite and locally plausible, but no same-target reference pass is established. |
| `BLOCKED_REFERENCE_MISSING` | No adequate value or gradient reference exists for the claim. |
| `FAIL_GRADIENT_DIRECTION` | Value may pass, but directional or norm gradient evidence fails. |
| `FAIL_NUMERICAL_VETO` | Nonfinite, replay, branch, measure, or conditioning diagnostics fail. |

## Non-Claims

These rules do not establish:

- HMC readiness;
- model-suite completion;
- production readiness;
- smoothing support;
- source-faithful adaptive TT/SIRT filtering;
- S&P 500 reproduction;
- that finite differences are ground truth;
- that likelihood variability can excuse systematic same-data bias.
