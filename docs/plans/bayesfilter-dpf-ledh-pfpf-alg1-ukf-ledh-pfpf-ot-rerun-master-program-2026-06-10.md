# Master Program: Algorithm 1 UKF LEDH-PFPF Rerun Of Former LEDH-PFPF-OT Tests

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Purpose

Redo every previous test and comparison lane that involved the old
`LEDH-PFPF-OT`, `dpf_ledh_pfpf_ot`, or auxiliary-flow-only `ledh_pfpf`
implementation, using the reviewed Li-Coates Algorithm 1 UKF covariance
lifecycle route as the replacement method.

This program does not revive old results as evidence.  It treats the old files
as historical coverage definitions and scaffolding only.  A rerun means one of:

- implement and run an Algorithm 1 UKF replacement for the old coverage;
- run a historical regression only with `HISTORICAL_ONLY_NOT_EVIDENCE`;
- mark a row `N/A_NOT_APPLICABLE` with a reason;
- mark a row `BLOCKED_REQUIRES_ADAPTER` with a concrete adapter plan.

## Governing Prior Art

- Source-faithful Algorithm 1 program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-master-program-2026-06-10.md`
- Supersession closeout:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-result-2026-06-10.md`
- New implementation route:
  `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
- New bounded LGSSM runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_tf.py`
- Old quarantined implementation route:
  `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`
- Old V2 and filter-oracle programs:
  `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-master-program-2026-06-07.md`
  and
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-master-program-2026-06-08.md`

## Role Contract

Codex in the current dialogue is the supervisor and executor.

Claude is a read-only reviewer only.  Claude review uses Opus with max effort
and must converge or stop after five iterations for each material plan/result
gate.

Execution must be visible in this dialogue when launched.  This program must
not use detached Codex agents, copied workspaces, background supervisors,
`codex exec`, `setsid`, `nohup`, or an overnight launch script.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can all old LEDH-PFPF-OT-related tests be redone or explicitly classified using the source-faithful Li-Coates Algorithm 1 UKF route? |
| Baseline/comparator | Old LEDH-PFPF-OT runners and artifacts define historical coverage only.  Valid comparators are Kalman for LGSSM, bootstrap/no-flow PF lanes, UKF/SVD/CUT4/Zhao-Cui only on declared compatible targets, and FilterFlow only for same-contract adapter checks. |
| Primary pass criterion | Every old LEDH-PFPF-OT-related lane is represented in a new result artifact as `RERUN_ALG1`, `HISTORICAL_ONLY`, `N/A_NOT_APPLICABLE`, or `BLOCKED_REQUIRES_ADAPTER`, with value and gradient evidence where applicable and uncertainty recorded for stochastic rows. |
| Veto diagnostics | Using `ledh_pfpf_ot_tf.py` as current Algorithm 1 evidence; running P2-P8 before P0 registry and P1 direct smoke pass; comparing filters on unsupported model/filter pairs; promoting one-seed stochastic differences; value agreement used to promote gradients; missing route identifiers; non-finite state, weights, determinants, or gradients; changing thresholds after seeing results. |
| Explanatory diagnostics | ESS, runtime, covariance spectra, determinant ranges, old-vs-new deltas, FilterFlow same-contract residuals, particle ladders, and blocked adapter inventory. |
| Not concluded | No production default, no HMC readiness, no universal superiority claim, no stochastic-resampling gradient correctness, no claim that OT resampling is part of Li-Coates Algorithm 1, and no proof of FilterFlow correctness. |
| Artifacts | Master program, visible runbook, phase subplans/results, Claude review ledger, JSON/Markdown reports, run manifests, and final closeout. |

## Mandatory Algorithm 1 Route Fields

Every replacement row and machine-readable artifact that claims Algorithm 1 UKF
evidence must include these fields:

| Field | Required value or role |
| --- | --- |
| `method_generation` | `li_coates_algorithm1_ukf_covariance_lifecycle` |
| `flow_source_route` | `li_coates_2017_algorithm1_ledh_pfpf` |
| `covariance_route` | `per_particle_ukf_prediction_update` |
| `prediction_covariance_route` | UKF prediction route for `(x_{k-1}^i, P_{k-1}^i) -> (m_{k|k-1}^i, P^i)` |
| `update_covariance_route` | UKF update route for `(m_{k|k-1}^i, P^i) -> P_k^i` |
| `flow_anchor_route` | `zero_noise_transition` unless a reviewed extension says otherwise |
| `core_resampling_route` | `none` or classical Algorithm-1-compatible resampling status |
| `extension_resampling_route` | `none`, `bayesfilter_ot_extension`, or another reviewed extension label |
| `evidence_route_class` | `SOURCE_ALGORITHM1_CORE` or `BAYESFILTER_EXTENSION_NOT_SOURCE_CORE` |
| `previous_ledh_pfpf_ot_evidence_status` | `quarantined` |

Rows missing any required field cannot be promoted beyond diagnostic or blocker
status.

## Threshold And Promotion Discipline

P0 must create a rerun registry that predeclares, before numerical execution:

- row id and model id;
- comparator route and claim class;
- value scalar and gradient scalar;
- value normalization rule;
- gradient normalization rule;
- value tolerance or `N/A` with reason;
- gradient tolerance or `N/A` with reason;
- certification band or `N/A` with reason;
- minimum seed count;
- particle ladder;
- primary pass/promote statistic;
- veto diagnostics;
- allowed final statuses.

Finite execution is never by itself a promotion criterion.  A finite run with
missing or failed predeclared thresholds can be `DIAGNOSTIC_ONLY`,
`N/A_NOT_APPLICABLE`, or `BLOCKED_REQUIRES_ADAPTER`, but not promoted as
closeness or correctness evidence.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P0 | Inventory And Rerun Registry | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p0-inventory-registry-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p0-inventory-registry-result-2026-06-10.md` |
| P1 | Direct LGSSM, Range-Bearing, Gradient Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p1-direct-lgssm-range-bearing-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p1-direct-lgssm-range-bearing-result-2026-06-10.md` |
| P2 | V2 Algorithm 1 Contract Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p2-v2-contracts-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p2-v2-contracts-result-2026-06-10.md` |
| P3 | V2 Algorithm 1 Value Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p3-v2-values-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p3-v2-values-result-2026-06-10.md` |
| P4 | V2 Algorithm 1 Gradient Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p4-v2-gradients-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p4-v2-gradients-result-2026-06-10.md` |
| P5 | Filter-Oracle Statistical Closeness Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p5-filter-oracle-statistical-closeness-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p5-filter-oracle-statistical-closeness-result-2026-06-10.md` |
| P6 | Cross-Filter Calibration Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p6-cross-filter-calibration-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p6-cross-filter-calibration-result-2026-06-10.md` |
| P7 | P44/P8 Blocker Closure Replacement | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p7-p44-blocker-closure-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p7-p44-blocker-closure-result-2026-06-10.md` |
| P8 | FilterFlow, Annealed, And Historical Regression Classification | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p8-filterflow-annealed-historical-regression-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p8-filterflow-annealed-historical-regression-result-2026-06-10.md` |
| P9 | Integration Closeout And Supersession Ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p9-closeout-supersession-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p9-closeout-supersession-result-2026-06-10.md` |

## Old Coverage To Redo Or Classify

| Historical lane | Old command or artifact family | New disposition |
| --- | --- | --- |
| Direct LGSSM value | `run_lgssm_ledh_pfpf_ot_tf.py` | P1 Algorithm 1 LGSSM value rerun against Kalman and bootstrap/no-flow comparator. |
| Direct LGSSM multiseed | `run_lgssm_multiseed_ledh_pfpf_ot_tf.py` | P1 Algorithm 1 paired multiseed particle ladder with MC uncertainty. |
| Direct range-bearing value | `run_range_bearing_ledh_pfpf_ot_tf.py` | P1 replacement only after range-bearing callbacks/adapters pass; otherwise concrete blocker. |
| Direct range-bearing stress | `run_range_bearing_stress_ledh_pfpf_ot_tf.py` | P1 stress rerun or blocked adapter/tuning note; no promotion from stress alone. |
| Direct gradient checks | `run_ledh_pfpf_gradient_checks_tf.py` | P1 same-scalar fixed-branch gradient smoke and, if feasible, ladder. |
| Annealed transport LEDH | `run_ledh_pfpf_annealed_transport_lgssm_tf.py` | P8 classify as BayesFilter extension, not Li-Coates core. |
| FilterFlow matched LEDH-PFPF-OT | `run_filterflow_matched_ledh_pfpf_ot_tf.py` | P8 same-contract adapter replacement or historical-only classification. |
| V2 contracts | `run_v2_ledh_pfpf_ot_contracts_tf.py` | P2 replacement contracts with Algorithm 1 route identifiers. |
| V2 values | `run_v2_ledh_pfpf_ot_values_tf.py` | P3 replacement value rows for all V2 rows, or explicit unsupported/blocker classifications. |
| V2 gradients | `run_v2_ledh_pfpf_ot_gradients_tf.py` | P4 replacement fixed-branch gradient rows where estimand is valid. |
| Filter-oracle P5 | `run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf.py` | P5 replacement statistical closeness rows using Algorithm 1 method id. |
| Filter-oracle P6 | `run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf.py` | P6 replacement calibration rows and tables. |
| Filter-oracle P7 | `run_filter_oracle_comparison_p7_integration_closeout.py` | P9 new closeout only after replacement rows. |
| Filter-oracle P8/P44 | `run_filter_oracle_comparison_p8_p44_dpf_blocker_closure_tf.py` | P7 replacement of P44/P8 DPF cells or concrete adapter blockers. |
| Auxiliary-flow-only repair | `run_ledh_pfpf_source_faithful_repair_tf.py` | P0/P9 historical-only; not rerun as evidence unless explicitly labelled regression. |
| Focused Algorithm 1 governance | `tests/test_ledh_pfpf_alg1_ukf_tf.py` | P0/P1/P9 must rerun as guardrail before and after material replacements. |
| Old V2 live gate/closeout consumers | `scripts/dpf_v2_algorithm_full_comparison_live_gate.py` and `run_v2_algorithm_full_comparison_closeout.py` | P0 inventory and P9 closeout must prevent old route ids from being accepted as current Algorithm 1 evidence. |
| Old filter-oracle upstream consumers | `run_filter_oracle_comparison_p1_lgssm_exact_oracle_tf.py` and any other runner/gate containing `dpf_ledh_pfpf_ot` | P0 inventory and P5-P9 replacements must classify or quarantine any old-route row surfaces. |

## Review Protocol

For the master program and for each material phase result:

1. Codex writes or updates the artifact.
2. Codex asks Claude Opus with max effort for read-only review.
3. Claude must not edit files, run experiments, launch agents, or change state.
4. Claude must end with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.
5. If Claude says revise, Codex audits the finding, patches accepted issues,
   records the revision, and repeats.
6. Stop after agreement or five iterations.  If material findings remain after
   five iterations, status becomes `BLOCKED_FOR_HUMAN_REVIEW`.

Review ledger:

`docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-claude-review-ledger-2026-06-10.md`

## Execution Discipline

P0 must pass before any rerun.  P1 direct smoke must pass before broad V2 and
filter-oracle replacement.  P2 contracts must pass before P3 values or P4
gradients.  P5-P7 cannot promote rows whose target-route applicability was not
predeclared.

Every serious run must record:

- git branch and commit;
- exact command;
- environment or conda environment;
- CPU/GPU status;
- `CUDA_VISIBLE_DEVICES` status before TensorFlow import;
- route identifiers;
- model fixture version or digest;
- random seeds;
- particle counts;
- pseudo-time schedule;
- UKF parameters;
- wall time;
- output JSON/Markdown paths;
- plan and result paths.

CPU-only TensorFlow commands must set `CUDA_VISIBLE_DEVICES=-1` before import.
GPU/CUDA commands and Claude Code commands require trusted/escalated execution.

## Skeptical Plan Audit

| Risk | Audit status | Control |
| --- | --- | --- |
| Wrong baseline | Pass for review | Old LEDH-PFPF-OT is coverage history, not a truth source.  Kalman is exact only for LGSSM.  Other filters are valid only on declared targets. |
| Proxy metrics promoted | Pass for review | ESS, runtime, FD residuals, stress rows, and same-contract residuals can explain or veto but cannot promote correctness alone. |
| Missing stop conditions | Pass for review | P0 registry, P1 direct smoke, P2 contracts, nonfinite diagnostics, unsupported route classification, and max-five review failure all block. |
| Unfair comparison | Pass for review | Stochastic DPF rows require paired seeds, particle ladders, and uncertainty; deterministic filters are not ranked on unsupported models. |
| Hidden assumption | Pass for review | UKF is the requested Algorithm 1 covariance option; OT is a BayesFilter extension, not the paper's Algorithm 1 core. |
| Stale context | Pass for review | P0 refreshes the inventory before execution and rechecks old row occurrences. |
| Artifact mismatch | Pass for review | Every phase has a result artifact and JSON/report requirement where numerical data exist. |
| Environment mismatch | Pass for review | CPU-only/GPU/trusted-Claude rules are explicit. |

## Stop Conditions

Stop and write a blocker if:

- the new Algorithm 1 route cannot be wired without altering its reviewed
  route identifiers;
- a model lacks required transition, observation, Jacobian, covariance, or
  density callbacks;
- a comparator is not valid for the target;
- a gradient scalar or parameterization cannot be matched;
- nonfinite numerical state appears and cannot be localized by a focused
  diagnostic;
- continuing would require package installation, network fetch, credentials,
  destructive git/filesystem action, default-policy change, or edits to
  unrelated dirty worktree files;
- Claude and Codex do not converge after five review iterations.
