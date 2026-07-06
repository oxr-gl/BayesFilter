# Low-Rank TF32 Scale Smoke Diagnostics

- Status: `PASS`
- Phase: `LR-TF32-2B`
- Mode: `tuning-cpu`
- Algorithm: `P = Q diag(1/g) R^T lazy low-rank solver-route resampling`
- Hard vetoes: `[]`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| num_rows | `14` | explanatory |
| num_executed_rows | `14` | explanatory |
| num_hard_vetoes | `0` | hard veto |
| num_viable_rows | `2` | explanatory |
| max_factor_marginal_residual | `9.289375157095492e-06` | hard veto |
| max_induced_row_residual | `0.038049161434173584` | hard veto |
| max_induced_column_residual | `0.03167521953582764` | hard veto |
| max_output_log_weight_normalization_residual | `0.0` | hard veto |
| max_weighted_mean_abs_error | `0.0020215660333633423` | hard veto |
| max_weighted_second_moment_abs_error | `0.10586152970790863` | hard veto |
| max_tiny_materialized_apply_parity | `None` | hard veto |
| max_wall_time_seconds_explanatory | `3.084677729057148` | explanatory |
| total_wall_time_seconds_explanatory | `32.4395371240098` | explanatory |
| max_memory_maxrss_kb_explanatory | `489840` | explanatory |

## Rows

| N | Rank | Epsilon | Status | Hard vetoes | Factor residual | Row residual | Column residual | Mean error | Second error | Dense materialized |
| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 4096 | `64` | `0.05` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `8.009374141693115e-08` | `9.5367431640625e-07` | `1.430511474609375e-06` | `7.450580596923828e-08` | `0.10534848272800446` | `False` |
| 4096 | `64` | `0.04` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `4.470348358154297e-08` | `5.364418029785156e-06` | `4.172325134277344e-06` | `2.384185791015625e-07` | `0.09661389887332916` | `False` |
| 4096 | `64` | `0.03125` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `3.5390257835388184e-08` | `4.8160552978515625e-05` | `4.661083221435547e-05` | `3.1739473342895508e-06` | `0.08814609050750732` | `False` |
| 4096 | `64` | `0.025` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `8.009374141693115e-08` | `0.0002592802047729492` | `0.0003281831741333008` | `2.300739288330078e-05` | `0.0814591646194458` | `False` |
| 4096 | `64` | `0.02` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `2.8559588827192783e-07` | `0.001170039176940918` | `0.0011608600616455078` | `9.943544864654541e-05` | `0.07558682560920715` | `False` |
| 4096 | `64` | `0.015625` | `PASS` | `[]` | `9.051291272044182e-07` | `0.0037071704864501953` | `0.003115415573120117` | `0.00031322240829467773` | `0.0698426365852356` | `False` |
| 4096 | `64` | `0.01` | `FAIL` | `['induced_row_residual_threshold', 'induced_column_residual_threshold']` | `9.289375157095492e-06` | `0.038049161434173584` | `0.03167521953582764` | `0.0018656104803085327` | `0.06123611330986023` | `False` |
| 4096 | `128` | `0.05` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `4.470348358154297e-08` | `5.960464477539062e-07` | `9.5367431640625e-07` | `7.450580596923828e-08` | `0.10586152970790863` | `False` |
| 4096 | `128` | `0.04` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `2.7008354663848877e-08` | `7.092952728271484e-06` | `5.245208740234375e-06` | `2.980232238769531e-07` | `0.09752510488033295` | `False` |
| 4096 | `128` | `0.03125` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `2.421438694000244e-08` | `7.456541061401367e-05` | `5.424022674560547e-05` | `4.388391971588135e-06` | `0.08961069583892822` | `False` |
| 4096 | `128` | `0.025` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `9.185168892145157e-08` | `0.0003554821014404297` | `0.0003764629364013672` | `2.5391578674316406e-05` | `0.083382248878479` | `False` |
| 4096 | `128` | `0.02` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `3.2506068237125874e-07` | `0.001278519630432129` | `0.0013315677642822266` | `0.00011017918586730957` | `0.07790617644786835` | `False` |
| 4096 | `128` | `0.015625` | `PASS` | `[]` | `9.381328709423542e-07` | `0.0038427114486694336` | `0.00345611572265625` | `0.00032529234886169434` | `0.07270905375480652` | `False` |
| 4096 | `128` | `0.01` | `FAIL` | `['induced_row_residual_threshold', 'induced_column_residual_threshold']` | `8.533912478014827e-06` | `0.034954965114593506` | `0.026285290718078613` | `0.0020215660333633423` | `0.06390997767448425` | `False` |

## Run Manifest

- Git commit: `43bcb2015127712705d7ac77d3f0c9b01d349733`
- Command: `docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py --mode tuning-cpu --phase-id LR-TF32-2B --phase-result-path docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02b-focused-tuning-result-2026-06-20.md --particle-counts 4096 --batch-size 2 --state-dim 8 --tuning-ranks 64 128 --tuning-assignment-epsilons 0.05 0.04 0.03125 0.025 0.02 0.015625 0.01 --dtype float32 --fixture-id bounded_smooth_v1 --output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-focused-tuning-cpu-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-focused-tuning-cpu-2026-06-20.md`
- Device scope: `cpu`
- CUDA_VISIBLE_DEVICES: `-1`
- TF32 requested: `default`
- TF32 execution recorded: `True`
- Fixture: `bounded_smooth_v1`

## Non-Claims

- low-rank TF32 scale-smoke diagnostic only
- no speedup claim
- no ranking claim
- no superiority claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no production/default readiness claim
- no dense Sinkhorn equivalence claim
- no full low-rank Sinkhorn solver-fidelity claim
- no broad scalable-OT selection claim
- no TF32-help claim
