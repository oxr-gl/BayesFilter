# W2-LR-0 Subplan: Governance And Intake

Date: 2026-06-19
Owner: peer agent

## Status

`DRAFT_READY_FOR_EXECUTION`

## Phase Objective

Confirm that the Wave 2 peer-agent low-rank coupling validation lane has a
bounded assignment, owned write set, evidence contract, source-route boundary,
and stop conditions before validation implementation/replay.

## Entry Conditions Inherited From Previous Phase

- User/coordinator assigned this agent as `peer agent`.
- Peer-agent lane is low-rank coupling solver-route validation.
- Current-agent lane is positive-feature Sinkhorn route and is not an evidence
  input for this lane.
- P12 diagnostic-only low-rank solver-route result exists as entry context.

## Required Artifacts

- Wave 2 low-rank coupling master program.
- Wave 2 low-rank coupling status file.
- This subplan.
- P00 result/close record.

## Required Checks, Tests, And Reviews

- Verify the Wave 2 structure file assigns peer agent to low-rank coupling.
- Verify the master/status files preserve owned write boundaries and non-claims.
- Verify no positive-feature lane artifacts are included as evidence.
- Run a local skeptical plan audit before implementation/replay.

Claude review is optional and read-only; it is not required for this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the peer-agent Wave 2 low-rank coupling lane sufficiently bounded to proceed to validation replay without shared-contract or assignment ambiguity? |
| Baseline/comparator | Wave 2 structure plus direct user/coordinator assignment. |
| Primary pass criterion | Master/status/subplan files exist, assign peer agent to low-rank coupling, forbid positive-feature evidence use, define owned writes, preserve non-claims, and record a skeptical audit. |
| Veto diagnostics | Missing assignment, overlapping current-agent ownership, positive-feature evidence dependency, shared contract edit requirement, missing stop condition, missing CPU-only rule, or unsupported claim. |
| Explanatory diagnostics | Draft/not-launched text in the Wave 2 structure is recorded as superseded for this lane by the direct user/coordinator assignment. |
| Not concluded | No validation result, solver correctness, speedup, ranking, readiness, dense equivalence, or coordinator merge. |

## Forbidden Claims And Actions

- Do not edit coordinator-owned Wave 2 records.
- Do not read current-agent positive-feature intermediate artifacts as evidence.
- Do not modify Phase 1 baseline, Phase 3 schema, public exports/defaults, or
  unrelated dirty files.
- Do not claim algorithm superiority, dense equivalence, posterior correctness,
  HMC readiness, public API readiness, or production/default readiness.

## Exact Next-Phase Handoff Conditions

Advance to W2-LR-1 only if P00 checks pass and no shared-contract,
write-ownership, approval, resource, or stop-condition blocker exists.

## Stop Conditions

Stop if assignment is ambiguous, if positive-feature artifacts are needed as
evidence, if a shared contract must change, or if validation would require
package installs, network, GPU evidence, external solver execution, public
export/default edits, or coordinator-owned file edits.
