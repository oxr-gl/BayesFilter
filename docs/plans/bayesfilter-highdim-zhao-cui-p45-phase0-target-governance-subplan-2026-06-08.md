# P45-M0 Subplan: Target Governance Registry

metadata_date: 2026-06-08
phase: P45-M0

## Decision Target

Create an executable target registry for generalized SV, spatial SIR, and
predator-prey before any comparison work proceeds.

## Evidence Contract

Question: for each model family, what is the exact target being compared, and
is a same-target CUT4--Zhao-Cui comparison authorized, blocked, or
diagnostic-only?

Primary criteria:

- registry rows exist for:
  - generalized SV native target;
  - generalized SV transformed-residual diagnostic;
  - generalized SV Gaussian-mixture or moment-matched approximation;
  - spatial SIR additive-Gaussian closure;
  - spatial SIR native/non-Gaussian route if proposed;
  - predator-prey additive-Gaussian closure;
  - predator-prey native/non-Gaussian route if proposed;
- every row declares state law, observation law, parameterization,
  transformation/Jacobian terms, reference route, CUT4 route, Zhao--Cui route,
  dimension/panel convention, claim class, and blocker class;
- no row is marked same-target comparison unless CUT4, Zhao--Cui, and
  reference routes are all specified.

Veto diagnostics:

- target identity is implied by model name rather than declared;
- transformation/Jacobian fields are blank for transformed targets;
- diagnostic closures are marked as native model correctness;
- current scalar-only Zhao--Cui route is listed as available for multistate
  rows without an explicit adapter plan.

## Implementation Steps

1. Add `docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json`.
2. Add tests under `tests/highdim/test_p45_target_registry.py` that validate
   required fields, claim classes, and nonclaim boundaries.
3. Write M0 result note, evidence manifest, command logs, and Claude review
   ledger.

## Required Artifacts

- Target registry:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json`
- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase0-target-governance-result-2026-06-08.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase0-target-governance-claude-review-ledger-2026-06-08.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase0-target-governance-evidence-manifest-<run_id>.json`
- Command logs:
  `docs/plans/logs/<run_id>-P45-M0-command0.log` and subsequent command logs.
- Phase gate:
  `python scripts/p45_phase_gate.py --root /home/chakwong/BayesFilter --phase P45-M0 --token PASS_P45_M0_CODE_GOVERNANCE --run-id <run_id>`

## Claim Boundary

M0 is governance only.  It creates launch authority for later phases only if
the registry blocks unsupported equality claims.
