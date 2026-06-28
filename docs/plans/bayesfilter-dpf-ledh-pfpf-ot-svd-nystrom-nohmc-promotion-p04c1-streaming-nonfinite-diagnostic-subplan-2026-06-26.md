# P04C1 Subplan: Streaming Comparator Nonfinite Diagnostic

Date: 2026-06-26

Status: `P04C1_CLOSED_GPU_TF32_OR_JIT_SPECIFIC_DIAGNOSTIC`

## Phase Objective

Diagnose why P04C seed `84101` produced a deterministic-invalid streaming
comparator artifact while the SVD-Nystrom route passed deterministic checks.
This phase decides whether the P04C blocker is reproducible, route-specific,
environment-specific, or a broader range-bearing fixture/harness validity
problem.

P04C1 must not continue the calibration panel, drop seed `84101`, freeze a
threshold, validate or reject SVD-Nystrom, launch P05, or change the locked
candidate policy.

## Entry Conditions Inherited From Previous Phase

- P04C0 emitted `P04C0_HARNESS_CONTROL_PASS_TO_P04C_PREFLIGHT`.
- P04C emitted `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`.
- Seed `84100` P04C row passed with `--paired-threshold-mode record-only`.
- Seed `84101` P04C row failed because the streaming comparator route emitted
  nonfinite log likelihood, filtered means, filtered variances, and ESS.
- The SVD-Nystrom route passed deterministic checks on seed `84101`.
- P04C has no valid aggregate scale summary.
- P05 remains blocked.
- No HMC readiness claim is in scope.

## Required Artifacts

- P04C1 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-subplan-2026-06-26.md`
- P04C1 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-result-2026-06-26.md`
- P04C1 aggregate diagnostic summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-summary-2026-06-26.json`
- Per-row JSON/Markdown/log artifacts listed in the manifest below.
- Updated execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-execution-ledger-2026-06-25.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-claude-review-ledger-2026-06-25.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-stop-handoff-2026-06-25.md`

## Required Checks, Tests, And Reviews

- Before runtime diagnostics:
  - Parse P04C seed `84100` and seed `84101` row artifacts.
  - Confirm seed `84101` failure is from the streaming route, not from the
    record-only paired threshold mode.
  - Confirm this subplan has exact artifact paths and no wildcard artifacts.
  - Confirm no command changes the locked SVD-Nystrom policy.
- Claude read-only review is required before GPU rows. Claude may review this
  exact subplan, P04C/P04C0 result documents, same-prefix benchmark artifacts,
  and same-prefix logs only. Claude may not read source code, run commands,
  edit files, authorize threshold freeze, authorize P05, or authorize
  promotion/default/scientific/HMC boundaries.
- Trusted GPU preflight is required immediately before GPU rows; use GPU1 if
  suitable, otherwise GPU0.
- Run rows one at a time and parse each JSON before launching the next row.
- A diagnostic row may exit nonzero if the benchmark records a valid JSON
  artifact with route nonfinite hard vetoes. For P04C1, process nonzero is a
  blocker only when the JSON/Markdown/log artifact is missing, malformed,
  timed out, route/GPU/TF32 mismatched, or otherwise fails the row's diagnostic
  evidence contract.
- Stop on malformed artifacts, GPU/TF32 mismatch for GPU rows, non-predeclared
  command changes, or any result that invalidates the benchmark harness more
  broadly than the planned diagnostics can explain.

## Diagnostic Panel

All GPU rows use the same range-bearing fixture, `T=20`, `N=4096`,
`float32`, TF32 enabled, active-all transport, and trusted GPU. Diagnostic rows
are not calibration rows and must not be included in any P04C scale summary.

| Row | Purpose | Route | Seed | Device scope | JIT | Expected diagnostic meaning |
| --- | --- | --- | ---: | --- | --- | --- |
| gpu-streaming-repro-84101 | Reproduce the seed `84101` streaming failure with route selection set to streaming only | `streaming` | 84101 | visible GPU | on | If nonfinite, streaming-selected failure is reproducible without selecting the both-route row. |
| gpu-both-repro-84101 | Check whether the original both-route row remains reproducible | `both` | 84101 | visible GPU | on | If nonfinite, original P04C blocker is reproducible. |
| gpu-streaming-control-84100 | Check passing-neighbor streaming route under same command shape | `streaming` | 84100 | visible GPU | on | If finite, seed-specific initial-particle path is implicated more than blanket streaming failure. |
| cpu-streaming-control-84101 | Check whether seed `84101` streaming failure is GPU/TF32-specific | `streaming` | 84101 | CPU hidden | off | If finite, GPU/TF32/JIT/numerics are implicated; if nonfinite, fixture/seed/harness route is implicated. |

The CPU row is diagnostic only and cannot replace GPU/TF32 evidence. It may run
without trusted GPU preflight only after the GPU rows have established the
failure classification or if trusted GPU becomes unavailable.

## P04C1 Per-Row Artifact Manifest

Only the following artifacts are valid for P04C1.

| Row | JSON artifact | Markdown artifact | Log artifact |
| --- | --- | --- | --- |
| gpu-streaming-repro-84101 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-repro-seed84101-2026-06-26.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-repro-seed84101-2026-06-26.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-streaming-repro-seed84101.log` |
| gpu-both-repro-84101 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-both-repro-seed84101-2026-06-26.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-both-repro-seed84101-2026-06-26.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-both-repro-seed84101.log` |
| gpu-streaming-control-84100 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-control-seed84100-2026-06-26.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-control-seed84100-2026-06-26.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-streaming-control-seed84100.log` |
| cpu-streaming-control-84101 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-cpu-streaming-control-seed84101-2026-06-26.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-cpu-streaming-control-seed84101-2026-06-26.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-cpu-streaming-control-seed84101.log` |

## Command Shapes

`${GPU}` and `${GPU_NOTE}` must come from the immediately preceding trusted GPU
preflight.

### gpu-streaming-repro-84101

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route streaming --seed 84101 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --paired-threshold-mode record-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04C1-STREAMING-REPRO-SEED84101 --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-repro-seed84101-2026-06-26.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-repro-seed84101-2026-06-26.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-streaming-repro-seed84101.log 2>&1
```

### gpu-both-repro-84101

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route both --seed 84101 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --paired-threshold-mode record-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04C1-BOTH-REPRO-SEED84101 --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-both-repro-seed84101-2026-06-26.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-both-repro-seed84101-2026-06-26.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-both-repro-seed84101.log 2>&1
```

### gpu-streaming-control-84100

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route streaming --seed 84100 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --paired-threshold-mode record-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04C1-STREAMING-CONTROL-SEED84100 --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-control-seed84100-2026-06-26.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-control-seed84100-2026-06-26.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-streaming-control-seed84100.log 2>&1
```

### cpu-streaming-control-84101

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route streaming --seed 84101 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --paired-threshold-mode record-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode disabled --no-jit-compile --device-scope cpu --device /CPU:0 --expect-device-kind cpu --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04C1-CPU-STREAMING-CONTROL-SEED84101 --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-cpu-streaming-control-seed84101-2026-06-26.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-cpu-streaming-control-seed84101-2026-06-26.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-cpu-streaming-control-seed84101.log 2>&1
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the seed `84101` streaming comparator nonfinite artifact reproducible, route-specific, and/or GPU/TF32/JIT-specific? |
| Baseline/comparator | P04C seed `84101` failed both-route artifact and P04C seed `84100` passed artifact. |
| Primary criterion | Produce a diagnostic classification with exact row artifacts; do not resume calibration unless a later reviewed plan authorizes it. |
| Veto diagnostics | Malformed artifact, GPU/TF32 mismatch for GPU rows, route/policy mismatch, non-predeclared command change, source-code disclosure to Claude, unsupported claim, or need to change calibration pass/fail criteria after seeing diagnostics. |
| Explanatory diagnostics | Route finite status, log likelihood, ESS, per-route hard vetoes, runtime, GPU/CPU/JIT differences. |
| Not concluded | No calibrated threshold, no repaired P04C panel, no seed exclusion, no SVD-Nystrom rejection, no default promotion, no posterior correctness, no HMC readiness, no statistical superiority, and no broad nonlinear validity. |
| Artifact | P04C1 aggregate diagnostic summary and result. |

## Forbidden Claims And Actions

- Do not drop seed `84101` from P04C.
- Do not count seed `84101` as a non-exceedance.
- Do not resume P04C calibration rows `84102..84111`.
- Do not freeze or validate a threshold.
- Do not tune SVD-Nystrom rank, epsilon, kernel mode, scaling mode, solver, or
  rcond.
- Do not change fixture, shape, dtype target, or seed split.
- Do not send source code or tests to Claude without explicit approval.
- Do not launch P05.
- Do not make default, product, HMC-readiness, posterior-correctness,
  statistical-superiority, or broad scientific-validity claims.

## Exact Next-Phase Handoff Conditions

- `P04C1_STREAMING_NONFINITE_REPRODUCED_ROUTE_SPECIFIC`: seed `84101`
  streaming-only GPU row reproduces nonfinite output and seed `84100`
  streaming-only GPU control remains finite.
- `P04C1_GPU_TF32_OR_JIT_SPECIFIC_DIAGNOSTIC`: GPU seed `84101` reproduces
  nonfinite output but CPU/no-JIT control is finite.
- `P04C1_FIXTURE_OR_SEED_PATH_INVALIDITY_DIAGNOSTIC`: seed `84101` remains
  nonfinite even in CPU/no-JIT streaming control.
- `P04C1_REPRO_INCONSISTENT_BLOCKER`: the seed `84101` failure does not
  reproduce in planned controls, requiring a separate nondeterminism/provenance
  diagnostic before calibration can resume.
- `P04C1_BLOCKED_INVALID_DIAGNOSTIC_ARTIFACT`: any required diagnostic artifact
  is missing, malformed, or violates route/GPU/TF32 policy.

Any handoff from P04C1 still requires a later reviewed subplan before P04C can
resume, seed `84101` can be handled, or a threshold can be frozen.

## Stop Conditions

- P04C result does not emit `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`.
- Claude review does not converge for this material diagnostic plan.
- Trusted GPU unavailable for GPU rows.
- A required row artifact is malformed, missing, timed out, or route/GPU/TF32
  mismatched. A nonzero process exit with a valid JSON nonfinite-route
  diagnostic is not by itself malformed in P04C1.
- Any need arises to change commands, seeds, fixture, shape, dtype target,
  candidate policy, or calibration rules after seeing diagnostics.
- Continuing would require P04C calibration continuation, P05 execution,
  threshold freeze, source-code disclosure to Claude, package installation,
  network fetches, commits, pushes, destructive actions, or default/product/
  scientific/HMC authorization.

## End-Of-Phase Requirements

At P04C1 close, Codex must:

1. run required local checks;
2. write the P04C1 result/close record;
3. update the exact execution ledger, Claude review ledger, and stop handoff
   artifacts listed above;
4. draft or refresh the next subplan only if the diagnostic result justifies
   one;
5. review any material next subplan locally and, when appropriate, with Claude.

## Local Self-Review Of This Subplan

Skeptical audit:

- Wrong baseline: P04C1 compares against the failed seed `84101` artifact and
  passing seed `84100` control, not against a threshold or promotion claim.
- Proxy metric: finite route status is a diagnostic validity check, not a
  method ranking.
- Missing stop conditions: artifact malformedness, GPU/TF32 mismatch, command
  drift, review nonconvergence, and calibration continuation are explicit
  stops.
- Unfair comparison: diagnostic rows are route/device/JIT controls and are not
  calibration rows.
- Hidden assumption: CPU/no-JIT finite output cannot substitute for GPU/TF32
  calibration evidence.
- Environment mismatch: GPU rows require trusted preflight.
- Artifact fit: exact row artifacts and result/summary paths are named before
  execution.

Audit status: `P04C1_LOCAL_AND_CLAUDE_REVIEW_PASS_READY_FOR_PREFLIGHT`.
