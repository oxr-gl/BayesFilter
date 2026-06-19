# P8p Phase 3h Subplan: Dense-vs-Streaming Transport AD Contract

Date: 2026-06-19

Status: `DRAFT_EXECUTABLE`

## Phase Objective

Localize the Phase 3f active-transport AD/FD mismatch inside the relaxed
annealed transport implementation by comparing the same repaired gradient
diagnostic under:

- streaming transport plan mode;
- dense transport plan mode.

The phase does not change the operational default.  It only exposes and tests a
diagnostic switch that the underlying value core already supports.

## Entry Conditions

- Phase 3f with active streaming transport produced smooth FD plateaus that
  disagreed with AD.
- Phase 3g with transport skipped made `rho` and `tau_perp` agree with AD and
  left only a much smaller `omega_perp` mismatch.
- Therefore the primary repair surface is active relaxed transport.
- TF32 remains enabled.

## Required Artifacts

- Patched scripts:
  - `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
  - `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
- Streaming baseline JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3f-adaptive-higher-particle-regression-fd-n64-gpu-tf32-2026-06-19.json`
- Dense diagnostic JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3h-dense-transport-ad-contract-n64-gpu-tf32-2026-06-19.json`
- Result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3h-dense-streaming-transport-ad-contract-result-2026-06-19.md`

## Required Checks

Local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3h-*
```

Trusted GPU dense transport diagnostic:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --time-steps 3 \
  --num-particles 64 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P8p Phase 3h dense transport AD-contract GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode dense \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 64 \
  --col-chunk-size 64 \
  --particle-chunk-size 64 \
  --dtype float32 \
  --tf32-mode enabled \
  --base-step-mode ad-signal \
  --target-objective-delta 0.15 \
  --adaptive-step-factors 1.0,0.5,0.25 \
  --min-adaptive-base-step 0.00025 \
  --max-adaptive-base-step 0.05 \
  --regression-offsets=-4,-3,-2,-1,0,1,2,3,4 \
  --basis-set semantic-orthogonal \
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3h-dense-transport-ad-contract-n64-gpu-tf32-2026-06-19.json
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does dense active transport show the same AD/FD mismatch as streaming active transport? |
| Baseline/comparator | Phase 3f active-all streaming transport, same `T=3`, `N=64`, seeds, TF32, semantic-orthogonal adaptive regression FD. |
| Primary diagnostic | AD/FD agreement and slope plateaus for the three semantic-orthogonal directions in dense transport. |
| Veto diagnostics | Nonfinite objective/gradient/slope; missing GPU placement; TF32 disabled; missing output artifact; no slope plateau. |
| Explanatory diagnostics | Selected adaptive steps, objective line values, per-seed gradient noise, seed-gradient covariance/correlation, dense-vs-streaming slope pattern. |
| Not concluded | HMC readiness, full-horizon stability, exact likelihood correctness, posterior validity, production/default readiness, leaderboard ranking. |
| Artifact preserving result | Phase 3h dense JSON plus result markdown. |

## Skeptical Plan Audit

- Wrong baseline: checked.  The comparator is Phase 3f active-all streaming
  transport, not no-resampling or another lane.
- Proxy metric risk: checked.  A dense pass/fail only localizes the transport
  AD contract; it does not validate HMC.
- Hidden assumption: checked.  Dense and streaming should be forward-equivalent
  for the same transport equations, but this phase treats mismatches as
  diagnostic, not impossible.
- Unfair comparison: checked.  Target, seeds, particle count, TF32 mode, and FD
  protocol are held fixed.
- Artifact adequacy: checked.  The JSON records slopes, AD derivatives, value
  lines, device metadata, selected steps, and transport plan mode.

Audit result: `PASS_TO_RUN`.

## Forbidden Claims And Actions

- Do not claim dense transport is the production fix from this phase alone.
- Do not claim HMC/NUTS readiness.
- Do not claim full-horizon SIR d18 gradient stability.
- Do not disable TF32.
- Do not touch Zhao-Cui or monograph artifacts.

## Handoff Conditions

- If dense transport passes while streaming fails, repair streaming transport
  gradient semantics against dense or switch active diagnostic validation to a
  documented dense/full-gradient contract.
- If dense transport fails in the same pattern, repair the shared annealed
  transport AD contract, especially stopped centering/scale and stopped
  Sinkhorn-key choices.
- If dense transport fails differently, write a localization result and plan a
  smaller transport-core unit diagnostic before changing production code.

## Stop Conditions

Stop and write a blocker if the dense diagnostic cannot run on trusted GPU, if
the artifact is missing or malformed, if TF32 is not enabled, or if slope lines
do not plateau enough to answer the localization question.
