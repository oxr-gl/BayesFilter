# P85 Phase 1 Result: Author Basis/Domain Semantics Inventory

Date: 2026-06-23

Status: `PASS_P85_PHASE1_AUTHOR_BASIS_DOMAIN_INVENTORY`

## Phase Objective

Inventory the exact author and local basis/domain semantics needed to design a
setup-configurable BayesFilter basis/domain surface.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What author operations and local gaps must a configurable basis/domain setup represent? |
| Baseline/comparator | Author README, SIR script, `ApproxBases`, `Lagrangep`, `AlgebraicMapping`, and local Legendre-only code. |
| Primary criterion | A reviewed inventory classifies each basis/domain operation as `source_faithful`, `fixed_hmc_adaptation`, `extension_or_invention`, or `local_gap`. |
| Veto diagnostics | Missing paper/source/code anchors; claiming Legendre equals author parity; copying third-party code; using README alone for algorithmic correctness. |
| Explanatory diagnostics | Cardinality formulas, domain-map formulas, replication semantics, current manifest nonclaims. |
| Not concluded | No implementation, fit quality, correctness, XLA performance, or production readiness. |
| Artifact | This Phase 1 result and refreshed Phase 2 subplan. |

## Skeptical Plan Audit

Phase 1 audit passed:

- Wrong-baseline risk is controlled. The comparator is the author basis/domain
  setup and current BayesFilter Legendre route, not P83 execution status.
- Proxy-promotion risk is controlled. Source inventory can justify a setup
  parameter surface only; it does not justify fit, correctness, scaling, or
  production claims.
- Hidden-assumption risk is controlled by separating author setup facts,
  implementation details, and unresolved design inputs.
- Artifact risk is controlled by writing this result before interface design.
- Environment risk is absent because Phase 1 used read-only source/code scans
  and no TensorFlow, GPU, fitting, HMC, LEDH, d=50/d=100, or long commands.

## Author Setup Anchors

The author README explicitly presents basis/domain choices as main-script
configuration:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/README.md:28-41` shows
  `BoundedDomain([-1,1])`, `AlgebraicMapping(1)`, `ApproxBases(...)`, and says
  the user can switch between bounded and algebraic mappings while polynomial
  freedom can be modified in `ApproxBases`.

The SIR script fixes the concrete paper-demo route:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:39-45`
  sets `N=5e3`, `tau=10`, `sqr=1`, `dom = BoundedDomain([-1,1])`,
  `poly1 = ApproxBases(Lagrangep(4,8), dom, d + 2*m)`, and
  `poly2 = ApproxBases(Lagrangep(4,8), AlgebraicMapping(1), d + 2*m)`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:53-56`
  passes `poly2` into `full_sol(..., sqr, poly2, ...)` and solves it.

This supports the P85 premise that basis/domain are setup choices in the author
code, and that the author SIR run uses the algebraic-mapped `Lagrangep(4,8)`
configuration.

## Author Basis Semantics

`Lagrangep(order, num_elems)` is a piecewise high-order Lagrange basis:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Polynomials/Piecewise.m:31-43`
  sets the reference domain to `[-1,1]`, stores `order`, `num_elems`, the grid,
  element size, and a constant-weight flag.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Polynomials/Lagrangep.m:12-52`
  constructs a local `LagrangeRef(order + 1)`, computes global nodes, mass
  matrices, Cholesky mass factors, and integration weights.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Polynomials/Lagrangep.m:56-136`
  evaluates basis values and derivatives using local element selection and
  barycentric formulas.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Polynomials/Oned.m:178-180`
  defines cardinality as the length of `nodes`.

For `Lagrangep(4,8)`, the local node count is `order + 1 = 5`, and the global
node/cardinality formula from `Lagrangep.m:19-22` is:

```text
num_nodes = num_elems * (cardinal(local) - 1) + 1
          = 8 * (5 - 1) + 1
          = 33
```

This cardinality is a setup-static quantity and must not be hidden behind
runtime tensor dispatch in a later implementation; this is a local design
implication for Phase 2, not an additional author claim.

## Author Domain Semantics

Bounded and algebraic domain mappings are distinct author-domain configurations:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Domains/BoundedDomain.m:4-17`
  stores a finite bound and linear mapping parameters for `[-1,1]` by default.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Domains/MappedDomain.m:9-17`
  sets mapped-domain bounds to `[-inf, inf]` and records a `scale`, defaulting
  to `1`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Domains/AlgebraicMapping.m:5-12`
  maps physical domain values to reference values with
  `z = (x/scale) / sqrt(1 + (x/scale)^2)` and
  `dzdx = (1 + (x/scale)^2)^(-3/2) / scale`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Domains/AlgebraicMapping.m:24-43`
  maps reference values back to the unbounded physical domain with
  `x = z / sqrt(1 - z^2) * scale`, plus log-Jacobian formulas.

For the SIR `AlgebraicMapping(1)` route, the scale is `1`.

## ApproxBases Replication Semantics

`ApproxBases` stores tensor-product one-dimensional bases and domain mappings:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/ApproxBases.m:1-12`
  describes tensor-product polynomial basis functions and mappings from the
  approximation domain to the reference domain.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/ApproxBases.m:70-119`
  replicates a single one-dimensional basis or domain mapping across dimension
  `d` when only one is supplied.

For SIR, `d + 2*m = 36`, so `ApproxBases(Lagrangep(4,8),
AlgebraicMapping(1), d + 2*m)` represents 36 replicated one-dimensional
`Lagrangep(4,8)` bases and 36 replicated algebraic mappings.

## Local BayesFilter Gaps

The current local implementation remains Legendre-only at the basis layer:

- `bayesfilter/highdim/bases.py:55-73` defines `LegendreBasis1D`, where
  `basis_dim = max_degree + 1`.
- `bayesfilter/highdim/bases.py:124-143` makes `ProductBasis` accept only
  `LegendreBasis1D`.

The source-route fitting surfaces construct bounded Legendre product bases:

- `bayesfilter/highdim/source_route.py:2262-2269` constructs
  `LegendreBasis1D(BoundedInterval(-1.0, 1.0), fit_degree)` for the P59
  author-SIR 36-dimensional target prep.
- `bayesfilter/highdim/source_route.py:3421-3427` constructs the same
  bounded Legendre product basis in `_p59_fixed_ttsirt_transport_from_values`.

The current manifest and tests explicitly avoid algebraic-mapping parity:

- `tests/highdim/test_p59_author_sir_36d_target_fit.py:44-47` asserts the
  manifest includes `no AlgebraicMapping(1) parity claim`.
- `bayesfilter/highdim/source_route.py:2680` preserves the same nonclaim in
  the source-route manifest.

Additional local design inputs:

- `bayesfilter/highdim/filtering.py:2884-2911` assumes bounded basis domains
  for tensor-product quadrature and uniform reference-weight density.
- `bayesfilter/highdim/fitting.py:1143-1162`,
  `bayesfilter/highdim/filtering.py:4530-4548`, and
  `bayesfilter/highdim/tt.py:348-357` emit basis payloads that assume
  `LegendreBasis1D`.
- `bayesfilter/highdim/squared_tt.py:321-331` reconstructs retained
  `ProductBasis` objects from existing basis axes for defensive marginals;
  Phase 2 must decide whether the generalized basis interface is sufficient
  for that path.

## Classification Ledger

| Operation or route element | Top-level classification | Subtype or tag | Reason |
|---|---|---|---|
| Author exposes basis/domain as main-script setup choices. | `source_faithful` | `setup_surface` | README lines 28-41 explicitly expose domain and polynomial freedom as configurable. |
| Author SIR constructs `Lagrangep(4,8)` with `BoundedDomain([-1,1])`. | `source_faithful` | `optional_sir_config` | SIR script constructs `poly1`; it is not the `full_sol` argument in the shown run. |
| Author SIR constructs and solves with `Lagrangep(4,8)` plus `AlgebraicMapping(1)`. | `source_faithful` | `sir_config` | SIR script constructs `poly2` and passes `poly2` to `full_sol`. |
| Replicating one basis/domain across `d + 2*m` axes. | `source_faithful` | `replication_semantics` | `ApproxBases` replicates singleton inputs across dimension. |
| Local fixed Legendre bounded basis. | `local_gap` | `diagnostic_legendre_route` | Current code hard-codes bounded Legendre product bases and manifests no algebraic parity claim. |
| General setup schema for multiple basis families. | `fixed_hmc_adaptation` until reviewed | `design_input` | It is source-backed as a setup surface, but the exact BayesFilter API is a local design choice. |
| Any non-author family or learned basis added later. | `extension_or_invention` unless separately anchored | `out_of_scope` | Not part of the current P85 author SIR blocker repair. |

## Decision

Phase 1 passes as an inventory:

```text
PASS_P85_PHASE1_AUTHOR_BASIS_DOMAIN_INVENTORY
```

The user premise is supported at the setup-surface level: in the author code,
basis/domain choices are configuration choices. This identifies a candidate
setup-surface direction for later evaluation in Phase 2-4, where any actual
P84 Phase 1 repair must be implemented and tested before it can be claimed.

This phase does not repair the blocker by itself.

## Required Design Inputs For Phase 2

Phase 2 must design:

- a setup-static basis specification that can represent at least
  `legendre(max_degree)` and `lagrangep(order=4, num_elems=8)`;
- a setup-static domain-map specification that can represent at least bounded
  `[-1,1]` and `algebraic(scale=1)`;
- a product-basis specification that records replicated dimension and axis
  cardinalities;
- manifest fields that distinguish top-level classifications and subtypes such
  as `source_faithful`/`sir_config`,
  `source_faithful`/`optional_sir_config`, and
  `local_gap`/`diagnostic_legendre_route`;
- XLA rules stating that changes to family, cardinality, degree/order,
  element count, domain-map family, scale, or dimension may retrace/recompile;
- a decision about which existing helper paths must remain Legendre-only,
  become generic, or explicitly block unsupported basis/domain configurations.

## Local Checks

Phase 1 local checks passed:

- Author source scan found `Lagrangep(4,8)`, `AlgebraicMapping(1)`,
  `ApproxBases`, `BoundedDomain`, and README setup-configuration language.
- Local code/doc scan found `LegendreBasis1D`, `ProductBasis`,
  `BoundedInterval`, `fit_degree`, and explicit `no AlgebraicMapping(1) parity
  claim` anchors.
- No code edits or runtime commands were run in Phase 1.

## Next-Phase Handoff

Phase 2 may begin using:

- `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase2-config-interface-xla-contract-subplan-2026-06-23.md`

Phase 2 remains design-only. It must not implement code or run TensorFlow
tests.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Pass Phase 1 inventory. | PASS: source/local anchors classify setup surface and local gaps. | PASS: no Legendre-as-author-parity claim, no code copy, no runtime/fitting scope. | How to expose author-compatible setup in local TF/TFP code without over-generalizing downstream helpers. | Run Phase 2 setup API and XLA contract design. | No implementation, P84 Phase 1 repair, fit quality, correctness, scaling, or production readiness. |
