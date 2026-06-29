# P85 Phase 5 Result: Manifest Classification And Regression Checks

Date: 2026-06-23

Status: `PASS_P85_PHASE5_MANIFEST_CLASSIFICATION_REGRESSION`

## Phase Objective

Verify that manifests and regression tests preserve route classification:
legacy bounded Legendre remains a local diagnostic gap, while the author SIR
`Lagrangep(4,8)` plus `AlgebraicMapping(1)` setup is represented as an
author-source configuration surface.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Do manifests preserve the intended distinction between author setup and diagnostic/adaptation setup? |
| Baseline/comparator | P84 blocker language, Phase 4 implementation, existing P59 nonclaims. |
| Primary criterion | Tests and manifest examples show route classification fields and preserve nonclaims where appropriate. |
| Veto diagnostics | Legacy route silently reclassified as source-faithful; author route lacks source anchors; tests rely on fitting loss; production claims appear. |
| Explanatory diagnostics | Manifest payloads, branch hashes, basis dimensions, classification string scans. |
| Not concluded | No fit quality, correctness, HMC readiness, LEDH agreement, scaling, or production readiness. |
| Artifact | This Phase 5 result and refreshed Phase 6 subplan. |

## Skeptical Plan Audit

Phase 5 audit passed:

- Wrong-baseline risk is controlled. The phase compares manifest/classification
  behavior against P84/P85 blocker language and Phase 4, not against fit loss.
- Proxy-promotion risk is controlled. Classification metadata is treated as
  route-governance evidence only.
- Hidden-assumption risk is controlled by preserving the legacy
  `no AlgebraicMapping(1) parity claim` and full author-fit block.
- Environment risk is controlled by running TensorFlow tests with
  `CUDA_VISIBLE_DEVICES=-1`.
- Artifact risk is controlled by recording both broad and focused scans.

## Manifest Classification Evidence

The P85 tests assert the route split directly:

```text
legacy["classification"] == "local_gap"
legacy["classification_subtype"] == "diagnostic_legendre_route"
author["classification"] == "source_faithful"
author["classification_subtype"] == "sir_config"
author["basis_dim_tuple"] == (33,) * 36
```

The source-route manifest keeps the fitted legacy path and the available author
setup config separate:

```text
basis_domain_config
author_basis_domain_config_available
author_basis_domain_config_status
author_basis_domain_full_fit_status
```

The author setup status remains:

```text
PASS_P85_AUTHOR_SIR_BASIS_DOMAIN_CONFIG
```

The full-fit status remains blocked:

```text
BLOCK_P85_AUTHOR_SIR_BASIS_DOMAIN_FULL_FIT_REQUIRES_DOWNSTREAM_MAPPING_REPAIR
```

## Regression Evidence

The existing P59 regression still asserts the historical nonclaim:

```text
no AlgebraicMapping(1) parity claim
```

The new P85 regression asserts:

- bounded and algebraic `DomainMapSpec` payloads;
- algebraic map formula and inverse;
- author `Lagrangep(4,8)` config has 33 basis functions across 36 axes;
- author-style Jacobi(1,1) interior nodes for local Lagrange elements;
- piecewise local support rather than one global degree-32 basis;
- `Lagrangep` mass matrix and integral vector remain blocked in P85;
- legacy bounded Legendre remains `local_gap`/`diagnostic_legendre_route`;
- P59 manifest distinguishes fitted legacy config from available author config.

## Local Checks

Required Phase 5 regression check passed:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p85_configurable_basis_domain.py tests/highdim/test_p59_author_sir_36d_target_fit.py
```

Result:

```text
13 passed, 2 warnings in 7.44s
```

Required broad classification scan ran:

```bash
rg -n "basis_family|domain_map|classification|source_faithful|fixed_hmc_adaptation|extension_or_invention|no AlgebraicMapping\\(1\\) parity claim" bayesfilter/highdim tests/highdim docs/plans -S
```

Result:

```text
PASS_AS_SCAN_EXECUTED_WITH_TRUNCATED_OUTPUT
```

The repository has many older Zhao-Cui/doc classification artifacts, so the
broad scan output exceeded the command capture budget. It is explanatory
evidence only and did not reveal a P85 veto before truncation.

Focused P85 scan also ran:

```bash
rg -n "basis_family|domain_map|classification|source_faithful|fixed_hmc_adaptation|extension_or_invention|no AlgebraicMapping\\(1\\) parity claim|author_basis_domain" bayesfilter/highdim/bases.py bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p85_configurable_basis_domain.py tests/highdim/test_p59_author_sir_36d_target_fit.py docs/plans/bayesfilter-highdim-zhao-cui-p85-* -S
```

Focused scan found the expected P85 classification evidence in:

- `bayesfilter/highdim/bases.py`
- `bayesfilter/highdim/source_route.py`
- `tests/highdim/test_p85_configurable_basis_domain.py`
- `tests/highdim/test_p59_author_sir_36d_target_fit.py`
- P85 Phase 1-5 result/subplan/ledger artifacts

Documentation/code hygiene check passed:

```bash
git diff --check -- bayesfilter/highdim/bases.py bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p85_configurable_basis_domain.py docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-result-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-phase6-p84-handoff-reset-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-execution-ledger-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-stop-handoff-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-claude-review-ledger-2026-06-23.md
```

Result:

```text
PASS
```

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Branch | `zhaocui-fixed-branch-derivative-validation` |
| Worktree state | Dirty; unrelated dirty files preserved. |
| CPU/GPU status | CPU-only by explicit `CUDA_VISIBLE_DEVICES=-1` for TensorFlow tests. |
| Data version | N/A; no dataset or fitting ladder run. |
| Random seeds | N/A; deterministic tests and text scans only. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-subplan-2026-06-23.md` |
| Result file | This file. |

## Decision

Phase 5 passes:

```text
PASS_P85_PHASE5_MANIFEST_CLASSIFICATION_REGRESSION
```

The manifest classification is now review-ready for Phase 6 handoff:

- the fitted legacy diagnostic route remains `local_gap`;
- the available author setup config is `source_faithful`/`sir_config`;
- the legacy `no AlgebraicMapping(1) parity claim` remains intact;
- full author algebraic `Lagrangep` fitting remains blocked.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Pass Phase 5 manifest classification. | PASS: tests and focused scan show legacy/author distinction and preserved nonclaims. | PASS: no legacy source-faithful reclassification; author config has anchors; no fit/production claims. | Phase 6 must word the P84 handoff without overstating Phase 2 readiness. | Write Phase 6 handoff/reset artifacts. | No fit quality, correctness, HMC readiness, LEDH agreement, scaling, or production readiness. |

## Next-Phase Handoff

Phase 6 may begin using:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p85-phase6-p84-handoff-reset-subplan-2026-06-23.md
```

Phase 6 must not run P84 Phase 2 fitting or claim production readiness.
