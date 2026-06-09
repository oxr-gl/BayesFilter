# P7 Subplan: Integration Closeout and Next Actions

metadata_date: 2026-06-08
phase: P7
status: REVIEWED_READY_AFTER_P6_PASS

## Question

What can responsibly be concluded from the DPF-versus-filter comparison
program, and what remains blocked or diagnostic-only?

## Evidence Contract

Primary criteria:

- every P0-P6 phase has a result or blocker artifact;
- exact-target, approximation-target, diagnostic-only, and blocked rows are
  separate;
- final claims match the strongest valid evidence class for each row;
- nonclaims preserve no HMC, production, GPU, paper-scale, or global correctness
  claims;
- Claude final review converges or records unresolved blockers.

Veto diagnostics:

- missing phase artifact;
- blocked row hidden from final table;
- exact and approximation rows merged;
- value-only row described as gradient-valid;
- stochastic-gradient caveats omitted;
- unsupported production/HMC/public API claim.

Explanatory-only diagnostics:

- total row counts by claim class, strongest comparator by target, unresolved
  implementation gaps, and next smallest discriminating run.

What will not be concluded:

- no universal DPF superiority claim;
- no default production method change;
- no HMC readiness unless a separate HMC phase is later run.

## Tasks

1. Collect P0-P6 artifacts.
2. Build promoted, approximation, diagnostic, and blocked ledgers.
3. Write final result note and reset memo.
4. Run Claude final read-only review.

## Planned Commands And Artifacts

Runner status:
planned module; P7 `PRECHECK` must implement this closeout audit, select an
existing audit by reviewed amendment, or write a blocker before any closeout
claim.

Planned command template:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p7_integration_closeout
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p7_integration_closeout --validate-only
```

P7 is closeout-only.  It must not introduce new numerical evidence.

Required artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p7_integration_closeout_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p7-integration-closeout-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-integration-closeout-result-2026-06-08.md`
- Phase Claude review ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-claude-review-ledger-2026-06-08.md`
- Reset memo:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-reset-memo-2026-06-08.md`

Claude final review follows the master max-five read-only loop.  Unresolved
material findings at the cap force `BLOCKED_FOR_HUMAN_REVIEW`.

## Exit Criteria

P7 exits with `PASS_P7_FILTER_COMPARISON_CLOSEOUT` only if all claims are
traceable to phase artifacts and Claude review returns `VERDICT: AGREE`.

## Stop Conditions

- any phase artifact is missing or stale;
- final result would need a human scientific decision to classify;
- Claude and Codex fail to converge after five rounds.
