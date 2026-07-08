# Phase 2 Result: Shared Value/Score Protocol And Diagnostics

Date: 2026-07-04

Status: `PASSED_WITH_USER_DIRECTED_CODEX_ONLY_CONTINUATION`

## Phase Objective

Define and implement the shared TensorFlow/TFP value-and-score adapter protocol
that SSL-LSTM filter candidates must satisfy before HMC or benchmarking.

## Entry Conditions

Phase 1 passed with a Gaussian additive SSL-LSTM target, augmented state
`[z, a, c]`, HMC-over-parameters estimand, invariant metrics, and an exact
handoff requiring a shared adapter protocol before filter-specific work.

## Implementation Summary

Added `bayesfilter/nonlinear/ssl_lstm_protocol.py`.

The module is a protocol layer, not a filter implementation. It provides:

- `SSLLSTMStaticConfig`, which maps Phase 1 dimensions into
  `NonlinearSSMStaticShape` and deterministic parameter names.
- `SSLLSTMFilterProtocolSpec`, which declares the required gradient path,
  likelihood term, seed policy, and branch/randomness policy for each candidate.
- `SSLLSTMAdapterProtocol`, which binds the SSL-LSTM-specific filter metadata to
  the existing `NonlinearSSMAdapterContract`.
- `build_expected_ssl_lstm_adapter_protocol(...)`, which builds expected
  protocol metadata for later adapter implementations.
- `validate_ssl_lstm_adapter_protocol(...)`, which fails closed on unsupported
  score authority, wrong gradient path, missing evidence metadata, or mismatched
  seed/branch policy.
- `ssl_lstm_value_score_artifact_schema()` and
  `validate_ssl_lstm_value_score_artifact(...)`, which define and validate the
  JSON/Markdown value-score artifact fields needed by later phases.

Added `tests/test_ssl_lstm_protocol.py`.

## Candidate Filter Protocol

| Filter | Required value/score authority | Required gradient path | Seed policy | Branch/randomness policy | Likelihood term |
| --- | --- | --- | --- | --- | --- |
| `fixed_sgqf` | `graph_native` | `analytic_first_order_fixed_sgqf` | `not_used` | `fixed_sparse_grid_branch_manifest` | `tf_fixed_sgqf_score` |
| `svd_ukf` | `graph_native` | `analytic_first_order_svd_ukf` | `not_used` | `deterministic_sigma_point_rule` | `tf_svd_ukf_score` |
| `zhaocui_fixed` | `graph_native` | `analytic_first_order_zhaocui_fixed` | `stateless_required` | `fixed_hmc_adaptation_manifest` | `zhaocui_fixed_analytic_score` |
| `ledh_streaming_ot` | `graph_native` | `manual_vjp_streaming_ot` | `stateless_required` | `streaming_ot_manual_vjp_fixed_seed_manifest` | `ledh_streaming_ot_manual_vjp_score` |

Target paths explicitly reject:

- `gradient_tape_fallback`;
- `reviewed_gradient_tape_xla_exception`;
- `reviewed_tf_py_function_finite_reject_bridge`;
- `debug_only`;
- `unavailable`;
- wrong gradient path for the filter lane;
- missing evidence path, target scope, or nonclaims.

This is stricter than the generic `ValueScoreCapability` contract because the
user specifically required analytical gradients for SGQF/UKF/Zhao-Cui and manual
VJP for LEDH.

## Artifact Schema

The value/score artifact schema version is
`ssl_lstm.filter_hmc.value_score.v1`.

Required fields:

- `schema_version`;
- `artifact_role`;
- `target_scope`;
- `filter_name`;
- `gradient_path`;
- `value_score_authority`;
- `compile_mode`;
- `jit_compile`;
- `device`;
- `tf32_enabled`;
- `seed_policy`;
- `branch_or_randomness_policy`;
- `log_likelihood`;
- `score`;
- `score_finite`;
- `finite_difference_check`;
- `diagnostic_roles`;
- `nonclaims`.

Diagnostic role rules:

| Diagnostic | Required role |
| --- | --- |
| `score_finite` | hard/promotion veto |
| `finite_difference_check` | `promotion_veto_for_adapter_admission` or explicitly explanatory |
| runtime and score norm | explanatory |

Target artifacts require `compile_mode == "xla"` and `jit_compile == true`.
Debug/reference artifacts may use a weaker role only when labeled
`debug_reference`; they cannot be used as Phase 7 HMC target evidence.

## Required Checks Run

| Check | Command | Result |
| --- | --- | --- |
| Focused SSL-LSTM protocol tests | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_protocol.py` | Passed: 11 tests |
| Compile check | `python -m compileall -q bayesfilter/nonlinear/ssl_lstm_protocol.py tests/test_ssl_lstm_protocol.py` | Passed |
| Existing nonlinear contract plus SSL-LSTM protocol | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nonlinear_ssm_phase1_contract.py tests/test_ssl_lstm_protocol.py` | Passed: 19 tests |
| Existing runtime authority checks | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_common_inference_runtime_contracts.py::test_value_score_authority_fails_closed_for_xla_and_unknown_labels tests/test_common_inference_runtime_contracts.py::test_reviewed_gradient_tape_exception_must_be_scoped tests/test_common_inference_runtime_contracts.py::test_full_chain_xla_diagnostic_authority_requires_scoped_target_authority` | Passed: 3 tests |
| Diff whitespace hygiene | `git diff --check -- bayesfilter/nonlinear/ssl_lstm_protocol.py tests/test_ssl_lstm_protocol.py docs/plans/bayesfilter-ssl-lstm-filter-hmc-visible-execution-ledger-2026-07-04.md` | Passed |

All runtime checks were CPU-hidden debug/protocol checks with
`CUDA_VISIBLE_DEVICES=-1`. They are not production GPU/XLA evidence.

## Skeptical Plan Audit

| Risk | Phase 2 finding |
| --- | --- |
| Wrong baseline | The implementation builds on existing `NonlinearSSMAdapterContract` and does not create a parallel HMC target contract. |
| Proxy metrics promoted | No numerical filter metric is promoted; tests are protocol checks only. |
| Missing stop conditions | The result is marked pending review decision because Phase 2 originally required material Claude review. |
| Unfair comparison | The same protocol covers all four candidate filters with explicit lane-specific gradient paths. |
| Hidden assumptions | Diagonal covariance mode is admitted for Phase 2; dense covariance is explicitly rejected until reviewed. |
| Stale context | Phase 2 used Phase 1 target dimensions and existing local contract tests. |
| Environment mismatch | CPU-hidden tests are labeled debug/protocol checks only. |
| Artifact mismatch | The artifact schema is declared, and tests validate missing/JIT/nonfinite failure cases. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 2 local protocol gate | Passed locally | No local contract/test veto fired | Material external review unresolved after Phase 0 Claude export denial | Ask user for Phase 2 review decision or Codex-only exception | No filter implementation, no filter accuracy, no HMC convergence, no SSL-LSTM estimation success |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Protocol rejects unsupported score authority, wrong gradient path, missing metadata, no JIT target artifact, and nonfinite score flag |
| Statistically supported ranking | Not applicable |
| Descriptive-only differences | Not applicable |
| Default-readiness | Not checked and not claimed |
| Next evidence needed | Phase 2 material review decision, then Phase 3 SGQF/UKF analytic adapter subplan execution |

## Phase 3 Subplan Review

Phase 3 subplan remains structurally consistent with this result. Its handoff
must use:

- `fixed_sgqf` with `analytic_first_order_fixed_sgqf`;
- `svd_ukf` with `analytic_first_order_svd_ukf`;
- the artifact schema `ssl_lstm.filter_hmc.value_score.v1`;
- no automatic differentiation target score path;
- no SGQF/UKF sufficiency claim before Phase 6 shared benchmark.

## Review Boundary

Phase 2 local checks passed, but the subplan required Claude read-only review
for the protocol and authority labels. Phase 0 established that Claude export is
blocked by approval policy unless the user explicitly authorizes the export risk
or grants a Codex-only exception.

No Claude review was attempted in Phase 2.

After the handoff identified this boundary, the user directed Codex to
"continue with the runbook." Codex interprets that as authorization to continue
locally without external Claude export for this phase only. This is not a
general waiver for later material review gates and does not create a Claude
review artifact.

## Phase 2 Gate Status

`PASSED_WITH_USER_DIRECTED_CODEX_ONLY_CONTINUATION`

Phase 3 may start under the same no-export boundary. Phase 3 must still write a
dedicated subplan/result pair, run local checks, and stop before any external
Claude export or broader scientific claim unless explicitly authorized.
