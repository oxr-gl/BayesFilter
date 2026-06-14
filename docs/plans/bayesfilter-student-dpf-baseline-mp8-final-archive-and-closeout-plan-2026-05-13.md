# Plan: MP8 final archive and closeout

## Date

2026-05-13

## Status

Planned.  Execute only after MP7 exits with `mp7_ready_for_final_archive` or
`mp7_ready_with_caveats`.

## Goal

Close the student DPF experimental-baseline program by packaging the evidence,
final caveats, and recommended future use.  The finish line is a durable
quarantined baseline archive, not production code.

## Owned write set

Allowed:

- final summary documents under `docs/plans/` whose filenames begin with
  `bayesfilter-student-dpf-baseline-mp8-`;
- existing student-baseline master and reset memo;
- final index or README updates under `experiments/student_dpf_baselines/` and
  `experiments/controlled_dpf_baseline/`.

Out of scope:

- production `bayesfilter/`;
- DPF monograph files;
- `docs/references.bib`;
- vendored student source edits;
- broad new experiments.

## Final finishing line

The program is complete when:

1. student snapshots have provenance and permissions recorded;
2. reproduction, adapter, linear, nonlinear, flow, and clean-room phases have
   result notes or structured blocker records;
3. the clean-room controlled baseline has a final report or a documented
   blocker;
4. every claim is labeled as comparison-only, proxy-only, reference-backed, or
   blocked;
5. no production or monograph claim depends on student code;
6. master program and reset memo both identify the program as complete or
   complete-with-caveats;
7. path-scoped final commit excludes monograph, production, references, and
   vendored student edits.

## Required artifact checklist

MP8 must verify every required artifact by exact path.  Missing paths are a hard
stop unless the closeout classifies the corresponding phase as blocked with a
linked blocker note.

Governance:

- `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-master-program-and-final-subplans-audit-2026-05-13.md`.

Student snapshot provenance:

- `experiments/student_dpf_baselines/sources.yml`;
- `experiments/student_dpf_baselines/PERMISSIONS.md`;
- `experiments/student_dpf_baselines/vendor/SNAPSHOT.md`.

Clean-room specification:

- `docs/plans/bayesfilter-student-dpf-baseline-clean-room-controlled-baseline-spec-2026-05-13.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-clean-room-controlled-baseline-spec-audit-2026-05-13.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-clean-room-controlled-baseline-spec-result-2026-05-13.md`.

Final clean-room phase outputs:

- `docs/plans/bayesfilter-student-dpf-baseline-mp5-clean-room-implementation-result.md`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke.json`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke_summary.json`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-smoke-result.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp6-clean-room-fixed-grid-execution-result.md`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid_summary.json`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp7-clean-room-comparison-audit-result.md`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_comparison_audit.json`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_comparison_audit_summary.json`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-comparison-audit.md`.

Student aggregate comparison inputs:

- `experiments/student_dpf_baselines/reports/student-dpf-baseline-full-horizon-edh-pfpf-confirmation-result-2026-05-12.md`;
- `experiments/student_dpf_baselines/reports/outputs/full_horizon_edh_pfpf_confirmation_2026-05-12.json`;
- `experiments/student_dpf_baselines/reports/outputs/full_horizon_edh_pfpf_confirmation_summary_2026-05-12.json`.

## Required closeout sections

The final closeout note must include:

- executive status and final decision label;
- phase index linking MP0 through MP8 plans, audits, reports, and blockers;
- artifact index for student snapshots, student reports, controlled-baseline
  reports, and reset/master records;
- claim ledger labeling each major claim as `reference_backed`,
  `proxy_only`, `comparison_only`, `blocked`, or `out_of_scope`;
- final caveats and prohibited uses;
- recommended future work separated into:
  - optional student-lane research;
  - separate production BayesFilter work;
  - separate monograph/documentation work;
- final lane-boundary verification and commit scope.

The canonical closeout note path is:

`docs/plans/bayesfilter-student-dpf-baseline-mp8-final-archive-and-closeout-result.md`.

This is a phase-stable canonical path.  A rerun or repair must deliberately
replace it and record the replacement in the reset memo, or stop and create a
documented MP8 revision plan before claiming final closeout.

## Hypotheses

### MP8-H1: the program evidence can be archived coherently

Criterion:

- one final closeout note links the governing master, reset memo, all major
  phase plans/results, and final clean-room comparison evidence.

Veto:

- unresolved artifacts cannot be classified as completed, caveated, or blocked.

### MP8-H2: final claims remain bounded

Criterion:

- final closeout explicitly states what the student evidence can and cannot be
  used for.

Veto:

- final text promotes student code to production or uses student agreement as a
  correctness certificate.

### MP8-H3: future work is clearly separated

Criterion:

- future production work, monograph work, or deeper algorithm research is listed
  as separate follow-on work requiring separate plans.

Veto:

- closeout silently authorizes production edits or monograph edits.

## Phase cycle

1. Plan: identify all phase outputs and unresolved blockers.
2. Execute: write final archive/closeout note and update indexes.
3. Test: check links, report fields, lane boundaries, and claim labels.
4. Audit: review final package for missing phases, overclaims, production drift,
   monograph drift, and vendored-code drift.
5. Tidy: keep final files concise and remove transient artifacts.
6. Update reset memo: mark program complete or complete-with-caveats.

## Required checks

- link/path check for every closeout artifact reference;
- search for overclaiming terms such as production correctness, certificate, or
  monograph proof unless they are explicitly prohibited-use statements;
- production import-boundary search;
- vendored student dirt check;
- `git diff --check`;
- path-scoped staging review.

## Exit decision

Use one of:

- `student_dpf_baseline_program_complete`;
- `student_dpf_baseline_program_complete_with_caveats`;
- `student_dpf_baseline_program_needs_revision`;
- `student_dpf_baseline_program_blocked`.

No further student-baseline phase should run after MP8 unless a new master
program revision is explicitly approved.
