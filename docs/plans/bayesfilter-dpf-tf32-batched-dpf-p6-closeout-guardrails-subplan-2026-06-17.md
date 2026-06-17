# Phase 6 Subplan - Closeout And Guardrails - 2026-06-17

## Phase Objective

Close the visible TF32 batched DPF master program with explicit guardrails,
remaining limitations, artifact index, and next research actions.

## Entry Conditions Inherited From Previous Phase

- Phase 0 through Phase 4 passed.
- Phase 5 result exists and records
  `PHASE_5_HMC_FACING_DIAGNOSTICS_PASSED_WITH_GPU_HMC_TF32_LIMITATION`.
- No HMC readiness, posterior correctness, production readiness, public API
  readiness, TF32 superiority, or particle-cloud sharding claim has been made.

## Required Artifacts

- This subplan.
- Phase 6 result:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p6-closeout-guardrails-result-2026-06-17.md`.
- Refreshed visible stop handoff.
- Updated ledger entry.

## Required Checks, Tests, And Reviews

Local checks:

1. Verify the Phase 4 and Phase 5 result statuses.
2. Verify required Phase 5 artifacts exist.
3. Run `git diff --check`.
4. Review closeout text for forbidden claims.

Review:

- Claude review is optional unless the closeout proposes a default-policy,
  public API, or HMC-readiness change. This closeout should not propose those
  changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Is the visible execution recoverable and honestly bounded after Phase 5? |
| Baseline/comparator | Phase 0-5 result artifacts and current handoff. |
| Primary pass criterion | Closeout result lists final status, artifacts, checks, limitations, nonclaims, and next actions without unsupported claims. |
| Veto diagnostics | Missing result artifact, stale handoff, default/HMC/posterior claim, or unresolved hard-veto hidden as success. |
| Explanatory diagnostics | Git status and artifact inventory. |
| What will not be concluded | No production readiness, posterior correctness, HMC readiness, TF32 superiority, or GPU-scale score proof. |
| Artifact preserving result | Phase 6 result and refreshed handoff. |

## Forbidden Claims And Actions

- Do not claim HMC readiness.
- Do not claim posterior correctness.
- Do not claim production/default/public API readiness.
- Do not claim TF32 superiority.
- Do not claim one filter's particles are sharded across GPUs.
- Do not change defaults.
- Do not modify unrelated dirty files.

## Handoff Conditions

The program may close if:

- Phase 6 result is written;
- ledger and handoff point to the final status;
- all forbidden claims are absent;
- next actions are stated as research/engineering follow-ups, not completed
  readiness claims.

## Stop Conditions

Stop and write a blocker if:

- Phase 5 artifacts are missing or contradictory;
- closeout cannot avoid a forbidden claim;
- evidence gaps require a new implementation or experiment before honest
  closeout.
