# Holiday reset memo: student DPF experimental-baseline lane

## Date

2026-05-16

## Purpose

This memo is a compact handoff for resuming the student DPF experimental
baseline work after a break.  It is scoped only to the quarantined student DPF
lane.  It is not a monograph-writing memo and it is not a production
BayesFilter implementation memo.

## Active Lane

Active governing program:

- `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`

Active reset memo:

- `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`

Owned surfaces:

- `experiments/student_dpf_baselines/`
- `experiments/controlled_dpf_baseline/`
- `docs/plans/bayesfilter-student-dpf-baseline-*`

Forbidden surfaces for this lane:

- `bayesfilter/` production code
- `docs/chapters/`
- `docs/references.bib`
- DPF monograph/reviewer-grade plans and reset memos
- vendored student source edits under `experiments/student_dpf_baselines/vendor/`

## Repository State At Handoff

Current branch: `main`.

Current pushed head:

- `185c414 Add student DPF experiment replication artifacts`

Remote status at memo creation:

- `main` matches `origin/main`
- there are no committed-but-unpushed commits

Recently pushed experiment replication artifacts:

- clean-room controlled baseline package under `experiments/controlled_dpf_baseline/`
- clean-room smoke, fixed-grid, and comparison-audit outputs
- future-work usability gate runner and outputs under `experiments/student_dpf_baselines/`

Local uncommitted student-plan files still exist and should be reviewed before
any future plan commit:

- modified:
  - `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`
  - `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`
- untracked:
  - `docs/plans/bayesfilter-student-dpf-baseline-blocker-debug-master-program-2026-05-15.md`
  - `docs/plans/bayesfilter-student-dpf-baseline-future-work-usability-gates-plan-2026-05-15.md`
  - `docs/plans/bayesfilter-student-dpf-baseline-master-program-and-final-subplans-audit-2026-05-13.md`
  - `docs/plans/bayesfilter-student-dpf-baseline-mp5-clean-room-implementation-plan-2026-05-13.md`
  - `docs/plans/bayesfilter-student-dpf-baseline-mp5-clean-room-implementation-result.md`
  - `docs/plans/bayesfilter-student-dpf-baseline-mp6-clean-room-fixed-grid-execution-plan-2026-05-13.md`
  - `docs/plans/bayesfilter-student-dpf-baseline-mp6-clean-room-fixed-grid-execution-result.md`
  - `docs/plans/bayesfilter-student-dpf-baseline-mp7-clean-room-comparison-audit-plan-2026-05-13.md`
  - `docs/plans/bayesfilter-student-dpf-baseline-mp7-clean-room-comparison-audit-result.md`
  - `docs/plans/bayesfilter-student-dpf-baseline-mp8-final-archive-and-closeout-plan-2026-05-13.md`
  - `docs/plans/bayesfilter-student-dpf-baseline-mp8-final-archive-and-closeout-result.md`

Do not assume those plan files are already pushed.  The experiment artifacts
needed for replication across machines were committed and pushed; the plan
documentation still needs a separate review/commit decision.

## Completed State

The student DPF baseline program is complete with caveats as a quarantined
comparison package.

Key completed outputs:

- source snapshots are provenance-recorded and protected from upstream drift;
- student code remains comparison-only;
- linear Kalman-path comparisons matched independent references in prior phases;
- kernel PFF remains excluded from routine panels;
- clean-room controlled baseline was implemented under `experiments/`;
- MP5 smoke execution passed;
- MP6 fixed-grid execution produced 15/15 `ok` records;
- MP7 proxy comparison classified all three clean-room cells as
  `same_qualitative_regime`;
- MP8 closed the student DPF archive as
  `student_dpf_baseline_program_complete_with_caveats`;
- future-work usability gates completed as
  `future_work_usability_gates_complete`.

Important pushed artifacts:

- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke.json`
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json`
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_comparison_audit.json`
- `experiments/student_dpf_baselines/reports/outputs/future_work_usability_gates_2026-05-15.json`
- `experiments/student_dpf_baselines/reports/outputs/future_work_usability_gates_summary_2026-05-15.json`

## Current Evidence Summary

Clean-room fixed-grid result:

- planned records: `15`
- successful records: `15`
- blocked records: `0`
- failed records: `0`
- runtime warnings: `0`
- successful records with finite required metrics: `15`

Clean-room comparison audit:

- planned cells: `3`
- classified cells: `3`
- all cells represented: `true`
- final class counts: `same_qualitative_regime: 3`
- decision: `mp7_ready_for_final_archive`

Future-work usability gates:

- final label: `future_work_usability_gates_complete`
- planned execution probes: `15`
- observed execution records: `15`
- total records including contract audits: `30`
- status counts: `ok: 24`, `blocked: 6`
- veto diagnostic fired: `false`

Family decisions from future-work gates:

- differentiable resampling: `component_spec_next`
- neural OT: `component_spec_next`
- stochastic flow: `clean_room_spec_next`
- DPF: `clean_room_spec_next`
- neural resampling: `debug_gate_next`
- dPFPF: `debug_gate_next`

## Remaining Blockers

The following are student-lane blockers, not production blockers:

1. MLCOE transformer resampler:
   - current class: `blocked_environment_drift`
   - observed issue: shape error in `WeightedMultiHeadAttention.call`
   - next action if pursued: bounded debug gate only

2. Advanced TF DPF soft resampling:
   - current class: `blocked_environment_drift`
   - observed issue: TensorFlow loop shape-invariant error
   - next action if pursued: bounded forward/gradient debug gate only

3. MLCOE stochastic flow:
   - current class: `blocked_missing_assumption`
   - missing contract: exact model, covariance, and observation semantics
   - next action if pursued: contract audit before execution

4. MLCOE dPFPF:
   - current class: `blocked_missing_assumption`
   - missing contract: exact model plus flow/resampling semantics
   - next action if pursued: contract audit before execution

5. Kernel PFF:
   - current class: excluded from routine panels
   - reason: previous bounded checks found long runtime or iteration-cap behavior
   - next action if pursued: independent kernel PFF debug program only

## What Is Usable Now

Usable for replication and comparison:

- frozen student snapshots;
- student adapter and aggregate result artifacts;
- clean-room controlled baseline package under `experiments/`;
- fixed-grid JSON outputs and reports;
- future-work usability gate outputs.

Usable as inputs to future BayesFilter-owned clean-room specification work:

- non-neural differentiable resampling API smokes;
- successful student-lane DPF smokes;
- successful stochastic-flow smokes;
- advanced amortized OT as component-only evidence, with artifact caveats.

Not usable as production code:

- any student implementation;
- the clean-room prototype;
- any debug shim;
- any neural or DPF path without a separate BayesFilter-owned implementation
  plan, production contract, and tests.

## Recommended Restart Sequence

1. Run `git status --short --branch` and verify that only student-plan docs are
   dirty.
2. Review the uncommitted student-plan files listed above.
3. Decide whether to commit those plan/result docs as historical governance
   records.
4. If continuing the optional blocker work, start from:
   `docs/plans/bayesfilter-student-dpf-baseline-blocker-debug-master-program-2026-05-15.md`.
5. Audit that blocker-debug program before execution.
6. Execute only bounded DBG gates that do not edit vendored source, production
   code, monograph files, or references.
7. If starting BayesFilter-owned implementation work, create a separate
   production or clean-room implementation master plan.  Do not treat student
   code as the implementation.

## Validation Commands Worth Reusing

Experiment artifact checks:

```bash
git diff --check -- experiments
python -m experiments.controlled_dpf_baseline.runners.validate_results --records-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke.json --summary-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke_summary.json --expected-records 1 --require-finite-success-metrics --require-smoke-only
python -m experiments.controlled_dpf_baseline.runners.validate_results --records-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json --summary-json experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid_summary.json --expected-records 15 --require-finite-success-metrics --require-fixed-grid
CUDA_VISIBLE_DEVICES=-1 python -m experiments.student_dpf_baselines.runners.run_future_work_usability_gates --validate-only
```

Syntax check:

```bash
python -m py_compile experiments/controlled_dpf_baseline/results.py experiments/controlled_dpf_baseline/metrics.py experiments/controlled_dpf_baseline/fixtures/range_bearing.py experiments/controlled_dpf_baseline/prototypes/particle_flow_baseline.py experiments/controlled_dpf_baseline/runners/run_smoke.py experiments/controlled_dpf_baseline/runners/run_fixed_grid.py experiments/controlled_dpf_baseline/runners/validate_results.py experiments/student_dpf_baselines/runners/run_future_work_usability_gates.py
```

## Do Not Conclude

Do not conclude that:

- student code is production-ready;
- agreement between student and clean-room proxies proves correctness;
- the clean-room prototype is a production BayesFilter implementation;
- neural OT or learned resampling is scientifically validated;
- blocked paths invalidate the research direction;
- this student-lane archive is automatically monograph evidence.

The correct conclusion is narrower: the student DPF lane now has a reproducible,
quarantined comparison archive and a clean-room experimental baseline that can
inform future independently implemented BayesFilter work.

## Next Best Action

For bookkeeping, commit the student-plan documentation separately after review.
For technical progress, either:

- execute the optional blocker-debug master program if the remaining blocked
  student surfaces matter; or
- move on to a separate BayesFilter-owned clean-room implementation/specification
  program using only the quarantined archive as comparison evidence.
