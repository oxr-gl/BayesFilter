# P12-1 Subplan: Intake And Artifact Baseline

Date: 2026-06-19

## Status

`DRAFT_PENDING_PHASE_P12_0_GATE`

## Phase Objective

Inventory the P12 lane artifacts, verify that the peer-agent status record and
existing result/diagnostic artifacts are internally consistent, and establish
the baseline state before replaying implementation checks.

## Entry Conditions Inherited From Previous Phase

- P12-0 governance passed or was explicitly accepted by the user.
- Write boundaries and non-claims are locked.
- Claude review approval state is recorded.

## Required Artifacts

- Existing P12 implementation/test/diagnostic files.
- Existing P12 JSON/Markdown diagnostics.
- Existing P12 result note.
- Existing peer-agent status record.
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p01-intake-artifact-baseline-result-2026-06-19.md`

## Required Checks, Tests, And Reviews

- `git status --short` scoped to P12-owned files.
- `test -f` or equivalent existence checks for every P12 artifact.
- Text scan for required statuses:
  `LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY`, `DIAGNOSTIC_RUN_COMPLETE`,
  `source_faithful`, `fixed_hmc_adaptation`, `extension_or_invention`.
- JSON validity check for the P12 diagnostic JSON.
- Claude read-only review for material inconsistency findings after approval.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the P12 lane artifacts present, scoped, and internally consistent before replay? |
| Baseline/comparator | P12-0 governance and existing June 18 P12 result/status artifacts. |
| Primary pass criterion | All required P12 artifacts exist; status/result/JSON agree on diagnostic-only pass; source-route classification and non-claims are present. |
| Veto diagnostics | Missing artifact, stale status, invalid JSON, unsupported claim, or evidence copied from Phase 6 context as P12 validation. |
| Explanatory diagnostics | File status, artifact timestamps, scoped dirty-worktree snapshot. |
| Not concluded | No new algorithmic validity beyond artifact consistency. |

## Forbidden Claims And Actions

- Do not modify implementation or diagnostics in this intake phase unless a
  P12-owned artifact has a localized metadata inconsistency and the repair is
  separately recorded.
- Do not edit shared or other-lane files.
- Do not treat Phase 6 context checks as P12 solver evidence.

## Exact Next-Phase Handoff Conditions

Advance to P12-2 only if:

- all required P12 artifacts are present;
- JSON parses successfully;
- status/result/diagnostic artifacts agree on the diagnostic-only status;
- no forbidden claim scan produces a positive claim requiring repair.

## Stop Conditions

Stop if:

- a required P12 artifact is absent and cannot be recreated within the owned
  write set;
- consistency repair would change shared contracts or another lane's files;
- artifact status contradicts the result and cannot be locally reconciled.

## End-Of-Phase Protocol

At phase end:

1. run required local checks;
2. write the P12-1 result/close record;
3. draft or refresh the P12-2 subplan;
4. review the P12-2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
