# Phase 7 subplan: batched CPU/GPU/XLA benchmarking

Date: 2026-06-30

Status: `DRAFT_REVISED_REVIEW_READY`

## Phase Objective

Add batched evaluator status and trusted CPU/GPU/XLA timing/status fields to the leaderboard without allowing timing to override correctness gates.

This phase is a status-and-evidence integration phase. It must not force GPU
benchmarking for cells whose value/score row is still blocked. Blocked cells
receive explicit batch/GPU/XLA non-applicability or blocker status. Existing
P91 SIR d18 CPU/GPU/XLA benchmark evidence may be referenced only as scoped
local complete-data sidecar evidence, not as full observed-data/filtering row
admission.

## Entry Conditions Inherited From Previous Phase

- Phase 6 closed or precisely blocked generalized-SV rows.
- Value/score validity ledger is current.
- GPU/CUDA commands will run only with escalated/trusted permissions.
- CPU-only benchmark commands must hide GPU devices before framework import and record that CPU-only choice.

## Required Artifacts

- Batched API status fields or explicit blocker notes per row/cell.
- CPU/GPU/XLA benchmark evidence fields per row/cell where trusted evidence
  already exists or is newly run under this phase.
- Explicit `not_applicable_until_value_score_row_exists` status for blocked
  main leaderboard cells.
- Scoped P91 sidecar timing/status fields for the local complete-data SIR d18
  component only.
- P91 sidecar timing/status fields must live under a separate sidecar namespace
  or section and must not be rendered or sorted as admitted main-row evidence.
- Regenerated leaderboard with batch and CPU/GPU/XLA status columns:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
  and
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`.
- If any new benchmark manifest is generated in this phase, the Phase 7 result
  must enumerate the exact manifest path. If no new benchmark is run, the Phase
  7 result must enumerate the reused trusted evidence paths and state that no
  new timing claim was generated.
- Phase result:
  `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-result-2026-06-30.md`
- Refreshed Phase 8 subplan.

## Required Checks, Tests, Reviews

- CPU reference timing with intentional CPU-only environment recorded when a
  new CPU timing is run in this phase.
- Escalated/trusted GPU device probe before any new GPU run or new GPU claim.
- GPU/XLA compile and execution smoke per row/cell only where claimed for the
  main leaderboard row, or for explicitly scoped sidecar evidence.
- CPU/GPU value parity within stated numerical tolerance where both CPU and GPU
  timings are claimed for the same target.
- Batch shape/parity tests where a batched route is claimed.
- Schema/status tests proving blocked value/score cells cannot be ranked by
  batch/GPU/XLA timings.
- Schema/status tests proving P91 sidecar timing/status fields cannot be
  interpreted as full observed-data/filtering SIR leaderboard admission and are
  not part of main leaderboard sorting/ranking.
- Claude review of benchmark result and nonclaims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which current leaderboard cells have reviewed batched and GPU/XLA evidence, and which cells remain blocked/not-applicable because the value/score row is not admitted? |
| Baseline/comparator | Correctness-passing value/score rows from Phases 1-6 plus scoped P91 local complete-data sidecar evidence. |
| Primary criterion | Batch/GPU/XLA status is reported per cell only after correctness status is known; blocked main rows are marked not-applicable/blocker rather than benchmarked as rankable rows; P91 timing is structurally isolated as scoped sidecar evidence. |
| Veto diagnostics | GPU claim from non-escalated context; CPU/GPU parity failure for a claimed target; timing compared for invalid value/score cell; batch path changes scalar; P91 local complete-data evidence promoted to full SIR observed-data/filtering row. |
| Explanatory diagnostics | First-call time, steady time, compile time, memory, device details. |
| Not concluded | No universal GPU superiority; no HMC convergence; no production deployment claim beyond reported gates; no full SIR observed-data/filtering readiness from P91 sidecar timing. |
| Artifact | Benchmark manifests, regenerated leaderboard, Phase 7 result. |

## Forbidden Claims And Actions

- Do not claim GPU is faster globally; benchmark per model.
- Do not debug GPU setup from non-escalated failure alone.
- Do not rank invalid cells by speed.
- Do not run GPU benchmarks for blocked cells solely to fill timing columns.
- Do not treat P91 local complete-data SIR d18 CPU/GPU/XLA evidence as full
  observed-data/filtering leaderboard evidence.
- Do not put P91 sidecar timing in a main-row field that can be sorted/ranked
  as if it were full SIR observed-data/filtering timing.
- Do not add new default policy claims from timing fields.

## Exact Next-Phase Handoff Conditions

Advance to Phase 8 if:

- Batch/GPU/XLA status is recorded per row/cell with trusted evidence, scoped
  sidecar evidence, explicit blocker, or explicit not-applicable status.
- P91 sidecar evidence is structurally isolated from main leaderboard
  admission/ranking fields.
- Correctness vetoes remain primary over speed.

## Stop Conditions

Stop if:

- Trusted GPU context is unavailable for a required new GPU claim.
- CPU/GPU parity fails and cannot be diagnosed in a focused repair.
- Benchmark would require package installation or environment changes not authorized by this program.

## Skeptical Audit Before Execution

Audit status: `PASSED_AFTER_SCOPE_TIGHTENING_FOR_CLAUDE_REVIEW`.

- Wrong-baseline risk: controlled by treating correctness-passing rows and
  P91 local complete-data sidecar evidence as different scopes.
- Proxy-metric risk: controlled by making timing explanatory only; batch/GPU/XLA
  fields cannot admit or rank a blocked value/score cell.
- Hidden-assumption risk: controlled by explicit not-applicable statuses for
  rows with no reviewed batched evaluator or no admitted value/score row.
- Environment risk: controlled by requiring escalated/trusted GPU context for
  any new GPU/XLA claim and CPU-hidden environment for CPU-only TensorFlow
  checks.
- Artifact risk: controlled by adding schema/status tests and a Phase 7 result
  that names every row/cell status category.
- Sidecar-leakage risk: controlled by requiring a separate P91 sidecar
  namespace/section and a focused anti-promotion test.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 7 result/close record.
3. Draft or refresh Phase 8 subplan.
4. Review Phase 8 subplan for final artifact coverage and nonclaims.
