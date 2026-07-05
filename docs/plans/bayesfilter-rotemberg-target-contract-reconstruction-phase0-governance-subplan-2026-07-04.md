# Phase 0 Subplan: Governance And Reconstruction Boundary

Date: 2026-07-04

Status: `PHASE0_READY_FOR_EXECUTION`

## Phase Objective

Launch the Rotemberg target-contract reconstruction program with stable scope,
evidence boundaries, repair loop, anticipated approvals, and a reviewed Phase 1
metadata-source inventory subplan.

## Entry Conditions Inherited From Previous Phase

- Dense-IAF migration stopped at
  `MASTER_PROGRAM_STOPPED_AT_PHASE4_TARGET_SIGNATURE_BRIDGE`.
- Phase 4 found Rotemberg embedded dense-IAF payload candidates, but they were
  blocked by missing generic `SSMTargetContract` metadata.
- User directed Codex to continue with the recommended model-specific
  reconstruction program.
- No phase may claim real-artifact reuse before target contract, payload
  presence, schema binding, and loader checks pass.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-master-program-2026-07-04.md`
- Visible runbook:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-gated-execution-runbook-2026-07-04.md`
- Execution ledger:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-execution-ledger-2026-07-04.md`
- Claude review ledger:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-claude-review-ledger-2026-07-04.md`
- Stop handoff:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-stop-handoff-2026-07-04.md`
- Phase 0 result:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase0-governance-result-2026-07-04.md`
- Phase 1 subplan:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-subplan-2026-07-04.md`

## Required Checks, Tests, And Reviews

Local checks:

```text
test -f docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-master-program-2026-07-04.md
test -f docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-gated-execution-runbook-2026-07-04.md
test -f docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-execution-ledger-2026-07-04.md
test -f docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-claude-review-ledger-2026-07-04.md
test -f docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-stop-handoff-2026-07-04.md
test -f docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase0-governance-subplan-2026-07-04.md
test -f docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-subplan-2026-07-04.md
rg -n "Phase Objective|Entry Conditions|Required Artifacts|Required Checks|Evidence Contract|Forbidden Claims|Exact Next-Phase Handoff|Stop Conditions" docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase0-governance-subplan-2026-07-04.md docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-subplan-2026-07-04.md
git diff --check -- docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-master-program-2026-07-04.md docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-gated-execution-runbook-2026-07-04.md docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase0-governance-subplan-2026-07-04.md docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-subplan-2026-07-04.md
```

Claude reviews:

- Master program exact-path review for boundary safety and phase feasibility.
- Phase 1 subplan exact-path review for consistency, correctness, feasibility,
  artifact coverage, and boundary safety.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the Rotemberg reconstruction program safely launch with complete governance, artifacts, and next-phase handoff? |
| Baseline/comparator | Dense-IAF Phase 4 stop handoff, local Rotemberg evidence, and the visible-gated execution template. |
| Primary pass criterion | Required artifacts exist; local consistency checks pass; Claude review converges or fixable issues are patched; Phase 1 has a reviewed handoff. |
| Veto diagnostics | Missing required field, missing stop condition, hidden runtime approval, overclaim, unreviewed next-phase handoff, or Claude `VERDICT: REVISE` unresolved after five rounds. |
| Explanatory diagnostics | Existing worktree state, Rotemberg result/source paths, and review findings. |
| Not concluded | No canonical target signature, real-artifact loader reuse, migrated payload, HMC convergence, posterior correctness, sampler superiority, GPU readiness, or default-policy change. |
| Result artifact | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase0-governance-result-2026-07-04.md` |

## Forbidden Claims And Actions

- Do not train NeuTra.
- Do not run serious HMC or MCMC.
- Do not run GPU/CUDA probes or GPU jobs in Phase 0.
- Do not fetch from network or reconcile remote branches in Phase 0.
- Do not copy historical payloads into BayesFilter.
- Do not modify `/home/chakwong/python`.
- Do not claim historical R-hat, ESS, acceptance, or candidate selection as a
  BayesFilter validity claim.
- Do not claim canonical target signature readiness before Phase 2/3 gates.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- all Phase 0 required artifacts exist;
- local consistency checks pass;
- the master program and Phase 1 subplan have Claude `VERDICT: AGREE`, or all
  fixable `VERDICT: REVISE` findings have been patched and rereviewed;
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
  training, package installation, or modifying `/home/chakwong/python` before a
  reviewed subplan and explicit human approval.

## Skeptical Plan Audit

Phase 0 is safe to execute because it creates and checks governance artifacts
only. It does not use proxy metrics as pass criteria, does not compare samplers,
does not run training/HMC, does not hide GPU devices for training, and does not
load historical artifacts. The artifact outputs answer the Phase 0 question
directly.

`PHASE0_READY_FOR_EXECUTION`
