# BayesFilter NeuTra Real Target HMC Smoke Phase 0 Subplan

Date: 2026-07-06

## Phase Objective

Freeze the launch contract for the real-target NeuTra program: scope, evidence,
review protocol, approval boundaries, and handoff into Phase 1 inventory.

## Entry Conditions Inherited From Previous Phase

- The prior c603 import/mechanics fixture program is closed.
- c603 target signature and transport hashes are recorded.
- No real Rotemberg/c603 target adapter has been accepted yet.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-master-program-2026-07-06.md`.
- Phase 1 subplan:
  `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase1-target-authority-inventory-subplan-2026-07-06.md`.
- Visible runbook, ledger, and stop handoff.
- Launch review bundle under `docs/reviews/`.

## Required Checks/Tests/Reviews

- Local text checks that required planning artifacts exist and contain required
  headings.
- Bounded Claude read-only launch review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the new real-target NeuTra/HMC-smoke program scoped, bounded, and safe to enter Phase 1 inventory? |
| Baseline/comparator | Closed c603 import/mechanics fixture program and existing BayesFilter target-builder/fixed-transport surfaces. |
| Primary criterion | Required planning artifacts exist, name approval/stop conditions, preserve nonclaims, and Phase 1 has exact handoff conditions. |
| Veto diagnostics | Missing subplan headings, hidden HMC/training/GPU launch, unclear review authority, or unsupported HMC/posterior/product claims. |
| Explanatory diagnostics | Review status and text-check output. |
| Not concluded | No real target adapter correctness, no mechanics pass, no HMC readiness. |
| Artifact | Phase 0 result note and launch review record. |

## Forbidden Claims/Actions

- Do not implement target code in Phase 0.
- Do not run HMC, GPU, or training.
- Do not claim that c603 fixture mechanics proves real target readiness.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- launch artifacts pass local text checks;
- review returns `VERDICT: AGREE` or a bounded fallback agreement is explicitly
  recorded as weaker evidence;
- Phase 1 inventory scope is exact and read-only.

## Stop Conditions

Stop if planning artifacts are missing required headings, if review does not
converge after five rounds for the same material blocker, or if Phase 1 would
need network/GPU/training/HMC before inventory.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 0 result;
3. draft or refresh Phase 1 subplan;
4. review Phase 1 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
