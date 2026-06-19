# Wave 2 Coordinator Master Program

Date: 2026-06-19
Coordinator/supervisor: Codex in the current conversation
Read-only reviewer: Claude Opus max effort, by compact packet only

## Status

`WAVE2_COORDINATOR_MASTER_PROGRAM_COMPLETE`

## Purpose

Govern Wave 2 algorithm-complete parallel execution with exactly two active
agents and minimal interaction.  Each agent owns one complete algorithm family,
runs independently to lane closeout, and stops.  Coordinator synthesis happens
only after both lanes close or one writes a true blocker.

## Assignments

| Active agent | Algorithm family | Status file | Current status |
| --- | --- | --- | --- |
| `peer agent` | low-rank coupling solver-route validation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-status-2026-06-19.md` | already closed as `LOW_RANK_COUPLING_VALIDATION_PASSED_DIAGNOSTIC_ONLY` if the peer-owned status/result artifacts remain valid |
| `current agent` | positive-feature Sinkhorn route | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-status-2026-06-19.md` | planned, not yet closed |

New operational records must not use alphabet-agent labels.  Historical files
may retain old titles, but Wave 2 active roles are only `peer agent` and
`current agent`.

## Shared Contracts

- Phase 1 dense/streaming TensorFlow baseline is read-only comparator context.
- Phase 3 candidate schema is read-only:
  `docs/benchmarks/scalable_ot_candidate_result_schema.py`.
- Transport-object records declare `kind`, `materialized`, `factor_shapes` or
  `shape`, `orientation`, and `semantic_output`.
- CPU-only TensorFlow commands set `CUDA_VISIBLE_DEVICES=-1` before import.
- Runtime and memory are explanatory only.
- No package install, network fetch, GPU evidence, public API/default/export
  edit, or shared schema/baseline edit is authorized by this program.
- No speedup, ranking, posterior correctness, HMC readiness, public API
  readiness, production/default readiness, dense Sinkhorn equivalence, or
  broad scalable-OT selection claim is authorized.

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Wave 2 operationalize two independent algorithm-complete lanes with final-only coordinator merge and no mid-lane synthesis? |
| Baseline/comparator | Wave 2 algorithm-complete structure, existing lane artifacts, Phase 1/Phase 3 shared contracts, and lane-owned evidence contracts. |
| Primary pass criterion | Coordinator records valid lane ownership, both lane programs/statuses exist, current-agent positive-feature lane closes or blocks under its own contract, and coordinator merge occurs only after final lane status availability. |
| Veto diagnostics | Any write-set collision, shared contract change, use of another lane's intermediate artifacts as evidence, unsupported claim, missing lane result, failed planning review that cannot be repaired, or required unapproved boundary crossing. |
| Explanatory diagnostics | Existing peer-agent low-rank status, current-agent positive-feature replay metrics, runtime/log paths, Claude review findings. |
| Not concluded | No algorithm ranking, no default selection, no speedup, no posterior correctness, no HMC/API/production readiness, no dense Sinkhorn equivalence, and no broad scalable-OT selection. |
| Artifacts | This master program, phase subplans/results, lane master programs/statuses/results, runbook, review packet/ledger, final merge result. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| W2-0 | Coordinator Launch Packet And Review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p00-coordinator-launch-packet-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p00-coordinator-launch-packet-result-2026-06-19.md` |
| W2-1 | Current-Agent Positive-Feature Execution | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p01-current-positive-feature-execution-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p01-current-positive-feature-execution-result-2026-06-19.md` |
| W2-2 | Final Coordinator Merge | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p02-final-merge-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-final-merge-result-2026-06-19.md` |

## Phase Advancement Rule

Each phase may start only after:

- its dedicated subplan exists;
- inherited entry conditions are satisfied;
- required local checks from the previous phase have passed or a blocker result
  has been written;
- material Claude review has converged, or review is explicitly unnecessary
  for a non-material record-only phase;
- no human-required stop condition is active.

At the end of each phase, Codex must:

1. run the required local checks;
2. write a phase result/close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Claude Review Protocol

Claude is read-only reviewer only and cannot authorize crossing human,
runtime, model-file, funding, product-capability, public API/default, or
scientific-claim boundaries.

Prompts must be compact.  Do not paste whole files.  Provide paths, summaries,
evidence contracts, stop conditions, changed sections, and targeted review
questions.  If Claude does not respond, run a tiny read-only probe; if the
probe responds, redesign the prompt.

For material findings, patch the relevant subplan visibly, rerun focused local
checks, and rerun focused Claude review.  Stop after five rounds for the same
blocker and write a blocker result.

## Valid Stop Conditions

Stop if continuing requires:

- package install, network fetch, credentials, GPU evidence, external solver,
  destructive action, or public API/default/export change;
- editing Phase 1 baseline, Phase 3 schema, peer-owned low-rank artifacts, or
  unrelated dirty worktree files;
- changing evidence thresholds after seeing results;
- using the other lane's intermediate artifacts as evidence;
- making a forbidden claim;
- Claude/Codex nonconvergence after five review rounds for the same material
  blocker.

## Launch Status

W2-0 review/repair completed with Claude `VERDICT: AGREE`.  W2-1 current-agent
positive-feature execution passed.  W2-2 final coordinator merge completed.

Final merge:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-final-merge-result-2026-06-19.md`
