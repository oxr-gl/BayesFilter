# BayesFilter DPF Batched LEDH-PFPF-OT Reset Memo

Date: 2026-06-15

Purpose: compact handoff for restarting the DPF parameter-batching work without
loading the full prior conversation.

## Current Status

- Lane: DPF filtering only. Keep independent from HMC/NeuTra. Do not use HMC
  tests, blockers, or generic HMC tuning as filtering readiness gates.
- Scope: experimental opt-in batched LEDH-PFPF-OT over model-parameter rows.
- Backend rule: BayesFilter-owned algorithmic implementation must use
  TensorFlow / TensorFlow Probability. NumPy is allowed only for benchmark
  fixture generation, reference checks, reporting, and other reviewed
  comparison-only uses.
- Public API status: not production default, not public API, not promoted.
- Key implementation file:
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`.
- Key tests:
  `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`,
  `tests/test_experimental_batched_benchmark_harness.py`.
- Key benchmark harnesses:
  `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_cpu_gpu.py`,
  `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_lgssm_scale.py`.

## What Was Implemented

- Shape contracts and deterministic fixed-input fixtures for a batched
  LEDH-PFPF-OT value/score lane.
- Batched LEDH flow core over `[B, N, D]`.
- Batched fixed-mask annealed transport core over `[B, N, D]` / `[B, N, N]`.
- Fixed-branch batched value recursion.
- Batched value-plus-score wrapper using TensorFlow autodiff over
  `theta_batch`.
- Compiled benchmark harnesses for value, value+score, scalar-loop parity, and
  one larger synthetic LGSSM scale timing.

## Verification Already Done

- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`: 20 passed in the final
  prior run.
- `tests/test_experimental_batched_benchmark_harness.py`: 8 passed in the final
  prior run.
- `git diff --check` passed for the DPF artifacts checked at the time.
- Tiny benchmark fixture parity:
  - B=1 and B=20 scalar-stack parity passed.
  - Row permutation and identical-row tests passed.
  - B20 active value parity vs scalar compiled loop max abs delta:
    `2.220446049250313e-16`.
- Score boundary:
  - No-resampling autodiff score matched central finite difference at about
    `5e-11`.
  - Active transport raw autodiff versus central finite difference differed by
    about `4.33e-3`.
  - Therefore active-transport score is not promoted as finite-difference
    equivalent; it is only checked for finite values and row locality.
- Trusted GPU was observed with two RTX 4080 SUPER GPUs and TensorFlow 2.20.0.

## Benchmark Results To Preserve

Tiny diagnostic fixture: `T=3`, `N=4` particles, `D=1`,
`parameter_dim=3`. These are descriptive only.

- Active value CPU/GPU warm-call medians:
  - B20: `0.0004247` / `0.001184` seconds.
  - B256: `0.0036069` / `0.0012761` seconds.
  - B4096: `0.033666` / `0.0016139` seconds.
- No-resampling value+score CPU/GPU warm-call medians:
  - B20: `0.001457` / `0.001782` seconds.
  - B256: `0.0099436` / `0.0018915` seconds.
- Interpretation: GPU is not universally faster on tiny shapes; it becomes
  favorable in that diagnostic only at larger batch sizes.

Larger synthetic LGSSM scale diagnostic:

- Artifact:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-lgssm-compiled-value-gpu0-b1-t200-np1000-d20-m20-activeall-2026-06-15.json`.
- Shape: `B=1`, `T=200`, `N=1000` particles, `state_dim=20`, `obs_dim=20`.
- Transport: active at every time step.
- Device/JIT: `/GPU:0`, `tf.function(jit_compile=True)`.
- Compile plus first call: `363.3586277551949` seconds.
- Warm-call timing: `8.290091150905937` seconds.
- Output finite: true.
- Interpretation: useful as one synthetic scale timing only. The first-call
  cost is dominated by XLA compilation/graph construction in the current
  unrolled implementation.

## Important Technical Diagnosis

The experimental implementation is not merely an outer Python loop over
parameter rows. It really batches model-parameter rows through TensorFlow tensor
ops. But it is not production-shaped yet.

Current recurrent particle state is reasonable:

- `particles`: `[B, N, D]`
- `log_weights`: `[B, N]`

Main problems:

1. The value recursion uses a Python `for t in range(time_steps)` in
   `batched_ledh_pfpf_ot_value_core_tf`. Under `tf.function(jit_compile=True)`,
   fixed `T=200` can be statically unrolled into a huge XLA graph. This likely
   explains the `363s` compile-plus-first-call time.
2. The fixed-branch test path requires `pre_flow_particles` with shape
   `[B, T, N, D]`. For `B=1,T=200,N=1000,D=20,float64`, this is about 32 MB, so
   not catastrophic, but it is the wrong production interface. Production DPF
   should generate proposal/pre-flow particles per time step from current
   particles and fixed/random inputs rather than requiring all pre-flow
   particles up front.
3. Active OT transport builds dense `[B, N, N]` matrices and several dense cost
   matrices. With `N=1000`, this is expensive by design. This is a real
   algorithmic cost, not just a coding accident.
4. Current fixed-mask transport computes transport even when rows are masked
   off, then selects identity output with `tf.where`. This preserves fixed graph
   behavior for tests but is not optimal for production.
5. Filtered means, variances, and ESS are appended to Python lists and stacked.
   For value-only likelihood use, a production path should support returning
   only the log likelihood to avoid unnecessary trajectory outputs.

## Nonclaims And Boundaries

- Do not claim production default readiness.
- Do not claim active-transport score finite-difference equivalence.
- Do not claim CPU/GPU superiority from one repeat or tiny fixtures.
- Do not claim scalar parity for the new LGSSM scale benchmark; it was only a
  finite GPU timing.
- Do not introduce HMC/NeuTra criteria into filtering readiness.
- Do not overwrite existing files used by other agents unless the user
  explicitly authorizes it. Prefer new opt-in files for the next iteration.

## Recommended Next Engineering Step

Create a new opt-in production-shaped experimental path rather than patching the
current fixed-branch file in place.

Suggested file name:

`experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`

Minimum design goals:

- Use `tf.while_loop` over time so XLA compiles one loop body, not a
  statically unrolled `T` copies.
- Keep recurrent state as `[B, N, D]` particles, `[B, N]` log weights, and
  `[B]` log likelihood.
- Accept a per-step proposal/pre-flow callback or deterministic noise tensor
  indexed inside the loop, instead of mandatory full `pre_flow_particles`.
- Add `return_history=False` mode for likelihood-only evaluation.
- Add an active-row/skip transport policy that avoids dense OT work when no
  rows are active, while preserving a fixed-branch option for gradient/parity
  tests.
- Keep a fixed-branch deterministic mode for scalar parity and score checks.
- Add tests for:
  - B=1 parity with the existing fixed-branch implementation on tiny fixtures;
  - B=20 scalar-stack parity where feasible;
  - `tf.function(jit_compile=True)` smoke;
  - no Python time-loop in the new streaming value core source;
  - finite likelihood at a moderate LGSSM scale.

## Suggested Next Plan Skeleton

Before implementation, write a short plan under `docs/plans` with:

- Question: can a streaming `tf.while_loop` DPF value path preserve existing
  fixed-branch parity while reducing compile blow-up at `T=200`?
- Baseline: current fixed-branch experimental value core.
- Primary correctness criterion: tiny-fixture parity versus current
  fixed-branch output.
- Primary performance diagnostic: compile-plus-first-call and warm-call timing
  for `B=1,T=200,N=1000,D=20`.
- Vetoes: non-finite likelihood, failed parity, failed JIT compile, wrong
  device placement in trusted GPU run.
- Explanatory only: GPU memory, compile time, warm-call time until repeated
  benchmark evidence exists.
- Artifact: JSON benchmark and result note.

## Git / Worktree Caution

At reset time, the worktree contains unrelated modified HMC files. Do not
revert or stage them for DPF work unless the user explicitly asks. DPF-related
new files are mostly untracked, plus one modified DPF benchmark test file.

DPF-related files to consider in a future DPF commit:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`
- `tests/test_experimental_batched_benchmark_harness.py`
- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_cpu_gpu.py`
- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_lgssm_scale.py`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-*.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-*.md`
- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-*2026-06-15.md`
- `docs/plans/dpf-lgssm-t200-d20-n1000-single-run-benchmark-2026-06-15.md`
- this reset memo.

Unrelated modified HMC files observed at reset time include:

- `bayesfilter/inference/generic_hmc_tuning.py`
- `bayesfilter/inference/hmc.py`
- `bayesfilter/inference/hmc_tuning.py`
- `tests/test_generic_hmc_tuning.py`
- `tests/test_hmc_mass_matrix.py`
- `tests/test_hmc_trajectory_tuning.py`
- `tests/test_nonlinear_ssm_phase4_full_chain_hmc.py`

## Fast Restart Prompt

Use this prompt after restarting Codex:

> Read `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-reset-memo-2026-06-15.md`.
> Continue the DPF parameter-batched LEDH-PFPF-OT work from the recommended next
> engineering step. Keep filtering independent from HMC, preserve unrelated
> dirty worktree changes, write a short plan before nontrivial experiments, and
> prefer a new opt-in streaming file rather than overwriting the current
> fixed-branch experimental implementation.
