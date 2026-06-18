# Phase 10 Result: Comparative Decision

Date: 2026-06-17
Close timestamp: 2026-06-18T04:18:00+08:00

## Status

`PHASE_10_COMPARATIVE_DECISION_COMPLETED_NO_DEFAULT_ALGORITHM_YET`

## Phase Objective

Synthesize the scalable OT source audit and Phase 1-9 diagnostics into an
evidence-class-aware decision about which routes deserve deeper LEDH-PFPF-OT
testing.

Phase 10 is a decision/documentation phase.  It did not implement new
algorithms, run new candidate diagnostics, install packages, fetch network
sources, use GPU evidence, execute POT/external code, unblock Mini-batch/BoMb,
or change BayesFilter defaults.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Which scalable OT routes are justified for deeper LEDH-PFPF-OT testing, and which remain reference-only or blocked? |
| Baseline/comparator | Phase 1 dense/streaming TensorFlow baseline and each lane's declared semantic comparator. |
| Primary criterion | Passed for comparative documentation: the result classifies evidence types, preserves non-claims, avoids unsupported ranking/default claims, and identifies next justified testing routes. |
| Promotion veto | No route is production/default-ready.  Semantic replacements are not dense OT approximations unless separately tested.  Sparse implementation is blocked for now by Phase 8 locality diagnostics.  Mini-batch/BoMb remains source-blocked. |
| Continuation veto | None.  Required Phase 1-9 result and benchmark artifacts were available. |
| Explanatory diagnostics | Dense-reference discrepancies, residual magnitudes, source maturity, implementation effort, and fixture behavior. |
| Not concluded | No speedup, no production/default readiness, no posterior correctness, no HMC readiness, no public API readiness, and no statistically supported ranking. |
| Artifact preserving result | This result, reset memo, ledger, and stop handoff. |

## Comparative Decision

Do not select a final scalable OT algorithm yet.

The next justified LEDH-PFPF-OT work should use a ladder:

1. Treat the TensorFlow Nystrom route as the lowest semantic-risk next
   diagnostic target, but only through a reduced-rank ladder with memory/runtime
   and dense-reference validity gates.  Phase 4 validated the full-rank factor
   path, not scalability.
2. Treat low-rank coupling as a promising transport-object route for a later
   true solver-port plan.  Phase 6 validated `Q,R,g` factors and lazy apply,
   but did not implement low-rank Sinkhorn/Dykstra solver fidelity.
3. Keep positive-feature and sliced/subspace routes as semantic-replacement
   candidates for downstream filtering diagnostics only.  Their dense-reference
   discrepancies are explanatory and cannot be used as dense OT equivalence.
4. Keep exact online/GPU sources as reference-only until a dedicated
   TensorFlow operator/parity plan or approved trusted external/GPU plan exists.
5. Do not implement sparse/localized solvers in this runbook.  Phase 8 found
   diffuse support on the Phase 1 fixtures and blocks sparse implementation
   for now.  A later LEDH-specific locality screen could reopen that lane.
6. Keep Mini-batch/BoMb blocked until a clean source archive/checkout and a
   full-particle transport-object audit are available.

This is a next-work recommendation, not a statistically supported performance
ranking.

## Non-Claims Preserved

- No speedup.
- No production/default readiness.
- No posterior correctness.
- No HMC-readiness.
- No public API readiness.
- No statistically supported ranking.
- No dense OT equivalence for semantic-replacement lanes.
- No sparse solver validity or broad rejection of sparse OT.
- No Mini-batch/BoMb viability.

## Candidate Evidence Table

| Lane | Source status | Semantic class | Transport object | Execution artifact | Hard veto status | Readiness status | Next justified action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Dense/streaming baseline | local TensorFlow baseline | exact local comparator | dense matrix / streaming nonmaterialized | Phase 1 diagnostics | Passed baseline fixture gate | Comparator only; not scalable solution | Keep as reference for future ladders. |
| Nystrom | `source_locked` | approximate-kernel / fixed adaptation | kernel factors | Phase 4 full-rank diagnostic | No hard veto; max row residual `6.102528e-05`, max dense error `3.532978e-03` | Lowest semantic-risk candidate, but scalability untested | Run reduced-rank ladder under a new reviewed subplan. |
| Positive-feature | `source_locked` | `semantic_replacement` | positive feature factors | Phase 5 diagnostic | No hard veto; max row residual `3.221883e-05` | Valid semantic-replacement screen only | Consider downstream filtering smoke after Nystrom/low-rank solver priorities. |
| Low-rank coupling | `source_locked` | `semantic_replacement` / transport-object fixture | `Q,R,g` factors | Phase 6 diagnostic | No hard veto; max induced row residual `3.709804e-04`, column residual `5.748172e-04` | Transport object validated; solver fidelity untested | Plan true low-rank Sinkhorn/Dykstra solver route or downstream semantic-replacement test. |
| Exact online/GPU | `source_reference_only` | reference-only exact/operator ideas | lazy/operator source designs | Phase 7 reference close | No runtime gate run | Reference-only | Revisit only with TensorFlow operator parity or approved external/GPU plan. |
| Sparse/localized | `source_reference_only` | diagnostic/reference-only for this run | dense-plan locality screen | Phase 8 diagnostic | No hard diagnostic veto; promotion veto fired | Sparse implementation blocked for now | Reopen only with LEDH-specific locality evidence or revised reviewed screen. |
| Sliced/subspace | `source_locked` | `semantic_replacement` | projected output | Phase 9 diagnostic | No hard veto; projection consistency `5.551115e-17` | Exploratory semantic replacement; dense error large and explanatory | Carry as optional downstream surrogate experiment, not dense replacement. |
| Mini-batch/BoMb | `source_partial_user_needed` | blocked / semantic replacement if later unblocked | unknown full-particle transport; visible source has scalar/local examples | Phase 2 audit only | Source blocker active | Blocked | Ask user for clean source/archive before decision-grade testing. |

## Diagnostic Summary

| Lane | Key recorded diagnostic | Evidence role |
| --- | --- | --- |
| Nystrom | Full-rank max dense-reference particle error `3.532978e-03`; max row residual `6.102528e-05` | Validity for full-rank factor route; not scalability. |
| Positive-feature | Max dense-reference particle error `1.487610e-01`; residuals finite | Semantic-replacement validity; dense error explanatory. |
| Low-rank coupling | Max factor residual `8.981518e-06`; max dense-reference particle error `9.884159e-02` | Transport-object validity; solver fidelity untested. |
| Sparse/localized | 99% support p90 fraction reaches `1.0`; max truncated column residual `2.113375e-01` | Promotion veto for sparse implementation on Phase 1 fixtures. |
| Sliced/subspace | Projection consistency `5.551115e-17`; max dense-reference particle error `6.491195e-01` | Semantic-replacement mechanics pass; dense discrepancy explanatory. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `NO_DEFAULT_ALGORITHM_YET` | Comparative synthesis complete with evidence classes preserved. | Default-readiness veto active for every route. | Downstream LEDH/PFPF filtering behavior and actual large-N/large-D runtime remain untested. | Start a reviewed reduced-rank Nystrom ladder, then a true low-rank coupling solver-route plan if needed. | No speedup, no posterior correctness, no ranking, no default readiness. |
| `NYSTROM_REDUCED_RANK_LADDER_NEXT` | Phase 4 passed full-rank factor correctness with smallest dense-reference discrepancy. | Scalability and reduced-rank validity are still vetoes until tested. | Useful rank, stability, memory/runtime, and LEDH sensitivity. | New subplan with rank ladder, dense validity gates, memory/runtime proxy, and downstream smoke. | Not a production choice. |
| `LOW_RANK_SOLVER_ROUTE_LATER` | Phase 6 passed transport-object fixture diagnostics. | Solver fidelity veto remains active. | Whether a source-grounded TensorFlow low-rank solver can preserve marginals and useful particles. | New subplan for solver-route port or use as semantic-replacement downstream comparator. | Not dense Sinkhorn equivalence. |
| `SPARSE_BLOCKED_FOR_NOW` | Phase 8 completed diagnostic. | Promotion veto fired under declared locality thresholds. | LEDH-specific fixtures may be more local than Phase 1 fixtures. | Do not implement sparse solver unless a new locality diagnostic passes. | Not a broad rejection of sparse OT. |
| `MINIBATCH_SOURCE_BLOCKED` | Phase 2 audit identified partial/incomplete source. | Source blocker active. | Clean source may expose different transport semantics. | Ask user for clean source/archive if this lane should continue. | No Mini-batch viability claim. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Nystrom, positive-feature, low-rank coupling, sparse diagnostic, and sliced/subspace diagnostic hard screens passed within their own scopes; Mini-batch remains source-blocked. |
| Statistically supported ranking | None.  Fixture diagnostics are deterministic and descriptive; no uncertainty-aware ranking was run. |
| Descriptive-only differences | Dense-reference errors, runtime fields, support curves, source maturity, and implementation effort are descriptive unless a phase declared them as a validity gate. |
| Default-readiness | None.  No candidate is ready to become the BayesFilter default. |
| Next evidence needed | Reduced-rank Nystrom ladder, true low-rank solver route, downstream LEDH/PFPF filtering diagnostics, LEDH-specific sparse locality screen, and clean Mini-batch source if desired. |

## Recommendation For The Next Master Program

Use the following evidence ladder:

| Step | Purpose | Promotion gate | Stop/veto |
| --- | --- | --- | --- |
| 1. Reduced-rank Nystrom ladder | Test whether the full-rank factor route becomes useful at small rank. | Dense-reference residual/error thresholds plus memory/runtime proxy and finite particles on Phase 1 and LEDH-specific fixtures. | Rank reduction breaks marginals/particles or offers no plausible memory/runtime path. |
| 2. True low-rank coupling solver route | Replace fixture factors with a source-grounded optimization route. | Factor marginal residuals, lazy/materialized parity on tiny cases, finite particles, and source anchors. | Solver route cannot preserve the Phase 1 scaled marginal convention. |
| 3. Downstream semantic-replacement smoke | Test positive-feature, low-rank coupling, and sliced outputs in filtering metrics. | Predeclared downstream validity screen, not dense equivalence. | Filtering diagnostics fail or uncertainty is too large for interpretation. |
| 4. LEDH-specific sparse locality screen | Reassess sparse/localized only on actual LEDH post-flow particles. | Same or reviewed locality thresholds pass. | Diffuse support persists or truncation residuals fail. |
| 5. Mini-batch source repair | Decide whether Mini-batch/BoMb is real transport or scalar/local objective only. | Clean source and transport-object audit. | Source remains incomplete or only scalar/local costs are available. |

## Post-Run Red Team

Strongest alternative explanation: the deterministic Phase 1 fixtures are too
small and synthetic to predict LEDH/PFPF performance.  They are useful for
interface and numerical validity, not final algorithm selection.

What would overturn this comparative decision: a reduced-rank Nystrom ladder
fails hard validity gates, or a true low-rank/sparse/semantic-replacement
downstream diagnostic passes stronger LEDH-specific criteria under a reviewed
plan.

Weakest evidence link: no downstream filtering objective or large-scale
runtime/memory benchmark has been run.  The next program must add those before
choosing a production algorithm.

## Close Conditions

The comparative decision phase can close after:

- this result passes local content checks;
- the reset memo is written;
- read-only review of material recommendations converges or a blocker is
  recorded;
- ledger and stop handoff are updated.
