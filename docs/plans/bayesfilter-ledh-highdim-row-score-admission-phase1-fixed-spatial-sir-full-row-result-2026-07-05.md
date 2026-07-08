# Phase 1 Result: Fixed Spatial SIR Full-Row Score Promotion

Date: 2026-07-06

Status: `BLOCK_PHASE1_FIXED_SIR_FULL_ROW_SCORE`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Do not promote the scoped parameterized SIR score into the fixed full-row LEDH leaderboard row. The two rows are different targets. |
| Primary criterion status | Passed by precise blocker: the fixed full-row SIR row is `no_free_theta` value-only, while the parameterized SIR score row is explicitly a scoped local-complete-data component row. |
| Veto diagnostic status | Passed: no scoped local-complete-data score was promoted to the full observed-data/filtering row. |
| Main uncertainty | Whether a future separate parameterized full observed-data SIR row should be created and admitted as a new row. |
| Next justified action | Advance to actual-SV same-target repair. The fixed full-row SIR bridge is not a code-plumbing issue; it is a target-identity blocker. |
| What is not concluded | No fixed-row LEDH SIR score, no full observed-data parameterized SIR score, no HMC readiness, and no claim that the scoped SIR score is wrong for its own scoped target. |

## Question Answered

Phase 1 asked:

- Is the scoped parameterized SIR score the derivative of the fixed full-row
  SIR leaderboard scalar?

Answer:

- No.

The fixed full-row row and the parameterized scoped row are different targets.
Promoting the scoped score as the fixed full-row score would be wrong relative
to the stated target.

## Evidence

Fixed full-row SIR:

- `zhao_cui_spatial_sir_austria_j9_T20` is the fixed source-parity row.
- Its dataset contract preserves `truth_theta_coordinate = "no_free_theta"`
  and `truth_theta = []`:
  [bayesfilter-parameterized-sir-leaderboard-repair-phase2-dataset-row-contract-result-2026-07-02.md](/home/chakwong/BayesFilter/docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase2-dataset-row-contract-result-2026-07-02.md)
- The LEDH July 3 row ledger keeps this row as value-only with
  `blocked_score_for_full_leaderboard_row`:
  [bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json](/home/chakwong/BayesFilter/docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json)
- The July 3 closeout says the fixed SIR LEDH row is
  `executed_value_only_score_blocked`:
  [bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-result-2026-07-03.md](/home/chakwong/BayesFilter/docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-result-2026-07-03.md)

Parameterized scoped SIR:

- `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` is a distinct
  row with theta coordinate `sir_log_scale_theta` and three parameters:
  [bayesfilter-parameterized-sir-target-contract-2026-07-02.md](/home/chakwong/BayesFilter/docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md)
- The current score route in
  [benchmark_p8p_parameterized_sir_gradient.py](/home/chakwong/BayesFilter/docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:314)
  builds scaled `kappa`, `nu`, and observation covariance from those three log
  scales and computes a manual score route in
  [benchmark_p8p_parameterized_sir_gradient.py](/home/chakwong/BayesFilter/docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:1314).
- The two-lane leaderboard code labels this row as
  `target_scope = local_complete_data_zhao_cui_sir_d18_component`,
  `row_admission_status = scoped_component_row_admitted`, and explicitly says
  it is not full observed-data/filtering evidence:
  [benchmark_two_lane_highdim_leaderboard.py](/home/chakwong/BayesFilter/docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py:1611)
- Focused tests enforce that this scoped row remains not-full-row evidence:
  [test_two_lane_highdim_leaderboard_phase5.py](/home/chakwong/BayesFilter/tests/test_two_lane_highdim_leaderboard_phase5.py:60)

Prior classification already reached the same conclusion:

- [bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-score-target-result-2026-07-03.md](/home/chakwong/BayesFilter/docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-score-target-result-2026-07-03.md)

## Plain Scientific Classification

The fixed full-row SIR leaderboard cell has no free theta.

The parameterized SIR score differentiates a different row with respect to a
three-parameter log-scale theta and is further scoped as a local-complete-data
component target rather than a full observed-data/filtering target.

Therefore:

- fixed full-row SIR score bridge: blocked;
- reason: wrong target, not just missing plumbing;
- promoting the scoped parameterized score as the fixed full-row score would be
  wrong relative to the stated target.

## Required Checks Run

```bash
rg -n "local_complete_data|full observed-data|not a full observed-data/filtering row|no_free_theta|scoped_score_diagnostic_not_full_observed_data_score|scoped_component_row_admitted" docs/plans docs/benchmarks tests -g '!*.pyc'
```

Result: passed; the repo consistently labels the parameterized row as scoped
and the fixed row as `no_free_theta`.

```bash
rg -n "zhao_cui_spatial_sir_austria_j9_T20|parameterized_logscale|manual_reverse_scan_no_autodiff|_manual_value_and_score_from_components|_build_base_tensors|scoped_component_row|blocked_score_for_full_leaderboard_row" docs/plans docs/benchmarks tests experiments -g '!*.pyc'
```

Result: passed; the code and plan anchors for the fixed row and the scoped row
were located.

```bash
git diff --check -- docs/plans/bayesfilter-ledh-highdim-row-score-admission-* docs/reviews/ledh-highdim-row-score-admission-launch-review-bundle-2026-07-05.md
```

Result: passed.

## Evidence Contract Result

| Field | Status |
| --- | --- |
| Question | Answered directly: no, the scoped parameterized score is not the fixed full-row score. |
| Baseline/comparator | Passed: row contracts, row ledger, July 3 closeout, leaderboard code, and focused tests agree. |
| Primary criterion | Passed by blocker: the target mismatch is explicit and stable across artifacts. |
| Veto diagnostics | Passed: no target confusion was promoted. |
| Explanatory diagnostics | The manual no-autodiff score route remains valid as scoped evidence for its own row. |
| Not concluded | No full-row repair, no new code, no new score admission. |

## Next-Phase Handoff

Phase 2 should proceed exactly as the master program states:

- actual-SV same-target adapter and score repair.

The Phase 2 subplan remains valid and should carry forward this fixed-SIR
classification:

- fixed SIR main row: blocked full-row score because it has no free theta;
- parameterized SIR scoped row: valid scoped evidence only, not a substitute
  for the fixed row.
