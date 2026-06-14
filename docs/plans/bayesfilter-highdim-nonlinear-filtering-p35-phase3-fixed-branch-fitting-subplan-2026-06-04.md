# P35 Phase 3 Subplan: Fixed-Branch Fitting

metadata_date: 2026-06-04

parent_plan:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Gorodetsky, Karaman, and Marzouk, "A Continuous Analogue of the Tensor-Train
  Decomposition," Computer Methods in Applied Mechanics and Engineering, 2019.

what_is_not_concluded:
- This phase does not implement adaptive TT-cross, pivot adaptation, or rank
  adaptation.
- This phase does not implement filtering.
- This phase does not certify derivative correctness.

## Evidence Contract

Question: can BayesFilter fit declared fixed-rank TT cores to supplied target
values with a fixed design, fixed branch manifest, and early complexity gates?

Promotion criteria:
- fixed-rank least-squares fits pass on separable and low-rank analytic
  targets;
- branch serialization/reload is stable;
- repeated fit calls with the same declared seed, target, samples, config, and
  backend produce the same branch hash and fitted values within tolerance;
- bad basis/rank choices are vetoed by diagnostics;
- no adaptive branch changes occur during fitting.

Veto diagnostics:
- design matrix exceeds row/column/memory budget;
- ridge solve is singular after declared stabilization;
- branch manifest is missing sample points, weights, ranks, sweep order, or
  solver choices;
- holdout residual exceeds declared tolerance on acceptance tests;
- coordinate-order sensitivity is not reported on coupled examples.
- deterministic replay produces a different branch hash or scalar without a
  declared source of nondeterminism.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/fitting.py
bayesfilter/highdim/fixed_branch.py
bayesfilter/highdim/validation.py
tests/highdim/test_fixed_branch_fit.py
tests/highdim/test_failure_exits.py
```

## Implementation Details

### Fixed Design

Define:

```text
FixedTTFitConfig:
  ranks
  ridge
  sweep_order
  max_sweeps
  row_budget
  column_budget
  dense_matrix_byte_budget
  condition_number_warning
  condition_number_veto
  holdout_tolerance
```

A fit is valid only if all branch-defining choices are declared before the
target is evaluated.

### Initial Minimal Solver

Start with supplied-sample weighted ridge least squares and declared fixed
ranks.  The simplest accepted path may support:

1. rank-one product fits exactly;
2. fixed low-rank TT with alternating core updates.

For core \(j\), hold all other cores fixed.  For sample \(i\), build left and
right environments:

```text
L_i = product_{k<j} H_k(z_{i,k})
R_i = product_{k>j} H_k(z_{i,k})
b_i[l] = psi_{j,l}(z_{i,j})
```

The row block for the vectorized core \(C_j\) is the Kronecker-style product:

```text
A_i = R_i^T \otimes b_i^T \otimes L_i
```

Solve:

```text
(A^T W A + ridge I) vec(C_j) = A^T W y.
```

All \(A\), \(W\), ridge, sample points, target values, sweep order, and solver
diagnostics enter the realized branch manifest.

### Complexity Gates

Before materializing \(A\), estimate:

```text
n_rows
n_cols = R_{j-1} * p_j * R_j
dense_bytes = n_rows * n_cols * dtype_size
normal_matrix_bytes = n_cols^2 * dtype_size
```

Fail before allocation if budgets are exceeded.

### Diagnostics

Record:

```text
fit_residual
holdout_residual
ridge
condition_number_estimate
rank_tuple
sweep_count
core_update_statuses
complexity_gate_status
coordinate_order
branch_hash
```

## Tests

`test_fixed_branch_fit.py`:

- rank-one separable target fit;
- known rank-two bivariate target fit;
- trivariate coupled example reports coordinate-order sensitivity;
- deterministic replay: same seed/config/sample matrix/target values gives the
  same branch hash and same fitted evaluations;
- holdout residual veto on intentionally under-ranked target;
- branch reload reproduces evaluations;
- full branch hash changes when sample points, ridge, ranks, or sweep order
  changes.

`test_failure_exits.py`:

- row budget failure before allocation;
- column budget failure before allocation;
- ridge singularity or condition veto reports deterministic status;
- missing measure convention fails.

Suggested commands:

```bash
pytest -q tests/highdim/test_fixed_branch_fit.py tests/highdim/test_failure_exits.py
```

## Exit Criteria

- Phase 0--3 tests pass.
- A result ledger records the solver equation, complexity budgets, and why no
  adaptive branch is claimed.
- The result ledger records deterministic replay status and any allowed source
  of nondeterminism.
