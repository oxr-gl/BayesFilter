# SIR Gradient Reparameterization Diagnostic Result

Date: 2026-07-01

Status: `PHYSICS_AND_WHITENING_COMPLETED`

## Decision

The hand-designed SIR physics basis did not remove the budget-10 gradient
discrepancy.  It confirms that the issue is not merely a bad raw
`log_kappa_scale` axis.

The result does support the broader parametrization concern: seed-gradient
geometry is highly anisotropic, with `log_kappa_scale` and `log_nu_scale`
almost perfectly anticorrelated across seeds.

The generic local whitening diagnostic also completed.  It improved two
directions in absolute size but concentrated the large mismatch into the
dominant kappa/nu covariance direction.  This is evidence for a localized
dynamic-parameter score problem, not evidence that whitening fixes the score.

## Command

```bash
bash scripts/run_sir_gradient_reparam_physics_budget10.sh
bash scripts/run_sir_gradient_reparam_whitened_budget10.sh
```

## Artifacts

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-physics-budget10-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-physics-budget10-progress-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-progress-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-memory-2026-07-01.json`

## Route Checks

- GPU output tensors: yes.
- XLA manual reverse compiler: yes.
- TF32 enabled: yes.
- Basis sets: `physics`, then `whitened`.
- Sinkhorn budget: `10`.
- Same fixed seeds, theta, FD offsets, seed microbatching, and theta-offset
  chunking as the completed raw budget-10 artifact.
- The whitening run used the GPU/XLA/TF32 route and took `1791.730865`
  seconds.  The successful physics run took `1788.108907` seconds, so the
  initially long no-progress interval was normal XLA compile latency rather
  than evidence of a stall.

## Raw-Basis Reference

| Direction | Manual | FD slope | Difference | Combined z | Gate reason |
| --- | ---: | ---: | ---: | ---: | --- |
| `log_kappa_scale` | -143.369888 | -263.185455 | 119.815567 | 2.447659 | `inconclusive_precision_veto` |
| `log_nu_scale` | 68.266624 | 105.052803 | -36.786179 | -2.828196 | `within_4_combined_se_requires_ladder_certificate` |
| `log_obs_noise_scale` | 46.060081 | 46.766800 | -0.706718 | -1.292074 | `within_2_combined_se` |

## Physics-Basis Result

The physics basis uses columns:

- `rho_log_kappa_minus_log_nu = (log_kappa_scale - log_nu_scale) / sqrt(2)`;
- `tau_common_rate = (log_kappa_scale + log_nu_scale) / sqrt(2)`;
- `omega_obs_noise = log_obs_noise_scale`.

| Direction | Manual | FD slope | Difference | Slope SE | Slope z | Regression R2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `rho_log_kappa_minus_log_nu` | -149.649612 | -260.371185 | 110.721573 | 0.986200 | 112.270860 | 0.999871 |
| `tau_common_rate` | -53.106022 | -111.582886 | 58.476864 | 0.150151 | 389.454445 | 0.999984 |
| `omega_obs_noise` | 46.060081 | 46.766800 | -0.706718 | 0.065962 | -10.714088 | 0.999982 |

Projected seed-MCSE context:

| Direction | Direction MCSE | Combined z using direction MCSE |
| --- | ---: | ---: |
| `rho_log_kappa_minus_log_nu` | 43.780297 | 2.528386 |
| `tau_common_rate` | 25.447353 | 2.297915 |
| `omega_obs_noise` | 0.542972 | -1.292074 |

## Whitening-Basis Result

The local whitening basis was constructed from the five-seed manual-score
covariance.  The covariance eigenvalues were:

```text
[0.106830, 6.008498, 12816.767578]
```

The columns below map whitened coordinate increments into the original
`(log_kappa_scale, log_nu_scale, log_obs_noise_scale)` coordinates:

```text
whitened_0 = [-0.116105, -0.423152,  0.898589]
whitened_1 = [ 0.228424,  0.869081,  0.438771]
whitened_2 = [-0.966614,  0.256203, -0.004246]
```

| Direction | Manual | FD slope | Difference | Slope SE | Direction MCSE | Combined z | Relative diff vs FD | Regression R2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `whitened_0` | 29.147808 | 27.869690 | 1.278118 | 0.073113 | 0.146253 | 7.816766 | 4.5861% | 0.999938 |
| `whitened_1` | 46.789886 | 51.659393 | -4.869507 | 0.067910 | 1.096269 | -4.433393 | 9.4262% | 0.999984 |
| `whitened_2` | 155.877838 | 281.072083 | -125.194244 | 1.157193 | 50.629574 | -2.472104 | 44.5417% | 0.999847 |

The first two whitened directions are much closer in absolute difference than
the raw kappa/nu directions, but they still do not certify correctness under a
strict MCSE-aware test.  The third whitened direction is essentially the
dominant kappa/nu covariance direction and carries the large discrepancy.

## Geometry Observation

Seed-gradient correlation matrix:

```text
[[ 1.000, -0.997,  0.400],
 [-0.997,  1.000, -0.331],
 [ 0.400, -0.331,  1.000]]
```

This supports the concern that the kappa/nu block is nearly one-dimensional or
badly conditioned in the five-seed diagnostic geometry.

## Interpretation

The simple physics rotation does not rescue the gradient check:

- the infection-vs-recovery contrast `rho` still has a large gap;
- the common-rate direction `tau` also has a large gap;
- observation noise remains the stable direction.

This weakens the hypothesis that the issue is only the raw
`log_kappa_scale` coordinate.  It strengthens the hypothesis that either:

- the kappa/nu block has a highly anisotropic local geometry, with the main
  problem concentrated along a dynamic-parameter direction close to
  `-0.967 log_kappa_scale + 0.256 log_nu_scale`; or
- the manual score / FD objective path has a component mismatch in the
  transition/flow terms affecting the SIR dynamic parameters.

## Next Step

Do not promote whitening as a default.  If the manual score is wrong, the
manual-score covariance is also a bad covariance estimate.  The next
discriminating diagnostic should inspect or decompose the manual score against
the FD objective along `whitened_2`, ideally separating transition, observation,
transport, and correction terms.  The smaller `whitened_0` and `whitened_1`
gaps are useful controls, but the root-cause search should focus on the
dominant kappa/nu direction first.

## Runtime Note

The monolithic whitening run initially appeared stalled because progress JSON
is written only after the AD/manual-score stage completes.  The successful
physics run had already shown that this stage takes about 30 minutes under the
current five-seed XLA microbatch route.  The rerun added a memory sampler and
completed without exit 137.  This corrects the earlier suspicion that the
monolithic whitening diagnostic itself required immediate splitting.

## Nonclaims

- No SIR gradient correctness claim.
- No HMC readiness claim.
- No posterior correctness claim.
- No budget-100 conclusion.
- No global reparameterization proof.
- No whitening-default proposal.
