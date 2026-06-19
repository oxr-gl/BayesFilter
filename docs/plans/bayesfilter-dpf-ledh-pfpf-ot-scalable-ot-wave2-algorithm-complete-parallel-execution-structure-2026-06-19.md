# Wave 2 Algorithm-Complete Parallel Execution Structure

Date: 2026-06-19
Coordinator: Codex

## Status

`DRAFT_ALGORITHM_COMPLETE_PARALLEL_STRUCTURE_NOT_LAUNCHED`

## Purpose

Replace frequent merge-style parallelism with independent, algorithm-complete
lanes.  Each active agent owns one different scalable-OT algorithm family and
takes that lane from subplan through implementation, tests, diagnostics, and
final closeout before any coordinator synthesis.

This structure minimizes cross-agent interaction.  The coordinator freezes
shared contracts once before launch, then merges only after both lanes have
ended or one lane writes a true blocker.

## Core Correction

The prior pattern mixed an algorithm lane with a diagnostic/review-adjacent
lane.  That creates repeated merge pressure because one lane can affect what
the other should do next.

For future waves, do not pair:

- implementation lane plus dependent review lane;
- algorithm lane plus locality screen for deciding whether an algorithm should
  exist;
- partial prototype lane plus shared-harness lane;
- two lanes editing common infrastructure.

Instead, pair complete algorithm families with disjoint write sets and separate
evidence contracts.

## Candidate Algorithm Families

The scalable-OT planning corpus already contains multiple algorithm families:

| Algorithm family | Existing status | Wave-2 suitability |
| --- | --- | --- |
| Nystrom kernel approximation | Reduced-rank diagnostic and independent review already completed. | Useful as read-only baseline context or later deeper validation, but not the cleanest next parallel lane unless explicitly reopened. |
| Low-rank coupling solver route | Diagnostic-only P12 route exists and passed finite/factor checks. | Suitable for an algorithm-complete validation lane, preserving all diagnostic-only boundaries. |
| Positive-feature Sinkhorn | Source audit and earlier prototype context exist. | Suitable for an independent approximate-kernel/semantic-replacement algorithm lane. |
| Sparse/screened/localized OT | Locality diagnostics did not justify reopening sparse implementation. | Stand down unless a new reviewed plan freezes different input artifacts and thresholds. |
| Sliced/subspace OT | Source audit and exploratory context exist; full-state reconstruction semantics remain open. | Suitable later, but only as a semantic-replacement lane with explicit reconstruction semantics. |
| Exact online/GPU/streaming route | Reference/context exists. | Suitable only under a separate resource and backend contract. |

Recommended Wave 2 pair:

- `peer agent`: low-rank coupling solver-route validation lane.
- `current agent`: positive-feature Sinkhorn algorithm lane.

This pair is preferred because the lanes are genuinely different algorithm
families, can use disjoint implementation/test/diagnostic files, and do not
need each other's intermediate artifacts.

## Two Active Agents Only

Exactly two active agents are allowed:

- `peer agent`
- `current agent`

Historical `Agent A`, `Agent B`, `Agent C`, or other alphabet labels must not
be used for new active assignments.  Old files may retain historical titles,
but new operational records use only `peer agent` and `current agent`.

## Shared Contracts Frozen Before Launch

The coordinator freezes these contracts once before either lane starts:

- Phase 1 dense/streaming TensorFlow baseline remains the common comparator
  only where a lane's evidence contract requires dense-reference diagnostics.
- Phase 3 candidate schema remains read-only shared infrastructure:
  `docs/benchmarks/scalable_ot_candidate_result_schema.py`.
- Transport-object records must declare `kind`, `materialized`,
  `factor_shapes` or `shape`, `orientation`, and `semantic_output`.
- CPU-only TensorFlow diagnostics must set `CUDA_VISIBLE_DEVICES=-1` before
  importing TensorFlow.
- Runtime and memory fields are explanatory only unless a later reviewed
  evidence contract gives them a different role.
- BayesFilter public exports and defaults are read-only.
- No lane may claim speedup, ranking, posterior correctness, HMC readiness,
  public API readiness, production/default readiness, dense Sinkhorn
  equivalence, or broad scalable-OT selection.

Any lane needing a shared contract change stops with
`BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`.  The other lane may continue if its
own contract is unaffected.

## Algorithm-Complete Lane Lifecycle

Each lane must execute its whole algorithm program independently:

1. Write a lane master program and phase subplans.
2. Run source/context intake and first checks.
3. Implement only lane-owned algorithm files.
4. Add focused lane-owned tests.
5. Run deterministic diagnostics under the lane evidence contract.
6. Run any lane-owned repair loop until the lane converges or reaches a stop
   condition.
7. Write a final lane result and status closeout.
8. Stop.  Do not compare against the other lane and do not edit coordinator
   synthesis files.

Claude may be used as a read-only reviewer inside a lane, but Claude is not an
execution authority and does not authorize boundary crossings.

## No Mid-Lane Merge Rule

After launch, the coordinator does not synthesize or compare partial lane
state.  The agents do not read each other's intermediate artifacts as inputs.

Allowed cross-lane events are only:

- shared contract conflict;
- shared file ownership conflict;
- unanticipated public API/default/export boundary;
- unanticipated GPU/network/package/resource boundary;
- evidence that a lane's planned commands cannot answer its stated question;
- user-requested stop or reassignment.

All other questions stay inside the lane until final closeout.

## Proposed Wave 2 Assignments

| Active agent | Algorithm family | Lane status family | Parallel class |
| --- | --- | --- | --- |
| peer agent | Low-rank coupling solver-route validation | `LOW_RANK_COUPLING_VALIDATION_*` | algorithm-complete independent lane |
| current agent | Positive-feature Sinkhorn route | `POSITIVE_FEATURE_SINKHORN_*` | algorithm-complete independent lane |

## Peer-Agent Lane: Low-Rank Coupling Solver-Route Validation

Entry context:

- P12 diagnostic status:
  `LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY`.
- Existing implementation:
  `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`.
- Existing tests and diagnostics remain lane-local context.

Objective:

Validate the low-rank coupling route as an experimental algorithm candidate
under a stronger source/boundary/artifact contract, without claiming default
readiness or dense Sinkhorn equivalence.

Owned future files should use a new Wave-2 prefix, for example:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-master-program-2026-06-19.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-status-2026-06-19.md`
- `docs/benchmarks/scalable_ot_wave2_low_rank_coupling_validation.py`
- `docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.json`
- `docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.md`

Forbidden:

- editing positive-feature lane files;
- editing Phase 1 baseline or Phase 3 schema;
- changing public exports/defaults;
- claiming full solver fidelity without source anchors and direct checks;
- treating dense-reference deltas as ranking evidence.

## Current-Agent Lane: Positive-Feature Sinkhorn Route

Entry context:

- Source audit:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-audit-2026-06-17.md`.
- Earlier prototype context may be read but must not be treated as final Wave-2
  evidence.

Objective:

Build and test a TensorFlow positive-feature Sinkhorn transport route as an
approximate-kernel or semantic-replacement algorithm candidate, preserving the
feature-kernel semantic delta from dense entropic OT.

Owned future files should use a new Wave-2 prefix, for example:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-master-program-2026-06-19.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-status-2026-06-19.md`
- `experiments/dpf_implementation/tf_tfp/resampling/positive_feature_sinkhorn_tf.py`
- `tests/test_positive_feature_sinkhorn_tf.py`
- `docs/benchmarks/scalable_ot_wave2_positive_feature_diagnostics.py`
- `docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.json`
- `docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.md`

Forbidden:

- editing low-rank coupling lane files;
- editing Phase 1 baseline or Phase 3 schema;
- changing public exports/defaults;
- reporting scalar Sinkhorn cost without transported particles;
- silently treating feature-kernel transport as dense Gibbs Sinkhorn
  equivalence;
- using random-feature luck as promotion evidence without a predeclared
  replication or uncertainty contract.

## Communication Protocol

Coordinator-owned files:

- this structure file;
- one future Wave-2 coordination record;
- one future final Wave-2 merge result.

Lane-owned files:

- one status file per lane;
- lane master program and subplans;
- lane implementation, tests, diagnostics, JSON/Markdown outputs, and final
  result.

Rules:

- Each agent reads the Wave-2 coordination record before acting.
- Each agent updates only its own lane-owned records.
- Each agent does not read the other lane's intermediate artifacts as evidence.
- Cross-lane questions are written as `QUESTION_FOR_COORDINATOR` in the
  lane-owned status file.
- The coordinator answers only if the question affects a frozen shared
  contract, ownership boundary, resource approval, or stop condition.

## Final Merge Gate

The coordinator merge starts only after:

- both lanes write final result/status closeout files; or
- one lane writes a true blocker and the coordinator records whether the other
  lane can continue independently to closeout.

The final merge must not rank algorithms unless a predeclared comparative
evidence contract and uncertainty analysis exist.  Under the default Wave-2
structure, the merge records:

- which lanes passed their own hard veto screens;
- which lanes remain viable under their own evidence contracts;
- which lanes are blocked or rejected for their own stated criteria;
- what separate next-phase plan, if any, is justified.

## Note To Send To The Other Agent

Read
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-algorithm-complete-parallel-execution-structure-2026-06-19.md`.

Future parallel work should use algorithm-complete lanes.  There are exactly two
active agents: `peer agent` and `current agent`.  Each agent owns one different
algorithm family, writes its own master program/subplans/status/result files,
runs its own tests and diagnostics to lane closeout, and then stops.  Do not
request or perform mid-lane synthesis.  Do not read the other lane's
intermediate artifacts as evidence.  Ask the coordinator only for shared
contract, write-ownership, approval, resource, or stop-condition issues.

Recommended next assignment is:

- `peer agent`: low-rank coupling solver-route validation.
- `current agent`: positive-feature Sinkhorn route.

No lane may claim speedup, ranking, posterior correctness, HMC readiness,
public API readiness, production/default readiness, dense Sinkhorn equivalence,
or broad scalable-OT selection.

## Launch Status

Not launched.  A separate Wave-2 coordination record and lane master programs
must be written before execution.
