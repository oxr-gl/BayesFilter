# Result: MP7 clean-room comparison audit

## Status

Decision: `mp7_ready_for_final_archive`.

MP7 compared the clean-room fixed-grid results against the frozen student
aggregate evidence using proxy metrics only.  No student implementation code was
executed, and MP6 outputs were not rewritten.

## Inputs

Clean-room inputs:

- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid_summary.json`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md`.

Frozen student aggregate inputs:

- `experiments/student_dpf_baselines/reports/student-dpf-baseline-full-horizon-edh-pfpf-confirmation-result-2026-05-12.md`;
- `experiments/student_dpf_baselines/reports/outputs/full_horizon_edh_pfpf_confirmation_2026-05-12.json`;
- `experiments/student_dpf_baselines/reports/outputs/full_horizon_edh_pfpf_confirmation_summary_2026-05-12.json`.

## Outputs

- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-comparison-audit.md`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_comparison_audit.json`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_comparison_audit_summary.json`.

## Results

| Cell | Final class | Interpretation |
| --- | --- | --- |
| low-noise N128/steps20 | `same_qualitative_regime` | Clean-room proxy medians are within the fixed 2.0x band for both frozen student aggregates. |
| moderate N128/steps10 | `same_qualitative_regime` | Clean-room proxy medians are within the fixed 2.0x band for both frozen student aggregates. |
| moderate N128/steps20 | `same_qualitative_regime` | Clean-room proxy medians are within the fixed 2.0x band for both frozen student aggregates. |

All three fixed-grid cells were classified exactly once.  The comparison JSON
and summary JSON preserve per-student classes, denominator medians, the derived
final class, and the aggregation rule for every clean-room cell.

## Hypothesis Results

- MP7-H1 clean-room results can be compared qualitatively to student
  aggregates: supported.
- MP7-H2 comparison remains proxy-only: supported.
- MP7-H3 next engineering decision is clear: supported.

## Caveats

- `same_qualitative_regime` is not a correctness certificate.
- Student aggregate agreement is not production evidence.
- ESS, resampling, and runtime remain diagnostic context.
- Moderate-noise steps10 and steps20 remain diagnostic variants; no universal
  moderate-noise winner is claimed.

## Audit

- no student implementation code was executed;
- no MP6 output file was rewritten;
- code-only clean-room import search found no forbidden student imports;
- artifact size is approximately `16.6K` total for MP7 outputs.

Next phase justified: MP8 final archive and closeout.
