# P86 Algebraic Measure Contract

Date: 2026-06-24

Status: `PASS_P86_PHASE2_ALGEBRAIC_MEASURE_CONTRACT_REVIEWED`

## Scope

This contract freezes the algebraic-map density and measure naming used by the
Zhao-Cui author-route setup after Phase 1 implemented reference-domain
`Lagrangep` mass and integral operations.

This contract does not approve fitting, downstream correctness, HMC, LEDH,
scale, production readiness, or a default-policy change.

## Source Anchors

- Author SIR setup:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:43-55`
- Author algebraic map formulas:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Domains/AlgebraicMapping.m:5-43`
- Local algebraic map:
  `bayesfilter/highdim/bases.py:100-143`
- Local measure naming:
  `bayesfilter/highdim/diagnostics.py:13-25`
- Local measure compatibility gate:
  `bayesfilter/highdim/diagnostics.py:109-123`

## One-Dimensional Map

For scale `s > 0`, physical coordinate `x`, and reference coordinate `z`:

```text
z = T(x) = (x/s) / sqrt(1 + (x/s)^2)
x = T^{-1}(z) = s * z / sqrt(1 - z^2)
```

The Jacobian identities are:

```text
dz/dx = (1 + (x/s)^2)^(-3/2) / s
dx/dz = s * (1 - z^2)^(-3/2)
```

Local method naming:

- `AlgebraicMap.domain_to_reference_log_density(x)` returns `log |dz/dx|`.
- `AlgebraicMap.reference_to_domain_log_density(z)` returns `log |dx/dz|`.

## Density Transform Direction

If a physical density `p_X(x)` is transformed to a reference density:

```text
p_Z(z) = p_X(T^{-1}(z)) * |dx/dz|
log p_Z(z) = log p_X(T^{-1}(z)) + log |dx/dz|
```

If a reference density `p_Z(z)` is transformed to a physical density:

```text
p_X(x) = p_Z(T(x)) * |dz/dx|
log p_X(x) = log p_Z(T(x)) + log |dz/dx|
```

These identities are local one-dimensional density identities. Product-route
uses must apply them axiswise and preserve the declared measure convention in
manifests before they are eligible for downstream fitting gates.

## Measure Naming

The author algebraic `Lagrangep` basis mass/integral from Phase 1 remains a
reference-coordinate contraction:

- `MassMeasure.REFERENCE_LEBESGUE` means integration over reference-coordinate
  Lebesgue measure.
- `MassMeasure.REFERENCE_MEASURE` means integration over the normalized
  reference measure.

`DensityMeasure.PHYSICAL_LEBESGUE` exists in local enums, but the current
`assert_density_matches_mass` gate rejects it for product-basis contractions.
Phase 2 does not change that policy. A future physical-density route must add a
reviewed convention and tests before fitting can use it.

## Required Manifest Rules

Author-route manifests must preserve:

- basis family: `lagrangep`;
- domain-map family: `algebraic`;
- algebraic scale;
- density measure name;
- mass measure name;
- reference and physical coordinate names;
- nonclaims that fitting, correctness, HMC, LEDH, scale, and production
  readiness remain unresolved.

## Non-Approval Boundary

Passing Phase 2 approves only this author-route algebraic measure contract and
the focused tests that exercise it.

Passing Phase 2 does not approve:

- all downstream P84/P86 paths;
- all mass/integral consumers;
- any global default policy;
- broad physical/reference equivalence beyond the identities above;
- fitting, HMC, LEDH, scale, or production promotion.
