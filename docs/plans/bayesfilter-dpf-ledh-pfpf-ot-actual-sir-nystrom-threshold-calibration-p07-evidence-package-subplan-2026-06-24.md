# P07 Subplan: Evidence Package Or Repair Closeout

Date: 2026-06-24

Status: `DRAFT_LOCAL_REVIEWED`

## Phase Objective

Package the P06 bounded value-route validation evidence and decide the next non-promotion evidence gap.

## Entry Conditions Inherited From Previous Phase

- P06 passed the frozen SVD bounded value-route CP screen.
- P06 status: `P06_PASS_TO_P07_EVIDENCE_PACKAGE`.
- P06 summary artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-summary-2026-06-24.json`.
- P06 result artifact: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p06-svd-fresh-validation-result-2026-06-24.md`.

## Required Artifacts

- P06 aggregate summary JSON.
- P06 result markdown.
- This P07 subplan.
- Any later closeout or repair result must be a separate reviewed artifact.

## Required Checks, Tests, And Reviews

- Parse the P06 summary JSON.
- Verify deterministic validity, exceedance counts, CP upper bound, and status agree between summary and result.
- Verify no default, posterior, HMC, superiority, or broad Nystrom claim is made.
- Review boundary safety before any further experiment or promotion action.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the next justified action after P06 under the statistical evidence discipline? |
| Baseline/comparator | P06 uses the fixed same-artifact compiled streaming TF32 value-route comparator; P07 does not add a new numerical comparison. |
| Primary criterion | Consistency of P06 summary/result with the predeclared P06 gate. |
| Veto diagnostics | Missing/malformed P06 artifacts, inconsistent counts/status, unsupported promotion claims, or any proposed threshold/default change without a reviewed plan. |
| Explanatory diagnostics | P06 row deltas, CP upper bound, runtime, and residual diagnostics. |
| Not concluded | No default readiness, no posterior correctness, no HMC readiness, no statistical superiority, and no broad Nystrom rejection. |

## Forbidden Claims And Actions

- Do not promote SVD/Nystrom to a new default from P07 alone.
- Do not claim posterior correctness, HMC readiness, or statistical superiority.
- Do not change `tau_component=0.03` or the CP gate in P07.
- Do not launch another tuning or validation sweep without a new reviewed subplan.

## Exact Next-Phase Handoff Conditions

- `P07_CLOSEOUT_READY_FOR_NEXT_MODEL_SUITE_OR_DEFAULT_GAP_PLAN`: P07 local checks confirm P06 artifacts and boundary claims are internally consistent.

## Stop Conditions

- Stop before any default promotion, posterior correctness, HMC readiness, or superiority claim.
- P06 summary/result mismatch.
- Required artifact missing or malformed.
- Any next step would require human product/scientific authorization.

## Local Consistency Review

- Consistency: `PASS`; P07 scope is closeout/repair planning, not promotion.
- Correctness: `PASS`; it preserves the P06 statistical interpretation boundary.
- Feasibility: `PASS`; checks are artifact parsing and boundary review.
- Artifact coverage: `PASS`; P06 summary, result, row artifacts, and logs are named.
- Boundary safety: `PASS`; forbidden claims/actions block default and scientific overclaiming.
