# Reset Memo: DPF Filter Oracle Comparison

metadata_date: 2026-06-08
status: PASS_P7_FILTER_COMPARISON_CLOSEOUT

## Where The Run Stands

P0-P7 completed in the visible gated dialogue with Claude as read-only reviewer. P7 final closeout is promoted after final Claude review and records `PASS_P7_FILTER_COMPARISON_CLOSEOUT`.

## Main Conclusions

- No DPF row is promoted for correctness.
- LGSSM DPF rows are diagnostic only.
- P44 DPF rows are blocked pending numeric P5 bands and reviewed same-target adapters.
- Deterministic CUT4/Zhao-Cui rows are claim-class-separated certified approximations where supported, not exactness claims.
- No HMC, production, GPU, paper-scale, public API, or global ranking claim is made.

## Next Work

- dpf_numeric_band_amendment: Predeclare numeric P5 DPF value/score CI and max-error bands before any rerun.
- p44_dpf_adapter_probe: Build one reviewed same-target DPF adapter for P44-M2 dense scalar value and fixed-branch score before M3/M4.
- lgssm_dpf_directional_branch_probe: Add directional residuals and per-time branch records to the LGSSM DPF ladder.
- structured_metric_export: Export P44-M3/M4 and P3 exact-transformed reference uncertainty as JSON before calibration.
