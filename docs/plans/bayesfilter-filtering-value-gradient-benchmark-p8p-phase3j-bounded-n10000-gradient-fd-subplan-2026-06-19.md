# P8p Phase 3j-b Subplan: Bounded N=10000 Gradient/FD Validation

Date: 2026-06-19

Status: `DRAFT_EXECUTABLE_AFTER_PHASE3J_BLOCKER`

## Phase Objective

Continue the SIR d18 `N=10000` validation of the Phase 3i candidate
`transport_ad_mode=full` contract, but replace the full three-direction,
9-point FD diagnostic with a bounded and observable sequence:

1. run AD/JVP-only at `N=10000` over five fixed seeds to measure runtime,
   gradient, seed MCSE, and direction geometry;
2. only if AD/JVP-only completes in bounded time, run one targeted
   semantic-orthogonal FD line for `tau_perp_given_rho`;
3. preserve progress JSON after AD and after each FD window.

This phase remains a gradient-contract diagnostic, not an HMC readiness phase.

## Entry Conditions

- Phase 3i showed `transport_ad_mode=full` was the first active-transport AD
  contract to pass local AD/FD agreement at `T=3`, `N=64`.
- Phase 3j attempted exact five-seed, three-direction, 9-point FD at
  `N=10000`, but the run remained active for more than six hours with no JSON
  result and was killed after user authorization.
- Static checks passed after adding generic `--fd-mode ad-only`,
  `--direction-filter`, and `--progress-output` controls to the FD harness.
- A tiny trusted-GPU mechanics smoke verified the new controls.

## Required Artifacts

- Phase 3j blocker result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-n10000-full-transport-fd-result-2026-06-19.md`
- This subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-bounded-n10000-gradient-fd-subplan-2026-06-19.md`
- AD/JVP-only JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-bounded-n10000-ad-only-gpu-tf32-2026-06-19.json`
- AD/JVP-only progress JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-bounded-n10000-ad-only-progress-2026-06-19.json`
- Targeted FD JSON, only if AD/JVP-only completes:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-bounded-n10000-tau-fd-gpu-tf32-2026-06-19.json`
- Targeted FD progress JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-bounded-n10000-tau-fd-progress-2026-06-19.json`
- Phase 3j-b result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-bounded-n10000-gradient-fd-result-2026-06-19.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the `full` active-transport AD contract produce a usable, finite, five-seed `N=10000` SIR d18 gradient under TF32/GPU, and does the previously suspicious tau-like direction agree with targeted regression FD? |
| Baseline/comparator | Phase 3i `N=64` full-mode pass; Phase 3j full FD runtime blocker. |
| Primary criterion | AD/JVP-only must complete with finite objective/gradient, GPU placement, TF32 enabled, and recorded seed MCSE.  The targeted tau FD is promoted to evaluation only if AD/JVP-only finishes within the wall-time stop. |
| Targeted FD criterion | For `tau_perp_given_rho`, the AD directional derivative and 7-point OLS FD slope must be interpretable relative to FD slope SE, seed MCSE, and residual diagnostics. |
| Veto diagnostics | Missing GPU placement, TF32 disabled, nonfinite objective/gradient/slope, missing output artifact, progress file stuck beyond stop time, or FD line too nonlinear to interpret. |
| Explanatory diagnostics | Runtime, GPU memory, seed-gradient covariance/correlation, MCSE, selected adaptive base step, FD residuals, slope SE, and progress records. |
| Not concluded | HMC/NUTS readiness, posterior validity, exact likelihood correctness, full-horizon stability, production/default readiness, or leaderboard ranking. |
| Artifact preserving result | Phase 3j-b JSON artifacts and result markdown. |

## Skeptical Plan Audit

- Wrong baseline risk: controlled.  The comparator is Phase 3i full-mode local
  pass and Phase 3j runtime blocker, not a Zhao-Cui or monograph artifact.
- Proxy metric risk: controlled.  AD-only completion does not prove FD
  correctness; it only gates whether a targeted FD run is feasible.
- Missing stop condition risk: controlled.  If AD-only runs longer than a
  bounded wall-time budget with no artifact, stop and write a blocker.  If FD
  progress does not advance after a completed AD phase, stop rather than wait
  silently.
- Unfair comparison risk: controlled.  The target, theta, seeds, transport
  policy, Sinkhorn settings, chunking, dtype, TF32 mode, and fixed random
  streams are inherited from Phase 3j.
- Hidden assumption risk: controlled.  The tau direction is prioritized because
  it was the direction that remained problematic in earlier transport AD
  ablations before `full`; success for tau alone does not certify rho or omega.
- Artifact adequacy risk: controlled.  The run emits progress JSON after AD and
  each FD window, so a long run can be diagnosed without waiting for final
  output.

Audit result: `PASS_TO_RUN_BOUNDED_SEQUENCE`.

## Commands

### 1. AD/JVP-Only Gate

```bash
env MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 10000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode forward-jvp \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P8p Phase 3j-b N10000 full transport AD-only GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-ad-mode full \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --basis-set semantic-orthogonal \
  --progress-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-bounded-n10000-ad-only-progress-2026-06-19.json \
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-bounded-n10000-ad-only-gpu-tf32-2026-06-19.json
```

### 2. Targeted Tau FD Gate

Run only if the AD/JVP-only gate completes with finite values and acceptable
runtime.

```bash
env MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 10000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode forward-jvp \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P8p Phase 3j-b N10000 full transport targeted tau FD GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-ad-mode full \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --base-step-mode ad-signal \
  --target-objective-delta 0.15 \
  --adaptive-step-factors 1.0 \
  --min-adaptive-base-step 0.00025 \
  --max-adaptive-base-step 0.05 \
  --regression-offsets=-3,-2,-1,0,1,2,3 \
  --basis-set semantic-orthogonal \
  --direction-filter tau_perp_given_rho \
  --progress-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-bounded-n10000-tau-fd-progress-2026-06-19.json \
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-bounded-n10000-tau-fd-gpu-tf32-2026-06-19.json
```

## Required Checks

Before running:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py
```

After each gate:

- validate the JSON with `python -m json.tool`;
- inspect elapsed time, GPU placement, TF32 status, finite values, MCSE, and
  progress records;
- write or update the Phase 3j-b result.

## Forbidden Claims And Actions

- Do not claim HMC/NUTS readiness.
- Do not claim posterior validity or exact likelihood correctness.
- Do not promote `transport_ad_mode=full` to the default.
- Do not disable TF32.
- Do not use one-seed semantic-orthogonal geometry as scientific evidence.
- Do not touch Zhao-Cui or monograph artifacts.

## Handoff Conditions

If AD/JVP-only and targeted tau FD complete with usable diagnostics, hand off
to a later phase that decides whether to test rho and omega separately or move
to a small HMC-facing repeated-gradient smoke.  If AD-only is too slow or FD
does not progress, close with a runtime blocker and return to transport-core
optimization before further `N=10000` FD validation.

## Stop Conditions

Stop and write a blocker result if:

- the AD/JVP-only gate does not produce an artifact in bounded time;
- trusted GPU placement is absent;
- TF32 is disabled;
- any objective, gradient, or FD slope is nonfinite;
- the progress JSON stops advancing for the targeted FD run;
- GPU memory is again near the device ceiling with low utilization and no
  artifact progress.
