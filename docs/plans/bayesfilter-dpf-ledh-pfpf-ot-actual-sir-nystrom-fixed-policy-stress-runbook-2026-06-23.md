# Actual-SIR Nystrom Fixed-Policy Stress Runbook

Date: 2026-06-23

Status: `READY_TO_LAUNCH_P01_SEED_REPLICATION`

## Objective

Stress-test the restricted fixed Nystrom policy:

- `rank=32`;
- `epsilon=0.5`;
- `kernel_mode=raw`;
- `scaling_normalization=none`;
- `float32`, TF32 enabled, JIT compiled;
- trusted GPU, GPU1 if available otherwise GPU0.

This runbook is separate from the closed balanced-scaling repair lane.  It
tests restricted-policy viability only.

## Research Intent Ledger

| Field | Plan |
| --- | --- |
| Main question | Does fixed `rank=32,epsilon=0.5` remain stable under extra seed batches and a one-seed high-N ladder? |
| Candidate/mechanism | Current compiled tensor-only fixed-rank Nystrom route with raw kernel and default scaling normalization `none`. |
| Expected failure mode | Nonfinite factors/particles/log likelihood, residual hard veto, paired likelihood drift, missing GPU/TF32 evidence, or fixed-policy metadata missing. |
| Promotion criterion | None in this runbook; passing all phases only supports a fixed-policy candidate for a later promotion/stress program. |
| Promotion veto | Any default-readiness, superiority, posterior-correctness, HMC-readiness, or broad rank/epsilon robustness claim. |
| Continuation veto | Invalid/missing artifact, trusted GPU unavailable, missing fixed-policy metadata, threshold drift, hard-veto failure, or a high-N row exceeding the runtime stop limit. |
| Repair trigger | Any hard veto at the fixed policy stops this stress runbook and triggers classification rather than tuning. |
| Explanatory diagnostics | Runtime, residuals, paired deltas, denominator/factor/scaling diagnostics, spectrum diagnostics. |
| What must not be concluded | No default readiness, no statistical ranking, no broad robust rank/epsilon policy, no posterior correctness, no HMC readiness. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Is the restricted fixed policy stable across the predeclared seed and high-N stress gates? |
| Exact baseline/comparator | Compiled streaming TF32 actual-SIR route in each paired artifact. |
| Primary pass/fail criterion | Every launched row has aggregate `status == PASS`, finite outputs, no Nystrom residual veto, paired max delta <= `10.0`, paired mean delta <= `5.0`, trusted GPU/TF32 evidence, and fixed-policy metadata. |
| Veto diagnostics | Any aggregate hard veto, missing GPU/TF32 evidence, missing metadata, threshold drift, nonfinite outputs, residual threshold failure, paired threshold failure, missing artifact, or runtime stop. |
| Explanatory only | Runtime, warm timing ratio, factor/scaling ranges, denominator floor hits, spectrum diagnostics. |
| Not concluded if pass | No default readiness, no superiority/ranking, no broad rank/epsilon robustness, no posterior correctness, no HMC readiness. |
| Artifact preserving result | Phase JSON/Markdown/log files and phase result notes. |

## Skeptical Plan Audit

Wrong-baseline risk: prior artifacts could be stale after code changes.
Mitigation: every stress row uses paired streaming and fixed Nystrom in the same
current-code artifact.

Proxy-promotion risk: stress rows passing could be misread as default
readiness.  Mitigation: this runbook only supports restricted-policy viability.

Hidden tuning risk: fixed `epsilon=0.5` was selected after observed failures.
Mitigation: this is explicitly a restricted policy, not an optimized broad
policy.

Statistical risk: seed batches remain limited and high-N ladder is one seed per
N.  Mitigation: hard-veto pass/fail only; no ranking or superiority claim.

Environment risk: sandbox GPU failures can be misleading.  Mitigation: trusted
GPU preflight and artifact manifests are required.

Audit status: `PASS_READY_TO_RUN_P01`.

## Phases

| Phase | Objective | Required artifacts |
| --- | --- | --- |
| P01 | Extra `N=1024,T=20` seed replication at the fixed policy | two JSON/Markdown/log row artifacts and P01 result |
| P02 | One-seed high-N ladder at the fixed policy, only if P01 passes | row artifacts and P02 result |
| P03 | Closeout / next recommendation | final result and stop handoff |

## P01 Seed Replication Gate

Rows:

- batch seeds `81925,81926,81927,81928,81929`;
- batch seeds `81930,81931,81932,81933,81934`.

Fixed row shape:

- `T=20`;
- `N=1024`;
- `rank=32`;
- `epsilon=0.5`;
- raw kernel;
- scaling normalization `none`.

P01 passes only if both seed batches pass the aggregate hard-veto screen and
paired thresholds.

## P02 One-Seed High-N Ladder

Run only if P01 passes.

Rows:

- `N=2048`, seed `82920`;
- `N=4096`, seed `82920`;
- `N=8192`, seed `82920`, only if `N=4096` passes and runtime remains
  reasonable.

Each row uses `T=20`, `rank=32`, `epsilon=0.5`, raw kernel, and scaling
normalization `none`.

Runtime stop: if a row takes more than 15 minutes, stop the ladder and classify
the runbook as blocked by runtime envelope rather than continuing automatically.

## Common Command Template

Replace `<SEEDS>`, `<N>`, `<PHASE_ID>`, `<OUTPUT_JSON>`, `<OUTPUT_MD>`,
`<GPU_ID>`, and `<GPU_NOTE>`.

```bash
python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py \
  --route both \
  --batch-seeds <SEEDS> \
  --time-steps 20 \
  --num-particles <N> \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --annealed-scaling 0.9 \
  --annealed-convergence-threshold 0.001 \
  --row-chunk-size 1024 \
  --col-chunk-size 1024 \
  --particle-chunk-size 1024 \
  --nystrom-diagnostics \
  --nystrom-rank 32 \
  --nystrom-epsilon 0.5 \
  --nystrom-max-iterations 160 \
  --nystrom-convergence-threshold 0.0001 \
  --nystrom-kernel-mode raw \
  --nystrom-scaling-normalization none \
  --history-mode value-only \
  --warmups 0 \
  --repeats 1 \
  --dtype float32 \
  --tf32-mode enabled \
  --jit-compile \
  --device-scope visible \
  --cuda-visible-devices <GPU_ID> \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --selected-physical-gpu <GPU_ID> \
  --gpu-selection-note "<GPU_NOTE>" \
  --phase-id <PHASE_ID> \
  --quiet \
  --output <OUTPUT_JSON> \
  --markdown-output <OUTPUT_MD>
```

## Stop Conditions

Stop and write a result if:

- trusted GPU is unavailable;
- any launched artifact is missing or invalid;
- any row hard-vetoes;
- fixed-policy metadata is missing;
- thresholds drift;
- a row exceeds the runtime stop limit;
- continuing would require tuning or changing the fixed policy.

## Nonclaims

- No default readiness.
- No superiority or ranking.
- No broad rank/epsilon robustness.
- No posterior correctness.
- No HMC readiness.
