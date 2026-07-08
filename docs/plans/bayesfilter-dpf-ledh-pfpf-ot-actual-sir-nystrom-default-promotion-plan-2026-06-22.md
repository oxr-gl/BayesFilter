# Actual-SIR Nystrom Default-Promotion Test Plan

Date: 2026-06-22

Status: `PILOT_PLAN_READY`

## Purpose

Test the fixed-rank Nystrom LEDH/PFPF-OT route on the serious actual-SIR d18
model that the other agent is also testing.  This lane intentionally reuses the
existing P8j actual-SIR tensor/callback setup and the low-rank actual-SIR
validation thresholds, but writes separate Nystrom artifacts so it does not
collide with the other agent's low-rank tuning lane.

This is not a default switch.  It is the next serious model gate needed before
Nystrom can be considered for default-promotion testing.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can the Nystrom route pass actual-SIR d18 validity and paired comparability against the streaming TF32 route on the same serious SIR workload? |
| Candidate | Fixed-rank Nystrom kernel transport in the LEDH/PFPF-OT route. |
| Comparator | Existing streaming TF32 actual-SIR route from `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`. |
| Serious model | `zhao_cui_spatial_sir_austria_j9_T20`, `D=18`, `M=9`, actual callback/tensor setup from P8j. |
| Expected failure mode | Nystrom may pass LGSSM but fail actual-SIR log-likelihood/filter comparability, residuals, route-fired evidence, runtime, or GPU provenance. |
| Primary pilot criterion | Tiny CPU SIR smoke passes for both routes, then a GPU SIR paired pilot passes hard validity and paired comparability gates at the predeclared shape. |
| Default-promotion criterion | Not in this pilot. Later default promotion would require replicated actual-SIR, synthetic, stress, and gradient/HMC gates plus uncertainty-supported resource evidence. |
| Promotion veto | Nonfinite outputs; actual-SIR semantics missing; route invocation mismatch; materialized dense transport in scalable route; Nystrom residual above threshold; log-weight normalization failure; ESS floor failure; paired actual-SIR comparability failure; GPU/TF32 mismatch; mixed physical GPU. |
| Continuation veto | Neither GPU1 nor GPU0 is usable in trusted context; tiny actual-SIR smoke cannot run both routes; implementation would require changing public/default BayesFilter behavior; package/network dependency required. |
| Repair trigger | Harness schema bug, route not firing, missing diagnostics, dtype propagation mismatch, or GPU1 busy causing pre-run GPU0 fallback with manifest note. |
| Explanatory diagnostics | Runtime, warm-call median, memory, row/column residual magnitudes, ESS, log-likelihood deltas, filtered summary deltas, rank and landmarks. |
| What must not be concluded | No default readiness, no posterior correctness, no HMC readiness, no public API readiness, no statistical ranking, no broad scalable-OT selection, and no dense Sinkhorn equivalence claim. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering/scientific question | Is Nystrom viable on the actual-SIR d18 model against the current streaming TF32 route? |
| Exact baseline | Streaming TF32 actual-SIR route using the same P8j callbacks, seeds, observations, dtype, GPU, and fixed resampling mask. |
| Primary pass/fail criterion | Both routes pass hard validity gates and paired comparability passes on all required pilot rows. |
| Hard-veto diagnostics | Finite outputs; actual-SIR semantics; route-fired count; sentinel transport shapes; Nystrom residual `<= 5e-2`; final log-sum-exp residual `<= 1e-5`; ESS fraction `>= 0.01`; expected GPU output in GPU mode; TF32 recorded true in GPU TF32 mode. |
| Paired-comparability vetoes | Log-likelihood max absolute delta `<= 10.0`, mean absolute delta `<= 5.0`; filtered mean relative L2 `<= 0.20` or RMS `<= 2.5`; filtered variance relative L2 `<= 0.75` or RMS `<= 25.0`; final particle mean relative L2 `<= 0.20` or absolute L2 `<= 25.0`. |
| Explanatory-only diagnostics | Runtime, memory, warm-time ratios, residual values below thresholds, ESS above threshold, landmarks, and previews. |
| Not concluded on pass | Default readiness, statistical superiority, posterior correctness, HMC readiness, or production/API readiness. |
| Artifacts | `docs/benchmarks/actual-sir-nystrom-default-promotion-*.json`, matching Markdown, and this plan/result prefix. |

## Pilot Shape

| Phase | Shape | Role |
| --- | --- | --- |
| P01 tiny smoke | `B=1,T=1,N=8,rank=4`, CPU, TF32 disabled | Harness correctness and actual-SIR callback contract. |
| P02 GPU pilot | `B=1,T=3,N=128,rank=32`, GPU TF32, active-all transport | First serious SIR route-comparability screen. |
| P03 serious row | `B=5,T=20,N=1024,rank=32 or 64`, GPU TF32 | Only after P02 passes; this is the first default-promotion-relevant SIR row. |

## GPU Selection Rule

Use trusted/elevated GPU context. Prefer physical GPU1 by setting
`CUDA_VISIBLE_DEVICES=1`; use physical GPU0 only if GPU1 is busy, unavailable,
or unsuitable. Record the selected physical GPU and fallback reason. All paired
rows in one artifact must run under one selected physical GPU.

## Skeptical Plan Audit

Pre-execution audit status: `PASSED_FOR_P01_P02`.

The plan uses the real actual-SIR comparator rather than synthetic-only
fixtures, keeps runtime/memory as explanatory until validity and comparability
pass, predeclares stop conditions, avoids default/public API changes, preserves
the other agent's low-rank write set, and writes artifacts that answer only the
actual-SIR viability question.

## Owned Write Set

- `docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py`
- `tests/test_actual_sir_nystrom_default_promotion.py`
- `docs/benchmarks/actual-sir-nystrom-default-promotion-*.json`
- `docs/benchmarks/actual-sir-nystrom-default-promotion-*.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-*.md`

## Forbidden Writes

- Existing low-rank actual-SIR harnesses and result artifacts.
- BayesFilter public exports/defaults/package metadata.
- Shared schemas, unrelated stop handoffs, model files, or dependency locks.
