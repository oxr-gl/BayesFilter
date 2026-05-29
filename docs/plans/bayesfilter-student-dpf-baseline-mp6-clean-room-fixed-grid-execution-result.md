# Result: MP6 clean-room fixed-grid execution

## Status

Decision: `mp6_ready_for_student_comparison_audit`.

MP6 ran the exact 15-record clean-room fixed first-target grid and produced the
canonical JSON, summary JSON, and Markdown report artifacts.

## Command

```bash
python -m experiments.controlled_dpf_baseline.runners.run_fixed_grid --grid first-target --fixtures range_bearing_gaussian_low_noise,range_bearing_gaussian_moderate --seeds 31,43,59,71,83 --num-particles 128 --low-noise-flow-steps 20 --moderate-flow-steps 10,20 --max-records 15 --per-record-warning-seconds 45 --records-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json --summary-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid_summary.json --report-md experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md
```

Validation:

```bash
python -m experiments.controlled_dpf_baseline.runners.validate_results --records-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json --summary-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid_summary.json --expected-records 15 --require-finite-success-metrics --require-fixed-grid
```

Validation passed.

## Artifacts

- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid_summary.json`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md`.

Total MP6 artifact size is approximately `42.8K`.

## Results

| Cell | Records | Position RMSE median | Observation proxy RMSE median | Average ESS median | Resampling median | Runtime median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| low-noise N128/steps20 | 5 | 0.0474580 | 0.0180015 | 63.2496 | 10 | 3.8111 |
| moderate N128/steps10 | 5 | 0.0623641 | 0.0723264 | 90.3857 | 1 | 1.8924 |
| moderate N128/steps20 | 5 | 0.0638511 | 0.0725413 | 90.0386 | 2 | 3.7640 |

All 15 records returned `ok`.  No structured blockers, failed records,
nonfinite required metrics, missing grid cells, duplicate grid cells, or runtime
warnings were observed.

## Hypothesis Results

- MP6-H1 fixed target grid runs: supported.
- MP6-H2 successful records have finite required metrics: supported.
- MP6-H3 moderate-noise policy remains diagnostic: supported.  Both moderate
  N128/steps10 and N128/steps20 were run and should be interpreted by MP7
  rather than collapsed into a universal winner claim.

## Audit

- no student code was imported or executed by the clean-room algorithm;
- no vendored student files were edited;
- no production `bayesfilter/`, monograph, or reference files were edited by
  MP6;
- clean-room import search over `experiments/controlled_dpf_baseline/` found no
  forbidden student imports;
- artifact sizes are suitable for normal repository history.

## Interpretation

The clean-room controlled baseline is now ready for MP7 proxy-only comparison
against the frozen student aggregate evidence.  These metrics are diagnostic
and comparison-only; they are not production correctness evidence.

Next phase justified: MP7 clean-room comparison audit.
