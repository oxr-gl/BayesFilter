# P04C2 Subplan: Streaming GPU TF32/JIT Isolation

Date: 2026-06-26

Status: `P04C2_REVIEW_AGREE_READY_FOR_PREFLIGHT`

## Phase Objective

Disentangle the P04C1 seed `84101` streaming comparator nonfinite diagnostic
by isolating GPU device execution, TF32, and JIT/XLA factors for the streaming
route only.

P04C2 must not continue the P04C calibration panel, drop seed `84101`, freeze a
threshold, tune SVD-Nystrom, validate or reject SVD-Nystrom, launch P05, or
change the locked candidate policy.

## Entry Conditions Inherited From Previous Phase

- P04C0 emitted `P04C0_HARNESS_CONTROL_PASS_TO_P04C_PREFLIGHT`.
- P04C emitted `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`.
- P04C1 emitted `P04C1_GPU_TF32_OR_JIT_SPECIFIC_DIAGNOSTIC`.
- P04C1 `gpu-streaming-repro-84101` reproduced streaming nonfinite output on
  GPU1 with TF32 enabled and JIT on.
- P04C1 `gpu-both-repro-84101` reproduced the original both-route blocker:
  streaming failed and Nystrom passed.
- P04C1 `gpu-streaming-control-84100` passed on GPU1 with TF32 enabled and JIT
  on.
- P04C1 `cpu-streaming-control-84101` passed with CPU hidden, TF32 disabled,
  and JIT off.
- P04C has no valid aggregate scale summary.
- P05 remains blocked.
- No HMC readiness claim is in scope.

## Required Artifacts

- P04C2 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-subplan-2026-06-26.md`
- P04C2 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-result-2026-06-26.md`
- P04C2 aggregate isolation summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-summary-2026-06-26.json`
- P04C1 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-result-2026-06-26.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-execution-ledger-2026-06-25.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-claude-review-ledger-2026-06-25.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-stop-handoff-2026-06-25.md`
- Per-row JSON/Markdown/log artifacts listed in the manifest below.

## Required Checks, Tests, And Reviews

- Before runtime diagnostics:
  - Parse/review the P04C1 result.
  - Parse the P04C1 aggregate summary as an execution-side local check; do not
    send the summary to Claude unless a separate review prompt explicitly
    authorizes that exact artifact.
  - Confirm P04C1 classified the issue as GPU/TF32/JIT-specific, not as a
    SVD-Nystrom failure.
  - Confirm this subplan has exact artifact paths and no wildcard artifacts.
  - Confirm no command changes the locked SVD-Nystrom policy or resumes P04C
    calibration.
- Claude read-only review is required before GPU rows. For the P04C2 plan
  review, Claude may review only this exact subplan and the exact P04C1 result
  unless a separate review prompt explicitly authorizes additional exact
  artifacts. Claude may not read benchmark JSONs, logs, source code, tests, or
  unrelated paths; run commands; edit files; authorize threshold freeze;
  authorize P05; or authorize promotion/default/scientific/HMC boundaries.
- Trusted GPU preflight is required immediately before GPU rows; use GPU1 if
  suitable, otherwise GPU0.
- Run rows one at a time and parse each JSON before launching the next row.
- A diagnostic row may exit nonzero if the benchmark records a valid JSON
  artifact with route nonfinite hard vetoes. For P04C2, process nonzero is a
  blocker only when the JSON/Markdown/log artifact is missing, malformed,
  timed out, route/GPU/TF32/JIT mismatched, or otherwise fails the row's
  diagnostic evidence contract.
- Stop on malformed artifacts, GPU/TF32/JIT mismatch, non-predeclared command
  changes, or any result that invalidates the benchmark harness more broadly
  than the planned diagnostics can explain.

## Diagnostic Panel

All rows use the same range-bearing fixture, `T=20`, `N=4096`, `float32`,
streaming route only, active-all transport, and seed `84101`. Rows are not
calibration rows and must not be included in any P04C scale summary.

P04C1 already established the GPU/TF32/JIT-on row as nonfinite and the
CPU/no-JIT/TF32-disabled row as finite. P04C2 adds the missing GPU controls.

| Row | Purpose | Route | Seed | Device scope | TF32 | JIT | Expected diagnostic meaning |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| gpu-tf32-nojit-84101 | Test whether TF32 is sufficient to reproduce nonfinites without JIT | `streaming` | 84101 | visible GPU | enabled | off | If nonfinite while no-TF32/no-JIT is finite, TF32 is implicated independent of JIT. |
| gpu-notf32-jit-84101 | Test whether JIT is sufficient to reproduce nonfinites without TF32 | `streaming` | 84101 | visible GPU | disabled | on | If nonfinite while no-TF32/no-JIT is finite, JIT/XLA is implicated independent of TF32. |
| gpu-notf32-nojit-84101 | Test GPU execution without TF32 or JIT | `streaming` | 84101 | visible GPU | disabled | off | If nonfinite, GPU/device-kernel behavior is implicated beyond TF32/JIT toggles. If finite, the P04C1 CPU pass is supported as not merely CPU-specific. |

## P04C2 Per-Row Artifact Manifest

Only the following artifacts are valid for P04C2.

| Row | JSON artifact | Markdown artifact | Log artifact |
| --- | --- | --- | --- |
| gpu-tf32-nojit-84101 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-tf32-nojit-seed84101-2026-06-26.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-tf32-nojit-seed84101-2026-06-26.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c2-gpu-tf32-nojit-seed84101.log` |
| gpu-notf32-jit-84101 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-jit-seed84101-2026-06-26.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-jit-seed84101-2026-06-26.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-jit-seed84101.log` |
| gpu-notf32-nojit-84101 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-nojit-seed84101-2026-06-26.json` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-nojit-seed84101-2026-06-26.md` | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-nojit-seed84101.log` |

## Command Shapes

`${GPU}` and `${GPU_NOTE}` must come from the immediately preceding trusted GPU
preflight.

### gpu-tf32-nojit-84101

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route streaming --seed 84101 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --paired-threshold-mode record-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --no-jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04C2-GPU-TF32-NOJIT-SEED84101 --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-tf32-nojit-seed84101-2026-06-26.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-tf32-nojit-seed84101-2026-06-26.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c2-gpu-tf32-nojit-seed84101.log 2>&1
```

### gpu-notf32-jit-84101

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route streaming --seed 84101 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --paired-threshold-mode record-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode disabled --jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04C2-GPU-NOTF32-JIT-SEED84101 --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-jit-seed84101-2026-06-26.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-jit-seed84101-2026-06-26.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-jit-seed84101.log 2>&1
```

### gpu-notf32-nojit-84101

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py --route streaming --seed 84101 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode full --paired-threshold-mode record-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode disabled --no-jit-compile --device-scope visible --cuda-visible-devices ${GPU} --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu ${GPU} --gpu-selection-note "${GPU_NOTE}" --phase-id SVD-NYSTROM-NOHMC-PROMOTION-P04C2-GPU-NOTF32-NOJIT-SEED84101 --quiet --output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-nojit-seed84101-2026-06-26.json --markdown-output docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-nojit-seed84101-2026-06-26.md > docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c2-gpu-notf32-nojit-seed84101.log 2>&1
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which execution factor explains the seed `84101` streaming comparator nonfinite artifact: TF32, JIT/XLA, GPU/device behavior, or a TF32+JIT interaction? |
| Baseline/comparator | P04C1 GPU/TF32/JIT-on seed `84101` streaming failure and P04C1 CPU/no-JIT/TF32-disabled seed `84101` streaming pass. |
| Primary criterion | Produce an isolation classification with exact row artifacts; do not resume calibration unless a later reviewed plan authorizes it. |
| Veto diagnostics | Malformed artifact, GPU/TF32/JIT mismatch, route/policy mismatch, non-predeclared command change, source-code disclosure to Claude, unsupported claim, or need to change calibration pass/fail criteria after seeing diagnostics. |
| Explanatory diagnostics | Route finite status, log likelihood, ESS, per-route hard vetoes, runtime, GPU/TF32/JIT differences. |
| Not concluded | No calibrated threshold, no repaired P04C panel, no seed exclusion, no SVD-Nystrom rejection, no default promotion, no posterior correctness, no HMC readiness, no statistical superiority, and no broad nonlinear validity. |
| Artifact | P04C2 aggregate isolation summary and result. |

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

- `P04C2_TF32_SPECIFIC_STREAMING_NONFINITE`: GPU TF32/no-JIT is nonfinite and
  GPU no-TF32/no-JIT is finite.
- `P04C2_JIT_SPECIFIC_STREAMING_NONFINITE`: GPU no-TF32/JIT is nonfinite and
  GPU no-TF32/no-JIT is finite.
- `P04C2_TF32_JIT_INTERACTION_STREAMING_NONFINITE`: GPU TF32/no-JIT,
  GPU no-TF32/JIT, and GPU no-TF32/no-JIT are all finite while the P04C1
  GPU TF32/JIT row remains the active reproduced failure.
- `P04C2_GPU_DEVICE_STREAMING_NONFINITE`: GPU no-TF32/no-JIT is nonfinite
  while the P04C1 CPU no-TF32/no-JIT control was finite.
- `P04C2_REPRO_INCONSISTENT_BLOCKER`: the planned rows contradict P04C1 in a
  way that requires a separate nondeterminism/provenance diagnostic.
- `P04C2_BLOCKED_INVALID_DIAGNOSTIC_ARTIFACT`: any required diagnostic artifact
  is missing, malformed, or violates route/GPU/TF32/JIT policy.

Any handoff from P04C2 still requires a later reviewed subplan before P04C can
resume, seed `84101` can be handled, a threshold can be frozen, or P05 can run.

## Stop Conditions

- P04C1 result does not emit `P04C1_GPU_TF32_OR_JIT_SPECIFIC_DIAGNOSTIC`.
- Claude review does not converge for this material diagnostic plan.
- Trusted GPU unavailable for GPU rows.
- A required row artifact is malformed, missing, timed out, or route/GPU/TF32/
  JIT mismatched. A nonzero process exit with a valid JSON nonfinite-route
  diagnostic is not by itself malformed in P04C2.
- Any need arises to change commands, seeds, fixture, shape, dtype target,
  candidate policy, or calibration rules after seeing diagnostics.
- Continuing would require P04C calibration continuation, P05 execution,
  threshold freeze, source-code disclosure to Claude, package installation,
  network fetches, commits, pushes, destructive actions, or default/product/
  scientific/HMC authorization.

## End-Of-Phase Requirements

At P04C2 close, Codex must:

1. run required local checks;
2. write the P04C2 result/close record;
3. update the exact execution ledger, Claude review ledger, and stop handoff
   artifacts listed above;
4. draft or refresh the next subplan only if the diagnostic result justifies
   one;
5. review any material next subplan locally and, when appropriate, with Claude.

## Local Self-Review Of This Subplan

Skeptical audit:

- Wrong baseline: P04C2 compares against the P04C1 reproduced failure and
  P04C1 CPU/no-JIT pass, not against a threshold or promotion claim.
- Proxy metric: finite route status is a diagnostic validity check, not a
  method ranking.
- Missing stop conditions: artifact malformedness, GPU/TF32/JIT mismatch,
  command drift, review nonconvergence, and calibration continuation are
  explicit stops.
- Unfair comparison: diagnostic rows are execution-factor controls and are not
  calibration rows.
- Hidden assumption: no single factor will be named unless the predeclared row
  pattern supports it.
- Environment mismatch: GPU rows require trusted preflight.
- Artifact fit: exact row artifacts and result/summary paths are named before
  execution.

Audit status: `P04C2_LOCAL_AND_CLAUDE_REVIEW_PASS_READY_FOR_PREFLIGHT`.
