# Manual Adjoint Phase 8 Result: Closeout And Code-Doc Audit

Date: 2026-06-22

Status: MANUAL_ADJOINT_LOCAL_ROUTE_PASSED_P82_WIRING_BLOCKED

## Evidence Contract

| Field | Result |
|---|---|
| Question | Are the manual-adjoint artifacts, code, tests, docs, limitations, and downstream handoff internally consistent? |
| Baseline/comparator | M0-M7 phase results, implementation diffs, focused tests, and P82 downstream correction artifacts. |
| Primary criterion | Passed for closeout: artifacts record supported/unsupported modes, tests actually run, review trail, nonclaims, and downstream blocker. |
| Veto diagnostics | No unsupported P82-ready claim; no raw full-AD N10000 route reintroduced; no HMC/default/posterior/production claim; no Zhao-Cui source-faithfulness claim; final focused tests and diff hygiene passed. |
| Explanatory diagnostics | Test list, review trail, code paths, handoff path, and limitation table below. |
| Not concluded | P82 FD agreement, N10000 feasibility, GPU/TF32 success, HMC/NUTS readiness, posterior correctness, exact likelihood correctness, default-gradient readiness, production readiness, scientific superiority, or Zhao-Cui source-faithfulness. |

## Final Status

The manual-adjoint program is closed as a local route success with a downstream
P82 wiring blocker:

```text
MANUAL_ADJOINT_LOCAL_ROUTE_PASSED_P82_WIRING_BLOCKED
```

M6 produced reviewed local evidence for:

```text
manual_streaming_finite_sinkhorn_stopped_scale_keys
```

M7 blocked P82 return because the current P82 SIR d18 benchmark path does not
expose or forward `transport_gradient_mode`; the streaming value core still
calls the batched transport core with `transport_gradient_mode="raw"`.

## Supported Local Route

Supported only in the experimental batched transport core:

- `transport_gradient_mode="manual_streaming_finite_sinkhorn_stopped_scale_keys"`;
- `transport_plan_mode="streaming"`;
- `transport_ad_mode="stabilized"`;
- scalar `epsilon`;
- no warmstart;
- static positive finite Sinkhorn iterations.

Unsupported:

- governed raw/full AD N10000 route;
- dense plan with manual streaming route;
- warmstart with manual streaming route;
- `transport_ad_mode="full"` for manual streaming;
- vector epsilon;
- default/public route promotion.

## Final Checks

Commands run:

```bash
git diff --check -- AGENTS.md memory.md experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py
rg -n "P82_RETURN_READY|MANUAL_ADJOINT_READY_FOR_P82|P82 has passed|production readiness|default-gradient readiness|HMC readiness|posterior correctness|Zhao-Cui source-faithful|source-faithful" docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_m6_manual_streaming_value_and_score_tiny_opt_in_smoke tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_m5_manual_dense_value_and_score_tiny_opt_in_smoke tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_phase4_value_and_score_source_has_no_numpy_rng_or_runtime_ess_branch tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_phase3_value_core_source_has_no_numpy_rng_or_runtime_ess_branch -q
```

Observed results:

- diff hygiene: passed;
- `py_compile`: passed;
- unsupported-claim scan: hits were nonclaim/forbidden-claim language or
  historical option names, not active readiness claims;
- focused pytest bundle: `23 passed in 51.89s`.

## Review Trail

- M1 derivation contract: Claude R2 `VERDICT: AGREE`.
- M2 primitive VJP parity: Claude R1 `VERDICT: AGREE`.
- M3 dense custom-gradient prototype: Claude R2 `VERDICT: AGREE`.
- M4 loop-adjoint integration design: Claude R2 `VERDICT: AGREE`.
- M5 opt-in tiny integration: Claude R1 `VERDICT: AGREE`.
- M6 streaming memory route: Claude R3 one-path `VERDICT: AGREE`.
- M7 P82 handoff blocker: Claude R2 one-path `VERDICT: AGREE`.

The one-path Claude review rule was added to:

- `AGENTS.md`;
- `memory.md`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Close manual-adjoint program as local route passed, P82 wiring blocked | Passed for M8 closeout | No active unsupported claim or forbidden run observed | Whether the manual streaming route remains feasible after wiring into the full SIR d18 benchmark path | Start a separate P82 wiring subplan for `transport_gradient_mode` propagation | No P82 FD agreement, N10000 feasibility, GPU evidence, HMC/default/posterior readiness, or production readiness |

## Required Next Action

Create a narrow P82 wiring subplan.  It should:

1. Add or supply `transport_gradient_mode` through
   `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`,
   `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`, and
   `streaming_batched_ledh_pfpf_ot_value_core_tf`.
2. Ensure metadata records
   `manual_streaming_finite_sinkhorn_stopped_scale_keys`, not `"raw"`, for the
   actual-gradient route.
3. Add CPU-hidden local tests for CLI parsing, metadata, and route forwarding.
4. Run a tiny trusted GPU smoke only after local tests and review.
5. Preserve the P82 FD protocol unchanged.

Do not run P82 validation until this wiring subplan passes.
