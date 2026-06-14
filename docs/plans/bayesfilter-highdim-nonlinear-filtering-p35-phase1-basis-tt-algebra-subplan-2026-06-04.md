# P35 Phase 1 Subplan: Basis, Mass, And TT Algebra

metadata_date: 2026-06-04

parent_plan:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Gorodetsky, Karaman, and Marzouk, "A Continuous Analogue of the Tensor-Train
  Decomposition," Computer Methods in Applied Mechanics and Engineering, 2019.

what_is_not_concluded:
- This phase does not fit TT cores from arbitrary targets.
- This phase does not build a probability density or transport map.
- This phase does not implement filtering or derivatives.

## Evidence Contract

Question: can BayesFilter represent one-dimensional basis functions, reference
measures, mass matrices, and fixed-rank functional TT algebra with explicit
measure conventions and TensorFlow-backed operations?

Promotion criteria:
- analytic low-degree basis and mass tests pass;
- TT evaluation and contraction match exact polynomial examples;
- rank/shape invariants are enforced;
- complexity gates fail before large allocations.

Veto diagnostics:
- missing density/mass convention;
- mass matrix mismatch under non-uniform reference;
- rank boundary \(R_0=R_D=1\) violation;
- materializing a design/contraction tensor beyond declared memory budget.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/bases.py
bayesfilter/highdim/tt.py
bayesfilter/highdim/diagnostics.py
bayesfilter/highdim/fixed_branch.py
tests/highdim/test_bases.py
tests/highdim/test_tt_algebra.py
```

Do not expose top-level API symbols.

## Implementation Details

### Basis Objects

Implement bounded Legendre first:

```text
BoundedInterval(left, right)
UniformReferenceMeasure(domain)
LegendreBasis1D(domain, degree, normalized=True)
ProductBasis(bases)
```

For \(x\in[a,b]\), map to \(\xi=2(x-a)/(b-a)-1\).  Normalized basis functions
under the uniform reference on \([a,b]\) satisfy

```text
psi_n(x) = sqrt(2n+1) P_n(xi)
```

when the reference measure is uniform probability on \([a,b]\).  The mass
matrix is the identity for the normalized basis and diagonal
\((2n+1)^{-1}\) scaling variants for non-normalized forms, depending on the
declared convention.  Tests must pin the chosen convention.

Every basis object stores:

```text
domain
reference_measure
measure_convention
degree
dtype
```

### Mass And Derivative Evaluation

Provide TensorFlow functions:

```text
evaluate_basis(points) -> [n_points, degree]
evaluate_basis_derivative(points) -> [n_points, degree]
mass_matrix() -> [degree, degree]
gram(points, weights) -> [degree, degree]
```

Use recurrence relations rather than symbolic packages.  Derivative tests use
finite differences on low degrees.

### Functional TT Objects

Implement:

```text
TTCore(values: tf.Tensor)  # [left_rank, basis_dim, right_rank]
FunctionalTT(cores, product_basis, measure_convention, branch_identity)
```

Required methods:

```text
evaluate(points) -> [n_points]
integrate_all() -> scalar
marginalize(keep_axes) -> FunctionalTT or contracted representation
rank_tuple()
shape_tuple()
manifest()
```

Evaluation contraction for point \(z=(z_1,\ldots,z_D)\):

```text
v_0 = [1]
v_k = v_{k-1} H_k(z_k)
f(z) = v_D[0]
```

where

```text
H_k(z_k)[a,b] = sum_l core_k[a,l,b] psi_{k,l}(z_k).
```

Integration replaces each core with its basis integral vector and contracts in
coordinate order.  Marginalization integrates selected coordinates and keeps
unintegrated cores with shape/rank checks.

### Complexity Gate

Before any operation that could create dense arrays, compute:

```text
estimated_elements
estimated_bytes
rank_product
basis_product
```

Fail with `COMPLEXITY_GATE` if the request exceeds declared budgets.

## Tests

`tests/highdim/test_bases.py`:

- normalized Legendre mass is identity for degrees 1--5;
- non-uniform reference mismatch test fails unless density ratio is declared;
- basis derivative finite differences pass;
- invalid interval and negative degree fail.

`tests/highdim/test_tt_algebra.py`:

- rank-one separable product evaluates exactly;
- low-rank bivariate polynomial evaluates exactly;
- trivariate example has expected rank/shape and exact integral;
- marginalization preserves normalization on constant functions;
- branch manifest hash changes when a core or basis field changes;
- complexity gate fires before large allocation.

Suggested commands:

```bash
pytest -q tests/highdim/test_phase0_contracts.py tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py
```

## Exit Criteria

- Phase 0 and Phase 1 tests pass.
- No NumPy algorithmic implementation path is introduced.
- A result ledger records basis convention choices and exact formulas used.
