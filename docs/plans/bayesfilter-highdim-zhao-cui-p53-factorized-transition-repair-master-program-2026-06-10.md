# P53 Master Program: Factorized Spatial SIR Transition Repair

metadata_date: 2026-06-10
program: P53-factorized-spatial-sir-transition-repair
status: PLAN_AMENDMENT_REVIEW_CONVERGED
supervisor: Codex
reviewer: Claude Code read-only agreed through M4A-M4D amendment

## Objective

Repair the P52 planning error before attempting any more spatial SIR rank or
dimension ladders.  P52 correctly stopped at M4, but its master program placed a
route contract gate where an actual route-design and implementation gate was
needed.  P53 replaces that ordering with a dependency-safe program:

1. preserve the P52 stop as evidence of the planning failure;
2. choose and document a concrete memory-bounded transition route before coding;
3. implement a lower-rung route in TensorFlow / TensorFlow Probability;
4. tie the lower-rung route out against the dense route on tiny grids;
5. split the actual scaling route into route choice/derivation,
   implementation, lower-rung tie-out, and admission-gate phases;
6. only then resume rank selection and spatial SIR scaling.

## Planning Error Being Repaired

P52 asked whether BayesFilter could replace the dense retained-grid spatial SIR
route, but its phase order allowed P52-M4 to add a contract and static guard
without implementing the route.  That made P52-M5 through P52-M8 structurally
unreachable.  This was a logical planning error: a contract may define the
acceptance boundary, but it cannot satisfy the implementation prerequisite for
rank selection or filtering.

P53 makes this non-repeatable by separating the evidence classes:

- design evidence: a route choice with equations and memory model;
- implementation evidence: TensorFlow code that exposes the route interface;
- equivalence evidence: lower-rung tie-out to the dense route;
- scaling-route derivation evidence: a selected `C_scale` design with
  equations, approximation status, replay identity, and route-width metadata;
- scaling-route implementation evidence: TensorFlow code for the selected
  `C_scale` route;
- scaling-route lower-rung tie-out evidence: the selected route checked against
  dense or `C_low` references before promotion;
- scaling-route admission evidence: a final gate that emits the only token that
  can unlock rank/scaling phases;
- scaling evidence: bounded d=18/d=50/d=100 experiments after the route passes.

No phase may promote a weaker evidence class into a stronger one.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter replace the dense all-pairs spatial SIR transition application with a concrete TensorFlow factorized route, validate it on lower rungs, and then resume rank-calibrated spatial SIR scaling without the P52 ordering error? |
| Baseline/comparator | P52-M4 blocker, current dense route in `bayesfilter/highdim/filtering.py`, lower-rung dense spatial SIR references, P52 memory/rank and UKF scout artifacts, and P30 Zhao-Cui notation. |
| Primary pass criterion | A concrete TensorFlow route is designed, implemented, tied out against dense lower-rung references, integrated into rank selection, and then addressed for d=18/d=50/d=100 rows with explicit pass/block tokens, dimension-specific claim classes, and Claude read-only review. |
| Veto diagnostics | Contract-only artifact treated as implementation; dense `tf.repeat`/`tf.tile` route used as production path; route design not documented before coding; NumPy/default-backend drift in gradient-bearing path; lower-rung dense tie-out skipped; rank/scaling phases run before route equivalence passes; UKF promoted to truth; d=100 promoted to correctness. |
| Explanatory diagnostics | Static route audits, dense tiny-grid tie-outs, deterministic replay checks, memory forecasts, `R_eff` or conservative route-width metadata, UKF scout diagnostics, gradient finite checks, and higher-rank same-route comparisons. |
| Not concluded | No production HMC readiness, no exact d=50/d=100 posterior correctness, no GPU readiness, no S&P 500 reproduction, and no adaptive filtering path. |
| Artifacts | P53 master program, phase subplans, Claude review ledger, visible runbook, execution ledger, phase manifests/results, code/tests, P30 amendment if needed, and stop handoff. |

## Corrected Dependency DAG

The following dependencies are mandatory:

```text
P53-M0 planning-failure lock
  -> P53-M1 route design and math
  -> P53-M2 lower-rung TensorFlow route implementation
  -> P53-M3 lower-rung dense tie-out
  -> P53-M4A scaling-route choice and derivation
  -> P53-M4B scaling-route TensorFlow implementation
  -> P53-M4C scaling-route lower-rung tie-out
  -> P53-M4D scaling-route admission gate
  -> P53-M5 rank-selection integration
  -> P53-M6 spatial SIR d=18 calibration row
  -> P53-M7 d=50/d=100 scaling policy
  -> P53-M8 integration closeout
```

P53-M5 through P53-M8 must stop if any of P53-M1 through P53-M4D blocks.

## Route Design Candidates

P53-M1 must choose one initial implementation route before P53-M2 starts.  The
allowed first candidates are:

1. **blocked streaming dense-equivalent route** for lower-rung validation:
   compute transition log densities in bounded current/previous blocks and
   reduce log-sum-exp without materializing the full `N_current x N_previous`
   matrix.  This is dense-equivalent but memory-bounded; it is acceptable for
   lower-rung tie-out and as a conservative fallback for moderate retained
   counts, but it is not enough by itself to claim high-dimensional scalability.
2. **local-neighborhood sparse route** for spatial SIR:
   use the spatial locality of site transitions to restrict previous/current
   interactions to a deterministic neighborhood and expose the resulting route
   width as `R_eff`.  This must be justified against model equations and tested
   against dense lower-rung references.
3. **TT-MPO factorized contraction route**:
   represent the transition operator as a product of local cores and contract
   against the retained TT density without enumerating all grid pairs.  This is
   the preferred high-dimensional end state, but it requires more design work.

The default P53 strategy is staged: implement the blocked streaming
dense-equivalent route first for correctness tie-out and interface hardening,
then implement or block on the local/TT factorized route required for high
dimensional scaling.  The program must not treat streaming dense-equivalent
tie-out as proof of d=18/d=50/d=100 scalability.

## Route-Class Gate

P53 distinguishes two route classes:

- `lower_rung_dense_equivalent`: a blocked streaming route that is allowed for
  tiny-grid dense equivalence, interface hardening, and conservative memory
  smoke tests only;
- `scaling_route`: a local-neighborhood sparse route or TT-MPO factorized
  route that exposes deterministic replay, TensorFlow gradients, `R_eff` or a
  conservative route-width bound, and memory metadata without relying on dense
  all-pairs transition semantics.

The original P53-M4 phase was itself too large: it attempted route choice,
derivation, implementation, tie-out, and admission in one step.  That was a
planning error because execution could reach the gate before an implementable
`C_scale` design existed.  The amended P53 plan therefore replaces P53-M4 with:

- `P53-M4A`: choose one `C_scale` route and derive its exact equations,
  approximation status, replay identity, route-width metadata, and lower-rung
  tie-out criteria;
- `P53-M4B`: implement the selected `C_scale` route in TensorFlow without
  reusing `C_low` as a scaling route;
- `P53-M4C`: tie the selected `C_scale` route out on J=1/J=2/J=3 against dense
  or `C_low` references with predeclared tolerances;
- `P53-M4D`: emit the final scaling-route admission token or a precise blocker.

Only `PASS_P53_M4D_SCALING_ROUTE_ADMISSION` may unlock rank selection or
d=18/d=50/d=100 filtering phases.  If P53-M1 through P53-M3 pass only for
`lower_rung_dense_equivalent`, then P53-M4A must not pretend the route is
already chosen; it must derive and review a real `C_scale` route or block.

## Phase Index

| Phase | Name | Subplan | Required result artifact | Required token |
| --- | --- | --- | --- | --- |
| P53-M0 | Planning Failure Lock And Prerequisite DAG | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m0-planning-failure-lock-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m0-planning-failure-lock-result-2026-06-10.md` | `PASS_P53_M0_PLANNING_FAILURE_LOCK` or `BLOCK_P53_M0_PLANNING_FAILURE_LOCK` |
| P53-M1 | Route Design, Math, And P30 Amendment | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m1-route-design-math-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m1-route-design-math-result-2026-06-10.md` | `PASS_P53_M1_ROUTE_DESIGN_MATH` or `BLOCK_P53_M1_ROUTE_DESIGN_MATH` |
| P53-M2 | Lower-Rung TensorFlow Route Implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m2-route-implementation-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m2-route-implementation-result-2026-06-10.md` | `PASS_P53_M2_ROUTE_IMPLEMENTATION` or `BLOCK_P53_M2_ROUTE_IMPLEMENTATION` |
| P53-M3 | Lower-Rung Dense Tie-Out | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m3-lower-rung-dense-tieout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m3-lower-rung-dense-tieout-result-2026-06-10.md` | `PASS_P53_M3_LOWER_RUNG_DENSE_TIEOUT` or `BLOCK_P53_M3_LOWER_RUNG_DENSE_TIEOUT` |
| P53-M4A | Scaling Route Choice And Derivation | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-result-2026-06-10.md` | `PASS_P53_M4A_SCALING_ROUTE_DERIVATION` or `BLOCK_P53_M4A_SCALING_ROUTE_DERIVATION` |
| P53-M4B | Scaling Route TensorFlow Implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4b-scaling-route-implementation-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4b-scaling-route-implementation-result-2026-06-10.md` | `PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION` or `BLOCK_P53_M4B_SCALING_ROUTE_IMPLEMENTATION` |
| P53-M4C | Scaling Route Lower-Rung Tie-Out | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-result-2026-06-10.md` | `PASS_P53_M4C_SCALING_ROUTE_TIEOUT` or `BLOCK_P53_M4C_SCALING_ROUTE_TIEOUT` |
| P53-M4D | Scaling Route Admission Gate | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4d-scaling-route-admission-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4d-scaling-route-admission-result-2026-06-10.md` | `PASS_P53_M4D_SCALING_ROUTE_ADMISSION` or `BLOCK_P53_M4D_SCALING_ROUTE_ADMISSION` |
| P53-M5 | Rank Selection Integration | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m5-rank-selection-integration-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m5-rank-selection-integration-result-2026-06-10.md` | `PASS_P53_M5_RANK_SELECTION_INTEGRATION` or `BLOCK_P53_M5_RANK_SELECTION_INTEGRATION` |
| P53-M6 | Spatial SIR d=18 Calibration Row | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m6-spatial-sir-d18-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m6-spatial-sir-d18-result-2026-06-10.md` | `PASS_P53_M6_SPATIAL_SIR_D18` or `BLOCK_P53_M6_SPATIAL_SIR_D18` |
| P53-M7 | Spatial SIR d=50/d=100 Scaling Policy | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m7-spatial-sir-d50-d100-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m7-spatial-sir-d50-d100-result-2026-06-10.md` | `PASS_P53_M7_SPATIAL_SIR_D50_D100` or `BLOCK_P53_M7_SPATIAL_SIR_D50_D100` |
| P53-M8 | Integration Closeout | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m8-integration-closeout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m8-integration-closeout-result-2026-06-10.md` | `PASS_P53_M8_INTEGRATION_CLOSEOUT` or `BLOCK_P53_M8_INTEGRATION_CLOSEOUT` |

## Review And Repair Protocol

Each material phase must be reviewed by Claude Code as a read-only reviewer.
Codex remains supervisor and executor.  Claude must not edit files, run
experiments, launch agents, or supervise recovery.

If Claude does not respond to a review prompt, Codex must run a minimal Claude
probe.  If the probe responds, Codex must treat the review prompt as the
problem, split or shorten it, and retry.  Review may loop until convergence or
five iterations.  On the fifth iteration, accept only if no major blocker
remains; otherwise stop with a human-required blocker.

## Stop Discipline

P53 must stop, not skip ahead, if:

- route design is not concrete enough to implement;
- implementation is contract-only;
- P53-M1 through P53-M3 pass only for `lower_rung_dense_equivalent` and no
  `scaling_route` has passed P53-M4D;
- P53-M4A does not choose and derive a concrete `C_scale` route before P53-M4B;
- P53-M4B attempts to implement before the P53-M4A derivation is reviewed;
- P53-M4C skips lower-rung tie-out for the selected scaling route;
- lower-rung dense tie-out fails without a repaired explanation;
- rank/scaling phases would run on the dense all-pairs production route;
- continuing requires a new scientific policy or backend decision;
- Claude and Codex do not converge after five review rounds.
