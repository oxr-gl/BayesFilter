# P85 Phase 2 Result: Config Interface And XLA Contract

Date: 2026-06-23

Status: `PASS_P85_PHASE2_CONFIG_INTERFACE_XLA_CONTRACT`

## Phase Objective

Design the BayesFilter setup configuration surface for basis family, basis
parameters, domain mapping, dimension replication, manifest identity, and
XLA/static compilation boundaries.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What setup API can express the author basis/domain route while remaining XLA-safe and locally maintainable? |
| Baseline/comparator | Phase 1 inventory and existing `ProductBasis`/manifest APIs. |
| Primary criterion | A reviewed design states setup fields, allowed families, manifest identity, classification labels, and static compilation rules. |
| Veto diagnostics | Runtime tensor-controlled basis dispatch; hidden Python branching inside `tf.function` hot paths; missing manifest identity; unsupported source-faithful labels. |
| Explanatory diagnostics | Expected retrace/recompile triggers, basis cardinality, domain-map formulas, import/export surface. |
| Not concluded | No implementation, no performance claim, no fit quality, no production readiness. |
| Artifact | This Phase 2 result and refreshed Phase 3 subplan. |

## Skeptical Plan Audit

Phase 2 audit passed:

- Wrong-baseline risk is controlled. The design starts from Phase 1 source/local
  inventory and existing BayesFilter basis APIs.
- Proxy-promotion risk is controlled. The design can authorize Phase 3 planning
  only; it does not implement, test, fit, or repair P84 Phase 1 by itself.
- Hidden-assumption risk is controlled by making family, degree/order, element
  count, domain-map family, scale, cardinality, and dimension explicit setup
  identity fields.
- Environment risk is absent because Phase 2 runs no TensorFlow tests, GPU,
  fitting, HMC, LEDH, d=50/d=100, or long commands.
- Artifact risk is controlled by giving Phase 3 a concrete implementation/test
  matrix to freeze before code edits.

## Existing API Inputs

Current local structure:

- `bayesfilter/highdim/bases.py:55-143` exposes `BoundedInterval`,
  `LegendreBasis1D`, and `ProductBasis`, with `ProductBasis` currently limited
  to `LegendreBasis1D`.
- `bayesfilter/highdim/fitting.py:224-247` validates `ProductBasis` and uses
  it throughout `FixedTTFitter`.
- `bayesfilter/highdim/fitting.py:522-542` builds ALS design matrices from
  `product_basis.evaluate_axis(...)` and core `basis_dim`.
- `bayesfilter/highdim/fitting.py:600-631` validates ranks, sweep order, batch
  dimension, and initial cores against `product_basis.dimension` and basis
  dimensions.

Legendre-specific local surfaces that Phase 3 must account for:

- `bayesfilter/highdim/filtering.py:2884-2911` assumes bounded basis domains for
  tensor-product quadrature and uniform reference-weight density.
- `bayesfilter/highdim/fitting.py:1143-1162`,
  `bayesfilter/highdim/filtering.py:4530-4548`, and
  `bayesfilter/highdim/tt.py:348-357` emit basis payloads that assume
  `LegendreBasis1D`.
- `bayesfilter/highdim/__init__.py:19-24` and `:431-610` export the current
  basis classes from the highdim namespace.

## Proposed Setup Data Model

Phase 3 should freeze exact names before implementation, but Phase 2 approves
the following shape.

### `DomainMapSpec`

Fields:

- `family`: one of `bounded_interval`, `algebraic`.
- `classification`: top-level source class, one of `source_faithful`,
  `fixed_hmc_adaptation`, `extension_or_invention`, or `local_gap`.
- `classification_subtype`: a narrower tag such as `author_sir_config`,
  `diagnostic_legendre_route`, or `legacy_bounded_route`.
- `source_anchors`: tuple of source/code anchors supporting the classification.
- For `bounded_interval`: `left`, `right`, `dtype_name`.
- For `algebraic`: `scale`, `dtype_name`.

Required semantics:

- `bounded_interval(-1,1)` maps local/physical points to reference points with
  the current `BoundedInterval` convention.
- `algebraic(scale=1)` records the author map
  `z = (x/scale) / sqrt(1 + (x/scale)^2)` and inverse
  `x = z / sqrt(1 - z^2) * scale`.
- Domain-map formulas belong to documentation/manifests and test fixtures
  unless Phase 4 explicitly implements evaluation methods.

### `BasisSpec`

Fields:

- `family`: one of `legendre`, `lagrangep`.
- `classification`: top-level source class.
- `classification_subtype`: narrower route tag.
- `source_anchors`: tuple of source/code anchors supporting the classification.
- `domain_map`: a `DomainMapSpec`.
- For `legendre`: `max_degree`, `normalized`.
- For `lagrangep`: `order`, `num_elems`.
- `basis_dim`: explicit setup-static integer.
- `dtype_name`.

Required cardinalities:

- `legendre(max_degree)` has `basis_dim = max_degree + 1`.
- `lagrangep(order, num_elems)` has
  `basis_dim = num_elems * order + 1` for the author-style `Lagrangep`
  construction, because `LagrangeRef(order + 1)` creates `order + 1` local
  nodes.
- For `Lagrangep(4,8)`, `basis_dim = 33`.

Required methods for an implementation object, if Phase 4 reaches code:

- `basis_dim -> int`
- `dtype -> tf.DType`
- `evaluate(points: tf.Tensor) -> tf.Tensor`
- `derivative(points: tf.Tensor) -> tf.Tensor` only if Phase 3 includes it;
  otherwise derivative readiness must remain blocked.
- `mass_matrix(measure: MassMeasure) -> tf.Tensor`
- `integral_vector(measure: MassMeasure) -> tf.Tensor`
- `manifest_payload() -> Mapping[str, object]`

### `ProductBasisSpec`

Fields:

- `dimension`: setup-static integer.
- `axis_specs`: tuple of `BasisSpec`, or one `BasisSpec` plus
  `replicated=True`.
- `basis_dim_tuple`: explicit tuple.
- `measure_convention`: existing `MeasureConvention`.
- `route_classification`: top-level classification.
- `classification_subtype`: narrower route tag.
- `source_anchors`: tuple of anchors.

Required replication semantics:

- A single `BasisSpec` with `replicated=True` expands to `dimension` identical
  axis specs.
- For the author SIR route, `dimension = 36`, `family = lagrangep`,
  `order = 4`, `num_elems = 8`, `domain_map.family = algebraic`,
  `domain_map.scale = 1`, and `basis_dim_tuple = (33, ..., 33)`.
- The legacy diagnostic route remains `dimension = target_dim`,
  `family = legendre`, `max_degree = fit_degree`,
  `domain_map.family = bounded_interval`, and
  `classification = local_gap` or reviewed `fixed_hmc_adaptation`, not
  `source_faithful`.

## Manifest Identity Contract

Every branch/transport/fit manifest that uses a basis configuration must include
or reference:

- `basis_config_version`, e.g. `basis_config.v1`;
- `basis_family`;
- `basis_parameters`;
- `basis_dim`;
- `domain_map_family`;
- `domain_map_parameters`;
- `dimension`;
- `basis_dim_tuple`;
- `classification`;
- `classification_subtype`;
- `source_anchors`;
- `xla_static_fields`;
- `nonclaims`.

Changing any identity field must change branch identity or manifest hash. A
hash that omits basis family or domain-map family is not sufficient for P85.

## XLA / Static Compilation Contract

The following fields are setup-static for a compiled run:

- basis family;
- basis cardinality;
- Legendre degree;
- Lagrangep order;
- Lagrangep element count;
- domain-map family;
- domain-map scale;
- bounded interval endpoints;
- replicated dimension;
- `basis_dim_tuple`;
- measure convention;
- dtype.

Changing any setup-static field may retrace or recompile. That is acceptable and
must be stated in manifests or result notes. Phase 4 must not implement
runtime tensor-controlled dispatch that switches basis family, cardinality, or
domain-map family inside one XLA-compiled hot path.

Allowed implementation pattern:

- Python/dataclass setup builds concrete basis objects before compiled
  computation.
- Compiled functions receive tensors with fixed shape assumptions derived from
  those objects.
- Different basis/domain configurations may create different Python objects and
  different traced graphs.

Forbidden implementation pattern:

- A tensor flag, string tensor, or runtime branch selects between Legendre and
  Lagrangep evaluation inside a compiled function.
- A dynamic cardinality tensor changes the last dimension of basis evaluations.
- A manifest says two configurations are the same branch when basis/domain
  identity differs.

## Source-Classification Contract

Approved P85 classifications:

| Route | Top-level classification | Subtype |
|---|---|---|
| Author SIR `Lagrangep(4,8)` plus `AlgebraicMapping(1)` | `source_faithful` | `sir_config` |
| Author SIR `Lagrangep(4,8)` plus `BoundedDomain([-1,1])` construction not used by `full_sol` in the shown run | `source_faithful` | `optional_sir_config` |
| Current local bounded Legendre route | `local_gap` unless a later reviewed result classifies it as fixed adaptation | `diagnostic_legendre_route` |
| Local setup API itself | `fixed_hmc_adaptation` until reviewed by implementation result | `design_input` |
| Any non-author basis family | `extension_or_invention` unless separately anchored | `out_of_scope` |

## Scope For Phase 3 Implementation Matrix

Phase 3 should freeze a minimal implementation matrix:

1. Add setup-spec dataclasses and payload helpers in `bayesfilter/highdim/bases.py`
   or a new small highdim module chosen by Phase 3.
2. Add a BayesFilter-owned `LagrangePiecewiseBasis1D` or equivalent, not copied
   from third-party MATLAB code.
3. Generalize `ProductBasis` only as far as needed for basis objects supporting
   the existing minimal protocol.
4. Add a builder for:
   - legacy bounded Legendre diagnostic config;
   - author SIR algebraic `Lagrangep(4,8)` config.
5. Update manifest payload helpers in the minimal files frozen by Phase 3.
6. Add focused tests for:
   - spec payload and hash/manifest identity;
   - `Lagrangep(4,8)` `basis_dim == 33`;
   - algebraic mapping formulas at representative points;
   - legacy Legendre manifest remains diagnostic/non-parity;
   - XLA/static contract is documented as retrace/recompile on setup changes,
     not as one-graph dynamic switching.

Phase 3 must decide whether Phase 4 includes derivative, mass, and integral
methods for Lagrangep or blocks them explicitly. If any downstream route needs
those methods, omitting them must block Phase 4 repair rather than silently
claiming support.

## Deferred Or Explicitly Unsupported In P85

P85 Phase 2 does not authorize:

- production fitting;
- HMC or derivative-readiness claims;
- KR closure;
- LEDH comparison;
- d=50/d=100 scaling;
- one XLA executable across all basis families;
- source-faithfulness for the legacy Legendre route;
- copying third-party MATLAB code into BayesFilter production modules.

## Local Checks

Phase 2 local checks passed:

- Existing API scan found `ProductBasis`, `LegendreBasis1D`, manifest payload
  helpers, `FixedTTFitConfig`, and `BranchManifest` surfaces.
- Existing fitter inspection found that the core ALS path uses
  `product_basis.evaluate_axis(...)` and `basis_dim`, making a minimal protocol
  plausible.
- Existing payload/quadrature inspection found Legendre-specific surfaces that
  Phase 3 must freeze before implementation.
- No code edits or runtime TensorFlow tests were run.

## Decision

Phase 2 passes as a design contract:

```text
PASS_P85_PHASE2_CONFIG_INTERFACE_XLA_CONTRACT
```

This result authorizes Phase 3 to freeze an exact implementation/test matrix.
It does not authorize code edits by itself.

## Next-Phase Handoff

Phase 3 may begin using:

- `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase3-implementation-test-matrix-subplan-2026-06-23.md`

Phase 3 must freeze exact files, tests, and CPU-hidden commands before any code
edits.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Pass Phase 2 setup API/XLA design. | PASS: setup specs, manifest identity, classifications, and static fields are stated. | PASS: no runtime basis dispatch, no code edits, no fitting/GPU scope, no source overclaim. | Whether implementation can provide enough `Lagrangep` methods without widening Phase 4 too much. | Run Phase 3 implementation/test matrix review. | No implementation, P84 repair, fit quality, XLA performance, correctness, or production readiness. |
