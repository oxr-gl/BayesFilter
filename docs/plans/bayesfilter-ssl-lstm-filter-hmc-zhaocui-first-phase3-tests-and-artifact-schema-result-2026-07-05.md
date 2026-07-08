# Phase 3 Result: Focused Tests And Artifact Schema

Date: 2026-07-05

Status: `PASSED_PHASE3_FOCUSED_SCHEMA_TEST_GATE`

## Phase Objective

Check that the Phase 2 `zhaocui_fixed` adapter and debug value/score artifact
survive the focused test/schema gate before any shared benchmark or launch-smoke
integration.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the focused test/schema surface admit `zhaocui_fixed` as a Phase 3 candidate for later shared benchmark integration? |
| Baseline/comparator | Phase 2 adapter/result artifact, SSL-LSTM protocol validator, SGQF/UKF focused tests, and forbidden target-path scan. |
| Primary pass criterion | Focused adapter tests, protocol tests, schema validation, compile check, and forbidden-source scan pass together. |
| Veto diagnostics | Test failure, invalid schema, nonfinite score, finite-difference mismatch, target autodiff, NumPy implementation logic, adaptive randomness, or source-faithful parity claim. |
| Explanatory diagnostics | Runtime, finite-difference residual, score norm, recenter frame, and protocol signature stability. |
| Not concluded | Shared benchmark pass, HMC launch pass, posterior correctness, method superiority, source-faithful parity, LEDH result, GPU/XLA production readiness, or default readiness. |

## Checks Run

| Check | Result |
| --- | --- |
| `python -m compileall -q bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py tests/test_ssl_lstm_zhaocui_fixed_adapter.py` | Passed |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_zhaocui_fixed_adapter.py tests/test_ssl_lstm_protocol.py` | Passed: `18 passed in 3.57s` |
| `rg -n 'GradientTape\|tf\\.py_function\|np\\.\|numpy' bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py` | Passed: no hits |
| JSON schema reload using `validate_ssl_lstm_value_score_artifact` | Passed: `zhaocui_fixed analytic_first_order_zhaocui_fixed 8.616574120878795e-11` |
| Forbidden-claims scan over Phase 2/3 artifacts and adapter/test files | Passed: hits were nonclaims, veto wording, or tests asserting nonclaims. |

CPU-only note: all Phase 3 commands were deliberate CPU-hidden debug/reference
checks. They are not GPU/XLA production evidence.

## Artifact Summary

| Artifact | Status |
| --- | --- |
| `bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py` | Focused test/schema gate passed. |
| `tests/test_ssl_lstm_zhaocui_fixed_adapter.py` | Focused tests passed. |
| `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-debug-value-score-artifact-2026-07-05.json` | Schema reload passed. |

## Skeptical Plan Audit

| Risk | Finding |
| --- | --- |
| Wrong baseline | Passed: the gate checked focused adapter/schema readiness, not a custom benchmark. |
| Proxy metrics promoted | Passed: finite-difference residual and score finiteness remain adapter-admission screens. |
| Missing stop conditions | Passed: schema, nonfinite score, target autodiff, adaptive randomness, and unsupported claims remained vetoes. |
| Unfair comparison | Passed: no SGQF/UKF ranking is made. |
| Hidden assumptions | Recorded: Phase 3 does not prove the fixed replay approximation is scientifically sufficient. |
| Environment mismatch | Recorded: CPU-hidden debug checks only; no GPU/default-readiness claim. |
| Artifact mismatch | Passed: the saved Phase 2 JSON artifact was reloaded and validated. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Admit `zhaocui_fixed` to Phase 4 integration | Passed focused schema/test gate | No Phase 3 veto fired | Shared benchmark and launch-smoke harnesses still list `zhaocui_fixed` as blocked and must be updated carefully | Execute Phase 4 shared benchmark and launch-smoke integration | No shared benchmark pass yet, HMC launch pass, posterior correctness, method superiority, source-faithful parity, LEDH result, GPU/XLA production readiness, or default readiness |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | No focused test/schema hard veto fired. |
| Statistically supported ranking | Not applicable. |
| Descriptive-only differences | Runtime and residual summaries are descriptive. |
| Default-readiness | Not checked and not claimed. |
| Next evidence needed | Phase 4 integration into shared benchmark and launch-smoke harnesses. |

## Post-Run Red-Team Note

Strongest alternative explanation: focused tests may still miss harness-level
assumptions in Phase 6/7 benchmark scripts, especially admitted/blocked filter
lists and target-scope provenance fields.

Result that would overturn this gate: Phase 4 discovers that admitting
`zhaocui_fixed` requires changing benchmark semantics, target authority,
default policy, or HMC interpretation criteria.
