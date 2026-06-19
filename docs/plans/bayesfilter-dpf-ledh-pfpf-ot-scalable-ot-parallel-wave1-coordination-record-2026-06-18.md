# Parallel Wave 1 Coordination Record

Date: 2026-06-18
Coordinator: Codex

## Status

`WAVE1_COORDINATOR_MERGE_COMPLETED_LOW_RANK_SOLVER_ROUTE_REMAINS_DIAGNOSTIC_ONLY_SPARSE_NOT_REOPENED`

## Purpose

Make the parallel-wave plan operational through repository artifacts rather
than chat copy/paste.  Agents must communicate by reading this coordinator
record and updating only their own lane communication record.  Shared ledgers
and stop handoffs are coordinator-owned during the active wave.

## Frozen Shared Contracts

These contracts are frozen for Wave 1:

- Phase 1 dense/streaming TensorFlow baseline remains the common comparator
  where dense-reference deltas are reported.
- Phase 3 candidate schema remains read-only:
  `docs/benchmarks/scalable_ot_candidate_result_schema.py`.
- Transport-object convention is frozen:
  - record `transport_object.kind`;
  - record `materialized`;
  - record `factor_shapes` or `shape` as applicable;
  - record `orientation`;
  - record `semantic_output`.
- CPU-only diagnostics must set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow
  import.
- Runtime and memory fields are explanatory only until a reviewed evidence
  contract says otherwise.
- No lane may claim speedup, ranking, posterior correctness, HMC readiness,
  public API readiness, production readiness, default readiness, or broad
  scalable-OT selection.

Any lane needing a shared contract change must stop and write
`BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED` in its lane record.

## Communication Protocol

Agents communicate only through files under `docs/plans`.

Coordinator-owned records:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-parallel-wave1-coordination-record-2026-06-18.md`
- shared visible ledger and shared stop handoff, if updated after lane closeout.

Lane-owned records:

- peer agent:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-peer-agent-wave1-low-rank-solver-status-2026-06-18.md`
- current agent:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-current-agent-wave1-sparse-locality-status-2026-06-18.md`

Rules:

- Agents read this coordinator record before acting.
- Agents update only their own lane-owned status/result artifacts.
- Agents do not edit the other agent's status record.
- Agents do not edit shared ledger/stop-handoff files during active parallel
  execution.
- Cross-lane questions are recorded as `QUESTION_FOR_COORDINATOR` in the
  lane-owned status record.
- The coordinator answers by updating this coordinator record or by writing a
  separate coordinator amendment.

## Wave 1 Assignments

| Agent | Lane | Status file | Parallel class |
| --- | --- | --- | --- |
| peer agent | P12 true low-rank coupling solver-route plan/prototype | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-peer-agent-wave1-low-rank-solver-status-2026-06-18.md` | true parallel independent algorithm lane |
| current agent | LEDH-specific sparse locality screen | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-current-agent-wave1-sparse-locality-status-2026-06-18.md` | true parallel independent diagnostic lane |

The independent Phase 11 Nystrom review is complete with status
`PHASE_11_NYSTROM_INDEPENDENT_REVIEW_AGREE`; that completed review is not an
active Wave 1 execution lane unless reassigned in a later coordinator
amendment.

This coordinator record supersedes older role labels in historical plans or
lane subplans.  For Wave 1, exactly two agents are active: `peer agent` and
`current agent`.

## Peer-Agent Lane Contract

The peer agent owns P12 true low-rank coupling solver-route work.

Read first:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-parallel-execution-structure-2026-06-18.md`

Owned files:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
- `tests/test_low_rank_coupling_solver_tf.py`
- `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-peer-agent-wave1-low-rank-solver-status-2026-06-18.md`

Read-only context:

- Phase 1 baseline artifacts.
- Phase 3 schema helper.
- Phase 6 low-rank coupling fixture-route files and result.
- Phase 11 Nystrom artifacts.
- shared visible ledger and shared stop handoff.

Required status updates in the peer-agent status file:

- `LANE_ACCEPTED`
- `IMPLEMENTATION_STARTED`
- `FIRST_CHECKS_RUN`
- `DIAGNOSTIC_RUN_COMPLETE`
- final lane status or blocker

The checks already run against
`low_rank_coupling_transport_tf.py` are Phase 6 context checks only.  They do
not count as P12 solver-route evidence.

## Current-Agent Lane Contract

The current agent owns an LEDH-specific sparse locality screen.

Read first:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-parallel-execution-structure-2026-06-18.md`
- Phase 8 sparse locality result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p08-sparse-localized-diagnostic-result-2026-06-17.md`

Owned files:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-subplan-2026-06-18.md`
- `docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py`
- `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-current-agent-wave1-sparse-locality-status-2026-06-18.md`

Input data rule:

- Use deterministic synthetic/archived LEDH-like particles only unless a
  coordinator amendment freezes an actual LEDH post-flow particle artifact by
  exact path, git commit or content hash, generation command, and approval
  note.

Required boundaries:

- Diagnostic only; do not implement a sparse solver.
- Do not edit Phase 8 artifacts.
- Do not edit Phase 1 baseline artifacts.
- Do not edit Phase 3 schema.
- Do not edit peer-agent files.
- Passing this screen may reopen a sparse implementation plan; it does not
  validate sparse OT, speedup, posterior correctness, or default readiness.

Required status updates in the current-agent status file:

- `LANE_ACCEPTED`
- `SUBPLAN_WRITTEN`
- `FIRST_CHECKS_RUN`
- `DIAGNOSTIC_RUN_COMPLETE`
- final lane status or blocker

## Coordinator Merge Rule

No synthesis or comparative decision should start until:

- peer agent writes a final P12 result or blocker; and
- current agent writes a final sparse-locality result or blocker; or
- the coordinator records that one lane was intentionally not launched.

The merge result must read lane-owned records and artifacts.  It must not infer
rankings from descriptive metrics without a predeclared uncertainty analysis.

## Wave 1 Merge Result

Coordinator merge completed on 2026-06-19:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave1-coordinator-merge-result-2026-06-19.md`

Merge decision:

- The peer-agent P12 low-rank coupling solver route remains open only as a
  diagnostic-only candidate under
  `LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY`.
- The current-agent P12E LEDH sparse-locality lane is closed for now under
  `LEDH_SPARSE_LOCALITY_SCREEN_COMPLETED_DOES_NOT_REOPEN_SPARSE_IMPLEMENTATION`.
- No ranking, default selection, speedup, posterior correctness, HMC readiness,
  public API readiness, production readiness, dense Sinkhorn equivalence, or
  broad scalable-OT selection claim is made.

Next justified action: draft a reviewed next-phase validation subplan for the
P12 low-rank solver route before any further implementation or diagnostic
execution.

## Message To Peer Agent

Read this coordinator record before any further work.  This record supersedes
older alphabet-agent labels in prior plans or subplans.  For Wave 1 there are
exactly two active agents:

- `peer agent`
- `current agent`

The peer agent owns only the P12 true low-rank coupling solver-route lane.
Proceed only within the peer-agent owned file set listed above.  Do not edit
the current-agent status/result files, shared visible ledgers, shared stop
handoffs, Phase 1 baseline artifacts, Phase 3 schema helper, or BayesFilter
public API/default exports.

Before implementing, update the peer-agent status file with
`IMPLEMENTATION_STARTED` or a blocker/question.  The checks previously run
against `low_rank_coupling_transport_tf.py` count only as Phase 6 context
checks; they are not P12 solver-route evidence.

If a cross-lane issue appears, do not resolve it by reading or editing
current-agent artifacts as inputs.  Write `QUESTION_FOR_COORDINATOR` in the
peer-agent status file and wait for a coordinator amendment or coordinator
record update.

The peer-agent final result should preserve the evidence contract boundaries:
finite/nonnegative/Phase-3-valid transport-object factors only; no claims of
speedup, ranking, posterior correctness, HMC readiness, public API readiness,
production/default readiness, or dense Sinkhorn equivalence.

## Open Coordinator Questions

None.
