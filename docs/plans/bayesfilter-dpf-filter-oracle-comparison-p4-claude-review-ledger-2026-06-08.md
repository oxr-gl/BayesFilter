# P4 Claude Review Ledger: Zhao-Cui TT Route Classification

metadata_date: 2026-06-08
phase: P4
status: PASS_P4_ZHAOCUI_ROUTE_CLASSIFICATION_READY_FOR_P5

## Role Contract

Codex is supervisor and executor in this dialogue.

Claude is a read-only critical reviewer only. Claude must not edit files, run
experiments, launch agents, or change state.

## Review Protocol

Claude must check wrong baselines, proxy metrics being treated as promotion
criteria, missing stop conditions, unfair comparisons, hidden assumptions,
stale context, environment mismatches, unsupported Zhao-Cui/fixed-design TT
claims, missing artifacts, and whether P4 answers the route-classification
question.

Claude must specifically check that:

- all P0 targets have a `zhao_cui_fixed_design_tt` classification;
- classifications use only the master claim classes;
- no Zhao-Cui/fixed-design TT row is promoted to `EXACT_ORACLE`;
- same-target value evidence exists before gradient-bearing runnable rows are
  interpreted;
- blocked multistate/native/KSC-mixture rows stay blocked;
- scalar-only routes are not applied to unsupported multistate targets;
- fit residuals, finite status, and Kalman sanity checks are not promoted to
  likelihood correctness;
- P5 eligibility is known and matches P0;
- the repaired P4 runner is genuinely pure Python and records that TensorFlow
  was not imported.

Claude must end with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.

## Iteration 1

Status: `VERDICT: AGREE`.

Scope for review:

- P4 subplan:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-subplan-2026-06-08.md`
- P4 result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-result-2026-06-08.md`
- P4 JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p4_zhaocui_tt_route_classification_2026-06-08.json`
- P4 runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p4_zhaocui_tt_route_classification_tf.py`
- P0 registry:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json`
- P2 result/JSON:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-result-2026-06-08.md`
  and
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_2026-06-08.json`
- P3 result/JSON:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-result-2026-06-08.md`
  and
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p3_conditional_gaussian_mixture_2026-06-08.json`
- P45 blocker sources:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json`
  and
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase5-cross-model-error-calibration-result-2026-06-08.md`
- Visible ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md`

Questions:

1. Does P4 classify every P0 `zhao_cui_fixed_design_tt` row using the master
   schema?
2. Are non-oracle Zhao-Cui/fixed-design TT rows kept as diagnostics,
   certified approximations, or blockers rather than exact oracles?
3. Are runnable gradient-bearing rows backed by same-target value evidence?
4. Are multistate/native/KSC-mixture unsupported rows preserved as blocked?
5. Does P5 eligibility match P0 and avoid making Zhao-Cui the P5 comparator?
6. Is the repaired P4 runner genuinely classification-only and pure Python?

Claude findings:

- P4 answers the route-classification question as a classification-only gate,
  with explicit skeptical-audit and non-promotion language in both the subplan
  and result note.
- All 13 P0 targets appear in the registry target list and all 13 receive a P4
  Zhao-Cui/fixed-design TT row classification.
- The classes used are restricted to the master schema, and no Zhao-Cui row is
  promoted to `EXACT_ORACLE`.
- Same-target value evidence is present before any gradient-bearing runnable
  Zhao-Cui row is interpreted, for LGSSM, P44-M2/M3/M4, and exact-transformed
  SV.
- Upstream P2/P3 evidence keeps Zhao-Cui as certified/local only rather than
  oracle truth.
- Blocked KSC-mixture, generalized-SV, spatial-SIR, and predator-prey rows
  stay blocked, and P45 blocker logic is preserved rather than bypassed.
- Claude did not see scalar-only TT applied to unsupported multistate rows.
- P5 eligibility matches P0; Zhao-Cui is not used as the P5 comparator.
- The repaired runner is genuinely pure Python with TensorFlow/TFP not
  imported.

Codex-supervisor classification:

| Finding | Classification | Decision |
| --- | --- | --- |
| P4 all-row classification accepted | `ACCEPT_AGREE` | P4 review gate passed. |
| No Zhao-Cui exact-oracle promotion | `ACCEPT_AGREE` | Preserve exact Kalman/dense as P5 references. |
| Blocked multistate/native rows preserved | `ACCEPT_AGREE` | No scalar TT route is forced onto unsupported targets. |
| Pure-Python repair accepted | `ACCEPT_AGREE` | P4 environment claim is now consistent with the runner and manifest. |

Decision: `PASS_P4_ZHAOCUI_ROUTE_CLASSIFICATION_READY_FOR_P5`.
