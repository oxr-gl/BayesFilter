# Phase 2 Subplan: Primitive Parity And FD Validation

Date: 2026-07-04

Status: `READY_REVIEWED`

## Phase Objective

Validate the candidate no-tape total VJP against the current tape-backed total
helper and same-scalar finite differences on small primitive tensors.

## Entry Conditions Inherited From Previous Phase

Phase 1 provided a finite, static-clean no-tape total VJP candidate and a local
close record.  The Phase 1 read-only review gate accepted the result and this
refreshed validation subplan with `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.

## Required Artifacts

- Primitive validation JSON:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-2026-07-04.json`
- Phase 2 result:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-result-2026-07-04.md`
- Refreshed Phase 3 subplan.

## Required Checks, Tests, And Reviews

- Focused pytest comparing candidate VJP to tape-backed total helper on tiny
  tensors.
- Same-scalar finite-difference check for each differentiated input.
- Tolerances must be declared before running the validation and may not be
  loosened after failures without a visible repair note.
- Negative check showing stopped-key partial derivative does not pass the
  unstopped total target when dependencies matter.
- Static no-tape check remains passing.
- Claude read-only review of validation result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the no-tape primitive compute the same total VJP as the finite transport scalar? |
| Baseline/comparator | Tape-backed total helper and same-scalar finite differences. |
| Primary criterion | Candidate VJP matches tape and FD within declared tiny-tensor tolerances for differentiated inputs. |
| Veto diagnostics | Candidate matches stopped route but not total route; FD mismatch beyond predeclared tolerance; nonfinite cotangent; tape found in production helper; wrong scalar; tolerances changed after seeing failures. |
| Explanatory diagnostics | Per-input max absolute errors, relative errors, tensor shapes. |
| Not concluded | No downstream SIR/LGSSM score admission, no GPU scalability, no HMC readiness. |

## Forbidden Claims And Actions

- Do not use primitive parity alone as leaderboard score evidence.
- Do not change tolerances after seeing failures.
- Do not hide failed input components.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- primitive parity and FD checks pass;
- stopped-route negative check catches the original bug;
- Phase 2 result records exact tolerances and artifacts;
- Phase 3 SIR regression subplan is refreshed and reviewed.

## Stop Conditions

Stop if:

- no-tape candidate fails tape or FD parity;
- stopped-key route also passes because the test is insensitive;
- Phase 2 cannot state fixed tolerances before running;
- validation artifacts do not identify per-input errors;
- Claude blocks validation and the issue is not fixed within five rounds.

## Phase-End Duties

At the end of Phase 2:

1. run required local checks;
2. write Phase 2 result;
3. draft or refresh Phase 3 subplan;
4. review Phase 3 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
