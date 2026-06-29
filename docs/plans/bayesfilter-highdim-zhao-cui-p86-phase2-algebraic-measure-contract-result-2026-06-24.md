# P86 Phase 2 Result: Algebraic Measure Contract

Date: 2026-06-24

Status: `PASS_P86_PHASE2_ALGEBRAIC_MEASURE_CONTRACT_REVIEWED`

## Phase Objective

Freeze and test the algebraic-domain measure convention for the author SIR
route so downstream densities, normalizers, integrals, and samples cannot
silently mix physical and reference measures.

## Evidence Contract Result

| Field | Result |
|---|---|
| Question | The author algebraic `Lagrangep` route uses reference-coordinate basis contractions, while physical/reference density transforms use explicit algebraic Jacobian directions. |
| Baseline/comparator | Author `AlgebraicMapping.m`, Phase 1 author `Lagrangep` reference-domain mass, local `MeasureConvention`, and local downstream mass calls. |
| Primary criterion | Passed. The contract note and focused CPU-hidden tests prevent reference/physical Jacobian confusion before fitting, and Claude read-only bounded review agreed. |
| Veto diagnostics | No silent physical/reference measure mismatch, reversed Jacobian direction, manifest omission, unsupported mixed convention acceptance, or proxy-correctness claim observed. |
| Explanatory diagnostics | Jacobian formula checks, inverse-map residuals, scalar Gaussian density-transform identities, convention manifest snapshots. |
| Not concluded | No fit quality, posterior correctness, KR closure, HMC readiness, LEDH comparison, scale, default-policy change, or production readiness. |
| Artifact | This result, the Phase 2 contract note, and focused tests. |

## Contract Artifacts

- Contract note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-algebraic-measure-contract-2026-06-24.md`
- Focused tests:
  `tests/highdim/test_p86_algebraic_measure_contract.py`

Claude reviewer may inspect these exact changed line neighborhoods:

- `docs/plans/bayesfilter-highdim-zhao-cui-p86-algebraic-measure-contract-2026-06-24.md:7-109`
- `tests/highdim/test_p86_algebraic_measure_contract.py:19-96`
- `bayesfilter/highdim/bases.py:100-143`
- `bayesfilter/highdim/diagnostics.py:13-25`
- `bayesfilter/highdim/diagnostics.py:109-123`

## Source Mapping

| Source anchor | Operation | Local contract / test |
|---|---|---|
| `AlgebraicMapping.m:5-43` | Defines `z = (x/s)/sqrt(1+(x/s)^2)`, inverse map, `log |dz/dx|`, and `log |dx/dz|`. | Contract note lines 29-64; tests lines 19-67. |
| `bayesfilter/highdim/bases.py:100-143` | Local `AlgebraicMap` implementation. | Tests lines 19-67. |
| `bayesfilter/highdim/diagnostics.py:13-25` | Local density and mass measure names. | Contract note lines 70-83; tests lines 70-96. |
| `bayesfilter/highdim/diagnostics.py:109-123` | Local reference measure compatibility gate. | Test lines 87-96. |

## Frozen Identities

For `z = T(x) = (x/s)/sqrt(1 + (x/s)^2)`:

- `domain_to_reference_log_density(x)` returns `log |dz/dx|`.
- `reference_to_domain_log_density(z)` returns `log |dx/dz|`.
- Physical-to-reference density transform:
  `log p_Z(z) = log p_X(T^{-1}(z)) + log |dx/dz|`.
- Reference-to-physical density transform:
  `log p_X(x) = log p_Z(T(x)) + log |dz/dx|`.

Phase 2 keeps `Lagrangep` mass/integral as reference-coordinate contractions.
It does not add or approve a `PHYSICAL_LEBESGUE` product-basis contraction
route.

## Local Checks

Exact Phase 2 CPU-hidden test command:

```text
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p86_algebraic_measure_contract.py tests/highdim/test_p85_configurable_basis_domain.py
```

Result:

```text
14 passed, 2 warnings in 4.69s
```

Warnings:

```text
TensorFlow Probability distutils Version deprecation warnings only.
```

Diff whitespace check:

```text
git diff --check -- bayesfilter/highdim tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p86*.md
PASS
```

## Non-Approval Boundary

Passing Phase 2 approves only the author-route algebraic measure contract and
focused tests that exercise it.

Passing Phase 2 does not approve:

- all downstream P84/P86 paths;
- all mass/integral consumers;
- any global default policy;
- broad physical/reference equivalence beyond the frozen identities;
- fitting, HMC, LEDH, scale, or production promotion.

## Claude Review

Claude review:

- Reviewer: Claude Opus max effort through trusted wrapper.
- Prompt shape: one exact path, read-only bounded review.
- Reviewed path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase2-algebraic-measure-contract-result-2026-06-24.md`
- Allowed cited line neighborhoods:
  - `docs/plans/bayesfilter-highdim-zhao-cui-p86-algebraic-measure-contract-2026-06-24.md:7-109`
  - `tests/highdim/test_p86_algebraic_measure_contract.py:19-96`
  - `bayesfilter/highdim/bases.py:100-143`
  - `bayesfilter/highdim/diagnostics.py:13-25`
  - `bayesfilter/highdim/diagnostics.py:109-123`
- Verdict: `VERDICT: AGREE`.

Claude agreed the result satisfies the reviewed subplan for exact density and
Jacobian identities, local checks, evidence/nonclaim boundaries, artifact
coverage, and safe Phase 3 handoff.

## Decision

Phase 2 passes.

```text
PASS_P86_PHASE2_ALGEBRAIC_MEASURE_CONTRACT_REVIEWED
```

## Next-Phase Handoff Draft

If Claude review agrees, Phase 3 may begin by refreshing the downstream wiring
subplan for:

- `FunctionalTT.integrate_all`;
- `SquaredTTDensity.sqrt_square_normalizer`;
- marginal/axis contractions;
- trainable normalizer path without fitting;
- derivative normalizer path if in scope;
- route manifests that preserve `lagrangep` plus `algebraic` identity.

No fitting, GPU, HMC, LEDH, d=50/d=100, long command, or production claim is
authorized by this Phase 2 result.
