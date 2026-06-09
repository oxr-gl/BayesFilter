# P3 Claude Review Ledger: Conditional Gaussian Mixture

metadata_date: 2026-06-08
phase: P3
status: PASS_P3_CONDITIONAL_GAUSSIAN_READY_FOR_P4

## Role Contract

Codex is supervisor and executor in this dialogue.

Claude is a read-only critical reviewer only. Claude must not edit files, run
experiments, launch agents, or change state.

## Review Protocol

Claude must check wrong baselines, proxy metrics being treated as promotion
criteria, missing stop conditions, unfair comparisons, hidden assumptions,
stale context, environment mismatches, unsupported transformed-SV or
mixture-oracle claims, missing artifacts, and whether P3 evidence answers the
conditional-Gaussian/mixture target question.

Claude must specifically check that:

- exact transformed SV and finite KSC-mixture SV targets are not mixed;
- KSC Kalman evidence is exact only for the declared finite-mixture target and
  not called native-SV truth;
- transformation and Jacobian conventions are recorded;
- DPF bootstrap-OT and LEDH-PFPF-OT remain blocked and were not executed;
- Zhao-Cui/fixed-design TT and CUT4 stay in their P0 claim classes;
- value and gradient gaps are present for the selected reference/candidate
  rows;
- CPU-only TensorFlow execution and run artifacts are recorded.

Claude must end with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.

## Iteration 1

Status: `VERDICT: AGREE`.

Scope for review:

- P3 subplan:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-subplan-2026-06-08.md`
- P3 result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-result-2026-06-08.md`
- P3 JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p3_conditional_gaussian_mixture_2026-06-08.json`
- P3 runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p3_conditional_gaussian_mixture_tf.py`
- P0 registry:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json`
- Visible ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md`

Questions:

1. Does P3 correctly separate exact transformed SV from the finite KSC-mixture
   approximation target?
2. Are exact-oracle claims scoped to dense exact transformed SV and
   component-enumerated KSC Kalman mixture only?
3. Are Zhao-Cui/fixed-design TT and CUT4 kept as same-target local
   certificates rather than exact oracles?
4. Are KSC-vs-exact transformed gaps treated as approximation-only diagnostics
   rather than native-SV correctness evidence?
5. Are DPF bootstrap-OT and LEDH-PFPF-OT correctly blocked rather than executed
   or promoted in P3?

Claude findings:

- P3 answers the scoped conditional-Gaussian/mixture target question with
  target separation and claim scoping preserved.
- The P3 subplan and visible ledger state the right evidence contract: exact
  transformed SV and finite KSC-mixture SV are separate rows; same-target
  comparisons are primary; KSC-vs-exact transformed gaps are explanatory only;
  and DPF must remain blocked in P3.
- The P0 registry supports the split: for
  `sv_exact_transformed_log_chi_square_panel`, dense transformed quadrature is
  `EXACT_ORACLE`, Zhao-Cui/fixed-design TT is
  `CERTIFIED_APPROXIMATION`, Kalman is blocked, and both DPF routes are
  blocked. For `sv_ksc_transformed_mixture_panel`, KSC Kalman is
  `EXACT_ORACLE` only for the declared finite-mixture target, CUT4 is
  `CERTIFIED_APPROXIMATION`, dense is `DIAGNOSTIC_ONLY`, and both DPF routes
  remain blocked.
- The runner implements that separation: exact transformed rows call dense and
  TT transformed-SV routes, KSC rows call mixture Kalman and CUT4 routes, and
  the only cross-target comparison is explicitly stored as
  `approximation_gap_to_exact_transformed`.
- Transform and Jacobian conventions are recorded with the right scope: exact
  transformed rows record `z = log(y^2)`, zero offset, and the raw-native
  Jacobian relation; KSC rows record `z = log(y^2 + offset)` with
  `offset = 1e-8` and say native exactness is not promoted.
- KSC Kalman exactness is correctly scoped only to the declared finite-mixture
  target, not native SV, in both result note and JSON nonclaims/target
  metadata.
- Zhao-Cui/fixed-design TT and CUT4 remain in their P0 claim classes rather
  than being upgraded to exact oracles.
- Value and gradient gaps are present for both same-target comparisons, and
  cross-target KSC-vs-exact transformed gaps are marked approximation-only.
- DPF bootstrap-OT and LEDH-PFPF-OT remain blocked and are not executed; the
  veto flag `dpf_executed_or_p3_eligible` is false.
- CPU-only execution is recorded in the runner, visible ledger, result note,
  and JSON manifest.
- Claude found no material wrong-baseline, proxy-promotion, stop-condition,
  unfair-comparison, stale-context, environment, or unsupported-claim blocker.

Codex-supervisor classification:

| Finding | Classification | Decision |
| --- | --- | --- |
| P3 target separation and claim scoping accepted | `ACCEPT_AGREE` | P3 review gate passed. |
| DPF blockers preserved | `ACCEPT_AGREE` | P3 does not execute or promote DPF routes. |
| KSC mixture exactness properly scoped | `ACCEPT_AGREE` | Advance to P4 route classification. |

Decision: `PASS_P3_CONDITIONAL_GAUSSIAN_READY_FOR_P4`.
