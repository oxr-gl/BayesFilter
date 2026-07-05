# BayesFilter Rotemberg Target-Contract Reconstruction Master Program

Date: 2026-07-04

Status: `MASTER_PROGRAM_DRAFT_FOR_REVIEW`

## Objective

Recover, audit, and if supported mint a canonical generic
`SSMTargetContract` manifest for one historical Rotemberg dense-IAF target
cell, using reviewed local evidence only. The program is for metadata recovery
and frozen-transport reuse decisions, not for retraining, HMC validation, or
payload export by default.

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Can one historical Rotemberg dense-IAF evidence cell be reconstructed into a BayesFilter `SSMTargetContract` manifest with reviewed static shape, data signature, chart, prior, and filter-program metadata? |
| Candidate/mechanism | Field-by-field reconstruction from legacy preflight/result/source anchors, then fail-closed schema admission and one artifact canary if the metadata is sufficient. |
| Baseline/comparator | Dense-IAF migration Phase 4 stop handoff plus the Rotemberg source/result artifacts already present under `/home/chakwong/python`. |
| Expected failure mode | The target cell may lack enough locally verified metadata to support a canonical target signature, or the serious payload may be absent from the reconciled checkout. |
| Promotion criterion | Every required field is either supported by exact evidence or classified with a precise blocker, and any minted manifest passes local validation without inventing fields. |
| Promotion veto | Any required field is unsupported, any field depends only on a legacy target name, any process-local identity appears, payload presence is assumed rather than verified, or local validation fails. |
| Continuation veto | `/home/chakwong/python` becomes inaccessible; exact evidence sources are missing; local checks cannot run; Claude and Codex fail to converge after five review rounds for the same blocker; human-required approval is denied or absent. |
| Repair trigger | A fixable subplan gap, missing source anchor, malformed manifest, unsupported soft claim, or Claude `VERDICT: REVISE` with bounded findings. |
| Explanatory diagnostics | Source paths, hashes, candidate index/step/leapfrog/R-hat values, and artifact existence. |
| Must not conclude | No real-artifact reuse, HMC convergence, posterior validity, sampler superiority, GPU readiness, or default-policy change follows from metadata recovery alone. |

## Role And Boundary Contract

Codex is supervisor and executor. Claude Opus at max effort may be used only
as a read-only reviewer. Claude cannot authorize crossing human, runtime,
model-file, funding, product-capability, or scientific-claim boundaries.

Claude review prompts must start with one exact path and one bounded question.
Do not paste whole files or broad artifact bundles into Claude. If Claude
hangs, use a tiny probe first. If the probe responds, treat the prompt surface
as the problem and narrow it.

Human approval remains required before network fetch, `git pull`, modifying
`/home/chakwong/python`, copying large historical artifacts, GPU/CUDA probes,
GPU training, serious HMC/MCMC, package installation, detached execution, or
scientific/product default claims.

## Program Artifacts

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

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and reconstruction boundary | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase0-governance-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase0-governance-result-2026-07-04.md` |
| 1 | Metadata-source inventory | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-result-2026-07-04.md` |
| 2 | Canonical contract manifest draft | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-result-2026-07-04.md` |
| 3 | Local `SSMTargetContract` validation | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase3-contract-validation-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase3-contract-validation-result-2026-07-04.md` |
| 4 | Bridge rerun and payload boundary decision | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-result-2026-07-04.md` |
| 5 | Closeout or handoff to a separate payload program | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase5-closeout-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase5-closeout-result-2026-07-04.md` |

## Phase Objectives And Gates

| Phase | Objective | Gate |
| --- | --- | --- |
| 0 | Freeze scope, approvals, nonclaims, repair loop, and Phase 1 handoff. | Required plan artifacts exist; Phase 1 subplan is drafted and reviewed. |
| 1 | Inventory exact Rotemberg metadata sources and classify each required field. | JSON inventory and result record field support, blockers, and payload presence separately. |
| 2 | Draft a canonical manifest from supported fields only. | Manifest is complete, stable, hash-bearing, process-local-free, and evidence-grounded. |
| 3 | Instantiate BayesFilter `SSMTargetContract` from the manifest and verify stable signatures. | Focused CPU-only metadata tests pass; signature stability is recorded. |
| 4 | Rerun a model-specific bridge against Rotemberg dense-IAF candidates using the validated contract manifest. | Bridge classifies candidates as signature-ready or writes exact fail-closed blockers. |
| 5 | Close out, or hand off to a separate payload export/load program if and only if Phase 4 permits. | Result separates metadata success from payload/HMC nonclaims. |

## Required Subplan Shape

Every phase subplan must state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each phase, Codex must run required local checks, write a phase
result or blocker record, draft or refresh the next subplan, and review the
next subplan for consistency, correctness, feasibility, artifact coverage, and
boundary safety. Claude review is required for material subplans and boundary
decisions.

## Skeptical Plan Audit

Initial audit status: `PASSED_WITH_BOUNDARIES`.

- Wrong baseline: avoided by using the Phase 4 bridge blocker and local
  Rotemberg evidence, not historical HMC success.
- Proxy metrics: R-hat, ESS, acceptance, training loss, and file existence are
  explanatory only.
- Missing stop conditions: every phase has stop conditions and a hard invention
  veto.
- Unfair comparisons: no sampler comparison or ranking is part of this
  program.
- Hidden assumptions: state-dimension semantics and payload presence are named
  decision items, not silently assumed.
- Stale context: Phase 1 checks the current local source tree and artifact
  paths rather than trusting old summaries.
- Environment mismatch: GPU/HMC/training/network actions are excluded until a
  later approved gate.
- Artifact mismatch: Phase 1 answers metadata support only; later payload
  export requires a separate gate.

`MASTER_PROGRAM_DRAFT_FOR_REVIEW`
