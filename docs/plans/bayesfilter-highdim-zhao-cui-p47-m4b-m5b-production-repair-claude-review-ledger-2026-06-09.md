# P47 M4b/M5b Production Repair Claude Review Ledger

metadata_date: 2026-06-09
program: P47-production-repair
status: `REVIEW_PASSED_BLOCKER_CLOSEOUT`

## Review Protocol

Claude is read-only reviewer.  Codex is supervisor and execution agent.
Claude must not edit files, run experiments, launch agents, or change state.

Expected plan-review token:

```text
PASS_P47_PRODUCTION_REPAIR_PLAN
```

or

```text
BLOCK_P47_PRODUCTION_REPAIR_PLAN
```

Expected blocker-review token:

```text
PASS_P47_PRODUCTION_REPAIR_BLOCKER_REVIEW
```

or

```text
BLOCK_P47_PRODUCTION_REPAIR_BLOCKER_REVIEW
```

## Iteration 1

Claude returned:

```text
PASS_P47_PRODUCTION_REPAIR_BLOCKER_REVIEW
```

Claude found that:

- No production pass tokens are emitted for M4b or M5b.
- `BLOCKED_M4B_ROUTE_ARCHITECTURE` is evidence-backed by the all-axes
  retained-grid preflight cap.
- `BLOCKED_M5B_PRODUCTION_ACCURACY_TUNING` is evidence-backed by the
  horizon-25 same-target candidate failing reviewed value/state/covariance
  tolerances while deterministic replay passes.
- Lower-rung evidence is preserved without promotion to production evidence.
- Nonclaims are guarded for production filtering, production HMC/API, adaptive
  MATLAB reproduction, native non-Gaussian correctness, nonlinear
  preconditioning usefulness, and S&P 500 reproduction.
- Future work should create concrete route-amendment plans rather than loosen
  tolerances after the fact.
