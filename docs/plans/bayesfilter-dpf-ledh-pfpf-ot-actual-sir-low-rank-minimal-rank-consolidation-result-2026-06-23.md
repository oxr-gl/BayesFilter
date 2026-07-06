# Actual-SIR Low-Rank Minimal-Rank Consolidation Result

Date: 2026-06-23

Status: `MINIMAL_RANK_TIER_SELECTED_FOR_NEXT_VALIDATION`

## Phase Objective

Consolidate the five viable low-rank actual-SIR candidates into a
minimal-rank survivor tier for the next larger-`N` validation phase, using only
hard-veto survival and resource-envelope criteria. This was a document and
artifact analysis phase; no GPU benchmark was run.

## Evidence Contract Result

- Question: among the five candidates that remain viable after independent
  `N=1024` seed replication, which candidates should be carried forward as the
  smallest resource-envelope survivor tier for the next larger-`N` validation?
- Comparator: not a performance comparator. The criterion was hard-veto
  survival plus low-rank rank tier as the implementation resource envelope.
- Source artifacts: exactly the pinned N512 seed-replication, N1024
  paired-validation, and N1024 seed-replication result/aggregate artifacts in
  the subplan's source artifact manifest.
- Result: all source artifacts passed consistency checks, and the smallest
  passing low-rank rank tier is rank `16`.
- Consolidated survivor tier:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- Deferred but still viable candidates:
  - `r32_eps0p25_alpha1em08_it120`
  - `r64_eps0p25_alpha1em08_it120`
  - `r128_eps0p25_alpha1em08_it120`
- Candidate rejection: no candidate was scientifically or statistically
  rejected by this consolidation phase.

## Checks And Runs

- Source manifest check:
  - Result: pass, `minimal-rank-consolidation-source-manifest-check-pass`.
- Boundary/patch consistency checks:
  - Result: pass, `minimal-rank-consolidation-subplan-boundary-check-pass`.
  - Result: pass, `minimal-rank-consolidation-r1-patch-consistency-pass`.
- Syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Claude read-only review:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-minimal-rank-consolidation-review-ledger-2026-06-23.md`
  - Round 1: `VERDICT: REVISE`; fixed exact source-artifact pinning and
    rank-only resource-envelope language.
  - Round 2: `VERDICT: AGREE`.

## Source Artifact Manifest Result

| Source | Result note | Aggregate JSON | Aggregate Markdown | Status |
| --- | --- | --- | --- | --- |
| `n512_seed_replication` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n512-seed-replication-result-2026-06-23.md` | `docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.json` | `docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.md` | `PASS` |
| `n1024_paired_validation` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-paired-validation-result-2026-06-23.md` | `docs/benchmarks/actual-sir-low-rank-n1024-paired-validation-2026-06-23.json` | `docs/benchmarks/actual-sir-low-rank-n1024-paired-validation-2026-06-23.md` | `PASS` |
| `n1024_seed_replication` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-seed-replication-result-2026-06-23.md` | `docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.json` | `docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.md` | `PASS` |

Every source aggregate contained exactly these row ids in order, and every
recorded row JSON, Markdown, and log artifact existed:

1. `r16_eps0p25_alpha1em08_it120`
2. `r16_eps0p125_alpha1em08_it120`
3. `r32_eps0p25_alpha1em08_it120`
4. `r64_eps0p25_alpha1em08_it120`
5. `r128_eps0p25_alpha1em08_it120`

## Consolidation Summary

| Candidate | Rank | Assignment epsilon | Consolidation status | Rationale |
| --- | ---: | ---: | --- | --- |
| `r16_eps0p25_alpha1em08_it120` | 16 | 0.25 | Carry forward | Passed all source gates and belongs to the smallest passing rank tier |
| `r16_eps0p125_alpha1em08_it120` | 16 | 0.125 | Carry forward | Passed all source gates and belongs to the smallest passing rank tier |
| `r32_eps0p25_alpha1em08_it120` | 32 | 0.25 | Deferred viable | Passed all source gates but is outside the smallest passing rank tier |
| `r64_eps0p25_alpha1em08_it120` | 64 | 0.25 | Deferred viable | Passed all source gates but is outside the smallest passing rank tier |
| `r128_eps0p25_alpha1em08_it120` | 128 | 0.25 | Deferred viable | Passed all source gates but is outside the smallest passing rank tier |

Timing, warm ratios, wall times, deltas, and residual magnitudes were not used
to eliminate or rank candidates.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Carry forward the two rank-16 candidates as the minimal-rank survivor tier for the next larger-`N` validation subplan | Passed: all source artifacts and row artifacts matched the manifest, and rank 16 is the smallest passing rank tier | No source artifact, row artifact, hard-veto, comparability, warm-screen, or provenance veto fired | Rank-only consolidation is an engineering resource-envelope choice, not a statistical ranking or scientific-validity result | Draft and review a larger-`N` validation subplan for the two rank-16 candidates | No speedup, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, scientific superiority, production scientific validity, statistical ranking, or invalidity of deferred viable candidates |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Source artifact integrity | Passed for all pinned result notes, aggregate JSON/Markdown artifacts, and recorded row artifacts |
| Hard veto screen | Previously passed for all five candidates in all three source stages; no new hard veto was introduced |
| Rank-only consolidation | Selected rank-16 tier because it is the smallest passing low-rank rank tier |
| Statistically supported ranking | Not established; not attempted |
| Descriptive-only differences | Warm ratios, row wall times, deltas, and residual magnitudes remain explanatory only |
| Deferred candidates | Rank-32/64/128 candidates remain viable but deferred for resource-envelope reasons |
| Default-readiness | Not established; this is not a public API/default promotion gate |
| Next evidence needed | Larger-`N` validation of the rank-16 survivor tier under a reviewed subplan |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Working tree | Dirty before and during the document-only consolidation; unrelated user/generated changes preserved |
| Command | Local Python source-manifest check embedded in the subplan |
| Environment | Repository working directory `/home/ubuntu/python/BayesFilter`; no GPU benchmark executed |
| CPU/GPU status | N/A for execution; this phase was document/artifact analysis only |
| Source artifacts | N512 seed-replication, N1024 paired-validation, and N1024 seed-replication result/aggregate artifacts listed above |
| Wall time | N/A; quick local artifact check |
| Plan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-minimal-rank-consolidation-subplan-2026-06-23.md` |
| Review ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-minimal-rank-consolidation-review-ledger-2026-06-23.md` |
| Result artifact | This file |

## Post-Run Red-Team Note

- Strongest alternative explanation: rank-16 may be the smallest passing
  resource tier in current artifacts but could fail at larger `N`; deferred
  higher-rank candidates might still be useful if the rank-16 tier fails.
- What would overturn advancement: larger-`N` validation showing hard vetoes,
  missing GPU/XLA provenance, failed paired comparability, failed warm screen,
  missing row artifacts, timeout, or an inability to preserve nonclaim
  boundaries.
- Weakest part of the evidence: this phase is not an empirical benchmark and
  contains no new scientific validation. It is a resource-envelope narrowing
  based on already-passed artifacts.

## Next-Phase Handoff

Draft a larger-`N` validation subplan for:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`

The next subplan must state the new particle count, seed batch, GPU/XLA/TF32
contract, row timeout, promotion/veto diagnostics, nonclaims, result artifact
paths, and exact handoff conditions before any GPU execution.

## Forbidden Claims Preserved

This consolidation result does not claim speedup, posterior correctness, HMC
readiness, dense Sinkhorn equivalence, public API/default readiness, broad
scalable-OT superiority, statistical ranking, or production scientific
validity. It does not claim that rank-32/64/128 candidates are worse or invalid.
It also does not authorize NumPy as BayesFilter-owned algorithmic
implementation; the production route remains the GPU/XLA TensorFlow/TFP lane.
