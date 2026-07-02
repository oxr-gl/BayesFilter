# LEDH-PFPF-OT LGSSM OT-Reset Moment Hypothesis Test Plan

Date: 2026-06-26

## Question

The N1000 LGSSM statistical check passes Kalman for SIS/no-transport and
LEDH/no-OT, but fails only after OT/reset. Is the next correct target the
OT/reset step, and if so is the likely failure a wiring/normalization bug,
finite Sinkhorn approximation, or barycentric covariance contraction after
resetting weights to uniform?

## Trace Summary

- The statistical harness uses the manual streaming finite transport path:
  `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py` calls
  `_filterflow_manual_streaming_finite_transport_stopped_scale_keys` in
  `_transport_forward`.
- The core route also resets transported active rows to uniform weights after
  transport in `batched_annealed_transport_core_tf`.
- The streaming transport constructs a row-stochastic barycentric map from
  source weighted particles to uniform target rows, with source column mass
  intended to match `N * weights`.
- The previous decomposition result
  `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-value-decomposition-n1000-xla-2026-06-26.md`
  found:
  - 1d SIS/no-transport and LEDH/no-OT within the Kalman statistical gate;
  - 2d SIS/no-transport and LEDH/no-OT within the Kalman statistical gate;
  - LEDH+OT fails at prefix 1 in both 1d and 2d.

## Hypotheses

H1: Transport orientation or normalization is wrong.

Prediction: dense finite transport and streaming finite transport disagree on
the same small post-flow cloud, or dense column mass/row mass residuals are
large.

H2: Finite Sinkhorn settings cause the value gap.

Prediction: lowering epsilon or increasing finite Sinkhorn steps materially
reduces the post-OT covariance distortion and the value gap.

Decision refinement: H2 is not considered cleanly supported merely because a
tighter Sinkhorn setting reduces the magnitude of the same barycentric reset
effect. H2 is supported only if the tighter setting materially closes the
value/moment gap while preserving good dense/streaming parity and changing the
qualitative reset-moment pattern enough that finite approximation, rather than
reset semantics, is the most likely cause. Otherwise the result is recorded as
mixed H2/H3 or H3 with epsilon sensitivity.

H3: The barycentric transport plus uniform reset preserves the first moment but
contracts covariance enough to bias the next predictive likelihood.

Prediction: pre-OT weighted means and post-OT uniform means match, while
post-OT uniform covariance/trace is much smaller than the pre-OT weighted
covariance and Kalman filtered covariance. The value gap starts at the next
increment, matching the previous prefix-1 failure.

## Evidence Contract

Scientific/engineering question:

- Identify whether the next move should target OT/reset semantics rather than
  LEDH proposal density, Kalman reference, or gradient code.

Comparator:

- Kalman transition-first LGSSM value and filtered moments for 1d and 2d,
  `T=10`.
- LEDH/no-OT weighted post-flow cloud is the local no-OT comparator.
- Dense finite transport on a small shared cloud is the streaming transport
  orientation/normalization comparator.

Primary decision criterion:

- If dense and streaming finite transport agree on the same small cloud and
  row/column mass residuals are small, H1 is disfavored.
- If the post-OT uniform covariance trace is consistently and materially below
  the pre-OT weighted covariance trace while means remain matched, and the
  value gap appears at the next increment, H3 becomes the recommended target.
- If tighter Sinkhorn settings materially reduce both covariance distortion and
  value gap without leaving the same qualitative reset-moment pattern, H2
  becomes the recommended target. If the same reset-moment pattern remains, the
  result is mixed H2/H3 or H3 with epsilon sensitivity.

Diagnostics that can veto:

- Non-finite values, non-finite moments, or non-finite transport output.
- Dense-vs-streaming particle disagreement above `1e-4` on the same small
  cloud.
- Dense row residual or column residual above `1e-3` on the same small cloud.
- GPU-visible run not actually using GPU when the run is declared GPU/XLA.

Explanatory-only diagnostics:

- Runtime and XLA compile time.
- TF32 enabled status.
- Per-step ESS.
- Per-seed moment scatter.

What will not be concluded:

- No gradient correctness claim.
- No SIR correctness claim.
- No HMC readiness, posterior correctness, production readiness, or broad
  scientific validity claim.
- No claim that OT resampling is impossible in general; only this route and
  fixture are being diagnosed.

Artifact contract:

- Plan: this file.
- Diagnostic script:
  `docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py`.
- Dense/streaming parity record: the JSON must identify the exact shared cloud
  construction, including source state dimension, seed batch, time index,
  particle subset size, renormalized subset log-weights, epsilon, finite
  Sinkhorn step count, dense row residual, dense column residual, streaming row
  residual, and max absolute dense-vs-streaming transported-particle
  difference.
- Moment/value record: the JSON and Markdown must report the time index for
  each comparison. For each state dimension and setting, pre-OT weighted
  moments, post-OT uniform moments, and Kalman filtered moments are compared at
  the same filtering time index `t`. The value-gap column must separately
  report the likelihood increment at time `t` and the next increment at
  `t + 1` when available, because transport after time `t` can only affect the
  next predictive update.
- JSON result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-ot-reset-moments-2026-06-26.json`.
- Markdown result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-ot-reset-moments-2026-06-26.md`.

## Skeptical Plan Audit

- Wrong baseline risk: do not compare LEDH+OT directly to Kalman without also
  preserving LEDH/no-OT and pre-OT weighted moments.
- Proxy metric risk: moment contraction is not by itself a correctness proof;
  it only explains the value failure if it aligns with the next-increment gap.
- Hidden assumption risk: dense transport must be checked on the same cloud as
  streaming transport before blaming barycentric semantics.
- Environment risk: GPU/CUDA/XLA diagnostics must run with trusted GPU access;
  non-escalated CUDA failures are sandbox evidence only.
- Boundary risk: do not change production transport code during this diagnostic.
- Execution artifact risk: result must preserve command, device visibility,
  TF32 status, settings, seeds, and output paths.

Audit status: PASS for a bounded diagnostic. The plan tests the currently
localized boundary and includes vetoes for wrong transport orientation and bad
environment evidence.

## Planned Checks

1. Write the diagnostic script.
2. Run syntax check:

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py
```

3. Run a CPU small smoke with dense parity:

```bash
/usr/bin/timeout 300 python docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py \
  --device-scope cpu \
  --num-particles 128 \
  --dense-parity-particles 64 \
  --seed-count 10 \
  --state-dims 1 2 \
  --settings 0.5:8 \
  --xla \
  --output /tmp/ledh_ot_reset_moments_smoke.json \
  --markdown-output /tmp/ledh_ot_reset_moments_smoke.md
```

4. Run the GPU/XLA diagnostic on the failing N1000 setting and one tighter
   Sinkhorn setting:

```bash
BAYESFILTER_TEST_DEVICE_SCOPE=visible CUDA_VISIBLE_DEVICES=0 TF_FORCE_GPU_ALLOW_GROWTH=true \
/usr/bin/timeout 1200 python docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --num-particles 1000 \
  --dense-parity-particles 128 \
  --seed-count 10 \
  --state-dims 1 2 \
  --settings 0.5:8 0.25:16 \
  --xla \
  --tf32-mode enabled \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-ot-reset-moments-2026-06-26.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-ot-reset-moments-2026-06-26.md
```

## Stop Conditions

- Stop if the syntax check fails and patch the script before any GPU run.
- Stop if the CPU smoke fails before running the GPU diagnostic.
- Stop if dense-vs-streaming parity fails; analyze orientation/normalization
  before running larger settings.
- Stop if GPU-visible run reports no GPU devices.
- Stop after the two planned settings complete; do not expand into a sweep
  without a new plan.

## Expected Next Move After Results

- If H1 is supported, inspect transport formula orientation/normalization and
  patch the smallest transport-level bug.
- If H2 is supported, plan a bounded epsilon/iteration/chunk policy study.
- If H3 is supported, plan an algorithmic correction to reset semantics, such
  as covariance-preserving deterministic resampling, residual/noise
  regularization after barycentric OT, or a different resampling policy for
  likelihood-preserving LGSSM behavior.
