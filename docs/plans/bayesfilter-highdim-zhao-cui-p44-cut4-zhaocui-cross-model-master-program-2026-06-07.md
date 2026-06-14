# P44 Master Program: CUT4--Zhao-Cui Cross-Model Value and Gradient Tests

metadata_date: 2026-06-07
phase: P44

## Scope

Create a governed cross-model program for comparing CUT4 and Zhao--Cui style
fixed-design TT filtering on value and gradient diagnostics.  The program
covers exact linear baselines, clean same-target nonlinear additive-Gaussian
fixtures, and diagnostic-only closures for models whose native likelihood is
not currently a shared CUT4/Zhao--Cui target.

This is a planning artifact.  It authorizes later gated implementation phases
only after Claude plan review returns an explicit pass verdict.  Reaching the
maximum review count without a pass records a blocked carry-forward state; it
does not create launch, implementation, repair, or promotion authority.

## Governing Sources

- Source governance charter:
  `docs/plans/bayesfilter-highdim-zhao-cui-source-governance-charter-2026-06-05.md`
- P30 model-suite master program:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`
- P38 CUT4 comparator governance:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-cut4-statistical-comparator-master-plan-2026-06-06.md`
- P42 likelihood and gradient validation rules:
  `docs/plans/bayesfilter-highdim-zhao-cui-p42-gradient-likelihood-validation-rules-2026-06-07.md`
- P43 SV value/gradient result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p43-sv-value-gradient-cut4-zhaocui-result-2026-06-07.md`

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_WITH_SCOPE_RESTRICTIONS`.

- Wrong-baseline risk: CUT4 is not treated as nonlinear truth.  Same-target
  rows require an exact Kalman, dense quadrature, or independently refined
  reference whenever feasible.
- Target-mismatch risk: native SV, KSC mixture SV, exact transformed SV,
  generalized SV, SIR closure, and predator-prey closure are distinct targets.
  P44 records target identity before any value or gradient comparison.
- Proxy-metric risk: finite values, wall time, point counts, and visual
  trajectory reasonableness are diagnostics only; they cannot promote equality
  or HMC readiness.
- Gradient-risk: P42 remains governing.  Autodiff and finite differences are
  both diagnostic routes unless a phase freezes the branch decisions, declares
  parameterization, and passes directional/refinement checks.
- Fairness risk: Zhao--Cui/fixed-design TT and CUT4 must use matched data,
  parameterization, horizon, observation target, and uncertainty model before a
  same-target comparison is allowed.
- Dimension-risk: dimensions 2 and 3 may be independent product panels unless
  the subplan explicitly implements a coupled multivariate target.  Factorized
  panels must not be described as coupled TT.
- Diagnostic-closure risk: SIR, predator-prey, and generalized SV closures can
  test feasibility and finite gradients, but cannot claim native model
  correctness without a reviewed common target.

## Evidence Contract

Question:

- Across the next model families, where can CUT4 and Zhao--Cui be compared on
  the same mathematical likelihood and score target in dimensions 1, 2, and 3?
- Where a same-target comparison is not yet available, can the program produce
  explicit diagnostic-only blockers instead of overclaiming?

Baselines and comparators:

- LGSSM: exact Kalman value and score.
- Cubic additive-Gaussian observation: dense quadrature refinement and matched
  fixed-design TT/CUT4 target.
- Quadratic additive-Gaussian observation: dense quadrature refinement, with
  multimodality diagnostics.
- Nonlinear additive-Gaussian transition: dense/sequential quadrature
  refinement on tiny horizons.
- Spatial SIR: clean-room additive-Gaussian closure diagnostic only until a
  native shared target is specified.
- Predator-prey: clean-room additive-Gaussian closure diagnostic only until a
  native shared target is specified.
- Generalized SV: target-definition phase first; only finite diagnostics until
  CUT4 and Zhao--Cui share a declared likelihood.

Primary promotion criteria:

- Each phase has a subplan with target identity, parameterization, baseline,
  value criterion, gradient criterion, veto diagnostics, planned commands, and
  Claude review gate.
- Same-target implementation phases must test dims 1, 2, and 3 for value and
  gradient, with at least five deterministic directional score checks per
  dimension.
- Diagnostic-only phases must produce explicit non-claim rows rather than
  equality assertions.

Veto diagnostics:

- target mismatch used as equality evidence;
- gradients compared in different parameterizations;
- finite values used as correctness proof;
- CUT4 treated as ground truth for nonlinear models;
- Zhao--Cui factorized panels described as coupled multivariate TT;
- no exact/dense/refined reference for a same-target promotion;
- no Claude pass before execution or promotion;
- HMC/Tier-2/Tier-3 readiness claimed from Tier-1 local tests.

Explanatory-only diagnostics:

- wall time, point count, fit residual, holdout residual, condition number,
  branch hash, rank, basis order, quadrature order, finite diagnostic score,
  paired error summaries, and trajectory plots.

What will not be concluded:

- no HMC readiness;
- no production analytic score API;
- no paper-scale Zhao--Cui reproduction;
- no adaptive MATLAB TT-cross/SIRT reproduction;
- no exact native generalized-SV/SIR/predator-prey claim from closure tests;
- no stable public API claim.

## Phase Map

| Phase | Subplan | Target class | Main outcome |
| --- | --- | --- | --- |
| P44-M0 | `bayesfilter-highdim-zhao-cui-p44-phase0-target-governance-subplan-2026-06-07.md` | governance | target matrix, parameterization matrix, and pass/block labels |
| P44-M1 | `bayesfilter-highdim-zhao-cui-p44-phase1-lgssm-subplan-2026-06-07.md` | exact same-target | CUT4 and Zhao--Cui versus Kalman value/gradient dims 1--3 |
| P44-M2 | `bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-subplan-2026-06-07.md` | nonlinear same-target | cubic observation additive-Gaussian value/gradient ladder |
| P44-M3 | `bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-subplan-2026-06-07.md` | nonlinear same-target | quadratic observation multimodality stress ladder |
| P44-M4 | `bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-subplan-2026-06-07.md` | nonlinear same-target | additive-Gaussian nonlinear transition ladder |
| P44-M5 | `bayesfilter-highdim-zhao-cui-p44-phase5-spatial-sir-diagnostic-subplan-2026-06-07.md` | diagnostic-only | finite CUT4/Zhao--Cui closure checks with native-model nonclaims |
| P44-M6 | `bayesfilter-highdim-zhao-cui-p44-phase6-predator-prey-diagnostic-subplan-2026-06-07.md` | diagnostic-only | finite predator-prey closure checks with native-model nonclaims |
| P44-M7 | `bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-subplan-2026-06-07.md` | target-definition | common generalized-SV target decision before implementation |
| P44-M8 | `bayesfilter-highdim-zhao-cui-p44-phase8-integration-closeout-subplan-2026-06-07.md` | integration | traceability update, result synthesis, and blocker ledger |

## Required Execution Order

```text
M0 -> M1 -> M2 -> M3 -> M4 -> M5 -> M6 -> M7 -> M8
```

Allowed parallel preparation:

- M2--M4 implementation sketches may be prepared after M1 passes, but none may
  promote before M0 and M1 result ledgers pass Claude review.
- M5--M7 may prepare diagnostic target notes in parallel, but their nonclaims
  remain active until a later reviewed common target is implemented.

## Review Loop

Plan review:

- Run Claude review on the master program and subplans.
- Accepted token: `PASS_P44_PLAN_GOVERNANCE`.
- Blocking token: `BLOCKED_P44_PLAN_GOVERNANCE`.
- Loop until explicit pass/convergence or maximum five iterations.  Maximum
  iteration exhaustion without a pass writes a blocker note and stops.

Later implementation review:

- Each phase must run a Claude code/result review after local tests.
- Accepted token pattern: `PASS_P44_M{phase}_CODE_GOVERNANCE`.
- Blocking token pattern: `BLOCKED_P44_M{phase}_CODE_GOVERNANCE`.
- Loop per phase until explicit pass/convergence or maximum five iterations.
  Maximum iteration exhaustion without a pass writes a blocker note and stops.

## Planned Common Commands For Later Execution

Any phase extending beyond tiny local fixtures must add a phase-specific
experiment plan before execution.  That plan must include:

- wall-time and memory caps;
- early-stop rule after any tiny-row failure;
- maximum CUT4 augmented dimension or point count;
- dense/TT quadrature refinement policy;
- whether the run is correctness evidence, approximation evidence, or
  diagnostic-only evidence;
- a pre-mortem describing how the run could pass while misleading us.

Deliberate CPU-only default for local numerical tests:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p44_*.py
```

Guardrail subset:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_p30_cut4_statistical_comparators.py \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/test_v1_public_api.py
```

Static checks:

```bash
python -m compileall -q bayesfilter/highdim tests/highdim
git diff --check
```
