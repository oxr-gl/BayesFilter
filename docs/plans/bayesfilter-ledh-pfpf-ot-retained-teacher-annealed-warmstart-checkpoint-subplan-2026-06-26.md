# Subplan: Phase C checkpointed learned-mode hardening and checkpoint-v1 integration

## Parent program
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-learned-warmstart-repair-master-program-2026-06-26.md`

## Dependencies
This subplan must follow:
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-annealed-warmstart-contract-subplan-2026-06-26.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-annealed-teacher-data-subplan-2026-06-26.md`

No learned-arm artifact should be treated as admissible unless the Phase A target-object contract is frozen and the Phase B dataset / manifest contract is satisfied.

## Purpose
Harden the `learned` benchmark path so checkpoint-backed evaluation is artifact-safe, provenance-bearing, and unambiguous, then define the integration requirements for the first real annealed warm-start checkpoint (`checkpoint v1`) that will enter Phase D training and later Phase E correctness qualification.

## Question
Given the now-frozen Phase A learned-object contract and Phase B dataset contract, what exact checkpoint provenance, artifact fields, and benchmark-side admissibility rules are required so that a future `learned` result is clearly a real checkpoint-backed retained-teacher evaluation rather than a random-model plumbing stub or a route-mismatched artifact?

## Scope
- In scope:
  - hardening the `learned` benchmark path around checkpoint provenance,
  - defining the checkpoint manifest convention,
  - defining artifact admissibility rules for `learned` mode,
  - defining what metadata a first real annealed checkpoint must carry,
  - integrating one real checkpoint into the benchmark once it exists.
- Out of scope:
  - broad model-family search,
  - effectiveness interpretation,
  - posterior/HMC/default-promotion claims,
  - broad training sweeps.

## Current state
The repository is no longer in the original pre-repair state.

What is already true now:
- the benchmark requires `--warmstart-checkpoint` for `--warmstart-mode learned` unless an explicit random-stub override is used,
- the benchmark builds the warm-start student, loads weights from the supplied checkpoint path, and records checkpoint-related metadata in the output artifact,
- the repaired benchmark now records stronger replay-sensitive correctness diagnostics.

Therefore the Phase C problem is no longer “add any checkpoint loading at all.” The remaining Phase C problem is to freeze what counts as an admissible checkpoint-backed learned artifact and what provenance must accompany `checkpoint v1`.

## Why this subplan is needed
Even with load-time checkpoint enforcement, a `learned` artifact can still be scientifically ambiguous if:
- the checkpoint provenance is not tied to the Phase A learned-object contract,
- the checkpoint is not tied to a Phase B route-matched dataset manifest,
- the benchmark artifact records only a path but not enough contract / dataset lineage,
- or a route-mismatched checkpoint is loadable at the tensor-shape level and therefore looks valid operationally while remaining invalid scientifically.

This subplan exists to close that gap.

## Frozen Phase C checkpoint / provenance contract
This committed section is the Phase C hardening contract future work should quote verbatim.

### 1. Learned-mode admissibility rule
A `learned` benchmark artifact is admissible only if all of the following hold:
- a checkpoint path is supplied,
- checkpoint loading succeeds,
- random-stub mode is not used,
- the artifact records the checkpoint provenance fields below,
- the artifact route metadata match the frozen same-route comparator contract from Phase A,
- the checkpoint lineage points back to a Phase B-compliant teacher-data manifest,
- and the checkpoint’s target-object convention identifier matches the frozen Phase A contract.

### 2. Required checkpoint provenance fields
Every admissible checkpoint must have a manifest or metadata record with at least:
- checkpoint path,
- checkpoint identifier or digest,
- model class / model config,
- training script path,
- git commit,
- environment / conda env when applicable,
- training seed policy,
- Phase A target-object convention identifier,
- Phase B dataset manifest path,
- Phase B dataset reproducibility digest,
- route-family identifier,
- shape envelope used during training,
- precision mode,
- compiled / JIT mode if relevant to training/eval interpretation,
- heldout evaluation summary path for the checkpoint run.

### 3. Required benchmark artifact fields for learned mode
Every admissible `learned` benchmark output must record at minimum:
- `warmstart_mode`,
- `warmstart_checkpoint_path`,
- `warmstart_checkpoint_loaded`,
- `warmstart_random_stub_allowed`,
- warm-start model config,
- route metadata needed to check same-route use,
- a checkpoint manifest or checkpoint metadata reference,
- the Phase A target-object convention identifier,
- the Phase B dataset manifest reference when available.

### 3a. Concrete field-name / placement recommendation
For the smallest implementation delta, extend the existing learned-mode `warmstart_metadata` block rather than introducing a second parallel provenance container.

Recommended learned-mode field names:
- `target_object_convention_id`
- `dataset_manifest_path`
- `dataset_manifest_reproducibility_digest`
- `checkpoint_manifest_path`
- `checkpoint_manifest_reproducibility_digest`
- `checkpoint_reference`

Keep the existing fields already emitted by the benchmark:
- `mode`
- `checkpoint_path`
- `checkpoint_loaded`
- `random_stub_allowed`
- `model_config`

The resulting learned-mode `warmstart_metadata` payload should therefore carry:
- `mode`
- `checkpoint_path`
- `checkpoint_loaded`
- `random_stub_allowed`
- `model_config`
- `target_object_convention_id`
- `dataset_manifest_path`
- `dataset_manifest_reproducibility_digest`
- `checkpoint_manifest_path`
- `checkpoint_manifest_reproducibility_digest`
- `checkpoint_reference`

### 3b. Concrete CLI / ingestion recommendation
The smallest benchmark-side wiring path is to add three learned-mode CLI inputs:
- `--target-object-convention-id`
- `--dataset-manifest`
- `--checkpoint-manifest`

Benchmark-side handling should then:
- resolve the manifest paths,
- read each manifest's `reproducibility_digest`,
- emit both path and digest into `warmstart_metadata`.

This follows the existing retained-teacher runner pattern of storing upstream artifact path plus upstream `reproducibility_digest`.

### 4. Route-mismatch rule
Tensor-shape compatibility is not enough for admissibility. A checkpoint is inadmissible if its recorded route family, target-object convention, or dataset lineage do not match the benchmarked streaming annealed LEDH-PFPF-OT retained-teacher route.

### 5. Checkpoint-v1 integration rule
The first real checkpoint (`checkpoint v1`) is eligible to enter Phase D / Phase E handoff only if:
- it is trained against the frozen Phase A latent target contract,
- it is trained from a Phase B-compliant route-matched dataset artifact,
- it has a reproducible manifest,
- it improves clearly over the explicit random stub on heldout replay-sensitive evaluation,
- and it can be loaded and recorded by the benchmark without any manual hidden state.

## Planned steps

### Step 1 — freeze the checkpoint manifest convention
Write or reuse a small manifest convention that stores the required checkpoint provenance fields listed above.

### Step 2 — align benchmark artifact fields with the manifest convention
Ensure the benchmark output records not only path/load success, but also references sufficient to connect the run back to:
- the Phase A target-object contract,
- the Phase B dataset manifest,
- and the checkpoint manifest / digest.

### Step 3 — define the `checkpoint v1` entry gate
Before any Phase D training result is considered meaningful, require that `checkpoint v1` satisfy:
- Phase A target-object match,
- Phase B dataset lineage,
- reproducible seed / manifest record,
- and heldout replay-sensitive summary.

### Step 4 — integrate `checkpoint v1` into learned-mode benchmarking
Once a real checkpoint exists, run the benchmark in `learned` mode using that exact artifact and confirm that the emitted benchmark record is provenance-complete and unambiguous.

### Step 5 — hand off to Phase D / E execution
After Phase C passes, the next work is:
- produce one minimal credible checkpoint under the Phase D training policy,
- then rerun the Phase E correctness rung using the now-admissible learned artifact.

## Evidence contract

### Exact baseline
Same as the repair master program: the exact same-route cold / zero-init streaming LEDH-PFPF-OT comparator under matched route, device, precision, seed, particle count, and transport settings.

### Primary criterion
This subplan succeeds only if a future `learned` benchmark artifact can no longer be ambiguous about what it is. Concretely, success requires:
1. learned mode is checkpoint-backed rather than silent random fallback,
2. checkpoint provenance is reconstructible,
3. dataset lineage is reconstructible,
4. route-family compatibility is checked by recorded metadata,
5. `checkpoint v1` has a clear handoff contract into Phase D / E.

### Veto diagnostics
- checkpoint provenance missing or incomplete,
- no link to Phase B dataset manifest,
- target-object convention mismatch with Phase A,
- route-family mismatch,
- random-stub path still confusable with admissible learned evaluation,
- benchmark artifact records a loadable checkpoint but not enough metadata to audit lineage.

### Explanatory-only diagnostics
- checkpoint size,
- training runtime,
- latent loss by itself,
- convenience of a particular metadata layout.

### Non-claims
Even if this subplan succeeds, it does not conclude:
- that the checkpoint is effective,
- that the learned arm passes correctness,
- posterior correctness,
- HMC readiness,
- default-route promotion,
- broad generalization of the student.

## Main risks and guards

### Risk 1 — route-matched checkpoint in name only
Guard: require recorded Phase B dataset manifest and route-family identifier.

### Risk 2 — Phase A target drift hidden behind compatible tensor shapes
Guard: require a target-object convention identifier in both checkpoint metadata and benchmark artifact.

### Risk 3 — benchmark artifact still too weak to audit later
Guard: require a manifest or digest reference, not only a checkpoint path string.

### Risk 4 — random stub and real checkpoint remain operationally easy to confuse
Guard: keep explicit random-stub allowance separate and non-admissible for scientific learned-arm evaluation.

## Critical files to inspect / modify next
- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`
- `experiments/dpf_implementation/tf_tfp/filters/batched_annealed_warmstart_student_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- future checkpoint-manifest / training-runner artifacts produced under the repair program

## Verification
After execution of this subplan:
1. confirm learned mode remains checkpoint-backed and non-silent,
2. confirm the benchmark artifact records checkpoint provenance sufficient to audit lineage,
3. confirm the checkpoint metadata link back to the Phase A target-object contract and Phase B dataset manifest,
4. confirm `checkpoint v1` is distinguishable from the random stub in both artifact policy and heldout evaluation,
5. then hand off to Phase D training execution and Phase E correctness rerun.

## Skeptical audit
This subplan passes the skeptical audit only if it remains a narrow artifact-hardening and provenance-hardening step. The goal is not to claim the learned route works; it is to ensure that when a later checkpoint is evaluated, we know exactly what object was trained, on what route-matched data, under what lineage, and under what admissibility rules.
