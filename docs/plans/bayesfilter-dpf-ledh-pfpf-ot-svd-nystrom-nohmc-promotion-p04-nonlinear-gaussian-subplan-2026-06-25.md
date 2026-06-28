# P04 Subplan: Nonlinear Gaussian Gate

Date: 2026-06-25

Status: `P04_HISTORICAL_UNCALIBRATED_THRESHOLD_PLAN`

Governance correction on 2026-06-25: this historical subplan used
`tau_component=0.05` for a nonlinear range-bearing gate without a prior
calibration/freeze/validation procedure. It is retained for provenance, but it
must not govern active P04 pass/fail interpretation. The active next step is
P04B threshold-governance repair and P04C nonlinear threshold scale extraction.

## Phase Objective

Build or verify a fair nonlinear Gaussian DPF/LEDH-PFPF-OT harness for the
existing range-bearing fixture, then evaluate fixed SVD-Nystrom against the
same-artifact compiled streaming TF32 route with predeclared validity and
quality screens.

## Entry Conditions Inherited From Previous Phase

- P03 actual-SIR stress emitted
  `P03_PASS_TO_P04_NONLINEAR_GAUSSIAN`.
- Candidate policy remains locked.
- No HMC readiness claim is in scope.
- P04 must not use sigma-point value benchmarks as substitute evidence for the
  DPF SVD-Nystrom route.

## Required Artifacts

- Harness implementation:
  `docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py`
- Focused local tests:
  `tests/test_svd_nystrom_range_bearing_gate.py`
- Local test log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-local-tests.log`
- Local harness review note:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-harness-local-review-2026-06-25.md`
- Per-seed JSON/Markdown/log artifacts must be exactly the seed-specific paths
  listed in the P04 per-row artifact manifest below. No wildcard, alternate
  directory, alternate prefix, or unlisted row artifact may be used for P04
  evidence.
- Aggregate summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-summary-2026-06-25.json`
- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-nonlinear-gaussian-result-2026-06-25.md`
- Refreshed P05 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p05-sv-heavy-tail-subplan-2026-06-25.md`

## Required Checks, Tests, And Reviews

- Implement or verify the harness against
  `experiments/dpf_implementation/fixtures/range_bearing.py`, using its
  `range_bearing_gaussian_moderate` fixture and preserving the model and
  observation checksums in artifacts.
- The harness must use the DPF LEDH-PFPF-OT streaming route and the locked
  SVD-Nystrom route. It must not use the sigma-point nonlinear benchmarks as
  primary evidence.
- Required local tests:
  - TensorFlow range/bearing observation and wrapped-angle residual match the
    fixture NumPy definitions on representative points.
  - Tiny CPU-hidden route smoke uses `T=2`, `N=16`, `rank=4`, `float64`, and
    emits finite streaming and Nystrom rows.
  - Harness metadata records fixture checksum, candidate policy, TF32/dtype,
    route names, residual thresholds, and nonclaims.
  - Artifact paths use the exact P04 prefix and no dense transport matrix is
    materialized.
- Claude read-only artifact review of the P04 subplan, local harness review
  note, local test log, and P03 result is required before trusted GPU evidence
  is interpreted. Claude must not read harness or test source code under the
  current approval.
- Trusted GPU preflight for GPU claims.
- Run seed rows one at a time and validate artifacts after every row.
- Verify deterministic validity, route/policy metadata, finite outputs, GPU/TF32
  provenance, residual thresholds, comparator availability, no dense
  materialization, and statistical uncertainty handling.
- Claude review is required for material threshold or P04 result consistency
  before P05 execution. Source-level harness review remains local unless the
  user grants explicit source-code disclosure approval.

## Frozen P04 Panel

| Quantity | Value |
| --- | --- |
| Fixture | `range_bearing_gaussian_moderate` from `experiments/dpf_implementation/fixtures/range_bearing.py` |
| Model | Linear Gaussian transition with nonlinear Gaussian range-bearing observation |
| Shape | `T=20`, `N=4096`, `state_dim=4`, `obs_dim=2` |
| Seeds | `84000..84005` (`6` seeds) |
| Candidate | `rank=32`, `epsilon=0.5`, `kernel_mode=raw`, `scaling_normalization=none`, `core_solver=svd_truncated`, `core_rcond=1e-6` |
| Comparator | Same-artifact compiled streaming TF32 DPF route |
| Primary threshold | `tau_component=0.05`, so `tau_total=20*2*0.05=2.0` for `abs(log_likelihood_delta)/(T*M)` exceedance |
| Statistical rule | Descriptive viability only for six seeds unless all deterministic-valid rows have zero exceedances; with zero exceedances, record one-sided 95% CP upper bound but do not rank or claim superiority |
| Deterministic Nystrom residual thresholds | `max_row_residual <= 5.0e-2`, `max_column_residual <= 5.0e-2` |
| Deterministic log-weight threshold | `final_logsumexp_residual <= 1.0e-5` |
| ESS threshold | `ess_fraction_min >= 0.005` for each route when history is returned |

P04 may pass only if all six rows are deterministic-valid and have zero
exceedances. Any exceedance is a P04 quality failure or repair trigger, not a
statistically supported ranking. If the harness cannot be implemented and
locally checked without changing the candidate policy, write
`P04_BLOCKED_RANGE_BEARING_HARNESS` and stop.

## P04 Per-Row Artifact Manifest

Only the following per-row artifact paths are valid for P04.

| Seed | JSON artifact | Markdown artifact | Log artifact |
| ---: | --- | --- | --- |
| 84000 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84000-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84000-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84000-r32-eps0p5.log` |
| 84001 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84001-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84001-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84001-r32-eps0p5.log` |
| 84002 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84002-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84002-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84002-r32-eps0p5.log` |
| 84003 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84003-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84003-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84003-r32-eps0p5.log` |
| 84004 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84004-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84004-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84004-r32-eps0p5.log` |
| 84005 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84005-r32-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84005-r32-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84005-r32-eps0p5.log` |

## Per-Row Command Shape

After local tests and review converge, launch each seed with the exact manifest
paths implied by the seed:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route both --seed ${SEED} --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04-RANGE-BEARING-SEED${SEED} --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed${SEED}-r32-eps0p5-2026-06-25.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed${SEED}-r32-eps0p5-2026-06-25.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-seed${SEED}-r32-eps0p5.log 2>&1
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does fixed SVD-Nystrom remain viable on the range-bearing nonlinear Gaussian DPF fixture outside actual-SIR? |
| Baseline/comparator | Same-artifact compiled streaming TF32 DPF route. |
| Primary criterion | Harness local checks pass, all six GPU rows are deterministic-valid, and no row exceeds `abs(log_likelihood_delta)/(T*M) > 0.05`. |
| Veto diagnostics | Missing/invalid harness, nonfinite outputs, route/policy mismatch, comparator failure, malformed artifacts, GPU/TF32 mismatch, dense materialization, residual/log-weight/ESS threshold failure, post-hoc threshold change, or any exceedance. |
| Explanatory diagnostics | Runtime, memory, ESS/tails, residuals, factor/core diagnostics, approximate UKF/sigma-point diagnostics if separately labeled. |
| Not concluded | No broad nonlinear validity, no posterior correctness, no HMC readiness, no statistical superiority, no default promotion. |
| Artifact | P04 aggregate summary and result. |

## Forbidden Claims And Actions

- Do not promote from one nonlinear fixture.
- Do not tune candidate settings after seeing P04 results.
- Do not treat sigma-point or UKF proxy diagnostics as primary DPF evidence.
- Do not treat descriptive deltas as statistical ranking.
- Do not launch HMC/autodiff checks.
- Do not send harness or test source code to Claude without explicit
  source-code disclosure approval.
- Do not execute P04 GPU rows before the harness implementation, local tests,
  and material review converge.

## Exact Next-Phase Handoff Conditions

- `P04_PASS_TO_P05_SV_HEAVY_TAIL`: gate passes and P05 subplan reviewed.
- `P04_FAIL_OPTIONAL_OR_REPAIR`: deterministic validity passes but quality gate
  fails.
- `P04_BLOCKED`: no fair executable nonlinear Gaussian harness exists.

## Stop Conditions

- Missing comparator/reference.
- Harness invalidity or failure to implement the exact DPF streaming plus
  SVD-Nystrom route.
- Trusted GPU unavailable.
- Required threshold cannot be justified before results.
- Any need to change candidate policy, threshold, fixture, seeds, shape, dtype,
  TF32 mode, or harness after seeing row results.

## Local Self-Review Of Next Subplan

Skeptical audit:

- Wrong baseline: P04 must use the same-artifact compiled streaming DPF route,
  not a sigma-point or UKF proxy.
- Proxy metric: log-likelihood delta is a bounded value-route screen only; it
  is not posterior correctness or superiority.
- Missing stop conditions: harness invalidity, comparator absence, GPU/TF32
  mismatch, dense materialization, residual/log-weight/ESS failures, and
  threshold/candidate changes are explicit stops.
- Unfair comparison: seed, fixture, dtype, TF32 mode, route policy, device, and
  candidate are fixed per row.
- Hidden assumption: range-bearing is one nonlinear Gaussian fixture only; it
  does not replace P05-P08.
- Artifact fit: P04 result must distinguish harness blockers from candidate
  quality failures.

P05 moves to non-Gaussian/heavy-tail stress and preserves the same candidate
lock and statistical interpretation boundary.
