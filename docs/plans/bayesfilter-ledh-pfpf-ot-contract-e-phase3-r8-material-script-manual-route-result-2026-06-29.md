# Phase R8 Result: Phase 3 Tiny Material Manual Route

Date: 2026-06-29

Status: `R8_TINY_MATERIAL_ROUTE_UNBLOCKED_FULL_PHASE3_STILL_BLOCKED`

Subplan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r8-material-script-manual-route-execution-subplan-2026-06-29.md`

## Objective

Move the verified fixed-ridge Contract E manual LGSSM route into the actual
Phase 3 material entrypoint, replacing the old tiny material blocker only if
the real script path runs without an outer `tf.GradientTape` and passes
same-scalar finite differences.

## Claude Reviews

Plan review:

- Round 1: `VERDICT: REVISE`
- Claude required a real material entrypoint execution, explicit generic
  autodiff API audits, and blocker replacement tied to actual material-route
  execution rather than helper parity alone.
- Round 2: `VERDICT: AGREE`

Implementation review:

- `VERDICT: AGREE`
- Claude confirmed that material mode dispatches to the fixed-ridge manual
  route before the taped diagnostic wrapper, emits
  `score_route=manual_likelihood_reverse_scan_no_autodiff`, forbids branchy
  reset in the material route, passes same-scalar FD on the tiny fixture, and
  preserves the full `T=10` blocker.

## Implementation

Updated:

- `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`
- `tests/test_contract_e_phase3_material_manual_route.py`
- `tests/test_contract_e_phase3_gradient_route_audit.py`
- Current-state Contract E audit tests that inspected the live Phase 3 script.

The Phase 3 script now has a material tiny route:

```text
score_route=manual_likelihood_reverse_scan_no_autodiff
route_label=contract_e_cholesky_fixed_ridge_manual_lgssm_tiny
```

For `--gate-mode material`, the script accepts only the reviewed tiny route:

- `state_dim=1`;
- `time_steps=2`;
- `num_particles=4`;
- `seed_count=1`;
- `settings=0.55:2`;
- fixed ridge `lambda=0.75`;
- `--no-xla`;
- FP64 material precision with TF32 disabled; and
- FD steps `1e-5,1e-5,1e-5`.

Non-tiny material runs remain blocked with:

```text
PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION
```

## Local Evidence

Focused pytest:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest \
  tests/test_contract_e_phase3_material_manual_route.py \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  tests/test_contract_e_cholesky_ridge_reset.py \
  tests/test_contract_e_phase3_gradient_route_audit.py -q
```

Outcome: `17 passed`.

Documented material entrypoint:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  --device-scope cpu \
  --num-particles 4 \
  --seed-count 1 \
  --time-steps 2 \
  --state-dims 1 \
  --settings 0.55:2 \
  --contract-e-reset-factorization cholesky-ridge \
  --chol-ridge-abs 0.75 \
  --chol-ridge-rel 0 \
  --chol-ridge-max-attempts 1 \
  --gate-mode material \
  --fd-steps 1e-5,1e-5,1e-5 \
  --no-xla \
  --output /tmp/contract_e_phase3_r8_tiny_material_final.json
```

Outcome: `{"status": "passed"}`.

The output artifact reported:

- `score_route=manual_likelihood_reverse_scan_no_autodiff`;
- `route_label=contract_e_cholesky_fixed_ridge_manual_lgssm_tiny`;
- `outer_gradient_tape_used=false`;
- `tf32_execution_enabled=false`;
- `same_scalar_fd.status=pass`;
- all three parameter rows passed with branch replay stable; and
- absolute FD errors around `1e-11`.

Hygiene checks:

```bash
python -m py_compile \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  docs/benchmarks/contract_e_reset_tf.py \
  tests/test_contract_e_phase3_material_manual_route.py \
  tests/test_contract_e_phase3_gradient_route_audit.py \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py
```

Outcome: passed.

```bash
git diff --check -- \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r8-material-script-manual-route-execution-subplan-2026-06-29.md \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  tests/test_contract_e_phase3_material_manual_route.py \
  tests/test_contract_e_phase3_gradient_route_audit.py \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  tests/test_contract_e_cholesky_ridge_reset.py \
  tests/test_contract_e_phase3_r1_design_artifacts.py \
  tests/test_contract_e_phase3_r2_reset_decision_artifacts.py
```

Outcome: passed.

## Decision Table

| Decision | Status | Evidence | Not concluded |
| --- | --- | --- | --- |
| The real Phase 3 material entrypoint can execute the fixed-ridge manual tiny route. | Passed | CLI `--gate-mode material` tiny run passed and emitted the expected route label. | No full `T=10` material evidence. |
| The tiny material route no longer uses outer `tf.GradientTape`. | Passed | Material dispatch returns before taped wrapper; audits forbid generic autodiff APIs in material route functions. | Taped wrapper remains available for non-material smoke diagnostics. |
| The material tiny manual score matches same-scalar FD. | Passed | All three LGSSM parameter rows passed with branch replay stable and errors around `1e-11`. | No exact Kalman statistical gate. |
| Branchy ridge escalation is separated from material manual score. | Passed | Material route calls `contract_e_cholesky_ridge_reset_fixed_ridge`; static audit forbids branchy reset in material route functions. | Branchy reset value diagnostics remain separate. |
| Full Phase 3 material statistical gate remains blocked. | Preserved intentionally | Non-tiny material scopes raise `PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION`. | No claim that full Phase 3 is complete. |

## Nonclaims

R8 does not certify full `T=10,N>=64` Phase 3 LGSSM correctness, exact Kalman
agreement, SIR/SV correctness, HMC readiness, production readiness,
GPU/XLA/TF32 readiness, or broad scientific validity.

## Next Step

The next justified phase is R9: run a reviewed full Phase 3 material
statistical gate using the manual route, likely starting with the smallest
`T=10`/`N=64` CPU or reviewed GPU scope before any larger evidence claim.
