# P86 Phase 2 Subplan: Algebraic Measure Contract

Date: 2026-06-24

Status: `REVIEWED_READY_FOR_EXECUTION`

## Phase Objective

Freeze and test the algebraic-domain measure convention for the author SIR
route so downstream densities, normalizers, integrals, and samples cannot
silently mix physical and reference measures.

## Entry Conditions Inherited From Previous Phase

- Phase 1 passed as
  `PASS_P86_PHASE1_LAGRANGEP_MASS_INTEGRAL_REVIEWED`.
- The author `AlgebraicMapping(1)` formulas are inspected.
- No fitting or production-relevant runtime command is authorized.

## Required Artifacts

- Measure-convention contract note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-algebraic-measure-contract-2026-06-24.md`
- Focused tests for `AlgebraicMap` Jacobian/log-density direction and
  convention compatibility:
  `tests/highdim/test_p86_algebraic_measure_contract.py`
- Any minimal code change needed to expose manifest fields or assertions.
- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase2-algebraic-measure-contract-result-2026-06-24.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`
- Refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase3-downstream-author-route-wiring-subplan-2026-06-24.md`

## Required Checks / Tests / Reviews

- Inspect `AlgebraicMapping.m:5-43` and local `MeasureConvention` enums.
- Contract note and tests must pin these exact one-dimensional identities for
  `z = T(x) = (x/s)/sqrt(1 + (x/s)^2)` and
  `x = T^{-1}(z) = s*z/sqrt(1-z^2)`:
  - `dz/dx = (1 + (x/s)^2)^(-3/2) / s`;
  - `dx/dz = s * (1 - z^2)^(-3/2)`;
  - `domain_to_reference_log_density(x)` returns `log |dz/dx|`;
  - `reference_to_domain_log_density(z)` returns `log |dx/dz|`;
  - if a physical density `p_X(x)` is transformed to a reference density, the
    reference density is `p_Z(z) = p_X(T^{-1}(z)) * |dx/dz|`;
  - if a reference density `p_Z(z)` is transformed to a physical density, the
    physical density is `p_X(x) = p_Z(T(x)) * |dz/dx|`;
  - Phase 2 does not choose a production physical-density default; it only
    freezes naming and manifest rules for the author-route contract.
- CPU-hidden tests for:
  - `to_reference`/`from_reference` inverse behavior;
  - `domain_to_reference_log_density` and
    `reference_to_domain_log_density`;
  - the two density-transform identities above on a scalar Gaussian fixture;
  - manifest preservation of density and mass measure names;
  - rejection or clear nonclaim for unsupported mixed conventions.
- Exact CPU-hidden test command after implementation:
  `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p86_algebraic_measure_contract.py tests/highdim/test_p85_configurable_basis_domain.py`
- If the focused test path changes, this subplan must be patched and rereviewed
  before execution.
- `git diff --check -- bayesfilter/highdim tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p86*.md`
- Claude read-only bounded review of the Phase 2 contract/result is required.
  This phase is downstream-interpretation-sensitive by definition.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What measure does the author algebraic `Lagrangep` route use for basis mass, density evaluation, and physical/reference density transforms? |
| Baseline/comparator | Author `AlgebraicMapping.m`, author `Lagrangep` reference-domain mass, P85 `MeasureConvention`, and local downstream mass calls. |
| Primary criterion | A reviewed contract and focused tests prevent reference/physical Jacobian confusion before fitting. |
| Veto diagnostics | Silent physical/reference measure mismatch; unsupported mixed convention accepted; Jacobian direction reversed; manifest omits convention; proxy smoke promoted to correctness. |
| Explanatory diagnostics | Jacobian formula checks, inverse-map residuals, convention manifest snapshots. |
| Not concluded | No fit quality, posterior correctness, KR closure, HMC readiness, or production readiness. |
| Artifact | Phase 2 result and measure-convention contract. |

## Forbidden Claims / Actions

- Do not run fitting, GPU, HMC, LEDH, d=50/d=100, or long commands.
- Do not decide production policy or default measure policy beyond the author
  route contract.
- Do not claim author-route correctness from Jacobian formula tests alone.
- Do not treat Phase 2 as approval for all downstream P84/P86 paths, all
  mass/integral consumers, any global default policy, or physical/reference
  equivalence beyond the tested author-route contract.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- the algebraic measure convention is recorded and tested, or the unresolved
  ambiguity is written as a blocker;
- downstream code paths that depend on `mass_matrix`, `integral_vector`,
  defensive density, normalizer, marginalization, quadrature, or transport are
  listed for Phase 3;
- Phase 3 subplan is refreshed and reviewed.

## Stop Conditions

Stop if:

- the author source and local convention cannot be reconciled without a human
  scientific decision;
- the required physical/reference density identity cannot be written
  unambiguously from `AlgebraicMapping.m:5-43` and local naming;
- changing the convention would alter default policy;
- Claude and Codex do not converge after five review rounds.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 2 result / close record;
3. draft or refresh the Phase 3 subplan;
4. review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
