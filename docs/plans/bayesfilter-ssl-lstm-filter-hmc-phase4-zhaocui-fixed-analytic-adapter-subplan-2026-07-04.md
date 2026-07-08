# Phase 4 Subplan: Zhao-Cui Fixed Analytic Adapter

Date: 2026-07-04

Status: `BLOCKED_SOURCE_ANCHORED_FIXED_VARIANT_IMPL_UNAVAILABLE`

## Phase Objective

Build or wire the fixed-variant Zhao-Cui adapter for the SSL-LSTM target using
an analytical gradient path and fixed deterministic branch choices suitable for
HMC.

## Entry Conditions Inherited From Previous Phase

- Phase 2 protocol is active.
- Phase 3 local checks passed for SGQF/UKF analytic SSL-LSTM adapters without
  changing the shared benchmark contract.
- The repository does not yet contain an SSL-LSTM Zhao-Cui adapter to wire;
  Phase 4 is blocked on implementation availability, not on review logistics.
- The user has authorized bounded Claude read-only review gates for material
  artifacts in Phases 3-8, so a bounded review of blocker/result/subplan
  artifacts is permitted if needed.
- The project Zhao-Cui source-anchor gate applies before any source-faithful
  or author-faithfulness claim.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase4-zhaocui-fixed-analytic-adapter-result-2026-07-04.md`
- Paper/source anchor ledger for every Zhao-Cui operation used or adapted.
- Classification table for implementation choices:
  `source_faithful`, `fixed_hmc_adaptation`, or `extension_or_invention`.
- Code/tests for fixed branch construction, deterministic repeated evaluation,
  analytical gradient, and artifact metadata.
- Value/score JSON artifacts on tiny SSL-LSTM fixtures.
- Refreshed Phase 5 subplan.

## Required Checks, Tests, And Reviews

- Inspect and cite both the Zhao-Cui paper/math claim and local author source
  lines before implementing any source-route behavior.
- Verify no adaptive randomness, ranks, bases, schedules, or samples remain
  inside the HMC target path unless explicitly frozen and classified.
- If a real SSL-LSTM Zhao-Cui implementation later appears, run focused tests
  for deterministic fixed branch, shape, finite values, analytic score,
  finite-difference diagnostics, and metadata classification.
- Claude read-only review must inspect the cited anchors for any source-related
  claim.
- If the lane still cannot be implemented without inventing a new route, stop
  and record the blocker rather than broadening scope.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the runbook honestly record the SSL-LSTM Zhao-Cui fixed-variant blocker without inventing a new route? |
| Baseline/comparator | Phase 2 protocol, Phase 3 SGQF/UKF adapters, cited Zhao-Cui paper/source anchors, and the current local source inventory. |
| Primary pass criterion | The blocker is recorded accurately, the missing adapter is explicitly classified, and the Phase 5 handoff remains intact. |
| Veto diagnostics | `BLOCK_SOURCE_UNGROUNDED`, hidden implementation claim, invented SSL-LSTM Zhao-Cui route, adaptive randomness in target path, or a handoff that implies Phase 4 can still execute. |
| Explanatory diagnostics | Fixed-rank/basis summaries, score residuals, runtime, and source-code crosswalk notes. |
| Not concluded | Paper-scale Zhao-Cui validity, broad source-faithfulness, HMC success, or method ranking. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase4-zhaocui-fixed-analytic-adapter-result-2026-07-04.md` |

## Forbidden Claims And Actions

- Do not call the route source-faithful unless anchors and classifications pass
  the project Zhao-Cui gate.
- Do not use adaptive randomness in the HMC target.
- Do not replace the fixed variant with a new invented route and call it the
  Zhao-Cui target.
- Do not use automatic differentiation as the requested target gradient path.
- Do not imply that Phase 4 can continue as an implementation phase when the
  SSL-LSTM Zhao-Cui adapter is absent.
- Do not continue if Claude review does not inspect the required anchors for
  source-related claims.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only when:

- Zhao-Cui adapter status is recorded as passed, failed, or blocked with exact
  source/adaptation classification;
- all source-related claims have anchors or are explicitly not checked;
- the shared benchmark contract remains intact;
- Phase 5 subplan is refreshed for LEDH manual VJP work.

## Stop Conditions

- Required Zhao-Cui paper/source anchors cannot be inspected.
- The fixed route would require an unapproved invention to proceed.
- Analytical gradients cannot be built without reverting to autodiff.
- Claude and Codex cannot converge on source-anchor adequacy after five rounds.
- The current repository state still lacks any SSL-LSTM Zhao-Cui adapter to
  wire and no human-approved scope change has added one.

## End-Of-Phase Protocol

1. Run source-anchor or source-inventory checks, deterministic-branch checks,
   and value/score checks as applicable to the current state.
2. Write the Phase 4 result/close record.
3. Draft or refresh the Phase 5 subplan.
4. Review Phase 5 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
