# Master Program: Fixed-SGQF Testing and Comparison Gap Closure

metadata_date: 2026-06-14
program_id: fixed-sgqf-testing-and-comparison
status: DRAFT_REVIEW_READY

## Date

2026-06-14

## Status

`DRAFT_REVIEW_READY`

This document is the controlling roadmap for the fixed-SGQF testing and
comparison lane.  It organizes the current evidence, the remaining gaps, the
phase order, the artifact contract, and the review discipline before any longer
execution ladder begins.

## Purpose

The purpose of this program is to close the known testing and comparison gaps
for the TensorFlow fixed-SGQF value and score paths implemented in:

- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`

The goal is not to redesign the algorithm or to claim general scientific
superiority.  The goal is to expand local evidence in a governed way so that a
future worker can say, precisely and honestly, what the fixed-SGQF lane is
supported for on the currently tested fixtures.

This program therefore separates four evidence families that must not be merged
casually:

- exact affine/Kalman reference rows;
- dense numerical reference rows on tractable nonlinear fixtures;
- same-target baseline comparison rows against existing repo methods;
- branch/failure contract rows.

## Governing Constraints

This program is governed by:

- `AGENTS.md`
- project `CLAUDE.md`
- global `CLAUDE.md`
- BayesFilter TensorFlow/TFP backend policy
- BayesFilter research-engineering and evidence-discipline rules

Additional lane-specific constraints:

1. The default implementation backend remains TensorFlow / TensorFlow
   Probability.  New algorithmic behavior must not be specified as a NumPy
   production path.
2. CPU-only test commands must set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow
   import unless a separate trusted GPU plan explicitly opens a GPU lane.
3. Comparisons must be same-target.  No row may compare methods with different
   observation laws, state laws, parameterizations, or returned scalar meaning
   as though they were directly rankable.
4. The words `exact`, `oracle`, `dense numerical reference`, `baseline-only`,
   and `contract/failure` are controlled labels.  They must be used explicitly
   and only where justified.
5. Branch/failure evidence is part of the supported contract.  A clean failure
   record can be a passing test outcome for a contract phase.
6. Dense nonlinear reference rows are local numerical comparators on selected
   low-dimensional fixtures.  They must not be promoted into general nonlinear
   exactness claims.
7. Baseline ladders versus UKF/CUT4/SVD sigma-point routes are fixture-specific
   positioning evidence only.  They do not establish a universal method ranking.
8. Production-code edits are not the default objective of this program.  The
   default objective is tests and evidence artifacts.  Production files should
   change only when a phase discovers a genuine missing contract surface or
   missing diagnostic output.

## Current Evidence Base

The fixed-SGQF lane already has real local evidence.  The current foundation is
not a blank slate.

### Construction and cloud evidence

Existing tests cover:

- one-dimensional GHQ level rules;
- active multi-index and combination-coefficient checks for the current p47
  preview case;
- merged 3D level-2 cloud geometry, weight total, and covariance recovery.

Representative files:

- `tests/test_fixed_sgqf_tf.py`
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`

### Value-path evidence

Existing tests cover:

- 1D affine fixed-SGQF exact-vs-Kalman parity;
- p47 one-step scalar numeric oracle recovery;
- one-step scalar quadratic nonlinear comparison against a dense projection
  reference.

Representative files:

- `tests/test_fixed_sgqf_values_tf.py`
- `tests/test_fixed_sgqf_verification_tf.py`

### Score-path and branch-contract evidence

Existing tests cover:

- one-step analytic score versus centered finite difference on the accepted
  branch;
- same-branch-signature checks between value and score paths;
- branch-mismatch rejection;
- diagnostic snapshot and branch-summary helpers.

Representative files:

- `tests/test_fixed_sgqf_scores_tf.py`
- `tests/test_fixed_sgqf_branch_contract_tf.py`
- `tests/test_fixed_sgqf_testing_integration_tf.py`
- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`

### Failure/audit evidence

Existing tests cover:

- cloud weight-sum failure;
- predictive, innovation, and previous-covariance veto behavior;
- no-hidden-repair/no-adaptive-language checks.

Representative files:

- `tests/test_fixed_sgqf_audit_tf.py`
- `tests/test_fixed_sgqf_verification_tf.py`

## Remaining Gaps

This program treats the following as the current primary gaps.

### G1. Multistep nonlinear dense-reference accuracy

Current nonlinear accuracy evidence is strongest at one step.  We still need a
controlled multistep same-target ladder against dense numerical references on
tractable low-dimensional fixtures.

### G2. Higher-dimensional accepted-path validation

Current accepted-path numerical evidence is concentrated in 1D and in special
local fixtures.  We need explicit accepted-path rows in higher-dimensional
settings where the recursion is expected to pass.

### G3. Cloud exactness beyond the current small cases

Current cloud evidence is strong for the existing 1D and 3D level-2 fixtures,
but it is not yet a broader ladder across multiple `(dim, sparse_level)` cells
with explicit moment tests.

### G4. Later-time and later-stage failure coverage

Current failure tests are mostly early-stage or first-time-index failures.  We
need contract rows that fail after earlier accepted steps, including a direct
attempt to cover `carried_covariance` if that stage is reachable.

### G5. Broader score/finite-difference coverage

Current score evidence is concentrated in a one-parameter scalar one-step case.
We need multi-parameter, multistep, and broader accepted-branch score evidence
with explicit same-branch gating.

### G6. Multidimensional affine exact-vs-Kalman parity

Current exact affine evidence is strong in 1D but not yet a multidimensional
ladder with coupled dynamics, nontrivial covariance structure, and partial
observations.

### G7. Same-target baseline comparison ladder

The repo already contains UKF, CUT4, and SVD sigma-point routes, but the
fixed-SGQF lane is not yet positioned against them in a governed same-target
fixture panel.

### G8. Sparse-level ladder versus dense reference

We do not yet have a tested sparse-level ladder showing how fixed-SGQF behaves
against the same dense nonlinear comparator as sparse level increases on chosen
fixtures.

## Skeptical Plan Audit

Status: `PASS_TO_IMPLEMENTATION_PLANNING_WITH_REFERENCE_LADDER_GATES`

Wrong-baseline risk:
Exact Kalman is exact only on affine Gaussian rows.  Dense nonlinear references
are tractable numerical comparators only on selected low-dimensional fixtures.
Baseline comparisons against UKF/CUT4/SVD methods are same-target comparator
rows, not universal truth rows.

Proxy-promotion risk:
Finite values, stable Cholesky factors, visually plausible filtered means,
finite-difference agreement at one step, or improved sparse-level behavior are
useful diagnostics.  They do not by themselves establish general convergence,
global ranking, or production-default readiness.

Missing-stop-condition risk:
If a dense comparator ceases to be credible at a chosen horizon or dimension,
the phase must reduce the rung or stop.  It must not silently weaken the label
from `dense numerical reference` to a vaguer claim after the fact.

Branch-consistency risk:
Finite-difference score evidence is only comparable when the declared scalar and
the branch signature are the same.  Branch-leaving FD rows are blocked or
separately classified; they are not promotion rows.

Unfair-comparison risk:
A baseline row is valid only when model semantics, observation semantics,
parameterization, and reported scalar meaning agree.  Comparison convenience is
not a valid reason to compare different targets.

Environment risk:
CPU-only TensorFlow commands must declare that GPU devices are intentionally
hidden.  Non-escalated GPU failures, if any future worker probes them, are
sandbox evidence only.

Artifact-answer mismatch risk:
Every phase must predeclare what artifact will answer its question.  A phase
that runs tests but does not preserve a phase result, review ledger, and any
needed matrix/JSON artifact has not answered its question durably.

## Evidence Contract

Question:

Can the fixed-SGQF lane be extended from its current one-step/small-case local
evidence to a broader, governed testing ladder across multistep nonlinear,
multidimensional affine, cloud-exactness, branch/failure, score, sparse-level,
and same-target baseline-comparison regimes without overstating what the results
prove?

Baselines and comparators:

- exact Kalman on affine Gaussian rows;
- dense numerical references on tractable low-dimensional nonlinear rows;
- existing fixed-SGQF local contract tests;
- repo same-target sigma-point routes where eligible:
  - UKF / sigma-point route,
  - CUT4 route,
  - SVD sigma-point route;
- branch/failure contract rows that may intentionally fail and still pass the
  contract phase.

Primary program criterion:

- each gap G1-G8 is either closed with explicit evidence or converted into a
  reviewed blocker with a reason;
- each phase labels its rows correctly as exact-reference, dense-reference,
  baseline-only, or contract/failure;
- each phase ends with an artifact that preserves what passed, what failed, what
  remains uncertain, and what is not being concluded.

Veto diagnostics:

- a dense nonlinear comparator is called exact;
- a baseline-only row is summarized as an oracle row;
- different-target rows are directly ranked;
- a branch-leaving FD row is used as analytic-score promotion evidence;
- a later-time failure path is omitted from the result because the first step
  passed;
- a local sparse-level improvement is promoted to a general convergence claim;
- production-default or paper-scale claims appear without separate evidence.

Explanatory-only diagnostics:

- runtime;
- point count;
- weight total;
- negative-weight count;
- branch hash;
- same-branch signature;
- finite-difference step-size sensitivity;
- horizon-specific mismatch summaries;
- per-step local residual and covariance diagnostics.

What will not be concluded:

- no general nonlinear exactness claim;
- no universal SGQF convergence theorem;
- no universal ranking versus UKF/CUT4/SVD methods;
- no production-default policy change;
- no paper-scale high-dimensional readiness claim;
- no HMC readiness claim.

## Phase Map

| Phase | Subplan | Primary gaps | Purpose | Required outcome token |
| --- | --- | --- | --- | --- |
| P0 | `docs/plans/bayesfilter-fixed-sgqf-p0-inventory-and-evidence-contract-subplan-2026-06-14.md` | G1-G8 | freeze current coverage, gap mapping, comparator ladder, and tolerance language | `PASS_P0_FIXED_SGQF_INVENTORY_READY_FOR_EXECUTION_PHASES` |
| P1 | `docs/plans/bayesfilter-fixed-sgqf-p1-multistep-dense-reference-subplan-2026-06-14.md` | G1 | add multistep nonlinear dense-reference rows | `PASS_P1_FIXED_SGQF_MULTISTEP_DENSE_REFERENCE_READY_FOR_P3_P5_P6` |
| P2 | `docs/plans/bayesfilter-fixed-sgqf-p2-accepted-path-and-failure-ladder-subplan-2026-06-14.md` | G2, G4 | broaden accepted-path and late-failure contract coverage | `PASS_P2_FIXED_SGQF_ACCEPTED_PATH_AND_FAILURE_LADDER_READY_FOR_P5` |
| P3 | `docs/plans/bayesfilter-fixed-sgqf-p3-cloud-exactness-ladder-subplan-2026-06-14.md` | G3 | broaden cloud exactness/moment evidence | `PASS_P3_FIXED_SGQF_CLOUD_EXACTNESS_READY_FOR_P6_P7` |
| P4 | `docs/plans/bayesfilter-fixed-sgqf-p4-affine-kalman-ladder-subplan-2026-06-14.md` | G6 | extend affine exact-vs-Kalman parity to multidimensional rows | `PASS_P4_FIXED_SGQF_AFFINE_KALMAN_LADDER_READY_FOR_P7` |
| P5 | `docs/plans/bayesfilter-fixed-sgqf-p5-score-fd-ladder-subplan-2026-06-14.md` | G5 | broaden multi-parameter and multistep score evidence | `PASS_P5_FIXED_SGQF_SCORE_FD_LADDER_READY_FOR_P8` |
| P6 | `docs/plans/bayesfilter-fixed-sgqf-p6-sparse-level-vs-dense-ladder-subplan-2026-06-14.md` | G8 | add sparse-level ladders versus the same dense comparator | `PASS_P6_FIXED_SGQF_SPARSE_LEVEL_LADDER_READY_FOR_P8` |
| P7 | `docs/plans/bayesfilter-fixed-sgqf-p7-baseline-comparison-ladder-subplan-2026-06-14.md` | G7 | position fixed-SGQF against same-target repo baselines | `PASS_P7_FIXED_SGQF_BASELINE_COMPARISON_READY_FOR_P8` |
| P8 | `docs/plans/bayesfilter-fixed-sgqf-p8-closeout-and-claim-audit-subplan-2026-06-14.md` | synthesis | close the program with supported claims, unsupported claims, and next steps | `PASS_P8_FIXED_SGQF_CLOSEOUT_COMPLETE` |

## Recommended Execution Ladder

The phase identifiers and the recommended execution order are intentionally not
identical.

Recommended execution order:

```text
P0 -> P4 -> P2 -> P1 -> P3 -> P5 -> P6 -> P7 -> P8
```

Rationale:

- P4 gives strong low-ambiguity exact-reference evidence early.
- P2 stabilizes the branch/failure contract before wider score and comparison
  work.
- P1 then broadens nonlinear reference evidence.
- P3 deepens trust in the cloud-construction surface.
- P5, P6, and P7 depend on the earlier ladders for honest interpretation.
- P8 closes the program only after the comparison and derivative ladders exist.

## Review Protocol

Codex/Claude-style future execution workers must preserve a read-only critical
review loop for every phase result.

Plan/package review:

- review the master program and all P0-P8 subplans before execution begins;
- the reviewer must be read-only and must not mutate the repo while reviewing;
- every review note must classify issues as material, wording-only, or
  non-issue;
- unresolved material issues block phase execution until the plan text is
  amended.

Per-phase result review:

- each phase result must be reviewed before promotion to the next dependent
  phase;
- a phase may proceed with partial closure only if the result explicitly marks
  the uncovered or blocked rows;
- a clean blocker is preferable to an overclaimed pass.

## Artifact Contract

Each execution phase must predeclare and then write, or explicitly mark blocked:

- a phase result note:
  `docs/plans/bayesfilter-fixed-sgqf-p<N>-<slug>-result-2026-06-14.md`
- a phase review ledger:
  `docs/plans/bayesfilter-fixed-sgqf-p<N>-claude-review-ledger-2026-06-14.md`
- a machine-readable matrix or JSON artifact when a phase produces structured
  comparison data, moment tables, or coverage matrices;
- a run manifest with git commit, command, environment, CPU/GPU status,
  tolerance policy, seed list when applicable, output paths, plan path, result
  path, and wall time.

Planning-package artifacts created immediately by this program:

- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-p0-inventory-and-evidence-contract-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-p1-multistep-dense-reference-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-p2-accepted-path-and-failure-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-p3-cloud-exactness-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-p4-affine-kalman-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-p5-score-fd-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-p6-sparse-level-vs-dense-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-p7-baseline-comparison-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-p8-closeout-and-claim-audit-subplan-2026-06-14.md`

## Stop Rules

Stop and amend the program or phase before execution if any of the following
becomes true:

1. A proposed comparator does not preserve same-target semantics.
2. A proposed row would require calling a dense nonlinear comparator exact.
3. A phase depends on a branch or diagnostic surface that is not currently
   exposed and the required production edit would be larger than a local test
   support change.
4. A later-time failure row cannot be made deterministic enough for contract
   testing with the current fixture/tolerance design.
5. A score/FD row cannot preserve the same scalar and same-branch condition.
6. The only way to make a phase pass is to weaken its claim label after seeing
   results.
7. The worker is about to interpret a local ladder as evidence for production
   default, high-dimensional asymptotics, or general convergence.

## Exit Criteria

The master program exits successfully only if:

- every gap G1-G8 is either closed or explicitly marked blocked with a reason;
- every phase produced the required artifact class or a blocker artifact;
- the final closeout lists supported claims and unsupported claims separately;
- the final closeout states what evidence is exact-reference, what evidence is
  dense-reference, what evidence is baseline-only, and what evidence is purely
  contract/failure;
- no phase result relies on an unsupported scientific, asymptotic, or
  production-readiness leap.
