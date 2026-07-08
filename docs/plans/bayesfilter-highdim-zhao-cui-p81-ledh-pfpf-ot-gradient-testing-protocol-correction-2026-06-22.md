# P81 / LEDH-PFPF-OT Gradient Testing Protocol Correction

Date: 2026-06-22

Status: REQUIRED_PROTOCOL_CORRECTION_BEFORE_GRADIENT_TESTING

## Purpose

This note corrects the finite-difference and comparator policy for testing
LEDH-PFPF-OT gradients on the SIR target.

The two-point centered finite difference

```text
[f(theta + eps v) - f(theta - eps v)] / (2 eps)
```

is too noisy for this stochastic high-dimensional filtering setting and must
not be used as the promotion criterion.

## Binding Finite-Difference Protocol

For each tested theta direction `v`, use the previous regression-style
finite-difference protocol:

1. Run a 13-point line test around `theta`.
2. Evaluate the 13 theta-offset values in batched form when memory permits,
   folding theta-offset rows into the filter batch axis instead of launching 13
   separate value calls.
3. Use 1000 particles for each finite-difference line point unless a reviewed
   subplan explicitly changes the budget.
4. Use five fixed seeds for the finite-difference line.  The value at each
   theta-offset point is the mean over the five seed evaluations.
5. Evaluate values along the line, e.g. at symmetric offsets around zero.
6. Drop the highest and lowest value among the 13 mean-over-seed line values.
   This is a value-outlier trim, not an extreme-offset trim.
7. Fit an ordinary least squares regression to the remaining 11 points:

   ```text
   f(theta + x v) = intercept + slope * x + residual
   ```

8. Use the fitted slope as the finite-difference gradient estimate in
   direction `v`.
9. Explicitly compute and record the slope standard error.
10. Compare gradient discrepancies in standard-error units.

For LEDH-PFPF-OT's actual gradient estimate at `theta`, use `N = 10000`
particles and the same five fixed seeds by default.  The reported LEDH estimate
is the mean over seeds, with seed-level standard deviation and standard error
recorded.

The batched line-evaluation implementation must preserve seed identity.  If the
13 offsets and five seeds are folded into a single batch axis, the artifact must
record the mapping from `(seed, offset)` to each batch row and the exact
aggregation rule:

```text
mean_value(offset) = mean_seed f_seed(theta + offset * v)
```

The existing P8p regression-FD harness has a `batched-theta` evaluation mode and
seed microbatching support, but the current checkout must be audited before
reuse because it previously accepted 7/9/15/17 offsets and its trim option
removed extreme offsets rather than highest/lowest values.  A valid SIR
gradient test must either patch that harness or use a new harness that supports
13 offsets and value-outlier trimming.

The artifact must record the 13 raw line values, the two dropped points, the
11 retained points, the fitted slope, intercept, residual diagnostics, slope
standard error, seed list, per-seed values, per-offset seed mean and standard
error, LEDH `N = 10000` seed-level estimates, and the standardized discrepancy.

## Pass / Warning Rule

For a directional comparison between two gradient estimates, compute:

```text
z = abs(direction_a - direction_b) / standard_error
```

where `standard_error` is the conservative combined uncertainty scale.  For
LEDH-PFPF-OT versus its regression finite-difference slope, this should include
the regression slope standard error and the LEDH seed-mean standard error when
available.  For LEDH-PFPF-OT versus Zhao-Cui, the uncertainty scale should at
least include the LEDH seed-mean standard error and any recorded Zhao-Cui
diagnostic uncertainty; if Zhao-Cui is deterministic under a fixed branch, do
not describe it as oracle variance zero, only as deterministic comparator
output for that approximation.

If the discrepancy is more than 2 standard errors, treat this as a likely
issue requiring investigation.  The result should not be promoted as agreement
without a documented explanation.

## Comparator Policy

Zhao-Cui is not an oracle.  LEDH-PFPF-OT is not an oracle.  All
high-dimensional filters in this comparison are approximations.

Therefore:

- compare LEDH-PFPF-OT against its own regression finite-difference slope;
- compare Zhao-Cui analytical derivatives against their own diagnostics;
- compare LEDH-PFPF-OT and Zhao-Cui as approximate methods under matched theta,
  data, directions, and budgets;
- interpret disagreements in standard-error units and route diagnostics, not as
  automatic proof that one method is correct and the other is wrong.

## Forbidden Uses

Do not:

- use a two-point centered finite difference as the promotion criterion;
- tune step size or tolerance after seeing the result;
- report a finite-difference slope without its standard error;
- call Zhao-Cui the oracle;
- call LEDH-PFPF-OT correct solely because it matches Zhao-Cui;
- call Zhao-Cui correct solely because LEDH-PFPF-OT disagrees;
- conclude posterior correctness, HMC readiness, production readiness, or
  scientific superiority from this gradient diagnostic.

## Required Update To The Testing Plan

Any LEDH-PFPF-OT SIR gradient subplan must now include:

- theta convention and tested directions;
- finite-difference particle count, with 1000 particles as the default
  per-line-point budget;
- LEDH actual-estimate particle count, with `N = 10000` as the default;
- five fixed seeds for both regression finite-difference values and the actual
  LEDH estimate;
- batched theta-offset value evaluation for the 13-point line, or a documented
  blocker if memory/device constraints require microbatching;
- 13-point offset grid;
- outlier-drop rule: highest and lowest mean-over-seed values dropped before
  regression;
- regression formula and slope standard-error computation;
- standardized discrepancy threshold, with more than 2 standard errors treated
  as an issue;
- Zhao-Cui classified as an approximate comparator, not an oracle;
- explicit nonclaims for posterior correctness, HMC readiness, and default
  readiness.
