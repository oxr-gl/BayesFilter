# Phase 3 Result: Bounded Mechanics Smoke

Date: 2026-07-08

## Status

`PASSED_MECHANICS_SMOKE_ONLY`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the Phase 2 fixed geometry execute the smallest bounded HMC mechanics smoke without immediate finite-value or artifact failures? |
| Primary criterion | Passed after a diagnostics-wiring repair: tiny mechanics artifact exists, fixed-kernel HMC runtime executed, samples/log-accept/target-log-prob were finite, no runtime exception, and no hard-veto diagnostics remained. |
| Veto diagnostics | No accepted-rerun vetoes. Native boolean divergence telemetry was not exposed by TFP; this is recorded and is not zero divergences. |
| Explanatory diagnostics | Acceptance rate `1.0`; 4 finite retained samples; log accept ratio finite count `4`; target log prob finite count `4`; runtime about `4.76s`. |
| Not concluded | No HMC readiness, no convergence, no posterior correctness, no sampler superiority, no default readiness, and no source-faithful Zhao-Cui claim. |

## Artifact

- JSON:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_mechanics_cpu_hidden_2026-07-08.json`
- Markdown:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_mechanics_cpu_hidden_2026-07-08.md`
- Script:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_mechanics_2026_07_08.py`

## Key Diagnostics

| Diagnostic | Value |
| --- | --- |
| Mechanics decision | `mechanics_smoke_passed=true` |
| Vetoes | `[]` |
| Step size | `0.22590050090246147` |
| Leapfrog steps | `7` |
| Retained samples | `4` |
| Burn-in steps | `1` |
| Fixed/adaptive policy | `fixed_kernel_no_adaptation` |
| Finite sample count | `4` |
| Nonfinite sample count | `0` |
| Acceptance rate | `1.0` |
| Log accept finite/nonfinite | `4` / `0` |
| Target log prob finite/nonfinite | `4` / `0` |
| Target log prob min/max | `-10.07256227895811` / `-5.962127100479027` |
| Native divergence trace present | `false` |
| HMC runtime invoked | `true` |
| HMC tuning invoked | `false` |

## Repair Loop Note

The first Phase 3 run produced a false failure because the script checked
nonexistent top-level diagnostic keys for log-accept and target-log-prob
nonfinite counts. The trace summary itself recorded finite counts and zero
nonfinite values. The script was repaired to use the trace-summary fields for
those veto checks, then rerun with the same fixed geometry.

This was an artifact diagnostics repair, not a change to mechanics pass/fail
criteria.

## Interpretation

The fixed geometry from Phase 2 can execute a tiny CPU-hidden fixed-kernel HMC
smoke on the minimal scalar target with finite mechanics telemetry. The result
does not establish convergence, posterior correctness, absence of divergences,
or readiness for longer HMC. Native boolean divergence telemetry is not exposed
by the TFP kernel in this path and must be addressed or explicitly handled in
any short-chain validation plan.

## Decision Table

| Decision | Status |
| --- | --- |
| Phase 3 bounded mechanics smoke | Passed after diagnostics-wiring repair. |
| Primary criterion status | Satisfied for tiny finite mechanics execution only. |
| Veto diagnostic status | No accepted-rerun vetoes; native divergence telemetry unavailable remains a future evidence gap. |
| Main uncertainty | Whether short-chain HMC with adequate telemetry and uncertainty checks is stable enough to justify any HMC-readiness claim. |
| Next justified action | Write closeout and, if desired, draft a separate short-chain validation plan with native-divergence policy. |
| What is not being concluded | HMC readiness, posterior correctness, sampler convergence, default readiness, or source-faithful Zhao-Cui behavior. |

