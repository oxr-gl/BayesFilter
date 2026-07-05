# Phase R2 Result: Contract E Reset VJP Decision

Date: 2026-06-29

Status: `R2_BLOCKED_WITH_EXPLICIT_BOUNDARIES`

Subplan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-subplan-2026-06-29.md`

## Objective

Execute the local/static R2 reset VJP decision gate for Contract E Phase 3,
without running material Phase 3 or claiming gradient correctness.

## Claude Review

The patched R2 subplan was re-reviewed by Claude as a bounded read-only review.
Claude returned:

```text
VERDICT: AGREE
```

The R3 handoff subplan was also sent for bounded read-only review as required
by the phase-close protocol.  Round 1 returned `VERDICT: REVISE`; the subplan
was patched to prohibit R3 GPU runs and full-filter FD, limit R3 numerical
checks to local tiny reset fixtures, extend the audit scope to the reset path
and eigensystem boundary, and collapse the R4 handoff text to one
authorization statement.  Round 2 review was then requested.
Round 2 returned:

```text
VERDICT: AGREE
```

## Artifacts Created

- R2 decision note:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-2026-06-29.md`
- R2 decision manifest:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-manifest-2026-06-29.json`
- R2 artifact tests:
  `tests/test_contract_e_phase3_r2_reset_decision_artifacts.py`
- R3 handoff subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r3-reset-blocker-resolution-subplan-2026-06-29.md`

## Decision

R2 does not implement a Contract E reset VJP and does not approve a
stop-gradient material policy.  The reset derivative policy is therefore
closed conservatively:

| Boundary set | R2 classification | Reason |
| --- | --- | --- |
| E01-E13 | `blocked` | No implemented manual reset VJP and no local same-map FD parity artifact.  Spectral branches E05/E07/E10/E11 require fixed-rank treatment before any manual VJP claim. |
| E14 | `non_gradient_monitor` | Diagnostics do not feed the material score route. |

The material blocker remains:

```text
PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN
```

R2 cannot unblock material mode.

## Checks

```bash
python -m pytest tests/test_contract_e_phase3_r1_design_artifacts.py tests/test_contract_e_phase3_gradient_route_audit.py tests/test_contract_e_phase3_r2_reset_decision_artifacts.py -q
python -m json.tool docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-manifest-2026-06-29.json
git diff --check -- docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-subplan-2026-06-29.md docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-2026-06-29.md docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-manifest-2026-06-29.json docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-result-2026-06-29.md docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r3-reset-blocker-resolution-subplan-2026-06-29.md tests/test_contract_e_phase3_r2_reset_decision_artifacts.py
```

Outcomes:

- Focused tests passed: `12 passed`.
- R2 manifest JSON parse passed.
- Diff whitespace check passed.

## Decision Table

| Decision | Status | Evidence | Not concluded |
| --- | --- | --- | --- |
| Reset VJP is not implemented in R2. | Closed as blocked | R2 manifest lists E01-E13 as `blocked`. | No gradient repair. |
| Spectral reset boundaries need fixed-rank policy. | Preserved | Manifest safety rule covers E05/E07/E10/E11. | No spectral adjoint derivation. |
| E14 remains diagnostic only. | Passed | Manifest classifies E14 as `non_gradient_monitor`. | No diagnostic gradient route. |
| Material Phase 3 remains blocked. | Passed | Manifest and script retain blocker code. | No material readiness. |
| R3 handoff drafted. | Passed review | R3 subplan created, reviewed, patched, and Claude Round 2 returned `AGREE`. | R3 not executed. |

## Nonclaims

R2 does not implement a reset VJP, does not approve a stopped-reset material
gradient, does not claim full LGSSM gradient correctness, and does not run GPU,
XLA, Kalman, SIR, SV, HMC, production, or nonlinear-model evidence.
