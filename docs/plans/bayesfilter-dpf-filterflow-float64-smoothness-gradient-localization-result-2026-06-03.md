# FilterFlow Float64 Smoothness Gradient Localization

## Decision

`filterflow_float64_smoothness_gradient_localized`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_localized | localized raw failure: {'status': 'failure', 'time_index': 1, 'scalar_delta': 1.7926993223227328e-11, 'max_abs_gradient_delta': 0.05220128095433019, 'relative_gradient_delta': 0.005931950625260563, 'gradient_explosion_ratio': 1.0059319506252606, 'resampling_flag': [True], 'transport_status': 'computed_raw_transport_gradient'} | scalar path remained aligned before gradient mismatch | single theta row only; no analytic-gradient correctness is concluded | patch BayesFilter annealed transport backward semantics to mirror FilterFlow custom gradient | correctness of either implementation, analytic gradient correctness, production readiness |

## Model Contract

| Key | Value |
| --- | --- |
| `model` | `filterflow_simple_linear_smoothness_constant_velocity_lgssm` |
| `theta` | `[0.95, 0.95]` |
| `transition_matrix` | `A(theta)=diag(theta_1, theta_2)+[[0,1],[0,0]]` |
| `transition_covariance` | `[[0.3333333333333333, 0.5], [0.5, 1.0]]` |
| `observation_matrix` | `[[1.0, 0.0]]` |
| `observation_covariance` | `[[0.01]]` |
| `T` | `100` |
| `batch_size` | `1` |
| `num_particles` | `50` |
| `data_seed` | `123` |
| `filter_seed` | `1234` |
| `epsilon` | `0.25` |
| `scaling` | `0.85` |
| `convergence_threshold` | `1e-06` |
| `max_iter` | `500` |
| `resampling_neff` | `0.9999` |
| `optimal_proposal` | `True` |
| `resampling_correction` | `False` |
| `dtype` | `float64` |

## Gradient Localization Contract

| Key | Value |
| --- | --- |
| `filterflow_cumulative_gradient` | `tape.gradient(cumulative_log_likelihood_at_t, transition_matrix_variable)` |
| `bayesfilter_cumulative_gradient` | `tape.gradient(cumulative_log_likelihood_at_t, theta_variable)` |
| `filterflow_transport_backward` | `RegularisedTransform transport @tf.custom_gradient clips d_transport to [-1,1]` |
| `primary_ablation` | `transport_upstream_clip` |
| `scalar` | `tf.reduce_mean(log_likelihoods), batch_size=1` |
| `resampling_correction` | `False` |
| `correctness_status` | `difference audit only` |

## Localization Summary

```json
{
  "best_ablation": {
    "final_relative_gradient_delta": 1.2331545006366909e-09,
    "mode": "transport_upstream_clip"
  },
  "first_raw_gradient_failure": {
    "gradient_explosion_ratio": 1.0059319506252606,
    "max_abs_gradient_delta": 0.05220128095433019,
    "relative_gradient_delta": 0.005931950625260563,
    "resampling_flag": [
      true
    ],
    "scalar_delta": 1.7926993223227328e-11,
    "status": "failure",
    "time_index": 1,
    "transport_status": "computed_raw_transport_gradient"
  },
  "first_raw_scalar_failure": {
    "status": "no_failure"
  },
  "interpretive_hint": {
    "best_ablation_final_relative_gradient_delta": 1.2331545006366909e-09,
    "best_ablation_mode": "transport_upstream_clip",
    "raw_final_relative_gradient_delta": 1.960013011801916e+228,
    "status": "transport_custom_gradient_clipping_is_primary_suspect",
    "transport_clip_final_relative_gradient_delta": 1.2331545006366909e-09
  }
}
```

## Mode Summaries

```json
[
  {
    "final_bayesfilter_gradient_diag": [
      3.711418912951682e+232,
      -3.0135023214837034e+232
    ],
    "final_bayesfilter_gradient_max_abs": 3.711418912951682e+232,
    "final_filterflow_gradient_diag": [
      18935.6850725171,
      2073.5151524806142
    ],
    "final_filterflow_gradient_max_abs": 18935.6850725171,
    "final_gradient_delta": [
      3.711418912951682e+232,
      -3.0135023214837034e+232
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 3.711418912951682e+232,
    "final_relative_gradient_delta": 1.960013011801916e+228,
    "final_scalar_delta": 9.3001517598168e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "bayesfilter_gradient_max_abs": 10507308.455697542,
      "filterflow_gradient_max_abs": 8.578663144440544,
      "gradient_explosion_ratio": 1224818.864989106,
      "resampling_flag": [
        true
      ],
      "status": "explosion",
      "time_index": 8,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 1.0059319506252606,
      "max_abs_gradient_delta": 0.05220128095433019,
      "relative_gradient_delta": 0.005931950625260563,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.7926993223227328e-11,
      "status": "failure",
      "time_index": 1,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_scalar_failure": {
      "status": "no_failure"
    },
    "mode": "raw",
    "mode_description": "BayesFilter raw TensorFlow gradient through annealed transport",
    "sample_rows": [
      {
        "bayesfilter_gradient_max_abs": 0.008913771203554865,
        "filterflow_gradient_max_abs": 0.008913771203554867,
        "gradient_delta": [
          -1.734723475976807e-18,
          -5.766308833278761e-19
        ],
        "gradient_explosion_ratio": 0.008913771203554865,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 1.734723475976807e-18,
        "relative_gradient_delta": 1.734723475976807e-18,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.852220743698464,
        "filterflow_gradient_max_abs": 8.800019462744133,
        "gradient_delta": [
          -0.05220128095433019,
          0.03535723378440208
        ],
        "gradient_explosion_ratio": 1.0059319506252606,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.05220128095433019,
        "relative_gradient_delta": 0.005931950625260563,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7926993223227328e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.033623704741912,
        "filterflow_gradient_max_abs": 1.4485716238559057,
        "gradient_delta": [
          -7.482195328597818,
          -1.0154401349116362
        ],
        "gradient_explosion_ratio": 4.1652229032909025,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.482195328597818,
        "relative_gradient_delta": 5.1652229032909025,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4985346297180513e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 118.73925036371355,
        "filterflow_gradient_max_abs": 16.840076774872443,
        "gradient_delta": [
          -135.579327138586,
          103.05266320945421
        ],
        "gradient_explosion_ratio": 7.050992222368473,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 135.579327138586,
        "relative_gradient_delta": 8.050992222368473,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.4439117396468646e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 484.3298090358302,
        "filterflow_gradient_max_abs": 11.278780998887767,
        "gradient_delta": [
          -473.0510280369424,
          417.36798351539386
        ],
        "gradient_explosion_ratio": 42.941680407092875,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 473.0510280369424,
        "relative_gradient_delta": 41.94168040709287,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.665601073204016e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13379.159809137533,
        "filterflow_gradient_max_abs": 0.16051708831084313,
        "gradient_delta": [
          -13379.320326225843,
          10962.12104851948
        ],
        "gradient_explosion_ratio": 13379.159809137533,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13379.320326225843,
        "relative_gradient_delta": 13379.320326225843,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.347366828165832e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 132185.01267551768,
        "filterflow_gradient_max_abs": 6.732984884221974,
        "gradient_delta": [
          -132191.7456604019,
          110566.32232819559
        ],
        "gradient_explosion_ratio": 19632.45350294474,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 132191.7456604019,
        "relative_gradient_delta": 19633.453502944743,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.53681536782824e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 687741.9539166507,
        "filterflow_gradient_max_abs": 16.75562828027451,
        "gradient_delta": [
          687758.709544931,
          -568315.8047401941
        ],
        "gradient_explosion_ratio": 41045.42917834313,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 687758.709544931,
        "relative_gradient_delta": 41046.429178343125,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.6477489351891563e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10507308.455697542,
        "filterflow_gradient_max_abs": 8.578663144440544,
        "gradient_delta": [
          10507299.877034398,
          -9078268.994187659
        ],
        "gradient_explosion_ratio": 1224818.864989106,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10507299.877034398,
        "relative_gradient_delta": 1224817.864989106,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.839595473844383e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 313395180.4660868,
        "filterflow_gradient_max_abs": 56.8762754108451,
        "gradient_delta": [
          -313395237.3423622,
          255462227.14382806
        ],
        "gradient_explosion_ratio": 5510121.367868772,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 313395237.3423622,
        "relative_gradient_delta": 5510122.367868772,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.645795108146558e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 58170262851.63072,
        "filterflow_gradient_max_abs": 104.45156511568617,
        "gradient_delta": [
          58170262747.17915,
          -47395967876.48537
        ],
        "gradient_explosion_ratio": 556911356.8303528,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 58170262747.17915,
        "relative_gradient_delta": 556911355.8303527,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.562661608062626e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1953444659534.2131,
        "filterflow_gradient_max_abs": 9.13071410440192,
        "gradient_delta": [
          1953444659543.3438,
          -1600304134205.1963
        ],
        "gradient_explosion_ratio": 213942155804.92844,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1953444659543.3438,
        "relative_gradient_delta": 213942155805.92844,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.412914561020443e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5780114336150.3545,
        "filterflow_gradient_max_abs": 62.46161279976278,
        "gradient_delta": [
          -5780114336212.816,
          4648132897126.474
        ],
        "gradient_explosion_ratio": 92538666183.34111,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5780114336212.816,
        "relative_gradient_delta": 92538666184.34111,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.171952003976912e-11,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 651197396761222.6,
        "filterflow_gradient_max_abs": 78.21898890138324,
        "gradient_delta": [
          651197396761144.4,
          -532756113707864.5
        ],
        "gradient_explosion_ratio": 8325310847245.006,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 651197396761144.4,
        "relative_gradient_delta": 8325310847244.006,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1748113593057496e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.989080854202397e+16,
        "filterflow_gradient_max_abs": 55.1203162059954,
        "gradient_delta": [
          8.989080854202392e+16,
          -7.319297220407389e+16
        ],
        "gradient_explosion_ratio": 1630810828553385.5,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.989080854202392e+16,
        "relative_gradient_delta": 1630810828553384.8,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1169021263413015e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.521662265102552e+18,
        "filterflow_gradient_max_abs": 3.2014311273644616,
        "gradient_delta": [
          -5.521662265102552e+18,
          4.4846630218317983e+18
        ],
        "gradient_explosion_ratio": 1.724748103404677e+18,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.521662265102552e+18,
        "relative_gradient_delta": 1.724748103404677e+18,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.603695616533514e-11,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.1027776008943575e+19,
        "filterflow_gradient_max_abs": 25.054390338542845,
        "gradient_delta": [
          4.1027776008943575e+19,
          -3.3342190140776456e+19
        ],
        "gradient_explosion_ratio": 1.6375483679532127e+18,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.1027776008943575e+19,
        "relative_gradient_delta": 1.6375483679532127e+18,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1939249588976963e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.4979554297475257e+21,
        "filterflow_gradient_max_abs": 145.3600680670563,
        "gradient_delta": [
          -4.4979554297475257e+21,
          3.652309481561789e+21
        ],
        "gradient_explosion_ratio": 3.0943542401703928e+19,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.4979554297475257e+21,
        "relative_gradient_delta": 3.0943542401703928e+19,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.48947520983711e-09,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2986940029761342e+24,
        "filterflow_gradient_max_abs": 168.66458545141114,
        "gradient_delta": [
          1.2986940029761342e+24,
          -1.0544731195972697e+24
        ],
        "gradient_explosion_ratio": 7.699861826359878e+21,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2986940029761342e+24,
        "relative_gradient_delta": 7.699861826359878e+21,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.252356523513299e-09,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.769795514170296e+25,
        "filterflow_gradient_max_abs": 101.15910809775511,
        "gradient_delta": [
          1.769795514170296e+25,
          -1.4370051257200713e+25
        ],
        "gradient_explosion_ratio": 1.7495167241491038e+23,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.769795514170296e+25,
        "relative_gradient_delta": 1.7495167241491038e+23,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.767464479802584e-09,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7617860351760577e+27,
        "filterflow_gradient_max_abs": 125.28072286451086,
        "gradient_delta": [
          -1.7617860351760577e+27,
          1.4304799093238545e+27
        ],
        "gradient_explosion_ratio": 1.406270649540713e+25,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7617860351760577e+27,
        "relative_gradient_delta": 1.406270649540713e+25,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9853310934413457e-09,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.439531878989388e+30,
        "filterflow_gradient_max_abs": 278.9526477486435,
        "gradient_delta": [
          4.439531878989388e+30,
          -3.604694796995738e+30
        ],
        "gradient_explosion_ratio": 1.5915001756820485e+28,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.439531878989388e+30,
        "relative_gradient_delta": 1.5915001756820485e+28,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.0152165209074155e-09,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.152352826870279e+32,
        "filterflow_gradient_max_abs": 252.28215416061428,
        "gradient_delta": [
          -7.152352826870279e+32,
          5.807378409386588e+32
        ],
        "gradient_explosion_ratio": 2.835060946212139e+30,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.152352826870279e+32,
        "relative_gradient_delta": 2.835060946212139e+30,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.021582983819826e-09,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3718004064716017e+34,
        "filterflow_gradient_max_abs": 69.58591013728201,
        "gradient_delta": [
          -3.3718004064716017e+34,
          2.7377450745911802e+34
        ],
        "gradient_explosion_ratio": 4.845521744013367e+32,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3718004064716017e+34,
        "relative_gradient_delta": 4.845521744013367e+32,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9725839567618095e-09,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3104626374692797e+36,
        "filterflow_gradient_max_abs": 64.72471139759364,
        "gradient_delta": [
          2.3104626374692797e+36,
          -1.8759907158098694e+36
        ],
        "gradient_explosion_ratio": 3.5696762296497146e+34,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3104626374692797e+36,
        "relative_gradient_delta": 3.5696762296497146e+34,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.974680057832302e-09,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.958273048917215e+38,
        "filterflow_gradient_max_abs": 0.6534447816938739,
        "gradient_delta": [
          -3.958273048917215e+38,
          3.21393654606172e+38
        ],
        "gradient_explosion_ratio": 3.958273048917215e+38,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.958273048917215e+38,
        "relative_gradient_delta": 3.958273048917215e+38,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.903298934597842e-09,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.8356474235433043e+40,
        "filterflow_gradient_max_abs": 262.5095687458148,
        "gradient_delta": [
          2.8356474235433043e+40,
          -2.3024146639610743e+40
        ],
        "gradient_explosion_ratio": 1.0802072614309275e+38,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.8356474235433043e+40,
        "relative_gradient_delta": 1.0802072614309275e+38,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.970814705349767e-09,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.3968326022006136e+42,
        "filterflow_gradient_max_abs": 28.548993251385596,
        "gradient_delta": [
          4.3968326022006136e+42,
          -3.5700243926572466e+42
        ],
        "gradient_explosion_ratio": 1.5401007536359335e+41,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.3968326022006136e+42,
        "relative_gradient_delta": 1.5401007536359335e+41,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9090827524669294e-09,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2186234761245253e+44,
        "filterflow_gradient_max_abs": 485.70702239538065,
        "gradient_delta": [
          2.2186234761245253e+44,
          -1.801420717574852e+44
        ],
        "gradient_explosion_ratio": 4.567822522274543e+41,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2186234761245253e+44,
        "relative_gradient_delta": 4.567822522274543e+41,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8526088158287166e-09,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.766688839459076e+45,
        "filterflow_gradient_max_abs": 245.11951564783823,
        "gradient_delta": [
          -7.766688839459076e+45,
          6.306195131922029e+45
        ],
        "gradient_explosion_ratio": 3.1685314076001325e+43,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.766688839459076e+45,
        "relative_gradient_delta": 3.1685314076001325e+43,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8581510491676454e-09,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.869482957898164e+49,
        "filterflow_gradient_max_abs": 434.75519438634416,
        "gradient_delta": [
          1.869482957898164e+49,
          -1.517934617542802e+49
        ],
        "gradient_explosion_ratio": 4.3000819358511274e+46,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.869482957898164e+49,
        "relative_gradient_delta": 4.3000819358511274e+46,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9084219477226725e-09,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.04083970997124e+50,
        "filterflow_gradient_max_abs": 251.90780939902413,
        "gradient_delta": [
          -3.04083970997124e+50,
          2.46902256775332e+50
        ],
        "gradient_explosion_ratio": 1.207124033679529e+48,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.04083970997124e+50,
        "relative_gradient_delta": 1.207124033679529e+48,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.980804936214554e-09,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.370752220623899e+53,
        "filterflow_gradient_max_abs": 369.7748801823844,
        "gradient_delta": [
          -6.370752220623899e+53,
          5.1727592550288095e+53
        ],
        "gradient_explosion_ratio": 1.7228731755606676e+51,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.370752220623899e+53,
        "relative_gradient_delta": 1.7228731755606676e+51,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9715820915043878e-09,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.425444668497596e+54,
        "filterflow_gradient_max_abs": 153.94165873710156,
        "gradient_delta": [
          4.425444668497596e+54,
          -3.593258958017613e+54
        ],
        "gradient_explosion_ratio": 2.874754439313455e+52,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.425444668497596e+54,
        "relative_gradient_delta": 2.874754439313455e+52,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.075740551139461e-09,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5539871920405229e+57,
        "filterflow_gradient_max_abs": 231.88010181357106,
        "gradient_delta": [
          1.5539871920405229e+57,
          -1.2617665345469409e+57
        ],
        "gradient_explosion_ratio": 6.701684102631241e+54,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5539871920405229e+57,
        "relative_gradient_delta": 6.701684102631241e+54,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8847040312030003e-09,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.323781683294017e+60,
        "filterflow_gradient_max_abs": 317.10552544548756,
        "gradient_delta": [
          2.323781683294017e+60,
          -1.88680439649131e+60
        ],
        "gradient_explosion_ratio": 7.328102151576951e+57,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.323781683294017e+60,
        "relative_gradient_delta": 7.328102151576951e+57,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8788775807697675e-09,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.053291723130761e+63,
        "filterflow_gradient_max_abs": 440.433114763931,
        "gradient_delta": [
          -4.053291723130761e+63,
          3.2910873987591114e+63
        ],
        "gradient_explosion_ratio": 9.202967686258778e+60,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.053291723130761e+63,
        "relative_gradient_delta": 9.202967686258778e+60,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.7967104188064695e-09,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2275212638553773e+65,
        "filterflow_gradient_max_abs": 274.3754691050723,
        "gradient_delta": [
          1.2275212638553773e+65,
          -9.966910946063454e+64
        ],
        "gradient_explosion_ratio": 4.473873950390576e+62,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2275212638553773e+65,
        "relative_gradient_delta": 4.473873950390576e+62,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9457680739142234e-09,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.387169703671358e+68,
        "filterflow_gradient_max_abs": 184.24153726601756,
        "gradient_delta": [
          -1.387169703671358e+68,
          1.1263183220002733e+68
        ],
        "gradient_explosion_ratio": 7.529082335372017e+65,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.387169703671358e+68,
        "relative_gradient_delta": 7.529082335372017e+65,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8393571938067907e-09,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1095924491289246e+70,
        "filterflow_gradient_max_abs": 187.1386096136716,
        "gradient_delta": [
          -2.1095924491289246e+70,
          1.7128925330087772e+70
        ],
        "gradient_explosion_ratio": 1.1272887265134444e+68,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1095924491289246e+70,
        "relative_gradient_delta": 1.1272887265134444e+68,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.6310544853913598e-09,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.468486436839226e+73,
        "filterflow_gradient_max_abs": 954.1501022077981,
        "gradient_delta": [
          -5.468486436839226e+73,
          4.4401607468527537e+73
        ],
        "gradient_explosion_ratio": 5.73126432013763e+70,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.468486436839226e+73,
        "relative_gradient_delta": 5.73126432013763e+70,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.98600263906701e-09,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.1936811685208645e+75,
        "filterflow_gradient_max_abs": 422.91186590476366,
        "gradient_delta": [
          4.1936811685208645e+75,
          -3.4050772045155175e+75
        ],
        "gradient_explosion_ratio": 9.91620596775889e+72,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.1936811685208645e+75,
        "relative_gradient_delta": 9.91620596775889e+72,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5840096163374255e-09,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.318805187781066e+77,
        "filterflow_gradient_max_abs": 354.26740709319216,
        "gradient_delta": [
          6.318805187781066e+77,
          -5.130580661732676e+77
        ],
        "gradient_explosion_ratio": 1.783625888598571e+75,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.318805187781066e+77,
        "relative_gradient_delta": 1.783625888598571e+75,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.941782094647351e-09,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.097530718514138e+80,
        "filterflow_gradient_max_abs": 199.05378088782396,
        "gradient_delta": [
          2.097530718514138e+80,
          -1.7030989596909792e+80
        ],
        "gradient_explosion_ratio": 1.0537507547752604e+78,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.097530718514138e+80,
        "relative_gradient_delta": 1.0537507547752604e+78,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.940716280543711e-09,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2244886471654443e+83,
        "filterflow_gradient_max_abs": 548.7404094827189,
        "gradient_delta": [
          2.2244886471654443e+83,
          -1.8061829881164985e+83
        ],
        "gradient_explosion_ratio": 4.0538087021191e+80,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2244886471654443e+83,
        "relative_gradient_delta": 4.0538087021191e+80,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.836934408558591e-09,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0182157792441476e+85,
        "filterflow_gradient_max_abs": 399.4756572109477,
        "gradient_delta": [
          -2.0182157792441476e+85,
          1.6386988584833154e+85
        ],
        "gradient_explosion_ratio": 5.0521621100391746e+82,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0182157792441476e+85,
        "relative_gradient_delta": 5.0521621100391746e+82,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.73063721528888e-09,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.942218403148744e+87,
        "filterflow_gradient_max_abs": 381.20393707705813,
        "gradient_delta": [
          8.942218403148744e+87,
          -7.260672144301769e+87
        ],
        "gradient_explosion_ratio": 2.3457833283975572e+85,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.942218403148744e+87,
        "relative_gradient_delta": 2.3457833283975572e+85,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.649024276659475e-09,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.134939199506339e+90,
        "filterflow_gradient_max_abs": 48.850988576799736,
        "gradient_delta": [
          -5.134939199506339e+90,
          4.169335653377767e+90
        ],
        "gradient_explosion_ratio": 1.0511433543322436e+89,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.134939199506339e+90,
        "relative_gradient_delta": 1.0511433543322436e+89,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.737742642646481e-09,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1585393826649593e+91,
        "filterflow_gradient_max_abs": 346.85073969207997,
        "gradient_delta": [
          -1.1585393826649593e+91,
          9.406809635548444e+90
        ],
        "gradient_explosion_ratio": 3.340166965460312e+88,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1585393826649593e+91,
        "relative_gradient_delta": 3.340166965460312e+88,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.721428581433429e-09,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.215874986802222e+93,
        "filterflow_gradient_max_abs": 322.6295207830076,
        "gradient_delta": [
          8.215874986802222e+93,
          -6.670914527958242e+93
        ],
        "gradient_explosion_ratio": 2.546535409054527e+91,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.215874986802222e+93,
        "relative_gradient_delta": 2.546535409054527e+91,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6360639771592105e-09,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.667903004177259e+96,
        "filterflow_gradient_max_abs": 86.66552831338745,
        "gradient_delta": [
          4.667903004177259e+96,
          -3.790123634510905e+96
        ],
        "gradient_explosion_ratio": 5.3861126736548094e+94,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.667903004177259e+96,
        "relative_gradient_delta": 5.3861126736548094e+94,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.636163453142217e-09,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.26537262037288e+99,
        "filterflow_gradient_max_abs": 1118.3947944525503,
        "gradient_delta": [
          -5.26537262037288e+99,
          4.27524162244225e+99
        ],
        "gradient_explosion_ratio": 4.707973111543548e+96,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.26537262037288e+99,
        "relative_gradient_delta": 4.707973111543548e+96,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9218832625920186e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.7420065745238236e+101,
        "filterflow_gradient_max_abs": 72.987643547552,
        "gradient_delta": [
          -3.7420065745238236e+101,
          3.038338102978147e+101
        ],
        "gradient_explosion_ratio": 5.126904216445731e+99,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.7420065745238236e+101,
        "relative_gradient_delta": 5.126904216445731e+99,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9393910356011475e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.072461913603353e+103,
        "filterflow_gradient_max_abs": 7.513193750877159,
        "gradient_delta": [
          5.072461913603353e+103,
          -4.118606956207095e+103
        ],
        "gradient_explosion_ratio": 6.751405702815992e+102,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.072461913603353e+103,
        "relative_gradient_delta": 6.751405702815992e+102,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.889368827003636e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1251524796144548e+105,
        "filterflow_gradient_max_abs": 330.52600026078443,
        "gradient_delta": [
          -1.1251524796144548e+105,
          9.135723260742698e+104
        ],
        "gradient_explosion_ratio": 3.404126993721255e+102,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1251524796144548e+105,
        "relative_gradient_delta": 3.404126993721255e+102,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.899515377270291e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1740940847546465e+107,
        "filterflow_gradient_max_abs": 286.4569368626525,
        "gradient_delta": [
          2.1740940847546465e+107,
          -1.7652649095118205e+107
        ],
        "gradient_explosion_ratio": 7.589601803907647e+104,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1740940847546465e+107,
        "relative_gradient_delta": 7.589601803907647e+104,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.8836134308439796e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.4741876039950455e+110,
        "filterflow_gradient_max_abs": 609.6787100623405,
        "gradient_delta": [
          5.4741876039950455e+110,
          -4.4447898336964545e+110
        ],
        "gradient_explosion_ratio": 8.978807220339548e+107,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.4741876039950455e+110,
        "relative_gradient_delta": 8.978807220339548e+107,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.874831122629985e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.66645527463394e+112,
        "filterflow_gradient_max_abs": 237.18680047332637,
        "gradient_delta": [
          5.66645527463394e+112,
          -4.6009023840190955e+112
        ],
        "gradient_explosion_ratio": 2.3890263974749218e+110,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.66645527463394e+112,
        "relative_gradient_delta": 2.3890263974749218e+110,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.782176349886868e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1325832104563677e+115,
        "filterflow_gradient_max_abs": 20.398532585564105,
        "gradient_delta": [
          -2.1325832104563677e+115,
          1.7315599791338083e+115
        ],
        "gradient_explosion_ratio": 1.0454591287441831e+114,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1325832104563677e+115,
        "relative_gradient_delta": 1.0454591287441831e+114,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.6820893001277e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6111818097066886e+116,
        "filterflow_gradient_max_abs": 478.6428510468603,
        "gradient_delta": [
          1.6111818097066886e+116,
          -1.3082059012363045e+116
        ],
        "gradient_explosion_ratio": 3.366146190594519e+113,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6111818097066886e+116,
        "relative_gradient_delta": 3.366146190594519e+113,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.958078309551638e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.809352796238392e+118,
        "filterflow_gradient_max_abs": 310.27237965253573,
        "gradient_delta": [
          -6.809352796238392e+118,
          5.528882872169889e+118
        ],
        "gradient_explosion_ratio": 2.1946371133208738e+116,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.809352796238392e+118,
        "relative_gradient_delta": 2.1946371133208738e+116,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.521620328683639e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.243434585160553e+121,
        "filterflow_gradient_max_abs": 291.33394004387503,
        "gradient_delta": [
          -2.243434585160553e+121,
          1.8215662227957655e+121
        ],
        "gradient_explosion_ratio": 7.700560342618133e+118,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.243434585160553e+121,
        "relative_gradient_delta": 7.700560342618133e+118,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.524789349285129e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.056219628974459e+124,
        "filterflow_gradient_max_abs": 772.789629727978,
        "gradient_delta": [
          -9.056219628974459e+124,
          7.353235922936114e+124
        ],
        "gradient_explosion_ratio": 1.1718867956551447e+122,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.056219628974459e+124,
        "relative_gradient_delta": 1.1718867956551447e+122,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.415127818901965e-09,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2213983846848298e+127,
        "filterflow_gradient_max_abs": 137.0827775975205,
        "gradient_delta": [
          -1.2213983846848298e+127,
          9.917195967449928e+126
        ],
        "gradient_explosion_ratio": 8.909933152003202e+124,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2213983846848298e+127,
        "relative_gradient_delta": 8.909933152003202e+124,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.988418484368594e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3365812652215278e+129,
        "filterflow_gradient_max_abs": 205.40967733109431,
        "gradient_delta": [
          1.3365812652215278e+129,
          -1.0852428249317207e+129
        ],
        "gradient_explosion_ratio": 6.506905042585353e+126,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3365812652215278e+129,
        "relative_gradient_delta": 6.506905042585353e+126,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.800110448537453e-09,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.0671830428588906e+132,
        "filterflow_gradient_max_abs": 1075.2940301638955,
        "gradient_delta": [
          4.0671830428588906e+132,
          -3.3023665150768125e+132
        ],
        "gradient_explosion_ratio": 3.7823915401436514e+129,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.0671830428588906e+132,
        "relative_gradient_delta": 3.7823915401436514e+129,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.299266720408923e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.888782007558424e+135,
        "filterflow_gradient_max_abs": 1320.7702359098546,
        "gradient_delta": [
          -4.888782007558424e+135,
          3.96946727775563e+135
        ],
        "gradient_explosion_ratio": 3.701462884792094e+132,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.888782007558424e+135,
        "relative_gradient_delta": 3.701462884792094e+132,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.148105858803319e-09,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4065535655293914e+137,
        "filterflow_gradient_max_abs": 352.8826174689448,
        "gradient_delta": [
          -2.4065535655293914e+137,
          1.954011370473425e+137
        ],
        "gradient_explosion_ratio": 6.81969994099009e+134,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4065535655293914e+137,
        "relative_gradient_delta": 6.81969994099009e+134,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.5889797800336964e-09,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.50195263643835e+140,
        "filterflow_gradient_max_abs": 974.6366511077524,
        "gradient_delta": [
          -6.50195263643835e+140,
          5.279288009151538e+140
        ],
        "gradient_explosion_ratio": 6.671155480402221e+137,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.50195263643835e+140,
        "relative_gradient_delta": 6.671155480402221e+137,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.8240451633319026e-09,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.075476648355451e+143,
        "filterflow_gradient_max_abs": 731.310897142959,
        "gradient_delta": [
          2.075476648355451e+143,
          -1.6851920639242042e+143
        ],
        "gradient_explosion_ratio": 2.8380223191857213e+140,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.075476648355451e+143,
        "relative_gradient_delta": 2.8380223191857213e+140,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.972274953412125e-09,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.1761236228221957e+145,
        "filterflow_gradient_max_abs": 483.3559108394908,
        "gradient_delta": [
          -3.1761236228221957e+145,
          2.5788670411990546e+145
        ],
        "gradient_explosion_ratio": 6.570983309805637e+142,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.1761236228221957e+145,
        "relative_gradient_delta": 6.570983309805637e+142,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.955818783651921e-09,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.288453792439288e+149,
        "filterflow_gradient_max_abs": 1076.6780654517022,
        "gradient_delta": [
          3.288453792439288e+149,
          -2.6700739986601146e+149
        ],
        "gradient_explosion_ratio": 3.054259112318474e+146,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.288453792439288e+149,
        "relative_gradient_delta": 3.054259112318474e+146,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5558010697277496e-09,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.905584579851266e+151,
        "filterflow_gradient_max_abs": 18.05494027199655,
        "gradient_delta": [
          4.905584579851266e+151,
          -3.9831101975658074e+151
        ],
        "gradient_explosion_ratio": 2.7170317408692246e+150,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.905584579851266e+151,
        "relative_gradient_delta": 2.7170317408692246e+150,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6730690428375965e-09,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.759979522647206e+153,
        "filterflow_gradient_max_abs": 989.4278480713913,
        "gradient_delta": [
          3.759979522647206e+153,
          -3.0529313144059125e+153
        ],
        "gradient_explosion_ratio": 3.800155342278084e+150,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.759979522647206e+153,
        "relative_gradient_delta": 3.800155342278084e+150,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.355683813628275e-09,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2439647942646707e+156,
        "filterflow_gradient_max_abs": 778.7073741209738,
        "gradient_delta": [
          2.2439647942646707e+156,
          -1.821996728325755e+156
        ],
        "gradient_explosion_ratio": 2.8816534539662216e+153,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2439647942646707e+156,
        "relative_gradient_delta": 2.8816534539662216e+153,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.821792577378801e-09,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.609469349780909e+159,
        "filterflow_gradient_max_abs": 1097.9215016104433,
        "gradient_delta": [
          -4.609469349780909e+159,
          3.74267818108561e+159
        ],
        "gradient_explosion_ratio": 4.198359666897578e+156,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.609469349780909e+159,
        "relative_gradient_delta": 4.198359666897578e+156,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0083482493428164e-08,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.865748592858761e+162,
        "filterflow_gradient_max_abs": 1697.7646785016034,
        "gradient_delta": [
          4.865748592858761e+162,
          -3.950765199036654e+162
        ],
        "gradient_explosion_ratio": 2.865973508857026e+159,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.865748592858761e+162,
        "relative_gradient_delta": 2.865973508857026e+159,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8990448324984754e-08,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.963036594210704e+165,
        "filterflow_gradient_max_abs": 947.0739014815089,
        "gradient_delta": [
          -2.963036594210704e+165,
          2.4058501249037973e+165
        ],
        "gradient_explosion_ratio": 3.128622369992059e+162,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.963036594210704e+165,
        "relative_gradient_delta": 3.128622369992059e+162,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1565390423129429e-08,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.75318086937974e+166,
        "filterflow_gradient_max_abs": 249.89093531615012,
        "gradient_delta": [
          -7.75318086937974e+166,
          6.29522807765652e+166
        ],
        "gradient_explosion_ratio": 3.102625895401442e+164,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.75318086937974e+166,
        "relative_gradient_delta": 3.102625895401442e+164,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.132605782724568e-09,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.095759089574179e+170,
        "filterflow_gradient_max_abs": 974.2890696675929,
        "gradient_delta": [
          -8.095759089574179e+170,
          6.573385915954729e+170
        ],
        "gradient_explosion_ratio": 8.309401533506152e+167,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.095759089574179e+170,
        "relative_gradient_delta": 8.309401533506152e+167,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.223679515140248e-09,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.828163529810629e+173,
        "filterflow_gradient_max_abs": 1029.3299119039873,
        "gradient_delta": [
          8.828163529810629e+173,
          -7.168064806342287e+173
        ],
        "gradient_explosion_ratio": 8.57661224813808e+170,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.828163529810629e+173,
        "relative_gradient_delta": 8.57661224813808e+170,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.178016403486254e-09,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5346781540287131e+177,
        "filterflow_gradient_max_abs": 1426.254117759735,
        "gradient_delta": [
          -1.5346781540287131e+177,
          1.2460884336599442e+177
        ],
        "gradient_explosion_ratio": 1.0760201389912784e+174,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5346781540287131e+177,
        "relative_gradient_delta": 1.0760201389912784e+174,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.153612730486202e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.1102547763389943e+180,
        "filterflow_gradient_max_abs": 1942.7454564725651,
        "gradient_delta": [
          3.1102547763389943e+180,
          -2.525384552036244e+180
        ],
        "gradient_explosion_ratio": 1.600958461118355e+177,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.1102547763389943e+180,
        "relative_gradient_delta": 1.600958461118355e+177,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.01524527357833e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.507924853971741e+182,
        "filterflow_gradient_max_abs": 169.06130724664092,
        "gradient_delta": [
          5.507924853971741e+182,
          -4.472182936849121e+182
        ],
        "gradient_explosion_ratio": 3.257945264753167e+180,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.507924853971741e+182,
        "relative_gradient_delta": 3.257945264753167e+180,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.081496278260602e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4926078128865e+186,
        "filterflow_gradient_max_abs": 1963.5208371745916,
        "gradient_delta": [
          -1.4926078128865e+186,
          1.2119292418060542e+186
        ],
        "gradient_explosion_ratio": 7.601690721216323e+182,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4926078128865e+186,
        "relative_gradient_delta": 7.601690721216323e+182,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.653859933678177e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0301533401217673e+188,
        "filterflow_gradient_max_abs": 1119.9768301540837,
        "gradient_delta": [
          2.0301533401217673e+188,
          -1.6483916116489583e+188
        ],
        "gradient_explosion_ratio": 1.812674410275491e+185,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0301533401217673e+188,
        "relative_gradient_delta": 1.812674410275491e+185,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.3080741458397824e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0914417834458432e+191,
        "filterflow_gradient_max_abs": 979.6868013870265,
        "gradient_delta": [
          -2.0914417834458432e+191,
          1.6981550230474107e+191
        ],
        "gradient_explosion_ratio": 2.1348065325416345e+188,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0914417834458432e+191,
        "relative_gradient_delta": 2.1348065325416345e+188,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.394845624730806e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.551276941484494e+195,
        "filterflow_gradient_max_abs": 2882.4178802677957,
        "gradient_delta": [
          1.551276941484494e+195,
          -1.2595658895076927e+195
        ],
        "gradient_explosion_ratio": 5.381859972851577e+191,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.551276941484494e+195,
        "relative_gradient_delta": 5.381859972851577e+191,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.620751946684322e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0104075479898404e+197,
        "filterflow_gradient_max_abs": 858.8073873147812,
        "gradient_delta": [
          -1.0104075479898404e+197,
          8.204046923634564e+196
        ],
        "gradient_explosion_ratio": 1.1765240529067465e+194,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0104075479898404e+197,
        "relative_gradient_delta": 1.1765240529067465e+194,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.615852837261627e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.1621631550850765e+199,
        "filterflow_gradient_max_abs": 442.0116504772855,
        "gradient_delta": [
          -3.1621631550850765e+199,
          2.56753178023242e+199
        ],
        "gradient_explosion_ratio": 7.154026713256457e+196,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.1621631550850765e+199,
        "relative_gradient_delta": 7.154026713256457e+196,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.274422841874184e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1067232618450242e+204,
        "filterflow_gradient_max_abs": 3282.5855155180925,
        "gradient_delta": [
          -1.1067232618450242e+204,
          8.986086445729715e+203
        ],
        "gradient_explosion_ratio": 3.371498645238948e+200,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1067232618450242e+204,
        "relative_gradient_delta": 3.371498645238948e+200,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0136062655874412e-08,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.9897543841550904e+206,
        "filterflow_gradient_max_abs": 1855.9144036285215,
        "gradient_delta": [
          4.9897543841550904e+206,
          -4.0514522270207025e+206
        ],
        "gradient_explosion_ratio": 2.6885692434950443e+203,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.9897543841550904e+206,
        "relative_gradient_delta": 2.6885692434950443e+203,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.873637741795392e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.3037452983866495e+209,
        "filterflow_gradient_max_abs": 1310.8611477302254,
        "gradient_delta": [
          -4.3037452983866495e+209,
          3.49444424139345e+209
        ],
        "gradient_explosion_ratio": 3.2831435318978254e+206,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.3037452983866495e+209,
        "relative_gradient_delta": 3.2831435318978254e+206,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.93335175330867e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.050496088060541e+212,
        "filterflow_gradient_max_abs": 914.416967723082,
        "gradient_delta": [
          3.050496088060541e+212,
          -2.4768632317327086e+212
        ],
        "gradient_explosion_ratio": 3.3360011851664806e+209,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.050496088060541e+212,
        "relative_gradient_delta": 3.3360011851664806e+209,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.058265166255296e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.5506494558921818e+216,
        "filterflow_gradient_max_abs": 3551.3298618369327,
        "gradient_delta": [
          -2.5506494558921818e+216,
          2.0710106395694523e+216
        ],
        "gradient_explosion_ratio": 7.182237514182513e+212,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.5506494558921818e+216,
        "relative_gradient_delta": 7.182237514182513e+212,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.786315675024525e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.688985190153924e+219,
        "filterflow_gradient_max_abs": 3023.0985131010166,
        "gradient_delta": [
          5.688985190153924e+219,
          -4.619195644444477e+219
        ],
        "gradient_explosion_ratio": 1.8818391678272863e+216,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.688985190153924e+219,
        "relative_gradient_delta": 1.8818391678272863e+216,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.745331570025883e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.7341907250410905e+222,
        "filterflow_gradient_max_abs": 2001.070628323309,
        "gradient_delta": [
          -5.7341907250410905e+222,
          4.6559004701517023e+222
        ],
        "gradient_explosion_ratio": 2.8655613869290317e+219,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.7341907250410905e+222,
        "relative_gradient_delta": 2.8655613869290317e+219,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.205052720062668e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0626986513089231e+226,
        "filterflow_gradient_max_abs": 2346.9001573329506,
        "gradient_delta": [
          1.0626986513089231e+226,
          -8.628626753992973e+225
        ],
        "gradient_explosion_ratio": 4.528094848809369e+222,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0626986513089231e+226,
        "relative_gradient_delta": 4.528094848809369e+222,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.456598728414974e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.019387834272036e+229,
        "filterflow_gradient_max_abs": 4046.6212127655212,
        "gradient_delta": [
          -4.019387834272036e+229,
          3.2635589928298165e+229
        ],
        "gradient_explosion_ratio": 9.932700944660759e+225,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.019387834272036e+229,
        "relative_gradient_delta": 9.932700944660759e+225,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.6329352092725458e-08,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.711418912951682e+232,
        "filterflow_gradient_max_abs": 2730.4139020142047,
        "gradient_delta": [
          3.711418912951682e+232,
          -3.0135023214837034e+232
        ],
        "gradient_explosion_ratio": 1.359288022308192e+229,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.711418912951682e+232,
        "relative_gradient_delta": 1.359288022308192e+229,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.300094916397939e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_raw_transport_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      18935.685049166474,
      2073.5151589713964
    ],
    "final_bayesfilter_gradient_max_abs": 18935.685049166474,
    "final_filterflow_gradient_diag": [
      18935.6850725171,
      2073.5151524806142
    ],
    "final_filterflow_gradient_max_abs": 18935.6850725171,
    "final_gradient_delta": [
      -2.3350625269813463e-05,
      6.49078219794319e-06
    ],
    "final_gradient_within_tolerance": true,
    "final_max_abs_gradient_delta": 2.3350625269813463e-05,
    "final_relative_gradient_delta": 1.2331545006366909e-09,
    "final_scalar_delta": 9.3001517598168e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "status": "no_explosion"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 0.9982253078830365,
      "max_abs_gradient_delta": 0.015617325169657192,
      "relative_gradient_delta": 0.0017746921169634778,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.7926993223227328e-11,
      "status": "failure",
      "time_index": 1,
      "transport_status": "computed_with_clipped_upstream_gradient"
    },
    "first_scalar_failure": {
      "status": "no_failure"
    },
    "mode": "transport_upstream_clip",
    "mode_description": "Clip upstream gradient entering transport matrix to [-1,1]",
    "sample_rows": [
      {
        "bayesfilter_gradient_max_abs": 0.008913771203554865,
        "filterflow_gradient_max_abs": 0.008913771203554867,
        "gradient_delta": [
          -1.734723475976807e-18,
          -5.766308833278761e-19
        ],
        "gradient_explosion_ratio": 0.008913771203554865,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 1.734723475976807e-18,
        "relative_gradient_delta": 1.734723475976807e-18,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.784402137574476,
        "filterflow_gradient_max_abs": 8.800019462744133,
        "gradient_delta": [
          0.015617325169657192,
          -0.010206170198178068
        ],
        "gradient_explosion_ratio": 0.9982253078830365,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.015617325169657192,
        "relative_gradient_delta": 0.0017746921169634778,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7926993223227328e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.956008778138175,
        "filterflow_gradient_max_abs": 1.4485716238559057,
        "gradient_delta": [
          -7.404580401994081,
          -1.0858187897624467
        ],
        "gradient_explosion_ratio": 4.111642586428739,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.404580401994081,
        "relative_gradient_delta": 5.111642586428739,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4985346297180513e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 54.07229669910405,
        "filterflow_gradient_max_abs": 16.840076774872443,
        "gradient_delta": [
          -63.27047341702753,
          54.07229669910405
        ],
        "gradient_explosion_ratio": 3.2109293456302326,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 63.27047341702753,
        "relative_gradient_delta": 3.7571368743066067,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.4439117396468646e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 31.247625389868073,
        "filterflow_gradient_max_abs": 11.278780998887767,
        "gradient_delta": [
          -6.048036986860824,
          31.247625389868073
        ],
        "gradient_explosion_ratio": 2.7704789545031057,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 31.247625389868073,
        "relative_gradient_delta": 2.7704789545031057,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.665601073204016e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 49.23471339246846,
        "filterflow_gradient_max_abs": 0.16051708831084313,
        "gradient_delta": [
          49.07419630415762,
          5.576227567012385
        ],
        "gradient_explosion_ratio": 49.23471339246846,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 49.07419630415762,
        "relative_gradient_delta": 49.07419630415762,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.347366828165832e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 87.70335608185847,
        "filterflow_gradient_max_abs": 6.732984884221974,
        "gradient_delta": [
          80.9703711976365,
          1.1220475405753023
        ],
        "gradient_explosion_ratio": 13.025924993145589,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 80.9703711976365,
        "relative_gradient_delta": 12.025924993145589,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.53681536782824e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 34.69289891468638,
        "filterflow_gradient_max_abs": 16.75562828027451,
        "gradient_delta": [
          45.217675425731,
          -34.69289891468638
        ],
        "gradient_explosion_ratio": 2.0705221155764386,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 45.217675425731,
        "relative_gradient_delta": 2.698655918439257,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.6477489351891563e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 229.76048423427102,
        "filterflow_gradient_max_abs": 8.578663144440544,
        "gradient_delta": [
          221.18182108983046,
          -24.544121729215902
        ],
        "gradient_explosion_ratio": 26.782784259709363,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 221.18182108983046,
        "relative_gradient_delta": 25.782784259709363,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.839595473844383e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 150.60339205791385,
        "filterflow_gradient_max_abs": 56.8762754108451,
        "gradient_delta": [
          93.72711664706875,
          -18.053441489016183
        ],
        "gradient_explosion_ratio": 2.6479123495698693,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 93.72711664706875,
        "relative_gradient_delta": 1.6479123495698695,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.645795108146558e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 104.88905184994616,
        "filterflow_gradient_max_abs": 104.45156511568617,
        "gradient_delta": [
          0.4374867342599913,
          22.355985820722843
        ],
        "gradient_explosion_ratio": 1.0041884172226185,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 22.355985820722843,
        "relative_gradient_delta": 0.21403208076357969,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.562661608062626e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 334.26767640414283,
        "filterflow_gradient_max_abs": 9.13071410440192,
        "gradient_delta": [
          -325.1369622997409,
          31.387910231402607
        ],
        "gradient_explosion_ratio": 36.60914935919331,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 325.1369622997409,
        "relative_gradient_delta": 35.60914935919331,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.412914561020443e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 106.41188501815697,
        "filterflow_gradient_max_abs": 62.46161279976278,
        "gradient_delta": [
          43.95027221839418,
          57.34469890839237
        ],
        "gradient_explosion_ratio": 1.703636525673591,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 57.34469890839237,
        "relative_gradient_delta": 0.9180790622910421,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.171952003976912e-11,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 400.49649931986283,
        "filterflow_gradient_max_abs": 78.21898890138324,
        "gradient_delta": [
          322.2775104184796,
          21.84189605761094
        ],
        "gradient_explosion_ratio": 5.120195299696342,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 322.2775104184796,
        "relative_gradient_delta": 4.120195299696342,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1748113593057496e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 103.15592537730333,
        "filterflow_gradient_max_abs": 55.1203162059954,
        "gradient_delta": [
          -158.27624158329874,
          -17.460524098171465
        ],
        "gradient_explosion_ratio": 1.8714683165421162,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 158.27624158329874,
        "relative_gradient_delta": 2.871468316542116,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1169021263413015e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1076.1632427692716,
        "filterflow_gradient_max_abs": 3.2014311273644616,
        "gradient_delta": [
          1072.9618116419072,
          -26.763911671794446
        ],
        "gradient_explosion_ratio": 336.1506776049903,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1072.9618116419072,
        "relative_gradient_delta": 335.1506776049903,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.603695616533514e-11,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1138.9811452833271,
        "filterflow_gradient_max_abs": 25.054390338542845,
        "gradient_delta": [
          1113.9267549447843,
          -148.76807043577526
        ],
        "gradient_explosion_ratio": 45.46034167637104,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1113.9267549447843,
        "relative_gradient_delta": 44.46034167637104,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1939249588976963e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 131.75953807567103,
        "filterflow_gradient_max_abs": 145.3600680670563,
        "gradient_delta": [
          -13.600529991385258,
          -32.6508477584607
        ],
        "gradient_explosion_ratio": 0.9064355832228204,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 32.6508477584607,
        "relative_gradient_delta": 0.2246204765355399,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.48947520983711e-09,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 384.54510895891144,
        "filterflow_gradient_max_abs": 168.66458545141114,
        "gradient_delta": [
          -553.2096944103225,
          32.766609541750725
        ],
        "gradient_explosion_ratio": 2.279939845876484,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 553.2096944103225,
        "relative_gradient_delta": 3.279939845876484,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.252356523513299e-09,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1335.0141249779117,
        "filterflow_gradient_max_abs": 101.15910809775511,
        "gradient_delta": [
          1436.1732330756668,
          -22.93671608039871
        ],
        "gradient_explosion_ratio": 13.197171763197247,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1436.1732330756668,
        "relative_gradient_delta": 14.197171763197247,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.767464479802584e-09,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 171.75344110998785,
        "filterflow_gradient_max_abs": 125.28072286451086,
        "gradient_delta": [
          -212.495802005688,
          171.75344110998785
        ],
        "gradient_explosion_ratio": 1.3709486757650378,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 212.495802005688,
        "relative_gradient_delta": 1.6961572151487254,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9853310934413457e-09,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1115.2851132327878,
        "filterflow_gradient_max_abs": 278.9526477486435,
        "gradient_delta": [
          836.3324654841442,
          -54.29296846486785
        ],
        "gradient_explosion_ratio": 3.998116247449066,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 836.3324654841442,
        "relative_gradient_delta": 2.9981162474490657,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.0152165209074155e-09,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 478.9035536504289,
        "filterflow_gradient_max_abs": 252.28215416061428,
        "gradient_delta": [
          -731.1857078110431,
          225.08691431237906
        ],
        "gradient_explosion_ratio": 1.8982854940486085,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 731.1857078110431,
        "relative_gradient_delta": 2.8982854940486082,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.021582983819826e-09,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2511.464154456364,
        "filterflow_gradient_max_abs": 69.58591013728201,
        "gradient_delta": [
          2441.878244319082,
          11.161703034040576
        ],
        "gradient_explosion_ratio": 36.091561488549075,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2441.878244319082,
        "relative_gradient_delta": 35.091561488549075,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9725839567618095e-09,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2392.0739973047757,
        "filterflow_gradient_max_abs": 64.72471139759364,
        "gradient_delta": [
          2327.349285907182,
          3.178700011881463
        ],
        "gradient_explosion_ratio": 36.95766185206519,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2327.349285907182,
        "relative_gradient_delta": 35.95766185206519,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.974680057832302e-09,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 405.0045735862938,
        "filterflow_gradient_max_abs": 0.6534447816938739,
        "gradient_delta": [
          405.65801836798767,
          69.5096367996552
        ],
        "gradient_explosion_ratio": 405.0045735862938,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 405.65801836798767,
        "relative_gradient_delta": 405.65801836798767,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.903298934597842e-09,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 117.8288447529232,
        "filterflow_gradient_max_abs": 262.5095687458148,
        "gradient_delta": [
          -380.338413498738,
          95.92388611683052
        ],
        "gradient_explosion_ratio": 0.4488554276930591,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 380.338413498738,
        "relative_gradient_delta": 1.448855427693059,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.970814705349767e-09,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 166.84413650312365,
        "filterflow_gradient_max_abs": 28.548993251385596,
        "gradient_delta": [
          32.27608724992828,
          166.84413650312365
        ],
        "gradient_explosion_ratio": 5.8441338030379075,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 166.84413650312365,
        "relative_gradient_delta": 5.8441338030379075,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9090827524669294e-09,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 549.1470950360834,
        "filterflow_gradient_max_abs": 485.70702239538065,
        "gradient_delta": [
          63.440072640702795,
          65.34281774195912
        ],
        "gradient_explosion_ratio": 1.13061386744592,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 65.34281774195912,
        "relative_gradient_delta": 0.13453134241235662,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8526088158287166e-09,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1004.5653107452829,
        "filterflow_gradient_max_abs": 245.11951564783823,
        "gradient_delta": [
          -1249.684826393121,
          229.54701650147175
        ],
        "gradient_explosion_ratio": 4.098267361904125,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1249.684826393121,
        "relative_gradient_delta": 5.098267361904125,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8581510491676454e-09,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2505.8502472212836,
        "filterflow_gradient_max_abs": 434.75519438634416,
        "gradient_delta": [
          2071.0950528349395,
          -5.4968256094107195
        ],
        "gradient_explosion_ratio": 5.763818994177366,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2071.0950528349395,
        "relative_gradient_delta": 4.763818994177367,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9084219477226725e-09,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4679.008764893693,
        "filterflow_gradient_max_abs": 251.90780939902413,
        "gradient_delta": [
          4930.916574292717,
          -48.011933434013194
        ],
        "gradient_explosion_ratio": 18.574290237592844,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4930.916574292717,
        "relative_gradient_delta": 19.574290237592844,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.980804936214554e-09,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6362.001064040937,
        "filterflow_gradient_max_abs": 369.7748801823844,
        "gradient_delta": [
          -6731.775944223322,
          545.8291563512453
        ],
        "gradient_explosion_ratio": 17.205065581802103,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6731.775944223322,
        "relative_gradient_delta": 18.205065581802103,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9715820915043878e-09,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6050.468387045806,
        "filterflow_gradient_max_abs": 153.94165873710156,
        "gradient_delta": [
          -6204.410045782907,
          570.5030753401195
        ],
        "gradient_explosion_ratio": 39.303645528327536,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6204.410045782907,
        "relative_gradient_delta": 40.303645528327536,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.075740551139461e-09,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6855.125102823905,
        "filterflow_gradient_max_abs": 231.88010181357106,
        "gradient_delta": [
          6623.245001010334,
          -56.94669222381985
        ],
        "gradient_explosion_ratio": 29.563231382118964,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6623.245001010334,
        "relative_gradient_delta": 28.563231382118968,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8847040312030003e-09,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9793.829554255753,
        "filterflow_gradient_max_abs": 317.10552544548756,
        "gradient_delta": [
          -10110.935079701241,
          827.7901461600545
        ],
        "gradient_explosion_ratio": 30.885080102268272,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10110.935079701241,
        "relative_gradient_delta": 31.885080102268272,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8788775807697675e-09,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7670.779636408764,
        "filterflow_gradient_max_abs": 440.433114763931,
        "gradient_delta": [
          -8111.212751172696,
          599.3766035426776
        ],
        "gradient_explosion_ratio": 17.416446173717542,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8111.212751172696,
        "relative_gradient_delta": 18.416446173717542,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.7967104188064695e-09,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7304.49517342419,
        "filterflow_gradient_max_abs": 274.3754691050723,
        "gradient_delta": [
          -7030.119704319118,
          552.5900509788953
        ],
        "gradient_explosion_ratio": 26.622260354576117,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7030.119704319118,
        "relative_gradient_delta": 25.622260354576117,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9457680739142234e-09,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4211.564772339335,
        "filterflow_gradient_max_abs": 184.24153726601756,
        "gradient_delta": [
          -4027.3232350733174,
          422.30897221598747
        ],
        "gradient_explosion_ratio": 22.85893200217092,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4027.3232350733174,
        "relative_gradient_delta": 21.85893200217092,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8393571938067907e-09,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2857.0426665638925,
        "filterflow_gradient_max_abs": 187.1386096136716,
        "gradient_delta": [
          -3044.181276177564,
          339.8608251058596
        ],
        "gradient_explosion_ratio": 15.266986713548652,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3044.181276177564,
        "relative_gradient_delta": 16.26698671354865,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.6310544853913598e-09,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4125.3252444345135,
        "filterflow_gradient_max_abs": 954.1501022077981,
        "gradient_delta": [
          -5079.475346642312,
          481.5220478951193
        ],
        "gradient_explosion_ratio": 4.323560029904064,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5079.475346642312,
        "relative_gradient_delta": 5.323560029904065,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.98600263906701e-09,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7940.840121673082,
        "filterflow_gradient_max_abs": 422.91186590476366,
        "gradient_delta": [
          -7517.928255768318,
          617.5111321189985
        ],
        "gradient_explosion_ratio": 18.776583874478696,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7517.928255768318,
        "relative_gradient_delta": 17.776583874478696,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5840096163374255e-09,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5252.357727992092,
        "filterflow_gradient_max_abs": 354.26740709319216,
        "gradient_delta": [
          4898.090320898899,
          -4.424395746512929
        ],
        "gradient_explosion_ratio": 14.825969374626743,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4898.090320898899,
        "relative_gradient_delta": 13.825969374626741,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.941782094647351e-09,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4188.590729336164,
        "filterflow_gradient_max_abs": 199.05378088782396,
        "gradient_delta": [
          3989.5369484483404,
          56.43819823619222
        ],
        "gradient_explosion_ratio": 21.042507761742186,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3989.5369484483404,
        "relative_gradient_delta": 20.042507761742186,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.940716280543711e-09,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3456.203464615118,
        "filterflow_gradient_max_abs": 548.7404094827189,
        "gradient_delta": [
          2907.463055132399,
          126.73180402428642
        ],
        "gradient_explosion_ratio": 6.298430742276074,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2907.463055132399,
        "relative_gradient_delta": 5.298430742276074,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.836934408558591e-09,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2687.331456871495,
        "filterflow_gradient_max_abs": 399.4756572109477,
        "gradient_delta": [
          2287.8557996605473,
          206.2278175022332
        ],
        "gradient_explosion_ratio": 6.727146969689867,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2287.8557996605473,
        "relative_gradient_delta": 5.727146969689867,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.73063721528888e-09,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5543.132677235018,
        "filterflow_gradient_max_abs": 381.20393707705813,
        "gradient_delta": [
          -5161.9287401579595,
          516.5285993818214
        ],
        "gradient_explosion_ratio": 14.541121268940373,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5161.9287401579595,
        "relative_gradient_delta": 13.541121268940373,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.649024276659475e-09,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 982.6438189046636,
        "filterflow_gradient_max_abs": 48.850988576799736,
        "gradient_delta": [
          -1031.4948074814633,
          160.08019908370036
        ],
        "gradient_explosion_ratio": 20.115126582542484,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1031.4948074814633,
        "relative_gradient_delta": 21.115126582542484,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.737742642646481e-09,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 232.0740468309279,
        "filterflow_gradient_max_abs": 346.85073969207997,
        "gradient_delta": [
          -114.77669286115207,
          194.0939857671775
        ],
        "gradient_explosion_ratio": 0.6690890930114602,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 194.0939857671775,
        "relative_gradient_delta": 0.5595893667099752,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.721428581433429e-09,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6220.07213003388,
        "filterflow_gradient_max_abs": 322.6295207830076,
        "gradient_delta": [
          6542.701650816887,
          32.0648803845651
        ],
        "gradient_explosion_ratio": 19.279302510625932,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6542.701650816887,
        "relative_gradient_delta": 20.279302510625932,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6360639771592105e-09,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3775.1059564394286,
        "filterflow_gradient_max_abs": 86.66552831338745,
        "gradient_delta": [
          3861.771484752816,
          152.6958593377608
        ],
        "gradient_explosion_ratio": 43.55948702912687,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3861.771484752816,
        "relative_gradient_delta": 44.55948702912687,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.636163453142217e-09,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1790.1703583963604,
        "filterflow_gradient_max_abs": 1118.3947944525503,
        "gradient_delta": [
          671.7755639438101,
          236.1127404290799
        ],
        "gradient_explosion_ratio": 1.6006604888326947,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 671.7755639438101,
        "relative_gradient_delta": 0.6006604888326948,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9218832625920186e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4849.997803602566,
        "filterflow_gradient_max_abs": 72.987643547552,
        "gradient_delta": [
          4777.010160055014,
          132.99091149585826
        ],
        "gradient_explosion_ratio": 66.44957376165674,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4777.010160055014,
        "relative_gradient_delta": 65.44957376165674,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9393910356011475e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10387.61025051468,
        "filterflow_gradient_max_abs": 7.513193750877159,
        "gradient_delta": [
          10380.097056763801,
          -177.63206825906838
        ],
        "gradient_explosion_ratio": 1382.582506846963,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10380.097056763801,
        "relative_gradient_delta": 1381.5825068469628,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.889368827003636e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6782.033157155527,
        "filterflow_gradient_max_abs": 330.52600026078443,
        "gradient_delta": [
          6451.507156894742,
          4.161197061283189
        ],
        "gradient_explosion_ratio": 20.51890971301657,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6451.507156894742,
        "relative_gradient_delta": 19.51890971301657,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.899515377270291e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5334.90542955874,
        "filterflow_gradient_max_abs": 286.4569368626525,
        "gradient_delta": [
          5048.448492696088,
          168.11101805942343
        ],
        "gradient_explosion_ratio": 18.623760653129747,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5048.448492696088,
        "relative_gradient_delta": 17.623760653129747,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.8836134308439796e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7717.819345385175,
        "filterflow_gradient_max_abs": 609.6787100623405,
        "gradient_delta": [
          7108.140635322835,
          105.07866900108557
        ],
        "gradient_explosion_ratio": 12.658830328183868,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7108.140635322835,
        "relative_gradient_delta": 11.658830328183868,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.874831122629985e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8898.775124555641,
        "filterflow_gradient_max_abs": 237.18680047332637,
        "gradient_delta": [
          8661.588324082315,
          18.016905416609358
        ],
        "gradient_explosion_ratio": 37.51800313844354,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8661.588324082315,
        "relative_gradient_delta": 36.51800313844355,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.782176349886868e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7158.324790720362,
        "filterflow_gradient_max_abs": 20.398532585564105,
        "gradient_delta": [
          7178.723323305926,
          114.99131482701813
        ],
        "gradient_explosion_ratio": 350.92351671346483,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7178.723323305926,
        "relative_gradient_delta": 351.92351671346483,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.6820893001277e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 805.0043558971045,
        "filterflow_gradient_max_abs": 478.6428510468603,
        "gradient_delta": [
          326.36150485024416,
          432.7948145396345
        ],
        "gradient_explosion_ratio": 1.6818476534987308,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 432.7948145396345,
        "relative_gradient_delta": 0.9042124281038574,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.958078309551638e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 984.9321379100702,
        "filterflow_gradient_max_abs": 310.27237965253573,
        "gradient_delta": [
          -1295.2045175626058,
          443.10039252165336
        ],
        "gradient_explosion_ratio": 3.1744112673292566,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1295.2045175626058,
        "relative_gradient_delta": 4.174411267329257,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.521620328683639e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 726.016615465453,
        "filterflow_gradient_max_abs": 291.33394004387503,
        "gradient_delta": [
          434.682675421578,
          412.66260440105515
        ],
        "gradient_explosion_ratio": 2.4920426894172185,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 434.682675421578,
        "relative_gradient_delta": 1.4920426894172185,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.524789349285129e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3712.495457641089,
        "filterflow_gradient_max_abs": 772.789629727978,
        "gradient_delta": [
          2939.705827913111,
          405.9845575459273
        ],
        "gradient_explosion_ratio": 4.804018215083823,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2939.705827913111,
        "relative_gradient_delta": 3.804018215083823,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.415127818901965e-09,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 619.4015323128731,
        "filterflow_gradient_max_abs": 137.0827775975205,
        "gradient_delta": [
          -756.4843099103936,
          420.15636726372
        ],
        "gradient_explosion_ratio": 4.518448948645148,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 756.4843099103936,
        "relative_gradient_delta": 5.518448948645148,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.988418484368594e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1337.0505654721733,
        "filterflow_gradient_max_abs": 205.40967733109431,
        "gradient_delta": [
          1131.640888141079,
          312.3521976987116
        ],
        "gradient_explosion_ratio": 6.5091897462894,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1131.640888141079,
        "relative_gradient_delta": 5.509189746289399,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.800110448537453e-09,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1355.3581509211456,
        "filterflow_gradient_max_abs": 1075.2940301638955,
        "gradient_delta": [
          280.06412075725007,
          425.2174251356866
        ],
        "gradient_explosion_ratio": 1.2604535251763305,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 425.2174251356866,
        "relative_gradient_delta": 0.39544293300956507,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.299266720408923e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3182.1764363714087,
        "filterflow_gradient_max_abs": 1320.7702359098546,
        "gradient_delta": [
          1861.4062004615541,
          501.0385057077531
        ],
        "gradient_explosion_ratio": 2.4093338491832874,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1861.4062004615541,
        "relative_gradient_delta": 1.4093338491832876,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.148105858803319e-09,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13674.271006822335,
        "filterflow_gradient_max_abs": 352.8826174689448,
        "gradient_delta": [
          13321.38838935339,
          30.980599869041384
        ],
        "gradient_explosion_ratio": 38.7501971757669,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13321.38838935339,
        "relative_gradient_delta": 37.7501971757669,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.5889797800336964e-09,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10488.7014516074,
        "filterflow_gradient_max_abs": 974.6366511077524,
        "gradient_delta": [
          9514.064800499647,
          117.17616024266344
        ],
        "gradient_explosion_ratio": 10.761653011597863,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9514.064800499647,
        "relative_gradient_delta": 9.761653011597863,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.8240451633319026e-09,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9385.831748016011,
        "filterflow_gradient_max_abs": 731.310897142959,
        "gradient_delta": [
          8654.520850873052,
          191.8583292379634
        ],
        "gradient_explosion_ratio": 12.834256654295743,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8654.520850873052,
        "relative_gradient_delta": 11.834256654295743,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.972274953412125e-09,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 15989.516594743414,
        "filterflow_gradient_max_abs": 483.3559108394908,
        "gradient_delta": [
          -16472.872505582905,
          1296.110591344409
        ],
        "gradient_explosion_ratio": 33.08021322625988,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 16472.872505582905,
        "relative_gradient_delta": 34.08021322625988,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.955818783651921e-09,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 15882.807545819702,
        "filterflow_gradient_max_abs": 1076.6780654517022,
        "gradient_delta": [
          -16959.485611271404,
          1367.0163032102953
        ],
        "gradient_explosion_ratio": 14.751677456302907,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 16959.485611271404,
        "relative_gradient_delta": 15.751677456302907,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5558010697277496e-09,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 21718.637256553102,
        "filterflow_gradient_max_abs": 18.05494027199655,
        "gradient_delta": [
          21700.582316281107,
          -278.8973886880421
        ],
        "gradient_explosion_ratio": 1202.919363307947,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 21700.582316281107,
        "relative_gradient_delta": 1201.9193633079472,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6730690428375965e-09,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8212.83659671928,
        "filterflow_gradient_max_abs": 989.4278480713913,
        "gradient_delta": [
          -9202.264444790671,
          1130.2064462029718
        ],
        "gradient_explosion_ratio": 8.30059171341081,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9202.264444790671,
        "relative_gradient_delta": 9.30059171341081,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.355683813628275e-09,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2722.2459329881885,
        "filterflow_gradient_max_abs": 778.7073741209738,
        "gradient_delta": [
          -3500.9533071091623,
          915.7855832436946
        ],
        "gradient_explosion_ratio": 3.495852259086585,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3500.9533071091623,
        "relative_gradient_delta": 4.495852259086584,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.821792577378801e-09,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 16225.006881085854,
        "filterflow_gradient_max_abs": 1097.9215016104433,
        "gradient_delta": [
          15127.085379475411,
          305.1003893801726
        ],
        "gradient_explosion_ratio": 14.777929803985836,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 15127.085379475411,
        "relative_gradient_delta": 13.777929803985836,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0083482493428164e-08,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5494.985956135951,
        "filterflow_gradient_max_abs": 1697.7646785016034,
        "gradient_delta": [
          -7192.750634637554,
          1261.0397776110385
        ],
        "gradient_explosion_ratio": 3.236600469851724,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7192.750634637554,
        "relative_gradient_delta": 4.236600469851724,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8990448324984754e-08,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 12945.04083276385,
        "filterflow_gradient_max_abs": 947.0739014815089,
        "gradient_delta": [
          -13892.114734245359,
          1494.772177770885
        ],
        "gradient_explosion_ratio": 13.668459042651167,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13892.114734245359,
        "relative_gradient_delta": 14.668459042651167,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1565390423129429e-08,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13391.075704762878,
        "filterflow_gradient_max_abs": 249.89093531615012,
        "gradient_delta": [
          13141.184769446727,
          523.382554719984
        ],
        "gradient_explosion_ratio": 53.58768091295959,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13141.184769446727,
        "relative_gradient_delta": 52.58768091295959,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.132605782724568e-09,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 18159.045571100523,
        "filterflow_gradient_max_abs": 974.2890696675929,
        "gradient_delta": [
          -19133.334640768117,
          1540.302753010614
        ],
        "gradient_explosion_ratio": 18.638252379548927,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 19133.334640768117,
        "relative_gradient_delta": 19.638252379548927,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.223679515140248e-09,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 26760.666127724486,
        "filterflow_gradient_max_abs": 1029.3299119039873,
        "gradient_delta": [
          25731.3362158205,
          607.0450579833731
        ],
        "gradient_explosion_ratio": 25.99814288717633,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 25731.3362158205,
        "relative_gradient_delta": 24.99814288717633,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.178016403486254e-09,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7809.771345322588,
        "filterflow_gradient_max_abs": 1426.254117759735,
        "gradient_delta": [
          -9236.025463082322,
          1273.7922166333456
        ],
        "gradient_explosion_ratio": 5.475722206916154,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9236.025463082322,
        "relative_gradient_delta": 6.475722206916153,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.153612730486202e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 37888.977721303076,
        "filterflow_gradient_max_abs": 1942.7454564725651,
        "gradient_delta": [
          35946.23226483051,
          187.684761020645
        ],
        "gradient_explosion_ratio": 19.50280084046519,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 35946.23226483051,
        "relative_gradient_delta": 18.50280084046519,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.01524527357833e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 44953.78745271879,
        "filterflow_gradient_max_abs": 169.06130724664092,
        "gradient_delta": [
          45122.84875996543,
          -233.6034417737789
        ],
        "gradient_explosion_ratio": 265.9022823426794,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 45122.84875996543,
        "relative_gradient_delta": 266.9022823426794,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.081496278260602e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 11065.833774850853,
        "filterflow_gradient_max_abs": 1963.5208371745916,
        "gradient_delta": [
          -13029.354612025445,
          1671.3168688932124
        ],
        "gradient_explosion_ratio": 5.635709876536902,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13029.354612025445,
        "relative_gradient_delta": 6.635709876536903,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.653859933678177e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 11741.577377545855,
        "filterflow_gradient_max_abs": 1119.9768301540837,
        "gradient_delta": [
          -12861.554207699939,
          1761.980775094222
        ],
        "gradient_explosion_ratio": 10.48376811146216,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 12861.554207699939,
        "relative_gradient_delta": 11.483768111462162,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.3080741458397824e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1142.275997654743,
        "filterflow_gradient_max_abs": 979.6868013870265,
        "gradient_delta": [
          -1499.1184940117446,
          1142.275997654743
        ],
        "gradient_explosion_ratio": 1.165960382478895,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1499.1184940117446,
        "relative_gradient_delta": 1.530201786825457,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.394845624730806e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 34194.81526137903,
        "filterflow_gradient_max_abs": 2882.4178802677957,
        "gradient_delta": [
          31312.397381111234,
          650.9159412180402
        ],
        "gradient_explosion_ratio": 11.863240058100843,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 31312.397381111234,
        "relative_gradient_delta": 10.86324005810084,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.620751946684322e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 36450.83309317907,
        "filterflow_gradient_max_abs": 858.8073873147812,
        "gradient_delta": [
          35592.02570586429,
          589.2857185007799
        ],
        "gradient_explosion_ratio": 42.443548613559656,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 35592.02570586429,
        "relative_gradient_delta": 41.443548613559656,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.615852837261627e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 21970.40349853083,
        "filterflow_gradient_max_abs": 442.0116504772855,
        "gradient_delta": [
          -22412.415149008117,
          2375.6265753267444
        ],
        "gradient_explosion_ratio": 49.70548508123513,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 22412.415149008117,
        "relative_gradient_delta": 50.70548508123513,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.274422841874184e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 22463.381965171266,
        "filterflow_gradient_max_abs": 3282.5855155180925,
        "gradient_delta": [
          -25745.96748068936,
          2680.3556553257727
        ],
        "gradient_explosion_ratio": 6.84319779605981,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 25745.96748068936,
        "relative_gradient_delta": 7.84319779605981,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0136062655874412e-08,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 22071.066724293047,
        "filterflow_gradient_max_abs": 1855.9144036285215,
        "gradient_delta": [
          -23926.98112792157,
          2685.5533226818866
        ],
        "gradient_explosion_ratio": 11.892286994023877,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 23926.98112792157,
        "relative_gradient_delta": 12.892286994023877,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.873637741795392e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9841.678061116465,
        "filterflow_gradient_max_abs": 1310.8611477302254,
        "gradient_delta": [
          -11152.53920884669,
          2274.9695203134556
        ],
        "gradient_explosion_ratio": 7.5077959844621756,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 11152.53920884669,
        "relative_gradient_delta": 8.507795984462176,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.93335175330867e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4441.41261065634,
        "filterflow_gradient_max_abs": 914.416967723082,
        "gradient_delta": [
          -5355.829578379422,
          2181.252550277817
        ],
        "gradient_explosion_ratio": 4.857097765492643,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5355.829578379422,
        "relative_gradient_delta": 5.857097765492643,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.058265166255296e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2258.0912248515788,
        "filterflow_gradient_max_abs": 3551.3298618369327,
        "gradient_delta": [
          -2239.033957982696,
          2258.0912248515788
        ],
        "gradient_explosion_ratio": 0.6358438423637663,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2258.0912248515788,
        "relative_gradient_delta": 0.6358438423637663,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.786315675024525e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13160.309545607119,
        "filterflow_gradient_max_abs": 3023.0985131010166,
        "gradient_delta": [
          10137.211032506102,
          2057.991295978962
        ],
        "gradient_explosion_ratio": 4.353251966012716,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10137.211032506102,
        "relative_gradient_delta": 3.353251966012716,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.745331570025883e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 23034.69584439991,
        "filterflow_gradient_max_abs": 2001.070628323309,
        "gradient_delta": [
          21033.6252160766,
          1134.4408898516208
        ],
        "gradient_explosion_ratio": 11.511185821412317,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 21033.6252160766,
        "relative_gradient_delta": 10.511185821412317,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.205052720062668e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 19217.15647794509,
        "filterflow_gradient_max_abs": 2346.9001573329506,
        "gradient_delta": [
          16870.256320612138,
          1743.3894817123073
        ],
        "gradient_explosion_ratio": 8.188314452960679,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 16870.256320612138,
        "relative_gradient_delta": 7.188314452960678,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.456598728414974e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 28106.471905675186,
        "filterflow_gradient_max_abs": 4046.6212127655212,
        "gradient_delta": [
          24059.850692909666,
          1582.3227329585068
        ],
        "gradient_explosion_ratio": 6.945664154828765,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 24059.850692909666,
        "relative_gradient_delta": 5.945664154828765,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.6329352092725458e-08,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 18935.685049166474,
        "filterflow_gradient_max_abs": 2730.4139020142047,
        "gradient_delta": [
          16205.271147152269,
          2073.5151589713964
        ],
        "gradient_explosion_ratio": 6.935096922557334,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 16205.271147152269,
        "relative_gradient_delta": 5.935096922557334,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.300094916397939e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_with_clipped_upstream_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      2877.6722404002735,
      2764.9054584793257
    ],
    "final_bayesfilter_gradient_max_abs": 2877.6722404002735,
    "final_filterflow_gradient_diag": [
      18935.6850725171,
      2073.5151524806142
    ],
    "final_filterflow_gradient_max_abs": 18935.6850725171,
    "final_gradient_delta": [
      -16058.012832116825,
      691.3903059987115
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 16058.012832116825,
    "final_relative_gradient_delta": 0.8480291455323751,
    "final_scalar_delta": 9.3001517598168e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "status": "no_explosion"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 0.9938843426030545,
      "max_abs_gradient_delta": 0.05381790412059573,
      "relative_gradient_delta": 0.006115657396945523,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.7926993223227328e-11,
      "status": "failure",
      "time_index": 1,
      "transport_status": "computed_transport_matrix_stop_gradient"
    },
    "first_scalar_failure": {
      "status": "no_failure"
    },
    "mode": "transport_matrix_stop_gradient",
    "mode_description": "Stop gradient through transport matrix only",
    "sample_rows": [
      {
        "bayesfilter_gradient_max_abs": 0.008913771203554865,
        "filterflow_gradient_max_abs": 0.008913771203554867,
        "gradient_delta": [
          -1.734723475976807e-18,
          -5.766308833278761e-19
        ],
        "gradient_explosion_ratio": 0.008913771203554865,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 1.734723475976807e-18,
        "relative_gradient_delta": 1.734723475976807e-18,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.746201558623538,
        "filterflow_gradient_max_abs": 8.800019462744133,
        "gradient_delta": [
          0.05381790412059573,
          -0.031075280934558604
        ],
        "gradient_explosion_ratio": 0.9938843426030545,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.05381790412059573,
        "relative_gradient_delta": 0.006115657396945523,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7926993223227328e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.149098814003055,
        "filterflow_gradient_max_abs": 1.4485716238559057,
        "gradient_delta": [
          -6.597670437858961,
          -1.4867410767286051
        ],
        "gradient_explosion_ratio": 3.5546042247443976,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.597670437858961,
        "relative_gradient_delta": 4.554604224744398,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4985346297180513e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 11.809944772020398,
        "filterflow_gradient_max_abs": 16.840076774872443,
        "gradient_delta": [
          -12.464430175451419,
          11.809944772020398
        ],
        "gradient_explosion_ratio": 0.7012999364493606,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 12.464430175451419,
        "relative_gradient_delta": 0.7401646882067633,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.4439117396468646e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.923200395673119,
        "filterflow_gradient_max_abs": 11.278780998887767,
        "gradient_delta": [
          10.997688886565177,
          8.923200395673119
        ],
        "gradient_explosion_ratio": 0.7911493623781738,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10.997688886565177,
        "relative_gradient_delta": 0.9750777932162785,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.665601073204016e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.041837594757622,
        "filterflow_gradient_max_abs": 0.16051708831084313,
        "gradient_delta": [
          -0.4102776502334051,
          9.041837594757622
        ],
        "gradient_explosion_ratio": 9.041837594757622,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.041837594757622,
        "relative_gradient_delta": 9.041837594757622,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.347366828165832e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10.009357422880136,
        "filterflow_gradient_max_abs": 6.732984884221974,
        "gradient_delta": [
          -5.941953615899251,
          10.009357422880136
        ],
        "gradient_explosion_ratio": 1.486615163259313,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10.009357422880136,
        "relative_gradient_delta": 1.486615163259313,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.53681536782824e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.679846888075318,
        "filterflow_gradient_max_abs": 16.75562828027451,
        "gradient_delta": [
          15.087028092995498,
          7.679846888075318
        ],
        "gradient_explosion_ratio": 0.45834431031848466,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 15.087028092995498,
        "relative_gradient_delta": 0.9004155404161499,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.6477489351891563e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.794806450589656,
        "filterflow_gradient_max_abs": 8.578663144440544,
        "gradient_delta": [
          -9.384580534907144,
          8.794806450589656
        ],
        "gradient_explosion_ratio": 1.0251954532436893,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.384580534907144,
        "relative_gradient_delta": 1.0939444033291923,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.839595473844383e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13.839381451226782,
        "filterflow_gradient_max_abs": 56.8762754108451,
        "gradient_delta": [
          -52.032299907006944,
          13.839381451226783
        ],
        "gradient_explosion_ratio": 0.24332432725698322,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 52.032299907006944,
        "relative_gradient_delta": 0.9148331097835124,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.645795108146558e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 24.291289919299523,
        "filterflow_gradient_max_abs": 104.45156511568617,
        "gradient_delta": [
          -87.1949410703737,
          24.291289919299523
        ],
        "gradient_explosion_ratio": 0.23256032489695594,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 87.1949410703737,
        "relative_gradient_delta": 0.8347882674022189,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.562661608062626e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 23.427881452483206,
        "filterflow_gradient_max_abs": 9.13071410440192,
        "gradient_delta": [
          25.170861986782732,
          23.427881452483206
        ],
        "gradient_explosion_ratio": 2.5658323308128352,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 25.170861986782732,
        "relative_gradient_delta": 2.7567243590123858,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.412914561020443e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 30.310566751863462,
        "filterflow_gradient_max_abs": 62.46161279976278,
        "gradient_delta": [
          -40.068428775688204,
          30.310566751863462
        ],
        "gradient_explosion_ratio": 0.4852671167654924,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 40.068428775688204,
        "relative_gradient_delta": 0.6414888597919838,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.171952003976912e-11,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 37.55190654747693,
        "filterflow_gradient_max_abs": 78.21898890138324,
        "gradient_delta": [
          -47.638395773909494,
          37.55190654747693
        ],
        "gradient_explosion_ratio": 0.4800868315342396,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 47.638395773909494,
        "relative_gradient_delta": 0.6090387569950684,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1748113593057496e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 42.89399827745065,
        "filterflow_gradient_max_abs": 55.1203162059954,
        "gradient_delta": [
          -19.127671939795682,
          42.89399827745065
        ],
        "gradient_explosion_ratio": 0.7781885379094595,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 42.89399827745065,
        "relative_gradient_delta": 0.7781885379094595,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1169021263413015e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 43.23484482234133,
        "filterflow_gradient_max_abs": 3.2014311273644616,
        "gradient_delta": [
          33.074559535472716,
          43.23484482234133
        ],
        "gradient_explosion_ratio": 13.504849269687048,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 43.23484482234133,
        "relative_gradient_delta": 13.504849269687048,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.603695616533514e-11,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 45.39786134393227,
        "filterflow_gradient_max_abs": 25.054390338542845,
        "gradient_delta": [
          13.27872047774133,
          45.39786134393227
        ],
        "gradient_explosion_ratio": 1.8119723022792418,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 45.39786134393227,
        "relative_gradient_delta": 1.8119723022792418,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1939249588976963e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 55.81357256119132,
        "filterflow_gradient_max_abs": 145.3600680670563,
        "gradient_delta": [
          -96.07346356426123,
          55.81357256119132
        ],
        "gradient_explosion_ratio": 0.3839677106882192,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 96.07346356426123,
        "relative_gradient_delta": 0.6609343600468144,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.48947520983711e-09,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 68.24852083592695,
        "filterflow_gradient_max_abs": 168.66458545141114,
        "gradient_delta": [
          -105.30388584320553,
          68.24852083592695
        ],
        "gradient_explosion_ratio": 0.4046404919756434,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 105.30388584320553,
        "relative_gradient_delta": 0.6243390428486925,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.252356523513299e-09,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 59.994084323348446,
        "filterflow_gradient_max_abs": 101.15910809775511,
        "gradient_delta": [
          155.81869866980074,
          59.994084323348446
        ],
        "gradient_explosion_ratio": 0.5930665607032949,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 155.81869866980074,
        "relative_gradient_delta": 1.5403328637419909,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.767464479802584e-09,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 69.42880118631346,
        "filterflow_gradient_max_abs": 125.28072286451086,
        "gradient_delta": [
          -62.09242099100873,
          69.42880118631346
        ],
        "gradient_explosion_ratio": 0.5541858284246941,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 69.42880118631346,
        "relative_gradient_delta": 0.5541858284246941,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9853310934413457e-09,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 86.24566993616499,
        "filterflow_gradient_max_abs": 278.9526477486435,
        "gradient_delta": [
          -196.01381862438478,
          86.24566993616499
        ],
        "gradient_explosion_ratio": 0.30917673889182284,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 196.01381862438478,
        "relative_gradient_delta": 0.7026777490959949,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.0152165209074155e-09,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 104.06851444259586,
        "filterflow_gradient_max_abs": 252.28215416061428,
        "gradient_delta": [
          -149.69469476252436,
          104.06851444259586
        ],
        "gradient_explosion_ratio": 0.41250842648323477,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 149.69469476252436,
        "relative_gradient_delta": 0.5933622029690689,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.021582983819826e-09,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 109.25297856316739,
        "filterflow_gradient_max_abs": 69.58591013728201,
        "gradient_delta": [
          38.46325476847757,
          109.25297856316739
        ],
        "gradient_explosion_ratio": 1.5700445441847137,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 109.25297856316739,
        "relative_gradient_delta": 1.5700445441847137,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9725839567618095e-09,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 114.03857152579974,
        "filterflow_gradient_max_abs": 64.72471139759364,
        "gradient_delta": [
          48.05744775264644,
          114.03857152579974
        ],
        "gradient_explosion_ratio": 1.7619015838522458,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 114.03857152579974,
        "relative_gradient_delta": 1.7619015838522458,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.974680057832302e-09,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 114.0875104766665,
        "filterflow_gradient_max_abs": 0.6534447816938739,
        "gradient_delta": [
          113.38489366367135,
          114.0875104766665
        ],
        "gradient_explosion_ratio": 114.0875104766665,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 114.0875104766665,
        "relative_gradient_delta": 114.0875104766665,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.903298934597842e-09,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 129.77729631167466,
        "filterflow_gradient_max_abs": 262.5095687458148,
        "gradient_delta": [
          -134.0038792316894,
          129.77729631167466
        ],
        "gradient_explosion_ratio": 0.4943716792180502,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 134.0038792316894,
        "relative_gradient_delta": 0.5104723605768593,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.970814705349767e-09,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 131.4506125932156,
        "filterflow_gradient_max_abs": 28.548993251385596,
        "gradient_delta": [
          101.70491094093565,
          131.4506125932156
        ],
        "gradient_explosion_ratio": 4.604386972098772,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 131.4506125932156,
        "relative_gradient_delta": 4.604386972098772,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9090827524669294e-09,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 159.622092399649,
        "filterflow_gradient_max_abs": 485.70702239538065,
        "gradient_delta": [
          -327.44982265251355,
          159.622092399649
        ],
        "gradient_explosion_ratio": 0.32863863407293226,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 327.44982265251355,
        "relative_gradient_delta": 0.6741714810661296,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8526088158287166e-09,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 174.42891263489247,
        "filterflow_gradient_max_abs": 245.11951564783823,
        "gradient_delta": [
          -70.69060301294576,
          173.80285083621064
        ],
        "gradient_explosion_ratio": 0.7116076097567583,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 173.80285083621064,
        "relative_gradient_delta": 0.7090535014189249,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8581510491676454e-09,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 201.1610313437098,
        "filterflow_gradient_max_abs": 434.75519438634416,
        "gradient_delta": [
          -233.59416304263436,
          200.1763632979281
        ],
        "gradient_explosion_ratio": 0.4626995466440558,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 233.59416304263436,
        "relative_gradient_delta": 0.5373004533559442,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9084219477226725e-09,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 184.7554684353428,
        "filterflow_gradient_max_abs": 251.90780939902413,
        "gradient_delta": [
          436.33687735516173,
          184.7554684353428
        ],
        "gradient_explosion_ratio": 0.7334249338125464,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 436.33687735516173,
        "relative_gradient_delta": 1.7321292197972329,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.980804936214554e-09,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 206.97041533957906,
        "filterflow_gradient_max_abs": 369.7748801823844,
        "gradient_delta": [
          -165.14155461695185,
          206.97041533957906
        ],
        "gradient_explosion_ratio": 0.5597200524748865,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 206.97041533957906,
        "relative_gradient_delta": 0.5597200524748865,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9715820915043878e-09,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 214.7977092619848,
        "filterflow_gradient_max_abs": 153.94165873710156,
        "gradient_delta": [
          59.60470799825222,
          214.7977092619848
        ],
        "gradient_explosion_ratio": 1.3953189216234962,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 214.7977092619848,
        "relative_gradient_delta": 1.3953189216234962,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.075740551139461e-09,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 228.01168642736354,
        "filterflow_gradient_max_abs": 231.88010181357106,
        "gradient_delta": [
          -5.572431570132409,
          228.01168642736354
        ],
        "gradient_explosion_ratio": 0.983317174022471,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 228.01168642736354,
        "relative_gradient_delta": 0.983317174022471,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8847040312030003e-09,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 244.2940843876757,
        "filterflow_gradient_max_abs": 317.10552544548756,
        "gradient_delta": [
          -73.5015508298855,
          244.2940843876757
        ],
        "gradient_explosion_ratio": 0.77038734674988,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 244.2940843876757,
        "relative_gradient_delta": 0.77038734674988,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8788775807697675e-09,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 267.60842451467033,
        "filterflow_gradient_max_abs": 440.433114763931,
        "gradient_delta": [
          -172.82469024926064,
          267.37574157989013
        ],
        "gradient_explosion_ratio": 0.6076028698661919,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 267.37574157989013,
        "relative_gradient_delta": 0.6070745650521797,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.7967104188064695e-09,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 252.82054885204843,
        "filterflow_gradient_max_abs": 274.3754691050723,
        "gradient_delta": [
          526.6686496771732,
          252.82054885204843
        ],
        "gradient_explosion_ratio": 0.921440060500564,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 526.6686496771732,
        "relative_gradient_delta": 1.9195179926070034,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9457680739142234e-09,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 243.33045952959094,
        "filterflow_gradient_max_abs": 184.24153726601756,
        "gradient_delta": [
          427.57199679560847,
          243.18370700872168
        ],
        "gradient_explosion_ratio": 1.3207144444211714,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 427.57199679560847,
        "relative_gradient_delta": 2.320714444421171,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8393571938067907e-09,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 251.36321213006212,
        "filterflow_gradient_max_abs": 187.1386096136716,
        "gradient_delta": [
          64.22460251639052,
          251.2141645739261
        ],
        "gradient_explosion_ratio": 1.3431926882911849,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 251.2141645739261,
        "relative_gradient_delta": 1.3423962328913948,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.6310544853913598e-09,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 292.2977104754542,
        "filterflow_gradient_max_abs": 954.1501022077981,
        "gradient_delta": [
          -661.8523917323439,
          290.2459790107884
        ],
        "gradient_explosion_ratio": 0.3063435300159897,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 661.8523917323439,
        "relative_gradient_delta": 0.6936564699840103,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.98600263906701e-09,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 272.1979952861001,
        "filterflow_gradient_max_abs": 422.91186590476366,
        "gradient_delta": [
          694.4431866310783,
          272.1979952861001
        ],
        "gradient_explosion_ratio": 0.6436281817341982,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 694.4431866310783,
        "relative_gradient_delta": 1.642051790496371,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5840096163374255e-09,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 288.99332352288735,
        "filterflow_gradient_max_abs": 354.26740709319216,
        "gradient_delta": [
          -68.07700122625198,
          288.99332352288735
        ],
        "gradient_explosion_ratio": 0.8157491141906428,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 288.99332352288735,
        "relative_gradient_delta": 0.8157491141906428,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.941782094647351e-09,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 296.5245795139857,
        "filterflow_gradient_max_abs": 199.05378088782396,
        "gradient_delta": [
          95.7000973664289,
          296.5245795139857
        ],
        "gradient_explosion_ratio": 1.4896706718727994,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 296.5245795139857,
        "relative_gradient_delta": 1.4896706718727994,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.940716280543711e-09,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 320.31626457956855,
        "filterflow_gradient_max_abs": 548.7404094827189,
        "gradient_delta": [
          -230.52509637363846,
          320.31626457956855
        ],
        "gradient_explosion_ratio": 0.5837300462007547,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 320.31626457956855,
        "relative_gradient_delta": 0.5837300462007547,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.836934408558591e-09,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 336.9467886734296,
        "filterflow_gradient_max_abs": 399.4756572109477,
        "gradient_delta": [
          -63.163623179836975,
          336.9467886734296
        ],
        "gradient_explosion_ratio": 0.8434726436797648,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 336.9467886734296,
        "relative_gradient_delta": 0.8434726436797648,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.73063721528888e-09,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 320.05526302877314,
        "filterflow_gradient_max_abs": 381.20393707705813,
        "gradient_delta": [
          700.340717618699,
          320.05526302877314
        ],
        "gradient_explosion_ratio": 0.8395906545007059,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 700.340717618699,
        "relative_gradient_delta": 1.837181228999556,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.649024276659475e-09,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 322.2663531443124,
        "filterflow_gradient_max_abs": 48.850988576799736,
        "gradient_delta": [
          272.17959093209305,
          322.2663531443124
        ],
        "gradient_explosion_ratio": 6.596925927868793,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 322.2663531443124,
        "relative_gradient_delta": 6.596925927868793,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.737742642646481e-09,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 334.9123073921131,
        "filterflow_gradient_max_abs": 346.85073969207997,
        "gradient_delta": [
          -12.636519848020612,
          334.9123073921131
        ],
        "gradient_explosion_ratio": 0.965580490586339,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 334.9123073921131,
        "relative_gradient_delta": 0.965580490586339,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.721428581433429e-09,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 322.74538986094063,
        "filterflow_gradient_max_abs": 322.6295207830076,
        "gradient_delta": [
          644.2484273613738,
          322.74538986094063
        ],
        "gradient_explosion_ratio": 1.0003591397267424,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 644.2484273613738,
        "relative_gradient_delta": 1.9968675705738625,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6360639771592105e-09,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 319.61100597728154,
        "filterflow_gradient_max_abs": 86.66552831338745,
        "gradient_delta": [
          405.3327682831849,
          319.61100597728154
        ],
        "gradient_explosion_ratio": 3.6878677393109527,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 405.3327682831849,
        "relative_gradient_delta": 4.676977988497096,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.636163453142217e-09,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 354.0045005679045,
        "filterflow_gradient_max_abs": 1118.3947944525503,
        "gradient_delta": [
          -764.3902938846459,
          353.7974618326244
        ],
        "gradient_explosion_ratio": 0.3165291025350205,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 764.3902938846459,
        "relative_gradient_delta": 0.6834708974649796,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9218832625920186e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 356.87067913083536,
        "filterflow_gradient_max_abs": 72.987643547552,
        "gradient_delta": [
          283.88303558328334,
          356.206718699828
        ],
        "gradient_explosion_ratio": 4.889467062987606,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 356.206718699828,
        "relative_gradient_delta": 4.880370174819477,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9393910356011475e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 357.1217816778358,
        "filterflow_gradient_max_abs": 7.513193750877159,
        "gradient_delta": [
          349.60858792695865,
          356.563140624348
        ],
        "gradient_explosion_ratio": 47.5326197512399,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 356.563140624348,
        "relative_gradient_delta": 47.45826507970989,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.889368827003636e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 368.74001827047255,
        "filterflow_gradient_max_abs": 330.52600026078443,
        "gradient_delta": [
          38.21401800968812,
          367.74851479082145
        ],
        "gradient_explosion_ratio": 1.1156157699531575,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 367.74851479082145,
        "relative_gradient_delta": 1.112615995415394,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.899515377270291e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 379.0704884198165,
        "filterflow_gradient_max_abs": 286.4569368626525,
        "gradient_delta": [
          92.61355155716399,
          377.7271706222986
        ],
        "gradient_explosion_ratio": 1.3233070651787686,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 377.7271706222986,
        "relative_gradient_delta": 1.3186176420067195,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.8836134308439796e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 401.1412474905192,
        "filterflow_gradient_max_abs": 609.6787100623405,
        "gradient_delta": [
          -208.53746257182132,
          398.8269069888204
        ],
        "gradient_explosion_ratio": 0.6579551505898934,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 398.8269069888204,
        "relative_gradient_delta": 0.6541591503958532,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.874831122629985e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 410.74072841116964,
        "filterflow_gradient_max_abs": 237.18680047332637,
        "gradient_delta": [
          173.55392793784327,
          407.94897805265435
        ],
        "gradient_explosion_ratio": 1.7317183232435434,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 407.94897805265435,
        "relative_gradient_delta": 1.7199480630395856,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.782176349886868e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 409.9239260884323,
        "filterflow_gradient_max_abs": 20.398532585564105,
        "gradient_delta": [
          430.32245867399644,
          407.30628952294444
        ],
        "gradient_explosion_ratio": 20.095755631879744,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 430.32245867399644,
        "relative_gradient_delta": 21.095755631879744,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.6820893001277e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 427.4352410302137,
        "filterflow_gradient_max_abs": 478.6428510468603,
        "gradient_delta": [
          -51.20761001664658,
          424.4778504225773
        ],
        "gradient_explosion_ratio": 0.8930149903949297,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 424.4778504225773,
        "relative_gradient_delta": 0.886836290345053,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.958078309551638e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 439.83140931738643,
        "filterflow_gradient_max_abs": 310.27237965253573,
        "gradient_delta": [
          129.5590296648507,
          436.2717727444796
        ],
        "gradient_explosion_ratio": 1.4175654623525942,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 436.2717727444796,
        "relative_gradient_delta": 1.4060928440779892,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.521620328683639e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 450.9302046686931,
        "filterflow_gradient_max_abs": 291.33394004387503,
        "gradient_delta": [
          159.59626462481805,
          447.25258731863266
        ],
        "gradient_explosion_ratio": 1.5478121244671417,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 447.25258731863266,
        "relative_gradient_delta": 1.5351887502406214,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.524789349285129e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 481.7383025771807,
        "filterflow_gradient_max_abs": 772.789629727978,
        "gradient_delta": [
          -291.05132715079725,
          476.5011220494619
        ],
        "gradient_explosion_ratio": 0.62337573389378,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 476.5011220494619,
        "relative_gradient_delta": 0.6165987530360498,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.415127818901965e-09,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 487.5884422427044,
        "filterflow_gradient_max_abs": 137.0827775975205,
        "gradient_delta": [
          350.50566464518386,
          482.2494932410043
        ],
        "gradient_explosion_ratio": 3.556890594048801,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 482.2494932410043,
        "relative_gradient_delta": 3.5179436957201475,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.988418484368594e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 495.7068845256421,
        "filterflow_gradient_max_abs": 205.40967733109431,
        "gradient_delta": [
          290.2972071945478,
          490.6839956018453
        ],
        "gradient_explosion_ratio": 2.413259642712089,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 490.6839956018453,
        "relative_gradient_delta": 2.388806613093136,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.800110448537453e-09,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 539.2567943293898,
        "filterflow_gradient_max_abs": 1075.2940301638955,
        "gradient_delta": [
          -536.0372358345057,
          530.9289856322731
        ],
        "gradient_explosion_ratio": 0.5014970595969892,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 536.0372358345057,
        "relative_gradient_delta": 0.49850294040301085,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.299266720408923e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 598.811573088497,
        "filterflow_gradient_max_abs": 1320.7702359098546,
        "gradient_delta": [
          -721.9586628213576,
          583.9043140279244
        ],
        "gradient_explosion_ratio": 0.4533805780957704,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 721.9586628213576,
        "relative_gradient_delta": 0.5466194219042295,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.148105858803319e-09,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 616.1566436827463,
        "filterflow_gradient_max_abs": 352.8826174689448,
        "gradient_delta": [
          263.27402621380156,
          600.0825785264035
        ],
        "gradient_explosion_ratio": 1.7460668595753965,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 600.0825785264035,
        "relative_gradient_delta": 1.700516117315451,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.5889797800336964e-09,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 661.1148378688308,
        "filterflow_gradient_max_abs": 974.6366511077524,
        "gradient_delta": [
          -313.5218132389216,
          644.7959319100429
        ],
        "gradient_explosion_ratio": 0.6783192865950823,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 644.7959319100429,
        "relative_gradient_delta": 0.6615757073953465,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.8240451633319026e-09,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 697.6639283739469,
        "filterflow_gradient_max_abs": 731.310897142959,
        "gradient_delta": [
          -33.64696876901212,
          678.5971591506653
        ],
        "gradient_explosion_ratio": 0.9539908828099485,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 678.5971591506653,
        "relative_gradient_delta": 0.9279188397188768,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.972274953412125e-09,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 721.6219155731446,
        "filterflow_gradient_max_abs": 483.3559108394908,
        "gradient_delta": [
          238.26600473365386,
          702.050537443978
        ],
        "gradient_explosion_ratio": 1.4929411214188615,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 702.050537443978,
        "relative_gradient_delta": 1.4524505063456432,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.955818783651921e-09,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 774.5468900734463,
        "filterflow_gradient_max_abs": 1076.6780654517022,
        "gradient_delta": [
          -302.1311753782559,
          752.1172169826792
        ],
        "gradient_explosion_ratio": 0.7193857801389296,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 752.1172169826792,
        "relative_gradient_delta": 0.6985534869860482,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5558010697277496e-09,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 775.4603613158199,
        "filterflow_gradient_max_abs": 18.05494027199655,
        "gradient_delta": [
          757.4054210438234,
          752.9923250555266
        ],
        "gradient_explosion_ratio": 42.950037476367015,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 757.4054210438234,
        "relative_gradient_delta": 41.950037476367015,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6730690428375965e-09,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 823.8151117639061,
        "filterflow_gradient_max_abs": 989.4278480713913,
        "gradient_delta": [
          -165.6127363074852,
          802.1639763395839
        ],
        "gradient_explosion_ratio": 0.8326176722938411,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 802.1639763395839,
        "relative_gradient_delta": 0.8107351919628852,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.355683813628275e-09,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 862.2728902346603,
        "filterflow_gradient_max_abs": 778.7073741209738,
        "gradient_delta": [
          83.5655161136865,
          837.8583362489834
        ],
        "gradient_explosion_ratio": 1.107313117726691,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 837.8583362489834,
        "relative_gradient_delta": 1.0759604494496804,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.821792577378801e-09,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 915.6926695412888,
        "filterflow_gradient_max_abs": 1097.9215016104433,
        "gradient_delta": [
          -182.22883206915458,
          889.9321519213461
        ],
        "gradient_explosion_ratio": 0.8340238060718737,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 889.9321519213461,
        "relative_gradient_delta": 0.8105608193445377,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0083482493428164e-08,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1000.2712193414375,
        "filterflow_gradient_max_abs": 1697.7646785016034,
        "gradient_delta": [
          -697.4934591601659,
          967.0831099898655
        ],
        "gradient_explosion_ratio": 0.5891695309766057,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 967.0831099898655,
        "relative_gradient_delta": 0.5696214099844417,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8990448324984754e-08,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1049.5970955622895,
        "filterflow_gradient_max_abs": 947.0739014815089,
        "gradient_delta": [
          102.52319408078063,
          1012.9556684304923
        ],
        "gradient_explosion_ratio": 1.1082525808391546,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1012.9556684304923,
        "relative_gradient_delta": 1.0695634911340335,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1565390423129429e-08,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1062.4143150887137,
        "filterflow_gradient_max_abs": 249.89093531615012,
        "gradient_delta": [
          812.5233797725635,
          1025.4098101992288
        ],
        "gradient_explosion_ratio": 4.251512019612067,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1025.4098101992288,
        "relative_gradient_delta": 4.103429397716765,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.132605782724568e-09,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1110.3289650832373,
        "filterflow_gradient_max_abs": 974.2890696675929,
        "gradient_delta": [
          136.03989541564442,
          1073.4501822141206
        ],
        "gradient_explosion_ratio": 1.1396299103119965,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1073.4501822141206,
        "relative_gradient_delta": 1.1017779174925562,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.223679515140248e-09,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1160.1054245025987,
        "filterflow_gradient_max_abs": 1029.3299119039873,
        "gradient_delta": [
          130.77551259861139,
          1120.6263973814184
        ],
        "gradient_explosion_ratio": 1.1270491715884476,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1120.6263973814184,
        "relative_gradient_delta": 1.0886950669766866,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.178016403486254e-09,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1229.7233449868552,
        "filterflow_gradient_max_abs": 1426.254117759735,
        "gradient_delta": [
          -196.5307727728798,
          1188.5795820615933
        ],
        "gradient_explosion_ratio": 0.8622049392701651,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1188.5795820615933,
        "relative_gradient_delta": 0.8333575113027789,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.153612730486202e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1324.5409479631946,
        "filterflow_gradient_max_abs": 1942.7454564725651,
        "gradient_delta": [
          -618.2045085093705,
          1277.5896722097582
        ],
        "gradient_explosion_ratio": 0.6817882103650151,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1277.5896722097582,
        "relative_gradient_delta": 0.6576207232673046,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.01524527357833e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1316.0955234885266,
        "filterflow_gradient_max_abs": 169.06130724664092,
        "gradient_delta": [
          1485.1568307351677,
          1269.6236012511786
        ],
        "gradient_explosion_ratio": 7.784723452827058,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1485.1568307351677,
        "relative_gradient_delta": 8.784723452827059,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.081496278260602e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1406.7307269485034,
        "filterflow_gradient_max_abs": 1963.5208371745916,
        "gradient_delta": [
          -556.7901102260882,
          1361.7460535553664
        ],
        "gradient_explosion_ratio": 0.716432797816762,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1361.7460535553664,
        "relative_gradient_delta": 0.693522588492033,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.653859933678177e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1461.571457674553,
        "filterflow_gradient_max_abs": 1119.9768301540837,
        "gradient_delta": [
          341.5946275204692,
          1412.0915791324564
        ],
        "gradient_explosion_ratio": 1.305001512820112,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1412.0915791324564,
        "relative_gradient_delta": 1.260822135881315,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.3080741458397824e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1507.3135164245462,
        "filterflow_gradient_max_abs": 979.6868013870265,
        "gradient_delta": [
          527.6267150375196,
          1457.640742175838
        ],
        "gradient_explosion_ratio": 1.5385667279486803,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1457.640742175838,
        "relative_gradient_delta": 1.487864019513309,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.394845624730806e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1640.9243039714381,
        "filterflow_gradient_max_abs": 2882.4178802677957,
        "gradient_delta": [
          -1241.4935762963576,
          1586.0645783846417
        ],
        "gradient_explosion_ratio": 0.5692874427419891,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1586.0645783846417,
        "relative_gradient_delta": 0.5502549055230277,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.620751946684322e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1682.4372954312546,
        "filterflow_gradient_max_abs": 858.8073873147812,
        "gradient_delta": [
          823.6299081164734,
          1624.26515059258
        ],
        "gradient_explosion_ratio": 1.9590391515980123,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1624.26515059258,
        "relative_gradient_delta": 1.8913031892647583,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.615852837261627e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1703.0226933630418,
        "filterflow_gradient_max_abs": 442.0116504772855,
        "gradient_delta": [
          1261.0110428857563,
          1645.113316502643
        ],
        "gradient_explosion_ratio": 3.852890962317651,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1645.113316502643,
        "relative_gradient_delta": 3.721877725906647,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.274422841874184e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1849.6908619222083,
        "filterflow_gradient_max_abs": 3282.5855155180925,
        "gradient_delta": [
          -1432.8946535958842,
          1786.8909906214408
        ],
        "gradient_explosion_ratio": 0.5634859634815242,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1786.8909906214408,
        "relative_gradient_delta": 0.5443547417650183,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0136062655874412e-08,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1938.4033367492455,
        "filterflow_gradient_max_abs": 1855.9144036285215,
        "gradient_delta": [
          82.48893312072391,
          1867.7927822664092
        ],
        "gradient_explosion_ratio": 1.0444465180934255,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1867.7927822664092,
        "relative_gradient_delta": 1.006400283663225,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.873637741795392e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1999.6784740233695,
        "filterflow_gradient_max_abs": 1310.8611477302254,
        "gradient_delta": [
          688.8173262931441,
          1928.2456242549115
        ],
        "gradient_explosion_ratio": 1.525469327919163,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1928.2456242549115,
        "relative_gradient_delta": 1.470976256786385,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.93335175330867e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2041.8696404269135,
        "filterflow_gradient_max_abs": 914.416967723082,
        "gradient_delta": [
          1127.4526727038315,
          1969.1074338689668
        ],
        "gradient_explosion_ratio": 2.232974356885801,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1969.1074338689668,
        "relative_gradient_delta": 2.1534021167302777,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.058265166255296e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2202.109524568214,
        "filterflow_gradient_max_abs": 3551.3298618369327,
        "gradient_delta": [
          -1349.2203372687186,
          2125.5101268402955
        ],
        "gradient_explosion_ratio": 0.62008025450758,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2125.5101268402955,
        "relative_gradient_delta": 0.5985110393943724,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.786315675024525e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2344.6883619706264,
        "filterflow_gradient_max_abs": 3023.0985131010166,
        "gradient_delta": [
          -678.4101511303902,
          2255.198227436181
        ],
        "gradient_explosion_ratio": 0.7755911201072655,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2255.198227436181,
        "relative_gradient_delta": 0.7459889969390566,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.745331570025883e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2440.5634496315947,
        "filterflow_gradient_max_abs": 2001.070628323309,
        "gradient_delta": [
          439.4928213082858,
          2347.6311378817177
        ],
        "gradient_explosion_ratio": 1.2196288402256623,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2347.6311378817177,
        "relative_gradient_delta": 1.1731875450337257,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.205052720062668e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2551.780512423556,
        "filterflow_gradient_max_abs": 2346.9001573329506,
        "gradient_delta": [
          204.88035509060546,
          2455.4977579705273
        ],
        "gradient_explosion_ratio": 1.0872982834188543,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2455.4977579705273,
        "relative_gradient_delta": 1.0462727825460578,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.456598728414974e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2744.1217418968677,
        "filterflow_gradient_max_abs": 4046.6212127655212,
        "gradient_delta": [
          -1302.4994708686536,
          2640.0633171320496
        ],
        "gradient_explosion_ratio": 0.6781266636077099,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2640.0633171320496,
        "relative_gradient_delta": 0.6524117722715616,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.6329352092725458e-08,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2877.6722404002735,
        "filterflow_gradient_max_abs": 2730.4139020142047,
        "gradient_delta": [
          147.25833838606877,
          2764.9054584793257
        ],
        "gradient_explosion_ratio": 1.0539326064364958,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2764.9054584793257,
        "relative_gradient_delta": 1.0126323545451028,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.300094916397939e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_transport_matrix_stop_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      60605.43234825605,
      8.881784197001252e-16
    ],
    "final_bayesfilter_gradient_max_abs": 60605.43234825605,
    "final_filterflow_gradient_diag": [
      18935.6850725171,
      2073.5151524806142
    ],
    "final_filterflow_gradient_max_abs": 18935.6850725171,
    "final_gradient_delta": [
      41669.74727573895,
      -2073.5151524806142
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 41669.74727573895,
    "final_relative_gradient_delta": 2.200593594377932,
    "final_scalar_delta": 9.3001517598168e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "status": "no_explosion"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 0.9989870736926509,
      "max_abs_gradient_delta": 0.008913771218997724,
      "relative_gradient_delta": 0.0010129263073491112,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.7926993223227328e-11,
      "status": "failure",
      "time_index": 1,
      "transport_status": "computed_post_resample_state_stop_gradient"
    },
    "first_scalar_failure": {
      "status": "no_failure"
    },
    "mode": "post_resample_state_stop_gradient",
    "mode_description": "Stop gradient through post-resampling particles and log weights",
    "sample_rows": [
      {
        "bayesfilter_gradient_max_abs": 0.008913771203554865,
        "filterflow_gradient_max_abs": 0.008913771203554867,
        "gradient_delta": [
          -1.734723475976807e-18,
          -5.766308833278761e-19
        ],
        "gradient_explosion_ratio": 0.008913771203554865,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 1.734723475976807e-18,
        "relative_gradient_delta": 1.734723475976807e-18,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.791105691525136,
        "filterflow_gradient_max_abs": 8.800019462744133,
        "gradient_delta": [
          0.008913771218997724,
          1.784088485773141e-16
        ],
        "gradient_explosion_ratio": 0.9989870736926509,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.008913771218997724,
        "relative_gradient_delta": 0.0010129263073491112,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7926993223227328e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.34253406766651,
        "filterflow_gradient_max_abs": 1.4485716238559057,
        "gradient_delta": [
          -8.791105691522416,
          2.68052137108038e-16
        ],
        "gradient_explosion_ratio": 5.068809817026277,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.791105691522416,
        "relative_gradient_delta": 6.068809817026278,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4985346297180513e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.497542707161104,
        "filterflow_gradient_max_abs": 16.840076774872443,
        "gradient_delta": [
          -7.342534067711339,
          -2.7455810949428476e-16
        ],
        "gradient_explosion_ratio": 0.5639845253753627,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.342534067711339,
        "relative_gradient_delta": 0.4360154746246373,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.4439117396468646e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7812382914936915,
        "filterflow_gradient_max_abs": 11.278780998887767,
        "gradient_delta": [
          9.497542707394075,
          1.0079978010276107e-15
        ],
        "gradient_explosion_ratio": 0.15792826296293408,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.497542707394075,
        "relative_gradient_delta": 0.842071737037066,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.665601073204016e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6207212034602356,
        "filterflow_gradient_max_abs": 0.16051708831084313,
        "gradient_delta": [
          -1.7812382917710787,
          1.2577928790488268e-15
        ],
        "gradient_explosion_ratio": 1.6207212034602356,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7812382917710787,
        "relative_gradient_delta": 1.7812382917710787,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.347366828165832e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.11226368107804,
        "filterflow_gradient_max_abs": 6.732984884221974,
        "gradient_delta": [
          -1.6207212031439342,
          1.6386494760117575e-15
        ],
        "gradient_explosion_ratio": 0.7592863743178868,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6207212031439342,
        "relative_gradient_delta": 0.24071362568211316,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.53681536782824e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 11.643364599099243,
        "filterflow_gradient_max_abs": 16.75562828027451,
        "gradient_delta": [
          5.112263681175268,
          1.042109480631756e-15
        ],
        "gradient_explosion_ratio": 0.6948927491311289,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.112263681175268,
        "relative_gradient_delta": 0.3051072508688712,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.6477489351891563e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.064701454679305,
        "filterflow_gradient_max_abs": 8.578663144440544,
        "gradient_delta": [
          -11.643364599119849,
          2.0002286082020054e-15
        ],
        "gradient_explosion_ratio": 0.35724697462510857,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 11.643364599119849,
        "relative_gradient_delta": 1.3572469746251086,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.839595473844383e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 53.811573954213756,
        "filterflow_gradient_max_abs": 56.8762754108451,
        "gradient_delta": [
          -3.0647014566313473,
          1.7580320210352958e-15
        ],
        "gradient_explosion_ratio": 0.9461163475545206,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.0647014566313473,
        "relative_gradient_delta": 0.05388365244547946,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.645795108146558e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 158.2631390682533,
        "filterflow_gradient_max_abs": 104.45156511568617,
        "gradient_delta": [
          53.811573952567144,
          2.1449585125149607e-16
        ],
        "gradient_explosion_ratio": 1.5151820740356328,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 53.811573952567144,
        "relative_gradient_delta": 0.5151820740356328,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.562661608062626e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 149.13242496742828,
        "filterflow_gradient_max_abs": 9.13071410440192,
        "gradient_delta": [
          158.2631390718302,
          -1.1001734173734845e-16
        ],
        "gradient_explosion_ratio": 16.333051638921813,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 158.2631390718302,
        "relative_gradient_delta": 17.333051638921813,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.412914561020443e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 211.59403776762687,
        "filterflow_gradient_max_abs": 62.46161279976278,
        "gradient_delta": [
          149.1324249678641,
          1.2955840461364398e-15
        ],
        "gradient_explosion_ratio": 3.387585242890662,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 149.1324249678641,
        "relative_gradient_delta": 2.387585242890662,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.171952003976912e-11,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 289.8130266677918,
        "filterflow_gradient_max_abs": 78.21898890138324,
        "gradient_delta": [
          211.59403776640858,
          1.8775525884200073e-15
        ],
        "gradient_explosion_ratio": 3.7051492321536093,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 211.59403776640858,
        "relative_gradient_delta": 2.7051492321536093,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1748113593057496e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 344.93334287389405,
        "filterflow_gradient_max_abs": 55.1203162059954,
        "gradient_delta": [
          289.81302666789867,
          2.1745252458348423e-15
        ],
        "gradient_explosion_ratio": 6.257825909140482,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 289.81302666789867,
        "relative_gradient_delta": 5.257825909140483,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1169021263413015e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 348.1347740002103,
        "filterflow_gradient_max_abs": 3.2014311273644616,
        "gradient_delta": [
          344.93334287284586,
          2.176127076014113e-15
        ],
        "gradient_explosion_ratio": 108.74348382025258,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 344.93334287284586,
        "relative_gradient_delta": 107.74348382025258,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.603695616533514e-11,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 373.189164341339,
        "filterflow_gradient_max_abs": 25.054390338542845,
        "gradient_delta": [
          348.1347740027961,
          1.6161682130097922e-15
        ],
        "gradient_explosion_ratio": 14.895160460848937,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 348.1347740027961,
        "relative_gradient_delta": 13.895160460848937,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1939249588976963e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 518.5492326742843,
        "filterflow_gradient_max_abs": 145.3600680670563,
        "gradient_delta": [
          373.189164607228,
          2.3943823862325625e-15
        ],
        "gradient_explosion_ratio": 3.5673430782590962,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 373.189164607228,
        "relative_gradient_delta": 2.567343078259096,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.48947520983711e-09,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 687.2138178530261,
        "filterflow_gradient_max_abs": 168.66458545141114,
        "gradient_delta": [
          518.549232401615,
          1.974398325815325e-15
        ],
        "gradient_explosion_ratio": 4.074440499846356,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 518.549232401615,
        "relative_gradient_delta": 3.0744404998463564,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.252356523513299e-09,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 586.054709837705,
        "filterflow_gradient_max_abs": 101.15910809775511,
        "gradient_delta": [
          687.2138179354602,
          1.197040276521395e-15
        ],
        "gradient_explosion_ratio": 5.793395383353627,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 687.2138179354602,
        "relative_gradient_delta": 6.793395383353628,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.767464479802584e-09,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 711.3354326796743,
        "filterflow_gradient_max_abs": 125.28072286451086,
        "gradient_delta": [
          586.0547098151635,
          1.0176600890471965e-15
        ],
        "gradient_explosion_ratio": 5.67793205862144,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 586.0547098151635,
        "relative_gradient_delta": 4.67793205862144,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9853310934413457e-09,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 990.2880804190407,
        "filterflow_gradient_max_abs": 278.9526477486435,
        "gradient_delta": [
          711.3354326703973,
          2.277276943685071e-15
        ],
        "gradient_explosion_ratio": 3.5500221575647557,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 711.3354326703973,
        "relative_gradient_delta": 2.5500221575647557,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.0152165209074155e-09,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1242.5702345617601,
        "filterflow_gradient_max_abs": 252.28215416061428,
        "gradient_delta": [
          990.2880804011459,
          6.591160970486996e-16
        ],
        "gradient_explosion_ratio": 4.925319583923813,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 990.2880804011459,
        "relative_gradient_delta": 3.9253195839238137,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.021582983819826e-09,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1312.1561447160786,
        "filterflow_gradient_max_abs": 69.58591013728201,
        "gradient_delta": [
          1242.5702345787965,
          -1.4067067022514786e-16
        ],
        "gradient_explosion_ratio": 18.856635518992302,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1242.5702345787965,
        "relative_gradient_delta": 17.856635518992302,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9725839567618095e-09,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1376.880856102082,
        "filterflow_gradient_max_abs": 64.72471139759364,
        "gradient_delta": [
          1312.1561447044883,
          3.503665504591294e-15
        ],
        "gradient_explosion_ratio": 21.272877489466445,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1312.1561447044883,
        "relative_gradient_delta": 20.272877489466445,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.974680057832302e-09,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1376.2274113372034,
        "filterflow_gradient_max_abs": 0.6534447816938739,
        "gradient_delta": [
          1376.8808561188973,
          2.693022349285733e-15
        ],
        "gradient_explosion_ratio": 1376.2274113372034,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1376.8808561188973,
        "relative_gradient_delta": 1376.8808561188973,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.903298934597842e-09,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1638.7369800870579,
        "filterflow_gradient_max_abs": 262.5095687458148,
        "gradient_delta": [
          1376.2274113412432,
          -8.038504048243402e-17
        ],
        "gradient_explosion_ratio": 6.2425799863845315,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1376.2274113412432,
        "relative_gradient_delta": 5.2425799863845315,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.970814705349767e-09,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1667.2859733301545,
        "filterflow_gradient_max_abs": 28.548993251385596,
        "gradient_delta": [
          1638.736980078769,
          1.4140656349579897e-15
        ],
        "gradient_explosion_ratio": 58.40086754194859,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1638.736980078769,
        "relative_gradient_delta": 57.40086754194859,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9090827524669294e-09,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2152.9929957161894,
        "filterflow_gradient_max_abs": 485.70702239538065,
        "gradient_delta": [
          1667.2859733208088,
          3.006815547975504e-15
        ],
        "gradient_explosion_ratio": 4.432698924339591,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1667.2859733208088,
        "relative_gradient_delta": 3.432698924339591,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8526088158287166e-09,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2398.1125113606486,
        "filterflow_gradient_max_abs": 245.11951564783823,
        "gradient_delta": [
          2152.99299571281,
          1.5841346399365171e-15
        ],
        "gradient_explosion_ratio": 9.783441783582841,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2152.99299571281,
        "relative_gradient_delta": 8.783441783582841,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8581510491676454e-09,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2832.8677057380714,
        "filterflow_gradient_max_abs": 434.75519438634416,
        "gradient_delta": [
          2398.1125113517273,
          1.577322938317603e-15
        ],
        "gradient_explosion_ratio": 6.516006576382962,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2398.1125113517273,
        "relative_gradient_delta": 5.516006576382962,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9084219477226725e-09,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2580.9598963665285,
        "filterflow_gradient_max_abs": 251.90780939902413,
        "gradient_delta": [
          2832.8677057655527,
          4.239718593162933e-15
        ],
        "gradient_explosion_ratio": 10.245652576329087,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2832.8677057655527,
        "relative_gradient_delta": 11.245652576329089,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.980804936214554e-09,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2950.7347766228036,
        "filterflow_gradient_max_abs": 369.7748801823844,
        "gradient_delta": [
          2580.959896440419,
          -8.094030335033758e-16
        ],
        "gradient_explosion_ratio": 7.979814029464117,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2580.959896440419,
        "relative_gradient_delta": 6.979814029464116,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9715820915043878e-09,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3104.676435272906,
        "filterflow_gradient_max_abs": 153.94165873710156,
        "gradient_delta": [
          2950.7347765358045,
          2.3130903874139615e-15
        ],
        "gradient_explosion_ratio": 20.167876978479292,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2950.7347765358045,
        "relative_gradient_delta": 19.167876978479292,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.075740551139461e-09,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3336.5565370844433,
        "filterflow_gradient_max_abs": 231.88010181357106,
        "gradient_delta": [
          3104.6764352708724,
          1.4238024834251886e-15
        ],
        "gradient_explosion_ratio": 14.38914555836704,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3104.6764352708724,
        "relative_gradient_delta": 13.389145558367042,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8847040312030003e-09,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3653.6620624983825,
        "filterflow_gradient_max_abs": 317.10552544548756,
        "gradient_delta": [
          3336.556537052895,
          -3.2479201484656617e-15
        ],
        "gradient_explosion_ratio": 11.52191232671053,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3336.556537052895,
        "relative_gradient_delta": 10.52191232671053,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8788775807697675e-09,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4094.095177239975,
        "filterflow_gradient_max_abs": 440.433114763931,
        "gradient_delta": [
          3653.662062476044,
          -8.358266365515253e-15
        ],
        "gradient_explosion_ratio": 9.295611615022137,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3653.662062476044,
        "relative_gradient_delta": 8.295611615022137,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.7967104188064695e-09,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3819.719708301809,
        "filterflow_gradient_max_abs": 274.3754691050723,
        "gradient_delta": [
          4094.0951774068812,
          1.4961187319388716e-15
        ],
        "gradient_explosion_ratio": 13.921505886661627,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4094.0951774068812,
        "relative_gradient_delta": 14.921505886661626,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9457680739142234e-09,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3635.4781709008585,
        "filterflow_gradient_max_abs": 184.24153726601756,
        "gradient_delta": [
          3819.719708166876,
          2.2497546991074132e-15
        ],
        "gradient_explosion_ratio": 19.732131119009093,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3819.719708166876,
        "relative_gradient_delta": 20.732131119009093,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8393571938067907e-09,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3822.6167806416206,
        "filterflow_gradient_max_abs": 187.1386096136716,
        "gradient_delta": [
          3635.478171027949,
          3.408859913601743e-17
        ],
        "gradient_explosion_ratio": 20.42666015598288,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3635.478171027949,
        "relative_gradient_delta": 19.42666015598288,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.6310544853913598e-09,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4776.766882660707,
        "filterflow_gradient_max_abs": 954.1501022077981,
        "gradient_delta": [
          3822.6167804529086,
          3.974676307401524e-15
        ],
        "gradient_explosion_ratio": 5.0063054771023925,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3822.6167804529086,
        "relative_gradient_delta": 4.006305477102392,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.98600263906701e-09,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4353.855016958635,
        "filterflow_gradient_max_abs": 422.91186590476366,
        "gradient_delta": [
          4776.766882863399,
          1.010340815934336e-15
        ],
        "gradient_explosion_ratio": 10.294946460402906,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4776.766882863399,
        "relative_gradient_delta": 11.294946460402906,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5840096163374255e-09,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4708.122424025215,
        "filterflow_gradient_max_abs": 354.26740709319216,
        "gradient_delta": [
          4353.855016932022,
          3.5082981292620594e-15
        ],
        "gradient_explosion_ratio": 13.289741956946989,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4353.855016932022,
        "relative_gradient_delta": 12.289741956946987,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.941782094647351e-09,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4907.176204880965,
        "filterflow_gradient_max_abs": 199.05378088782396,
        "gradient_delta": [
          4708.122423993141,
          4.4457956480944976e-15
        ],
        "gradient_explosion_ratio": 24.652514425970068,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4708.122423993141,
        "relative_gradient_delta": 23.652514425970065,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.940716280543711e-09,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5455.916614342384,
        "filterflow_gradient_max_abs": 548.7404094827189,
        "gradient_delta": [
          4907.176204859665,
          4.057945896674416e-15
        ],
        "gradient_explosion_ratio": 9.942618622684472,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4907.176204859665,
        "relative_gradient_delta": 8.942618622684472,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.836934408558591e-09,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5855.392271569117,
        "filterflow_gradient_max_abs": 399.4756572109477,
        "gradient_delta": [
          5455.91661435817,
          7.49230492359127e-15
        ],
        "gradient_explosion_ratio": 14.657694820380781,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5455.91661435817,
        "relative_gradient_delta": 13.657694820380783,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.73063721528888e-09,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5474.18833440528,
        "filterflow_gradient_max_abs": 381.20393707705813,
        "gradient_delta": [
          5855.392271482338,
          5.5924277793354064e-15
        ],
        "gradient_explosion_ratio": 14.360261796820597,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5855.392271482338,
        "relative_gradient_delta": 15.360261796820597,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.649024276659475e-09,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5523.039323016433,
        "filterflow_gradient_max_abs": 48.850988576799736,
        "gradient_delta": [
          5474.188334439633,
          1.3774803244591701e-14
        ],
        "gradient_explosion_ratio": 113.05890594892544,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5474.188334439633,
        "relative_gradient_delta": 112.05890594892544,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.737742642646481e-09,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5869.890062734427,
        "filterflow_gradient_max_abs": 346.85073969207997,
        "gradient_delta": [
          5523.039323042347,
          7.740385650708844e-15
        ],
        "gradient_explosion_ratio": 16.923389201780218,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5523.039323042347,
        "relative_gradient_delta": 15.923389201780216,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.721428581433429e-09,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5547.260541972002,
        "filterflow_gradient_max_abs": 322.6295207830076,
        "gradient_delta": [
          5869.89006275501,
          9.845173674141605e-15
        ],
        "gradient_explosion_ratio": 17.193902555814006,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5869.89006275501,
        "relative_gradient_delta": 18.193902555814006,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6360639771592105e-09,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5460.595013625715,
        "filterflow_gradient_max_abs": 86.66552831338745,
        "gradient_delta": [
          5547.260541939103,
          7.413518103529223e-15
        ],
        "gradient_explosion_ratio": 63.00769313815171,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5547.260541939103,
        "relative_gradient_delta": 64.00769313815171,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.636163453142217e-09,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6578.989808186319,
        "filterflow_gradient_max_abs": 1118.3947944525503,
        "gradient_delta": [
          5460.5950137337695,
          6.671357557797033e-15
        ],
        "gradient_explosion_ratio": 5.882528996754414,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5460.5950137337695,
        "relative_gradient_delta": 4.882528996754414,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9218832625920186e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6651.977451603898,
        "filterflow_gradient_max_abs": 72.987643547552,
        "gradient_delta": [
          6578.989808056346,
          7.445989167628214e-15
        ],
        "gradient_explosion_ratio": 91.13840546544135,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6578.989808056346,
        "relative_gradient_delta": 90.13840546544135,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9393910356011475e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6659.490645398038,
        "filterflow_gradient_max_abs": 7.513193750877159,
        "gradient_delta": [
          6651.977451647162,
          9.706828289736955e-15
        ],
        "gradient_explosion_ratio": 886.3728084505406,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6651.977451647162,
        "relative_gradient_delta": 885.3728084505407,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.889368827003636e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6990.016645670503,
        "filterflow_gradient_max_abs": 330.52600026078443,
        "gradient_delta": [
          6659.490645409718,
          7.328012773581626e-15
        ],
        "gradient_explosion_ratio": 21.148159721641843,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6659.490645409718,
        "relative_gradient_delta": 20.148159721641843,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.899515377270291e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7276.473582442708,
        "filterflow_gradient_max_abs": 286.4569368626525,
        "gradient_delta": [
          6990.016645580055,
          7.99288884691469e-15
        ],
        "gradient_explosion_ratio": 25.40163161044886,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6990.016645580055,
        "relative_gradient_delta": 24.40163161044886,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.8836134308439796e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7886.152292414331,
        "filterflow_gradient_max_abs": 609.6787100623405,
        "gradient_delta": [
          7276.47358235199,
          8.062690890020705e-15
        ],
        "gradient_explosion_ratio": 12.934931402817002,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7276.47358235199,
        "relative_gradient_delta": 11.934931402817002,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.874831122629985e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8123.3390929250545,
        "filterflow_gradient_max_abs": 237.18680047332637,
        "gradient_delta": [
          7886.1522924517285,
          1.0006199304307735e-14
        ],
        "gradient_explosion_ratio": 34.24869797439926,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7886.1522924517285,
        "relative_gradient_delta": 33.24869797439926,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.782176349886868e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8102.940560313702,
        "filterflow_gradient_max_abs": 20.398532585564105,
        "gradient_delta": [
          8123.339092899266,
          7.36237566855635e-15
        ],
        "gradient_explosion_ratio": 397.23154233398606,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8123.339092899266,
        "relative_gradient_delta": 398.23154233398606,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.6820893001277e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8581.583411170372,
        "filterflow_gradient_max_abs": 478.6428510468603,
        "gradient_delta": [
          8102.940560123511,
          3.736033352369771e-15
        ],
        "gradient_explosion_ratio": 17.928991088869754,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8102.940560123511,
        "relative_gradient_delta": 16.928991088869754,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.958078309551638e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8891.855790831316,
        "filterflow_gradient_max_abs": 310.27237965253573,
        "gradient_delta": [
          8581.58341117878,
          1.2627038024522703e-15
        ],
        "gradient_explosion_ratio": 28.658225397919807,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8581.58341117878,
        "relative_gradient_delta": 27.658225397919807,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.521620328683639e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9183.189730926882,
        "filterflow_gradient_max_abs": 291.33394004387503,
        "gradient_delta": [
          8891.855790883008,
          -3.766204434035405e-16
        ],
        "gradient_explosion_ratio": 31.52118057217738,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8891.855790883008,
        "relative_gradient_delta": 30.52118057217738,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.524789349285129e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9955.979360424344,
        "filterflow_gradient_max_abs": 772.789629727978,
        "gradient_delta": [
          9183.189730696366,
          -4.803354494424925e-15
        ],
        "gradient_explosion_ratio": 12.883168947193106,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9183.189730696366,
        "relative_gradient_delta": 11.883168947193106,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.415127818901965e-09,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10093.062138010673,
        "filterflow_gradient_max_abs": 137.0827775975205,
        "gradient_delta": [
          9955.979360413152,
          -5.8444490370134585e-15
        ],
        "gradient_explosion_ratio": 73.62749949263672,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9955.979360413152,
        "relative_gradient_delta": 72.62749949263672,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.988418484368594e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10298.471815257422,
        "filterflow_gradient_max_abs": 205.40967733109431,
        "gradient_delta": [
          10093.062137926328,
          1.2174625766877997e-15
        ],
        "gradient_explosion_ratio": 50.13625428493125,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10093.062137926328,
        "relative_gradient_delta": 49.13625428493125,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.800110448537453e-09,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 11373.765845241001,
        "filterflow_gradient_max_abs": 1075.2940301638955,
        "gradient_delta": [
          10298.471815077106,
          -7.218468387405266e-15
        ],
        "gradient_explosion_ratio": 10.57735421771794,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10298.471815077106,
        "relative_gradient_delta": 9.57735421771794,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.299266720408923e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 12694.536080901786,
        "filterflow_gradient_max_abs": 1320.7702359098546,
        "gradient_delta": [
          11373.76584499193,
          -2.197122402901967e-15
        ],
        "gradient_explosion_ratio": 9.611464383248121,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 11373.76584499193,
        "relative_gradient_delta": 8.611464383248121,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.148105858803319e-09,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13047.41869875554,
        "filterflow_gradient_max_abs": 352.8826174689448,
        "gradient_delta": [
          12694.536081286595,
          -7.707835555933041e-15
        ],
        "gradient_explosion_ratio": 36.97382090491825,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 12694.536081286595,
        "relative_gradient_delta": 35.97382090491825,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.5889797800336964e-09,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 14022.05534953447,
        "filterflow_gradient_max_abs": 974.6366511077524,
        "gradient_delta": [
          13047.418698426718,
          -1.573014386627245e-14
        ],
        "gradient_explosion_ratio": 14.386956753162611,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13047.418698426718,
        "relative_gradient_delta": 13.386956753162611,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.8240451633319026e-09,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 14753.36624682898,
        "filterflow_gradient_max_abs": 731.310897142959,
        "gradient_delta": [
          14022.055349686021,
          3.314519466260152e-15
        ],
        "gradient_explosion_ratio": 20.173863543489556,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 14022.055349686021,
        "relative_gradient_delta": 19.173863543489556,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.972274953412125e-09,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 15236.722157538177,
        "filterflow_gradient_max_abs": 483.3559108394908,
        "gradient_delta": [
          14753.366246698686,
          3.8297220875627344e-15
        ],
        "gradient_explosion_ratio": 31.522780245047784,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 14753.366246698686,
        "relative_gradient_delta": 30.52278024504778,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.955818783651921e-09,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 16313.40022261484,
        "filterflow_gradient_max_abs": 1076.6780654517022,
        "gradient_delta": [
          15236.722157163138,
          2.6502891533456854e-14
        ],
        "gradient_explosion_ratio": 15.15160450098965,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 15236.722157163138,
        "relative_gradient_delta": 14.15160450098965,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5558010697277496e-09,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 16331.455163199686,
        "filterflow_gradient_max_abs": 18.05494027199655,
        "gradient_delta": [
          16313.400222927688,
          -1.9255713090770343e-15
        ],
        "gradient_explosion_ratio": 904.5421871890646,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 16313.400222927688,
        "relative_gradient_delta": 903.5421871890646,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6730690428375965e-09,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 17320.88301165736,
        "filterflow_gradient_max_abs": 989.4278480713913,
        "gradient_delta": [
          16331.455163585968,
          -6.333061527405524e-15
        ],
        "gradient_explosion_ratio": 17.505958666333783,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 16331.455163585968,
        "relative_gradient_delta": 16.505958666333786,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.355683813628275e-09,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 18099.59038800022,
        "filterflow_gradient_max_abs": 778.7073741209738,
        "gradient_delta": [
          17320.883013879244,
          1.298554704430069e-15
        ],
        "gradient_explosion_ratio": 23.243121857464793,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 17320.883013879244,
        "relative_gradient_delta": 22.24312185746479,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.821792577378801e-09,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 19197.511889466048,
        "filterflow_gradient_max_abs": 1097.9215016104433,
        "gradient_delta": [
          18099.590387855606,
          1.738493369820853e-14
        ],
        "gradient_explosion_ratio": 17.485322822539615,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 18099.590387855606,
        "relative_gradient_delta": 16.485322822539615,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0083482493428164e-08,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 20895.276565745713,
        "filterflow_gradient_max_abs": 1697.7646785016034,
        "gradient_delta": [
          19197.51188724411,
          -2.9625098469535875e-14
        ],
        "gradient_explosion_ratio": 12.307522255785921,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 19197.51188724411,
        "relative_gradient_delta": 11.307522255785921,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8990448324984754e-08,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 21842.350468394085,
        "filterflow_gradient_max_abs": 947.0739014815089,
        "gradient_delta": [
          20895.276566912577,
          9.123544269070063e-15
        ],
        "gradient_explosion_ratio": 23.062984244657223,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 20895.276566912577,
        "relative_gradient_delta": 22.062984244657223,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1565390423129429e-08,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 22092.241402269094,
        "filterflow_gradient_max_abs": 249.89093531615012,
        "gradient_delta": [
          21842.350466952943,
          -1.3529575599539906e-14
        ],
        "gradient_explosion_ratio": 88.40753416813236,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 21842.350466952943,
        "relative_gradient_delta": 87.40753416813236,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.132605782724568e-09,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 23066.530472355502,
        "filterflow_gradient_max_abs": 974.2890696675929,
        "gradient_delta": [
          22092.24140268791,
          1.467083288507541e-14
        ],
        "gradient_explosion_ratio": 23.675242995618664,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 22092.24140268791,
        "relative_gradient_delta": 22.67524299561866,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.223679515140248e-09,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 24095.860384240004,
        "filterflow_gradient_max_abs": 1029.3299119039873,
        "gradient_delta": [
          23066.530472336017,
          1.7777903743546368e-14
        ],
        "gradient_explosion_ratio": 23.40926859850896,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 23066.530472336017,
        "relative_gradient_delta": 22.40926859850896,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.178016403486254e-09,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 25522.114502144796,
        "filterflow_gradient_max_abs": 1426.254117759735,
        "gradient_delta": [
          24095.86038438506,
          -1.1392839814864174e-14
        ],
        "gradient_explosion_ratio": 17.89450714591677,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 24095.86038438506,
        "relative_gradient_delta": 16.89450714591677,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.153612730486202e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 27464.85995832301,
        "filterflow_gradient_max_abs": 1942.7454564725651,
        "gradient_delta": [
          25522.114501850443,
          -1.370364926282932e-15
        ],
        "gradient_explosion_ratio": 14.137137660942388,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 25522.114501850443,
        "relative_gradient_delta": 13.137137660942386,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.01524527357833e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 27295.798651279154,
        "filterflow_gradient_max_abs": 169.06130724664092,
        "gradient_delta": [
          27464.859958525794,
          1.4993785858933123e-14
        ],
        "gradient_explosion_ratio": 161.45503128907987,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 27464.859958525794,
        "relative_gradient_delta": 162.45503128907987,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.081496278260602e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 29259.31948738698,
        "filterflow_gradient_max_abs": 1963.5208371745916,
        "gradient_delta": [
          27295.79865021239,
          -3.8337990206776965e-16
        ],
        "gradient_explosion_ratio": 14.901456064754413,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 27295.79865021239,
        "relative_gradient_delta": 13.901456064754413,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.653859933678177e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 30379.296318253764,
        "filterflow_gradient_max_abs": 1119.9768301540837,
        "gradient_delta": [
          29259.31948809968,
          5.769263387545676e-15
        ],
        "gradient_explosion_ratio": 27.12493285604333,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 29259.31948809968,
        "relative_gradient_delta": 26.12493285604333,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.3080741458397824e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 31358.983119687015,
        "filterflow_gradient_max_abs": 979.6868013870265,
        "gradient_delta": [
          30379.29631829999,
          3.7383442378029024e-15
        ],
        "gradient_explosion_ratio": 32.00919219825093,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 30379.29631829999,
        "relative_gradient_delta": 31.009192198250926,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.394845624730806e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 34241.40100040151,
        "filterflow_gradient_max_abs": 2882.4178802677957,
        "gradient_delta": [
          31358.98312013371,
          2.6056531894978138e-15
        ],
        "gradient_explosion_ratio": 11.879402093224684,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 31358.98312013371,
        "relative_gradient_delta": 10.879402093224684,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.620751946684322e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 35100.20838698788,
        "filterflow_gradient_max_abs": 858.8073873147812,
        "gradient_delta": [
          34241.4009996731,
          -2.7469151046866533e-14
        ],
        "gradient_explosion_ratio": 40.87087384836676,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 34241.4009996731,
        "relative_gradient_delta": 39.87087384836676,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.615852837261627e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 35542.22003737941,
        "filterflow_gradient_max_abs": 442.0116504772855,
        "gradient_delta": [
          35100.20838690212,
          -1.7123465990454406e-16
        ],
        "gradient_explosion_ratio": 80.41014303356216,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 35100.20838690212,
        "relative_gradient_delta": 79.41014303356215,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.274422841874184e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 38824.805552116355,
        "filterflow_gradient_max_abs": 3282.5855155180925,
        "gradient_delta": [
          35542.220036598264,
          -6.785167968966263e-16
        ],
        "gradient_explosion_ratio": 11.82750772784928,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 35542.220036598264,
        "relative_gradient_delta": 10.827507727849282,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0136062655874412e-08,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 40680.71995623156,
        "filterflow_gradient_max_abs": 1855.9144036285215,
        "gradient_delta": [
          38824.80555260304,
          2.089186662260899e-15
        ],
        "gradient_explosion_ratio": 21.91950225543601,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 38824.80555260304,
        "relative_gradient_delta": 20.91950225543601,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.873637741795392e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 41991.58110373599,
        "filterflow_gradient_max_abs": 1310.8611477302254,
        "gradient_delta": [
          40680.71995600576,
          -6.987614604163088e-16
        ],
        "gradient_explosion_ratio": 32.03358431703084,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 40680.71995600576,
        "relative_gradient_delta": 31.033584317030833,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.93335175330867e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 42905.99807094041,
        "filterflow_gradient_max_abs": 914.416967723082,
        "gradient_delta": [
          41991.58110321733,
          -1.7073638301014287e-14
        ],
        "gradient_explosion_ratio": 46.92169938379126,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 41991.58110321733,
        "relative_gradient_delta": 45.92169938379126,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.058265166255296e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 46457.32793263785,
        "filterflow_gradient_max_abs": 3551.3298618369327,
        "gradient_delta": [
          42905.99807080092,
          -3.475372171759522e-14
        ],
        "gradient_explosion_ratio": 13.081670737453743,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 42905.99807080092,
        "relative_gradient_delta": 12.081670737453743,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.786315675024525e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 49480.42644582876,
        "filterflow_gradient_max_abs": 3023.0985131010166,
        "gradient_delta": [
          46457.32793272774,
          6.259393734508407e-17
        ],
        "gradient_explosion_ratio": 16.3674541968773,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 46457.32793272774,
        "relative_gradient_delta": 15.367454196877299,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.745331570025883e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 51481.49707393803,
        "filterflow_gradient_max_abs": 2001.070628323309,
        "gradient_delta": [
          49480.42644561472,
          3.8143292655365965e-15
        ],
        "gradient_explosion_ratio": 25.726976522100184,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 49480.42644561472,
        "relative_gradient_delta": 24.726976522100184,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.205052720062668e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 53828.39723303359,
        "filterflow_gradient_max_abs": 2346.9001573329506,
        "gradient_delta": [
          51481.49707570064,
          3.2306758139115564e-15
        ],
        "gradient_explosion_ratio": 22.93595535576806,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 51481.49707570064,
        "relative_gradient_delta": 21.93595535576806,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.456598728414974e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 57875.01844357183,
        "filterflow_gradient_max_abs": 4046.6212127655212,
        "gradient_delta": [
          53828.39723080631,
          2.133487496928068e-15
        ],
        "gradient_explosion_ratio": 14.302059768035265,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 53828.39723080631,
        "relative_gradient_delta": 13.302059768035264,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.6329352092725458e-08,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 60605.43234825605,
        "filterflow_gradient_max_abs": 2730.4139020142047,
        "gradient_delta": [
          57875.01844624185,
          2.446490013338861e-15
        ],
        "gradient_explosion_ratio": 22.196426814098736,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 57875.01844624185,
        "relative_gradient_delta": 21.196426814098736,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.300094916397939e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_post_resample_state_stop_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      -4.6565250369319974e+210,
      1.149344864086458e+211
    ],
    "final_bayesfilter_gradient_max_abs": 1.149344864086458e+211,
    "final_filterflow_gradient_diag": [
      18935.6850725171,
      2073.5151524806142
    ],
    "final_filterflow_gradient_max_abs": 18935.6850725171,
    "final_gradient_delta": [
      -4.6565250369319974e+210,
      1.149344864086458e+211
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 1.149344864086458e+211,
    "final_relative_gradient_delta": 6.069729506404791e+206,
    "final_scalar_delta": 9.3001517598168e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "bayesfilter_gradient_max_abs": 2642771588.232864,
      "filterflow_gradient_max_abs": 104.45156511568617,
      "gradient_explosion_ratio": 25301407.26283844,
      "resampling_flag": [
        true
      ],
      "status": "explosion",
      "time_index": 10,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 0.010899762307410662,
      "max_abs_gradient_delta": 0.0024553285995017,
      "relative_gradient_delta": 0.0024553285995017,
      "resampling_flag": [
        false
      ],
      "scalar_delta": 0.0,
      "status": "failure",
      "time_index": 0,
      "transport_status": "not_triggered"
    },
    "first_scalar_failure": {
      "status": "no_failure"
    },
    "mode": "proposal_mean_stop_gradient",
    "mode_description": "Stop gradient through optimal proposal mean",
    "sample_rows": [
      {
        "bayesfilter_gradient_max_abs": 0.010899762307410662,
        "filterflow_gradient_max_abs": 0.008913771203554867,
        "gradient_delta": [
          0.001985991103855795,
          -0.0024553285995017
        ],
        "gradient_explosion_ratio": 0.010899762307410662,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.0024553285995017,
        "relative_gradient_delta": 0.0024553285995017,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 10.375557181385211,
        "filterflow_gradient_max_abs": 8.800019462744133,
        "gradient_delta": [
          -1.575537718641078,
          0.9201494547783748
        ],
        "gradient_explosion_ratio": 1.1790379811443932,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.575537718641078,
        "relative_gradient_delta": 0.17903798114439326,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7926993223227328e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.083197306701376,
        "filterflow_gradient_max_abs": 1.4485716238559057,
        "gradient_delta": [
          -9.53176893055728,
          0.5675300416898237
        ],
        "gradient_explosion_ratio": 5.580115731650863,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.53176893055728,
        "relative_gradient_delta": 6.580115731650863,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4985346297180513e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 83.50589606678301,
        "filterflow_gradient_max_abs": 16.840076774872443,
        "gradient_delta": [
          -64.20330251955556,
          83.50589606678301
        ],
        "gradient_explosion_ratio": 4.958759819396104,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 83.50589606678301,
        "relative_gradient_delta": 4.958759819396104,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.4439117396468646e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 127.86253736428823,
        "filterflow_gradient_max_abs": 11.278780998887767,
        "gradient_delta": [
          -64.05177706723423,
          127.86253736428823
        ],
        "gradient_explosion_ratio": 11.336556439645129,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 127.86253736428823,
        "relative_gradient_delta": 11.336556439645129,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.665601073204016e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2924.161572124281,
        "filterflow_gradient_max_abs": 0.16051708831084313,
        "gradient_delta": [
          -1279.630379172213,
          2924.161572124281
        ],
        "gradient_explosion_ratio": 2924.161572124281,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2924.161572124281,
        "relative_gradient_delta": 2924.161572124281,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.347366828165832e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13188.4343814126,
        "filterflow_gradient_max_abs": 6.732984884221974,
        "gradient_delta": [
          -5479.812309288689,
          13188.4343814126
        ],
        "gradient_explosion_ratio": 1958.779740070155,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13188.4343814126,
        "relative_gradient_delta": 1958.779740070155,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.53681536782824e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 319684.23979829263,
        "filterflow_gradient_max_abs": 16.75562828027451,
        "gradient_delta": [
          131177.58329327946,
          -319684.23979829263
        ],
        "gradient_explosion_ratio": 19079.215321017804,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 319684.23979829263,
        "relative_gradient_delta": 19079.215321017804,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.6477489351891563e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1589317.5629433652,
        "filterflow_gradient_max_abs": 8.578663144440544,
        "gradient_delta": [
          648540.6827715132,
          -1589317.5629433652
        ],
        "gradient_explosion_ratio": 185264.013306471,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1589317.5629433652,
        "relative_gradient_delta": 185264.013306471,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.839595473844383e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8758148.905141879,
        "filterflow_gradient_max_abs": 56.8762754108451,
        "gradient_delta": [
          -3527741.744118849,
          8758148.905141879
        ],
        "gradient_explosion_ratio": 153985.97819349973,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8758148.905141879,
        "relative_gradient_delta": 153985.97819349973,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.645795108146558e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2642771588.232864,
        "filterflow_gradient_max_abs": 104.45156511568617,
        "gradient_delta": [
          1070762503.9506841,
          -2642771588.232864
        ],
        "gradient_explosion_ratio": 25301407.26283844,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2642771588.232864,
        "relative_gradient_delta": 25301407.26283844,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.562661608062626e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 71342825560.46133,
        "filterflow_gradient_max_abs": 9.13071410440192,
        "gradient_delta": [
          28903897246.34078,
          -71342825560.46133
        ],
        "gradient_explosion_ratio": 7813499003.989944,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 71342825560.46133,
        "relative_gradient_delta": 7813499003.989944,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.412914561020443e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1372890267591.6233,
        "filterflow_gradient_max_abs": 62.46161279976278,
        "gradient_delta": [
          -556221553063.6802,
          1372890267591.6233
        ],
        "gradient_explosion_ratio": 21979744134.894276,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1372890267591.6233,
        "relative_gradient_delta": 21979744134.894276,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.171952003976912e-11,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 32912939897083.61,
        "filterflow_gradient_max_abs": 78.21898890138324,
        "gradient_delta": [
          13334545446969.422,
          -32912939897083.61
        ],
        "gradient_explosion_ratio": 420779408675.04065,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 32912939897083.61,
        "relative_gradient_delta": 420779408675.04065,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1748113593057496e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 749319138578224.1,
        "filterflow_gradient_max_abs": 55.1203162059954,
        "gradient_delta": [
          303583655140054.1,
          -749319138578224.1
        ],
        "gradient_explosion_ratio": 13594246008638.121,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 749319138578224.1,
        "relative_gradient_delta": 13594246008638.121,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1169021263413015e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.581253930502948e+16,
        "filterflow_gradient_max_abs": 3.2014311273644616,
        "gradient_delta": [
          -1.0457848374167206e+16,
          2.581253930502948e+16
        ],
        "gradient_explosion_ratio": 8062812622890730.0,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.581253930502948e+16,
        "relative_gradient_delta": 8062812622890730.0,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.603695616533514e-11,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.6645964294594352e+17,
        "filterflow_gradient_max_abs": 25.054390338542845,
        "gradient_delta": [
          -1.0795506801926208e+17,
          2.6645964294594352e+17
        ],
        "gradient_explosion_ratio": 1.0635247529293532e+16,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.6645964294594352e+17,
        "relative_gradient_delta": 1.0635247529293532e+16,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1939249588976963e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.3873635238802194e+19,
        "filterflow_gradient_max_abs": 145.3600680670563,
        "gradient_delta": [
          -2.5878149441526243e+19,
          6.3873635238802194e+19
        ],
        "gradient_explosion_ratio": 4.394166574642531e+17,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.3873635238802194e+19,
        "relative_gradient_delta": 4.394166574642531e+17,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.48947520983711e-09,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.452068611847153e+21,
        "filterflow_gradient_max_abs": 168.66458545141114,
        "gradient_delta": [
          3.019175985124389e+21,
          -7.452068611847153e+21
        ],
        "gradient_explosion_ratio": 4.418277015238592e+19,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.452068611847153e+21,
        "relative_gradient_delta": 4.418277015238592e+19,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.252356523513299e-09,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.160970763498287e+22,
        "filterflow_gradient_max_abs": 101.15910809775511,
        "gradient_delta": [
          3.30638486973665e+22,
          -8.160970763498287e+22
        ],
        "gradient_explosion_ratio": 8.067460179277117e+20,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.160970763498287e+22,
        "relative_gradient_delta": 8.067460179277117e+20,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.767464479802584e-09,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.677542873479484e+24,
        "filterflow_gradient_max_abs": 125.28072286451086,
        "gradient_delta": [
          -3.1105259813465523e+24,
          7.677542873479484e+24
        ],
        "gradient_explosion_ratio": 6.128271531273511e+22,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.677542873479484e+24,
        "relative_gradient_delta": 6.128271531273511e+22,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9853310934413457e-09,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.466545700875953e+27,
        "filterflow_gradient_max_abs": 278.9526477486435,
        "gradient_delta": [
          1.4044572131631613e+27,
          -3.466545700875953e+27
        ],
        "gradient_explosion_ratio": 1.2427004112897186e+25,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.466545700875953e+27,
        "relative_gradient_delta": 1.2427004112897186e+25,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.0152165209074155e-09,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4435775339887256e+29,
        "filterflow_gradient_max_abs": 252.28215416061428,
        "gradient_delta": [
          -9.900057260664534e+28,
          2.4435775339887256e+29
        ],
        "gradient_explosion_ratio": 9.685891347007577e+26,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4435775339887256e+29,
        "relative_gradient_delta": 9.685891347007577e+26,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.021582983819826e-09,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2170886671448452e+30,
        "filterflow_gradient_max_abs": 69.58591013728201,
        "gradient_delta": [
          -4.9309863625925876e+29,
          1.2170886671448452e+30
        ],
        "gradient_explosion_ratio": 1.7490446912941448e+28,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2170886671448452e+30,
        "relative_gradient_delta": 1.7490446912941448e+28,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9725839567618095e-09,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7892633490620118e+32,
        "filterflow_gradient_max_abs": 64.72471139759364,
        "gradient_delta": [
          -7.249129345694311e+31,
          1.7892633490620118e+32
        ],
        "gradient_explosion_ratio": 2.7644207450703807e+30,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7892633490620118e+32,
        "relative_gradient_delta": 2.7644207450703807e+30,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.974680057832302e-09,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.200793760420743e+34,
        "filterflow_gradient_max_abs": 0.6534447816938739,
        "gradient_delta": [
          -3.322518998548542e+34,
          8.200793760420743e+34
        ],
        "gradient_explosion_ratio": 8.200793760420743e+34,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.200793760420743e+34,
        "relative_gradient_delta": 8.200793760420743e+34,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.903298934597842e-09,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.0648880863423647e+36,
        "filterflow_gradient_max_abs": 262.5095687458148,
        "gradient_delta": [
          -1.6468732525658843e+36,
          4.0648880863423647e+36
        ],
        "gradient_explosion_ratio": 1.548472349317808e+34,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.0648880863423647e+36,
        "relative_gradient_delta": 1.548472349317808e+34,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.970814705349767e-09,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4291520761050965e+37,
        "filterflow_gradient_max_abs": 28.548993251385596,
        "gradient_delta": [
          9.841613091375687e+36,
          -2.4291520761050965e+37
        ],
        "gradient_explosion_ratio": 8.50871361632761e+35,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4291520761050965e+37,
        "relative_gradient_delta": 8.50871361632761e+35,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9090827524669294e-09,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.8299285132446198e+40,
        "filterflow_gradient_max_abs": 485.70702239538065,
        "gradient_delta": [
          -7.413882642171301e+39,
          1.8299285132446198e+40
        ],
        "gradient_explosion_ratio": 3.767556219837812e+37,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.8299285132446198e+40,
        "relative_gradient_delta": 3.767556219837812e+37,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8526088158287166e-09,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.003851951179119e+41,
        "filterflow_gradient_max_abs": 245.11951564783823,
        "gradient_delta": [
          1.622144704988396e+41,
          -4.003851951179119e+41
        ],
        "gradient_explosion_ratio": 1.6334284688010846e+39,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.003851951179119e+41,
        "relative_gradient_delta": 1.6334284688010846e+39,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8581510491676454e-09,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.86649945520109e+44,
        "filterflow_gradient_max_abs": 434.75519438634416,
        "gradient_delta": [
          -3.997373040557122e+44,
          9.86649945520109e+44
        ],
        "gradient_explosion_ratio": 2.2694379693674802e+42,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.86649945520109e+44,
        "relative_gradient_delta": 2.2694379693674802e+42,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9084219477226725e-09,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1616020221855888e+45,
        "filterflow_gradient_max_abs": 251.90780939902413,
        "gradient_delta": [
          -8.757644681512122e+44,
          2.1616020221855888e+45
        ],
        "gradient_explosion_ratio": 8.580925011187694e+42,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1616020221855888e+45,
        "relative_gradient_delta": 8.580925011187694e+42,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.980804936214554e-09,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.8622136488121697e+48,
        "filterflow_gradient_max_abs": 369.7748801823844,
        "gradient_delta": [
          1.1596144841466624e+48,
          -2.8622136488121697e+48
        ],
        "gradient_explosion_ratio": 7.740422084378575e+45,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.8622136488121697e+48,
        "relative_gradient_delta": 7.740422084378575e+45,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9715820915043878e-09,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0279953407103826e+50,
        "filterflow_gradient_max_abs": 153.94165873710156,
        "gradient_delta": [
          -4.164882265926444e+49,
          1.0279953407103826e+50
        ],
        "gradient_explosion_ratio": 6.677824242922913e+47,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0279953407103826e+50,
        "relative_gradient_delta": 6.677824242922913e+47,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.075740551139461e-09,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.1500430497089456e+51,
        "filterflow_gradient_max_abs": 231.88010181357106,
        "gradient_delta": [
          1.6813734475313795e+51,
          -4.1500430497089456e+51
        ],
        "gradient_explosion_ratio": 1.789736599755995e+49,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.1500430497089456e+51,
        "relative_gradient_delta": 1.789736599755995e+49,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8847040312030003e-09,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.631019379844697e+54,
        "filterflow_gradient_max_abs": 317.10552544548756,
        "gradient_delta": [
          3.4968231983563215e+54,
          -8.631019379844697e+54
        ],
        "gradient_explosion_ratio": 2.7218129888211056e+52,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.631019379844697e+54,
        "relative_gradient_delta": 2.7218129888211056e+52,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8788775807697675e-09,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1210658164264935e+57,
        "filterflow_gradient_max_abs": 440.433114763931,
        "gradient_delta": [
          4.541953599268763e+56,
          -1.1210658164264935e+57
        ],
        "gradient_explosion_ratio": 2.5453713148417026e+54,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1210658164264935e+57,
        "relative_gradient_delta": 2.5453713148417026e+54,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.7967104188064695e-09,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6339930416104748e+58,
        "filterflow_gradient_max_abs": 274.3754691050723,
        "gradient_delta": [
          6.620057866164943e+57,
          -1.6339930416104748e+58
        ],
        "gradient_explosion_ratio": 5.955317532358318e+55,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6339930416104748e+58,
        "relative_gradient_delta": 5.955317532358318e+55,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9457680739142234e-09,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0801958903111277e+61,
        "filterflow_gradient_max_abs": 184.24153726601756,
        "gradient_delta": [
          4.376370717959233e+60,
          -1.0801958903111277e+61
        ],
        "gradient_explosion_ratio": 5.862933550926057e+58,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0801958903111277e+61,
        "relative_gradient_delta": 5.862933550926057e+58,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8393571938067907e-09,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.800408438052669e+63,
        "filterflow_gradient_max_abs": 187.1386096136716,
        "gradient_delta": [
          2.3500124253560894e+63,
          -5.800408438052669e+63
        ],
        "gradient_explosion_ratio": 3.099525239621591e+61,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.800408438052669e+63,
        "relative_gradient_delta": 3.099525239621591e+61,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.6310544853913598e-09,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.015333023554408e+66,
        "filterflow_gradient_max_abs": 954.1501022077981,
        "gradient_delta": [
          1.221650190261149e+66,
          -3.015333023554408e+66
        ],
        "gradient_explosion_ratio": 3.1602292098248064e+63,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.015333023554408e+66,
        "relative_gradient_delta": 3.1602292098248064e+63,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.98600263906701e-09,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6303771785244939e+68,
        "filterflow_gradient_max_abs": 422.91186590476366,
        "gradient_delta": [
          -6.605408340582072e+67,
          1.6303771785244939e+68
        ],
        "gradient_explosion_ratio": 3.8551228044560035e+65,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6303771785244939e+68,
        "relative_gradient_delta": 3.8551228044560035e+65,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5840096163374255e-09,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6947969273417298e+70,
        "filterflow_gradient_max_abs": 354.26740709319216,
        "gradient_delta": [
          6.866402392596887e+69,
          -1.6947969273417298e+70
        ],
        "gradient_explosion_ratio": 4.783948208071829e+67,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6947969273417298e+70,
        "relative_gradient_delta": 4.783948208071829e+67,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.941782094647351e-09,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.1671358478171934e+71,
        "filterflow_gradient_max_abs": 199.05378088782396,
        "gradient_delta": [
          1.2831525011814236e+71,
          -3.1671358478171934e+71
        ],
        "gradient_explosion_ratio": 1.5910955489973945e+69,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.1671358478171934e+71,
        "relative_gradient_delta": 1.5910955489973945e+69,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.940716280543711e-09,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6940673287639515e+75,
        "filterflow_gradient_max_abs": 548.7404094827189,
        "gradient_delta": [
          -6.863446452956383e+74,
          1.6940673287639515e+75
        ],
        "gradient_explosion_ratio": 3.0871925950576487e+72,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6940673287639515e+75,
        "relative_gradient_delta": 3.0871925950576487e+72,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.836934408558591e-09,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4043118576360645e+76,
        "filterflow_gradient_max_abs": 399.4756572109477,
        "gradient_delta": [
          -9.740973933505658e+75,
          2.4043118576360645e+76
        ],
        "gradient_explosion_ratio": 6.018669258653826e+73,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4043118576360645e+76,
        "relative_gradient_delta": 6.018669258653826e+73,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.73063721528888e-09,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5008573023433146e+79,
        "filterflow_gradient_max_abs": 381.20393707705813,
        "gradient_delta": [
          -6.080663709911625e+78,
          1.5008573023433146e+79
        ],
        "gradient_explosion_ratio": 3.937150581002329e+76,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5008573023433146e+79,
        "relative_gradient_delta": 3.937150581002329e+76,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.649024276659475e-09,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.955876054262049e+81,
        "filterflow_gradient_max_abs": 48.850988576799736,
        "gradient_delta": [
          1.1975614354599504e+81,
          -2.955876054262049e+81
        ],
        "gradient_explosion_ratio": 6.050800895492729e+79,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.955876054262049e+81,
        "relative_gradient_delta": 6.050800895492729e+79,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.737742642646481e-09,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.993065952021782e+81,
        "filterflow_gradient_max_abs": 346.85073969207997,
        "gradient_delta": [
          2.02292082586738e+81,
          -4.993065952021782e+81
        ],
        "gradient_explosion_ratio": 1.4395431177267846e+79,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.993065952021782e+81,
        "relative_gradient_delta": 1.4395431177267846e+79,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.721428581433429e-09,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.506044256947092e+84,
        "filterflow_gradient_max_abs": 322.6295207830076,
        "gradient_delta": [
          -2.2307519473111903e+84,
          5.506044256947092e+84
        ],
        "gradient_explosion_ratio": 1.70661514283757e+82,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.506044256947092e+84,
        "relative_gradient_delta": 1.70661514283757e+82,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6360639771592105e-09,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3987808152939903e+87,
        "filterflow_gradient_max_abs": 86.66552831338745,
        "gradient_delta": [
          -9.718565135284211e+86,
          2.3987808152939903e+87
        ],
        "gradient_explosion_ratio": 2.7678603730653588e+85,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3987808152939903e+87,
        "relative_gradient_delta": 2.7678603730653588e+85,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.636163453142217e-09,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.758406874892496e+90,
        "filterflow_gradient_max_abs": 1118.3947944525503,
        "gradient_delta": [
          3.5484337356821645e+90,
          -8.758406874892496e+90
        ],
        "gradient_explosion_ratio": 7.831230007807485e+87,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.758406874892496e+90,
        "relative_gradient_delta": 7.831230007807485e+87,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9218832625920186e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.210818201386663e+91,
        "filterflow_gradient_max_abs": 72.987643547552,
        "gradient_delta": [
          2.1111422842563557e+91,
          -5.210818201386663e+91
        ],
        "gradient_explosion_ratio": 7.139315571945785e+89,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.210818201386663e+91,
        "relative_gradient_delta": 7.139315571945785e+89,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9393910356011475e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.549792487473955e+94,
        "filterflow_gradient_max_abs": 7.513193750877159,
        "gradient_delta": [
          -1.4381843178960913e+94,
          3.549792487473955e+94
        ],
        "gradient_explosion_ratio": 4.724745035437852e+93,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.549792487473955e+94,
        "relative_gradient_delta": 4.724745035437852e+93,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.889368827003636e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3734136386902628e+96,
        "filterflow_gradient_max_abs": 330.52600026078443,
        "gradient_delta": [
          -5.564330771781317e+95,
          1.3734136386902628e+96
        ],
        "gradient_explosion_ratio": 4.1552363130484195e+93,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3734136386902628e+96,
        "relative_gradient_delta": 4.1552363130484195e+93,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.899515377270291e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.303432416046784e+98,
        "filterflow_gradient_max_abs": 286.4569368626525,
        "gradient_delta": [
          1.3383725140983852e+98,
          -3.303432416046784e+98
        ],
        "gradient_explosion_ratio": 1.1532038470517753e+96,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.303432416046784e+98,
        "relative_gradient_delta": 1.1532038470517753e+96,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.8836134308439796e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.964949116168511e+101,
        "filterflow_gradient_max_abs": 609.6787100623405,
        "gradient_delta": [
          -1.2012373504310952e+101,
          2.964949116168511e+101
        ],
        "gradient_explosion_ratio": 4.86313375755788e+98,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.964949116168511e+101,
        "relative_gradient_delta": 4.86313375755788e+98,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.874831122629985e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2635063583909613e+103,
        "filterflow_gradient_max_abs": 237.18680047332637,
        "gradient_delta": [
          -5.119045793837289e+102,
          1.2635063583909613e+103
        ],
        "gradient_explosion_ratio": 5.327051740946491e+100,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2635063583909613e+103,
        "relative_gradient_delta": 5.327051740946491e+100,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.782176349886868e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.771445494233453e+105,
        "filterflow_gradient_max_abs": 20.398532585564105,
        "gradient_delta": [
          7.176941015014571e+104,
          -1.771445494233453e+105
        ],
        "gradient_explosion_ratio": 8.684181015486831e+103,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.771445494233453e+105,
        "relative_gradient_delta": 8.684181015486831e+103,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.6820893001277e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.627896654555355e+107,
        "filterflow_gradient_max_abs": 478.6428510468603,
        "gradient_delta": [
          3.4955580386163824e+107,
          -8.627896654555355e+107
        ],
        "gradient_explosion_ratio": 1.802575058978717e+105,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.627896654555355e+107,
        "relative_gradient_delta": 1.802575058978717e+105,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.958078309551638e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.453651754830162e+109,
        "filterflow_gradient_max_abs": 310.27237965253573,
        "gradient_delta": [
          3.019817384447614e+109,
          -7.453651754830162e+109
        ],
        "gradient_explosion_ratio": 2.40229303142525e+107,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.453651754830162e+109,
        "relative_gradient_delta": 2.40229303142525e+107,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.521620328683639e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.178492593549796e+109,
        "filterflow_gradient_max_abs": 291.33394004387503,
        "gradient_delta": [
          -3.313483769425247e+109,
          8.178492593549796e+109
        ],
        "gradient_explosion_ratio": 2.807257057766119e+107,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.178492593549796e+109,
        "relative_gradient_delta": 2.807257057766119e+107,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.524789349285129e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4019894641397568e+115,
        "filterflow_gradient_max_abs": 772.789629727978,
        "gradient_delta": [
          -5.68010459286357e+114,
          1.4019894641397568e+115
        ],
        "gradient_explosion_ratio": 1.8141929060736196e+112,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4019894641397568e+115,
        "relative_gradient_delta": 1.8141929060736196e+112,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.415127818901965e-09,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2172912927567188e+117,
        "filterflow_gradient_max_abs": 137.0827775975205,
        "gradient_delta": [
          -4.9318072922058835e+116,
          1.2172912927567188e+117
        ],
        "gradient_explosion_ratio": 8.879972481522994e+114,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2172912927567188e+117,
        "relative_gradient_delta": 8.879972481522994e+114,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.988418484368594e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.843184623487847e+118,
        "filterflow_gradient_max_abs": 205.40967733109431,
        "gradient_delta": [
          -2.7724890524435387e+118,
          6.843184623487847e+118
        ],
        "gradient_explosion_ratio": 3.331481122214852e+116,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.843184623487847e+118,
        "relative_gradient_delta": 3.331481122214852e+116,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.800110448537453e-09,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.572735838046671e+121,
        "filterflow_gradient_max_abs": 1075.2940301638955,
        "gradient_delta": [
          3.4732098530407318e+121,
          -8.572735838046671e+121
        ],
        "gradient_explosion_ratio": 7.972457390784567e+118,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.572735838046671e+121,
        "relative_gradient_delta": 7.972457390784567e+118,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.299266720408923e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.75648919820155e+124,
        "filterflow_gradient_max_abs": 1320.7702359098546,
        "gradient_delta": [
          -2.737364745453753e+124,
          6.75648919820155e+124
        ],
        "gradient_explosion_ratio": 5.115567427628415e+121,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.75648919820155e+124,
        "relative_gradient_delta": 5.115567427628415e+121,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.148105858803319e-09,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.127090213235036e+126,
        "filterflow_gradient_max_abs": 352.8826174689448,
        "gradient_delta": [
          -8.617821459196857e+125,
          2.127090213235036e+126
        ],
        "gradient_explosion_ratio": 6.027755712343155e+123,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.127090213235036e+126,
        "relative_gradient_delta": 6.027755712343155e+123,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.5889797800336964e-09,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.312280259557478e+127,
        "filterflow_gradient_max_abs": 974.6366511077524,
        "gradient_delta": [
          1.341957182731605e+127,
          -3.312280259557478e+127
        ],
        "gradient_explosion_ratio": 3.398477017863844e+124,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.312280259557478e+127,
        "relative_gradient_delta": 3.398477017863844e+124,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.8240451633319026e-09,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.503362178841397e+130,
        "filterflow_gradient_max_abs": 731.310897142959,
        "gradient_delta": [
          -6.090812117489031e+129,
          1.503362178841397e+130
        ],
        "gradient_explosion_ratio": 2.0557087070829124e+127,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.503362178841397e+130,
        "relative_gradient_delta": 2.0557087070829124e+127,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.972274953412125e-09,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.714433954742316e+132,
        "filterflow_gradient_max_abs": 483.3559108394908,
        "gradient_delta": [
          1.504888154003782e+132,
          -3.714433954742316e+132
        ],
        "gradient_explosion_ratio": 7.684676801181765e+129,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.714433954742316e+132,
        "relative_gradient_delta": 7.684676801181765e+129,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.955818783651921e-09,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4409369910656486e+134,
        "filterflow_gradient_max_abs": 1076.6780654517022,
        "gradient_delta": [
          5.837898950261389e+133,
          -1.4409369910656486e+134
        ],
        "gradient_explosion_ratio": 1.3383174017398856e+131,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4409369910656486e+134,
        "relative_gradient_delta": 1.3383174017398856e+131,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5558010697277496e-09,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.057454315163704e+136,
        "filterflow_gradient_max_abs": 18.05494027199655,
        "gradient_delta": [
          -2.04900751528725e+136,
          5.057454315163704e+136
        ],
        "gradient_explosion_ratio": 2.8011470760763923e+135,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.057454315163704e+136,
        "relative_gradient_delta": 2.8011470760763923e+135,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6730690428375965e-09,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.479676376477054e+140,
        "filterflow_gradient_max_abs": 989.4278480713913,
        "gradient_delta": [
          1.0046310286279417e+140,
          -2.479676376477054e+140
        ],
        "gradient_explosion_ratio": 2.5061720077017028e+137,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.479676376477054e+140,
        "relative_gradient_delta": 2.5061720077017028e+137,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.355683813628275e-09,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.133770688204893e+142,
        "filterflow_gradient_max_abs": 778.7073741209738,
        "gradient_delta": [
          -1.2696347393720104e+142,
          3.133770688204893e+142
        ],
        "gradient_explosion_ratio": 4.0243238889863845e+139,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.133770688204893e+142,
        "relative_gradient_delta": 4.0243238889863845e+139,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.821792577378801e-09,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.7596696025526025e+145,
        "filterflow_gradient_max_abs": 1097.9215016104433,
        "gradient_delta": [
          1.5232151969281706e+145,
          -3.7596696025526025e+145
        ],
        "gradient_explosion_ratio": 3.424351920458683e+142,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.7596696025526025e+145,
        "relative_gradient_delta": 3.424351920458683e+142,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0083482493428164e-08,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.938430186805951e+148,
        "filterflow_gradient_max_abs": 1697.7646785016034,
        "gradient_delta": [
          -2.000785362736247e+148,
          4.938430186805951e+148
        ],
        "gradient_explosion_ratio": 2.908783678527499e+145,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.938430186805951e+148,
        "relative_gradient_delta": 2.908783678527499e+145,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8990448324984754e-08,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.482685612125212e+151,
        "filterflow_gradient_max_abs": 947.0739014815089,
        "gradient_delta": [
          6.007041829214218e+150,
          -1.482685612125212e+151
        ],
        "gradient_explosion_ratio": 1.56554373402735e+148,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.482685612125212e+151,
        "relative_gradient_delta": 1.56554373402735e+148,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1565390423129429e-08,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.753775402370604e+152,
        "filterflow_gradient_max_abs": 249.89093531615012,
        "gradient_delta": [
          -3.5465573129973896e+152,
          8.753775402370604e+152
        ],
        "gradient_explosion_ratio": 3.503038392047212e+150,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.753775402370604e+152,
        "relative_gradient_delta": 3.503038392047212e+150,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.132605782724568e-09,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.45988891478152e+155,
        "filterflow_gradient_max_abs": 974.2890696675929,
        "gradient_delta": [
          3.8326363961514926e+155,
          -9.45988891478152e+155
        ],
        "gradient_explosion_ratio": 9.709529963226454e+152,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.45988891478152e+155,
        "relative_gradient_delta": 9.709529963226454e+152,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.223679515140248e-09,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.897635888584225e+158,
        "filterflow_gradient_max_abs": 1029.3299119039873,
        "gradient_delta": [
          -3.60484181722332e+158,
          8.897635888584225e+158
        ],
        "gradient_explosion_ratio": 8.644105049008008e+155,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.897635888584225e+158,
        "relative_gradient_delta": 8.644105049008008e+155,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.178016403486254e-09,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.199099673826291e+162,
        "filterflow_gradient_max_abs": 1426.254117759735,
        "gradient_delta": [
          4.858104671122537e+161,
          -1.199099673826291e+162
        ],
        "gradient_explosion_ratio": 8.407335403243266e+158,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.199099673826291e+162,
        "relative_gradient_delta": 8.407335403243266e+158,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.153612730486202e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0759555069461506e+165,
        "filterflow_gradient_max_abs": 1942.7454564725651,
        "gradient_delta": [
          -4.3591909732871234e+164,
          1.0759555069461506e+165
        ],
        "gradient_explosion_ratio": 5.538324659884978e+161,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0759555069461506e+165,
        "relative_gradient_delta": 5.538324659884978e+161,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.01524527357833e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.8302753422555064e+166,
        "filterflow_gradient_max_abs": 169.06130724664092,
        "gradient_delta": [
          -7.415287806124401e+165,
          1.8302753422555064e+166
        ],
        "gradient_explosion_ratio": 1.0826104281716845e+164,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.8302753422555064e+166,
        "relative_gradient_delta": 1.0826104281716845e+164,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.081496278260602e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.7957959929518356e+170,
        "filterflow_gradient_max_abs": 1963.5208371745916,
        "gradient_delta": [
          1.5378516604165844e+170,
          -3.7957959929518356e+170
        ],
        "gradient_explosion_ratio": 1.933157988999901e+167,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.7957959929518356e+170,
        "relative_gradient_delta": 1.933157988999901e+167,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.653859933678177e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.9077103925812736e+172,
        "filterflow_gradient_max_abs": 1119.9768301540837,
        "gradient_delta": [
          -7.729012834916906e+171,
          1.9077103925812736e+172
        ],
        "gradient_explosion_ratio": 1.7033480882982333e+169,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.9077103925812736e+172,
        "relative_gradient_delta": 1.7033480882982333e+169,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.3080741458397824e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.590076492108922e+175,
        "filterflow_gradient_max_abs": 979.6868013870265,
        "gradient_delta": [
          6.442131711292206e+174,
          -1.590076492108922e+175
        ],
        "gradient_explosion_ratio": 1.6230457426370494e+172,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.590076492108922e+175,
        "relative_gradient_delta": 1.6230457426370494e+172,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.394845624730806e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.380924681059328e+178,
        "filterflow_gradient_max_abs": 2882.4178802677957,
        "gradient_delta": [
          -1.3697681972805792e+178,
          3.380924681059328e+178
        ],
        "gradient_explosion_ratio": 1.1729474425634695e+175,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.380924681059328e+178,
        "relative_gradient_delta": 1.1729474425634695e+175,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.620751946684322e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.928019960544454e+179,
        "filterflow_gradient_max_abs": 858.8073873147812,
        "gradient_delta": [
          3.617151803218611e+179,
          -8.928019960544454e+179
        ],
        "gradient_explosion_ratio": 1.0395835075964526e+177,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.928019960544454e+179,
        "relative_gradient_delta": 1.0395835075964526e+177,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.615852837261627e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.458104325456408e+182,
        "filterflow_gradient_max_abs": 442.0116504772855,
        "gradient_delta": [
          -2.2113292746016655e+182,
          5.458104325456408e+182
        ],
        "gradient_explosion_ratio": 1.234832683609749e+180,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.458104325456408e+182,
        "relative_gradient_delta": 1.234832683609749e+180,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.274422841874184e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.3633431852773435e+186,
        "filterflow_gradient_max_abs": 3282.5855155180925,
        "gradient_delta": [
          2.5780832008490654e+186,
          -6.3633431852773435e+186
        ],
        "gradient_explosion_ratio": 1.9385155863252546e+183,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.3633431852773435e+186,
        "relative_gradient_delta": 1.9385155863252546e+183,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0136062655874412e-08,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2851702063607572e+188,
        "filterflow_gradient_max_abs": 1855.9144036285215,
        "gradient_delta": [
          -5.206816012872294e+187,
          1.2851702063607572e+188
        ],
        "gradient_explosion_ratio": 6.924727799127508e+184,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2851702063607572e+188,
        "relative_gradient_delta": 6.924727799127508e+184,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.873637741795392e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.53020123406057e+190,
        "filterflow_gradient_max_abs": 1310.8611477302254,
        "gradient_delta": [
          2.2405390505784774e+190,
          -5.53020123406057e+190
        ],
        "gradient_explosion_ratio": 4.218754399454276e+187,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.53020123406057e+190,
        "relative_gradient_delta": 4.218754399454276e+187,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.93335175330867e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.46750558729645e+193,
        "filterflow_gradient_max_abs": 914.416967723082,
        "gradient_delta": [
          -3.835722260748977e+193,
          9.46750558729645e+193
        ],
        "gradient_explosion_ratio": 1.0353597889670335e+191,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.46750558729645e+193,
        "relative_gradient_delta": 1.0353597889670335e+191,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.058265166255296e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.6287413626715912e+197,
        "filterflow_gradient_max_abs": 3551.3298618369327,
        "gradient_delta": [
          1.0650241153362141e+197,
          -2.6287413626715912e+197
        ],
        "gradient_explosion_ratio": 7.402132341803556e+193,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.6287413626715912e+197,
        "relative_gradient_delta": 7.402132341803556e+193,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.786315675024525e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.315062245142296e+199,
        "filterflow_gradient_max_abs": 3023.0985131010166,
        "gradient_delta": [
          -3.3688144209813485e+199,
          8.315062245142296e+199
        ],
        "gradient_explosion_ratio": 2.7505098524271774e+196,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.315062245142296e+199,
        "relative_gradient_delta": 2.7505098524271774e+196,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.745331570025883e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.303992517808491e+202,
        "filterflow_gradient_max_abs": 2001.070628323309,
        "gradient_delta": [
          9.334534115316838e+201,
          -2.303992517808491e+202
        ],
        "gradient_explosion_ratio": 1.1513799089335489e+199,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.303992517808491e+202,
        "relative_gradient_delta": 1.1513799089335489e+199,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.205052720062668e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.224308699856436e+205,
        "filterflow_gradient_max_abs": 2346.9001573329506,
        "gradient_delta": [
          -1.3063158549555854e+205,
          3.224308699856436e+205
        ],
        "gradient_explosion_ratio": 1.3738584872398598e+202,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.224308699856436e+205,
        "relative_gradient_delta": 1.3738584872398598e+202,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.456598728414974e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.751597607904007e+208,
        "filterflow_gradient_max_abs": 4046.6212127655212,
        "gradient_delta": [
          2.330236911516621e+208,
          -5.751597607904007e+208
        ],
        "gradient_explosion_ratio": 1.4213333310664083e+205,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.751597607904007e+208,
        "relative_gradient_delta": 1.4213333310664083e+205,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.6329352092725458e-08,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.149344864086458e+211,
        "filterflow_gradient_max_abs": 2730.4139020142047,
        "gradient_delta": [
          -4.6565250369319974e+210,
          1.149344864086458e+211
        ],
        "gradient_explosion_ratio": 4.2094162472531926e+207,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.149344864086458e+211,
        "relative_gradient_delta": 4.2094162472531926e+207,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.300094916397939e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_raw_transport_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      3.711418912951682e+232,
      -3.0135023214837034e+232
    ],
    "final_bayesfilter_gradient_max_abs": 3.711418912951682e+232,
    "final_filterflow_gradient_diag": [
      18935.6850725171,
      2073.5151524806142
    ],
    "final_filterflow_gradient_max_abs": 18935.6850725171,
    "final_gradient_delta": [
      3.711418912951682e+232,
      -3.0135023214837034e+232
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 3.711418912951682e+232,
    "final_relative_gradient_delta": 1.960013011801916e+228,
    "final_scalar_delta": 9.3001517598168e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "bayesfilter_gradient_max_abs": 10507308.455697542,
      "filterflow_gradient_max_abs": 8.578663144440544,
      "gradient_explosion_ratio": 1224818.864989106,
      "resampling_flag": [
        true
      ],
      "status": "explosion",
      "time_index": 8,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 1.0059319506252606,
      "max_abs_gradient_delta": 0.05220128095433019,
      "relative_gradient_delta": 0.005931950625260563,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.7926993223227328e-11,
      "status": "failure",
      "time_index": 1,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_scalar_failure": {
      "status": "no_failure"
    },
    "mode": "proposal_log_prob_stop_gradient",
    "mode_description": "Stop gradient through proposal log probability",
    "sample_rows": [
      {
        "bayesfilter_gradient_max_abs": 0.008913771203554865,
        "filterflow_gradient_max_abs": 0.008913771203554867,
        "gradient_delta": [
          -1.734723475976807e-18,
          -5.766308833278761e-19
        ],
        "gradient_explosion_ratio": 0.008913771203554865,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 1.734723475976807e-18,
        "relative_gradient_delta": 1.734723475976807e-18,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.852220743698464,
        "filterflow_gradient_max_abs": 8.800019462744133,
        "gradient_delta": [
          -0.05220128095433019,
          0.03535723378440208
        ],
        "gradient_explosion_ratio": 1.0059319506252606,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.05220128095433019,
        "relative_gradient_delta": 0.005931950625260563,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7926993223227328e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.033623704741912,
        "filterflow_gradient_max_abs": 1.4485716238559057,
        "gradient_delta": [
          -7.482195328597818,
          -1.0154401349116362
        ],
        "gradient_explosion_ratio": 4.1652229032909025,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.482195328597818,
        "relative_gradient_delta": 5.1652229032909025,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4985346297180513e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 118.73925036371355,
        "filterflow_gradient_max_abs": 16.840076774872443,
        "gradient_delta": [
          -135.579327138586,
          103.05266320945421
        ],
        "gradient_explosion_ratio": 7.050992222368473,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 135.579327138586,
        "relative_gradient_delta": 8.050992222368473,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.4439117396468646e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 484.3298090358302,
        "filterflow_gradient_max_abs": 11.278780998887767,
        "gradient_delta": [
          -473.0510280369424,
          417.36798351539386
        ],
        "gradient_explosion_ratio": 42.941680407092875,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 473.0510280369424,
        "relative_gradient_delta": 41.94168040709287,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.665601073204016e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13379.159809137533,
        "filterflow_gradient_max_abs": 0.16051708831084313,
        "gradient_delta": [
          -13379.320326225843,
          10962.12104851948
        ],
        "gradient_explosion_ratio": 13379.159809137533,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13379.320326225843,
        "relative_gradient_delta": 13379.320326225843,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.347366828165832e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 132185.01267551768,
        "filterflow_gradient_max_abs": 6.732984884221974,
        "gradient_delta": [
          -132191.7456604019,
          110566.32232819559
        ],
        "gradient_explosion_ratio": 19632.45350294474,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 132191.7456604019,
        "relative_gradient_delta": 19633.453502944743,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.53681536782824e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 687741.9539166507,
        "filterflow_gradient_max_abs": 16.75562828027451,
        "gradient_delta": [
          687758.709544931,
          -568315.8047401941
        ],
        "gradient_explosion_ratio": 41045.42917834313,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 687758.709544931,
        "relative_gradient_delta": 41046.429178343125,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.6477489351891563e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10507308.455697542,
        "filterflow_gradient_max_abs": 8.578663144440544,
        "gradient_delta": [
          10507299.877034398,
          -9078268.994187659
        ],
        "gradient_explosion_ratio": 1224818.864989106,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10507299.877034398,
        "relative_gradient_delta": 1224817.864989106,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.839595473844383e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 313395180.4660868,
        "filterflow_gradient_max_abs": 56.8762754108451,
        "gradient_delta": [
          -313395237.3423622,
          255462227.14382806
        ],
        "gradient_explosion_ratio": 5510121.367868772,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 313395237.3423622,
        "relative_gradient_delta": 5510122.367868772,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.645795108146558e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 58170262851.63072,
        "filterflow_gradient_max_abs": 104.45156511568617,
        "gradient_delta": [
          58170262747.17915,
          -47395967876.48537
        ],
        "gradient_explosion_ratio": 556911356.8303528,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 58170262747.17915,
        "relative_gradient_delta": 556911355.8303527,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.562661608062626e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1953444659534.2131,
        "filterflow_gradient_max_abs": 9.13071410440192,
        "gradient_delta": [
          1953444659543.3438,
          -1600304134205.1963
        ],
        "gradient_explosion_ratio": 213942155804.92844,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1953444659543.3438,
        "relative_gradient_delta": 213942155805.92844,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.412914561020443e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5780114336150.3545,
        "filterflow_gradient_max_abs": 62.46161279976278,
        "gradient_delta": [
          -5780114336212.816,
          4648132897126.474
        ],
        "gradient_explosion_ratio": 92538666183.34111,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5780114336212.816,
        "relative_gradient_delta": 92538666184.34111,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.171952003976912e-11,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 651197396761222.6,
        "filterflow_gradient_max_abs": 78.21898890138324,
        "gradient_delta": [
          651197396761144.4,
          -532756113707864.5
        ],
        "gradient_explosion_ratio": 8325310847245.006,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 651197396761144.4,
        "relative_gradient_delta": 8325310847244.006,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1748113593057496e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.989080854202397e+16,
        "filterflow_gradient_max_abs": 55.1203162059954,
        "gradient_delta": [
          8.989080854202392e+16,
          -7.319297220407389e+16
        ],
        "gradient_explosion_ratio": 1630810828553385.5,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.989080854202392e+16,
        "relative_gradient_delta": 1630810828553384.8,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1169021263413015e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.521662265102552e+18,
        "filterflow_gradient_max_abs": 3.2014311273644616,
        "gradient_delta": [
          -5.521662265102552e+18,
          4.4846630218317983e+18
        ],
        "gradient_explosion_ratio": 1.724748103404677e+18,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.521662265102552e+18,
        "relative_gradient_delta": 1.724748103404677e+18,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.603695616533514e-11,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.1027776008943575e+19,
        "filterflow_gradient_max_abs": 25.054390338542845,
        "gradient_delta": [
          4.1027776008943575e+19,
          -3.3342190140776456e+19
        ],
        "gradient_explosion_ratio": 1.6375483679532127e+18,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.1027776008943575e+19,
        "relative_gradient_delta": 1.6375483679532127e+18,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1939249588976963e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.4979554297475257e+21,
        "filterflow_gradient_max_abs": 145.3600680670563,
        "gradient_delta": [
          -4.4979554297475257e+21,
          3.652309481561789e+21
        ],
        "gradient_explosion_ratio": 3.0943542401703928e+19,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.4979554297475257e+21,
        "relative_gradient_delta": 3.0943542401703928e+19,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.48947520983711e-09,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2986940029761342e+24,
        "filterflow_gradient_max_abs": 168.66458545141114,
        "gradient_delta": [
          1.2986940029761342e+24,
          -1.0544731195972697e+24
        ],
        "gradient_explosion_ratio": 7.699861826359878e+21,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2986940029761342e+24,
        "relative_gradient_delta": 7.699861826359878e+21,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.252356523513299e-09,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.769795514170296e+25,
        "filterflow_gradient_max_abs": 101.15910809775511,
        "gradient_delta": [
          1.769795514170296e+25,
          -1.4370051257200713e+25
        ],
        "gradient_explosion_ratio": 1.7495167241491038e+23,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.769795514170296e+25,
        "relative_gradient_delta": 1.7495167241491038e+23,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.767464479802584e-09,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7617860351760577e+27,
        "filterflow_gradient_max_abs": 125.28072286451086,
        "gradient_delta": [
          -1.7617860351760577e+27,
          1.4304799093238545e+27
        ],
        "gradient_explosion_ratio": 1.406270649540713e+25,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7617860351760577e+27,
        "relative_gradient_delta": 1.406270649540713e+25,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9853310934413457e-09,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.439531878989388e+30,
        "filterflow_gradient_max_abs": 278.9526477486435,
        "gradient_delta": [
          4.439531878989388e+30,
          -3.604694796995738e+30
        ],
        "gradient_explosion_ratio": 1.5915001756820485e+28,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.439531878989388e+30,
        "relative_gradient_delta": 1.5915001756820485e+28,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.0152165209074155e-09,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.152352826870279e+32,
        "filterflow_gradient_max_abs": 252.28215416061428,
        "gradient_delta": [
          -7.152352826870279e+32,
          5.807378409386588e+32
        ],
        "gradient_explosion_ratio": 2.835060946212139e+30,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.152352826870279e+32,
        "relative_gradient_delta": 2.835060946212139e+30,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.021582983819826e-09,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3718004064716017e+34,
        "filterflow_gradient_max_abs": 69.58591013728201,
        "gradient_delta": [
          -3.3718004064716017e+34,
          2.7377450745911802e+34
        ],
        "gradient_explosion_ratio": 4.845521744013367e+32,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3718004064716017e+34,
        "relative_gradient_delta": 4.845521744013367e+32,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9725839567618095e-09,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3104626374692797e+36,
        "filterflow_gradient_max_abs": 64.72471139759364,
        "gradient_delta": [
          2.3104626374692797e+36,
          -1.8759907158098694e+36
        ],
        "gradient_explosion_ratio": 3.5696762296497146e+34,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3104626374692797e+36,
        "relative_gradient_delta": 3.5696762296497146e+34,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.974680057832302e-09,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.958273048917215e+38,
        "filterflow_gradient_max_abs": 0.6534447816938739,
        "gradient_delta": [
          -3.958273048917215e+38,
          3.21393654606172e+38
        ],
        "gradient_explosion_ratio": 3.958273048917215e+38,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.958273048917215e+38,
        "relative_gradient_delta": 3.958273048917215e+38,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.903298934597842e-09,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.8356474235433043e+40,
        "filterflow_gradient_max_abs": 262.5095687458148,
        "gradient_delta": [
          2.8356474235433043e+40,
          -2.3024146639610743e+40
        ],
        "gradient_explosion_ratio": 1.0802072614309275e+38,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.8356474235433043e+40,
        "relative_gradient_delta": 1.0802072614309275e+38,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.970814705349767e-09,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.3968326022006136e+42,
        "filterflow_gradient_max_abs": 28.548993251385596,
        "gradient_delta": [
          4.3968326022006136e+42,
          -3.5700243926572466e+42
        ],
        "gradient_explosion_ratio": 1.5401007536359335e+41,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.3968326022006136e+42,
        "relative_gradient_delta": 1.5401007536359335e+41,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9090827524669294e-09,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2186234761245253e+44,
        "filterflow_gradient_max_abs": 485.70702239538065,
        "gradient_delta": [
          2.2186234761245253e+44,
          -1.801420717574852e+44
        ],
        "gradient_explosion_ratio": 4.567822522274543e+41,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2186234761245253e+44,
        "relative_gradient_delta": 4.567822522274543e+41,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8526088158287166e-09,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.766688839459076e+45,
        "filterflow_gradient_max_abs": 245.11951564783823,
        "gradient_delta": [
          -7.766688839459076e+45,
          6.306195131922029e+45
        ],
        "gradient_explosion_ratio": 3.1685314076001325e+43,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.766688839459076e+45,
        "relative_gradient_delta": 3.1685314076001325e+43,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8581510491676454e-09,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.869482957898164e+49,
        "filterflow_gradient_max_abs": 434.75519438634416,
        "gradient_delta": [
          1.869482957898164e+49,
          -1.517934617542802e+49
        ],
        "gradient_explosion_ratio": 4.3000819358511274e+46,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.869482957898164e+49,
        "relative_gradient_delta": 4.3000819358511274e+46,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9084219477226725e-09,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.04083970997124e+50,
        "filterflow_gradient_max_abs": 251.90780939902413,
        "gradient_delta": [
          -3.04083970997124e+50,
          2.46902256775332e+50
        ],
        "gradient_explosion_ratio": 1.207124033679529e+48,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.04083970997124e+50,
        "relative_gradient_delta": 1.207124033679529e+48,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.980804936214554e-09,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.370752220623899e+53,
        "filterflow_gradient_max_abs": 369.7748801823844,
        "gradient_delta": [
          -6.370752220623899e+53,
          5.1727592550288095e+53
        ],
        "gradient_explosion_ratio": 1.7228731755606676e+51,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.370752220623899e+53,
        "relative_gradient_delta": 1.7228731755606676e+51,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9715820915043878e-09,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.425444668497596e+54,
        "filterflow_gradient_max_abs": 153.94165873710156,
        "gradient_delta": [
          4.425444668497596e+54,
          -3.593258958017613e+54
        ],
        "gradient_explosion_ratio": 2.874754439313455e+52,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.425444668497596e+54,
        "relative_gradient_delta": 2.874754439313455e+52,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.075740551139461e-09,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5539871920405229e+57,
        "filterflow_gradient_max_abs": 231.88010181357106,
        "gradient_delta": [
          1.5539871920405229e+57,
          -1.2617665345469409e+57
        ],
        "gradient_explosion_ratio": 6.701684102631241e+54,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5539871920405229e+57,
        "relative_gradient_delta": 6.701684102631241e+54,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8847040312030003e-09,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.323781683294017e+60,
        "filterflow_gradient_max_abs": 317.10552544548756,
        "gradient_delta": [
          2.323781683294017e+60,
          -1.88680439649131e+60
        ],
        "gradient_explosion_ratio": 7.328102151576951e+57,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.323781683294017e+60,
        "relative_gradient_delta": 7.328102151576951e+57,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8788775807697675e-09,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.053291723130761e+63,
        "filterflow_gradient_max_abs": 440.433114763931,
        "gradient_delta": [
          -4.053291723130761e+63,
          3.2910873987591114e+63
        ],
        "gradient_explosion_ratio": 9.202967686258778e+60,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.053291723130761e+63,
        "relative_gradient_delta": 9.202967686258778e+60,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.7967104188064695e-09,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2275212638553773e+65,
        "filterflow_gradient_max_abs": 274.3754691050723,
        "gradient_delta": [
          1.2275212638553773e+65,
          -9.966910946063454e+64
        ],
        "gradient_explosion_ratio": 4.473873950390576e+62,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2275212638553773e+65,
        "relative_gradient_delta": 4.473873950390576e+62,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9457680739142234e-09,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.387169703671358e+68,
        "filterflow_gradient_max_abs": 184.24153726601756,
        "gradient_delta": [
          -1.387169703671358e+68,
          1.1263183220002733e+68
        ],
        "gradient_explosion_ratio": 7.529082335372017e+65,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.387169703671358e+68,
        "relative_gradient_delta": 7.529082335372017e+65,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8393571938067907e-09,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1095924491289246e+70,
        "filterflow_gradient_max_abs": 187.1386096136716,
        "gradient_delta": [
          -2.1095924491289246e+70,
          1.7128925330087772e+70
        ],
        "gradient_explosion_ratio": 1.1272887265134444e+68,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1095924491289246e+70,
        "relative_gradient_delta": 1.1272887265134444e+68,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.6310544853913598e-09,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.468486436839226e+73,
        "filterflow_gradient_max_abs": 954.1501022077981,
        "gradient_delta": [
          -5.468486436839226e+73,
          4.4401607468527537e+73
        ],
        "gradient_explosion_ratio": 5.73126432013763e+70,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.468486436839226e+73,
        "relative_gradient_delta": 5.73126432013763e+70,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.98600263906701e-09,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.1936811685208645e+75,
        "filterflow_gradient_max_abs": 422.91186590476366,
        "gradient_delta": [
          4.1936811685208645e+75,
          -3.4050772045155175e+75
        ],
        "gradient_explosion_ratio": 9.91620596775889e+72,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.1936811685208645e+75,
        "relative_gradient_delta": 9.91620596775889e+72,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5840096163374255e-09,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.318805187781066e+77,
        "filterflow_gradient_max_abs": 354.26740709319216,
        "gradient_delta": [
          6.318805187781066e+77,
          -5.130580661732676e+77
        ],
        "gradient_explosion_ratio": 1.783625888598571e+75,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.318805187781066e+77,
        "relative_gradient_delta": 1.783625888598571e+75,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.941782094647351e-09,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.097530718514138e+80,
        "filterflow_gradient_max_abs": 199.05378088782396,
        "gradient_delta": [
          2.097530718514138e+80,
          -1.7030989596909792e+80
        ],
        "gradient_explosion_ratio": 1.0537507547752604e+78,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.097530718514138e+80,
        "relative_gradient_delta": 1.0537507547752604e+78,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.940716280543711e-09,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2244886471654443e+83,
        "filterflow_gradient_max_abs": 548.7404094827189,
        "gradient_delta": [
          2.2244886471654443e+83,
          -1.8061829881164985e+83
        ],
        "gradient_explosion_ratio": 4.0538087021191e+80,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2244886471654443e+83,
        "relative_gradient_delta": 4.0538087021191e+80,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.836934408558591e-09,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0182157792441476e+85,
        "filterflow_gradient_max_abs": 399.4756572109477,
        "gradient_delta": [
          -2.0182157792441476e+85,
          1.6386988584833154e+85
        ],
        "gradient_explosion_ratio": 5.0521621100391746e+82,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0182157792441476e+85,
        "relative_gradient_delta": 5.0521621100391746e+82,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.73063721528888e-09,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.942218403148744e+87,
        "filterflow_gradient_max_abs": 381.20393707705813,
        "gradient_delta": [
          8.942218403148744e+87,
          -7.260672144301769e+87
        ],
        "gradient_explosion_ratio": 2.3457833283975572e+85,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.942218403148744e+87,
        "relative_gradient_delta": 2.3457833283975572e+85,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.649024276659475e-09,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.134939199506339e+90,
        "filterflow_gradient_max_abs": 48.850988576799736,
        "gradient_delta": [
          -5.134939199506339e+90,
          4.169335653377767e+90
        ],
        "gradient_explosion_ratio": 1.0511433543322436e+89,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.134939199506339e+90,
        "relative_gradient_delta": 1.0511433543322436e+89,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.737742642646481e-09,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1585393826649593e+91,
        "filterflow_gradient_max_abs": 346.85073969207997,
        "gradient_delta": [
          -1.1585393826649593e+91,
          9.406809635548444e+90
        ],
        "gradient_explosion_ratio": 3.340166965460312e+88,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1585393826649593e+91,
        "relative_gradient_delta": 3.340166965460312e+88,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.721428581433429e-09,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.215874986802222e+93,
        "filterflow_gradient_max_abs": 322.6295207830076,
        "gradient_delta": [
          8.215874986802222e+93,
          -6.670914527958242e+93
        ],
        "gradient_explosion_ratio": 2.546535409054527e+91,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.215874986802222e+93,
        "relative_gradient_delta": 2.546535409054527e+91,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6360639771592105e-09,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.667903004177259e+96,
        "filterflow_gradient_max_abs": 86.66552831338745,
        "gradient_delta": [
          4.667903004177259e+96,
          -3.790123634510905e+96
        ],
        "gradient_explosion_ratio": 5.3861126736548094e+94,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.667903004177259e+96,
        "relative_gradient_delta": 5.3861126736548094e+94,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.636163453142217e-09,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.26537262037288e+99,
        "filterflow_gradient_max_abs": 1118.3947944525503,
        "gradient_delta": [
          -5.26537262037288e+99,
          4.27524162244225e+99
        ],
        "gradient_explosion_ratio": 4.707973111543548e+96,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.26537262037288e+99,
        "relative_gradient_delta": 4.707973111543548e+96,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9218832625920186e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.7420065745238236e+101,
        "filterflow_gradient_max_abs": 72.987643547552,
        "gradient_delta": [
          -3.7420065745238236e+101,
          3.038338102978147e+101
        ],
        "gradient_explosion_ratio": 5.126904216445731e+99,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.7420065745238236e+101,
        "relative_gradient_delta": 5.126904216445731e+99,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9393910356011475e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.072461913603353e+103,
        "filterflow_gradient_max_abs": 7.513193750877159,
        "gradient_delta": [
          5.072461913603353e+103,
          -4.118606956207095e+103
        ],
        "gradient_explosion_ratio": 6.751405702815992e+102,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.072461913603353e+103,
        "relative_gradient_delta": 6.751405702815992e+102,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.889368827003636e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1251524796144548e+105,
        "filterflow_gradient_max_abs": 330.52600026078443,
        "gradient_delta": [
          -1.1251524796144548e+105,
          9.135723260742698e+104
        ],
        "gradient_explosion_ratio": 3.404126993721255e+102,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1251524796144548e+105,
        "relative_gradient_delta": 3.404126993721255e+102,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.899515377270291e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1740940847546465e+107,
        "filterflow_gradient_max_abs": 286.4569368626525,
        "gradient_delta": [
          2.1740940847546465e+107,
          -1.7652649095118205e+107
        ],
        "gradient_explosion_ratio": 7.589601803907647e+104,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1740940847546465e+107,
        "relative_gradient_delta": 7.589601803907647e+104,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.8836134308439796e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.4741876039950455e+110,
        "filterflow_gradient_max_abs": 609.6787100623405,
        "gradient_delta": [
          5.4741876039950455e+110,
          -4.4447898336964545e+110
        ],
        "gradient_explosion_ratio": 8.978807220339548e+107,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.4741876039950455e+110,
        "relative_gradient_delta": 8.978807220339548e+107,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.874831122629985e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.66645527463394e+112,
        "filterflow_gradient_max_abs": 237.18680047332637,
        "gradient_delta": [
          5.66645527463394e+112,
          -4.6009023840190955e+112
        ],
        "gradient_explosion_ratio": 2.3890263974749218e+110,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.66645527463394e+112,
        "relative_gradient_delta": 2.3890263974749218e+110,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.782176349886868e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1325832104563677e+115,
        "filterflow_gradient_max_abs": 20.398532585564105,
        "gradient_delta": [
          -2.1325832104563677e+115,
          1.7315599791338083e+115
        ],
        "gradient_explosion_ratio": 1.0454591287441831e+114,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1325832104563677e+115,
        "relative_gradient_delta": 1.0454591287441831e+114,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.6820893001277e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6111818097066886e+116,
        "filterflow_gradient_max_abs": 478.6428510468603,
        "gradient_delta": [
          1.6111818097066886e+116,
          -1.3082059012363045e+116
        ],
        "gradient_explosion_ratio": 3.366146190594519e+113,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6111818097066886e+116,
        "relative_gradient_delta": 3.366146190594519e+113,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.958078309551638e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.809352796238392e+118,
        "filterflow_gradient_max_abs": 310.27237965253573,
        "gradient_delta": [
          -6.809352796238392e+118,
          5.528882872169889e+118
        ],
        "gradient_explosion_ratio": 2.1946371133208738e+116,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.809352796238392e+118,
        "relative_gradient_delta": 2.1946371133208738e+116,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.521620328683639e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.243434585160553e+121,
        "filterflow_gradient_max_abs": 291.33394004387503,
        "gradient_delta": [
          -2.243434585160553e+121,
          1.8215662227957655e+121
        ],
        "gradient_explosion_ratio": 7.700560342618133e+118,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.243434585160553e+121,
        "relative_gradient_delta": 7.700560342618133e+118,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.524789349285129e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.056219628974459e+124,
        "filterflow_gradient_max_abs": 772.789629727978,
        "gradient_delta": [
          -9.056219628974459e+124,
          7.353235922936114e+124
        ],
        "gradient_explosion_ratio": 1.1718867956551447e+122,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.056219628974459e+124,
        "relative_gradient_delta": 1.1718867956551447e+122,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.415127818901965e-09,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2213983846848298e+127,
        "filterflow_gradient_max_abs": 137.0827775975205,
        "gradient_delta": [
          -1.2213983846848298e+127,
          9.917195967449928e+126
        ],
        "gradient_explosion_ratio": 8.909933152003202e+124,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2213983846848298e+127,
        "relative_gradient_delta": 8.909933152003202e+124,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.988418484368594e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3365812652215278e+129,
        "filterflow_gradient_max_abs": 205.40967733109431,
        "gradient_delta": [
          1.3365812652215278e+129,
          -1.0852428249317207e+129
        ],
        "gradient_explosion_ratio": 6.506905042585353e+126,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3365812652215278e+129,
        "relative_gradient_delta": 6.506905042585353e+126,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.800110448537453e-09,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.0671830428588906e+132,
        "filterflow_gradient_max_abs": 1075.2940301638955,
        "gradient_delta": [
          4.0671830428588906e+132,
          -3.3023665150768125e+132
        ],
        "gradient_explosion_ratio": 3.7823915401436514e+129,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.0671830428588906e+132,
        "relative_gradient_delta": 3.7823915401436514e+129,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.299266720408923e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.888782007558424e+135,
        "filterflow_gradient_max_abs": 1320.7702359098546,
        "gradient_delta": [
          -4.888782007558424e+135,
          3.96946727775563e+135
        ],
        "gradient_explosion_ratio": 3.701462884792094e+132,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.888782007558424e+135,
        "relative_gradient_delta": 3.701462884792094e+132,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.148105858803319e-09,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4065535655293914e+137,
        "filterflow_gradient_max_abs": 352.8826174689448,
        "gradient_delta": [
          -2.4065535655293914e+137,
          1.954011370473425e+137
        ],
        "gradient_explosion_ratio": 6.81969994099009e+134,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4065535655293914e+137,
        "relative_gradient_delta": 6.81969994099009e+134,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.5889797800336964e-09,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.50195263643835e+140,
        "filterflow_gradient_max_abs": 974.6366511077524,
        "gradient_delta": [
          -6.50195263643835e+140,
          5.279288009151538e+140
        ],
        "gradient_explosion_ratio": 6.671155480402221e+137,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.50195263643835e+140,
        "relative_gradient_delta": 6.671155480402221e+137,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.8240451633319026e-09,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.075476648355451e+143,
        "filterflow_gradient_max_abs": 731.310897142959,
        "gradient_delta": [
          2.075476648355451e+143,
          -1.6851920639242042e+143
        ],
        "gradient_explosion_ratio": 2.8380223191857213e+140,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.075476648355451e+143,
        "relative_gradient_delta": 2.8380223191857213e+140,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.972274953412125e-09,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.1761236228221957e+145,
        "filterflow_gradient_max_abs": 483.3559108394908,
        "gradient_delta": [
          -3.1761236228221957e+145,
          2.5788670411990546e+145
        ],
        "gradient_explosion_ratio": 6.570983309805637e+142,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.1761236228221957e+145,
        "relative_gradient_delta": 6.570983309805637e+142,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.955818783651921e-09,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.288453792439288e+149,
        "filterflow_gradient_max_abs": 1076.6780654517022,
        "gradient_delta": [
          3.288453792439288e+149,
          -2.6700739986601146e+149
        ],
        "gradient_explosion_ratio": 3.054259112318474e+146,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.288453792439288e+149,
        "relative_gradient_delta": 3.054259112318474e+146,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5558010697277496e-09,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.905584579851266e+151,
        "filterflow_gradient_max_abs": 18.05494027199655,
        "gradient_delta": [
          4.905584579851266e+151,
          -3.9831101975658074e+151
        ],
        "gradient_explosion_ratio": 2.7170317408692246e+150,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.905584579851266e+151,
        "relative_gradient_delta": 2.7170317408692246e+150,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6730690428375965e-09,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.759979522647206e+153,
        "filterflow_gradient_max_abs": 989.4278480713913,
        "gradient_delta": [
          3.759979522647206e+153,
          -3.0529313144059125e+153
        ],
        "gradient_explosion_ratio": 3.800155342278084e+150,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.759979522647206e+153,
        "relative_gradient_delta": 3.800155342278084e+150,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.355683813628275e-09,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2439647942646707e+156,
        "filterflow_gradient_max_abs": 778.7073741209738,
        "gradient_delta": [
          2.2439647942646707e+156,
          -1.821996728325755e+156
        ],
        "gradient_explosion_ratio": 2.8816534539662216e+153,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2439647942646707e+156,
        "relative_gradient_delta": 2.8816534539662216e+153,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.821792577378801e-09,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.609469349780909e+159,
        "filterflow_gradient_max_abs": 1097.9215016104433,
        "gradient_delta": [
          -4.609469349780909e+159,
          3.74267818108561e+159
        ],
        "gradient_explosion_ratio": 4.198359666897578e+156,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.609469349780909e+159,
        "relative_gradient_delta": 4.198359666897578e+156,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0083482493428164e-08,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.865748592858761e+162,
        "filterflow_gradient_max_abs": 1697.7646785016034,
        "gradient_delta": [
          4.865748592858761e+162,
          -3.950765199036654e+162
        ],
        "gradient_explosion_ratio": 2.865973508857026e+159,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.865748592858761e+162,
        "relative_gradient_delta": 2.865973508857026e+159,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8990448324984754e-08,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.963036594210704e+165,
        "filterflow_gradient_max_abs": 947.0739014815089,
        "gradient_delta": [
          -2.963036594210704e+165,
          2.4058501249037973e+165
        ],
        "gradient_explosion_ratio": 3.128622369992059e+162,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.963036594210704e+165,
        "relative_gradient_delta": 3.128622369992059e+162,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1565390423129429e-08,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.75318086937974e+166,
        "filterflow_gradient_max_abs": 249.89093531615012,
        "gradient_delta": [
          -7.75318086937974e+166,
          6.29522807765652e+166
        ],
        "gradient_explosion_ratio": 3.102625895401442e+164,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.75318086937974e+166,
        "relative_gradient_delta": 3.102625895401442e+164,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.132605782724568e-09,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.095759089574179e+170,
        "filterflow_gradient_max_abs": 974.2890696675929,
        "gradient_delta": [
          -8.095759089574179e+170,
          6.573385915954729e+170
        ],
        "gradient_explosion_ratio": 8.309401533506152e+167,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.095759089574179e+170,
        "relative_gradient_delta": 8.309401533506152e+167,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.223679515140248e-09,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.828163529810629e+173,
        "filterflow_gradient_max_abs": 1029.3299119039873,
        "gradient_delta": [
          8.828163529810629e+173,
          -7.168064806342287e+173
        ],
        "gradient_explosion_ratio": 8.57661224813808e+170,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.828163529810629e+173,
        "relative_gradient_delta": 8.57661224813808e+170,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.178016403486254e-09,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5346781540287131e+177,
        "filterflow_gradient_max_abs": 1426.254117759735,
        "gradient_delta": [
          -1.5346781540287131e+177,
          1.2460884336599442e+177
        ],
        "gradient_explosion_ratio": 1.0760201389912784e+174,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5346781540287131e+177,
        "relative_gradient_delta": 1.0760201389912784e+174,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.153612730486202e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.1102547763389943e+180,
        "filterflow_gradient_max_abs": 1942.7454564725651,
        "gradient_delta": [
          3.1102547763389943e+180,
          -2.525384552036244e+180
        ],
        "gradient_explosion_ratio": 1.600958461118355e+177,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.1102547763389943e+180,
        "relative_gradient_delta": 1.600958461118355e+177,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.01524527357833e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.507924853971741e+182,
        "filterflow_gradient_max_abs": 169.06130724664092,
        "gradient_delta": [
          5.507924853971741e+182,
          -4.472182936849121e+182
        ],
        "gradient_explosion_ratio": 3.257945264753167e+180,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.507924853971741e+182,
        "relative_gradient_delta": 3.257945264753167e+180,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.081496278260602e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4926078128865e+186,
        "filterflow_gradient_max_abs": 1963.5208371745916,
        "gradient_delta": [
          -1.4926078128865e+186,
          1.2119292418060542e+186
        ],
        "gradient_explosion_ratio": 7.601690721216323e+182,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4926078128865e+186,
        "relative_gradient_delta": 7.601690721216323e+182,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.653859933678177e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0301533401217673e+188,
        "filterflow_gradient_max_abs": 1119.9768301540837,
        "gradient_delta": [
          2.0301533401217673e+188,
          -1.6483916116489583e+188
        ],
        "gradient_explosion_ratio": 1.812674410275491e+185,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0301533401217673e+188,
        "relative_gradient_delta": 1.812674410275491e+185,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.3080741458397824e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0914417834458432e+191,
        "filterflow_gradient_max_abs": 979.6868013870265,
        "gradient_delta": [
          -2.0914417834458432e+191,
          1.6981550230474107e+191
        ],
        "gradient_explosion_ratio": 2.1348065325416345e+188,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0914417834458432e+191,
        "relative_gradient_delta": 2.1348065325416345e+188,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.394845624730806e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.551276941484494e+195,
        "filterflow_gradient_max_abs": 2882.4178802677957,
        "gradient_delta": [
          1.551276941484494e+195,
          -1.2595658895076927e+195
        ],
        "gradient_explosion_ratio": 5.381859972851577e+191,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.551276941484494e+195,
        "relative_gradient_delta": 5.381859972851577e+191,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.620751946684322e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0104075479898404e+197,
        "filterflow_gradient_max_abs": 858.8073873147812,
        "gradient_delta": [
          -1.0104075479898404e+197,
          8.204046923634564e+196
        ],
        "gradient_explosion_ratio": 1.1765240529067465e+194,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0104075479898404e+197,
        "relative_gradient_delta": 1.1765240529067465e+194,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.615852837261627e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.1621631550850765e+199,
        "filterflow_gradient_max_abs": 442.0116504772855,
        "gradient_delta": [
          -3.1621631550850765e+199,
          2.56753178023242e+199
        ],
        "gradient_explosion_ratio": 7.154026713256457e+196,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.1621631550850765e+199,
        "relative_gradient_delta": 7.154026713256457e+196,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.274422841874184e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1067232618450242e+204,
        "filterflow_gradient_max_abs": 3282.5855155180925,
        "gradient_delta": [
          -1.1067232618450242e+204,
          8.986086445729715e+203
        ],
        "gradient_explosion_ratio": 3.371498645238948e+200,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1067232618450242e+204,
        "relative_gradient_delta": 3.371498645238948e+200,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0136062655874412e-08,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.9897543841550904e+206,
        "filterflow_gradient_max_abs": 1855.9144036285215,
        "gradient_delta": [
          4.9897543841550904e+206,
          -4.0514522270207025e+206
        ],
        "gradient_explosion_ratio": 2.6885692434950443e+203,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.9897543841550904e+206,
        "relative_gradient_delta": 2.6885692434950443e+203,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.873637741795392e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.3037452983866495e+209,
        "filterflow_gradient_max_abs": 1310.8611477302254,
        "gradient_delta": [
          -4.3037452983866495e+209,
          3.49444424139345e+209
        ],
        "gradient_explosion_ratio": 3.2831435318978254e+206,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.3037452983866495e+209,
        "relative_gradient_delta": 3.2831435318978254e+206,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.93335175330867e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.050496088060541e+212,
        "filterflow_gradient_max_abs": 914.416967723082,
        "gradient_delta": [
          3.050496088060541e+212,
          -2.4768632317327086e+212
        ],
        "gradient_explosion_ratio": 3.3360011851664806e+209,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.050496088060541e+212,
        "relative_gradient_delta": 3.3360011851664806e+209,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.058265166255296e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.5506494558921818e+216,
        "filterflow_gradient_max_abs": 3551.3298618369327,
        "gradient_delta": [
          -2.5506494558921818e+216,
          2.0710106395694523e+216
        ],
        "gradient_explosion_ratio": 7.182237514182513e+212,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.5506494558921818e+216,
        "relative_gradient_delta": 7.182237514182513e+212,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.786315675024525e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.688985190153924e+219,
        "filterflow_gradient_max_abs": 3023.0985131010166,
        "gradient_delta": [
          5.688985190153924e+219,
          -4.619195644444477e+219
        ],
        "gradient_explosion_ratio": 1.8818391678272863e+216,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.688985190153924e+219,
        "relative_gradient_delta": 1.8818391678272863e+216,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.745331570025883e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.7341907250410905e+222,
        "filterflow_gradient_max_abs": 2001.070628323309,
        "gradient_delta": [
          -5.7341907250410905e+222,
          4.6559004701517023e+222
        ],
        "gradient_explosion_ratio": 2.8655613869290317e+219,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.7341907250410905e+222,
        "relative_gradient_delta": 2.8655613869290317e+219,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.205052720062668e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0626986513089231e+226,
        "filterflow_gradient_max_abs": 2346.9001573329506,
        "gradient_delta": [
          1.0626986513089231e+226,
          -8.628626753992973e+225
        ],
        "gradient_explosion_ratio": 4.528094848809369e+222,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0626986513089231e+226,
        "relative_gradient_delta": 4.528094848809369e+222,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.456598728414974e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.019387834272036e+229,
        "filterflow_gradient_max_abs": 4046.6212127655212,
        "gradient_delta": [
          -4.019387834272036e+229,
          3.2635589928298165e+229
        ],
        "gradient_explosion_ratio": 9.932700944660759e+225,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.019387834272036e+229,
        "relative_gradient_delta": 9.932700944660759e+225,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.6329352092725458e-08,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.711418912951682e+232,
        "filterflow_gradient_max_abs": 2730.4139020142047,
        "gradient_delta": [
          3.711418912951682e+232,
          -3.0135023214837034e+232
        ],
        "gradient_explosion_ratio": 1.359288022308192e+229,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.711418912951682e+232,
        "relative_gradient_delta": 1.359288022308192e+229,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.300094916397939e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_raw_transport_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      -1.3832594583394986e+228,
      1.2680960330198352e+228
    ],
    "final_bayesfilter_gradient_max_abs": 1.3832594583394986e+228,
    "final_filterflow_gradient_diag": [
      18935.6850725171,
      2073.5151524806142
    ],
    "final_filterflow_gradient_max_abs": 18935.6850725171,
    "final_gradient_delta": [
      -1.3832594583394986e+228,
      1.2680960330198352e+228
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 1.3832594583394986e+228,
    "final_relative_gradient_delta": 7.305040472748122e+223,
    "final_scalar_delta": 9.3001517598168e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "bayesfilter_gradient_max_abs": 278345833.87246245,
      "filterflow_gradient_max_abs": 104.45156511568617,
      "gradient_explosion_ratio": 2664831.623769144,
      "resampling_flag": [
        true
      ],
      "status": "explosion",
      "time_index": 10,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 0.00039679191160874164,
      "max_abs_gradient_delta": 0.009310563115163609,
      "relative_gradient_delta": 0.009310563115163609,
      "resampling_flag": [
        false
      ],
      "scalar_delta": 0.0,
      "status": "failure",
      "time_index": 0,
      "transport_status": "not_triggered"
    },
    "first_scalar_failure": {
      "status": "no_failure"
    },
    "mode": "transition_log_prob_stop_gradient",
    "mode_description": "Stop gradient through transition log probability",
    "sample_rows": [
      {
        "bayesfilter_gradient_max_abs": 0.00039679191160874164,
        "filterflow_gradient_max_abs": 0.008913771203554867,
        "gradient_delta": [
          -0.009310563115163609,
          -6.039123805044973e-19
        ],
        "gradient_explosion_ratio": 0.00039679191160874164,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.009310563115163609,
        "relative_gradient_delta": 0.009310563115163609,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 0.09527938485448965,
        "filterflow_gradient_max_abs": 8.800019462744133,
        "gradient_delta": [
          8.704740077889644,
          9.225482034804e-06
        ],
        "gradient_explosion_ratio": 0.010827178878167894,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.704740077889644,
        "relative_gradient_delta": 0.9891728211218321,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7926993223227328e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 0.13126125038256548,
        "filterflow_gradient_max_abs": 1.4485716238559057,
        "gradient_delta": [
          -1.3173103734733402,
          -0.07639915446395518
        ],
        "gradient_explosion_ratio": 0.09061426319615831,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3173103734733402,
        "relative_gradient_delta": 0.9093857368038417,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4985346297180513e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.6916740000201047,
        "filterflow_gradient_max_abs": 16.840076774872443,
        "gradient_delta": [
          -20.352423294103666,
          3.6916740000201043
        ],
        "gradient_explosion_ratio": 0.2192195468804843,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 20.352423294103666,
        "relative_gradient_delta": 1.2085706951450539,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.4439117396468646e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 76.81085589987714,
        "filterflow_gradient_max_abs": 11.278780998887767,
        "gradient_delta": [
          -65.1796631655011,
          76.81085589987714
        ],
        "gradient_explosion_ratio": 6.810209002856929,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 76.81085589987714,
        "relative_gradient_delta": 6.810209002856929,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.665601073204016e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 31.725530124455542,
        "filterflow_gradient_max_abs": 0.16051708831084313,
        "gradient_delta": [
          27.053734703678735,
          -31.725530124455542
        ],
        "gradient_explosion_ratio": 31.725530124455542,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 31.725530124455542,
        "relative_gradient_delta": 31.725530124455542,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.347366828165832e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3733.2172796414607,
        "filterflow_gradient_max_abs": 6.732984884221974,
        "gradient_delta": [
          -3739.9502645256825,
          3578.442353422772
        ],
        "gradient_explosion_ratio": 554.466903436818,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3739.9502645256825,
        "relative_gradient_delta": 555.466903436818,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.53681536782824e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 177.051165928888,
        "filterflow_gradient_max_abs": 16.75562828027451,
        "gradient_delta": [
          -160.29553764861348,
          44.417318883345715
        ],
        "gradient_explosion_ratio": 10.566668284072684,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 160.29553764861348,
        "relative_gradient_delta": 9.566668284072684,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.6477489351891563e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 187462.11480640786,
        "filterflow_gradient_max_abs": 8.578663144440544,
        "gradient_delta": [
          -187470.6934695523,
          173116.0918429253
        ],
        "gradient_explosion_ratio": 21852.136125416448,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 187470.6934695523,
        "relative_gradient_delta": 21853.136125416448,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.839595473844383e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1457183.8601741244,
        "filterflow_gradient_max_abs": 56.8762754108451,
        "gradient_delta": [
          1457126.9838987135,
          -1405252.5636482998
        ],
        "gradient_explosion_ratio": 25620.240595013896,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1457126.9838987135,
        "relative_gradient_delta": 25619.240595013896,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.645795108146558e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 278345833.87246245,
        "filterflow_gradient_max_abs": 104.45156511568617,
        "gradient_delta": [
          278345729.42089736,
          -255211153.94127506
        ],
        "gradient_explosion_ratio": 2664831.623769144,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 278345729.42089736,
        "relative_gradient_delta": 2664830.6237691445,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.562661608062626e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4912314281.721071,
        "filterflow_gradient_max_abs": 9.13071410440192,
        "gradient_delta": [
          -4912314272.590357,
          4530335583.069662
        ],
        "gradient_explosion_ratio": 537998915.0413595,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4912314272.590357,
        "relative_gradient_delta": 537998914.0413594,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.412914561020443e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1013893765337.948,
        "filterflow_gradient_max_abs": 62.46161279976278,
        "gradient_delta": [
          -1013893765400.4097,
          932163210042.7511
        ],
        "gradient_explosion_ratio": 16232270027.804958,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1013893765400.4097,
        "relative_gradient_delta": 16232270028.80496,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.171952003976912e-11,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 64690374334099.734,
        "filterflow_gradient_max_abs": 78.21898890138324,
        "gradient_delta": [
          64690374334021.516,
          -59281411331102.23
        ],
        "gradient_explosion_ratio": 827041812259.4236,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 64690374334021.516,
        "relative_gradient_delta": 827041812258.4236,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1748113593057496e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 978321117660057.2,
        "filterflow_gradient_max_abs": 55.1203162059954,
        "gradient_delta": [
          978321117660002.1,
          -898921690408905.1
        ],
        "gradient_explosion_ratio": 17748829923324.094,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 978321117660002.1,
        "relative_gradient_delta": 17748829923323.094,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1169021263413015e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5497136619927594e+17,
        "filterflow_gradient_max_abs": 3.2014311273644616,
        "gradient_delta": [
          -1.5497136619927594e+17,
          1.4195393931996602e+17
        ],
        "gradient_explosion_ratio": 4.8406903048654424e+16,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5497136619927594e+17,
        "relative_gradient_delta": 4.8406903048654424e+16,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.603695616533514e-11,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6077475308369705e+18,
        "filterflow_gradient_max_abs": 25.054390338542845,
        "gradient_delta": [
          1.6077475308369705e+18,
          -1.4745400990626038e+18
        ],
        "gradient_explosion_ratio": 6.4170291478362776e+16,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6077475308369705e+18,
        "relative_gradient_delta": 6.4170291478362776e+16,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1939249588976963e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.950302384313414e+19,
        "filterflow_gradient_max_abs": 145.3600680670563,
        "gradient_delta": [
          5.950302384313414e+19,
          -5.450825808839367e+19
        ],
        "gradient_explosion_ratio": 4.093491743254048e+17,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.950302384313414e+19,
        "relative_gradient_delta": 4.093491743254048e+17,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.48947520983711e-09,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.912807340223626e+21,
        "filterflow_gradient_max_abs": 168.66458545141114,
        "gradient_delta": [
          7.912807340223626e+21,
          -7.2551521535376e+21
        ],
        "gradient_explosion_ratio": 4.691445639904736e+19,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.912807340223626e+21,
        "relative_gradient_delta": 4.691445639904736e+19,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.252356523513299e-09,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.329476106287484e+23,
        "filterflow_gradient_max_abs": 101.15910809775511,
        "gradient_delta": [
          6.329476106287484e+23,
          -5.803806218958845e+23
        ],
        "gradient_explosion_ratio": 6.256951277359024e+21,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.329476106287484e+23,
        "relative_gradient_delta": 6.256951277359024e+21,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.767464479802584e-09,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5127517668747933e+25,
        "filterflow_gradient_max_abs": 125.28072286451086,
        "gradient_delta": [
          1.5127517668747933e+25,
          -1.3869076793787396e+25
        ],
        "gradient_explosion_ratio": 1.2074896538638356e+23,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5127517668747933e+25,
        "relative_gradient_delta": 1.2074896538638356e+23,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9853310934413457e-09,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.258001823056869e+27,
        "filterflow_gradient_max_abs": 278.9526477486435,
        "gradient_delta": [
          5.258001823056869e+27,
          -4.8212148765756315e+27
        ],
        "gradient_explosion_ratio": 1.8849083762039456e+25,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.258001823056869e+27,
        "relative_gradient_delta": 1.8849083762039456e+25,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.0152165209074155e-09,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1609147424306718e+30,
        "filterflow_gradient_max_abs": 252.28215416061428,
        "gradient_delta": [
          2.1609147424306718e+30,
          -1.9814029389370722e+30
        ],
        "gradient_explosion_ratio": 8.565468095119147e+27,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1609147424306718e+30,
        "relative_gradient_delta": 8.565468095119147e+27,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.021582983819826e-09,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.382969357801563e+32,
        "filterflow_gradient_max_abs": 69.58591013728201,
        "gradient_delta": [
          4.382969357801563e+32,
          -4.0184961677794566e+32
        ],
        "gradient_explosion_ratio": 6.298644868127264e+30,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.382969357801563e+32,
        "relative_gradient_delta": 6.298644868127264e+30,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9725839567618095e-09,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.9805139131567027e+33,
        "filterflow_gradient_max_abs": 64.72471139759364,
        "gradient_delta": [
          -1.9805139131567027e+33,
          1.8157087141448947e+33
        ],
        "gradient_explosion_ratio": 3.059903814774422e+31,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.9805139131567027e+33,
        "relative_gradient_delta": 3.059903814774422e+31,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.974680057832302e-09,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4014132300874377e+36,
        "filterflow_gradient_max_abs": 0.6534447816938739,
        "gradient_delta": [
          -1.4014132300874377e+36,
          1.285015730030977e+36
        ],
        "gradient_explosion_ratio": 1.4014132300874377e+36,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4014132300874377e+36,
        "relative_gradient_delta": 1.4014132300874377e+36,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.903298934597842e-09,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3080483823161563e+38,
        "filterflow_gradient_max_abs": 262.5095687458148,
        "gradient_delta": [
          2.3080483823161563e+38,
          -2.116147351755277e+38
        ],
        "gradient_explosion_ratio": 8.792244767850785e+35,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3080483823161563e+38,
        "relative_gradient_delta": 8.792244767850785e+35,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.970814705349767e-09,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.9873471468119476e+40,
        "filterflow_gradient_max_abs": 28.548993251385596,
        "gradient_delta": [
          1.9873471468119476e+40,
          -1.822083906228302e+40
        ],
        "gradient_explosion_ratio": 6.961181185313754e+38,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.9873471468119476e+40,
        "relative_gradient_delta": 6.961181185313754e+38,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9090827524669294e-09,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3937001463969847e+42,
        "filterflow_gradient_max_abs": 485.70702239538065,
        "gradient_delta": [
          2.3937001463969847e+42,
          -2.1947200651440084e+42
        ],
        "gradient_explosion_ratio": 4.9282798807229065e+39,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3937001463969847e+42,
        "relative_gradient_delta": 4.9282798807229065e+39,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8526088158287166e-09,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.597086328263516e+43,
        "filterflow_gradient_max_abs": 245.11951564783823,
        "gradient_delta": [
          8.597086328263516e+43,
          -7.880991711425129e+43
        ],
        "gradient_explosion_ratio": 3.507303898484729e+41,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.597086328263516e+43,
        "relative_gradient_delta": 3.507303898484729e+41,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8581510491676454e-09,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.950645724153546e+46,
        "filterflow_gradient_max_abs": 434.75519438634416,
        "gradient_delta": [
          -4.950645724153546e+46,
          4.538474485662793e+46
        ],
        "gradient_explosion_ratio": 1.138720316186531e+44,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.950645724153546e+46,
        "relative_gradient_delta": 1.138720316186531e+44,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9084219477226725e-09,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.360494981148795e+48,
        "filterflow_gradient_max_abs": 251.90780939902413,
        "gradient_delta": [
          7.360494981148795e+48,
          -6.747742721746042e+48
        ],
        "gradient_explosion_ratio": 2.9219002772120126e+46,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.360494981148795e+48,
        "relative_gradient_delta": 2.9219002772120126e+46,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.980804936214554e-09,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.130868389455651e+51,
        "filterflow_gradient_max_abs": 369.7748801823844,
        "gradient_delta": [
          2.130868389455651e+51,
          -1.953476228630739e+51
        ],
        "gradient_explosion_ratio": 5.762609911210413e+48,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.130868389455651e+51,
        "relative_gradient_delta": 5.762609911210413e+48,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9715820915043878e-09,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.069554304365269e+53,
        "filterflow_gradient_max_abs": 153.94165873710156,
        "gradient_delta": [
          -2.069554304365269e+53,
          1.897252824194873e+53
        ],
        "gradient_explosion_ratio": 1.344375733861366e+51,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.069554304365269e+53,
        "relative_gradient_delta": 1.344375733861366e+51,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.075740551139461e-09,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0694589519396302e+55,
        "filterflow_gradient_max_abs": 231.88010181357106,
        "gradient_delta": [
          -2.0694589519396302e+55,
          1.8971709578051542e+55
        ],
        "gradient_explosion_ratio": 8.924693993810006e+52,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0694589519396302e+55,
        "relative_gradient_delta": 8.924693993810006e+52,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8847040312030003e-09,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4252633459602515e+58,
        "filterflow_gradient_max_abs": 317.10552544548756,
        "gradient_delta": [
          -2.4252633459602515e+58,
          2.223347128847712e+58
        ],
        "gradient_explosion_ratio": 7.648127047149702e+55,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4252633459602515e+58,
        "relative_gradient_delta": 7.648127047149702e+55,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8788775807697675e-09,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1061886951752303e+61,
        "filterflow_gradient_max_abs": 440.433114763931,
        "gradient_delta": [
          1.1061886951752303e+61,
          -1.0140927174236643e+61
        ],
        "gradient_explosion_ratio": 2.51159292545053e+58,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1061886951752303e+61,
        "relative_gradient_delta": 2.51159292545053e+58,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.7967104188064695e-09,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.327699419292864e+63,
        "filterflow_gradient_max_abs": 274.3754691050723,
        "gradient_delta": [
          2.327699419292864e+63,
          -2.13390652285007e+63
        ],
        "gradient_explosion_ratio": 8.48362802580383e+60,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.327699419292864e+63,
        "relative_gradient_delta": 8.48362802580383e+60,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9457680739142234e-09,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.608531080608317e+65,
        "filterflow_gradient_max_abs": 184.24153726601756,
        "gradient_delta": [
          8.608531080608317e+65,
          -7.891826839433245e+65
        ],
        "gradient_explosion_ratio": 4.6724160080030545e+63,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.608531080608317e+65,
        "relative_gradient_delta": 4.6724160080030545e+63,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8393571938067907e-09,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.040869537495277e+67,
        "filterflow_gradient_max_abs": 187.1386096136716,
        "gradient_delta": [
          7.040869537495277e+67,
          -6.454681133888316e+67
        ],
        "gradient_explosion_ratio": 3.762382093161014e+65,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.040869537495277e+67,
        "relative_gradient_delta": 3.762382093161014e+65,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.6310544853913598e-09,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.0843844681903696e+70,
        "filterflow_gradient_max_abs": 954.1501022077981,
        "gradient_delta": [
          -3.0843844681903696e+70,
          2.827593687486406e+70
        ],
        "gradient_explosion_ratio": 3.232598792426311e+67,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.0843844681903696e+70,
        "relative_gradient_delta": 3.232598792426311e+67,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.98600263906701e-09,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.5168461838097026e+72,
        "filterflow_gradient_max_abs": 422.91186590476366,
        "gradient_delta": [
          3.5168461838097026e+72,
          -3.224050752854807e+72
        ],
        "gradient_explosion_ratio": 8.315789807140734e+69,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.5168461838097026e+72,
        "relative_gradient_delta": 8.315789807140734e+69,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5840096163374255e-09,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4959008227365065e+75,
        "filterflow_gradient_max_abs": 354.26740709319216,
        "gradient_delta": [
          1.4959008227365065e+75,
          -1.3713594275734873e+75
        ],
        "gradient_explosion_ratio": 4.222518901782576e+72,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4959008227365065e+75,
        "relative_gradient_delta": 4.222518901782576e+72,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.941782094647351e-09,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6287289721694605e+77,
        "filterflow_gradient_max_abs": 199.05378088782396,
        "gradient_delta": [
          -1.6287289721694605e+77,
          1.493128954117551e+77
        ],
        "gradient_explosion_ratio": 8.1823563707505e+74,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6287289721694605e+77,
        "relative_gradient_delta": 8.1823563707505e+74,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.940716280543711e-09,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.469528774955221e+79,
        "filterflow_gradient_max_abs": 548.7404094827189,
        "gradient_delta": [
          -6.469528774955221e+79,
          5.93090741264171e+79
        ],
        "gradient_explosion_ratio": 1.178978012764515e+77,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.469528774955221e+79,
        "relative_gradient_delta": 1.178978012764515e+77,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.836934408558591e-09,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.5057321850577086e+82,
        "filterflow_gradient_max_abs": 399.4756572109477,
        "gradient_delta": [
          4.5057321850577086e+82,
          -4.1306069337397316e+82
        ],
        "gradient_explosion_ratio": 1.1279115770196743e+80,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.5057321850577086e+82,
        "relative_gradient_delta": 1.1279115770196743e+80,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.73063721528888e-09,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5729007963180682e+85,
        "filterflow_gradient_max_abs": 381.20393707705813,
        "gradient_delta": [
          -1.5729007963180682e+85,
          1.4419487596167699e+85
        ],
        "gradient_explosion_ratio": 4.1261399564194836e+82,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5729007963180682e+85,
        "relative_gradient_delta": 4.1261399564194836e+82,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.649024276659475e-09,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.758767469941102e+87,
        "filterflow_gradient_max_abs": 48.850988576799736,
        "gradient_delta": [
          8.758767469941102e+87,
          -8.029555276830276e+87
        ],
        "gradient_explosion_ratio": 1.7929560332584156e+86,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.758767469941102e+87,
        "relative_gradient_delta": 1.7929560332584156e+86,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.737742642646481e-09,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.418052049452425e+89,
        "filterflow_gradient_max_abs": 346.85073969207997,
        "gradient_delta": [
          3.418052049452425e+89,
          -3.133481732942667e+89
        ],
        "gradient_explosion_ratio": 9.854532968523674e+86,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.418052049452425e+89,
        "relative_gradient_delta": 9.854532968523674e+86,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.721428581433429e-09,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.154514445761954e+90,
        "filterflow_gradient_max_abs": 322.6295207830076,
        "gradient_delta": [
          -5.154514445761954e+90,
          4.725374752763028e+90
        ],
        "gradient_explosion_ratio": 1.5976574100386644e+88,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.154514445761954e+90,
        "relative_gradient_delta": 1.5976574100386644e+88,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6360639771592105e-09,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6877474912794711e+93,
        "filterflow_gradient_max_abs": 86.66552831338745,
        "gradient_delta": [
          -1.6877474912794711e+93,
          1.5472338797483095e+93
        ],
        "gradient_explosion_ratio": 1.9474265306229722e+91,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6877474912794711e+93,
        "relative_gradient_delta": 1.9474265306229722e+91,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.636163453142217e-09,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.8419149860605016e+95,
        "filterflow_gradient_max_abs": 1118.3947944525503,
        "gradient_delta": [
          -3.8419149860605016e+95,
          3.522055911970354e+95
        ],
        "gradient_explosion_ratio": 3.435204638931732e+92,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.8419149860605016e+95,
        "relative_gradient_delta": 3.435204638931732e+92,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9218832625920186e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.612520712393806e+97,
        "filterflow_gradient_max_abs": 72.987643547552,
        "gradient_delta": [
          6.612520712393806e+97,
          -6.061994539844824e+97
        ],
        "gradient_explosion_ratio": 9.05978106840194e+95,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.612520712393806e+97,
        "relative_gradient_delta": 9.05978106840194e+95,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9393910356011475e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3941964956741784e+99,
        "filterflow_gradient_max_abs": 7.513193750877159,
        "gradient_delta": [
          3.3941964956741784e+99,
          -3.111612275994063e+99
        ],
        "gradient_explosion_ratio": 4.5176480312089765e+98,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3941964956741784e+99,
        "relative_gradient_delta": 4.5176480312089765e+98,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.889368827003636e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.049450889309273e+102,
        "filterflow_gradient_max_abs": 330.52600026078443,
        "gradient_delta": [
          2.049450889309273e+102,
          -1.8788236197700677e+102
        ],
        "gradient_explosion_ratio": 6.200573896432534e+99,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.049450889309273e+102,
        "relative_gradient_delta": 6.200573896432534e+99,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.899515377270291e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.96855706306533e+102,
        "filterflow_gradient_max_abs": 286.4569368626525,
        "gradient_delta": [
          4.96855706306533e+102,
          -4.55489927314666e+102
        ],
        "gradient_explosion_ratio": 1.734486557554584e+100,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.96855706306533e+102,
        "relative_gradient_delta": 1.734486557554584e+100,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.8836134308439796e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.589130758534633e+106,
        "filterflow_gradient_max_abs": 609.6787100623405,
        "gradient_delta": [
          -5.589130758534633e+106,
          5.1238070343180175e+106
        ],
        "gradient_explosion_ratio": 9.167337921252222e+103,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.589130758534633e+106,
        "relative_gradient_delta": 9.167337921252222e+103,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.874831122629985e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3575013199459115e+109,
        "filterflow_gradient_max_abs": 237.18680047332637,
        "gradient_delta": [
          3.3575013199459115e+109,
          -3.0779721613417506e+109
        ],
        "gradient_explosion_ratio": 1.4155515033913071e+107,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3575013199459115e+109,
        "relative_gradient_delta": 1.4155515033913071e+107,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.782176349886868e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.7959017396404847e+111,
        "filterflow_gradient_max_abs": 20.398532585564105,
        "gradient_delta": [
          2.7959017396404847e+111,
          -2.563128618695209e+111
        ],
        "gradient_explosion_ratio": 1.3706386613413184e+110,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.7959017396404847e+111,
        "relative_gradient_delta": 1.3706386613413184e+110,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.6820893001277e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.919285386000156e+113,
        "filterflow_gradient_max_abs": 478.6428510468603,
        "gradient_delta": [
          3.919285386000156e+113,
          -3.592984830355523e+113
        ],
        "gradient_explosion_ratio": 8.188329518404211e+110,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.919285386000156e+113,
        "relative_gradient_delta": 8.188329518404211e+110,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.958078309551638e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.5482570896275477e+114,
        "filterflow_gradient_max_abs": 310.27237965253573,
        "gradient_delta": [
          -4.5482570896275477e+114,
          4.169591422448787e+114
        ],
        "gradient_explosion_ratio": 1.4658917093171482e+112,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.5482570896275477e+114,
        "relative_gradient_delta": 1.4658917093171482e+112,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.521620328683639e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.831189728378784e+114,
        "filterflow_gradient_max_abs": 291.33394004387503,
        "gradient_delta": [
          -9.831189728378784e+114,
          9.012692896851932e+114
        ],
        "gradient_explosion_ratio": 3.3745432224265396e+112,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.831189728378784e+114,
        "relative_gradient_delta": 3.3745432224265396e+112,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.524789349285129e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.8285249988767256e+120,
        "filterflow_gradient_max_abs": 772.789629727978,
        "gradient_delta": [
          3.8285249988767256e+120,
          -3.509780709702022e+120
        ],
        "gradient_explosion_ratio": 4.9541619757816456e+117,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.8285249988767256e+120,
        "relative_gradient_delta": 4.9541619757816456e+117,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.415127818901965e-09,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3322505079134917e+123,
        "filterflow_gradient_max_abs": 137.0827775975205,
        "gradient_delta": [
          -1.3322505079134917e+123,
          1.2213338386290766e+123
        ],
        "gradient_explosion_ratio": 9.718584137717304e+120,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3322505079134917e+123,
        "relative_gradient_delta": 9.718584137717304e+120,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.988418484368594e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.400404768031929e+125,
        "filterflow_gradient_max_abs": 205.40967733109431,
        "gradient_delta": [
          3.400404768031929e+125,
          -3.1173036779226577e+125
        ],
        "gradient_explosion_ratio": 1.655425787243173e+123,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.400404768031929e+125,
        "relative_gradient_delta": 1.655425787243173e+123,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.800110448537453e-09,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.112651856237717e+128,
        "filterflow_gradient_max_abs": 1075.2940301638955,
        "gradient_delta": [
          -8.112651856237717e+128,
          7.437232092752576e+128
        ],
        "gradient_explosion_ratio": 7.544589320375185e+125,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.112651856237717e+128,
        "relative_gradient_delta": 7.544589320375185e+125,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.299266720408923e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.410083218900739e+130,
        "filterflow_gradient_max_abs": 1320.7702359098546,
        "gradient_delta": [
          9.410083218900739e+130,
          -8.626645658074242e+130
        ],
        "gradient_explosion_ratio": 7.124693578833039e+127,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.410083218900739e+130,
        "relative_gradient_delta": 7.124693578833039e+127,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.148105858803319e-09,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.784782482048012e+133,
        "filterflow_gradient_max_abs": 352.8826174689448,
        "gradient_delta": [
          -6.784782482048012e+133,
          6.219914636055145e+133
        ],
        "gradient_explosion_ratio": 1.9226740412185657e+131,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.784782482048012e+133,
        "relative_gradient_delta": 1.9226740412185657e+131,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.5889797800336964e-09,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3934731514551986e+136,
        "filterflow_gradient_max_abs": 974.6366511077524,
        "gradient_delta": [
          -2.3934731514551986e+136,
          2.1942042689108373e+136
        ],
        "gradient_explosion_ratio": 2.4557594347953415e+133,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3934731514551986e+136,
        "relative_gradient_delta": 2.4557594347953415e+133,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.8240451633319026e-09,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.2818231860703464e+139,
        "filterflow_gradient_max_abs": 731.310897142959,
        "gradient_delta": [
          -3.2818231860703464e+139,
          3.0085946192076625e+139
        ],
        "gradient_explosion_ratio": 4.4875896132432513e+136,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.2818231860703464e+139,
        "relative_gradient_delta": 4.4875896132432513e+136,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.972274953412125e-09,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.151581928063026e+141,
        "filterflow_gradient_max_abs": 483.3559108394908,
        "gradient_delta": [
          -2.151581928063026e+141,
          1.9724517271468008e+141
        ],
        "gradient_explosion_ratio": 4.451340885282992e+138,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.151581928063026e+141,
        "relative_gradient_delta": 4.451340885282992e+138,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.955818783651921e-09,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4494888168818575e+145,
        "filterflow_gradient_max_abs": 1076.6780654517022,
        "gradient_delta": [
          -2.4494888168818575e+145,
          2.2455563436689478e+145
        ],
        "gradient_explosion_ratio": 2.275042926461231e+142,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4494888168818575e+145,
        "relative_gradient_delta": 2.275042926461231e+142,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5558010697277496e-09,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.0748712900354187e+147,
        "filterflow_gradient_max_abs": 18.05494027199655,
        "gradient_delta": [
          -3.0748712900354187e+147,
          2.8188725270826938e+147
        ],
        "gradient_explosion_ratio": 1.703063673273173e+146,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.0748712900354187e+147,
        "relative_gradient_delta": 1.703063673273173e+146,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6730690428375965e-09,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.122089787777568e+149,
        "filterflow_gradient_max_abs": 989.4278480713913,
        "gradient_delta": [
          -5.122089787777568e+149,
          4.695649613304851e+149
        ],
        "gradient_explosion_ratio": 5.176819914419862e+146,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.122089787777568e+149,
        "relative_gradient_delta": 5.176819914419862e+146,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.355683813628275e-09,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.6474569900982215e+152,
        "filterflow_gradient_max_abs": 778.7073741209738,
        "gradient_delta": [
          -3.6474569900982215e+152,
          3.3437875388225334e+152
        ],
        "gradient_explosion_ratio": 4.683989276736426e+149,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.6474569900982215e+152,
        "relative_gradient_delta": 4.683989276736426e+149,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.821792577378801e-09,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.140094794049343e+156,
        "filterflow_gradient_max_abs": 1097.9215016104433,
        "gradient_delta": [
          1.140094794049343e+156,
          -1.0451760708262608e+156
        ],
        "gradient_explosion_ratio": 1.0384119378088866e+153,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.140094794049343e+156,
        "relative_gradient_delta": 1.0384119378088866e+153,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0083482493428164e-08,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.6022295637525246e+158,
        "filterflow_gradient_max_abs": 1697.7646785016034,
        "gradient_delta": [
          -2.6022295637525246e+158,
          2.385580642089209e+158
        ],
        "gradient_explosion_ratio": 1.5327386631987038e+155,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.6022295637525246e+158,
        "relative_gradient_delta": 1.5327386631987038e+155,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8990448324984754e-08,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.760361065299095e+161,
        "filterflow_gradient_max_abs": 947.0739014815089,
        "gradient_delta": [
          7.760361065299095e+161,
          -7.114271312137363e+161
        ],
        "gradient_explosion_ratio": 8.194039613127922e+158,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.760361065299095e+161,
        "relative_gradient_delta": 8.194039613127922e+158,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1565390423129429e-08,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1975937719345278e+164,
        "filterflow_gradient_max_abs": 249.89093531615012,
        "gradient_delta": [
          -1.1975937719345278e+164,
          1.0978879646935366e+164
        ],
        "gradient_explosion_ratio": 4.792465842826149e+161,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1975937719345278e+164,
        "relative_gradient_delta": 4.792465842826149e+161,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.132605782724568e-09,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.9428069369226944e+166,
        "filterflow_gradient_max_abs": 974.2890696675929,
        "gradient_delta": [
          4.9428069369226944e+166,
          -4.5312929768207145e+166
        ],
        "gradient_explosion_ratio": 5.073244780021064e+163,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.9428069369226944e+166,
        "relative_gradient_delta": 5.073244780021064e+163,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.223679515140248e-09,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7041317126159064e+170,
        "filterflow_gradient_max_abs": 1029.3299119039873,
        "gradient_delta": [
          -1.7041317126159064e+170,
          1.562254030856695e+170
        ],
        "gradient_explosion_ratio": 1.6555738766628425e+167,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7041317126159064e+170,
        "relative_gradient_delta": 1.6555738766628425e+167,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.178016403486254e-09,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.4044278143337413e+173,
        "filterflow_gradient_max_abs": 1426.254117759735,
        "gradient_delta": [
          3.4044278143337413e+173,
          -3.120991785041846e+173
        ],
        "gradient_explosion_ratio": 2.3869714183060098e+170,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.4044278143337413e+173,
        "relative_gradient_delta": 2.3869714183060098e+170,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.153612730486202e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3801574546657092e+176,
        "filterflow_gradient_max_abs": 1942.7454564725651,
        "gradient_delta": [
          -1.3801574546657092e+176,
          1.2652522870187287e+176
        ],
        "gradient_explosion_ratio": 7.104159992074595e+172,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3801574546657092e+176,
        "relative_gradient_delta": 7.104159992074595e+172,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.01524527357833e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.272437154374405e+178,
        "filterflow_gradient_max_abs": 169.06130724664092,
        "gradient_delta": [
          -7.272437154374405e+178,
          6.66696956254234e+178
        ],
        "gradient_explosion_ratio": 4.30165676157038e+176,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.272437154374405e+178,
        "relative_gradient_delta": 4.30165676157038e+176,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.081496278260602e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.0189658703985194e+181,
        "filterflow_gradient_max_abs": 1963.5208371745916,
        "gradient_delta": [
          3.0189658703985194e+181,
          -2.7676215195884345e+181
        ],
        "gradient_explosion_ratio": 1.5375267800787185e+178,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.0189658703985194e+181,
        "relative_gradient_delta": 1.5375267800787185e+178,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.653859933678177e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.9296478290468727e+184,
        "filterflow_gradient_max_abs": 1119.9768301540837,
        "gradient_delta": [
          1.9296478290468727e+184,
          -1.7689947770731994e+184
        ],
        "gradient_explosion_ratio": 1.7229354903542034e+181,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.9296478290468727e+184,
        "relative_gradient_delta": 1.7229354903542034e+181,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.3080741458397824e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.295151573851639e+186,
        "filterflow_gradient_max_abs": 979.6868013870265,
        "gradient_delta": [
          -6.295151573851639e+186,
          5.771048005442643e+186
        ],
        "gradient_explosion_ratio": 6.425677639975401e+183,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.295151573851639e+186,
        "relative_gradient_delta": 6.425677639975401e+183,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.394845624730806e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.967476141548906e+190,
        "filterflow_gradient_max_abs": 2882.4178802677957,
        "gradient_delta": [
          -4.967476141548906e+190,
          4.5539083439780825e+190
        ],
        "gradient_explosion_ratio": 1.7233712625621773e+187,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.967476141548906e+190,
        "relative_gradient_delta": 1.7233712625621773e+187,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.620751946684322e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.626750271859786e+192,
        "filterflow_gradient_max_abs": 858.8073873147812,
        "gradient_delta": [
          5.626750271859786e+192,
          -5.158294530733975e+192
        ],
        "gradient_explosion_ratio": 6.551818667341524e+189,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.626750271859786e+192,
        "relative_gradient_delta": 6.551818667341524e+189,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.615852837261627e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.9451455218623233e+195,
        "filterflow_gradient_max_abs": 442.0116504772855,
        "gradient_delta": [
          -3.9451455218623233e+195,
          3.6166919776316607e+195
        ],
        "gradient_explosion_ratio": 8.925433340054144e+192,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.9451455218623233e+195,
        "relative_gradient_delta": 8.925433340054144e+192,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.274422841874184e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.399469849071215e+199,
        "filterflow_gradient_max_abs": 3282.5855155180925,
        "gradient_delta": [
          -1.399469849071215e+199,
          1.2829568258065103e+199
        ],
        "gradient_explosion_ratio": 4.263315738326883e+195,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.399469849071215e+199,
        "relative_gradient_delta": 4.263315738326883e+195,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0136062655874412e-08,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.089349593078591e+201,
        "filterflow_gradient_max_abs": 1855.9144036285215,
        "gradient_delta": [
          -3.089349593078591e+201,
          2.8321454373405736e+201
        ],
        "gradient_explosion_ratio": 1.6645970239999026e+198,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.089349593078591e+201,
        "relative_gradient_delta": 1.6645970239999026e+198,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.873637741795392e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.440224674995345e+205,
        "filterflow_gradient_max_abs": 1310.8611477302254,
        "gradient_delta": [
          1.440224674995345e+205,
          -1.320318604010319e+205
        ],
        "gradient_explosion_ratio": 1.0986859115392308e+202,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.440224674995345e+205,
        "relative_gradient_delta": 1.0986859115392308e+202,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.93335175330867e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.107386979416728e+208,
        "filterflow_gradient_max_abs": 914.416967723082,
        "gradient_delta": [
          -4.107386979416728e+208,
          3.7654260039748247e+208
        ],
        "gradient_explosion_ratio": 4.491809671515841e+205,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.107386979416728e+208,
        "relative_gradient_delta": 4.491809671515841e+205,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.058265166255296e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.9367867995185035e+212,
        "filterflow_gradient_max_abs": 3551.3298618369327,
        "gradient_delta": [
          2.9367867995185035e+212,
          -2.692284276707551e+212
        ],
        "gradient_explosion_ratio": 8.269541027651665e+208,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.9367867995185035e+212,
        "relative_gradient_delta": 8.269541027651665e+208,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.786315675024525e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4769283366511616e+215,
        "filterflow_gradient_max_abs": 3023.0985131010166,
        "gradient_delta": [
          -1.4769283366511616e+215,
          1.353966498092979e+215
        ],
        "gradient_explosion_ratio": 4.8854786909877e+211,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4769283366511616e+215,
        "relative_gradient_delta": 4.8854786909877e+211,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.745331570025883e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.53418380202861e+218,
        "filterflow_gradient_max_abs": 2001.070628323309,
        "gradient_delta": [
          1.53418380202861e+218,
          -1.4064551531143616e+218
        ],
        "gradient_explosion_ratio": 7.666814855576078e+214,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.53418380202861e+218,
        "relative_gradient_delta": 7.666814855576078e+214,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.205052720062668e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.9757700467302206e+221,
        "filterflow_gradient_max_abs": 2346.9001573329506,
        "gradient_delta": [
          -1.9757700467302206e+221,
          1.811277084217906e+221
        ],
        "gradient_explosion_ratio": 8.41863698614053e+217,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.9757700467302206e+221,
        "relative_gradient_delta": 8.41863698614053e+217,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.456598728414974e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.830732685490335e+224,
        "filterflow_gradient_max_abs": 4046.6212127655212,
        "gradient_delta": [
          2.830732685490335e+224,
          -2.5950597101421433e+224
        ],
        "gradient_explosion_ratio": 6.995299378554313e+220,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.830732685490335e+224,
        "relative_gradient_delta": 6.995299378554313e+220,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.6329352092725458e-08,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3832594583394986e+228,
        "filterflow_gradient_max_abs": 2730.4139020142047,
        "gradient_delta": [
          -1.3832594583394986e+228,
          1.2680960330198352e+228
        ],
        "gradient_explosion_ratio": 5.0661163764185315e+224,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3832594583394986e+228,
        "relative_gradient_delta": 5.0661163764185315e+224,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.300094916397939e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_raw_transport_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      1.5603365296363644e+227,
      -1.5137105419841878e+227
    ],
    "final_bayesfilter_gradient_max_abs": 1.5603365296363644e+227,
    "final_filterflow_gradient_diag": [
      18935.6850725171,
      2073.5151524806142
    ],
    "final_filterflow_gradient_max_abs": 18935.6850725171,
    "final_gradient_delta": [
      1.5603365296363644e+227,
      -1.5137105419841878e+227
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 1.5603365296363644e+227,
    "final_relative_gradient_delta": 8.240190537922537e+222,
    "final_scalar_delta": 9.3001517598168e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "bayesfilter_gradient_max_abs": 138676775.4293832,
      "filterflow_gradient_max_abs": 56.8762754108451,
      "gradient_explosion_ratio": 2438218.298010078,
      "resampling_flag": [
        true
      ],
      "status": "explosion",
      "time_index": 9,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 1.0040080173332893,
      "max_abs_gradient_delta": 0.03535723378440209,
      "relative_gradient_delta": 0.004017858589300954,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.7926993223227328e-11,
      "status": "failure",
      "time_index": 1,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_scalar_failure": {
      "status": "no_failure"
    },
    "mode": "normalized_weights_stop_gradient",
    "mode_description": "Stop gradient through normalized weights after each update",
    "sample_rows": [
      {
        "bayesfilter_gradient_max_abs": 0.008913771203554865,
        "filterflow_gradient_max_abs": 0.008913771203554867,
        "gradient_delta": [
          -1.734723475976807e-18,
          -5.766308833278761e-19
        ],
        "gradient_explosion_ratio": 0.008913771203554865,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 1.734723475976807e-18,
        "relative_gradient_delta": 1.734723475976807e-18,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.835290093284096,
        "filterflow_gradient_max_abs": 8.800019462744133,
        "gradient_delta": [
          -0.035270630539962156,
          0.03535723378440209
        ],
        "gradient_explosion_ratio": 1.0040080173332893,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.03535723378440209,
        "relative_gradient_delta": 0.004017858589300954,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7926993223227328e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.1218839451571885,
        "filterflow_gradient_max_abs": 1.4485716238559057,
        "gradient_delta": [
          -7.570455569013094,
          -1.0316804040634353
        ],
        "gradient_explosion_ratio": 4.226152055126929,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.570455569013094,
        "relative_gradient_delta": 5.22615205512693,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4985346297180513e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 89.7932252043885,
        "filterflow_gradient_max_abs": 16.840076774872443,
        "gradient_delta": [
          -100.81687066282139,
          89.7932252043885
        ],
        "gradient_explosion_ratio": 5.332114954390916,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 100.81687066282139,
        "relative_gradient_delta": 5.986722745424362,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.4439117396468646e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 343.1965469854467,
        "filterflow_gradient_max_abs": 11.278780998887767,
        "gradient_delta": [
          -306.7402487668241,
          343.1965469854467
        ],
        "gradient_explosion_ratio": 30.42851412925655,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 343.1965469854467,
        "relative_gradient_delta": 30.42851412925655,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.665601073204016e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7331.748028364517,
        "filterflow_gradient_max_abs": 0.16051708831084313,
        "gradient_delta": [
          -7331.908545452829,
          7149.070035407609
        ],
        "gradient_explosion_ratio": 7331.748028364517,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7331.908545452829,
        "relative_gradient_delta": 7331.908545452829,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.347366828165832e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 61021.92967742947,
        "filterflow_gradient_max_abs": 6.732984884221974,
        "gradient_delta": [
          -60253.49027026898,
          61021.92967742947
        ],
        "gradient_explosion_ratio": 9063.131839257177,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 61021.92967742947,
        "relative_gradient_delta": 9063.131839257177,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.53681536782824e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 519861.8398747263,
        "filterflow_gradient_max_abs": 16.75562828027451,
        "gradient_delta": [
          519878.5955030066,
          -514268.363291547
        ],
        "gradient_explosion_ratio": 31026.10246413328,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 519878.5955030066,
        "relative_gradient_delta": 31027.102464133284,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.6477489351891563e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5351138.431716598,
        "filterflow_gradient_max_abs": 8.578663144440544,
        "gradient_delta": [
          5226363.187153895,
          -5351138.431716598
        ],
        "gradient_explosion_ratio": 623772.9983819724,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5351138.431716598,
        "relative_gradient_delta": 623772.9983819724,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.839595473844383e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 138676775.4293832,
        "filterflow_gradient_max_abs": 56.8762754108451,
        "gradient_delta": [
          -138676832.3056586,
          134738929.25274953
        ],
        "gradient_explosion_ratio": 2438218.298010078,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 138676832.3056586,
        "relative_gradient_delta": 2438219.298010078,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.645795108146558e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 26535171059.102966,
        "filterflow_gradient_max_abs": 104.45156511568617,
        "gradient_delta": [
          26535170954.6514,
          -25896062602.07456
        ],
        "gradient_explosion_ratio": 254042828.65186104,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 26535170954.6514,
        "relative_gradient_delta": 254042827.65186104,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.562661608062626e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 668931253976.1555,
        "filterflow_gradient_max_abs": 9.13071410440192,
        "gradient_delta": [
          668931253985.2863,
          -654049847055.5708
        ],
        "gradient_explosion_ratio": 73261657996.02286,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 668931253985.2863,
        "relative_gradient_delta": 73261657997.02286,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.412914561020443e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2040377199131.7288,
        "filterflow_gradient_max_abs": 62.46161279976278,
        "gradient_delta": [
          -2040377199194.1904,
          1968369837515.8564
        ],
        "gradient_explosion_ratio": 32666098547.162037,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2040377199194.1904,
        "relative_gradient_delta": 32666098548.162037,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.171952003976912e-11,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 217244106739928.06,
        "filterflow_gradient_max_abs": 78.21898890138324,
        "gradient_delta": [
          217244106739849.84,
          -211290643095774.62
        ],
        "gradient_explosion_ratio": 2777383213350.2085,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 217244106739849.84,
        "relative_gradient_delta": 2777383213349.2085,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1748113593057496e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0546304672504616e+16,
        "filterflow_gradient_max_abs": 55.1203162059954,
        "gradient_delta": [
          2.054630467250456e+16,
          -1.99546095009965e+16
        ],
        "gradient_explosion_ratio": 372753751914612.7,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.054630467250456e+16,
        "relative_gradient_delta": 372753751914611.7,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1169021263413015e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4007046194887652e+18,
        "filterflow_gradient_max_abs": 3.2014311273644616,
        "gradient_delta": [
          -1.4007046194887652e+18,
          1.3576806974945503e+18
        ],
        "gradient_explosion_ratio": 4.375245206795618e+17,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4007046194887652e+18,
        "relative_gradient_delta": 4.375245206795618e+17,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.603695616533514e-11,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.743676040271843e+18,
        "filterflow_gradient_max_abs": 25.054390338542845,
        "gradient_delta": [
          9.743676040271843e+18,
          -9.449399150425184e+18
        ],
        "gradient_explosion_ratio": 3.889009434519145e+17,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.743676040271843e+18,
        "relative_gradient_delta": 3.889009434519145e+17,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1939249588976963e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.376174364334969e+20,
        "filterflow_gradient_max_abs": 145.3600680670563,
        "gradient_delta": [
          -3.376174364334969e+20,
          3.2774871838658606e+20
        ],
        "gradient_explosion_ratio": 2.322628497103827e+18,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.376174364334969e+20,
        "relative_gradient_delta": 2.322628497103827e+18,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.48947520983711e-09,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.613242406063426e+22,
        "filterflow_gradient_max_abs": 168.66458545141114,
        "gradient_delta": [
          9.613242406063426e+22,
          -9.327577932655434e+22
        ],
        "gradient_explosion_ratio": 5.6996211625189134e+20,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.613242406063426e+22,
        "relative_gradient_delta": 5.6996211625189134e+20,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.252356523513299e-09,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.2495467022693376e+23,
        "filterflow_gradient_max_abs": 101.15910809775511,
        "gradient_delta": [
          5.2495467022693376e+23,
          -5.103887444113118e+23
        ],
        "gradient_explosion_ratio": 5.189395993088866e+21,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.2495467022693376e+23,
        "relative_gradient_delta": 5.189395993088866e+21,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.767464479802584e-09,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0222999314574275e+26,
        "filterflow_gradient_max_abs": 125.28072286451086,
        "gradient_delta": [
          -2.0222999314574275e+26,
          1.961656978906584e+26
        ],
        "gradient_explosion_ratio": 1.6142147692143453e+24,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0222999314574275e+26,
        "relative_gradient_delta": 1.6142147692143453e+24,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9853310934413457e-09,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.9543076477168178e+29,
        "filterflow_gradient_max_abs": 278.9526477486435,
        "gradient_delta": [
          2.9543076477168178e+29,
          -2.8665609970555817e+29
        ],
        "gradient_explosion_ratio": 1.0590713770097864e+27,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.9543076477168178e+29,
        "relative_gradient_delta": 1.0590713770097864e+27,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.0152165209074155e-09,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.297401108209508e+31,
        "filterflow_gradient_max_abs": 252.28215416061428,
        "gradient_delta": [
          -4.297401108209508e+31,
          4.169696938836742e+31
        ],
        "gradient_explosion_ratio": 1.703410660380515e+29,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.297401108209508e+31,
        "relative_gradient_delta": 1.703410660380515e+29,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.021582983819826e-09,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.025262146340404e+33,
        "filterflow_gradient_max_abs": 69.58591013728201,
        "gradient_delta": [
          -2.025262146340404e+33,
          1.965034192269162e+33
        ],
        "gradient_explosion_ratio": 2.9104485984948413e+31,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.025262146340404e+33,
        "relative_gradient_delta": 2.9104485984948413e+31,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9725839567618095e-09,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.101467207805217e+34,
        "filterflow_gradient_max_abs": 64.72471139759364,
        "gradient_delta": [
          9.101467207805217e+34,
          -8.832322237000889e+34
        ],
        "gradient_explosion_ratio": 1.4061811959108395e+33,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.101467207805217e+34,
        "relative_gradient_delta": 1.4061811959108395e+33,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.974680057832302e-09,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.169179297972906e+37,
        "filterflow_gradient_max_abs": 0.6534447816938739,
        "gradient_delta": [
          -2.169179297972906e+37,
          2.1048339423252652e+37
        ],
        "gradient_explosion_ratio": 2.169179297972906e+37,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.169179297972906e+37,
        "relative_gradient_delta": 2.169179297972906e+37,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.903298934597842e-09,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.453848334227833e+39,
        "filterflow_gradient_max_abs": 262.5095687458148,
        "gradient_delta": [
          1.453848334227833e+39,
          -1.4106379036561675e+39
        ],
        "gradient_explosion_ratio": 5.538267961712202e+36,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.453848334227833e+39,
        "relative_gradient_delta": 5.538267961712202e+36,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.970814705349767e-09,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2353695881529585e+41,
        "filterflow_gradient_max_abs": 28.548993251385596,
        "gradient_delta": [
          2.2353695881529585e+41,
          -2.1689049129278494e+41
        ],
        "gradient_explosion_ratio": 7.829941912380631e+39,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2353695881529585e+41,
        "relative_gradient_delta": 7.829941912380631e+39,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9090827524669294e-09,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.449310571887383e+42,
        "filterflow_gradient_max_abs": 485.70702239538065,
        "gradient_delta": [
          -2.449310571887383e+42,
          2.3755127058290977e+42
        ],
        "gradient_explosion_ratio": 5.0427736453305135e+39,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.449310571887383e+42,
        "relative_gradient_delta": 5.0427736453305135e+39,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8526088158287166e-09,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.048403857067737e+44,
        "filterflow_gradient_max_abs": 245.11951564783823,
        "gradient_delta": [
          5.048403857067737e+44,
          -4.897987100287338e+44
        ],
        "gradient_explosion_ratio": 2.059568306393339e+42,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.048403857067737e+44,
        "relative_gradient_delta": 2.059568306393339e+42,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8581510491676454e-09,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.5642430848470543e+47,
        "filterflow_gradient_max_abs": 434.75519438634416,
        "gradient_delta": [
          -3.5642430848470543e+47,
          3.4577260970940827e+47
        ],
        "gradient_explosion_ratio": 8.198276020319836e+44,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.5642430848470543e+47,
        "relative_gradient_delta": 8.198276020319836e+44,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9084219477226725e-09,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5035185192844977e+48,
        "filterflow_gradient_max_abs": 251.90780939902413,
        "gradient_delta": [
          1.5035185192844977e+48,
          -1.4581547541790926e+48
        ],
        "gradient_explosion_ratio": 5.968526830793529e+45,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5035185192844977e+48,
        "relative_gradient_delta": 5.968526830793529e+45,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.980804936214554e-09,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.184671870338196e+51,
        "filterflow_gradient_max_abs": 369.7748801823844,
        "gradient_delta": [
          7.184671870338196e+51,
          -6.969913421072586e+51
        ],
        "gradient_explosion_ratio": 1.9429853825642496e+49,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.184671870338196e+51,
        "relative_gradient_delta": 1.9429853825642496e+49,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9715820915043878e-09,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3788816636210585e+53,
        "filterflow_gradient_max_abs": 153.94165873710156,
        "gradient_delta": [
          -2.3788816636210585e+53,
          2.3078791888482133e+53
        ],
        "gradient_explosion_ratio": 1.545313778698243e+51,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3788816636210585e+53,
        "relative_gradient_delta": 1.545313778698243e+51,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.075740551139461e-09,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.31870425760955e+55,
        "filterflow_gradient_max_abs": 231.88010181357106,
        "gradient_delta": [
          -4.31870425760955e+55,
          4.189751533653702e+55
        ],
        "gradient_explosion_ratio": 1.8624729866134605e+53,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.31870425760955e+55,
        "relative_gradient_delta": 1.8624729866134605e+53,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8847040312030003e-09,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.2627433019466935e+58,
        "filterflow_gradient_max_abs": 317.10552544548756,
        "gradient_delta": [
          -4.2627433019466935e+58,
          4.135375919471528e+58
        ],
        "gradient_explosion_ratio": 1.344266485409913e+56,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.2627433019466935e+58,
        "relative_gradient_delta": 1.344266485409913e+56,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8788775807697675e-09,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.82409544978152e+61,
        "filterflow_gradient_max_abs": 440.433114763931,
        "gradient_delta": [
          5.82409544978152e+61,
          -5.650058747697386e+61
        ],
        "gradient_explosion_ratio": 1.3223563929572357e+59,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.82409544978152e+61,
        "relative_gradient_delta": 1.3223563929572357e+59,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.7967104188064695e-09,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6806171460944403e+63,
        "filterflow_gradient_max_abs": 274.3754691050723,
        "gradient_delta": [
          -1.6806171460944403e+63,
          1.6303971626672697e+63
        ],
        "gradient_explosion_ratio": 6.125245640858829e+60,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6806171460944403e+63,
        "relative_gradient_delta": 6.125245640858829e+60,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.9457680739142234e-09,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.927199976781353e+66,
        "filterflow_gradient_max_abs": 184.24153726601756,
        "gradient_delta": [
          1.927199976781353e+66,
          -1.8696113671678724e+66
        ],
        "gradient_explosion_ratio": 1.0460181810135252e+64,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.927199976781353e+66,
        "relative_gradient_delta": 1.0460181810135252e+64,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.8393571938067907e-09,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.885227163292527e+68,
        "filterflow_gradient_max_abs": 187.1386096136716,
        "gradient_delta": [
          2.885227163292527e+68,
          -2.799010795044669e+68
        ],
        "gradient_explosion_ratio": 1.5417594312839992e+66,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.885227163292527e+68,
        "relative_gradient_delta": 1.5417594312839992e+66,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.6310544853913598e-09,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.395960323948381e+71,
        "filterflow_gradient_max_abs": 954.1501022077981,
        "gradient_delta": [
          5.395960323948381e+71,
          -5.234718198291619e+71
        ],
        "gradient_explosion_ratio": 5.65525310059992e+68,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.395960323948381e+71,
        "relative_gradient_delta": 5.65525310059992e+68,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.98600263906701e-09,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.840535492374637e+73,
        "filterflow_gradient_max_abs": 422.91186590476366,
        "gradient_delta": [
          -2.840535492374637e+73,
          2.7556545893840778e+73
        ],
        "gradient_explosion_ratio": 6.7166133688344e+70,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.840535492374637e+73,
        "relative_gradient_delta": 6.7166133688344e+70,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5840096163374255e-09,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.019177052840649e+75,
        "filterflow_gradient_max_abs": 354.26740709319216,
        "gradient_delta": [
          -4.019177052840649e+75,
          3.899075973454738e+75
        ],
        "gradient_explosion_ratio": 1.1345037596934173e+73,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.019177052840649e+75,
        "relative_gradient_delta": 1.1345037596934173e+73,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.941782094647351e-09,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3528504668591693e+78,
        "filterflow_gradient_max_abs": 199.05378088782396,
        "gradient_delta": [
          -1.3528504668591693e+78,
          1.312424578999676e+78
        ],
        "gradient_explosion_ratio": 6.7964067842628085e+75,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3528504668591693e+78,
        "relative_gradient_delta": 6.7964067842628085e+75,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.940716280543711e-09,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5052449871733253e+81,
        "filterflow_gradient_max_abs": 548.7404094827189,
        "gradient_delta": [
          -1.5052449871733253e+81,
          1.460265245193604e+81
        ],
        "gradient_explosion_ratio": 2.743091197880387e+78,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5052449871733253e+81,
        "relative_gradient_delta": 2.743091197880387e+78,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.836934408558591e-09,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3266914914346996e+83,
        "filterflow_gradient_max_abs": 399.4756572109477,
        "gradient_delta": [
          1.3266914914346996e+83,
          -1.287047286393474e+83
        ],
        "gradient_explosion_ratio": 3.3210821923352516e+80,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3266914914346996e+83,
        "relative_gradient_delta": 3.3210821923352516e+80,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.73063721528888e-09,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.6219079655041014e+85,
        "filterflow_gradient_max_abs": 381.20393707705813,
        "gradient_delta": [
          -5.6219079655041014e+85,
          5.453914069683832e+85
        ],
        "gradient_explosion_ratio": 1.4747769943330008e+83,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.6219079655041014e+85,
        "relative_gradient_delta": 1.4747769943330008e+83,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.649024276659475e-09,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3376868334412006e+88,
        "filterflow_gradient_max_abs": 48.850988576799736,
        "gradient_delta": [
          3.3376868334412006e+88,
          -3.237950050536323e+88
        ],
        "gradient_explosion_ratio": 6.832383398329694e+86,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3376868334412006e+88,
        "relative_gradient_delta": 6.832383398329694e+86,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.737742642646481e-09,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.720918302076503e+89,
        "filterflow_gradient_max_abs": 346.85073969207997,
        "gradient_delta": [
          3.720918302076503e+89,
          -3.6097297935295216e+89
        ],
        "gradient_explosion_ratio": 1.07277219745294e+87,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.720918302076503e+89,
        "relative_gradient_delta": 1.07277219745294e+87,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.721428581433429e-09,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.234494393433482e+90,
        "filterflow_gradient_max_abs": 322.6295207830076,
        "gradient_delta": [
          -4.234494393433482e+90,
          4.107959199724047e+90
        ],
        "gradient_explosion_ratio": 1.3124944001269788e+88,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.234494393433482e+90,
        "relative_gradient_delta": 1.3124944001269788e+88,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6360639771592105e-09,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.163057905752182e+93,
        "filterflow_gradient_max_abs": 86.66552831338745,
        "gradient_delta": [
          8.163057905752182e+93,
          -7.919129348443703e+93
        ],
        "gradient_explosion_ratio": 9.419036685767497e+91,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.163057905752182e+93,
        "relative_gradient_delta": 9.419036685767497e+91,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.636163453142217e-09,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.7073997527613143e+96,
        "filterflow_gradient_max_abs": 1118.3947944525503,
        "gradient_delta": [
          -2.7073997527613143e+96,
          2.6264972132706137e+96
        ],
        "gradient_explosion_ratio": 2.42079073167233e+93,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.7073997527613143e+96,
        "relative_gradient_delta": 2.42079073167233e+93,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9218832625920186e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5088540112354405e+98,
        "filterflow_gradient_max_abs": 72.987643547552,
        "gradient_delta": [
          -1.5088540112354405e+98,
          1.4637664245067576e+98
        ],
        "gradient_explosion_ratio": 2.0672732231071563e+96,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5088540112354405e+98,
        "relative_gradient_delta": 2.0672732231071563e+96,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9393910356011475e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4165591513055662e+100,
        "filterflow_gradient_max_abs": 7.513193750877159,
        "gradient_delta": [
          1.4165591513055662e+100,
          -1.3742295202795457e+100
        ],
        "gradient_explosion_ratio": 1.8854287514416677e+99,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4165591513055662e+100,
        "relative_gradient_delta": 1.8854287514416677e+99,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.889368827003636e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.360333011512068e+101,
        "filterflow_gradient_max_abs": 330.52600026078443,
        "gradient_delta": [
          -5.360333011512068e+101,
          5.2001555006382316e+101
        ],
        "gradient_explosion_ratio": 1.6217583510170983e+99,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.360333011512068e+101,
        "relative_gradient_delta": 1.6217583510170983e+99,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.899515377270291e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0593218329311244e+103,
        "filterflow_gradient_max_abs": 286.4569368626525,
        "gradient_delta": [
          2.0593218329311244e+103,
          -1.9977851631676813e+103
        ],
        "gradient_explosion_ratio": 7.188940353427389e+100,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0593218329311244e+103,
        "relative_gradient_delta": 7.188940353427389e+100,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.8836134308439796e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3181486495182084e+107,
        "filterflow_gradient_max_abs": 609.6787100623405,
        "gradient_delta": [
          1.3181486495182084e+107,
          -1.2787597218426543e+107
        ],
        "gradient_explosion_ratio": 2.1620381813618287e+104,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3181486495182084e+107,
        "relative_gradient_delta": 2.1620381813618287e+104,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.874831122629985e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6597846008942415e+109,
        "filterflow_gradient_max_abs": 237.18680047332637,
        "gradient_delta": [
          1.6597846008942415e+109,
          -1.6101869052013102e+109
        ],
        "gradient_explosion_ratio": 6.997794976710342e+106,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6597846008942415e+109,
        "relative_gradient_delta": 6.997794976710342e+106,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.782176349886868e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.981605959438117e+111,
        "filterflow_gradient_max_abs": 20.398532585564105,
        "gradient_delta": [
          -5.981605959438117e+111,
          5.802863565979992e+111
        ],
        "gradient_explosion_ratio": 2.9323707155637543e+110,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.981605959438117e+111,
        "relative_gradient_delta": 2.9323707155637543e+110,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.6820893001277e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7233695887651484e+112,
        "filterflow_gradient_max_abs": 478.6428510468603,
        "gradient_delta": [
          -1.7233695887651484e+112,
          1.671871845860714e+112
        ],
        "gradient_explosion_ratio": 3.6005334353075426e+109,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7233695887651484e+112,
        "relative_gradient_delta": 3.6005334353075426e+109,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.958078309551638e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.7130420751215878e+115,
        "filterflow_gradient_max_abs": 310.27237965253573,
        "gradient_delta": [
          -2.7130420751215878e+115,
          2.6319709318157342e+115
        ],
        "gradient_explosion_ratio": 8.744065708200769e+112,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.7130420751215878e+115,
        "relative_gradient_delta": 8.744065708200769e+112,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.521620328683639e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.176220437235253e+117,
        "filterflow_gradient_max_abs": 291.33394004387503,
        "gradient_delta": [
          -4.176220437235253e+117,
          4.051426587344269e+117
        ],
        "gradient_explosion_ratio": 1.4334822906683347e+115,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.176220437235253e+117,
        "relative_gradient_delta": 1.4334822906683347e+115,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.524789349285129e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0270418287558663e+121,
        "filterflow_gradient_max_abs": 772.789629727978,
        "gradient_delta": [
          -1.0270418287558663e+121,
          9.96351757270378e+120
        ],
        "gradient_explosion_ratio": 1.329005707694842e+118,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0270418287558663e+121,
        "relative_gradient_delta": 1.329005707694842e+118,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.415127818901965e-09,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.45363552761052e+123,
        "filterflow_gradient_max_abs": 137.0827775975205,
        "gradient_delta": [
          -1.45363552761052e+123,
          1.4101979800753536e+123
        ],
        "gradient_explosion_ratio": 1.0604071153842836e+121,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.45363552761052e+123,
        "relative_gradient_delta": 1.0604071153842836e+121,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.988418484368594e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.050413049688657e+124,
        "filterflow_gradient_max_abs": 205.40967733109431,
        "gradient_delta": [
          5.050413049688657e+124,
          -4.899496569827016e+124
        ],
        "gradient_explosion_ratio": 2.4587025866108698e+122,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.050413049688657e+124,
        "relative_gradient_delta": 2.4587025866108698e+122,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.800110448537453e-09,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.496480140810575e+128,
        "filterflow_gradient_max_abs": 1075.2940301638955,
        "gradient_delta": [
          2.496480140810575e+128,
          -2.4218803028830992e+128
        ],
        "gradient_explosion_ratio": 2.3216720922649066e+125,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.496480140810575e+128,
        "relative_gradient_delta": 2.3216720922649066e+125,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.299266720408923e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.2246409441859335e+131,
        "filterflow_gradient_max_abs": 1320.7702359098546,
        "gradient_delta": [
          -3.2246409441859335e+131,
          3.128282199779605e+131
        ],
        "gradient_explosion_ratio": 2.4414851701776402e+128,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.2246409441859335e+131,
        "relative_gradient_delta": 2.4414851701776402e+128,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.148105858803319e-09,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2478372699454514e+133,
        "filterflow_gradient_max_abs": 352.8826174689448,
        "gradient_delta": [
          -1.2478372699454514e+133,
          1.2105493874689027e+133
        ],
        "gradient_explosion_ratio": 3.5361256354749934e+130,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2478372699454514e+133,
        "relative_gradient_delta": 3.5361256354749934e+130,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.5889797800336964e-09,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.776089610199004e+136,
        "filterflow_gradient_max_abs": 974.6366511077524,
        "gradient_delta": [
          -1.776089610199004e+136,
          1.723016487406909e+136
        ],
        "gradient_explosion_ratio": 1.8223094813645025e+133,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.776089610199004e+136,
        "relative_gradient_delta": 1.8223094813645025e+133,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.8240451633319026e-09,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.463020444109193e+138,
        "filterflow_gradient_max_abs": 731.310897142959,
        "gradient_delta": [
          5.463020444109193e+138,
          -5.299774427027236e+138
        ],
        "gradient_explosion_ratio": 7.470175086207233e+135,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.463020444109193e+138,
        "relative_gradient_delta": 7.470175086207233e+135,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.972274953412125e-09,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.578634822547375e+140,
        "filterflow_gradient_max_abs": 483.3559108394908,
        "gradient_delta": [
          -5.578634822547375e+140,
          5.411934015758747e+140
        ],
        "gradient_explosion_ratio": 1.1541463955325223e+138,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.578634822547375e+140,
        "relative_gradient_delta": 1.1541463955325223e+138,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.955818783651921e-09,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.7681760238294724e+144,
        "filterflow_gradient_max_abs": 1076.6780654517022,
        "gradient_delta": [
          4.7681760238294724e+144,
          -4.625693352823689e+144
        ],
        "gradient_explosion_ratio": 4.428599575704242e+141,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.7681760238294724e+144,
        "relative_gradient_delta": 4.428599575704242e+141,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.5558010697277496e-09,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.568408832181668e+146,
        "filterflow_gradient_max_abs": 18.05494027199655,
        "gradient_delta": [
          6.568408832181668e+146,
          -6.372131591159103e+146
        ],
        "gradient_explosion_ratio": 3.6380119420108836e+145,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.568408832181668e+146,
        "relative_gradient_delta": 3.6380119420108836e+145,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.6730690428375965e-09,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.819647024116914e+148,
        "filterflow_gradient_max_abs": 989.4278480713913,
        "gradient_delta": [
          -7.819647024116914e+148,
          7.585980274242243e+148
        ],
        "gradient_explosion_ratio": 7.903200864377423e+145,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.819647024116914e+148,
        "relative_gradient_delta": 7.903200864377423e+145,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.355683813628275e-09,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.89416861418387e+151,
        "filterflow_gradient_max_abs": 778.7073741209738,
        "gradient_delta": [
          7.89416861418387e+151,
          -7.658275009606833e+151
        ],
        "gradient_explosion_ratio": 1.0137529034054702e+149,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.89416861418387e+151,
        "relative_gradient_delta": 1.0137529034054702e+149,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.821792577378801e-09,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1895304330286e+155,
        "filterflow_gradient_max_abs": 1097.9215016104433,
        "gradient_delta": [
          -1.1895304330286e+155,
          1.1539848758818958e+155
        ],
        "gradient_explosion_ratio": 1.0834385074741533e+152,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1895304330286e+155,
        "relative_gradient_delta": 1.0834385074741533e+152,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0083482493428164e-08,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.340200146952032e+157,
        "filterflow_gradient_max_abs": 1697.7646785016034,
        "gradient_delta": [
          7.340200146952032e+157,
          -7.12086023218631e+157
        ],
        "gradient_explosion_ratio": 4.323449674680636e+154,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.340200146952032e+157,
        "relative_gradient_delta": 4.323449674680636e+154,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8990448324984754e-08,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.708093899794626e+160,
        "filterflow_gradient_max_abs": 947.0739014815089,
        "gradient_delta": [
          -5.708093899794626e+160,
          5.537524595907783e+160
        ],
        "gradient_explosion_ratio": 6.0270839380807e+157,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.708093899794626e+160,
        "relative_gradient_delta": 6.0270839380807e+157,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1565390423129429e-08,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3061395776958432e+162,
        "filterflow_gradient_max_abs": 249.89093531615012,
        "gradient_delta": [
          -1.3061395776958432e+162,
          1.2671095052307346e+162
        ],
        "gradient_explosion_ratio": 5.226838564765775e+159,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3061395776958432e+162,
        "relative_gradient_delta": 5.226838564765775e+159,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.132605782724568e-09,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6454561300862978e+166,
        "filterflow_gradient_max_abs": 974.2890696675929,
        "gradient_delta": [
          -1.6454561300862978e+166,
          1.5962865979075698e+166
        ],
        "gradient_explosion_ratio": 1.6888787745999172e+163,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6454561300862978e+166,
        "relative_gradient_delta": 1.6888787745999172e+163,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.223679515140248e-09,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.654349548936637e+169,
        "filterflow_gradient_max_abs": 1029.3299119039873,
        "gradient_delta": [
          1.654349548936637e+169,
          -1.6049142635504283e+169
        ],
        "gradient_explosion_ratio": 1.6072102149217925e+166,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.654349548936637e+169,
        "relative_gradient_delta": 1.6072102149217925e+166,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.178016403486254e-09,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.8189331110193667e+172,
        "filterflow_gradient_max_abs": 1426.254117759735,
        "gradient_delta": [
          -2.8189331110193667e+172,
          2.7346977310674993e+172
        ],
        "gradient_explosion_ratio": 1.976459226948392e+169,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.8189331110193667e+172,
        "relative_gradient_delta": 1.976459226948392e+169,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.153612730486202e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.525090658981865e+175,
        "filterflow_gradient_max_abs": 1942.7454564725651,
        "gradient_delta": [
          4.525090658981865e+175,
          -4.3898718666359394e+175
        ],
        "gradient_explosion_ratio": 2.3292246773275453e+172,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.525090658981865e+175,
        "relative_gradient_delta": 2.3292246773275453e+172,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.01524527357833e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.824022007575553e+177,
        "filterflow_gradient_max_abs": 169.06130724664092,
        "gradient_delta": [
          7.824022007575553e+177,
          -7.590224524413001e+177
        ],
        "gradient_explosion_ratio": 4.627919974711428e+175,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.824022007575553e+177,
        "relative_gradient_delta": 4.627919974711428e+175,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.081496278260602e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.9923776239698067e+181,
        "filterflow_gradient_max_abs": 1963.5208371745916,
        "gradient_delta": [
          -1.9923776239698067e+181,
          1.9328413811598398e+181
        ],
        "gradient_explosion_ratio": 1.0146964505030355e+178,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.9923776239698067e+181,
        "relative_gradient_delta": 1.0146964505030355e+178,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.653859933678177e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4157814618321113e+183,
        "filterflow_gradient_max_abs": 1119.9768301540837,
        "gradient_delta": [
          2.4157814618321113e+183,
          -2.343593062425741e+183
        ],
        "gradient_explosion_ratio": 2.1569923562612933e+180,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4157814618321113e+183,
        "relative_gradient_delta": 2.1569923562612933e+180,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.3080741458397824e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1731154902322756e+186,
        "filterflow_gradient_max_abs": 979.6868013870265,
        "gradient_delta": [
          -2.1731154902322756e+186,
          2.1081784371736398e+186
        ],
        "gradient_explosion_ratio": 2.2181736930165944e+183,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1731154902322756e+186,
        "relative_gradient_delta": 2.2181736930165944e+183,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.394845624730806e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6761149304177094e+190,
        "filterflow_gradient_max_abs": 2882.4178802677957,
        "gradient_delta": [
          1.6761149304177094e+190,
          -1.6260292517420346e+190
        ],
        "gradient_explosion_ratio": 5.814961605296409e+186,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6761149304177094e+190,
        "relative_gradient_delta": 5.814961605296409e+186,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.620751946684322e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0271409982093253e+192,
        "filterflow_gradient_max_abs": 858.8073873147812,
        "gradient_delta": [
          -1.0271409982093253e+192,
          9.964479633479839e+191
        ],
        "gradient_explosion_ratio": 1.1960085734950067e+189,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0271409982093253e+192,
        "relative_gradient_delta": 1.1960085734950067e+189,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.615852837261627e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0729091980457425e+194,
        "filterflow_gradient_max_abs": 442.0116504772855,
        "gradient_delta": [
          -2.0729091980457425e+194,
          2.010966510147067e+194
        ],
        "gradient_explosion_ratio": 4.6897162004834236e+191,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0729091980457425e+194,
        "relative_gradient_delta": 4.6897162004834236e+191,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.274422841874184e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.644368446723236e+198,
        "filterflow_gradient_max_abs": 3282.5855155180925,
        "gradient_delta": [
          -8.644368446723236e+198,
          8.386057365233841e+198
        ],
        "gradient_explosion_ratio": 2.6334023609919234e+195,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.644368446723236e+198,
        "relative_gradient_delta": 2.6334023609919234e+195,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0136062655874412e-08,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.8417747875879254e+201,
        "filterflow_gradient_max_abs": 1855.9144036285215,
        "gradient_delta": [
          3.8417747875879254e+201,
          -3.726974845135599e+201
        ],
        "gradient_explosion_ratio": 2.0700172271290225e+198,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.8417747875879254e+201,
        "relative_gradient_delta": 2.0700172271290225e+198,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.873637741795392e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3949646722137566e+204,
        "filterflow_gradient_max_abs": 1310.8611477302254,
        "gradient_delta": [
          -2.3949646722137566e+204,
          2.3233983202678314e+204
        ],
        "gradient_explosion_ratio": 1.8270162910546794e+201,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3949646722137566e+204,
        "relative_gradient_delta": 1.8270162910546794e+201,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.93335175330867e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5994870587725104e+207,
        "filterflow_gradient_max_abs": 914.416967723082,
        "gradient_delta": [
          1.5994870587725104e+207,
          -1.5516911747208033e+207
        ],
        "gradient_explosion_ratio": 1.7491878598395517e+204,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5994870587725104e+207,
        "relative_gradient_delta": 1.7491878598395517e+204,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.058265166255296e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4375375315533913e+211,
        "filterflow_gradient_max_abs": 3551.3298618369327,
        "gradient_delta": [
          -1.4375375315533913e+211,
          1.3945810244649048e+211
        ],
        "gradient_explosion_ratio": 4.047885123264281e+207,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4375375315533913e+211,
        "relative_gradient_delta": 4.047885123264281e+207,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.786315675024525e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.7803830441161616e+214,
        "filterflow_gradient_max_abs": 3023.0985131010166,
        "gradient_delta": [
          2.7803830441161616e+214,
          -2.6972996175469633e+214
        ],
        "gradient_explosion_ratio": 9.197130136735493e+210,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.7803830441161616e+214,
        "relative_gradient_delta": 9.197130136735493e+210,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.745331570025883e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.266690752479937e+217,
        "filterflow_gradient_max_abs": 2001.070628323309,
        "gradient_delta": [
          -2.266690752479937e+217,
          2.198957482746732e+217
        ],
        "gradient_explosion_ratio": 1.1327390050091287e+214,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.266690752479937e+217,
        "relative_gradient_delta": 1.1327390050091287e+214,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.205052720062668e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.0722146841410616e+220,
        "filterflow_gradient_max_abs": 2346.9001573329506,
        "gradient_delta": [
          4.0722146841410616e+220,
          -3.9505287350054483e+220
        ],
        "gradient_explosion_ratio": 1.7351461123803333e+217,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.0722146841410616e+220,
        "relative_gradient_delta": 1.7351461123803333e+217,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.456598728414974e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5022880033041414e+224,
        "filterflow_gradient_max_abs": 4046.6212127655212,
        "gradient_delta": [
          -1.5022880033041414e+224,
          1.457396622142671e+224
        ],
        "gradient_explosion_ratio": 3.7124502747255044e+220,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5022880033041414e+224,
        "relative_gradient_delta": 3.7124502747255044e+220,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.6329352092725458e-08,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5603365296363644e+227,
        "filterflow_gradient_max_abs": 2730.4139020142047,
        "gradient_delta": [
          1.5603365296363644e+227,
          -1.5137105419841878e+227
        ],
        "gradient_explosion_ratio": 5.714652011130314e+223,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5603365296363644e+227,
        "relative_gradient_delta": 5.714652011130314e+223,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.300094916397939e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_raw_transport_gradient"
      }
    ]
  }
]
```

## FilterFlow Reference Rows

```json
{
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "first_rows": [
    {
      "cumulative_mean_log_likelihood": -2.004278145529374,
      "ess_before_resampling": [
        49.99999999999999
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        0.008913771203554867,
        5.766308833278761e-19
      ],
      "gradient_matrix": [
        [
          0.008913771203554867,
          0.00016384347951870905
        ],
        [
          -1.4528816526185797e-19,
          5.766308833278761e-19
        ]
      ],
      "resampling_flag": [
        false
      ],
      "time_index": 0
    },
    {
      "cumulative_mean_log_likelihood": -17.01411740171092,
      "ess_before_resampling": [
        49.93816336447469
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        -8.800019462744133,
        3.8431585919786795e-17
      ],
      "gradient_matrix": [
        [
          -8.800019462744133,
          -8.631155697800054
        ],
        [
          -6.554192008470387e-17,
          3.8431585919786795e-17
        ]
      ],
      "resampling_flag": [
        true
      ],
      "time_index": 1
    },
    {
      "cumulative_mean_log_likelihood": -17.92954145935854,
      "ess_before_resampling": [
        6.000674141689701
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        1.4485716238559057,
        1.708329023140942e-16
      ],
      "gradient_matrix": [
        [
          1.4485716238559057,
          4.795485883862204
        ],
        [
          2.0733006354101827e-17,
          1.708329023140942e-16
        ]
      ],
      "resampling_flag": [
        true
      ],
      "time_index": 2
    },
    {
      "cumulative_mean_log_likelihood": -21.22138045289012,
      "ess_before_resampling": [
        43.95083606901166
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        16.840076774872443,
        4.913985439913856e-16
      ],
      "gradient_matrix": [
        [
          16.840076774872443,
          15.001128133938149
        ],
        [
          1.3279867624785524e-16,
          4.913985439913856e-16
        ]
      ],
      "resampling_flag": [
        true
      ],
      "time_index": 3
    },
    {
      "cumulative_mean_log_likelihood": -22.038839202252312,
      "ess_before_resampling": [
        17.14318279111833
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        -11.278780998887767,
        -3.4186398625251673e-16
      ],
      "gradient_matrix": [
        [
          -11.278780998887767,
          -6.777684256257009
        ],
        [
          -1.710562468875603e-15,
          -3.4186398625251673e-16
        ]
      ],
      "resampling_flag": [
        true
      ],
      "time_index": 4
    }
  ],
  "full_routine": {
    "final_ess": [
      27.982214166117192
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      18935.6850725171,
      2073.5151524806142
    ],
    "gradient_matrix": [
      [
        18935.6850725171,
        1678.5016416026954
      ],
      [
        31902.57896987284,
        2073.5151524806142
      ]
    ],
    "mean_log_likelihood": -258.58524847172157
  },
  "initial_particles_checksum": -0.13359209100740663,
  "last_row": {
    "cumulative_mean_log_likelihood": -258.5852484717215,
    "ess_before_resampling": [
      7.667894761101062
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      2730.4139020142047,
      -1.5583115936387357e-15
    ],
    "gradient_matrix": [
      [
        2730.4139020142047,
        195.5288347815283
      ],
      [
        -7.106556086362378e-14,
        -1.5583115936387357e-15
      ]
    ],
    "resampling_flag": [
      true
    ],
    "time_index": 99
  },
  "localization_contract": "first_failing_smoothness_row_per_time_cumulative_gradient",
  "observation_checksum": 24302.800267778097,
  "package_versions": {
    "numpy": "1.26.4",
    "python": "3.11.14",
    "tensorflow": "2.19.1"
  },
  "settings": {
    "T": 100,
    "batch_size": 1,
    "convergence_threshold": 1e-06,
    "data_seed": 123,
    "dtype": "float64",
    "epsilon": 0.25,
    "filter_seed": 1234,
    "max_iter": 500,
    "n_particles": 50,
    "optimal_proposal": true,
    "resampling_correction": false,
    "resampling_neff": 0.9999,
    "scaling": 0.85,
    "theta": [
      0.95,
      0.95
    ]
  },
  "source_gradient_note": "FilterFlow RegularisedTransform transport uses @tf.custom_gradient and clips upstream d_transport to [-1, 1].",
  "status": "executed",
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-03 05:07:30.043889: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780434450.055579     119 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780434450.059557     119 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780434450.069240     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780434450.069276     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780434450.069281     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780434450.069283     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-03 05:07:30.072239: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-03 05:07:32.365961: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n"
}
```

## BayesFilter Mode Finals

```json
{
  "backend": "tensorflow_tensorflow_probability",
  "cpu_only_manifest": {
    "cuda_visible_devices": "-1",
    "gpu_devices_visible": [],
    "pre_import_cuda_visible_devices": "-1"
  },
  "finite_values": true,
  "localization_contract": "same fixed data/seeds with gradient-path ablations",
  "mode_final_summaries": [
    {
      "final_gradient_diag": [
        3.711418912951682e+232,
        -3.0135023214837034e+232
      ],
      "final_gradient_max_abs": 3.711418912951682e+232,
      "final_mean_log_likelihood": -258.5852484624214,
      "finite_values": true,
      "mode": "raw"
    },
    {
      "final_gradient_diag": [
        18935.685049166474,
        2073.5151589713964
      ],
      "final_gradient_max_abs": 18935.685049166474,
      "final_mean_log_likelihood": -258.5852484624214,
      "finite_values": true,
      "mode": "transport_upstream_clip"
    },
    {
      "final_gradient_diag": [
        2877.6722404002735,
        2764.9054584793257
      ],
      "final_gradient_max_abs": 2877.6722404002735,
      "final_mean_log_likelihood": -258.5852484624214,
      "finite_values": true,
      "mode": "transport_matrix_stop_gradient"
    },
    {
      "final_gradient_diag": [
        60605.43234825605,
        8.881784197001252e-16
      ],
      "final_gradient_max_abs": 60605.43234825605,
      "final_mean_log_likelihood": -258.5852484624214,
      "finite_values": true,
      "mode": "post_resample_state_stop_gradient"
    },
    {
      "final_gradient_diag": [
        -4.6565250369319974e+210,
        1.149344864086458e+211
      ],
      "final_gradient_max_abs": 1.149344864086458e+211,
      "final_mean_log_likelihood": -258.5852484624214,
      "finite_values": true,
      "mode": "proposal_mean_stop_gradient"
    },
    {
      "final_gradient_diag": [
        3.711418912951682e+232,
        -3.0135023214837034e+232
      ],
      "final_gradient_max_abs": 3.711418912951682e+232,
      "final_mean_log_likelihood": -258.5852484624214,
      "finite_values": true,
      "mode": "proposal_log_prob_stop_gradient"
    },
    {
      "final_gradient_diag": [
        -1.3832594583394986e+228,
        1.2680960330198352e+228
      ],
      "final_gradient_max_abs": 1.3832594583394986e+228,
      "final_mean_log_likelihood": -258.5852484624214,
      "finite_values": true,
      "mode": "transition_log_prob_stop_gradient"
    },
    {
      "final_gradient_diag": [
        1.5603365296363644e+227,
        -1.5137105419841878e+227
      ],
      "final_gradient_max_abs": 1.5603365296363644e+227,
      "final_mean_log_likelihood": -258.5852484624214,
      "finite_values": true,
      "mode": "normalized_weights_stop_gradient"
    }
  ],
  "status": "executed"
}
```

## Interpretation

The scalar path stays aligned on the first failing smoothness row, but the raw BayesFilter gradient diverges. The strongest diagnostic hint is `transport_custom_gradient_clipping_is_primary_suspect`.

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No DSGE/NAWM validation is concluded.
- No banking/model-risk claim is concluded.
- No monograph claim is concluded.
- No gradient correctness beyond this fixed 1D scalar fixture is concluded.
- No correctness claim is made for either implementation.
- No analytic smoothness-gradient correctness is concluded.
- No full mesh_size=20 surface agreement is concluded.
- No production dtype default is concluded.
- Finite gradients alone are smoke evidence only.
