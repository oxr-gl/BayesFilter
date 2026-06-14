# P35 Phase 4 Subplan: Filtering Value Path

metadata_date: 2026-06-04

parent_plan:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- This phase does not implement analytical derivatives.
- This phase does not expose public API symbols.
- This phase does not justify DSGE deployment.

## Evidence Contract

Question: can BayesFilter compute a fixed-branch squared-TT filtering value
path on exact small models before moving to stress models?

Promotion criteria:
- one-step and two-step scalar Kalman evidence/marginals match exact
  references;
- small multivariate Kalman evidence/marginals match exact references;
- at least one exact small-model filtering recursion passes under a non-identity
  physical-to-reference map and non-uniform reference measure;
- scalar nonlinear dense-quadrature oracle agrees;
- P10-aligned comparison is labeled `STAGE_SANITY_ONLY`.

Veto diagnostics:
- exact Kalman evidence mismatch;
- retained marginal is stored under the wrong measure convention;
- carried filter normalizer is nonpositive or nonfinite;
- branch hash changes unexpectedly within a declared fixed run;
- deterministic replay with the same seed/config/observations changes branch
  hash, value, or retained marginal without a declared source of nondeterminism;
- correction-weight diagnostics are nonfinite.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/filtering.py
bayesfilter/highdim/validation.py
tests/highdim/test_filtering_kalman_exact.py
tests/highdim/test_failure_exits.py
```

Do not edit `bayesfilter/__init__.py`.

## Implementation Details

### Model Protocol

Define a TensorFlow model protocol:

```text
TFHighDimStateSpaceModel:
  parameter_dim
  state_dim
  observation_dim
  initial_log_density(theta, x0)
  transition_log_density(theta, x_prev, x_next, t)
  observation_log_density(theta, x_t, y_t, t)
  simulate_initial(seed)
  simulate_transition(theta, x_prev, t, seed)
```

The initial phase may implement only models with explicit log densities.
Simulation hooks are for diagnostics and stress tests.

### Adjacent-State Target

At time \(t\), fit a target over the adjacent block:

```text
u_t = (theta, x_t, x_{t-1})
```

or the relevant retained ordering declared by the branch.  The unnormalized
target is:

```text
carried_filter(theta, x_{t-1})
* transition(theta, x_{t-1}, x_t)
* observation(theta, x_t, y_t)
```

For \(t=1\), `carried_filter` is the initial density/prior over
\((theta,x_0)\).  Every target builder returns its `DensityMeasure`.

### Value Recursion

For each time:

1. construct the target under the declared physical/reference coordinate map;
2. transform to the declared reference measure target;
3. fit a square-root TT with fixed branch;
4. build `SquaredTTDensity`;
5. compute normalizer \(Z_t\);
6. accumulate \(\log Z_t\) plus any coordinate/constant offsets;
7. retain the marginal over \((theta,x_t)\) for the next step;
8. record diagnostics and branch manifest.

### Retained Filter Storage

For scalar/small vector retained states:

- retain a marginal squared-TT density when feasible;
- store measure convention, retained coordinate order, normalizer, basis, mass
  matrices, and branch hash;
- refuse dense product-basis storage when complexity budgets are exceeded.

### Exact References

Use existing BayesFilter Kalman functions for exact references where possible,
or implement a tiny closed-form fixture in tests.  NumPy may be used only inside
test reference fixtures, not production filtering code.

### Recursive Measure/Map Fixture

Add one exact small linear-Gaussian filtering fixture with:

```text
r = a + B z
z_reference_measure has non-uniform density omega(z)
fitted target is q_z^nu(z) = q_r(a+Bz) |det B| / omega(z)
```

The test must check:

- accumulated log evidence includes the affine Jacobian/reference-density
  convention correctly;
- retained marginal over \((theta,x_t)\) is stored under the declared measure;
- the next-step target consumes that retained marginal without switching
  measure conventions;
- intentionally omitting the \(\omega(z)\) factor fails the test.

## Tests

`test_filtering_kalman_exact.py`:

- one-step scalar linear-Gaussian evidence;
- two-step scalar linear-Gaussian evidence;
- filtering mean/covariance marginal against Kalman;
- small multivariate linear-Gaussian case;
- non-identity affine map plus non-uniform reference recursive filtering case;
- deterministic replay: same seed/config/observations gives same branch hash,
  value, and retained marginal;
- scalar nonlinear observation against dense quadrature;
- retained filter measure convention assertion.

P10 sanity:

- optional test or result note checks that the reduced P10 smoke and BayesFilter
  value path share the same high-level stages;
- label this `STAGE_SANITY_ONLY`;
- do not compare bitwise values or treat P10 as correctness evidence.

Suggested commands:

```bash
pytest -q tests/highdim/test_filtering_kalman_exact.py tests/highdim/test_failure_exits.py
```

## Exit Criteria

- Phase 0--4 tests pass.
- Exact small-model value references pass.
- Recursive non-identity map/non-uniform reference fixture passes.
- Deterministic replay status is recorded.
- No public API export has occurred.
- A result ledger records all model fixtures, tolerances, and non-conclusions.
