# P05 Subplan: SVD Core-Solver Focused Tuning

Date: 2026-06-24

Status: `READY_FOR_LOCAL_AND_CLAUDE_REVIEW`

## Phase Objective

Test whether the existing opt-in `svd_truncated` Nystrom core solver is a viable
policy-robustness candidate for reducing bounded value-route paired-error tails
without changing `tau_component=0.03`, the model shape, dtype, TF32 mode,
transport policy, or comparator.

This is a tuning/nomination phase, not validation and not promotion.

## Entry Conditions Inherited From Previous Phase

- P3 final status:
  `P3_INCONCLUSIVE_STOP_THRESHOLD_UNSUPPORTED_BY_PANEL`.
- P3 deterministic validity passed for all included rows.
- Frozen threshold `tau_component=0.03` remains unsupported for the current
  fixed policy under the predeclared CP gate.
- P04 selected policy robustness/tuning as the next path.
- Current fixed policy baseline:
  `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=cholesky`.
- Candidate policy:
  `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=svd_truncated`.
- Tuning seeds must be disjoint from P1 calibration seeds and all P3 validation
  seeds already run.

## Required Artifacts

Per seed and arm:

- JSON:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-<ARM>-seed<SEED>-r32-eps0p5-2026-06-24.json`
- Markdown:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-<ARM>-seed<SEED>-r32-eps0p5-2026-06-24.md`
- Log:
  `docs/plans/logs/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-<ARM>-seed<SEED>-r32-eps0p5-2026-06-24.log`

Aggregate summary:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-summary-2026-06-24.json`

P05 result:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-result-2026-06-24.md`

Next subplan:

- P06 fresh validation subplan if SVD is nominated;
- or closeout/no-promotion subplan if SVD is not nominated.

## Required Checks, Tests, And Reviews

Pre-run local checks:

- verify benchmark harness supports `--nystrom-core-solver svd_truncated`;
- verify focused tests exist for SVD core-solver metadata and tensor route;
- verify tuning seeds are disjoint from P1 and all executed P3 seeds;
- verify `tau_component=0.03` and CP pass gate are not changed;
- verify output/log paths are unique and predeclared;
- trusted `nvidia-smi` preflight before GPU work;
- select physical GPU1 if available/suitable, otherwise GPU0.

Review:

- local review required before launch;
- Claude read-only review required before execution because this phase launches
  material GPU tuning and can influence the next validation design.

Execution:

- tuning seeds: `82962..82967` (`6` fresh disjoint seeds);
- arms:
  - `control_cholesky_raw`: current fixed policy;
  - `candidate_svd_raw`: same policy except `--nystrom-core-solver svd_truncated`;
- run one seed and arm at a time;
- parse structured artifacts after every row;
- stop immediately on deterministic invalidity, malformed/missing artifact,
  GPU/TF32/shape/policy mismatch, or seed overlap.
- set `CUDA_VISIBLE_DEVICES=<GPU>` through the benchmark
  `--cuda-visible-devices <GPU>` option.  TensorFlow then sees the selected
  physical GPU as visible device `/GPU:0`, which is why the benchmark device
  target remains `--device /GPU:0`.  Record the selected physical GPU and this
  remapping note in row metadata.

Per-row command template:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds <SEED> --time-steps 20 --num-particles 8192 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-core-solver <cholesky|svd_truncated> --nystrom-core-rcond 1e-6 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices <GPU> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <GPU> --gpu-selection-note '<GPU note; CUDA_VISIBLE_DEVICES remaps selected physical GPU to TensorFlow /GPU:0>' --phase-id ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P05-<ARM>-SEED<SEED> --quiet --output <JSON> --markdown-output <MD> > <LOG> 2>&1
```

Post-run checks:

- each JSON parses;
- deterministic validity is assessed from parsed artifacts and declared checks,
  not process exit alone;
- legacy-threshold-only process exits remain stochastic exceedances, not
  deterministic invalidity, if parsed artifact checks pass;
- compute `abs(delta)/(20*9)` for each deterministic-valid row;
- report exceedance counts by arm;
- report paired candidate-control delta summaries on the same tuning seeds as
  descriptive tuning evidence only;
- do not use candidate-control descriptive summaries as a promotion or veto
  criterion in P05;
- do not declare statistical superiority from this tuning split.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is `svd_truncated` a viable robustness candidate worth a fresh validation split under the existing `tau_component=0.03` screen? |
| Baseline/comparator | Same-seed `control_cholesky_raw` plus same-artifact compiled streaming TF32 comparator inside each benchmark artifact. |
| Primary tuning criterion | Candidate is deterministic-valid on all tuning rows and has at most one `tau_component=0.03` exceedance across six tuning seeds. |
| Nomination criterion | If the candidate passes the primary tuning screen, has SVD metadata recorded in every candidate row, and no deterministic/artifact/GPU/metadata veto fires, nominate it for a fresh P06 validation split. |
| Veto diagnostics | Deterministic invalidity, malformed artifact, GPU/TF32/shape/policy mismatch, seed overlap, missing paired delta, or SVD metadata not recorded. |
| Explanatory diagnostics | Runtime, residual magnitudes below deterministic thresholds, SVD singular-value/core diagnostics, normalized paired errors, control-vs-candidate descriptive deltas. |
| Not concluded | No validation pass, no default readiness, no posterior correctness, no HMC readiness, no statistical superiority, no broad Nystrom rejection. |
| Artifact | Per-row JSON/Markdown/logs, aggregate summary, P05 result, and P06-or-closeout subplan. |

Candidate-control descriptive summaries are explanatory only in this tuning
phase.  They may nominate follow-up analysis language, but they must not veto a
candidate that passes the primary tuning criterion and must not promote a
candidate that fails it.

## Forbidden Claims And Actions

- Do not change `tau_component=0.03`.
- Do not change the CP pass gate.
- Do not call P05 a validation split.
- Do not use P3 rows as validation for the SVD candidate.
- Do not rank SVD as superior from six tuning seeds.
- Do not claim default readiness, HMC readiness, posterior correctness,
  statistical superiority, or broad Nystrom rejection.
- Do not tune threshold, rank, epsilon, kernel mode, scaling normalization,
  dtype, TF32 mode, shape, or transport policy in this phase.

## Exact Next-Phase Handoff Conditions

- `P05_NOMINATE_SVD_TO_P06`: candidate deterministic validity passes all tuning
  rows, candidate exceedances are `<=1/6`, SVD metadata is recorded in every
  candidate row, every required artifact/log is parseable/present, and no
  deterministic, GPU/TF32, shape, policy, seed-overlap, paired-delta, or
  metadata veto occurs.
- `P05_NO_SVD_REPAIR_CLOSEOUT`: candidate deterministic validity passes but
  candidate exceedance count is `>=2/6`, or candidate deterministic validity
  passes but required SVD metadata or paired-delta fields are missing.
- `P05_DETERMINISTIC_BLOCKER`: any deterministic validity, artifact, GPU/TF32,
  metadata, or seed-overlap veto occurs.
- `P05_BLOCKED`: execution requires unapproved Claude export, GPU runtime,
  environment setup, package install, or human product/scientific decision.

## Stop Conditions

- Claude/local review does not converge.
- Trusted GPU unavailable.
- Any tuning seed overlaps P1 or executed P3 seeds.
- A launched row times out and writes no parseable artifact.
- Deterministic validity fails.
- Continuing would require changing threshold, default policy, HMC/posterior
  scope, package/environment setup, or destructive action.

## Skeptical Plan Audit

| Risk | P05 Audit |
| --- | --- |
| Wrong baseline | Same-seed control arm and same-artifact streaming comparator are explicit. |
| Proxy metric | Six-seed tuning evidence can nominate only; it cannot validate or rank. |
| Missing stop conditions | GPU, artifact, deterministic validity, seed overlap, timeout, metadata, and threshold-change stops are explicit. |
| Unfair comparison | Candidate differs only by `core_solver=svd_truncated`; rank, epsilon, kernel mode, dtype, TF32, transport policy, shape, and comparator stay fixed. |
| Hidden assumption | SVD may not address the observed tail; P05 can fail without rejecting Nystrom broadly. |
| Stale context | P3 final status remains threshold-support failure for cholesky raw policy. |
| Environment mismatch | Trusted GPU preflight required; GPU1 preferred otherwise GPU0. |
| Artifact mismatch | Structured JSON/Markdown/logs required for every included row. |

Audit status: `READY_FOR_LOCAL_AND_CLAUDE_REVIEW`.
