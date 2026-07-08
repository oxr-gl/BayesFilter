# BayesFilter Quadratic MAP-Covariance Initializer Master Program

Date: 2026-07-08

## Status

`DRAFT_MASTER_PROGRAM`

## Objective

Create a reusable BayesFilter initializer that uses a finite local optimizer only
as a neighborhood locator, then fits a constrained SPD quadratic log-posterior
surrogate to produce a covariance or precision candidate for later HMC tuning.

The program must not certify a global MAP, posterior covariance correctness,
HMC convergence, Zhao-Cui source faithfulness, production default readiness, or
scientific superiority.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can a BFGS-located local neighborhood plus constrained SPD quadratic fit provide a reusable, finite, well-conditioned covariance initializer artifact? |
| Mechanism under test | BFGS or fallback locator for a local center; local design cloud; `fit_low_rank_spd_quadratic_geometry`; analytic surrogate mode; `covariance_from_precision` regularization. |
| Expected failure mode | Locator does not converge, local design has too few finite points, fit residuals reject, surrogate mode leaves trust region, or precision/covariance conditioning is unusable. |
| Primary promotion criterion | Unit tests on controlled Gaussian/quadratic targets demonstrate correct sign convention, mode/covariance recovery within stated tolerances, fail-closed nonfinite handling, and clear API payload nonclaims. |
| Promotion veto | Nonfinite accepted result, indefinite accepted precision, BFGS inverse Hessian used as covariance authority, unsupported MAP/HMC claim, missing sample-budget guard, or missing focused tests. |
| Continuation veto | Broken import/compile path, missing local artifacts, inability to run focused tests, or review nonconvergence after five rounds for the same material blocker. |
| Repair trigger | Any fixable unit-test failure, review finding, sign mismatch, boundary-language finding, or artifact mismatch. |
| Explanatory diagnostics | Locator status, log-probability changes, finite sample count, fit residuals, holdout residuals, eigen summaries, condition number, trust-region displacement, gradient norm when available. |
| What must not be concluded | Global MAP, posterior covariance correctness, HMC readiness, sampler convergence, default readiness, Zhao-Cui source faithfulness, or statistical superiority. |

## Phase Index

| Phase | Name | Objective | Required artifacts |
| --- | --- | --- | --- |
| 0 | Governance and API boundary | Converge on scope, evidence contract, current-code inventory, and implementation boundaries. | Phase 0 subplan, Claude/Codex review record, Phase 0 result, Phase 1 subplan. |
| 1 | Reusable initializer implementation | Add reusable dataclasses/config/API for locator plus SPD quadratic covariance initializer. | Source diff, tests drafted, Phase 1 result, Phase 2 subplan. |
| 2 | Focused unit validation | Validate Gaussian sign convention, covariance recovery, fallback handling, sample-budget behavior, payload nonclaims, and public exports. | Focused pytest log, result note, Phase 3 subplan. |
| 3 | Benchmark-local adoption smoke | Refactor or add a bounded benchmark-facing smoke that uses the reusable API without making HMC readiness claims. | Smoke artifact or explicit no-refactor result, focused test/log, Phase 3 result, Phase 4 subplan. |
| 4 | Closeout and handoff | Record final evidence, residual gaps, and exact next HMC-readiness gates. | Closeout result, reset memo or handoff, final review record. |

## Required Subplan Contract

Before each phase executes, the dedicated subplan must state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each subplan execution, Codex must:

1. run required local checks;
2. write a phase result or close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Design Boundary

BFGS, L-BFGS, or any optimizer output is a local point locator only. Its inverse
Hessian, optimizer status, or local convergence flag is not covariance authority.

The covariance candidate comes from the constrained SPD quadratic fit and
`covariance_from_precision` regularization. If that fit rejects, the initializer
must reject or return an explicitly unaccepted diagnostic result.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| TensorFlow/TFP target function interface | BayesFilter `AGENTS.md` default backend | Compatible with gradient-bearing BayesFilter code | NumPy-only implementation path sneaks into algorithmic API | Public function accepts TensorFlow `value_and_score_fn`; tests use TF target functions | reviewed default |
| NumPy inside quadratic fitting utility | Existing `quadratic_geometry.py` diagnostic utility | Existing accepted diagnostic implementation uses NumPy for regression/reporting | New code could become differentiable algorithmic path by accident | Nonclaims and module docs label it diagnostic initializer | inherited exception |
| BFGS as locator only | User directive and DSGE-HMC pattern | We need local finite center more than exact MAP | Treating optimizer curvature as covariance authority | Tests/assertions and result payload label covariance source as quadratic SPD fit | reviewed default |
| `n_samples >= 5 * n_regression_parameters` | User directive | Prevents underdetermined fit from being accepted | Fitting high-rank K with too little data | Config/result diagnostics record sample ratio and rank reduction/rejection | reviewed default |
| Condition cap on precision | Existing quadratic config and mass-matrix helpers | HMC mass initializer should be SPD and not extreme | Artificial cap hides true curvature | Report raw/regularized eigen summaries and nonclaims | hypothesis, not posterior claim |
| Optional benchmark adoption | Scope control | Reusable API should be tested before benchmark churn | Refactor hides implementation bug | Phase 3 may choose smoke over broad refactor | reviewed default |

## Skeptical Plan Audit

| Risk | Audit finding |
| --- | --- |
| Wrong baseline | Baseline is current benchmark-local MAP/covariance helpers plus existing `fit_low_rank_spd_quadratic_geometry`; no HMC baseline is used for promotion. |
| Proxy metric promoted | Fit residuals and short smokes are diagnostics only; pass criterion is focused correctness behavior on controlled targets. |
| Missing stop conditions | Each phase has stop conditions; review nonconvergence and failed focused checks stop the run. |
| Unfair comparison | No method superiority comparison is planned. |
| Hidden assumptions | Numeric defaults are labeled as inherited, reviewed, or hypothesis. |
| Stale context | Phase 0 inventory must inspect current `quadratic_geometry.py`, `mass_matrix.py`, and benchmark-local helpers before implementation. |
| Environment mismatch | Focused CPU-safe tests are allowed for smoke/unit checks; GPU/HMC evidence is out of scope. |
| Artifact mismatch | Required artifacts are source diffs, tests, logs, result notes, and review records that directly support the initializer question. |

Audit status: `PASSED_FOR_PHASE_0_PLANNING_REVIEW`.

## Claude Review Policy

Claude may be used only as a read-only reviewer through the project-local
review gate. Claude cannot authorize human, runtime, model-file, funding,
product, default-policy, public-benchmark, HMC-readiness, or scientific-claim
boundaries.

If the primary Claude review path fails, Codex must follow the review gate
status. A bounded fallback agreement is weaker than full review and must be
recorded as such. If Claude is unavailable and the plan permits fallback, a
fresh Codex review may replace Claude review only as a clearly labeled weaker
review signal.
