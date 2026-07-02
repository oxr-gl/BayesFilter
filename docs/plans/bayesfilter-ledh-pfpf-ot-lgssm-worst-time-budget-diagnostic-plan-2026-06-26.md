# LEDH-PFPF-OT LGSSM Worst-Time Budget Diagnostic Plan

Date: 2026-06-26

## Question

The transport step ladder showed that `8` finite Sinkhorn steps is badly
under-converged, but `80`/`100` still failed the all-time row-residual gate at
later times. Does a larger finite budget clear those worst-time residuals, or
does a transport normalization/application issue remain?

## Evidence Contract

Question:

- On the observed worst-time clouds, do candidate finite budgets
  `100`, `200`, and `400` clear dense and streaming row residuals below
  `1e-3`?

Baseline/comparator:

- Same LGSSM fixture and seeds as
  `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`.
- `N=128`, 10 seeds, CPU-only diagnostic, GPU hidden.
- Target clouds:
  - state dimension 1, target time 8;
  - state dimension 2, target time 7.
- Target clouds are produced by replaying the filter with baseline
  `steps=100` before the target time, matching the prior fallback context.

Primary criteria:

- Pass if the best tested candidate for each state dimension has dense row
  residual and streaming row residual below `1e-3`.
- If rows pass but covariance trace ratio remains far below one, the next
  target is reset covariance semantics.
- If rows fail at `400`, inspect transport-from-potentials
  normalization/application before any harness or production-code change.

Diagnostics that can veto:

- Non-finite row/column residuals, particles, or moments.
- Dense/streaming particle mismatch above `1e-4`.
- Dense column residual above `1e-3`.
- Runtime timeout or missing artifact.

Explanatory-only diagnostics:

- Runtime.
- ESS at target time.
- Value prefix/increment deltas to Kalman.
- Covariance trace ratios and pre/post mean shift.

What will not be concluded:

- No gradient correctness, SIR correctness, GPU/XLA performance, HMC readiness,
  posterior correctness, production readiness, or broad scientific validity.
- No production transport or LGSSM harness change is authorized by this plan
  alone.

## Skeptical Plan Audit

- Wrong-baseline risk: this focuses on the exact worst-time clouds from the
  prior artifact instead of retesting only the easy first-time shared cloud.
- Proxy-risk: row residual pass is necessary but not enough for value
  correctness, so covariance/value diagnostics remain explanatory and can
  direct the next target.
- Environment risk: CPU-only diagnostic is intentional and cannot support GPU
  performance or production-target claims.
- Boundary risk: no production transport code changes are made by this
  diagnostic.

Audit status: PASS for bounded diagnostic execution.

## Command

```bash
/usr/bin/timeout 600 python docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_worst_time_budget.py \
  --device-scope cpu \
  --num-particles 128 \
  --dense-parity-particles 64 \
  --seed-count 10 \
  --state-dims 1 2 \
  --baseline-steps 100 \
  --candidate-steps 100 200 400 \
  --epsilon 0.5 \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-worst-time-budget-diagnostic-2026-06-26.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-worst-time-budget-diagnostic-2026-06-26.md
```

## Stop Conditions

- Stop after artifact completion and interpret against the evidence contract.
- Stop on timeout or missing artifact; do not infer transport correctness from
  timeout.
- Do not launch N1000 GPU/XLA from this diagnostic.
