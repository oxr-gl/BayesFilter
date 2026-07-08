# Phase 3 Result: HMC Mechanics Canary

Date: 2026-07-08
Status: `PASSED_WITH_REPAIR`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Subplan: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-subplan-2026-07-08.md`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 3 mechanics canary passes after a coordinate-composition repair | Passed: final artifact reports `mechanics_canary_passed: true`, 3/3 fixed candidates passed finite mechanics telemetry, and required checks passed | No final artifact vetoes; native divergence telemetry is not exposed by this TFP kernel, so no zero-divergence claim is made | Two retained samples per candidate are only launch/mechanics evidence, not convergence or posterior validation | Draft and review Phase 4 short HMC smoke subplan | No HMC convergence, posterior correctness, tuned kernel, sampler superiority, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | A tiny fixed-grid mass-preconditioned HMC mechanics canary can evaluate finite target/trace telemetry using the Phase 2 mass handoff. |
| Baseline/comparator | Phase 2 mass handoff artifact `docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json`. |
| Primary criterion | Passed in the final artifact: at least one predeclared candidate had finite mechanics telemetry; all three did. |
| Veto diagnostics | Final artifact vetoes are `[]`; `git diff --check` passed. |
| Explanatory diagnostics | Acceptance was 1.0 for each two-sample tiny candidate; max finite log-accept absolute values were about `5.26e-05`, `0.0135`, and `0.0478`; trajectory lengths were `0.10`, `0.50`, and `1.57`. These are mechanics-only diagnostics. |
| Not concluded | No posterior correctness, HMC convergence, zero divergences, sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, or source-faithful Zhao-Cui behavior. |
| Preserving artifacts | JSON/Markdown/log artifacts listed below plus this result and ledger entry. |

## Repair Record

The first Phase 3 implementation artifact failed before sampling. The mass-handoff precondition was valid, but the adapter composition fed Phase 1 whitened `z` values directly into a base adapter that expects free parameter values. That produced a target-path runtime exception from the SVD-UKF spectral-gap assertion at the nominal initial position.

The repair composed both maps explicitly:

- Phase 2 mass preconditioner: `z = u @ chol(M_z).T`.
- Phase 1 parameter map: `free = center + scale * z`.
- Implemented base-target coordinate: free parameter values.

Focused tests now evaluate the repaired initial adapter value/score and verify the composition metadata.

## Final Artifacts

- Script: `docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_mechanics_canary_2026_07_08.py`
- Tests: `tests/test_scalar_ssl_lstm_filtering_hmc_mechanics_canary.py`
- JSON: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.json`
- Markdown: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.md`
- Log: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.log`

## Final Candidate Summary

| Candidate | Leapfrog steps | Step size | `L * epsilon` | Status | Acceptance | Max abs `u` | Vetoes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0.10 | 0.10 | `passed_mechanics_canary` | 1.0 | 0.07699729249971801 | none |
| 1 | 2 | 0.25 | 0.50 | `passed_mechanics_canary` | 1.0 | 1.1771417860859845 | none |
| 2 | 4 | 0.3925 | 1.57 | `passed_mechanics_canary` | 1.0 | 2.704452978845203 | none |

Native divergence telemetry was not exposed by the TensorFlow Probability HMC kernel trace. This is recorded as unavailable and is not interpreted as zero divergences.

## Checks

- `python -m py_compile docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_mechanics_canary_2026_07_08.py`: passed.
- `pytest tests/test_scalar_ssl_lstm_filtering_hmc_mechanics_canary.py -q`: passed, `5 passed`; TensorFlow/gast deprecation warnings observed.
- CPU-hidden mechanics canary command with `timeout 180`: passed and wrote structured artifacts.
- `git diff --check`: passed.

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | Passed for Phase 3 mechanics canary. |
| Statistically supported ranking | None; fixed tiny mechanics grid only. |
| Descriptive-only differences | Acceptance, log-accept ratio, target log-prob range, trajectory length, and runtime. |
| Default readiness | Not assessed. |
| HMC readiness | Not assessed; Phase 3 is mechanics-only. |
| Next evidence needed | Reviewed Phase 4 short HMC smoke if continuing. |

## Handoff

Phase 4 may be drafted as a short fixed-kernel HMC smoke only. It must remain CPU-hidden/debug-reference unless explicitly reviewed otherwise, must keep native divergence unavailability separate from zero-divergence claims, and must not claim convergence, posterior correctness, tuned-kernel readiness, or default readiness.
