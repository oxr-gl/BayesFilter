# BayesFilter LGSSM-First NeuTra/HMC Phase 0 Subplan

Date: 2026-07-06

## Phase Objective

Freeze the LGSSM-first scope, explicitly defer DSGE/c603 to a later stress
phase, and validate the visible gated execution/review protocol before any code
implementation or HMC/NeuTra execution.

## Entry Conditions Inherited From Previous Phase

- No previous phase in this program.
- Existing c603 import and real-target blocker artifacts remain historical
  context only.
- User has directed that BayesFilter should start with LGSSM and non-DSGE
  SSMs rather than DSGE.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-master-program-2026-07-06.md`
- Visible runbook:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-gated-execution-runbook-2026-07-06.md`
- Execution ledger:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-execution-ledger-2026-07-06.md`
- Stop handoff:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-visible-stop-handoff-2026-07-06.md`
- Phase 0 result:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase0-scope-reset-result-2026-07-06.md`
- Phase 1 subplan:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase1-interface-inventory-subplan-2026-07-06.md`
- Launch review bundle:
  `docs/reviews/bayesfilter-lgssm-first-neutra-hmc-launch-review-bundle-2026-07-06.md`

## Required Checks/Tests/Reviews

- Local text checks for required headings and artifact existence.
- `git diff --check` over new planning/review artifacts.
- Bounded Claude read-only launch review, or documented fresh Codex
  read-only substitute if Claude is unavailable after tiny-probe handling.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the LGSSM-first NeuTra/HMC program scoped, bounded, and safe to enter Phase 1 inventory? |
| Baseline/comparator | Existing BayesFilter generic SSM, QR LGSSM, HMC smoke, c603 blocker, and visible runbook template. |
| Primary criterion | Required planning artifacts exist, defer DSGE/c603, name approvals/stop conditions, and preserve nonclaims. |
| Veto diagnostics | DSGE/c603 used as foundation, hidden HMC/training/GPU launch, missing subplan fields, unsupported readiness/product/scientific claims, or unclear review authority. |
| Explanatory diagnostics | Artifact list, local text checks, review status. |
| Not concluded | No interface correctness, no LGSSM target correctness, no HMC readiness, no NeuTra readiness. |
| Artifact | Phase 0 result and reviewed Phase 1 subplan. |

## Forbidden Claims/Actions

- Do not edit algorithm code in Phase 0.
- Do not run HMC, NeuTra training, GPU/CUDA, package installation, or git
  commit/push.
- Do not use DSGE/c603 as the foundation.
- Do not claim posterior convergence, HMC readiness, production readiness, or
  broad nonlinear SSM support.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only after:

- Phase 0 local checks pass;
- launch review returns `VERDICT: AGREE` or a documented substitute review
  agrees;
- the stop handoff says Phase 1 inventory is next.

## Stop Conditions

Stop if launch review finds a material unresolved boundary issue, if local
checks fail in a way that cannot be patched safely, if review cannot converge
after five rounds for the same blocker, or if continuing would require human
approval for GPU/training/HMC/package/git/detached execution.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 0 result;
3. draft or refresh Phase 1 subplan;
4. review Phase 1 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
