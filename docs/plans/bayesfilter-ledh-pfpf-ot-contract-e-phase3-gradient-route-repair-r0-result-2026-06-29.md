# Contract E Phase 3 Gradient Route Repair R0 Result

Date: 2026-06-29

Status: `R0_CONTAINMENT_PASSED`

Plan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-gradient-route-repair-plan-2026-06-29.md`

## Objective

Prevent the current Contract E Phase 3 diagnostic from producing material
gradient evidence through an outer `tf.GradientTape` score route while only the
transport matrix has a manual/custom VJP.

## Review

Claude bounded read-only review inspected the repair plan and current Phase 3
diagnostic and returned `VERDICT: AGREE`.

Reviewer note incorporated during execution:

- the static audit must verify that material mode is impossible while
  `_make_compiled_value_and_gradient` still contains an outer `GradientTape`.

## Changes

- Renamed the current transport-gradient route in
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py` from the
  misleading `manual-custom-vjp` to `manual-transport-vjp-only`.
- Updated manifest text to state that the current reverse route is an outer
  `GradientTape` diagnostic with transport-only VJP support, not a full manual
  likelihood reverse scan.
- Added a hard material-mode blocker:
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.
- Added `tests/test_contract_e_phase3_gradient_route_audit.py` to enforce that
  material mode remains blocked while the score route still contains the outer
  tape.

## Checks

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py
python -m pytest tests/test_contract_e_phase3_gradient_route_audit.py -q
git diff --check -- docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py tests/test_contract_e_phase3_gradient_route_audit.py docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-gradient-route-repair-plan-2026-06-29.md
python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py --gate-mode material --output /tmp/contract_e_phase3_should_not_run.json
```

Outcomes:

- Compile check passed.
- Focused pytest passed: `3 passed`.
- Diff whitespace check passed.
- Material invocation failed immediately with the expected blocker code before
  any TensorFlow/GPU/FD/material computation.

## Decision Table

| Decision | Status | Evidence | Not concluded |
| --- | --- | --- | --- |
| Current taped Phase 3 score route cannot be promoted as material evidence. | Passed | Material parse path raises `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`. | No Contract E gradient correctness. |
| Static guard catches the known route mismatch. | Passed | Test checks route naming, outer tape presence, and material blocker. | No full route audit manifest yet. |
| Proceed to manual reverse-scan repair design. | Justified next step | R0 containment is complete and Claude agreed with the staged plan. | No GPU, FD, or material Phase 3 run authorized. |

## Nonclaims

This result does not repair the Contract E gradient.  It only prevents the
known wrong wiring from being used as material evidence.  Phase R1 must design
the full manual likelihood reverse scan and account for every derivative
boundary before implementation or numerical promotion.
