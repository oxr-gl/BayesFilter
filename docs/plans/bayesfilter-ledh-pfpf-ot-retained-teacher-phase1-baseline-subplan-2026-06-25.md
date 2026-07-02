# Subplan: LEDH-PFPF-OT retained-teacher Phase 1 baseline rung

## Parent program
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md`

## Purpose
Establish the exact same-route cold / zero-init LEDH-PFPF-OT baseline as a trusted
reference artifact before any retained-teacher comparison is interpreted.

## Question
Can we run the exact batched streaming LEDH-PFPF-OT reference lane under the frozen
GPU/JIT/precision contract and obtain a finite, trusted, semantics-preserving baseline
artifact?

## Scope
- Arm: `cold` / `zero-init` only
- Route: exact same batched streaming LEDH-PFPF-OT path
- Device: trusted GPU only for the primary rung
- JIT mode: compiled / `tf.function(jit_compile=True)` required for benchmark evidence
- Precision: `float32` with TF32 **disabled** for the primary baseline rung unless a later subplan explicitly opens a TF32 descriptive branch
- Seeds: fixed and recorded
- Particle counts: primary rung at `N=50000`, with smaller pilot counts used only if the primary rung itself cannot execute cleanly
- Proposal mode: `callback`
- Transport policy: `active-all`

## Frozen baseline contract
Must match the master program exactly:
- same GPU device
- same JIT mode
- same precision mode
- same seeds
- same particle counts
- same transport settings
- same cost and barycentric output rule

## Hard pass gates
- finite outputs
- trusted requested device evidence
- memory growth applied before execution
- same declared transport route
- residual contract satisfied
- same barycentric semantics preserved
- no fallback off intended GPU/JIT path

## Diagnostics
Primary:
- finite-output flag
- trusted device execution
- residual summary
- route metadata
- warm-call median seconds

Secondary:
- compile + first-call seconds
- warm-call timing list
- GPU memory before/after
- shape echo and transport settings echo

## Expected failure modes
- route accidentally differs from the frozen reference lane
- GPU fallback or untrusted device execution
- JIT disabled or silently bypassed
- non-finite outputs at target particle count
- residual failure even before warm-start comparison begins

## What would change our mind
- If the exact baseline itself is unstable or route-ambiguous, later retained-teacher phases should be postponed and the baseline lane must be repaired first.
- If the 50k rung itself is not executable, record smaller pilot counts only as diagnostics and do not quietly upgrade them into the baseline claim.

## Exact command bundle
```bash
# Primary baseline rung: 50k particles, exact same-route cold / zero-init baseline
CUDA_VISIBLE_DEVICES=0 python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode disabled \
  --proposal-mode callback \
  --transport-policy active-all \
  --num-particles 50000 \
  --warmstart-mode none \
  --output docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n50000_2026-06-25.json \
  --markdown-output docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n50000_2026-06-25.md

# Optional diagnostic pilots if the 50k rung fails to execute cleanly; these are not promotable
CUDA_VISIBLE_DEVICES=0 python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode disabled \
  --proposal-mode callback \
  --transport-policy active-all \
  --num-particles 10000 \
  --warmstart-mode none \
  --output docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n10000_2026-06-25.json \
  --markdown-output docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n10000_2026-06-25.md

CUDA_VISIBLE_DEVICES=0 python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode disabled \
  --proposal-mode callback \
  --transport-policy active-all \
  --num-particles 20000 \
  --warmstart-mode none \
  --output docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n20000_2026-06-25.json \
  --markdown-output docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n20000_2026-06-25.md
```

## Interpretation rule
- If the 50k baseline rung passes all hard gates, Phase 1 is certified and later phases may use this artifact as the frozen comparator.
- If the 50k baseline rung fails, record any 10k/20k pilot runs as diagnostics only and do not advance to retained-teacher comparison until the exact-route primary rung is either repaired or explicitly re-scoped by a new reviewed plan.
