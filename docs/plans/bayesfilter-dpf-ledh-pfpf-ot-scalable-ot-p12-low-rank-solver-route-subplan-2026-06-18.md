# Agent C Subplan: True Low-Rank Coupling Solver Route

Date: 2026-06-18

## Status

`DRAFT_AGENT_C_LOW_RANK_SOLVER_ROUTE_SUBPLAN`

## Chosen Lane

Agent C: true low-rank coupling solver-route plan/prototype.

Parallel class: true parallel independent algorithm lane.

This lane depends only on the coordinator-frozen Phase 1 baseline, Phase 3
schema, and transport-object contract.  It does not depend on Agent A Nystrom,
Agent B review, semantic-replacement downstream lanes, sparse lanes, or shared
audit harness artifacts.

## Phase Objective

Plan and implement a distinct TensorFlow low-rank coupling solver-route
prototype that goes beyond the Phase 6 deterministic transport-object fixture
route.

The lane asks whether a source-grounded TensorFlow route based on low-rank
coupling factors `Q`, `R`, `g` and an anchored Dykstra-style marginal
projection can produce finite, nonnegative, Phase 3-valid
`low_rank_coupling_factors` transport objects on deterministic fixtures.

This is a semantic-replacement solver-route diagnostic.  It is not a dense
Sinkhorn equivalence claim and not a production/default selection.

## Shared Contracts And Read-Only Inputs

Read-only shared contracts:

- Phase 1 dense/streaming TensorFlow baseline remains the descriptive
  comparator when dense-reference deltas are reported.
- Phase 3 schema helper remains read-only:
  `docs/benchmarks/scalable_ot_candidate_result_schema.py`
- Transport-object convention remains frozen:
  - `transport_object.kind = low_rank_coupling_factors`;
  - `materialized = false` for the primary route;
  - `factor_shapes` records `Q`, `R`, and `g`;
  - `orientation` must be recorded explicitly;
  - `semantic_output = full_state_particles`.
- CPU-only diagnostics set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.

Forbidden shared edits:

- Do not edit shared ledger or shared stop handoff.
- Do not edit Phase 1 baseline scripts/artifacts.
- Do not edit Phase 3 schema.
- Do not edit Agent A Nystrom artifacts.
- Do not edit BayesFilter public exports.

If this lane needs a shared contract change, stop and report
`BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`.

## Owned Files

Agent C may create or edit only:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
- `tests/test_low_rank_coupling_solver_tf.py`
- `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-result-2026-06-18.md`

Read-only lane context:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_transport_tf.py`
- `tests/test_low_rank_coupling_transport_tf.py`
- `docs/benchmarks/scalable_ot_p06_low_rank_coupling_prototype_diagnostics.py`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p06-low-rank-coupling-prototype-result-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-parallel-execution-structure-2026-06-18.md`

## Source Anchors

| Anchor | Planned use | Classification |
| --- | --- | --- |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` lines 628-760 | Local equations for nonnegative rank, `Pi_{a,b}(r)`, `P = Q diag(1/g) R^T`, constraints, and transport application. | Source/paper notation anchor. |
| `.localsource/scalable_ot_code_audit/POT/ot/lowrank.py` lines 206-319 | LR-Dykstra projection route for enforcing `Q in Pi(a,g)` and `R in Pi(b,g)`. | `source_faithful` for Dykstra-style factor marginal projection if mirrored. |
| `.localsource/scalable_ot_code_audit/POT/ot/lowrank.py` lines 322-527 | Low-rank Sinkhorn route returning `Q`, `R`, `g`, lazy plan, and objective values. | `source_faithful` for high-level solver-route structure when mirrored; frozen schedules are adaptations. |
| `.localsource/scalable_ot_code_audit/POT/ot/utils.py` lines 812-850 | Lazy low-rank tensor convention `Q @ diag(d) @ R^T`. | `source_faithful` for lazy apply convention. |
| `.localsource/scalable_ot_code_audit/ott-sparse/src/ott/solvers/linear/sinkhorn_lr.py` lines 120-150 | Marginal-deviation diagnostic for low-rank factors. | `source_faithful` for marginal diagnostics. |
| `.localsource/scalable_ot_code_audit/ott-sparse/src/ott/solvers/linear/sinkhorn_lr.py` lines 153-248 | `LRSinkhornOutput` with `q`, `r`, `g`, `matrix`, `apply`, marginals, and transport mass. | `source_faithful` for output/apply interface convention. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p06-low-rank-coupling-prototype-result-2026-06-17.md` | Prior fixture-route boundary and known gap: not solver fidelity. | Read-only context; not evidence that P12 solver works. |

Source-route classification before implementation:

- `source_faithful`: factor form `Q diag(1/g) R^T`, lazy apply, factor
  marginal diagnostics, and Dykstra-style projection if implemented from the
  cited source route.
- `fixed_hmc_adaptation`: deterministic initialization, frozen rank grids,
  fixed iteration budgets, epsilon/gamma floors, Phase 1 scaled transport
  adapter, CPU-only deterministic fixtures.
- `extension_or_invention`: any simplified mirror objective, stabilization, or
  update that is not present in the cited source route.  Extensions may be
  useful, but they cannot close a solver-fidelity gap unless explicitly
  reported as such.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a source-grounded TensorFlow low-rank coupling solver route produce finite, nonnegative, Phase 3-valid `Q,R,g` transport-object factors beyond the Phase 6 fixture route? |
| Baseline/comparator | Phase 1 local dense/streaming TensorFlow baseline for descriptive semantic delta only; Phase 6 fixture route is read-only context, not a promotion comparator; no external POT/OTT execution. |
| Primary pass criterion | A P12 diagnostic writes Phase 3-valid candidate records with `transport_object.kind = low_rank_coupling_factors`, `semantic_class = semantic_replacement`, `implementation_scope = solver_route`, finite nonnegative `Q,R`, strictly positive `g`, valid factor marginal residuals, valid induced row/column residuals under predeclared thresholds on tiny deterministic fixtures, and explicit source-route classification. |
| Promotion veto | Missing or invalid `Q,R,g`; nonpositive `g`; negative or nonfinite factors; invalid transported particles; wrong orientation; missing factor marginal residuals; candidate JSON schema failure; dense-reference delta treated as dense equivalence or promotion; runtime/memory proxy promoted before validity; claiming solver fidelity for an extension/invention route. |
| Continuation veto | Phase 1 baseline or Phase 3 schema missing/inconsistent; source anchors contradict the planned factor or `g` convention; implementation requires package install, network, GPU evidence, POT/external solver execution, non-TensorFlow default code, public API changes, or shared contract changes. |
| Repair trigger | Localized errors in orientation, factor normalization, Dykstra projection, `g` lower bound, deterministic initialization, cost scaling, dtype, residual threshold, or materialization-limited tiny checks. |
| Explanatory diagnostics | Rank, initialization rule, iteration counts, Dykstra residuals, factor marginal residuals, induced row/column residuals, dense-reference particle delta, objective trace if available, runtime proxy, memory proxy, source-route component table. |
| Not concluded | No dense Sinkhorn equivalence, no speedup, no ranking, no posterior correctness, no HMC readiness, no public API readiness, no production/default readiness, no broad scalable-OT decision, and no solver-fidelity claim for any extension/invention component. |
| Artifact preserving result | Agent C implementation, tests, diagnostic script, JSON/Markdown diagnostics, and P12 result note. |

## Planned Diagnostic Scope

Minimum fixtures:

- `tiny_manual_solver`: deterministic `B=1`, small `N`, low dimension,
  materialized tiny parity allowed.
- `small_batch_solver`: deterministic `B=2`, moderate `N`, rank strictly less
  than `N`, batch shape check.

Optional Phase 1 descriptive fixture subset may be included only if it uses
read-only Phase 1 fixture construction or a lane-local deterministic copy.  It
must remain descriptive and must not change Phase 1 artifacts.

Predeclared hard validity thresholds:

- all `Q`, `R`, `g`, transported particles, and log weights finite;
- `Q >= 0`, `R >= 0`, `g > 0`;
- factor marginal residual `<= 5e-3` for tiny fixtures;
- induced row/column residual `<= 5e-3` for tiny fixtures;
- materialized tiny apply parity `<= 1e-10` when materialization is used;
- every candidate record validates under Phase 3 schema.

Dense-reference transported-particle deltas, runtime proxy, and memory proxy
are explanatory only.

## Required Checks And Commands

First local checks before implementation:

```bash
python -m py_compile docs/benchmarks/scalable_ot_candidate_result_schema.py
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_transport_tf.py tests/test_low_rank_coupling_transport_tf.py
pytest -q tests/test_low_rank_coupling_transport_tf.py
```

Implementation checks after Agent C files exist:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py tests/test_low_rank_coupling_solver_tf.py docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py
pytest -q tests/test_low_rank_coupling_solver_tf.py
python docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py --output docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.json --markdown-output docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.md
```

All commands are CPU-only local commands.  No package install, network fetch,
GPU evidence, POT/external solver execution, or public API export change is
allowed.

## Result Status Names

Allowed P12 statuses:

- `LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY`
- `LOW_RANK_SOLVER_ROUTE_COMPLETED_CANDIDATE_NOT_PROMOTED`
- `LOW_RANK_SOLVER_ROUTE_BLOCKED`
- `BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`

Do not use statuses that imply default readiness, production readiness,
speedup, posterior correctness, HMC readiness, public API readiness, ranking,
or dense Sinkhorn equivalence.

## Stop Conditions

Stop and write
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-result-2026-06-18.md`
with the appropriate blocked status if:

- a shared contract change is needed;
- Phase 1 baseline or Phase 3 schema is missing/inconsistent;
- source anchors contradict the planned factor or `g` convention;
- only scalar costs/losses can be produced, not valid factors and transported
  particles;
- implementation requires POT/external execution, package install, network,
  GPU evidence, public export changes, non-TensorFlow default code, or edits to
  another lane's files;
- hard validity failures are not localized to a repair trigger.

## Skeptical Plan Audit

- Wrong baseline risk: use Phase 1 only as descriptive semantic-delta
  comparator; do not compare against external POT/OTT execution.
- Proxy metric risk: runtime/memory/rank are explanatory only.
- Missing stop conditions: stop for shared contract drift, source contradiction,
  scalar-only outputs, or invalid factors.
- Unfair comparison risk: do not rank P12 against Nystrom, positive-feature,
  sliced/subspace, sparse, or Phase 6 fixture route.
- Hidden assumptions: record rank, `g` lower bound, deterministic
  initialization, projection iterations, dtype, cost scaling, and orientation.
- Environment mismatch: no package install, network, GPU, or external solver.
- Artifact adequacy: JSON/Markdown must contain Phase 3-valid records and
  source-route classification; a loss trace alone is insufficient.

Skeptical audit status:

`PASSED_FOR_AGENT_C_SUBPLAN_ONLY_NOT_IMPLEMENTATION`

