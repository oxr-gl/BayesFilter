# Plan: MP6 clean-room fixed-grid execution

## Date

2026-05-13

## Status

Planned.  Execute only after MP5 exits with
`mp5_ready_for_fixed_grid_execution` or `mp5_ready_with_caveats`.

MP6 is non-executable until MP5 has created the canonical
`experiments.controlled_dpf_baseline.runners.run_fixed_grid` and
`experiments.controlled_dpf_baseline.runners.validate_results` entry points,
the fixed report-output directory, and the result schema used below.

## Goal

Run the clean-room controlled baseline on the fixed first target grid from the
clean-room specification, then produce machine-readable and human-readable
results.

The phase must not expand the grid.  It must run only:

| Fixture | Particles | Flow steps | Seeds |
| --- | ---: | ---: | --- |
| `range_bearing_gaussian_low_noise` | 128 | 20 | `31, 43, 59, 71, 83` |
| `range_bearing_gaussian_moderate` | 128 | 10 | `31, 43, 59, 71, 83` |
| `range_bearing_gaussian_moderate` | 128 | 20 | `31, 43, 59, 71, 83` |

Planned records: 15 for one clean-room controlled algorithm.

## Owned write set

Allowed:

- `experiments/controlled_dpf_baseline/`;
- MP6 plan/audit/result notes whose filenames begin with
  `docs/plans/bayesfilter-student-dpf-baseline-mp6-`;
- `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`.

Out of scope:

- production `bayesfilter/`;
- DPF monograph files and reset memos;
- `docs/references.bib`;
- vendored student code edits;
- student adapter calls from the clean-room algorithm;
- broad grid expansion.
- algorithm design changes except narrow bug fixes documented in an MP6
  revision note.

## Hypotheses

### MP6-H1: the clean-room baseline runs the fixed target grid

Criterion:

- all 15 planned records complete with `ok` or a structured blocker.

Veto:

- unbounded runtime;
- missing target-grid cells;
- generated artifacts too large for repository history.

### MP6-H2: successful records have finite required metrics

Criterion:

- state RMSE, position RMSE, final-position error, observation proxy RMSE,
  runtime, and finite-output checks are present for every successful record.

Veto:

- required metrics are missing without a structured blocker.

### MP6-H3: moderate-noise policy remains diagnostic

Criterion:

- moderate steps10 and steps20 are both reported and interpreted as diagnostic
  variants.

Veto:

- the report claims a universal moderate-noise winner without the MP7
  comparison audit.

## Phase cycle

1. Plan: confirm MP5 exit decision and exact runner command.
2. Execute: run the fixed target grid only.
3. Test: validate JSON schema, finite metrics, planned-record counts, and
   runtime-warning counts.
4. Audit: verify no student imports, production edits, monograph edits, vendor
   edits, or grid expansion.
5. Tidy: keep reports small and remove transient artifacts.
6. Update reset memo: record results and whether MP7 is justified.

## Canonical MP6 command

Execute MP6 only from the repository root with this command:

```bash
python -m experiments.controlled_dpf_baseline.runners.run_fixed_grid --grid first-target --fixtures range_bearing_gaussian_low_noise,range_bearing_gaussian_moderate --seeds 31,43,59,71,83 --num-particles 128 --low-noise-flow-steps 20 --moderate-flow-steps 10,20 --max-records 15 --per-record-warning-seconds 45 --records-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json --summary-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid_summary.json --report-md experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md
```

The runner must refuse any command that would produce more or fewer than 15
planned records for `--grid first-target`.

These are phase-stable canonical paths, not wall-date claims.  A rerun or
repair must deliberately replace them and record the replacement in the MP6
result note and reset memo.  MP7 and MP8 must consume these canonical paths
unless a documented MP6 revision plan changes the contract before comparison
begins.

## Canonical MP6 validation command

```bash
python -m experiments.controlled_dpf_baseline.runners.validate_results --records-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json --summary-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid_summary.json --expected-records 15 --require-finite-success-metrics --require-fixed-grid
```

The validation command must fail if any planned grid cell is absent, duplicated,
or outside the fixed target grid.

## Required record schema

Every MP6 record must include:

- `implementation_name`;
- `implementation_type`;
- `fixture_name`;
- `target`;
- `status`;
- `failure_reason`;
- `seed`;
- `num_particles`;
- `flow_steps`;
- `horizon`;
- `runtime_seconds`;
- `metrics`;
- `diagnostics`;
- `provenance`.

Every successful record must include finite:

- `state_rmse`;
- `position_rmse`;
- `final_position_error`;
- `observation_proxy_rmse`;
- finite-output diagnostics.

Optional diagnostics such as `average_ess`, `min_ess`, `resampling_count`, and
`log_likelihood` must be present as values or `null`, with semantics labeled.

Allowed `status` values:

- `ok`;
- `blocked`;
- `failed`.

Allowed `failure_reason` values when `status != "ok"`:

- `blocked_missing_dependency`;
- `blocked_environment_drift`;
- `blocked_missing_assumption`;
- `blocked_runtime_limit`;
- `blocked_schema_validation`;
- `failed_algorithmic`;
- `failed_nonfinite_output`;
- `failed_metric_contract`;
- `failed_unexpected_exception`.

For `status = "ok"`, `failure_reason` must be `null`.

## Runtime and artifact gates

- default runtime-warning threshold: 45 seconds per record;
- any record exceeding the threshold must remain included and labeled;
- any run that cannot complete inside a bounded local execution should return a
  structured blocker rather than hanging;
- generated JSON and Markdown artifacts must be small enough for normal
  repository history, or the phase must stop before commit and ask for
  direction.

## Required outputs

- JSON record file:
  `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json`;
- summary JSON:
  `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid_summary.json`;
- Markdown result report:
  `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md`;
- MP6 result note:
  `docs/plans/bayesfilter-student-dpf-baseline-mp6-clean-room-fixed-grid-execution-result.md`.

## Required checks

- canonical MP6 command exits normally or emits only structured blockers;
- canonical validation command passes;
- output-size check for all MP6 artifacts;
- clean-room import search:

```bash
rg -n "experiments/student_dpf_baselines|advanced_particle_filter|2026MLCOE|from src\\.|import src\\." experiments/controlled_dpf_baseline
```

  Expected result: no matches.

- production import-boundary search:

```bash
rg -n "experiments/student_dpf_baselines|advanced_particle_filter|2026MLCOE" bayesfilter tests
```

  Expected result: no production or normal-test imports.

- vendored student dirt check:

```bash
git status --short -- experiments/student_dpf_baselines/vendor
```

  Expected result: no dirty vendored student files.

- path-scoped whitespace check:

```bash
git diff --check -- experiments/controlled_dpf_baseline docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md docs/plans/bayesfilter-student-dpf-baseline-mp6-clean-room-fixed-grid-execution-plan-2026-05-13.md
```

## Exit decision

Use one of:

- `mp6_ready_for_student_comparison_audit`;
- `mp6_ready_with_caveats`;
- `mp6_needs_revision`;
- `mp6_blocked_or_excluded`.

Proceed to MP7 only if records are complete or blocked structurally, required
metrics are finite for successful records, and no lane-boundary veto fires.
