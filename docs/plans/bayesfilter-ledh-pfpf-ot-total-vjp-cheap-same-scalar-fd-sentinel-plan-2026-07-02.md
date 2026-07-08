# Cheap Same-Scalar FD Sentinel Plan

Date: 2026-07-02

Status: `DRAFT_FOR_REVIEW`

## Objective

Add and run a cheap regression sentinel for the corrected LEDH-PFPF-OT
`transport_ad_mode="full"` route.  The sentinel must compare the manual
total derivative against a finite-difference slope of the same executed
finite-Sinkhorn scalar in raw parameter directions.

The sentinel is a routine regression check.  It does not replace the expensive
`N=1000,T=3` raw-direction material gate recorded on 2026-07-01.

## Scientific Target

The target derivative is the total derivative of the fixed-randomness,
finite-Sinkhorn active-transport scalar evaluated by
`docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py` with:

- `ad-evaluation-mode=manual-reverse`;
- `manual-reverse-compiler=xla`;
- `transport-ad-mode=full`;
- streaming finite Sinkhorn transport;
- trusted GPU/XLA/TF32 execution.

The stopped partial derivative route must not be called the score of this
scalar.  Any result using stopped functional dependencies is a partial
derivative unless a separate derivation proves otherwise.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the cheap sentinel catch obvious regressions in the corrected full-route total derivative by comparing it with same-scalar regression FD? |
| Baseline/comparator | Same-scalar regression FD along raw theta directions from the same benchmark harness. |
| Primary pass criterion | For every checked raw direction, route prerequisites pass, FD regression values are finite, and the manual-minus-FD error passes one of: `<=2 MCSE`, `<=4 MCSE` with an external decreasing-MCSE ladder certificate from the same SIR target family, route, horizon, theta, seed set, and raw parameter coordinates, or relative error `<1%`. |
| Veto diagnostics | Wrong route metadata, non-GPU output, non-XLA manual reverse route, nonfinite objective/gradient/MCSE/FD slope, missing raw direction, bad FD fit quality, sign disagreement for a non-near-zero direction, or missing ladder certificate when using the `4 MCSE` arm. |
| Explanatory diagnostics | FD slope standard error, R-squared, selected base step, elapsed time, TensorFlow memory info, and exact pass arm. |
| Not concluded | No posterior correctness, exact nonlinear likelihood correctness, HMC production readiness, long-horizon validity, all-basis validity, or model-family transfer. |
| Artifact | Summary JSON and markdown result under `docs/plans`; raw benchmark JSON preserved separately. |

## Skeptical Plan Audit

Result: `PASS_FOR_EXECUTION_AFTER_CLAUDE_REVIEW`

- Wrong baseline: blocked by requiring same-scalar FD from the existing P8p
  regression harness, not a proxy metric.
- Proxy promotion: blocked by labeling the new check as a regression sentinel
  only.
- Missing stop conditions: blocked by explicit vetoes and no-overclaim rules.
- Unfair comparison: blocked by fixed theta, seeds, route, dtype, TF32 policy,
  transport policy, and raw basis.
- Hidden assumptions: explicitly records that the `4 MCSE` arm depends on an
  external decreasing-MCSE ladder artifact.
- Stale context: anchors to the 2026-07-01 full-route result and refuses to
  call stopped partial derivatives scores.
- Environment mismatch: GPU/CUDA and Claude calls must run with trusted
  escalated permissions per repository policy.
- Artifact risk: raw JSON plus summary JSON/markdown preserve the command,
  route metadata, and direction-level pass/fail rows.

## Implementation Steps

1. Add `docs/benchmarks/benchmark_p8p_total_vjp_same_scalar_fd_sentinel.py`.
   It will:
   - run the existing P8p regression FD harness with a cheap default
     `N=16,T=3`, two fixed seeds, raw basis, batched theta offsets, and
     `transport_ad_mode=full`;
   - preserve the raw benchmark JSON;
   - parse direction results and evaluate the three-arm rule;
  - optionally read the existing `N=64,256,1000` Phase 3 MCSE ladder JSON
     files as the decreasing-MCSE certificate for the `4 MCSE` arm, but only
     after verifying the certificate uses the same P8p scalar, raw parameter
     names, `transport_ad_mode="full"`, manual-reverse XLA route, `T=3`, and
     fixed seed set recorded by the Phase 3 artifacts;
   - write a compact summary JSON and markdown result.
2. Add focused parser/gate tests that do not initialize GPU.
3. Run local non-GPU checks for the new parser/gate.
4. Run the sentinel under trusted GPU/XLA/TF32.
5. Run the existing tiny LGSSM same-scalar manual route test as an entry sanity
   check for carrying the discipline to LGSSM.  This check is CPU-hidden FP64
   by design and is not evidence for SIR.
6. Write the result record.
7. Send the plan and execution result to Claude as bounded read-only review.

## Planned Sentinel Command

The wrapper will run the underlying benchmark with equivalent arguments:

```bash
python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --fd-mode enabled \
  --basis-set raw \
  --fd-evaluation-mode batched-theta \
  --theta-offset-batch-size 3 \
  --base-step-mode ad-signal \
  --target-objective-delta 0.15 \
  --adaptive-step-factors 1.0 \
  --regression-offsets -3,-2,-1,0,1,2,3 \
  --batch-seeds 81120,81121 \
  --time-steps 3 \
  --num-particles 16 \
  --theta 0.02,-0.01,0.01 \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode full \
  --row-chunk-size 16 \
  --col-chunk-size 16 \
  --particle-chunk-size 16
```

## Required Artifacts

- Plan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-cheap-same-scalar-fd-sentinel-plan-2026-07-02.md`
- New wrapper:
  `docs/benchmarks/benchmark_p8p_total_vjp_same_scalar_fd_sentinel.py`
- New tests:
  `tests/test_p8p_total_vjp_same_scalar_fd_sentinel.py`
- Raw sentinel JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-cheap-same-scalar-fd-sentinel-raw-2026-07-02.json`
- Summary JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-cheap-same-scalar-fd-sentinel-summary-2026-07-02.json`
- Result markdown:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-cheap-same-scalar-fd-sentinel-result-2026-07-02.md`

## Stop Conditions

Stop and write a blocker result if:

- Claude finds a material flaw in the plan after five focused review attempts;
- the wrapper cannot preserve the same-scalar FD comparator;
- the GPU sentinel cannot run in trusted GPU/XLA/TF32 context;
- route metadata is not `transport_ad_mode="full"`;
- output tensors are not on GPU;
- any checked raw direction is missing or nonfinite;
- the sentinel fails the stated three-arm rule;
- the LGSSM entry sanity check fails.

## Next-Phase Handoff

If this plan passes, the next justified action is to use the cheap sentinel as
the preflight check before running broader LGSSM or model-family carryover
diagnostics.  A sentinel pass does not authorize production promotion or claims
about exact likelihood correctness.
