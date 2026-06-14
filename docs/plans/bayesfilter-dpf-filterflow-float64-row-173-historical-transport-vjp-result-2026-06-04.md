# Result: Row 173 Historical Transport VJP Probe

## Decision

`filterflow_float64_row_173_historical_transport_h3_upstreams_or_masks_diverge`

## Hypothesis Classification

`h3_transport_upstreams_or_masks_diverge_historically`

historical upstream or clip-mask deltas exceed tolerance

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_row_173_historical_transport_h3_upstreams_or_masks_diverge | h3_transport_upstreams_or_masks_diverge_historically | {'all_vetoes_clear': True, 'comparator_drift': False, 'path_boundary_clean': True, 'scalar_value_gate_pass': True, 'all_resampling_flags_match': True, 'all_transport_vjps_finite': True, 'all_upstreams_finite': True, 'cpu_only_parent': True} | single row and target time; no global gradient claim | inspect first historical upstream or clip-mask divergence | correctness, posterior correctness, production readiness, global gradient agreement |

## Historical Transport Comparison

```json
{
  "all_resampling_flags_match": true,
  "all_transport_vjps_finite": true,
  "all_upstreams_finite": true,
  "cumulative_transport_vjp_delta": [
    -3.8733078526274767,
    0.03330367154740088
  ],
  "explained_fraction_by_max_abs_norm": -0.7304359520518555,
  "full_gradient_delta": [
    5.302734403676368,
    -0.1337765252068337
  ],
  "history_length": 94,
  "interpretation": "historical_transport_upstreams_or_masks_diverge",
  "max_abs_clipped_upstream_delta": 0.038257926126621045,
  "max_abs_full_gradient_delta": 5.302734403676368,
  "max_abs_raw_upstream_delta": 3.8853325680154285,
  "max_abs_reconstruction_residual": 9.176042256303845,
  "max_abs_transport_vjp_delta": 4.463208271430858,
  "reconstruction_residual": [
    9.176042256303845,
    -0.16708019675423458
  ],
  "rows": [
    {
      "bayesfilter_clip_count": 0.0,
      "bayesfilter_resampling_flag": [
        false
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 0.0,
      "filterflow_resampling_flag": [
        false
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.0,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.0,
      "raw_upstream_sum_delta": 0.0,
      "resampling_flags_match": true,
      "time_index": 0,
      "transport_vjp_delta": [
        0.0,
        0.0
      ]
    },
    {
      "bayesfilter_clip_count": 1473.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 3.954877492162723e-08,
      "clipped_upstream_sum_delta": -2.0459715665416267e-07,
      "filterflow_clip_count": 1473.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.3157036571342928e-10,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 4.684715726455124e-08,
      "raw_upstream_sum_delta": -9.234666925525548e-07,
      "resampling_flags_match": true,
      "time_index": 1,
      "transport_vjp_delta": [
        5.432503058511173e-11,
        -1.3157036571342928e-10
      ]
    },
    {
      "bayesfilter_clip_count": 1361.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 2.513628860612016e-09,
      "clipped_upstream_sum_delta": 1.0072113354187007e-06,
      "filterflow_clip_count": 1361.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.5400473785120994e-08,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 7.629577858381253e-09,
      "raw_upstream_sum_delta": 6.364929936164554e-07,
      "resampling_flags_match": true,
      "time_index": 2,
      "transport_vjp_delta": [
        -1.5400473785120994e-08,
        6.605452185226568e-09
      ]
    },
    {
      "bayesfilter_clip_count": 2175.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 2.0968495828554978e-08,
      "clipped_upstream_sum_delta": -5.289824048515523e-07,
      "filterflow_clip_count": 2175.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 6.2076352946860425e-09,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.393387488197618e-08,
      "raw_upstream_sum_delta": -4.501890255553809e-06,
      "resampling_flags_match": true,
      "time_index": 3,
      "transport_vjp_delta": [
        1.6469741126456938e-09,
        6.2076352946860425e-09
      ]
    },
    {
      "bayesfilter_clip_count": 2250.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 1.6373074895881246e-08,
      "clipped_upstream_sum_delta": -4.971710418910646e-07,
      "filterflow_clip_count": 2250.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 8.836611442575304e-09,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.1667735577702842e-07,
      "raw_upstream_sum_delta": 4.0786153210348175e-05,
      "resampling_flags_match": true,
      "time_index": 4,
      "transport_vjp_delta": [
        8.836611442575304e-09,
        6.66349819766765e-09
      ]
    },
    {
      "bayesfilter_clip_count": 2315.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 3.720594832223867e-08,
      "clipped_upstream_sum_delta": -1.3654139676688715e-06,
      "filterflow_clip_count": 2315.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.7201509194819664e-07,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.7254220569261633e-07,
      "raw_upstream_sum_delta": -0.00010749817095345726,
      "resampling_flags_match": true,
      "time_index": 5,
      "transport_vjp_delta": [
        1.7201509194819664e-07,
        -2.8644958405266152e-08
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 4.7638221811752146e-08,
      "clipped_upstream_sum_delta": 2.2308594194164755e-06,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.9314904164957625e-07,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.5955937087142047e-06,
      "raw_upstream_sum_delta": 9.939073004794352e-05,
      "resampling_flags_match": true,
      "time_index": 6,
      "transport_vjp_delta": [
        -9.285164992434147e-08,
        1.9314904164957625e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2429.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 1.1498815943866703e-07,
      "clipped_upstream_sum_delta": -4.0863907146970746e-07,
      "filterflow_clip_count": 2429.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.800478853259847e-07,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.1933585675194536e-07,
      "raw_upstream_sum_delta": -1.2046250144726045e-05,
      "resampling_flags_match": true,
      "time_index": 7,
      "transport_vjp_delta": [
        2.800478853259847e-07,
        2.692346257049394e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2289.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 8.46458592107524e-09,
      "clipped_upstream_sum_delta": -6.798009379027636e-08,
      "filterflow_clip_count": 2289.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.0372635844978504e-07,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.963860185583144e-07,
      "raw_upstream_sum_delta": -2.2161444851245826e-05,
      "resampling_flags_match": true,
      "time_index": 8,
      "transport_vjp_delta": [
        2.0372635844978504e-07,
        -1.0739597655629041e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2376.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 2.135172938455554e-08,
      "clipped_upstream_sum_delta": 1.1063010345035984e-06,
      "filterflow_clip_count": 2376.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.8402727235411476e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.135172938455554e-08,
      "raw_upstream_sum_delta": 1.1183078154120007e-05,
      "resampling_flags_match": true,
      "time_index": 9,
      "transport_vjp_delta": [
        1.435181729902979e-06,
        -1.8402727235411476e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2499.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 4.135921471970505e-08,
      "clipped_upstream_sum_delta": -4.135921471970505e-08,
      "filterflow_clip_count": 2499.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 7.316543815250043e-09,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.3797568954032613e-07,
      "raw_upstream_sum_delta": -1.838618457616903e-05,
      "resampling_flags_match": true,
      "time_index": 10,
      "transport_vjp_delta": [
        7.316543815250043e-09,
        4.221369920287543e-09
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 1.1473632266501e-08,
      "clipped_upstream_sum_delta": 5.539816003707898e-07,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.662300235238945e-07,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.1473632266501e-08,
      "raw_upstream_sum_delta": 1.822877266244305e-06,
      "resampling_flags_match": true,
      "time_index": 11,
      "transport_vjp_delta": [
        -1.662300235238945e-07,
        -1.266158236035153e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.2349553319145343e-08,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.4243096480015538e-08,
      "raw_upstream_sum_delta": -1.7289149001342707e-06,
      "resampling_flags_match": true,
      "time_index": 12,
      "transport_vjp_delta": [
        2.2349553319145343e-08,
        7.286985237442423e-09
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.165740736221778e-08,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 6.712433275879448e-09,
      "raw_upstream_sum_delta": 5.462856571547547e-07,
      "resampling_flags_match": true,
      "time_index": 13,
      "transport_vjp_delta": [
        3.165740736221778e-08,
        -8.605280044093888e-09
      ]
    },
    {
      "bayesfilter_clip_count": 2400.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 9.671426992596821e-10,
      "clipped_upstream_sum_delta": -7.202145846374464e-08,
      "filterflow_clip_count": 2400.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.2284471040402423e-07,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.3550391031458275e-08,
      "raw_upstream_sum_delta": -6.276484377787384e-07,
      "resampling_flags_match": true,
      "time_index": 14,
      "transport_vjp_delta": [
        -1.2284471040402423e-07,
        1.966718343737739e-09
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 4.0597358808014405e-10,
      "clipped_upstream_sum_delta": -2.0007714041092584e-08,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 8.743816977130336e-07,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.5483557547213422e-08,
      "raw_upstream_sum_delta": 2.95007088413346e-06,
      "resampling_flags_match": true,
      "time_index": 15,
      "transport_vjp_delta": [
        8.743816977130336e-07,
        -6.675218804375049e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.124647736285624e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.3432185969340935e-08,
      "raw_upstream_sum_delta": -3.6274577341899317e-06,
      "resampling_flags_match": true,
      "time_index": 16,
      "transport_vjp_delta": [
        3.124647736285624e-05,
        -1.4830133991949879e-05
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 8.911807071854128e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.1676405026482826e-07,
      "raw_upstream_sum_delta": 8.029333316006415e-06,
      "resampling_flags_match": true,
      "time_index": 17,
      "transport_vjp_delta": [
        8.911807071854128e-06,
        -1.5366656214155228e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2443.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 8.750099422805135e-09,
      "clipped_upstream_sum_delta": 3.8472779551046443e-07,
      "filterflow_clip_count": 2443.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 6.777988454587103e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 7.463280127240068e-08,
      "raw_upstream_sum_delta": -6.742441520546372e-06,
      "resampling_flags_match": true,
      "time_index": 18,
      "transport_vjp_delta": [
        -6.777988454587103e-05,
        1.0459225084247237e-05
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.0467068679863587e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 4.66682763544668e-08,
      "raw_upstream_sum_delta": 8.076693367442545e-06,
      "resampling_flags_match": true,
      "time_index": 19,
      "transport_vjp_delta": [
        2.0467068679863587e-06,
        -2.3789974079591047e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2400.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 2.4254807051704574e-09,
      "clipped_upstream_sum_delta": 1.1163575119876867e-08,
      "filterflow_clip_count": 2400.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.8578950403025374e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 4.072956016898388e-08,
      "raw_upstream_sum_delta": -2.796547216965539e-06,
      "resampling_flags_match": true,
      "time_index": 20,
      "transport_vjp_delta": [
        -1.8578950403025374e-05,
        2.6396524432925617e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.0521639524085913e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.56877263179922e-07,
      "raw_upstream_sum_delta": 1.2721577492325054e-05,
      "resampling_flags_match": true,
      "time_index": 21,
      "transport_vjp_delta": [
        -1.0521639524085913e-06,
        9.164578607112617e-08
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 7.151757586143503e-08,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 4.6638191975034715e-08,
      "raw_upstream_sum_delta": -8.670477159133938e-06,
      "resampling_flags_match": true,
      "time_index": 22,
      "transport_vjp_delta": [
        -7.151757586143503e-08,
        8.318522759509506e-09
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 9.712482551549328e-08,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 9.379567700307234e-08,
      "raw_upstream_sum_delta": 1.7894405319740514e-05,
      "resampling_flags_match": true,
      "time_index": 23,
      "transport_vjp_delta": [
        9.712482551549328e-08,
        3.633867962093973e-08
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 6.2000656275706945e-09,
      "clipped_upstream_sum_delta": 3.09090341876761e-07,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.9739534233594895e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 8.877795920625431e-08,
      "raw_upstream_sum_delta": 7.564579407870475e-06,
      "resampling_flags_match": true,
      "time_index": 24,
      "transport_vjp_delta": [
        4.9739534233594895e-06,
        -1.5745824555324361e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.205607183394022e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 6.80561072385899e-07,
      "raw_upstream_sum_delta": -8.447480186379863e-05,
      "resampling_flags_match": true,
      "time_index": 25,
      "transport_vjp_delta": [
        -4.205607183394022e-06,
        4.001981039891689e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2337.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 2.9623251962540564e-08,
      "clipped_upstream_sum_delta": 1.1618003539215493e-06,
      "filterflow_clip_count": 2337.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.3744446732744109e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 4.187037916381087e-08,
      "raw_upstream_sum_delta": -5.141904181327206e-06,
      "resampling_flags_match": true,
      "time_index": 26,
      "transport_vjp_delta": [
        1.3744446732744109e-05,
        2.63748532347563e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 8.702832019480411e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 7.596059958814294e-08,
      "raw_upstream_sum_delta": 1.999990320866729e-05,
      "resampling_flags_match": true,
      "time_index": 27,
      "transport_vjp_delta": [
        8.702832019480411e-06,
        -1.0948946567168605e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.618327511707321e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.0635153557814192e-07,
      "raw_upstream_sum_delta": -3.349614790781885e-05,
      "resampling_flags_match": true,
      "time_index": 28,
      "transport_vjp_delta": [
        4.618327511707321e-05,
        5.899697015365746e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.472553316896665e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 9.935388334270101e-08,
      "raw_upstream_sum_delta": 1.0355531117056671e-05,
      "resampling_flags_match": true,
      "time_index": 29,
      "transport_vjp_delta": [
        3.472553316896665e-06,
        -5.122936030943492e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.3360232666600496e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 7.766161047584319e-08,
      "raw_upstream_sum_delta": -2.5395520838245034e-05,
      "resampling_flags_match": true,
      "time_index": 30,
      "transport_vjp_delta": [
        -4.3360232666600496e-06,
        5.558887608003715e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.00023180879770734464,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.6340035219618585e-07,
      "raw_upstream_sum_delta": 9.042638645206935e-06,
      "resampling_flags_match": true,
      "time_index": 31,
      "transport_vjp_delta": [
        0.00023180879770734464,
        -2.76310674536262e-05
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.0769066395587288e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.1628903823511791e-07,
      "raw_upstream_sum_delta": -3.8951743360549074e-05,
      "resampling_flags_match": true,
      "time_index": 32,
      "transport_vjp_delta": [
        -2.0769066395587288e-06,
        1.7979985500460316e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.00023073184956956538,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.2705994834050216e-07,
      "raw_upstream_sum_delta": 3.923419485940549e-05,
      "resampling_flags_match": true,
      "time_index": 33,
      "transport_vjp_delta": [
        0.00023073184956956538,
        -2.7004151647247454e-05
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.2912154236109927e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.3732347642635432e-07,
      "raw_upstream_sum_delta": -2.72451282770092e-05,
      "resampling_flags_match": true,
      "time_index": 34,
      "transport_vjp_delta": [
        2.2912154236109927e-06,
        -4.321274786889262e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.2910891150095267e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.7152778986637713e-07,
      "raw_upstream_sum_delta": -6.904155200793127e-05,
      "resampling_flags_match": true,
      "time_index": 35,
      "transport_vjp_delta": [
        3.2910891150095267e-06,
        -5.014254753632486e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.8299100449658e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.3582490510088974e-06,
      "raw_upstream_sum_delta": 0.0003023714006777922,
      "resampling_flags_match": true,
      "time_index": 36,
      "transport_vjp_delta": [
        2.8299100449658e-06,
        -4.441167789082101e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 2.7769978538927376e-08,
      "clipped_upstream_sum_delta": -1.3830709811868402e-06,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 5.5738358923917986e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 6.669308163509413e-07,
      "raw_upstream_sum_delta": -0.0003904202058352402,
      "resampling_flags_match": true,
      "time_index": 37,
      "transport_vjp_delta": [
        5.5738358923917986e-06,
        -5.681649355437912e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.04100831777032e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 5.9866511037398595e-06,
      "raw_upstream_sum_delta": 0.001201337642113609,
      "resampling_flags_match": true,
      "time_index": 38,
      "transport_vjp_delta": [
        1.04100831777032e-06,
        -3.752158157510621e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 6.1520549934357405e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.339303160032614e-05,
      "raw_upstream_sum_delta": -0.003469316217659113,
      "resampling_flags_match": true,
      "time_index": 39,
      "transport_vjp_delta": [
        6.1520549934357405e-06,
        -6.687819222861435e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 1.9223199771989385e-06,
      "clipped_upstream_sum_delta": 9.595652070881755e-05,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.2266551038919715e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.58171466245949e-05,
      "raw_upstream_sum_delta": 0.011118973839945756,
      "resampling_flags_match": true,
      "time_index": 40,
      "transport_vjp_delta": [
        1.2266551038919715e-05,
        -5.514919827476206e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.9194258129573427e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 5.5153032803900714e-05,
      "raw_upstream_sum_delta": -0.031099410112260584,
      "resampling_flags_match": true,
      "time_index": 41,
      "transport_vjp_delta": [
        -1.9194258129573427e-06,
        -3.668750885310601e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.6966658790806832e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.00016919221803846085,
      "raw_upstream_sum_delta": 0.0864602097445526,
      "resampling_flags_match": true,
      "time_index": 42,
      "transport_vjp_delta": [
        1.6966658790806832e-05,
        -3.7765701677017205e-08
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.2806911172447144e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.0010672900132249197,
      "raw_upstream_sum_delta": -0.2512387528610418,
      "resampling_flags_match": true,
      "time_index": 43,
      "transport_vjp_delta": [
        -1.2806911172447144e-05,
        8.462069445158704e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 7.562634617697128e-05,
      "clipped_upstream_sum_delta": -0.0037735049637515616,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.11814065691032738,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.0004043180958888115,
      "raw_upstream_sum_delta": -0.31208523840387775,
      "resampling_flags_match": true,
      "time_index": 44,
      "transport_vjp_delta": [
        -0.11814065691032738,
        0.00513701345207096
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.4104120964475442e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.0011110268147973557,
      "raw_upstream_sum_delta": 0.8633703120073211,
      "resampling_flags_match": true,
      "time_index": 45,
      "transport_vjp_delta": [
        -1.4104120964475442e-06,
        4.4334782955957053e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.8627792087499984e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.006187247177876998,
      "raw_upstream_sum_delta": -2.389257807613008,
      "resampling_flags_match": true,
      "time_index": 46,
      "transport_vjp_delta": [
        -1.8627792087499984e-05,
        1.0311081837244274e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 6.861593647045083e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.006941124237442864,
      "raw_upstream_sum_delta": 6.550974005607053,
      "resampling_flags_match": true,
      "time_index": 47,
      "transport_vjp_delta": [
        6.861593647045083e-06,
        -1.258847532881191e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.9391048883553594e-07,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.020387363826650073,
      "raw_upstream_sum_delta": -17.896774173229772,
      "resampling_flags_match": true,
      "time_index": 48,
      "transport_vjp_delta": [
        2.9099464882165194e-07,
        -2.9391048883553594e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.725463648152072e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.1156377474275132,
      "raw_upstream_sum_delta": 48.67631454253094,
      "resampling_flags_match": true,
      "time_index": 49,
      "transport_vjp_delta": [
        -3.725463648152072e-05,
        1.3557735201175092e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 9.488733212492662e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.9577901580405523,
      "raw_upstream_sum_delta": -127.26307690319584,
      "resampling_flags_match": true,
      "time_index": 50,
      "transport_vjp_delta": [
        9.488733212492662e-06,
        -6.156203369300783e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 5.848775572303566e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.8853325680154285,
      "raw_upstream_sum_delta": 276.9609688870665,
      "resampling_flags_match": true,
      "time_index": 51,
      "transport_vjp_delta": [
        5.848775572303566e-06,
        -4.763841303656591e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.038257926126621045,
      "clipped_upstream_sum_delta": -1.9092531867589029,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.463208271430858,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.06167895758798991,
      "raw_upstream_sum_delta": -32.150265266150306,
      "resampling_flags_match": true,
      "time_index": 52,
      "transport_vjp_delta": [
        -4.463208271430858,
        0.053972612751095994
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 7.67166966397781e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.4052660943005151,
      "raw_upstream_sum_delta": 118.18998536927191,
      "resampling_flags_match": true,
      "time_index": 53,
      "transport_vjp_delta": [
        7.67166966397781e-06,
        -1.0846338227565866e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.020636594767113714,
      "clipped_upstream_sum_delta": -1.0298565098502492,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.8647824981858321,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.029784651025892117,
      "raw_upstream_sum_delta": -10.621317429470436,
      "resampling_flags_match": true,
      "time_index": 54,
      "transport_vjp_delta": [
        0.8647824981858321,
        -0.028376664074812652
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0013693174724487278,
      "clipped_upstream_sum_delta": -0.06824236009233808,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.17764483727114566,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.011599830915031362,
      "raw_upstream_sum_delta": -0.8448525008236254,
      "resampling_flags_match": true,
      "time_index": 55,
      "transport_vjp_delta": [
        -0.17764483727114566,
        0.004255516741068277
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.00019018711646417996,
      "clipped_upstream_sum_delta": 0.009486233108798606,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.006358362881655921,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.0007412603212770819,
      "raw_upstream_sum_delta": 0.025349789971968364,
      "resampling_flags_match": true,
      "time_index": 56,
      "transport_vjp_delta": [
        -0.006358362881655921,
        -0.00040296663766525853
      ]
    },
    {
      "bayesfilter_clip_count": 2400.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 1.0120558726622875e-05,
      "clipped_upstream_sum_delta": -0.00023062004998164465,
      "filterflow_clip_count": 2400.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.026126328603822913,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.086730913575252e-05,
      "raw_upstream_sum_delta": -0.011145874457629268,
      "resampling_flags_match": true,
      "time_index": 57,
      "transport_vjp_delta": [
        0.026126328603822913,
        -0.0012003851655606468
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 8.812291980575537e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 9.148309459305892e-05,
      "raw_upstream_sum_delta": 0.003130664951099593,
      "resampling_flags_match": true,
      "time_index": 58,
      "transport_vjp_delta": [
        8.812291980575537e-06,
        -4.949923777530785e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 3.025331850148305e-06,
      "clipped_upstream_sum_delta": 0.00015096347413767752,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.0012818548574387023,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 5.0734338969959936e-06,
      "raw_upstream_sum_delta": 0.0016876630595996645,
      "resampling_flags_match": true,
      "time_index": 59,
      "transport_vjp_delta": [
        -0.0012818548574387023,
        4.2169275872083745e-05
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 1.3507117507804978e-07,
      "clipped_upstream_sum_delta": -6.741635921236888e-06,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.0017966039376915433,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.28797881365972e-07,
      "raw_upstream_sum_delta": -0.0002841033669189197,
      "resampling_flags_match": true,
      "time_index": 60,
      "transport_vjp_delta": [
        0.0017966039376915433,
        -5.474679039707553e-05
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.00029818488201271975,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.712190112357348e-06,
      "raw_upstream_sum_delta": 0.0006381221563005468,
      "resampling_flags_match": true,
      "time_index": 61,
      "transport_vjp_delta": [
        0.00029818488201271975,
        -8.340787644556258e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.2900339445186546e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.6688093700831814e-06,
      "raw_upstream_sum_delta": -0.000547959096502737,
      "resampling_flags_match": true,
      "time_index": 62,
      "transport_vjp_delta": [
        -2.2900339445186546e-05,
        9.84700051276377e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.6734057428257074e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.896557392910836e-06,
      "raw_upstream_sum_delta": -1.601357361380451e-05,
      "resampling_flags_match": true,
      "time_index": 63,
      "transport_vjp_delta": [
        -2.6734057428257074e-05,
        5.829216718211683e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 8.605833500041626e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 6.757969988058221e-07,
      "raw_upstream_sum_delta": 5.909710115625799e-05,
      "resampling_flags_match": true,
      "time_index": 64,
      "transport_vjp_delta": [
        8.605833500041626e-06,
        -1.263991123323649e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.516690074116923e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.1470990557427285e-06,
      "raw_upstream_sum_delta": -0.00017058008276649161,
      "resampling_flags_match": true,
      "time_index": 65,
      "transport_vjp_delta": [
        2.516690074116923e-06,
        -1.4046361229702597e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.7823684831673745e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 5.509819857252296e-06,
      "raw_upstream_sum_delta": -3.724267104399104e-05,
      "resampling_flags_match": true,
      "time_index": 66,
      "transport_vjp_delta": [
        -2.7823684831673745e-05,
        5.006917831451574e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.9568656827905215e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 5.229330781730823e-07,
      "raw_upstream_sum_delta": -0.00012036641213075683,
      "resampling_flags_match": true,
      "time_index": 67,
      "transport_vjp_delta": [
        -2.9568656827905215e-05,
        5.870577979294467e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.864093221432995e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.744187912462337e-06,
      "raw_upstream_sum_delta": 7.714116953749794e-05,
      "resampling_flags_match": true,
      "time_index": 68,
      "transport_vjp_delta": [
        -2.864093221432995e-05,
        5.376118679123465e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.7098482405563118e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.4187474448590365e-06,
      "raw_upstream_sum_delta": 0.0001547614762262839,
      "resampling_flags_match": true,
      "time_index": 69,
      "transport_vjp_delta": [
        -2.7098482405563118e-05,
        2.780675458780024e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.696878146934978e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 5.821926833959878e-07,
      "raw_upstream_sum_delta": -6.778728697698355e-05,
      "resampling_flags_match": true,
      "time_index": 70,
      "transport_vjp_delta": [
        -2.696878146934978e-05,
        4.6214324811444385e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.169327828800306e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.8298724171472713e-06,
      "raw_upstream_sum_delta": -0.00013913984998836781,
      "resampling_flags_match": true,
      "time_index": 71,
      "transport_vjp_delta": [
        3.169327828800306e-05,
        -7.369079639829579e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 7.998555634003424e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 9.830864087234659e-07,
      "raw_upstream_sum_delta": -9.947140175547986e-05,
      "resampling_flags_match": true,
      "time_index": 72,
      "transport_vjp_delta": [
        -7.998555634003424e-05,
        5.498740563325555e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.95480510633206e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 7.328244180371257e-07,
      "raw_upstream_sum_delta": 0.000184861265164038,
      "resampling_flags_match": true,
      "time_index": 73,
      "transport_vjp_delta": [
        -3.95480510633206e-05,
        1.135040577082691e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.802427181653911e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.3379654976452002e-06,
      "raw_upstream_sum_delta": -9.002958449855214e-06,
      "resampling_flags_match": true,
      "time_index": 74,
      "transport_vjp_delta": [
        -3.802427181653911e-05,
        1.1304374538667616e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.654476702446118e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.7359548343829374e-07,
      "raw_upstream_sum_delta": -7.021427336439956e-06,
      "resampling_flags_match": true,
      "time_index": 75,
      "transport_vjp_delta": [
        -2.654476702446118e-06,
        3.9742303670209367e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 7.057646803332318e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.445067027816549e-06,
      "raw_upstream_sum_delta": 6.718113170656181e-05,
      "resampling_flags_match": true,
      "time_index": 76,
      "transport_vjp_delta": [
        -7.057646803332318e-05,
        1.809138211683603e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.5200288607484254e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.388872078678105e-06,
      "raw_upstream_sum_delta": -0.00012653611004198595,
      "resampling_flags_match": true,
      "time_index": 77,
      "transport_vjp_delta": [
        -3.5200288607484254e-05,
        9.233409059561382e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.2516504284576513e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 6.719485895700927e-06,
      "raw_upstream_sum_delta": 0.0005710047119791284,
      "resampling_flags_match": true,
      "time_index": 78,
      "transport_vjp_delta": [
        -1.2516504284576513e-05,
        1.1017585848094313e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.6824691051151603e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.9013393742616245e-05,
      "raw_upstream_sum_delta": -0.0035452735575276506,
      "resampling_flags_match": true,
      "time_index": 79,
      "transport_vjp_delta": [
        -3.6824691051151603e-05,
        7.004555300227366e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 2.386835749046412e-07,
      "clipped_upstream_sum_delta": -1.1909842742352517e-05,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 6.39513018541038e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.1786335107899504e-06,
      "raw_upstream_sum_delta": -0.0002184040623783856,
      "resampling_flags_match": true,
      "time_index": 80,
      "transport_vjp_delta": [
        -6.39513018541038e-05,
        2.212496156062116e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.8155407966987696e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 7.846431344660232e-07,
      "raw_upstream_sum_delta": 0.00012625788813735994,
      "resampling_flags_match": true,
      "time_index": 81,
      "transport_vjp_delta": [
        -4.8155407966987696e-05,
        1.5352161426562816e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.177835762675386e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.415354629192734e-06,
      "raw_upstream_sum_delta": -0.00019044583176253127,
      "resampling_flags_match": true,
      "time_index": 82,
      "transport_vjp_delta": [
        -4.177835762675386e-05,
        7.214928245957708e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.129065953544341e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.513575398348621e-06,
      "raw_upstream_sum_delta": 0.00029736760418686004,
      "resampling_flags_match": true,
      "time_index": 83,
      "transport_vjp_delta": [
        -3.129065953544341e-05,
        6.131600116532354e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.593324956658762e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 9.182782292782576e-06,
      "raw_upstream_sum_delta": -0.0010377640911638508,
      "resampling_flags_match": true,
      "time_index": 84,
      "transport_vjp_delta": [
        -4.593324956658762e-05,
        1.1814595382020343e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.4277001506998204e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 4.126536794046842e-06,
      "raw_upstream_sum_delta": 0.0015679270457908956,
      "resampling_flags_match": true,
      "time_index": 85,
      "transport_vjp_delta": [
        -4.4277001506998204e-05,
        1.2182129012217047e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.00017444394688936882,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 4.461609364625474e-06,
      "raw_upstream_sum_delta": -0.0009655380510231737,
      "resampling_flags_match": true,
      "time_index": 86,
      "transport_vjp_delta": [
        -0.00017444394688936882,
        6.17197730434782e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.5927663045877125e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 5.459406111185672e-06,
      "raw_upstream_sum_delta": 0.0005825479175278758,
      "resampling_flags_match": true,
      "time_index": 87,
      "transport_vjp_delta": [
        2.5927663045877125e-05,
        -3.190999109392578e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.0407800295506604e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.41563663191846e-06,
      "raw_upstream_sum_delta": -0.0001867963155657293,
      "resampling_flags_match": true,
      "time_index": 88,
      "transport_vjp_delta": [
        -3.0407800295506604e-05,
        8.78772652868065e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.281906174379401e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.6198341604176676e-06,
      "raw_upstream_sum_delta": 0.00010864672012544929,
      "resampling_flags_match": true,
      "time_index": 89,
      "transport_vjp_delta": [
        -3.281906174379401e-06,
        5.540266556636197e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.0105860787443817e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.0267047855450073e-05,
      "raw_upstream_sum_delta": -0.0006674113554190342,
      "resampling_flags_match": true,
      "time_index": 90,
      "transport_vjp_delta": [
        -3.0105860787443817e-05,
        4.5509183621561533e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 6.008615127939265e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.7318884601991158e-06,
      "raw_upstream_sum_delta": 0.00016206299099863486,
      "resampling_flags_match": true,
      "time_index": 91,
      "transport_vjp_delta": [
        -6.008615127939265e-05,
        -4.1831856378848897e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.950677430315409e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.2457875843429065e-06,
      "raw_upstream_sum_delta": 0.0001273953970226671,
      "resampling_flags_match": true,
      "time_index": 92,
      "transport_vjp_delta": [
        -4.950677430315409e-05,
        1.7982122244575294e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2200.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 1.74666986707539e-08,
      "clipped_upstream_sum_delta": -1.9912844623354298e-06,
      "filterflow_clip_count": 2200.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.0008782294207776431,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.360472966562611e-08,
      "raw_upstream_sum_delta": -8.271588089039938e-06,
      "resampling_flags_match": true,
      "time_index": 93,
      "transport_vjp_delta": [
        0.0008782294207776431,
        -3.587239052649238e-05
      ]
    }
  ],
  "scalar_delta": 6.2123888255882775e-09,
  "status": "compared",
  "top_transport_vjp_delta_rows": [
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.038257926126621045,
      "clipped_upstream_sum_delta": -1.9092531867589029,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.463208271430858,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.06167895758798991,
      "raw_upstream_sum_delta": -32.150265266150306,
      "resampling_flags_match": true,
      "time_index": 52,
      "transport_vjp_delta": [
        -4.463208271430858,
        0.053972612751095994
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.020636594767113714,
      "clipped_upstream_sum_delta": -1.0298565098502492,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.8647824981858321,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.029784651025892117,
      "raw_upstream_sum_delta": -10.621317429470436,
      "resampling_flags_match": true,
      "time_index": 54,
      "transport_vjp_delta": [
        0.8647824981858321,
        -0.028376664074812652
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0013693174724487278,
      "clipped_upstream_sum_delta": -0.06824236009233808,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.17764483727114566,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.011599830915031362,
      "raw_upstream_sum_delta": -0.8448525008236254,
      "resampling_flags_match": true,
      "time_index": 55,
      "transport_vjp_delta": [
        -0.17764483727114566,
        0.004255516741068277
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 7.562634617697128e-05,
      "clipped_upstream_sum_delta": -0.0037735049637515616,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.11814065691032738,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.0004043180958888115,
      "raw_upstream_sum_delta": -0.31208523840387775,
      "resampling_flags_match": true,
      "time_index": 44,
      "transport_vjp_delta": [
        -0.11814065691032738,
        0.00513701345207096
      ]
    },
    {
      "bayesfilter_clip_count": 2400.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 1.0120558726622875e-05,
      "clipped_upstream_sum_delta": -0.00023062004998164465,
      "filterflow_clip_count": 2400.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.026126328603822913,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 2.086730913575252e-05,
      "raw_upstream_sum_delta": -0.011145874457629268,
      "resampling_flags_match": true,
      "time_index": 57,
      "transport_vjp_delta": [
        0.026126328603822913,
        -0.0012003851655606468
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.00019018711646417996,
      "clipped_upstream_sum_delta": 0.009486233108798606,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.006358362881655921,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.0007412603212770819,
      "raw_upstream_sum_delta": 0.025349789971968364,
      "resampling_flags_match": true,
      "time_index": 56,
      "transport_vjp_delta": [
        -0.006358362881655921,
        -0.00040296663766525853
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 1.3507117507804978e-07,
      "clipped_upstream_sum_delta": -6.741635921236888e-06,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.0017966039376915433,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.28797881365972e-07,
      "raw_upstream_sum_delta": -0.0002841033669189197,
      "resampling_flags_match": true,
      "time_index": 60,
      "transport_vjp_delta": [
        0.0017966039376915433,
        -5.474679039707553e-05
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 3.025331850148305e-06,
      "clipped_upstream_sum_delta": 0.00015096347413767752,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.0012818548574387023,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 5.0734338969959936e-06,
      "raw_upstream_sum_delta": 0.0016876630595996645,
      "resampling_flags_match": true,
      "time_index": 59,
      "transport_vjp_delta": [
        -0.0012818548574387023,
        4.2169275872083745e-05
      ]
    },
    {
      "bayesfilter_clip_count": 2200.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 1.74666986707539e-08,
      "clipped_upstream_sum_delta": -1.9912844623354298e-06,
      "filterflow_clip_count": 2200.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.0008782294207776431,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.360472966562611e-08,
      "raw_upstream_sum_delta": -8.271588089039938e-06,
      "resampling_flags_match": true,
      "time_index": 93,
      "transport_vjp_delta": [
        0.0008782294207776431,
        -3.587239052649238e-05
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.00029818488201271975,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.712190112357348e-06,
      "raw_upstream_sum_delta": 0.0006381221563005468,
      "resampling_flags_match": true,
      "time_index": 61,
      "transport_vjp_delta": [
        0.00029818488201271975,
        -8.340787644556258e-06
      ]
    }
  ],
  "total_clip_mask_mismatch_count": 0,
  "upstream_or_mask_delta_rows": [
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.8299100449658e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 1.3582490510088974e-06,
      "raw_upstream_sum_delta": 0.0003023714006777922,
      "resampling_flags_match": true,
      "time_index": 36,
      "transport_vjp_delta": [
        2.8299100449658e-06,
        -4.441167789082101e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 2.7769978538927376e-08,
      "clipped_upstream_sum_delta": -1.3830709811868402e-06,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 5.5738358923917986e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 6.669308163509413e-07,
      "raw_upstream_sum_delta": -0.0003904202058352402,
      "resampling_flags_match": true,
      "time_index": 37,
      "transport_vjp_delta": [
        5.5738358923917986e-06,
        -5.681649355437912e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.04100831777032e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 5.9866511037398595e-06,
      "raw_upstream_sum_delta": 0.001201337642113609,
      "resampling_flags_match": true,
      "time_index": 38,
      "transport_vjp_delta": [
        1.04100831777032e-06,
        -3.752158157510621e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 6.1520549934357405e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.339303160032614e-05,
      "raw_upstream_sum_delta": -0.003469316217659113,
      "resampling_flags_match": true,
      "time_index": 39,
      "transport_vjp_delta": [
        6.1520549934357405e-06,
        -6.687819222861435e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 1.9223199771989385e-06,
      "clipped_upstream_sum_delta": 9.595652070881755e-05,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.2266551038919715e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.58171466245949e-05,
      "raw_upstream_sum_delta": 0.011118973839945756,
      "resampling_flags_match": true,
      "time_index": 40,
      "transport_vjp_delta": [
        1.2266551038919715e-05,
        -5.514919827476206e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.9194258129573427e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 5.5153032803900714e-05,
      "raw_upstream_sum_delta": -0.031099410112260584,
      "resampling_flags_match": true,
      "time_index": 41,
      "transport_vjp_delta": [
        -1.9194258129573427e-06,
        -3.668750885310601e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.6966658790806832e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.00016919221803846085,
      "raw_upstream_sum_delta": 0.0864602097445526,
      "resampling_flags_match": true,
      "time_index": 42,
      "transport_vjp_delta": [
        1.6966658790806832e-05,
        -3.7765701677017205e-08
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.2806911172447144e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.0010672900132249197,
      "raw_upstream_sum_delta": -0.2512387528610418,
      "resampling_flags_match": true,
      "time_index": 43,
      "transport_vjp_delta": [
        -1.2806911172447144e-05,
        8.462069445158704e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 7.562634617697128e-05,
      "clipped_upstream_sum_delta": -0.0037735049637515616,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.11814065691032738,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.0004043180958888115,
      "raw_upstream_sum_delta": -0.31208523840387775,
      "resampling_flags_match": true,
      "time_index": 44,
      "transport_vjp_delta": [
        -0.11814065691032738,
        0.00513701345207096
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.4104120964475442e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.0011110268147973557,
      "raw_upstream_sum_delta": 0.8633703120073211,
      "resampling_flags_match": true,
      "time_index": 45,
      "transport_vjp_delta": [
        -1.4104120964475442e-06,
        4.4334782955957053e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 1.8627792087499984e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.006187247177876998,
      "raw_upstream_sum_delta": -2.389257807613008,
      "resampling_flags_match": true,
      "time_index": 46,
      "transport_vjp_delta": [
        -1.8627792087499984e-05,
        1.0311081837244274e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 6.861593647045083e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.006941124237442864,
      "raw_upstream_sum_delta": 6.550974005607053,
      "resampling_flags_match": true,
      "time_index": 47,
      "transport_vjp_delta": [
        6.861593647045083e-06,
        -1.258847532881191e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 2.9391048883553594e-07,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.020387363826650073,
      "raw_upstream_sum_delta": -17.896774173229772,
      "resampling_flags_match": true,
      "time_index": 48,
      "transport_vjp_delta": [
        2.9099464882165194e-07,
        -2.9391048883553594e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 3.725463648152072e-05,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.1156377474275132,
      "raw_upstream_sum_delta": 48.67631454253094,
      "resampling_flags_match": true,
      "time_index": 49,
      "transport_vjp_delta": [
        -3.725463648152072e-05,
        1.3557735201175092e-06
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 9.488733212492662e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.9577901580405523,
      "raw_upstream_sum_delta": -127.26307690319584,
      "resampling_flags_match": true,
      "time_index": 50,
      "transport_vjp_delta": [
        9.488733212492662e-06,
        -6.156203369300783e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 5.848775572303566e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 3.8853325680154285,
      "raw_upstream_sum_delta": 276.9609688870665,
      "resampling_flags_match": true,
      "time_index": 51,
      "transport_vjp_delta": [
        5.848775572303566e-06,
        -4.763841303656591e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.038257926126621045,
      "clipped_upstream_sum_delta": -1.9092531867589029,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 4.463208271430858,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.06167895758798991,
      "raw_upstream_sum_delta": -32.150265266150306,
      "resampling_flags_match": true,
      "time_index": 52,
      "transport_vjp_delta": [
        -4.463208271430858,
        0.053972612751095994
      ]
    },
    {
      "bayesfilter_clip_count": 2500.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0,
      "clipped_upstream_sum_delta": 0.0,
      "filterflow_clip_count": 2500.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 7.67166966397781e-06,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.4052660943005151,
      "raw_upstream_sum_delta": 118.18998536927191,
      "resampling_flags_match": true,
      "time_index": 53,
      "transport_vjp_delta": [
        7.67166966397781e-06,
        -1.0846338227565866e-07
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.020636594767113714,
      "clipped_upstream_sum_delta": -1.0298565098502492,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.8647824981858321,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.029784651025892117,
      "raw_upstream_sum_delta": -10.621317429470436,
      "resampling_flags_match": true,
      "time_index": 54,
      "transport_vjp_delta": [
        0.8647824981858321,
        -0.028376664074812652
      ]
    },
    {
      "bayesfilter_clip_count": 2450.0,
      "bayesfilter_resampling_flag": [
        true
      ],
      "clip_count_delta": 0.0,
      "clip_mask_mismatch_count": 0,
      "clipped_upstream_finite": true,
      "clipped_upstream_max_abs_delta": 0.0013693174724487278,
      "clipped_upstream_sum_delta": -0.06824236009233808,
      "filterflow_clip_count": 2450.0,
      "filterflow_resampling_flag": [
        true
      ],
      "finite": true,
      "max_abs_transport_vjp_delta": 0.17764483727114566,
      "raw_upstream_finite": true,
      "raw_upstream_max_abs_delta": 0.011599830915031362,
      "raw_upstream_sum_delta": -0.8448525008236254,
      "resampling_flags_match": true,
      "time_index": 55,
      "transport_vjp_delta": [
        -0.17764483727114566,
        0.004255516741068277
      ]
    }
  ]
}
```

## Veto Status

```json
{
  "all_resampling_flags_match": true,
  "all_transport_vjps_finite": true,
  "all_upstreams_finite": true,
  "all_vetoes_clear": true,
  "comparator_drift": false,
  "cpu_only_parent": true,
  "path_boundary_clean": true,
  "scalar_value_gate_pass": true
}
```

## FilterFlow History

```json
{
  "backend": "executable_filterflow_subprocess",
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "cumulative_transport_vjp_diag": [
    182094.5135869977,
    -12406.717812937466
  ],
  "history_length": 94,
  "resampling_flags": [
    [
      false
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ]
  ],
  "settings": {
    "T": 100,
    "dtype": "float64",
    "mesh_index": 173,
    "n_particles": 50,
    "target_time_index": 93,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ],
    "transport_backward": "FilterFlow custom gradient clips d_transport to [-1,1]"
  },
  "status": "executed",
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-04 23:11:18.030781: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780585878.041756     119 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780585878.044662     119 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780585878.054625     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780585878.054678     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780585878.054682     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780585878.054684     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-04 23:11:18.057813: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-04 23:11:20.554737: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n",
  "target_scalar": -141.71711568701727,
  "total_gradient_diag": [
    9105.143875898348,
    57.123649814928335
  ]
}
```

## BayesFilter History

```json
{
  "backend": "tensorflow_tensorflow_probability",
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "cumulative_transport_vjp_diag": [
    182090.64027914507,
    -12406.684509265919
  ],
  "history_length": 94,
  "resampling_flags": [
    [
      false
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ],
    [
      true
    ]
  ],
  "settings": {
    "T": 100,
    "dtype": "float64",
    "mesh_index": 173,
    "n_particles": 50,
    "target_time_index": 93,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ],
    "transport_backward": "FilterFlow custom gradient clips d_transport to [-1,1]"
  },
  "status": "executed",
  "stderr_excerpt": "",
  "target_scalar": -141.71711568080488,
  "total_gradient_diag": [
    9110.446610302024,
    56.9898732897215
  ]
}
```

## Non-Implications

- No correctness claim is made for either implementation.
- No analytic gradient correctness is concluded.
- No posterior correctness is concluded.
- No global gradient agreement is concluded.
- No full mesh or surface agreement is concluded.
- No production readiness or public API readiness is concluded.
