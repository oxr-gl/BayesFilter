# P8p Phase 3g Subplan: No-Resampling AD/FD Localization

Date: 2026-06-19

Status: `DRAFT_EXECUTABLE`

## Phase Objective

Localize the Phase 3f AD/FD discrepancy by rerunning the repaired regression-FD
diagnostic with relaxed transport skipped.

This phase asks whether the mismatch is introduced by the active streaming
annealed-transport path or whether it already exists upstream in LEDH flow,
correction terms, or target log-density callbacks.

## Entry Conditions

- Phase 3f ran on trusted GPU with TF32 enabled, `T=3`, `N=64`, five fixed
  seeds, semantic metric-orthogonal directions, and adaptive regression
  windows.
- Phase 3f produced clean nested FD slope plateaus but systematic AD/FD
  mismatch.
- Code trace identifies transport as a plausible but unproven source because
  the streaming annealed transport path uses stopped centering/scale and
  stopped Sinkhorn potential keys.

## Required Artifacts

- Script:
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
- JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3g-no-resampling-localization-n64-gpu-tf32-2026-06-19.json`
- Result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3g-no-resampling-localization-result-2026-06-19.md`

## Required Checks

Local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3f-* docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3g-*
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
  --phase-label "P8p Phase 3g no-resampling localization GPU TF32" \
  --transport-policy no-resampling \
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
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3g-no-resampling-localization-n64-gpu-tf32-2026-06-19.json
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does skipping relaxed transport remove the Phase 3f AD/FD discrepancy under the repaired regression-FD protocol? |
| Baseline/comparator | Phase 3f active-all transport run, same target, seeds, TF32 mode, particle count, and adaptive regression-FD protocol. |
| Primary diagnostic | All semantic-orthogonal directions show nested FD plateaus and AD agreement, or a clear remaining mismatch. |
| Veto diagnostics | Nonfinite objective/gradient/slope; missing trusted GPU placement; TF32 disabled; no slope plateau; missing output artifact. |
| Explanatory diagnostics | Selected adaptive base steps, per-seed gradient noise, seed-gradient covariance/correlation, objective line values. |
| Not concluded | HMC readiness, full-horizon gradient stability, exact likelihood correctness, posterior validity, production/default readiness, leaderboard ranking. |
| Artifact preserving result | Phase 3g JSON plus Phase 3g result markdown. |

## Skeptical Plan Audit

- Wrong baseline: checked.  The comparator is Phase 3f active-all, not a
  different model lane.
- Proxy metric risk: checked.  The run localizes an implementation gradient
  issue; it does not establish scientific validity.
- Hidden assumption: checked.  The semantic basis will be recomputed under the
  no-resampling objective, so the comparison is qualitative localization, not a
  same-direction equality proof.
- Missing stop condition: checked.  Missing GPU placement, TF32 disabled,
  nonfinite results, or non-plateaued slopes stop promotion.
- Artifact adequacy: checked.  The JSON records device metadata, selected
  steps, objective values, gradients, slopes, and nonclaims.

Audit result: `PASS_TO_RUN`.

## Forbidden Claims And Actions

- Do not claim HMC/NUTS readiness from this phase.
- Do not claim full-horizon SIR d18 gradient stability.
- Do not disable TF32.
- Do not touch Zhao-Cui or monograph artifacts.
- Do not change production defaults from this localization result.

## Handoff Conditions

If no-resampling passes, write a result that identifies relaxed transport as
the next repair surface.  If no-resampling fails, write a result that redirects
localization upstream to LEDH flow/correction/target callbacks.  Either way,
do not move to HMC until the repaired Phase 3 gradient gate passes.

## Stop Conditions

Stop and write a blocker if the trusted GPU command cannot run, if the output
artifact is missing or malformed, if TF32 is not enabled, or if the diagnostic
is too noisy to interpret.
