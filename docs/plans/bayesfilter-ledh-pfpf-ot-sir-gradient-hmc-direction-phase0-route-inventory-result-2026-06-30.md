# Phase 0 Result: SIR Route Inventory And Governance Freeze

Date: 2026-06-30

Status: `PASS`

## Decision

Phase 0 passes.  The active SIR gradient route and diagnostics are present,
syntax-valid, and locally wired.  This phase did not run material GPU evidence
and does not claim SIR gradient correctness.

## Route Inventory

Active diagnostics:

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
  - P8p parameterized SIR d18 target.
  - Parameter order: `log_kappa_scale`, `log_nu_scale`,
    `log_obs_noise_scale`.
  - Supports manual reverse score route
    `manual_reverse_scan_no_autodiff`.
  - Exposes seed-gradient MCSE via `standard_error_of_batch_mean`.
- `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
  - Regression finite-difference comparator for raw/physics/whitened style
    directions.
  - Supports `--ad-evaluation-mode manual-reverse` and
    `--manual-reverse-compiler xla`.
  - Emits compiler metadata with `jit_compile`.
  - Emits `regression_slope_standard_error`.
- `docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py`
  - Focused Sinkhorn-budget ladder for P8p SIR.
  - Defaults to visible GPU, `float32`, TF32 enabled, manual reverse XLA,
    streaming transport, stabilized transport AD, and row residual reporting.
  - Varies `--candidate-steps` and records row-residual and FD comparison
    summaries.
- `tests/test_ledh_pfpf_ot_p7_manual_score.py`
  - Tiny CPU-hidden manual-score and route tests.
  - This is wiring evidence only, not material LEDH GPU evidence.

Transport route constants:

- `manual_streaming_finite_sinkhorn_stopped_scale_keys`
- `manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys`

Material route constraints:

- GPU/XLA/TF32 route is required for material LEDH evidence.
- CPU-hidden tests remain allowed only as syntax/tiny wiring diagnostics.
- Dense/full transport autodiff remains forbidden for material SIR gradient
  evidence unless a later reviewed plan explicitly changes scope.

## Checks Run

Passed:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
```

Passed:

```bash
python -m pytest tests/test_ledh_pfpf_ot_p7_manual_score.py -q
```

Result: `5 passed, 2 warnings in 34.37s`.

Route inventory grep confirmed the expected fields:

- manual reverse route;
- XLA compiler metadata;
- TF32 mode flag;
- GPU expectation flag;
- `regression_slope_standard_error`;
- `standard_error_of_batch_mean`;
- row residual threshold/pass fields;
- manual streaming transport constants.

## Claude Review

Master/runbook/Phase 0/Phase 1 review converged after three Claude review
rounds.  Final verdict: `VERDICT: AGREE`.

Review trail:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-claude-review-ledger-2026-06-30.md`

## Gate Status

Phase 0 gate: `PASSED`.

Exact next-phase handoff conditions:

- py_compile passed for active SIR diagnostics.
- manual-score unit tests passed.
- comparator limitation is recorded: SIR uses fixed-randomness regression FD,
  not an exact nonlinear oracle.
- Phase 1 subplan is queued, with one nonblocking wording cleanup to separate
  supportive labels from pass arms before Phase 1 execution.

## Nonclaims

- No SIR gradient correctness.
- No FD correctness as exact oracle.
- No HMC/NUTS readiness.
- No posterior validity.
- No production budget promotion.
- No GPU evidence from the CPU-hidden unit test.

## Next Action

Refresh Phase 1 wording to separate supportive labels from pass arms, run a
focused local check, and then enter Phase 1 only under the visible state
machine.
