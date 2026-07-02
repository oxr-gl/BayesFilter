# Phase 0 Result: Scope And Route Freeze

Date: 2026-07-01

Status: `PASSED`

## Decision

Phase 0 passes.  The program is launched under the visible runbook, the
baseline artifacts exist, the current code anchors are identified, and Phase 1
has an exact diagnostic target.

## Commands Run

```bash
rg -n "^#|Phase Objective|Entry Conditions|Required Artifacts|Required Checks|Evidence Contract|Forbidden Claims|Exact Next-Phase|Stop Conditions|End-Of-Subplan" docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-*.md
rg -n "log_kappa_scale|log_nu_scale|PARAMETER_NAMES|_manual_value_and_score|_sir_transition_mean_vjp_tf|_sir_rhs_vjp_tf" docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/test_ledh_pfpf_ot_p7_manual_score.py
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
```

## Baseline Artifacts

| Artifact | Status | Route notes |
| --- | --- | --- |
| `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.json` | exists | GPU expected, TF32 enabled |
| `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-physics-budget10-2026-07-01.json` | exists, `status=pass` | GPU expected, TF32 enabled, XLA manual reverse |
| `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-2026-07-01.json` | exists, `status=pass` | GPU expected, TF32 enabled, XLA manual reverse |

## Code Anchors

Primary scalar parameter list:

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:56`

Scalar parameter scaling:

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:299`
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:304`
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:305`

Manual transition derivative anchors:

- `_sir_rhs_vjp_tf`:
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:397`
- `_sir_transition_mean_vjp_tf`:
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:509`

Manual score route:

- `_manual_value_and_score_from_components`:
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:1013`

Regional expansion anchor:

- `_theta_score_from_parameter_cotangents`:
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:738`

The key Phase 1 observation is that `_theta_score_from_parameter_cotangents`
already receives region-level `bar_kappa` and scalar `kappa`; it then reduces
the regional vector by:

```text
sum_j bar_kappa_j * kappa_j
```

That is the exact chain-rule scalar score for the diagonal global
`log_kappa_scale` parameter.  Phase 1 can therefore expose per-region
diagnostic components without changing the forward model.

## Claude Review

Claude plan review converged:

- Iteration 1: `VERDICT: REVISE`
- Iteration 2: `VERDICT: REVISE`
- Iteration 3: `VERDICT: AGREE`

Review ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-claude-review-ledger-2026-07-01.md`

## Skeptical Audit

Checked:

- Wrong baseline: mitigated by exact prior artifact paths.
- Proxy metrics: phase criteria classify diagnostic patterns and preserve
  nonclaims.
- Missing stop conditions: each phase subplan has stop conditions and handoff
  conditions.
- Unfair comparisons: Phase 1 keeps the same scalar forward model and diagonal
  chain-rule comparator.
- Hidden assumptions: Phase 4 covariance-independence shortcut was removed
  after Claude review.
- Environment mismatch: material phases remain GPU/XLA/TF32 by contract.
- Artifact mismatch: planned diagnostic/test/wrapper paths are now concrete.

## Phase 1 Handoff

Advance to Phase 1 with this exact target:

- Add diagnostic harness:
  `docs/benchmarks/benchmark_p8p_regional_kappa_gradient_decomposition.py`
- Add tests:
  `tests/test_p8p_regional_kappa_gradient_decomposition.py`
- Add wrapper:
  `scripts/run_sir_gradient_reparam_rootcause_phase1_regional_kappa_budget10.sh`

Phase 1 must first implement a local/tiny chain-rule check that regional kappa
components sum to the current scalar `log_kappa_scale` score before launching
the material GPU/XLA/TF32 budget-10 run.

## Nonclaims

- No SIR gradient correctness claim.
- No HMC readiness claim.
- No posterior correctness claim.
- No production reparameterization.
- No default-policy change.
