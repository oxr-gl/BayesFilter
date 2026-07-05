# P91 Reset Memo: Zhao-Cui SIR d18 Scoped Production Readiness

Date: 2026-06-29

Status: `P91_SCOPED_PRODUCTION_READY_CLOSED`

## Final Status

P91 closes with a scoped production-readiness recommendation for Zhao-Cui SIR
d18:

- supported scope: highdim subpackage API and local complete-data component
  route;
- not supported scope: full observed-data/filtering source-route derivative
  readiness, exact likelihood correctness, posterior correctness/convergence,
  universal GPU superiority, package publication, release tagging, CI mutation,
  or default-policy change.

Final decision artifact:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md`

## What Changed From P90

P90 closed not production ready because it required full source-route
derivative/FD/HMC/GPU/package readiness before promotion.

P91 used the owner-approved reframing:

- score identity at true parameters is the primary scientific validation gate
  for the approximate high-dimensional score route;
- FD is necessary engineering evidence but not a truth oracle;
- solving `score(theta) = 0` is not a high-dimensional production gate;
- Hessian/information checks are optional/advisory;
- GPU/XLA capability is required for HMC-facing use;
- CPU/GPU performance is model-specific;
- batched API correctness is required.

## What Passed

- Score contract and release caveats were frozen.
- Batched highdim API matched looped single calls and fails closed on
  missing/ambiguous setup identity.
- Phase 3 limited FD evidence was owner-accepted for continuation with caveats.
- Local complete-data component score identity passed across four regimes and
  ten seeds each under the reviewed `2 sample SD` screen.
- GPU/XLA single and batched local target helpers compiled and ran with finite
  value/score outputs.
- CPU/GPU single/batched benchmark showed no closed-rule pathology and showed
  GPU/XLA faster on the tested deterministic fixture.
- Tiny trusted GPU/XLA TFP HMC smoke passed after repairing a harness
  diagnostic that had used a disconnected batched-gradient wrapper.
- Release-note draft was reviewed and repaired to be scope-first and
  user-readable.

## Caveats That Must Travel With The Result

- Phase 3 is not a full FD pass and not full source-route derivative readiness.
- Score identity is local complete-data component score identity only.
- HMC smoke is not posterior correctness or convergence.
- GPU/XLA speed evidence is model/fixture-specific.
- No release, package publication, CI-service mutation, root default, or
  default-policy change occurred in P91.

Preserved blockers:

- `BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FIXED_TTSIRT_PROPOSAL_TRANSPORT_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FULL_SOURCE_ROUTE_FD_NOT_CLAIMED`;
- `full_observed_data_filtering_score_identity = NOT_CLAIMED`.

## Current Best Answer

Zhao-Cui SIR d18 can be treated as production-ready only for the P91 scoped
route:

```text
highdim API + local complete-data Zhao-Cui SIR d18 component route
```

It should not be advertised as a full observed-data/filtering likelihood,
posterior-correct HMC target, or source-faithful full derivative route.

## Next Safe Actions

Product/release path:

1. Use the reviewed release-note draft:
   `docs/plans/bayesfilter-highdim-zhao-cui-p91-release-notes-draft-2026-06-29.md`.
2. Decide separately whether to publish, tag, broaden CI, or change defaults.
3. Do not take any of those product actions without a reviewed authority for
   the exact action.

Scientific/engineering expansion path:

1. Implement previous-marginal derivative ownership.
2. Implement fixed TTSIRT proposal/transport derivative ownership.
3. Rerun full source-route FD and score-identity gates.
4. Add broader posterior validation only after those gates pass.

## Guardrails

- Do not revive ALS training.
- Keep training-base/L1 tuning policy for any future training work.
- Do not treat Phase 7 HMC smoke as posterior validation.
- Do not treat Phase 6 benchmark as universal GPU superiority.
- Do not erase the Phase 3 limited-FD caveat.
- Keep Claude read-only; Claude cannot authorize product/default/scientific
  boundary crossings.
