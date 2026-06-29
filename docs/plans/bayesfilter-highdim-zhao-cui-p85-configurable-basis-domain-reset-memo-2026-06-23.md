# P85 Reset Memo: Configurable Basis/Domain Repair

Date: 2026-06-23

Status: `PARTIAL_P85_P84_PHASE1_BASIS_DOMAIN_REPAIR`

## Short Answer

P85 repaired the representation/configuration break: Zhao-Cui SIR can now be
declared as author `Lagrangep(4,8)` plus `AlgebraicMapping(1)`, while the old
bounded Legendre fitted diagnostic route is still labeled as a local gap.

P85 did not make the author algebraic `Lagrangep` route production-fit-ready.
Mass matrices, integral vectors, downstream squared-density conventions,
quadrature, and transport/fitting wiring remain open.

## Main Artifacts

- Master program:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-configurable-basis-domain-master-program-2026-06-23.md`
- Runbook:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-gated-execution-runbook-2026-06-23.md`
- Phase 4 implementation result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-result-2026-06-23.md`
- Phase 5 manifest result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-result-2026-06-23.md`
- Phase 6 handoff result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase6-p84-handoff-reset-result-2026-06-23.md`

## Code And Tests

Implemented in:

- `bayesfilter/highdim/bases.py`
- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p85_configurable_basis_domain.py`

Key code behavior:

- New setup specs: `DomainMapSpec`, `BasisSpec`, `ProductBasisSpec`.
- New algebraic map: `AlgebraicMap(scale=1)`.
- New author-style setup builder:
  `p85_author_sir_lagrangep_algebraic_product_basis_spec(...)`.
- New legacy diagnostic setup builder:
  `p85_legacy_legendre_product_basis_spec(...)`.
- New P59 manifest fields distinguish fitted legacy config from available
  author config.
- `LagrangePiecewiseBasis1D` uses piecewise local Lagrange support and
  author-style Jacobi(1,1) interior nodes.
- `LagrangePiecewiseBasis1D.mass_matrix(...)` and
  `integral_vector(...)` intentionally raise `NotImplementedError` in P85.

## Evidence

Final relevant checks:

```text
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p85_configurable_basis_domain.py
9 passed
```

```text
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p59_author_sir_36d_target_fit.py
4 passed
```

```text
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p85_configurable_basis_domain.py tests/highdim/test_p59_author_sir_36d_target_fit.py
13 passed
```

Claude bounded reviews:

- Master program: `VERDICT: AGREE`.
- Phase 1 inventory: `VERDICT: REVISE`, repaired, then `VERDICT: AGREE`.
- Phase 2 config/XLA design: `VERDICT: AGREE`.
- Phase 3 implementation/test matrix: `VERDICT: REVISE`, repaired, then
  `VERDICT: AGREE`.
- Phase 4 implementation result: `VERDICT: AGREE`.

## P84 Handoff

Use this status:

```text
PARTIAL_P85_P84_PHASE1_BASIS_DOMAIN_REPAIR
```

Meaning:

- The author basis/domain setup can now be represented and manifested.
- The legacy fitted route is still bounded Legendre and remains diagnostic.
- P84 Phase 2 production-relevant fitting remains blocked until the author
  algebraic `Lagrangep` mass/integral/downstream mapping gap is repaired or a
  reviewed fixed-HMC adaptation contract explicitly accepts a narrower target.

## Forbidden Future Shortcut

Do not say "Zhao-Cui can handle SIR in production" from P85 alone.

Do not launch P84 Phase 2 fitting from P85 alone.

Do not remove the legacy `no AlgebraicMapping(1) parity claim` from the fitted
diagnostic route unless a later reviewed result actually wires author
algebraic fitting.

## Next Smallest Repair

The smallest useful next repair is not another manifest edit. It is a dedicated
subplan for the algebraic author route downstream gap:

- exact `Lagrangep` mass matrix and integral vector implementation;
- algebraic-domain density/mass convention;
- squared-density normalizer and marginal contractions under that convention;
- fitting/transport blockers or tests;
- then a renewed decision on whether P84 Phase 2 may launch.
