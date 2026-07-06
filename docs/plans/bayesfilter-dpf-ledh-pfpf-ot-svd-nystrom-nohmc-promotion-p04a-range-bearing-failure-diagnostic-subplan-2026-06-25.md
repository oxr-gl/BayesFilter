# P04A Subplan: Range-Bearing Failure Diagnostic

Date: 2026-06-25

Status: `P04A_HISTORICAL_UNCALIBRATED_THRESHOLD_DIAGNOSTIC_PLAN`

Governance correction on 2026-06-25: this diagnostic remains useful for
reproducibility and scale context, but its pass/fail labels inherited the
uncalibrated P04 `0.05` nonlinear threshold. It is not an active
repair-required promotion verdict.

## Phase Objective

Diagnose the P04 range-bearing quality failure without changing the P04 pass
threshold or making a promotion claim. The diagnostic asks whether seed `84000`
reproduces the locked-candidate failure and whether simple predeclared
Nystrom-parameter controls nominate a repair candidate that would require a
new candidate-freeze validation lane.

## Entry Conditions Inherited From Previous Phase

- P04 emitted `P04_FAIL_OPTIONAL_OR_REPAIR`.
- P04 seed `84000` was deterministic-valid on GPU1/TF32 but exceeded
  `abs(log_likelihood_delta)/(T*M) > 0.05`.
- P05 is not eligible because P04 did not emit
  `P04_PASS_TO_P05_SV_HEAVY_TAIL`.
- The original locked candidate remains failed for this promotion runbook
  unless a separate reviewed repair lane freezes a new candidate and repeats
  the required evidence gates.
- No HMC readiness claim is in scope.

## Required Artifacts

- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-nonlinear-gaussian-result-2026-06-25.md`
- P04 summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-summary-2026-06-25.json`
- P04A per-row JSON/Markdown/log artifacts listed in the manifest below.
- P04A aggregate summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-diagnostic-summary-2026-06-25.json`
- P04A result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04a-range-bearing-failure-diagnostic-result-2026-06-25.md`

## Required Checks, Tests, And Reviews

- Local checks before GPU rows:
  - P04 summary JSON parses.
  - P04 seed `84000` row artifact parses and records the expected P04 failure.
  - P04A manifest has exact per-row JSON/Markdown/log paths and no wildcard
    artifacts.
- Claude artifact review is required before P04A GPU rows. Claude may review
  this subplan, the P04 result, the P04 summary, and same-prefix benchmark/log
  artifacts only. Claude must not read harness or test source code.
- Trusted GPU preflight is required immediately before GPU rows; use GPU1 if
  suitable, otherwise GPU0.
- Run rows one at a time and parse each JSON before launching the next row.
- Stop on malformed artifacts, GPU/TF32 mismatch, nonfinite outputs, route
  validity failure, or unplanned parameter/path changes.

## Frozen P04A Diagnostic Panel

All rows use the P04 range-bearing fixture, seed `84000`, `T=20`, `N=4096`,
`float32`, TF32 enabled, same-artifact streaming comparator, and active-all
transport. These rows are diagnostic only.

| Row | Purpose | Rank | Epsilon | Kernel | Scaling | Core solver | Core rcond |
| --- | --- | ---: | ---: | --- | --- | --- | ---: |
| locked-rerun | Reproduce the failed locked candidate | 32 | 0.5 | `raw` | `none` | `svd_truncated` | 1e-6 |
| rank64 | Rank sensitivity diagnostic | 64 | 0.5 | `raw` | `none` | `svd_truncated` | 1e-6 |
| rank128 | Larger-rank sensitivity diagnostic | 128 | 0.5 | `raw` | `none` | `svd_truncated` | 1e-6 |
| eps1p0 | Kernel-smoothing sensitivity diagnostic | 32 | 1.0 | `raw` | `none` | `svd_truncated` | 1e-6 |

## P04A Per-Row Artifact Manifest

Only the following artifacts are valid for P04A.

| Row | JSON artifact | Markdown artifact | Log artifact |
| --- | --- | --- | --- |
| locked-rerun | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-locked-r32-eps0p5-rerun-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-locked-r32-eps0p5-rerun-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-locked-r32-eps0p5-rerun.log` |
| rank64 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank64-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank64-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank64-eps0p5.log` |
| rank128 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank128-eps0p5-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank128-eps0p5-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank128-eps0p5.log` |
| eps1p0 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-r32-eps1p0-2026-06-25.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-r32-eps1p0-2026-06-25.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-r32-eps1p0.log` |

## Per-Row Command Shapes

After local checks, Claude artifact review, and trusted GPU preflight converge,
launch rows one at a time using the exact command shape for that row. `${GPU}`
and `${GPU_NOTE}` must come from the immediately preceding trusted GPU
preflight.

### locked-rerun

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route both --seed 84000 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04A-RANGE-BEARING-LOCKED-RERUN-SEED84000 --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-locked-r32-eps0p5-rerun-2026-06-25.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-locked-r32-eps0p5-rerun-2026-06-25.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-locked-r32-eps0p5-rerun.log 2>&1
```

### rank64

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route both --seed 84000 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 64 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04A-RANGE-BEARING-RANK64-SEED84000 --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank64-eps0p5-2026-06-25.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank64-eps0p5-2026-06-25.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank64-eps0p5.log 2>&1
```

### rank128

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route both --seed 84000 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 128 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04A-RANGE-BEARING-RANK128-SEED84000 --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank128-eps0p5-2026-06-25.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank128-eps0p5-2026-06-25.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank128-eps0p5.log 2>&1
```

### eps1p0

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route both --seed 84000 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 1.0 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04A-RANGE-BEARING-EPS1P0-SEED84000 --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-r32-eps1p0-2026-06-25.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-r32-eps1p0-2026-06-25.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-r32-eps1p0.log 2>&1
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the P04 failure reproducible for the locked candidate, and do simple parameter controls suggest a repair candidate worth a new freeze-and-validation lane? |
| Baseline/comparator | Same-artifact compiled streaming TF32 DPF route. |
| Primary diagnostic criterion | Locked rerun records deterministic-valid outputs and either reproduces or contradicts the P04 exceedance. |
| Repair-nomination diagnostic | A control row is a descriptive nominee only if it is deterministic-valid and has `abs(log_likelihood_delta)/(T*M) <= 0.05` on seed `84000`. |
| Veto diagnostics | Malformed artifact, GPU/TF32 mismatch, nonfinite outputs, route/policy mismatch, residual/log-weight/ESS threshold failure, dense materialization, or unplanned parameter/path changes. |
| Explanatory diagnostics | Runtime, memory, residuals, ESS, factor/core diagnostics, and one-seed deltas. |
| Not concluded | No P04 pass, no default promotion, no posterior correctness, no statistical superiority, no HMC readiness, no broad nonlinear validity, and no approval of a new candidate. |
| Artifact | P04A aggregate summary and result. |

## Forbidden Claims And Actions

- Do not change the P04 threshold after seeing the P04 result.
- Do not describe any P04A control as promoted, superior, default-ready, or
  validated.
- Do not run P05 from P04A unless a separate owner-approved plan changes the
  master program after a new candidate is frozen and revalidated.
- Do not send harness or test source code to Claude without explicit
  source-code disclosure approval.
- Do not launch HMC/autodiff checks.
- Do not add unplanned rows after seeing P04A outputs.

## Exact Next-Phase Handoff Conditions

- `P04A_LOCKED_FAILURE_CONFIRMED_REPAIR_REQUIRED`: locked rerun is
  deterministic-valid and exceeds the P04 threshold again.
- `P04A_REPRO_INCONSISTENT_BLOCKER`: locked rerun is deterministic-valid but
  contradicts the P04 exceedance enough that nondeterminism or artifact
  validity must be investigated.
- `P04A_REPAIR_CANDIDATE_NOMINATED_NO_PROMOTION`: one or more control rows pass
  the one-seed diagnostic screen; this only nominates a new candidate-freeze
  lane.
- `P04A_BLOCKED`: harness/runtime/artifact validity fails.

## Stop Conditions

- Trusted GPU unavailable.
- Locked rerun artifact is malformed or missing.
- Any route has nonfinite outputs or fails deterministic residual/log-weight/ESS
  checks.
- GPU/TF32 provenance does not match the runbook target.
- Any need arises to change threshold, seed, fixture, dtype, candidate row set,
  source code, or artifact paths after seeing results.

## Local Self-Review Of This Subplan

Skeptical audit:

- Wrong baseline: same-artifact streaming DPF remains the comparator.
- Proxy metric: one-seed deltas can only diagnose or nominate repair; they do
  not establish superiority, validity, or promotion readiness.
- Missing stop conditions: malformed artifacts, route invalidity, GPU/TF32
  mismatch, post-hoc changes, and unplanned rows are explicit stops.
- Unfair comparison: all rows use the same fixture, seed, shape, dtype, TF32
  target, comparator, and artifact schema.
- Hidden assumption: a passing control row would not rescue the original locked
  candidate or close P04; it would only motivate a new frozen candidate lane.
- Environment mismatch: trusted GPU preflight is required before rows.
- Artifact fit: exact row artifacts and result/summary paths are named before
  execution.

Audit status: `PASS_FOR_CLAUDE_ARTIFACT_REVIEW`.
