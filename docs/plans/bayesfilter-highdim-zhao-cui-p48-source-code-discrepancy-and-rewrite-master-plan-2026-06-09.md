# P48 Master Plan: Zhao--Cui Source-Code Discrepancy Audit And BayesFilter Rewrite Decision

metadata_date: 2026-06-09
program: P48-source-code-discrepancy-and-rewrite
supervisor: Codex
reviewer: Claude Code read-only
status: PLAN_REVIEW_PASSED_EXECUTION_STARTED

## Objective

Re-audit the Zhao--Cui companion code against the BayesFilter high-dimensional
implementation and decide, discrepancy by discrepancy, whether BayesFilter
should keep its current implementation choice, rewrite toward the source-code
choice, or run scientific tests before choosing.

This plan treats the old P10/P34 source audits as valid source-understanding
artifacts, but not as evidence that BayesFilter has implemented the same
algorithmic route.

## Evidence Contract

Question: where does the BayesFilter implementation differ from the
Zhao--Cui paper/code route, which differences matter, and what should be
rewritten or experimentally decided?

Baseline/comparator:

- Source route: Zhao--Cui companion code snapshots
  `third_party/audit/tensor-ssm-paper-demo` and
  `third_party/audit/zhao_cui_tensor_ssm_p10/source`, especially
  `models/Y_sol.m`, `models/full_sol.m`, `models/pre_sol.m`,
  `deep-tensor.dev/src/@TTFun/*`, `deep-tensor.dev/src/@TTSIRT/*`,
  `deep-tensor.dev/src/AbstractIRT.m`, and examples `eg1`--`eg4`.
- BayesFilter route: `bayesfilter/highdim/*`, especially `fitting.py`,
  `filtering.py`, `squared_tt.py`, `transport.py`, `tt.py`, `models.py`,
  and P30--P47 tests/artifacts.

Primary criterion:

- A discrepancy ledger exists with source-code anchor, BayesFilter anchor,
  implementation difference, affected claims, severity, decision
  (`source_wins`, `bayesfilter_wins`, `split_lanes`, `test_required`,
  `documentation_only`, or `blocked`), and next action.
- Every material discrepancy has either a clear winner with justification or a
  test plan capable of deciding scientifically.
- The result artifact names which BayesFilter routes should be rewritten before
  future paper-scale claims.

Veto diagnostics:

- Any promoted claim that BayesFilter reproduces adaptive MATLAB TT/SIRT without
  evidence.
- Any comparison that treats fixed-design retained-grid behavior as equivalent
  to source adaptive/random TT/SIRT.
- Any rewrite recommendation that violates the TensorFlow/TFP backend policy
  without a reviewed exception.
- Any scientific test that lacks a baseline, pass/fail criterion, veto
  diagnostic, and non-claims.
- Any attempt to copy LGPL/GPL MATLAB code into production Python.

Explanatory diagnostics:

- Existing unit tests and P30--P47 artifacts.
- Static line anchors and source-code structure.
- Complexity formulas, ESS behavior, condition-number behavior, and finite
  smoke outcomes.

What will not be concluded:

- No code rewrite will be declared complete in P48 unless a separate patch and
  focused tests are added.
- No adaptive-route differentiability claim is made.
- No paper-figure reproduction or S&P 500 reproduction is in scope.
- No HMC readiness claim follows from this audit alone.

Artifacts:

- Master plan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p48-source-code-discrepancy-and-rewrite-master-plan-2026-06-09.md`
- Claude plan review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p48-source-code-discrepancy-and-rewrite-claude-review-ledger-2026-06-09.md`
- Discrepancy ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p48-source-code-discrepancy-ledger-2026-06-09.md`
- Decision matrix:
  `docs/plans/bayesfilter-highdim-zhao-cui-p48-implementation-choice-decision-matrix-2026-06-09.json`
- Scientific test ladder:
  `docs/plans/bayesfilter-highdim-zhao-cui-p48-scientific-decision-test-ladder-2026-06-09.md`
- Execution result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p48-source-code-discrepancy-and-rewrite-result-2026-06-09.md`

## Skeptical Plan Audit

Status: PASSED_AND_EXECUTED.

- Wrong baseline risk: P48 compares against source code and the paper-code
  crosswalk, not against P46/P47 fixed-design substitutes as if they were the
  source route.
- Proxy promotion risk: existing small fixed-design tests can explain local
  correctness but cannot certify paper-scale or adaptive-route equivalence.
- Hidden assumption risk: adaptive/random TT/SIRT may be better for filtering
  scalability and worse for HMC differentiation; the plan allows split lanes.
- Environment mismatch risk: MATLAB execution is not required for the static
  discrepancy audit; if a source smoke is used, it must be labeled as smoke or
  blocked by environment.
- Artifact adequacy risk: the decision matrix is machine-readable, and the
  markdown ledger preserves source and BayesFilter anchors.
- Stop condition: if the source code cannot be read or a material discrepancy
  cannot be classified from static evidence, mark `blocked` or `test_required`
  instead of inventing a winner.

## Phase Plan

### P48-M0: Source And BayesFilter Surface Inventory

Read and summarize:

- source examples `eg1_kalman`, `eg2_sv`, `eg3_sir`, `eg4_predatorprey`;
- source solvers `Y_sol.m`, `full_sol.m`, `pre_sol.m`;
- source TT/SIRT core classes `TTFun`, `TTIRT`, `TTSIRT`, `SIRT`,
  `AbstractIRT`;
- BayesFilter highdim modules and tests that implement fixed-branch TT,
  retained filters, scalar/multistate value paths, and model fixtures.

Gate: inventory must list all compared surfaces and existing non-claim guards.

### P48-M1: Discrepancy Ledger

Create a ledger over implementation-choice classes:

1. adaptive/random/fixed-rank fitting;
2. retained representation after each time step;
3. transition propagation route;
4. squared density and defensive term;
5. coordinate maps and preconditioning;
6. sampling, ESS, and particle correction;
7. smoothing/backward path;
8. gradient and branch differentiability;
9. model contracts for SV, generalized SV, spatial SIR, predator-prey;
10. license/runtime/backend boundary;
11. diagnostics and pass-token governance.

Gate: each row must identify source anchor, BayesFilter anchor, severity,
decision, and next action.

### P48-M2: Winner Or Split-Lane Decision

For each discrepancy:

- pick source if it is clearly better for source-faithful filtering and does
  not violate a hard BayesFilter constraint;
- pick BayesFilter if it is clearly better for deterministic gradients,
  TensorFlow integration, or governance and the source choice is not needed for
  the claimed route;
- split lanes when the source choice is better for paper-scale filtering but
  BayesFilter's choice is better for HMC/fixed-branch differentiation;
- require tests when neither choice dominates.

Gate: no `source_wins` or `bayesfilter_wins` decision without a stated claim
target.

### P48-M3: Scientific Decision Test Ladder

For `test_required` and `split_lanes` items, define tests with:

- scientific question;
- exact source-faithful or clean-room route under test;
- comparator/baseline ladder;
- pass/fail metric;
- veto diagnostics;
- explanatory diagnostics;
- non-claims;
- artifact path.

Gate: tests must not require impossible paper-scale execution before a smaller
diagnostic rung.

### P48-M4: Rewrite Roadmap

Classify rewrite work:

- immediate documentation/governance correction;
- clean-room source-faithful filtering lane;
- deterministic fixed-branch gradient lane;
- shared infrastructure improvement;
- blocked pending MATLAB/source execution or license decision.

Gate: no implementation edit is made in P48 unless it is purely artifact or
test-governance documentation. Code rewrite follows in a separate reviewed P49
or later plan.

### P48-M5: Result Review

Run focused validation on artifacts and ask Claude for read-only review. Claude
must check whether the ledger honestly separates source-faithful filtering,
fixed-branch BayesFilter implementation, and future scientific tests.

## Claude Review Loop

Use up to five plan-review iterations. Stop early if Claude returns a clear
pass token. If iteration 5 still has minor comments but no major blocker, accept
iteration 5 and record the residual minor risks. If Claude identifies a major
blocker at iteration 5, stop and record `BLOCKED_P48_PLAN_MAJOR_REVIEW_ISSUE`.

Plan pass token:

```text
PASS_P48_SOURCE_CODE_DISCREPANCY_REWRITE_PLAN
```

Result pass token:

```text
PASS_P48_SOURCE_CODE_DISCREPANCY_REWRITE_RESULT
```

## Planned Local Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p48-implementation-choice-decision-matrix-2026-06-09.json
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p48-*
```

No GPU command is planned. The CPU-only environment hides GPU intentionally.

## Execution Status

Plan review passed with Claude token
`PASS_P48_SOURCE_CODE_DISCREPANCY_REWRITE_PLAN`.

Execution artifacts were created on 2026-06-09:

- `docs/plans/bayesfilter-highdim-zhao-cui-p48-source-code-discrepancy-ledger-2026-06-09.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p48-implementation-choice-decision-matrix-2026-06-09.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p48-scientific-decision-test-ladder-2026-06-09.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p48-source-code-discrepancy-and-rewrite-result-2026-06-09.md`
