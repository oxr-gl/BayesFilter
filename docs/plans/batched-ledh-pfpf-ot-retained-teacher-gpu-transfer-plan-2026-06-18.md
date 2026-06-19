# Experiment plan: batched LEDH-PFPF-OT retained-teacher GPU transfer and 50k speed test

## Question
Does a retained-teacher warm-start attached to the actual batched annealed-transport LEDH-PFPF-OT path preserve the declared batched target semantics and materially reduce warm-call wall-clock time at 50k particles on the streaming TF32 GPU lane?

## Mechanism being tested
This experiment transfers the retained-teacher idea into the batched annealed-transport path by:
- adding optional warm-start state plumbing to the batched annealed transport solver,
- exercising the streaming batched LEDH-PFPF-OT benchmark lane with cold-start and warm-start modes,
- enabling TensorFlow GPU memory growth before execution,
- measuring compile+first-call and repeated warm-call timing summaries at high particle counts.

## Scope
- Variant: batched LEDH-PFPF-OT streaming route, cold-start vs warm-start
- Objective: GPU/TF32 speed impact at large particle count while preserving finite batched execution
- Seed(s): benchmark seed 20260615 unless overridden in the command
- Training steps: N/A in this first transfer pass; warm-start modes are `none`, `heuristic`, or static learned initializer shape only
- HMC/MCMC settings: N/A
- XLA/JIT mode: TensorFlow `tf.function(jit_compile=True)` in the existing benchmark harness
- Expected runtime: can exceed 5 minutes for the 50k rung depending on GPU behavior
- Device policy: trusted GPU execution only
- Primary benchmark family: streaming LGSSM benchmark harness
- Particle target: 50,000

## Evidence Contract

### Exact baseline
Cold-start batched streaming LEDH-PFPF-OT on the same GPU, same TF32 mode, same seed, same tensor shapes, same transport settings, and same benchmark harness.

### Primary correctness criterion
Warm-start mode must preserve:
- finite outputs,
- trusted requested GPU execution,
- the same declared benchmark transport path,
- and successful benchmark completion without transport residual or shape failures.

### Primary speed criterion
At the 50k-particle streaming rung, warm-start mode should reduce **warm-call median seconds** by at least 20% relative to cold-start.

### Veto diagnostics
- missing trusted GPU evidence,
- GPU memory-growth not applied before execution,
- nonfinite output,
- benchmark falls back off the requested GPU path,
- warm-start path changes the transport route or benchmark semantics,
- no measurable speed improvement at 50k.

### Explanatory-only diagnostics
- compile+first-call time,
- warm-call mean/min/max,
- GPU memory before/after,
- smaller pilot rung timings,
- heuristic vs learned warm-start ranking if multiple warm-start modes are run.

### What will not be concluded even if the run passes
- posterior correctness,
- HMC readiness,
- broad production readiness,
- universal benefit on all models or particle counts,
- or that the current batched warm-start predictor is the final architecture.

## Diagnostics
Primary:
- warm-call timing summary seconds (median emphasized)
- trusted GPU evidence in the artifact
- finite output flag
- transport route metadata

Secondary:
- compile-and-first-call seconds
- GPU memory snapshots before/after
- warm-call full timing list
- smaller 10k/20k pilot timings if collected first

Sanity checks:
- memory growth applied before execution
- TF32 mode recorded
- logical/physical GPU visibility recorded
- identical benchmark shape/transport settings between cold-start and warm-start runs

## Expected failure modes
- warm-start plumbing only affects dense path but not streaming,
- warm-start changes no practical compute and therefore produces no speed benefit,
- 50k exceeds runtime or memory budget even with streaming,
- GPU execution succeeds but transport remains dominated by all-pairs compute so initialization savings are negligible.

## What would change our mind
- If the 50k rung shows no meaningful speed gain, the retained-teacher transfer into the batched annealed path is not yet justified as a future default on performance grounds.
- If speedup appears only at smaller particle counts, we should treat the 50k result as the binding criterion because that is the stated target.
- If the transfer is finite and GPU-correct but sub-threshold on speed, the route may still be useful as a research option but not a default-candidate speed win.

## Skeptical Audit Before Execution
Status: `PASSED_FOR_BATCHED_GPU_TRANSFER`

Checked risks:
1. **Algorithm mismatch** — the batched path uses annealed potentials, not fixed-target `(log_u, log_v)`, so the warm-start state is kept distinct.
2. **Streaming irrelevance risk** — the benchmark target is the streaming lane specifically, not the scalar comparator or dense-only path.
3. **Fake speedup risk** — baseline and warm-start runs must use identical benchmark settings except for warm-start mode.
4. **GPU-policy overreach** — GPU-by-default is scoped to this batched DPF/OT benchmark lane, not repo-wide import behavior.
5. **Memory policy mismatch** — memory growth must be configured before the benchmarked computation begins.

## Command
```bash
CUDA_VISIBLE_DEVICES=0 python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --proposal-mode callback \
  --transport-policy active-all \
  --num-particles 50000 \
  --warmstart-mode none \
  --output <cold_json> \
  --markdown-output <cold_md>

CUDA_VISIBLE_DEVICES=0 python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --proposal-mode callback \
  --transport-policy active-all \
  --num-particles 50000 \
  --warmstart-mode heuristic \
  --output <warm_json> \
  --markdown-output <warm_md>
```

## Interpretation rule
- If warm-start passes the correctness gates and improves warm-call median seconds by at least 20% at 50k particles, the batched retained-teacher transfer passes its first GPU/TF32 speed rung.
- If warm-start is finite but below the 20% threshold, record it as a non-passing transfer for the speed claim.
- If 50k itself is not executable, back off to smaller pilot counts for diagnosis but do not quietly promote those results as a 50k success.
