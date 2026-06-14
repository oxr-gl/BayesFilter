# DPF Common Model Suite V2 P6 Retirement And Regression Subplan

metadata_date: 2026-06-07
phase: P6
status: REVIEWED_READY_FOR_PHASE_EXECUTION

## Question

After v2 BF/FF closure, can the standalone LGSSM, SV, and range-bearing fixture
modules be retired from the production path without damaging closed v1 evidence
or v2 reproducibility?

## Inputs

- P0 through P5 results and Claude reviews.
- v2 manifest and all v2 JSON artifacts.
- closed v1 JSON artifacts and validation-only runners.

## Evidence Contract

Primary criterion:

- No production v2 runner imports `lgssm_tf.py`,
  `stochastic_volatility_tf.py`, or `range_bearing_tf.py`, while v1 closed
  artifacts remain readable and v2 artifacts validate.
- Retirement PASS requires the production-v2 forbidden import class to be
  empty; it does not require zero imports repo-wide.

Veto diagnostics:

- deleting files before a reviewed cleanup amendment;
- breaking v1 validation-only commands;
- losing source checksums or successor mapping;
- changing v2 fixtures after seeing results;
- claiming old files were wrong merely because v2 supersedes them.
- v1 validation commands rebind to v2 semantics or altered v1 checksums.

Non-claims:

- retirement is source-of-truth cleanup, not a new mathematical result.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_retirement_manifest_2026-06-07.json`
- P6 result ledger under `docs/plans/`.

Required artifact sections:

- `primary_criterion_fields`;
- `veto_diagnostics`;
- `explanatory_only_fields`;
- `review_round`;
- `open_material_blockers`;
- `repair_amendment_required`;
- `next_allowed_action`;
- import inventory classes: `production_v2_imports_forbidden`,
  `legacy_v1_validation_allowed`, `reference_only_allowed`,
  `nonproduction_research_runner_allowed`.

## Planned Checks

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_tieout_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_noresampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_filter_path_fixed_resampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_fixed_branch_gradient_tf --validate-only
```

## Tasks

1. Verify P1 through P5 are closed or classified.
2. Record source checksums for the three standalone fixture files.
3. Record successor v2 model ids.
4. Build the import inventory ledger and verify
   `production_v2_imports_forbidden` is empty.
5. Remove production v2 imports of the old files only where they exist.
6. Mark old files `RETIRED_BY_V2_COMMON_SUITE` in the result ledger, or create
   a separate reviewed deletion amendment if physical deletion is desired.
7. Run v1 validation-only checks against original v1 checksums/artifact schema
   and v2 manifest validation.
8. Run Claude result/governance review.

## Exit Criteria

- v1 closed artifacts validate.
- v2 artifacts validate.
- retirement ledger maps every retired module to v2 successors and checksums.
- allowed legacy/reference/nonproduction imports are documented but do not
  block retirement.

## Stop Conditions

- Any v1 validation-only command fails for a reason caused by the retirement
  change.
- Cleanup would require changing closed v1 artifacts.
- Preserving v1 validation would require changing closed artifact semantics.
