# P8j TF32 Batched Actual-SIR Test Plan

metadata_date: 2026-06-17
status: DRAFT_ROUND1_REPAIRED_PENDING_CLAUDE_REVIEW
lane: P8j DPF SIR d18
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Objective

Test whether the merged experimental batched TF32/GPU LEDH-PFPF-OT code is
useful for the actual Zhao-Cui spatial SIR d18 DPF lane, not merely for a
SIR-shaped synthetic LGSSM proxy.

The test is a feasibility and runtime gate only.  It may justify a later
particle-tuning repair path if it passes, but it cannot by itself select a SIR
d18 particle count or complete the leaderboard.

## Entry Conditions

- Current branch includes the merged TF32/GPU batched DPF code from
  `65d8dc8 Add experimental batched DPF TF32 diagnostics`.
- Existing P8j scalar actual-SIR evidence shows:
  - adaptive LEDH OT is finite and transport-valid for SIR d18 at `N=64`;
  - runtime is about `789.755664` seconds for five fixed seeds;
  - MC SE remains blocked and no SIR d18 DPF particle count is selected.
- Existing TF32/GPU proxy artifacts are finite and fast for SIR-shaped
  dimensions, but they are LGSSM-shaped and are not actual-SIR evidence.
- GPU/CUDA commands must run in trusted/escalated context.

## Required Artifacts

- This reviewed plan.
- Claude review artifacts:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-test-claude-review-round-01-2026-06-17.md`
  and later rounds if needed.
- If the plan converges, implementation patch:
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  - focused tests for the opt-in nonlinear prior-mean route
  - a standalone actual-SIR probe script under `docs/benchmarks/`
- Probe JSON/markdown result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-probe-2026-06-17.{json,md}`
- Close record:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-test-result-2026-06-17.md`

## Skeptical Audit

The plan would be misleading if it simply reran the existing
`benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py` at
`T=20,D=18,M=9`.  That benchmark tests an LGSSM-shaped proxy with a linear
transition matrix; it does not exercise the actual SIR transition, observation,
or density route.

The current experimental batched flow also computes prior means as
`transition_matrix @ ancestors`.  Actual SIR is nonlinear.  Therefore, before
making any actual-SIR claim, execution must add or use an opt-in nonlinear
`prior_mean_fn` hook so the flow/proposal density is anchored at the SIR
transition mean.  If that hook cannot be implemented without disturbing the
existing linear path, stop with a blocker.

This plan passes the skeptical audit because the primary probe must use actual
SIR equations/callback semantics, must record the route difference from scalar
Algorithm 1 UKF covariance lifecycle, and must treat proxy speed only as an
engineering motivation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the experimental batched TF32/GPU streaming LEDH-PFPF-OT path execute an actual SIR d18 value probe with finite output and materially lower runtime than the scalar P8j path, while preserving route boundaries? |
| Baseline/comparator | P8j scalar actual-SIR adaptive LEDH OT `N=64`, five seeds, runtime about `789.755664s`, finite/transport-valid but MC-SE blocked.  Existing SIR-shaped LGSSM proxy timings are explanatory only. |
| Primary pass criterion | A trusted-GPU actual-SIR batched probe using five fixed seeds at `T=20,D=18,M=9,N=64` is finite, outputs on GPU, uses TF32/float32 where declared, records actual SIR transition/observation semantics from `_dpf_sir_callbacks()`, and has mean warm-call wall time for one full batched five-seed evaluation at least `5x` faster than the scalar P8j `N=64` five-seed runtime. |
| Veto diagnostics | Probe uses LGSSM proxy rather than actual SIR; nonlinear prior mean hook absent; output not finite; no GPU device evidence; TensorFlow silently falls back to CPU; route metadata claims scalar Li-Coates Algorithm 1 UKF parity; model/data semantics changed without tieout; implementation breaks existing linear-path tests; Claude review does not converge within five rounds. |
| Explanatory diagnostics | Compile time, warm-call time, TF32 flag, output device, log-likelihood values by seed, ESS if history is requested, memory info, shape, chunk sizes, transport settings, and scalar/proxy runtime comparison. |
| Not concluded | No selected SIR d18 particle count, no leaderboard completion, no MC-SE adequacy, no exact likelihood correctness, no gradient/HMC/NUTS readiness, no Zhao-Cui TT/SIRT or MATLAB parity, no production/default readiness. |

## Required Checks And Execution

Plan review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name p8j-tf32-batched-actual-sir-plan-review-r1 --model opus --effort max "<bounded read-only prompt>"
```

Local implementation checks after a converged review:

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py -q -k "nonlinear_prior_mean"
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sir_dpf"
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py
```

The `nonlinear_prior_mean` test must fail if the new hook is absent.  It must
prove at minimum that:

- the default linear path is unchanged;
- the opt-in nonlinear prior-mean callback is used for pre-flow log density
  and LEDH anchoring;
- a nonlinear prior callback produces different log-density output from a
  deliberately wrong linear transition matrix on the same particles.

The actual-SIR probe JSON must include a `sir_semantics` block derived from
`_dpf_sir_callbacks()` with at least:

- `row_id`;
- `state_dimension`;
- `observation_dimension`;
- `process_noise_policy`;
- `flow_observation_contract`;
- `target_density_used_for_correction`;
- `adapter_classification`;
- `actual_sir_callbacks_used: true`;
- `nonlinear_prior_mean_hook_used: true`.

Trusted GPU probe after local checks pass:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 64 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --warmups 1 --repeats 2 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-probe-2026-06-17.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-probe-2026-06-17.md
```

Each timed warm call must be exactly one full batched evaluation of the five
seeds listed in `--batch-seeds` at the declared `T=20,N=64,D=18,M=9`.  The JSON
must separate:

- `compile_and_first_call_seconds`;
- `warm_call_timings_seconds`;
- `warm_call_timing_summary_seconds`;
- `batch_seed_count`;
- `full_batched_evaluation_per_warm_call: true`;
- `scalar_comparator_runtime_seconds: 789.755664`;
- `scalar_comparator_scope: P8j Phase 5d scalar actual-SIR adaptive LEDH OT N=64 five-seed trusted-GPU run`;
- `speedup_vs_scalar_comparator_mean_warm_call`.

If `N=64` fails before producing an informative artifact, run one smaller
debug-only trusted GPU probe at `N=16` and record it as a blocker/debug result,
not as pass evidence.

## Forbidden Claims And Actions

- Do not claim the existing SIR-shaped LGSSM proxy is actual SIR evidence.
- Do not claim scalar Li-Coates Algorithm 1 UKF parity unless an explicit
  route-parity check is implemented and passes.  The first batched probe is an
  experimental streaming LEDH-PFPF-OT SIR adapter.
- Do not select a particle count or refresh the leaderboard from this probe.
- Do not claim MC-SE adequacy, gradient correctness, HMC/NUTS readiness,
  Zhao-Cui TT/SIRT source-faithfulness, MATLAB parity, or production readiness.
- Do not stage, commit, merge, push, or clean unrelated dirty worktree entries.
- Do not run GPU/CUDA commands without trusted/escalated permissions.

## Stop Conditions

Stop and write a blocker if:

- Claude review finds a material plan flaw that does not converge after five
  rounds.
- The nonlinear SIR prior-mean hook would require a broad rewrite or would
  change existing linear/LGSSM behavior.
- Actual-SIR probe cannot be made to use GPU in trusted context.
- Probe output is nonfinite or route metadata is ambiguous.
- Runtime is not materially better than the scalar P8j comparator.
- Fixing the problem requires changing SIR model/data definitions or changing
  P8j scientific promotion criteria after seeing results.

## Handoff Conditions

If the probe passes, draft a follow-on reviewed subplan for a batched SIR
particle-tuning feasibility ladder.  If it fails, write a blocker explaining
whether the failure is implementation, adapter, GPU/runtime, numerical, or
scientific-evidence scope.
