# P1 Common Model Contracts Subplan

metadata_date: 2026-06-07
parent_program: `bayesfilter-dpf-cross-implementation-common-sense-tieout-plan-2026-06-06.md`

## Phase Question

Do BayesFilter and executable float64 FilterFlow evaluate the same declared
density components for the common model suite?

## Evidence Contract

Primary comparator:

- shared declarative model specs in
  `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`;
- BayesFilter highdim adapters;
- executable float64 FilterFlow subprocess adapters.

Primary pass criterion:

- each common model density cell is `MATCHED` within tolerance for initial,
  transition, observation, and scalar density components where both surfaces
  expose those components.

Veto diagnostics:

- nonfinite density component;
- unclassified mismatch;
- spec checksum mismatch;
- FilterFlow reference checkout mismatch;
- CPU-only TensorFlow import without `CUDA_VISIBLE_DEVICES=-1`;
- range-bearing local adapter mislabeled as upstream FilterFlow coverage.

Explanatory diagnostics:

- per-component deltas, model checksums, backend notes, and manifest fields.

Non-claims:

- density agreement is not full filter-path agreement;
- density agreement is not filtering correctness;
- no student-repository tie-out claim.

## Current Artifact

- Plan:
  `docs/plans/bayesfilter-dpf-common-model-suite-implementation-plan-2026-06-06.md`
- Result:
  `docs/plans/bayesfilter-dpf-common-model-suite-implementation-result-2026-06-06.md`
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_tieout_tf.py`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_tieout_2026-06-06.json`

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_tieout_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_tieout_tf --validate-only
```

## Exit Gate

P1 exits when the common LGSSM, SV, and range-bearing density cells are matched
or each non-matched cell is classified with a concrete mismatch or interface
blocker.
