# DPF V2 Algorithm Full Comparison P1 Architecture Report

metadata_date: 2026-06-07
visible_execution_timestamp: `2026-06-08T02:15:50+08:00`
phase: P1
status: `PASS_P1_ARCHITECTURE_READY_FOR_P2`

## Summary

P1 freezes the BF/FilterFlow architecture for bootstrap-OT and LEDH-PFPF-OT
across all six V2 rows. Claude read-only review returned `VERDICT: AGREE`, so
the architecture is ready for P2/P5 contract freeze.

All FilterFlow-side work is adapter-hosted in BayesFilter-owned experiment code.
No mutation of `.localsource/filterflow` is required.

## Required Rows

1. `lgssm_2d_h25_rich`
2. `sv_1d_h18_rich`
3. `range_bearing_4d_h20_rich`
4. `structural_ar1_quadratic_h16`
5. `spatial_sir_j3_rk4`
6. `predator_prey_rk4`

## Architecture Matrix

| Surface | Cells | Status |
| --- | --- | --- |
| bootstrap-OT BF | 6 | `ARCHITECTURE_READY_FOR_CONTRACT_FREEZE` |
| bootstrap-OT FF adapter | 6 | `ARCHITECTURE_READY_FOR_CONTRACT_FREEZE` |
| LEDH-PFPF-OT BF | 6 | `ARCHITECTURE_READY_FOR_CONTRACT_FREEZE` |
| LEDH-PFPF-OT FF adapter | 6 | `ARCHITECTURE_READY_FOR_CONTRACT_FREEZE` |

## Key Decisions

- Bootstrap-OT proposal equals transition model.
- LEDH-PFPF-OT uses transition proposal, local affine LEDH flow, PF-PF
  correction, and FilterFlow-style annealed OT.
- PF-PF correction is
  `previous_log_weight + target_transition + target_observation -
  pre_flow_log_density + forward_log_det`.
- LEDH is not native FilterFlow support; it is BayesFilter-owned
  FilterFlow-side adapter work.
- P1 makes no numerical agreement claim.

## Veto Results

| Veto | Status |
| --- | --- |
| `.localsource/filterflow` mutation required | PASS |
| missing V2 row | PASS |
| bootstrap/LEDH surfaces conflated | PASS |
| LEDH proposal density/logdet unstated | PASS |
| model convention mismatch accepted | PASS |

## Next Gate

Begin P2 `PRECHECK` visibly in the current dialogue.
