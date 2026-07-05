# Phase 0 Subplan: Governance And Boundary Freeze

Date: 2026-07-04

Status: `PHASE0_READY_FOR_EXECUTION`

## Phase Objective

Launch the dense-IAF migration bridge with stable artifacts, scope boundaries,
evidence gates, repair loop, anticipated approvals, and the Phase 1 historical
artifact taxonomy subplan.

## Entry Conditions Inherited From Previous Phase

- Prior generic SSM interface program closed with
  `MASTER_PROGRAM_CLOSED_WITH_REAL_ARTIFACT_MIGRATION_BLOCKED`.
- Prior Phase 6 inventory classified zero historical artifacts as reusable by
  the current affine-diagonal generic loader.
- User requested a gated master program, Claude read-only review to convergence
  or max five rounds, phase subplans, local checks, phase result records,
  next-phase handoffs, and launch after the execution plan is written.
- No phase in this new program may claim real-artifact reuse before schema,
  target-signature, and payload checks pass.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-master-program-2026-07-04.md`
- Visible runbook:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-visible-gated-execution-runbook-2026-07-04.md`
- Execution ledger:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-visible-execution-ledger-2026-07-04.md`
- Claude review ledger:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-claude-review-ledger-2026-07-04.md`
- Stop handoff:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-visible-stop-handoff-2026-07-04.md`
- Phase 0 result:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase0-governance-boundary-freeze-result-2026-07-04.md`
- Phase 1 subplan:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-subplan-2026-07-04.md`

## Required Checks, Tests, And Reviews

Local checks:

```text
test -f <master program>
test -f <visible runbook>
test -f <execution ledger>
test -f <Claude review ledger>
test -f <stop handoff>
test -f <Phase 0 subplan>
test -f <Phase 1 subplan>
rg -n "Phase Objective|Entry Conditions|Required Artifacts|Required Checks|Evidence Contract|Forbidden Claims|Exact Next-Phase Handoff|Stop Conditions" <Phase 0 and Phase 1 subplans>
git diff --check -- <Phase 0 created docs>
```

Claude reviews:

- Master program exact-path review for boundary safety and phase feasibility.
- Phase 1 subplan exact-path review for consistency, correctness, feasibility,
  artifact coverage, and boundary safety.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the dense-IAF migration program safely launch with complete governance, artifacts, and next-phase handoff? |
| Baseline/comparator | User protocode, local visible-gated runbook template, prior generic SSM interface closeout, and Phase 6 inventory. |
| Primary pass criterion | Required artifacts exist; local consistency checks pass; Claude reviews converge or fixable issues are patched; Phase 1 has a reviewed handoff. |
| Veto diagnostics | Missing required field, missing stop condition, hidden runtime approval, overclaim, unreviewed next-phase handoff, or Claude `VERDICT: REVISE` unresolved after five rounds. |
| Explanatory diagnostics | Existing worktree state, legacy dense-IAF source paths, prior inventory counts, and review findings. |
| Not concluded | No real-artifact loader reuse, no migrated dense-IAF payload, no HMC convergence, no posterior correctness, no sampler superiority, and no production default change. |
| Result artifact | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase0-governance-boundary-freeze-result-2026-07-04.md` |

## Forbidden Claims And Actions

- Do not train NeuTra.
- Do not run serious HMC or MCMC.
- Do not run GPU/CUDA probes or GPU jobs in Phase 0.
- Do not fetch from network or reconcile remote branches in Phase 0.
- Do not copy large historical artifacts into BayesFilter.
- Do not modify `/home/chakwong/python`.
- Do not treat historical R-hat, ESS, acceptance, or candidate selection as a
  new BayesFilter validity claim.
- Do not claim real-artifact reuse, posterior correctness, sampler superiority,
  all-filter readiness, or default policy change.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- all Phase 0 required artifacts exist;
- local consistency checks pass;
- the master program and Phase 1 subplan have Claude `VERDICT: AGREE`, or
  all fixable `VERDICT: REVISE` findings have been patched and rereviewed;
- the Phase 0 result records review rounds and nonclaims;
- no human-required approval boundary is crossed.

## Stop Conditions

Stop and write a blocker result if:

- required plan artifacts cannot be created;
- local checks fail for a non-fixable reason;
- Claude is unreachable after probe handling;
- Claude and Codex do not converge after five review rounds for the same
  blocker;
- executing Phase 1 would require network, GPU, large copy, serious HMC,
  training, package installation, or modifying `/home/chakwong/python` before
  a reviewed subplan and explicit human approval.

## Skeptical Plan Audit

Phase 0 is safe to execute because it only creates and checks governance
artifacts. It does not use proxy metrics as pass criteria, does not compare
samplers, does not run training/HMC, does not hide GPU devices for training,
and does not load historical artifacts. The artifact outputs answer the Phase 0
question directly.

`PHASE0_READY_FOR_EXECUTION`
