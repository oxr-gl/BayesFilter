# P82 Phase 5 Result: Manual Streaming Transport-Gradient Wiring

status: REVIEWED_PASSED_CLAUDE_AGREE
date: 2026-06-23
phase: P5-MANUAL-STREAMING-WIRING

## Evidence Contract

| Field | Result |
|---|---|
| Question | Can P82 select and record the manual streaming transport-gradient route through the SIR d18 benchmark path? |
| Baseline/comparator | Prior P82 path hard-wired `transport_gradient_mode="raw"` in the streaming value core; M6 manual route exists in `batched_annealed_transport_core_tf`. |
| Primary criterion | Locally passed: CLI/API wiring and metadata tests pass without launching P82 validation. |
| Veto diagnostics | No P82 validation launched; no GPU evidence claimed; FD protocol unchanged; raw full-AD N10000 route not reintroduced; route metadata now records the requested mode. |
| Explanatory diagnostics | Parser choices, forwarded mode captured by test double, metadata field update, and focused test list below. |
| Not concluded | No P82 FD agreement, no N10000 feasibility, no GPU/TF32 success, no HMC/default/posterior/scientific-superiority readiness, no Zhao-Cui source-faithfulness. |

## Implementation

Patched the P82 benchmark path so `transport_gradient_mode` can flow through:

- `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
  accepts `--transport-gradient-mode` and records
  `transport.gradient_mode = args.transport_gradient_mode`.
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
  accepts `--transport-gradient-mode`, passes it into both streaming value-core
  call sites, and records the requested mode in metadata.
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  adds `transport_gradient_mode: str = "raw"` for backward compatibility and
  forwards it into `batched_annealed_transport_core_tf`.

Default behavior remains `"raw"` unless the caller explicitly selects:

```text
manual_streaming_finite_sinkhorn_stopped_scale_keys
```

## Tests

Added focused CPU-hidden tests in:

- `tests/highdim/test_p82_regression_fd_harness_protocol.py`

Coverage:

- regression-FD harness CLI accepts the manual streaming transport-gradient
  mode;
- parameterized SIR gradient CLI accepts the manual streaming
  transport-gradient mode;
- streaming value core forwards the requested mode to
  `batched_annealed_transport_core_tf`, verified with a monkeypatched test
  double and no GPU/P82 validation run.

## Local Checks

Commands run:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/highdim/test_p82_regression_fd_harness_protocol.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-phase5-manual-streaming-gradient-wiring-subplan-2026-06-23.md
rg -n "transport_gradient_mode=\"raw\"|\"gradient_mode\": \"raw\"|transport-gradient-mode|transport_gradient_mode|gradient_mode" experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/highdim/test_p82_regression_fd_harness_protocol.py
```

Observed results:

- `py_compile`: passed;
- focused pytest: `10 passed, 2 warnings in 6.91s` on the 2026-06-23
  post-crash rerun;
- diff hygiene: passed;
- route scan: old hard-coded call/metadata blocker removed from active call
  sites; `"raw"` remains only as the default value for backward compatibility.

## Claude Review

One-path read-only Claude review was run on exactly this result path:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p82-phase5-manual-streaming-gradient-wiring-result-2026-06-23.md
```

Claude returned `VERDICT: AGREE`.  The review found that the result stays
scoped to CLI/API forwarding and metadata capture, preserves non-claims about
P82 validation, GPU feasibility, FD agreement, Zhao-Cui source-faithfulness,
and production readiness, and hands off only to a separate tiny trusted GPU
smoke subplan.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Accept P5 reviewed wiring | Local checks and one-path Claude review passed | No local or review veto observed | Whether the manually wired route is feasible in the full SIR d18 GPU path | Draft and review a separate tiny trusted GPU smoke subplan | No P82 FD agreement, N10000 feasibility, GPU evidence, or production readiness |

## Handoff

P82 validation still must not run.  The next phase is a separate tiny trusted
GPU smoke subplan that exercises the manual streaming gradient mode at very
small size before any governed `N=10000` or `N=1000` work.
