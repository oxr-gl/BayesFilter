# Wave 2 Peer-Agent Master Program: Low-Rank Coupling Validation

Date: 2026-06-19
Owner: peer agent

## Status

`LOW_RANK_COUPLING_VALIDATION_PASSED_DIAGNOSTIC_ONLY`

## Program Objective

Execute the Wave 2 peer-agent lane for low-rank coupling solver-route
validation as an algorithm-complete independent lane.  The lane validates the
existing TensorFlow low-rank coupling solver-route candidate under a stronger
Wave 2 source, boundary, artifact, and diagnostic contract.

This program does not perform coordinator synthesis and does not read the
current-agent positive-feature Sinkhorn intermediate artifacts as evidence.

## Governing Inputs

- Wave 2 structure:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-algorithm-complete-parallel-execution-structure-2026-06-19.md`
- User/coordinator assignment in the active conversation:
  peer agent owns low-rank coupling solver-route validation; current agent owns
  positive-feature Sinkhorn route.
- Existing P12 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-result-2026-06-18.md`
- Existing P12 implementation:
  `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`

The Wave 2 structure file still says not launched, but the user/coordinator
assignment explicitly launches this peer-agent lane.  The peer agent will not
edit coordinator-owned Wave 2 records.

## Owned Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-*-2026-06-19.md`
- `docs/benchmarks/scalable_ot_wave2_low_rank_coupling_validation.py`
- `docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.json`
- `docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.md`
- `docs/benchmarks/logs/wave2-low-rank-coupling-*.log`
- `tests/test_wave2_low_rank_coupling_validation.py`

Read-only lane context:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
- `tests/test_low_rank_coupling_solver_tf.py`
- `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py`
- P12 low-rank solver-route result/status/diagnostic artifacts.
- Phase 3 candidate result schema.
- Phase 1 dense/streaming baseline only as descriptive context if explicitly
  used by diagnostics.

Forbidden writes include positive-feature Sinkhorn lane files, coordinator
records, Phase 1 baseline files, Phase 3 schema, public exports/defaults, Phase
6 fixture-route files, Agent A/Nystrom artifacts, package metadata, and
unrelated dirty worktree files.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the low-rank coupling solver-route candidate pass a Wave 2 lane-local hard-veto validation screen for finite nonnegative `Q,R,g` factors, finite transported particles, valid lazy/materialized apply parity, Phase 3 candidate-record validity, and preserved source/boundary classifications? |
| Baseline/comparator | P12 diagnostic result is the entry context. Phase 1 dense/streaming baseline is not a promotion comparator in this Wave 2 lane. Runtime, memory, and any dense-reference deltas remain explanatory only. |
| Primary pass criterion | CPU-only validation script exits 0, JSON validates under Phase 3 schema, all fixture rows pass finite/nonnegative/positive-factor checks, factor and induced residuals are below fixed thresholds, materialized tiny apply parity is below threshold, source-route classifications match the allowed Wave 2 contract, and forbidden-claim scans pass. |
| Veto diagnostics | Missing or invalid `Q,R,g`, negative/nonfinite factors, nonpositive `g`, nonfinite transported particles, residual threshold failure, apply-parity failure, schema failure, source-route overclaim, positive-feature artifact dependency, external solver execution, package/network/GPU requirement, public export/default edit, or shared contract change. |
| Explanatory diagnostics | Projection iterations, projection error, floor hits, factor minima, fixture shapes, rank, runtime, and memory proxies. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or full solver-fidelity claim for extension components. |
| Preserving artifacts | Wave 2 peer-lane subplans/results/status, validation script, focused test, logs, JSON, and Markdown diagnostics. |

## Source-Route Boundary

- `source_faithful`: `Q diag(1/g) R^T` factor form, lazy apply, factor marginal
  diagnostics, and Dykstra-style projection only where actually mirrored.
- `fixed_hmc_adaptation`: deterministic initialization, rank, floors,
  schedules, and Phase 1 scaled transport adapter.
- `extension_or_invention`: cost-nudged assignment kernel, simplified update,
  and any unanchored stabilization.

Overall route classification remains `extension_or_invention`.

## Phase Index

| Phase | Name | Subplan | Result artifact |
| --- | --- | --- | --- |
| W2-LR-0 | Governance And Intake | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-p00-governance-intake-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-p00-governance-intake-result-2026-06-19.md` |
| W2-LR-1 | Validation Implementation And Replay | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-p01-validation-replay-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-p01-validation-replay-result-2026-06-19.md` |
| W2-LR-2 | Lane Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-p02-closeout-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-result-2026-06-19.md` |

## Repair Loop Protocol

For each phase, run the smallest checks that answer the phase question.  If a
fixable issue is in a peer-lane-owned artifact, patch visibly and rerun focused
checks.  Stop with `BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED` if the lane needs a
shared contract edit.  Stop with `LOW_RANK_COUPLING_VALIDATION_BLOCKED` if the
route cannot produce valid finite low-rank factors and transported particles
without forbidden actions.

Claude is optional read-only review only.  It cannot authorize boundary
crossings or scientific/product claims.

## Skeptical Plan Audit

Audit result before execution: passed with one recorded caveat.  The Wave 2
structure file is still draft/not-launched, but the user/coordinator assignment
explicitly assigns this peer-agent lane and forbids current-agent artifact use.
Proceeding lane-locally does not require editing coordinator-owned records.

The plan does not treat dense-reference deltas, runtime, or memory as promotion
criteria; has explicit stop conditions; uses CPU-only diagnostics; preserves
source-route classifications; and does not compare against the current-agent
positive-feature lane.

## Closeout Status

The peer-agent Wave 2 lane completed:

- P00 governance/intake passed.
- P01 validation replay passed.
- Final result/status closeout recorded
  `LOW_RANK_COUPLING_VALIDATION_PASSED_DIAGNOSTIC_ONLY`.

The lane stops here.  No coordinator synthesis, cross-lane comparison, public
export/default change, or readiness claim is authorized by this program.
