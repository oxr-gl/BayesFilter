# Phase R4 Subplan: Cholesky-Ridge Reset Manual VJP

Date: 2026-06-29

Status: `REVIEWED_EXECUTED_LOCAL_PASS`

## Phase Objective

Implement and test a local manual VJP for the opt-in Contract E
Cholesky-ridge reset map introduced in R3.  R4 is a local reset-map phase: it
does not wire the full filtering reverse scan, does not run material Phase 3,
does not run GPU/XLA jobs, and does not claim LGSSM/SIR/SV/HMC correctness.

The local map is

```text
(post_flow, weights, matrix, residual_noise) -> y_star
```

with `rho` and the realized ridge treated as fixed scalar/tensor inputs on the
tested smooth chart.

## Entry Conditions Inherited From R3

- R3 documented the eigensystem derivative problem and the Cholesky-ridge
  alternative in `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`.
- R3 implemented `contract_e_cholesky_ridge_reset` in
  `docs/benchmarks/contract_e_reset_tf.py`.
- R3 kept `cholesky-ridge` opt-in and kept `eigh-support` as the default
  factorization.
- R3 local checks passed, and the tiny value smoke emitted finite reset
  diagnostics.
- The tiny gradient smoke failed because the outer TensorFlow autodiff
  diagnostic produced NaN gradients, reinforcing that the reset must not be
  promoted through hidden generic autodiff.
- The material blocker remains:
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.

## Required Artifacts

- An R4 reset-VJP implementation in `docs/benchmarks/contract_e_reset_tf.py`.
- A deterministic fixed-ridge local fixture test file or extension to
  `tests/test_contract_e_cholesky_ridge_reset.py`.
- Local same-map finite-difference parity tests for the scalar objective
  `sum(y_star * upstream)` with perturbations of:
  - `post_flow`;
  - `weights` on a small unconstrained softmax chart;
  - `matrix`;
  - `residual_noise`.
- Per-perturbation fixed-chart records asserting that center, `+h`, and `-h`
  evaluations use identical realized ridge values and identical ridge-attempt
  counts.  Any branch change invalidates that finite-difference comparison.
- Static tests proving the manual VJP helper itself contains no
  generic autodiff API/wrapper (`tf.GradientTape`, `tf.gradients`,
  `tf.compat.v1.gradients`, Jacobian, `batch_jacobian`, `ForwardAccumulator`,
  or local aliases/wrappers) and no `tf.linalg.eigh`.
- Updated R4 result / close record under `docs/plans`.
- If R4 passes, an R5 handoff subplan for integrating the reset VJP into the
  manual likelihood reverse scan.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- Bounded Claude read-only review of this subplan before implementation.
- Focused local CPU-hidden tests:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_contract_e_cholesky_ridge_reset.py -q
python -m py_compile docs/benchmarks/contract_e_reset_tf.py
git diff --check -- docs/benchmarks/contract_e_reset_tf.py tests/test_contract_e_cholesky_ridge_reset.py docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r4-cholesky-ridge-reset-vjp-subplan-2026-06-29.md
```

- Bounded Claude read-only implementation review after local checks.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the opt-in Cholesky-ridge reset map have a local manual VJP that matches finite differences on a fixed smooth chart? |
| Baseline/comparator | Same-map central finite differences of `sum(y_star * upstream)` on deterministic tiny fixtures.  Tiny TensorFlow autodiff may be used only as a local test oracle, not as implementation. |
| Primary pass criterion | Manual VJP directional derivatives match central finite differences for all four input groups within the frozen tolerances, every FD comparison records identical center/plus/minus realized ridge and attempt count, and static audits find no hidden autodiff/eigensystem fallback in the helper. |
| Veto diagnostics | Nonfinite reset output, nonfinite VJP, fixed-ridge Cholesky failure, any center/plus/minus ridge or attempt-count branch change treated as differentiable, hidden generic autodiff API/wrapper or eigensystem fallback in the helper, or weakening of the material blocker. |
| Explanatory diagnostics | Covariance residual, mean residual, Cholesky diagonal/condition proxy, directional derivative magnitudes, and finite-difference step sensitivity. |
| Not concluded | Full filtering reverse-scan correctness, LGSSM gradient correctness, SIR/SV correctness, HMC readiness, production readiness, or validity across ridge branch changes. |
| Artifact preserving result | R4 result note and focused test output. |

## Skeptical Plan Audit

- Wrong baseline risk: comparing only to TensorFlow autodiff would recreate the
  failure mode.  R4 uses same-map finite differences as the primary comparator;
  local autodiff, if used, is only a secondary oracle inside tests.
- Proxy metric risk: covariance residual is explanatory only.  It does not
  promote the VJP.
- Missing stop condition risk: if finite-difference parity fails, R4 stops with
  a blocker instead of wiring into the full reverse scan.
- Hidden assumption risk: the ridge is fixed on the local chart.  R4 does not
  differentiate through `max`, escalation, or branch selection.  Tests must
  assert and record identical realized ridge and attempt counts for center,
  `+h`, and `-h` finite-difference probes.
- Environment mismatch risk: all checks are CPU-hidden local tests.  GPU/XLA
  behavior remains out of scope.
- Artifact relevance risk: local reset-map parity answers only whether this
  primitive is differentiable as implemented.  It does not answer the full
  LGSSM gradient question.

Audit outcome before implementation: `PASS_WITH_SCOPE_LIMITS`.

## Forbidden Claims And Actions

- Do not remove or weaken
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.
- Do not run material Phase 3, full-filter FD, SIR, SV, GPU, or XLA jobs in R4.
- Do not claim gradient correctness for the full filter from local reset-map
  parity.
- Do not differentiate through ridge branch selection, `max`, or escalation.
- Do not use generic TensorFlow autodiff APIs or wrappers as the implementation
  path, including aliased `GradientTape`, `tf.gradients`,
  `tf.compat.v1.gradients`, Jacobian, `batch_jacobian`, or
  `ForwardAccumulator`.
- Do not add NumPy-backed algorithmic implementation code; NumPy may appear
  only in test assertions/reporting if needed.

## Exact Next-Phase Handoff Conditions

Advance to R5 only if:

- local finite-difference parity passes for all declared input groups;
- fixed-chart records show identical center/plus/minus realized ridge and
  attempt counts for every accepted finite-difference comparison;
- static hidden-autodiff/eigh checks pass;
- `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py` still
  contains `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`, and no
  R4 artifact claims reverse-scan integration or material Phase 3 readiness;
- the R4 close record is written; and
- bounded Claude implementation review returns `VERDICT: AGREE` or all
  fixable findings are patched and re-reviewed.

R5 may then plan integration of the local reset VJP into the manual likelihood
reverse scan.  R5 still must not run material Phase 3 until that integration
has its own reviewed subplan and checks.

## Stop Conditions

Stop and write an R4 blocker result if any of the following occur:

- local finite-difference parity fails after one focused repair attempt;
- the fixed-ridge Cholesky chart is not stable on the fixture;
- any accepted finite-difference comparison changes realized ridge or attempt
  count across center, `+h`, and `-h`;
- the manual VJP requires differentiating through branch selection;
- a hidden generic autodiff or eigensystem fallback is needed to pass tests;
- Claude review does not converge after five rounds for the same blocker; or
- any artifact would overclaim beyond local reset-map parity.
