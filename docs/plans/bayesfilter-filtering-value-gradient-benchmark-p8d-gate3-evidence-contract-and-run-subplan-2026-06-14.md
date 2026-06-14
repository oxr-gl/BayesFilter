# P8d Gate 3 Evidence Contract And Run Subplan

Date: 2026-06-14

Status: `CODEX_REVIEWED_READY_FOR_CPU_ONLY_FULL_RUN_AFTER_FINAL_LOCAL_CHECK`

## Question

Can P8d safely fill target-compatible remaining P8c holes with reviewed numeric value/score cells while preserving true not-applicable cells?

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P8d safely fill target-compatible remaining P8c holes with reviewed numeric value/score cells while preserving true not-applicable cells? |
| Baseline/comparator | P8c partial numeric artifact plus source-paper scope contract, generated dataset manifest, and P8 adapter matrix. |
| Primary pass criterion | Every executable deterministic cell has finite value and finite score when score is contractually meaningful; every executed DPF value cell averages exactly five seeds; true invalid cells remain structured not-applicable. |
| Veto diagnostics | Exact Kalman outside LGSSM/KSC is filled; spatial SIR gradient is filled despite no free theta; old LEDH-PFPF-OT evidence is used; proxy route is reported as native/source-faithful; DPF value lacks five seeds; nonfinite value or score is hidden as executed; stale P8c metadata appears in P8d artifact; Claude `VERDICT: REVISE` is unresolved. |
| Explanatory diagnostics | Monte Carlo SE, runtime, per-cell provenance, structured gap reason. |
| Not concluded | P8d does not prove posterior correctness, optimality, asymptotic validity, or DPF gradient correctness. |
| Artifact | P8d JSON/CSV/Markdown outputs and final result note. |

## Skeptical Plan Audit

Status: `PASS_BEFORE_FULL_RUN`.

This subplan preserves the reset memo order: Gate 1 focused validation passed, Gate 2 read-only implementation review converged, and this Gate 3 records the evidence contract before the full run. The planned command is CPU-only and intentionally hides CUDA before TensorFlow import. The primary criterion is artifact and cell-contract correctness, not speed, validation loss, or any proxy metric. The run can fail or remain partial if real route gaps remain; it must not convert real gaps into not-applicable cells or promote structured not-applicable cells as failures.

## Planned Final Local Check

Before launching the full run, rerun:

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py
```

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

```bash
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gate1-focused-validation-result-2026-06-14.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gate2-implementation-review-subplan-2026-06-14.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gate2-implementation-review-result-2026-06-14.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gate3-evidence-contract-and-run-subplan-2026-06-14.md scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

## Planned Full Run

Only if the final local check passes, run:

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --enable-p8d-execution
```

This is a deliberate CPU-only run. CUDA is hidden by environment variable before TensorFlow imports.

## Expected Artifacts

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-numeric-results-2026-06-13.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-value-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-score-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-curvature-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-status-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-stochastic-uncertainty-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-numeric-summary-2026-06-13.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-repair-execution-result-2026-06-14.md`

## Post-Run Audit

Inspect at minimum:

- `executed_cell_count`
- `structured_not_applicable_cell_count`
- `real_gap_cell_count`
- `pending_or_not_applicable_cell_count`

The scientific status is clean only if `real_gap_cell_count == 0`. True not-applicable cells are allowed and must not be counted as real gaps.

## Result Note Requirements

Write `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-repair-execution-result-2026-06-14.md` with:

- command actually run;
- CPU/GPU status;
- git status summary;
- random seeds;
- wall time;
- output artifact paths;
- decision table;
- post-run red-team note;
- Claude final read-only review status.

