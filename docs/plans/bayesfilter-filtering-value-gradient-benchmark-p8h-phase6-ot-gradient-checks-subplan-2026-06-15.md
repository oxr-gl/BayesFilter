# P8h Phase 6 Subplan: OT Gradient Checks

Date: 2026-06-15

Status: `READY_FOR_REVIEW_AFTER_PHASE5`

## Phase Objective

Run AD gradient checks through LEDH + PF-PF correction + relaxed Sinkhorn OT
transport for the exact Phase 5 selected Stage 0 route/count. Fixed random
numbers are allowed for reproducibility, but no no-resampling detour is allowed
for the serious route.

## Entry Conditions

- Phase 5 selected Stage 0 prefix count `N=5` for
  `ot_sinkhorn_barycentric_covariance_carry`, pending review.
- Phase 6 may execute only after Phase 5 result review accepts the selected
  diagnostic count and this subplan review converges.

## Required Artifacts

- P8h-specific OT gradient runner surface in
  `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`; P8g
  no-resampling G3 is historical diagnostic context only.
- Focused gradient tests proving the P8h route uses the OT resampling route and
  fails closed on no-resampling detours.
- Gradient JSON/CSV artifacts under `docs/plans`:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-gpu-2026-06-16.json` and
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-gpu-2026-06-16.csv`.
- Per-run manifest fields in the JSON result or sibling manifest: git commit,
  command, route ID, resampling family/policy, transport settings, gradient
  scalar ID, fixed-randomness/common-randomness policy, CPU/GPU context, trusted
  GPU proof or CPU-only declaration, seeds, particle counts, environment, output
  paths, and wall time.
- Phase 6 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-result-2026-06-16.md`.

## Required Checks, Tests, Reviews

- `git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*`
- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py`
- `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py -k "p8h or gradient or sinkhorn or ot"`
- Trusted GPU gradient run:
  `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-ot-gradient-check --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --horizon 4 --particles 5 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-gpu-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-gpu-2026-06-16.csv`
- Finite differences as diagnostic only.
- Claude read-only review of result and gradient claim boundaries.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are AD gradients finite, connected, and reproducible for the selected P8h OT-resampled scalar on trusted GPU? |
| Baseline/comparator | Phase 5 selected Stage 0 route/count and Phase 4 CPU/GPU route diagnostics. Historical P8g no-resampling gradient smoke is context only. |
| Primary criterion | AD gradients through the declared relaxed Sinkhorn OT computational graph are finite, non-`None`, repeatable under fixed randomness, use the exact P8h route/count, and carry seed uncertainty diagnostics. |
| Veto diagnostics | Disconnected gradients; nonfinite gradients; zero/missing gradient norm; no-resampling detour; missing route/manifest fields; missing trusted GPU evidence; FD promoted to proof; stochastic categorical-resampling gradient claim. |
| Explanatory diagnostics | FD deltas, gradient norms, seed variability, CPU/GPU deltas. |
| Not concluded | Stochastic PF marginal-gradient correctness, HMC readiness, GPU scaling, full-horizon value adequacy, or filter ranking. |

## Forbidden Claims And Actions

- Do not claim gradients of categorical resampling.
- Do not claim HMC readiness from gradient finiteness alone.
- Do not use P8g no-resampling gradient artifacts as P8h gradient evidence.
- Do not treat finite-difference agreement as proof; FD is diagnostic only.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 7 only after a gradient pass result review converges. A
diagnostic-only gradient result may proceed only to closeout or a refreshed
repair phase, not to Phase 7 scaling or Phase 8 HMC.

## Stop Conditions

- Gradient path is disconnected or nonfinite under the declared route.
- The P8h OT-gradient runner surface or focused tests are absent or fail.
- The run uses a no-resampling detour, wrong route, wrong particle count, or
  lacks required route/manifest provenance fields.
- Trusted GPU proof is missing for the GPU artifact.
- Gradient norm is zero, missing, or not finite under the declared route.
