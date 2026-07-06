# P02 Reference, No-NumPy, And Implementation-Path Audit Result

Date: 2026-06-24

Status: `PASS_P02_READY_FOR_P03_GPU_APPROVAL`

## Phase Summary

P02 completed the local-check-only implementation-path audit for the locked
actual-SIR d18 low-rank candidate `r16_eps0p25_alpha1em08_it120`.

The active candidate path is the TensorFlow solver route in
`experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
called from
`docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py` through
`low_rank_coupling_solver_resample_tensors_tf(...)`.

P02 found no NumPy or `.numpy()` implementation barrier in the active solver
path or the active low-rank compiled harness region. Reporting and test
conversions remain outside the active implementation path. The older
`low_rank_coupling_transport_tf.py` fixture contains eager `.numpy()` diagnostics
and remains excluded from the default-certification candidate path.

P02 did not run a GPU benchmark, change defaults, change public API, change
algorithmic code, or make default-readiness, performance, HMC, posterior,
dense-equivalence, or scientific claims.

## Skeptical Plan Audit

| Audit item | P02 status |
| --- | --- |
| Wrong baseline | Guarded: P02 used the current streaming GPU/TF32 route as comparator context and did not introduce a new baseline. |
| Proxy metric promoted | Guarded: P02 did not use timing as a promotion criterion. |
| Missing stop conditions | Guarded: no active-path NumPy/`.numpy()`, fixture confusion, dense materialization, failed checks, or unsupported claim was found. |
| Unfair comparison | Guarded: P02 did not run a comparison; P03 must preserve paired runtime contracts. |
| Hidden assumptions | Guarded: P02 separated active solver path, reporting conversions, tests, and fixture route. |
| Stale context | Guarded: P02 reread current source/tests and started from P01 closeout. |
| Environment mismatch | Guarded: P02 did not initialize trusted GPU runtime. |
| Artifact mismatch | Guarded: P02 wrote this result and drafted the P03 subplan. |

Audit conclusion: P02 local-only execution was valid and sufficient to hand off
to a reviewed trusted-GPU P03 subplan, pending explicit approval for GPU
benchmark runtime.

## Implementation-Path Inventory

Active solver path:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
  imports TensorFlow and defines the active solver tensor route.
- `low_rank_coupling_solver_resample_tensors_tf(...)` returns tensor outputs,
  low-rank factors, factor diagnostics, and a zero-sized `transport_matrix`
  placeholder with shape suffix `[0, 0]`.
- The source contains no `import numpy`, no `np.`, and no `.numpy(`.
- The route uses TensorFlow tensor operations including `tf.cast`, `tf.exp`,
  `tf.gather`, `tf.einsum`, `tf.while_loop`, and TensorFlow reductions.

Active harness path:

- `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py` imports
  the solver tensor route and calls `low_rank_coupling_solver_resample_tensors_tf(...)`
  inside `_low_rank_value_core`.
- `_run_low_rank_compiled_core_timed` wraps the low-rank route in
  `tf.function(jit_compile=args.jit_compile, reduce_retracing=True)`.
- Argument validation requires `args.low_rank_timing_source == "compiled_core"`
  and `args.jit_compile is True`.
- The low-rank row hard-veto logic checks nonfinite values, route invocation
  count, dense materialization, final logsumexp residual, ESS floor, device
  kind, factor residual threshold, finite factors, finite particles,
  nonnegative factors, and positive `g`.

Reporting/test surfaces:

- The benchmark harness uses `.numpy()` after compiled tensors return to
  materialize timing rows, diagnostics, and JSON/Markdown artifacts.
- `tests/test_actual_sir_low_rank_tuning_grid.py` explicitly asserts no
  `import numpy`, no `np.`, and no `.numpy(` in the solver, and no `.numpy(`
  in the protected compiled harness region.
- Tests use NumPy assertions and `.numpy()` conversions as comparison fixtures;
  this is outside BayesFilter-owned algorithmic implementation.

Fixture exclusion:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_transport_tf.py`
  is an older transport-object fixture route.
- It contains eager `.numpy()` diagnostics and is not the locked candidate
  route for default certification.
- P03/P05 must not accidentally default to or benchmark this fixture as the
  candidate route.

## Required Checks

Completed checks:

- Solver/compiled-region source audit:
  - Result: pass, `errors=[]`.
  - Solver lines scanned: `538`.
  - Low-rank compiled region lines scanned: `178`.
- Focused NumPy/`.numpy()` scan:
  - Active solver path: no hits.
  - Protected compiled region: no hits.
  - Harness/reporting rows: `.numpy()` hits only after compiled outputs return
    and in JSON/reporting helpers.
  - Older fixture route: eager `.numpy()` hits found and explicitly excluded.
- Local syntax check:
  `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Focused tests:
  `python -m pytest tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `23 passed`.
  - Warnings: TensorFlow Probability/gast Python deprecation warnings only.
- P02 subplan Claude Opus/max review:
  - Round 1: `VERDICT: REVISE`.
  - Fixes: corrected JIT contract wording, added skeptical audit, named P03
    artifact, fixed stale status.
  - Round 2: `VERDICT: AGREE`.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P02 passes and can hand off to P03 trusted-GPU end-to-end benchmark subplan after human approval for GPU runtime |
| Primary criterion status | Passed: active candidate implementation path is source-anchored as TensorFlow/XLA-oriented, no NumPy/`.numpy()` barriers were found in solver/compiled path, reporting conversions are outside the compiled implementation path, and defaults/API remained untouched |
| Veto diagnostic status | No active-path NumPy import, `np.`, `.numpy(`, fixture confusion, dense active-route materialization, unidentified default surface, failed local test, or unsupported claim was found |
| Main uncertainty | P02 does not prove performance, default readiness, N4096 feasibility, HMC readiness, posterior correctness, dense equivalence, or scientific validity |
| Next justified action | Draft/review P03 and request approval for trusted GPU benchmark runtime |
| What is not being concluded | No default readiness, speedup, statistical ranking, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API readiness, N4096 feasibility, formal memory scaling, production readiness, or scientific validity |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for P02 implementation-path audit and focused local checks |
| Statistically supported ranking | None |
| Descriptive-only differences | None newly generated by P02 |
| Default-readiness | Not certified |
| Next evidence needed | P03 trusted-GPU actual-SIR d18 end-to-end benchmark evidence for locked candidate versus streaming comparator |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Commands | Solver/compiled-region audit; targeted `rg`; `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py`; `python -m pytest tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py -q`; Claude Opus/max read-only reviews |
| Environment | Local repository environment |
| CPU/GPU status | P02 did not initialize or use GPU benchmark runtime |
| Data version | Existing actual-SIR d18 harness source; no new benchmark data |
| Random seeds | N/A for P02 |
| Wall time | Local source/test audit only; N/A for new runtime |
| Output artifact paths | This P02 result, P03 subplan, updated ledgers |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p02-implementation-audit-subplan-2026-06-24.md` |
| Result file | This file |

## Post-Run Red-Team Note

The strongest alternative explanation is that P02 proves path hygiene, not that
the candidate helps LEDH in a full benchmark. The active path looks clean enough
to test under trusted GPU/XLA, but performance, resource envelope, robustness,
and default-policy readiness remain unproven. A later default switch would still
need P03/P04 runtime evidence and P05 approval.

## Handoff

Proceed to P03 only after explicit approval for trusted GPU benchmark runtime:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p03-end-to-end-benchmark-subplan-2026-06-24.md`
