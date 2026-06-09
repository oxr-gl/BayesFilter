# P6 Claude Review Ledger: Cross-Filter Error Calibration

metadata_date: 2026-06-08
phase: P6
status: `VERDICT_AGREE_ITERATION_2`

## Iteration 1

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name dpf-filter-oracle-p6-review-iter1 "<bounded P6 review prompt>"
```

Claude status: `VERDICT: REVISE`

Accepted findings:

- P6 let P3 exact-transformed rows into `exact_target_calibration_rows` even
  though their reference uncertainty was `not_structured_in_p3_artifact`.
- The validator checked missing reference uncertainty for P2 dense rows only.
- The markdown did not expose DPF evaluator-variance fields, although JSON did.

Repairs:

- Moved P3 exact-transformed rows to `unstructured_metric_rows` with
  `valid_for_calibration_table: false`.
- Added a validator check that exact-target calibration rows must have accepted
  reference uncertainty.
- Added value SE and gradient-error-norm SE to the DPF diagnostic markdown
  table.

## Iteration 2

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name dpf-filter-oracle-p6-review-iter2 "<bounded P6 repair review prompt>"
```

Claude status: `VERDICT: AGREE`

Findings:

- Iteration-1 blockers are fixed: P3 exact-transformed rows are no longer in
  `exact_target_calibration_rows`; they are in `unstructured_metric_rows`.
- Exact-target calibration now contains only P2 dense-refinement rows with
  accepted reference uncertainty.
- The runner enforces accepted exact-target uncertainty and keeps DPF out of
  valid calibration rows.
- DPF evaluator-variance fields are visible in markdown and JSON.
- No remaining global-ranking or approximation-as-exact overclaim was found.

Codex decision:

- Accept Claude iteration-2 agreement.
- P6 exits `PASS_P6_CROSS_FILTER_CALIBRATION_READY_FOR_P7`.
