# P12E Master Program: Current-Agent LEDH Sparse Locality Screen

Date: 2026-06-19
Owner: current agent
Supervisor/executor: Codex in the current conversation
Read-only reviewer: Claude Opus, max effort, when explicitly approved

Codex and Claude are execution/review roles, not additional active Wave 1
agents.  The only active Wave 1 agents remain `peer agent` and
`current agent`.

## Status

`P12E_MASTER_PROGRAM_REVIEWED_NOT_LAUNCHED_PENDING_USER_APPROVALS`

## Purpose

Govern the current-agent Wave 1 lane end to end with explicit phases, one
dedicated subplan per phase, visible gates, repair loops, and bounded
read-only Claude review.  This master program replaces the earlier compact
gate sketch for P12E.

This program does not launch execution.  It prepares the lane so execution can
start only after explicit human approval.

## Two-Agent Boundary

Exactly two agents are active in Wave 1:

- `peer agent`: P12 true low-rank coupling solver-route lane.
- `current agent`: P12E LEDH sparse-locality screen lane.

This master program governs only the current-agent lane.  The peer-agent lane
is independent and is not an input during active Wave 1 execution.  Cross-lane
questions must be written as `QUESTION_FOR_COORDINATOR` in the current-agent
status record.

## Governing Records

| Artifact | Role |
| --- | --- |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-parallel-wave1-coordination-record-2026-06-18.md` | Wave-level contracts, two-agent boundary, file communication rules, and shared non-claims. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-current-agent-wave1-sparse-locality-status-2026-06-18.md` | Coordinator-visible lane status. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-subplan-2026-06-18.md` | Earlier reviewed umbrella subplan and evidence contract; superseded operationally by the phase subplans below, but retained as context. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p08-sparse-localized-diagnostic-result-2026-06-17.md` | Historical Phase 8 blocker and LEDH-specific uncertainty motivating this lane. |
| `docs/benchmarks/scalable_ot_p08_sparse_locality_diagnostics.py` | Read-only implementation pattern for locality thresholds, truncation semantics, and CPU import ordering. |
| `experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py` | Read-only TensorFlow LEDH flow route for deterministic LEDH-like post-flow particles. |

## Owned Planning And Execution Artifacts

The current agent may create or edit the following lane-owned artifacts:

- this master program;
- the P12E phase subplans listed below;
- the P12E phase result/close records listed below;
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-master-program-claude-review-ledger-2026-06-19.md`;
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-master-program-review-packet-2026-06-19.md`;
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-visible-gated-overnight-execution-plan-2026-06-19.md`;
- `docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py`;
- `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.json`;
- `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.md`;
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-current-agent-wave1-sparse-locality-status-2026-06-18.md`.

Shared visible ledgers and stop handoffs remain coordinator-owned during active
Wave 1 execution.

## Research Question

Do deterministic LEDH-like post-flow particles exhibit enough local support
concentration that sparse/localized OT work should be reopened after Phase 8
blocked sparse implementation on Phase 1 dense fixtures?

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a deterministic, CPU-scoped TensorFlow LEDH-like locality diagnostic produce valid evidence on whether sparse/localized OT work should be reopened for LEDH post-flow particles? |
| Comparator | Dense TensorFlow transport on the same deterministic LEDH-like post-flow particles, preserving Phase 1/Phase 8 orientation and truncation conventions. |
| Primary pass criterion | P12E writes valid JSON/Markdown/result artifacts recording deterministic fixture provenance, finite dense plans, support curves, nearest-neighbor mass, 99% truncation residuals, transported-particle errors, decisions, and non-claims. |
| Reopen criterion | Every fixture passes the reviewed 99% support median/p90 thresholds, truncation row/column residual thresholds, transported-particle error threshold, and finite LEDH/dense/truncated checks. |
| Block criterion | Any fixture fails the reviewed thresholds or required provenance/finite checks. |
| Veto diagnostics | Missing deterministic provenance, non-finite LEDH/dense/truncated artifacts, orientation mismatch, threshold/reporting mismatch, package/network/GPU/external-solver need, shared-file edit need, or unsupported claim. |
| Explanatory diagnostics | Runtime, memory, 90/95/99.9% support curves, nearest-neighbor mass, LEDH log-det ranges, and descriptive comparison to Phase 8. |
| Not concluded | No sparse solver validity, speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, or broad sparse-OT validation/rejection. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P12E-0 | Intake, Governance, And First Checks | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p0-first-checks-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p0-first-checks-result-2026-06-19.md` |
| P12E-1 | Diagnostic Implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p1-diagnostic-implementation-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p1-diagnostic-implementation-result-2026-06-19.md` |
| P12E-2 | Smoke Diagnostic And Artifact Validation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p2-smoke-diagnostic-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p2-smoke-diagnostic-result-2026-06-19.md` |
| P12E-3 | Official Diagnostic | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p3-official-diagnostic-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p3-official-diagnostic-result-2026-06-19.md` |
| P12E-4 | Result Closeout And Coordinator Handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p4-closeout-handoff-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p4-closeout-handoff-result-2026-06-19.md` |

## Phase Advancement Rule

Each phase may start only after:

- its dedicated subplan exists;
- inherited entry conditions are satisfied;
- required human approvals for that phase are present;
- no cross-lane or shared-contract blocker is open;
- any material subplan review has converged or the master program explicitly
  records that Claude review is not required for that non-material phase.

At the end of every phase, Codex must:

1. run the required local checks declared in that phase subplan;
2. write the phase result/close record;
3. draft or refresh the next phase subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Claude Review Protocol

Claude is read-only reviewer only.  Claude is not an execution authority and
cannot authorize crossing human, runtime, model-file, funding,
product-capability, or scientific-claim boundaries.

For material planning artifacts, Codex uses Claude Opus with max effort after
explicit user approval.  Prompts must not paste whole files.  Instead, Codex
must provide a concise review packet with:

- artifact paths;
- phase index;
- evidence contracts;
- stop conditions;
- claimed boundaries;
- known risks;
- specific questions for review.

Claude may inspect targeted snippets if needed, but the prompt must say not to
read whole files unless a specific finding requires line-level confirmation.

If Claude does not respond:

1. run a tiny read-only Claude probe;
2. if the probe responds, treat the original prompt as the problem and redesign
   a shorter prompt;
3. if the probe fails or auth/network/tooling fails, record an external-review
   blocker and ask the user for direction.

For material findings:

- patch the same subplan visibly;
- rerun focused local checks when applicable;
- rerun focused Claude review on the changed sections only;
- stop after five Claude review rounds for the same blocker and write a blocker
  result.

## Repair Loop

For each phase:

1. classify the blocker as fixable local issue, shared-contract issue,
   human-required boundary, or non-repairable result;
2. patch only lane-owned files for fixable local issues;
3. rerun the smallest relevant check;
4. update the phase result with the repair and rerun evidence;
5. ask Claude for read-only review only when the repair is material to claims,
   boundaries, or artifacts;
6. continue to the next phase if the gate passes;
7. stop only for a valid stop condition.

Valid stop conditions are listed in the phase subplans and include:

- package installation, network fetch, GPU evidence, external sparse solver, or
  credentials required;
- destructive action required;
- shared schema/baseline/ledger/peer-file edit required;
- changing thresholds after seeing results;
- unsupported scientific or production claim required to interpret outputs;
- Claude/Codex nonconvergence after five review rounds for the same material
  blocker.

## Final Lane Decisions

Use exactly one final status family:

- `LEDH_SPARSE_LOCALITY_SCREEN_COMPLETED_REOPENS_SPARSE_IMPLEMENTATION_PLAN_ONLY`
- `LEDH_SPARSE_LOCALITY_SCREEN_COMPLETED_DOES_NOT_REOPEN_SPARSE_IMPLEMENTATION`
- `LEDH_SPARSE_LOCALITY_SCREEN_BLOCKED`
- `BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`

If the screen reopens sparse work, the only authorized next action is writing a
new reviewed sparse/localized implementation plan.  This lane still does not
implement that solver.

## Launch Boundary

This master program does not launch execution.  Before any phase command runs,
the user must approve the visible gated execution plan and the anticipated
command classes listed there.
