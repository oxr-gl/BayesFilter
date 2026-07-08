# Phase 0 Result: Baseline And Boundary Freeze

Date: 2026-07-02

Status: `PASS_PHASE0_BASELINE_BOUNDARY_FREEZE`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | The strange SIR leaderboard behavior is confirmed as a target/theta-contract issue, not absence of local parameterized SIR score math. |
| Primary criterion status | PASS: current fixed row is `no_free_theta`; parameterized SIR local score convention and local score hooks exist and pass focused tests. |
| Veto diagnostic status | No Phase 0 veto triggered. |
| Main uncertainty | Whether the parameterized log-scale SIR surface should be classified as source-faithful, fixed-HMC adaptation, or extension/invention for leaderboard inference. |
| Next justified action | Phase 1 source/theta target contract. |
| What is not being concluded | No full observed-data/filtering score is admitted; no dataset row is repaired; no source-faithful parameterized inference claim is made; no leaderboard is regenerated. |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Is the current SIR blocker caused by a fixed/no-free-theta row contract while parameterized local score math already exists? |
| Baseline/comparator | Current generator/test/model state at launch commit `ef119f8bdb17b206339de92d722344a448eea745`. |
| Primary criterion | State exact blocker and distinguish fixed row from parameterized candidate. |
| Outcome | PASS. |
| Veto diagnostics | None. |
| Artifact | This Phase 0 result. |

## Findings

The current P8 dataset generator still emits the source-scope SIR row with:

- `truth_theta_coordinate = no_free_theta`;
- `truth_theta = []`.

The repository also contains a separate parameterized SIR candidate:

- `ParameterizedZhaoCuiSIRSSM`;
- `parameter_dim() == 3`;
- parameter order `log_kappa_scale`, `log_nu_scale`,
  `log_obs_noise_scale`;
- local analytical transition and observation density score hooks.

These are different targets. The fixed row remains fixed-target evidence. The
parameterized route must be introduced by a reviewed target contract rather
than silently reinterpreting the old row.

## Checks Run

CPU-only, sandboxed local checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py::test_p8_dataset_manifest_generates_sir_raw_synthetic_but_not_source_route_success
```

Result:

```text
1 passed in 0.02s
```

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_zhao_cui_sir_matches_p8p_p79_theta_convention tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape
```

Result:

```text
2 passed, 2 warnings in 5.35s
```

Static evidence search:

```bash
rg -n "truth_theta_coordinate|truth_theta|ParameterizedZhaoCuiSIRSSM|parameterized_zhao_cui_sir_austria_model|transition_log_density_parameter_score|observation_log_density_parameter_score" scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.md
```

Result: found the fixed `no_free_theta` generator entries and the
parameterized SIR model/test hooks.

## Environment

| Field | Value |
| --- | --- |
| CPU/GPU | CPU-only by `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA used. |
| Trusted/escalated | Local pytest/static checks ran sandboxed; Claude reviews ran trusted/escalated as required by cross-agent policy. |
| TensorFlow dtype/TF32 | Existing tests use TensorFlow float64; TF32 not used. |
| Exit status | All Phase 0 local checks exited 0. |

## Boundary Safety

Phase 0 did not:

- edit code;
- add or repair a dataset row;
- admit full observed-data/filtering score;
- claim the parameterized route is source-faithful;
- compare fixed and parameterized rows as the same target.

## Phase 1 Handoff

Phase 1 may start. It must produce the reviewed target contract and canonical
semantic-binding draft before any dataset or evaluator code is changed.
