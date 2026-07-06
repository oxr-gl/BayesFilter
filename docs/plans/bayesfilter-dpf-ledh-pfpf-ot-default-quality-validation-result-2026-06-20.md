# Final Result: Default Quality Validation

Date: 2026-06-20

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | The promoted GPU TF32 streaming LEDH-PFPF-OT default passed this medium paired downstream filter-quality validation rung. |
| Primary criterion status | Passed: P00-P03 gates completed; P02 preserved three paired seeds and per-seed/per-output drift records; default-arm drift stayed below `1.0e-2` for all required outputs. |
| Veto diagnostic status | No hard veto fired: child wrappers, finite outputs, output arrays, GPU placement, metadata assertions, paired seed checks, and tolerance screens all passed. |
| Main uncertainty | This is a medium synthetic LGSSM-shaped engineering screen, not posterior/scientific validation or HMC readiness. |
| Next justified action | Plan a separate target-shape repeated stability rung if stronger LEDH filter evidence is needed. A draft is written but not launched. |
| What is not concluded | No posterior correctness, no HMC readiness, no sampler convergence, no speedup, no statistical superiority, no dense Sinkhorn equivalence, no public API readiness, and no target-shape scientific validity. |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the reviewed medium trusted-GPU paired quality rung. |
| Statistically supported ranking | None. |
| Descriptive-only differences | FP32-no-TF32 drift, TF32-vs-no-TF32 extra drift, runtime, memory, compile time, and warm-call timing. |
| Default-readiness | Supports continued use of the owner-directed GPU TF32 default for follow-on validation. |
| Next evidence needed | A reviewed target-shape repeated stability screen, then separate posterior/HMC-specific plans if those claims are needed. |

## Comparator And Tolerance

| Field | Value |
| --- | --- |
| Comparator | Paired FP64 TF32-disabled streaming arm on the same seed, shape, transport settings, and GPU device. |
| Default arm | `fp32_tf32_enabled`. |
| Drift formula | `max(abs(candidate - reference) / max(1.0, abs(reference)))` per output array and paired seed. |
| Tolerance | `1.0e-2`, gross engineering sanity screen only. |
| Required outputs | `log_likelihood`, `filtered_means`, `filtered_variances`, `ess_by_time`. |

## Phase Outcomes

| Phase | Outcome |
| --- | --- |
| P00 governance/review | Passed after Claude round 1 `REVISE`, visible plan patch, and Claude round 2 `AGREE`. |
| P01 harness | Passed compile/help/static checks. |
| P02 medium GPU quality | Passed trusted GPU paired quality screen. |
| P03 closeout | Passed final artifact consistency checks and wrote next-rung draft. |

## P02 Key Result

| Output | Worst seed | Worst default-arm max-relative drift | Tolerance |
| --- | ---: | ---: | ---: |
| `log_likelihood` | `20261629` | `0.0001302131797900768` | `0.01` |
| `filtered_means` | `20260620` | `4.222283782952252e-05` | `0.01` |
| `filtered_variances` | `20261629` | `3.3208038858826812e-06` | `0.01` |
| `ess_by_time` | `20261629` | `4.772058632153245e-06` | `0.01` |

Worst overall drift was `0.0001302131797900768`, below the predeclared
`0.01` screen.

## Key Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-master-program-2026-06-20.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-claude-review-ledger-2026-06-20.md`
- P01 wrapper:
  `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py`
- P02 parent JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.json`
- P02 parent Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.md`
- P02 child directory:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-children-2026-06-20/`
- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p02-medium-gpu-result-2026-06-20.md`
- Next-rung draft:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-next-target-shape-repeated-stability-subplan-2026-06-20.md`

## GPU Selection For Next Runs

Future GPU scalability/efficiency runs should run trusted `nvidia-smi` first,
prefer GPU1 if it is not busy, and use GPU0 only if GPU1 is busy or otherwise
unsuitable. The chosen GPU and reason must be recorded in the run manifest.

## Answer To "Does It Help The LEDH Filter?"

Yes, in the bounded engineering sense tested here: the GPU TF32 streaming
default preserved downstream LEDH filter outputs within the predeclared
medium-screen tolerance against paired FP64 arms on trusted GPU.

This is stronger than the previous operational smoke ladder because it checks
paired downstream outputs over three seeds. It is not yet target-shape repeated
stability, posterior correctness, or HMC readiness.

## Post-Run Red-Team Note

Strongest alternative explanation: a target-shape workload may expose numerical,
memory, or stability issues not present in this medium synthetic screen.

What would overturn this result: reproducing the same P02 contract with CPU
fallback, nonfinite output, missing arrays, metadata mismatch, lost paired seed
records, or default-arm drift above `0.01`.

Weakest part of the evidence: the comparator is a same-route FP64 arm, not an
exact posterior oracle, and the tolerance is an engineering sanity threshold.
