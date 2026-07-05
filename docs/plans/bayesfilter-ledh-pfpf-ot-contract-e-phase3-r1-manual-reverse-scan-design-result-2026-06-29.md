# Phase R1 Result: Contract E Manual Reverse-Scan Design

Date: 2026-06-29

Status: `R1_DESIGN_PASSED`

Subplan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-design-subplan-2026-06-29.md`

## Objective

Design and bind the future full manual likelihood reverse-scan route for the
Contract E LGSSM Phase 3 gradient gate, without implementing the reset VJP or
running material gradient evidence.

## Claude Review

Round 1 returned `VERDICT: REVISE`.

Required fixes:

- split Contract E reset into granular sub-boundaries;
- require artifact tests to classify each reset sub-boundary individually;
- state that R2 cannot remove or weaken the material blocker.

The subplan was patched and re-reviewed.  Round 2 returned `VERDICT: AGREE`.

## Artifacts Created

- R1 design:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-design-2026-06-29.md`
- R1 route manifest:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-route-manifest-2026-06-29.json`
- R1 artifact tests:
  `tests/test_contract_e_phase3_r1_design_artifacts.py`
- R2 handoff subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-subplan-2026-06-29.md`

## Design Decision

The future material route is named:

```text
manual_likelihood_reverse_scan_no_autodiff
```

The route is design-only and not implemented in R1.  The manifest records:

```json
{
  "material_gate_authorized": false,
  "material_blocker_code": "PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN"
}
```

Every Contract E reset sub-boundary from weighted moments through final
recentering is classified individually.  E01 through E13 are
`blocked_pending_r2`; E14 is `non_gradient_monitor`.

## Checks

```bash
python -m pytest tests/test_contract_e_phase3_r1_design_artifacts.py tests/test_contract_e_phase3_gradient_route_audit.py -q
python -m json.tool docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-route-manifest-2026-06-29.json >/tmp/contract_e_r1_manifest_check.json
git diff --check -- docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-design-subplan-2026-06-29.md docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-design-2026-06-29.md docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-route-manifest-2026-06-29.json docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-subplan-2026-06-29.md tests/test_contract_e_phase3_r1_design_artifacts.py
```

Outcomes:

- Focused tests passed: `7 passed`.
- Manifest JSON parse check passed.
- Diff whitespace check passed.

## Decision Table

| Decision | Status | Evidence | Not concluded |
| --- | --- | --- | --- |
| Future score route must be a full manual likelihood reverse scan. | Bound in manifest | `selected_route_name=manual_likelihood_reverse_scan_no_autodiff` | Route is not implemented. |
| Contract E reset is not one opaque derivative boundary. | Passed | E01-E14 listed individually in design and manifest. | No reset VJP chosen yet. |
| Material Phase 3 remains blocked. | Passed | Manifest and script retain `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`. | No material gradient evidence. |
| Advance to R2 reset VJP decision. | Justified | R2 handoff subplan drafted; R1 checks passed. | R2 cannot unblock material mode by itself. |

## Nonclaims

R1 does not implement a Contract E reset VJP, does not repair the gradient, and
does not authorize GPU, FD, Kalman comparison, or material Phase 3 runs.  R2
must decide the reset derivative policy, and a later implemented-and-audited
full reverse scan is required before material mode can be considered.
