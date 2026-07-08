# P82 Phase 8R Result: Governed FD Consistency

status: COMPLETE_DIAGNOSTIC_ISSUE_ROWS_EXCEED_2SE
date: 2026-06-24
phase: P8R-GOVERNED-FD-CONSISTENCY

## Question

Are the P7R N10000 actual-gradient components consistent with P8R N1000
13-point regression-FD slopes for the same LEDH scalar in raw theta directions?

## Decision

No, not as a validation result.  The governed FD run completed and satisfied
the protocol metadata, but two raw theta rows exceed the 2 combined-SE triage
threshold by a large margin.

This is a diagnostic issue result, not a proof that either the actual-gradient
route or FD route is correct or incorrect.  It blocks any P82 claim of FD
consistency.

## Decision Table

| Field | Result |
|---|---|
| Decision | P8R completed but does not validate FD consistency; kappa and nu rows are diagnostic issues. |
| Primary protocol status | PASS: P8R JSON records `fd_mode=enabled`, `ad_evaluation_mode=manual-reverse`, `compiler.mode=xla`, GPU outputs, five seeds, N1000, 13 raw FD points, 11 value-trimmed fit points, and route metadata. |
| P7R/P8R same-scalar metadata | PASS: theta, transport policy, transport route, Sinkhorn settings, dtype, and TF32 mode match. |
| Combined-SE triage status | FAIL/ISSUE: `log_kappa_scale` and `log_nu_scale` exceed 2 combined SE; `log_obs_noise_scale` is within 2 combined SE. |
| Veto diagnostic status | No timeout, OOM, missing artifact, `transport_ad_mode=full`, Zhao-Cui comparator use, or protocol metadata veto. The >2SE rows block validation claims. |
| Main uncertainty | FD uses N1000 while actual gradient uses N10000; regression slopes are precise but may be estimating a different particle-count approximation or exposing a route/linearity mismatch. |
| Next justified action | Stop P82 validation and write P9R closeout. A future remediation should isolate whether the issue is N mismatch, FD line nonlinearity/window choice, seed coupling, or an actual-gradient route defect. |
| Not concluded | Exact correctness, posterior validity, HMC readiness, production readiness, scientific superiority, or calibrated hypothesis-test validity. |

## Artifact Summary

| Artifact | Path |
|---|---|
| P8R subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-consistency-subplan-2026-06-24.md` |
| P8R JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-gpu-tf32-2026-06-24.json` |
| P8R progress JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-progress-2026-06-24.json` |
| P8R memory sidecar | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-memory-samples-2026-06-24.json` |
| P7R actual-gradient comparator | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-gpu-tf32-2026-06-24.json` |

## P7R/P8R Same-Scalar Metadata Check

| Field | Status |
|---|---|
| Theta | PASS: both use `log_kappa_scale=0.02`, `log_nu_scale=-0.01`, `log_obs_noise_scale=0.01`. |
| Transport policy | PASS: both use `active-all`. |
| Transport plan mode | PASS: both use `streaming`. |
| Transport gradient mode | PASS: both use `manual_streaming_finite_sinkhorn_stopped_scale_keys`. |
| Transport AD mode | PASS: both use `stabilized`. |
| Sinkhorn settings | PASS: both use `sinkhorn_iterations=10`, `sinkhorn_epsilon=1.0`. |
| dtype / TF32 | PASS: both use `float32`, TF32 enabled. |

## FD Protocol Check

| Field | Status |
|---|---|
| `fd_mode` | PASS: `enabled`. |
| AD side | PASS: `manual-reverse`, XLA. |
| Seeds | PASS: `81120,81121,81122,81123,81124`. |
| Particles | PASS: P8R uses N1000. |
| FD offsets | PASS: 13 offsets `-6..6`. |
| Fit points | PASS: one low-value and one high-value point dropped; 11 fit points retained. |
| Trim mode | PASS: `value`. |
| FD evaluation | PASS: `batched-theta`, `theta_offset_batch_size=13`. |
| GPU output | PASS. |

## Comparison Table

| Direction | P7R N10000 actual gradient | P7R seed SE | P8R FD slope | FD slope SE | Difference | Combined SE | Difference / combined SE | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `log_kappa_scale` | `-156.6765899658203` | `5.062162399291992` | `-263.2330322265625` | `1.1118820905685425` | `106.55644226074219` | `5.182834160971459` | `20.559492924382802` | ISSUE |
| `log_nu_scale` | `70.43897247314453` | `1.2023807764053345` | `105.13096618652344` | `0.11481457948684692` | `-34.691993713378906` | `1.2078501227933192` | `-28.722101408698713` | ISSUE |
| `log_obs_noise_scale` | `46.97493362426758` | `0.038100458681583405` | `46.83678436279297` | `0.062081485986709595` | `0.13814926147460938` | `0.07284061953378118` | `1.8965964644293025` | WITHIN_2SE |

## Regression Diagnostics

| Direction | Regression R2 | Max abs residual | Raw points | Fit points | Trim mode |
|---|---:|---:|---:|---:|---|
| `log_kappa_scale` | `0.9998394250869751` | `0.01793670654296875` | 13 | 11 | `value` |
| `log_nu_scale` | `0.9999892711639404` | `0.00209808349609375` | 13 | 11 | `value` |
| `log_obs_noise_scale` | `0.9999842047691345` | `0.00118255615234375` | 13 | 11 | `value` |

The regressions are very linear over the selected window.  That makes the
large kappa/nu discrepancy more concerning as a route or approximation mismatch
signal, not less.

## Runtime / Memory

| Quantity | Value |
|---|---:|
| Wall time | `2183.522269928013` seconds |
| TF allocator peak | `2.056873083114624` GiB |
| Compile plus first call timings | `[358.9863392589905, 364.60291457601124, 364.8326095030061, 377.86183939300827, 365.06105048701284]` |
| Warm-call timings by context | `[[0.2826656030083541], [0.42697796499123797], [0.3389297940011602], [0.2627283899928443], [0.2571643780102022]]` |

P8R is still compile-heavy because the current harness creates `tf.function`
inside the seed-context loop and retraces.  This is a performance follow-up,
not the reason P8R failed the consistency criterion.

## Checks

- `CUDA_VISIBLE_DEVICES=-1 /home/chakwong/anaconda3/envs/tf-gpu/bin/python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q`: `16 passed, 2 warnings`.
- `CUDA_VISIBLE_DEVICES=-1 /home/chakwong/anaconda3/envs/tf-gpu/bin/python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`: passed.
- `git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-consistency-subplan-2026-06-24.md`: passed.
- Trusted `nvidia-smi`: GPU visible.
- Trusted TensorFlow GPU probe: TensorFlow `2.19.1`, GPU visible.
- `python -m json.tool` on P8R JSON, progress JSON, and memory sidecar: passed.
- P8R protocol/comparison validation script: protocol passed; combined-SE triage failed for two rows.

## Non-Claims

P8R does not prove the manual gradient is wrong, FD is right, or either method
is correct.  It does not claim posterior correctness, HMC readiness, default
readiness, production readiness, scientific superiority, or Zhao-Cui comparator
readiness.

## Handoff

Proceed to P9R closeout with an issue result.  P82 should not be described as
validated.  A future remediation plan should target the kappa/nu mismatch
before any HMC/default/scientific claim.
