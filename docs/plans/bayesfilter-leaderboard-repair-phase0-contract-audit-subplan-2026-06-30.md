# Phase 0 subplan: contract audit and fail-closed schema

Date: 2026-06-30

Status: `DRAFT_REVIEW_READY`

## Phase Objective

Create and verify the leaderboard contract that prevents stale target labels, missing parameterization, and autodiff/tape gradients from being reported as analytical leaderboard scores.

## Entry Conditions Inherited From Previous Phase

- Master program exists and names this phase as Phase 0.
- Current known artifacts exist or are explicitly missing:
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
  - `docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-30.json`
  - `docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md`
  - P91 SIR d18 result/manifests.
- No implementation edits have been made under this program yet.

## Required Artifacts

- This subplan.
- Phase result:
  `docs/plans/bayesfilter-leaderboard-repair-phase0-contract-audit-result-2026-06-30.md`
- Updated or confirmed Claude review ledger:
  `docs/plans/bayesfilter-leaderboard-repair-claude-review-ledger-2026-06-30.md`
- Updated visible execution ledger:
  `docs/plans/bayesfilter-leaderboard-repair-visible-execution-ledger-2026-06-30.md`
- Draft/refreshed Phase 1 subplan.

## Required Checks, Tests, Reviews

- Local artifact presence check for master program, runbook, all phase subplans, and existing leaderboard artifacts.
- Text check that each phase subplan contains required headings:
  - Phase Objective
  - Entry Conditions
  - Required Artifacts
  - Required Checks
  - Evidence Contract
  - Forbidden Claims
  - Next-Phase Handoff Conditions
  - Stop Conditions
- Read-only Claude review of this subplan or master program with `VERDICT: AGREE` before advancing.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the program have a fail-closed leaderboard contract before implementation starts? |
| Baseline/comparator | Current June 30 two-lane artifacts plus corrected actual-SV and P91 SIR evidence. |
| Primary criterion | Every planned phase has explicit artifacts, checks, forbidden claims, next handoff, and stop conditions. |
| Veto diagnostics | Missing phase subplan; missing evidence contract; stale `not_same_target` not listed as a veto; no rule excluding `GradientTape` as analytical score; no rule requiring free `theta` for score rows. |
| Explanatory diagnostics | `rg`, `sed`, and JSON key inspection. |
| Not concluded | No implementation correctness, production readiness, GPU performance, or scientific superiority. |
| Artifact | Phase 0 result and execution ledger entry. |

## Forbidden Claims And Actions

- Do not claim any leaderboard blocker is fixed in this phase.
- Do not edit algorithm implementation files in this phase unless the subplan is revised and reviewed.
- Do not run GPU/XLA benchmarks in this phase.
- Do not claim Claude approval authorizes execution beyond the written phase gate.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- Master program, runbook, all phase subplans, ledgers, and Phase 0 result exist.
- Local checks pass.
- Claude review of the master program or this subplan returns `VERDICT: AGREE`.
- Phase 1 subplan still says actual-SV SGQF score remains value-only unless strict analytical score is implemented.

## Stop Conditions

Stop and write a blocker result if:

- Required artifacts are missing and cannot be created without overwriting unrelated user work.
- Claude flags a material plan defect that cannot be repaired within five review rounds.
- The current artifact state contradicts the corrected actual-SV target note in a way not covered by Phase 1.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 0 result/close record.
3. Draft or refresh Phase 1 subplan.
4. Review Phase 1 subplan for consistency, correctness, feasibility, artifact coverage, and boundary safety.
