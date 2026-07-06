# BayesFilter NeuTra Real Target HMC Smoke Phase 5 Subplan

Date: 2026-07-06

## Phase Objective

Close the program with a clear decision, completed evidence, unresolved
blockers, nonclaims, and next-program boundary.

## Entry Conditions Inherited From Previous Phase

- Phase 4 stopped with status `BLOCKED_NO_ENTRY_HMC_SMOKE_NOT_RUN`.
- All prior phase results are written.

## Required Artifacts

- Phase 5 closeout result:
  `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase5-closeout-result-2026-07-06.md`.
- Updated visible stop handoff.

## Required Checks/Tests/Reviews

- Local text checks for result artifacts.
- Final bounded read-only review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What did this program prove, block, or leave for a separate program? |
| Baseline/comparator | Phase 0-4 results. |
| Primary criterion | Closeout separates transport/import evidence, missing real-target authority, no-mechanics/no-HMC blockers, and nonclaims. |
| Veto diagnostics | Unsupported HMC/posterior/product claims or missing blocker details. |
| Explanatory diagnostics | Review status, test summary, artifact index. |
| Not concluded | Anything not explicitly supported by phase artifacts. |
| Artifact | Phase 5 result and final stop handoff. |

## Forbidden Claims/Actions

- Do not add new experiments in closeout.
- Do not change pass/fail criteria after seeing results.
- Do not commit/push without explicit approval.
- Do not reopen HMC, GPU, training, package installation, or live external
  target-authority work in this program.

## Exact Next-Phase Handoff Conditions

This is the terminal phase. Any further work must be a separate reviewed
program.

## Stop Conditions

Stop if closeout cannot faithfully classify the current evidence or if review
does not converge after five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 5 result;
3. update final visible handoff;
4. review final decision for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
