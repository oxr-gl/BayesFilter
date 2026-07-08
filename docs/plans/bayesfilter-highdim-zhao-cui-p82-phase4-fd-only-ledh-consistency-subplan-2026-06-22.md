# P82 Phase 4 Subplan: FD-Only LEDH Consistency Check

status: SUPERSEDED_NOT_EXECUTABLE
date: 2026-06-22
phase: P4-FD-ONLY

## Phase Objective

Under the human-approved FD-only amendment, this subplan originally attempted
to run a bounded LEDH-PFPF-OT SIR d=18 same-scalar consistency check:

1. trusted GPU preflight;
2. tiny GPU mechanics smoke;
3. N=10000 five-seed LEDH actual-gradient AD-only run;
4. N=1000 five-seed 13-point regression-FD run in raw theta directions;
5. compare raw-direction gradient components to FD slopes in standard-error
   units and write a result.

## Supersession Note

This subplan is no longer executable.  Its N=10000 actual-gradient route used
`transport_ad_mode=full`, but prior P8p Phase 3j evidence had already shown
that raw/full autodiff through the whole Sinkhorn transport solve is infeasible
for governed N=10000 validation on this hardware/harness.

The active correction is:

`docs/plans/bayesfilter-highdim-zhao-cui-p82-full-ad-route-correction-2026-06-22.md`

The next active plan is:

`docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-master-program-2026-06-22.md`

P82 may resume only after a reviewed memory-disciplined actual-gradient route
exists.  The regression-FD comparator protocol below remains the downstream
comparator contract, but the full-AD N=10000 command in this file must not be
rerun as a governed validation route.

## Entry Conditions

- P2 harness repair passed local checks for 13 offsets and value-outlier
  trimming.
- P3 Zhao-Cui comparator blocker remains valid for the old scope.
- Human owner removed Zhao-Cui from the comparator for now.
- FD-only scope amendment exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-fd-only-scope-amendment-2026-06-22.md`.
- GPU commands require trusted/escalated execution under repository policy.

## Required Artifacts

- Actual-gradient JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n10000-adonly-gpu-tf32-2026-06-22.json`
- Actual-gradient progress JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n10000-adonly-progress-2026-06-22.json`
- Regression-FD JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n1000-raw-regression-fd-gpu-tf32-2026-06-22.json`
- Regression-FD progress JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n1000-raw-regression-fd-progress-2026-06-22.json`
- Result markdown:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase4-fd-only-ledh-consistency-result-2026-06-22.md`
- Updated P82 execution ledger and stop handoff.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the differentiable LEDH-PFPF-OT SIR d=18 gradient agree with regression-FD slopes of the same LEDH scalar in raw theta directions? |
| Baseline/comparator | N=1000 13-point regression FD of the same LEDH scalar.  FD is noisy diagnostic evidence, not an oracle. |
| Primary criterion | For each raw theta direction, N=10000 actual-gradient component and N=1000 FD slope are finite, uncertainty is recorded, and discrepancy is no more than 2 combined SE unless diagnostics downgrade the row. |
| Veto diagnostics | Missing GPU placement, TF32 disabled, wrong transport AD mode, nonfinite objective/gradient/slope/SE, missing five seeds, missing 13 raw/11 fit FD records, wrong trim mode, FD residuals too nonlinear, missing artifact, OOM/unbounded runtime, or unsupported Zhao-Cui/HMC/default/oracle claims. |
| Explanatory diagnostics | Gradient MCSE, FD slope SE, FD R2/residuals, dropped value-outlier points, runtime, device placement, memory/chunk metadata, progress files. |
| Not concluded | Posterior correctness, exact likelihood correctness, HMC readiness, default readiness, scientific superiority, Zhao-Cui comparator readiness, or manual-adjoint correctness. |
| Artifact preserving result | P4 JSON outputs, progress outputs, and result markdown. |

## Skeptical Plan Audit

- Wrong baseline: controlled by removing Zhao-Cui from the pass/fail path.
- Proxy metric risk: controlled; FD is a noisy diagnostic comparator and never
  an oracle.
- Missing stop conditions: controlled by predeclared artifact, runtime, GPU,
  finite-value, and FD-linearity vetoes.
- Unfair comparison: particle counts intentionally differ by owner instruction
  (`N=10000` actual, `N=1000` FD); the result must not present this as an exact
  same-budget comparison.
- Hidden assumptions: raw directions avoid basis mismatch; the original
  `transport_ad_mode=full` choice is now recognized as an invalid governed
  N=10000 route because later P8p evidence established runtime/memory
  infeasibility.
- Environment mismatch: GPU preflight must be trusted/escalated; CPU-only
  checks cannot substitute for GPU evidence.
- Artifact adequacy: JSON outputs include gradient, per-seed contributions,
  regression slopes, slope SE, raw/fit objective values, trim metadata, and
  device metadata.

Audit result: `SUPERSEDED_BY_FULL_AD_ROUTE_CORRECTION`.

## Local Checks Before GPU Work

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-*
```

## Trusted GPU Commands

### 0. GPU Preflight

```bash
nvidia-smi
```

### 1. Tiny Mechanics Smoke

```bash
env MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 1 --num-particles 8 \
  --batch-seeds 81120 \
  --ad-evaluation-mode reverse-gradient \
  --fd-mode enabled \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 FD-only tiny LEDH mechanics smoke" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-ad-mode full \
  --sinkhorn-iterations 2 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 8 --col-chunk-size 8 --particle-chunk-size 8 \
  --dtype float32 --tf32-mode enabled \
  --base-step-mode fixed \
  --base-step 0.001 \
  --regression-offsets=-3,-2,-1,0,1,2,3 \
  --trim-extreme-offsets 1 \
  --trim-extreme-mode value \
  --fd-evaluation-mode batched-theta \
  --basis-set raw \
  --direction-filter log_obs_noise_scale \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-tiny-smoke-gpu-tf32-2026-06-22.json
```

### 2. N=10000 Actual Gradient

Do not run this command as governed validation.  It is retained only as a
historical record of the superseded P4 attempt.

```bash
env MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 10000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode forward-jvp \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 FD-only LEDH N10000 AD-only GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-ad-mode full \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --basis-set raw \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n10000-adonly-progress-2026-06-22.json \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n10000-adonly-gpu-tf32-2026-06-22.json
```

### 3. N=1000 Regression FD

```bash
env MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 1000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode forward-jvp \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 FD-only LEDH N1000 raw 13-point regression FD GPU TF32" \
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
  --regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6 \
  --trim-extreme-offsets 1 \
  --trim-extreme-mode value \
  --fd-evaluation-mode batched-theta \
  --theta-offset-batch-size 13 \
  --basis-set raw \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n1000-raw-regression-fd-progress-2026-06-22.json \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n1000-raw-regression-fd-gpu-tf32-2026-06-22.json
```

## Post-Run Checks

- `python -m json.tool` on every produced JSON artifact.
- Verify actual-gradient JSON records:
  - `num_particles = 10000`;
  - five seeds;
  - `transport_ad_mode = full`;
  - `tf32_execution_enabled = true`;
  - GPU output devices;
  - finite objective and gradient;
  - seed MCSE for each parameter.
- Verify FD JSON records:
  - `num_particles = 1000`;
  - five seeds;
  - 13 offsets;
  - `trim_extreme_mode = value`;
  - each direction has 13 raw objective values and 11 retained fit points;
  - finite slope and slope SE.
- Write the result decision table with one row per raw direction.

## Forbidden Claims / Actions

- Do not use Zhao-Cui as comparator evidence.
- Do not call regression FD an oracle.
- Do not claim HMC/NUTS readiness, exact likelihood correctness, posterior
  correctness, default-gradient readiness, scientific superiority, or
  production readiness.
- Do not change the default transport AD mode based on this phase.
- Do not run unbounded N=10000 FD lines.
- Do not revert unrelated dirty worktree changes.

## Stop Conditions

Stop and write a blocker result if:

- GPU preflight fails in trusted context;
- tiny smoke fails;
- N=10000 AD-only run produces no artifact in bounded time;
- N=1000 FD run produces no artifact or progress stalls;
- memory reaches device ceiling with no progress;
- any required metadata is missing;
- FD residuals make slope interpretation invalid;
- continuing would require changing pass/fail criteria after seeing results.
