# P82 Phase 0 Subplan: Governance Bootstrap

status: DRAFT_PENDING_REVIEW
date: 2026-06-22

## Phase Objective

Initialize the P82 governed execution lane: master program, visible runbook,
ledgers, stop handoff, approval register, and nonclaim boundaries.

## Entry Conditions Inherited From Previous Phase

- User requested execution of a governed master-program prompt.
- P81 correction artifacts exist and define the corrected comparator and
  regression-FD protocol.
- Manual-adjoint lane is reset/inventory only and must not be treated as ready.
- Current worktree is dirty; unrelated user/other-lane changes must be
  preserved.

## Required Artifacts

- P82 master program.
- P82 visible gated execution runbook.
- P82 execution ledger.
- P82 Claude review ledger.
- P82 stop handoff.
- P0 result.
- P1 subplan draft or refresh.

## Required Checks / Tests / Reviews

- `test -f` for required P82 bootstrap artifacts.
- `rg` checks for forbidden overclaims in P82 artifacts.
- `git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p82-*`
- Claude read-only review of the bootstrap fact packet, unless blocked by
  approval.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are the P82 governance artifacts sufficient and safe to launch visible execution? |
| Baseline/comparator | P81 route/protocol corrections and visible runbook template. |
| Primary criterion | Required bootstrap artifacts exist, preserve corrected protocol, include repair loop, and do not authorize GPU/code/scientific claims prematurely. |
| Veto diagnostics | Missing artifact, detached execution, Claude as execution authority, oracle language, central-difference promotion, JVP/autodiff comparator promotion, missing stop conditions, or missing approval register. |
| Explanatory diagnostics | Dirty worktree summary and anticipated approval list. |
| Not concluded | Any numerical gradient, GPU, HMC, posterior, default, or scientific claim. |
| Artifact preserving result | P0 result under `docs/plans`. |

## Forbidden Claims / Actions

- Do not run GPU/CUDA/TensorFlow GPU work.
- Do not edit code.
- Do not claim LEDH gradient validity.
- Do not claim Zhao-Cui is an oracle.
- Do not run detached agents or background supervisors.
- Do not revert unrelated dirty files.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- P0 artifacts exist;
- local artifact checks pass or have explicit non-material warnings;
- Claude review agrees, or review is blocked by approval and the user permits
  proceeding without it for P0 only;
- P1 subplan exists.

## Stop Conditions

Stop if:

- P0 artifacts are missing or internally inconsistent;
- review identifies a material blocker that cannot be fixed in five rounds;
- Claude usage approval is denied and the user requires Claude before launch;
- continuing would require GPU/code/long-run work before P1/P2 planning.
