# P47-M4 Claude Review Ledger

metadata_date: 2026-06-08
phase: P47-M4
status: `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY`

## Review Protocol

Claude is read-only reviewer.  Codex is supervisor and execution agent.
Claude must not edit files, run experiments, launch agents, or change state.

Expected terminal token for the first M4 gate:

```text
PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY
```

or

```text
BLOCK_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY
```

The production token `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING` is not
requested by the M4a review.

## Iteration 1

Claude returned:

```text
PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY
```

Findings summary:

- M4a is correctly scoped to a small-`J` additive-Gaussian spatial SIR closure.
- Dense reference and Zhao--Cui route share the same target inputs, model, and observations.
- Registry and readiness rows preserve the M1 documented-deviation route label.
- Observed infectious and unobserved susceptible errors are tested separately.
- CUT4 is held to value diagnostic and state-moment non-promotion.
- The production token is not emitted from M4a.
- No native SIR, paper-scale, HMC, production score API, adaptive MATLAB, or S&P 500 claim is promoted.
