# P35 Phase 5 Subplan: Fixed-Branch Derivatives

metadata_date: 2026-06-04

parent_plan:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- This phase does not differentiate adaptive TT-cross, rank selection, basis
  training, pivot choice, or branch changes.
- This phase does not claim exact nonlinear likelihood gradients.
- This phase does not certify HMC performance on DSGE models.

## Evidence Contract

Question: can BayesFilter differentiate the same fixed-branch deterministic
scalar computed by the Phase 4 value path?

Promotion criteria:
- all finite-difference rows use identical full branch manifest hashes;
- component derivatives match finite differences;
- exact Kalman score baselines pass;
- dense-quadrature scalar nonlinear score baseline passes;
- repeated value/score calls with the same seed, config, observations, and
  branch manifest produce the same branch hash, scalar, and score within
  tolerance;
- branch mismatch invalidates evidence rather than counting as success/failure.

Veto diagnostics:
- any finite-difference row has `INVALID_BRANCH_MISMATCH`;
- derivative path recomputes or changes branch-defining objects;
- exact score baseline mismatch;
- deterministic replay changes branch hash, scalar, or score without declared
  nondeterminism;
- nonfinite derivative of normalizer, carried filter, or log likelihood;
- hidden NumPy algorithmic differentiation path.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/derivatives.py
bayesfilter/highdim/filtering.py
bayesfilter/highdim/fitting.py
bayesfilter/highdim/validation.py
tests/highdim/test_fixed_branch_derivatives.py
tests/highdim/test_failure_exits.py
```

## Implementation Details

### Same-Scalar Contract

The derivative target is:

```text
ell_hat(theta; branch, y_1:T)
```

where `branch` includes the full realized manifest.  During derivative
evaluation:

- basis functions are fixed;
- sample points are fixed;
- row weights are fixed;
- ranks and sweep order are fixed;
- ridge and solver choices are fixed;
- defensive density and floors are fixed;
- coordinate maps and preconditioners are fixed unless the branch explicitly
  declares their parameter derivatives as part of the scalar.

Default first implementation: coordinate maps and preconditioners are fixed
constants in the branch.

### Target Derivatives

Model primitives may provide explicit TensorFlow derivative functions or use
TensorFlow autodiff for primitive log-density derivatives.  This is allowed
because production differentiable paths use TensorFlow/TFP.  The TT derivative
recursion itself must be represented as explicit TensorFlow operations and
diagnostics, not as an opaque end-to-end tape over adaptive fitting.

### Least-Squares Derivative

For fixed design:

```text
K = A^T W A + rho I
b = A^T W y
c = K^{-1} b
```

If \(A,W,\rho\) are fixed:

```text
dot c = K^{-1} A^T W dot y.
```

If a future reviewed branch allows fixed-shape parameter-dependent coordinate
maps, then:

```text
dot c = K^{-1} (dot b - dot K c)
```

with `dot K` and `dot b` stored and tested.  The initial implementation should
not enable this moving-coordinate path without a separate gate.

### TT Contraction Derivatives

For each core:

```text
dot H_k(z_k) = sum_l dot C_k[:,l,:] psi_{k,l}(z_k)
```

for frozen bases.  Evaluation derivative uses product rule through left/right
environments.  Normalizer derivative for squared density:

```text
dot Z = 2 integral h(z) dot h(z) dM(z) + dot defensive_mass
dot log Z = dot Z / Z
```

The initial defensive mass has zero derivative unless explicitly declared.

### Filtering Derivative Recursion

At each time:

1. differentiate target evaluations at fixed branch sample points;
2. differentiate fixed-design fit coefficients;
3. differentiate normalizer and retained marginal;
4. add \(\dot{\log Z_t}\) to total score;
5. pass retained-filter derivative to the next target.

Every step records branch hash equality.

## Tests

`test_fixed_branch_derivatives.py`:

- target derivative unit finite differences;
- fixed-design LS derivative finite differences;
- TT evaluation derivative finite differences;
- normalizer and log-normalizer derivative finite differences;
- carried-filter quotient derivative finite differences;
- one-step scalar Kalman exact score;
- two-step scalar Kalman exact score;
- scalar nonlinear dense-quadrature score;
- deterministic replay for score: same seed/config/branch gives same branch
  hash, scalar, and score;
- branch mismatch invalidates finite-difference row.

Suggested commands:

```bash
pytest -q tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_filtering_kalman_exact.py
```

## Exit Criteria

- Phase 0--5 tests pass.
- A finite-difference table is recorded in a result ledger.
- Diagnostics state `FIXED_BRANCH_ONLY`.
- The result ledger records deterministic replay status for value and score.
- No adaptive derivative claim is made.
