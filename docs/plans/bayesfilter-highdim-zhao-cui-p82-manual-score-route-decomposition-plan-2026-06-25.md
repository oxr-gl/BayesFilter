# P82 Manual Score Route Decomposition Diagnostic Plan

Date: 2026-06-25
Status: PLANNED

## Question

For the P82 LEDH-PFPF-OT SIR d18 route, which manual score contribution carries
the robust kappa/nu mismatch between the manual reverse score and the FD
consistency diagnostics?

## Evidence Contract

Primary comparator: the already-recorded FD consistency artifacts for the same
theta, seeds, T3 SIR d18 target, streaming transport route, TF32 float32 GPU
route, and fixed random streams:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-gpu-tf32-2026-06-24.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-n1000-central-fd-sanity-result-2026-06-25.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-n2500-fd-regression-diagnostic-result-2026-06-25.md`

Primary criterion: produce a finite manual-score decomposition whose component
sum exactly reconstructs the current manual gradient to floating-point
tolerance, and identify whether the kappa/nu gap is compatible with one of the
transition-density, LEDH-flow, pre-flow/clamp, observation-density-covariance,
or flow-covariance paths.

Veto diagnostics:

- no `transport_ad_mode=full`;
- no Zhao-Cui comparator or oracle language;
- no FD-oracle certification claim;
- no dense transport matrix materialization;
- no nonfinite decomposition component;
- no decomposition-total mismatch against the recorded manual gradient.

Explanatory diagnostics:

- per-seed component means and standard errors;
- comparison of component magnitudes against the central/13-point FD residual;
- existing MCSE summaries.

Not concluded even if the diagnostic passes:

- LEDH gradient correctness;
- posterior correctness or HMC readiness;
- exact nonlinear likelihood correctness;
- scientific superiority of any high-dimensional filter.

Artifact contract:

- diagnostic JSON under `docs/plans`;
- result note under `docs/plans`;
- local syntax/schema checks recorded in the result note.

## Skeptical Plan Audit

This plan does not rerun the noisy FD ladder or treat FD as an oracle.  It
answers a narrower engineering question: whether the current manual score is
missing a route-local dependency and where the existing manual reverse pass
attributes the score.  The baseline artifacts use the same route and theta, so
the comparison is fair for localization.  The planned command is bounded and
uses `--fd-mode ad-only` to avoid another expensive FD sweep.  The main hidden
assumption is that the current component split is algebraically faithful to the
manual reverse code; the decomposition-total equality check is the guard for
that assumption.

## Required Implementation

Add a diagnostic-only `manual_score_decomposition` payload to the manual reverse
score path.  The default objective and gradient outputs must remain unchanged.

Required component labels:

- `observation_density_covariance`
- `ledh_flow_observation_covariance`
- `transition_mean_from_transition_density`
- `transition_mean_from_ledh_flow_prior`
- `transition_mean_from_pre_flow_clamp`

The transition mean split must evaluate the existing `_sir_transition_mean_vjp_tf`
separately against the three existing upstream cotangent sources:

- `transition_vjp["transition_mean"]`;
- `flow_vjp.prior_means`;
- `bar_pushed`.

## Commands

Local checks:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-gpu-tf32-2026-06-24.json >/tmp/p82_phase8r.json.check
```

Bounded GPU diagnostic:

```bash
/home/chakwong/anaconda3/bin/conda run -n tf-gpu python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --time-steps 3 \
  --num-particles 1000 \
  --theta 0.02,-0.01,0.01 \
  --basis-set raw \
  --direction-filter log_kappa_scale,log_nu_scale,log_obs_noise_scale \
  --fd-mode ad-only \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --row-chunk-size 500 \
  --col-chunk-size 500 \
  --particle-chunk-size 512 \
  --dtype float32 \
  --tf32-mode enabled \
  --device /GPU:0 \
  --device-scope visible \
  --expect-device-kind gpu \
  --phase-label P82 manual score route decomposition N1000 GPU TF32 \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-manual-score-route-decomposition-n1000-gpu-tf32-2026-06-25.json
```

## Stop Conditions

Stop and write a blocker result if:

- the local syntax check fails;
- the diagnostic JSON is not produced;
- GPU device validation fails under escalated GPU execution;
- any decomposition component is nonfinite;
- decomposition components do not reconstruct the manual gradient;
- the run attempts `transport_ad_mode=full`.

## Result Template

The result note must include a decision table, run manifest, decomposition
table, FD residual comparison table, and explicit nonclaims.
