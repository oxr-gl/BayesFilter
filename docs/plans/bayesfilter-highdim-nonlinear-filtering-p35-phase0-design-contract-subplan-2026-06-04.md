# P35 Phase 0 Subplan: Design Contract And Non-Public Skeleton

metadata_date: 2026-06-04

parent_plan:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports," Foundations of Computational Mathematics, 2022.

what_is_not_concluded:
- This phase does not implement TT fitting, squared densities, filtering, or
  derivatives.
- This phase does not expose a new top-level public API.
- This phase does not certify any Zhao--Cui numerical result.

## Evidence Contract

Question: can the repo accept a non-public high-dimensional filtering skeleton
with the right contracts before any numerical algorithm is implemented?

Promotion criteria:
- import isolation passes;
- no new top-level `bayesfilter.__all__` symbols are introduced;
- every high-dimensional object requires a declared measure convention;
- every branch-bearing object can produce a full canonical manifest hash;
- production backend policy is TensorFlow/TensorFlow Probability by default.

Veto diagnostics:
- any NumPy-backed BayesFilter-owned algorithmic implementation path is added;
- any constructor permits an implicit or missing density measure;
- branch hashes are computed from selective fields rather than the full
  canonical manifest;
- existing public API tests regress.

## Planned File Ownership

Allowed production writes for this phase only:

```text
bayesfilter/highdim/__init__.py
bayesfilter/highdim/diagnostics.py
bayesfilter/highdim/fixed_branch.py
bayesfilter/highdim/validation.py
tests/highdim/test_phase0_contracts.py
```

Do not edit:
- `bayesfilter/__init__.py`;
- `bayesfilter/nonlinear/`;
- `docs/chapters/`;
- any third-party audit source.

## Implementation Details

### `diagnostics.py`

Define small immutable dataclasses/enums:

```text
DensityMeasure:
  PHYSICAL_LEBESGUE
  REFERENCE_LEBESGUE
  REFERENCE_MEASURE

MeasureConvention:
  density_measure
  mass_measure
  reference_weight_name
  physical_coordinate_name
  reference_coordinate_name

HighDimStatus:
  OK
  MEASURE_MISMATCH
  INVALID_BRANCH_MISMATCH
  NUMERICAL_FAILURE
  COMPLEXITY_GATE
  FIXED_BRANCH_ONLY
```

Add assertion helpers:

```text
assert_density_matches_mass(density_measure, mass_measure)
assert_fixed_branch_only(diagnostics)
assert_finite_tensor(name, tensor)
```

All helpers use TensorFlow tensors where tensor values are involved.

### `fixed_branch.py`

Define:

```text
BranchManifest
BranchHash
BranchIdentity
```

The manifest must support nested dictionaries/lists/scalars/tensors.  The hash
must be over the full manifest using canonical serialization:

- sorted mapping keys;
- explicit dtype;
- explicit shape;
- stable byte order for numeric arrays;
- stable encoding for floats, integers, booleans, strings, and `None`;
- explicit version tag.

The serializer may use Python standard library logic for serialization, but
production numerical payloads are TensorFlow tensors converted only at the
serialization/reporting boundary.  NumPy is not used as an algorithmic backend.

Hash equality is a necessary condition for finite-difference evidence.  It is
not by itself a mathematical correctness proof.

### `validation.py`

Define reusable validation result dataclasses:

```text
HighDimValidationResult
FiniteDifferenceRowStatus
ComplexityBudget
```

Include status strings:

```text
VALID
INVALID_BRANCH_MISMATCH
INVALID_NONFINITE_VALUE
INVALID_MEASURE_MISMATCH
INVALID_COMPLEXITY_GATE
```

### `__init__.py`

Expose only phase-0 internal symbols from `bayesfilter.highdim`.  Do not change
top-level `bayesfilter.__init__`.

## Tests

Create `tests/highdim/test_phase0_contracts.py`.

Required tests:

1. `import bayesfilter.highdim` succeeds.
2. Existing `tests/test_v1_public_api.py` still passes.
3. Constructing a measure-bearing object without `DensityMeasure` fails.
4. A full manifest hash changes when any listed manifest field changes.
5. Two identical manifests have identical hashes.
6. A selective-hash attempt is not accepted as a `BranchIdentity`.
7. NumPy is not imported from `bayesfilter.highdim` modules except inside a
   serialization/reporting helper explicitly marked as non-algorithmic.

Suggested validation commands:

```bash
pytest -q tests/test_v1_public_api.py tests/highdim/test_phase0_contracts.py
```

## Exit Criteria

- All phase-0 tests pass.
- `git diff --check` passes.
- A result ledger records the exact files changed and confirms no top-level API
  exposure.
