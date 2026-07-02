# Phase 4 Subplan: Spatial SIR d18 Full Observed-Data Filtering Route

Date: 2026-07-01

Status: `DRAFT_PENDING_PHASE3_REVIEW`

## Phase Objective

Build or precisely block the full observed-data/filtering Zhao-Cui row for
`zhao_cui_spatial_sir_austria_j9_T20`, without promoting the P91 local
complete-data component as a full likelihood.

## Entry Conditions Inherited From Previous Phase

- Phase 3 closed generalized-SV Zhao-Cui status.
- P91 local complete-data component evidence remains available as sidecar
  evidence only.
- Preserved blockers include previous-marginal derivative, fixed-TTSIRT
  proposal/transport derivative, and full source-route FD not claimed.

## Required Artifacts

- Full observed-data/filtering target contract or blocker note.
- Derivative ownership design for previous marginal and fixed-TTSIRT
  proposal/transport, if implementation proceeds.
- Code/tests if a full route is implemented.
- Regenerated leaderboard if status changes.
- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase4-sir-full-filtering-result-2026-07-01.md`
- Refreshed Phase 5 subplan.

## Required Checks, Tests, Reviews

- Boundary test that P91 local complete-data component is not reported as full
  observed-data/filtering likelihood.
- Finite full-filtering value check if implemented.
- Manual analytical score same-scalar checks if implemented.
- FD consistency and score-at-true multi-seed calibration if implemented.
- Claude read-only review of target/derivative design and result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can SIR d18 move from local complete-data sidecar to full observed-data/filtering Zhao-Cui leaderboard row? |
| Baseline/comparator | P91 sidecar plus current full-filtering blocker list. |
| Primary criterion | Either full filtering row has finite value plus optional manual score under reviewed derivative ownership, or the row remains blocked with exact missing derivative/evaluator items. |
| Veto diagnostics | Local complete-data score reported as full filtering score; no free theta; autodiff analytical score; missing previous-marginal derivative; missing fixed-TTSIRT proposal/transport derivative; FD treated as oracle. |
| Explanatory diagnostics | FD residual, expected-score mean, runtime, GPU/XLA compile. |
| Not concluded | No exact likelihood correctness, posterior correctness, or source-faithful adaptive TT reproduction. |
| Artifact | Phase 4 result and regenerated leaderboard if changed. |

## Forbidden Claims And Actions

- Do not promote P91 local component to a full filtering row.
- Do not erase preserved P91 caveats.
- Do not make source-faithfulness claims without paper/source anchors.
- Do not call ForwardAccumulator/JVP or tape routes analytical.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 if SIR full-filtering status is admitted or precisely
blocked, with sidecar evidence preserved and not overclaimed.

## Stop Conditions

Stop if completing the full route requires a scientific/product direction not
already approved, or if derivative ownership cannot be stated without
unsupported invention.

## End-of-Subplan Protocol

1. Run the required local checks.
2. Write the Phase 4 result / close record.
3. Draft or refresh the Phase 5 subplan.
4. Review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
