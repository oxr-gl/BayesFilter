# Actual-SIR Low-Rank Route Performance Repair Result

Date: 2026-06-22

Status: `COMPILED_GPU_XLA_ROUTE_REPAIR_PASS`

## Phase Objective

Repair the actual-SIR low-rank route bug where the low-rank algorithmic path
could pass through eager/Python/NumPy-style execution barriers instead of the
BayesFilter GPU/XLA TensorFlow route.

## Evidence Contract

- Question: does the actual-SIR low-rank route now execute through a
  tensor-only TensorFlow compiled core, with GPU/XLA evidence for the smoke
  shape?
- Baseline/comparator: previous route/harness behavior that allowed eager
  diagnostic-loop timing and `.numpy()` barriers in the low-rank solver route.
- Primary pass criterion: solver source has no NumPy or `.numpy()` barrier, the
  actual-SIR harness defaults to and requires `compiled_core` timing, and the
  compiled low-rank route passes focused CPU and trusted GPU XLA smokes.
- Veto diagnostics: syntax failure, focused unit-test failure, source guard
  finding `.numpy()` in the solver or compiled core region, failed XLA compile,
  missing GPU output devices in trusted GPU smoke, or low-rank invariant hard
  vetoes.
- Explanatory diagnostics only: warm timing, first-call timing, GPU memory
  snapshots, and smoke-shape numerical values.
- Not concluded: speedup, posterior correctness, dense Sinkhorn equivalence,
  HMC readiness, production statistical validity, or scientific superiority.
- Artifact preserving result: this result note plus `/tmp/actual_sir_lr_xla_gpu_smoke.json`
  for the trusted smoke transcript.

## Changes

- Added `low_rank_coupling_solver_resample_tensors_tf` and
  `LowRankCouplingSolverTensorsTF` so the algorithmic solver path returns
  tensors directly.
- Replaced the Dykstra projection Python loop and eager convergence break with
  `tf.while_loop`.
- Removed solver-route `.numpy()` diagnostics and NumPy-like scalar extraction
  from `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`.
- Removed the actual-SIR validation harness diagnostic loop fallback and made
  `compiled_core` the only accepted timing source for streaming and low-rank
  routes.
- Added `--jit-compile` provenance through the harness and tuning grid. The
  actual-SIR low-rank route harness/grid do not expose a `--no-jit-compile`
  escape.
- Updated tuning-grid aggregation so stale rows without `compiled_core` and XLA
  provenance cannot be treated as complete low-rank provenance.
- Replaced NumPy assertions in the immediate low-rank solver test with
  TensorFlow assertions.
- Added source guards for no `.numpy()` in the solver or compiled core region.

## Checks

- `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_low_rank_coupling_solver_tf.py tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- `python -m pytest tests/test_low_rank_coupling_solver_tf.py tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: `21 passed`.
- CPU-hidden direct solver XLA smoke:
  - Result: compiled with XLA on host; finite particles/log weights;
    max factor residual `1.4028647049579845e-08`.
- Trusted GPU actual-SIR low-rank smoke:
  - Command used GPU-visible scope with `CUDA_VISIBLE_DEVICES=1`, `--device /GPU:0`,
    `--expect-device-kind gpu`, `--jit-compile`, `--route low_rank`,
    `--time-steps 1`, `--num-particles 8`, `--low-rank-rank 4`.
  - Result: `PASS`, hard vetoes `[]`.
  - Selected physical GPU: NVIDIA GeForce RTX 4080 SUPER,
    UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`.
  - Row output devices: all `/device:GPU:0`.
- `jit_compile`: `true`.
  - `low_rank_timing_source`: `compiled_core`.
  - XLA compilation was logged by TensorFlow during the trusted run.
  - Max factor marginal residual: `1.1920928955078125e-07`.

## Read-Only Claude Review Attempt

- Round 1 command: `claude_worker.sh --name actual-sir-low-rank-xla-repair-review`
  with read-only scope over the changed files and this result note.
  - Outcome: reviewer responded, then routed through generic PR-review tooling,
    consumed a large diff, and was interrupted after it failed to produce a
    bounded verdict. Worker reported auth/404 noise during shutdown.
- Round 2 command: `claude_worker.sh --name actual-sir-low-rank-xla-repair-review-r2 --model opus --effort max`
  with a tighter prompt forbidding skills, edits, and `gh`.
  - Outcome: reviewer responded and inspected evidence, but repeatedly hit its
    `Read` tool `pages` parameter issue and again failed to produce the
    requested bounded verdict before manual interruption.
- Decision: no Claude `VERDICT: AGREE` is recorded for this repair. This is a
  reviewer-tool failure, not a route-execution veto. The local source guards,
  focused tests, CPU XLA smoke, and trusted GPU XLA smoke remain the release
  evidence for this repair. Do not cite Claude as agreeing with this result.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Repair accepted for the actual-SIR low-rank compiled route | Passed focused source, unit, CPU-XLA, and trusted GPU-XLA checks | No veto fired in the focused checks | Smoke shape is tiny; broad route performance and statistical behavior remain separate gates | Continue with compiled-core route performance/tuning work only under this provenance contract | No speedup, posterior correctness, HMC readiness, or scientific superiority claim |

## Handoff Conditions

Next phase may run compiled-core route performance/tuning rows only if:

- `low_rank_timing_source == "compiled_core"`;
- `streaming_timing_source == "compiled_core"` when streaming rows are present;
- `jit_compile is True` for promotional or tuning-screen rows;
- GPU/TF32 provenance is present for GPU-targeted rows;
- row artifacts record no hard vetoes before any descriptive timing comparison.

Stop if a future row reintroduces eager diagnostic-loop timing, solver `.numpy()`
barriers, NumPy in the algorithmic route, missing GPU/XLA provenance for a
GPU-targeted claim, or any hard-veto invariant failure.

## Boundary Safety

This result repairs a code-path execution bug. It does not authorize crossing
scientific-claim, HMC-readiness, dense-equivalence, public-API, or default-policy
boundaries beyond the existing owner directive that BayesFilter DPF work targets
the GPU TF32 TensorFlow route.
