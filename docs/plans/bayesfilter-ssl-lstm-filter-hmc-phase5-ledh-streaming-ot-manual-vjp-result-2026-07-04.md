# Phase 5 Result: LEDH Streaming-OT Manual VJP Adapter

Date: 2026-07-04

Status: `BLOCKED_MANUAL_VJP_IMPL_UNAVAILABLE`

## Phase Objective

Build or repair the LEDH streaming-OT adapter so the target gradient uses a
manual VJP path through the streaming transport operations, not ordinary
automatic differentiation through the transport solve.

## Entry Conditions

- Phase 2 protocol remains active.
- Phase 3 admitted fixed SGQF and SVD-UKF locally under analytic score checks.
- Phase 4 is blocked because the repository does not contain an SSL-LSTM
  Zhao-Cui fixed-variant adapter to wire.
- Phase 4 blocker review fell back to a separate Codex read-only review on the
  same bounded bundle and returned `VERDICT: AGREE`.

## Skeptical Audit

| Risk | Finding |
| --- | --- |
| Wrong baseline | The relevant local LEDH streaming route is `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`, not the Phase 3 SGQF/UKF adapter module. |
| Proxy promotion | The protocol label `manual_vjp_streaming_ot` exists, but a metadata label is not an implemented manual VJP. |
| Missing stop conditions | The Phase 5 subplan forbids existing GradientTape score helpers as final target evidence. |
| Unfair comparison | Admitting LEDH through the existing GradientTape wrapper would give LEDH a different target-gradient authority than SGQF/UKF. |
| Hidden assumptions | The streaming value recursion exists, but the exposed value/score helper differentiates it with `tf.GradientTape`. |
| Stale context | Local source inspection found no `manual_vjp` implementation in the LEDH streaming path. |
| Environment mismatch | This is a code-shape blocker, not a GPU/runtime blocker. |
| Artifact mismatch | A blocker result is the correct artifact because no manual VJP adapter evidence can be produced from the current code. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can LEDH streaming OT expose a deterministic manual-VJP value/score adapter for SSL-LSTM? |
| Baseline/comparator | Phase 2 protocol and current LEDH streaming code inventory; finite differences are independent diagnostics only. |
| Primary pass criterion | Manual VJP adapter passes contract tests, finite-difference diagnostics, and streaming/chunking checks on tiny fixtures. |
| Veto diagnostics | Target path uses ordinary autodiff through transport solve, non-finite VJP, chunking mismatch beyond tolerance, disconnected cotangent, or missing artifact metadata. |
| Explanatory diagnostics | Runtime, memory/chunk counts, transport residuals, score residuals, and compile mode. |
| Not concluded | Dense Sinkhorn equivalence, posterior correctness, HMC success, or method ranking. |
| Result artifact | This file |

## Source Inventory

| Path | Evidence |
| --- | --- |
| `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py` | Defines `streaming_batched_ledh_pfpf_ot_value_core_tf`, the streaming value recursion. |
| `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py` | Defines `streaming_batched_ledh_pfpf_ot_value_and_score_tf`, whose current score path opens `tf.GradientTape()`. |
| `tests/test_experimental_batched_ledh_pfpf_ot_tf.py` | Existing test explicitly asserts `"GradientTape" in source` for the value/score helper. |
| `bayesfilter/nonlinear/ssl_lstm_protocol.py` | Declares `ledh_streaming_ot` as requiring `manual_vjp_streaming_ot`, but this is protocol metadata only. |

## Result

Phase 5 is blocked because the repository does not currently expose the
requested manual VJP streaming-OT score path for SSL-LSTM. The current LEDH
streaming value/score helper uses `tf.GradientTape`, which is explicitly
forbidden as the final target evidence for this master program.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 5 LEDH admission | Failed | Target path uses ordinary autodiff through the streaming transport solve | Whether a manual VJP can be built without a larger transport-core redesign | Record LEDH as blocked and refresh Phase 6 around admitted SGQF/UKF plus blocked Zhao-Cui/LEDH statuses | No LEDH HMC readiness, no posterior correctness, no method ranking |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Blocked by unavailable manual VJP implementation |
| Statistically supported ranking | Not applicable |
| Descriptive-only differences | Existing GradientTape helper is descriptive source inventory only |
| Default-readiness | Not checked and not claimed |
| Next evidence needed | A real manual VJP design/implementation or an explicit human-approved scope change |

## Forbidden Claims And Actions

- Do not claim LEDH streaming OT is admitted to HMC under this runbook.
- Do not use the existing GradientTape helper as final target evidence.
- Do not claim dense Sinkhorn equivalence, posterior correctness, HMC success,
  or method ranking.
- Do not treat this blocker as evidence against SGQF/UKF, which remain
  separately admitted to the shared benchmark gate.

## Next-Phase Handoff

Phase 6 may start as benchmark-harness planning only after it records candidate
statuses explicitly:

- `fixed_sgqf`: locally admitted for later shared benchmark.
- `svd_ukf`: locally admitted for later shared benchmark.
- `zhaocui_fixed`: blocked by missing SSL-LSTM Zhao-Cui adapter.
- `ledh_streaming_ot`: blocked by missing manual VJP streaming-OT score path.
