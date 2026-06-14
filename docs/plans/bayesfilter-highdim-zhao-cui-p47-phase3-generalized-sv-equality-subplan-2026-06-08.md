# P47-M3 Subplan: Generalized SV Same-Target Equality

metadata_date: 2026-06-08
phase: P47-M3
status: `DRAFT_FOR_CLAUDE_PLAN_REVIEW`

## Purpose

Build a same-target value and gradient comparison for generalized SV using
CUT4, Zhao--Cui/fixed-design or adaptive TT, and an explicit reference route.

## Phase Prerequisites

- `PASS_P47_M0_GOVERNANCE`
- `PASS_P47_M1_ADAPTIVE_ROUTE`

M3 may prepare derivations after M0, but the equality gate cannot promote until
M1 has fixed the Zhao--Cui route label and branch policy.
Every promoted comparison row must carry the M1 route label: `adaptive route
candidate` or `documented-deviation fixed-design substitute`.

## Tasks

1. Freeze the generalized SV target: native, transformed exact, KSC mixture, or
   another reviewed approximation target.
2. Record observation Jacobian and parameter transform terms.
3. Implement or select the matching CUT4 route only if the target is compatible
   with CUT4 assumptions.
4. Implement or select the matching Zhao--Cui route using P46/P47 retained-grid
   contracts.
5. Add value tests and at least five P42 directional score checks in the same
   unconstrained parameterization.

## Evidence Contract

Question: do CUT4 and Zhao--Cui evaluate the same generalized SV likelihood
and score target within justified tolerances?

Primary pass criterion: same data, same parameters, same target, reference
route stability, M1 route label, value agreement, and P42 Tier 1 directional
gradient checks.

Veto diagnostics:

- native and transformed targets are mixed without Jacobian accounting;
- KSC mixture is labeled exact native SV;
- gradient parameterization mismatch;
- dense/reference route is absent or unstable;
- M1 route label is absent or generic Zhao--Cui wording hides a
  documented-deviation substitute;
- value pass is promoted to HMC readiness.

## Local Gates

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_generalized_sv_equality.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_generalized_sv_equality.py
```

## Claude Gate

Expected token:

```text
PASS_P47_M3_GENERALIZED_SV_EQUALITY
```
