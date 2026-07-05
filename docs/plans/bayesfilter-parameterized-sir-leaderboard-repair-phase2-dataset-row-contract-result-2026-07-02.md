# Phase 2 Result: Dataset Row Contract Repair

Date: 2026-07-02

Status: `PASS_PHASE2_PARAMETERIZED_SIR_ROW_GENERATED`

## Objective

Expose a parameterized SIR dataset row with free theta while preserving the
old fixed/no-free-theta SIR row as fixed-target evidence.

## Entry Evidence

- Phase 1 target contract passed Claude review.
- The reviewed new row id is
  `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`.
- The reviewed theta coordinate is `sir_log_scale_theta` with truth theta
  `[0.0, 0.0, 0.0]`.
- The fixed row must remain `zhao_cui_spatial_sir_austria_j9_T20` with
  `truth_theta_coordinate = no_free_theta`.

## Implementation Changes

- `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py`
  now adds a distinct parameterized SIR row.
- The new row uses `parameterized_zhao_cui_sir_austria_model()` and simulates
  the scaled base model at truth theta `[0, 0, 0]`.
- The old fixed row was not mutated.
- `tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py`
  now checks both the fixed row and the parameterized row.
- The P8 dataset manifest JSON/CSV/MD artifacts were regenerated.
- The canonical semantic binding was refreshed with dataset manifest path,
  manifest SHA256, fixed-row SHA256, and parameterized-row SHA256.

## Dataset Evidence

| Field | Value |
| --- | --- |
| Dataset manifest | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json` |
| Manifest SHA256 | `77af3011569d4ed158ef736f3f5f9fdbb58fc84c08f99bc36e9b59f02fc6abfc` |
| Fixed row id | `zhao_cui_spatial_sir_austria_j9_T20` |
| Fixed row SHA256 | `591c97ae11254441d6098bf148b1ad4d710dc013ad78403d2a154a535cc0ff2f` |
| Fixed truth coordinate | `no_free_theta` |
| Fixed truth theta | `[]` |
| Parameterized row id | `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` |
| Parameterized row SHA256 | `46c5f88b1563f16723f6a92be8367b2ac9c5172664e248b54bd2731302b409ad` |
| Parameterized truth coordinate | `sir_log_scale_theta` |
| Parameterized truth theta | `[0.0, 0.0, 0.0]` |
| Dataset status counts | `{"generated": 7}` |

The fixed and parameterized rows have identical generated state/observation
hashes at truth theta, as expected from the reviewed log-scale origin.

## Checks Run

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py
```

Exit status: 0. TensorFlow printed CUDA plugin/cuInit warnings despite the
deliberate CPU-only environment; this command is not GPU evidence.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py::test_p8_dataset_manifest_status_and_scope_boundary \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py::test_p8_dataset_manifest_generates_sir_raw_synthetic_but_not_source_route_success \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py::test_p8_dataset_manifest_generates_parameterized_sir_without_mutating_fixed_row \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py::test_p8_dataset_emitter_regenerates_manifest_artifacts
```

Exit status: 0. Result: `4 passed`.

```text
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json >/tmp/p8_dataset_manifest_json_check.json
```

Exit status: 0.

```text
rg -n "zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale|sir_log_scale_theta|no_free_theta|\"generated\": 7" ...
```

Exit status: 0. Confirmed the new row, theta coordinate, fixed-row
`no_free_theta`, and generated count.

```text
git diff --check -- <Phase 2 changed paths>
```

Exit status: 0 after cleaning the generated CSV inserted-row whitespace.

## Environment

- CPU-only by explicit `CUDA_VISIBLE_DEVICES=-1`.
- `MPLCONFIGDIR=/tmp`.
- TensorFlow imported in CPU-only mode; plugin/cuInit warnings are not treated
  as GPU diagnostics.
- No package installation, network fetch, or GPU benchmark was run.

## Gate Assessment

Primary criterion passed:

- A distinct parameterized row exists.
- It has the reviewed row id, theta coordinate, truth theta, truth semantics,
  parameter order, theta domain, and fixed-base-row binding.
- Tests fail if the row regresses to `no_free_theta`.
- The old fixed row remains preserved.

Veto diagnostics:

- No old-row silent mutation: pass.
- No missing truth theta on parameterized row: pass.
- No new-row `no_free_theta`: pass.
- Manifest/test disagreement: pass.
- Dataset status count stale: pass.

## Nonclaims

- Phase 2 does not admit a full observed-data/filtering value.
- Phase 2 does not admit a leaderboard score.
- Phase 2 does not prove exact likelihood correctness.
- Phase 2 does not claim source-faithful inference parameterization.
- Phase 2 does not claim HMC or GPU production readiness.

## Next Handoff

Phase 3 may start. It must wire the parameterized SIR row to a full
observed-data/filtering value and analytical/manual score evaluator, or write
a precise blocker if the current candidate route remains blocked.
