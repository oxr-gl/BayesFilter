# LEDH-PFPF-OT Large-Particle Efficiency Master Program

Date: 2026-06-21

Status: DRAFT_FOR_REVIEW

## Purpose

This master program answers a narrower and more useful question than the prior
medium-quality screen:

Can the repository-default GPU TF32 streaming LEDH-PFPF-OT route make the
LGSSM-shaped LEDH-PFPF-OT benchmark operational at much larger particle counts
by avoiding dense transport storage, while preserving finite downstream filter
outputs and recording same-route runtime evidence?

This lane is independent of the peer low-rank coupling solver route. This lane
owns only the current positive-feature/streaming production-default LEDH-PFPF-OT
candidate and the large-particle efficiency evidence for that route.

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Does GPU TF32 streaming LEDH-PFPF-OT handle large `N` more efficiently for the LGSSM-shaped LEDH-PFPF-OT benchmark than dense/non-streaming storage-oriented routes, and does TF32 provide same-route runtime benefit evidence? |
| Candidate/mechanism | Current production-default TensorFlow/TensorFlow Probability streaming LEDH-PFPF-OT value route with callback proposal, no dense `[B,N,N]` transport matrix, no full `[B,T,N,D]` pre-flow storage, `return_history=False`, dtype `float32`, TF32 enabled. |
| Expected failure mode | OOM, timeout, CPU fallback, non-finite value/summary outputs, accidental dense transport materialization, accidental full pre-flow tensor storage, stale precision metadata, or misleading runtime comparison. |
| Promotion criterion | The streaming default reaches the predeclared large-particle ladder in trusted GPU context with finite outputs, GPU placement, no dense transport matrix, no full pre-flow storage, `return_history=False`, and complete JSON/Markdown artifacts. |
| Promotion veto | Any required rung fails hard invariants: non-finite output, CPU fallback, OOM/timeout, missing artifact, dense transport matrix materialized, full pre-flow storage, `return_history=True`, wrong production-default precision metadata, unrecorded GPU selection policy violation, or unrelated compute-process contamination on the selected GPU during a timing/memory-sensitive phase. |
| Continuation veto | Broken harness, missing required artifacts, unable to obtain trusted GPU status, repeated Claude/Codex review non-convergence after five rounds for the same blocker, or a human-boundary decision not already authorized. |
| Repair trigger | Failed static harness check, missing metadata, wrapper stdout too large, incorrect GPU-selection record, or Claude/Codex review finding a fixable baseline/claim/artifact mismatch. |
| Explanatory diagnostics | Single-run timing, warm-call median, compile plus first-call time, GPU memory info, dense small-`N` breakpoint context, and TF32-vs-FP32-no-TF32 runtime ratios. |
| Must not conclude | No posterior correctness, no HMC readiness, no sampler convergence, no dense Sinkhorn equivalence, no public API readiness, no statistical superiority, and no final production capacity limit beyond the tested shapes. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the current GPU TF32 streaming LEDH-PFPF-OT route make the LGSSM-shaped large-particle benchmark operational by avoiding dense storage, and is same-route TF32 descriptively faster than FP32-no-TF32 at matched shape? |
| Baseline/comparator | Primary large-`N` route is streaming FP32+TF32 default. Same-route comparator for TF32 effect is streaming FP32 with TF32 disabled. Dense/non-streaming is small-`N` breakpoint/context only, not a required large-`N` comparator. |
| Primary pass/fail criterion | Required streaming ladder rungs pass hard invariants in trusted GPU context and produce complete result artifacts. |
| Veto diagnostics | Non-finite output, CPU fallback, OOM/timeout, missing artifact, dense transport materialization, full pre-flow storage, `return_history=True`, stale/default metadata mismatch, GPU0 use without recording GPU1 busy/unsuitable, or selected-GPU contamination during timing/memory-sensitive runs. |
| Explanatory only | Runtime, compile time, memory metadata, dense small-`N` breakpoint, TF32/FP32 timing ratio, and output preview values. |
| Not concluded even if pass | No posterior correctness, no statistical ranking, no HMC readiness, no dense Sinkhorn equivalence, no public API readiness, and no claim that all future larger `N` will pass. |
| Result preservation | Phase results under `docs/plans`; benchmark JSON/Markdown and child artifacts under `docs/benchmarks`; execution/review ledgers under `docs/plans`. |

## Baseline And Assumption Audit

| Choice | Provenance | Why reasonable | How it could mislead | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Use streaming LGSSM harness as primary implementation target | Current default harness `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py` | It exercises the production-default streaming LEDH-PFPF-OT value route and records storage/device/precision metadata. | Synthetic LGSSM-shaped fixture is not posterior-validity or full-filter-readiness evidence. | Static harness audit and hard artifact checks. | Required |
| Use dense only at small `N` | Dense route materializes `[B,N,N]` transport and older pre-flow tensor surface. | Large dense runs would mostly answer OOM and storage pressure, not the current route's large-`N` viability. | Dense small-`N` timing could be misread as large-`N` ranking. | Mark dense as contextual only in plan/result. | Required |
| Prefer GPU1 unless busy, then GPU0 | User directive on 2026-06-21. | Keeps agent coordination predictable and reduces conflict with GPU0. | GPU0 could be used silently if wrapper only sees logical GPU0. | Trusted `nvidia-smi`; GPU1 is busy if total memory used is at least 2048 MiB, utilization is at least 20%, or any single non-display compute process uses at least 2048 MiB. Light compute processes below these thresholds are warnings, not vetoes; wrapper parent artifact records physical GPU and reason; child artifacts record remapped `CUDA_VISIBLE_DEVICES`. | Required |
| Treat runtime as descriptive unless replicated | Scientific coding policy. | Single-rung timing is useful for operational feasibility but not statistical ranking. | Overclaiming speedup from one timing. | Nonclaim table and inference-status table. | Required |

## Runtime Budget And GPU Selection Rules

- P03 phase wall-clock budget: 4 hours.
- P03 per-rung child timeout: 3600 seconds.
- P03 mandatory rungs: `1000`, `5000`, and `10000` particles.
- P03 optional `20000` rung: attempt only if all mandatory rungs pass, elapsed
  P03 time is at most 2 hours, the `10000` child elapsed time is at most 1200
  seconds, and no GPU-memory warning/OOM occurred. Otherwise write a justified
  skip in the P03 result; this is not a failure.
- P04 phase wall-clock budget: 3 hours.
- P04 per-arm child timeout: 3600 seconds.
- P04 preferred matched shape: `10000` particles. If the P03 `10000` child
  elapsed time exceeded 1800 seconds or failed for a non-harness reason, use the
  largest P03-passing rung with child elapsed time at most 1800 seconds and
  record the downgrade.
- GPU1 busy/unsuitable rule: physical GPU1 is preferred unless it is absent,
  has total memory used of at least 2048 MiB, has at least 20% utilization, or
  has any single non-display compute process using at least 2048 MiB. Light
  compute processes below these thresholds are recorded as shared-GPU warnings,
  not vetoes. Use physical GPU0 only if GPU1 is busy/unsuitable by this rule
  and GPU0 is usable by the same thresholds; otherwise stop and ask for
  direction.
- Parent-vs-child GPU metadata: the parent wrapper/result records selected
  physical GPU index, GPU selection reason, and trusted `nvidia-smi` summary.
  Child artifacts record `CUDA_VISIBLE_DEVICES` and logical `/GPU:0` device
  evidence after remapping.
- P03/P04 just-in-time GPU lease rule: P02 selection is not a durable lease.
  Immediately before launching timing/memory-sensitive GPU phases, rerun trusted
  `nvidia-smi`; stop or defer if the selected physical GPU has unrelated
  compute processes. During startup/rungs, if an unrelated process appears on
  the selected GPU, stop only this lane's launched processes, preserve completed
  artifacts as contaminated diagnostic-only evidence, and write a blocker or
  repair result.

## Skeptical Plan Audit

Pre-execution audit result:

- Wrong baseline: avoided. The large-`N` primary route is the current streaming
  default; FP32-no-TF32 is the same-route comparator; dense is explicitly
  small-`N` context only.
- Proxy metrics: guarded. Runtime and memory are explanatory unless a matched
  same-route comparison is present, and even then single-run ratios are
  descriptive only.
- Stop conditions: included in every phase subplan.
- Unfair comparisons: guarded. Dense is not used as a large-`N` ranking
  comparator because it uses a different storage surface.
- Hidden assumptions: GPU selection, callback proposal, no history, no dense
  matrix, and production-default precision metadata are explicit hard checks.
- Stale context: phase 1 re-checks current harness metadata before GPU work.
- Environment mismatch: phase 2 requires trusted `nvidia-smi`; GPU artifacts
  must record physical GPU selection and child logical device mapping.
- Artifact mismatch: each phase names required result artifacts and handoff
  conditions.

Audit status: PASS_FOR_REVIEW. Execution may start only after local plan checks
and Claude read-only review converge.

## Phase Index

| Phase | Name | Subplan | Result artifact |
| --- | --- | --- | --- |
| P00 | Governance and claim lock | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p00-governance-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p00-governance-result-2026-06-21.md` |
| P01 | Harness implementation and static checks | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p01-harness-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p01-harness-result-2026-06-21.md` |
| P02 | Trusted GPU selection preflight | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p02-gpu-selection-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p02-gpu-selection-result-2026-06-21.md` |
| P03 | Streaming large-`N` reach ladder | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-ladder-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-ladder-result-2026-06-21.md` |
| P04 | Same-route TF32-vs-FP32 runtime check | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-runtime-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-runtime-result-2026-06-21.md` |
| P05 | Dense breakpoint context | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-context-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-context-result-2026-06-21.md` |
| P06 | Closeout and decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p06-closeout-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-result-2026-06-21.md` |

## Planned Artifact Names

- Wrapper: `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_large_particle_efficiency.py`
- Wrapper test: `tests/test_experimental_batched_benchmark_harness.py`
- P03 JSON: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-2026-06-21.json`
- P04 JSON: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.json`
- P05 JSON: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-gpu-2026-06-21.json`
- Review ledger: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-claude-review-ledger-2026-06-21.md`
- Execution ledger: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-execution-ledger-2026-06-21.md`
- Stop handoff: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-stop-handoff-2026-06-21.md`

## Repair Loop

For any material issue:

1. Record the blocker in the execution ledger.
2. Patch the same subplan or implementation artifact visibly.
3. Rerun focused local checks.
4. Use Claude only as read-only reviewer for material plan or claim-boundary
   changes.
5. Stop after five Claude review rounds for the same blocker and write a
   blocker result.

Claude cannot authorize human, runtime, model-file, funding,
product-capability, or scientific-claim boundary crossings.
