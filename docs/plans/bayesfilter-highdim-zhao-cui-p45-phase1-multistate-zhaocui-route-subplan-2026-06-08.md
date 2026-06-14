# P45-M1 Subplan: Multistate Zhao-Cui Route Feasibility

metadata_date: 2026-06-08
phase: P45-M1

## Decision Target

Determine whether the current fixed-branch Zhao--Cui implementation can be
extended to the two-state or factorized multistate targets required by P45.

## Evidence Contract

Question: can a reviewed fixed-design TT route evaluate the same tiny
multistate likelihood and score target as CUT4 and a dense/refined reference?

Baseline/comparator:

- baseline reference: dense/refined tensor quadrature for a tiny two-state
  additive-Gaussian target;
- CUT4: `tf_svd_cut4_filter` on the same structural target;
- Zhao--Cui: fixed-design TT route with declared product basis, coordinate
  maps, branch identities, and fixed fitting configuration.

Primary criteria:

- either implement and test a multistate/factorized fixed-design TT route for
  state dimensions needed by P45, or record a blocker that prevents M2--M4
  equality promotion;
- if implemented, test value and diagnostic score against dense reference on a
  tiny two-state fixture;
- branch identities and fitting choices are frozen during the compared value
  path.

Veto diagnostics:

- scalar-only `state_dim == 1` route is silently reused for state dimension 2;
- TT fit residual alone is treated as likelihood correctness;
- gradients cross adaptive fitting branches without diagnostic-only labeling;
- dense reference is absent or unrefined.

## Implementation Steps

1. Add a minimal multistate dense/reference fixture.
2. Decide whether to implement a multistate fixed-design TT adapter or record
   an implementation blocker.
3. If implemented, add tiny value and gradient tests.
4. If blocked, create an executable blocker test proving current scalar-only
   route rejection remains active.

## Required Artifacts

- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase1-multistate-zhaocui-route-result-2026-06-08.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase1-multistate-zhaocui-route-claude-review-ledger-2026-06-08.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase1-multistate-zhaocui-route-evidence-manifest-<run_id>.json`
- Command logs:
  `docs/plans/logs/<run_id>-P45-M1-command0.log` and subsequent command logs.
- Phase gate:
  `python scripts/p45_phase_gate.py --root /home/chakwong/BayesFilter --phase P45-M1 --token PASS_P45_M1_CODE_GOVERNANCE --run-id <run_id>`

## Claim Boundary

Passing M1 may authorize M2--M4 implementation only for the route class it
actually proves.  It does not by itself validate generalized SV, SIR, or
predator-prey.
