# Master Program: P12 Low-Rank Coupling Solver Route Lane

Date: 2026-06-19

## Status

`VISIBLE_EXECUTION_COMPLETE_LANE_LOCAL_CLAUDE_PATH_ONLY_R5_AGREE`

## Program Objective

Govern the peer-agent Wave 1 P12 lane for a TensorFlow low-rank coupling
solver-route prototype.  The lane asks whether a source-grounded route can
produce finite, nonnegative, Phase 3-valid `Q,R,g` low-rank coupling factors
and transported particles beyond the Phase 6 fixture route.

This master program is the lane-level governance layer under the Wave 1
coordination record.  It does not authorize edits outside the peer-agent owned
file set and does not authorize public API, default-policy, runtime-ranking,
posterior-correctness, HMC-readiness, production-readiness, or dense Sinkhorn
equivalence claims.

## Governing Inputs

- Wave 1 coordinator:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-parallel-wave1-coordination-record-2026-06-18.md`
- Parallel execution structure:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-parallel-execution-structure-2026-06-18.md`
- Existing P12 lane subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-subplan-2026-06-18.md`
- Existing P12 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-result-2026-06-18.md`
- Existing peer-agent status record:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-peer-agent-wave1-low-rank-solver-status-2026-06-18.md`

## Owned Write Set

The program may write only peer-agent P12 lane artifacts:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
- `tests/test_low_rank_coupling_solver_tf.py`
- `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-*-2026-06-19.md`
- `docs/benchmarks/logs/p12-low-rank-solver-route-*.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-peer-agent-wave1-low-rank-solver-status-2026-06-18.md`

Forbidden writes include current-agent sparse-locality artifacts, shared
ledger/handoff files, Phase 1 baseline artifacts, Phase 3 schema helper, Phase
6 fixture-route files, Agent A Nystrom artifacts, public exports, package
metadata, and any unrelated dirty worktree files.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the P12 peer-agent lane produce finite, nonnegative, Phase 3-valid `Q,R,g` low-rank coupling factors and transported particles under the frozen Wave 1 contracts? |
| Baseline/comparator | Phase 1 dense/streaming TensorFlow baseline is descriptive only for semantic deltas; Phase 6 fixture checks are read-only context and do not validate P12. |
| Primary pass criterion | P12 writes a valid implementation, tests, diagnostic script, JSON/Markdown diagnostics, status record, and result note showing finite nonnegative factors, positive `g`, finite transported particles, residuals below predeclared thresholds, candidate schema validation, and explicit source-route classification. |
| Veto diagnostics | Missing or invalid `Q,R,g`, nonpositive `g`, negative/nonfinite factors, nonfinite transported particles, invalid orientation, missing factor diagnostics, schema failure, external solver execution, shared contract change, or unsupported claim. |
| Explanatory diagnostics | Dense-reference particle deltas, runtime, memory proxy, rank, iteration count, projection residuals, source-route component table. |
| Not concluded | No dense Sinkhorn equivalence, speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, broad scalable-OT selection, or full solver-fidelity claim for extension components. |
| Preserving artifacts | Phase subplans/results, implementation/test/diagnostic files, JSON/Markdown diagnostics, peer-agent status record, Claude review ledger, visible execution ledger, and stop handoff. |

## Pinned Replay Thresholds

These P12 replay thresholds are fixed before replay and must not be changed
after seeing results:

| Diagnostic | Threshold | Source |
| --- | ---: | --- |
| factor marginal residual | `<= 5.0e-3` | existing P12 subplan and `VALIDITY_THRESHOLD` in `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py` |
| induced row residual | `<= 5.0e-3` | existing P12 subplan and `VALIDITY_THRESHOLD` in `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py` |
| induced column residual | `<= 5.0e-3` | existing P12 subplan and `VALIDITY_THRESHOLD` in `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py` |
| materialized tiny apply parity | `<= 1.0e-10` | existing P12 subplan and `MATERIALIZED_PARITY_THRESHOLD` in `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py` |

## Source-Route Boundary

- `source_faithful`: directly anchored `Q diag(1/g) R^T`, lazy apply, factor
  marginal diagnostics, and Dykstra-style projection if actually mirrored.
- `fixed_hmc_adaptation`: deterministic initialization, rank choices, floors,
  fixed schedules, CPU-only fixture choices, and Phase 1 scaled adapter.
- `extension_or_invention`: simplified objective/update/stabilization,
  cost-nudged assignment kernel, or any route not present in the cited source.

Overall route claims must remain at the weakest applicable classification.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P12-0 | Governance, Source Anchors, And Review Gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p00-governance-source-lock-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p00-governance-source-lock-result-2026-06-19.md` |
| P12-1 | Intake And Artifact Baseline | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p01-intake-artifact-baseline-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p01-intake-artifact-baseline-result-2026-06-19.md` |
| P12-2 | Implementation And Diagnostic Replay | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p02-implementation-diagnostic-replay-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p02-implementation-diagnostic-replay-result-2026-06-19.md` |
| P12-3 | Result Closeout And Status Sync | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p03-result-closeout-status-sync-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p03-result-closeout-status-sync-result-2026-06-19.md` |
| P12-4 | Read-Only Independent Review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p04-readonly-independent-review-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p04-readonly-independent-review-result-2026-06-19.md` |
| P12-5 | Coordinator Handoff Readiness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p05-coordinator-handoff-readiness-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p05-coordinator-handoff-readiness-result-2026-06-19.md` |

## Repair Loop Protocol

For each phase:

1. Run the smallest local check that can answer the phase question.
2. If a problem is in a P12-owned artifact and is fixable without crossing a
   boundary, patch visibly and rerun focused checks.
3. If a problem requires a shared contract change, write
   `BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED` and stop.
4. If the route cannot produce finite nonnegative `Q,R,g` and transported
   particles without forbidden actions, write `LOW_RANK_SOLVER_ROUTE_BLOCKED`
   and stop.
5. Send material subplans/results to Claude Opus at max effort as read-only
   review only after explicit user approval.
6. Stop after five Claude review rounds for the same blocker and write a
   blocker result.

Claude cannot authorize crossing human, runtime, model-file, funding,
product-capability, shared-contract, or scientific-claim boundaries.

## Convergence And No-Invalid-Stop Rule

The supervisor must not stop for vague discomfort, long output, nonblocking
wording issues, or expected diagnostic-only limitations.  A phase advances when
its evidence contract is met and material review has converged.  A phase stops
only when a declared stop condition fires, a human approval is required, or a
same-blocker Claude/Codex loop fails to converge after five rounds.  Nonblocking
findings are recorded and carried forward without halting the program.

## Program Stop Conditions

Stop before further execution if:

- Claude Code approval is not granted for required material reviews;
- source anchors contradict the factor or `g` convention;
- Phase 1 baseline or Phase 3 schema is absent or inconsistent;
- executing a phase requires package installation, network, GPU evidence,
  external POT/OTT solver execution, public export changes, shared contract
  edits, destructive filesystem/git actions, or current-agent file edits;
- Codex and Claude fail to converge after five review rounds on the same
  material blocker.

## Review And Execution Status

User approval for Claude Code read-only review and visible local phase
execution was granted on 2026-06-19.  P12-0 governance review converged with
Claude at round 4 (`VERDICT: AGREE`).

For P12-4, the user clarified that Claude should receive paths and bounded
questions, not pasted file contents.  A path-only Claude artifact review round
1 ran and returned `VERDICT: REVISE`: the technical artifacts were
conservative and boundary-safe, but P12-4/P12-5 had a procedural mismatch
because they claimed pass while saying the required Claude artifact review was
not performed.

Codex repaired the P12-4/P12-5 procedural wording.  Focused Claude path-only
round 2 returned `VERDICT: REVISE` because the visible execution ledger still
contained stale pass/complete entries and two lines allowed overly loose
finalization.  Codex repaired those issues.

Focused Claude path-only round 3 returned `VERDICT: REVISE` on one remaining
P12-5 subplan wording issue: an explanatory diagnostics row still used loose
review-note wording.  Codex repaired that wording.

Focused Claude path-only round 4 returned `VERDICT: REVISE` on one remaining
P12-5 subplan handoff condition that did not require focused Claude `VERDICT:
AGREE`.  Codex repaired that handoff condition.

Focused Claude path-only round 5 returned `VERDICT: AGREE` on the repaired
P12-4/P12-5 procedural handoff scope.  The P12 lane-local visible execution is
complete.  The underlying diagnostic status remains
`LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY`; no coordinator merge, ranking,
default claim, public API readiness, HMC readiness, production readiness,
posterior correctness, speedup, or dense Sinkhorn equivalence is authorized.
