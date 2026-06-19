# P8p Phase 3j Subplan: N=10000 Full-Transport FD Validation

Date: 2026-06-19

Status: `DRAFT_EXECUTABLE`

## Phase Objective

Test whether the Phase 3i candidate transport AD contract,
`transport_ad_mode=full`, still agrees with regression finite differences at a
meaningful particle count for the parameterized SIR d18 LEDH-PFPF-OT target.

Phase 3j is a gradient-contract validation phase.  It is not an HMC readiness
phase.

## Entry Conditions

- Phase 3g localized the large mismatch to active transport by showing that
  `no-resampling` largely removed the issue.
- Phase 3h showed dense and streaming transport fail similarly under the
  stabilized AD contract, so chunking was not the primary cause.
- Phase 3i showed that `transport_ad_mode=full` is the first tested dense
  active transport contract to pass local AD/FD agreement at `N=64`.
- The user identified `N=64` as too small for a meaningful gradient-quality
  claim because seed Monte Carlo error remains large.

## Required Artifacts

- Subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-n10000-full-transport-fd-subplan-2026-06-19.md`
- JSON diagnostic:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-n10000-full-streaming-fd-gpu-tf32-2026-06-19.json`
- Result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-n10000-full-transport-fd-result-2026-06-19.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the `full` active transport AD contract still match regression FD for SIR d18 when particle count is raised to `N=10000`? |
| Baseline/comparator | Phase 3i `full` dense `N=64` result, with Phase 3h stabilized result as the known failed comparator. |
| Primary criterion | In all three semantic-orthogonal directions, AD directional derivative agrees with 9-point OLS FD slope within a tolerance informed by regression SE and seed-gradient MCSE. |
| Veto diagnostics | Missing GPU placement, TF32 disabled, nonfinite objective/gradient/slope, missing JSON artifact, failed FD regression, or obvious line nonlinearity/poor fit. |
| Explanatory diagnostics | Seed-gradient covariance/correlation, MCSE, FD residuals, slope SE, selected adaptive base step, runtime, and TensorFlow device records. |
| Not concluded | HMC/NUTS readiness, posterior validity, full-horizon stability, exact likelihood correctness, production/default readiness, or leaderboard ranking. |
| Artifact preserving result | Phase 3j JSON plus Phase 3j result markdown. |

## Planned Command

Use one adaptive 9-point FD window rather than the full Phase 3i three-window
ladder.  If a direction is borderline, the next subphase can run a focused
half-step confirmation instead of repeating the full diagnostic immediately.

```bash
env MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 10000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode forward-jvp \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P8p Phase 3j N10000 full transport streaming FD GPU TF32" \
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
  --regression-offsets=-4,-3,-2,-1,0,1,2,3,4 \
  --basis-set semantic-orthogonal \
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-n10000-full-streaming-fd-gpu-tf32-2026-06-19.json
```

## Skeptical Plan Audit

- Wrong baseline risk: checked.  The direct candidate baseline is Phase 3i
  `full`; the known failed comparator is Phase 3h `stabilized`.
- Proxy metric risk: checked.  This test validates a local gradient contract
  only; it does not rank filtering quality or HMC performance.
- Missing stop condition risk: checked.  The run stops on nonfinite values,
  failed GPU/TF32 placement, failed artifact creation, or unusable FD line fit.
- Unfair comparison risk: checked.  The target, theta, seeds, transport policy,
  Sinkhorn settings, TF32 mode, and semantic-orthogonal basis are inherited from
  Phase 3i; only particle count and operational streaming plan mode change.
- Hidden runtime risk: checked.  `N=10000` with 9-point FD and five seeds may be
  materially slower than a single filter evaluation.  The bounded one-window
  protocol is used to avoid an unnecessary three-window ladder.
- GPU memory risk: checked after OOMs with chunk sizes `4096` and `1024`.  The
  executable command uses chunk size `512`, which preserves the same target and
  AD/FD question while further reducing streaming Sinkhorn block memory for the
  full-AD tape.
- Full-AD tape risk: checked after chunk `512` still saturated GPU memory with
  the five-seed batch.  The executable command uses `--seed-microbatch-size 1`;
  this preserves the exact five-seed batch-mean objective by evaluating
  independent fixed-seed groups sequentially, while avoiding a single massive
  full-AD tape.
- Diagnostic harness risk: checked after the one-seed microbatch still exposed
  the old persistent-tape per-seed-Jacobian path.  The runner now uses a lean
  scalar-gradient path for one-seed microbatches; this preserves the per-seed
  gradient contribution while avoiding unnecessary Jacobian tape retention.
- Reverse-mode full-AD risk: checked after the lean one-seed reverse-gradient
  path still OOMed at `N=10000`.  The executable command uses forward-mode JVP
  directional AD over the three raw parameters.  This is the appropriate memory
  geometry for a low-parameter directional AD/FD diagnostic and avoids retaining
  the full reverse-mode Sinkhorn tape.
- Artifact adequacy risk: checked.  The JSON records GPU placement, precision,
  MCSE, FD residuals, and AD/FD gaps needed to decide the phase.

Audit result: `PASS_TO_RUN_BOUNDED_N10000_DIAGNOSTIC`.

## Forbidden Claims And Actions

- Do not claim HMC/NUTS readiness.
- Do not claim posterior validity or full-horizon stability.
- Do not promote `transport_ad_mode=full` to the default in this phase.
- Do not disable TF32.
- Do not touch Zhao-Cui or monograph artifacts.

## Handoff Conditions

If all directions pass with usable FD fits, Phase 3j hands off to a longer
horizon or repeated-gradient HMC-smoke subplan using `full` as the candidate
transport AD contract.  If one direction is borderline, the next action is a
focused half-step FD confirmation for that direction or a slightly larger seed
batch.  If the run fails or gives unusable FD lines, write a blocker result and
return to smaller transport-core diagnostics.

## Stop Conditions

Stop if the GPU diagnostic cannot run in trusted context, if TensorFlow does
not report `/GPU:0`, if TF32 is disabled, if any value is nonfinite, if the JSON
artifact is missing, or if the FD regression line is too nonlinear to answer
the AD/FD question.
