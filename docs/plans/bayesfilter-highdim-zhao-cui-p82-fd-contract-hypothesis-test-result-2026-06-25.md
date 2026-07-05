# P82 FD Contract Hypothesis Test Result

Date: 2026-06-25

## Decision Table

| Item | Status |
| --- | --- |
| Decision | Stop derivative interpretation and open a forward value-contract audit. |
| Primary criterion status | BLOCKED_BY_THETA0_VALUE_MISMATCH: no-resampling manual value and ordinary value route disagree at theta0. |
| Veto diagnostic status | No nonfinite values; trusted GPU run completed; no `transport_ad_mode=full`; no-resampling metadata present. |
| Main uncertainty | Which forward-route term causes the manual value to differ from the ordinary streaming value route. |
| Next justified action | Stepwise no-resampling value tie-out between `_manual_value_and_score_from_components` and `_objective_from_components`, before any LEDH VJP audit. |
| Not concluded | No LEDH VJP bug claim, no active-transport gradient correctness claim, no raw-FD oracle claim, no Zhao-Cui source-faithfulness claim, no HMC readiness claim. |

## Artifacts

| Artifact | Path |
| --- | --- |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p82-fd-contract-hypothesis-test-plan-2026-06-25.md` |
| Diagnostic JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-noresampling-fd-contract-diagnostic-2026-06-25.json` |
| Progress JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-noresampling-fd-contract-diagnostic-progress-2026-06-25.json` |
| Code guard test | `tests/test_ledh_pfpf_ot_p7_manual_score.py::test_p7_manual_no_resampling_transport_shortcuts_are_identity` |

## Claude Reviews

- `p82-fd-contract-micro-review-iter1`: `VERDICT: AGREE`; confirmed manual transport freezes branch artifacts while regression FD evaluates ordinary perturbed-theta values.
- `p82-fd-contract-plan-review-iter1`: `VERDICT: REVISE`; required theta0 value consistency as a hard discriminator and combined FD-SE/manual-MCSE uncertainty.
- `p82-fd-contract-plan-review-iter2`: `VERDICT: AGREE`; accepted the repaired plan.
- `p82-noresampling-manual-skip-review-iter1`: `VERDICT: AGREE`; accepted the no-resampling manual transport shortcut repair.

## Execution Notes

An initial command attempt failed before execution because the negative
`--regression-offsets` argument needed equals-form CLI syntax.  The plan command
was patched visibly to use:

```bash
--regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6
```

A second attempt exposed an invalid discriminator condition: the manual
no-resampling route computed full Sinkhorn transport and then discarded it with
`tf.where`, while the ordinary value route statically skipped transport when
the fixed resampling mask was all false.  That was repaired before the final
run:

- `_manual_forward_transport_tf`: under `transport_policy == "no-resampling"`,
  return `(post_flow, normalized_log_weights)` immediately.
- `_manual_transport_vjp_tf`: under `transport_policy == "no-resampling"`,
  return zero transport contributions; the caller already adds inactive
  passthrough cotangents.

Focused local checks after that repair:

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py tests/test_ledh_pfpf_ot_p7_manual_score.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_pfpf_ot_p7_manual_score.py`: `5 passed, 2 warnings`.
- `git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py tests/test_ledh_pfpf_ot_p7_manual_score.py docs/plans/bayesfilter-highdim-zhao-cui-p82-fd-contract-hypothesis-test-plan-2026-06-25.md`: passed.

## Run Manifest

| Field | Value |
| --- | --- |
| Command | `MPLCONFIGDIR=/tmp /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py ...` |
| Git commit recorded by artifact | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Device | `/GPU:0` |
| GPU | NVIDIA GeForce RTX 4080 SUPER |
| TensorFlow | `2.19.1` |
| Precision | `float32`, TF32 enabled |
| Particles | `1000` |
| Time steps | `3` |
| Seeds | `81120,81121,81122,81123,81124` |
| Seed microbatch size | `1` |
| Transport policy | `no-resampling` |
| Transport AD mode | `stabilized` |
| Transport gradient mode | `manual_streaming_finite_sinkhorn_stopped_scale_keys` |
| FD protocol | 13 points, drop highest/lowest values, regress remaining 11 points |
| Wall time | `323.82233958202414` seconds |

## Key Findings

The hard discriminator failed before derivative interpretation:

| Quantity | Value |
| --- | ---: |
| Manual objective from manual reverse route | `-120.70552825927734` |
| Ordinary value at theta0 from FD kappa window | `-119.86080169677734` |
| Ordinary value at theta0 from FD nu window | `-119.86080169677734` |
| Ordinary value at theta0 from FD obs-noise window | `-119.86080169677734` |

The ordinary theta0 value is internally consistent across all three FD windows,
but it does not match the manual reverse route's theta0 value.  Under the plan's
evidence contract, this blocks derivative residual interpretation and favors
H3: a forward value-route/manual-route contract mismatch.

Derivative residuals are recorded for completeness only:

| Parameter | Manual derivative | FD slope | FD slope SE | Manual MCSE | Residual | Residual / combined SE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `log_kappa_scale` | `-201.32192993164062` | `-187.10777282714844` | `0.7982507348060608` | `2.895693778991699` | `-14.214157104492188` | `-4.732207312207719` |
| `log_nu_scale` | `79.99671173095703` | `74.12387084960938` | `0.08101634681224823` | `1.2112512588500977` | `5.872840881347656` | `4.83776407927423` |
| `log_obs_noise_scale` | `31.455028533935547` | `28.196369171142578` | `0.042001232504844666` | `0.8638631105422974` | `3.2586593627929688` | `3.7677434313304636` |

Because theta0 values disagree, these derivative residuals are not valid
evidence for or against the LEDH primitive VJP.

## Next Move

Create and run a small no-resampling value-contract audit:

1. Use the same seeds, theta, N, and T, but start with a tiny N/T smoke if needed.
2. Compare `_manual_value_and_score_from_components(...)[\"log_likelihood\"]`
   against `_objective_from_components(...)[1]`.
3. Instrument per-time-step quantities on both routes:
   `prior_means`, `pre_flow`, `flow.pre_flow_log_density`, `post_flow`,
   `transition_log_density`, `observation_log_density`,
   `flow.forward_log_det`, `corrected_log_weights`, `incremental`,
   `normalized_log_weights`, and post-step particles.
4. Stop at the first differing term.
5. Only after theta0 values match should we resume derivative/FD interpretation.
