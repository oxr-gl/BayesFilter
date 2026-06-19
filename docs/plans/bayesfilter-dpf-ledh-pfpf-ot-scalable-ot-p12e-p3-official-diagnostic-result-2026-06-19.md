# P12E-3 Result: Official Diagnostic

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-master-program-2026-06-19.md`

## Status

`P12E_3_OFFICIAL_DIAGNOSTIC_COMPLETED_VALID_ARTIFACTS`

## Phase Objective

Run the official P12E LEDH sparse-locality screen and write lane-owned
JSON/Markdown diagnostic artifacts.  This phase produces official diagnostic
evidence but does not write final lane interpretation.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What do the official deterministic LEDH-like fixture diagnostics say under the predeclared locality/truncation thresholds? |
| Baseline/comparator | Dense TensorFlow transport on the same LEDH-like post-flow particles, preserving Phase 1/Phase 8 orientation and truncation semantics. |
| Primary pass criterion | Passed: official JSON/Markdown artifacts exist, are readable, preserve required fields/non-claims, and record a valid decision status. |
| Reopen criterion | Not met. |
| Block criterion | Met: reviewed threshold promotion vetoes fired. |
| Veto diagnostics | No hard artifact/provenance/finite veto fired. Promotion vetoes fired for diffuse support and truncation residual checks. |
| Explanatory diagnostics | Runtime, memory, support curves outside the 99% screen, nearest-neighbor mass, LEDH diagnostics, and descriptive Phase 8 context. |
| Not concluded | No sparse solver validity, no speedup, no ranking, no posterior correctness, no HMC readiness, no public API/default readiness. |

## Commands And Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Official diagnostic | `PASS` | `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py --output docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.json --markdown-output docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.md` exited 0. |
| Artifact validation | `PASS` | Required top-level fields, roles, fixture fields, finite/provenance checks, official scope, P12E-4 handoff, and non-claims were present. |

TensorFlow printed a CUDA initialization warning during the CPU-scoped run.
The run manifest records `device_scope=cpu` and `cuda_visible_devices=-1`, and
the command exited 0; this is recorded as environment noise, not GPU evidence.

## Official Artifact Summary

| Field | Value |
| --- | --- |
| Official JSON | `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.json` |
| Official Markdown | `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.md` |
| Artifact scope | `official` |
| Status | `PASS` |
| P12E status | `LEDH_SPARSE_LOCALITY_SCREEN_COMPLETED_DOES_NOT_REOPEN_SPARSE_IMPLEMENTATION` |
| Diagnostic completed | `True` |
| Hard vetoes | `[]` |
| Promotion vetoes | `['ledh_lgssm_tiny_manual:truncated_row_residual_too_large', 'ledh_lgssm_moderate_clustered:median_99_support_too_large', 'ledh_lgssm_moderate_clustered:p90_99_support_too_large', 'ledh_lgssm_moderate_clustered:truncated_column_residual_too_large', 'ledh_lgssm_moderate_diffuse:median_99_support_too_large', 'ledh_lgssm_moderate_diffuse:p90_99_support_too_large', 'ledh_lgssm_moderate_diffuse:truncated_column_residual_too_large']` |

## Fixture Rows

| Fixture | Digest | N | Median k99 | P90 k99 | Trunc row residual | Trunc column residual | Trunc max particle error | Finite/provenance |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ledh_lgssm_tiny_manual` | `0e782f89ee79` | 8 | `8.000` | `8.000` | `3.010697e-02` | `2.676974e-03` | `1.870943e-03` | `PASS` |
| `ledh_lgssm_moderate_clustered` | `4c87456187f8` | 64 | `62.000` | `63.000` | `4.293260e-04` | `1.244273e-01` | `3.929614e-03` | `PASS` |
| `ledh_lgssm_moderate_diffuse` | `4137e761f73c` | 64 | `59.000` | `61.000` | `4.036299e-03` | `5.358002e-02` | `3.361478e-03` | `PASS` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `ADVANCE_TO_P12E_4_CLOSEOUT` | Official artifacts valid. | No hard veto fired; promotion vetoes fired, so reopen criterion is not met. | Synthetic LEDH-like fixtures may not represent a future frozen real LEDH run, but this does not invalidate the official artifact under the current contract. | Write final P12E result under P12E-4, preserving that sparse implementation is not reopened. | No sparse solver validity, speedup, ranking, posterior correctness, HMC/API/default/production readiness. |

## Next-Phase Handoff

P12E-4 may begin because:

- official command exited 0;
- official artifacts exist and passed validation;
- this P3 result note exists;
- current-agent status records `DIAGNOSTIC_RUN_COMPLETE`;
- P12E-4 subplan exists and passed Codex consistency review.
