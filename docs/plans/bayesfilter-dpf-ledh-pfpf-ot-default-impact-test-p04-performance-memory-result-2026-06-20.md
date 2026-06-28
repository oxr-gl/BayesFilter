# P04 Result: Performance And Memory Interpretation

Date: 2026-06-20

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | P04 passed; no performance/memory blocker stops the ladder before P05. |
| Primary criterion status | Passed: artifact/schema check passed, P04 preserved evidence classes, and P05 subplan was drafted with HMC nonclaims and review gate. |
| Veto diagnostic status | No P04 veto fired. Required timing/memory fields were present, P03 finite/GPU/default/storage metadata remained coherent, and no speedup/ranking claim was made. |
| Main uncertainty | P04 can detect blocker-worthy contradictions, but cannot justify comparative performance or memory superiority from one-run descriptive artifacts. |
| Next justified action | Review P05 tiny HMC mechanics subplan before execution. |
| What is not concluded | No speedup, no statistical ranking, no posterior correctness, no HMC readiness, no broad memory sufficiency, no dense Sinkhorn equivalence, and no public API readiness. |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed: no artifact/schema, metadata, or storage contradiction blocked continuing to P05. |
| Statistically supported ranking | None. |
| Descriptive-only differences | P02/P03 timing, drift, and memory metadata remain descriptive only. |
| Default-readiness | Owner-directed default remains operational through P03, but not scientifically/default validated by P04. |
| Next evidence needed | P05 tiny HMC mechanics hard-veto screen. |

## Command Actually Run

```bash
python -c "import json, math, pathlib; paths=['docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json','docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.json','docs/benchmarks/experimental-batched-ledh-pfpf-ot-tf32-capacity-gpu0-b1-t120-np5000-d50-m50-activeall-callback-2026-06-15.json']; data=[]; [data.append(json.load(open(pathlib.Path(p)))) for p in paths]; assert data[0]['overall_passed'] is True; assert data[1]['finite_output'] is True; assert data[2]['finite_output'] is True; assert data[1]['shape']==data[2]['shape']; assert data[1]['transport']['dense_transport_matrix_materialized'] is False; assert data[1]['stores_full_pre_flow_particles'] is False; assert data[1]['return_history'] is False; assert data[1]['precision']['precision_default_policy']=='production_ledh_pfpf_ot_gpu_tf32'; assert all(math.isfinite(float(data[i]['compile_and_first_call_seconds'])) for i in [1,2]); assert all(data[i]['warm_call_timing_summary_seconds'] and all(math.isfinite(float(v)) for v in data[i]['warm_call_timing_summary_seconds'].values()) for i in [1,2]); assert all(isinstance(data[i]['gpu_memory_info_before'], dict) and isinstance(data[i]['gpu_memory_info_after'], dict) for i in [1,2]); assert all(k in data[1]['gpu_memory_info_after'] for k in ['current','peak']); assert all(k in data[2]['gpu_memory_info_after'] for k in ['current','peak'])"
```

## Artifacts Interpreted

- P02 precision screen:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json`
- P03 target-shape smoke:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.json`
- Historical same-shape context:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-tf32-capacity-gpu0-b1-t120-np5000-d50-m50-activeall-callback-2026-06-15.json`
- Next subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-subplan-2026-06-20.md`

## Descriptive Diagnostics

| Artifact | Compile plus first call seconds | Warm-call median seconds | GPU peak bytes | Interpretation role |
| --- | ---: | ---: | ---: | --- |
| P03 production-default target-shape smoke | `112.19805304496549` | `98.53211762499996` | `73400320` | Primary descriptive target-shape runtime/memory context |
| 2026-06-15 historical same-shape artifact | `94.80793855385855` | `86.96749837393872` | `73400320` | Historical context only, not a speed comparator |

P02’s largest TF32-enabled max-relative drift was
`3.580009806270103e-05`, below its predeclared `1.0e-2` tiny-fixture sanity
bound.  That remains precision-screen context only.

## Interpretation

No performance/memory blocker was identified that invalidates continuing to P05.
The P03 target-shape run completed before timeout, recorded finite GPU output,
and preserved streaming/no-dense-storage metadata.  The historical same-shape
artifact had similar memory metadata but older experimental policy metadata, so
it is not used for a speedup or regression claim.

The P03 warm-call time around `98.5` seconds is operationally significant for
future benchmark planning, but under this evidence contract it is descriptive
only.  It does not veto P05 because P05 is a separate tiny HMC mechanics screen,
not a target-shape HMC run.

## Post-Run Red-Team Note

Strongest alternative explanation: P03 target-shape runtime may be too slow for
some future use cases even though it is not a blocker for the P05 tiny mechanics
screen.

What would overturn this result: discovering that P03 timing/memory fields were
malformed, that P03 did not actually use production-default metadata, or that
the target-shape smoke materialized dense/full-history storage despite the
recorded metadata.

Weakest part of the evidence: performance interpretation is based on one run
and therefore cannot rank or certify runtime behavior.
