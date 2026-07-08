# Reset Memo: Scalar Filtering Geometry To HMC Readiness

Date: 2026-07-08
Status: `RESET_MEMO_FOR_FUTURE_AGENT`

## Current State

The scalar filtering geometry-to-HMC readiness runbook completed through Phase 6 and is closed with boundaries.

Primary closeout:

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase6-closeout-result-2026-07-08.md`

Execution ledger:

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-execution-ledger-2026-07-08.md`

## Evidence Class

This runbook established CPU-hidden scalar finite-telemetry engineering viability only. It did not establish posterior correctness, HMC convergence, tuned-kernel readiness, zero divergences, sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, package/public API readiness, or Zhao-Cui source-faithfulness.

Claude review was policy-blocked for private repository context transfer. Material reviews used local Codex substitute review and are explicitly weaker than full external Claude review.

## Key Artifacts

| Role | Path |
| --- | --- |
| Filtering geometry | `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json` |
| Mass handoff | `docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json` |
| HMC mechanics canary | `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.json` |
| Short HMC smoke | `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.json` |
| Replicated finite-telemetry diagnostic | `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.json` |

## Coordinate Contract

The accepted coordinate composition is:

- Phase 1 free-parameter map: `free = center + scale * z`.
- Phase 2 mass/covariance: `M_z = inv(K_z)` in `z` coordinates.
- TFP HMC coordinate: `u`.
- Phase 3+ HMC execution map: `z = u @ chol(M_z).T`, then `free = center + scale * z`.

Do not feed `z` directly to the free-parameter adapter. That bug was found in the first Phase 3 attempt and repaired.

## Numerical Summary

- Phase 2 `K_z`/`M_z` condition number: about `35.99`.
- Phase 3 fixed mechanics grid: `(L, epsilon)` = `(1, 0.10)`, `(2, 0.25)`, `(4, 0.3925)`, all passed finite mechanics telemetry.
- Phase 4 short smoke: `L=4`, `epsilon=0.3925`, `num_results=8`, `num_burnin_steps=2`, passed finite telemetry.
- Phase 5 replicated diagnostic: three seeds, 16 retained samples each, passed finite telemetry.
- Phase 5 acceptance rates: `[0.9375, 0.9375, 0.75]`.
- Phase 5 max abs finite log-accept values: `[1.8844, 77.7562, 178.0001]`, descriptive caution only.

## Boundaries For Future Work

- Native divergence telemetry was unavailable; do not claim zero divergences.
- Large finite log-accept tails in Phase 5 should inform any longer validation plan.
- The center is `truth_free_initial_center`, not MAP.
- All runs were CPU-hidden debug/reference, not GPU/XLA production evidence.
- The lane is `extension_or_invention`; it does not establish Zhao-Cui source-faithfulness.
- Longer chains, convergence diagnostics, posterior correctness, GPU/XLA, dimensional lift, and Zhao-Cui source-faithfulness each require a new reviewed plan.

## Suggested Next Plans

1. Native divergence / richer HMC telemetry route for the scalar target.
2. Longer scalar validation with predeclared R-hat/ESS/MCSE and clear stop conditions.
3. GPU/XLA reproduction of the finite-telemetry ladder.
4. Dimensional lift beyond four free parameters.
5. Separate Zhao-Cui source-anchor plan if source-faithfulness is the target.
