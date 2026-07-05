# BayesFilter General NeuTra Dense-IAF Artifact Migration Master Program

Date: 2026-07-04

Status: `MASTER_PROGRAM_VISIBLE_LAUNCH_READY`

## Objective

Build a fail-closed migration bridge from historical dense-IAF NeuTra artifacts
in `/home/chakwong/python` into the generic BayesFilter nonlinear SSM target
interface. The bridge is for frozen transport reuse and mechanics checks only.

The program must not claim real-artifact reuse, posterior correctness, HMC
convergence, sampler superiority, all-filter HMC readiness, or default policy
change until those exact claims have their own reviewed evidence.

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Can historical dense-IAF NeuTra transport states be migrated into a stable BayesFilter frozen-transport schema for arbitrary nonlinear SSM targets and filters? |
| Candidate/mechanism | A BayesFilter-owned dense autoregressive IAF frozen transport schema and TensorFlow/TFP loader bound to `SSMTargetContract` signatures. |
| Baseline/comparator | Prior generic SSM interface closeout and Phase 6 inventory: `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-stop-handoff-2026-07-03.md` and `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-inventory-2026-07-03.json`. |
| Expected failure mode | Historical result notes may lack full payloads, target signatures, or stable schema fields; legacy target identities may not reconstruct a generic `SSMTargetContract`. |
| Promotion criterion | A signed dense-IAF frozen transport payload can be loaded fail-closed against a matching generic target signature and can pass bounded forward/logdet/value-score mechanics checks. |
| Promotion veto | Missing payload, missing or mismatched target signature, process-local identity in a manifest, nonfinite parameters/logdet, shape mismatch, unsupported legacy schema, or unsafe copy/runtime boundary. |
| Continuation veto | `/home/chakwong/python` inaccessible; no local source or payload evidence sufficient to define even a synthetic dense-IAF schema; local focused tests cannot run; Claude and Codex fail to converge after five review rounds for the same blocker; human-required approval is denied or absent. |
| Repair trigger | A fixable schema mismatch, missing required plan field, missing test coverage for loader invariants, or Claude `VERDICT: REVISE` with bounded findings. |
| Explanatory diagnostics | Historical candidate IDs, step sizes, leapfrog counts, R-hat values where present, source paths, SHA-256 hashes, topology sizes, and payload sizes. |
| Must not conclude | No HMC convergence, posterior validity, statistical ranking, production default, or scientific claim follows from this migration program. |

## Role And Boundary Contract

Codex is supervisor and executor. Claude Opus at max effort may be used only as
a read-only reviewer. Claude cannot authorize crossing human, runtime,
model-file, funding, product-capability, or scientific-claim boundaries.

Claude review prompts must start with one exact path and a bounded question. Do
not paste whole files or broad artifact bundles into Claude. If Claude hangs,
first run a tiny probe. If the probe responds, treat the stalled review as a
prompt-surface problem and redesign the prompt.

## Program Artifacts

- Master program: `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-master-program-2026-07-04.md`
- Visible runbook: `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-visible-gated-execution-runbook-2026-07-04.md`
- Execution ledger: `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-visible-execution-ledger-2026-07-04.md`
- Claude review ledger: `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-claude-review-ledger-2026-07-04.md`
- Stop handoff: `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-visible-stop-handoff-2026-07-04.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and boundary freeze | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase0-governance-boundary-freeze-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase0-governance-boundary-freeze-result-2026-07-04.md` |
| 1 | Historical artifact taxonomy | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-result-2026-07-04.md` |
| 2 | Dense-IAF frozen schema | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-result-2026-07-04.md` |
| 3 | TensorFlow/TFP loader implementation | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-result-2026-07-04.md` |
| 4 | Target-signature bridge | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-result-2026-07-04.md` |
| 5 | Payload restoration or export | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase5-payload-export-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase5-payload-export-result-2026-07-04.md` |
| 6 | One real-artifact load canary | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase6-real-artifact-load-canary-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase6-real-artifact-load-canary-result-2026-07-04.md` |
| 7 | Mechanics canary and closeout | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase7-mechanics-closeout-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase7-mechanics-closeout-result-2026-07-04.md` |

## Phase Objectives And Gates

| Phase | Objective | Gate |
| --- | --- | --- |
| 0 | Freeze scope, approvals, nonclaims, repair loop, and launch evidence. | Required plan artifacts exist; Phase 1 subplan is drafted and reviewed. |
| 1 | Classify historical dense-IAF source/result/payload evidence without loading or copying it. | Inventory JSON classifies every checked candidate fail-closed and records hashes/sizes. |
| 2 | Define `bayesfilter.neutra.dense_iaf_frozen_transport.v1` schema and schema invariants. | Schema covers topology, tensor payloads, masks, logdet convention, target signature, hashes, and nonclaims. |
| 3 | Implement a BayesFilter-owned TensorFlow/TFP dense-IAF loader against synthetic fixtures. | Focused tests pass for shape, forward/logdet, inverse diagnostic, hash stability, and rejection cases. |
| 4 | Bridge old target identities to generic `SSMTargetContract` signatures. | At least one candidate is classified as bridgeable or the blocker is written with exact missing fields. |
| 5 | Restore or export a small signed payload if Phase 4 permits it. | Payload/export manifest has SHA-256 evidence and no process-local identity; no large copy without approval. |
| 6 | Load one real artifact through the new loader after it is reusable by schema and signature. | One load canary passes, or a precise fail-closed blocker is recorded. |
| 7 | Run a bounded mechanics canary and close out evidence. | Mechanics result and final ledger distinguish migration success from HMC/posterior nonclaims. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| TensorFlow/TFP implementation backend | `AGENTS.md` BayesFilter policy | BayesFilter-owned differentiable code defaults to TensorFlow/TFP. | Accidentally porting NumPy implementation code into production path. | Phase 3 tests inspect public loader behavior and implementation imports. | Required |
| CPU-only checks only when deliberate | `AGENTS.md` GPU policy | Small smoke tests may hide GPUs with `CUDA_VISIBLE_DEVICES=-1`; default production target remains GPU. | Treating CPU-only smoke as GPU readiness or hiding GPUs for training. | Run artifacts must state CPU-only when used; GPU commands require escalation. | Required |
| Historical artifacts as evidence first | Prior Phase 6 closeout | Old results are valuable but not generic loader payloads yet. | Loading signature-absent payloads or claiming reuse prematurely. | Phase 1 fail-closed classification. | Required |
| Claude as read-only reviewer | User instruction and repo policy | Cross-agent review should catch plan defects without delegating authority. | Claude edits, launches commands, or approves boundary crossing. | Exact-path prompts and review ledger inspection. | Required |

## Skeptical Plan Audit

This plan passes the pre-execution skeptical audit for Phase 0 because:

- the baseline is the prior generic SSM interface closeout and Phase 6 artifact
  inventory, not a weak or convenient comparator;
- historical HMC diagnostics are treated as explanatory unless a source result
  made them a hard screen;
- the first executable phase has stop conditions and no hidden training, GPU,
  remote fetch, or artifact-copy command;
- Phase 1 artifacts answer the artifact-taxonomy question without claiming
  loader success;
- later phases cannot run until their dedicated subplans exist and pass review.

## Anticipated Approval Boundaries

Phase 0 and Phase 1 need only local file reads, local plan edits, local checks,
and escalated Claude read-only review commands.

Ask for explicit human approval before any later phase performs:

- network fetch, `git pull`, or remote reconciliation in `/home/chakwong/python`;
- GPU/CUDA detection, GPU benchmark, GPU training, or GPU HMC;
- serious HMC, long MCMC, or new NeuTra training;
- package installation or environment mutation;
- large artifact copying from `/home/chakwong/python`;
- modifying `/home/chakwong/python` or other directories outside this repo;
- changing default product policy or scientific claim boundaries.

## Repair Loop

For each material phase:

1. Run local checks specified by the phase subplan.
2. Write a phase result or blocker record.
3. Draft or refresh the next phase subplan.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
5. Use Claude read-only review for material subplans.
6. If Claude returns `VERDICT: REVISE`, patch the same artifact visibly and run
   focused checks.
7. Stop after five Claude review rounds for the same blocker.

`MASTER_PROGRAM_VISIBLE_LAUNCH_READY`
