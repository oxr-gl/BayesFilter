# P5 Claude Review Ledger: DPF Statistical Closeness

metadata_date: 2026-06-08
phase: P5
status: `VERDICT_AGREE_ITERATION_1`

## Iteration 1

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name dpf-filter-oracle-p5-review-iter1 "<bounded P5 review prompt>"
```

Claude status: `VERDICT: AGREE`

Findings:

- No wrong-baseline or comparator drift found. P5 keeps exact Kalman for
  `lgssm_2d_h25_rich` and `dense_refined_quadrature` for P44-M2/M3/M4.
- Zhao-Cui, CUT4, SVD, UKF, and BF/FilterFlow agreement are explicitly excluded
  as P5 DPF comparators.
- No placeholder DPF band is promoted. All 8 P4-eligible rows are classified:
  0 promoted, 2 LGSSM rows downgraded, and 6 P44 rows blocked.
- No fixed/stochastic gradient mixing or branch/residual overclaim appears.
  LGSSM rows stay `fixed_branch_score` and are downgraded because directional
  residuals are missing and branch decisions are aggregate-only.
- P44 rows are blocked pending reviewed same-target adapters, evaluator
  variance, scalar/gradient tie, and branch diagnostics.
- The P6 mention is conditional and does not claim DPF promotion readiness.

Codex decision:

- Accept Claude iteration-1 agreement.
- P5 exits `PASS_P5_DPF_STATISTICAL_CLOSENESS_READY_FOR_P6`.
- Keep the P5 conclusion scoped: this is a classification pass with no DPF row
  promoted.
