# P35 Phase 2 Subplan: Squared Density And Transport

metadata_date: 2026-06-04

parent_plan:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports," Foundations of Computational Mathematics, 2022.

what_is_not_concluded:
- This phase does not fit a TT from data.
- This phase does not implement sequential filtering.
- This phase does not prove adaptive TT differentiability.

## Evidence Contract

Question: can BayesFilter turn an existing square-root functional TT into a
nonnegative normalized density, compute marginals and conditionals under the
declared measure, and build basic KR transport operations?

Promotion criteria:
- normalizers and marginals match analytic examples;
- conditional CDFs are monotone and invertible on declared grids;
- KR Jacobian identity passes on small analytic cases;
- all tests run under the measure convention gate.

Veto diagnostics:
- normalizer is nonpositive or nonfinite;
- mass contraction uses a different measure than the fitted target;
- conditional CDF is nonmonotone after allowed floor policy;
- inverse-CDF cannot bracket the target probability;
- branch hash is missing from density/transport outputs.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/squared_tt.py
bayesfilter/highdim/transport.py
bayesfilter/highdim/diagnostics.py
tests/highdim/test_squared_tt_density.py
tests/highdim/test_transport.py
tests/highdim/test_failure_exits.py
```

## Implementation Details

### Squared Density

Implement:

```text
SquaredTTDensity(
    sqrt_tt,
    defensive_density,
    tau,
    measure_convention,
    branch_identity,
    normalizer_floor,
)
```

Density convention:

```text
q_unnormalized(z) = h(z)^2 + tau * q0(z)
Z = integral q_unnormalized(z) dM(z)
q(z) = q_unnormalized(z) / Z
```

Here \(dM\) is the declared mass measure.  If `density_measure` and
`mass_measure` disagree, construction fails.

`defensive_density` starts as a tensor-product reference density with analytic
normalizer.  More complicated defensive densities are postponed.

### Mass Contractions

For \(h(z)\) represented by TT cores, \(h^2\) integration contracts pairwise
core products with one-dimensional mass matrices:

```text
M_k[l,m] = integral psi_{k,l}(z_k) psi_{k,m}(z_k) dM_k(z_k)
```

The contracted core contribution is

```text
G_k[(a,a'),(b,b')] = sum_{l,m} C_k[a,l,b] C_k[a',m,b'] M_k[l,m].
```

The normalizer is the product contraction of \(G_1,\ldots,G_D\), plus the
defensive mass.

### Marginals And Conditionals

Implement marginalization by contracting integrated coordinates and retaining
unintegrated coordinates.  Conditional density is

```text
q(z_j | z_{<j}) = q(z_{\le j}) / q(z_{<j})
```

with denominator floors recorded in diagnostics.  Floor usage is explanatory
until it exceeds the declared threshold, then it is a veto.

### KR Transport

Start with lower triangular order:

```text
u_j = F_j(z_j | z_{<j})
z_j = F_j^{-1}(u_j | z_{<j})
```

Implement CDF evaluation by one-dimensional quadrature over coordinate \(j\)
using the same basis/reference convention.  Implement inversion by bracketed
bisection first; Newton refinement is optional only after bisection tests pass.

The log-Jacobian identity to test is:

```text
log |det dF/dz| = sum_j log q(z_j | z_{<j})
```

for the forward map from target coordinates to uniform coordinates.

## Tests

`test_squared_tt_density.py`:

- constant square-root TT normalizes correctly;
- Gaussian-like low-dimensional example matches dense quadrature;
- non-uniform reference missing-weight trap fails;
- defensive density prevents zero mass in a declared corner case;
- branch hash propagates to density diagnostics.

`test_transport.py`:

- one-dimensional CDF/inverse-CDF round trip;
- two-dimensional separable density gives independent coordinate maps;
- conditional Gaussian-like example passes monotonicity and sample moment
  checks;
- KR Jacobian identity passes within tolerance;
- bracket failure is reported, not silently clipped.

Suggested commands:

```bash
pytest -q tests/highdim/test_bases.py tests/highdim/test_tt_algebra.py \
  tests/highdim/test_squared_tt_density.py tests/highdim/test_transport.py \
  tests/highdim/test_failure_exits.py
```

## Exit Criteria

- Phase 0--2 tests pass.
- Every density/transport result carries measure convention and branch hash.
- A result ledger records all floor/default choices.
