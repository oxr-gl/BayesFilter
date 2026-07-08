# Phase 2 Result: `zhaocui_fixed` Adapter Implementation

Date: 2026-07-05

Status: `PASSED_PHASE2_DEBUG_ADAPTER_ADMISSION`

## Phase Objective

Implement the narrow `zhaocui_fixed` SSL-LSTM adapter as a deterministic
fixed-HMC clean-room approximation with an analytic first-order score path and
honest route classification.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Phase 2 implement a deterministic, finite, analytic-score `zhaocui_fixed` SSL-LSTM adapter under the Phase 1 design? |
| Baseline/comparator | Phase 1 design ledger, Phase 2 protocol, Phase 3 SGQF/UKF adapter style, Zhao-Cui source anchors for replay/recentering vocabulary. |
| Primary pass criterion | New adapter module and tests pass deterministic, finite-score, finite-difference subset, metadata, schema, and forbidden-target-path checks. |
| Veto diagnostics | Autodiff target path, adaptive randomness, unclassified route metadata, non-finite value/score, finite-difference failure, invalid artifact schema, or source-faithful parity claim. |
| Explanatory diagnostics | Score norm, particle log-likelihood range, finite-difference residual, manifest fields, and recentering diagnostics. |
| Not concluded | HMC readiness, posterior correctness, source-faithful Zhao-Cui parity, method superiority, SGQF/UKF sufficiency, LEDH result, or default readiness. |
| Preserved artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-debug-value-score-artifact-2026-07-05.json` |

## Implementation Summary

Phase 2 added:

- `bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py`
- `tests/test_ssl_lstm_zhaocui_fixed_adapter.py`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-debug-value-score-artifact-2026-07-05.json`

The adapter uses fixed stateless reference samples, propagates them through the
existing SSL-LSTM TensorFlow transition/observation functions, accumulates a
deterministic log-mean-exp likelihood, and computes the score by manual
first-order chain rule through the existing hand-coded SSL-LSTM derivative
helpers.  Finite differences are used only in tests and the debug artifact.

## Source-Anchor And Classification Ledger

| Choice | Classification | Anchors / handling |
| --- | --- | --- |
| Sequential fixed replay vocabulary | `fixed_hmc_adaptation` | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43` |
| Fixed reapproximation/recentering vocabulary | `fixed_hmc_adaptation` | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:46-124` |
| Prior/transition/likelihood target split vocabulary | `fixed_hmc_adaptation` | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:132-135` |
| Weighted recentering diagnostic | `fixed_hmc_adaptation` | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24-47`; diagnostic only, not differentiated in target score. |
| Deterministic log-mean-exp replay likelihood | `extension_or_invention` | Clean-room BayesFilter fixed adaptation; not TTSIRT/KR parity. |
| SSL-LSTM derivatives | Local BayesFilter substrate | Existing TensorFlow hand derivatives from `ssl_lstm_sgqf_ukf_adapters.py`. |

## Debug Artifact Summary

| Diagnostic | Value | Role |
| --- | ---: | --- |
| Log likelihood | `-1.3969803149874547` | adapter-admission diagnostic |
| Score finite | `true` | promotion veto |
| Score norm | `1.6251569331205424` | explanatory |
| Finite-difference max abs error | `8.616574120878795e-11` | promotion veto for adapter admission |
| Reference sample count | `9` | fixed branch metadata |
| Effective sample size | `7.719831264772175` | explanatory |

The finite-difference subset checked representative LSTM gate, latent map,
observation map, initial law, process-noise, and observation-noise coordinates:
`0, 4, 8, 12, 13, 14, 15, 16, 19, 22`.

## Required Checks Run

| Check | Result |
| --- | --- |
| `python -m compileall -q bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py tests/test_ssl_lstm_zhaocui_fixed_adapter.py` | Passed |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_zhaocui_fixed_adapter.py` | Passed: `7 passed in 3.49s` |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_protocol.py` | Passed: `11 passed in 1.94s` |
| `rg -n 'GradientTape\|tf\\.py_function\|np\\.\|numpy' bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py` | Passed: no hits |
| `git diff --check` | Passed |

CPU-only note: these were deliberate CPU-hidden debug/reference checks with
`CUDA_VISIBLE_DEVICES=-1`; they are not production GPU/XLA evidence.

## Skeptical Plan Audit

| Risk | Finding |
| --- | --- |
| Wrong baseline | Passed: Phase 2 used the shared SSL-LSTM protocol and existing SGQF/UKF adapter style as comparator substrate, not a one-off promotion benchmark. |
| Proxy metrics promoted | Passed: finite differences and score finiteness are adapter-admission screens only. |
| Missing stop conditions | Passed: target autodiff, adaptive randomness, nonfinite score, schema failure, and source-faithfulness overclaim remain vetoes. |
| Unfair comparison | Passed: no ranking against SGQF/UKF is made. |
| Hidden assumptions | Recorded: deterministic log-mean-exp replay is `extension_or_invention`, not source-faithful Zhao-Cui parity. |
| Stale context | Passed: source anchors and local protocol/derivative files were reopened before implementation. |
| Environment mismatch | Recorded: CPU-hidden debug checks only; no GPU/default-readiness claim. |
| Artifact mismatch | Passed: JSON debug artifact validates against the SSL-LSTM value/score schema. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `f98be292faabf3d1728f876ad211a70ac1ddf98c` |
| Worktree | Dirty before/during run; unrelated existing changes preserved. |
| Environment | Managed Codex shell; TensorFlow import available. |
| CPU/GPU status | CPU-hidden debug/reference checks, `CUDA_VISIBLE_DEVICES=-1`. |
| Random seeds | Stateless manifest seeds `(20260705, 41)` and `(20260705, 43)`. |
| Wall time | Focused tests under 5 seconds each in this session. |
| Plan file | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-adapter-implementation-subplan-2026-07-05.md` |
| Result file | This file. |
| Output artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-debug-value-score-artifact-2026-07-05.json` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Admit `zhaocui_fixed` to Phase 3 schema/test gate | Passed for tiny CPU-hidden debug fixture | No Phase 2 veto fired | Whether shared benchmark and launch-smoke integration remain clean when `zhaocui_fixed` is added to those harnesses | Execute Phase 3 focused schema/test gate | No HMC convergence, posterior correctness, source-faithful parity, method superiority, LEDH result, default readiness, or GPU/XLA production readiness |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | No target autodiff, adaptive randomness, nonfinite score, invalid schema, or forbidden source scan hit found in Phase 2. |
| Statistically supported ranking | Not applicable; no stochastic method ranking is attempted. |
| Descriptive-only differences | Score norm, particle log-likelihood range, and effective sample size are explanatory only. |
| Default-readiness | Not checked and not claimed. |
| Next evidence needed | Phase 3 schema/tests, then Phase 4 shared benchmark and launch-smoke integration under the master program. |

## Post-Run Red-Team Note

Strongest alternative explanation: the tiny fixture may be too small to expose
shape, branch, or numerical weaknesses that will appear in the shared benchmark
or launch smoke.

Result that would overturn this Phase 2 admission: a reviewed check finds
target-path autodiff/NumPy, a hidden adaptive branch, artifact schema mismatch,
or finite-difference failure on the Phase 3 focused expansion.

Weakest part of the evidence: Phase 2 validates a clean-room fixed replay on a
small CPU-hidden debug fixture only.
