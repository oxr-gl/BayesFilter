# Phase 1 Subplan: Source And Theta Contract

Date: 2026-07-02

Status: `READY_AFTER_PHASE0`

## Phase Objective

Define and review the mathematical target contract for a parameterized SIR
leaderboard row, including theta coordinates, score quantity, and
source-faithfulness classification.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result confirms the current fixed SIR row is `no_free_theta`.
- Phase 0 result confirms `ParameterizedZhaoCuiSIRSSM` and local analytical
  score tests exist.
- Phase 0 does not make implementation changes.
- Phase 0 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase0-baseline-boundary-result-2026-07-02.md`.

## Required Artifacts

- Target contract:
  `docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md`
- Semantic binding draft:
  `docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md`
- Phase 1 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase1-source-theta-contract-result-2026-07-02.md`
- Refreshed Phase 2 subplan.
- Claude review ledger entry.

## Required Checks/Tests/Reviews

- Inspect local author-source anchor ledger for SIR formulas.
- Inspect `ParameterizedZhaoCuiSIRSSM` parameter convention and score hooks.
- Decide whether truth theta `[0, 0, 0]` is legitimate because it reproduces
  the source base SIR parameter values under the reviewed log-scale
  parameterization.
- Check that any use of `source_faithful` is backed by both paper/source
  anchors and local code anchors.
- Claude read-only review of the target contract path.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the exact free-theta SIR target and score to be benchmarked? |
| Baseline/comparator | Fixed `zhao_cui_sir_austria_model()` source-parity target plus parameterized wrapper. |
| Primary pass criterion | Target contract defines theta, truth-theta semantics, likelihood terms, score terms, row id, classification, nonclaims, allowed diagnostics, and the semantic-binding fields needed to tie a final leaderboard row to this target. |
| Veto diagnostics | Source-faithful claim without anchors; ambiguity between fixed and parameterized row; missing analytical score path definition; missing semantic-binding fields. |
| Explanatory diagnostics | Existing tape and FD tests. |
| Not concluded | No code admission, no full leaderboard completion, no exact likelihood proof. |
| Artifact | Target contract and Phase 1 result. |

## Forbidden Claims/Actions

- Do not call the parameterized theta source-faithful unless anchors prove it.
- Do not alter dataset generator or leaderboard artifacts in Phase 1.
- Do not use FD or autodiff as admitted score provenance.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only if the target contract has:

- a distinct parameterized row id; replacing or retiring the old fixed row is
  forbidden without explicit human authorization in a later request;
- theta coordinate name and truth value;
- truth-theta legitimacy and base-parameter semantics;
- classification as `source_faithful`, `fixed_hmc_adaptation`, or
  `extension_or_invention`;
- required tests and nonclaims;
- Claude or Codex review convergence.

## Stop Conditions

Stop if source classification is ambiguous and requires human direction, if the
target would require changing scientific claim boundaries, or if Claude/Codex
do not converge after five review rounds.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 1 result or blocker.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
