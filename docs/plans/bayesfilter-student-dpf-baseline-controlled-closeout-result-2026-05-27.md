# Result: student DPF controlled-baseline closeout

## Date

2026-05-27

## Decision

`student_dpf_controlled_baseline_archive_complete`

## Scope

This result records the execution of the controlled-baseline closeout plan for
the quarantined student DPF experimental-baseline lane.

No experiments were executed.  No production `bayesfilter/` code, monograph
chapter files, references, or vendored student snapshots were edited.

## Evidence Reviewed

- reset memo:
  `docs/plans/bayesfilter-student-dpf-baseline-reset-memo-2026-05-09.md`;
- master program:
  `docs/plans/bayesfilter-student-dpf-baseline-master-program-2026-05-10.md`;
- controlled-baseline README:
  `experiments/controlled_dpf_baseline/README.md`;
- MP5 smoke result:
  `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-smoke-result.md`;
- MP6 fixed-grid result:
  `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md`;
- MP7 comparison audit:
  `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-comparison-audit.md`;
- future-work usability gates:
  `experiments/student_dpf_baselines/reports/student-dpf-baseline-future-work-usability-gates-result-2026-05-15.md`.

## Work Completed

1. Created a narrow closeout plan and skeptical pre-execution audit:
   - `docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-plan-2026-05-27.md`;
   - `docs/plans/bayesfilter-student-dpf-baseline-controlled-closeout-plan-audit-2026-05-27.md`.
2. Updated the reset memo so the active next-phase state is archive-complete
   rather than implementation-plan handoff.
3. Updated the master program so the current decision is
   `student_dpf_controlled_baseline_archive_complete`.
4. Corrected the controlled-baseline README authority list by replacing a stale
   reference to the missing
   `docs/plans/bayesfilter-student-dpf-baseline-mp5-clean-room-implementation-plan-2026-05-13.md`
   path with existing authoritative artifacts.
5. Added the final archive report:
   `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-final-archive-result.md`.

## Result Interpretation

The student DPF experimental-baseline lane is complete as a quarantined
controlled-baseline archive.

This closeout rests on existing artifacts:

- MP5 smoke decision `mp5_smoke_ok`;
- MP6 fixed-grid decision `mp6_fixed_grid_ok`;
- MP7 proxy comparison decision `mp7_ready_for_final_archive`;
- future-work usability decision `future_work_usability_gates_complete`.

The closeout does not add scientific or production evidence beyond those
artifacts.  It repairs continuity, authority pointers, and archive status.

## Persistent Caveats

- Student code remains comparison-only.
- Student agreement is not a correctness certificate.
- The clean-room controlled baseline is not production `bayesfilter/` code.
- The archive does not validate HMC readiness, DPF-HMC targets, monograph claims,
  model-risk use, banking use, or production readiness.
- Kernel PFF remains excluded from routine panels pending debug.
- Differentiable resampling and neural OT require component specifications.
- DPF and stochastic flow require clean-room specifications.
- dPFPF and neural resampling require debug gates.

## Next Status

No further work is required to finish this archived lane.  Any future
student-DPF-adjacent work must begin from a separate scoped plan and evidence
contract.
