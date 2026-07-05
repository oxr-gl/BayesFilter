# Experiment plan: LEDH-PFPF-OT retained-teacher neural OT effectiveness

## Question
Does a retained-teacher neural warm start improve the real batched streaming LEDH-PFPF-OT route at fixed corrective budget while preserving the declared finite entropic OT / Sinkhorn transport semantics?

## Mechanism being tested
This plan tests a narrow teacher-preserving mechanism:
- keep the current LEDH-PFPF-OT entropic OT / Sinkhorn correction route fixed,
- compare the exact same route under cold-start, heuristic warm start, and learned retained-teacher warm start,
- judge the learned route only by whether it reduces execution burden without changing the transport object or violating the teacher residual contract.

In particular, this is not a generic neural OT bakeoff. It is a direct test of whether a solver-native latent prediction can accelerate the current transport correction path.

## Scope
- Variant: batched streaming LEDH-PFPF-OT retained-teacher lane only
- Objective: runtime / correction-burden improvement at fixed transport semantics
- Seed(s): matched deterministic seeds between baseline and warm-start arms
- Training steps: use existing retained-teacher warm-start candidate(s); no new broad model-family search in the primary plan
- HMC/MCMC settings: N/A for the primary plan
- XLA/JIT mode: TensorFlow `tf.function(jit_compile=True)` for GPU comparison arms
- Device policy: trusted GPU execution only for the main effectiveness rung; CPU allowed only for smoke/reference checks
- Precision policy: FP64 reference when needed for fidelity comparison; FP32-no-TF32 as main performance lane; TF32 only as a descriptive later rung
- Transport route: exact same batched streaming LEDH-PFPF-OT path in all primary arms
- Corrective budgets: fixed matched budgets across cold, heuristic, and learned warm-start runs
- Expected runtime: >5 minutes for meaningful GPU/large-particle evaluation

## Evidence Contract

### Exact baseline
The baseline is the exact same-route cold / zero-init batched streaming LEDH-PFPF-OT lane under:
- same GPU device,
- same JIT/compiled mode,
- same precision mode,
- same seeds,
- same particle counts,
- same transport settings,
- same cost definition,
- and same barycentric output rule.

This should be treated as the retained entropic reference lane, not merely “the current implementation.”

### Primary effectiveness criterion
At fixed corrective budget on the real LEDH-PFPF-OT path, the warm-started route must:
- match or improve teacher-preservation discrepancy relative to cold-start,
- preserve the declared residual contract,
- and improve the primary runtime/iteration metric.

A practical first promotion threshold is:
- improved warm-call median time or reduced effective correction burden,
- with no residual or teacher-object regression beyond the declared tolerance envelope.

### Primary correctness-preservation criterion
The warm-started route must preserve:
- row/column or equivalent declared residual contract,
- no teacher/object drift,
- the same barycentric-output semantics,
- finite outputs,
- no hidden route change,
- and the same executed scalar/gradient path as applicable.

### Veto diagnostics
- non-finite outputs,
- fallback off the requested GPU/JIT path,
- memory-growth misconfiguration before execution,
- residual failure,
- teacher/object drift,
- barycentric-output mismatch caused by route change,
- runtime gain without fidelity parity,
- or unfair budget mismatch between baseline and warm-start arms.

### Explanatory-only diagnostics
- compile + first-call time,
- mean/min/max timing,
- GPU memory before/after,
- latent/state prediction loss,
- gradient norms,
- warm-start vs baseline iteration counts without residual parity,
- TF32 descriptive speed differences,
- smaller-particle pilot rungs.

### What will not be concluded even if the run passes
- posterior correctness,
- HMC readiness,
- production/default readiness,
- broad cross-model generalization,
- teacher replacement,
- dense-Sinkhorn equivalence for later approximate routes,
- or universal GPU speedup.

## Skeptical Audit Before Execution
Status: `PASSED_FOR_NARROW_LEDH_RETAINED_TEACHER_TEST`

Main risks checked before execution:
1. **Wrong baseline** — guarded by using exact same-route cold-start LEDH-PFPF-OT as the primary comparator.
2. **Semantic drift hidden by speed** — guarded by requiring residual parity and teacher-preservation discrepancy checks before runtime promotion.
3. **Proxy-metric promotion** — guarded by treating runtime as promotable only after transport-object preservation passes.
4. **Route mismatch** — guarded by fixing device, precision, seeds, transport settings, cost, and barycentric output semantics across arms.
5. **Overreading narrow retained-teacher evidence** — guarded by stating explicitly that existing support is strongest in low-budget/narrow heldout settings, not yet broad full-path wins.
6. **Precision confusion** — guarded by keeping FP64 as reference where fidelity matters and FP32-no-TF32 as the main performance lane.

## Diagnostics
Primary:
- warm-call median seconds,
- corrected teacher-cloud replay discrepancy / RMSE,
- residual parity under matched budget,
- finite-output flag,
- trusted requested device evidence,
- route metadata confirming exact same transport path.

Secondary:
- compile-and-first-call seconds,
- warm-call full timing list,
- GPU memory snapshots,
- latent/state prediction loss,
- student-vs-baseline iteration count differences,
- descriptive TF32 timing deltas.

Sanity checks:
- memory growth applied before execution,
- identical benchmark shape and transport settings between arms,
- same seed schedule,
- same precision mode recorded,
- no accidental switch from retained-teacher lane to a semantic-changing route.

## Candidate set for the primary plan
Primary arms:
- `cold` / `zero-init`
- `heuristic` warm start
- `learned` retained-teacher warm start
- optionally `learned_base` vs `learned_wide` if an ablation rung is cheap and already supported by existing artifacts

Deferred to later branches only:
- positive-feature kernels,
- low-rank couplings,
- direct learned maps,
- dynamic/operator methods.

## Expected failure modes
- learned warm start reduces latent loss but not corrected LEDH-PFPF-OT replay discrepancy,
- warm start helps only at tiny budgets and disappears on the real route,
- GPU/JIT path nullifies practical savings,
- heuristic warm start matches the learned arm closely enough that the neural route is not justified,
- residual parity is lost when runtime improves,
- the full batched route exposes object drift not visible in narrower fixed-target heldout tests.

## What would change our mind
- If learned warm start fails teacher-preservation or residual parity, the retained-teacher effectiveness claim does not pass.
- If learned warm start is finite and teacher-consistent but does not improve runtime or correction burden on the real LEDH path, it remains a research option rather than a promoted route.
- If a semantic-changing comparator later beats retained-teacher methods while preserving downstream constraints under its own evidence contract, then the ranking can be revisited — but not before that separate contract is written and passed.

## Command
```bash
# Exact same-route baseline arm
CUDA_VISIBLE_DEVICES=0 python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode disabled \
  --proposal-mode callback \
  --transport-policy active-all \
  --num-particles <N> \
  --warmstart-mode none \
  --output <cold_json> \
  --markdown-output <cold_md>

# Heuristic warm-start arm
CUDA_VISIBLE_DEVICES=0 python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode disabled \
  --proposal-mode callback \
  --transport-policy active-all \
  --num-particles <N> \
  --warmstart-mode heuristic \
  --output <heuristic_json> \
  --markdown-output <heuristic_md>

# Learned warm-start arm
CUDA_VISIBLE_DEVICES=0 python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode disabled \
  --proposal-mode callback \
  --transport-policy active-all \
  --num-particles <N> \
  --warmstart-mode learned \
  --output <learned_json> \
  --markdown-output <learned_md>
```

## Interpretation rule
- If the learned warm-start arm preserves the declared residual and teacher-preservation contracts and improves the primary runtime/correction metric relative to cold-start at fixed budget, the retained-teacher effectiveness test passes for that rung.
- If the learned arm is finite but sub-threshold on improvement, record it as non-promoted narrow evidence rather than a success claim.
- If heuristic and learned are statistically indistinguishable on the primary rung, prefer the simpler heuristic lane until stronger evidence appears.
- If any semantic-changing route is later tested, it must be evaluated under a separate plan and not folded back into this retained-teacher claim.
