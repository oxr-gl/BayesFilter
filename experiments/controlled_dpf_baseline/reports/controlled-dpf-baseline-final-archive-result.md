# Controlled DPF Baseline Final Archive Result

## Decision

`student_dpf_controlled_baseline_archive_complete`

## Scope

This report closes the BayesFilter-owned controlled DPF baseline inside the
quarantined student DPF experimental-baseline lane.  It archives existing MP5,
MP6, and MP7 artifacts; it does not execute new experiments and does not promote
student or clean-room code into production.

## Evidence Reviewed

| Artifact | Decision | Key result |
| --- | --- | --- |
| `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-smoke-result.md` | `mp5_smoke_ok` | 1/1 smoke record ok; no blocked, failed, or runtime-warning records. |
| `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md` | `mp6_fixed_grid_ok` | 15/15 fixed-grid records ok; no blocked, failed, or runtime-warning records. |
| `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-comparison-audit.md` | `mp7_ready_for_final_archive` | All three fixed-grid cells are in the same qualitative proxy regime as frozen student aggregate summaries under the fixed 2.0x rule. |
| `experiments/student_dpf_baselines/reports/student-dpf-baseline-future-work-usability-gates-result-2026-05-15.md` | `future_work_usability_gates_complete` | Future surfaces are classified into component-spec, clean-room-spec, debug-gate, or deferred paths. |

## Archive Interpretation

- The controlled baseline is a BayesFilter-owned experimental artifact under
  `experiments/controlled_dpf_baseline/`.
- Student implementation source was not imported or executed by MP5--MP7.
- MP7 qualitative agreement with frozen student aggregate summaries is proxy
  evidence only.
- Moderate-noise 10-step and 20-step settings remain diagnostic variants; there
  is no universal moderate-noise flow-step winner.
- The final archive is complete for the first fixed controlled baseline target
  grid.

## Persistent Caveats

- This archive is not production `bayesfilter/` code.
- This archive is not a public API.
- This archive is not an HMC-readiness certificate.
- This archive is not monograph evidence without a separate review.
- Student agreement is not a correctness certificate.
- State RMSE, position RMSE, observation proxy RMSE, ESS, resampling, and runtime
  remain proxy or diagnostic evidence.
- Kernel PFF remains excluded from routine panels pending debug.
- Differentiable resampling and neural OT require component specifications
  before further use.
- DPF and stochastic flow require clean-room specifications before further use.
- dPFPF and neural resampling require debug gates before further use.

## README Authority Correction

During closeout, the controlled-baseline README was found to cite
`docs/plans/bayesfilter-student-dpf-baseline-mp5-clean-room-implementation-plan-2026-05-13.md`.
That path is not present in the repository.  The README was corrected to cite
existing authoritative artifacts: the master program, clean-room specification,
closeout plan/audit, MP5 smoke result, MP6 fixed-grid result, MP7 comparison
audit, and this final archive report.

## Final Status

The student DPF controlled-baseline lane is closed as a quarantined experimental
archive.  Future work must begin from a separate scoped plan and evidence
contract rather than extending this archive.
