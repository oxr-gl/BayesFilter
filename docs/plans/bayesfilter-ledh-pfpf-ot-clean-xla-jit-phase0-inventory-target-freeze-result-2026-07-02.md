# Phase 0 Result: Inventory And Target Freeze

Date: 2026-07-02

Status: `PASS_TO_PHASE1_REVIEW`

## Phase Objective

Identify the current unclean compiled-path surfaces and freeze the exact
clean-XLA target before implementation edits.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Proceed to Phase 1 static guardrails after Claude read-only review of the Phase 1 subplan. |
| Primary criterion status | Met for Phase 0: concrete file/line surfaces were identified for Python time scans, reverse scans, record lists, seed loops, RK4 substep loops, streaming Sinkhorn loops, score-bearing stop-gradient risks, and compiler-heavy local autodiff. |
| Veto diagnostic status | No Phase 0 veto fired. Required files were readable. No code was changed. |
| Main uncertainty | The exact implementation repair order may change after the static audit makes the compiled-route surfaces machine-readable. |
| Next justified action | Add a static audit script and tests that detect these patterns before any refactor claims clean XLA. |
| Not concluded | No compiler issue is fixed. No GPU/XLA runtime evidence is claimed. No numerical correctness, posterior correctness, or HMC readiness claim is made. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded in Phase 0; worktree is heavily dirty and Phase 0 is inventory-only. |
| Command | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py::test_streaming_module_source_is_gpu_oriented tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r12_gpu_manual_score_route_is_explicit_reverse_scan tests/test_contract_e_phase3_gradient_route_audit.py::test_phase3_r14_manual_dense_sinkhorn_recursions_use_tf_while_loop` |
| Environment | Local repo, TensorFlow import with GPU intentionally hidden for source/static checks. |
| CPU/GPU status | CPU-hidden by `CUDA_VISIBLE_DEVICES=-1`; this is not GPU evidence. |
| Data version | N/A. |
| Random seeds | N/A. |
| Wall time | 4.15 seconds reported by pytest. |
| Output artifact paths | This result file and Phase 1 subplan. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-subplan-2026-07-02.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-result-2026-07-02.md` |

## Local Checks

Result: `PASS`

```text
...                                                                      [100%]
3 passed in 4.15s
```

These checks show that existing source-level guardrails already cover nearby
clean routes and dense finite Sinkhorn primitives. They do not show that the
P8p SIR manual score route is clean.

## Inventory

| Surface | File/line anchor | Current pattern | Why it is unclean for the target | Phase mapping |
| --- | --- | --- | --- | --- |
| SIR RK4 forward substeps | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:454`, `:456`, `:495` | Python `aux = []`, Python `for _ in range(int(substeps))`, and `aux.append(...)`. | XLA sees a Python-unrolled substep graph and Python-list tensor storage instead of loop state. | Phase 3 |
| SIR RK4 reverse substeps | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:527` | `for record in reversed(aux)`. | Reverse recursion is a Python loop over Python-stored tensors, not TensorFlow loop state. | Phase 3 |
| Manual score time length | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:1196` | `time_steps = int(observations.shape[0])`. | The compiled route binds time as a Python integer, which encourages graph unrolling by observed length. | Phase 4 |
| Manual forward time scan | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:1201`, `:1208`, `:1285` | Python `records = []`, Python `for time_index in range(time_steps)`, and `records.append(...)`. | Forward filter history needed by the reverse pass is stored in Python records, not `TensorArray` or TensorFlow loop state. | Phase 4 |
| Manual reverse time scan | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:1322` | `for record in reversed(records)`. | Reverse scan is Python unrolled and cannot be represented as an XLA loop. | Phase 4 |
| Fixed randomness construction | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:1221`, `:1222`, `:1232` | Python `noise_rows = []`, seed loop over `args.batch_seeds`, and `noise_rows.append(...)`. | Randomness should enter the compiled route as fixed tensors; seed-by-seed Python generation inside the route is not clean XLA. | Phase 2 |
| Repeated RK4 VJP calls inside reverse scan | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:1423`, `:1468`, `:1513`, `:1568` | Calls to `_sir_transition_mean_vjp_tf(...)` consume Python-list aux data. | Even if the outer scan is converted, the RK4 VJP must also use TensorFlow loop state. | Phase 3/4 |
| Historical stopped streaming Sinkhorn value route | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1549`, `:1585` | `tf.stop_gradient(x)` and Python `for _ in range(steps)`. | This is a stopped partial derivative route and a Python-unrolled finite Sinkhorn loop. It must not be called the score. | Phase 1/5 |
| Total streaming Sinkhorn value route | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1702` | Python `for _ in range(steps)`. | This route is mathematically total with respect to the finite Sinkhorn scalar, but the finite iteration loop is still Python-unrolled. | Phase 5 |
| Historical stopped streaming Sinkhorn VJP route | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1782`, `:1818`, `:1819`, `:1820` | `tf.stop_gradient(x)`, Python `states = []`, Python `for _ in range(steps)`, and `states.append(...)`. | Stopped keys omit total derivative terms, and Python state lists make the reverse finite Sinkhorn pass unclean for XLA. | Phase 1/5 |
| Total streaming custom-gradient helper | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2124`, `:2152`, `:2175` | `@tf.custom_gradient` body uses local `tf.GradientTape` and `tape.gradient(...)`. | This may compute the intended total derivative locally, but it is compiler-heavy and must be classified separately from a manual clean total-VJP route. | Phase 1/5 |
| Clean value-core counterexample | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:349`, `:505`, `:586`, `:651` | Dynamic time length, `TensorArray`, and `tf.while_loop`. | This is the local pattern Phase 4 should emulate for score-bearing scans. | Phase 4 |
| Existing static hygiene tests | `tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py:527` and `tests/test_contract_e_phase3_gradient_route_audit.py:86`, `:106` | Tests assert `tf.while_loop` presence and forbid selected Python/autodiff patterns. | Phase 1 should extend this practice to the current P8p SIR manual score route and streaming full route. | Phase 1 |

## Frozen Clean-XLA Target

For the corrected score-bearing route, clean XLA means the executed finite
computation uses TensorFlow loop state for dynamic recursion:

- time recursion uses `tf.while_loop` or an equivalent TensorFlow loop;
- reverse recursion uses `tf.while_loop`, not `reversed(records)`;
- saved forward state needed by reverse recursion is in `TensorArray` or tensor
  loop state, not Python lists;
- RK4 substeps and their VJP use TensorFlow loop state;
- fixed randomness is supplied as tensors to the compiled route;
- finite Sinkhorn iteration loops use TensorFlow loop state;
- stopped partial derivatives are not called scores.

## Phase 1 Guardrail Requirements

Phase 1 must create a machine-readable static audit that can report the current
route as unclean without making that expected current failure a pytest failure.
The audit must at minimum detect:

- Python time scan in `_manual_value_and_score_from_components`;
- `records.append(...)` and `reversed(records)` in that route;
- Python seed loops and `noise_rows.append(...)` in that route;
- Python RK4 `aux` lists and `reversed(aux)`;
- streaming finite Sinkhorn `range(steps)` in score-bearing full routes;
- score-bearing `tf.stop_gradient(x)` in stopped-key Sinkhorn helpers;
- local `GradientTape` in the total streaming custom-gradient helper as a
  warning or veto, explicitly classified in the Phase 1 subplan.

## Post-Run Red-Team Note

The strongest alternative explanation is that the current unclean surfaces are
in a diagnostic script rather than the final production API. That does not make
them harmless, because this script is currently the validated corrected SIR
gradient route used to decide whether the score is usable. Phase 1 should
therefore audit the route by symbol, not only by broad file-level pattern
matching.

The weakest part of Phase 0 evidence is that it is source/static evidence only.
Runtime HLO and compile-scaling evidence is intentionally deferred to Phase 6.

## Next Handoff

Draft and review:

`docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-subplan-2026-07-02.md`

Phase 1 may start only after the Phase 1 subplan survives Codex skeptical audit
and Claude read-only review returns `VERDICT: AGREE` or review findings are
patched and rereviewed.
