# Phase 3 Result: RK4 Sensitivity Audit

Date: 2026-07-01

Status: `PASSED`

## Decision

The manual SIR RHS/RK4 transition VJP passes the Phase 3 transition-only
audit against TensorFlow autodiff on identical fixed tensors in float64
CPU algebra.

This rules out a local RHS/RK4 transition derivative bug as the next smallest
explanation for the budget-10 SIR manual-score vs finite-difference mismatch.
It does not rule out transport-adjoint, stopped-scale-key, score-assembly, or
full-filter route issues.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the manual RK4 transition derivative for kappa/nu correct before LEDH transport terms enter? |
| Baseline/comparator | Independent TensorFlow autodiff on identical fixed tensors in float64 CPU transition-only algebra. |
| Primary criterion | For `bar_state`, `bar_kappa`, `bar_nu`, regional log-kappa contractions, and regional log-nu contractions: max absolute residual `<= 1.0e-8` and relative L2 residual `<= 1.0e-7`, denominator `max(norm(comparator), 1.0)`. |
| Veto diagnostics | Comparator semantic drift, missing regional chain-rule check, unsupported full-filter/GPU/HMC claim. |
| Not concluded | Full SIR score correctness, transport adjoint correctness, GPU/TF32 material behavior, HMC readiness. |

## Commands Run

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/diagnose_p8p_sir_rk4_sensitivity_vjp.py
pytest -q tests/test_p8p_sir_rk4_sensitivity_vjp.py
python docs/benchmarks/diagnose_p8p_sir_rk4_sensitivity_vjp.py --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-2026-07-01.json
```

## Artifacts

- Diagnostic:
  `docs/benchmarks/diagnose_p8p_sir_rk4_sensitivity_vjp.py`
- Tests:
  `tests/test_p8p_sir_rk4_sensitivity_vjp.py`
- JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-2026-07-01.json`

## Local Check Results

- Compile check: passed.
- `pytest -q tests/test_p8p_sir_rk4_sensitivity_vjp.py`: `3 passed`.
- Diagnostic status: `PASS`.
- Artifact CPU boundary: `CUDA_VISIBLE_DEVICES=-1`; recorded tensor devices
  were CPU only.

TensorFlow printed CUDA plugin registration and `cuInit` messages during import.
Those messages are not material GPU evidence because this diagnostic explicitly
hid CUDA devices and recorded CPU-only tensors.

## Numerical Summary

All comparisons passed.  Largest residuals by family:

| Family | Max absolute residual | Max relative L2 residual |
| --- | ---: | ---: |
| RHS | `3.410605131648481e-13` | `3.721360682445893e-16` |
| One RK4 step | `8.881784197001252e-16` | `2.5735369674468285e-16` |
| Full RK4 scan | `2.842170943040401e-14` | `6.074194148859855e-16` |
| Regional log-kappa chain rule vs regional autodiff | `3.552713678800501e-15` | `5.970156682613102e-16` |
| Regional log-nu chain rule vs regional autodiff | `8.881784197001252e-16` | `1.9139900674419949e-16` |

## Interpretation

Phase 3 clears the transition sensitivity algebra at machine precision.  The
dominant Phase 2 rho/tau mismatch should not be attributed to the hand-coded
SIR RHS or RK4 reverse scan unless a later full-route diagnostic shows a
different transition-context wiring problem.

The next smallest justified diagnostic is therefore the transport-adjoint /
stopped-scale-key boundary used between `post_flow`,
`normalized_log_weights`, and the next particle/log-weight state.  The
non-centered process-noise branch remains an idea, but Phase 3 did not produce
evidence that makes it the immediate next gate.

## Decision Table

| Item | Status |
| --- | --- |
| Primary criterion | Passed. |
| Veto diagnostics | No veto. |
| Main uncertainty | Full-filter mismatch remains; transport/score assembly remain live. |
| Next justified action | Refresh Phase 4 to a transport-adjoint/stopped-scale-key audit. |
| Not concluded | No full SIR gradient correctness or HMC readiness claim. |
