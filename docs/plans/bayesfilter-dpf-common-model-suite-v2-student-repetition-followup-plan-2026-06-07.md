# DPF Common Model Suite V2 Student Repetition Follow-Up Plan

metadata_date: 2026-06-07
status: DRAFT_AFTER_P7_STATIC_INVENTORY

## Purpose

Create a separate, reviewed student-repetition program after BF/FF v2 closure.
This plan must not treat BayesFilter, FilterFlow, either student repository, TT,
dense quadrature, simulated truth, or paper tables as an oracle.

## Entry Gate

- P0--P6 of the v2 BF/FF production common-suite program are closed.
- P7 static inventory is Claude-reviewed PASS.
- Any future execution plan has its own evidence contract and Claude review.

## Required Adapter Surface

Student adapters must expose the exact v2 frozen contract before any tie-out run:

- six model ids: `['lgssm_2d_h25_rich', 'sv_1d_h18_rich', 'range_bearing_4d_h20_rich', 'structural_ar1_quadratic_h16', 'spatial_sir_j3_rk4', 'predator_prey_rk4']`;
- density components: initial, transition, observation, scalar, float64;
- no-resampling fixed path: particles, observations, innovations, scalar log normalizer;
- fixed-ancestor path: fixed resampling flags and ancestor indices;
- fixed-branch AD gradients for declared physical knobs;
- FD diagnostics may be reported only as diagnostics, never as gates;
- artifact checksums, seeds, dtype, parameterization, scalar definition, and branch semantics.

## Phase Sketch

1. Build read-only contract adapters that translate v2 JSON fixtures into each student API without editing vendored student code.
2. Run adapter-surface dry checks that inspect shapes and required fields only.
3. Review by Claude before any student execution.
4. Execute density/path/gradient tie-outs only for cells whose exact contract equality is established before results.
5. Classify all cells as MATCHED, EXPLAINED_MISMATCH, INTERFACE_BLOCKED, or OUT_OF_SCOPE without correctness claims.

## Non-Claims

- No student correctness claim.
- No BF/FF oracle claim.
- Interface blocking is not student failure.
- Agreement, if later observed, is common-sense cross-implementation evidence only.
