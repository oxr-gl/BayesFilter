# P8i Reset Memo: DPF/LEDH Remaining-Gap Closure

Date: 2026-06-16

Status: `PHASE8_CLOSEOUT_REVIEWED_CLOSED`

## Active Lane

This memo covers only P8i DPF/LEDH filtering-value-gradient benchmark
remaining-gap closure. Zhao-Cui high-dimensional fixed-branch work and the
monograph rewrite are out of scope.

Active route:

- row alias: `actual_sv`;
- row ID: `zhao_cui_sv_actual_nongaussian_T1000`;
- algorithm ID: `ledh_pfpf_alg1_ukf_current`;
- route variant: `p8h_sv_scalar_graph_ot_resampled_alg1`;
- resampling route: `ot_sinkhorn_barycentric_covariance_carry`;
- coordinate: `canonical_unconstrained`.

## Completed Gated Phases

- Phase 0 mapped P8h remaining gaps into P8i gates.
- Phase 1 selected diagnostic `N=5` for horizons `16,32` only.
- Phase 2 passed fixed-seed relaxed-OT AD graph gradient checks at horizons
  `16,32`, `N=5`, five seeds, trusted GPU.
- Phase 3 profiled trusted-GPU runtime for selected `N=5` and adjacent
  `N=10`; the selected route passed the bounded HMC projection gate.
- Phase 4 passed a tiny fixed-kernel HMC execution diagnostic at H32, `N=5`.
- Phase 5 blocked NUTS because no NUTS command path, adaptation budget, or
  diagnostics exist.
- Phase 6 classified gradient/likelihood claims: relaxed-OT AD evidence is a
  deterministic graph diagnostic only; exact stochastic PF marginal-gradient
  and exact nonlinear-likelihood correctness are not concluded.
- Phase 7 preserved no filter ranking, no generic high-dimensional LEDH
  readiness, and no default sampler policy.

## Key Numerical Facts

- Phase 1 full ladder selected `N=5` at horizons `16,32`; this is not
  full-horizon adequacy.
- Phase 2 maximum finite-difference residuals were about `7.56e-09` at H16
  and `1.13e-08` at H32.
- Phase 3 selected `N=5` profile runtimes were about `50.01s` at H16 and
  `69.10s` at H32; projected Tier-1 HMC cost was `345.50s < 900s`.
- Phase 4 fixed-kernel HMC diagnostic wall time was about `139.36s`, with
  finite values, gradients, samples, target log probabilities, and log-accept
  ratios on trusted GPU.

## Boundaries

P8i has not established:

- full-horizon particle-count adequacy;
- stochastic PF marginal-gradient correctness;
- exact nonlinear likelihood correctness;
- production HMC readiness;
- posterior convergence;
- valid tuning;
- NUTS readiness;
- full GPU scaling law;
- generic high-dimensional LEDH readiness;
- filter ranking;
- default sampler policy.

## Repo Boundary

The intended P8i file set is:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-*`;
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`;
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`.

There is substantial unrelated dirty work in Zhao-Cui, monograph, P8g/P8h,
fixed-SGQF, and other lanes. Do not commit, push, or stage beyond the P8i
boundary without a fresh explicit request.
