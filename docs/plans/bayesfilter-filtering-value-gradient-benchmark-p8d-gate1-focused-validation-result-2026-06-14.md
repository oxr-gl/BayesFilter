# P8d Gate 1 Focused Validation Result

Date: 2026-06-14

Status: `PASS_CLOSED`

## Scope

This result closes the local focused validation gate from the P8d reset memo:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-reset-memo-2026-06-14.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md`

P8d full numeric execution has not been run in this gate.

## Skeptical Plan Audit

Status: `PASS_FOR_GATE_1_LOCAL_VALIDATION`.

The gate answers only whether the repaired P8d runner and focused tests are locally coherent before implementation review. It does not treat P8c as a full benchmark, does not use proxy metrics as promotion criteria, does not cross into the full benchmark run, and preserves CPU-only execution with CUDA intentionally hidden.

## Commands Actually Run

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py
```

Result: passed.

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

Result: passed. The focused test output was `7 passed, 2 warnings in 63.96s`.

```bash
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gap-closure-plan-2026-06-13.md scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

Result: passed.

## Findings And Patch

The local checks passed before the patch below. During artifact review, Codex found that the P8d runner's `run_manifest.command` still contained an abbreviated output-path placeholder and that `run_manifest.plan_file` pointed at the older P8 master plan rather than the current P8d visible repair plan.

Patch applied in `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`:

- added `P8D_VISIBLE_PLAN_PATH`;
- set `source_artifacts.plan` and `run_manifest.plan_file` to the current P8d visible repair plan;
- preserved the older P8 master plan under `source_artifacts.p8_master_plan`;
- set `run_manifest.command` to the exact default CPU-only P8d execution command.

## Post-Patch Focused Checks

After the artifact-coverage patch, the same gate checks were rerun:

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py
```

Result: passed.

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

Result: passed. The focused test output was `7 passed, 2 warnings in 63.85s`.

```bash
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gap-closure-plan-2026-06-13.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gate1-focused-validation-result-2026-06-14.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gate2-implementation-review-subplan-2026-06-14.md scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

Result: passed.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Proceed to Gate 2 bounded read-only implementation review. |
| Primary criterion status | Gate 1 local checks passed before and after the artifact-coverage patch. |
| Veto diagnostic status | No full-run crossing, no GPU use, no detached execution, no DPF score/Hessian promotion. |
| Main uncertainty | Claude read-only implementation review still has not been rerun after the reset-memo repairs and this manifest patch. |
| Next justified action | Execute Gate 2 bounded read-only review subplan. |
| Not concluded | P8d full numeric benchmark completion, posterior correctness, DPF gradient correctness, or Phase 8 closure. |
