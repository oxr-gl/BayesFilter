# P45-M3 Subplan: Spatial SIR Comparison

metadata_date: 2026-06-08
phase: P45-M3

## Decision Target

Promote or block spatial SIR from diagnostic-only CUT4 closure to a same-target
CUT4--Zhao-Cui value/gradient comparison.

## Evidence Contract

Question: can the declared spatial SIR target be evaluated by CUT4,
Zhao--Cui/fixed-design TT, and a reference route without changing the model or
parameterization?

Candidate target:

- additive-Gaussian closure already used in P44-M5, with state
  `(S_1,I_1,...,S_J,I_J)` and infectious-coordinate observations.

Primary criteria:

- M0 registry identifies whether the phase is native SIR, clean-room
  additive-Gaussian closure, or diagnostic-only;
- M1 route supports the required state dimension or M3 records an
  implementation blocker;
- for any promoted row, test value and score for `J=1` first, then `J=2,3`
  only under explicit point/rank/resource caps;
- `J=2,3` rows must be labeled replicated/factorized panels unless a
  separately implemented coupled multistate TT route is reviewed and tested;
- every promoted comparison uses the exact same observations, unconstrained
  parameter vector, horizon, closure/native target, and reference route for
  CUT4, Zhao--Cui, and dense/refined reference;
- at least five deterministic directional score checks are required for every
  promoted target;
- value and score tolerances are declared before execution and justified by
  dense/reference refinement or P42 diagnostic rules;
- dense/refined reference is used before claiming same-target agreement.

Veto diagnostics:

- negative-population diagnostics are hidden;
- closure likelihood is called native SIR filtering correctness without
  justification;
- no matched Zhao--Cui route exists;
- finite CUT4 value/score is promoted as equality.

## Implementation Steps

1. Freeze the P44-M5 closure as a named target or replace it with a reviewed
   native route.
2. Add dense/refined reference tests for the selected target.
3. Add CUT4 and Zhao--Cui comparison tests only after M1 route approval.
4. Record diagnostic-only blocker if the route remains unavailable.

## Required Artifacts

- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase3-spatial-sir-comparison-result-2026-06-08.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase3-spatial-sir-comparison-claude-review-ledger-2026-06-08.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase3-spatial-sir-comparison-evidence-manifest-<run_id>.json`
- Command logs:
  `docs/plans/logs/<run_id>-P45-M3-command0.log` and subsequent command logs.
- Phase gate:
  `python scripts/p45_phase_gate.py --root /home/chakwong/BayesFilter --phase P45-M3 --token PASS_P45_M3_CODE_GOVERNANCE --run-id <run_id>`

## Claim Boundary

Spatial SIR can pass as a blocker/nonclaim phase.  It can pass as a comparison
phase only with matched target, reference, value, and gradient evidence.
