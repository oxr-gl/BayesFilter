# P02B-R3 XLA Graph Reduction Plan

Date: 2026-06-26

## Research Intent Ledger

Main question: can the P02B staged gradient-path diagnostic reduce XLA
compile/first-call wall time by making the LGSSM route time recursion a
TensorFlow loop body and by avoiding repeated primary route readouts?

Mechanism under test: replace the Python-unrolled route time loop with
`tf.while_loop`; make the compact staged readout the default diagnostic readout;
keep the older primary-and-staged A/B readout as an explicit heavier mode.

Expected failure mode: XLA may still spend too long compiling the nested LEDH
chunk loop and low-rank Dykstra loop, or the loop-carried checkpoint tensors may
introduce a new XLA shape/control-flow error.

Promotion criterion: a reduced-shape visible-GPU XLA/JIT staged-only artifact
lands under the bounded command and records finite route/stage diagnostics with
no artifact vetoes.

Promotion veto: artifact missing, nonzero command exit, non-finite route
outputs, missing required staged checkpoints, direct scaled covariance gradient
disconnected, or GPU output missing when GPU is expected.

Continuation veto: syntax/test failure that indicates the harness no longer
preserves required staged checkpoints, or a TensorFlow/XLA error caused by the
refactor rather than by time budget.

Repair trigger: timeout or excessive wall time without artifact after the loop
refactor triggers further readout splitting or smaller checkpoint carries before
attempting full P02 shape.

Explanatory diagnostics: total artifact wall time, per-row staged compiled
call/readout time, TensorFlow/XLA log messages, and route invocation counts.

What must not be concluded: no low-rank solver repair, no posterior correctness,
no HMC readiness, no residual threshold calibration, no statistical superiority,
no package/public API/default readiness, and no broad scientific validity.

## Evidence Contract

Question: does the route-loop/readout refactor reduce the graph-size pressure
enough for a bounded JIT diagnostic artifact?

Baseline/comparator: P02B-R2 small visible-GPU non-JIT artifact took 211.958s
at `N=128`, `T=3`, rank 16, 40 projection iterations and was explicitly
non-default debug evidence; the previous full-shape JIT path compiled too
slowly to be useful.

Primary pass/fail criterion: the reduced-shape visible-GPU JIT staged-only run
writes JSON/Markdown artifacts with status `PASS` under the timeout.

Veto diagnostics: command timeout/failure, missing artifact, artifact vetoes,
non-finite route outputs, missing required stages, missing GPU output when
expected, disconnected `scaled_Q` or `scaled_R` whole-sum gradients.

Explanatory-only diagnostics: exact wall time, per-row first-call/readout time,
gradient values, and XLA log text. These do not establish scientific validity.

Artifact: `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r3-xla-graph-reduction-*.json`
and matching Markdown plus a result note under `docs/plans`.

## Skeptical Plan Audit

Wrong baseline: the direct comparator is a no-JIT R2 artifact, not proof that
JIT is faster. The run will be interpreted as bounded viability evidence only.

Proxy metrics: wall time and first-call/readout time are engineering diagnostics,
not promotion criteria for the scientific filter.

Stop conditions: use bounded commands; if reduced JIT still times out, stop and
record the failure rather than launching full P02 shape.

Unfair comparison: shape and seed settings will be recorded exactly; any
comparison to R2 must note that R2 was no-JIT and pre-refactor.

Hidden assumptions: the route math should remain equivalent except for control
flow representation. Tests and staged checkpoint presence guard this, but do not
prove posterior correctness.

Environment mismatch: visible-GPU runs must record CUDA visibility, device,
TF32, JIT, TensorFlow versions, and managed-session GPU trust basis.

Artifact relevance: the planned artifacts directly answer whether the reduced
JIT diagnostic lands and how long it takes; they do not answer full P02 shape
readiness unless a full-shape run is separately executed.

Audit decision: proceed with the bounded refactor and reduced-shape JIT timing
artifact.

## Planned Commands

```bash
python -m py_compile docs/benchmarks/benchmark_low_rank_ledh_route_internal_gradient_connectivity.py docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_staged_gradient_path.py tests/test_low_rank_ledh_route_internal_gradient_connectivity.py -q
timeout 300s env CUDA_VISIBLE_DEVICES=1 python docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py \
  --readout-mode staged-only \
  --seed-probes 91003:center,91002:qr_plus \
  --num-particles 128 \
  --time-steps 3 \
  --low-rank-rank 16 \
  --low-rank-assignment-epsilon 0.25 \
  --low-rank-alpha 1.0e-8 \
  --low-rank-max-projection-iterations 40 \
  --particle-chunk-size 64 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r3-xla-graph-reduction-small-visible-gpu-jit-2026-06-26.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r3-xla-graph-reduction-small-visible-gpu-jit-2026-06-26.md \
  --quiet
```
