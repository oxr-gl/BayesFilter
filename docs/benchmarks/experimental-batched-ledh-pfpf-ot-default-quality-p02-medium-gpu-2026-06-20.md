# Streaming LEDH-PFPF-OT Paired Quality Screen

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 12, 'num_particles': 128, 'state_dim': 6, 'obs_dim': 6}`
- Seeds: `[20260620, 20261629, 20262638]`
- Drift formula: `max(abs(candidate - reference) / max(1.0, abs(reference))) per output array and paired seed`
- Max-relative tolerance: `0.01`

## Seed Screens

| seed | wrapper | metadata | tolerance | device | worst default drift |
| ---: | --- | --- | --- | --- | ---: |
| 20260620 | True | True | True | True | 0.00012860370994749646 |
| 20261629 | True | True | True | True | 0.0001302131797900768 |
| 20262638 | True | True | True | True | 0.00011686794762932915 |

## Worst Default Drift By Output

| output | seed | max relative | tolerance | passed |
| --- | ---: | ---: | ---: | --- |
| log_likelihood | 20261629 | 0.000130213 | 0.01 | True |
| filtered_means | 20260620 | 4.22228e-05 | 0.01 | True |
| filtered_variances | 20261629 | 3.3208e-06 | 0.01 | True |
| ess_by_time | 20261629 | 4.77206e-06 | 0.01 | True |

## Nonclaims

- medium synthetic LGSSM-shaped quality screen only
- FP64 is a numerical comparator, not an exact posterior oracle
- three paired seeds do not support statistical ranking
- runtime and memory are descriptive only
- no posterior correctness claim
- no HMC readiness or sampler-convergence claim
- no speedup claim
- no dense Sinkhorn equivalence claim
- no public API readiness claim
