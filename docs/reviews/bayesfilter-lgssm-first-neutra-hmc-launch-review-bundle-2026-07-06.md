# BayesFilter LGSSM-First NeuTra/HMC Launch Review Bundle

Date: 2026-07-06

## Role Contract

READ-ONLY BOUNDED REVIEW.

Codex is supervisor and executor. Claude is read-only reviewer only.

Do not edit files, run commands, launch agents, inspect the whole repository,
or authorize runtime, model-file, funding, product-capability, default-policy,
or scientific-claim boundaries.

## Review Question

Is this LGSSM-first NeuTra/HMC master program and Phase 0/Phase 1 launch
boundary consistent, correct, feasible, artifact-covered, and boundary-safe?

End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

## Artifacts Under Review

- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-master-program-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase0-scope-reset-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase1-interface-inventory-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-gated-execution-runbook-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-execution-ledger-2026-07-06.md`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-stop-handoff-2026-07-06.md`

## Program Summary

The program deliberately starts from BayesFilter-owned LGSSM rather than
DSGE/c603:

```text
LGSSM for correctness,
simple nonlinear SSM for generality,
DSGE for stress.
```

DSGE/c603 is deferred to Phase 9 only. The program reuses existing
BayesFilter surfaces:

- `SSMTargetContract`;
- `GenericSSMPosteriorAdapter`;
- QR Kalman LGSSM code;
- fixed-transport mechanics;
- existing opt-in QR static LGSSM HMC smoke harness.

## Boundary Summary

Allowed in Phase 0/1:

- local read-only inventory;
- local text checks;
- bounded read-only review.

Forbidden without explicit approval:

- GPU/CUDA jobs;
- NeuTra training;
- long or decision-making HMC;
- package installation;
- detached execution;
- git commit/push;
- live DSGE/c603 runtime target authority;
- default-policy/product/scientific claims.

## Review Checklist

Please check:

- wrong baseline;
- DSGE/c603 accidentally made foundational;
- smoke/probe/training-loss proxy promoted to readiness;
- missing stop condition;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch;
- boundary unsafe action.
