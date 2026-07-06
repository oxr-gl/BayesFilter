# Final Result: LEDH-PFPF-OT Default Impact Test

Date: 2026-06-20

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | The promoted GPU-oriented LEDH-PFPF-OT TF32 default remains operationally viable through this staged LEDH filter ladder. |
| Primary criterion status | Passed: P00-P05 hard screens passed, required artifacts exist, JSON consistency passed, and final synthesis preserves evidence boundaries. |
| Veto diagnostic status | No ladder veto fired: CPU correctness, trusted GPU precision, target-shape trusted GPU execution, performance/memory interpretation, and tiny CPU-hidden HMC mechanics hard screens all passed. |
| Main uncertainty | The ladder is still engineering evidence, not posterior/scientific validation; target-shape evidence is one synthetic GPU smoke and HMC evidence is tiny CPU-hidden `float64`/TF32-disabled mechanics only. |
| Next justified action | Keep the owner-directed GPU TF32 default as the engineering default for follow-on validation, and plan the next validation rung separately if posterior/HMC/scientific claims are needed. |
| What is not concluded | No posterior correctness, no HMC readiness, no sampler convergence, no statistical superiority, no speedup, no dense Sinkhorn equivalence, no public API readiness, no target-shape HMC viability, and no low-rank lane rejection. |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed across P01-P05 under their phase-local contracts. |
| Statistically supported ranking | None. |
| Descriptive-only differences | P02 drift magnitudes, P03/P04 timing and memory values, and P05 acceptance/log-accept/target-log-prob traces are descriptive only unless explicitly used as hard finiteness screens. |
| Default-readiness | Operational engineering viability is supported for this ladder; scientific/default-policy proof beyond the owner directive is not established. |
| Next evidence needed | A separate reviewed validation plan for any posterior correctness, HMC readiness, target-shape HMC, speedup, or public API claim. |

## Phase Outcomes

| Phase | Outcome | Evidence role |
| --- | --- | --- |
| P00 governance/runbook | Passed after Claude review loop. | Established gated execution and repair-loop discipline. |
| P01 CPU-hidden correctness | Passed. | Removed small deterministic correctness/CPU-placement veto only. |
| P02 trusted GPU precision | Passed. | Removed tiny-fixture trusted GPU placement and gross TF32 drift veto. Largest TF32-enabled max-relative drift was `3.580009806270103e-05`, below the predeclared `1.0e-2` sanity bound. |
| P03 target-shape trusted GPU smoke | Passed. | Demonstrated finite trusted-GPU execution at `B=1,T=120,N=5000,D=50,M=50` with production-default TF32 metadata and streaming/no-dense-storage metadata. |
| P04 performance/memory interpretation | Passed. | Found no blocker in available runtime/memory metadata; did not rank speed or scalability. |
| P05 tiny HMC mechanics | Passed. | Removed tiny CPU-hidden HMC-facing value/score finiteness veto only; not GPU/TF32 HMC evidence. |

## Key Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-master-program-2026-06-20.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-gated-execution-runbook-2026-06-20.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-execution-ledger-2026-06-20.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-claude-review-ledger-2026-06-20.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-stop-handoff-2026-06-20.md`
- Benchmark artifacts:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.json`,
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json`,
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.json`,
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.json`

## Checks Actually Run In P06

```bash
python -c "import pathlib; paths=['docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p00-governance-result-2026-06-20.md','docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p01-correctness-result-2026-06-20.md','docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p02-precision-gpu-result-2026-06-20.md','docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p03-target-gpu-result-2026-06-20.md','docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p04-performance-memory-result-2026-06-20.md','docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-result-2026-06-20.md']; missing=[p for p in paths if not pathlib.Path(p).is_file()]; assert not missing, missing"
```

```bash
python -c "import json, pathlib; p01=json.load(open('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.json')); p02=json.load(open('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json')); p03=json.load(open('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.json')); p05=json.load(open('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.json')); assert p01['overall_passed'] is True; assert p02['overall_passed'] is True; assert p02['device']=='/GPU:0' and p02['expect_device_kind']=='gpu'; tf32=[c for c in p02['comparisons'] if c['arm_id']=='fp32_tf32_enabled'][0]; assert tf32['finite_output'] is True; assert tf32['precision']['precision_default_policy']=='production_ledh_pfpf_ot_gpu_tf32'; assert tf32['precision']['tf32_mode']=='enabled'; assert p03['finite_output'] is True; assert p03['precision']['precision_default_policy']=='production_ledh_pfpf_ot_gpu_tf32'; assert p03['precision']['tf32_mode']=='enabled'; assert p03['transport']['dense_transport_matrix_materialized'] is False; assert p03['stores_full_pre_flow_particles'] is False; assert p03['return_history'] is False; assert p05['overall_passed'] is True; assert p05['hard_veto_status']=='passed'; assert p05['precision']['tf32_mode']=='disabled' and p05['device_scope']=='cpu'"
```

## Answer To "Does It Help The LEDH Filter?"

Yes, in the narrow engineering sense tested here: the promoted GPU TF32 default
kept the LEDH-PFPF-OT route finite, GPU-placed in trusted GPU phases, compatible
with the target-shape synthetic smoke, and free of the staged hard-veto blockers
that would have made it unsuitable for follow-on validation.

The strongest concrete evidence is P03: the production-default TF32 route ran
the `B=1,T=120,N=5000,D=50,M=50` trusted-GPU smoke with finite output and
streaming/no-dense-storage metadata.  P02 supports that the tiny GPU TF32
precision screen did not show gross drift.  P05 adds only a separate tiny
CPU-hidden HMC-facing mechanics sanity check; it is not evidence that GPU/TF32
HMC works.

## Boundaries And Nonclaims

- no posterior correctness;
- no HMC readiness;
- no sampler convergence;
- no statistical superiority;
- no speedup;
- no dense Sinkhorn equivalence;
- no public API readiness;
- no target-shape HMC viability;
- no low-rank lane rejection.

Runtime and memory values are descriptive only.  Acceptance rate in P05 is
descriptive only.  P05 native divergence telemetry was not exposed by the TFP HMC
trace, which is an availability note, not zero divergences.

## Post-Run Red-Team Note

Strongest alternative explanation: the target-shape synthetic smoke and tiny HMC
mechanics fixture may not stress the future LEDH workload that matters for
posterior/scientific validation.

What would overturn this result: reproducing a phase artifact failure under the
same contracts, discovering stale or mismatched artifacts, seeing CPU fallback
in trusted GPU phases, or finding that streaming/no-dense-storage metadata was
incorrect.

Weakest part of the evidence: P03 is one synthetic target-shape run and P05 is a
tiny CPU-hidden mechanics screen, so the ladder is a viability screen rather
than a scientific validation.
