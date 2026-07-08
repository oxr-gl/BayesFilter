# Low-Rank LEDH/PFPF-OT Filter Integration Scale Result

Timestamp: 2026-06-20T16:53:47+08:00

Status: `LOW_RANK_FILTER_INTEGRATION_SCALE_PASSED_DIAGNOSTIC_ONLY`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | The low-rank solver-route integration lane passed the governed diagnostic program. |
| Primary criterion status | Passed: active rows proved route execution and passed fixed hard diagnostics. |
| Veto diagnostic status | No hard vetoes in P01, P02, P03, or P04 artifacts. |
| Main uncertainty | Diagnostic harness viability does not establish posterior correctness, default readiness, HMC readiness, dense Sinkhorn equivalence, or speedup. |
| Next justified action | Coordinator may compare lane closeouts separately; this lane should stop without mid-lane synthesis. |
| What is not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or TF32-help. |

## Evidence Summary

| Phase | Artifact | Status | Route execution evidence | Hard vetoes |
| --- | --- | --- | --- | --- |
| P01 | `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-small-2026-06-20.json` | `PASS` | invocations `2`, active count `2` | `[]` |
| P02 | `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-tuning-cpu-2026-06-20.json` | `PASS` | selected invocations `2`, active count `2` | `[]` |
| P03 | `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-medium-cpu-2026-06-20.json` | `PASS` | N=4096 and N=8192 invocations `2`, active count `2` | `[]` |
| P04 | `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-gpu-scale-2026-06-20.json` | `PASS` | N=50000 and N=100000 invocations `1`, active count `1` | `[]` |

## Selected Setting

The P02 predeclared selector chose:

- `rank=16`
- `assignment_epsilon=0.015625`

This is a viable diagnostic setting under the current harness, not a ranking or
speed claim.

## Run Manifest

| Field | Value |
| --- | --- |
| Plan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-master-program-2026-06-20.md` |
| Harness | `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py` |
| Tests | `tests/test_low_rank_ledh_pfpf_integration_smoke.py` |
| P01 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p01-harness-result-2026-06-20.md` |
| P02 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p02-tuning-result-2026-06-20.md` |
| P03 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p03-medium-cpu-result-2026-06-20.md` |
| P04 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p04-trusted-gpu-scale-result-2026-06-20.md` |
| Claude review ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-claude-review-ledger-2026-06-20.md` |
| CPU policy | CPU phases used `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import. |
| GPU policy | P04 ran in trusted/elevated context and recorded visible GPUs. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for this diagnostic harness. |
| Statistically supported ranking | Not attempted; no ranking supported. |
| Descriptive-only differences | Runtime, memory, ESS, TF32, and residual magnitudes are descriptive/explanatory only beyond hard thresholds. |
| Default-readiness | Not established. |
| Next evidence needed | Separate coordinator-level synthesis and, if desired, downstream correctness/posterior validation plans. |

## Post-Run Red-Team Note

The strongest alternative explanation is that the diagnostic fixture is too
regular or too short to expose failures that would appear in broader
LEDH/PFPF-OT filtering workloads.  This result says the low-rank route survived
the governed integration harness at the tested scales; it does not prove
posterior correctness, general scalability, or default readiness.

## Stop Condition

This independent lane is complete.  Do not perform mid-lane synthesis with the
positive-feature lane.
