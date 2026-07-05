# P85 Phase 4 Result: Configurable Basis/Domain Implementation

Date: 2026-06-23

Status: `PASS_P85_PHASE4_LOCAL_PENDING_REVIEW`

## Phase Objective

Implement the minimal reviewed BayesFilter-owned setup configuration surface for
legacy bounded Legendre diagnostics and the author SIR
`Lagrangep(4,8)` plus `AlgebraicMapping(1)` configuration.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the local code expose a setup-configurable basis/domain surface that can represent author and legacy diagnostic routes distinctly? |
| Baseline/comparator | Phase 2 design, Phase 3 implementation matrix, and previous Legendre-only behavior. |
| Primary criterion | Targeted CPU-hidden tests pass; manifests distinguish basis/domain configs; legacy diagnostic tests remain compatible or are explicitly updated. |
| Veto diagnostics | TensorFlow GPU use without escalation; dynamic runtime basis dispatch inside compiled paths; missing manifest identity; third-party code copying; source-faithfulness overclaim. |
| Explanatory diagnostics | Basis dimensions, domain-map formulas, branch hashes, test output. |
| Not concluded | No fit quality, posterior correctness, production readiness, HMC readiness, or XLA performance claim. |
| Artifact | This result, Phase 4 code diff, and test summaries below. |

## Skeptical Plan Audit

Phase 4 audit passed after one implementation correction:

- Wrong-baseline risk is controlled. The implementation targets only the P84
  basis/domain setup blocker, not P84 Phase 2 fitting.
- Proxy-promotion risk is controlled. Passing tests prove only setup-manifest
  and basis-unit behavior.
- Source-anchor risk is controlled by emitting both paper/local source-support
  anchors and pinned author-code anchors for the author SIR config.
- Hidden downstream-assumption risk is controlled. The author `Lagrangep`
  object exposes evaluation and derivative methods, but its mass matrix and
  integral vector intentionally raise `NotImplementedError` in P85.
- XLA risk is controlled. Basis family, domain-map family, order, element
  count, cardinality, scale, and dimension remain setup-static manifest
  fields; no runtime tensor-controlled basis switching was added.
- Dirty-worktree risk is controlled. The dirty and excluded
  `bayesfilter/highdim/filtering.py` file was not edited.

## Implementation Summary

Changed files were limited to the Phase 3 approved envelope:

- `bayesfilter/highdim/bases.py`
- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p85_configurable_basis_domain.py`
- this P85 documentation/result path and ledgers/subplans

The code now provides:

- `DomainMapSpec`, `BasisSpec`, and `ProductBasisSpec` setup identities.
- `AlgebraicMap(scale)` with the author algebraic map/inverse/log-density
  formulas.
- `LagrangePiecewiseBasis1D(order, num_elems)` with author-style
  `LagrangeRef` node structure: endpoints plus Jacobi(1,1) interior nodes, and
  piecewise local support.
- `p85_legacy_legendre_product_basis_spec(...)` classified as
  `local_gap` / `diagnostic_legendre_route`.
- `p85_author_sir_lagrangep_algebraic_product_basis_spec(...)` classified as
  `source_faithful` / `sir_config`.
- P59 source-route manifest fields:
  - `basis_domain_config`
  - `author_basis_domain_config_available`
  - `author_basis_domain_config_status`
  - `author_basis_domain_full_fit_status`

## Source And Paper Anchors

The author config manifest includes paper/source-support and author-code
anchors:

- `docs/references.bib:703-710`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-source-support-ledger-2026-06-01.md:18-22`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-paper-code-crosswalk-ledger-2026-05-30.md:16-30`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/README.md:28-41`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:43-55`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/ApproxBases.m:70-119`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Polynomials/Lagrangep.m:12-52`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Domains/AlgebraicMapping.m:5-43`

The paper source support permits the broad TT/piecewise-polynomial basis
context; the concrete `Lagrangep(4,8)` plus `AlgebraicMapping(1)` route is
anchored in the pinned companion source. Phase 4 does not claim paper-scale
fitting or posterior correctness.

## Manifest Behavior

The legacy route remains the fitted P59 diagnostic route:

```text
classification = local_gap
classification_subtype = diagnostic_legendre_route
basis_family = ("legendre",) * 36
domain_map_family = ("bounded_interval",) * 36
```

The author SIR setup is now available as a separate config:

```text
classification = source_faithful
classification_subtype = sir_config
basis_family = ("lagrangep",) * 36
domain_map_family = ("algebraic",) * 36
basis_dim_tuple = (33,) * 36
```

The manifest also records:

```text
author_basis_domain_config_status =
  PASS_P85_AUTHOR_SIR_BASIS_DOMAIN_CONFIG

author_basis_domain_full_fit_status =
  BLOCK_P85_AUTHOR_SIR_BASIS_DOMAIN_FULL_FIT_REQUIRES_DOWNSTREAM_MAPPING_REPAIR
```

## Deliberate Blocks

The author-style `Lagrangep` object is not a full fitting/transport route in
P85:

- `mass_matrix(...)` raises `NotImplementedError`.
- `integral_vector(...)` raises `NotImplementedError`.
- P59 still fits the legacy bounded Legendre diagnostic basis.
- Full algebraic `Lagrangep` fitting remains blocked until downstream density,
  mass/integral, quadrature, and transport conventions are reviewed and
  implemented.

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Branch | `zhaocui-fixed-branch-derivative-validation` |
| Worktree state | Dirty before and after Phase 4; unrelated dirty files preserved. |
| Conda/env | Existing `tf-gpu` environment implied by TensorFlow import paths. |
| TensorFlow | `2.19.1` |
| CPU/GPU status | CPU-only by explicit `CUDA_VISIBLE_DEVICES=-1` for TensorFlow tests. |
| Data version | N/A; no dataset or fitting ladder run. |
| Random seeds | N/A; deterministic unit/regression tests only. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-subplan-2026-06-23.md` |
| Result file | This file. |
| Output artifacts | Code diff, tests, this result, ledgers, and refreshed Phase 5 subplan. |

## Local Checks

Required Phase 4 checks passed:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p85_configurable_basis_domain.py
```

Result:

```text
9 passed, 2 warnings in 5.11s
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p59_author_sir_36d_target_fit.py
```

Result:

```text
4 passed, 2 warnings in 6.58s
```

```bash
git diff --check -- bayesfilter/highdim/bases.py bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p85_configurable_basis_domain.py docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-result-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-execution-ledger-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-stop-handoff-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-claude-review-ledger-2026-06-23.md
```

Result:

```text
PASS
```

## Decision

Phase 4 passes locally:

```text
PASS_P85_PHASE4_CONFIGURABLE_BASIS_DOMAIN_IMPLEMENTATION_LOCAL
```

This closes the narrow setup-surface part of the P84 Phase 1 blocker locally:
BayesFilter can now represent the author SIR basis/domain configuration and
the legacy diagnostic basis/domain configuration as distinct setup identities.

It does not close full author algebraic `Lagrangep` fitting or any production
gate.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Pass Phase 4 locally pending review. | PASS: targeted tests and manifest distinctions pass. | PASS: no GPU/fitting/HMC/LEDH run; no runtime basis switching; no third-party code copied; mass/integral blocked. | Whether Phase 5 manifest review finds wording or classification gaps. | Run Claude bounded review of this result, then Phase 5 manifest classification checks if agreed. | No fit quality, posterior correctness, full P84 Phase 2 readiness, HMC readiness, XLA performance, scaling, or production readiness. |

## Next-Phase Handoff

Phase 5 may begin only after bounded Claude review of this result agrees or any
fixable issue is patched and rechecked within the P85 repair loop.

The refreshed next subplan is:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-subplan-2026-06-23.md
```
