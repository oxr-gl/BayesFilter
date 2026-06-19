# Retained-Teacher Neural OT First-Pass Implementation Plan

Date: 2026-06-18

metadata_date: 2026-06-18

## Context

The neural-OT survey phase is closed. The first BayesFilter implementation pass
should stay narrow and implementation-bearing:

> retain the finite entropic OT / Sinkhorn teacher,
> learn only a solver-internal warm start,
> keep corrective Sinkhorn refinement in the deployed loop.

This plan treats the mathematical reference as fixed by:
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
- `docs/chapters/ch32d_retained_teacher_neural_ot.tex`

and it does **not** reopen the broader neural-OT survey unless a specific
implementation gap forces it.

## Question

What is the narrowest BayesFilter-native first implementation of the
retained-teacher neural OT route that:
1. predicts an explicit latent teacher object,
2. uses the local fixed-target Sinkhorn lane as the authoritative teacher,
3. preserves corrective Sinkhorn refinement in deployment,
4. names the exact implementation files,
5. and defines minimal verification gates before any broader training or
   promotion claim?

## Scope

### In scope
- TensorFlow / TensorFlow Probability only.
- The current fixed-target finite Sinkhorn equal-weighting path.
- Teacher latent export, student warm-start prediction, retained corrective
  refinement, and downstream scalar smoke checks.
- LGSSM as the first fixture lane.
- Deterministic seeds, fixed particle count, fixed epsilon, and explicit
  manifests.

### Out of scope for the first pass
- Direct-map ICNN/Brenier implementations.
- Dynamic/path/operator OT implementations.
- FNO/grid/image-style neural operators.
- Broad cross-model benchmarking.
- Claims about posterior correctness, HMC readiness, or general deployment.

## Evidence Contract

### Engineering question
Can a learned warm start for the retained finite Sinkhorn teacher reduce the
correction burden while preserving the declared teacher object and the local
scalar/residual contracts?

### Exact baseline
The baseline is the **zero-initialized BayesFilter fixed-target Sinkhorn route**
already implemented in:
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`

### Primary promotion criterion
On held-out fixed-envelope clouds, the **student-warm-started corrected route**
must:
- satisfy the same row/column/total-mass residual contract as the zero-init
  retained teacher,
- reproduce the teacher barycentric cloud at least as well as zero-init under
  the same corrective budget or residual target,
- and preserve same-executed-scalar gradient coherence on the declared smoke
  scalar.

### Veto diagnostics
- residual failure (row, column, or total mass),
- nonfinite latent/coupling/particles/scalars,
- teacher/object drift (different cost, target marginal, or solver contract),
- same-scalar GradientTape vs finite-difference mismatch,
- zero-init non-regression failure after warm-start refactor.

### Explanatory-only diagnostics
- runtime,
- raw latent prediction loss,
- gradient norms,
- iteration counts without residual parity,
- teacher/student latent MSE by itself.

### What is not concluded even if this pass succeeds
- posterior correctness,
- HMC target correctness,
- broad filtering superiority,
- cross-model generalization,
- or student replacement of the teacher.

## Skeptical Audit Before Execution

Status: `PASSED_FOR_NARROW_FIRST_PASS`

Main risks checked before implementation:
1. **Wrong mathematical object** — guarded by attaching only to the local
   fixed-target Sinkhorn equal-weighting lane, not the annealed-transport lane.
2. **Gauge non-identifiability** — guarded by supervising a canonicalized
   log-domain latent rather than an arbitrary dual representation.
3. **Proxy-speed promotion** — guarded by requiring teacher-cloud fidelity and
   residual parity, not just lower iteration counts.
4. **Permutation drift** — guarded by choosing a particle-set-native student
   architecture rather than flattened order-sensitive inputs.
5. **Teacher/object drift** — guarded by using the same finite BayesFilter
   Sinkhorn implementation for teacher generation and deployment correction.
6. **Over-claiming** — guarded by a narrow LGSSM-first envelope and explicit
   non-claims.

## Core Decisions

### 1. Exact latent teacher object
Predict the teacher’s **gauge-fixed log-domain Sinkhorn state** `(log_u, log_v)`.

Reasoning:
- the current solver already computes `log_u` and `log_v` internally,
- the chapters explicitly name dual/scaling coordinates as the right student
  target class,
- predicting logs is numerically cleaner than predicting raw positive scalings,
- predicting the coupling or barycentric cloud would be too broad for the first
  retained-teacher pass.

### 2. Gauge convention
Use a deterministic canonicalization so the supervised target is unique while the
represented coupling remains unchanged.

Recommended convention:
- `c = mean(log_u)`
- `log_u_canon = log_u - c`
- `log_v_canon = log_v + c`

This enforces `mean(log_u_canon) = 0` and preserves the same coupling.

### 3. External conceptual anchor
Use **Meta OT** as the primary conceptual anchor.

Reason:
- its central pattern is “predict solver-relevant potential state, then initialize
  a retained OT solve,” which is the closest conceptual match to the BayesFilter
  teacher/student route.

Use **UNOT** only as a secondary donor of ideas:
- log-scaling prediction,
- optional epsilon conditioning later,
- gauge-aware losses.

Do not import UNOT’s grid/FNO representation assumptions into the first pass.

## BayesFilter-Native Teacher-Data Generation Loop

First-pass envelope:
- LGSSM only,
- fixed `N`, fixed `epsilon`, fixed seeds,
- deterministic fixtures,
- teacher clouds captured before OT equal-weighting.

Loop:
1. Build deterministic LGSSM fixtures and observation paths.
2. Run the BayesFilter weighted particle path up to the pre-resampling cloud.
3. Capture for each chosen cloud:
   - particles `X`,
   - normalized weights `w`,
   - seed / fixture checksum / model checksum,
   - epsilon,
   - particle count,
   - whether the cloud came from the actual resampling trigger path.
4. Solve the **local fixed-target Sinkhorn teacher** with a stricter teacher
   budget than deployment.
5. Export:
   - final raw `(log_u, log_v)`,
   - canonicalized `(log_u, log_v)`,
   - coupling checksum and/or coupling payload,
   - barycentric teacher cloud,
   - row/column/total-mass residuals,
   - iterations used,
   - manifest metadata.
6. Split by deterministic fixture/seed into train and held-out sets.
7. Train the student only on the canonicalized latent.
8. Deploy by predicting the latent, replaying it as the retained solver
   initialization, and running a smaller corrective budget `K_corr`.

## Implementation Sequence

### Step A — expose warm-start state in the retained teacher
Modify:
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`

Changes:
- extend the result object to return final `log_u` and `log_v`,
- add optional warm-start inputs (`initial_log_u`, `initial_log_v` or
  equivalent `initial_state`),
- add latent canonicalization helper(s),
- preserve zero-init wrapper behavior for current callers,
- record initialization policy in diagnostics.

Reused logic:
- current cost construction,
- current residual diagnostics,
- current barycentric projection.

### Step B — add the BayesFilter-owned student module
Add:
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`

Contents:
- a config dataclass,
- a small permutation-aware DeepSets-style predictor,
- latent post-processing into canonicalized `(log_u, log_v)`,
- teacher-state loss helper,
- optional held-out latent replay helper.

### Step C — add teacher-data generation runner
Add:
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_teacher_data_tf.py`

Responsibilities:
- fixture-driven cloud capture,
- teacher solve and dataset manifest,
- artifact writing via `common_tf.py`,
- train/held-out split summary,
- residual and checksum summaries.

### Step D — integrate the warm-started retained teacher into the filter
Modify:
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`

Changes:
- add a new `transport_method`, e.g.
  `retained_teacher_sinkhorn_warmstart`,
- keep `annealed_transport` and `fixed_target_sinkhorn` unchanged,
- call the student predictor only inside the new branch,
- pass predicted latent into the corrected Sinkhorn solve,
- emit explicit diagnostics showing “student warm start + retained Sinkhorn
  correction”.

Boundary rule:
- the first neural OT implementation attaches to the **fixed-target Sinkhorn**
  lane only,
- not to `annealed_transport_tf.py`.

### Step E — add downstream scalar smoke-check runner
Add:
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_scalar_checks_tf.py`

Responsibilities:
- same-executed-scalar GradientTape vs finite-difference smoke check,
- manifest and reproducibility digest,
- explicit non-claims,
- teacher vs warm-started corrected route comparison on the declared scalar.

## Recommended File Boundaries

### Teacher generation / retained solver
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_teacher_data_tf.py`

### Student prediction
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`

### Corrective refinement in deployed filter loop
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`

### Downstream scalar checks and manifests
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_scalar_checks_tf.py`
- reused helpers in `experiments/dpf_implementation/tf_tfp/runners/common_tf.py`

### Reused fixture / contract substrate
- `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_gradient_checks_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_v2_bootstrap_ot_values_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_v2_bootstrap_ot_gradients_tf.py`

## Minimal Verification Gates

### Gate 1 — zero-init non-regression
Refactored warm-start-capable Sinkhorn must reproduce current zero-init behavior
on fixed clouds.

Check:
- same coupling within tight tolerance,
- same barycentric cloud within tight tolerance,
- same residual envelope,
- same finite/nonfinite behavior.

### Gate 2 — latent canonicalization round trip
Canonicalizing `(log_u, log_v)` and replaying that state through the retained
solver interface must leave the represented coupling and barycentric cloud
unchanged within tight tolerance.

### Gate 3 — teacher reproducibility
On fixed fixture and seed:
- same cloud checksum,
- same canonicalized teacher latent checksum,
- same residual diagnostics within declared tolerance,
- manifest records epsilon, iteration budget, initialization policy, and
  stabilization policy.

### Gate 4 — teacher-init replay
Using the exported teacher latent as the corrective-solver initialization on
held-out clouds must reproduce the teacher cloud under the declared budget and
residual envelope. This verifies the warm-start wiring before student claims.

### Gate 5 — corrected student vs zero-init baseline
At fixed corrective budget on held-out clouds:
- student-warm-started corrected route must satisfy the same residual contract,
- corrected student cloud must be no worse than zero-init against the teacher
  cloud,
- any iteration-benefit claim must be reported only alongside residual parity or
  explicit teacher-cloud discrepancy.

### Gate 6 — downstream scalar smoke check
Run a same-executed-scalar GradientTape vs finite-difference check through the
integrated warm-started corrected route.

Rule:
- the gradient claim is only local numerical evidence for the executed scalar,
  not posterior/HMC validation.

## Planned Commands / Environment (post-implementation)

All verification commands should run CPU-only for the first pass by setting
`CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.

Planned command family after code lands:
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_teacher_data_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_scalar_checks_tf
```

If a dedicated non-regression runner is added, it should also run CPU-only and
write its output under the existing TF/TFP reports/outputs structure.

## Success Criterion For This First Pass

This first implementation pass is successful if it ends with:
1. a BayesFilter-owned warm-start-capable retained Sinkhorn solver,
2. a documented and reproducible teacher latent dataset path,
3. a minimal particle-set-native student module,
4. an opt-in retained-teacher warm-start branch in `dpf_ot_tf.py`,
5. zero-init non-regression and teacher-replay checks passing,
6. and a downstream same-scalar smoke check through the integrated path.

## What Would Change the Next Step

Advance to broader experiments only if the first-pass gates pass.

If the pass fails, the next step depends on the failure class:
- **solver refactor failure** → fix retained-teacher API before any student work,
- **gauge/canonicalization instability** → revise the latent target definition,
- **student helps latent loss but not corrected teacher-cloud fidelity** → keep
  the teacher, simplify the student, or reduce claim scope,
- **scalar-check mismatch** → debug the executed graph before any promotion
  claim,
- **representation failure under permutation tests** → revise architecture before
  expanding the envelope.

## What Is Not Concluded

This plan does not conclude that retained-teacher neural OT is ready to replace
the BayesFilter teacher, that it preserves posterior/HMC correctness, or that
Meta OT or UNOT should be ported wholesale. It only fixes the narrowest
BayesFilter-native first implementation route and its local verification gates.
