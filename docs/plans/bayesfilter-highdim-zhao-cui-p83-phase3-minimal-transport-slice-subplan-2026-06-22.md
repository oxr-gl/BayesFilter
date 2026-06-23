# P83 Phase 3 Subplan: Minimal Source-Route Transport Slice

Date: 2026-06-22

Status: `READY_AFTER_PHASE2_REVIEW`

## Phase Objective

Implement the smallest source-route transport slice needed for honest two-step
retained-object mechanics:

- explicit metadata for the current fixed-TTSIRT transport marginal/KR/proposal
  semantics;
- a focused readiness/metadata gate or equivalent tests;
- positive-defensive-mass fixture checks;
- proposal correction through `eval_pdf`;
- retained-object carry across two steps without claiming production KR closure.

## Entry Conditions Inherited From Previous Phase

Phase 3 may begin only after Phase 2 passes local checks and read-only review.

Inherited boundaries:

- current numerical CDF-grid KR path is not production source-route closure;
- tensor-product suffix-grid conditional integration is not production
  Proposition-2/KR evidence;
- base/reference-density-only proposal correction is forbidden;
- d=18/LEDH/GPU/numerical validation is not authorized;
- unrelated dirty worktree changes must be preserved.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase3-minimal-transport-slice-result-2026-06-22.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md`
- Draft/refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase4-analytical-derivative-audit-subplan-2026-06-22.md`

## Required Checks / Tests / Reviews

Focused local checks after implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p83_minimal_source_route_transport_slice.py \
  tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py \
  tests/highdim/test_p57_m3_proposition2_marginalization.py \
  tests/highdim/test_p57_m5_proposal_density_retained_sampling.py \
  tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/transport.py \
  bayesfilter/highdim/source_route.py \
  tests/highdim/test_p83_minimal_source_route_transport_slice.py

git diff --check -- \
  bayesfilter/highdim/transport.py \
  bayesfilter/highdim/source_route.py \
  tests/highdim/test_p83_minimal_source_route_transport_slice.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase3-minimal-transport-slice-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase3-minimal-transport-slice-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase4-analytical-derivative-audit-subplan-2026-06-22.md
```

CPU-only note: these are deliberately small CPU-only tests with
`CUDA_VISIBLE_DEVICES=-1`; they are not GPU/default performance evidence.

Review:

- Codex skeptical implementation audit before edits.
- Claude read-only review of compact implementation diff/result and Phase 4
  subplan when material.
- Repair loop up to five rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the minimal fixed-TTSIRT source-route transport slice honestly expose retained-marginal/proposal mechanics while blocking silent grid/base-density promotion? |
| Baseline/comparator | Phase 2 design, P57-M2/M3/M5/M6 tests, P56/P61 source anchors, and author `full_sol`/`SIRT`/`@TTSIRT` operations. |
| Primary pass criterion | Metadata/readiness/tests distinguish paired-core marginal evaluation, numerical CDF-grid approximation, positive defensive mass, `eval_pdf` proposal correction, and two-step retained-object carry. |
| Veto diagnostics | Base-density-only proposal passes; zero defensive mass passes P83 slice; tensor-product suffix-grid or old local/operator route passes as source closure; numerical CDF-grid path is described as production KR closure; `production_kr_closure` is anything other than false/non-production for the current grid-CDF route; unsupported d=18/LEDH/HMC claims. |
| Explanatory diagnostics | Focused pytest, compileall, `git diff --check`, metadata payloads, and review notes. |
| Not concluded | No production KR closure, no d=18 correctness, no author-scale fit quality, no derivative readiness, no LEDH readiness, no HMC readiness. |
| Artifact preserving result | Phase 3 result and focused tests. |

## Forbidden Claims / Actions

- Do not run GPU, LEDH, d=18, fitting ladders, or numerical validation jobs.
- Do not implement broad KR replacement.
- Do not refactor unrelated code.
- Do not make NumPy a BayesFilter-owned algorithmic backend.
- Do not change default project policy.
- Do not claim production source-faithfulness, exact likelihood correctness,
  posterior correctness, HMC readiness, or scaling.

## Exact Next-Phase Handoff Conditions

P83-4 may begin only if:

- Phase 3 focused tests pass;
- Phase 3 result preserves nonclaims;
- Phase 4 subplan exists and is audit-first;
- Phase 4 treats ForwardAccumulator/JVP/FD as diagnostic-only unless it finds or
  wires a source-backed same-branch analytical route;
- Claude review agrees or non-material comments are resolved.

## Stop Conditions

Stop with a Phase 3 blocker result if:

- honest metadata/readiness cannot be added without broad refactor;
- existing dirty code conflicts make a scoped patch unsafe;
- positive defensive mass breaks minimal mechanics and requires a larger design;
- only base/reference-density proposal correction is available;
- tests cannot reject grid/operator substitutes;
- Claude and Codex do not converge after five rounds for the same blocker.
