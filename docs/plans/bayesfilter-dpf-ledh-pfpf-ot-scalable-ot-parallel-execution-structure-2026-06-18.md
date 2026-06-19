# Two-Agent Parallel Execution Structure For Scalable OT Follow-On Work

Date: 2026-06-18
Author: Codex

## Purpose

Design an operational parallel execution structure for the next scalable OT
follow-on work using exactly two active agents:

- `peer agent`
- `current agent`

The prior planning mistake was treating a dependent review as parallel
execution.  If a review verdict depends on another lane's artifacts, final
review is sequential with respect to those artifacts.  True parallel execution
comes from assigning the two active agents independent lanes with disjoint write
sets, frozen shared contracts, file-based communication, and a later
coordinator merge.

## Current Context

- Phase 10 ended with
  `PHASE_10_COMPARATIVE_DECISION_COMPLETED_NO_DEFAULT_ALGORITHM_YET`.
- The reduced-rank Nystrom diagnostic completed with status
  `PHASE_11_REDUCED_RANK_NYSTROM_LADDER_PASSED_DIAGNOSTIC_ONLY`.
- The independent Nystrom review completed with status
  `PHASE_11_NYSTROM_INDEPENDENT_REVIEW_AGREE`.
- Those completed Nystrom artifacts are read-only context for Wave 1 unless a
  later coordinator amendment assigns a follow-up.
- BayesFilter defaults remain unchanged.
- Runtime and memory proxy fields remain explanatory until validity gates pass.
- No speedup, ranking, posterior-correctness, HMC-readiness, public API, or
  production/default-readiness claim is allowed without a new reviewed evidence
  contract.

## Parallelism Rule

Classify each proposed lane before launch:

| Lane type | Parallel status | Rule |
| --- | --- | --- |
| Independent algorithm lane | True parallel | Can execute concurrently after shared contracts are frozen, because it owns a separate algorithm, files, artifacts, and evidence contract. |
| Independent diagnostic lane | True parallel | Can execute concurrently if it answers a separate diagnostic question and has a disjoint write set. |
| Dependent review lane | Partial parallel | Can prepare tests and review scripts early, but its final verdict depends on another lane's artifacts. |
| Comparative synthesis lane | Sequential merge | Must wait for lane results and reviews; it is not a parallel implementation lane. |
| Shared infrastructure edit | Coordinator-controlled | Must be serialized or explicitly assigned because it can break both lanes. |

If a lane cannot name its independent question, comparator, write set, and stop
conditions without relying on another unfinished lane, it is not true parallel
execution.

## Coordinator Gate Before Parallel Launch

Run one short coordinator phase before launching the two agents.

Coordinator responsibilities:

1. Freeze shared comparator contracts:
   - Phase 1 dense/streaming TensorFlow baseline remains the common comparator
     where dense-reference comparison is required.
   - Phase 3 candidate schema remains the common reporting schema.
   - The transport-object interface is frozen for the wave: every lane must
     declare `transport_object.kind`, `materialized`, `factor_shapes` or
     `shape` as applicable, `orientation`, and `semantic_output` using the
     Phase 3 schema conventions.  The schema helper
     `docs/benchmarks/scalable_ot_candidate_result_schema.py` and Phase 1
     baseline diagnostic script are read-only shared infrastructure.
   - CPU-only diagnostics use `CUDA_VISIBLE_DEVICES=-1` before TensorFlow
     import.
   - Any downstream smoke harness must either be coordinator-frozen by exact
     path before launch or vendored into a lane-owned diagnostic script.  A
     lane must not silently change shared downstream harness semantics.
2. Freeze global non-claims:
   - no speedup claim;
   - no ranking claim;
   - no posterior correctness claim;
   - no HMC readiness claim;
   - no production/default readiness claim;
   - no public API readiness claim.
3. Assign disjoint write sets.
4. Define merge artifact names and lane statuses.
5. Record active blockers and dirty-worktree exclusions.
6. Decide whether each lane may execute, only prepare, or must wait.

Coordinator outputs:

- a lane assignment table;
- a shared contract snapshot;
- a file ownership map;
- a merge/synthesis plan;
- a stop handoff naming which lanes are true parallel and which are dependent.

## Communication Records

Parallel agents communicate through repository files, not chat copy/paste.  For
each wave, the coordinator writes one coordinator-owned record and each active
agent writes one agent-owned status record.

Wave 1 records:

- coordinator-owned:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-parallel-wave1-coordination-record-2026-06-18.md`
- peer-agent-owned:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-peer-agent-wave1-low-rank-solver-status-2026-06-18.md`
- current-agent-owned:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-current-agent-wave1-sparse-locality-status-2026-06-18.md`

Rules:

- Each agent reads the coordinator record before acting.
- Each agent updates only its own status/result files.
- Neither agent edits the other agent's status record.
- Neither agent edits shared visible ledger or stop-handoff files during active
  parallel execution.
- Cross-lane questions are written as `QUESTION_FOR_COORDINATOR` in the
  lane-owned status record.
- The coordinator answers by updating the coordinator record or by writing a
  coordinator amendment under `docs/plans`.

## Wave 1 Assignments

| Agent | Lane | Parallel class | Main question | Output status family |
| --- | --- | --- | --- | --- |
| peer agent | P12 true low-rank coupling solver-route plan/prototype | true parallel independent algorithm lane | Can a source-grounded TensorFlow low-rank coupling solver route produce valid transport-object factors beyond the Phase 6 fixture route? | `LOW_RANK_SOLVER_ROUTE_*` |
| current agent | LEDH-specific sparse locality screen | true parallel independent diagnostic lane | Do deterministic or archived LEDH-like post-flow particles show enough locality to reopen sparse/localized work after Phase 8 blocked Phase 1 sparse implementation? | `LEDH_SPARSE_LOCALITY_SCREEN_*` |

The completed Nystrom diagnostic and completed independent review are not
active Wave 1 lanes.  They are read-only context unless a later coordinator
amendment reassigns work.

## Peer-Agent Lane: P12 Low-Rank Solver Route

Parallel status: true parallel.

Frozen dependency:

- This lane depends only on the coordinator-frozen Phase 1 baseline, Phase 3
  schema, and transport-object contract.  It must not wait for sparse-locality
  artifacts or any future synthesis artifact.

Owned files:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
- `tests/test_low_rank_coupling_solver_tf.py`
- `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-peer-agent-wave1-low-rank-solver-status-2026-06-18.md`

Required boundaries:

- TensorFlow/TensorFlow Probability implementation backend.
- No POT or external solver execution.
- No NumPy algorithmic backend except reference fixtures/sanity checks.
- Explicitly distinguish `source_faithful`, `fixed_hmc_adaptation`, and
  `extension_or_invention`.
- Do not claim dense Sinkhorn equivalence unless exact parity is tested under a
  reviewed contract.
- Do not change public API exports or BayesFilter defaults.

Required status updates:

- `LANE_ACCEPTED`
- `IMPLEMENTATION_STARTED`
- `FIRST_CHECKS_RUN`
- `DIAGNOSTIC_RUN_COMPLETE`
- final lane status or blocker

## Current-Agent Lane: LEDH Sparse Locality Screen

Parallel status: true parallel diagnostic lane.

Purpose:

- Reassess sparse/localized viability on LEDH-like post-flow geometry, because
  Phase 8 blocked sparse implementation only on Phase 1 fixtures.

Owned files:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-subplan-2026-06-18.md`
- `docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py`
- `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-current-agent-wave1-sparse-locality-status-2026-06-18.md`

Required boundaries:

- Diagnostic only; no sparse solver implementation in this lane.
- Use deterministic synthetic/archived LEDH-like particles unless the
  coordinator freezes an actual LEDH post-flow particle artifact by exact path,
  git commit or content hash, generation command, and approval note before
  lane launch.
- Predeclare locality/support thresholds and truncation residual rules.
- Passing the screen may reopen a sparse implementation plan; it does not
  validate sparse OT, speedup, posterior correctness, or default readiness.
- Use TensorFlow/TensorFlow Probability for BayesFilter-owned diagnostic code
  where differentiable or algorithmic code is needed.
- Do not change public API exports or BayesFilter defaults.

Required status updates:

- `LANE_ACCEPTED`
- `SUBPLAN_WRITTEN`
- `FIRST_CHECKS_RUN`
- `DIAGNOSTIC_RUN_COMPLETE`
- final lane status or blocker

## Deferred Work

Other useful lanes exist, such as Nystrom downstream LEDH smoke,
positive-feature downstream smoke, sliced/subspace downstream smoke, and a
shared manifest audit harness.  They are deliberately deferred in Wave 1
because there are only two active agents.  A later coordinator amendment may
assign one of them after one active lane finishes or is intentionally stopped.

Deferred work must not be represented as an active agent assignment in this
wave.

## Write-Set Isolation

Each active lane owns unique implementation, test, diagnostic, JSON/Markdown,
and result files.  Shared files are coordinator-controlled.

| Shared file or surface | Rule |
| --- | --- |
| `docs/benchmarks/scalable_ot_candidate_result_schema.py` | Do not edit in a lane.  Any change requires a coordinator amendment and both active agents must re-audit. |
| Phase 1 baseline fixture diagnostics | Read-only unless a coordinator amendment explicitly changes the comparator. |
| `visible-execution-ledger` and `visible-stop-handoff` | Coordinator-only during a parallel wave.  Lanes write per-lane handoff/result artifacts; the coordinator aggregates to shared ledgers after closeout. |
| BayesFilter public package exports | Do not edit.  No public API changes in this parallel wave. |
| Completed Nystrom artifacts | Read-only for review or downstream planning unless a later coordinator amendment assigns a follow-up. |
| Downstream smoke harness files | Coordinator-frozen by exact path or vendored into lane-owned diagnostics.  Do not share mutable downstream harness code across parallel lanes. |

## Evidence Contract Template For Each Lane

Every lane plan must state:

- scientific or engineering question;
- exact baseline or comparator;
- primary pass/promotion criterion;
- promotion vetoes;
- continuation vetoes;
- repair triggers;
- explanatory diagnostics;
- non-claims;
- artifact paths;
- expected commands;
- result status names;
- whether the lane is true parallel, partial parallel, or sequential.

For stochastic or downstream filtering comparisons, result interpretation must
also state whether any ranking is statistically supported.  With few seeds or
short chains, continuous metrics are descriptive only.

## Merge And Synthesis Gate

After both active lanes complete or stop, a coordinator writes a merge result.
This is sequential and must wait for lane closeout artifacts.

Merge questions:

1. Which lanes passed hard validity gates?
2. Which lanes are viable only as semantic replacements?
3. Which lanes remain blocked or need repair?
4. Did either lane change shared assumptions or invalidate the other lane's
   comparator?
5. Are any rankings statistically supported?  If not, say so.
6. What is the next smallest downstream LEDH-PFPF-OT validation step?

The merge result must not choose a default algorithm unless a reviewed
default-readiness evidence contract was written before the lane runs.  Any lane
reporting descriptive downstream metrics must include statistically
unsupported-ranking language by default unless it ran a predeclared uncertainty
analysis that supports ranking.

## Scheduling Model

Use two-agent wave scheduling:

1. Coordinator gate freezes shared contracts and write sets.
2. The peer agent and current agent execute their independent lanes
   concurrently.
3. Lane owners write result notes and lane status updates.
4. Synthesis waits for both lane statuses or records an explicit intentionally
   missing lane.
5. Only after synthesis may the coordinator assign new work or start a second
   wave.

Suggested Wave 1:

| Slot | Lanes |
| --- | --- |
| Start immediately | peer agent low-rank solver-route plan/prototype; current agent LEDH-specific sparse locality screen on a deterministic/archived fixture |
| Start after both lane artifacts exist | coordinator merge and comparative synthesis |
| Deferred until later amendment | Nystrom downstream smoke, positive-feature downstream smoke, sliced/subspace downstream smoke, shared manifest audit harness |

## Stop Conditions

Stop an individual lane if:

- it needs package install, network fetch, GPU evidence, or external solver
  execution not approved in its plan;
- it needs to edit the other active lane's owned files;
- the Phase 1 baseline or Phase 3 schema is missing or inconsistent;
- the frozen transport-object contract or downstream smoke harness contract is
  missing, ambiguous, or drifted since lane launch;
- source anchors contradict the route being implemented;
- the lane cannot produce a valid transport object or explicitly semantic
  output under its declared class;
- a default, speedup, ranking, posterior-correctness, or HMC-readiness claim
  would be required to interpret the result.

Stop the whole parallel wave if:

- a shared comparator/schema bug invalidates both lanes;
- a shared transport-object or downstream harness contract bug invalidates both
  lanes;
- dirty-worktree conflicts make write-set isolation impossible;
- a coordinator-controlled shared file must change and active lanes cannot
  safely re-audit;
- the scientific question changes enough that lane contracts no longer answer
  it.

## Expected Benefits And Limits

Expected benefits:

- True wall-clock speedup from two independent lanes.
- Cleaner evidence classes because each lane has its own contract.
- Later synthesis can compare readiness classes without pretending both lanes
  answered the same question.

Limits:

- Review verdicts remain dependent on reviewed artifacts.
- Shared schema or baseline changes serialize work.
- Descriptive fixture metrics cannot become rankings without uncertainty
  evidence.
- Parallel lane success does not imply production/default readiness.
- Only two agents are active; additional candidate lanes wait for a later
  coordinator amendment.

## Operational Message To Peer Agent

Read:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-parallel-wave1-coordination-record-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-parallel-execution-structure-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-peer-agent-wave1-low-rank-solver-status-2026-06-18.md`

Then proceed only on the peer-agent low-rank solver lane and update only the
peer-agent status/result files.  If a cross-lane issue appears, write
`QUESTION_FOR_COORDINATOR` in the peer-agent status file rather than editing
the current-agent record or shared ledgers.

## Current-Agent Next Action

The current agent should begin by writing the LEDH sparse-locality screen
subplan under its owned path, including skeptical plan audit, research intent
ledger, evidence contract, thresholds, commands, artifacts, and non-claims.
No diagnostic should run until that subplan exists and passes its own skeptical
audit.

## Claude Review Record

Claude read-only review of the initial draft returned `VERDICT: REVISE`.
Material findings were accepted and repaired:

- The sparse-locality lane now requires deterministic/archived LEDH-like
  particles or a coordinator-frozen actual particle artifact by path/hash
  before launch.
- Semantic-replacement downstream smoke ideas are deferred rather than bundled
  into Wave 1, avoiding hidden internal comparisons and ranking pressure.
- The coordinator gate freezes the transport-object contract and downstream
  smoke harness contract.
- Shared manifest-audit work is deferred and is not blocking for lane-local
  closeout unless a later coordinator amendment makes it mandatory at
  synthesis.
- Shared visible ledger and stop handoff files are coordinator-only during a
  parallel wave.
- Backend/default boundaries and the merge-level statistically
  unsupported-ranking rule are explicit.

Claude read-only review of the two-agent revision returned `VERDICT: AGREE`.
The review confirmed:

- only `peer agent` and `current agent` are active Wave 1 agents;
- communication is file-based through `docs/plans`;
- status-file paths are internally consistent;
- completed Nystrom work is read-only context, not an active Wave 1 lane;
- no stale alphabet-agent status path remains in the active coordination
  files.

Claude noted a residual soft-dependency risk because each lane status file
listed the other lane's artifacts as read-only inputs.  That risk was repaired
after review: the peer-agent status file now states that the current-agent
sparse-locality lane is not an input during active Wave 1 execution, and the
current-agent status file states the corresponding rule for the peer-agent
low-rank solver lane.  Cross-lane questions go through the coordinator record.
