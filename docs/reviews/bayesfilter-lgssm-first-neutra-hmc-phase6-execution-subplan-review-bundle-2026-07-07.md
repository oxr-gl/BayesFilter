# BayesFilter LGSSM-First NeuTra/HMC Phase 6 Execution Subplan Review Bundle

Date: 2026-07-07

## Role Contract

Read-only review only. Do not edit files, run experiments, launch agents, or
change state. Codex remains supervisor and executor.

Claude review was previously policy-rejected as an external-service
data-exfiltration risk for this program. Unless the user explicitly approves
that external review boundary, this bundle is intended for a fresh Codex
read-only substitute review.

## Exact Review Scope

Review this subplan only:

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-execution-subplan-2026-07-07.md`

Do not review the whole repository.

## Review Question

Does the Phase 6 execution subplan correctly operationalize the user's approval
as a conservative CPU-only tiny learned affine NeuTra-style LGSSM training gate,
with reviewed artifacts/checks before training, and without hidden GPU, dense
IAF, long HMC, package/git/default-policy, DSGE/c603, posterior, production, or
scientific-claim crossings?

## Evidence To Check

| Field | Contract |
| --- | --- |
| Primary criterion | Frozen learned affine payload is written, loads with target signature, transformed mechanics are finite, target/reference checks pass, and no hidden GPU/long-HMC/training expansion occurs. |
| Veto diagnostics | Nonfinite loss, missing artifact, signature mismatch, load failure, nonfinite mechanics, target/reference failure, GPU use, long HMC, dense IAF claim, or training loss promoted to correctness. |
| Not concluded | Dense IAF quality, HMC convergence, posterior correctness, sampler superiority, generic nonlinear SSM validity, production readiness, default-policy change, scientific validity. |

## Requested Output

Findings first. End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
