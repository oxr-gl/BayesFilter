# DPF5 Seed And Uncertainty Policy

## Status

DPF5 execution artifact.  This policy defines how stochastic DPF diagnostics
must handle seeds and Monte Carlo uncertainty.

## Seed Policy

| Run class | Minimum policy |
| --- | --- |
| Deterministic algebra/parity | Record `deterministic_no_rng` or fixed fixture id. |
| Smoke | One seed allowed only for finite/shape/debug claims. |
| Reference recovery | Multiple seeds or explicit MCSE/uncertainty field unless deterministic. |
| Proxy comparison | Multiple seeds when ranking would otherwise be implied. |
| Performance timing | Multiple repeats or clear smoke-only timing label. |
| HMC/posterior | Separate future plan with chain seeds, warmup, diagnostics, and posterior/reference criteria. |

## Uncertainty Rules

- One-seed differences are diagnostic only unless a plan justifies otherwise.
- MCSE or uncertainty intervals must be recorded for stochastic reference
  comparisons.
- Rankings require veto diagnostics to pass first.
- Runtime comparisons must state hardware/device, thread/GPU policy, dtype, and
  whether compilation/warmup is included.
- Same-regime student comparisons are explanatory only and cannot provide
  uncertainty for BayesFilter correctness.

## Stop Rules

Stop or downgrade to smoke-only if:

- seed list is missing;
- MC uncertainty is omitted from a stochastic promotion criterion;
- a single seed is used to rank candidate methods;
- runtime differences are reported after numerical veto failure;
- HMC/posterior language appears without a separate sampler plan.
