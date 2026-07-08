# BayesFilter LGSSM-First NeuTra/HMC Phase 1 Review Bundle

Date: 2026-07-06

## Role Contract

Read-only review only. Do not edit files, run experiments, launch agents, or
change state. Codex remains supervisor and executor.

Claude review was previously policy-rejected as an external-service
data-exfiltration risk for this program. Unless the user explicitly approves
that external review boundary, this bundle is intended for a fresh Codex
read-only substitute review.

## Exact Review Scope

Review these planning artifacts for consistency, correctness, feasibility,
artifact coverage, and boundary safety:

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase1-interface-inventory-result-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase2-lgssm-target-adapter-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-execution-ledger-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-stop-handoff-2026-07-06.md`

Do not review the whole repository.

## Review Question

Does the Phase 1 result correctly classify current BayesFilter surfaces and
does the refreshed Phase 2 subplan define a safe, minimal LGSSM generic-adapter
implementation boundary without hidden HMC, NeuTra training, GPU, package,
git, DSGE/c603, default-policy, or scientific-claim crossings?

## Evidence Contract To Check

| Field | Contract |
| --- | --- |
| Question | What current surfaces can be reused and what must Phase 2 implement for LGSSM-first generic SSM target work? |
| Primary criterion | Inventory contains `reuse`, `patch_needed`, and `blocked` classifications and Phase 2 names exact implementation/test artifacts. |
| Veto diagnostics | Hidden DSGE/c603 dependency, HMC smoke treated as readiness, missing target-signature policy, unapproved GPU/training/HMC/package/git action, or unsupported posterior/product/scientific claim. |
| Not concluded | No adapter correctness, HMC readiness, NeuTra readiness, posterior convergence, production readiness, or scientific validity. |

## Known Local Context

- Phase 0 passed local checks and substitute Codex review.
- Claude review was not retried after external-service approval rejection.
- Phase 1 was read-only inventory; no code, HMC, GPU, training, package, or git
  actions were performed.
- The intended sequence is LGSSM -> simple nonlinear non-DSGE SSM -> multiple
  filters -> DSGE/c603 stress only.

## Requested Output

Findings first. End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
