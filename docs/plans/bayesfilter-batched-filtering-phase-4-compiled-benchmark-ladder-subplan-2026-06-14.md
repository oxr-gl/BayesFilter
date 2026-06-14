# Phase 4 Subplan: Compiled Benchmark Ladder

Date: 2026-06-14

## Status

`DRAFT_FOR_LOCAL_AND_CLAUDE_REVIEW`

## Phase Objective

Build and run a bounded, artifact-preserving benchmark ladder for the
experimental batched value+score paths under the realistic shape
`T=200`, `state_dim=10`, `obs_dim=10`, `parameter_dim=2`, with batch sizes
`B=20`, `B=256`, and `B=4096` where feasible.

The phase must compare scalar-loop and batched execution fairly enough to
support engineering triage.  It must not claim production readiness or broad GPU
speedup.  GPU comparisons are allowed only for JIT/XLA-compiled functions in a
trusted GPU context.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed with reviewed baseline inventory and boundary audit.
- Phase 1 passed with deterministic batched Kalman and affine SVD sigma-point
  correctness tests.
- Phase 2 passed with nonlinear SVD sigma-point branch/fail-closed tests.
- Phase 3 passed with a non-default experimental value+score interface
  candidate and public-export checks.
- Existing experimental kernels remain unexported:
  - `bayesfilter/linear/experimental_batched_kalman_tf.py`
  - `bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py`
- Existing top-level interface candidate remains non-default:
  - `bayesfilter/experimental_batched_value_score.py`
- No production default change is authorized.
- No eager GPU benchmark comparison is authorized.
- CUT4 remains outside default-promotion scope.
- Existing unrelated dirty worktree changes must be preserved.

## Required Artifacts

New or refreshed benchmark/test artifacts:

- `docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py`
- `docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py`
- `tests/test_experimental_batched_benchmark_harness.py`

Benchmark JSON artifacts:

- `docs/benchmarks/experimental-batched-kalman-compiled-cpu-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-compiled-cpu-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-compiled-cpu-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-cpu-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-cpu-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-cpu-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-compiled-gpu1-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-kalman-compiled-gpu1-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-gpu1-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-kalman-compiled-gpu1-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-cpu-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-cpu-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-cpu-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-cpu-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-cpu-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-cpu-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b4096-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-gpu1-b256-t200-n10-m10-2026-06-14.json`
- `docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-gpu1-b4096-t200-n10-m10-2026-06-14.json`

Phase records:

- `docs/plans/bayesfilter-batched-filtering-phase-4-claude-review-round-01-2026-06-14.md`
- Additional Claude round files only if needed.
- `docs/plans/bayesfilter-batched-filtering-phase-4-compiled-benchmark-ladder-result-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-5-downstream-harness-subplan-2026-06-14.md`

If `B=4096` or a scalar-loop compiled comparator fails because of memory, XLA
incompatibility, compile timeout, or runtime timeout, write the failed
JSON/console evidence when available and record it as capacity or feasibility
evidence, not as a correctness failure, unless nonfinite output, wrong device
placement, or parity failure is observed.

## Required Checks, Tests, And Reviews

### Pre-execution local checks

1. Verify this subplan contains all required headings.
2. Verify Phase 3 result exists and records passing tests.
3. Verify no public export files are planned for editing:
   `bayesfilter/__init__.py`, `bayesfilter/linear/__init__.py`,
   `bayesfilter/nonlinear/__init__.py`.
4. Verify current benchmark harnesses do not permit eager GPU timing as a
   performance comparison.
5. Verify the SVD harness already has a `compiled-timing` path.
6. Verify the Kalman harness gap is real: it currently lacks a
   `compiled-timing` path and therefore must be repaired before Kalman GPU
   comparisons.

### Implementation

1. Add a `compiled-timing` mode to
   `docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py` using
   `@tf.function(jit_compile=True)` and reporting:
   - `compile_and_first_call_seconds`;
   - `warm_call_summary`;
   - `per_filter_warm_median_seconds`;
   - value/score device placement;
   - finite-output status;
   - `compiled: {"tf_function": true, "jit_compile": true}`;
   - explicit note that warm timings exclude compile.
2. Add scalar-loop compiled timing comparators where feasible:
   - Kalman scalar-loop comparator over the same deterministic fixture rows.
   - SVD-UKF scalar-loop comparator if it compiles within the bounded timeout.
   - The scalar-loop comparator may use a Python loop in the standalone
     benchmark harness to iterate independent rows, but each measured row call
     must be a compiled value+score authority call.  This comparator is not an
     HMC-jittable production implementation and must not be described that way.
   - If a scalar authority path cannot be XLA-compiled, preserve the failure
     and classify it as scalar-GPU comparator infeasibility.
3. If scalar GPU comparator is infeasible because scalar production authority
   paths are not XLA-compatible, record the failed command and error as an
   infeasibility artifact.  Do not compare batched GPU against scalar CPU as a
   broad speedup claim.
4. Add focused tests in
   `tests/test_experimental_batched_benchmark_harness.py` covering:
   - Kalman benchmark argument parser accepts `compiled-timing`;
   - benchmark argument parsers accept the scalar-loop compiled comparator
     mode, or otherwise fail closed with a documented infeasibility mode;
   - Kalman compiled timing JSON contains JIT fields and finite outputs for a
     tiny CPU shape;
   - SVD compiled timing JSON contains JIT fields and finite outputs for a tiny
     CPU shape;
   - GPU timing command construction, if represented in code, cannot use eager
     timing as benchmark evidence.
5. Do not edit public exports or default selection code.

### Required local test commands

Run before GPU benchmarks:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_benchmark_harness.py tests/test_experimental_batched_value_score_interface.py tests/test_experimental_batched_linear_kalman_tf.py tests/test_experimental_batched_svd_sigma_point_tf.py tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py
```

Run public API guard:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_v1_public_api.py -k public_api
```

Audit-only source scans:

```bash
rg -n "compiled-timing|jit_compile=True|allow-eager-gpu-timing|expect-device-kind|scalar-loop|compile_and_first_call" docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py tests/test_experimental_batched_benchmark_harness.py
```

```bash
rg -n "experimental_batched_value_score|experimental_batched_kalman|experimental_batched_svd" bayesfilter/__init__.py bayesfilter/linear/__init__.py bayesfilter/nonlinear/__init__.py
```

The second scan must not show new public export entries for the experimental
batched modules.

### Required benchmark commands

CPU benchmark commands run with GPU hidden:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py --mode compiled-timing --device-scope cpu --device /CPU:0 --expect-device-kind cpu --batch-size 20 --time-steps 200 --state-dim 10 --obs-dim 10 --parameter-dim 2 --warmups 3 --repeats 10 --output docs/benchmarks/experimental-batched-kalman-compiled-cpu-b20-t200-n10-m10-2026-06-14.json
```

Repeat the same CPU command for Kalman `B=256` and `B=4096`, changing
`--batch-size` and `--output`.

Run SVD-UKF CPU compiled timing with:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py --mode compiled-timing --backend tf_svd_ukf --device-scope cpu --device /CPU:0 --expect-device-kind cpu --batch-size 20 --time-steps 200 --state-dim 10 --obs-dim 10 --parameter-dim 2 --warmups 3 --repeats 10 --output docs/benchmarks/experimental-batched-svd-ukf-compiled-cpu-b20-t200-n10-m10-2026-06-14.json
```

Repeat the same CPU command for SVD-UKF `B=256` and `B=4096`, changing
`--batch-size` and `--output`.

Run scalar-loop CPU compiled comparator commands after the corresponding
batched CPU commands.  Exact mode names may be patched during harness repair,
but the commands must produce the scalar-loop artifacts listed above or an
explicit infeasibility artifact:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py --mode scalar-compiled-loop --device-scope cpu --device /CPU:0 --expect-device-kind cpu --batch-size 20 --time-steps 200 --state-dim 10 --obs-dim 10 --parameter-dim 2 --warmups 3 --repeats 10 --output docs/benchmarks/experimental-scalar-loop-kalman-compiled-cpu-b20-t200-n10-m10-2026-06-14.json
```

Repeat the same scalar-loop CPU command for Kalman `B=256` and `B=4096`.

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py --mode scalar-compiled-loop --backend tf_svd_ukf --device-scope cpu --device /CPU:0 --expect-device-kind cpu --batch-size 20 --time-steps 200 --state-dim 10 --obs-dim 10 --parameter-dim 2 --warmups 3 --repeats 10 --output docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-cpu-b20-t200-n10-m10-2026-06-14.json
```

Repeat the same scalar-loop CPU command for SVD-UKF `B=256` and `B=4096`.

GPU benchmark commands require trusted execution because they initialize CUDA:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py --mode compiled-timing --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --batch-size 20 --time-steps 200 --state-dim 10 --obs-dim 10 --parameter-dim 2 --warmups 3 --repeats 10 --output docs/benchmarks/experimental-batched-kalman-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json
```

Repeat the same trusted GPU command for Kalman `B=256` and `B=4096`, changing
`--batch-size` and `--output`.

Run SVD-UKF GPU compiled timing with:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py --mode compiled-timing --backend tf_svd_ukf --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --batch-size 20 --time-steps 200 --state-dim 10 --obs-dim 10 --parameter-dim 2 --warmups 3 --repeats 10 --output docs/benchmarks/experimental-batched-svd-ukf-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json
```

Repeat the same trusted GPU command for SVD-UKF `B=256` and `B=4096`, changing
`--batch-size` and `--output`.

Run scalar-loop GPU compiled comparator commands only after a successful
trusted compiled batched GPU run and only if the scalar authority path compiles:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py --mode scalar-compiled-loop --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --batch-size 20 --time-steps 200 --state-dim 10 --obs-dim 10 --parameter-dim 2 --warmups 3 --repeats 10 --output docs/benchmarks/experimental-scalar-loop-kalman-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json
```

Repeat the same scalar-loop GPU command for Kalman `B=256` and `B=4096`, or
write infeasibility artifacts if XLA compilation fails before timing.

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py --mode scalar-compiled-loop --backend tf_svd_ukf --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --batch-size 20 --time-steps 200 --state-dim 10 --obs-dim 10 --parameter-dim 2 --warmups 3 --repeats 10 --output docs/benchmarks/experimental-scalar-loop-svd-ukf-compiled-gpu1-b20-t200-n10-m10-2026-06-14.json
```

Repeat the same scalar-loop GPU command for SVD-UKF `B=256` and `B=4096`, or
write infeasibility artifacts if XLA compilation fails before timing.

Use `timeout` around long benchmark commands if needed.  A timeout is a capacity
or feasibility result when the command is otherwise well formed; it is not a
reason to change pass/fail criteria after seeing results.

### Review

- Claude Opus max effort must review this subplan read-only before execution.
- Claude must receive paths and bounded questions, not the whole file pasted in
  prompt text.
- If Claude requests a fixable revision, patch this same subplan visibly and
  rerun focused plan checks.
- Stop after five rounds for the same material blocker.
- Claude is not an execution authority and cannot authorize GPU, default,
  scientific-claim, funding, model-file, or product-capability boundary
  crossing.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | For realistic filtering dimensions, what is the compiled CPU/GPU behavior of experimental batched Kalman and SVD-UKF value+score relative to scalar-loop comparators where feasible? |
| Baseline/comparator | Scalar-loop production authority paths over the same deterministic fixture rows; batched compiled CPU; batched compiled GPU; previous parity tests. |
| Primary pass criterion | Harness repairs and tests pass; all GPU performance commands use JIT/XLA compiled paths in trusted context; benchmark JSON artifacts record compile time, warm timing, finite outputs, shapes, and device placement; scalar-loop comparator timing or infeasibility artifacts are recorded. |
| Promotion veto diagnostics | GPU benchmark run without JIT; wrong device placement; nonfinite outputs; required JSON missing/malformed; Phase 1-3 tests regress; public export/default edit; scalar parity failure in existing tests; unsupported broad speedup or production-readiness claim. |
| Continuation veto diagnostics | TensorFlow environment cannot import; benchmark harness cannot be repaired without modifying production exports/defaults; trusted GPU initialization unavailable after escalation; Claude/Codex subplan review does not converge after five rounds. |
| Explanatory diagnostics | Compile time, first-call time, warm-call median/mean/min/max, per-filter median, capacity timeout, memory/placement messages, scalar-GPU infeasibility errors. |
| Not concluded | No production default readiness, no downstream HMC/NeuTra throughput claim, no sampler convergence/posterior quality claim, no CUT4 readiness, no broad GPU superiority beyond this fixture and these batch sizes. |
| Artifact preserving result | Benchmark JSON files, Phase 4 result file, tests, source audit output, Claude review artifacts. |

## Forbidden Claims And Actions

- Do not run or report GPU performance comparisons unless the measured function
  is `@tf.function(jit_compile=True)`.
- Do not use eager GPU timing as CPU/GPU speed evidence.
- Do not compare batched GPU to scalar CPU as a broad speedup claim if scalar
  GPU compiled comparator is infeasible; only report it as a cross-device
  descriptive diagnostic.
- Do not claim production readiness, default readiness, or HMC/NeuTra
  downstream readiness.
- Do not include CUT4 in default-promotion scope.
- Do not edit public exports or production default selectors.
- Do not overwrite unrelated dirty worktree changes.
- Do not install packages, fetch network resources, commit, push, or run
  destructive filesystem/git commands.
- Do not let Claude edit files or authorize execution.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if:

- Claude review of this subplan converges with `VERDICT: AGREE`.
- Required local tests pass after benchmark harness repair.
- Public API guard passes.
- Benchmark JSON artifacts exist for every completed command.
- Any missing `B=4096`, scalar-loop CPU comparator, or scalar-loop GPU
  comparator artifact is explained as a capacity, timeout, or XLA-feasibility
  result with command/error evidence.
- Phase 4 result separates hard vetoes, viable paths, descriptive-only timing,
  and nonclaims.
- Phase 5 subplan exists and includes objective, inherited entry conditions,
  required artifacts, checks/tests/reviews, evidence contract, forbidden
  claims/actions, handoff conditions, and stop conditions.
- Phase 5 subplan explicitly audits downstream HMC/NeuTra gate status before
  making any downstream readiness claim.

## Stop Conditions

Stop and write a blocker result if:

- Kalman compiled timing cannot be added without changing production exports or
  default behavior.
- GPU timing would require eager execution to produce a benchmark comparison.
- Trusted GPU context is unavailable after the required escalation.
- Any required local correctness or public API test fails and cannot be repaired
  within Phase 4 scope.
- Benchmark output has nonfinite values or wrong device placement.
- Existing Phase 1-3 tests regress.
- Claude review does not converge after five rounds for the same material
  blocker.
- Continuing would require package installation, network access, credentials,
  destructive git/filesystem action, production default changes, or modifying
  unrelated dirty worktree changes.

## End-Of-Phase Procedure

1. Run the required local checks.
2. Write the Phase 4 result / close record with a decision table and run
   manifest.
3. Draft or refresh the Phase 5 downstream harness subplan.
4. Review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, downstream boundary safety, and scientific-claim safety.
5. Send material Phase 5 subplan questions to Claude as read-only review before
   execution.
