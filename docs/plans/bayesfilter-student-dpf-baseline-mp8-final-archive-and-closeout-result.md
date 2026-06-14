# Result: MP8 final archive and closeout

## Executive Status

Decision: `student_dpf_baseline_program_complete_with_caveats`.

The student DPF experimental-baseline stream is now closed as a quarantined
evidence package.  It includes fixed student snapshots, reproduction and adapter
evidence, nonlinear and flow proxy panels, a BayesFilter-owned clean-room
controlled baseline, a fixed-grid execution panel, and a proxy-only comparison
audit.

This closeout does not promote student code or the clean-room prototype to
production.  It does not create monograph evidence.

## Phase Index

| Phase | Status | Primary Evidence |
| --- | --- | --- |
| MP0 governance | complete | `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md` |
| MP1 MLCOE particle adapter gate | complete | `docs/plans/bayesfilter-student-dpf-baseline-mp1-mlcoe-particle-adapter-plan-audit-2026-05-10.md` |
| MP2 nonlinear reference/proxy spine | complete | `docs/plans/bayesfilter-student-dpf-baseline-mp2-nonlinear-reference-spine-plan-audit-2026-05-10.md` |
| MP3 kernel PFF debug gate | complete with exclusion | `docs/plans/bayesfilter-student-dpf-baseline-mp3-kernel-pff-debug-gate-plan-audit-2026-05-11.md` |
| MP4 flow/DPF readiness review | complete | `docs/plans/bayesfilter-student-dpf-baseline-mp4-flow-dpf-readiness-review-plan-audit-2026-05-11.md` |
| Clean-room specification | complete | `docs/plans/bayesfilter-student-dpf-baseline-clean-room-controlled-baseline-spec-result-2026-05-13.md` |
| MP5 clean-room scaffold | complete | `docs/plans/bayesfilter-student-dpf-baseline-mp5-clean-room-implementation-result.md` |
| MP6 fixed-grid execution | complete | `docs/plans/bayesfilter-student-dpf-baseline-mp6-clean-room-fixed-grid-execution-result.md` |
| MP7 comparison audit | complete | `docs/plans/bayesfilter-student-dpf-baseline-mp7-clean-room-comparison-audit-result.md` |
| MP8 final archive | complete with caveats | this note |

## Artifact Index

Governance and reset:

- `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-master-program-and-final-subplans-audit-2026-05-13.md`.

Student snapshot provenance:

- `experiments/student_dpf_baselines/sources.yml`;
- `experiments/student_dpf_baselines/PERMISSIONS.md`;
- `experiments/student_dpf_baselines/vendor/SNAPSHOT.md`.

Clean-room controlled-baseline specification and outputs:

- `docs/plans/bayesfilter-student-dpf-baseline-clean-room-controlled-baseline-spec-2026-05-13.md`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp5-clean-room-implementation-result.md`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_smoke.json`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp6-clean-room-fixed-grid-execution-result.md`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid.json`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_fixed_grid_summary.json`;
- `docs/plans/bayesfilter-student-dpf-baseline-mp7-clean-room-comparison-audit-result.md`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_comparison_audit.json`;
- `experiments/controlled_dpf_baseline/reports/outputs/clean_room_controlled_baseline_comparison_audit_summary.json`.

Frozen student aggregate comparison inputs:

- `experiments/student_dpf_baselines/reports/student-dpf-baseline-full-horizon-edh-pfpf-confirmation-result-2026-05-12.md`;
- `experiments/student_dpf_baselines/reports/outputs/full_horizon_edh_pfpf_confirmation_2026-05-12.json`;
- `experiments/student_dpf_baselines/reports/outputs/full_horizon_edh_pfpf_confirmation_summary_2026-05-12.json`.

## Clean-Room Final Evidence

MP6 fixed-grid execution:

- 15/15 planned clean-room records returned `ok`;
- all successful records had finite required metrics;
- no runtime warnings were observed;
- no student implementation code was imported or executed.

MP7 comparison:

- low-noise N128/steps20: `same_qualitative_regime`;
- moderate N128/steps10: `same_qualitative_regime`;
- moderate N128/steps20: `same_qualitative_regime`;
- all classifications are proxy-only and use the fixed 2.0x qualitative regime
  rule.

## Claim Ledger

| Claim | Label | Status |
| --- | --- | --- |
| Student snapshots are provenance-recorded and internally usable for comparison. | `comparison_only` | supported |
| Linear Kalman-path student comparisons matched independent references. | `reference_backed` | supported by earlier phase reports |
| Kernel PFF is routine-panel ready. | `blocked` | false; excluded pending separate debug |
| Student EDH/PFPF aggregate evidence can guide a clean-room target. | `comparison_only` | supported with caveats |
| Clean-room fixed-grid records completed with finite proxy metrics. | `proxy_only` | supported |
| Clean-room results are in the same qualitative proxy regime as frozen student aggregates. | `proxy_only` | supported under fixed 2.0x rule |
| Student agreement proves correctness. | `out_of_scope` | prohibited |
| Any student code is production-ready. | `out_of_scope` | prohibited |
| Clean-room prototype is production BayesFilter code. | `out_of_scope` | prohibited |
| This archive is monograph evidence. | `out_of_scope` | prohibited without separate review |

## Caveats And Prohibited Uses

Allowed uses:

- reproducibility reference for the quarantined student DPF work;
- comparison-only benchmark evidence;
- failure-mode inventory;
- clean-room experimental baseline evidence.

Prohibited uses:

- production correctness certificate;
- production API authority;
- monograph evidence without separate review;
- copied student implementation source;
- broad new experiments without a new student-lane master revision.

## Future Work

Optional student-lane research:

- run a separate kernel PFF debug program if that path becomes important;
- add a new clean-room experiment only through a new master revision;
- investigate why moderate-noise steps10 and steps20 remain diagnostic variants
  rather than a single clear policy.

Separate production BayesFilter work:

- reimplement any useful ideas independently in production code only through a
  separate production plan;
- add production tests only after the production contract is defined.

Separate monograph/documentation work:

- cite this archive only after a separate documentation review determines what,
  if anything, is appropriate for reader-facing material.

## Final Verification

- Required MP8 artifact checklist passed: all 24 required artifacts exist.
- Code-only clean-room import search found no forbidden student imports.
- No vendored student files were edited.
- No production `bayesfilter/`, monograph chapter, or `docs/references.bib`
  edits were required by MP5-MP8.

Final label:
`student_dpf_baseline_program_complete_with_caveats`.
