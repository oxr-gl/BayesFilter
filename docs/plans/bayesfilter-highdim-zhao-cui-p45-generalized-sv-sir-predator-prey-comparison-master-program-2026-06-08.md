# P45 Master Program: Generalized SV, Spatial SIR, and Predator-Prey CUT4--Zhao-Cui Comparison

metadata_date: 2026-06-08
phase: P45

## Scope

Create a governed program to determine whether generalized stochastic
volatility, spatial SIR, and predator-prey can be promoted from P44
diagnostic-only status to same-target CUT4--Zhao-Cui value and gradient
comparisons.

This program is intentionally stricter than P44-M5--M7.  It may end with
same-target comparison results, but only after the relevant phase proves that
CUT4, Zhao--Cui/fixed-design TT, and the reference route evaluate the same
likelihood and score target in the same parameterization.  If that route is not
available, the phase must record a blocker and nonclaim rather than compare
unmatched numbers.

## Governing Sources

- P44 completed run and closeout:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-overnight-gated-self-recovery-execution-result-2026-06-07.md`
- P44 generalized-SV target definition:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-definition-2026-06-08.md`
- P42 likelihood and gradient validation rules:
  `docs/plans/bayesfilter-highdim-zhao-cui-p42-gradient-likelihood-validation-rules-2026-06-07.md`
- P43 SV value/gradient ladder:
  `docs/plans/bayesfilter-highdim-zhao-cui-p43-sv-value-gradient-cut4-zhaocui-result-2026-06-07.md`
- P44 SIR and predator-prey diagnostic results:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase5-spatial-sir-diagnostic-result-2026-06-07.md`
  and
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase6-predator-prey-diagnostic-result-2026-06-07.md`
- Current code anchors:
  `bayesfilter/highdim/filtering.py`,
  `bayesfilter/highdim/models.py`,
  `bayesfilter/highdim/sv_mixture_cut4.py`,
  `tests/highdim/test_p44_generalized_sv_target.py`,
  `tests/highdim/test_p44_spatial_sir_diagnostic.py`,
  and
  `tests/highdim/test_p44_predator_prey_diagnostic.py`

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_WITH_STRICT_PROMOTION_GATES`.

- Wrong-baseline risk: CUT4 is not ground truth for nonlinear models.  P45
  requires dense/refined or exact reference routes before promotion.
- Target-mismatch risk: generalized SV native likelihood, transformed residual
  diagnostics, Gaussian-mixture approximations, SIR additive-Gaussian closures,
  and predator-prey additive-Gaussian closures are distinct targets.  P45-M0
  must freeze target identity before any comparison phase runs.
- Implementation-route risk: current Zhao--Cui nonlinear value paths are
  scalar-only for non-LGSSM models.  P45-M1 must either implement and test a
  reviewed multistate fixed-branch route or record a blocker before M2--M4 can
  claim equality.
- Gradient-risk: P42 remains governing.  A gradient pass requires the same
  unconstrained parameter vector, fixed branch decisions, directional checks,
  and explicit nonclaims for production analytic score/HMC readiness.
- Dimension-risk: dimensions 2 and 3 may be independent product panels only
  when labeled as factorized panels.  They must not be called coupled
  multivariate TT unless a coupled route is implemented and tested.
- Resource-risk: native multistate dense/TT routes can grow quickly.  P45 uses
  tiny fixtures first, requires point/rank/wall-time caps, and stops before
  long runs unless a phase-specific experiment plan is reviewed.
- Proxy-metric risk: finite likelihoods, finite gradients, point counts, TT
  fit residuals, wall time, and trajectory reasonableness are explanatory or
  veto diagnostics, not promotion criteria by themselves.

## Evidence Contract

Question:

- Can generalized SV, spatial SIR, and predator-prey be compared between CUT4
  and Zhao--Cui/fixed-design TT on the same likelihood and score target?
- If not, what exact target-definition, implementation, numerical-reference,
  or scientific-evidence blocker prevents comparison?

Baselines and comparators:

- CUT4 comparator: `tf_svd_cut4_filter` on a declared structural
  additive-Gaussian or declared transformed target.
- Zhao--Cui comparator: fixed-design TT route with frozen branch identities,
  fixed product basis, fixed coordinate maps, and no adaptive branch mutation
  during the compared value/score path.
- Reference route: exact Kalman only where the target is linear-Gaussian;
  otherwise dense/refined tensor quadrature or a separately reviewed exact
  transformed reference.

Primary promotion criteria:

- M0 target registry has one row per model/target with observation law, state
  law, parameterization, transformation/Jacobian terms, reference route, CUT4
  route, Zhao--Cui route, claim class, and blocker state.
- M1 proves a reusable multistate route or records why same-target comparison
  cannot proceed.
- For any model promoted to same-target comparison, value and gradient are
  tested on tiny deterministic fixtures with:
  - dimensions/panel counts declared by the phase;
  - exact same observations and parameter vector for CUT4, Zhao--Cui, and
    reference;
  - at least five deterministic directional score checks per promoted target;
  - explicit value and score tolerance bands justified by reference
    refinement or P42 diagnostic rules.
- Diagnostic-only outcomes must record nonclaims and may not present
  candidate-vs-CUT4 equivalence metrics.

Veto diagnostics:

- target mismatch is used as equality evidence;
- gradients are compared in different parameterizations;
- transformed residuals omit required Jacobian or conditioning terms;
- independent product panels are described as coupled multivariate TT;
- dense/refined reference is absent for a nonlinear same-target promotion;
- current scalar-only Zhao--Cui route is reused for a multistate target without
  a reviewed adapter;
- fit residual, finite value, or finite score is promoted as correctness;
- HMC readiness, production score API readiness, stable public API readiness,
  or paper-scale Zhao--Cui reproduction is claimed.

Explanatory-only diagnostics:

- wall time, memory, point count, augmented dimension, quadrature order, TT
  rank, fit residual, holdout residual, branch hash, condition number, finite
  value/gradient status, and approximation-gap summaries.

What will not be concluded:

- no HMC readiness;
- no production analytic score API;
- no stable public API;
- no paper-scale Zhao--Cui reproduction;
- no adaptive MATLAB TT-cross/SIRT reproduction;
- no coupled multivariate TT claim unless a coupled phase explicitly proves
  it.

## Phase Map

| Phase | Subplan | Purpose | Required pass token |
| --- | --- | --- | --- |
| P45-M0 | `bayesfilter-highdim-zhao-cui-p45-phase0-target-governance-subplan-2026-06-08.md` | target registry and blocker classification for generalized SV, SIR, and predator-prey | `PASS_P45_M0_CODE_GOVERNANCE` |
| P45-M1 | `bayesfilter-highdim-zhao-cui-p45-phase1-multistate-zhaocui-route-subplan-2026-06-08.md` | multistate/factorized Zhao--Cui route design and feasibility gate | `PASS_P45_M1_CODE_GOVERNANCE` |
| P45-M2 | `bayesfilter-highdim-zhao-cui-p45-phase2-generalized-sv-comparison-subplan-2026-06-08.md` | generalized SV target promotion or blocker | `PASS_P45_M2_CODE_GOVERNANCE` |
| P45-M3 | `bayesfilter-highdim-zhao-cui-p45-phase3-spatial-sir-comparison-subplan-2026-06-08.md` | spatial SIR same-target closure comparison or blocker | `PASS_P45_M3_CODE_GOVERNANCE` |
| P45-M4 | `bayesfilter-highdim-zhao-cui-p45-phase4-predator-prey-comparison-subplan-2026-06-08.md` | predator-prey same-target closure comparison or blocker | `PASS_P45_M4_CODE_GOVERNANCE` |
| P45-M5 | `bayesfilter-highdim-zhao-cui-p45-phase5-cross-model-error-calibration-subplan-2026-06-08.md` | value/gradient error calibration and likelihood-scale interpretation | `PASS_P45_M5_CODE_GOVERNANCE` |
| P45-M6 | `bayesfilter-highdim-zhao-cui-p45-phase6-integration-closeout-subplan-2026-06-08.md` | closeout ledger, nonclaims, and next justified implementation actions | `PASS_P45_M6_CODE_GOVERNANCE` |

Required order:

```text
M0 -> M1 -> M2 -> M3 -> M4 -> M5 -> M6
```

M2--M4 may prepare test sketches in parallel after M0, but none may claim
same-target comparison before M1 passes or records a reviewed route-specific
exception.

## Execution And Review Rules

- Codex is the supervisor and executor.
- Claude is read-only reviewer for plan, repair, and code/governance gates.
- Claude must not edit files, launch commands, or act as supervisor.
- Plan review loops until `PASS_P45_PLAN_GOVERNANCE` or maximum five
  iterations.
- Each phase review loops until the phase pass token or maximum five
  iterations.
- Any target, reference, tolerance, parameterization, resource cap, or claim
  class change requires a repair amendment and read-only Claude repair pass.
- If the same blocker survives five iterations, or if Codex and Claude agree a
  human scientific decision is required, the program stops with a blocker
  result instead of weakening the plan.

## Planned Execution Commands

The default local execution is CPU-only:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_*.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim
python scripts/p45_phase_gate.py --root /home/chakwong/BayesFilter --phase P45-M{n} --token PASS_P45_M{n}_CODE_GOVERNANCE --run-id <run_id>
```

GPU, long-horizon, or paper-scale runs require a separate phase-specific
experiment plan and trusted GPU execution approval.

