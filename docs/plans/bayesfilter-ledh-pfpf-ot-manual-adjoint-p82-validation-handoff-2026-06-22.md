# Manual Adjoint Return-To-P82 Validation Handoff

Date: 2026-06-22

Status: P82_RETURN_BLOCKED_BY_BENCHMARK_WIRING

## Summary

The manual-adjoint program has produced a reviewed local route candidate:

```text
manual_streaming_finite_sinkhorn_stopped_scale_keys
```

M6 local checks and Claude R3 one-path review support the narrow claim that this
route matches the M5 dense opt-in route on tiny CPU/float64 fixtures, rejects
unsupported combinations, and returns an empty `(B,0,0)` transport matrix from
the experimental batched core.

P82 cannot resume validation yet.  The P82 SIR d18 benchmark path currently
does not expose or pass `transport_gradient_mode` into the streaming value core.
The active streaming wrapper still calls the batched transport core with
`transport_gradient_mode="raw"`.

## Reviewed M6 Evidence

Supported local route:

- `transport_gradient_mode="manual_streaming_finite_sinkhorn_stopped_scale_keys"`
- `transport_plan_mode="streaming"`
- `transport_ad_mode="stabilized"`
- scalar `epsilon`
- no warmstart
- static positive finite Sinkhorn iterations

Unsupported combinations:

- dense plan with manual streaming route;
- warmstart with manual streaming route;
- `transport_ad_mode="full"`;
- vector epsilon.

M6 observed maxima:

- particle value error against dense opt-in route:
  `1.1102230246251565e-16`;
- particle/log-weight gradient error against dense opt-in route:
  `4.163336342344337e-17`;
- returned transport-matrix size: `0.0`.

Review:

- Claude R3 one-path review of
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase6-streaming-memory-route-result-2026-06-22.md`
  returned `VERDICT: AGREE`.

## Blocking Wiring Gap

The active P82 benchmark path is:

```text
docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
  -> docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
  -> streaming_batched_ledh_pfpf_ot_value_core_tf
  -> batched_annealed_transport_core_tf
```

The CLI exposes:

- `--transport-plan-mode`;
- `--transport-ad-mode`;
- chunk sizes;
- Sinkhorn settings.

The CLI does not expose:

- `--transport-gradient-mode`.

The streaming value core call currently passes:

```text
transport_gradient_mode="raw"
```

to `batched_annealed_transport_core_tf`.  Therefore an exact governed P82
actual-gradient command for the manual streaming route cannot yet be stated.

## P82 Comparator Contract Preserved

The downstream FD comparator contract remains unchanged:

- same LEDH scalar;
- Zhao-Cui removed from active pass/fail path for now;
- `N=1000`;
- five seeds `81120,81121,81122,81123,81124`;
- 13 offsets `-6..6`;
- `--trim-extreme-offsets 1`;
- `--trim-extreme-mode value`;
- OLS on 11 retained mean-over-seed values;
- slope standard error recorded;
- FD is a noisy diagnostic comparator, not an oracle.

## Forbidden Commands

Do not launch the old governed actual-gradient route:

```text
--transport-plan-mode streaming
--transport-ad-mode full
```

at `N=10000` as raw full-graph AD/JVP through the whole Sinkhorn transport solve.
That route is already recorded as memory/runtime infeasible.

Do not run P82 FD validation until the actual-gradient side is wired to the
manual streaming route and locally checked.

## Required Next P82 Subplan

Before P82 validation resumes, write and review a new P82 wiring subplan that
does all of the following:

1. Adds or otherwise supplies a bounded `transport_gradient_mode` route option
   through the P82 benchmark path.
2. Ensures the SIR d18 streaming value core can call
   `batched_annealed_transport_core_tf` with
   `manual_streaming_finite_sinkhorn_stopped_scale_keys`.
3. Updates result metadata so the actual route records
   `gradient_mode="manual_streaming_finite_sinkhorn_stopped_scale_keys"` rather
   than `"raw"`.
4. Adds CPU-hidden local tests for CLI parsing, metadata, and route forwarding.
5. Runs only a tiny trusted GPU smoke after local tests and review.
6. Preserves the P82 13-point regression-FD comparator protocol unchanged.

## Candidate Commands After Wiring

These are not executable yet.  They show the intended downstream command shape
after a reviewed wiring patch adds the missing gradient-mode option.

Actual-gradient candidate:

```bash
env MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 10000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode reverse-gradient \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 FD-only LEDH N10000 manual-streaming actual gradient GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-ad-mode stabilized \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --basis-set raw \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n10000-manual-streaming-progress-2026-06-22.json \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n10000-manual-streaming-gpu-tf32-2026-06-22.json
```

Regression-FD candidate:

```bash
env MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 1000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode reverse-gradient \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 FD-only LEDH N1000 raw 13-point regression FD manual-streaming GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-ad-mode stabilized \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --base-step-mode ad-signal \
  --target-objective-delta 0.15 \
  --adaptive-step-factors 1.0 \
  --min-adaptive-base-step 0.00025 \
  --max-adaptive-base-step 0.05 \
  --regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6 \
  --trim-extreme-offsets 1 \
  --trim-extreme-mode value \
  --fd-evaluation-mode batched-theta \
  --theta-offset-batch-size 13 \
  --basis-set raw \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n1000-raw-regression-fd-manual-streaming-progress-2026-06-22.json \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n1000-raw-regression-fd-manual-streaming-gpu-tf32-2026-06-22.json
```

These commands must remain non-executable placeholders until the missing
`--transport-gradient-mode` wiring exists and passes local checks.

## Nonclaims

This handoff does not conclude:

- P82 FD agreement;
- N10000 runtime feasibility;
- GPU/TF32 success for the manual streaming route;
- HMC/NUTS readiness;
- posterior correctness;
- exact likelihood correctness;
- default-gradient readiness;
- production readiness;
- Zhao-Cui source-faithfulness.

## Decision

P82 return status:

```text
P82_RETURN_BLOCKED_BY_BENCHMARK_WIRING
```

The next safe action is a narrow P82 wiring subplan, not validation execution.
