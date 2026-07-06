# Low-Rank TF32 Scale Smoke Diagnostics

- Status: `FAIL`
- Phase: `LR-TF32-2A`
- Mode: `tuning-cpu`
- Algorithm: `P = Q diag(1/g) R^T lazy low-rank solver-route resampling`
- Hard vetoes: `['tuning_grid_no_viable_setting']`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| num_rows | `16` | explanatory |
| num_executed_rows | `16` | explanatory |
| num_hard_vetoes | `1` | hard veto |
| num_viable_rows | `0` | explanatory |
| max_factor_marginal_residual | `1.7508864402770996e-07` | hard veto |
| max_induced_row_residual | `9.5367431640625e-07` | hard veto |
| max_induced_column_residual | `1.430511474609375e-06` | hard veto |
| max_output_log_weight_normalization_residual | `0.0` | hard veto |
| max_weighted_mean_abs_error | `1.564621925354004e-07` | hard veto |
| max_weighted_second_moment_abs_error | `0.29357314109802246` | hard veto |
| max_tiny_materialized_apply_parity | `None` | hard veto |
| max_wall_time_seconds_explanatory | `10.443082751939073` | explanatory |
| total_wall_time_seconds_explanatory | `77.71987030119635` | explanatory |
| max_memory_maxrss_kb_explanatory | `569592` | explanatory |

## Rows

| N | Rank | Epsilon | Status | Hard vetoes | Factor residual | Row residual | Column residual | Mean error | Second error | Dense materialized |
| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 4096 | `64` | `0.5` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `1.6763806343078613e-08` | `3.5762786865234375e-07` | `7.152557373046875e-07` | `1.1920928955078125e-07` | `0.29352012276649475` | `False` |
| 4096 | `64` | `0.25` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `2.421438694000244e-08` | `4.76837158203125e-07` | `4.76837158203125e-07` | `1.1175870895385742e-07` | `0.2755662798881531` | `False` |
| 4096 | `64` | `0.125` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `4.0978193283081055e-08` | `7.748603820800781e-07` | `9.5367431640625e-07` | `1.4901161193847656e-07` | `0.1976916640996933` | `False` |
| 4096 | `64` | `0.0625` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `1.7508864402770996e-07` | `9.5367431640625e-07` | `1.1920928955078125e-06` | `6.705522537231445e-08` | `0.11541613936424255` | `False` |
| 4096 | `128` | `0.5` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `9.313225746154785e-09` | `2.980232238769531e-07` | `7.152557373046875e-07` | `9.685754776000977e-08` | `0.2935502529144287` | `False` |
| 4096 | `128` | `0.25` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `1.210719347000122e-08` | `4.76837158203125e-07` | `7.152557373046875e-07` | `1.043081283569336e-07` | `0.2758675813674927` | `False` |
| 4096 | `128` | `0.125` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `2.561137080192566e-08` | `5.364418029785156e-07` | `9.5367431640625e-07` | `9.685754776000977e-08` | `0.19786816835403442` | `False` |
| 4096 | `128` | `0.0625` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `1.043081283569336e-07` | `7.152557373046875e-07` | `1.430511474609375e-06` | `1.1175870895385742e-07` | `0.11569878458976746` | `False` |
| 4096 | `256` | `0.5` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `5.122274160385132e-09` | `3.5762786865234375e-07` | `9.5367431640625e-07` | `7.450580596923828e-08` | `0.2935657501220703` | `False` |
| 4096 | `256` | `0.25` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `6.51925802230835e-09` | `5.960464477539062e-07` | `9.5367431640625e-07` | `1.2665987014770508e-07` | `0.2760322391986847` | `False` |
| 4096 | `256` | `0.125` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `1.7695128917694092e-08` | `7.152557373046875e-07` | `7.152557373046875e-07` | `5.960464477539063e-08` | `0.1979588121175766` | `False` |
| 4096 | `256` | `0.0625` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `4.377216100692749e-08` | `8.940696716308594e-07` | `9.5367431640625e-07` | `8.195638656616211e-08` | `0.11567762494087219` | `False` |
| 4096 | `512` | `0.5` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `2.7939677238464355e-09` | `4.76837158203125e-07` | `1.1920928955078125e-06` | `8.940696716308594e-08` | `0.29357314109802246` | `False` |
| 4096 | `512` | `0.25` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `3.725290298461914e-09` | `5.364418029785156e-07` | `9.5367431640625e-07` | `1.564621925354004e-07` | `0.2761261463165283` | `False` |
| 4096 | `512` | `0.125` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `8.96397978067398e-09` | `7.152557373046875e-07` | `1.1920928955078125e-06` | `1.043081283569336e-07` | `0.19800668954849243` | `False` |
| 4096 | `512` | `0.0625` | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `2.3748725652694702e-08` | `7.152557373046875e-07` | `1.430511474609375e-06` | `6.705522537231445e-08` | `0.11567898094654083` | `False` |

## Run Manifest

- Git commit: `3b11bb1b4848eeeafdd60671f476ba90d54b4caa`
- Command: `docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py --mode tuning-cpu --particle-counts 4096 --batch-size 2 --state-dim 8 --tuning-ranks 64 128 256 512 --tuning-assignment-epsilons 0.5 0.25 0.125 0.0625 --dtype float32 --fixture-id bounded_smooth_v1 --output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-tuning-cpu-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-tuning-cpu-2026-06-20.md`
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
