# P85 Phase 5 Subplan: Manifest Classification And Regression Checks

Date: 2026-06-23

Status: `DRAFT_READY_PENDING_PHASE4_REVIEW`

## Phase Objective

Verify that manifests and regression tests preserve route classification:
legacy Legendre remains diagnostic/adaptation unless explicitly approved, while
author `Lagrangep(4,8)` plus `AlgebraicMapping(1)` is represented as an
author-source configuration surface.

## Entry Conditions Inherited From Previous Phase

- Phase 4 has implemented or precisely blocked the configurable basis/domain
  surface.
- Phase 4 test and review evidence is recorded.
- P84 Phase 2 fitting remains blocked.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-result-2026-06-23.md`
- Manifest examples or JSON snippets showing legacy and author configurations.
- Updated or new regression tests from the Phase 3/4 matrix.
- Refreshed Phase 6 subplan.

## Required Checks / Tests / Reviews

Required checks:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p85_configurable_basis_domain.py tests/highdim/test_p59_author_sir_36d_target_fit.py
```

```bash
rg -n "basis_family|domain_map|classification|source_faithful|fixed_hmc_adaptation|extension_or_invention|no AlgebraicMapping\\(1\\) parity claim" bayesfilter/highdim tests/highdim docs/plans -S
```

Documentation hygiene check:

```bash
git diff --check -- bayesfilter/highdim/bases.py bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p85_configurable_basis_domain.py docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-result-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-phase6-p84-handoff-reset-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-execution-ledger-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-stop-handoff-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p85-claude-review-ledger-2026-06-23.md
```

Claude read-only review is required if Phase 5 changes any source-faithfulness
language beyond quoting Phase 4.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Do manifests preserve the intended distinction between author setup and diagnostic/adaptation setup? |
| Baseline/comparator | P84 blocker language, Phase 4 implementation, existing P59 nonclaims. |
| Primary criterion | Tests and manifest examples show route classification fields and preserve nonclaims where appropriate. |
| Veto diagnostics | Legacy route silently reclassified as source-faithful; author route lacks source anchors; tests rely on fitting loss; production claims appear. |
| Explanatory diagnostics | Manifest payloads, branch hashes, basis dimensions, classification string scans. |
| Not concluded | No fit quality, correctness, HMC readiness, LEDH agreement, scaling, or production readiness. |
| Artifact | Phase 5 result and refreshed Phase 6 subplan. |

## Forbidden Claims / Actions

- Do not use classification metadata as fit-quality evidence.
- Do not remove diagnostic nonclaims unless a reviewed result justifies it.
- Do not run fitting, GPU, HMC, LEDH, d=50/d=100, or long commands.
- Do not change default production policy.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if:

- manifest classification is reviewed;
- legacy and author routes are distinguishable;
- any remaining nonclaims are explicit;
- P84 handoff language can be written without overclaiming.

## Stop Conditions

Stop if:

- manifests cannot distinguish route classes;
- regression tests break existing diagnostic behavior without a reviewed
  replacement;
- source-faithfulness wording becomes unsupported.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 5 result / close record;
3. draft or refresh the Phase 6 subplan;
4. review the Phase 6 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
