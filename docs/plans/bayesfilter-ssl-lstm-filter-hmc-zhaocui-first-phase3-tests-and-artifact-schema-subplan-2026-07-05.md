# Phase 3 Subplan: Focused Tests And Artifact Schema

Date: 2026-07-05

Status: `READY_FOR_EXECUTION`

## Phase Objective

Promote the Phase 2 `zhaocui_fixed` debug adapter from local implementation
checks to a focused schema/test gate, without entering the shared benchmark,
HMC launch smoke, GPU evidence, or default-readiness claims.

## Entry Conditions

- Phase 2 result exists and records passing local implementation checks.
- `zhaocui_fixed` has a finite deterministic debug value/score artifact.
- The adapter remains a clean-room fixed adaptation, not source-faithful
  SSL-LSTM Zhao-Cui parity.
- LEDH remains out of scope.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the focused test/schema surface admit `zhaocui_fixed` as a Phase 3 candidate for later shared benchmark integration? |
| Baseline/comparator | Phase 2 adapter/result artifact, SSL-LSTM protocol validator, SGQF/UKF focused tests, and forbidden target-path scan. |
| Primary pass criterion | Focused adapter tests, protocol tests, schema validation, compile check, and forbidden-source scan pass together. |
| Veto diagnostics | Test failure, invalid schema, nonfinite score, finite-difference mismatch, target autodiff, NumPy implementation logic, adaptive randomness, or source-faithful parity claim. |
| Explanatory diagnostics | Runtime, finite-difference residual, score norm, recenter frame, and protocol signature stability. |
| Not concluded | Shared benchmark pass, HMC launch pass, posterior correctness, method superiority, source-faithful parity, LEDH result, GPU/XLA production readiness, or default readiness. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase3-tests-and-artifact-schema-result-2026-07-05.md` |

## Planned Checks

- `python -m compileall -q bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py tests/test_ssl_lstm_zhaocui_fixed_adapter.py`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_zhaocui_fixed_adapter.py tests/test_ssl_lstm_protocol.py`
- `rg -n 'GradientTape|tf\\.py_function|np\\.|numpy' bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py`
- JSON schema revalidation by loading
  `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-debug-value-score-artifact-2026-07-05.json`
  and calling `validate_ssl_lstm_value_score_artifact` with a reconstructed
  `zhaocui_fixed` protocol.
- Forbidden-claims scan over Phase 2/3 Zhao-Cui-first artifacts, treating hits
  in nonclaims/prohibitions as allowed and unsupported positive claims as vetoes.

## Skeptical Plan Audit

| Risk | Pre-run finding |
| --- | --- |
| Wrong baseline | Passed: Phase 3 checks the focused adapter/schema gate, not a custom benchmark. |
| Proxy metrics promoted | Passed: finite differences and score finiteness are admission screens only. |
| Missing stop conditions | Passed: schema, nonfinite score, target autodiff, adaptive randomness, and unsupported claims are vetoes. |
| Unfair comparison | Passed: no ranking against SGQF/UKF is made. |
| Hidden assumptions | Recorded: Phase 3 does not prove the fixed replay approximation is scientifically sufficient. |
| Stale context | Phase 2 result and code are current in this session. |
| Environment mismatch | CPU-hidden debug checks only; no GPU/default claim. |
| Artifact mismatch | Planned schema reload directly checks the Phase 2 JSON artifact. |

## Stop Conditions

Stop and write a blocker result if any planned check fails in a way that cannot
be repaired without target-path autodiff, NumPy target implementation logic,
adaptive branch selection, LEDH implementation, public API/default-policy
change, package install, network fetch, or an unsupported source-faithfulness
claim.
