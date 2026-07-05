# Phase 4 Result: Regeneration And Validation

Date: 2026-07-03

Status: `PASS_PHASE4_SPLIT_MERGE_FULL_ARTIFACT_VALIDATED`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 4 passes by the reviewed split/merge route: the July 3 full leaderboard JSON/MD was generated from the frozen July 1 full artifact plus the validated scoped Zhao-Cui SIR component row. |
| Primary criterion status | Passed: full JSON/MD contain the contracted scoped parameterized SIR row fields and no retained-grid production admission. |
| Veto diagnostic status | No veto triggered: JSON is valid, score provenance is analytical/manual, target scope is explicit, and retained-grid remains diagnostic/historical. |
| Main uncertainty | Unrelated expensive rows were not rerun on July 3; they remain frozen from the July 1 full artifact. |
| Next justified action | Proceed to Phase 5 closeout after bounded Claude read-only review of this result. |
| What is not being concluded | No fresh rerun of unrelated expensive rows, no full observed-data/filtering SIR score identity, no exact likelihood proof, no posterior correctness, and no new GPU result. |

## Failed Full-Rebuild Attempts Preserved As History

Command attempted:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md
```

Outcomes:

- Attempt 1: manually interrupted after several minutes with no output and no
  partial full artifact.
- Attempt 2: manually interrupted after several minutes with no output and no
  partial full artifact.
- Attempt 3: manually interrupted after roughly 8.5 minutes with no output and
  no partial full artifact.

The TensorFlow CUDA plugin/cuInit warnings occurred despite intentional
`CUDA_VISIBLE_DEVICES=-1`. They are CPU-only environment warnings and are not
GPU diagnostics.

## Split/Merge Regeneration

Command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --cached-baseline docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json --scoped-patch docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03-scoped-zhaocui-sir-row.json --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md
```

Generated:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md`

The JSON manifest records:

- `execution_mode = split_merge_cached_july1_full_leaderboard_plus_validated_scoped_zhaocui_sir_component_row`
- `cached_baseline_artifact = docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
- `scoped_patch_artifact = docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03-scoped-zhaocui-sir-row.json`

The nonclaims include:

- unaffected rows are preserved from the frozen July 1 full leaderboard
  artifact;
- the parameterized SIR local complete-data component row is not a full
  observed-data/filtering row;
- the split/merge artifact is not evidence that unrelated expensive rows were
  rerun on July 3.

## Scoped Row Result

| Field | Value |
| --- | --- |
| Row id | `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` |
| Algorithm id | `zhao_cui_scalar_or_multistate` |
| Comparison status | `executed_value_score` |
| Row admission status | `scoped_component_row_admitted` |
| Target scope | `local_complete_data_zhao_cui_sir_d18_component` |
| Average log likelihood | `-60.44641064507831` |
| Log likelihood | `-1208.9282129015662` |
| Score | `[1163.1499331099205, -508.7932467308049, 21.10862132639743]` |
| Score L2 norm | `1269.7377322529198` |
| Score provenance | `zhao_cui_sir_d18_local_complete_data_manual_parameter_score_methods` |
| Retained-grid admission | `not_admitted_for_production_leaderboard_use_fixed_variant_zhao_cui` |

Companion scoped cells:

- `fixed_sgqf`: blocked as `not_applicable_to_scoped_component_row`.
- `ukf`: blocked as `not_applicable_to_scoped_component_row`.

## Local Checks

Commands:

```bash
python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase7.py
python -m json.tool docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json
rg -n "split_merge_cached_july1|scoped_component_row_admitted|local_complete_data_zhao_cui_sir_d18_component|zhao_cui_sir_d18_local_complete_data_manual_parameter_score_methods|not a full observed-data/filtering row|not evidence that unrelated expensive rows were rerun|not_admitted_for_production_leaderboard_use_fixed_variant_zhao_cui|1163\\.149933|-508\\.793247|21\\.108621|-60\\.446411" docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md
git diff --check -- docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase7.py docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase7.py -q
```

Outcome:

- Python compile checks passed.
- JSON syntax validation passed.
- Required split/merge, scoped row, provenance, nonclaim, and retained-grid
  exclusion markers were found.
- `git diff --check` passed.
- Focused pytest passed: `9 passed, 2 warnings in 7.19s`.

## Phase 5 Handoff

Phase 5 may now close the program with the important limitation that the July 3
full artifact is a split/merge artifact, not a fresh full rerun of unrelated
expensive rows.
