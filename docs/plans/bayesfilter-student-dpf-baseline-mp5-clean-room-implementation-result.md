# Result: MP5 clean-room implementation scaffold

## Status

Decision: `mp5_ready_for_fixed_grid_execution`.

MP5 implemented the clean-room controlled-baseline scaffold under
`experiments/controlled_dpf_baseline/` and stopped after the required smoke
checks.  MP5 did not run the MP6 fixed grid.

## Files Created Or Updated

Implementation surfaces:

- `experiments/controlled_dpf_baseline/__init__.py`;
- `experiments/controlled_dpf_baseline/fixtures/__init__.py`;
- `experiments/controlled_dpf_baseline/fixtures/range_bearing.py`;
- `experiments/controlled_dpf_baseline/metrics.py`;
- `experiments/controlled_dpf_baseline/results.py`;
- `experiments/controlled_dpf_baseline/prototypes/__init__.py`;
- `experiments/controlled_dpf_baseline/prototypes/particle_flow_baseline.py`;
- `experiments/controlled_dpf_baseline/runners/__init__.py`;
- `experiments/controlled_dpf_baseline/runners/run_smoke.py`;
- `experiments/controlled_dpf_baseline/runners/run_fixed_grid.py`;
- `experiments/controlled_dpf_baseline/runners/validate_results.py`;
- `experiments/controlled_dpf_baseline/reports/outputs/README.md`.

Smoke artifacts:

- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke.json`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke_summary.json`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-smoke-result.md`.

## Smoke Result

Canonical command:

```bash
python -m experiments.controlled_dpf_baseline.runners.run_smoke --fixture range_bearing_gaussian_moderate --seed 31 --num-particles 32 --flow-steps 2 --max-records 1 --max-wall-seconds 30 --records-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke.json --summary-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke_summary.json --report-md experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-smoke-result.md
```

Summary:

- planned records: `1`;
- ok records: `1`;
- fixed-grid records: `0`;
- smoke records: `1`;
- runtime warning count: `0`;
- smoke wall time: approximately `0.119` seconds;
- position RMSE: approximately `0.0629`;
- observation proxy RMSE: approximately `0.0710`;
- average ESS: approximately `24.24`;
- resampling count: `1`.

Validation command:

```bash
python -m experiments.controlled_dpf_baseline.runners.validate_results --records-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke.json --summary-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke_summary.json --expected-records 1 --require-finite-success-metrics --require-smoke-only
```

Validation passed.

## Hypothesis Results

- MP5-H1 fixture generation can be implemented clean-room: supported.  The
  generated fixture arrays matched the BayesFilter-owned nonlinear fixture
  arrays exactly for states, observations, `A`, `Q`, and `R`.
- MP5-H2 metric and result schema are independent of student adapters:
  supported.  Metrics validated the smoke record and required finite outputs.
- MP5-H3 minimal flow-assisted baseline scaffold can be written without student
  code: supported.  The scaffold exposes particle count, seed, and `flow_steps`
  and ran the bounded smoke case.

## Checks

- `python -m py_compile` passed for all Python files under
  `experiments/controlled_dpf_baseline/`.
- Fixture parity check passed with maximum absolute difference `0.0` for both
  clean-room fixtures against BayesFilter-owned fixture arrays.
- Clean-room import search over `experiments/controlled_dpf_baseline/` found no
  forbidden student imports.
- Smoke artifacts are small: approximately `4.2K` total.

## Interpretation

MP5 created the exact runner, validation, schema, metric, fixture, and
algorithm surfaces required for MP6.  The implementation remains experimental,
clean-room, and comparison-only.  It is not production BayesFilter code and is
not monograph evidence.

Next phase justified: MP6 fixed-grid execution.
