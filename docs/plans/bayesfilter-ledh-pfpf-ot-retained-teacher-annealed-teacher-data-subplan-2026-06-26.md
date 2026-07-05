# Subplan: Phase B annealed teacher-data generation for retained-teacher warm-start

## Parent program
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-learned-warmstart-repair-master-program-2026-06-26.md`

## Dependency
This subplan must follow:
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-annealed-warmstart-contract-subplan-2026-06-26.md`

No data generation should be treated as valid until the target object and correctness
contract in the Phase A subplan are frozen.

## Purpose
Define and generate a reproducible teacher-data artifact from the actual batched
streaming annealed LEDH-PFPF-OT route so that a learned retained-teacher checkpoint can
be trained against the correct route-specific teacher object.

## Question
How do we generate route-matched annealed teacher examples, with enough metadata and
split structure, so that the later learned student is trained on the right target and
can be evaluated against replay-sensitive correctness metrics?

## Scope
- In scope:
  - route-matched teacher-data generation,
  - manifest format,
  - train/validation/heldout split,
  - saved target object fields,
  - replay-oriented summaries needed later for qualification.
- Out of scope:
  - actual student training,
  - checkpoint loading,
  - Phase E/F benchmark reruns.

## Required outputs per example
Each teacher example should record, at minimum:
- the pre-transport state representation seen by the student,
- normalized/log-weight representation used by the contract,
- `epsilon` and any route-critical scalar settings,
- the teacher warm-start / solved-state object frozen by Phase A,
- enough route metadata to guarantee same-route provenance,
- and replay-oriented transport output summaries needed later for heldout evaluation.

If memory is a concern, prefer compact saved summaries and route-native teacher state
plus a small number of replay-critical outputs over full dense histories.

## Split policy
The dataset artifact should explicitly define:
- train split,
- validation split,
- heldout split,
- and at least one stress slice if the shape or route envelope is expected to vary.

The split should be deterministic and manifest-recorded.

## Manifest requirements
The teacher-data manifest should record:
- generation script path,
- git commit,
- seed policy,
- shape envelope,
- route settings,
- precision mode,
- device mode if relevant,
- target-object convention from Phase A,
- dataset counts by split,
- artifact file paths,
- and a reproducibility digest.

## Primary design rules

### 1. Same-route rule
The teacher data must come from the same batched streaming annealed LEDH-PFPF-OT route
used later by the benchmark harness. Reusing the older fixed-target Sinkhorn teacher
artifact is not acceptable as a silent substitute.

### 2. No semantic broadening
Do not let this dataset become a broad OT cloud collection. It is a route-specific
teacher-data artifact for one repair program.

### 3. Replay-oriented usefulness
The artifact should be rich enough that later heldout evaluation can answer the real
question:
- does the corrected learned warm-start replay stay close to the teacher replay?

### 4. Streaming memory discipline
Because the eventual route is large and streaming-oriented, prefer online aggregation or
compact retained outputs over full-history storage unless a frozen contract explicitly
requires the larger artifact.

## Evidence contract
### Primary criterion
This subplan succeeds only if the dataset artifact is route-matched, reproducible,
split-labeled, and sufficient for later training and heldout replay-sensitive
qualification.

### Veto diagnostics
- teacher data generated from the wrong route,
- missing target-object fields,
- ambiguous normalization,
- missing manifest or digest,
- split leakage,
- artifact too weak to support later replay-sensitive evaluation.

### Explanatory-only diagnostics
- dataset size convenience,
- artifact compactness,
- storage layout aesthetics.

### Non-claims
This subplan does not claim the dataset is sufficient for effectiveness or that the
student will train successfully. It only establishes a route-matched teacher-data
artifact.

## Grounding files to inspect while executing
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`
- retained-teacher data/eval references for pattern only:
  - `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_heldout_eval_tf.py`
  - `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_low_budget_eval_tf.py`
  - `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_low_budget_ablation_tf.py`

## Frozen Phase B dataset / manifest contract
This committed section aligns the teacher-data artifact with the frozen Phase A contract.

### Dataset purpose
The artifact is a route-matched retained-teacher dataset for the benchmarked streaming LEDH-PFPF-OT annealed warm-start path. It is not a generic OT corpus and must not silently substitute fixed-target Sinkhorn teacher artifacts.

### Required per-example input fields
Each saved example must include the exact student-facing contract fields:
- `scaled_post_flow`
- `normalized_log_weights`
- `epsilon`
- `valid_mask`

### Required per-example latent target fields
Each saved example must include the frozen learned latent target:
- `a_y`
- `b_x`
- `a_x`
- `b_y`

### Required per-example replay / route fields
Each saved example or split-level aggregate must preserve enough information for later replay-sensitive heldout qualification. At minimum the artifact must record:
- route-family identifier,
- transport settings used to generate the target,
- precision mode,
- compiled / JIT mode,
- shape metadata needed to detect route-envelope drift,
- seed or deterministic example-generation lineage,
- target-object convention identifier tied to the Phase A contract.

If full replay objects are too large, the artifact may use compact replay-critical summaries or route-native teacher state, but the saved form must still support later heldout evaluation of retained-teacher replay closeness.

### Split contract
The artifact must define deterministic, manifest-recorded splits:
- `train`
- `validation`
- `heldout`
- optional `stress` slice when the route envelope varies materially

The split rule must be reproducible from the manifest and must prevent split leakage.

### Manifest schema
The manifest must record at minimum:
- generation script path,
- git commit,
- environment / conda env when applicable,
- seed policy,
- shape envelope,
- route settings,
- precision mode,
- device mode if relevant,
- compiled / JIT mode,
- target-object convention identifier from Phase A,
- dataset counts by split,
- artifact file paths,
- reproducibility digest,
- whether replay-sensitive evaluation fields are stored directly or reconstructible from saved route-native state.

### Artifact admissibility rule
A Phase B dataset artifact is admissible only if:
- it is generated from the same streaming annealed LEDH-PFPF-OT route family used later by the benchmark,
- its saved target fields match the Phase A learned-object contract exactly,
- its manifest makes the split policy and provenance reconstructible,
- and its contents are sufficient for later heldout replay-sensitive qualification.

## Verification
This subplan is complete only if it produces:
1. a teacher-data artifact,
2. a manifest with route and split provenance,
3. explicit target-object fields matching Phase A,
4. and a reproducibility digest.

## Advancement rule
Do not begin student training until the teacher-data artifact and manifest exist and are
checked against the Phase A contract.
