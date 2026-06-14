# P45-M2 Subplan: Generalized SV Comparison

metadata_date: 2026-06-08
phase: P45-M2

## Decision Target

Promote generalized SV from P44 diagnostic-only status to a same-target
comparison if, and only if, the native or transformed target has matched CUT4,
Zhao--Cui, and reference routes.

## Evidence Contract

Question: for generalized SV
`y_t = beta s_t + exp(h_t / 2) epsilon_t` with states `(s_t, h_t)`, can CUT4
and Zhao--Cui evaluate the same likelihood and score target?

Candidate routes:

- native raw-observation target with dense/refined reference;
- transformed-residual target with explicit conditioning and Jacobian terms;
- Gaussian-mixture or moment-matched approximation labeled approximation-only.

Primary criteria:

- target route is selected from the M0 registry and inherits its claim class;
- same-target promotion requires value and score comparison for panel counts
  1, 2, and 3 when feasible, or a documented smaller resource-capped subset
  with a nonclaim for larger panels;
- every promoted comparison uses the exact same observations, unconstrained
  parameter vector, horizon, transformation/Jacobian convention, and reference
  route for CUT4, Zhao--Cui, and dense/exact reference;
- at least five deterministic directional score checks per promoted target;
- value and score tolerances are declared before execution and justified by
  dense/reference refinement or P42 diagnostic rules;
- approximation routes must report gaps to the reference route and stay
  non-exact.

Veto diagnostics:

- `log(y_t^2)` style transformation is applied despite nonzero `beta s_t`
  without conditioning/Jacobian accounting;
- mixture or moment-matched Kalman route is described as exact native SV;
- independent `s_t` and `h_t` prior states are treated as posterior
  independent after observation without proof;
- same-target comparison proceeds after M1 blocks the needed route.

## Implementation Steps

1. Reuse P44-M7 target table and extend it with route-specific executable
   tests.
2. Add value/gradient fixtures for native, transformed, or approximation
   routes according to the M0/M1 decisions.
3. Record finite diagnostics separately from equality evidence.

## Required Artifacts

- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase2-generalized-sv-comparison-result-2026-06-08.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase2-generalized-sv-comparison-claude-review-ledger-2026-06-08.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase2-generalized-sv-comparison-evidence-manifest-<run_id>.json`
- Command logs:
  `docs/plans/logs/<run_id>-P45-M2-command0.log` and subsequent command logs.
- Phase gate:
  `python scripts/p45_phase_gate.py --root /home/chakwong/BayesFilter --phase P45-M2 --token PASS_P45_M2_CODE_GOVERNANCE --run-id <run_id>`

## Claim Boundary

No exact generalized-SV filtering claim is allowed unless native target,
Jacobian/conditioning terms, reference route, CUT4 route, and Zhao--Cui route
are all matched.
