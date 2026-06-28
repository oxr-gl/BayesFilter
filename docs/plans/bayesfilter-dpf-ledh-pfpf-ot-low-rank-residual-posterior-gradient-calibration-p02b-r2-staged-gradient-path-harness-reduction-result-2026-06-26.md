# P02B-R2 Staged Gradient Path Harness Reduction Result

Date: 2026-06-26

Status: `SMALL_TRUSTED_GPU_PASS_FULL_P02_SHAPE_NOT_RUN`

## Summary

P02B-R2 traced the P02B-R blocker to diagnostic harness pressure rather than a
confirmed route/solver issue: the old staged readout created one compiled
function per seed and stage group, returned full checkpoint tensors, and the
visible-GPU P02B-R reruns previously emitted slow XLA compile or retracing
warnings without writing an artifact.

The R2 harness now uses one compact staged function per seed.  It preserves the
same whole-sum gradient localization question while returning only compact
value summaries plus gradients.  The CPU-hidden artifact used a non-default
`--no-jit-compile` debug exception; the small visible-GPU artifact used the same
non-JIT exception only because it was the bounded R2 probe, not the repo
default.  No low-rank solver, route, posterior, default, or public API path was
changed.

Claude reviewed the R2 plan read-only and returned `VERDICT: AGREE`.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Engineering question | Answered for the reduced-shape harness: compact staged readout can produce a trusted visible-GPU artifact. |
| Baseline/comparator | P02B-R result dated 2026-06-25: CPU-hidden passed; full visible-GPU and smaller visible-GPU attempts did not land artifacts. |
| Primary pass/fail criterion | Passed for compile, targeted test, CPU-hidden artifact, and one bounded small visible-GPU artifact. |
| Veto diagnostics | No CPU-hidden or small visible-GPU artifact vetoes fired. |
| Explanatory diagnostics | The small visible-GPU run completed in 211.958 seconds, so full P02-shape execution was not launched under the R2 stop rule. |
| What must not be concluded | No low-rank solver repair, posterior correctness, HMC readiness, residual-threshold calibration, P03 handoff, statistical superiority, default/package/public API readiness, or scientific validity. |

## Commands And Outcomes

Plan review:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --name p02b-r2-harness-reduction-plan-review \
  "Read-only skeptical review..."
```

Outcome: `VERDICT: AGREE`.

Local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_staged_gradient_path.py -q
```

Outcome: syntax check passed; pytest passed with `2 passed` in 75.50 seconds
and TensorFlow/gast deprecation warnings.

CPU-hidden artifact:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py \
  --seed-probes 91001:center \
  --num-particles 8 \
  --time-steps 2 \
  --low-rank-rank 4 \
  --low-rank-max-projection-iterations 4 \
  --particle-chunk-size 4 \
  --dtype float32 \
  --tf32-mode disabled \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --no-jit-compile \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-cpu-hidden-debug-2026-06-26.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-cpu-hidden-debug-2026-06-26.md \
  --quiet
```

Outcome: `PASS`; evidence class `cpu_hidden_debug_only`; no artifact vetoes;
no diagnostic findings; wall time 69.135 seconds; first expected-connected
break `no_observed_expected_connected_break`.  This was a non-default JIT-off
debug exception under the repo policy.

Small visible-GPU artifact:

```bash
timeout 240s env CUDA_VISIBLE_DEVICES=1 python docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py \
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
  --no-jit-compile \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-small-visible-gpu-2026-06-26.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-small-visible-gpu-2026-06-26.md \
  --quiet
```

Outcome: `PASS`; evidence class
`owner_designated_managed_session_visible_gpu_trusted`; no artifact vetoes; no
diagnostic findings; wall time 211.958 seconds; first expected-connected break
`no_observed_expected_connected_break` for both `91003:center` and
`91002:qr_plus`.  This was also a non-default JIT-off debug exception, not the
repo execution default.

Full P02 shape was not launched.  The small no-JIT visible-GPU run consumed most
of the 240-second bound; launching `N=1024`, `T=12`, `it=120` would likely test
the time envelope rather than produce a discriminating artifact.

## Artifacts

| Artifact | Status |
| --- | --- |
| `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-cpu-hidden-debug-2026-06-26.json` | `PASS` |
| `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-cpu-hidden-debug-2026-06-26.md` | Preserved summary |
| `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-small-visible-gpu-2026-06-26.json` | `PASS` |
| `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-small-visible-gpu-2026-06-26.md` | Preserved summary |

## Hypothesis Review

| Hypothesis | Result |
| --- | --- |
| H1: repeated staged `tf.function` creation caused visible-GPU retracing pressure | Supported for the reduced shape: one compiled staged readout per seed landed a trusted visible-GPU artifact. Runtime remains high, so this is not full-shape evidence. |
| H2: returning full checkpoint tensors inflated compile/runtime pressure | Supported as an engineering lever: compact summaries preserved schema and produced CPU-hidden plus small visible-GPU artifacts. |
| H3: primary same/separated tape readout is not the main blocker | Not resolved. R2 compacted staged readout only; if full-shape remains blocked, primary A/B route repetitions are the next harness suspect. |
| H4: SIR passing evidence does not contradict the LGSSM posterior-parameter broken path | Preserved. SIR route tests are forward/residual coverage, and the SIR gradient smoke targets `initial_particles`, not posterior `theta`. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Keep the compact staged harness and treat it as the current R2 diagnostic path. | Passed for reduced-shape trusted GPU artifact. | No vetoes fired for CPU-hidden or small visible-GPU artifacts. | Whether full P02-shape localization can land without further harness reduction. | Reduce primary A/B route repetitions or add a staged-only/full-shape mode before trying the original P02 shape again. | No route repair, posterior correctness, HMC readiness, P03 handoff, threshold calibration, default readiness, or scientific validity. |

## Inference Status

| Row | Status |
| --- | --- |
| Hard veto screen | Passed for CPU-hidden and small trusted-GPU R2 artifacts. |
| Statistically supported ranking | None; no stochastic method ranking was attempted. |
| Descriptive-only differences | Gradient values, wall times, and same/separated gradient differences are descriptive only. |
| Default-readiness | Not assessed. |
| Next evidence needed | A full-shape or carefully reduced full-probe artifact that lands under a reviewed bound, likely after removing repeated primary route executions. |

## Post-Run Red-Team Note

Strongest alternative explanation: the compact staged path fixed enough harness
pressure for the reduced shape, but the remaining full-shape blocker may still
be primary A/B repeated route execution, route cost, or XLA/no-JIT execution
cost rather than staged tensor return volume alone.

What would overturn this result: a full P02-shape compact artifact that times
out or emits retracing/compile warnings before staged readout, or a compact
artifact that shows a missing stage or disconnected direct scaled covariance
gradient.

Weakest evidence: the trusted GPU artifact is small (`N=128`, `T=3`, `it=40`)
and no-JIT.  It does not reproduce the original P02 full shape
(`N=1024`, `T=12`, `it=120`) or certify the original broken path.
