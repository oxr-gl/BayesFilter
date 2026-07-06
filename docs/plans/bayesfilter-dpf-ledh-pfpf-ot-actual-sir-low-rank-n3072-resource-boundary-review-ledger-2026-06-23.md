# Actual-SIR Low-Rank N3072 Resource-Boundary Review Ledger

Date: 2026-06-23

Status: `SUBPLAN_REVIEW_CONVERGED`

## Round 1

Reviewer: Claude Opus/max, read-only.

Scope:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-resource-boundary-closeout-subplan-2026-06-23.md`
- `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json`

Verdict: `VERDICT: REVISE`

Material findings:

- The aggregate JSON records `plan_path` as the broader tuning master program,
  while the result recorded only the dedicated N3072 subplan as the plan file.
  Provenance hierarchy needed to be explicit.
- The result/subplan used the `selected_physical_gpu.memory_used_mib = 30693`
  field to support resource-boundary caution without clarifying memory
  provenance semantics.

Patch:

- Result now records both:
  - aggregate `plan_path`:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-master-program-2026-06-22.md`
  - governing phase subplan:
    `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-subplan-2026-06-23.md`
- Result explains that the grid runner does not accept a per-phase subplan path
  argument.
- Result/subplan now treat the memory-used field as an explanatory
  `nvidia-smi`-derived selected-physical-GPU snapshot, not as formal
  memory-scaling evidence or sole boundary rationale.
- Trusted post-review `nvidia-smi` check:
  `nvidia-smi --query-gpu=index,name,uuid,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits`
  reported `32760` MiB total memory for both local devices with the named GPU
  class, so the recorded `30693` MiB value is locally plausible on this host.

Focused checks after patch:

- `n3072-boundary-focused-patch-check`
  - Result: pass after wording patch.
- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `18 passed`.

## Round 2

Reviewer: Claude Opus/max, read-only focused review.

Scope:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-resource-boundary-closeout-subplan-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-resource-boundary-review-ledger-2026-06-23.md`
- `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json`

Verdict: `VERDICT: AGREE`

Reviewer summary:

- The aggregate `plan_path` versus governing phase-subplan ambiguity is fixed
  in the writeup layer. The result records both the broader master-program
  aggregate `plan_path` and the governing N3072 phase subplan, and the closeout
  subplan includes this hierarchy as a required check and stop condition.
- The `selected_physical_gpu.memory_used_mib = 30693` issue is fixed. The
  result demotes it to an explanatory `nvidia-smi` snapshot and states that it
  is not formal memory-scaling evidence or the sole basis for the boundary
  handoff. The closeout subplan repeats the same limitation.
- Boundary safety still holds. The result and subplan keep the boundary narrow
  and do not authorize N3072 two-candidate validation, N4096, or larger runtime
  without a new reviewed subplan and explicit stop conditions.
- No new prohibited claim was found in the named paths.

## Final Review State

The N3072 resource-boundary closeout subplan is reviewed and ready for local
artifact-analysis execution. It does not authorize further GPU runtime.
