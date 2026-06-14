# P6 Subplan: Gradient Semantics And Status Taxonomy

metadata_date: 2026-06-10
phase: FILTER_BENCH_P6
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Make gradient cells honest.  The benchmark must reveal invalid, unstable, or
diagnostic-only gradients rather than dropping the rows.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can every benchmark cell report a gradient value or an explicit gradient status that preserves scientific meaning? |
| Baseline/comparator | LGSSM analytic/Kalman gradient, deterministic autodiff or analytic sigma-point gradients, Zhao-Cui fixed-branch gradient lane, DPF fixed-branch and resampling-gradient diagnostics. |
| Primary criterion | Gradient status taxonomy exists and is enforced by adapter outputs and matrix emission, with row-level reference-gradient policy determining whether a gradient cell is benchmarkable, value-only, diagnostic, or blocked. |
| Veto diagnostics | Invalid DPF resampling gradients reported as valid; SVD/CUT4 branch-veto gradients reported as pass; missing reference gradient treated as zero error; finite gradient used as correctness proof. |
| Explanatory diagnostics | finite-gradient checks, finite-difference diagnostics, branch diagnostics, resampling counts, MC standard errors. |
| Not concluded | A valid status is not a guarantee of low error.  Finite-gradient checks and fixed-branch checks are explanatory only unless the row has a valid reference-gradient policy and no veto status. |
| Artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p6-gradient-semantics-result-2026-06-10.md` |

## Required Gradient Statuses

- `valid_exact_or_reference_gradient`
- `valid_autodiff_gradient`
- `valid_analytic_gradient`
- `fixed_branch_gradient_diagnostic`
- `resampling_gradient_not_valid`
- `branch_veto_gradient_not_valid`
- `reference_gradient_unavailable`
- `nonfinite_gradient`
- `adapter_failed`

## Tasks

- Define gradient error as normed error against the row reference when available.
- Define relative and absolute error fields.
- Define how DPF fixed-branch and resampling rows are reported.
- Define how SVD/CUT4 branch-veto diagnostics affect gradient status.
- Add cell-level reason codes for missing or invalid gradients.
- Declare which row classes may use `reference_gradient_unavailable` without
  blocking the value benchmark, and which `benchmarkable_value_gradient` rows
  must block if the reference gradient is missing.
- Make finite-gradient checks, finite-difference checks, and fixed-branch checks
  explicitly explanatory-only unless all row reference and branch diagnostics
  support a valid gradient classification.

## Exit Criteria

Pass with `PASS_FILTER_BENCH_P6_GRADIENT_SEMANTICS` only if every
algorithm/model cell can be represented without hiding invalid gradients, every
row class has a reference-gradient policy, and `reference_gradient_unavailable`
cannot be used to pass a row advertised as value/gradient benchmarkable.  Block
if DPF gradients cannot be classified without ambiguity or if any
`benchmarkable_value_gradient` row lacks a declared reference-gradient route.

## Validation

- Status schema tests once implemented.
- Claude read-only review, max five iterations.
