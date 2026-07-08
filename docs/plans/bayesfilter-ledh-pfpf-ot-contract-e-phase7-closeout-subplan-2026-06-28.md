# Phase 7 Subplan: Contract E final audit and closeout

Date: 2026-06-28

Status: `DRAFT_PENDING_PHASE6`

## Phase Objective

Audit the whole Contract E testing program and decide whether the candidate is
rejected, blocked, or promoted only to a next evidence program.

## Entry Conditions Inherited From Previous Phase

- Phase 0-6 result artifacts exist or a documented blocker explains why a phase
  stopped.
- Claude review ledgers and execution ledger are current.

## Required Artifacts

- Phase 7 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase7-closeout-result-2026-06-28.md`
- Stop handoff:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-visible-stop-handoff-2026-06-28.md`
- Final Claude review ledger update.

## Required Checks, Tests, And Reviews

- `git diff --check` on touched Contract E plan/code/test artifacts.
- Focused `rg` audit for forbidden route strings such as
  `transport_ad_mode=full` in new Contract E evidence paths.
- Focused artifact completeness audit.
- Bounded Claude read-only final review.
- MathDevMCP may be used for LaTeX label/math consistency if the closeout
  changes math claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the justified status of Contract E after the gated evidence program? |
| Baseline/comparator | All phase result artifacts and the original barycentric covariance-loss diagnostic. |
| Primary pass criterion | Closeout states passed/failed/blocked per phase, preserves nonclaims, records exact next action, and has no unsupported scientific or production claim. |
| Veto diagnostics | Missing phase result, hidden failure, unsupported claim, incomplete Claude review trail, missing command manifest, or unclassified GPU/FD uncertainty issue. |
| Explanatory diagnostics | Tables of values, gradients, FD z-scores, conditioning, runtime, memory, and review findings. |
| Not concluded | Anything outside explicitly passed gates. |
| Artifact | Phase 7 closeout and stop handoff. |

## Forbidden Claims And Actions

- Do not mark the whole program complete if any required phase is missing
  without a blocker.
- Do not claim production readiness or HMC readiness.
- Do not retroactively change thresholds after seeing results.

## Exact Next-Phase Handoff Conditions

There is no next phase in this master program.  The handoff condition is one of:

- `REJECTED`: evidence argues against Contract E as currently defined;
- `BLOCKED`: a specific human/tool/runtime/mathematical blocker remains;
- `PROMOTE_TO_NEXT_PROGRAM`: evidence justifies a separate implementation or
  production-readiness program, with nonclaims preserved.

## Stop Conditions

Stop if artifacts are missing, review does not converge, or closeout would
require changing policy or scientific claims beyond this program.

## End-Of-Phase Protocol

Run final checks, write result, write handoff, run bounded final review, repair
fixable issues, and report the final status to the user.
