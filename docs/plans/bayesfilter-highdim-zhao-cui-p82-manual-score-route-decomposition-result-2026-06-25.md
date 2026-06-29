# P82 Manual Score Route Decomposition Result

Date: 2026-06-25
Status: COMPLETE_LOCALIZED_TO_TRANSITION_MEAN_LEDHFLOW_PRIOR_CANDIDATE

## Question

For the P82 LEDH-PFPF-OT SIR d18 route, which manual score contribution carries
the robust kappa/nu mismatch between the manual reverse score and the FD
consistency diagnostics?

## Decision Table

| Field | Result |
|---|---|
| Decision | The mismatch is localized to the rate-parameter transition-mean channels, not to the observation-noise covariance channels.  The strongest next audit target is the LEDH flow direct `prior_means` cotangent. |
| Primary criterion status | PASS: decomposition is finite and reconstructs the manual per-seed gradient with max absolute delta `3.0517578125e-05`. |
| Veto diagnostic status | PASS: no `transport_ad_mode=full`, no dense transport matrix, no Zhao-Cui comparator/oracle claim, valid JSON artifacts, GPU-visible run, finite objective and finite gradients. |
| Main uncertainty | The decomposition is an accounting diagnostic for the current manual reverse pass.  It does not by itself prove which mathematical dependency is wrong. |
| Next justified action | Run a local primitive audit of `_batched_ledh_linearized_flow_with_aux_tf` / `_batched_ledh_linearized_flow_vjp`, with exact-path bounded review if needed, focusing on `prior_means` and the coupled `x0 - prior_means` dependency. |
| Not concluded | No LEDH gradient correctness claim, no posterior correctness claim, no HMC readiness claim, no FD-oracle claim, and no Zhao-Cui source-faithfulness claim. |

## Artifacts

| Artifact | Path |
|---|---|
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p82-manual-score-route-decomposition-plan-2026-06-25.md` |
| Diagnostic JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-manual-score-route-decomposition-n1000-gpu-tf32-2026-06-25.json` |
| Memory sidecar | `docs/plans/bayesfilter-highdim-zhao-cui-p82-manual-score-route-decomposition-n1000-gpu-tf32-memory-samples-2026-06-25.json` |
| Code instrumented | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py` |
| Runner instrumented | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py` |
| Reconstruction test | `tests/test_ledh_pfpf_ot_p7_manual_score.py` |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Conda env | `/home/chakwong/anaconda3/envs/tf-gpu` |
| TensorFlow | `2.19.1` |
| Device | GPU-visible, `/GPU:0` |
| Shape | N1000, five seeds, T3, state dim 18, obs dim 9 |
| Seeds | `81120,81121,81122,81123,81124` |
| Theta | `log_kappa_scale=0.02`, `log_nu_scale=-0.01`, `log_obs_noise_scale=0.01` |
| Route | `ad_evaluation_mode=manual-reverse`, `manual_score_decomposition=true` |
| Compiler | XLA, one seed microbatch per compiled call |
| Transport | streaming, `manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, chunks `500/500/512` |
| Sinkhorn | 10 iterations, epsilon 1.0 |
| FD mode | `ad-only`; no new FD sweep was run |
| Wall time | `1920.0013722889998` seconds |
| XLA compile/first-call timings | `393.92`, `378.30`, `366.69`, `363.56`, `415.47` seconds |
| TensorFlow allocator peak | `58512896` bytes |

## Manual Score Decomposition

Manual gradient from this run:

| Parameter | Manual gradient |
|---|---:|
| `log_kappa_scale` | `-157.29917907714844` |
| `log_nu_scale` | `70.6307144165039` |
| `log_obs_noise_scale` | `46.88982009887695` |

Component means:

| Component | `log_kappa_scale` | `log_nu_scale` | `log_obs_noise_scale` |
|---|---:|---:|---:|
| `observation_density_covariance` | `0.0` | `0.0` | `46.60095977783203` |
| `ledh_flow_observation_covariance` | `0.0` | `0.0` | `0.28886252641677856` |
| `transition_mean_from_transition_density` | `-229.6639862060547` | `92.89944458007812` | `0.0` |
| `transition_mean_from_ledh_flow_prior` | `130.36819458007812` | `-52.38304901123047` | `0.0` |
| `transition_mean_from_pre_flow_clamp` | `-58.003395080566406` | `30.114315032958984` | `0.0` |

The observation covariance terms sum to `46.88982230424881`, matching the
manual obs-noise score and the earlier FD checks.  The rate terms are entirely
inside the transition-mean channels.

## FD Residual Comparison

Using the prior N1000 13-point FD artifact as the FD consistency reference:

| Parameter | Manual gradient | 13-point FD slope | FD minus manual | FD slope SE | Residual / SE |
|---|---:|---:|---:|---:|---:|
| `log_kappa_scale` | `-157.29917907714844` | `-263.2330322265625` | `-105.93385314941406` | `1.1118820905685425` | about `-95.3` |
| `log_nu_scale` | `70.6307144165039` | `105.13096618652344` | `34.50025177001953` | `0.11481457948684692` | about `300.5` |
| `log_obs_noise_scale` | `46.88982009887695` | `46.83678436279297` | `-0.053035736083984375` | `0.062081485986709595` | about `-0.85` |

The N2500 FD artifact gives the same qualitative conclusion: kappa/nu are far
outside the FD slope standard errors, while obs-noise remains within the stated
diagnostic tolerance.

## Interpretation

The route decomposition does not support another FD-protocol explanation.  It
supports a rate-parameter adjoint accounting issue.  The observation-noise path
is behaving consistently: `observation_density_covariance` plus
`ledh_flow_observation_covariance` reconstructs the manual obs-noise score, and
that score agrees with the FD diagnostics.

For kappa/nu, the standout term is
`transition_mean_from_ledh_flow_prior`: it pulls kappa positive by about
`+130.37` and nu negative by about `-52.38`.  The FD residual has the opposite
sign: the manual gradient needs about `-105.93` more kappa and `+34.50` more nu
to match the FD consistency estimate.  This does not prove that the whole
`prior_means` term should be removed, but it makes the LEDH flow direct
`prior_means` cotangent the highest-value mathematical audit target.

The next diagnostic should be local, not a full-filter FD rerun: test the
manual VJP of `_batched_ledh_linearized_flow_with_aux_tf` against finite
differences with respect to `prior_means`, `pre_flow_particles`, and their
coupled SIR relation `pre_flow = clamp(prior_mean + noise)`.  That should tell
us whether the current flow primitive VJP is mathematically wrong or whether
the outer chain rule is using the wrong stopped/coupled contract.

## Checks

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/test_ledh_pfpf_ot_p7_manual_score.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_pfpf_ot_p7_manual_score.py`: `4 passed, 2 warnings`.
- `git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/test_ledh_pfpf_ot_p7_manual_score.py docs/plans/bayesfilter-highdim-zhao-cui-p82-manual-score-route-decomposition-plan-2026-06-25.md`: passed.
- JSON parse check for the diagnostic JSON and memory sidecar: passed.
