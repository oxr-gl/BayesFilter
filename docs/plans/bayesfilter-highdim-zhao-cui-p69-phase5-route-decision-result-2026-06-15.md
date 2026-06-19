# P69 Phase 5 Result: Fixed-Variant Repair Decision Or Adaptive-Reproduction Fork

metadata_date: 2026-06-15
status: P69_PHASE5_ROUTE_DECISION_PASSED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 5
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Primary route selected:

`CONTINUE_FIXED_VARIANT_WITH_BOUNDED_REPAIR_DESIGN_DIAGNOSTIC`

Claude review converged after one handoff patch.  Phase 5 does not authorize
d18 validation, d50/d100 scaling, HMC readiness, or adaptive Zhao--Cui parity
claims.  It selects the next engineering route only.

## Decision Table

| Route | Decision | Reason |
| --- | --- | --- |
| Continue fixed-HMC adaptation with bounded repair/design diagnostic | `selected` | Phase 4 supports inactive added rank capacity and degree/basis/design sensitivity in the current fixed variant.  Clean source-route and holdout/replay diagnostics weaken implementation-wiring and missing-diagnostic explanations, so the next smallest useful action is a bounded fixed-variant diagnostic focused on rank-channel activity, degree/basis sensitivity, design coverage, and target scaling. |
| Open adaptive Zhao--Cui reproduction lane | `deferred` | Phase 4 is not evidence against adaptive Zhao--Cui in principle.  Opening adaptive reproduction would change the scientific target and must be a separate reviewed lane with paper/source anchors, not a silent continuation of the fixed-HMC adaptation. |
| Stop for human direction | `not_selected` | The current target remains the fixed-HMC adaptation and a bounded next diagnostic is available.  Human direction is needed only if the target changes to adaptive author-algorithm reproduction or if the user wants to stop the fixed-variant repair lane. |

## Evidence Used

From Phase 4:

- inactive rank channels: supported;
- deterministic degeneracy: unresolved;
- metric-insensitive comparison: weakened;
- basis/domain sensitivity: supported;
- design coverage insufficiency: supported as an inference, not a proven
  mechanism;
- overfitting: unresolved;
- target scaling: unresolved;
- structural sensitivity of the fixed variant: supported;
- implementation failure in source-route wiring: weakened;
- missing holdout/replay diagnostic insufficiency: weakened;
- evidence against adaptive Zhao--Cui: weakened.

From Phase 3:

- all rows are interpretable under holdout/replay gates;
- rank ladder passes with zero deltas;
- degree ladder blocks on all four frozen threshold metrics;
- degree 2 improves in-sample fit residuals but changes downstream diagnostics
  sharply.

## Claim Boundaries

This route decision is not:

- a d18 correctness result;
- a d50 or d100 scaling result;
- an HMC-readiness result;
- an adaptive Zhao--Cui reproduction result;
- a proof that design coverage insufficiency is the only mechanism;
- a paper-failure claim.

The fixed-HMC/adaptive-reproduction boundary remains binding.

## Selected Next Subplan

Create a bounded fixed-variant repair/design diagnostic subplan before any
further execution.  The subplan should target these questions:

1. Do rank-3 cores/channels have measurable activity beyond rank 2 under the
   current fixed branch?
2. Does deterministic degeneracy remain a plausible unresolved explanation for
   rank zero-delta after direct rank-channel diagnostics?
3. Does degree instability decrease under better design coverage or a controlled
   target scaling/normalization diagnostic?
4. Is the degree-2 behavior overfitting-like, scaling-driven, or a structural
   sensitivity of the fixed local basis?
5. Can the fixed variant choose a conservative degree/rank branch for later d18
   validation without overclaiming source-faithful adaptive parity?

The next subplan must be bounded, CPU-only unless separately approved, and must
not tune P67 thresholds after seeing results.

## Deferred Routes

Adaptive reproduction is deferred, not rejected.  If opened later, it must have
a separate master/subplan or explicit phase amendment with:

- Zhao--Cui paper anchors;
- author source anchors;
- source-faithful/adaptive target definition;
- explicit differences from the fixed-HMC adaptation;
- separate success criteria and nonclaims.

## Required Local Checks

Text checks:

```bash
rg -n "fixed_hmc_adaptation|adaptive Zhao|d18 correctness|HMC|scaling|route decision|human direction" docs/plans/bayesfilter-highdim-zhao-cui-p69-phase4-structural-diagnosis-result-2026-06-15.md docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5-route-decision-result-2026-06-15.md
rg -n "inactive rank channels|deterministic degeneracy|metric-insensitive comparison|basis/domain sensitivity|design coverage insufficiency|overfitting|target scaling|structural sensitivity" docs/plans/bayesfilter-highdim-zhao-cui-p69-phase4-structural-diagnosis-result-2026-06-15.md docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5-route-decision-result-2026-06-15.md
```

## Nonclaims

- No correctness, scaling, HMC readiness, adaptive parity, or paper-failure
  claim.
- No new experiment has been run in Phase 5.
- No threshold has been changed.
- No source-route semantics have been changed.

## Next Handoff

Phase 5 may close after Claude review agrees that the route decision preserves
the claim boundary.  The next action is the existing bounded handoff subplan:
`docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5b-fixed-variant-repair-design-diagnostic-subplan-2026-06-15.md`.
Stop for human direction instead if the user wants to change the target.

Claude residual risks for Phase 5b:

- deterministic degeneracy remains a live unresolved explanation for rank
  zero-delta;
- Phase 5b may still fail to separate the bounded explanations and must then
  escalate to a blocker/human-direction handoff;
- later handoffs must not narrate fixed-variant diagnostics as adaptive
  Zhao--Cui parity evidence.
