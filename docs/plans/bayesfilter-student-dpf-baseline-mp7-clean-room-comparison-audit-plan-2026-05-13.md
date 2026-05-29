# Plan: MP7 clean-room comparison audit

## Date

2026-05-13

## Status

Planned.  Execute only after MP6 exits with
`mp6_ready_for_student_comparison_audit` or `mp6_ready_with_caveats`.

## Goal

Compare the clean-room fixed-grid results against the quarantined student
aggregate evidence without using student agreement as correctness evidence.

This phase is an audit and interpretation phase.  It should not implement new
algorithms or expand the execution grid.

## Owned write set

Allowed:

- `experiments/controlled_dpf_baseline/reports/`;
- MP7 plan/audit/result notes whose filenames begin with
  `docs/plans/bayesfilter-student-dpf-baseline-mp7-`;
- `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`.

Out of scope:

- production `bayesfilter/`;
- DPF monograph files;
- `docs/references.bib`;
- vendored student code edits;
- changing MP6 outputs after the comparison begins, except to correct
  documented schema defects through a separate revision note.

## Student aggregate evidence

Use only these frozen student-lane reports and summaries:

- `experiments/student_dpf_baselines/reports/student-dpf-baseline-full-horizon-edh-pfpf-confirmation-result-2026-05-12.md`;
- `experiments/student_dpf_baselines/reports/outputs/full_horizon_edh_pfpf_confirmation_2026-05-12.json`;
- `experiments/student_dpf_baselines/reports/outputs/full_horizon_edh_pfpf_confirmation_summary_2026-05-12.json`.

Do not import student code or call student adapters.

The frozen MP6 inputs must be:

- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid_summary.json`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md`.

If any frozen file is absent, malformed, or renamed, MP7 must stop with
`mp7_needs_revision` or `mp7_blocked_or_excluded`; it must not choose alternate
inputs ad hoc.

## Hypotheses

### MP7-H1: clean-room results can be compared qualitatively to student aggregates

Criterion:

- the audit classifies each fixed-grid cell as same qualitative regime, worse,
  better, mixed, blocked, or not comparable.

Veto:

- comparison requires direct student execution or student implementation
  internals.

### MP7-H2: comparison remains proxy-only

Criterion:

- the report states that state RMSE, position RMSE, observation proxy RMSE, ESS,
  resampling, and runtime are proxy or diagnostic evidence.

Veto:

- the report treats student agreement as a correctness certificate.

### MP7-H3: next engineering decision is clear

Criterion:

- the audit recommends one of: final archive, MP5/MP6 revision, additional
  bounded experiment, or stop.

Veto:

- results are ambiguous and cannot be converted into a concrete next decision.

## Phase cycle

1. Plan: freeze MP6 outputs and comparison tables to use.
2. Execute: compute or write comparison summaries.
3. Test: verify that all MP6 fixed-grid cells and student aggregate cells are
   represented or explicitly marked unavailable.
4. Audit: check interpretation language, no overclaiming, no student-code
   imports, and no production/monograph drift.
5. Tidy: keep tables compact and reproducible.
6. Update reset memo: record comparison result and whether MP8 finalization is
   justified.

## Qualitative comparison rubric

The audit should compare each clean-room fixed-grid cell against the matching
student aggregate cell using proxy metrics only:

- `same_qualitative_regime`: required metrics are finite and position RMSE plus
  observation proxy RMSE are within a documented coarse factor of the student
  aggregate medians;
- `worse_proxy_regime`: metrics are finite but materially worse by the same
  documented factor;
- `better_proxy_regime`: metrics are finite and materially better, without
  claiming correctness;
- `blocked`: clean-room cell failed or lacks required metrics;
- `mixed_proxy_regime`: primary proxy metrics give conflicting better/worse
  signals or the two student aggregates disagree on the comparison class;
- `not_comparable`: semantics, output alignment, or required fields differ too
  much for a fair proxy comparison.

Fixed coarse factor: 2.0x for median position RMSE and observation proxy RMSE.
Do not tune this threshold during MP7.  ESS, resampling, and runtime are
diagnostic context, not primary regime classifiers.

Comparison unit:

- compare each clean-room MP6 cell separately against each student implementation
  aggregate in
  `full_horizon_edh_pfpf_confirmation_summary_2026-05-12.json`;
- the denominator for the 2.0x test is the matching student implementation's
  median metric for the same fixture, particle count, and flow-step setting;
- the per-student comparison keys are:
  - `2026MLCOE/<fixture>/N128/steps<flow_steps>`;
  - `advanced_particle_filter/<fixture>/N128/steps<flow_steps>`;
- do not average the two student medians before classification;
- the row-level final class is derived from the two per-student classes by the
  aggregation rules below.

Aggregation rules:

- if the clean-room cell is `blocked`, the final class is `blocked`;
- else if either per-student class is `not_comparable`, the final class is
  `not_comparable`;
- else if both per-student classes are identical, use that class;
- else if one per-student class is `same_qualitative_regime` and the other is
  `better_proxy_regime` or `worse_proxy_regime`, the final class is
  `mixed_proxy_regime`;
- else if one per-student class is `better_proxy_regime` and the other is
  `worse_proxy_regime`, the final class is `mixed_proxy_regime`;
- else any unlisted combination is `mixed_proxy_regime` and must be explained in
  the comparison report.

Deterministic edge-case rules:

- classify the clean-room cell as `blocked` before per-student comparison if it
  has no successful records or lacks a required metric;
- classify `not_comparable` if the student aggregate lacks the matching fixture,
  particle count, flow-step setting, metric name, or time-alignment semantics;
- classify `not_comparable` if either primary metric is missing for the student
  aggregate, even if diagnostic ESS or runtime is available;
- classify `same_qualitative_regime` only when both primary clean-room medians
  are within `[0.5x, 2.0x]` of the matching student aggregate median;
- classify `worse_proxy_regime` when either primary clean-room median is greater
  than `2.0x` the matching student aggregate median and neither metric is less
  than `0.5x` by enough to create a mixed signal;
- classify `better_proxy_regime` when both primary clean-room medians are less
  than `0.5x` the matching student aggregate median;
- classify `mixed_proxy_regime` when one primary metric is materially better and
  the other is materially worse, or when the two student implementations disagree
  about the comparison class for the same clean-room cell.

`mixed_proxy_regime` is diagnostic evidence only and must lead to either
`mp7_ready_with_caveats` or `mp7_needs_revision`, not an uncaveated final archive
recommendation.

The comparison must include a table for:

- low-noise N128/steps20;
- moderate N128/steps10;
- moderate N128/steps20.

The moderate-noise rows must preserve the diagnostic-variant interpretation.

## Inputs frozen for MP7

MP7 should name the exact MP6 JSON and summary files being compared.  If an MP6
schema defect is found, MP7 must stop or create a documented revision path; it
must not silently rewrite MP6 outputs.

## Required outputs

- comparison Markdown report:
  `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-comparison-audit.md`;
- comparison JSON:
  `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_comparison_audit.json`;
- comparison summary JSON:
  `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_comparison_audit_summary.json`;
- MP7 result note:
  `docs/plans/bayesfilter-student-dpf-baseline-mp7-clean-room-comparison-audit-result.md`.

These are phase-stable canonical paths.  A rerun or repair must deliberately
replace them and record the replacement in the MP7 result note and reset memo,
or stop and create a documented MP7 revision plan before MP8 consumes alternate
filenames.

The comparison JSON and summary JSON must preserve, for every clean-room cell:

- `fixture_name`;
- `num_particles`;
- `flow_steps`;
- clean-room median primary metrics;
- `per_student_classes`, keyed by `2026MLCOE` and
  `advanced_particle_filter`;
- per-student denominator medians for `position_rmse` and
  `observation_proxy_rmse`;
- `final_class`;
- `aggregation_rule`;
- `comparison_status`;
- any `not_comparable_reason` or `blocked_reason`.

## Required checks

- every MP6 fixed-grid cell is classified exactly once;
- every matching student aggregate cell is either used or explicitly marked
  unavailable;
- comparison JSON and summary JSON preserve both per-student classes and the
  derived final class for every clean-room cell;
- no student code execution occurs;
- no MP6 output file is rewritten;
- clean-room import search:

```bash
rg -n "experiments/student_dpf_baselines/vendor|advanced_particle_filter|2026MLCOE|from src\\.|import src\\." experiments/controlled_dpf_baseline
```

  Expected result: no matches, except literal path references inside reports
  that are clearly labeled as frozen comparison artifacts.

- path-scoped whitespace check:

```bash
git diff --check -- experiments/controlled_dpf_baseline docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md docs/plans/bayesfilter-student-dpf-baseline-mp7-clean-room-comparison-audit-plan-2026-05-13.md
```

## Exit decision

Use one of:

- `mp7_ready_for_final_archive`;
- `mp7_ready_with_caveats`;
- `mp7_needs_revision`;
- `mp7_blocked_or_excluded`.

Proceed to MP8 only if the comparison is caveated, reproducible, and does not
depend on student implementation internals.
