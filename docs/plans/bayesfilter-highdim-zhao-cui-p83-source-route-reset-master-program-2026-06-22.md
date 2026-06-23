# P83 Zhao-Cui Source-Route Reset Master Program

Date: 2026-06-22

Status: `DRAFT_READY_FOR_PHASE0_REVIEW`

## Objective

Reset the Zhao-Cui validation lane to the documented fixed-TTSIRT
retained-object source route.  This program prevents the local all-grid,
operator, UKF, finite-difference, validation-CE, and ForwardAccumulator/JVP
diagnostic lanes from being used as source-faithful Zhao-Cui evidence.

The immediate objective is route identity and anchored inventory, not numerical
validation.  No d=18 SIR value/gradient or LEDH comparison may launch until the
source-route retained-object pipeline has passed the phase gates below.

## Governing Inputs

- `docs/plans/bayesfilter-highdim-zhao-cui-source-route-reset-memo-2026-06-22.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-result-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m6-sequential-fixed-hmc-source-loop-result-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-result-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p58-m9-source-route-pipeline-repair-result-2026-06-11.md`
- Zhao-Cui author source under
  `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

## Role Contract

Codex in this conversation is the supervisor and executor.

Claude Opus max effort may be used only as a read-only reviewer of compact
path-anchored fact packets.  Claude is not an execution authority and cannot
authorize crossing human, runtime, model-file, funding, product-capability,
default-policy, or scientific-claim boundaries.

## Source-Route Classification Rules

| Classification | Meaning |
|---|---|
| `source_faithful` | Matches a cited Zhao-Cui paper operation and a cited author-source operation. |
| `fixed_hmc_adaptation` | Preserves the author route while freezing randomness, ranks, bases, schedules, samples, or branches for replayability and differentiability. |
| `extension_or_invention` | Not present in the cited paper/source route.  Useful extensions may be studied, but they cannot close a source-faithfulness gap without explicit human approval. |

Binding veto: any `source_faithful`, source-route, paper-scale Zhao-Cui, or
equivalent claim without paper/math anchors and author-source file/line anchors
is blocked as `BLOCK_SOURCE_UNGROUNDED`.

## Whole-Program Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the Zhao-Cui lane be reset so every later implementation and validation step follows the documented fixed-TTSIRT retained-object source route rather than the local all-grid/operator route? |
| Baseline/comparator | P50/P56/P57/P58 source-route contracts and Zhao-Cui paper/source anchors; local all-grid/operator/JVP/UKF lanes are boundary examples, not promotion baselines. |
| Primary pass criterion | Every phase has a dedicated subplan, evidence contract, local checks, result/close record, next-phase handoff, and read-only review when material; route classifications remain anchored and conservative. |
| Veto diagnostics | Unanchored source-faithful labels; reuse of `multistate_tt_grid_retained_filter` or local/operator propagation as Zhao-Cui validation; UKF or validation CE promoted as truth; FD/JVP promoted as analytical derivative; d=18/LEDH launched before source-route mechanics gates. |
| Explanatory diagnostics | Search inventories, code anchors, source anchors, focused tests, compile checks, markdown scans, Claude findings, and dirty-worktree observations. |
| Not concluded | No d=18 correctness, no posterior correctness, no HMC readiness, no exact likelihood correctness, no LEDH agreement, no production readiness, no source-faithfulness beyond anchored implemented rows. |
| Artifacts | This master program, visible gated runbook, execution ledger, review ledger, phase subplans, phase results, blocker notes, and stop handoff. |

## Skeptical Plan Audit

Pre-execution audit result:

- Wrong baseline risk is material.  P56 already classifies the multistate
  all-grid/operator route as `extension_or_invention`, and P82 found the active
  multistate derivative surface is ForwardAccumulator/JVP-backed.
- Proxy promotion risk is material.  UKF, validation CE, FD agreement, and tiny
  mechanics smokes can scout, explain, or veto only under phase contracts.
- Missing-anchor risk is material.  Every source-route claim must cite both
  paper/project math anchors and author-source anchors.
- Environment mismatch is deferred but recorded.  Later GPU/LEDH work must use
  trusted/escalated execution.  Phase 0/1 are read-only documentation and
  inventory phases.
- Artifact mismatch risk is controlled.  Phase 0/1 artifacts answer route
  governance and inventory only; they cannot answer numerical validation.

The plan may begin with Phase 0 because it creates governance artifacts and
does not run numerical experiments or alter code.

## Phase Ladder

| Phase | Name | Purpose | Subplan | Required result |
|---|---|---|---|---|
| P83-0 | Governance reset | Open the source-route reset program, lock route boundaries, create visible execution artifacts, and close the old local/grid lane as diagnostic-only. | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase0-governance-reset-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase0-governance-reset-result-2026-06-22.md` |
| P83-1 | Anchored source-route inventory | Produce implemented/partial/missing/diagnostic-only table with code, paper/project, and author-source anchors. | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-result-2026-06-22.md` |
| P83-2 | Transport and Proposition-2 repair design | Design the narrow fixed-TTSIRT transport and mass-matrix/QR marginalization repair. | To be drafted or refreshed at P83-1 close. | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-result-2026-06-22.md` |
| P83-3 | Minimal transport slice | Implement the smallest fixed-TTSIRT source-route transport slice needed for a two-step retained-object mechanics test. | To be drafted after P83-2 passes. | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase3-minimal-transport-slice-result-2026-06-22.md` |
| P83-4 | Analytical fixed-branch derivative audit | Identify or repair a source-backed same-branch analytical derivative route; stop if only JVP/ForwardAccumulator exists. | To be drafted after P83-3 passes. | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase4-analytical-derivative-audit-result-2026-06-22.md` |
| P83-5 | Tiny source-route mechanics smoke | Run a tiny CPU or trusted-GPU mechanics smoke proving retained-object carry across at least two steps. | To be drafted after P83-4 passes or records an allowed blocker scope. | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase5-mechanics-smoke-result-2026-06-22.md` |
| P83-6 | Fitting budget design | Design source-route fixed TTSIRT fitting budget, rank/sample ladder, training loss, heldout target clouds, and stop conditions. | To be drafted after P83-5 passes. | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md` |
| P83-7 | SIR d=18 source-route validation | Validate actual source-route fixed branch against declared comparator criteria, then optionally compare to LEDH-PFPF-OT. | To be drafted after P83-6 passes. | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-result-2026-06-22.md` |
| P83-8 | Scale/stress and closeout | Attempt d=50/d=100 only after d=18 passes; close ledgers and handoff. | To be drafted after P83-7 passes. | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase8-scale-stress-closeout-result-2026-06-22.md` |

## Per-Phase Execution Protocol

Each phase must have a dedicated subplan before execution.  The subplan must
state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each phase:

1. run the required local checks;
2. write a phase result or close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude read-only review for material subplans and material boundary
   decisions;
6. patch fixable problems visibly and rerun focused checks;
7. stop after five Claude review rounds for the same blocker.

## Phase-Specific Boundaries

### P83-0: Governance Reset

Allowed:

- write plan/runbook/ledger/closeout artifacts;
- run read-only `rg`, `sed`, `git status`, and markdown scans;
- ask Claude to review compact fact packets.

Forbidden:

- code edits outside plan artifacts;
- numerical runs;
- d=18/LEDH launch;
- claiming any implementation has become source-faithful.

### P83-1: Anchored Source-Route Inventory

Allowed:

- read code, tests, P50/P56/P57/P58 artifacts, and author source;
- produce an inventory table with line anchors and classification;
- run local scans and markdown consistency checks.

Forbidden:

- implementation edits;
- route promotion without anchors;
- treating old local/operator evidence as source-route evidence.

### P83-2: Transport And Proposition-2 Repair Design

Allowed:

- design fixed TT/SIRT core representation, defensive density, normalizer,
  mass-matrix/QR marginalization, KR APIs, proposal correction, retained-object
  metadata, and branch identity.

Forbidden:

- implementing before design review passes;
- accepting tensor-product grid conditional integration or base-density-only
  proposal correction as the production source route.

### P83-3: Minimal Source-Route Transport Slice

Allowed:

- narrowly scoped TensorFlow/TFP implementation and focused tests.

Forbidden:

- broad refactors;
- NumPy as BayesFilter-owned algorithmic backend except independent reference
  checks or serialization;
- d=18 validation.

### P83-4: Analytical Derivative Audit

Allowed:

- audit or wire same-branch fixed scalar derivative path if source-backed.

Forbidden:

- promoting ForwardAccumulator/JVP/FD as the analytical Zhao-Cui comparator;
- inventing a new derivative route and calling it source-faithful.

### P83-5: Tiny Mechanics Smoke

Allowed:

- tiny smoke that checks retained object carry, previous marginal use, finite
  normalizers, proposal correction through `eval_pdf`, and metadata.

Forbidden:

- interpreting smoke as correctness, scaling, HMC readiness, or d=18 success.

### P83-6: Fitting Budget Design

Allowed:

- parameter-count-aware training budget design.

Forbidden:

- budget below `20 * number_of_parameters` for source-route claims;
- heldout/audit clouds defined by the model instead of target measure;
- default changes.

### P83-7: SIR d=18 Source-Route Validation

Allowed only after earlier gates pass:

- trusted GPU execution where appropriate;
- LEDH-PFPF-OT comparator on the same SIR convention;
- current preference `10` seeds and `N=2000` for LEDH if the subplan justifies
  it under uncertainty accounting.

Forbidden:

- launching without source-route value/gradient readiness;
- treating agreement as exact likelihood, posterior correctness, HMC readiness,
  or broad source-faithfulness.

### P83-8: Scale/Stress And Closeout

Allowed:

- d=50/d=100 stress only after d=18 passes.

Forbidden:

- scaling claims without a proper comparator or declared stress-only scope.

## Repair Loop

For any fixable issue found by local checks, Codex review, or Claude review:

1. write the issue in the execution ledger;
2. patch the same subplan/result visibly when the problem is in an artifact;
3. rerun focused local checks;
4. rerun Claude review for material issues;
5. stop after five rounds for the same blocker and write a blocker result.

If Claude does not respond, run a small read-only probe.  If the probe returns,
redesign the prompt rather than treating silence as a review result.

## Human-Required Stops

Stop and ask for human direction before:

- changing default project policy;
- launching GPU/LEDH/d=18 validation without the reviewed phase gates;
- using package installation, network fetches, credentials, or remote services
  not already covered by the runbook;
- destructive git or filesystem operations;
- modifying unrelated dirty worktree changes;
- continuing after five failed review rounds for the same blocker.
