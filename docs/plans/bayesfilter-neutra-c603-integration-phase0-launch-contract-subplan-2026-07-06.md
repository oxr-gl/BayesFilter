# BayesFilter NeuTra c603 Integration Phase 0 Subplan

Date: 2026-07-06

## Phase Objective

Freeze the launch contract for BayesFilter NeuTra c603 integration: scope,
evidence, review protocol, approval boundaries, local checks, and handoff into
Phase 1 implementation.

## Entry Conditions Inherited From Previous Phase

- No previous phase in this program.
- Manual c603 import validation exists at
  `docs/plans/bayesfilter-neutra-c603-followup-import-validation-result-2026-07-06.md`.
- c603 target signature is known:
  `8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07`.
- The worktree may contain unrelated dirty files; they must be preserved.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-neutra-c603-integration-master-program-2026-07-06.md`.
- Visible runbook:
  `docs/plans/bayesfilter-neutra-c603-integration-visible-gated-execution-runbook-2026-07-06.md`.
- Execution ledger:
  `docs/plans/bayesfilter-neutra-c603-integration-visible-execution-ledger-2026-07-06.md`.
- Stop handoff:
  `docs/plans/bayesfilter-neutra-c603-integration-visible-stop-handoff-2026-07-06.md`.
- Phase 1 subplan:
  `docs/plans/bayesfilter-neutra-c603-integration-phase1-legacy-adapter-subplan-2026-07-06.md`.
- Optional review record under `docs/reviews/`.

## Required Checks, Tests, Reviews

- Local text checks:
  - required artifact paths exist;
  - each subplan contains required headings;
  - master/runbook contain the forbidden claims boundary.
- Skeptical plan audit recorded in the ledger.
- Material read-only review of the launch plan with Claude when available, or a
  recorded Codex substitute if Claude is unavailable after probe.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the c603 integration program scoped, bounded, and ready to enter Phase 1 implementation? |
| Baseline/comparator | Existing manual c603 import validation and local BayesFilter dense-IAF/fixed-transport test surfaces. |
| Primary criterion | Required planning artifacts exist, name approval/stop conditions, preserve nonclaims, and Phase 1 has exact handoff conditions. |
| Veto diagnostics | Missing required subplan headings, missing stop conditions, unsupported claims, hidden GPU/HMC/training launch, or unclear review authority. |
| Explanatory diagnostics | Text-check output, review verdict, dirty worktree summary. |
| Not concluded | No code correctness, no adapter acceptance, no mechanics success, no HMC readiness. |
| Artifact | Phase 0 result note. |

## Forbidden Claims/Actions

- Do not claim implementation completion.
- Do not claim c603 posterior convergence, HMC readiness, production readiness,
  or scientific validity.
- Do not run GPU, training, long HMC, package installation, or detached
  overnight execution.
- Do not modify unrelated dirty worktree files.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- the master program, runbook, ledger, stop handoff, and Phase 1 subplan exist;
- local text checks pass;
- the review gate is `AGREE` or a documented reviewer substitute is accepted as
  weaker but sufficient for Phase 1 planning;
- no approval-required action remains before Phase 1's CPU-only implementation
  work.

## Stop Conditions

Stop and write
`docs/plans/bayesfilter-neutra-c603-integration-phase0-launch-contract-result-2026-07-06.md`
as blocked if:

- required artifacts cannot be written;
- review identifies a material unfixable boundary problem;
- more than five repair/review rounds are needed for the same blocker;
- continuing would require GPU, long HMC, training, package installation, or
  destructive git/filesystem action.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 0 result;
3. draft or refresh Phase 1 subplan;
4. review Phase 1 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
