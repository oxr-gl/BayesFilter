# DPF Common Model Suite V2 P6 Retirement Import-Absorption Repair Amendment

metadata_date: 2026-06-07
phase: P6
status: PENDING_CLAUDE_REVIEW

## Blocker

The P6 skeptical audit found a fixable retirement blocker:

- `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`
  still imports the standalone v1 source fixture modules
  `lgssm_tf.py`, `stochastic_volatility_tf.py`, and `range_bearing_tf.py`.

Under the P6 contract, retirement means that production v2 runners no longer
depend on those three standalone modules.  It does not mean the old modules are
wrong, deleted, or unusable for legacy validation/reference runs.

## Repair Scope

Patch only:

- `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`;
- a new P6 runner/report/manifest if needed;
- P6 result and review ledgers.

The repair may:

- absorb the small LGSSM, stochastic-volatility, and range-bearing fixture
  builders and helper functions directly into `common_model_suite_tf.py`;
- remove the three production-v2 imports from `common_model_suite_tf.py`;
- write a retirement manifest that classifies remaining imports repo-wide into
  production-v2-forbidden, legacy-v1-validation-allowed, reference-only-allowed,
  and nonproduction-research-runner-allowed;
- run closed-v1 validation-only checks and v2 validation-only checks.

The repair must not:

- delete or edit `lgssm_tf.py`, `stochastic_volatility_tf.py`, or
  `range_bearing_tf.py`;
- mutate `.localsource/filterflow`;
- change v1 expected checksums or closed 2026-06-06 artifacts;
- change v2 model equations, observations, scalar definitions, branch
  semantics, tolerances, classifications, gradient knobs, or non-claims;
- run student implementation commands;
- treat BayesFilter, FilterFlow, v1 fixtures, TT, dense quadrature, students,
  or paper tables as an oracle.

## Evidence Contract

Question:

- Can P6 remove production-v2 dependency on the three standalone fixture
  modules while preserving closed-v1 validation and v2 reproducibility?

Primary criterion:

- `common_model_suite_tf.py` has no imports from
  `experiments.dpf_implementation.tf_tfp.fixtures.lgssm_tf`,
  `experiments.dpf_implementation.tf_tfp.fixtures.stochastic_volatility_tf`,
  or `experiments.dpf_implementation.tf_tfp.fixtures.range_bearing_tf`;
- all v2 validation-only runners still validate their existing artifacts;
- all closed-v1 validation-only runners still validate their existing artifacts;
- the P6 retirement manifest has an empty
  `production_v2_imports_forbidden` class.

Veto diagnostics:

- any v1 validation-only command fails;
- any v2 validation-only command fails;
- v2 manifest row ids, row checksums, or artifact schemas drift because of the
  import absorption;
- the old standalone files are edited or deleted;
- the import inventory contains a production-v2 forbidden import after repair;
- any student command runs;
- `.localsource/filterflow` is mutated.

Explanatory-only diagnostics:

- remaining imports from old fixture modules in legacy, reference, or
  nonproduction research runners;
- source checksums of retired standalone modules;
- successor mapping from each retired standalone module to v2 model ids;
- dirty worktree state.

What will not be concluded:

- no new mathematical correctness claim;
- no proof that the old files were wrong;
- no filter correctness or stochastic-resampling distribution claim;
- no student implementation claim.

## Planned Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_manifest_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_density_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_noresampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_fixed_resampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_gradients_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_tieout_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_fixed_resampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_common_fixed_branch_gradient_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_retirement_tf
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_retirement_manifest_2026-06-07.json
git diff --check experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_v2_retirement_tf.py docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p6-retirement-regression-result-2026-06-07.md
```

## Review Request

Claude should block this amendment if it weakens the P6 evidence contract,
allows hidden model/tolerance/checksum drift, permits deleting legacy fixtures
without a separate cleanup amendment, or lets finite differences, runtime,
legacy artifact presence, or v1/v2 checksum similarity become a correctness
claim.
