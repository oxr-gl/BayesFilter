# Phase 1 Autodiff Leak Ledger

date: 2026-06-23
phase: P1-CALLGRAPH-LEAK-INVENTORY
status: INVENTORY_COMPLETE_REVIEW_PENDING

## Route Binding

P0 contract:

```text
docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-contract-2026-06-23.md
```

Inherited state:

```text
S7R_BLOCKED_N2500_GPU_OOM_REVIEWED
```

Current reviewed command route is inherited from the P82/S7R actual-gradient
feasibility blocker.  The N10000 command is recorded at
`docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-result-2026-06-23.md:68`.

Concrete command path:

```text
python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
```

Route flags that define the current reviewed route:

- `--ad-evaluation-mode reverse-gradient`;
- `--fd-mode ad-only`;
- `--transport-plan-mode streaming`;
- `--transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys`;
- `--transport-ad-mode stabilized`;
- `--row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512`;
- `--dtype float32 --tf32-mode enabled`;
- five seeds `81120,81121,81122,81123,81124`.

Phase 8 route manifest has not yet been created:

```text
ROUTE_MANIFEST_NOT_YET_CREATED_P1
```

This marker is valid here because the current route is pinned by exact command
path, route flags, and path/line call chain below.

## Production Callgraph

Path/line-anchored call chain for the inherited actual-gradient route:

1. `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:1039`
   enters `main`.
2. `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:1047`
   selects `_gradient_diagnostic_for_contexts` for
   `--ad-evaluation-mode reverse-gradient`.
3. `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:467`
   enters `_gradient_diagnostic_for_contexts`.
4. `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:477`
   opens the outer production-route `tf.GradientTape`.
5. `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:480`
   calls `p8p._objective_from_components`.
6. `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:535`
   enters `_objective_from_components`.
7. `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:540`
   calls `_value_core`.
8. `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:495`
   enters `_value_core`.
9. `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:507`
   calls `streaming_tf.streaming_batched_ledh_pfpf_ot_value_core_tf`.
10. `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:256`
    enters the streaming LEDH-PFPF-OT value recursion.
11. `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:371`
    calls the streaming LEDH flow.
12. `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:440`
    calls `batched_annealed_transport_core_tf`.
13. `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:698`
    enters `batched_annealed_transport_core_tf`.
14. `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:814`
    selects the manual streaming finite transport route for
    `manual_streaming_finite_sinkhorn_stopped_scale_keys`.
15. `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:821`
    calls
    `_filterflow_manual_streaming_finite_transport_stopped_scale_keys`.
16. `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1942`
    defines that custom-gradient transport primitive.

SIR callback route anchors:

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:501` builds
  parameterized callbacks.
- `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py:313` defines the
  actual-SIR callback adapter used by the related fixed actual-SIR harness.
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:317` defines
  `_sir_observations`.
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py:1718` defines
  `_dpf_sir_callbacks`.

## Scope Ledger

Included production-route files:

- `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`;
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`;
- `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`;
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`;
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`;
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`;
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.

Included adjacent validation files:

- `tests/highdim/test_p82_regression_fd_harness_protocol.py`;
- `tests/highdim/test_p81_analytical_sir_score.py`;
- `tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py`;
- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`.

Excluded roots:

- historical `third_party` MATLAB and vendor trees are excluded from P1
  production reachability because the reviewed command route above does not
  import or execute them;
- unrelated `docs/plans` artifacts are excluded from source reachability except
  when cited as blocker provenance;
- `.claude`, `.git`, and cache/worktree roots are excluded as execution
  infrastructure, not production source.

## Forbidden Occurrence Classifications

| ID | Path:line | Pattern | Reachability | Classification | P2 audit payload |
|---|---|---|---|---|---|
| P1-L001 | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:477` | `tf.GradientTape` | Directly reached by reviewed command with `--ad-evaluation-mode reverse-gradient`. | `production_leak` | P2 static audit must fail this route until a no-autodiff production entrypoint replaces this outer tape. Runtime sentinel must catch this tape if route is executed. |
| P1-L002 | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:479` | `tape.watch` | Same outer production leak as P1-L001. | `production_leak` | Same P2 static/runtime failure as P1-L001. |
| P1-L003 | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:485` | `tape.gradient` | Same outer production leak as P1-L001. | `production_leak` | Same P2 static/runtime failure as P1-L001. |
| P1-L004 | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:536` | `tf.autodiff.ForwardAccumulator` | Reachable if command uses `--ad-evaluation-mode forward-jvp`; not used by reviewed reverse-gradient command but remains a selectable gradient route. | `production_leak_or_boundary_unknown` | P2 must either block this flag in production no-autodiff route or classify it as diagnostic-only by exact command/flag whitelist. |
| P1-L005 | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:563` | `tf.GradientTape` | Reached when P8p `_gradient_diagnostic` is called; P82 regression harness reaches this only for multi-seed contexts, while current reviewed P82 command microbatches one seed. | `production_leak_or_boundary_unknown` | P2 static audit must fail this helper unless the no-autodiff production route proves it is not called or moves it to diagnostic-only exact whitelist. |
| P1-L006 | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:565` | `tape.watch` | Same helper as P1-L005. | `production_leak_or_boundary_unknown` | Same P2 action as P1-L005. |
| P1-L007 | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:567` | `tape.gradient` | Same helper as P1-L005. | `production_leak_or_boundary_unknown` | Same P2 action as P1-L005. |
| P1-L008 | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:568` | `tape.jacobian` | Same helper as P1-L005. | `production_leak_or_boundary_unknown` | Same P2 action as P1-L005. |
| P1-L009 | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:699` | `tf.GradientTape` | Isolated observation-noise diagnostic gated by `--check-isolated-observation-noise`; not part of reviewed command. | `diagnostic_or_test_only` | P2 whitelist may allow exact helper/flag as diagnostic-only; production route must not enable it. |
| P1-L010 | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:700` | `tape.watch` | Same diagnostic as P1-L009. | `diagnostic_or_test_only` | Same P2 action as P1-L009. |
| P1-L011 | `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:706` | `tape.gradient` | Same diagnostic as P1-L009. | `diagnostic_or_test_only` | Same P2 action as P1-L009. |
| P1-L012 | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1960` | `@tf.custom_gradient` | Reached by manual streaming finite route selected at `experimental_batched_ledh_pfpf_ot_tf.py:814-821`. | `custom_gradient_boundary` | P2/P6 must inspect the `grad` body and fail it while it opens autodiff at lines 1988-2003. |
| P1-L013 | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1988` | `tf.GradientTape` inside custom `grad` | Reached when differentiating through P1-L012. | `production_leak` | P2 static audit must fail current manual streaming finite route; implementation phase must replace this with manual VJP or route to audited blockwise manual VJP. |
| P1-L014 | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1989` | `tape.watch` inside custom `grad` | Same as P1-L013. | `production_leak` | Same P2 action as P1-L013. |
| P1-L015 | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2003` | `tape.gradient` inside custom `grad` | Same as P1-L013. | `production_leak` | Same P2 action as P1-L013. |
| P1-L016 | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2034` | `@tf.custom_gradient` | Reached only if route uses `manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys`. | `custom_gradient_boundary` | P2/P6 must inspect and certify that the custom `grad` body is manual and contains no forbidden autodiff before this route can be production candidate. |
| P1-L017 | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2128` | `@tf.custom_gradient` | Helper for clipped dense transport, not selected by reviewed streaming manual route. | `unreachable_or_irrelevant` | P2 may block for production route by reachability; no whitelist as production candidate. |
| P1-L018 | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2140` | `@tf.custom_gradient` | Reached by `filterflow_custom_op`, not selected by reviewed route. | `unreachable_or_irrelevant` | P2 should still ensure production no-autodiff route cannot select `filterflow_custom_op`. |
| P1-L019 | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2166` | `tf.GradientTape` inside custom `grad` | Reached by `filterflow_custom_op`, not selected by reviewed route. | `unreachable_or_irrelevant` | P2 static audit should fail if this mode is selected in production. |
| P1-L020 | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2634` | `@tf.custom_gradient` | Dense finite stopped-scale/key route, not selected by reviewed streaming route. | `custom_gradient_boundary` | P2/P6 may audit if dense finite route remains in production candidate set; otherwise block by route reachability. |
| P1-L021 | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:627` | `tf.GradientTape` | Score helper, not called by reviewed command callgraph; production module contains autodiff helper. | `production_leak_or_boundary_unknown` | P2 must either block production imports of this helper or exact-whitelist it as diagnostic-only outside production route. |
| P1-L022 | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:628` | `tape.watch` | Same helper as P1-L021. | `production_leak_or_boundary_unknown` | Same P2 action as P1-L021. |
| P1-L023 | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:638` | `tape.gradient` | Same helper as P1-L021. | `production_leak_or_boundary_unknown` | Same P2 action as P1-L021. |
| P1-L024 | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:24` | import `_filterflow_custom_gradient_transport_matrix` | Not selected by reviewed route, but production module imports custom-gradient helper. | `production_leak_or_boundary_unknown` | P2 must distinguish import-only occurrence from route-reachable mode and block production route selection of `filterflow_custom_op`. |
| P1-L025 | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:876` | `_filterflow_custom_gradient_transport_matrix` call | Reached only by `transport_gradient_mode=filterflow_custom_op`; not reviewed route. | `unreachable_or_irrelevant` | P2 must fail any production manifest selecting `filterflow_custom_op`. |
| P1-L026 | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:1111` | `tf.GradientTape` | Dense score helper, not called by reviewed command callgraph; production module contains autodiff helper. | `production_leak_or_boundary_unknown` | P2 must block or exact-whitelist as diagnostic-only outside production route. |
| P1-L027 | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:1112` | `tape.watch` | Same helper as P1-L026. | `production_leak_or_boundary_unknown` | Same P2 action as P1-L026. |
| P1-L028 | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:1122` | `tape.gradient` | Same helper as P1-L026. | `production_leak_or_boundary_unknown` | Same P2 action as P1-L026. |
| P1-L029 | `tests/highdim/test_p81_analytical_sir_score.py:115` | `tf.GradientTape` | Test-only analytical SIR score comparison. | `diagnostic_or_test_only` | P2 whitelist may allow exact test path only. |
| P1-L030 | `tests/test_experimental_batched_ledh_pfpf_ot_tf.py:1117` | `tf.GradientTape` | Test-only jacobian comparison. | `diagnostic_or_test_only` | P2 whitelist may allow exact test path only. |

## P2 Audit Requirements

P2 must implement tooling that:

- fails the current reviewed route because P1-L001/P1-L003 are direct outer
  production autodiff leaks;
- fails the manual streaming finite transport route because P1-L013/P1-L015
  open autodiff inside a custom-gradient `grad` body;
- treats `tf.custom_gradient` only as an auditable boundary and never as an
  automatic pass;
- supports exact route/manifest rules so selecting
  `manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys` requires
  a separate `grad`-body audit of P1-L016;
- rejects `transport_ad_mode=full` and `filterflow_custom_op` production
  manifests;
- uses a zero-default whitelist for exact diagnostic/test-only paths such as
  P1-L009/P1-L011 and P1-L029/P1-L030;
- prevents production modules from being broadly whitelisted just because a
  helper is not currently route-reachable.

## Nonclaims

This ledger does not fix any leak, certify any route as no-autodiff, authorize
GPU ladder or FD work, or claim N10000 feasibility.
