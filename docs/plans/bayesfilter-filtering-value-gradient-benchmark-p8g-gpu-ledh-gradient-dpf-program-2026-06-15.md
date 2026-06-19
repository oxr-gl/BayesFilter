# P8g Program: GPU-First LEDH/DPF Value And Gradient Implementation

Date: 2026-06-15

Status: `REVIEWED_READY_FOR_IMPLEMENTATION`

## Scope

This program supersedes the value-only P8f tuning plan as the next executable
DPF lane. P8f remains useful as a particle-count tuning component, but the real
target is a GPU-first, gradient-bearing LEDH/DPF implementation that can support
HMC-facing work.

The program covers:

1. replace `N=8` wiring evidence with tuned particle-count evidence;
2. implement the reviewed DPF tuning gates from P8f inside this broader GPU
   program;
3. add or explicitly block missing KSC and Spatial SIR DPF callbacks;
4. make LEDH gradients a first-class deliverable, not an afterthought;
5. regenerate stale P8d artifacts only after value and gradient gates are
   honest;
6. make GPU execution the default serious implementation path, with CPU used
   only for smoke, parity, and debugging.

This program does not enter the monograph rewrite lane and does not claim
Zhao-Cui source-faithful TT/SIRT behavior unless a separate source-anchor gate
authorizes it.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the current P8 DPF/LEDH lane become a GPU-executable, gradient-bearing implementation whose fixed-randomness/no-resampling LEDH surrogate objective is suitable for HMC diagnostic integrator tests, with tuned particle counts and honest artifacts? |
| Baseline/comparator | P8e repaired CPU-only P8d runner, where LEDH SV-style rows are finite at `N=8` but ESS collapses near 1 and no DPF gradient is certified. |
| Primary criterion | A GPU-backed LEDH value/gradient objective passes CPU/GPU parity on smoke horizons, finite multi-seed full-horizon value gates, fixed-randomness gradient checks, and diagnostic HMC integrator checks for the fixed-randomness/no-resampling surrogate objective, while non-ready rows remain explicit blockers. |
| Veto diagnostics | GPU unavailable after trusted probe; GPU path silently falls back to CPU for serious runs; Python particle loops dominate the supposedly GPU path; gradients pass through stochastic resampling or changing random streams without a fixed-branch contract; finite value is treated as gradient correctness; noisy fixed-seed gradients are promoted to HMC readiness; `N=8` is treated as serious evidence; KSC/Spatial SIR callbacks are fabricated without target-contract metadata; stale P8d artifacts are reused as current evidence. |
| Explanatory diagnostics | GPU device manifest, CPU/GPU parity deltas, per-kernel/runtime profiles, value MC SE, relative ESS, adjacent-rung stability, fixed-seed gradient finite-difference checks, common-random-number gradient variance, and short HMC tier diagnostics. |
| Not concluded | No HMC-facing claim for the stochastic PF target; no production HMC readiness; no exact nonlinear PF likelihood proof; no source-faithful Zhao-Cui TT/SIRT claim; no filter ranking before value and gradient gates both pass. |
| Artifacts | P8g plan/result docs, GPU probe manifest, vectorization/profile notes, tuning artifacts, gradient validation artifacts, refreshed P8d JSON/CSV/Markdown artifacts, and HMC-readiness tier manifest. |

## Skeptical Plan Audit

- Wrong-baseline risk: P8g must build from the repaired current Algorithm 1
  code, not historical LEDH-PFPF-OT results.
- Proxy-metric risk: ESS, MC SE, gradient finite-difference agreement, and short
  HMC chains are gates and diagnostics, not final scientific validation by
  themselves.
- Missing-stop risk: stop on GPU probe failure, CPU fallback, non-vectorized
  bottlenecks that make the path unusable, non-finite gradients, unstable
  fixed-randomness gradients, or callback target ambiguity.
- Unfair-comparison risk: particle counts may differ by algorithm/row. A global
  default is allowed only after every retained row passes its own tuning gate.
- Hidden-assumption risk: an HMC-facing DPF objective must freeze random streams,
  branch choices, and resampling policy or use a reviewed differentiable
  relaxation. The stochastic PF estimator itself is not automatically a smooth
  HMC target.
- Artifact-answer risk: refreshed P8d artifacts must separate value,
  gradient/HMC readiness, blocked callbacks, and nonclaims.

Audit status: `PASS_FOR_DRAFT_REVIEW`. Claude read-only review rounds 1, 2, 3,
and 4 returned `VERDICT: REVISE`; this revision narrows the fixed-branch
contract to the live `resampling_route="none"` path, adds operational GPU
promote/stop thresholds, preserves staged feasibility before full ladders,
requires a graph/batched-kernel acceptance gate, constrains HMC language to
diagnostic integrator compatibility for the fixed-randomness/no-resampling
surrogate objective, requires a canonical per-row optimization coordinate,
requires downstream GPU artifacts to cite the trusted G0 probe manifest,
requires artifacts to record the exact stateless seed/salt contract, and
preserves blocked rows in all refreshed output schemas. No conceptual issue
currently requires human intervention, but GPU execution and any expansion to
stochastic-target or production HMC claims remain explicit approval/review
boundaries.

## Review Record

Claude read-only local-file review:

- Round 1: `VERDICT: REVISE`.
- Round 2: `VERDICT: REVISE`.
- Round 3: `VERDICT: REVISE`.
- Round 4: `VERDICT: REVISE`.
- Round 5: `VERDICT: AGREE`.

Material fixes applied during review:

- narrowed the gradient target to the live no-resampling fixed-randomness LEDH
  objective;
- constrained HMC language to diagnostic integrator compatibility for the
  augmented conditional surrogate objective;
- added graph/batched-kernel GPU route acceptance, speedup, and no-CPU-fallback
  gates;
- restored staged GPU prefix ladders before full-horizon tuning;
- required canonical per-row optimization/HMC coordinates and transform
  metadata;
- required exact stateless seed/salt schedule artifacts;
- required downstream GPU artifacts to cite the trusted G0 probe manifest;
- required KSC and Spatial SIR blocked rows to remain present in every refreshed
  JSON/CSV/Markdown table schema.

## Conceptual Boundary

There is one important conceptual distinction:

- `stochastic_pf_estimator`: changing random streams or stochastic branch
  choices make the objective unsuitable as a naive HMC potential.
- `fixed_randomness_no_resampling_ledh_objective`: the live current route uses
  `resampling_route="none"`. Initial random normals, transition random normals,
  and the pseudo-time schedule are fixed. There are no resampling decisions or
  ancestor-resampling branches in this executable target.
- `future_resampling_gradient_objective`: any gradient that includes classical
  resampling, relaxed resampling, OT transport, or differentiable ancestor
  choices is a separate reviewed subplan, not part of this P8g certification.

P8g targets the no-resampling fixed-randomness object for LEDH gradients. The
artifact must not claim it is the exact stochastic PF marginal likelihood unless
a later derivation and validation gate establishes that relationship.

## Phase G0: GPU Device And Backend Gate

Goal: establish the trusted GPU baseline before implementation.

Required actions:

1. Run escalated `nvidia-smi`.
2. Run an escalated TensorFlow GPU device probe in the active environment.
3. Record CUDA, driver, TensorFlow, TFP, XLA, GPU name, memory, and visible
   device count.
4. Run a tiny TensorFlow matmul and a tiny `tf.function(jit_compile=True)` probe
   on GPU.
5. Write `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md`.

Stop if trusted GPU probe fails. Non-escalated GPU failures are sandbox evidence
only and do not diagnose the machine.

Every later GPU seriousness gate, tuning result, gradient result, or refreshed
P8d artifact must cite this G0 trusted probe manifest. A GPU-labeled artifact
without that citation is blocked, even if local CPU-only compile/pytest checks
pass.

## Phase G1: Current Bottleneck Profile

Goal: prove where CPU time is going before rewriting.

Required actions:

1. Profile the current P8d LEDH SV full-horizon path at small `N` on CPU and
   GPU, with explicit CPU/GPU status.
2. Identify Python loops over time, particles, sigma points, and seeds.
3. Record whether TensorFlow executes serious kernels on GPU or returns to CPU.
4. Write a profile note with the first vectorization targets.

Expected issue: `li_coates_ledh_alg1_time_step_tf` loops over particles in
Python and stores Python diagnostics, so GPU enablement alone will not be
enough.

Promote/stop threshold:

- promote to G2 implementation only if profiling identifies a concrete batched
  TensorFlow rewrite target whose estimated runtime can plausibly support at
  least a five-seed full-horizon `N=32` LEDH SV-style gate within a recorded
  per-cell budget;
- stop with `BLOCK_P8G_GPU_PROFILE_NO_ADMISSIBLE_VECTOR_TARGET` if profiling
  shows serious GPU runs are dominated by unvectorizable Python control flow or
  silent CPU fallback.

## Phase G2: Vectorized GPU Algorithm 1 Core

Goal: make Algorithm 1 LEDH GPU-native enough for real ladder and gradient work.

Implementation tasks:

1. Add a vectorized `tf.function`/TensorFlow implementation for per-particle
   UKF prediction/update and LEDH coefficients.
2. Replace Python particle loops with batched tensor operations where the state
   dimension is static.
3. Keep a compatibility wrapper so the existing P8d route can call the GPU path
   without changing model definitions.
4. Keep the existing CPU implementation as a reference path for smoke parity.
5. Avoid NumPy in differentiable algorithmic paths.
6. Record route identifiers that distinguish:
   - `algorithm1_cpu_reference`;
   - `algorithm1_gpu_vectorized_value`;
   - `algorithm1_gpu_vectorized_fixed_branch_gradient`.

Code-path acceptance gate:

- the serious GPU route must remove the Python particle loop from the promoted
  execution path;
- pseudo-time stepping must be graph/batch compatible or explicitly bounded and
  shown not to dominate runtime;
- profiler evidence must show batched TensorFlow kernels on the GPU for the
  expensive per-particle linear algebra;
- a wrapper that merely places `tf.function` around residual Python
  particle-loop structure is not sufficient for promotion.

Pass criteria:

- CPU/GPU smoke parity on LGSSM and the two SV-style rows for short horizons;
- finite particles, determinants, covariances, corrected weights, and ESS;
- runtime improvement is at least `5x` over the current CPU reference on the
  same short-horizon LEDH SV-style smoke, or a reviewed profile note justifies a
  lower threshold with projected full-horizon feasibility;
- a five-seed full-horizon `N=32` LEDH SV-style pilot is projected to fit inside
  the recorded per-cell runtime budget before G4 full laddering starts;
- no silent CPU fallback for serious GPU gate commands.

## Phase G3: LEDH Fixed-Branch Gradient Objective

Goal: build the gradient-bearing object needed for HMC.

Implementation tasks:

1. Define an explicit objective function
   `ledh_no_resampling_fixed_randomness_log_likelihood(theta, fixed_randomness, schedule, row_id, particle_count)`.
2. Freeze or materialize:
   - initial random normals;
   - transition random normals;
   - the exact stateless seed/salt schedule used to generate those normals,
     including base seeds, salt constants, time-index mapping, row callback
     family, and any callback-version/checksum identifier needed to reproduce
     the stream;
   - pseudo-time schedule;
   - model row and observation stream;
   - particle count and seed set.
3. Require `resampling_route="none"` for P8g gradient certification.
4. Use TensorFlow autodiff over physical/unconstrained theta as declared by the
   row.
5. Expose score vectors and optional Hessian-vector products; full Hessians are
   not required for initial HMC readiness.
6. Preserve true raw SV correction likelihood for actual SV/generalized-SV rows
   while keeping the P8e flow surrogate metadata.

Pass criteria:

- gradient is non-`None`, finite, and shape-correct;
- each row declares one canonical optimization/HMC coordinate before gradient
  checks run;
- the artifact records the forward transform from source/truth parameters to
  the canonical coordinate and whether any Jacobian term is included in the
  objective;
- CPU/GPU parity and finite-difference directional checks are performed in the
  same canonical coordinate that the HMC diagnostic uses;
- a gradient that passes only in a different parameterization is not promoted;
- repeated calls with the same fixed randomness are bitwise or tolerance-stable;
- finite-difference directional checks pass on short horizons;
- common-random-number seed variation is quantified before any HMC claim;
- any gradient involving resampling, transport, or differentiable ancestor
  choices is blocked into a future reviewed subplan.

## Phase G4: Particle Count Tuning Under GPU Path

Goal: replace `N=8` with tuned value counts using the reviewed P8f gates.

Required actions:

1. Implement a ladder runner with per-cell artifact fields:
   `tuning_status`, `selected_particle_count`, `selection_rule`,
   `selection_rung`, `next_rung_checked`, `next_rung_particle_count`,
   `adjacent_mean_delta`, `adjacent_combined_mc_se`, `min_relative_ess`,
   `mean_relative_ess`, `runtime_budget_status`, and `blocker_reason`.
2. Run GPU Stage 0 smoke/prefix gates:
   - horizon prefixes `[50, 200]`;
   - `N in [16, 32]`;
   - one algorithm/row cell at a time;
   - explicit GPU device and no-CPU-fallback diagnostics.
3. Authorize full-horizon laddering only for cells whose Stage 0 runtime
   projects below the recorded per-cell budget and whose finite/relative-ESS
   diagnostics are not already hopeless.
4. Run full-horizon GPU ladder one algorithm/row at a time.
5. Select the smallest count that passes finite, relative-ESS, MC-SE, and
   next-rung stability checks.
6. Block rather than guess if no count passes.

Rows:

- bootstrap DPF: LGSSM, actual SV, predator-prey, generalized SV;
- LEDH Algorithm 1: LGSSM, actual SV, predator-prey, generalized SV.

KSC and Spatial SIR remain callback-pending until Phase G5.

Pre-G5 artifact rule: any P8g artifact emitted before G5 must still include KSC
and Spatial SIR DPF rows as explicit callback-blocked rows. A smaller executed
roster must not look like a complete DPF matrix.

The blocked-row rule applies to every emitted format: JSON cells, value CSV,
score/gradient CSV, curvature/HMC-readiness CSV when present, status CSV,
uncertainty/tuning CSV, and Markdown summary tables.

## Phase G5: Missing Callback Closure

Goal: resolve KSC and Spatial SIR DPF gaps honestly.

KSC tasks:

1. Add bootstrap and LEDH callbacks only for the declared KSC Gaussian-mixture
   surrogate target.
2. Preserve metadata: surrogate target, not native SV.
3. Decide whether LEDH flow uses a mixture-moment Gaussian adapter or a blocked
   route; do not silently collapse mixture identity.

Spatial SIR tasks:

1. Start with bootstrap feasibility under GPU and source-row observation model.
2. Review whether LEDH has a valid additive/Gaussian observation adapter for
   this row.
3. Block LEDH Spatial SIR if the adapter would be an unreviewed invention or if
   dimension/runtime makes the route unsafe.

Pass criteria:

- every KSC/Spatial SIR DPF cell is either executed with explicit target
  metadata or blocked with a reason code;
- no Zhao-Cui source-faithful claim is emitted from these callback repairs.

## Phase G6: HMC-Facing Gradient Tiers

Goal: decide whether the LEDH fixed-randomness/no-resampling GPU surrogate
objective is compatible with diagnostic HMC integrator checks.

Required tiers:

1. `TIER_1_FINITE_VALUE_SCORE`: finite value and score on short and full rows.
2. `TIER_2_DIRECTIONAL_GRADIENT`: finite-difference directional checks with
   fixed randomness on smoke horizons.
3. `TIER_3_LEAPFROG_REVERSIBILITY`: Hamiltonian leapfrog reversibility and
   energy-error diagnostics on the fixed-randomness/no-resampling conditional
   surrogate objective, with random draws, pseudo-time schedule, row, particle
   count, and canonical parameter coordinate held fixed across the trajectory.
4. `TIER_4_SHORT_CHAIN_DIAGNOSTIC`: short HMC chain diagnostics, explicitly
   non-production.

Promotion boundary:

- Tier 1 and Tier 2 are not HMC readiness by themselves.
- Tier 3 establishes diagnostic integrator compatibility only for the
  augmented conditional surrogate objective with frozen auxiliary data, not
  HMC-facing readiness for the stochastic PF target and not a theta-only
  marginal PF objective.
- Tier 4 may justify a longer surrogate-objective HMC plan, not production
  readiness and not stochastic-target HMC readiness.

## Phase G7: Refresh P8d Artifacts

Goal: replace stale P8d outputs only after GPU/value/gradient gates are honest.

Required actions:

1. Regenerate JSON/CSV/Markdown value tables with tuned DPF particle counts.
2. Add separate gradient/HMC readiness tables or fields; do not overload the
   value table.
3. Preserve blocked cells for callback gaps, gradient gaps, GPU blockers, or
   HMC tier failures.
   KSC and Spatial SIR DPF rows must remain present as callback-blocked until
   G5 explicitly executes or blocks them.
   This requirement applies to every refreshed output table/schema, not only
   the narrative result note.
4. Write the final P8g result and a next subplan if any gate remains blocked.

## Local Checks

Every implementation phase must update and run focused checks before execution
artifacts are promoted:

```bash
python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q
git diff --check
```

GPU phases additionally require escalated GPU probes and GPU run manifests.

## Human Intervention Points

No conceptual intervention is required before drafting and reviewing this plan.

Ask for approval before:

- running GPU/CUDA commands, because local policy requires trusted escalation;
- converting any diagnostic fixed-branch LEDH gradient into a production HMC
  readiness claim;
- adding a differentiable resampling relaxation if it changes the mathematical
  objective;
- claiming any Zhao-Cui source-faithful route.

## Stop Conditions

- Trusted GPU probe fails.
- Vectorized GPU path cannot avoid Python particle-loop bottlenecks.
- GPU smoke speedup is below the recorded promote threshold and no reviewed
  feasibility exception is written.
- GPU Stage 0 prefix ladder projects infeasible full-horizon runtime.
- CPU/GPU parity fails beyond tolerance.
- Fixed-branch gradient is non-finite, unstable, or finite-difference checks
  fail.
- Particle ladder does not converge by the reviewed maximum count.
- Callback closure requires unreviewed model/data changes.
- HMC tiers fail but artifacts try to claim HMC readiness anyway.
