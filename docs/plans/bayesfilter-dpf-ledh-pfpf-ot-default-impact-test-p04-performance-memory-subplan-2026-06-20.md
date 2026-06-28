# P04 Subplan: Performance And Memory Interpretation

Date: 2026-06-20

## Phase Objective

Interpret P02/P03 runtime, memory, storage, and historical-context diagnostics
without running new numerical experiments or turning descriptive timing into a
speedup claim.  The phase should decide whether the existing evidence supports
continuing to P05 tiny HMC mechanics, stopping for a performance/memory blocker,
or requiring a narrower repair/measurement plan.

## Entry Conditions Inherited From Previous Phase

- P00 governance gate passed.
- P01 CPU-hidden correctness gate passed.
- P02 trusted-GPU precision drift screen passed.
- P03 target-shape trusted GPU smoke passed at
  `B=1,T=120,N=5000,state_dim=50,obs_dim=50`.
- P04 has no authority to run new GPU benchmarks unless a separate reviewed
  repair subplan is written first.
- Peer low-rank artifacts and unrelated HMC dirty files remain out of scope.

## Required Artifacts

- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p04-performance-memory-result-2026-06-20.md`
- P05 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-subplan-2026-06-20.md`

## Required Checks, Tests, And Reviews

- Artifact existence and schema check:
  `python -c "import json, math, pathlib; paths=['docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json','docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.json','docs/benchmarks/experimental-batched-ledh-pfpf-ot-tf32-capacity-gpu0-b1-t120-np5000-d50-m50-activeall-callback-2026-06-15.json']; data=[]; [data.append(json.load(open(pathlib.Path(p)))) for p in paths]; assert data[0]['overall_passed'] is True; assert data[1]['finite_output'] is True; assert data[2]['finite_output'] is True; assert data[1]['shape']==data[2]['shape']; assert data[1]['transport']['dense_transport_matrix_materialized'] is False; assert data[1]['stores_full_pre_flow_particles'] is False; assert data[1]['return_history'] is False; assert data[1]['precision']['precision_default_policy']=='production_ledh_pfpf_ot_gpu_tf32'; assert all(math.isfinite(float(data[i]['compile_and_first_call_seconds'])) for i in [1,2]); assert all(data[i]['warm_call_timing_summary_seconds'] and all(math.isfinite(float(v)) for v in data[i]['warm_call_timing_summary_seconds'].values()) for i in [1,2]); assert all(isinstance(data[i]['gpu_memory_info_before'], dict) and isinstance(data[i]['gpu_memory_info_after'], dict) for i in [1,2]); assert all(k in data[1]['gpu_memory_info_after'] for k in ['current','peak']); assert all(k in data[2]['gpu_memory_info_after'] for k in ['current','peak'])"`
- Local review of P04 result for:
  consistency, correctness, artifact coverage, boundary safety, and statistical
  humility.
- Draft P05 subplan and review it locally for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.
- Claude Opus max-effort read-only review is required for P04 before P05
  execution because P04 interprets evidence and drafts an HMC-mechanics phase.
  Claude is not an execution authority.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the P02/P03 diagnostics show any performance, memory, metadata, or storage blocker that should stop the LEDH default impact ladder before tiny HMC mechanics? |
| Baseline/comparator | P03 production-default target-shape artifact is primary; P02 precision artifact and the 2026-06-15 same-shape experimental-metadata capacity artifact are historical/contextual diagnostics only. |
| Primary pass criterion | Required artifacts exist and schemas expose the timing/memory fields needed for interpretation; P04 result separates hard vetoes from descriptive diagnostics; no performance/memory blocker is identified that invalidates continuing to P05; P05 subplan is drafted with HMC nonclaims and review gate. |
| Veto diagnostics | Missing/malformed required artifact, missing timing/memory fields needed for P04 interpretation, P03 contradiction on finite/GPU/default/storage metadata, treating timing as speedup/ranking evidence, or drafting P05 without explicit HMC nonclaims and Claude-review-before-execution condition. |
| Explanatory diagnostics | P02 drift/timing, P03 compile and warm-call seconds, P03 GPU memory info, historical same-shape timing/memory, and nonclaim consistency. |
| Not concluded | No speedup, no statistical ranking, no posterior correctness, no HMC readiness, no broad memory sufficiency, no dense Sinkhorn equivalence, and no public API readiness. |
| Artifact | P04 result note, P05 subplan, execution ledger, and Claude review ledger. |

## Forbidden Claims/Actions

- Do not run new GPU experiments in P04.
- Do not claim speedup or performance superiority from one-run descriptive
  timings.
- Do not claim broad scalability or memory sufficiency from one target-shape
  smoke.
- Do not claim posterior correctness or HMC readiness.
- Do not edit algorithm code.
- Do not touch peer low-rank files or unrelated HMC dirty files.
- Do not let Claude edit, execute, launch workers, or authorize phase crossing.

## Exact Next-Phase Handoff Conditions

Proceed to P05 only if:

- artifact/schema check passes;
- P04 result exists and preserves evidence classes, interpretation, and
  nonclaims;
- P04 result states whether any hard performance/memory blocker exists;
- P05 subplan exists, includes its evidence contract and stop conditions, and
  states that P05 cannot execute until Claude read-only review converges;
- local and Claude read-only review converge for P04/P05 handoff.

## Stop Conditions

- Required P02/P03/historical artifact is missing or malformed.
- P03 artifact contradicts finite/GPU/default/storage metadata required for
  target-shape viability.
- Interpretation would require a new speedup/ranking claim without uncertainty
  evidence.
- P05 cannot be drafted without crossing HMC-readiness or scientific-claim
  boundaries.
- Any action would cross human, runtime, model-file, funding,
  product-capability, default-policy, or scientific-claim boundaries.
