# P8h Phase 8 Subplan: Tier-0 HMC Execution Smoke

Date: 2026-06-15

Status: `READY_FOR_REVIEW_AFTER_PHASE7`

## Phase Objective

Run the smallest trusted-GPU TFP Hamiltonian Monte Carlo execution smoke on the
selected P8h OT-resampled scalar-SV objective. This phase tests whether the
reviewed relaxed-Sinkhorn value/gradient graph can be consumed by a tiny fixed
kernel HMC chain without nonfinite values, disconnected gradients, CPU fallback,
or runtime/OOM blockers.

## Entry Conditions

- Phase 5 has a reviewed passing value/filtering decision for the exact
  route/count entering HMC:
  `ot_sinkhorn_barycentric_covariance_carry`, `N=5`.
- Phase 6 has a reviewed pass for the same OT-resampled gradient route/count,
  and Phase 7 has a reviewed trusted-GPU feasibility result for the same
  route/count. A diagnostic-only no-resampling gradient route cannot enter
  Phase 8.
- Before execution, verify Phase 5, Phase 6, and Phase 7 reviewed pass statuses
  and exact route/count/configuration with focused grep checks.

## Required Artifacts

- HMC Tier-0 implementation in
  `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`, reusing the
  existing P8h OT value/gradient helper and TFP
  `mcmc.HamiltonianMonteCarlo`.
- Focused regression tests in
  `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`.
- HMC Tier-0 smoke JSON/CSV artifacts:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-gpu-2026-06-16.json` and
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-gpu-2026-06-16.csv`.
- Per-run manifest fields in the JSON result or sibling manifest: git commit,
  command, route ID, resampling family/policy, transport settings, scalar ID,
  trusted GPU proof for any success-path artifact, seeds, chain settings,
  particle counts, environment, output paths, and wall time. CPU-only execution
  may appear only as an explicit blocker artifact, never as a successful
  Phase 8 manifest.
- Phase 8 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-result-2026-06-16.md`.

## Required Checks, Tests, Reviews

- `git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*`
- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- Focused unit tests for the P8h HMC Tier-0 payload schema; route, count,
  coordinate, and trusted-GPU device-gate rejection; and HMC execution-error
  blocker path.
- Implementation must be fail-closed for route/count/coordinate/device:
  only `actual_sv`, `ledh_pfpf_alg1_ukf_current`,
  `ot_sinkhorn_barycentric_covariance_carry`, `N=5`,
  `canonical_unconstrained`, fixed-kernel HMC, and trusted GPU are allowed in
  Phase 8 execution.
- Required pre-execution grep checks:
  `rg -n "PASS|REVIEWED|N=5|ot_sinkhorn_barycentric_covariance_carry|small-HMC-feasibility" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-result-2026-06-15.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-result-2026-06-16.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-result-2026-06-16.md`
- Trusted GPU HMC Tier-0 smoke command:
  `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-hmc-tier0-smoke --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizon 4 --particles 5 --seeds 81120 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --hmc-num-results 2 --hmc-num-burnin-steps 1 --hmc-step-size 0.005 --hmc-num-leapfrog-steps 1 --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-gpu-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-gpu-2026-06-16.csv`
- Post-run JSON/CSV validation for trusted GPU evidence, exact route/count,
  finite initial value/gradient, sample-chain return, finite samples,
  finite target log probabilities and log-accept ratios when available, and
  blocker classification if the kernel fails.
- Claude read-only review of the Phase 8 result and Phase 9 refreshed subplan.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the selected P8h OT-resampled scalar-SV value/gradient graph execute inside a tiny fixed-kernel TFP HMC chain on trusted GPU? |
| Baseline/comparator | Reviewed Phase 5 selected route/count, reviewed Phase 6 OT-gradient scalar, and reviewed Phase 7 GPU feasibility profile. No-resampling P8g HMC/gradient material is historical context only. |
| Primary criterion | The Tier-0 artifact either passes sample-chain execution with trusted GPU tensors, finite initial value/gradient, finite samples and trace log quantities, exact route/count/configuration, and no runtime/OOM blocker; or writes an explicit blocker result. |
| Veto diagnostics | Missing reviewed Phase 5/6/7 pass for the exact route/count; no-resampling route; wrong particle count; missing manifest fields; untrusted GPU or CPU fallback treated as GPU success; HMC execution error without blocker classification; nonfinite initial value/gradient; disconnected gradient; nonfinite samples; nonfinite target log probability or log-accept ratio when available; treating speed or acceptance alone as pass. |
| Explanatory diagnostics | Acceptance rate, step size, sample displacement, runtime, target log probability range, trace shape, native divergence field if TFP exposes one. |
| Not concluded | Production HMC readiness, posterior convergence, valid tuning, NUTS readiness, stochastic PF marginal-gradient correctness, full-horizon HMC feasibility, filter ranking, or default sampler policy. |

## Forbidden Claims And Actions

- Do not run NUTS, adaptive HMC, long chains, multi-chain convergence, or
  tuning ladders in Phase 8.
- Do not claim HMC readiness, posterior convergence, sampler ranking, or
  production readiness from a Tier-0 execution smoke.
- Do not use P8g no-resampling gradients as an HMC entry route.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 9 only after the Phase 8 result or blocker is written and
reviewed. If Tier-0 passes, Phase 9 may record that a tiny fixed-kernel HMC
execution smoke is feasible; it must still preserve all Phase 8 nonclaims. If
Tier-0 blocks, Phase 9 must preserve the blocker rather than hiding it.

## Stop Conditions

- Phase 5, Phase 6, or Phase 7 reviewed exact-route/count status cannot be
  verified.
- Trusted GPU evidence is missing or sample-chain tensors silently fall back to
  CPU.
- HMC execution fails and cannot be classified as a recorded blocker.
- Nonfinite values, gradients, samples, or trace log quantities appear.
