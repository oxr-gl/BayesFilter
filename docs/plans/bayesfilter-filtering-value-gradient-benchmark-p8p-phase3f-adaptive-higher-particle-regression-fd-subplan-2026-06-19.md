# P8p Phase 3f Subplan: Adaptive Higher-Particle Regression FD

Date: 2026-06-19

Status: `DRAFT_EXECUTABLE`

## Phase Objective

Test whether the Phase 3e failures were mainly caused by low particle count
and poorly scaled finite-difference windows, while preserving TF32 as the
operational GPU path.

Phase 3f keeps the semantic metric-orthogonal parameter directions and changes
only two diagnostic controls:

1. raise the short-horizon gradient-validation particle count from `N=16` to
   `N=64`;
2. choose nested regression windows per direction from the AD directional
   derivative scale.

## Entry Conditions

- Phase 3c isolated the direct observation-covariance gradient path and found
  it correct.
- Phase 3d showed raw and simple physics coordinates are too collinear for a
  reliable scalar FD check.
- Phase 3e showed semantic metric-orthogonal directions are conceptually
  cleaner but did not converge at `N=16`.
- TF32 remains enabled; disabling TF32 is not the operational fix for this
  lane.

## Required Artifacts

- Script:
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
- JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3f-adaptive-higher-particle-regression-fd-n64-gpu-tf32-2026-06-19.json`
- Result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3f-adaptive-higher-particle-regression-fd-result-2026-06-19.md`

## Required Checks

Local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3e-* docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3f-*
```

Trusted GPU diagnostic:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --time-steps 3 \
  --num-particles 64 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P8p Phase 3f adaptive higher-particle regression FD GPU TF32" \
  --transport-policy active-all \
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
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3f-adaptive-higher-particle-regression-fd-n64-gpu-tf32-2026-06-19.json
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does increasing `N` and scaling regression windows by AD directional signal make semantic-orthogonal FD slopes stable and AD-consistent under TF32? |
| Baseline/comparator | Phase 3e: same target, same seeds, same TF32 route, same semantic-orthogonal construction, but `N=16` and fixed windows. |
| Primary pass criterion | For all three semantic-orthogonal directions, nested regression slopes have a plateau and agree with the AD directional derivative within the regression uncertainty scale and objective roughness visible in residuals. |
| Veto diagnostics | Nonfinite objective/gradient/slope; missing trusted GPU placement; TF32 disabled; no slope plateau; severe nonlinearity or residuals large enough that a slope is not interpretable; output artifact missing. |
| Explanatory diagnostics | Per-seed gradient noise, seed-gradient covariance/correlation, selected adaptive base steps, objective values along each line. |
| Not concluded even if pass | HMC readiness, full-horizon gradient stability, exact likelihood correctness, posterior validity, production/default readiness, fixed-parameter SIR d18 leaderboard ranking. |
| Artifact preserving result | Phase 3f JSON plus Phase 3f result markdown. |

## Skeptical Plan Audit

- Wrong baseline: checked.  The comparator is Phase 3e, not Zhao-Cui or a
  leaderboard run.
- Proxy metric risk: checked.  Slope plateau is a diagnostic gate only; it does
  not establish HMC readiness.
- Missing stop conditions: checked.  Nonfinite values, missing GPU placement,
  TF32 disabled, missing plateau, or uninterpretable regression residuals stop
  promotion.
- Unfair comparison: checked.  Seeds, target, transport policy, and TF32 route
  are held fixed; only `N` and step policy change.
- Hidden assumptions: checked.  The adaptive step rule assumes AD is usable for
  choosing a diagnostic window; this is acceptable because FD still tests the
  resulting slope, and selected steps are recorded.
- Artifact adequacy: checked.  The JSON stores objective values, slopes,
  selected steps, gradients, device metadata, and nonclaims.

Audit result: `PASS_TO_RUN`.

## Forbidden Claims And Actions

- Do not claim HMC/NUTS readiness from this phase.
- Do not claim full-horizon SIR d18 gradient stability from this phase.
- Do not disable TF32 as the operational fix.
- Do not touch Zhao-Cui or monograph artifacts in this phase.
- Do not change default production policy based only on this diagnostic.

## Handoff Conditions

If all directions pass the plateau and AD-agreement gate, Phase 3 can use this
as the repaired gradient-validation protocol and the next phase may design a
bounded HMC smoke.  If one or more directions remain mixed, write a blocker or
repair result and choose the next smallest discriminating action: `N=128`,
direction-specific roughness localization, or Hessian/observed-information
based reparameterization.

## Stop Conditions

Stop and write a blocker result if the trusted GPU command cannot run, if the
artifact is missing or malformed, if TensorFlow reports CPU placement while GPU
is required, if the run exceeds practical overnight bounds, or if the results
are too noisy to interpret under the stated evidence contract.
