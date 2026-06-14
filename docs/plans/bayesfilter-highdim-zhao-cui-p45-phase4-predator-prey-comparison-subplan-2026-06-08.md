# P45-M4 Subplan: Predator-Prey Comparison

metadata_date: 2026-06-08
phase: P45-M4

## Decision Target

Promote or block predator-prey from diagnostic-only CUT4 closure to a
same-target CUT4--Zhao-Cui value/gradient comparison.

## Evidence Contract

Question: can the declared predator-prey target be evaluated by CUT4,
Zhao--Cui/fixed-design TT, and a reference route without changing the ODE
transition, parameterization, or observation model?

Candidate target:

- P44-M6 additive-Gaussian RK4 closure with state `(prey, predator)` and
  parameter vector `(r,K,a,s,u,v)`.

Primary criteria:

- M0 registry identifies whether the target is native predator-prey,
  additive-Gaussian closure, or diagnostic-only;
- M1 route supports the two-state target or M4 records an implementation
  blocker;
- for any promoted row, test value and score on the two-state target and only
  expand to replicated panels under explicit caps;
- replicated panels must be labeled factorized panels unless a separately
  implemented coupled multistate TT route is reviewed and tested;
- every promoted comparison uses the exact same observations, unconstrained
  parameter vector, horizon, ODE/RK4 convention, closure/native target, and
  reference route for CUT4, Zhao--Cui, and dense/refined reference;
- at least five deterministic directional score checks are required for every
  promoted target;
- value and score tolerances are declared before execution and justified by
  dense/reference refinement or P42 diagnostic rules;
- dense/refined reference and fair-comparison manifest blockers pass.

Veto diagnostics:

- ODE solver or time-step differs across methods;
- wall-time or ESS proxy is promoted without matched value/score evidence;
- finite CUT4 diagnostic score is treated as production score API readiness;
- no matched Zhao--Cui route exists.

## Implementation Steps

1. Freeze the P44-M6 closure and RK4 conventions as a named target.
2. Add dense/refined reference tests for the selected target.
3. Add CUT4 and Zhao--Cui comparison tests only after M1 route approval.
4. Record diagnostic-only blocker if the route remains unavailable.

## Required Artifacts

- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase4-predator-prey-comparison-result-2026-06-08.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase4-predator-prey-comparison-claude-review-ledger-2026-06-08.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase4-predator-prey-comparison-evidence-manifest-<run_id>.json`
- Command logs:
  `docs/plans/logs/<run_id>-P45-M4-command0.log` and subsequent command logs.
- Phase gate:
  `python scripts/p45_phase_gate.py --root /home/chakwong/BayesFilter --phase P45-M4 --token PASS_P45_M4_CODE_GOVERNANCE --run-id <run_id>`

## Claim Boundary

No nonlinear preconditioning usefulness or paper-scale predator-prey validation
is concluded by this phase.
