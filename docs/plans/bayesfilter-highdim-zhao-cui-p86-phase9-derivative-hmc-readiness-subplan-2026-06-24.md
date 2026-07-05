# P86 Phase 9 Subplan: Derivative And HMC Readiness

Date: 2026-06-24

Status: `DRAFT_BLOCKED_PENDING_PHASE8_AND_APPROVAL`

## Phase Objective

Repair or block derivative readiness for the author-route candidate and, if
in scope and approved, evaluate HMC/NUTS readiness under predeclared sampler
diagnostics.

## Entry Conditions Inherited From Previous Phase

- Phase 8 KR/transport status is recorded.
- Same-branch author-route scalar value/gradient target is frozen.
- Exact HMC/MCMC commands, seeds, runtime posture, and artifacts require human
  approval before execution.

## Required Artifacts

- Derivative contract and focused tests if repaired.
- HMC diagnostics manifest if HMC is approved and run.
- Phase 9 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase9-derivative-hmc-readiness-result-2026-06-24.md`
- Updated execution ledger and refreshed Phase 10 subplan.

## Required Checks / Tests / Reviews

- Inventory `ForwardAccumulator`, JVP, finite-difference, analytical
  derivative, same-branch, and author-route derivative code paths.
- CPU-hidden derivative tests for finite values and shape/branch consistency.
- If HMC is in scope, predeclare divergence, R-hat, ESS, nonfinite gradient,
  and chain-length vetoes.
- Claude review is required before claiming derivative readiness or HMC
  readiness.
- Explicit human approval is required before any HMC/MCMC command.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the author-route candidate derivative-ready, and if approved, sampler-ready for HMC/NUTS under stated diagnostics? |
| Baseline/comparator | P83/P84 derivative blocker, author-route value path, Phase 8 KR status, and predeclared sampler diagnostics. |
| Primary criterion | Analytical or reviewed derivative route is implemented/identified and tested; if HMC runs, no sampler vetoes occur under declared uncertainty scope. |
| Veto diagnostics | FD/JVP promoted as analytical readiness; branch mismatch; nonfinite gradient; divergences; failed R-hat/ESS; short-chain overclaim; unapproved HMC command. |
| Explanatory diagnostics | FD/JVP comparisons, gradient norms, acceptance, step size, runtime, posterior summaries. |
| Not concluded | No production readiness, posterior correctness beyond declared sampler scope, LEDH superiority, scale claim, or default policy. |
| Artifact | Derivative contract, HMC manifest if any, and Phase 9 result. |

## Forbidden Claims / Actions

- Do not call FD/JVP/ForwardAccumulator the analytical comparator unless the
  reviewed contract explicitly classifies it as diagnostic only.
- Do not launch HMC/MCMC without exact approval.
- Do not rank speed if sampler validity vetoes fail.

## Exact Next-Phase Handoff Conditions

Phase 10 may begin only if:

- derivative readiness is pass or explicitly out of scope for final claims;
- HMC readiness is pass, blocked, or explicitly out of scope;
- LEDH/scale command approvals and comparator scope are refreshed.

## Stop Conditions

Stop if:

- only diagnostic derivative routes exist and HMC remains in scope;
- HMC approval is unavailable;
- sampler validity vetoes fail;
- Claude and Codex do not converge after five review rounds.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 9 result / close record;
3. draft or refresh the Phase 10 subplan;
4. review the Phase 10 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
