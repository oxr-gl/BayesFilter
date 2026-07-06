# P01 Value/Gradient Instrumentation Result

Date: 2026-06-24

Status: `PASS_P02_READY`

## Phase Objective

Implement a focused TensorFlow/TFP LGSSM value/gradient calibration harness and
tests. The harness measures low-rank residual diagnostics alongside exact
Kalman posterior value, posterior gradient, and fixed local peak-neighborhood
diagnostics at predeclared probe parameters.

## Artifacts

- Harness:
  `docs/benchmarks/benchmark_low_rank_ledh_posterior_gradient_calibration.py`
- Focused tests:
  `tests/test_low_rank_ledh_posterior_gradient_calibration.py`
- CPU-hidden smoke JSON:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p01-smoke-2026-06-24.json`
- CPU-hidden smoke Markdown:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p01-smoke-2026-06-24.md`
- Refreshed P02 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02-reproduction-determinism-subplan-2026-06-24.md`

## Checks Run

| Check | Result |
| --- | --- |
| Skeptical implementation audit | `PASS`; recorded in the execution ledger before code changes. |
| Compile check | `PASS`; `python -m py_compile` passed for the new harness and test. |
| Focused pytest | `PASS`; `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_low_rank_ledh_posterior_gradient_calibration.py` passed `4/4`. |
| No-active-path-NumPy audit | `PASS`; `rg -n "import numpy|from numpy|\\.numpy\\("` returned no hits for the new harness, test, and touched low-rank solver path. |
| CPU-hidden smoke | `PASS`; JSON/Markdown artifacts written with `evidence_class=cpu_hidden_command_shape_debug_only`. |

Pytest emitted TensorFlow/TFP/gast deprecation warnings during tracing. These
warnings are explanatory only and did not fail the focused checks.

## Smoke Command

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_low_rank_ledh_posterior_gradient_calibration.py \
  --case-ids lgssm_small_exact_ref \
  --seeds 91001 \
  --route low_rank \
  --num-particles 8 \
  --time-steps 1 \
  --low-rank-rank 4 \
  --low-rank-max-projection-iterations 8 \
  --particle-chunk-size 4 \
  --warmups 0 \
  --repeats 1 \
  --dtype float32 \
  --tf32-mode disabled \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p01-smoke-2026-06-24.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p01-smoke-2026-06-24.md \
  --quiet
```

The smoke command intentionally hid GPU devices. Its output is command-shape
evidence only.

## Instrumentation Summary

The new harness emits:

- fixed LGSSM theta probes for transition-covariance and observation-covariance
  log scales;
- exact Kalman posterior value and TensorFlow gradient;
- route posterior value and TensorFlow gradient for streaming or low-rank
  routes;
- value absolute error, gradient relative norm error, max coordinate error,
  and cosine similarity;
- fixed probe-neighborhood peak summary, explicitly not a global MAP claim;
- low-rank factor residuals, induced row/column residuals, projection
  iterations, finite/nonnegative factor checks, and nonmaterialization status;
- compact diagnostic repeat summaries for P02 jitter checks.

## Smoke Metrics

The tiny CPU-hidden smoke used only `N=8`, `T=1`, and rank `4`. It is not a
quality screen. Its descriptive output was:

| Metric | Value |
| --- | ---: |
| Artifact status | `PASS` |
| Hard vetoes | `[]` |
| Peak probe match | `False` |
| Max value absolute error over probes | `0.576040506362915` |
| Max gradient relative norm error | `6.747677223332192` |
| Min gradient cosine similarity | `0.256657694114053` |
| Center factor marginal residual | `8.568912744522095e-05` |

These numbers only demonstrate that the harness emits the required fields.
They do not calibrate a threshold and do not rank the route.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | P01 can instrument LGSSM residual/value/gradient/peak diagnostics in a TensorFlow/TFP harness suitable for later GPU calibration. |
| Baseline/comparator | Exact Kalman value/gradient oracle is present; streaming and low-rank route hooks are present. |
| Primary criterion | Satisfied for instrumentation: harness and tests exist, focused checks pass, structured metrics are emitted, and no active-path NumPy was introduced. |
| Veto diagnostics | No P01 veto fired. |
| Explanatory diagnostics | CPU-hidden smoke output is intentionally small and descriptively poor on some route metrics; this is not a P01 failure. |
| Not concluded | No threshold calibration, GPU readiness, posterior correctness, HMC readiness, package default readiness, public API readiness, statistical superiority, or scientific validity. |

## Decision Table

| Decision | Status |
| --- | --- |
| Phase result | `PASS_P02_READY`. |
| Primary criterion status | Passed. |
| Veto diagnostic status | No P01 veto fired. |
| Main uncertainty | Trusted GPU/XLA behavior and repeat/seed jitter are untested until P02. |
| Next justified action | Enter P02 reproduction after trusted GPU precheck. |
| What is not being concluded | The smoke output does not validate the low-rank threshold, route quality, default readiness, posterior correctness, HMC readiness, statistical superiority, or scientific validity. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | No P01 hard veto. |
| Statistically supported ranking | None; no ranking attempted. |
| Descriptive-only differences | Smoke value/gradient/peak differences are descriptive command-shape outputs only. |
| Default-readiness | Not assessed. |
| Next evidence needed | P02 trusted GPU/XLA reproduction on seeds `91001,91002,91003` with repeats and exact value/gradient/peak diagnostics. |

## Next-Phase Handoff

P02 may proceed only after bounded review convergence. P02 must use the
refreshed command shape in
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02-reproduction-determinism-subplan-2026-06-24.md`,
must run in trusted GPU/XLA context, and must not tune thresholds or claim
calibration from reproduction alone.
