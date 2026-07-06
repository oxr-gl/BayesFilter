# P02B-R Staged Gradient Path Diagnostic Result

Date: 2026-06-25

Status: `CPU_HIDDEN_PASS_TRUSTED_GPU_ARTIFACT_BLOCKED`

## Summary

The staged P02B-R diagnostic was implemented, reviewed, and executed.
The CPU-hidden debug lane passed and produced preserved JSON/Markdown artifacts.
Those artifacts show connected finite gradients for the staged whole-sum
readouts on the small CPU-hidden probe, with no observed expected-connected
break.

The trusted visible-GPU full-shape run did not produce a JSON/Markdown artifact
within a bounded wait.  The full-shape attempt hit a very slow XLA compile path.
The smaller visible-GPU rerun also failed to complete within the bounded window
and emitted a TensorFlow retracing warning before being stopped.  So the GPU
artifact blocker remains.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Partially answered: the staged CPU-hidden harness works, but the trusted visible-GPU full-shape localization artifact was not produced. |
| Baseline/comparator | P02/P02A failing-probe artifacts, P02B route-internal blocker note, and the SIR code inventory. |
| Primary criterion | Met only for CPU-hidden schema/debug execution. Not met for the trusted visible-GPU artifact. |
| Veto diagnostics | Fired for the GPU lane: no artifact within bounded wait; full-shape run hit very slow XLA compile; smaller rerun hit retracing/runtime pressure. |
| Explanatory diagnostics | CPU-hidden gradient summaries are finite/connected; H6 inventory confirms SIR tests are not the same gradient path. |
| What must not be concluded | No repair, no posterior correctness, no HMC readiness, no default readiness, no statistical superiority, no scientific validity, no P03 handoff. |

## Commands And Outcomes

CPU-hidden test and artifact:

```bash
python -m py_compile docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_staged_gradient_path.py -q
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
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r-staged-gradient-path-cpu-hidden-debug-2026-06-25.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r-staged-gradient-path-cpu-hidden-debug-2026-06-25.md \
  --quiet
```

Preserved artifacts:

- `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r-staged-gradient-path-cpu-hidden-debug-2026-06-25.json`
- `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r-staged-gradient-path-cpu-hidden-debug-2026-06-25.md`

Trusted visible-GPU attempt:

```bash
CUDA_VISIBLE_DEVICES=1 python docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py \
  --seed-probes 91003:center,91002:qr_plus \
  --num-particles 1024 \
  --time-steps 12 \
  --low-rank-rank 16 \
  --low-rank-assignment-epsilon 0.25 \
  --low-rank-alpha 1.0e-8 \
  --low-rank-max-projection-iterations 120 \
  --particle-chunk-size 64 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r-staged-gradient-path-2026-06-25.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r-staged-gradient-path-2026-06-25.md \
  --quiet
```

Outcome: no artifact before bounded stop; run was terminated after very slow XLA
compile. A smaller visible-GPU rerun also failed to finish inside the bounded
window and was stopped.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Working tree | Dirty before and after this phase; unrelated pre-existing changes were preserved. |
| CPU-hidden evidence class | `cpu_hidden_debug_only` |
| GPU trust basis | `owner_designated_managed_session_visible_gpu_trusted` for attempted GPU runs only |
| CPU-hidden TF32 | `False` |
| CPU-hidden JIT | `False` |
| CPU-hidden device | `/CPU:0` |
| GPU device requested | `/GPU:0` on visible GPU 1 |

## Outcome Table

| Question | Answer |
| --- | --- |
| Did the CPU-hidden staged harness work? | Yes. |
| Did it support a tape-artifact claim? | No. Same-tape and separated-tape gradients both stayed connected and finite on the small CPU-hidden probe. |
| Did it localize an expected-connected break? | No. The CPU-hidden debug probe observed no expected-connected break. |
| Did the trusted GPU full-shape artifact land? | No. |
| Did the smaller visible-GPU rerun land? | No. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Keep the staged harness as a valid CPU-hidden localization tool, but stop short of claiming trusted GPU evidence. | CPU-hidden criterion passed; trusted GPU criterion failed. | GPU artifact veto fired: slow XLA compile / retracing-runtime pressure with no artifact. | Whether a further reduction in retracing or stage grouping would allow a trusted GPU artifact. | If another GPU run is worth trying, reduce retracing by reusing compiled stage functions more aggressively or split the stages into a smaller visible-GPU artifact. | No repair, no posterior correctness, no HMC readiness, no default readiness, no scientific validity. |

## Inference Status

| Row | Status |
| --- | --- |
| Hard veto screen | CPU-hidden passed; trusted-GPU artifact veto failed. |
| Statistically supported ranking | None. |
| Descriptive-only differences | CPU-hidden gradient magnitudes and residuals are descriptive only. |
| Default-readiness | Not assessed. |
| Next evidence needed | A trusted visible-GPU artifact that completes on the reviewed stage set without the compile/retracing blocker. |

## Claude Execution Review

Claude `p02b-r-staged-gradient-path-plan-review-r1` returned `VERDICT: AGREE`.

## Post-Run Red-Team Note

Strongest alternative explanation: the GPU blocker is a harness compile/retracing
problem, not a route problem. That is consistent with the current evidence.

What would overturn the blocker: a trusted visible-GPU artifact with the same
stage set and the same P02 failing probes.

Weakest evidence: the GPU side still has no artifact, so no GPU-localized first
break is yet established.
