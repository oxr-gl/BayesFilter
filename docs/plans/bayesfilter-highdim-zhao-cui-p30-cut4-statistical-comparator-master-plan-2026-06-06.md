# BayesFilter Highdim P30 CUT4 Statistical Comparator Master Plan

metadata_date: 2026-06-06
phase: P38-CUT4

## Scope

Build a governed CUT4 statistical-comparator test layer for the P30
Zhao--Cui/highdim model suite.  The layer is a validation companion to the
P37 model-suite gates, not a replacement for exact references, dense
quadrature references, paper-scale validation, or adaptive Zhao--Cui
TT-cross/SIRT reproduction.

## Governing Sources

- Source governance charter:
  `docs/plans/bayesfilter-highdim-zhao-cui-source-governance-charter-2026-06-05.md`
- Current traceability ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md`
- P30 model-suite master program:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`
- P30 mathematical specification:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- CUT4 value and score code:
  `bayesfilter/nonlinear/svd_cut_tf.py`,
  `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`

## Evidence Contract

Question: where CUT4 is computationally and semantically feasible, do small
BayesFilter highdim/P30 candidate rows agree with CUT4 in a paired statistical
equivalence sense, and where it is not feasible or not semantically meaningful,
do the tests explicitly block overclaiming?

Baselines and comparators:

- affine LGSSM: exact Kalman remains the primary exact reference; CUT4 is a secondary
  deterministic comparator that must agree with both the highdim exact path and
  exact Kalman;
- stochastic volatility: native P30 heteroskedastic observation density is not
  represented by the current additive-Gaussian CUT4 filter, so direct CUT4
  comparison is `COMPARATOR_NOT_APPLICABLE` until a separate, reviewed
  heteroskedastic Gaussian-closure comparator exists;
- spatial SIR and predator-prey: CUT4 is feasible as a small Gaussian-closure
  diagnostic comparator, but current BayesFilter highdim evidence is only
  model-contract evidence, so the first gate records feasibility and blocks
  candidate-equivalence claims;
- stress rows: CUT4 is feasible only on small augmented dimensions and is
  diagnostic-only unless tied to an exact or value-validated candidate;
- fixed-branch gradient rows: CUT4 score comparison is meaningful only on
  certified smooth structural branches with production first-order CUT4 score;
  no production CUT4 Hessian claim is allowed.

Primary promotion criterion:

- each model family receives either a passing statistical-equivalence row or an
  explicit `COMPARATOR_NOT_APPLICABLE` / `DIAGNOSTIC_ONLY` row with non-claims;
- implemented rows must pass local tests, preserve source governance, and
  update the traceability ledger without promoting CUT4 as nonlinear truth.

Veto diagnostics:

- treating CUT4 as nonlinear ground truth;
- requiring machine-exact equality for nonlinear candidate-vs-CUT4 rows;
- missing P30/paper/MATLAB/BayesFilter anchors for a promoted claim;
- nonfinite value or score;
- active floor or weak spectral gap on score rows;
- CUT4 point-count explosion beyond the declared small-fixture cap;
- candidate/comparator semantic mismatch;
- public API, HMC, DSGE, GPU, paper-scale, or adaptive MATLAB overclaim.

Explanatory-only diagnostics:

- paired mean error, paired standard error, CI half-width, max absolute paired
  error, point count, wall time, branch hash, fixture seed, and comparator
  feasibility reason.

What will not be concluded:

- no full Zhao--Cui reproduction;
- no adaptive MATLAB TT-cross/SIRT reproduction;
- no paper-scale validation;
- no GPU/HMC/DSGE readiness;
- no stable top-level highdim API;
- no stable end-to-end score API;
- no claim that CUT4 is ground truth for nonlinear models;
- no production CUT4 Hessian support.

## Statistical Equivalence Rule

For rows with executable candidate and CUT4 comparator values, compute paired
errors on a fixed audit set:

```text
error_i = candidate_i - comparator_i.
```

The first-gate CI rule is a paired normal-approximation interval:

```text
mean(error) +/- 1.96 * sd(error) / sqrt(n).
```

A row passes first-gate equivalence only if:

- all paired values and errors are finite;
- the CI lies inside the declared equivalence band;
- the max absolute paired error is inside the declared outlier band;
- all comparator branch/floor/spectral diagnostics pass;
- the result ledger records that this is statistical equivalence to a
  comparator, not truth.

Exact affine LGSSM rows may additionally use exact Kalman tolerances, but the
CUT4 bridge still records the paired statistical row.

## Phase Map

| Phase | Subplan | Comparator status |
|---|---|---|
| P38-C0 | `bayesfilter-highdim-zhao-cui-p30-cut4-lgssm-subplan-2026-06-06.md` | exact Kalman plus CUT4 equivalence |
| P38-C1 | `bayesfilter-highdim-zhao-cui-p30-cut4-sv-subplan-2026-06-06.md` | native direct CUT4 not applicable |
| P38-C2 | `bayesfilter-highdim-zhao-cui-p30-cut4-sir-subplan-2026-06-06.md` | small CUT4 feasibility diagnostic only |
| P38-C3 | `bayesfilter-highdim-zhao-cui-p30-cut4-predator-prey-subplan-2026-06-06.md` | small CUT4 feasibility diagnostic only |
| P38-C4 | `bayesfilter-highdim-zhao-cui-p30-cut4-stress-subplan-2026-06-06.md` | small-dimension feasibility/resource guard |
| P38-C5 | `bayesfilter-highdim-zhao-cui-p30-cut4-fixed-branch-gradient-subplan-2026-06-06.md` | smooth-branch score comparator where meaningful |
| P38-C6 | result/closeout ledger | traceability and non-claim reconciliation |

## Required Traceability Rows Before Execution

The execution patch must add or update these traceability-ledger rows before a
P38 claim is promoted:

| CUT4 row | P30 anchor | Paper / MATLAB anchor | BayesFilter status | Required note |
|---|---|---|---|---|
| P38 LGSSM exact-plus-CUT4 bridge | P30 exact-reference LGSSM benchmark | Zhao--Cui Section 6.1; `eg1_kalman/*` audit anchors | `SOURCE_MATCHED` for exact Kalman value path; CUT4 is secondary comparator | exact Kalman remains the primary exact reference; CUT4 exercises the comparator harness |
| P38 SV direct-CUT4 boundary | P30 SV equations `eq:p27-sv1`--`eq:p27-sv6` | Zhao--Cui Section 6.2; `eg2_sv/mainscript.m` | `BAYESFILTER_EXTENSION` / comparator boundary | native heteroskedastic SV is not the additive-Gaussian CUT4 observation contract |
| P38 SIR Gaussian-closure diagnostic | P30 SIR equations as model-contract context only | Zhao--Cui SIR benchmark; `eg3_sir/*` audit anchors | `BAYESFILTER_EXTENSION` | clean-room additive-Gaussian closure diagnostic, not native SIR TT/SIRT filtering and not candidate equivalence |
| P38 predator-prey Gaussian-closure diagnostic | P30 predator-prey equations as model-contract context only | Zhao--Cui predator-prey/preconditioning context; `eg4_predatorprey/*` audit anchors | `BAYESFILTER_EXTENSION` | clean-room additive-Gaussian closure diagnostic, not nonlinear preconditioning usefulness evidence |
| P38 CUT4 stress feasibility guard | P30 stress-ladder equations and P37 M5 manifest governance | BayesFilter extension beyond paper model reproduction | `BAYESFILTER_EXTENSION` | point-count/resource diagnostic only; no correctness or scalability promotion |
| P38 CUT4 smooth-score sanity | P30 fixed-branch derivative sections as context | no Zhao--Cui stable score API; MATLAB has no audited BayesFilter score API | `BAYESFILTER_EXTENSION`; end-to-end score API remains `BLOCKED_UNVALIDATED` | first-order CUT4 score sanity only; no production Hessian, stable score API, HMC, or DSGE readiness |

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW`.

Wrong baselines: avoided.  Exact LGSSM keeps exact Kalman as exact reference.  Nonlinear
P30 rows do not use CUT4 as truth.

Proxy metrics as promotion criteria: avoided.  Feasibility, point count,
finiteness, and wall time are diagnostic-only unless paired equivalence is
explicitly available.

Missing stop conditions: addressed through point-count caps, finite-value
vetoes, branch/floor/spectral vetoes, and `COMPARATOR_NOT_APPLICABLE` rows.

Unfair comparisons: avoided.  Candidate-vs-CUT4 equivalence is only declared
when both operate on the same semantic model and fixed audit data.

Hidden assumptions: surfaced.  Native SV heteroskedastic observations are not
the additive-Gaussian CUT4 observation contract.  SIR and predator-prey
currently have model-contract evidence, not highdim candidate filters.

Stale context: checked against P37 closeout and traceability; current blockers
remain intact.

Commands whose artifacts would not answer the question: blocked.  The first
gate runs focused tests under `tests/highdim` and records result ledgers rather
than broad stress commands.

## Source-Governance Status

- P30 anchors identified: yes, through P30 model-suite equations and previous
  P37 phase anchors.
- Zhao--Cui paper anchors identified: yes, model-suite sections by family.
- MATLAB behavioral anchors identified: yes, as audit/reference anchors only.
- BayesFilter code/test anchors identified: planned for the new CUT4 tests.
- Deviations listed: yes, especially SV direct-CUT4 non-applicability and
  SIR/predator-prey diagnostic-only status.
- Clean-room boundary respected: yes, no MATLAB code is copied or ported.
- Unsupported claims removed: yes.
- Reviewer verdict: pending Claude review.

## Planned Commands

CPU-only deliberate guardrail:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_cut4_statistical_comparators.py
```

Broader CPU-only regression after local pass:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py tests/highdim
```

Static checks:

```bash
python -m compileall -q bayesfilter/highdim tests/highdim
git diff --check
```
