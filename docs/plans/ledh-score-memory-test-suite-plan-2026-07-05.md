# LEDH Score And Memory Test Suite Plan

Date: 2026-07-05

## Question

Do the currently implemented LEDH score routes have individual correctness and
memory tests, and does the all-model LEDH integration test truthfully report
which highdim rows have an admitted score route at `N=10000`?

## Baseline / Comparator

- LGSSM score correctness comparator: same-scalar central finite difference of
  the compact no-autodiff LEDH-PFPF-OT scalar.
- Parameterized SIR score correctness comparator: existing same-route manual
  score diagnostic checks and finite output under the no-autodiff sentinel.
- Other highdim rows: the current LEDH row-admission ledger, which blocks score
  admission until a same-target value adapter and total-derivative score route
  exist.

## Primary Criteria

- One test per highdim row exists.
- Implemented score routes run with `N=10000` and finite outputs.
- Memory diagnostics are recorded for GPU runs where available.
- The all-model integration test enumerates every highdim row and fails if a
  blocked row is silently treated as an admitted score route.
- No test uses tape gradients as an admitted score computation.

## Veto Diagnostics

- Non-finite score on an implemented route.
- Missing row from the all-model integration result.
- Treating blocked LEDH score rows as passing.
- GPU memory peak above the configured test budget.
- CPU-only execution being labeled as GPU evidence.

## Explanatory Diagnostics

- Exact Kalman value error for LGSSM is explanatory only.
- Runtime is explanatory only.
- Memory peak is a resource diagnostic; it does not by itself prove score
  correctness.

## Nonclaims

- These tests do not prove exact likelihood score correctness for nonlinear
  rows.
- These tests do not admit currently blocked LEDH rows.
- These tests do not prove HMC/NUTS readiness.
- These tests do not rank LEDH against other algorithms.

## Skeptical Audit

The plan rejects a false all-model pass: the current repo has implemented LEDH
score routes for LGSSM and scoped parameterized SIR diagnostics, but the LEDH
ledger still blocks actual SV, KSC SV, fixed SIR full-row score, predator-prey,
and generalized SV score admission. The integration test must preserve that
fact until those routes are implemented and reviewed.
