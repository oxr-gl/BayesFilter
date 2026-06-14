# Master Program: DPF Value and Gradient Comparison Against Filter Oracles and Approximation Routes

metadata_date: 2026-06-08
program_id: dpf-filter-oracle-comparison
status: REVIEWED_READY_FOR_P0_PRECHECK

## Purpose

Build a governed comparison program for BayesFilter DPF methods, especially
bootstrap-OT and LEDH-PFPF-OT, against available filtering routes for value and
gradient evidence.

The comparison routes include exact Kalman, UKF, SVD/sigma-point filters, CUT4,
and Zhao-Cui/fixed-design TT-style routes where they are valid for the declared
target.  The program must classify each route as exact oracle, certified
approximation, surrogate, diagnostic, or blocked before running numerical
comparisons.

## Governing Sources

- `AGENTS.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p42-gradient-likelihood-validation-rules-2026-06-07.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json`
- `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-closeout-result-2026-06-07.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p8-lgssm-validation-result-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase1-lgssm-exact-reference-result-2026-06-05.md`

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_WITH_STRICT_NONORACLE_GATES`.

Wrong-baseline risk:
Kalman is exact only for linear Gaussian targets.  CUT4, UKF, SVD, and
Zhao-Cui routes are not universal truth.  P0 must classify each target-route
pair before any comparison.

Proxy-promotion risk:
Finite values, stable runtime, high ESS, small Sinkhorn residuals, TT fit
residuals, and same-implementation AD/FD checks can explain or veto.  They do
not promote DPF correctness or gradient correctness without a same-target
reference.

Missing stop-condition risk:
Each phase has explicit blocked outcomes.  A blocked route must not be hidden
as a pass, and missing filters must not be omitted from summary tables.

Unfair-comparison risk:
DPF is stochastic while Kalman, UKF, SVD, CUT4, and many TT routes are
deterministic once their branch decisions are fixed.  DPF comparisons must use
paired seeds, particle ladders, and evaluator-variance reporting.

Target-mismatch risk:
Native SV, transformed SV, KSC mixture SV, generalized SV, additive-Gaussian
SIR closures, and predator-prey closures are distinct targets.  Same-target
evidence must state the observation law, state law, parameter vector, and any
Jacobian terms.

Gradient-risk:
Value agreement does not imply gradient correctness.  Score comparisons require
the same parameterization, fixed branch decisions or an explicit stochastic
score contract, and reference-route stability.

Environment-risk:
All TensorFlow CPU-only commands must set `CUDA_VISIBLE_DEVICES=-1` before
TensorFlow import.  GPU execution requires a separate trusted GPU plan.

## Evidence Contract

Question:

Can BayesFilter DPF methods be compared fairly against exact or approximation
filter routes for value and gradients, and which model/filter pairs support
oracle-grade, approximation-grade, diagnostic-only, or blocked claims?

Baselines and comparators:

- exact Kalman value and analytic gradient for LGSSM;
- dense/refined quadrature value and gradient for tiny nonlinear targets;
- exact transformed or finite-mixture Kalman references where the target is
  conditionally Gaussian;
- UKF, SVD/sigma-point, CUT4, and Zhao-Cui/fixed-design TT routes only after
  target-route classification;
- DPF bootstrap-OT and LEDH-PFPF-OT with paired random seeds and particle
  ladders.

Primary program criterion:

- produce a reviewed target-route registry;
- run exact-oracle rows before approximation rows;
- separate value gates from gradient gates;
- report DPF Monte Carlo uncertainty separately from bias;
- end with a closeout that lists promoted rows, diagnostic-only rows, blocked
  rows, and nonclaims.

Veto diagnostics:

- filter route used outside its declared target;
- approximate comparator called an oracle without proof;
- value agreement used to excuse a gradient mismatch;
- gradients compared in different parameterizations;
- finite differences used as a sole promotion gate;
- DPF same-dataset evaluator variance not reported for stochastic rows;
- branch, tolerance, fixture, particle count, or target changed after results
  without a reviewed amendment;
- HMC, production API, public API, paper-scale, GPU, DSGE, or deployment claim
  appears without separate evidence.

Explanatory-only diagnostics:

- runtime, ESS, resampling count, Sinkhorn residual, point count, quadrature
  order, TT rank, fit residual, branch hash, finite AD/FD checks, and local
  smoothness diagnostics.

What will not be concluded:

- no DPF scientific correctness from one row;
- no stochastic-resampling distribution correctness unless separately tested;
- no gradients through random/discrete branch choices unless explicitly
  contracted;
- no HMC readiness;
- no production score API readiness;
- no paper-scale Zhao-Cui or FilterFlow reproduction.

## Claim Class Definitions

Every target-route row must use exactly one of these classes.

`EXACT_ORACLE`:
The route evaluates the declared target exactly up to numerical linear algebra
or a reviewed refinement tolerance.  Examples are Kalman on LGSSM and dense
quadrature after refinement convergence on a tiny target.

`CERTIFIED_APPROXIMATION`:
The route is not exact, but its value and, when relevant, gradient error have
been certified against an `EXACT_ORACLE` or refined same-target reference on the
declared fixture, parameterization, horizon, and resource cap.  Certification
must state the empirical error band or theorem/bound used.  It is not an
oracle, and its certificate does not transfer to other targets or dimensions.

`SURROGATE_USEFULNESS`:
The route defines a useful approximate target or score for downstream
experiments, but exact-target correctness is not claimed.

`DIAGNOSTIC_ONLY`:
The route is useful for debugging, scale setting, or hypothesis formation only.

`BLOCKED`:
The route lacks a target definition, implementation, reference, parameter
contract, or numerical stability evidence needed for comparison.

Every registry row must also include `promotion_tolerance` and
`certification_band` fields.  For exact-target rows these fields define value
and gradient tolerances or reference-refinement bands.  For approximation rows
they define the empirical certificate scope.  For diagnostic or blocked rows
they must be `N/A` with a reason.

## DPF Stochastic Evidence Minimums

For any DPF row promoted beyond diagnostic status:

- use at least five independent paired seeds at the smallest particle count;
- use at least two particle counts, default `N_small` and `N_large`;
- add a third particle count when either the 95% confidence interval for mean
  value error excludes zero by more than the row tolerance, the relative score
  error confidence interval overlaps the suspicious band from P42, or the
  larger particle count does not reduce value RMSE or score RMSE by at least
  25%;
- report mean error, standard error, 95% confidence interval, RMSE, and maximum
  absolute error;
- record common-random-number policy, branch-freeze policy, and whether the
  gradient is fixed-branch or stochastic-score evidence.

These defaults may be changed only before execution through a reviewed
amendment.

## Gradient Estimand Contract

Every gradient row must declare one primary gradient object before execution:

`fixed_branch_score`:
Gradient of the declared scalar with observations, random numbers, ancestor
indices, branch decisions, resampling masks, and transport settings fixed.

`crn_pathwise_score`:
Common-random-number pathwise gradient of the declared scalar over continuous
random inputs, with discrete choices fixed or made differentiable by an
explicit reviewed mechanism.

`reference_score`:
Exact, refined, or otherwise certified score of the declared target in the
declared parameterization.

The scalar differentiated by AD, directional derivatives, finite differences,
or analytic recursion must be named.  Gradient evidence cannot mix these
objects in one promoted metric table.

## Phase Map

| Phase | Subplan | Purpose | Required outcome token |
| --- | --- | --- | --- |
| P0 | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p0-target-route-registry-subplan-2026-06-08.md` | create target-route registry and claim classes | `PASS_P0_TARGET_ROUTE_REGISTRY_READY_FOR_P1` |
| P1 | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p1-lgssm-exact-oracle-subplan-2026-06-08.md` | compare DPF and deterministic filters against LGSSM Kalman value and analytic gradient | `PASS_P1_LGSSM_EXACT_ORACLE_READY_FOR_P2` |
| P2 | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-subplan-2026-06-08.md` | tiny nonlinear dense/refined quadrature oracle rows | `PASS_P2_TINY_NONLINEAR_DENSE_ORACLE_READY_FOR_P3` |
| P3 | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-subplan-2026-06-08.md` | transformed SV or mixture/Kalman oracle rows | `PASS_P3_CONDITIONAL_GAUSSIAN_READY_FOR_P4` |
| P4 | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-subplan-2026-06-08.md` | classify Zhao-Cui/fixed-design TT routes and blocked multistate rows | `PASS_P4_ZHAOCUI_ROUTE_CLASSIFICATION_READY_FOR_P5` |
| P5 | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-subplan-2026-06-08.md` | DPF multi-seed particle-ladder value and gradient closeness | `PASS_P5_DPF_STATISTICAL_CLOSENESS_READY_FOR_P6` |
| P6 | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-subplan-2026-06-08.md` | cross-filter error scale and likelihood/score calibration | `PASS_P6_CROSS_FILTER_CALIBRATION_READY_FOR_P7` |
| P7 | `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-integration-closeout-subplan-2026-06-08.md` | final ledger, blockers, and next implementation actions | `PASS_P7_FILTER_COMPARISON_CLOSEOUT` |

Required order:

```text
P0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6 -> P7
```

P2-P4 may add blocked rows without stopping the program.  P5 must use only rows
that P0-P4 classify as runnable with an exact or approximation reference.

## Review Protocol

Codex is the supervisor and executor.  Claude is read-only critical reviewer
only.

Plan review:

- review the master program and all P0-P7 subplans;
- Claude must not edit files, run experiments, launch agents, or change state;
- Claude must end with exactly `VERDICT: AGREE` or `VERDICT: REVISE`;
- Codex audits every Claude finding and patches accepted findings;
- loop until convergence or maximum five iterations;
- at five iterations, unresolved material findings make the plan
  `BLOCKED_FOR_HUMAN_REVIEW`, not accepted by exhaustion.

Each later numerical phase must repeat the same max-five review loop for its
result or blocker note before promotion.

Review ledger:

`docs/plans/bayesfilter-dpf-filter-oracle-comparison-claude-review-ledger-2026-06-08.md`

## Per-Phase Artifact Contract

Each phase must predeclare and then write or explicitly mark blocked:

- phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p<N>-<slug>-result-2026-06-08.md`;
- phase Claude review ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p<N>-claude-review-ledger-2026-06-08.md`;
- machine-readable artifact when numerical or registry data are produced:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p<N>_<slug>_2026-06-08.json`;
- run manifest with git commit, command, environment, CPU/GPU status, seed
  list, particle counts when applicable, output paths, plan path, result path,
  and wall time.

Run-manifest rule:

- numerical, registry, or closeout JSON artifacts must include top-level
  `run_manifest`;
- markdown reports and phase results must summarize the same manifest;
- if a phase blocks before a command is run, the result must include
  `blocker_manifest` with the failed precheck, missing command, or missing
  reference route instead of silently omitting the manifest.

Required phase-result sections:

- skeptical plan audit before execution;
- evidence contract;
- pre-mortem;
- run or blocker manifest;
- decision table;
- veto diagnostics;
- post-run red-team note for executed numerical phases, or post-blocker
  red-team note for blocked phases;
- nonclaims.

Each phase review ledger must record iteration number, prompt summary, Claude
verdict, Codex classification of each finding, patch/control added, and the
decision to rerun, pass, or block.  The per-phase loop stops after five
iterations with `BLOCKED_FOR_HUMAN_REVIEW` if material findings remain.

## Planned Runner Convention

Subplans name intended runner modules so future execution has a stable command
contract.  These modules are not claimed to exist at plan-review time.

Each phase `PRECHECK` must do one of the following before execution:

- implement the named runner and validate it with a focused compile/import or
  `--validate-only` command;
- select an existing runner through a reviewed amendment while preserving the
  same artifacts and evidence contract;
- write a blocker result if no runner or reference route can be made
  executable without changing the reviewed plan.

Absence of a named runner during plan review is not a phase pass and must not be
treated as an executable command contract.

## Default Execution Policy

This document creates a planning lane only.  It does not authorize long
experiments, GPU runs, dependency installs, or detached execution.

Default command posture for later CPU-only TensorFlow runs:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp <command>
```

Any GPU, long-horizon, paper-scale, or HMC run requires a separate experiment
plan and trusted-context approval.

## Nonclaims To Preserve

- no new numerical comparison has been executed by this plan;
- no DPF correctness claim;
- no BayesFilter default-policy change;
- no FilterFlow, student, TT, UKF, SVD, CUT4, or Zhao-Cui oracle claim outside
  a classified target route;
- no production, HMC, DSGE, GPU, scalability, deployment, or public API claim.
