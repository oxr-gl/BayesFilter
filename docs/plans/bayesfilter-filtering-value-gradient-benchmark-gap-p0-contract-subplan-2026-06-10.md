# P0 Subplan: Benchmark Contract And Gap Lock

metadata_date: 2026-06-10
phase: FILTER_BENCH_P0
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Lock the benchmark contract before any full comparison run.  The central repair
is to remove the mistaken rule that non-LGSSM filters must be exact same-target
methods to be benchmarked.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we state a benchmark contract that compares approximate filters fairly without overclaiming exactness? |
| Baseline/comparator | Current P43/P44/P50/P51/P53 ledgers and existing DPF Algorithm 1 closeout artifacts. |
| Primary criterion | A written contract distinguishes exact, dense numerical, transformed, mixture, and diagnostic references, and declares exactness a cell attribute. |
| Veto diagnostics | Non-LGSSM rows excluded because UKF/SVD/CUT4/Zhao-Cui/DPF are approximate; DPF gradient failures hidden; old LEDH-PFPF-OT treated as current. |
| Explanatory diagnostics | Existing result ledgers and tests that show callable routes. |
| Not concluded | No benchmark result ranking. |
| Artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p0-contract-result-2026-06-10.md` |

## Tasks

- Write the final benchmark question and metric definitions.
- Define `reference_type` values: `exact`, `dense_numerical`,
  `transformed_actual_nongaussian`, `gaussian_mixture_surrogate`,
  `diagnostic`, and `blocked_only`.
- Define what a value error and a gradient error cell must report.
- Add non-claim rules for approximation rows.
- Define the old LEDH-PFPF-OT supersession guard.

## Exit Criteria

Pass with `PASS_FILTER_BENCH_P0_CONTRACT` only if the contract would permit all
existing filters to be tested on non-LGSSM rows while preserving exactness
labels.  Block with `BLOCK_FILTER_BENCH_P0_CONTRACT` if exactness scope cannot
be stated without ambiguity.

P0 may loop through Claude review at most five times for the same blocker.  If a
major blocker remains at iteration five, record `BLOCK_FILTER_BENCH_P0_CONTRACT`
and do not advance to P1.

## Validation

- Review the contract against the master program evidence contract.
- Claude read-only review, max five iterations.
