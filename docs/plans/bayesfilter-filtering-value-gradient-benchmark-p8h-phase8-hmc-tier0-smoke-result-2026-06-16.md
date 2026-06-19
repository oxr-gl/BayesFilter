# P8h Phase 8 Result: Tier-0 HMC Execution Smoke

Date: 2026-06-16

Status: `PASS_TIER0_HMC_EXECUTION_REVIEWED`

## Phase Objective

Run the smallest trusted-GPU TFP Hamiltonian Monte Carlo execution smoke on the
selected P8h OT-resampled scalar-SV objective.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the selected P8h OT-resampled scalar-SV value/gradient graph execute inside a tiny fixed-kernel TFP HMC chain on trusted GPU? |
| Baseline/comparator | Reviewed Phase 5 selected route/count, reviewed Phase 6 OT-gradient scalar, and reviewed Phase 7 GPU feasibility profile. P8g no-resampling material is historical context only. |
| Primary criterion | Sample-chain execution with trusted GPU tensors, finite initial value/gradient, finite samples and trace log quantities, exact route/count/configuration, and no runtime/OOM blocker; otherwise explicit blocker. |
| Veto diagnostics | Missing reviewed exact route/count provenance; no-resampling route; wrong particle count; untrusted GPU or CPU fallback; HMC execution error without blocker classification; nonfinite initial value/gradient; disconnected gradient; nonfinite samples; nonfinite target log probability or log-accept ratio. |
| Explanatory diagnostics | Acceptance rate, step size, sample displacement, runtime, target log probability range, trace shape. |
| Not concluded | Production HMC readiness, posterior convergence, valid tuning, NUTS readiness, stochastic PF marginal-gradient correctness, full-horizon HMC feasibility, filter ranking, or default sampler policy. |

## Skeptical Audit

- Wrong-baseline check: P8g no-resampling gradients and timings remain
  historical context only and are not used as Phase 8 entry evidence.
- Proxy-metric check: acceptance rate and sample displacement are explanatory
  only; the primary gate is finite trusted-GPU execution of the reviewed P8h
  OT route inside a tiny fixed-kernel HMC chain.
- Stop-condition check: wrong route/count/coordinate, CPU fallback, HMC
  execution error without blocker classification, nonfinite values/gradients,
  or nonfinite trace quantities would block.
- Artifact-fit check: the JSON/CSV artifacts preserve route, count, HMC
  settings, seed, device proof, finite diagnostics, and nonclaims needed for
  Phase 9 closeout.

## Implementation And Checks

Implemented Phase 8-specific HMC Tier-0 support in:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`;
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`.

Local checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h or particle"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*
rg -n "PASS|REVIEWED|N=5|ot_sinkhorn_barycentric_covariance_carry|small-HMC-feasibility" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-result-2026-06-15.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-result-2026-06-16.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-result-2026-06-16.md
```

Results:

- `py_compile`: passed.
- Focused pytest: `13 passed, 13 deselected, 2 warnings`.
- `git diff --check`: passed.
- Reviewed route/status grep: passed.

## Trusted GPU Run

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-hmc-tier0-smoke --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizon 4 --particles 5 --seeds 81120 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --hmc-num-results 2 --hmc-num-burnin-steps 1 --hmc-step-size 0.005 --hmc-num-leapfrog-steps 1 --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-gpu-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-gpu-2026-06-16.csv
```

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-gpu-2026-06-16.json`;
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-gpu-2026-06-16.csv`.

Programmatic JSON/CSV validation passed.

## Diagnostic Results

Run scope:

- row: `zhao_cui_sv_actual_nongaussian_T1000` (the CLI alias
  `--row actual_sv` resolves to this row ID);
- algorithm: `ledh_pfpf_alg1_ukf_current`;
- route: `ot_sinkhorn_barycentric_covariance_carry`;
- route variant: `p8h_sv_scalar_graph_ot_resampled_alg1`;
- horizon: `4`;
- particles: `5`;
- PF seed: `81120`;
- HMC seed: `[81120, 82120]`;
- coordinate: `theta=(Phi^{-1}(gamma), log(beta))`, sigma fixed at `1.0`;
- HMC kernel: `tfp.mcmc.HamiltonianMonteCarlo`;
- HMC settings: `num_results=2`, `num_burnin_steps=1`, `step_size=0.005`,
  `num_leapfrog_steps=1`;
- device: trusted GPU.

Summary:

| Metric | Value |
|---|---:|
| Status | `executed_p8h_hmc_tier0_smoke` |
| Wall time | `43.934145` seconds |
| Initial log likelihood | `-2.735546047598974` |
| Initial gradient | `[-0.7196653064013585, -0.6863372245627708]` |
| Initial gradient norm | `0.9944731967520736` |
| Sample shape | `[2, 2]` |
| Acceptance rate | `1.0` |
| Sample displacement L2 | `0.002514811172017426` |
| Target log-prob range | `[-2.737643874537946, -2.7351398246781278]` |
| Log-accept-ratio range | `[-2.724200109938124e-08, 2.8212486652412494e-08]` |

Veto diagnostics:

| Diagnostic | Status |
|---|---|
| Trusted GPU tensor evidence | pass: `/device:GPU:0` |
| Exact route/count/coordinate | pass |
| Initial value finite | pass |
| Initial gradient finite | pass |
| Initial gradient connected | pass |
| Sample chain returned | pass |
| Samples finite | pass |
| Target log probabilities finite | pass |
| Log accept ratios finite | pass |
| Blocker | none |

The acceptance rate of `1.0` is not interpreted as tuning quality. It is only
an explanatory trace value for this two-sample fixed-kernel execution smoke.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Pass Phase 8 Tier-0 HMC execution smoke | Passed for the selected short-prefix route/count on trusted GPU. | No Phase 8 veto fired; read-only review returned `VERDICT: AGREE` after Phase 9 subplan boundary repair. | The chain is intentionally tiny and fixed-kernel; it does not test tuning, convergence, NUTS, long horizons, or full stochastic marginal-gradient validity. | Execute Phase 9 closeout to preserve the pass, nonclaims, and remaining limitations. | No production HMC readiness, posterior convergence, valid tuning, NUTS readiness, full-horizon HMC feasibility, filter ranking, or default sampler policy. |

## Post-Run Red-Team Note

Strongest alternative explanation: the tiny HMC smoke passes because it uses a
very short horizon, one PF seed, one leapfrog step, and two samples. This
shows the graph can execute inside HMC on GPU, not that the sampler is useful
for inference.

What would overturn this result: a reviewed rerun showing CPU fallback,
nonfinite values/gradients/samples/trace quantities, wrong route/count, or an
unclassified HMC execution error.

Weakest part of the evidence: the HMC trace is too small to say anything about
posterior geometry, tuning, or convergence.

## Handoff

Read-only review accepted this result with `VERDICT: AGREE` after the Phase 9
subplan was repaired to preserve all Phase 8 nonclaims. Proceed to Phase 9
closeout/artifact preservation. Phase 9 must record this as a Tier-0
execution-smoke pass only and preserve all Phase 8 nonclaims.
