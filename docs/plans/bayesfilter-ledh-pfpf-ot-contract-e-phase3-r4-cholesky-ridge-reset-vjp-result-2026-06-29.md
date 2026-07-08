# Phase R4 Result: Cholesky-Ridge Reset Manual VJP

Date: 2026-06-29

Status: `R4_LOCAL_RESET_VJP_PASSED_MATERIAL_STILL_BLOCKED`

Subplan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r4-cholesky-ridge-reset-vjp-subplan-2026-06-29.md`

## Objective

Implement and test a local manual VJP for the opt-in Contract E
Cholesky-ridge reset map on a fixed-ridge smooth chart.

R4 does not wire the full filtering reverse scan and does not unblock material
Phase 3.

## Reviews

Subplan review:

- Round 1: `VERDICT: REVISE`
- Findings: make fixed-ridge chart mechanically checkable, broaden hidden
  autodiff audit, and make the R5 blocker handoff objective.
- Patched the subplan.
- Round 2: `VERDICT: AGREE`

Implementation review:

- Round 1: `VERDICT: REVISE`
- Finding: the static no-hidden-autodiff/eigh audit did not cover the private
  fixed-ridge forward helper feeding the VJP auxiliary values.
- Patched the test to audit:
  - `contract_e_cholesky_ridge_reset`;
  - `contract_e_cholesky_ridge_reset_fixed_ridge`;
  - `contract_e_cholesky_ridge_reset_fixed_ridge_vjp`;
  - `_contract_e_cholesky_ridge_fixed_ridge_forward`.
- Round 2: `VERDICT: AGREE`

## Implementation

Added to `docs/benchmarks/contract_e_reset_tf.py`:

- `contract_e_cholesky_ridge_reset_fixed_ridge`;
- `contract_e_cholesky_ridge_reset_fixed_ridge_vjp`;
- `_contract_e_cholesky_ridge_fixed_ridge_forward`.

The manual VJP covers local cotangents for:

- `post_flow`;
- `weights`;
- `matrix`;
- `residual_noise`.

The test uses a softmax chart for weights, so the finite-difference comparison
perturbs unconstrained logits and contracts the returned `weights` cotangent
through the softmax VJP.

## Local Evidence

Focused checks:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_contract_e_cholesky_ridge_reset.py tests/test_contract_e_phase3_gradient_route_audit.py tests/test_contract_e_phase3_r2_reset_decision_artifacts.py -q
python -m py_compile docs/benchmarks/contract_e_reset_tf.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py
git diff --check -- docs/benchmarks/contract_e_reset_tf.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py docs/chapters/ch32c_entropic_ot_sinkhorn.tex docs/references.bib docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r4-cholesky-ridge-reset-vjp-subplan-2026-06-29.md tests/test_contract_e_cholesky_ridge_reset.py tests/test_contract_e_phase3_r2_reset_decision_artifacts.py
```

Outcomes:

- Focused tests passed: `13 passed`.
- Python compile checks passed.
- Diff whitespace check passed.

The local parity test checks central finite differences of
`sum(y_star * upstream)` for perturbations in `post_flow`, softmax-chart
weights, `matrix`, and `residual_noise`.  For each accepted comparison it also
asserts identical center/`+h`/`-h` realized ridge and identical ridge-attempt
count.

## Decision Table

| Decision | Status | Evidence | Not concluded |
| --- | --- | --- | --- |
| Fixed-ridge Cholesky reset VJP exists locally. | Passed | Manual VJP helper and central-FD parity test. | No branch-selection derivative. |
| Hidden autodiff/eigh fallback is blocked in the reset helper family. | Passed | Static test audits public branchy, public fixed-ridge, public VJP, and private fixed-ridge forward helpers. | Does not audit unrelated repo files. |
| Fixed-chart condition is enforced in tests. | Passed | Center/plus/minus realized ridge and attempt counts are asserted identical. | No validity across ridge branch changes. |
| Material Phase 3 remains blocked. | Passed | Gradient diagnostic still contains `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`. | No full LGSSM gradient correctness. |

## Nonclaims

R4 does not certify the full filtering reverse scan, LGSSM gradient correctness,
SIR/SV/nonlinear correctness, HMC readiness, production readiness, GPU/XLA
readiness, or correctness across ridge branch changes.

## Next Step

The next justified phase is R5: integrate the local fixed-ridge reset VJP into
the manual likelihood reverse-scan design under a fresh reviewed subplan.  R5
must preserve the material blocker until the integrated reverse scan has its
own local checks and review evidence.
