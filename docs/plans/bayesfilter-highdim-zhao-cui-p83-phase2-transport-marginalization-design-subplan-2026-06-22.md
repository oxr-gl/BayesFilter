# P83 Phase 2 Subplan: Transport And Proposition-2 Marginalization Design

Date: 2026-06-22

Status: `REFRESHED_AFTER_PHASE1_INVENTORY_PENDING_REVIEW`

## Phase Objective

Design the narrow production repair for the documented fixed-TTSIRT
retained-object source route.  The design must cover fixed TT/SIRT core
representation, squared-TT defensive density, normalizer semantics,
Proposition-2 mass-matrix/QR marginalization, `eval_pdf`/potential semantics,
forward/inverse/conditional KR APIs, proposal-correction denominator,
retained-object manifest, and fixed branch identity.

Phase 1 identified a real source-route substrate and one central design risk:
`FixedTTSIRTTransport` exposes the required map surface, but its conditional
CDF/inversion implementation uses numerical grids over marginal ratios.  Phase
2 must decide whether that is only a diagnostic lower rung, a reviewed
fixed-HMC approximation with an explicit error/veto contract, or a path that
must be replaced before production source-route claims.

## Entry Conditions Inherited From Previous Phase

P83-2 may begin only after P83-1 passes local checks and review and records:

- complete enough inventory table to identify repair scope;
- code/test anchors for relevant local components;
- paper/project anchors where applicable;
- author-source anchors where applicable;
- classifications for all rows;
- no unanchored `source_faithful` labels;
- a reviewed handoff saying Phase 2 design is the next narrow action.

## Required Artifacts

- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md`
- Phase 2 design result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-result-2026-06-22.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md`
- Draft/refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase3-minimal-transport-slice-subplan-2026-06-22.md`

## Required Checks / Tests / Reviews

Local design checks after refresh:

```bash
rg -n "fixed TT|TTSIRT|defensive|normalizer|Proposition-2|Proposition 2|mass-matrix|QR|eval_pdf|potential|forward|inverse|conditional|KR|proposal|retained|branch" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-result-2026-06-22.md -S

rg -n "tensor-product grid|base-density-only|extension_or_invention|source_faithful|fixed_hmc_adaptation|BLOCK_SOURCE_UNGROUNDED" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-result-2026-06-22.md -S

git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase3-minimal-transport-slice-subplan-2026-06-22.md
```

Review:

- Codex skeptical design audit before any implementation.
- Claude read-only review of compact Phase 2 design fact packet.
- Repair loop up to five rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What is the narrow source-backed transport and marginalization repair design needed before implementation? |
| Baseline/comparator | P83-1 inventory, P56/P61 source anchors, P57-M2 contract, P57-M6 retained-object loop, P58-M9 readiness guard, and Zhao-Cui author `full_sol`, `SIRT`, `AbstractIRT`, and `@TTSIRT` operations. |
| Primary pass criterion | Design names each required operation, cites local inventory status and source anchors, gives an explicit classification for the current numerical CDF-grid map path, rejects base-density substitutes, defines focused tests for Phase 3, and preserves nonclaims. |
| Veto diagnostics | Design silently treats numerical CDF-grid conditionals as production source-route closure without an approximation/error contract; design relies on tensor-product suffix-grid integration; proposal correction denominator is base/reference density only; missing defensive density/normalizer; missing Proposition-2 marginalization; missing KR APIs; unanchored source-faithful labels. |
| Explanatory diagnostics | Anchor tables, API sketches, invariant lists, planned test matrix, and review comments. |
| Not concluded | No code implementation, no numerical correctness, no d=18 validation, no derivative readiness, no LEDH readiness. |
| Artifact preserving result | Phase 2 design result and refreshed Phase 3 subplan. |

## Forbidden Claims / Actions

- Do not implement code in Phase 2.
- Do not run numerical or GPU jobs.
- Do not claim source-route implementation readiness.
- Do not accept tensor-product grid conditional integration as the production
  Proposition-2 route.
- Do not silently accept the current numerical CDF-grid KR path as production
  source-route closure; either classify it as diagnostic, give a reviewed
  approximation/error contract, or design a replacement.
- Do not accept base/reference-density-only proposal correction as author
  `eval_pdf` semantics.
- Do not promote any route without paper/project and author-source anchors.

## Required Design Topics

- Fixed TT/SIRT core representation and branch metadata.
- Defensive density `phi^2 + tau * lambda` and positive defensive mass policy.
- Normalizer and log normalizer semantics.
- Proposition-2 mass-matrix/QR retained-object marginalization.
- Difference between paired-core marginal evaluation, tensor-product suffix-grid
  conditional integration, and author CDF-constructor semantics.
- `eval_pdf`, potential, and proposal log-density semantics.
- Forward KR, inverse KR, and conditional inverse KR APIs.
- Affine frame and determinant placement.
- Proposal correction denominator and sign.
- Retained-object manifest fields and source-route branch identity.
- Focused Phase 3 tests that reject grid/base-density substitutes.

## Exact Next-Phase Handoff Conditions

P83-3 may begin only if:

- Phase 2 design passes local checks and read-only review;
- Phase 3 subplan exists and names the smallest implementable transport slice;
- Phase 3 tests are scoped to transport contract, marginalization, proposal
  correction, and two-step retained-object mechanics;
- Phase 3 explicitly tests that source-route proposal correction cannot degrade
  to base/reference density and that marginal/KR semantics are not silently
  served by the old diagnostic grid route;
- Phase 3 explicitly forbids d=18 validation and broad refactors.

## Stop Conditions

Stop with a Phase 2 blocker result if:

- author-source anchors do not support the proposed operation;
- the design cannot avoid tensor-product grid or base-density-only substitutes;
- the inventory shows missing prerequisites that must be resolved first;
- Claude and Codex do not converge after five rounds for the same blocker;
- continuing requires implementation, package/network work, GPU runs, or
  project-boundary changes not authorized by Phase 2.
