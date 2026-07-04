# Phase 7 Subplan: Validation Ladder And Closeout

Date: 2026-07-03

Status: `REFRESHED_AFTER_PHASE6_REAL_ARTIFACT_REUSE_BLOCKED`

## Phase Objective

Run a bounded validation ladder that separates engineering correctness,
artifact-migration status, numerical validity, sampler diagnostics, and
scientific interpretation for the generic NeuTra SSM interface, then close the
master program or write a blocker.

## Entry Conditions Inherited From Previous Phase

- Phase 6 result states
  `PHASE6_GATE_PASSED_WITH_REAL_ARTIFACT_REUSE_BLOCKED`.
- Phase 6 artifact inventory exists and classifies all checked real artifacts.
- Phase 7 is explicitly narrowed to synthetic/interface validation plus
  migration-blocker closeout; no real external artifact is reusable in Phase 7.
- Phase 7 subplan has been refreshed and reviewed.

## Required Artifacts

- Validation ledger JSON:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase7-validation-ledger-2026-07-03.json`
- Closeout result:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase7-validation-closeout-result-2026-07-03.md`
- Final stop handoff:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-stop-handoff-2026-07-03.md`

## Required Checks, Tests, And Reviews

Local checks:

- Re-run all focused tests introduced by Phases 1-5.
- Validate synthetic frozen-transport and fixed-transport HMC mechanics
  surfaces only.
- Confirm Phase 6 inventory classifications are preserved in the validation
  ledger.
- Run validation ladder only at levels authorized by this Phase 7 evidence
  contract.
- Any GPU or serious HMC validation requires trusted-context approval and a
  separate evidence plan if expected to guide scientific direction.

Review:

- Claude read-only review of final closeout result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What level of evidence does the generic NeuTra SSM interface have after the planned implementation and fail-closed real-artifact inventory? |
| Baseline/comparator | Phase-by-phase gates and focused tests, not method-performance comparisons. |
| Primary pass criterion | Focused tests pass; validation ledger classifies every rung; closeout states exactly which surfaces are implemented, checked, blocked, or not checked; Phase 6 real-artifact reuse blocker remains explicit. |
| Veto diagnostics | Missing result artifact, failed focused tests, unclassified stochastic diagnostic, real artifact described as reusable despite Phase 6 classification, serious HMC claim from tiny mechanics smoke, or unsupported default-readiness claim. |
| Explanatory diagnostics | Test counts, loader counts, artifact classification counts, synthetic mechanics value/score shapes, and historical artifact availability. |
| Not concluded | No real-artifact reuse, no sampler superiority, no broad posterior correctness, no scientific claim, no default product change unless separately approved. |
| Artifacts | Validation ledger, closeout result, final handoff. |

## Forbidden Claims And Actions

- Do not rank methods without predeclared uncertainty evidence.
- Do not upgrade descriptive diagnostics to promotion evidence.
- Do not launch long benchmarks or serious model comparisons without a new plan.
- Do not claim all BayesFilter filters are HMC-safe.
- Do not load or canary Phase 6 real artifacts as reusable unless a new reviewed
  migration bridge supplies the missing loader schema and target signature.

## Exact Next-Phase Handoff Conditions

There is no automatic Phase 8. Closeout may recommend a later program for:

- serious GPU NeuTra training;
- serious HMC validation;
- particle-filter deterministic target expansion;
- real-model posterior/reference comparison;
- documentation/API stabilization.

## Stop Conditions

Stop if:

- focused tests fail and cannot be repaired within this phase;
- validation would require long runs or GPU training without approval;
- artifact evidence is insufficient to support the planned closeout;
- a closeout draft blurs historical NeuTra success with generic-loader reuse;
- Claude and Codex do not converge after five final-review rounds.

## Phase Execution Steps

1. Run focused tests.
2. Build validation ledger.
3. Write closeout and final stop handoff.
4. Run Claude final read-only review.
5. Patch fixable result wording or stop with blocker.

## End-Of-Subplan Closeout Requirements

The closeout must include a decision table, inference-status table, hard vetoes,
viable implemented surfaces, real-artifact migration blockers, unsupported
claims, and next evidence needed.
