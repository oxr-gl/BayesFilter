# Phase 5 Subplan: Optional Trusted GPU/XLA Bridge

Date: 2026-07-06

Status: `DRAFT_OPTIONAL_PENDING_PHASE4_RESULT_AND_APPROVAL`

## Phase Objective

Decide whether a trusted GPU/XLA bridge is needed after CPU-hidden HMC mechanics
evidence, and run it only if explicitly approved and still justified.

## Entry Conditions Inherited From Previous Phase

- Phase 4 result exists.
- CPU-hidden hard-veto status is known.
- GPU/XLA evidence is not required for the CPU-hidden mechanics question unless
  this phase records a new, narrow runtime-path question.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase5-optional-gpu-xla-result-2026-07-06.md`
- Optional JSON/Markdown GPU/XLA artifacts only if approved and run.
- Draft/refreshed Phase 6 subplan.

## Required Checks, Tests, And Reviews

- Audit whether GPU/XLA bridge answers a remaining required question.
- If needed, request explicit approval for trusted GPU/CUDA/XLA execution.
- If approved, run the smallest GPU/XLA smoke with provenance and trust basis.
- If not needed or not approved, record deferral without treating it as a
  failure of the CPU-hidden ladder.
- Review Phase 5 result/Phase 6 subplan if external review is available; else
  local Codex substitute review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is a trusted GPU/XLA bridge needed now, and if run, does it pass only a runtime-path hard-veto screen? |
| Baseline/comparator | CPU-hidden HMC ladder artifacts and repo GPU/XLA policy. |
| Primary pass criterion | Either GPU/XLA is explicitly deferred with rationale, or an approved smallest GPU/XLA smoke writes provenance and passes hard-veto checks. |
| Veto diagnostics | Unapproved GPU use, missing provenance, GPU evidence interpreted as posterior/convergence/default readiness, invalid artifact, or runtime hard veto. |
| Explanatory diagnostics | GPU device, XLA/TF32 settings, runtime, acceptance rate, finite counts. |
| Not concluded | HMC convergence, posterior correctness, ranking, default readiness, source-faithful parity, or LEDH result. |

## Forbidden Claims And Actions

- Do not run GPU/CUDA/XLA without explicit approval.
- Do not interpret GPU/XLA pass as convergence or production readiness.
- Do not change default policy.
- Do not run detached or long execution without approval.

## Exact Next-Phase Handoff Conditions

Phase 6 may start only when:

- Phase 5 result exists;
- any GPU/XLA run or deferral is recorded;
- Phase 6 closeout subplan exists.

## Stop Conditions

Stop if GPU approval is required and not granted, if GPU result cannot be
trusted/provenanced, if a runtime hard veto fires, or if continuing would
require default-policy/product-capability/scientific-claim decisions.

## End-Of-Phase Protocol

1. Run required local checks or record deferral.
2. Write Phase 5 result/close record.
3. Draft or refresh Phase 6 subplan.
4. Review Phase 6 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
