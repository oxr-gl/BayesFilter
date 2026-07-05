# Phase 6 Subplan: Value Validation Gate

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Validate the admitted value paths before any gradient admission is allowed.

## Entry Conditions Inherited From Previous Phase

- Phase 5 implementation is reviewed closed.
- Reviewed lane semantics and structural-admission categories are frozen.
- No gradient admission is authorized yet.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-result-2026-07-01.md`
- refreshed Phase 7 subplan:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-subplan-2026-07-01.md`
- validation tests/manifests named by the executable refresh.

## Required Checks/Tests/Reviews

This phase requires a reviewed executable refresh before any runtime.
That refresh must define:

- exact affine/LGSSM recovery checks,
- exact fixed-cloud one-step oracle checks,
- exact-target versus declared-surrogate separation checks,
- exact value-path tests to run,
- CPU/GPU policy for each command.

Required read-only Claude reviews:

- Phase 6 result,
- refreshed Phase 7 subplan.

## Skeptical Plan Audit

| Risk Checked | Phase 6 Control |
| --- | --- |
| Wrong baseline | Validation compares each lane only against the exact or declared scalar it is authorized to approximate. |
| Proxy metric promoted | Runtime and passing tests do not imply gradient or HMC authority. |
| Missing stop condition | Any lane that cannot state its scalar/comparator honestly must block. |
| Unfair comparison | Exact-target and declared-surrogate lanes must not be mixed in one pass claim. |
| Hidden assumption | Phase 6 must spell out exact comparators and tolerances before runtime. |
| Stale context | Validation is constrained to reviewed implementation and lane contracts. |
| Environment mismatch | Runtime commands require reviewed CPU/GPU policy. |
| Artifact-answer mismatch | Phase 6 must yield a value-gate decision, not a derivative or production decision. |

Audit status: executable only after a refreshed reviewed validation subplan is written.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the implemented value paths reproduce the exact or declared scalar they are authorized to compute at the intended claim level? |
| Baseline/comparator | reviewed Phase 5 implementation and the exact/declared comparators frozen in earlier phases. |
| Primary criterion | Phase 6 passes only when each reviewed lane clears its value comparator gate without target drift. |
| Veto diagnostics | wrong-scalar tieout, surrogate promoted as exact-target evidence, affine recovery failure, fixed-cloud oracle failure, or branch-invalid comparison. |
| Explanatory diagnostics | runtimes, point counts, branch telemetry, and error tables. |
| Not concluded | No gradient admission, no HMC readiness, and no top-level/production promotion. |
| Artifact | reviewed value-validation result and refreshed Phase 7 subplan. |

## Forbidden Claims/Actions

- Do not claim gradient support before the value gate passes.
- Do not compare one lane against the wrong target or surrogate.
- Do not run runtime commands not named by the reviewed executable refresh.

## Exact Next-Phase Handoff Conditions

Phase 7 may start only if:

- the executable Phase 6 refresh is reviewed `AGREE` before runtime;
- the Phase 6 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 7 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records which value lanes passed, which blocked, and what
  exact comparator each lane used.

## Stop Conditions

- A lane fails its value comparator gate.
- A lane's comparator cannot be stated honestly.
- Focused runtime checks fail and cannot be repaired within reviewed scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require wider runtime authority than the reviewed executable
  refresh provides.

## End-Of-Phase Requirements

1. Write an executable refresh before runtime.
2. Run the reviewed focused value checks.
3. Write the Phase 6 result.
4. Refresh the Phase 7 subplan.
5. Review the Phase 6 result and refreshed Phase 7 subplan.
6. Update the execution ledger and Claude review ledger.
