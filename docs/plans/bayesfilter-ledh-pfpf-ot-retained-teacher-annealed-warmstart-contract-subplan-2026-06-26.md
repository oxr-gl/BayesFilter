# Subplan: Phase A contract lock for annealed retained-teacher warm-start

## Parent program
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-learned-warmstart-repair-master-program-2026-06-26.md`

## Purpose
Freeze the exact mathematical and implementation contract for the annealed retained-
teacher learned warm-start route before any teacher-data generation, training, or new
benchmarking is attempted.

## Question
What exact object is the annealed student allowed to learn, what normalization or
canonicalization is part of that object, what remains auxiliary only, and what exact
criterion will later count as correctness-preserving on the real LEDH-PFPF-OT route?

## Why this subplan comes first
The current learned branch is blocked partly because the target object is still too
loose. If we generate data or train before freezing the contract, we risk building a
pipeline around the wrong latent state and drifting into non-comparable artifacts.

## Scope
- In scope:
  - exact target object for the annealed route,
  - normalization / canonicalization policy,
  - meaning of `valid_mask`,
  - distinction among learned object, optimized object, auxiliary objects, and deployed object,
  - correctness envelope for later Phase E qualification.
- Out of scope:
  - data generation implementation,
  - checkpoint saving/loading,
  - training hyperparameter search,
  - benchmark reruns.

## Required decisions

### 1. Target object
Freeze whether the student predicts the raw annealed warm-start state:
- `(a_y, b_x, a_x, b_y, valid_mask)`
or a normalized/canonicalized variant.

### 2. Representation convention
State exactly how the benchmark-side `scaled_post_flow`, `normalized_log_weights`, and
`epsilon` are encoded before prediction, and whether that encoding is itself part of the
student contract.

### 3. Auxiliary vs deployed distinction
Record explicitly:
- learned object: warm-start latent state,
- optimized object: student parameters under the chosen teacher-aligned objective,
- auxiliary object: annealed teacher solver state / diagnostics,
- deployed object: corrected retained-teacher transport output after the warm start is
  consumed by the annealed solver.

### 4. Correctness envelope
Freeze what later counts as correctness-preserving:
- paired replay RMSE threshold,
- paired replay max-abs threshold,
- row residual threshold,
- column residual threshold,
- no route drift,
- same barycentric-output semantics,
- finite outputs.

### 5. Allowed training target(s)
Decide whether training is against:
- latent-state loss only,
- replay-sensitive loss only,
- or a combined objective where replay-sensitive heldout metrics are mandatory at
  evaluation time.

## Frozen Phase A contract note
This committed section is the Phase A contract note future phases should quote verbatim.

### Route boundary
This contract applies only to the benchmarked streaming retained-teacher LEDH-PFPF-OT path that constructs `scaled_post_flow` / `normalized_log_weights`, calls the warm-start function, and passes `warmstart_state` into the streaming annealed transport core. It does not automatically govern every annealed-transport wrapper in the repo.

### Frozen learned object
- Learned numeric target: `(a_y, b_x, a_x, b_y)`.
- `valid_mask` is not a learned numeric target. It is a route-supplied batch-row applicability flag attached to the packaged warm-start state.
- The deployed route consumes `AnnealedTransportWarmstartStateTF(a_y, b_x, a_x, b_y, valid_mask)`.

### Frozen input representation
- The student-facing input contract is the caller-side representation:
  - `scaled_post_flow = (post_flow - mean(post_flow)) / std(post_flow)` with per-dimension std floor `1e-12`,
  - `normalized_log_weights = log(normalize(exp(log_weights)))`,
  - scalar `epsilon`,
  - batch-row `valid_mask`.
- The transport solver's internal filterflow scaling is a separate solver detail and is not the student input contract.

### Output canonicalization policy
- The frozen target tensors `(a_y, b_x, a_x, b_y)` are the raw executable warm-start latent state as consumed by the current solver.
- No extra post-prediction normalization / canonicalization is part of this Phase A contract beyond dtype-safe packaging into `AnnealedTransportWarmstartStateTF`.

### Auxiliary vs deployed distinction
- learned object: warm-start latent state `(a_y, b_x, a_x, b_y)`,
- auxiliary route field: `valid_mask`,
- optimized object: student parameters after training,
- auxiliary teacher object: annealed solver state / diagnostics used to generate targets or audits,
- deployed object: corrected retained-teacher transport output after the streaming annealed solver consumes the warm-start state.

### Frozen correctness envelope for later Phase E qualification
The learned arm is correctness-preserving only if all of the following hold relative to the frozen cold same-route comparator:
- `finite_output == true`,
- same route family / same barycentric-output semantics,
- same device kind, precision mode, compiled / JIT mode, compiled unit, plan mode, transport policy, particle count, and transport settings,
- checkpoint-backed learned mode only: checkpoint provenance recorded, checkpoint load successful, and no random-stub allowance used,
- absolute veto thresholds:
  - `teacher_replay_rmse <= 1e-5`,
  - `teacher_replay_max_abs <= 1e-4`,
  - `max_row_residual <= 9e-3`,
  - `max_column_residual <= 1e-9`,
- relative admissibility versus the same-rung heuristic arm:
  - `teacher_replay_rmse <= 3.0 * heuristic teacher_replay_rmse`,
  - `teacher_replay_max_abs <= 3.0 * heuristic teacher_replay_max_abs`,
  - `max_row_residual <= 1.15 * heuristic max_row_residual`,
  - `max_column_residual` remains subject to the absolute veto because the current heuristic reference is `0.0`.

These numerical thresholds are branch-local admissibility gates anchored to the repaired Phase 2 evidence. They freeze promotion policy for this repair branch; they are not universal scientific tolerances.

### Frozen training-target policy
- The allowed training target family is a combined objective:
  - latent-state supervision on `(a_y, b_x, a_x, b_y)` is allowed,
  - replay-sensitive heldout metrics are mandatory at evaluation time,
  - latent-only improvement is never sufficient for promotion.

### Minimum Phase B teacher-data fields implied by this contract
Each example must preserve at least:
- student inputs: `scaled_post_flow`, `normalized_log_weights`, `epsilon`, `valid_mask`,
- latent targets: `a_y`, `b_x`, `a_x`, `b_y`,
- same-route provenance metadata: route family, transport settings, precision mode, compiled / JIT mode, shape envelope, seed policy, and target-object convention identifier.

## Deliverable
This committed section is the contract note future phases should quote verbatim.

## Evidence contract
### Primary criterion
This subplan succeeds only if the target object is specified tightly enough that two
future researchers would generate the same teacher data and evaluate the same learned
checkpoint against the same correctness contract.

### Veto diagnostics
- ambiguous target object,
- ambiguous normalization,
- learned/deployed object confusion,
- hidden route change smuggled in as “normalization,”
- correctness criteria too weak to detect teacher drift.

### Explanatory-only diagnostics
- convenience of one target over another,
- elegance of parameterization,
- architectural taste.

### Non-claims
This subplan does not claim the chosen target is effective, only that it is explicit
and stable enough to support later data generation and training.

## Grounding files to inspect while executing
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/batched_annealed_warmstart_student_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-phase2-correctness-result-2026-06-25.md`
- `docs/plans/bayesfilter-neural-ot-retained-teacher-first-pass-implementation-plan-2026-06-18.md`

## Verification
This subplan is complete only if it answers:
1. what exactly is predicted,
2. in what normalized form,
3. what is only auxiliary,
4. what gets deployed,
5. what later metric thresholds define correctness.

## Advancement rule
Do not start Phase B teacher-data generation until this contract is written and treated
as frozen.
