# Phase 6 Subplan: Contract E GPU/XLA/TF32 chunked stress ladder

Date: 2026-06-28

Status: `DRAFT_PENDING_PHASE5`

## Phase Objective

Stress the Contract E route under the project-standard LEDH production target:
TensorFlow/TFP, GPU, XLA, TF32, streaming/chunked transport, and exact chunk
sizing where possible.

## Entry Conditions Inherited From Previous Phase

- Earlier phases justify stress testing.
- Contract E implementation route has passed focused correctness diagnostics.
- Chunk policy and particle counts are predeclared.

## Required Artifacts

- GPU preflight manifest.
- Stress ladder JSON/Markdown artifacts.
- Phase 6 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase6-gpu-xla-stress-result-2026-06-28.md`
- Refreshed Phase 7 closeout subplan.

## Required Checks, Tests, And Reviews

- Escalated/trusted `nvidia-smi`.
- Escalated/trusted TensorFlow GPU/XLA probe.
- Material GPU runs with recorded device, dtype, TF32 state, XLA state, chunk
  size, particle count, seeds, wall time, and memory telemetry.
- Bounded Claude review of stress result and Phase 7 subplan.

Predeclared stress envelope:

- device: trusted `/GPU:0`;
- dtype and precision: TensorFlow float32 with TF32 enabled unless Phase 0-5
  recorded a reviewed reason to use an explicit reference arm;
- XLA: material stress functions must be `jit_compile=True` or otherwise record
  an XLA-compiled route; Python loops are forbidden on XLA-critical loops;
- chunks and particle counts: first rung `N=2500, chunk=2500`; second rung
  `N=10000, chunk=2500`; optional exact-boundary confirmation
  `N=10240, chunk=2560` only after the first two rungs pass;
- timing envelope: each material post-compile run must complete within
  45 minutes wall time for the predeclared seed count; compile time is recorded
  separately and explanatory;
- memory envelope: no OOM; if TensorFlow peak memory telemetry is available,
  peak actual bytes must be below 85 percent of the total memory reported by
  `nvidia-smi`; if only allocator reservation is available, memory cannot pass
  the stress gate by itself and must be labeled explanatory;
- all runs must record seeds, chunk divisibility, residual/conditioning
  diagnostics, and whether the run is a correctness gate or timing-only replay.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is Contract E feasible on the GPU/XLA/TF32 streaming route at the scoped particle counts without memory-explosive paths? |
| Baseline/comparator | Phase 2-5 correctness gates are prerequisites.  Old barycentric streaming route timings/memory are explanatory only when available. |
| Primary pass criterion | Predeclared `N=2500, chunk=2500` and `N=10000, chunk=2500` trusted GPU/XLA/TF32 rungs complete with finite outputs, no full-transport autodiff, no XLA-critical Python loop, no conditioning veto, no OOM, and the predeclared timing/memory envelope satisfied. |
| Veto diagnostics | GPU not trusted, XLA not actually used for claimed XLA evidence, Python loops in XLA-critical path, `transport_ad_mode=full`, OOM, nonfinite output, or missing telemetry. |
| Explanatory diagnostics | `nvidia-smi`, TF allocator telemetry, compile time, run time, chunk padding, covariance residuals, condition spectra. |
| Not concluded | No production default change, no HMC readiness, no full scalability certification. |
| Artifact | GPU manifests and Phase 6 result. |

## Forbidden Claims And Actions

- Do not treat TF allocator reservation as actual peak memory without
  qualifying it.
- Do not run untrusted GPU commands and interpret CUDA failures as real driver
  failures.
- Do not use particle counts or chunks that silently violate the exact-chunk
  policy unless the artifact records the reason.

## Exact Next-Phase Handoff Conditions

Advance to Phase 7 only if:

- stress results are recorded with manifest fields;
- failures are classified rather than hidden;
- Phase 6 primary stress gates pass, or a reviewed repair closes Phase 6 as
  passed after focused reruns;
- final closeout can audit code, math, and artifact claims.

If the stress ladder fails and is not repaired inside Phase 6, classify the
failure in the Phase 6 result and stop rather than advancing to Phase 7.

## Stop Conditions

Stop on trusted GPU unavailability, OOM without a smaller discriminating
fallback, hidden full autodiff, or nonconvergent Claude review.

## End-Of-Phase Protocol

Run checks, write result, refresh Phase 7, review Phase 7, repair findings, and
advance or stop.
