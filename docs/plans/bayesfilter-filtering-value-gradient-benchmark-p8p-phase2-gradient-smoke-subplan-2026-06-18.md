# P8p Phase 2 Subplan: Fixed-Randomness Gradient Smoke Implementation

Date: 2026-06-18

Status: `ACTIVE_AFTER_PHASE1_REVIEW`

## Phase Objective

Implement and smoke-test a P8p-specific parameterized SIR d18 gradient harness
for the three-parameter diagnostic theta target:

```text
theta = [log_kappa_scale, log_nu_scale, log_obs_noise_scale]
```

The phase answers whether a tiny fixed-randomness SIR d18 LEDH-PFPF-OT graph
has finite values and explicit per-theta connected gradients.  It does not
answer full-horizon adequacy or HMC readiness.

## Entry Conditions Inherited From Previous Phase

Phase 2 may start only if:

- Phase 0 passed and the runbook is launched;
- Phase 1 result passed review;
- Phase 1 named exact theta-dependent implementation points;
- P8p remains separate from P8j/P8o fixed-parameter value-only artifacts;
- GPU operations will use trusted/escalated execution.

## Required Artifacts

- New diagnostic harness:
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- Phase 2 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-result-2026-06-18.md`
- Tiny smoke JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-2026-06-18.json`
- Optional CPU/FD diagnostic JSON if run:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-fd-cpu-2026-06-18.json`
- Phase 3 subplan draft:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-subplan-2026-06-18.md`

## Required Checks, Tests, And Reviews

Before execution:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-*
```

Tiny GPU smoke, trusted/escalated:

```bash
python docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --time-steps 3 \
  --num-particles 8 \
  --batch-seeds 81120 \
  --theta 0,0,0 \
  --phase-label "P8p Phase 2" \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 8 \
  --col-chunk-size 8 \
  --particle-chunk-size 8 \
  --dtype float32 \
  --tf32-mode enabled \
  --fd-step 0.001 \
  --repeat-evaluations 2 \
  --check-theta-zero-p8j-parity \
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-2026-06-18.json
```

The harness must emit these artifact fields at minimum:

- `theta`;
- `theta_transform`;
- `batch_seeds`;
- `initial_particle_seed_policy`;
- `process_noise_seed_policy`;
- `random_streams_fixed_across_theta`;
- `repeat_evaluations`;
- `repeat_value_max_abs_delta`;
- `repeat_gradient_max_abs_delta`;
- `transport_policy`;
- `resampling_mask_fixed`;
- `relaxed_sinkhorn_ot_used`;
- `categorical_resampling_used`;
- `theta_zero_p8j_parity_checked`;
- `theta_zero_p8j_value_delta_max_abs`;
- `connectivity_by_component`;
- `gradient`;
- `finite_difference_by_component`;
- `output_devices`;
- `primary_pass`.

Review:

- Claude read-only review is required for the implementation diff and Phase 2
  result if code changes are nontrivial or any diagnostic is borderline.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the tiny P8p parameterized SIR d18 fixed-randomness graph produce finite values and explicit connected gradients for all three theta components? |
| Baseline/comparator | Phase 1 theta-zero contract and current P8j fixed-parameter route at the same tiny shape.  The Phase 2 artifact must include theta-zero P8j parity status before gradient evidence can pass. |
| Primary pass criterion | Theta-zero P8j tiny-shape parity checked and within declared tolerance; value finite; AD gradient finite; every theta component explicitly connected; no component exactly zero without reviewed structural explanation; repeated same-theta evaluation is bitwise or tolerance-repeatable; same-randomness finite-difference sensitivity is finite for each component; artifact proves fixed random streams, fixed resampling mask, relaxed Sinkhorn OT, and no categorical resampling; GPU placement is trusted if GPU is claimed. |
| Veto diagnostics | Missing theta-zero P8j parity check; theta-zero parity failure; nonfinite value/gradient; disconnected theta component; masked zero-gradient success; stochastic categorical resampling; missing fixed-mask/relaxed-OT artifact fields; random streams vary across repeated theta; CPU fallback for GPU claim; changing criteria after result; broad code mutation outside P8p harness. |
| Explanatory diagnostics | FD residuals, gradient norms, per-component values, runtime, GPU memory, output devices. |
| Not concluded | Full-horizon gradient correctness, stochastic PF marginal-gradient correctness, exact likelihood correctness, HMC/NUTS readiness, posterior convergence, production/default readiness, or filter ranking. |

## Forbidden Claims And Actions

- Do not claim HMC readiness from Phase 2.
- Do not run the full `N=10000` or `N=50000` SIR d18 ladder in Phase 2.
- Do not mutate unrelated Zhao-Cui fixed-branch or monograph files.
- Do not use NumPy as the BayesFilter-owned differentiable implementation
  backend.  NumPy is allowed only for reporting serialized arrays after TF
  computation.
- Do not rely on `streaming_batched_ledh_pfpf_ot_value_and_score_tf` alone as a
  connectivity diagnostic.
- Do not pass Phase 2 unless the artifact explicitly records theta-zero P8j
  parity, repeated same-theta repeatability, fixed random streams, fixed mask,
  relaxed Sinkhorn OT, and no categorical resampling.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- harness compiles;
- tiny gradient smoke passes the primary criterion;
- Phase 2 result records command, environment, device placement, theta, seeds,
  theta-zero P8j parity status, random-stream contract, repeatability, fixed
  mask, relaxed-OT/no-categorical route fields, value, gradient, connectivity
  flags, FD diagnostic, and nonclaims;
- Phase 3 subplan exists and focuses on central finite-difference validation
  with same-randomness fixed across theta shifts.

## Stop Conditions

Stop and write a blocker if:

- any theta component is disconnected or nonfinite;
- repeated evaluation changes random streams;
- GPU claim cannot be verified in trusted context;
- the implementation would require broad changes to P8j/P8o value-only
  artifacts;
- Claude/Codex review fails to converge after five rounds for the same blocker.
