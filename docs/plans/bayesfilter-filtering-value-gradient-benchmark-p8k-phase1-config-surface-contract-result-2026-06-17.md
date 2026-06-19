# P8k Phase 1 Result: Generic Configuration Surface Contract

metadata_date: 2026-06-18
status: PASS_PENDING_CLAUDE_REVIEW_OF_PHASE2
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only, pending for Phase 2 handoff

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | The safe P8k configuration surface is opt-in and generic.  Phase 2 may implement harness plumbing only; core behavior repairs wait for later phases. |
| Primary criterion status | Passed locally.  The inventory checks found the expected engine and harness anchors, and this result classifies each required knob by owner surface, default behavior, required tests, and forbidden claim. |
| Veto diagnostic status | No active Phase 1 veto.  No implementation code was edited, no GPU command was run, and no default policy change is authorized. |
| Main uncertainty | Phase 2 harness smoke may expose that actual-SIR needs an explicit value-only/history flag and metadata repair before benchmarking knobs can be compared fairly. |
| Next justified action | Review Phase 2 harness-plumbing subplan with Claude, then implement only metadata/CLI plumbing and CPU-only smokes if review agrees. |
| What is not concluded | No implementation success, no runtime improvement, no memory improvement, no particle adequacy, no leaderboard completion, no exact likelihood/gradient/HMC/NUTS/production readiness. |

## Local Checks Run

```bash
rg -n "def streaming_batched_ledh_pfpf_ot_value_core_tf|def batched_ledh_flow_streaming_particles_tf|return_history|skip_transport_when_no_active|transport_plan_mode|row_chunk_size|col_chunk_size|particle_chunk_size|sinkhorn_iterations|prior_mean_fn|pre_flow_step_fn" experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py
rg -n -- "--return-history|--transport-policy|--sinkhorn-iterations|--row-chunk-size|--col-chunk-size|--particle-chunk-size|--tf32-mode|--proposal-mode|return_history=True|return_history=args.return_history" docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
```

Results:

- Engine anchors found in
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`.
- Harness anchors found in both LGSSM and actual-SIR benchmark files.
- `git diff --check` passed for the P8k planning artifacts.

## Configuration Surface Classification

| Knob | Owner surface | Current default behavior | Phase 2 action | Required checks | Forbidden claim |
| --- | --- | --- | --- | --- | --- |
| `return_history` / future `diagnostic_level` | Engine and harness | Engine defaults `False`; LGSSM exposes `--return-history`; actual-SIR currently forces `return_history=True`. | Add actual-SIR harness plumbing for an opt-in history mode or value-only mode, preserving existing default unless reviewed otherwise. | Pycompile, CPU-only actual-SIR smoke with value-only and history mode when feasible, metadata check. | Do not claim runtime speedup until trusted GPU profiling. |
| `skip_transport_when_no_active` | Engine | Argument exists and defaults `True`, but current dynamic branch does not use it except static all-false shortcut. | No Phase 2 implementation.  Phase 4 owns repair and tests. | Later focused tests must prove no OT call on all-inactive dynamic mask. | Do not claim no-resampling paths avoid OT until Phase 4 passes. |
| `transport_plan_mode` | Engine | Engine supports `streaming` and `dense`; harnesses hard-code or effectively use `streaming`. | Record metadata consistently; expose CLI only if CPU smoke can validate both paths without changing defaults. | Pycompile and tiny CPU smoke for any newly exposed mode. | Do not imply dense mode is recommended. |
| `transport_policy` | Harness | LGSSM and actual-SIR expose `active-all`, `active-odd`, and `no-resampling`. | Preserve existing CLI and metadata. | CPU smoke for `no-resampling` in Phase 2. | Do not treat transport policy runtime as statistical adequacy. |
| `sinkhorn_iterations` | Engine and harness | Harnesses expose integer CLI; P8j actual-SIR used `10`. | Preserve CLI and metadata. | Pycompile and CPU smoke. | Do not claim lower iterations preserve accuracy without a later validity check. |
| `sinkhorn_epsilon` | Engine and harness | Harnesses expose float CLI. | Preserve CLI and metadata. | Pycompile and CPU smoke. | Do not claim tuned epsilon is scientifically valid from runtime alone. |
| `row_chunk_size` | Engine and harness | Harnesses expose positive integer CLI. | Preserve CLI and metadata. | Pycompile and CPU smoke. | Do not call chunk size a model-specific optimization. |
| `col_chunk_size` | Engine and harness | Harnesses expose positive integer CLI. | Preserve CLI and metadata. | Pycompile and CPU smoke. | Do not infer accuracy differences from chunk size without equivalence checks. |
| `particle_chunk_size` | Engine and harness | Harnesses expose positive integer CLI. | Preserve CLI and metadata. | Pycompile and CPU smoke. | Do not treat smaller chunks as automatically faster. |
| `tf32_mode` | Harness/global TensorFlow precision policy | Both benchmark harnesses expose `default`, `enabled`, and `disabled`. | Preserve CLI and metadata. | Pycompile; GPU validation deferred to Phase 5 trusted context. | Do not claim TF32 numerical equivalence or default readiness. |
| `proposal_mode` | LGSSM harness | LGSSM exposes `callback` and `tensor`; actual-SIR uses callback route. | No actual-SIR proposal tensor mode in Phase 2.  Preserve LGSSM metadata. | LGSSM CPU smoke can cover callback mode. | Do not force tensor storage for actual-SIR. |
| `linear_observation_matrix` | Future generic engine fast path | Not an engine-level API; LGSSM has local constant-linear callbacks. | No Phase 2 implementation.  Phase 6 design owns it. | Phase 6 design and focused tests if implemented. | Do not implement a SIR-specific selector as a generic engine path. |
| transition/prior-mean cache | Future generic engine fast path | `prior_mean_fn` and `pre_flow_step_fn` exist; transition mean may be recomputed by callbacks. | No Phase 2 implementation.  Phase 6 design owns it. | Phase 6 design must prove cache key validity by time/particles and avoid caching randomness. | Do not cache stochastic noise or claim gradient safety without tests. |

## Phase 2 Implementation Checklist

Phase 2 may:

- add actual-SIR benchmark CLI plumbing for value-only/history output if it
  preserves current default or explicitly records the changed opt-in mode;
- ensure both LGSSM and actual-SIR artifacts record selected generic knobs;
- run CPU-only harness smokes with `CUDA_VISIBLE_DEVICES=-1`;
- update result metadata and markdown summaries.

Phase 2 must not:

- edit the core streaming engine;
- run trusted GPU profiling;
- change default BayesFilter implementation policy;
- claim speedup, memory improvement, particle adequacy, or leaderboard
  completion.

## Handoff

Phase 2 can proceed after Claude read-only review of this result and the Phase
2 subplan returns `VERDICT: AGREE`, or after any fixable issue is patched and
focused checks are rerun.
