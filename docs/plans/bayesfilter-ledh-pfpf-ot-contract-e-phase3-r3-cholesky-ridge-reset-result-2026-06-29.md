# Phase R3 Result: Cholesky-Ridge Reset Repair

Date: 2026-06-29

Status: `R3_LOCAL_RESET_REPAIR_IMPLEMENTED_MATERIAL_STILL_BLOCKED`

Policy design:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r3-cholesky-ridge-reset-policy-2026-06-29.md`

## Objective

Document and implement an opt-in Cholesky-ridge Contract E reset factorization
to avoid the eigensystem reset derivative blocker.  This is a local reset
repair.  It does not implement the full manual likelihood reverse scan and does
not unblock material Phase 3.

## Claude Review

Round 1 returned `VERDICT: REVISE`.

Required fixes:

- state the recentered particle map explicitly;
- make the ridge strictly positive with escalation-or-stop and realized-ridge
  reporting;
- keep Cholesky-ridge opt-in rather than default.

The policy was patched.  Round 2 returned:

```text
VERDICT: AGREE
```

A bounded implementation/documentation review of the exact R3 paths also
returned `VERDICT: AGREE`.  After that review, Codex added route-aware
diagnostic labels so Cholesky-diagonal diagnostics are not confused with
eigenvalue or rank diagnostics.  A bounded follow-up review of those labels and
the refreshed smoke artifact returned `VERDICT: AGREE`.

## Implementation

- Added `docs/benchmarks/contract_e_reset_tf.py`.
- Added opt-in `--contract-e-reset-factorization cholesky-ridge` to the Phase 2
  value and Phase 3 gradient diagnostics.
- Kept `eigh-support` as the default factorization.
- Added explicit ridge knobs:
  `--chol-ridge-rel`, `--chol-ridge-abs`, `--chol-ridge-escalation`,
  `--chol-ridge-max-attempts`.
- Added route-aware emitted diagnostic labels for the Cholesky-ridge path:
  `gap_diagnostic_label`, `tilde_positive_diagnostic_label`,
  `rank_margin_diagnostic_label`, and manifest-level
  `contract_e_diagnostic_labels`.
- Preserved the Phase 3 material blocker:
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.

## Local Evidence

Focused local checks:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_contract_e_cholesky_ridge_reset.py tests/test_contract_e_phase3_gradient_route_audit.py tests/test_contract_e_phase3_r2_reset_decision_artifacts.py -q
python -m py_compile docs/benchmarks/contract_e_reset_tf.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py
git diff --check -- docs/benchmarks/contract_e_reset_tf.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py docs/chapters/ch32c_entropic_ot_sinkhorn.tex docs/references.bib docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r3-cholesky-ridge-reset-policy-2026-06-29.md tests/test_contract_e_cholesky_ridge_reset.py tests/test_contract_e_phase3_r2_reset_decision_artifacts.py
```

Outcomes after the route-label guard was added:

- Focused tests passed: `12 passed`.
- Python compile checks passed.
- Diff whitespace check passed.

Tiny opt-in value smoke:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py --device-scope cpu --num-particles 16 --seed-count 10 --time-steps 10 --state-dims 1 --settings 0.5:2 --contract-e-reset-factorization cholesky-ridge --chol-ridge-rel 1e-4 --chol-ridge-abs 1e-5 --chol-ridge-max-attempts 3 --gate-mode smoke --no-xla --output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r3-cholesky-ridge-value-smoke-2026-06-29.json --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r3-cholesky-ridge-value-smoke-2026-06-29.md
```

Outcome: `smoke_passed`.

Key diagnostics for the Contract E arm:

| Diagnostic | Value |
| --- | ---: |
| covariance residual | `2.5171006564050913e-4` |
| mean residual | `4.470348358154297e-8` |
| condition proxy | `1.0` |
| max realized ridge | `4.332770549808629e-5` |
| max ridge attempts used | `1` |
| any ridge failure | `false` |

The fixture's material value gate remained `fail` in this tiny N=16 smoke
because the Contract E mean was just outside two MCSE of the Kalman value.  This
does not contradict the smoke outcome: smoke mode was used only to check finite
wiring, emitted diagnostics, and artifact generation.

Tiny opt-in gradient smoke was also attempted in smoke mode on CPU.  It failed
because the outer-tape diagnostic gradient was `nan` even though the value and
FD regression slopes were finite.  This is not a material failure of the new
manual route, because no full manual reverse scan exists yet.  It is useful
negative evidence against using TensorFlow autodiff through the Cholesky reset
as a shortcut.

## Decision Table

| Decision | Status | Evidence | Not concluded |
| --- | --- | --- | --- |
| Eigensystem reset factorization is not suitable for manual-gradient promotion. | Preserved | LaTeX explains eigenvector/repeated-eigenvalue and rank-floor issues. | Eigh route is not removed. |
| Cholesky-ridge reset is available as opt-in local repair. | Implemented | Helper, CLI flags, local tests, and value smoke. | Not default, not material. |
| Lambda policy is explicit. | Implemented | Ridge rel/abs/escalation/max-attempts and realized ridge are recorded. | No universal lambda is claimed. |
| Route-aware diagnostics are emitted. | Passed | JSON manifest/records label Cholesky diagonal diagnostics separately from legacy eig/rank field names. | Backward-compatible numeric names are not removed. |
| Hidden eigensystem/autodiff fallback in Cholesky helper is blocked. | Passed | Static tests reject `tf.linalg.eigh`, `GradientTape`, Jacobian, `ForwardAccumulator`. | Full manual VJP still not implemented. |
| Material Phase 3 remains blocked. | Passed | Material blocker remains in gradient script. | No LGSSM gradient correctness claim. |

## Nonclaims

R3 does not implement the full manual likelihood reverse scan, does not certify
LGSSM gradient correctness, does not promote Cholesky-ridge as default, does
not certify SIR/SV/nonlinear validity, and does not claim HMC or production
readiness.

## Next Step

The next justified step is a dedicated manual-VJP subplan for the Cholesky-ridge
reset helper: derive VJPs for weighted moments, Cholesky, triangular solve,
residual injection, and recentering; then check local same-map FD parity before
re-entering the full reverse-scan implementation.
