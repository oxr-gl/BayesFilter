# P86 Phase 1 Result: Lagrangep Mass And Integral Implementation

Date: 2026-06-24

Status: `PASS_P86_PHASE1_LAGRANGEP_MASS_INTEGRAL_REVIEWED`

## Phase Objective

Implement and test author-anchored one-dimensional `LagrangePiecewiseBasis1D`
mass matrices and integral vectors for the reference-domain `Lagrangep` basis,
without changing fitting defaults or claiming production readiness.

## Evidence Contract Result

| Field | Result |
|---|---|
| Question | BayesFilter now provides source-anchored `Lagrangep` mass and integral operations matching the author one-dimensional reference-domain assembly. |
| Baseline/comparator | Author `LagrangeRef.m`, `Piecewise.m`, `Lagrangep.m`, the closed-form order-1 analytical micro-baseline, and the P85 local `NotImplementedError` provenance blocker. |
| Primary criterion | Passed. Focused CPU-hidden tests pass for exact mass/integral semantics and no Legendre regression, and Claude read-only bounded review agreed. |
| Veto diagnostics | No missing source anchors, non-symmetric mass, non-positive author-setup mass, wrong basis cardinality, wrong measure scaling, third-party code copy, or production claim observed. |
| Explanatory diagnostics | Matrix/integral closed-form micro-baseline, author-setup mass eigenvalue positivity, partition-of-unity integral, interval scaling, Legendre regression. |
| Not concluded | No algebraic physical-measure correctness, fit quality, downstream wiring, correctness bridge, HMC readiness, LEDH comparison, scale, or production readiness. |
| Artifact | This result, `bayesfilter/highdim/bases.py`, `tests/highdim/test_p86_lagrangep_mass_integral.py`, and updated P85 regression test. |

## Source Mapping

| Author source anchor | Author operation | Local implementation / test |
|---|---|---|
| `LagrangeRef.m:27-45` | Build local `[0,1]` interpolation nodes and barycentric weights. | Existing local nodes/evaluation helpers: `bayesfilter/highdim/bases.py:780-879`; covered by P85 interpolation tests and P86 mass tests. |
| `LagrangeRef.m:46-62` | Compute local exact mass and local integral weights. | `_lagrange_ref_mass_and_integral`: `bayesfilter/highdim/bases.py:760-777`; micro-baseline test: `tests/highdim/test_p86_lagrangep_mass_integral.py:8-34`. |
| `Piecewise.m:24-35` | Fix default reference domain `[-1,1]`, grid, and element size. | `_lagrangep_reference_mass_and_integral`: `bayesfilter/highdim/bases.py:729-757`; tests at `tests/highdim/test_p86_lagrangep_mass_integral.py:8-90`. |
| `Lagrangep.m:18-33` | Assemble global nodes and global-to-local indexing. | Existing `_lagrangep_reference_nodes` and scatter helpers: `bayesfilter/highdim/bases.py:820-879`; P85 tests at `tests/highdim/test_p85_configurable_basis_domain.py:69-106`. |
| `Lagrangep.m:34-52` | Assemble unweighted mass/integral and normalized mass/integral weights. | `mass_matrix`/`integral_vector`: `bayesfilter/highdim/bases.py:373-397`; helper assembly: `bayesfilter/highdim/bases.py:729-777`; focused tests: `tests/highdim/test_p86_lagrangep_mass_integral.py:8-103`. |

No third-party code was copied. The implementation uses BayesFilter-owned
TensorFlow polynomial algebra and existing local Lagrange helpers.

## Implementation Summary

Changed paths:

- `bayesfilter/highdim/bases.py`
- `tests/highdim/test_p86_lagrangep_mass_integral.py`
- `tests/highdim/test_p85_configurable_basis_domain.py`

Claude reviewer may inspect the exact changed line neighborhoods named above,
especially:

- `bayesfilter/highdim/bases.py:373-397`
- `bayesfilter/highdim/bases.py:729-777`
- `tests/highdim/test_p86_lagrangep_mass_integral.py:8-103`
- `tests/highdim/test_p85_configurable_basis_domain.py:109-117`

Implementation behavior:

- `LagrangePiecewiseBasis1D.mass_matrix(REFERENCE_LEBESGUE)` returns the
  reference-domain Lebesgue mass assembled over `[-1,1]`.
- `LagrangePiecewiseBasis1D.mass_matrix(REFERENCE_MEASURE)` returns the
  reference-domain uniform-probability mass, equal to Lebesgue mass divided by
  two on the default `[-1,1]` reference domain.
- `LagrangePiecewiseBasis1D.integral_vector(...)` follows the same measure
  convention.
- Bounded intervals scale `REFERENCE_LEBESGUE` by physical interval length over
  reference interval length, while preserving `REFERENCE_MEASURE`.
- Algebraic maps still use reference-domain mass/integral only. Physical
  algebraic Jacobian semantics remain Phase 2.

## Local Checks

Exact Phase 1 CPU-hidden test command:

```text
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p85_configurable_basis_domain.py
```

Result:

```text
14 passed, 2 warnings in 6.00s
```

Warnings:

```text
TensorFlow Probability distutils Version deprecation warnings only.
```

Diff whitespace check:

```text
git diff --check -- bayesfilter/highdim/bases.py tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p86*.md
PASS
```

## P85 Blocker Context

Phase 1 resolves the narrow P85 local `LagrangePiecewiseBasis1D` mass/integral
`NotImplementedError` blocker. It does not resolve the P85 full-fit blocker:
algebraic measure convention, downstream squared-density/normalizer/marginal
wiring, fitting, correctness, KR, derivative/HMC, comparator, scale, and final
production gates remain open.

## P84 Boundary

This phase does not reopen, satisfy, or cross any P84 downstream approval gate.
P84 Phase 2 fitting remains blocked until later P86 phases pass and exact
human approval is obtained for the relevant command.

## Claude Review

Claude review:

- Reviewer: Claude Opus max effort through trusted wrapper.
- Prompt shape: one exact path, read-only bounded review.
- Reviewed path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase1-lagrangep-mass-integral-result-2026-06-24.md`
- Allowed cited line neighborhoods:
  - `bayesfilter/highdim/bases.py:373-397`
  - `bayesfilter/highdim/bases.py:729-777`
  - `tests/highdim/test_p86_lagrangep_mass_integral.py:8-103`
  - `tests/highdim/test_p85_configurable_basis_domain.py:109-117`
- Verdict: `VERDICT: AGREE`.

Claude agreed the result satisfies the reviewed subplan for source-anchored
mass/integral implementation, local checks, evidence/nonclaim boundaries,
artifact coverage, and safe handoff.

## Decision

Phase 1 passes.

```text
PASS_P86_PHASE1_LAGRANGEP_MASS_INTEGRAL_REVIEWED
```

## Next-Phase Handoff Draft

If Claude review agrees, Phase 2 may begin by refreshing the algebraic measure
contract:

- exact physical/reference density convention;
- Jacobian direction checks for `AlgebraicMapping(1)`;
- manifest fields that prevent mixed-measure fitting;
- downstream components that Phase 3 must exercise.

No fitting, GPU, HMC, LEDH, d=50/d=100, long command, or production claim is
authorized by this Phase 1 result.
