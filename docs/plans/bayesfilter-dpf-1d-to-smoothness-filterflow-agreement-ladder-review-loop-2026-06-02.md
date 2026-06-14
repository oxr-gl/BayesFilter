# Review Loop: 1D-to-Smoothness Filterflow Agreement Ladder

Reviewer command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

## Plan Review

### Round 1

Claude status: `REJECT`.

Codex-supervisor audit:

1. `ACCEPT`: rung contracts were too narrative to guarantee first-discrepancy
   localization. Control added: each rung now defines fixed variables, the one
   changed axis, promoted comparisons, and structured blockers for randomness
   capture that cannot be done without mutating filterflow.
2. `ACCEPT`: within-rung stopping order was underspecified. Control added:
   the plan now requires deterministic cell order and records first failing
   cell as `(rung_id, cell_index, cell_id)`.
3. `ACCEPT`: smoothness defaults were partially recovered. Control added:
   `mesh_size=20` and `diff_epsilon=1e-2` are now recorded, and the plan
   classifies authoritative defaults versus diagnostic/bounded substitutes.
4. `PARTIAL`: CPU-only execution needed stronger enforcement for TensorFlow
   executions, but non-TF verification commands do not need GPU manifests.
   Control added: every BayesFilter and filterflow TensorFlow run must record
   pre-import `CUDA_VISIBLE_DEVICES=-1` and no visible GPU devices; compile,
   JSON, `rg`, and git checks are explicitly not GPU/CUDA evidence.
5. `ACCEPT`: the pass criterion could be read as promoting gradients before
   scalar/gradient reconciliation. Control added: primary pass criteria now
   exclude gradient/FD agreement unless
   `scalar_gradient_contract_reconciled=true`.

Patch summary:

- Updated `docs/plans/bayesfilter-dpf-1d-to-smoothness-filterflow-agreement-ladder-plan-2026-06-02.md`
  with exact rung contracts, first-failing-cell semantics, smoothness defaults,
  CPU-only enforcement, and gradient diagnostic-only governance.

Round 1 findings are accepted/partially accepted; resubmitting patched plan.

### Round 2

Claude status: `ACCEPT`.

Codex-supervisor audit: `ACCEPT`. Claude's acceptance is consistent with the
patched plan text. The plan now enforces exact rung contracts, deterministic
first-failing-cell localization, smoothness default classification, CPU-only
TensorFlow manifests, gradient diagnostic-only governance, lane boundaries,
and cross-implementation residual governance.

Plan review final status: `ACCEPT_after_round_2`.

### Round 3

Implementation-discovered correction before execution:

- Codex found that `.localsource/filterflow/scripts/simple_linear_smoothness.py`
  draws initial particles from the NumPy `data_seed=123` random state after
  data generation; `seed=1234` is the SMC/filter seed. The plan's R2 wording
  incorrectly named `filterflow_initial_particles_seed_1234`.

Codex-supervisor audit: `ACCEPT`. The correction is materially required to
avoid a misleading R2 contract.

Patch summary:

- Updated R2 to use
  `filterflow_initial_particles_data_seed_123_after_data_generation` and to
  state that `filter_seed=1234` governs SMC seed splitting, not initial
  particle generation.

Resubmitting the narrow plan delta to Claude before execution.

Claude status: `ACCEPT`.

Codex-supervisor audit: `ACCEPT`. Claude agrees the correction makes R2 more
faithful to the executable comparator and introduces no new governance defect.

Plan review final status: `ACCEPT_after_round_3_seed_correction`.

## Result Review

### Round 1

Submitting result artifacts to Claude. Codex pre-review summary:

- Result decision:
  `one_d_to_smoothness_agreement_ladder_first_mismatch_detected`.
- First failing cell:
  `R1_1d_T100_filterflow_observation_path / T100_filterflow_observation_path`.
- Main metrics: scalar delta `8.470837339758873`; row residual delta
  `0.00016306889793304968`; trigger flags match; ledger and scalar fail the
  predeclared agreement tolerances.
- R2-R8 are blocked by the first R1 mismatch and are not evidence-bearing.
- The `import numpy as np` static-gate hit is confined to an embedded external
  filterflow fixture subprocess string, not the BayesFilter TF implementation
  backend.

Claude status: `REJECT`.

Codex-supervisor audit:

1. `ACCEPT`: result review status was still marked pending, so the artifact
   was not an accepted reviewed result.
2. `ACCEPT`: R1 violated the accepted one-axis contract by using a new
   transition-noise ledger from the fixture subprocess while claiming to change
   only observations.

Patch controls to add before resubmission:

- R1/R2 must use the existing controlled deterministic `generated_T100`
  transition-noise ledger from
  `run_filterflow_1d_to_smoothness_ladder_tf._generated_scenario(100)`.
- The filterflow fixture subprocess may generate observations and initial
  particles, but its generated transition-noise field must not be used for R1
  or R2.
- Result artifact must be regenerated and reviewed after the patch.

Patch applied:

- Updated the runner so R1/R2 use the existing controlled
  `generated_T100` transition-noise ledger and the fixture subprocess no
  longer emits or supplies transition noises.
- Regenerated the result/report/JSON artifacts.
- Corrected metrics after the one-axis patch: R1 still fails, now with scalar
  delta `2.205229699611664`, row residual delta
  `0.0005531286149466075`, column residual delta
  `4.768371573149466e-07`, and matching trigger flags.

### Round 2

Submitting patched result artifacts to Claude.

Claude status: `ACCEPT`.

Codex-supervisor audit: `ACCEPT`. Claude's acceptance is consistent with the
patched result: R1 now changes only observations, the fixture subprocess no
longer supplies transition noises, R1 remains the first failing cell, R2-R8
are blocked after R1, NumPy is confined to the external fixture subprocess,
and the result does not overclaim correctness or gradient agreement.

Result review final status: `ACCEPT_after_round_2`.
