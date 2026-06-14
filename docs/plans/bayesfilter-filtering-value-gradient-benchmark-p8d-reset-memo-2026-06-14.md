# P8d Reset Memo For Reboot Handoff

Date: 2026-06-14

Purpose: preserve the exact P8d state before reboot so the next machine can resume without replaying the failed/stalled execution loop.

## Bottom Line

The P8d full numeric benchmark has **not** been run.  Do not treat P8d as a completed result.

The last valid numeric artifact is still P8c:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-summary-2026-06-13.md`

P8c is partial comparator-only evidence.  It is not a full scientific baseline and should not be promoted as closing Phase 8.

## Current P8d State

P8d was created to fill remaining value/score benchmark cells while preserving true not-applicable cells.

The active visible repair plan is:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md`

Its last known status is:

- `PLAN_REVIEWED_READY_FOR_IMPLEMENTATION`

The older unsafe draft plan is:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gap-closure-plan-2026-06-13.md`

That older plan intentionally remains:

- `PAUSED_NOT_READY_FOR_EXECUTION`

This is not a contradiction.  The older draft lane was paused because it was unsafe; the visible repair plan is the current lane.

## Files That Matter

The P8d repair files exist but were untracked at the last check:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gap-closure-plan-2026-06-13.md`
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-reset-memo-2026-06-14.md`

No P8d output artifact existed at last check:

- no `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-numeric-results-2026-06-13.json`
- no `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-numeric-summary-2026-06-13.md`

## What Was Repaired Before Reboot

The P8d runner had been partially repaired after Claude implementation review.

Known repairs:

- P8d schema/phase/status metadata added.
- Full execution is gated by `--enable-p8d-execution`.
- P8c is labeled partial comparator-only evidence.
- Deterministic route dispatch added through `_deterministic_value_fn`.
- DPF route callbacks added for LGSSM, raw SV, predator-prey, and generalized SV.
- DPF execution is value-only and uses five seeds with Monte Carlo standard error.
- Exact Kalman remains LGSSM/KSC only.
- Spatial SIR gradients remain `not_applicable_no_free_theta`.
- Artifact accounting now separates:
  - `executed`
  - `structured_not_applicable`
  - `real_gaps`
- P8d summary title was corrected to `# P8d Numeric Benchmark Execution Summary`.
- Tests were added for not-applicable versus real-gap accounting.

Known explicit gaps preserved by design:

- KSC DPF callback is still a structured callback gap unless implemented later.
- Spatial SIR DPF callback is still a structured callback gap unless implemented later.
- DPF score/Hessian is not certified and must not be fabricated.
- Exact Kalman outside LGSSM/KSC remains not applicable.
- Old LEDH-PFPF-OT evidence must not be used.

## Why The Previous Loop Stalled

The problem was execution management, not a completed benchmark.

Sequence:

1. Claude plan review initially stalled on large prompts.
2. A small Claude probe returned successfully, so the prompt was the issue.
3. A bounded inline plan review returned `VERDICT: AGREE`.
4. The P8d runner and tests were patched.
5. Focused tests passed once before the final Claude repair.
6. Claude implementation review then returned `VERDICT: REVISE`.
7. The three Claude findings were patched:
   - stale P8c summary title;
   - true not-applicable cells counted as pending gaps;
   - missing test guard for that accounting.
8. The focused tests and Claude implementation review were not rerun after those final repairs.
9. The P8d full run was not launched.

## Required Next Gates

Resume here.  Do not start with the full benchmark.

### Gate 1: Local Focused Validation

Run:

```bash
python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py
```

Run CPU-only:

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

Run:

```bash
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gap-closure-plan-2026-06-13.md scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

If any of these fail, patch only the P8d files needed to fix the failure.

### Gate 2: Claude Read-Only Implementation Review

Use the Claude worker wrapper, not a detached Codex agent.

Run with trusted/escalated permissions if required by the local sandbox policy:

```bash
timeout 90s bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name p8d-implementation-review-r2 --model sonnet --effort low "<bounded review prompt>"
```

The bounded prompt should ask Claude to review only:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md`
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`

Tell Claude explicitly that the previous three findings were:

- stale P8c summary title;
- true not-applicable cells counted as real gaps;
- tests did not guard that accounting.

Ask for:

- `VERDICT: AGREE` or `VERDICT: REVISE`
- concise blocking findings only
- no broad redesign

If Claude times out, run a tiny probe.  If the probe succeeds, the review prompt is too large and must be redesigned smaller.

### Gate 3: Evidence Contract Before Full Run

Before launching P8d, record this evidence contract in the run note or terminal log:

| Field | Contract |
|---|---|
| Question | Can P8d safely fill target-compatible remaining P8c holes with reviewed numeric value/score cells while preserving true not-applicable cells? |
| Baseline/comparator | P8c partial numeric artifact plus source-paper scope contract, generated dataset manifest, and P8 adapter matrix. |
| Primary pass criterion | Every executable deterministic cell has finite value and finite score when score is contractually meaningful; every executed DPF value cell averages exactly five seeds; true invalid cells remain structured not-applicable. |
| Veto diagnostics | Exact Kalman outside LGSSM/KSC is filled; spatial SIR gradient is filled despite no free theta; old LEDH-PFPF-OT evidence is used; proxy route is reported as native/source-faithful; DPF value lacks five seeds; nonfinite value or score is hidden as executed; stale P8c metadata appears in P8d artifact; Claude `VERDICT: REVISE` is unresolved. |
| Explanatory diagnostics | Monte Carlo SE, runtime, per-cell provenance, structured gap reason. |
| Not concluded | P8d does not prove posterior correctness, optimality, asymptotic validity, or DPF gradient correctness. |
| Artifact | P8d JSON/CSV/Markdown outputs and a final result note. |

### Gate 4: Full P8d Run

Only after Gates 1 and 2 pass:

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --enable-p8d-execution
```

This is a CPU-only benchmark run.  It may take a while because DPF cells use five seeds.

Expected output artifacts should be under `docs/plans`, with names beginning:

- `bayesfilter-filtering-value-gradient-benchmark-p8d-`

### Gate 5: Post-Run Audit

After the run, inspect the artifact counts:

- `executed_cell_count`
- `structured_not_applicable_cell_count`
- `real_gap_cell_count`
- `pending_or_not_applicable_cell_count`

The scientific status is only clean if `real_gap_cell_count == 0`.  True not-applicable cells are allowed and should not be counted as real gaps.

Then write:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-repair-execution-result-2026-06-14.md`

The result note must include:

- command actually run;
- CPU/GPU status;
- git status summary;
- random seeds;
- wall time;
- output artifact paths;
- decision table;
- post-run red-team note;
- Claude final read-only review status.

## Do Not Do

- Do not claim P8d completed until the full run emits artifacts.
- Do not use old LEDH-PFPF-OT evidence to fill cells.
- Do not turn DPF value-only cells into score/Hessian evidence.
- Do not treat P8c as a full benchmark.
- Do not silently convert structured not-applicable cells into failures.
- Do not silently convert real route gaps into not-applicable cells.
- Do not launch detached Codex agents.

## Recommended Resume Message

Use this as the first working note on the new machine:

> Resuming P8d from reset memo `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-reset-memo-2026-06-14.md`.  P8d full run has not happened.  Starting at Gate 1 focused validation, then Claude read-only implementation review, then gated CPU-only full run only if both pass.

