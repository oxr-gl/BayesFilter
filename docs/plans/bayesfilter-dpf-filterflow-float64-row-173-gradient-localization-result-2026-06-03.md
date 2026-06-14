# FilterFlow Float64 Smoothness Gradient Localization

## Decision

`filterflow_float64_smoothness_gradient_localized`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_localized | localized raw failure: {'status': 'failure', 'time_index': 1, 'scalar_delta': 1.8406609569865395e-11, 'max_abs_gradient_delta': 0.05475160151717162, 'relative_gradient_delta': 0.006179306839748326, 'gradient_explosion_ratio': 1.0061793068397484, 'resampling_flag': [True], 'transport_status': 'computed_raw_transport_gradient'} | scalar path remained aligned before gradient mismatch | single theta row only; no analytic-gradient correctness is concluded | patch BayesFilter annealed transport backward semantics to mirror FilterFlow custom gradient | correctness of either implementation, analytic gradient correctness, production readiness |

## Model Contract

| Key | Value |
| --- | --- |
| `model` | `filterflow_simple_linear_smoothness_constant_velocity_lgssm` |
| `theta` | `[0.9710526315789474, 0.9842105263157894]` |
| `mesh_index` | `173` |
| `artifact_tag` | `row-173` |
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
    "final_relative_gradient_delta": 0.000755387810421488,
    "mode": "transport_upstream_clip"
  },
  "first_raw_gradient_failure": {
    "gradient_explosion_ratio": 1.0061793068397484,
    "max_abs_gradient_delta": 0.05475160151717162,
    "relative_gradient_delta": 0.006179306839748326,
    "resampling_flag": [
      true
    ],
    "scalar_delta": 1.8406609569865395e-11,
    "status": "failure",
    "time_index": 1,
    "transport_status": "computed_raw_transport_gradient"
  },
  "first_raw_scalar_failure": {
    "status": "no_failure"
  },
  "interpretive_hint": {
    "best_ablation_final_relative_gradient_delta": 0.000755387810421488,
    "best_ablation_mode": "transport_upstream_clip",
    "raw_final_relative_gradient_delta": 1.925265112611007e+214,
    "status": "transport_custom_gradient_clipping_is_primary_suspect",
    "transport_clip_final_relative_gradient_delta": 0.000755387810421488
  }
}
```

## Mode Summaries

```json
[
  {
    "final_bayesfilter_gradient_diag": [
      1.3515114431922745e+218,
      -1.1290717972775883e+218
    ],
    "final_bayesfilter_gradient_max_abs": 1.3515114431922745e+218,
    "final_filterflow_gradient_diag": [
      7019.871883303286,
      713.5990730344417
    ],
    "final_filterflow_gradient_max_abs": 7019.871883303286,
    "final_gradient_delta": [
      1.3515114431922745e+218,
      -1.1290717972775883e+218
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 1.3515114431922745e+218,
    "final_relative_gradient_delta": 1.925265112611007e+214,
    "final_scalar_delta": 7.407919611068792e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "bayesfilter_gradient_max_abs": 9195505.610780967,
      "filterflow_gradient_max_abs": 0.7972582915878877,
      "gradient_explosion_ratio": 9195505.610780967,
      "resampling_flag": [
        true
      ],
      "status": "explosion",
      "time_index": 8,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 1.0061793068397484,
      "max_abs_gradient_delta": 0.05475160151717162,
      "relative_gradient_delta": 0.006179306839748326,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.8406609569865395e-11,
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
        "bayesfilter_gradient_max_abs": 0.008924445612040184,
        "filterflow_gradient_max_abs": 0.008924445612040184,
        "gradient_delta": [
          0.0,
          -5.795395272864551e-20
        ],
        "gradient_explosion_ratio": 0.008924445612040184,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 5.795395272864551e-20,
        "relative_gradient_delta": 5.795395272864551e-20,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.915227855096703,
        "filterflow_gradient_max_abs": 8.860476253579531,
        "gradient_delta": [
          -0.05475160151717162,
          0.03707418793594731
        ],
        "gradient_explosion_ratio": 1.0061793068397484,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.05475160151717162,
        "relative_gradient_delta": 0.006179306839748326,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8406609569865395e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.41460040326663,
        "filterflow_gradient_max_abs": 1.4056099396090884,
        "gradient_delta": [
          -7.820210342875718,
          -0.8607962633986631
        ],
        "gradient_explosion_ratio": 4.563570747835336,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.820210342875718,
        "relative_gradient_delta": 5.563570747835336,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.5511147921642987e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 84.91559161373418,
        "filterflow_gradient_max_abs": 14.864972477668916,
        "gradient_delta": [
          -99.7805640914031,
          73.5703394417855
        ],
        "gradient_explosion_ratio": 5.71246208099609,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 99.7805640914031,
        "relative_gradient_delta": 6.71246208099609,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.2442492308982764e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 18.44534233601806,
        "filterflow_gradient_max_abs": 15.00462728219541,
        "gradient_delta": [
          7.886961778604195,
          18.44534233601806
        ],
        "gradient_explosion_ratio": 1.2293102647011718,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 18.44534233601806,
        "relative_gradient_delta": 1.2293102647011718,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.779998453661392e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9743.94004421566,
        "filterflow_gradient_max_abs": 6.525931066391355,
        "gradient_delta": [
          -9737.414113149269,
          7903.79187901978
        ],
        "gradient_explosion_ratio": 1493.1110894500712,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9737.414113149269,
        "relative_gradient_delta": 1492.1110894500712,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.1093350116861984e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 258298.98288897768,
        "filterflow_gradient_max_abs": 2.686919378388484,
        "gradient_delta": [
          -258301.66980835606,
          214891.3498982717
        ],
        "gradient_explosion_ratio": 96132.0183130675,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 258301.66980835606,
        "relative_gradient_delta": 96133.01831306748,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4224179873708636e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 324900.69275483215,
        "filterflow_gradient_max_abs": 24.973165642495765,
        "gradient_delta": [
          -324875.7195891897,
          282705.93505387544
        ],
        "gradient_explosion_ratio": 13009.9923015752,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 324875.7195891897,
        "relative_gradient_delta": 13008.9923015752,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.5496940376542625e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9195505.610780967,
        "filterflow_gradient_max_abs": 0.7972582915878877,
        "gradient_delta": [
          9195506.408039259,
          -8036478.510680706
        ],
        "gradient_explosion_ratio": 9195505.610780967,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9195506.408039259,
        "relative_gradient_delta": 9195506.408039259,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.66524613279762e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 382875866.76590914,
        "filterflow_gradient_max_abs": 49.77299487676166,
        "gradient_delta": [
          -382875916.538904,
          319724090.65727
        ],
        "gradient_explosion_ratio": 7692441.809336828,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 382875916.538904,
        "relative_gradient_delta": 7692442.809336828,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.581402089977928e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 65321312046.92027,
        "filterflow_gradient_max_abs": 91.01474473671405,
        "gradient_delta": [
          65321311955.905525,
          -54459712435.14222
        ],
        "gradient_explosion_ratio": 717700326.8633087,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 65321311955.905525,
        "relative_gradient_delta": 717700325.8633085,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.424994118489849e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2257902832598.7676,
        "filterflow_gradient_max_abs": 28.00263902728941,
        "gradient_delta": [
          2257902832626.77,
          -1890282276023.0234
        ],
        "gradient_explosion_ratio": 80631787253.99324,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2257902832626.77,
        "relative_gradient_delta": 80631787254.99323,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.85451720225683e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 50905494744162.92,
        "filterflow_gradient_max_abs": 40.13671871067378,
        "gradient_delta": [
          50905494744122.79,
          -42548666239420.91
        ],
        "gradient_explosion_ratio": 1268302352046.166,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 50905494744122.79,
        "relative_gradient_delta": 1268302352045.1663,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3077183780296764e-10,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2550359035201362.5,
        "filterflow_gradient_max_abs": 49.010874255508995,
        "gradient_delta": [
          -2550359035201411.5,
          2126258070040169.0
        ],
        "gradient_explosion_ratio": 52036595427895.13,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2550359035201411.5,
        "relative_gradient_delta": 52036595427896.13,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4137313542050833e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.22009120619641e+17,
        "filterflow_gradient_max_abs": 21.29035436921441,
        "gradient_delta": [
          2.2200912061964096e+17,
          -1.854041819684387e+17
        ],
        "gradient_explosion_ratio": 1.0427685550441728e+16,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2200912061964096e+17,
        "relative_gradient_delta": 1.0427685550441726e+16,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3353940175875323e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.706375256531782e+17,
        "filterflow_gradient_max_abs": 27.042811971633515,
        "gradient_delta": [
          -8.706375256531782e+17,
          7.243383565198019e+17
        ],
        "gradient_explosion_ratio": 3.219478531176533e+16,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.706375256531782e+17,
        "relative_gradient_delta": 3.219478531176533e+16,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.525606307950511e-10,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.370660598464977e+19,
        "filterflow_gradient_max_abs": 18.468136147749064,
        "gradient_delta": [
          -6.370660598464977e+19,
          5.315640861968841e+19
        ],
        "gradient_explosion_ratio": 3.449541712005111e+18,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.370660598464977e+19,
        "relative_gradient_delta": 3.449541712005111e+18,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7488588355263346e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.011912285155395e+21,
        "filterflow_gradient_max_abs": 102.94637935328883,
        "gradient_delta": [
          3.011912285155395e+21,
          -2.516770194780696e+21
        ],
        "gradient_explosion_ratio": 2.9257097763673543e+19,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.011912285155395e+21,
        "relative_gradient_delta": 2.9257097763673543e+19,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3816503496855148e-10,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.31482827076068e+23,
        "filterflow_gradient_max_abs": 113.77902775418237,
        "gradient_delta": [
          -6.31482827076068e+23,
          5.275275400724121e+23
        ],
        "gradient_explosion_ratio": 5.550081060987582e+21,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.31482827076068e+23,
        "relative_gradient_delta": 5.550081060987582e+21,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.3455015707440907e-10,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0155851142378778e+26,
        "filterflow_gradient_max_abs": 165.42250820864194,
        "gradient_delta": [
          1.0155851142378778e+26,
          -8.484299961470961e+25
        ],
        "gradient_explosion_ratio": 6.139340560336287e+23,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0155851142378778e+26,
        "relative_gradient_delta": 6.139340560336287e+23,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.92866184029117e-10,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0562297990305144e+28,
        "filterflow_gradient_max_abs": 73.77440324184383,
        "gradient_delta": [
          -1.0562297990305144e+28,
          8.824128395905481e+27
        ],
        "gradient_explosion_ratio": 1.431702260698783e+26,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0562297990305144e+28,
        "relative_gradient_delta": 1.431702260698783e+26,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4417447497835383e-10,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4578552520243467e+30,
        "filterflow_gradient_max_abs": 217.86217342911775,
        "gradient_delta": [
          -2.4578552520243467e+30,
          2.0533233616255708e+30
        ],
        "gradient_explosion_ratio": 1.1281698026500314e+28,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4578552520243467e+30,
        "relative_gradient_delta": 1.1281698026500314e+28,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.974509693056461e-10,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.9335133257350875e+32,
        "filterflow_gradient_max_abs": 165.63087578642663,
        "gradient_delta": [
          1.9335133257350875e+32,
          -1.6152607457863307e+32
        ],
        "gradient_explosion_ratio": 1.1673628582561284e+30,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.9335133257350875e+32,
        "relative_gradient_delta": 1.1673628582561284e+30,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.2155079427175224e-10,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3310273104099154e+34,
        "filterflow_gradient_max_abs": 20.952482372929534,
        "gradient_delta": [
          3.3310273104099154e+34,
          -2.782766763308961e+34
        ],
        "gradient_explosion_ratio": 1.5898007935869118e+33,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3310273104099154e+34,
        "relative_gradient_delta": 1.5898007935869118e+33,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.807603204426414e-10,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.258944781661576e+36,
        "filterflow_gradient_max_abs": 45.60764934214221,
        "gradient_delta": [
          1.258944781661576e+36,
          -1.0517159399915034e+36
        ],
        "gradient_explosion_ratio": 2.7603807690616727e+34,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.258944781661576e+36,
        "relative_gradient_delta": 2.7603807690616727e+34,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.035900585426134e-10,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.642422919625248e+36,
        "filterflow_gradient_max_abs": 95.80515251122853,
        "gradient_delta": [
          -7.642422919625248e+36,
          6.384289096445762e+36
        ],
        "gradient_explosion_ratio": 7.97704791371168e+34,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.642422919625248e+36,
        "relative_gradient_delta": 7.97704791371168e+34,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.194777941142092e-10,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2397859825626116e+39,
        "filterflow_gradient_max_abs": 162.31717661541148,
        "gradient_delta": [
          -1.2397859825626116e+39,
          1.0357044710462055e+39
        ],
        "gradient_explosion_ratio": 7.638045513199852e+36,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2397859825626116e+39,
        "relative_gradient_delta": 7.638045513199852e+36,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.324789415477426e-10,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0970839154365316e+42,
        "filterflow_gradient_max_abs": 65.61469672303252,
        "gradient_delta": [
          1.0970839154365316e+42,
          -9.165201620151445e+41
        ],
        "gradient_explosion_ratio": 1.6720094281125065e+40,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0970839154365316e+42,
        "relative_gradient_delta": 1.6720094281125065e+40,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.852775876111991e-10,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.1770033331277535e+44,
        "filterflow_gradient_max_abs": 353.91086072731014,
        "gradient_delta": [
          -4.1770033331277535e+44,
          3.489526129093571e+44
        ],
        "gradient_explosion_ratio": 1.1802416361407323e+42,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.1770033331277535e+44,
        "relative_gradient_delta": 1.1802416361407323e+42,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.191615860487218e-10,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.940681213904315e+46,
        "filterflow_gradient_max_abs": 106.57513689011893,
        "gradient_delta": [
          -4.940681213904315e+46,
          4.127513820512493e+46
        ],
        "gradient_explosion_ratio": 4.6358666365104045e+44,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.940681213904315e+46,
        "relative_gradient_delta": 4.6358666365104045e+44,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.87274212698685e-10,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0781517771816635e+49,
        "filterflow_gradient_max_abs": 301.25080522517993,
        "gradient_delta": [
          -1.0781517771816635e+49,
          9.007032464050631e+48
        ],
        "gradient_explosion_ratio": 3.5789174949283975e+46,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0781517771816635e+49,
        "relative_gradient_delta": 3.5789174949283975e+46,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.1155345797960763e-10,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.963295192829389e+51,
        "filterflow_gradient_max_abs": 406.1376803574301,
        "gradient_delta": [
          3.963295192829389e+51,
          -3.310992916015757e+51
        ],
        "gradient_explosion_ratio": 9.758501573509277e+48,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.963295192829389e+51,
        "relative_gradient_delta": 9.758501573509277e+48,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.641514005423232e-10,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.053266233509728e+52,
        "filterflow_gradient_max_abs": 226.31263344208014,
        "gradient_delta": [
          9.053266233509728e+52,
          -7.563226732060607e+52
        ],
        "gradient_explosion_ratio": 4.000336214472409e+50,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.053266233509728e+52,
        "relative_gradient_delta": 4.000336214472409e+50,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.090381697911653e-10,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1522600742980565e+56,
        "filterflow_gradient_max_abs": 6.85443174851973,
        "gradient_delta": [
          1.1522600742980565e+56,
          -9.626143827227235e+55
        ],
        "gradient_explosion_ratio": 1.6810439093611174e+55,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1522600742980565e+56,
        "relative_gradient_delta": 1.6810439093611174e+55,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.083187369971711e-10,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1850256639856927e+58,
        "filterflow_gradient_max_abs": 80.80287856491722,
        "gradient_delta": [
          -1.1850256639856927e+58,
          9.899872210950648e+57
        ],
        "gradient_explosion_ratio": 1.4665636732652295e+56,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1850256639856927e+58,
        "relative_gradient_delta": 1.4665636732652295e+56,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.413411940935475e-10,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.245354262372143e+59,
        "filterflow_gradient_max_abs": 195.04750763879625,
        "gradient_delta": [
          4.245354262372143e+59,
          -3.5466290641739363e+59
        ],
        "gradient_explosion_ratio": 2.176574473452904e+57,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.245354262372143e+59,
        "relative_gradient_delta": 2.176574473452904e+57,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.915747808809101e-10,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.017030740742271e+60,
        "filterflow_gradient_max_abs": 227.99933783381496,
        "gradient_delta": [
          9.017030740742271e+60,
          -7.532955146784457e+60
        ],
        "gradient_explosion_ratio": 3.954849530008126e+58,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.017030740742271e+60,
        "relative_gradient_delta": 3.954849530008126e+58,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4428105638871784e-10,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.193090202333769e+64,
        "filterflow_gradient_max_abs": 498.30983956509795,
        "gradient_delta": [
          -7.193090202333769e+64,
          6.009209410434649e+64
        ],
        "gradient_explosion_ratio": 1.443497525276958e+62,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.193090202333769e+64,
        "relative_gradient_delta": 1.443497525276958e+62,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.725002776875044e-10,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0808088184907515e+67,
        "filterflow_gradient_max_abs": 348.59095258355785,
        "gradient_delta": [
          -1.0808088184907515e+67,
          9.029229913931143e+66
        ],
        "gradient_explosion_ratio": 3.100507372553451e+64,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0808088184907515e+67,
        "relative_gradient_delta": 3.100507372553451e+64,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.749836080009118e-10,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.6805934796623426e+69,
        "filterflow_gradient_max_abs": 24.53415070247347,
        "gradient_delta": [
          4.6805934796623426e+69,
          -3.91023407092197e+69
        ],
        "gradient_explosion_ratio": 1.9077870419987503e+68,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.6805934796623426e+69,
        "relative_gradient_delta": 1.9077870419987503e+68,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9053560385582387e-10,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.047728750233288e+70,
        "filterflow_gradient_max_abs": 743.4955982984612,
        "gradient_delta": [
          -3.047728750233288e+70,
          2.54611575432522e+70
        ],
        "gradient_explosion_ratio": 4.0991886935285376e+67,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.047728750233288e+70,
        "relative_gradient_delta": 4.0991886935285376e+67,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3861267689208034e-10,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.171811284141271e+73,
        "filterflow_gradient_max_abs": 660.4154280128698,
        "gradient_delta": [
          8.171811284141271e+73,
          -6.826846861023913e+73
        ],
        "gradient_explosion_ratio": 1.2373743764178118e+71,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.171811284141271e+73,
        "relative_gradient_delta": 1.2373743764178118e+71,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2236966995260445e-10,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.685283526648857e+75,
        "filterflow_gradient_max_abs": 151.38043625809377,
        "gradient_delta": [
          -7.685283526648857e+75,
          6.4203946831013196e+75
        ],
        "gradient_explosion_ratio": 5.07680101644439e+73,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.685283526648857e+75,
        "relative_gradient_delta": 5.07680101644439e+73,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.503508428868372e-10,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.327945692814475e+78,
        "filterflow_gradient_max_abs": 78.34314644911912,
        "gradient_delta": [
          2.327945692814475e+78,
          -1.944798795888549e+78
        ],
        "gradient_explosion_ratio": 2.9714733174858977e+76,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.327945692814475e+78,
        "relative_gradient_delta": 2.9714733174858977e+76,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4379963886312908e-10,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.268714929943253e+79,
        "filterflow_gradient_max_abs": 375.1405380302191,
        "gradient_delta": [
          5.268714929943253e+79,
          -4.401559058387549e+79
        ],
        "gradient_explosion_ratio": 1.404464299595059e+77,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.268714929943253e+79,
        "relative_gradient_delta": 1.404464299595059e+77,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.290931888637715e-10,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.907981783086711e+82,
        "filterflow_gradient_max_abs": 190.9613749711765,
        "gradient_delta": [
          2.907981783086711e+82,
          -2.4293691591139295e+82
        ],
        "gradient_explosion_ratio": 1.5228115023394854e+80,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.907981783086711e+82,
        "relative_gradient_delta": 1.5228115023394854e+80,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.651177055668086e-10,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.5909447060530045e+85,
        "filterflow_gradient_max_abs": 677.2028181986615,
        "gradient_delta": [
          2.5909447060530045e+85,
          -2.164511895660028e+85
        ],
        "gradient_explosion_ratio": 3.825950862025113e+82,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.5909447060530045e+85,
        "relative_gradient_delta": 3.825950862025113e+82,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.92969196177728e-10,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.589410897629186e+87,
        "filterflow_gradient_max_abs": 152.6174741556563,
        "gradient_delta": [
          -2.589410897629186e+87,
          2.1632305303837516e+87
        ],
        "gradient_explosion_ratio": 1.6966673783293098e+85,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.589410897629186e+87,
        "relative_gradient_delta": 1.6966673783293098e+85,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.625100468227174e-11,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.270190291123869e+88,
        "filterflow_gradient_max_abs": 207.0601214499801,
        "gradient_delta": [
          -8.270190291123869e+88,
          6.909034076522848e+88
        ],
        "gradient_explosion_ratio": 3.9941009563841654e+86,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.270190291123869e+88,
        "relative_gradient_delta": 3.9941009563841654e+86,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.438458406890277e-10,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1255836450916413e+92,
        "filterflow_gradient_max_abs": 546.4746634801378,
        "gradient_delta": [
          -2.1255836450916413e+92,
          1.775742675739998e+92
        ],
        "gradient_explosion_ratio": 3.889628901649706e+89,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1255836450916413e+92,
        "relative_gradient_delta": 3.889628901649706e+89,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.842170943040401e-14,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.338216768127066e+93,
        "filterflow_gradient_max_abs": 272.67443106070385,
        "gradient_delta": [
          4.338216768127066e+93,
          -3.624207717989915e+93
        ],
        "gradient_explosion_ratio": 1.5909877399400442e+91,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.338216768127066e+93,
        "relative_gradient_delta": 1.5909877399400442e+91,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.5509905299259117e-10,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.078540190736647e+97,
        "filterflow_gradient_max_abs": 949.676068984666,
        "gradient_delta": [
          -9.078540190736647e+97,
          7.584341029033797e+97
        ],
        "gradient_explosion_ratio": 9.559617734121542e+94,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.078540190736647e+97,
        "relative_gradient_delta": 9.559617734121542e+94,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.264737647943548e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.936627081914298e+99,
        "filterflow_gradient_max_abs": 101.55125271438094,
        "gradient_delta": [
          -9.936627081914298e+99,
          8.301198968581746e+99
        ],
        "gradient_explosion_ratio": 9.784839493670911e+97,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.936627081914298e+99,
        "relative_gradient_delta": 9.784839493670911e+97,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.427679308108054e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.095141432173635e+101,
        "filterflow_gradient_max_abs": 177.86655077673558,
        "gradient_delta": [
          -1.095141432173635e+101,
          9.14896659829114e+100
        ],
        "gradient_explosion_ratio": 6.157096021658932e+98,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.095141432173635e+101,
        "relative_gradient_delta": 6.157096021658932e+98,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3662173614648054e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.358543390700818e+103,
        "filterflow_gradient_max_abs": 135.59093315487942,
        "gradient_delta": [
          -5.358543390700818e+103,
          4.4766030264886e+103
        ],
        "gradient_explosion_ratio": 3.951992412781756e+101,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.358543390700818e+103,
        "relative_gradient_delta": 3.951992412781756e+101,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.345853206657921e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.5293097467796575e+106,
        "filterflow_gradient_max_abs": 133.34005587444113,
        "gradient_delta": [
          2.5293097467796575e+106,
          -2.1130211779212787e+106
        ],
        "gradient_explosion_ratio": 1.896886670845081e+104,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.5293097467796575e+106,
        "relative_gradient_delta": 1.896886670845081e+104,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4315730823000195e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.65112643231841e+107,
        "filterflow_gradient_max_abs": 522.1712070050679,
        "gradient_delta": [
          -6.65112643231841e+107,
          5.556445202654388e+107
        ],
        "gradient_explosion_ratio": 1.2737443855754112e+105,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.65112643231841e+107,
        "relative_gradient_delta": 1.2737443855754112e+105,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3040164503763663e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.000450307092154e+110,
        "filterflow_gradient_max_abs": 6.415333698704999,
        "gradient_delta": [
          -1.000450307092154e+110,
          8.3579035309341e+109
        ],
        "gradient_explosion_ratio": 1.559467292081946e+109,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.000450307092154e+110,
        "relative_gradient_delta": 1.559467292081946e+109,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1294503110548249e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4055924940469942e+111,
        "filterflow_gradient_max_abs": 197.4197643907813,
        "gradient_delta": [
          -1.4055924940469942e+111,
          1.1742518729586123e+111
        ],
        "gradient_explosion_ratio": 7.119816490433567e+108,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4055924940469942e+111,
        "relative_gradient_delta": 7.119816490433567e+108,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0837482022907352e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.295277464971095e+113,
        "filterflow_gradient_max_abs": 315.57269054843385,
        "gradient_delta": [
          1.295277464971095e+113,
          -1.0820931355888004e+113
        ],
        "gradient_explosion_ratio": 4.1045296496348655e+110,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.295277464971095e+113,
        "relative_gradient_delta": 4.1045296496348655e+110,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1401937172195176e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.031733243629689e+116,
        "filterflow_gradient_max_abs": 60.009881084342744,
        "gradient_delta": [
          8.031733243629689e+116,
          -6.709823682454014e+116
        ],
        "gradient_explosion_ratio": 1.338401792921609e+115,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.031733243629689e+116,
        "relative_gradient_delta": 1.338401792921609e+115,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1782930187109741e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.97076092639515e+118,
        "filterflow_gradient_max_abs": 147.6346164990015,
        "gradient_delta": [
          -6.97076092639515e+118,
          5.823472385085568e+118
        ],
        "gradient_explosion_ratio": 4.7216303951602674e+116,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.97076092639515e+118,
        "relative_gradient_delta": 4.7216303951602674e+116,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2933298876305344e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3965606638333068e+121,
        "filterflow_gradient_max_abs": 512.611395216775,
        "gradient_delta": [
          -1.3965606638333068e+121,
          1.1667065541058287e+121
        ],
        "gradient_explosion_ratio": 2.7244042502073603e+118,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3965606638333068e+121,
        "relative_gradient_delta": 2.7244042502073603e+118,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.554774583695689e-10,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2085689834560543e+123,
        "filterflow_gradient_max_abs": 87.5818933878043,
        "gradient_delta": [
          -2.2085689834560543e+123,
          1.845069802496302e+123
        ],
        "gradient_explosion_ratio": 2.521718700093318e+121,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2085689834560543e+123,
        "relative_gradient_delta": 2.521718700093318e+121,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0234515457341331e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.763958503547678e+125,
        "filterflow_gradient_max_abs": 57.78168821303872,
        "gradient_delta": [
          -4.763958503547678e+125,
          3.979878392336481e+125
        ],
        "gradient_explosion_ratio": 8.244754784566277e+123,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.763958503547678e+125,
        "relative_gradient_delta": 8.244754784566277e+123,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.412825991399586e-10,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.517392781099118e+128,
        "filterflow_gradient_max_abs": 738.8517276846384,
        "gradient_delta": [
          2.517392781099118e+128,
          -2.1030655760454686e+128
        ],
        "gradient_explosion_ratio": 3.407169106835477e+125,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.517392781099118e+128,
        "relative_gradient_delta": 3.407169106835477e+125,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1248317832723842e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3655045520491896e+131,
        "filterflow_gradient_max_abs": 1019.3972961264672,
        "gradient_delta": [
          -2.3655045520491896e+131,
          1.9761759987336824e+131
        ],
        "gradient_explosion_ratio": 2.320493257180195e+128,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3655045520491896e+131,
        "relative_gradient_delta": 2.320493257180195e+128,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.905196414663806e-10,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.255276366901258e+133,
        "filterflow_gradient_max_abs": 122.24440141690243,
        "gradient_delta": [
          -3.255276366901258e+133,
          2.7195039721832146e+133
        ],
        "gradient_explosion_ratio": 2.6629247058926323e+131,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.255276366901258e+133,
        "relative_gradient_delta": 2.6629247058926323e+131,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.500755489469157e-10,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1642182871878157e+136,
        "filterflow_gradient_max_abs": 682.5428603420182,
        "gradient_delta": [
          2.1642182871878157e+136,
          -1.8080186028203177e+136
        ],
        "gradient_explosion_ratio": 3.170816681172723e+133,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1642182871878157e+136,
        "relative_gradient_delta": 3.170816681172723e+133,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.193943136167945e-10,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3122920658181975e+138,
        "filterflow_gradient_max_abs": 309.19172560146353,
        "gradient_delta": [
          3.3122920658181975e+138,
          -2.767135694410542e+138
        ],
        "gradient_explosion_ratio": 1.071274484908958e+136,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3122920658181975e+138,
        "relative_gradient_delta": 1.071274484908958e+136,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.828742016296019e-10,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7028209769074936e+141,
        "filterflow_gradient_max_abs": 66.90489544481636,
        "gradient_delta": [
          -1.7028209769074936e+141,
          1.422560756346774e+141
        ],
        "gradient_explosion_ratio": 2.5451365936473103e+139,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7028209769074936e+141,
        "relative_gradient_delta": 2.5451365936473103e+139,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.207851927480078e-10,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.373764197360021e+143,
        "filterflow_gradient_max_abs": 750.3754788438333,
        "gradient_delta": [
          -4.373764197360021e+143,
          3.6539045437287463e+143
        ],
        "gradient_explosion_ratio": 5.828767491308548e+140,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.373764197360021e+143,
        "relative_gradient_delta": 5.828767491308548e+140,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.709637207473861e-10,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7385792313518547e+145,
        "filterflow_gradient_max_abs": 347.8401730350442,
        "gradient_delta": [
          -1.7385792313518547e+145,
          1.4524337084526334e+145
        ],
        "gradient_explosion_ratio": 4.998212875131868e+142,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7385792313518547e+145,
        "relative_gradient_delta": 4.998212875131868e+142,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.423448439818458e-10,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.406500081287934e+147,
        "filterflow_gradient_max_abs": 441.50385013274905,
        "gradient_delta": [
          4.406500081287934e+147,
          -3.681252564707878e+147
        ],
        "gradient_explosion_ratio": 9.980660598912129e+144,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.406500081287934e+147,
        "relative_gradient_delta": 9.980660598912129e+144,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.418084007644211e-10,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3807413991679678e+151,
        "filterflow_gradient_max_abs": 216.5606746935064,
        "gradient_delta": [
          2.3807413991679678e+151,
          -1.9889050765730885e+151
        ],
        "gradient_explosion_ratio": 1.0993415136600304e+149,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3807413991679678e+151,
        "relative_gradient_delta": 1.0993415136600304e+149,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.252687505068025e-10,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.052256830238403e+153,
        "filterflow_gradient_max_abs": 592.4376179231792,
        "gradient_delta": [
          8.052256830238403e+153,
          -6.726969377324458e+153
        ],
        "gradient_explosion_ratio": 1.359173790899033e+151,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.052256830238403e+153,
        "relative_gradient_delta": 1.359173790899033e+151,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.707559118192876e-10,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.571031831462472e+157,
        "filterflow_gradient_max_abs": 1021.9536107722753,
        "gradient_delta": [
          -1.571031831462472e+157,
          1.31246223808501e+157
        ],
        "gradient_explosion_ratio": 1.5372829205772523e+154,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.571031831462472e+157,
        "relative_gradient_delta": 1.5372829205772523e+154,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.629843589209486e-10,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.262837809926604e+158,
        "filterflow_gradient_max_abs": 416.36976112409496,
        "gradient_delta": [
          -4.262837809926604e+158,
          3.5612350689301207e+158
        ],
        "gradient_explosion_ratio": 1.0238106144927528e+156,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.262837809926604e+158,
        "relative_gradient_delta": 1.0238106144927528e+156,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.8334494446608e-10,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.262079356201493e+162,
        "filterflow_gradient_max_abs": 73.20765898029507,
        "gradient_delta": [
          1.262079356201493e+162,
          -1.0543589654317367e+162
        ],
        "gradient_explosion_ratio": 1.723971745280368e+160,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.262079356201493e+162,
        "relative_gradient_delta": 1.723971745280368e+160,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.958771336940117e-10,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.0558199250318157e+164,
        "filterflow_gradient_max_abs": 18.775557058598526,
        "gradient_delta": [
          4.0558199250318157e+164,
          -3.3882893964801176e+164
        ],
        "gradient_explosion_ratio": 2.1601595693664903e+163,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.0558199250318157e+164,
        "relative_gradient_delta": 2.1601595693664903e+163,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.100187187665142e-10,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.196782127210011e+166,
        "filterflow_gradient_max_abs": 489.4717191114149,
        "gradient_delta": [
          -2.196782127210011e+166,
          1.8352228958844447e+166
        ],
        "gradient_explosion_ratio": 4.488067525531487e+163,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.196782127210011e+166,
        "relative_gradient_delta": 4.488067525531487e+163,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.418758857762441e-10,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.082038981854977e+168,
        "filterflow_gradient_max_abs": 603.1903641588457,
        "gradient_delta": [
          1.082038981854977e+168,
          -9.039506872999548e+167
        ],
        "gradient_explosion_ratio": 1.7938598594224726e+165,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.082038981854977e+168,
        "relative_gradient_delta": 1.7938598594224726e+165,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0115144277733634e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5404613362590854e+172,
        "filterflow_gradient_max_abs": 924.7685421225882,
        "gradient_delta": [
          1.5404613362590854e+172,
          -1.286923213508624e+172
        ],
        "gradient_explosion_ratio": 1.665780426227864e+169,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5404613362590854e+172,
        "relative_gradient_delta": 1.665780426227864e+169,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2003482652289676e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.105923378516135e+174,
        "filterflow_gradient_max_abs": 712.4012104561216,
        "gradient_delta": [
          -5.105923378516135e+174,
          4.265560691166644e+174
        ],
        "gradient_explosion_ratio": 7.167201997378723e+171,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.105923378516135e+174,
        "relative_gradient_delta": 7.167201997378723e+171,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.9136194850943866e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1109753841152565e+178,
        "filterflow_gradient_max_abs": 1186.5395908091443,
        "gradient_delta": [
          -1.1109753841152565e+178,
          9.281245674926302e+177
        ],
        "gradient_explosion_ratio": 9.363154779838759e+174,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1109753841152565e+178,
        "relative_gradient_delta": 9.363154779838759e+174,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.708955086447531e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.0228776282893772e+180,
        "filterflow_gradient_max_abs": 155.19429188795652,
        "gradient_delta": [
          -3.0228776282893772e+180,
          2.525354775140694e+180
        ],
        "gradient_explosion_ratio": 1.9478020689522283e+178,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.0228776282893772e+180,
        "relative_gradient_delta": 1.9478020689522283e+178,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.22875973022019e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.94018094941109e+182,
        "filterflow_gradient_max_abs": 232.51294890916668,
        "gradient_delta": [
          -7.94018094941109e+182,
          6.63333959946754e+182
        ],
        "gradient_explosion_ratio": 3.414941398602705e+180,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.94018094941109e+182,
        "relative_gradient_delta": 3.414941398602705e+180,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.486573056463385e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.92326011592649e+186,
        "filterflow_gradient_max_abs": 1518.8797828290087,
        "gradient_delta": [
          -1.92326011592649e+186,
          1.6067187345394106e+186
        ],
        "gradient_explosion_ratio": 1.2662359046904275e+183,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.92326011592649e+186,
        "relative_gradient_delta": 1.2662359046904275e+183,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.5804499627120094e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.363693825366473e+188,
        "filterflow_gradient_max_abs": 92.4227988005718,
        "gradient_delta": [
          -6.363693825366473e+188,
          5.316319932711531e+188
        ],
        "gradient_explosion_ratio": 6.885415620336205e+186,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.363693825366473e+188,
        "relative_gradient_delta": 6.885415620336205e+186,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.631609039686737e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.896718775355686e+189,
        "filterflow_gradient_max_abs": 495.480272228227,
        "gradient_delta": [
          -9.896718775355686e+189,
          8.267859004174193e+189
        ],
        "gradient_explosion_ratio": 1.997399155944009e+187,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.896718775355686e+189,
        "relative_gradient_delta": 1.997399155944009e+187,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.181977596497745e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.4221068831516946e+194,
        "filterflow_gradient_max_abs": 1905.453488616431,
        "gradient_delta": [
          4.4221068831516946e+194,
          -3.6942907079798645e+194
        ],
        "gradient_explosion_ratio": 2.3207634873116904e+191,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.4221068831516946e+194,
        "relative_gradient_delta": 2.3207634873116904e+191,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.158671794764814e-09,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.53052295090967e+196,
        "filterflow_gradient_max_abs": 536.1521590308598,
        "gradient_delta": [
          5.53052295090967e+196,
          -4.62027718634726e+196
        ],
        "gradient_explosion_ratio": 1.0315211564020475e+194,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.53052295090967e+196,
        "relative_gradient_delta": 1.0315211564020475e+194,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.624389925491414e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.096191776557516e+199,
        "filterflow_gradient_max_abs": 85.09097085867334,
        "gradient_delta": [
          -5.096191776557516e+199,
          4.257430773089252e+199
        ],
        "gradient_explosion_ratio": 5.989109919807738e+197,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.096191776557516e+199,
        "relative_gradient_delta": 5.989109919807738e+197,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.351314141284092e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.428324101233285e+202,
        "filterflow_gradient_max_abs": 286.3674760142073,
        "gradient_delta": [
          1.428324101233285e+202,
          -1.1932421794855127e+202
        ],
        "gradient_explosion_ratio": 4.98773157173206e+199,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.428324101233285e+202,
        "relative_gradient_delta": 4.98773157173206e+199,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.2123888255882775e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.8722507085397855e+205,
        "filterflow_gradient_max_abs": 1646.6707953160178,
        "gradient_delta": [
          2.8722507085397855e+205,
          -2.399518913478762e+205
        ],
        "gradient_explosion_ratio": 1.7442774334189627e+202,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.8722507085397855e+205,
        "relative_gradient_delta": 1.7442774334189627e+202,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.9354371134977555e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.458655116980666e+208,
        "filterflow_gradient_max_abs": 1706.2194857616348,
        "gradient_delta": [
          -4.458655116980666e+208,
          3.7248236200498724e+208
        ],
        "gradient_explosion_ratio": 2.6131779376499024e+205,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.458655116980666e+208,
        "relative_gradient_delta": 2.6131779376499024e+205,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.4229368490487104e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1628491625680144e+211,
        "filterflow_gradient_max_abs": 491.76925290563014,
        "gradient_delta": [
          -1.1628491625680144e+211,
          9.714606565536994e+210
        ],
        "gradient_explosion_ratio": 2.364623562163134e+208,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1628491625680144e+211,
        "relative_gradient_delta": 2.364623562163134e+208,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.928541213506833e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.099859724449997e+213,
        "filterflow_gradient_max_abs": 953.0377691516383,
        "gradient_delta": [
          -4.099859724449997e+213,
          3.425080868525209e+213
        ],
        "gradient_explosion_ratio": 4.3018858823397445e+210,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.099859724449997e+213,
        "relative_gradient_delta": 4.3018858823397445e+210,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.896453103559907e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.22166327232064e+217,
        "filterflow_gradient_max_abs": 1943.4208738111502,
        "gradient_delta": [
          2.22166327232064e+217,
          -1.8560089568311628e+217
        ],
        "gradient_explosion_ratio": 1.1431714572272972e+214,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.22166327232064e+217,
        "relative_gradient_delta": 1.1431714572272972e+214,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.690761887919507e-09,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3515114431922745e+218,
        "filterflow_gradient_max_abs": 950.6655619127545,
        "gradient_delta": [
          1.3515114431922745e+218,
          -1.1290717972775883e+218
        ],
        "gradient_explosion_ratio": 1.4216476301855425e+215,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3515114431922745e+218,
        "relative_gradient_delta": 1.4216476301855425e+215,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.408061719615944e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_raw_transport_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      7025.174608954654,
      713.4652966764394
    ],
    "final_bayesfilter_gradient_max_abs": 7025.174608954654,
    "final_filterflow_gradient_diag": [
      7019.871883303286,
      713.5990730344417
    ],
    "final_filterflow_gradient_max_abs": 7019.871883303286,
    "final_gradient_delta": [
      5.302725651367837,
      -0.13377635800236476
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 5.302725651367837,
    "final_relative_gradient_delta": 0.000755387810421488,
    "final_scalar_delta": 7.407919611068792e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "status": "no_explosion"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 0.9982237942828173,
      "max_abs_gradient_delta": 0.01573802857856954,
      "relative_gradient_delta": 0.001776205717182703,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.8406609569865395e-11,
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
        "bayesfilter_gradient_max_abs": 0.008924445612040184,
        "filterflow_gradient_max_abs": 0.008924445612040184,
        "gradient_delta": [
          0.0,
          -5.795395272864551e-20
        ],
        "gradient_explosion_ratio": 0.008924445612040184,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 5.795395272864551e-20,
        "relative_gradient_delta": 5.795395272864551e-20,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.844738225000961,
        "filterflow_gradient_max_abs": 8.860476253579531,
        "gradient_delta": [
          0.01573802857856954,
          -0.010466566493996415
        ],
        "gradient_explosion_ratio": 0.9982237942828173,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.01573802857856954,
        "relative_gradient_delta": 0.001776205717182703,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8406609569865395e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.332502147276955,
        "filterflow_gradient_max_abs": 1.4056099396090884,
        "gradient_delta": [
          -7.738112086886043,
          -0.9347283384324468
        ],
        "gradient_explosion_ratio": 4.505163181357465,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.738112086886043,
        "relative_gradient_delta": 5.505163181357465,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.5511147921642987e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 50.73284126858788,
        "filterflow_gradient_max_abs": 14.864972477668916,
        "gradient_delta": [
          -61.7198257412653,
          50.73284126858788
        ],
        "gradient_explosion_ratio": 3.412911886974692,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 61.7198257412653,
        "relative_gradient_delta": 4.152030946171253,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.2442492308982764e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.900398612096756,
        "filterflow_gradient_max_abs": 15.00462728219541,
        "gradient_delta": [
          22.272686058028675,
          -7.9003986120967555
        ],
        "gradient_explosion_ratio": 0.5265308136958138,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 22.272686058028675,
        "relative_gradient_delta": 1.4843878251116303,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.779998453661392e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.480401242657742,
        "filterflow_gradient_max_abs": 6.525931066391355,
        "gradient_delta": [
          15.006332309049096,
          5.14373424227443
        ],
        "gradient_explosion_ratio": 1.2994929239035236,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 15.006332309049096,
        "relative_gradient_delta": 2.2994929239035238,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.1093350116861984e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 129.43635622392736,
        "filterflow_gradient_max_abs": 2.686919378388484,
        "gradient_delta": [
          126.74943684553888,
          -12.008544879397796
        ],
        "gradient_explosion_ratio": 48.17277260531671,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 126.74943684553888,
        "relative_gradient_delta": 47.17277260531671,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4224179873708636e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 56.40807049950997,
        "filterflow_gradient_max_abs": 24.973165642495765,
        "gradient_delta": [
          -31.434904857014203,
          -11.23509060278943
        ],
        "gradient_explosion_ratio": 2.258747301284174,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 31.434904857014203,
        "relative_gradient_delta": 1.2587473012841741,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.5496940376542625e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 343.61344900930897,
        "filterflow_gradient_max_abs": 0.7972582915878877,
        "gradient_delta": [
          344.41070730089683,
          -61.05476766008374
        ],
        "gradient_explosion_ratio": 343.61344900930897,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 344.41070730089683,
        "relative_gradient_delta": 344.41070730089683,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.66524613279762e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 172.79510848644207,
        "filterflow_gradient_max_abs": 49.77299487676166,
        "gradient_delta": [
          123.02211360968042,
          -24.17772558607598
        ],
        "gradient_explosion_ratio": 3.471663879464842,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 123.02211360968042,
        "relative_gradient_delta": 2.471663879464842,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.581402089977928e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 184.3938068015041,
        "filterflow_gradient_max_abs": 91.01474473671405,
        "gradient_delta": [
          93.37906206479005,
          -42.64089343967298
        ],
        "gradient_explosion_ratio": 2.025977299995901,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 93.37906206479005,
        "relative_gradient_delta": 1.0259772999959014,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.424994118489849e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 293.4146571353721,
        "filterflow_gradient_max_abs": 28.00263902728941,
        "gradient_delta": [
          321.41729616266156,
          -42.70185892925031
        ],
        "gradient_explosion_ratio": 10.478107325864208,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 321.41729616266156,
        "relative_gradient_delta": 11.478107325864208,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.85451720225683e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 364.9141588298781,
        "filterflow_gradient_max_abs": 40.13671871067378,
        "gradient_delta": [
          324.7774401192043,
          -54.81422868643127
        ],
        "gradient_explosion_ratio": 9.091778564669623,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 324.7774401192043,
        "relative_gradient_delta": 8.091778564669623,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3077183780296764e-10,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 716.4812874761782,
        "filterflow_gradient_max_abs": 49.010874255508995,
        "gradient_delta": [
          667.4704132206692,
          -42.46869461214577
        ],
        "gradient_explosion_ratio": 14.618822829826243,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 667.4704132206692,
        "relative_gradient_delta": 13.618822829826245,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4137313542050833e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 898.238063245043,
        "filterflow_gradient_max_abs": 21.29035436921441,
        "gradient_delta": [
          876.9477088758287,
          -174.90861080779706
        ],
        "gradient_explosion_ratio": 42.18990664354015,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 876.9477088758287,
        "relative_gradient_delta": 41.18990664354015,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3353940175875323e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 635.2178853945101,
        "filterflow_gradient_max_abs": 27.042811971633515,
        "gradient_delta": [
          662.2606973661436,
          -3.275511403964778
        ],
        "gradient_explosion_ratio": 23.489342974422193,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 662.2606973661436,
        "relative_gradient_delta": 24.489342974422193,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.525606307950511e-10,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1084.0339802417498,
        "filterflow_gradient_max_abs": 18.468136147749064,
        "gradient_delta": [
          1102.5021163894987,
          -42.19862565145543
        ],
        "gradient_explosion_ratio": 58.69753025260614,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1102.5021163894987,
        "relative_gradient_delta": 59.697530252606136,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7488588355263346e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 303.9733079617048,
        "filterflow_gradient_max_abs": 102.94637935328883,
        "gradient_delta": [
          201.02692860841597,
          43.654245924411974
        ],
        "gradient_explosion_ratio": 2.952734325104691,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 201.02692860841597,
        "relative_gradient_delta": 1.9527343251046911,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3816503496855148e-10,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1458.6448718918386,
        "filterflow_gradient_max_abs": 113.77902775418237,
        "gradient_delta": [
          1344.8658441376563,
          -183.65921476825196
        ],
        "gradient_explosion_ratio": 12.819980102512528,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1344.8658441376563,
        "relative_gradient_delta": 11.819980102512528,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.3455015707440907e-10,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 110.9012514585786,
        "filterflow_gradient_max_abs": 165.42250820864194,
        "gradient_delta": [
          54.521256750063344,
          -16.291942553091168
        ],
        "gradient_explosion_ratio": 0.6704121020744197,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 54.521256750063344,
        "relative_gradient_delta": 0.32958789792558024,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.92866184029117e-10,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1067.227215092727,
        "filterflow_gradient_max_abs": 73.77440324184383,
        "gradient_delta": [
          993.4528118508831,
          -10.151807850176226
        ],
        "gradient_explosion_ratio": 14.46609078753497,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 993.4528118508831,
        "relative_gradient_delta": 13.466090787534968,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4417447497835383e-10,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1074.731139850693,
        "filterflow_gradient_max_abs": 217.86217342911775,
        "gradient_delta": [
          856.8689664215751,
          6.338957877369029
        ],
        "gradient_explosion_ratio": 4.933078206898365,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 856.8689664215751,
        "relative_gradient_delta": 3.933078206898365,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.974509693056461e-10,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1640.9413660373716,
        "filterflow_gradient_max_abs": 165.63087578642663,
        "gradient_delta": [
          1475.310490250945,
          -121.68212178818911
        ],
        "gradient_explosion_ratio": 9.907219038999044,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1475.310490250945,
        "relative_gradient_delta": 8.907219038999044,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.2155079427175224e-10,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1673.6069140984184,
        "filterflow_gradient_max_abs": 20.952482372929534,
        "gradient_delta": [
          1694.559396471348,
          -85.48736070690242
        ],
        "gradient_explosion_ratio": 79.87630698406922,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1694.559396471348,
        "relative_gradient_delta": 80.87630698406922,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.807603204426414e-10,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3224.3267645592096,
        "filterflow_gradient_max_abs": 45.60764934214221,
        "gradient_delta": [
          3269.934413901352,
          -184.3032449332778
        ],
        "gradient_explosion_ratio": 70.69706093315095,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3269.934413901352,
        "relative_gradient_delta": 71.69706093315095,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.035900585426134e-10,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 245.17416429907186,
        "filterflow_gradient_max_abs": 95.80515251122853,
        "gradient_delta": [
          -149.36901178784333,
          -8.937014001688441
        ],
        "gradient_explosion_ratio": 2.5590916341408363,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 149.36901178784333,
        "relative_gradient_delta": 1.5590916341408363,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.194777941142092e-10,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2704.031265436486,
        "filterflow_gradient_max_abs": 162.31717661541148,
        "gradient_delta": [
          2541.7140888210747,
          -179.81137140617543
        ],
        "gradient_explosion_ratio": 16.658934820208962,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2541.7140888210747,
        "relative_gradient_delta": 15.658934820208962,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.324789415477426e-10,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2332.385674735323,
        "filterflow_gradient_max_abs": 65.61469672303252,
        "gradient_delta": [
          -2266.7709780122905,
          262.1542171950335
        ],
        "gradient_explosion_ratio": 35.54669595716645,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2266.7709780122905,
        "relative_gradient_delta": 34.54669595716645,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.852775876111991e-10,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1966.0753104584846,
        "filterflow_gradient_max_abs": 353.91086072731014,
        "gradient_delta": [
          1612.1644497311745,
          -77.27607751780782
        ],
        "gradient_explosion_ratio": 5.55528391080757,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1612.1644497311745,
        "relative_gradient_delta": 4.55528391080757,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.191615860487218e-10,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1379.4559497645268,
        "filterflow_gradient_max_abs": 106.57513689011893,
        "gradient_delta": [
          1272.8808128744079,
          -196.75620956232189
        ],
        "gradient_explosion_ratio": 12.94350624373838,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1272.8808128744079,
        "relative_gradient_delta": 11.94350624373838,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.87274212698685e-10,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5328.271386082137,
        "filterflow_gradient_max_abs": 301.25080522517993,
        "gradient_delta": [
          5027.020580856957,
          -331.91774520785486
        ],
        "gradient_explosion_ratio": 17.68716064376772,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5027.020580856957,
        "relative_gradient_delta": 16.68716064376772,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.1155345797960763e-10,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2858.6995808150104,
        "filterflow_gradient_max_abs": 406.1376803574301,
        "gradient_delta": [
          -2452.56190045758,
          311.48615481223146
        ],
        "gradient_explosion_ratio": 7.0387450341941955,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2452.56190045758,
        "relative_gradient_delta": 6.038745034194195,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.641514005423232e-10,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2124.906432039978,
        "filterflow_gradient_max_abs": 226.31263344208014,
        "gradient_delta": [
          1898.5937985978978,
          10.310201951915372
        ],
        "gradient_explosion_ratio": 9.389252379424953,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1898.5937985978978,
        "relative_gradient_delta": 8.389252379424953,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.090381697911653e-10,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2626.5006963949804,
        "filterflow_gradient_max_abs": 6.85443174851973,
        "gradient_delta": [
          -2633.3551281435,
          62.67499664079372
        ],
        "gradient_explosion_ratio": 383.1828505641178,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2633.3551281435,
        "relative_gradient_delta": 384.1828505641178,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.083187369971711e-10,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2417.7759453694594,
        "filterflow_gradient_max_abs": 80.80287856491722,
        "gradient_delta": [
          2336.973066804542,
          66.05957576537386
        ],
        "gradient_explosion_ratio": 29.92190362905218,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2336.973066804542,
        "relative_gradient_delta": 28.92190362905218,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.413411940935475e-10,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 805.557281642863,
        "filterflow_gradient_max_abs": 195.04750763879625,
        "gradient_delta": [
          610.5097740040668,
          -1.9598614117177573
        ],
        "gradient_explosion_ratio": 4.130056781523479,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 610.5097740040668,
        "relative_gradient_delta": 3.130056781523479,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.915747808809101e-10,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2898.4060600731627,
        "filterflow_gradient_max_abs": 227.99933783381496,
        "gradient_delta": [
          2670.406722239348,
          96.5988807197291
        ],
        "gradient_explosion_ratio": 12.712344200691337,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2670.406722239348,
        "relative_gradient_delta": 11.712344200691337,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4428105638871784e-10,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2827.102555588917,
        "filterflow_gradient_max_abs": 498.30983956509795,
        "gradient_delta": [
          3325.412395154015,
          83.50976032434593
        ],
        "gradient_explosion_ratio": 5.673382966020263,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3325.412395154015,
        "relative_gradient_delta": 6.673382966020264,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.725002776875044e-10,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 279.4128414733892,
        "filterflow_gradient_max_abs": 348.59095258355785,
        "gradient_delta": [
          628.0037940569471,
          -79.1414143706532
        ],
        "gradient_explosion_ratio": 0.801549321353696,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 628.0037940569471,
        "relative_gradient_delta": 1.801549321353696,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.749836080009118e-10,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4880.745030628637,
        "filterflow_gradient_max_abs": 24.53415070247347,
        "gradient_delta": [
          4856.210879926164,
          -221.68556403192215
        ],
        "gradient_explosion_ratio": 198.9367836619905,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4856.210879926164,
        "relative_gradient_delta": 197.93678366199052,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9053560385582387e-10,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4671.090898808877,
        "filterflow_gradient_max_abs": 743.4955982984612,
        "gradient_delta": [
          -5414.586497107338,
          262.4267308527541
        ],
        "gradient_explosion_ratio": 6.282607334191321,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5414.586497107338,
        "relative_gradient_delta": 7.2826073341913204,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3861267689208034e-10,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4439.093410653595,
        "filterflow_gradient_max_abs": 660.4154280128698,
        "gradient_delta": [
          5099.508838666465,
          -50.82700916806921
        ],
        "gradient_explosion_ratio": 6.721668244502442,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5099.508838666465,
        "relative_gradient_delta": 7.721668244502441,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2236966995260445e-10,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4817.256170663271,
        "filterflow_gradient_max_abs": 151.38043625809377,
        "gradient_delta": [
          4665.875734405177,
          19.302706487077682
        ],
        "gradient_explosion_ratio": 31.822184489217378,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4665.875734405177,
        "relative_gradient_delta": 30.822184489217374,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.503508428868372e-10,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3759.7458057725753,
        "filterflow_gradient_max_abs": 78.34314644911912,
        "gradient_delta": [
          -3838.0889522216944,
          117.8936229474609
        ],
        "gradient_explosion_ratio": 47.990742983681244,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3838.0889522216944,
        "relative_gradient_delta": 48.990742983681244,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4379963886312908e-10,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4210.343179286367,
        "filterflow_gradient_max_abs": 375.1405380302191,
        "gradient_delta": [
          -4585.483717316586,
          161.05020820253063
        ],
        "gradient_explosion_ratio": 11.223375648480854,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4585.483717316586,
        "relative_gradient_delta": 12.223375648480856,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.290931888637715e-10,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4870.907648283121,
        "filterflow_gradient_max_abs": 190.9613749711765,
        "gradient_delta": [
          -5061.869023254297,
          177.33337266712505
        ],
        "gradient_explosion_ratio": 25.50729250361928,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5061.869023254297,
        "relative_gradient_delta": 26.50729250361928,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.651177055668086e-10,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 351.987986655819,
        "filterflow_gradient_max_abs": 677.2028181986615,
        "gradient_delta": [
          325.2148315428425,
          -5.665703533542062
        ],
        "gradient_explosion_ratio": 0.5197674569519604,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 325.2148315428425,
        "relative_gradient_delta": 0.4802325430480397,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.92969196177728e-10,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2179.4237050328616,
        "filterflow_gradient_max_abs": 152.6174741556563,
        "gradient_delta": [
          2332.041179188518,
          -125.88104724670987
        ],
        "gradient_explosion_ratio": 14.280302547859247,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2332.041179188518,
        "relative_gradient_delta": 15.280302547859248,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.625100468227174e-11,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13664.57077582417,
        "filterflow_gradient_max_abs": 207.0601214499801,
        "gradient_delta": [
          13457.51065437419,
          -294.13526978881794
        ],
        "gradient_explosion_ratio": 65.993252008814,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13457.51065437419,
        "relative_gradient_delta": 64.993252008814,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.438458406890277e-10,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2732.589436113304,
        "filterflow_gradient_max_abs": 546.4746634801378,
        "gradient_delta": [
          3279.064099593442,
          -125.18962097180408
        ],
        "gradient_explosion_ratio": 5.000395478010342,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3279.064099593442,
        "relative_gradient_delta": 6.000395478010342,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.842170943040401e-14,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7258.447703044252,
        "filterflow_gradient_max_abs": 272.67443106070385,
        "gradient_delta": [
          -6985.7732719835485,
          360.67994193379775
        ],
        "gradient_explosion_ratio": 26.619465839935494,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6985.7732719835485,
        "relative_gradient_delta": 25.619465839935494,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.5509905299259117e-10,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2884.0701464386952,
        "filterflow_gradient_max_abs": 949.676068984666,
        "gradient_delta": [
          1934.3940774540292,
          -63.95807558518791
        ],
        "gradient_explosion_ratio": 3.036898833854118,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1934.3940774540292,
        "relative_gradient_delta": 2.036898833854118,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.264737647943548e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4930.362579745341,
        "filterflow_gradient_max_abs": 101.55125271438094,
        "gradient_delta": [
          5031.913832459722,
          -125.7870833565469
        ],
        "gradient_explosion_ratio": 48.55048507980778,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5031.913832459722,
        "relative_gradient_delta": 49.55048507980778,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.427679308108054e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5882.9021610719865,
        "filterflow_gradient_max_abs": 177.86655077673558,
        "gradient_delta": [
          -5705.035610295251,
          295.9769001010349
        ],
        "gradient_explosion_ratio": 33.074808812458585,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5705.035610295251,
        "relative_gradient_delta": 32.074808812458585,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3662173614648054e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7641.796134538008,
        "filterflow_gradient_max_abs": 135.59093315487942,
        "gradient_delta": [
          7506.205201383129,
          -229.02995613187986
        ],
        "gradient_explosion_ratio": 56.35919715818408,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7506.205201383129,
        "relative_gradient_delta": 55.35919715818408,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.345853206657921e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6954.871588185397,
        "filterflow_gradient_max_abs": 133.34005587444113,
        "gradient_delta": [
          -7088.211644059838,
          351.4798513355178
        ],
        "gradient_explosion_ratio": 52.15890710841167,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7088.211644059838,
        "relative_gradient_delta": 53.158907108411675,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4315730823000195e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8426.44455255231,
        "filterflow_gradient_max_abs": 522.1712070050679,
        "gradient_delta": [
          -8948.615759557377,
          437.48200437268696
        ],
        "gradient_explosion_ratio": 16.137321322028633,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8948.615759557377,
        "relative_gradient_delta": 17.137321322028633,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3040164503763663e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3803.1029828810933,
        "filterflow_gradient_max_abs": 6.415333698704999,
        "gradient_delta": [
          3809.5183165797985,
          -133.47378020846332
        ],
        "gradient_explosion_ratio": 592.8145224384491,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3809.5183165797985,
        "relative_gradient_delta": 593.8145224384491,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1294503110548249e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 957.2309223336387,
        "filterflow_gradient_max_abs": 197.4197643907813,
        "gradient_delta": [
          -759.8111579428573,
          200.31384922828678
        ],
        "gradient_explosion_ratio": 4.848708665454863,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 759.8111579428573,
        "relative_gradient_delta": 3.848708665454863,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0837482022907352e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8834.094283706583,
        "filterflow_gradient_max_abs": 315.57269054843385,
        "gradient_delta": [
          -9149.666974255017,
          434.36527676383844
        ],
        "gradient_explosion_ratio": 27.99384911398324,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9149.666974255017,
        "relative_gradient_delta": 28.99384911398324,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1401937172195176e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 772.0616870954552,
        "filterflow_gradient_max_abs": 60.009881084342744,
        "gradient_delta": [
          712.0518060111125,
          -91.25754482671599
        ],
        "gradient_explosion_ratio": 12.86557602089458,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 712.0518060111125,
        "relative_gradient_delta": 11.86557602089458,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1782930187109741e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 847.4533950800969,
        "filterflow_gradient_max_abs": 147.6346164990015,
        "gradient_delta": [
          699.8187785810954,
          -53.764734405063734
        ],
        "gradient_explosion_ratio": 5.7402079212623445,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 699.8187785810954,
        "relative_gradient_delta": 4.740207921262345,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2933298876305344e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7176.180742735477,
        "filterflow_gradient_max_abs": 512.611395216775,
        "gradient_delta": [
          6663.569347518702,
          -187.08646915307267
        ],
        "gradient_explosion_ratio": 13.999261057590784,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6663.569347518702,
        "relative_gradient_delta": 12.999261057590784,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.554774583695689e-10,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8091.961875840569,
        "filterflow_gradient_max_abs": 87.5818933878043,
        "gradient_delta": [
          8179.543769228373,
          -294.4543331976615
        ],
        "gradient_explosion_ratio": 92.39309134377959,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8179.543769228373,
        "relative_gradient_delta": 93.39309134377959,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0234515457341331e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4166.132524799472,
        "filterflow_gradient_max_abs": 57.78168821303872,
        "gradient_delta": [
          4223.914213012511,
          -247.40131869602703
        ],
        "gradient_explosion_ratio": 72.10125999501973,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4223.914213012511,
        "relative_gradient_delta": 73.10125999501975,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.412825991399586e-10,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2429.491274976307,
        "filterflow_gradient_max_abs": 738.8517276846384,
        "gradient_delta": [
          1690.6395472916688,
          31.047686435399655
        ],
        "gradient_explosion_ratio": 3.288198679036288,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1690.6395472916688,
        "relative_gradient_delta": 2.288198679036288,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1248317832723842e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4508.91392292622,
        "filterflow_gradient_max_abs": 1019.3972961264672,
        "gradient_delta": [
          3489.516626799753,
          -135.79790419815114
        ],
        "gradient_explosion_ratio": 4.423117404822743,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3489.516626799753,
        "relative_gradient_delta": 3.4231174048227424,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.905196414663806e-10,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 14753.055806956583,
        "filterflow_gradient_max_abs": 122.24440141690243,
        "gradient_delta": [
          14875.300208373486,
          -587.2344614543055
        ],
        "gradient_explosion_ratio": 120.68492001235089,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 14875.300208373486,
        "relative_gradient_delta": 121.68492001235089,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.500755489469157e-10,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 11099.407014834074,
        "filterflow_gradient_max_abs": 682.5428603420182,
        "gradient_delta": [
          -11781.949875176093,
          711.0158075830417
        ],
        "gradient_explosion_ratio": 16.261846192739057,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 11781.949875176093,
        "relative_gradient_delta": 17.261846192739057,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.193943136167945e-10,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13666.682033569092,
        "filterflow_gradient_max_abs": 309.19172560146353,
        "gradient_delta": [
          -13975.873759170556,
          897.0318478861757
        ],
        "gradient_explosion_ratio": 44.20131879979521,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13975.873759170556,
        "relative_gradient_delta": 45.20131879979521,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.828742016296019e-10,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9331.436614280134,
        "filterflow_gradient_max_abs": 66.90489544481636,
        "gradient_delta": [
          9264.531718835316,
          -501.7665427349902
        ],
        "gradient_explosion_ratio": 139.47315143742762,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9264.531718835316,
        "relative_gradient_delta": 138.47315143742762,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.207851927480078e-10,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10869.909435541349,
        "filterflow_gradient_max_abs": 750.3754788438333,
        "gradient_delta": [
          10119.533956697516,
          -484.94245365069486
        ],
        "gradient_explosion_ratio": 14.485960351862156,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10119.533956697516,
        "relative_gradient_delta": 13.485960351862156,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.709637207473861e-10,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7686.743928642085,
        "filterflow_gradient_max_abs": 347.8401730350442,
        "gradient_delta": [
          8034.584101677129,
          122.53124699521211
        ],
        "gradient_explosion_ratio": 22.098493861626675,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8034.584101677129,
        "relative_gradient_delta": 23.098493861626675,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.423448439818458e-10,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6285.313871551408,
        "filterflow_gradient_max_abs": 441.50385013274905,
        "gradient_delta": [
          -6726.817721684157,
          727.4280137161155
        ],
        "gradient_explosion_ratio": 14.23614736238783,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6726.817721684157,
        "relative_gradient_delta": 15.23614736238783,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.418084007644211e-10,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 762.8643246802055,
        "filterflow_gradient_max_abs": 216.5606746935064,
        "gradient_delta": [
          546.3036499866992,
          -97.82621248290687
        ],
        "gradient_explosion_ratio": 3.5226355189365326,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 546.3036499866992,
        "relative_gradient_delta": 2.5226355189365326,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.252687505068025e-10,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5284.2786489366335,
        "filterflow_gradient_max_abs": 592.4376179231792,
        "gradient_delta": [
          -5876.716266859813,
          555.503693185995
        ],
        "gradient_explosion_ratio": 8.919552859355802,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5876.716266859813,
        "relative_gradient_delta": 9.919552859355802,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.707559118192876e-10,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4795.849583312769,
        "filterflow_gradient_max_abs": 1021.9536107722753,
        "gradient_delta": [
          3773.895972540494,
          168.50004847103943
        ],
        "gradient_explosion_ratio": 4.692825127051135,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3773.895972540494,
        "relative_gradient_delta": 3.6928251270511354,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.629843589209486e-10,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2560.945092210393,
        "filterflow_gradient_max_abs": 416.36976112409496,
        "gradient_delta": [
          2144.575331086298,
          256.35588995381426
        ],
        "gradient_explosion_ratio": 6.150651011006364,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2144.575331086298,
        "relative_gradient_delta": 5.150651011006364,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.8334494446608e-10,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 24691.504447660875,
        "filterflow_gradient_max_abs": 73.20765898029507,
        "gradient_delta": [
          24764.71210664117,
          -758.8748963532263
        ],
        "gradient_explosion_ratio": 337.28034459218213,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 24764.71210664117,
        "relative_gradient_delta": 338.28034459218213,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.958771336940117e-10,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8275.987973305575,
        "filterflow_gradient_max_abs": 18.775557058598526,
        "gradient_delta": [
          -8294.763530364173,
          837.3037731053362
        ],
        "gradient_explosion_ratio": 440.78521598460225,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8294.763530364173,
        "relative_gradient_delta": 441.78521598460225,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.100187187665142e-10,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 624.8299233606532,
        "filterflow_gradient_max_abs": 489.4717191114149,
        "gradient_delta": [
          -1114.3016424720681,
          460.3722040614311
        ],
        "gradient_explosion_ratio": 1.27653937697354,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1114.3016424720681,
        "relative_gradient_delta": 2.27653937697354,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.418758857762441e-10,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 16173.779834286079,
        "filterflow_gradient_max_abs": 603.1903641588457,
        "gradient_delta": [
          -16776.970198444924,
          1274.8198937747513
        ],
        "gradient_explosion_ratio": 26.813723818086117,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 16776.970198444924,
        "relative_gradient_delta": 27.813723818086117,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0115144277733634e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 16961.848887895332,
        "filterflow_gradient_max_abs": 924.7685421225882,
        "gradient_delta": [
          -17886.61743001792,
          1197.1885867999158
        ],
        "gradient_explosion_ratio": 18.341723485709633,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 17886.61743001792,
        "relative_gradient_delta": 19.34172348570963,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2003482652289676e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2016.988285403962,
        "filterflow_gradient_max_abs": 712.4012104561216,
        "gradient_delta": [
          2729.3894958600836,
          270.25172175135833
        ],
        "gradient_explosion_ratio": 2.831253310353819,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2729.3894958600836,
        "relative_gradient_delta": 3.831253310353819,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.9136194850943866e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1062.9961402185072,
        "filterflow_gradient_max_abs": 1186.5395908091443,
        "gradient_delta": [
          -123.54345059063712,
          333.1756115244914
        ],
        "gradient_explosion_ratio": 0.8958792007046403,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 333.1756115244914,
        "relative_gradient_delta": 0.28079603420336513,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.708955086447531e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 21657.773259536876,
        "filterflow_gradient_max_abs": 155.19429188795652,
        "gradient_delta": [
          21812.967551424834,
          -565.0495093630502
        ],
        "gradient_explosion_ratio": 139.55264073225604,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 21812.967551424834,
        "relative_gradient_delta": 140.55264073225607,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.22875973022019e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3244.477810407853,
        "filterflow_gradient_max_abs": 232.51294890916668,
        "gradient_delta": [
          3011.9648614986863,
          187.018798791387
        ],
        "gradient_explosion_ratio": 13.95396611513167,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3011.9648614986863,
        "relative_gradient_delta": 12.953966115131669,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.486573056463385e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1029.8929682019013,
        "filterflow_gradient_max_abs": 1518.8797828290087,
        "gradient_delta": [
          -488.9868146271074,
          297.9625778563908
        ],
        "gradient_explosion_ratio": 0.6780608839783627,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 488.9868146271074,
        "relative_gradient_delta": 0.3219391160216372,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.5804499627120094e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9293.495509041566,
        "filterflow_gradient_max_abs": 92.4227988005718,
        "gradient_delta": [
          9385.918307842137,
          -16.361109611162217
        ],
        "gradient_explosion_ratio": 100.55414496908818,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9385.918307842137,
        "relative_gradient_delta": 101.55414496908818,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.631609039686737e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 15575.867128537817,
        "filterflow_gradient_max_abs": 495.480272228227,
        "gradient_delta": [
          -15080.38685630959,
          1173.8227504772403
        ],
        "gradient_explosion_ratio": 31.435897656412234,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 15080.38685630959,
        "relative_gradient_delta": 30.43589765641223,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.181977596497745e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 22599.349386250396,
        "filterflow_gradient_max_abs": 1905.453488616431,
        "gradient_delta": [
          -24504.80287486683,
          1644.7990320702252
        ],
        "gradient_explosion_ratio": 11.860352153050984,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 24504.80287486683,
        "relative_gradient_delta": 12.860352153050984,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.158671794764814e-09,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 23660.404215859828,
        "filterflow_gradient_max_abs": 536.1521590308598,
        "gradient_delta": [
          -24196.556374890686,
          1775.3397901848912
        ],
        "gradient_explosion_ratio": 44.130017602890945,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 24196.556374890686,
        "relative_gradient_delta": 45.13001760289094,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.624389925491414e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1001.4592302010708,
        "filterflow_gradient_max_abs": 85.09097085867334,
        "gradient_delta": [
          -1086.550201059744,
          280.67333906234586
        ],
        "gradient_explosion_ratio": 11.769277281656398,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1086.550201059744,
        "relative_gradient_delta": 12.769277281656397,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.351314141284092e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9110.446610302024,
        "filterflow_gradient_max_abs": 286.3674760142073,
        "gradient_delta": [
          8824.079134287816,
          56.9898732897215
        ],
        "gradient_explosion_ratio": 31.81383143471934,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8824.079134287816,
        "relative_gradient_delta": 30.813831434719336,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.2123888255882775e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8383.773392155563,
        "filterflow_gradient_max_abs": 1646.6707953160178,
        "gradient_delta": [
          6737.102596839545,
          207.4167537924887
        ],
        "gradient_explosion_ratio": 5.091347594190256,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6737.102596839545,
        "relative_gradient_delta": 4.091347594190256,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.9354371134977555e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10609.559423779932,
        "filterflow_gradient_max_abs": 1706.2194857616348,
        "gradient_delta": [
          8903.339938018298,
          -136.46211789260155
        ],
        "gradient_explosion_ratio": 6.218168009635618,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8903.339938018298,
        "relative_gradient_delta": 5.218168009635618,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.4229368490487104e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2268.52188516782,
        "filterflow_gradient_max_abs": 491.76925290563014,
        "gradient_delta": [
          -2760.2911380734504,
          422.4444691684963
        ],
        "gradient_explosion_ratio": 4.61298031905046,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2760.2911380734504,
        "relative_gradient_delta": 5.61298031905046,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.928541213506833e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 810.8295942082866,
        "filterflow_gradient_max_abs": 953.0377691516383,
        "gradient_delta": [
          -1763.8673633599249,
          367.09674961054594
        ],
        "gradient_explosion_ratio": 0.8507843240358244,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1763.8673633599249,
        "relative_gradient_delta": 1.8507843240358244,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.896453103559907e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3930.0078873197845,
        "filterflow_gradient_max_abs": 1943.4208738111502,
        "gradient_delta": [
          1986.5870135086343,
          727.426714952718
        ],
        "gradient_explosion_ratio": 2.0222114212516575,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1986.5870135086343,
        "relative_gradient_delta": 1.0222114212516578,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.690761887919507e-09,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_with_clipped_upstream_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7025.174608954654,
        "filterflow_gradient_max_abs": 950.6655619127545,
        "gradient_delta": [
          6074.5090470419,
          713.4652966764394
        ],
        "gradient_explosion_ratio": 7.389743449652146,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6074.5090470419,
        "relative_gradient_delta": 6.389743449652147,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.408061719615944e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_with_clipped_upstream_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      543.3812985353517,
      732.7210862949149
    ],
    "final_bayesfilter_gradient_max_abs": 732.7210862949149,
    "final_filterflow_gradient_diag": [
      7019.871883303286,
      713.5990730344417
    ],
    "final_filterflow_gradient_max_abs": 7019.871883303286,
    "final_gradient_delta": [
      -6476.490584767935,
      19.12201326047318
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 6476.490584767935,
    "final_relative_gradient_delta": 0.9225938439378388,
    "final_scalar_delta": 7.407919611068792e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "status": "no_explosion"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 0.9938714034626872,
      "max_abs_gradient_delta": 0.054302284086629626,
      "relative_gradient_delta": 0.00612859653731278,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.8406609569865395e-11,
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
        "bayesfilter_gradient_max_abs": 0.008924445612040184,
        "filterflow_gradient_max_abs": 0.008924445612040184,
        "gradient_delta": [
          0.0,
          -5.795395272864551e-20
        ],
        "gradient_explosion_ratio": 0.008924445612040184,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 5.795395272864551e-20,
        "relative_gradient_delta": 5.795395272864551e-20,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.806173969492901,
        "filterflow_gradient_max_abs": 8.860476253579531,
        "gradient_delta": [
          0.054302284086629626,
          -0.031331175239548495
        ],
        "gradient_explosion_ratio": 0.9938714034626872,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.054302284086629626,
        "relative_gradient_delta": 0.00612859653731278,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8406609569865395e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.314937776787198,
        "filterflow_gradient_max_abs": 1.4056099396090884,
        "gradient_delta": [
          -6.720547716396286,
          -1.4439473860965477
        ],
        "gradient_explosion_ratio": 3.78123235117797,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.720547716396286,
        "relative_gradient_delta": 4.7812323511779695,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.5511147921642987e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10.212711285486696,
        "filterflow_gradient_max_abs": 14.864972477668916,
        "gradient_delta": [
          -11.606925132316723,
          10.212711285486696
        ],
        "gradient_explosion_ratio": 0.6870319673197421,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 11.606925132316723,
        "relative_gradient_delta": 0.7808238561997586,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.2442492308982764e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.094145793175583,
        "filterflow_gradient_max_abs": 15.00462728219541,
        "gradient_delta": [
          12.208146211053172,
          6.094145793175584
        ],
        "gradient_explosion_ratio": 0.40615109449649156,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 12.208146211053172,
        "relative_gradient_delta": 0.8136254224414784,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.779998453661392e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.219240845906949,
        "filterflow_gradient_max_abs": 6.525931066391355,
        "gradient_delta": [
          2.3235912536886243,
          4.219240845906949
        ],
        "gradient_explosion_ratio": 0.6465346941275713,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.219240845906949,
        "relative_gradient_delta": 0.6465346941275713,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.1093350116861984e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.645989892043312,
        "filterflow_gradient_max_abs": 2.686919378388484,
        "gradient_delta": [
          -6.5430389440698615,
          4.645989892043312
        ],
        "gradient_explosion_ratio": 1.7291139918123657,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.5430389440698615,
        "relative_gradient_delta": 2.4351452435443512,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4224179873708636e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.071539159219872,
        "filterflow_gradient_max_abs": 24.973165642495765,
        "gradient_delta": [
          17.90162648327589,
          1.300336719014506
        ],
        "gradient_explosion_ratio": 0.28316550894879494,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 17.90162648327589,
        "relative_gradient_delta": 0.716834491051205,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.5496940376542625e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.16004939315663,
        "filterflow_gradient_max_abs": 0.7972582915878877,
        "gradient_delta": [
          -6.362791101568742,
          1.349497169736036
        ],
        "gradient_explosion_ratio": 7.16004939315663,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.362791101568742,
        "relative_gradient_delta": 6.362791101568742,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.66524613279762e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.370028156849783,
        "filterflow_gradient_max_abs": 49.77299487676166,
        "gradient_delta": [
          -52.988133271608724,
          5.3700281568497825
        ],
        "gradient_explosion_ratio": 0.1078903965924899,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 52.988133271608724,
        "relative_gradient_delta": 1.0645960405398103,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.581402089977928e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13.553337244844354,
        "filterflow_gradient_max_abs": 91.01474473671405,
        "gradient_delta": [
          -85.15139954993194,
          13.553337244844354
        ],
        "gradient_explosion_ratio": 0.14891364343273417,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 85.15139954993194,
        "relative_gradient_delta": 0.9355780735995745,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.424994118489849e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10.698702340289287,
        "filterflow_gradient_max_abs": 28.00263902728941,
        "gradient_delta": [
          30.66057423544933,
          10.698702340289287
        ],
        "gradient_explosion_ratio": 0.38206050257845636,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 30.66057423544933,
        "relative_gradient_delta": 1.0949173113851765,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.85451720225683e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 14.833325795245468,
        "filterflow_gradient_max_abs": 40.13671871067378,
        "gradient_delta": [
          -34.16258201792412,
          14.83332579524547
        ],
        "gradient_explosion_ratio": 0.3695699666475416,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 34.16258201792412,
        "relative_gradient_delta": 0.8511553289691087,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3077183780296764e-10,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 19.013093768069297,
        "filterflow_gradient_max_abs": 49.010874255508995,
        "gradient_delta": [
          -38.88098748737118,
          19.013093768069297
        ],
        "gradient_explosion_ratio": 0.38793622959974355,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 38.88098748737118,
        "relative_gradient_delta": 0.7933134855883706,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4137313542050833e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 20.94976759318094,
        "filterflow_gradient_max_abs": 21.29035436921441,
        "gradient_delta": [
          -9.489514048634799,
          20.94976759318094
        ],
        "gradient_explosion_ratio": 0.9840027662232831,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 20.94976759318094,
        "relative_gradient_delta": 0.9840027662232831,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3353940175875323e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 18.8462261204084,
        "filterflow_gradient_max_abs": 27.042811971633515,
        "gradient_delta": [
          36.87789450732264,
          18.8462261204084
        ],
        "gradient_explosion_ratio": 0.6969033449693434,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 36.87789450732264,
        "relative_gradient_delta": 1.3636856457829016,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.525606307950511e-10,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 17.559078270217867,
        "filterflow_gradient_max_abs": 18.468136147749064,
        "gradient_delta": [
          27.139783413016254,
          17.559078270217867
        ],
        "gradient_explosion_ratio": 0.9507769560361404,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 27.139783413016254,
        "relative_gradient_delta": 1.469546422870838,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7488588355263346e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 24.068692086239,
        "filterflow_gradient_max_abs": 102.94637935328883,
        "gradient_delta": [
          -88.62431438200738,
          24.068692086239
        ],
        "gradient_explosion_ratio": 0.23379833499185687,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 88.62431438200738,
        "relative_gradient_delta": 0.8608784003745159,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3816503496855148e-10,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 31.38729635864174,
        "filterflow_gradient_max_abs": 113.77902775418237,
        "gradient_delta": [
          -92.30991955680057,
          31.38729635864174
        ],
        "gradient_explosion_ratio": 0.2758618787502162,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 92.30991955680057,
        "relative_gradient_delta": 0.8113087392189232,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.3455015707440907e-10,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 19.341138945500482,
        "filterflow_gradient_max_abs": 165.42250820864194,
        "gradient_delta": [
          175.99173780620836,
          19.341138945500482
        ],
        "gradient_explosion_ratio": 0.11691963297465024,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 175.99173780620836,
        "relative_gradient_delta": 1.0638923306871626,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.92866184029117e-10,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 24.189777887715373,
        "filterflow_gradient_max_abs": 73.77440324184383,
        "gradient_delta": [
          -59.71342447296984,
          24.189777887715373
        ],
        "gradient_explosion_ratio": 0.32788849282070864,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 59.71342447296984,
        "relative_gradient_delta": 0.8094057267697586,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4417447497835383e-10,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 35.136960569293514,
        "filterflow_gradient_max_abs": 217.86217342911775,
        "gradient_delta": [
          -192.9753137592895,
          35.136960569293514
        ],
        "gradient_explosion_ratio": 0.16128068501403,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 192.9753137592895,
        "relative_gradient_delta": 0.8857678720536345,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.974509693056461e-10,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 45.10685864071033,
        "filterflow_gradient_max_abs": 165.63087578642663,
        "gradient_delta": [
          -131.25454724330342,
          45.10685864071033
        ],
        "gradient_explosion_ratio": 0.27233363602371785,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 131.25454724330342,
        "relative_gradient_delta": 0.7924521718556273,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.2155079427175224e-10,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 43.8157539674544,
        "filterflow_gradient_max_abs": 20.952482372929534,
        "gradient_delta": [
          54.0938502252219,
          43.8157539674544
        ],
        "gradient_explosion_ratio": 2.091196316865254,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 54.0938502252219,
        "relative_gradient_delta": 2.5817394455900264,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.807603204426414e-10,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 41.02908974761212,
        "filterflow_gradient_max_abs": 45.60764934214221,
        "gradient_delta": [
          76.32111235638584,
          41.02908974761212
        ],
        "gradient_explosion_ratio": 0.8996098316713853,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 76.32111235638584,
        "relative_gradient_delta": 1.6734278889016079,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.035900585426134e-10,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 35.66539001644361,
        "filterflow_gradient_max_abs": 95.80515251122853,
        "gradient_delta": [
          122.01212961267336,
          35.66539001644361
        ],
        "gradient_explosion_ratio": 0.3722700614903104,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 122.01212961267336,
        "relative_gradient_delta": 1.2735445476001235,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.194777941142092e-10,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 43.64474121016264,
        "filterflow_gradient_max_abs": 162.31717661541148,
        "gradient_delta": [
          -129.80015089339693,
          43.64474121016264
        ],
        "gradient_explosion_ratio": 0.26888553707148893,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 129.80015089339693,
        "relative_gradient_delta": 0.7996698414791971,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.324789415477426e-10,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 40.66292757919069,
        "filterflow_gradient_max_abs": 65.61469672303252,
        "gradient_delta": [
          95.4109613857377,
          40.66292757919069
        ],
        "gradient_explosion_ratio": 0.6197228610357489,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 95.4109613857377,
        "relative_gradient_delta": 1.4541096149309167,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.852775876111991e-10,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 57.335899042459104,
        "filterflow_gradient_max_abs": 353.91086072731014,
        "gradient_delta": [
          -311.2493005403259,
          57.335899042459104
        ],
        "gradient_explosion_ratio": 0.16200661071725816,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 311.2493005403259,
        "relative_gradient_delta": 0.8794567646234086,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.191615860487218e-10,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 62.527365982766206,
        "filterflow_gradient_max_abs": 106.57513689011893,
        "gradient_delta": [
          -59.156083898752996,
          62.527365982766206
        ],
        "gradient_explosion_ratio": 0.586697496314109,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 62.527365982766206,
        "relative_gradient_delta": 0.586697496314109,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.87274212698685e-10,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 77.58762745707347,
        "filterflow_gradient_max_abs": 301.25080522517993,
        "gradient_delta": [
          -241.577547334087,
          77.58762745707347
        ],
        "gradient_explosion_ratio": 0.25755160189224396,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 241.577547334087,
        "relative_gradient_delta": 0.8019150260976459,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.1155345797960763e-10,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 57.29274567624318,
        "filterflow_gradient_max_abs": 406.1376803574301,
        "gradient_delta": [
          447.5330816797905,
          57.29274567624318
        ],
        "gradient_explosion_ratio": 0.14106729921198516,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 447.5330816797905,
        "relative_gradient_delta": 1.1019245524964083,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.641514005423232e-10,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 68.370949880001,
        "filterflow_gradient_max_abs": 226.31263344208014,
        "gradient_delta": [
          -177.3520994432785,
          68.370949880001
        ],
        "gradient_explosion_ratio": 0.30210841012328676,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 177.3520994432785,
        "relative_gradient_delta": 0.7836597398291861,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.090381697911653e-10,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 68.71217020357992,
        "filterflow_gradient_max_abs": 6.85443174851973,
        "gradient_delta": [
          42.32465697895238,
          68.71217020357992
        ],
        "gradient_explosion_ratio": 10.024488203331934,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 68.71217020357992,
        "relative_gradient_delta": 10.024488203331934,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.083187369971711e-10,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 72.4775899074066,
        "filterflow_gradient_max_abs": 80.80287856491722,
        "gradient_delta": [
          -28.936694213949785,
          72.4775899074066
        ],
        "gradient_explosion_ratio": 0.8969679198888679,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 72.4775899074066,
        "relative_gradient_delta": 0.8969679198888679,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.413411940935475e-10,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 80.35151254948109,
        "filterflow_gradient_max_abs": 195.04750763879625,
        "gradient_delta": [
          -136.7617096767103,
          80.35151254948109
        ],
        "gradient_explosion_ratio": 0.4119586736698123,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 136.7617096767103,
        "relative_gradient_delta": 0.7011712753078393,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.915747808809101e-10,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 89.62061860945914,
        "filterflow_gradient_max_abs": 227.99933783381496,
        "gradient_delta": [
          -162.17072878999085,
          89.62061860945914
        ],
        "gradient_explosion_ratio": 0.39307403021837795,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 162.17072878999085,
        "relative_gradient_delta": 0.7112771919898928,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4428105638871784e-10,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 68.75806857550877,
        "filterflow_gradient_max_abs": 498.30983956509795,
        "gradient_delta": [
          547.0689927981526,
          68.75806857550877
        ],
        "gradient_explosion_ratio": 0.13798256248666024,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 547.0689927981526,
        "relative_gradient_delta": 1.0978490677117865,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.725002776875044e-10,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 54.59505701429374,
        "filterflow_gradient_max_abs": 348.59095258355785,
        "gradient_delta": [
          387.9688635243901,
          54.59505701429374
        ],
        "gradient_explosion_ratio": 0.156616391245,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 387.9688635243901,
        "relative_gradient_delta": 1.1129630894003002,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.749836080009118e-10,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 55.39516349085981,
        "filterflow_gradient_max_abs": 24.53415070247347,
        "gradient_delta": [
          15.339101366653129,
          55.39516349085981
        ],
        "gradient_explosion_ratio": 2.2578798085427514,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 55.39516349085981,
        "relative_gradient_delta": 2.2578798085427514,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9053560385582387e-10,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 76.64923713925091,
        "filterflow_gradient_max_abs": 743.4955982984612,
        "gradient_delta": [
          -688.0610669667869,
          76.64923713925091
        ],
        "gradient_explosion_ratio": 0.10309306109500548,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 688.0610669667869,
        "relative_gradient_delta": 0.925440673141119,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3861267689208034e-10,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 56.34514164214734,
        "filterflow_gradient_max_abs": 660.4154280128698,
        "gradient_delta": [
          697.9632349101832,
          56.34514164214734
        ],
        "gradient_explosion_ratio": 0.08531772465050486,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 697.9632349101832,
        "relative_gradient_delta": 1.056854830012514,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2236966995260445e-10,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 61.74651196590116,
        "filterflow_gradient_max_abs": 151.38043625809377,
        "gradient_delta": [
          -110.87764268361752,
          61.74651196590116
        ],
        "gradient_explosion_ratio": 0.40788964209765777,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 110.87764268361752,
        "relative_gradient_delta": 0.732443672540211,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.503508428868372e-10,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 63.73045520389371,
        "filterflow_gradient_max_abs": 78.34314644911912,
        "gradient_delta": [
          -36.24519874722415,
          63.73045520389371
        ],
        "gradient_explosion_ratio": 0.8134783716567244,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 63.73045520389371,
        "relative_gradient_delta": 0.8134783716567244,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4379963886312908e-10,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 75.24633877873818,
        "filterflow_gradient_max_abs": 375.1405380302191,
        "gradient_delta": [
          -325.2149197984535,
          75.24633877873818
        ],
        "gradient_explosion_ratio": 0.20058173177934926,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 325.2149197984535,
        "relative_gradient_delta": 0.8669148940983181,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.290931888637715e-10,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 80.87492897165504,
        "filterflow_gradient_max_abs": 190.9613749711765,
        "gradient_delta": [
          -136.62038953976372,
          80.87492897165504
        ],
        "gradient_explosion_ratio": 0.42351459285346166,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 136.62038953976372,
        "relative_gradient_delta": 0.7154346765694636,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.651177055668086e-10,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 59.040349052429164,
        "filterflow_gradient_max_abs": 677.2028181986615,
        "gradient_delta": [
          715.8122620874484,
          59.040349052429164
        ],
        "gradient_explosion_ratio": 0.08718266886347972,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 715.8122620874484,
        "relative_gradient_delta": 1.057013117564228,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.92969196177728e-10,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 54.473560239370954,
        "filterflow_gradient_max_abs": 152.6174741556563,
        "gradient_delta": [
          188.57329843912194,
          54.473560239370954
        ],
        "gradient_explosion_ratio": 0.356928723534061,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 188.57329843912194,
        "relative_gradient_delta": 1.235594413302856,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.625100468227174e-11,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 59.36399955374341,
        "filterflow_gradient_max_abs": 207.0601214499801,
        "gradient_delta": [
          -167.86179890134008,
          59.36399955374341
        ],
        "gradient_explosion_ratio": 0.2866993370719339,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 167.86179890134008,
        "relative_gradient_delta": 0.8106911061669148,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.438458406890277e-10,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 45.67726432813721,
        "filterflow_gradient_max_abs": 546.4746634801378,
        "gradient_delta": [
          576.4662033828239,
          45.67726432813721
        ],
        "gradient_explosion_ratio": 0.08358532861752227,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 576.4662033828239,
        "relative_gradient_delta": 1.0548818488888208,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.842170943040401e-14,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 39.07163393656562,
        "filterflow_gradient_max_abs": 272.67443106070385,
        "gradient_delta": [
          299.47684910389154,
          39.07163393656562
        ],
        "gradient_explosion_ratio": 0.14329042068439243,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 299.47684910389154,
        "relative_gradient_delta": 1.0982945776724509,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.5509905299259117e-10,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 55.928384909046585,
        "filterflow_gradient_max_abs": 949.676068984666,
        "gradient_delta": [
          -914.3284731778193,
          55.928384909046585
        ],
        "gradient_explosion_ratio": 0.0588920651321052,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 914.3284731778193,
        "relative_gradient_delta": 0.9627793129033586,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.264737647943548e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 53.90541826215319,
        "filterflow_gradient_max_abs": 101.55125271438094,
        "gradient_delta": [
          135.16571552953232,
          53.90541826215319
        ],
        "gradient_explosion_ratio": 0.5308198256673943,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 135.16571552953232,
        "relative_gradient_delta": 1.331009829191316,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.427679308108054e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 49.222077526462456,
        "filterflow_gradient_max_abs": 177.86655077673558,
        "gradient_delta": [
          208.84185633607265,
          49.222077526462456
        ],
        "gradient_explosion_ratio": 0.27673599848600966,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 208.84185633607265,
        "relative_gradient_delta": 1.1741491327293931,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3662173614648054e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 52.14858037379463,
        "filterflow_gradient_max_abs": 135.59093315487942,
        "gradient_delta": [
          -102.89996089174403,
          52.14858037379463
        ],
        "gradient_explosion_ratio": 0.3846022677211584,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 102.89996089174403,
        "relative_gradient_delta": 0.758900012688946,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.345853206657921e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 55.11274796233903,
        "filterflow_gradient_max_abs": 133.34005587444113,
        "gradient_delta": [
          -98.83769367856635,
          55.11274796233903
        ],
        "gradient_explosion_ratio": 0.41332477027185005,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 98.83769367856635,
        "relative_gradient_delta": 0.7412453296977487,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4315730823000195e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 66.60283722274795,
        "filterflow_gradient_max_abs": 522.1712070050679,
        "gradient_delta": [
          -480.4230944328384,
          66.60283722274795
        ],
        "gradient_explosion_ratio": 0.1275498080500282,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 480.4230944328384,
        "relative_gradient_delta": 0.9200489954019538,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3040164503763663e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 66.54373252019431,
        "filterflow_gradient_max_abs": 6.415333698704999,
        "gradient_delta": [
          48.04240290845946,
          66.54373252019431
        ],
        "gradient_explosion_ratio": 10.372606577523293,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 66.54373252019431,
        "relative_gradient_delta": 10.372606577523293,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1294503110548249e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 61.22464844452993,
        "filterflow_gradient_max_abs": 197.4197643907813,
        "gradient_delta": [
          235.6699489924378,
          61.22464844452993
        ],
        "gradient_explosion_ratio": 0.3101242098705943,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 235.6699489924378,
        "relative_gradient_delta": 1.1937505331327538,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0837482022907352e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 68.6289488932409,
        "filterflow_gradient_max_abs": 315.57269054843385,
        "gradient_delta": [
          -272.85726600963403,
          68.6289488932409
        ],
        "gradient_explosion_ratio": 0.2174742965684725,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 272.85726600963403,
        "relative_gradient_delta": 0.8646415681136265,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1401937172195176e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 70.35613612302491,
        "filterflow_gradient_max_abs": 60.009881084342744,
        "gradient_delta": [
          -16.257767691581115,
          70.35613612302491
        ],
        "gradient_explosion_ratio": 1.1724091908154375,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 70.35613612302491,
        "relative_gradient_delta": 1.1724091908154375,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1782930187109741e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 74.13508228935662,
        "filterflow_gradient_max_abs": 147.6346164990015,
        "gradient_delta": [
          -101.5196648744253,
          74.13508228935662
        ],
        "gradient_explosion_ratio": 0.5021524358405335,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 101.5196648744253,
        "relative_gradient_delta": 0.6876413356288422,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2933298876305344e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 87.0651200352431,
        "filterflow_gradient_max_abs": 512.611395216775,
        "gradient_delta": [
          -457.54004356890005,
          87.0651200352431
        ],
        "gradient_explosion_ratio": 0.16984624385578606,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 457.54004356890005,
        "relative_gradient_delta": 0.8925670553527469,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.554774583695689e-10,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 84.8051699302292,
        "filterflow_gradient_max_abs": 87.5818933878043,
        "gradient_delta": [
          140.7823371669994,
          84.8051699302292
        ],
        "gradient_explosion_ratio": 0.9682956904656076,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 140.7823371669994,
        "relative_gradient_delta": 1.6074365570475693,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0234515457341331e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 83.42925985079768,
        "filterflow_gradient_max_abs": 57.78168821303872,
        "gradient_delta": [
          109.94487447628909,
          83.42925985079768
        ],
        "gradient_explosion_ratio": 1.4438702369373047,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 109.94487447628909,
        "relative_gradient_delta": 1.9027632780635768,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.412825991399586e-10,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 102.17139966646559,
        "filterflow_gradient_max_abs": 738.8517276846384,
        "gradient_delta": [
          -673.2868850065388,
          102.17139966646559
        ],
        "gradient_explosion_ratio": 0.1382840370241038,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 673.2868850065388,
        "relative_gradient_delta": 0.9112611634765178,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1248317832723842e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 131.10016779218316,
        "filterflow_gradient_max_abs": 1019.3972961264672,
        "gradient_delta": [
          -930.4635790748016,
          131.10016779218316
        ],
        "gradient_explosion_ratio": 0.12860556751557126,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 930.4635790748016,
        "relative_gradient_delta": 0.912758531546436,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.905196414663806e-10,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 127.12977897234259,
        "filterflow_gradient_max_abs": 122.24440141690243,
        "gradient_delta": [
          207.81926545052448,
          127.12977897234259
        ],
        "gradient_explosion_ratio": 1.0399640187919859,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 207.81926545052448,
        "relative_gradient_delta": 1.7000309465443528,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.500755489469157e-10,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 150.73690373220657,
        "filterflow_gradient_max_abs": 682.5428603420182,
        "gradient_delta": [
          -580.336653327167,
          150.73690373220657
        ],
        "gradient_explosion_ratio": 0.22084606328849912,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 580.336653327167,
        "relative_gradient_delta": 0.8502567194628096,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.193943136167945e-10,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 161.132889304879,
        "filterflow_gradient_max_abs": 309.19172560146353,
        "gradient_delta": [
          -198.29563086493346,
          161.132889304879
        ],
        "gradient_explosion_ratio": 0.521142307386884,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 198.29563086493346,
        "relative_gradient_delta": 0.6413355030093174,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.828742016296019e-10,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 163.72124761464272,
        "filterflow_gradient_max_abs": 66.90489544481636,
        "gradient_delta": [
          45.83475138179453,
          163.72124761464272
        ],
        "gradient_explosion_ratio": 2.447074261549085,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 163.72124761464272,
        "relative_gradient_delta": 2.447074261549085,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.207851927480078e-10,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 190.23951319672761,
        "filterflow_gradient_max_abs": 750.3754788438333,
        "gradient_delta": [
          -617.1931974244158,
          190.23951319672761
        ],
        "gradient_explosion_ratio": 0.253525759516883,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 617.1931974244158,
        "relative_gradient_delta": 0.8225124818515889,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.709637207473861e-10,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 177.5032573858143,
        "filterflow_gradient_max_abs": 347.8401730350442,
        "gradient_delta": [
          470.69738894441366,
          177.5032573858143
        ],
        "gradient_explosion_ratio": 0.5103011990737804,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 470.69738894441366,
        "relative_gradient_delta": 1.353200192023225,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.423448439818458e-10,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 194.18231951298122,
        "filterflow_gradient_max_abs": 441.50385013274905,
        "gradient_delta": [
          -306.7988190662768,
          194.18231951298122
        ],
        "gradient_explosion_ratio": 0.4398202177729492,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 306.7988190662768,
        "relative_gradient_delta": 0.6948950025555386,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.418084007644211e-10,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 201.80979357925358,
        "filterflow_gradient_max_abs": 216.5606746935064,
        "gradient_delta": [
          -75.8852029875342,
          201.80979357925358
        ],
        "gradient_explosion_ratio": 0.9318856891486442,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 201.80979357925358,
        "relative_gradient_delta": 0.9318856891486442,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.252687505068025e-10,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 222.9809223291022,
        "filterflow_gradient_max_abs": 592.4376179231792,
        "gradient_delta": [
          -435.8831269253868,
          222.9809223291022
        ],
        "gradient_explosion_ratio": 0.3763787369052853,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 435.8831269253868,
        "relative_gradient_delta": 0.7357451885877836,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.707559118192876e-10,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 258.20840473700025,
        "filterflow_gradient_max_abs": 1021.9536107722753,
        "gradient_delta": [
          -836.7160257467751,
          258.20840473700025
        ],
        "gradient_explosion_ratio": 0.25266157095122543,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 836.7160257467751,
        "relative_gradient_delta": 0.818741689375197,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.629843589209486e-10,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 273.78589991220576,
        "filterflow_gradient_max_abs": 416.36976112409496,
        "gradient_delta": [
          -218.5252447065646,
          273.78589991220576
        ],
        "gradient_explosion_ratio": 0.6575547157244365,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 273.78589991220576,
        "relative_gradient_delta": 0.6575547157244365,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.8334494446608e-10,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 271.0983543281826,
        "filterflow_gradient_max_abs": 73.20765898029507,
        "gradient_delta": [
          268.8359972503755,
          271.0983543281826
        ],
        "gradient_explosion_ratio": 3.703141967716148,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 271.0983543281826,
        "relative_gradient_delta": 3.703141967716148,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.958771336940117e-10,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 271.8846052101976,
        "filterflow_gradient_max_abs": 18.775557058598526,
        "gradient_delta": [
          177.3461480200049,
          271.8846052101976
        ],
        "gradient_explosion_ratio": 14.48077435794025,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 271.8846052101976,
        "relative_gradient_delta": 14.48077435794025,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.100187187665142e-10,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 289.0920080889533,
        "filterflow_gradient_max_abs": 489.4717191114149,
        "gradient_delta": [
          -280.3669556707946,
          289.0920080889533
        ],
        "gradient_explosion_ratio": 0.5906204522168713,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 289.0920080889533,
        "relative_gradient_delta": 0.5906204522168713,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.418758857762441e-10,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 310.13018150799564,
        "filterflow_gradient_max_abs": 603.1903641588457,
        "gradient_delta": [
          -377.80211853781316,
          310.13018150799564
        ],
        "gradient_explosion_ratio": 0.5141497608975816,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 377.80211853781316,
        "relative_gradient_delta": 0.6263397776001637,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0115144277733634e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 342.30211329160954,
        "filterflow_gradient_max_abs": 924.7685421225882,
        "gradient_delta": [
          -674.3432792301655,
          342.30211329160954
        ],
        "gradient_explosion_ratio": 0.37014895911785206,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 674.3432792301655,
        "relative_gradient_delta": 0.7292022257616695,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2003482652289676e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 316.9160091943521,
        "filterflow_gradient_max_abs": 712.4012104561216,
        "gradient_delta": [
          942.855720204196,
          316.9160091943521
        ],
        "gradient_explosion_ratio": 0.44485607905051655,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 942.855720204196,
        "relative_gradient_delta": 1.323489778464194,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.9136194850943866e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 358.1245407057877,
        "filterflow_gradient_max_abs": 1186.5395908091443,
        "gradient_delta": [
          -927.2755548861325,
          358.1245407057877
        ],
        "gradient_explosion_ratio": 0.30182266439299305,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 927.2755548861325,
        "relative_gradient_delta": 0.7814956720102274,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.708955086447531e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 353.0468086465371,
        "filterflow_gradient_max_abs": 155.19429188795652,
        "gradient_delta": [
          410.23999908881126,
          353.0468086465371
        ],
        "gradient_explosion_ratio": 2.2748698057878407,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 410.23999908881126,
        "relative_gradient_delta": 2.6433961848608876,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.22875973022019e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 361.2219171895822,
        "filterflow_gradient_max_abs": 232.51294890916668,
        "gradient_delta": [
          28.300125879987576,
          361.2219171895822
        ],
        "gradient_explosion_ratio": 1.5535561304617784,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 361.2219171895822,
        "relative_gradient_delta": 1.5535561304617784,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.486573056463385e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 409.92378082180574,
        "filterflow_gradient_max_abs": 1518.8797828290087,
        "gradient_delta": [
          -1220.9699767592351,
          409.92378082180574
        ],
        "gradient_explosion_ratio": 0.2698855995425109,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1220.9699767592351,
        "relative_gradient_delta": 0.8038621558877438,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.5804499627120094e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 406.91685125960294,
        "filterflow_gradient_max_abs": 92.4227988005718,
        "gradient_delta": [
          387.87271302386176,
          406.91685125960294
        ],
        "gradient_explosion_ratio": 4.402775684575843,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 406.91685125960294,
        "relative_gradient_delta": 4.402775684575843,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.631609039686737e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 389.8362688181594,
        "filterflow_gradient_max_abs": 495.480272228227,
        "gradient_delta": [
          778.6670162894665,
          389.8362688181594
        ],
        "gradient_explosion_ratio": 0.7867846424339452,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 778.6670162894665,
        "relative_gradient_delta": 1.5715398976183628,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.181977596497745e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 449.9201747493603,
        "filterflow_gradient_max_abs": 1905.453488616431,
        "gradient_delta": [
          -1579.028037589394,
          449.9201747493603
        ],
        "gradient_explosion_ratio": 0.2361223600771551,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1579.028037589394,
        "relative_gradient_delta": 0.828688838128472,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.158671794764814e-09,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 467.0146322938016,
        "filterflow_gradient_max_abs": 536.1521590308598,
        "gradient_delta": [
          -195.88017324900795,
          467.0146322938016
        ],
        "gradient_explosion_ratio": 0.8710486835266501,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 467.0146322938016,
        "relative_gradient_delta": 0.8710486835266501,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.624389925491414e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 469.998815338338,
        "filterflow_gradient_max_abs": 85.09097085867334,
        "gradient_delta": [
          257.29668530593017,
          469.998815338338
        ],
        "gradient_explosion_ratio": 5.523486341681937,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 469.998815338338,
        "relative_gradient_delta": 5.523486341681937,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.351314141284092e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 479.4430974083069,
        "filterflow_gradient_max_abs": 286.3674760142073,
        "gradient_delta": [
          62.913335990623125,
          479.4430974083069
        ],
        "gradient_explosion_ratio": 1.6742232884872748,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 479.4430974083069,
        "relative_gradient_delta": 1.6742232884872748,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.2123888255882775e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 531.4569025416237,
        "filterflow_gradient_max_abs": 1646.6707953160178,
        "gradient_delta": [
          -1258.9103981229714,
          531.4569025416237
        ],
        "gradient_explosion_ratio": 0.3227462975923066,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1258.9103981229714,
        "relative_gradient_delta": 0.7645185678302929,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.9354371134977555e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 585.69642891066,
        "filterflow_gradient_max_abs": 1706.2194857616348,
        "gradient_delta": [
          -1275.717418260669,
          585.69642891066
        ],
        "gradient_explosion_ratio": 0.34327144532006826,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1275.717418260669,
        "relative_gradient_delta": 0.7476865836467721,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.4229368490487104e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 602.4664824157647,
        "filterflow_gradient_max_abs": 491.76925290563014,
        "gradient_delta": [
          -48.41465981817686,
          602.4664824157647
        ],
        "gradient_explosion_ratio": 1.2250999403807323,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 602.4664824157647,
        "relative_gradient_delta": 1.2250999403807323,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.928541213506833e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 635.0470664872132,
        "filterflow_gradient_max_abs": 953.0377691516383,
        "gradient_delta": [
          -485.49280849771355,
          635.0470664872132
        ],
        "gradient_explosion_ratio": 0.666339873447524,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 635.0470664872132,
        "relative_gradient_delta": 0.666339873447524,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.896453103559907e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 700.0079952008275,
        "filterflow_gradient_max_abs": 1943.4208738111502,
        "gradient_delta": [
          -1425.752117475014,
          700.0079952008275
        ],
        "gradient_explosion_ratio": 0.3601937205851222,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1425.752117475014,
        "relative_gradient_delta": 0.7336301347216877,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.690761887919507e-09,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_transport_matrix_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 732.7210862949149,
        "filterflow_gradient_max_abs": 950.6655619127545,
        "gradient_delta": [
          -407.2842633774028,
          732.7210862949149
        ],
        "gradient_explosion_ratio": 0.7707453763452504,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 732.7210862949149,
        "relative_gradient_delta": 0.7707453763452504,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.408061719615944e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_transport_matrix_stop_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      22174.945679855195,
      2.3092638912203256e-14
    ],
    "final_bayesfilter_gradient_max_abs": 22174.945679855195,
    "final_filterflow_gradient_diag": [
      7019.871883303286,
      713.5990730344417
    ],
    "final_filterflow_gradient_max_abs": 7019.871883303286,
    "final_gradient_delta": [
      15155.073796551907,
      -713.5990730344417
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 15155.073796551907,
    "final_relative_gradient_delta": 2.158881821276274,
    "final_scalar_delta": 7.407919611068792e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "status": "no_explosion"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 0.9989927803684195,
      "max_abs_gradient_delta": 0.008924445627757294,
      "relative_gradient_delta": 0.001007219631580404,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.8406609569865395e-11,
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
        "bayesfilter_gradient_max_abs": 0.008924445612040184,
        "filterflow_gradient_max_abs": 0.008924445612040184,
        "gradient_delta": [
          0.0,
          -5.795395272864551e-20
        ],
        "gradient_explosion_ratio": 0.008924445612040184,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 5.795395272864551e-20,
        "relative_gradient_delta": 5.795395272864551e-20,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.851551807951774,
        "filterflow_gradient_max_abs": 8.860476253579531,
        "gradient_delta": [
          0.008924445627757294,
          -2.3210746969482462e-17
        ],
        "gradient_explosion_ratio": 0.9989927803684195,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.008924445627757294,
        "relative_gradient_delta": 0.001007219631580404,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8406609569865395e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.44594186834015,
        "filterflow_gradient_max_abs": 1.4056099396090884,
        "gradient_delta": [
          -8.851551807949239,
          1.0423572610936313e-16
        ],
        "gradient_explosion_ratio": 5.297303084247488,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.851551807949239,
        "relative_gradient_delta": 6.297303084247488,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.5511147921642987e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.419030609289096,
        "filterflow_gradient_max_abs": 14.864972477668916,
        "gradient_delta": [
          -7.44594186837982,
          1.605818523089732e-16
        ],
        "gradient_explosion_ratio": 0.49909480965635317,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.44594186837982,
        "relative_gradient_delta": 0.5009051903436469,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.2442492308982764e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.585596672726346,
        "filterflow_gradient_max_abs": 15.00462728219541,
        "gradient_delta": [
          7.419030609469063,
          9.62999243333739e-16
        ],
        "gradient_explosion_ratio": 0.5055504898630482,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.419030609469063,
        "relative_gradient_delta": 0.4944495101369518,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.779998453661392e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 14.11152773947067,
        "filterflow_gradient_max_abs": 6.525931066391355,
        "gradient_delta": [
          -7.585596673079316,
          -7.68770318979113e-17
        ],
        "gradient_explosion_ratio": 2.1623776892381312,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.585596673079316,
        "relative_gradient_delta": 1.1623776892381312,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.1093350116861984e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 11.424608360850055,
        "filterflow_gradient_max_abs": 2.686919378388484,
        "gradient_delta": [
          -14.11152773923854,
          -4.1240030435109337e-16
        ],
        "gradient_explosion_ratio": 4.251935675011625,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 14.11152773923854,
        "relative_gradient_delta": 5.251935675011625,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4224179873708636e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 36.39777400333314,
        "filterflow_gradient_max_abs": 24.973165642495765,
        "gradient_delta": [
          -11.424608360837375,
          7.228210241648882e-16
        ],
        "gradient_explosion_ratio": 1.4574753767458544,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 11.424608360837375,
        "relative_gradient_delta": 0.4574753767458543,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.5496940376542625e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 37.19503229501251,
        "filterflow_gradient_max_abs": 0.7972582915878877,
        "gradient_delta": [
          -36.39777400342462,
          1.5620946960815544e-15
        ],
        "gradient_explosion_ratio": 37.19503229501251,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 36.39777400342462,
        "relative_gradient_delta": 36.39777400342462,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.66524613279762e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 12.577962581112835,
        "filterflow_gradient_max_abs": 49.77299487676166,
        "gradient_delta": [
          -37.19503229564882,
          7.640493386485329e-16
        ],
        "gradient_explosion_ratio": 0.2527065653223394,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 37.19503229564882,
        "relative_gradient_delta": 0.7472934346776605,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.581402089977928e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 103.59270731588516,
        "filterflow_gradient_max_abs": 91.01474473671405,
        "gradient_delta": [
          12.577962579171114,
          5.908470856308452e-16
        ],
        "gradient_explosion_ratio": 1.1381969769355111,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 12.577962579171114,
        "relative_gradient_delta": 0.13819697693551122,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.424994118489849e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 75.59006829251159,
        "filterflow_gradient_max_abs": 28.00263902728941,
        "gradient_delta": [
          103.592707319801,
          1.0011561224586355e-15
        ],
        "gradient_explosion_ratio": 2.699390875940186,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 103.592707319801,
        "relative_gradient_delta": 3.699390875940186,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.85451720225683e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 115.72678700230485,
        "filterflow_gradient_max_abs": 40.13671871067378,
        "gradient_delta": [
          75.59006829163107,
          9.26066579874666e-16
        ],
        "gradient_explosion_ratio": 2.8833145986976003,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 75.59006829163107,
        "relative_gradient_delta": 1.8833145986976005,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3077183780296764e-10,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 164.7376612572329,
        "filterflow_gradient_max_abs": 49.010874255508995,
        "gradient_delta": [
          115.7267870017239,
          8.862290202782064e-16
        ],
        "gradient_explosion_ratio": 3.3612471468761,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 115.7267870017239,
        "relative_gradient_delta": 2.3612471468761,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4137313542050833e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 186.028015627166,
        "filterflow_gradient_max_abs": 21.29035436921441,
        "gradient_delta": [
          164.7376612579516,
          9.436251236241856e-16
        ],
        "gradient_explosion_ratio": 8.737666475676903,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 164.7376612579516,
        "relative_gradient_delta": 7.737666475676902,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3353940175875323e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 158.98520365560321,
        "filterflow_gradient_max_abs": 27.042811971633515,
        "gradient_delta": [
          186.02801562723673,
          1.0640323730794625e-15
        ],
        "gradient_explosion_ratio": 5.879018935692424,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 186.02801562723673,
        "relative_gradient_delta": 6.879018935692424,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.525606307950511e-10,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 140.51706750563707,
        "filterflow_gradient_max_abs": 18.468136147749064,
        "gradient_delta": [
          158.98520365338612,
          4.359991774786871e-16
        ],
        "gradient_explosion_ratio": 7.608622027770983,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 158.98520365338612,
        "relative_gradient_delta": 8.608622027770982,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7488588355263346e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 243.46344687016102,
        "filterflow_gradient_max_abs": 102.94637935328883,
        "gradient_delta": [
          140.5170675168722,
          1.67977522106491e-15
        ],
        "gradient_explosion_ratio": 2.3649539536951485,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 140.5170675168722,
        "relative_gradient_delta": 1.3649539536951485,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3816503496855148e-10,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 357.2424746082045,
        "filterflow_gradient_max_abs": 113.77902775418237,
        "gradient_delta": [
          243.4634468540221,
          5.72747441642347e-16
        ],
        "gradient_explosion_ratio": 3.1397919428527787,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 243.4634468540221,
        "relative_gradient_delta": 2.1397919428527787,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.3455015707440907e-10,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 191.81996641762416,
        "filterflow_gradient_max_abs": 165.42250820864194,
        "gradient_delta": [
          357.24247462626613,
          9.192501987320103e-16
        ],
        "gradient_explosion_ratio": 1.1595759760557371,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 357.24247462626613,
        "relative_gradient_delta": 2.1595759760557374,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.92866184029117e-10,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 265.59436965748574,
        "filterflow_gradient_max_abs": 73.77440324184383,
        "gradient_delta": [
          191.81996641564191,
          1.0792224463106488e-15
        ],
        "gradient_explosion_ratio": 3.6000883502483454,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 191.81996641564191,
        "relative_gradient_delta": 2.6000883502483454,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4417447497835383e-10,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 483.4565430759857,
        "filterflow_gradient_max_abs": 217.86217342911775,
        "gradient_delta": [
          265.5943696468679,
          -1.4626462067339038e-15
        ],
        "gradient_explosion_ratio": 2.219093546467717,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 265.5943696468679,
        "relative_gradient_delta": 1.2190935464677166,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.974509693056461e-10,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 649.0874188689313,
        "filterflow_gradient_max_abs": 165.63087578642663,
        "gradient_delta": [
          483.4565430825047,
          -2.190727513066111e-15
        ],
        "gradient_explosion_ratio": 3.91887935016355,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 483.4565430825047,
        "relative_gradient_delta": 2.9188793501635506,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.2155079427175224e-10,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 628.1349364966311,
        "filterflow_gradient_max_abs": 20.952482372929534,
        "gradient_delta": [
          649.0874188695607,
          -8.918002715114472e-16
        ],
        "gradient_explosion_ratio": 29.97902230946044,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 649.0874188695607,
        "relative_gradient_delta": 30.97902230946044,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.807603204426414e-10,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 582.527287157353,
        "filterflow_gradient_max_abs": 45.60764934214221,
        "gradient_delta": [
          628.1349364994952,
          -4.840476011451153e-16
        ],
        "gradient_explosion_ratio": 12.7725786257326,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 628.1349364994952,
        "relative_gradient_delta": 13.7725786257326,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.035900585426134e-10,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 486.72213462667173,
        "filterflow_gradient_max_abs": 95.80515251122853,
        "gradient_delta": [
          582.5272871379002,
          -4.122399838827976e-16
        ],
        "gradient_explosion_ratio": 5.080333592388229,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 582.5272871379002,
        "relative_gradient_delta": 6.080333592388228,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.194777941142092e-10,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 649.0393112616083,
        "filterflow_gradient_max_abs": 162.31717661541148,
        "gradient_delta": [
          486.7221346461968,
          -1.4625010587481742e-15
        ],
        "gradient_explosion_ratio": 3.998586747226505,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 486.7221346461968,
        "relative_gradient_delta": 2.998586747226505,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.324789415477426e-10,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 583.4246145366355,
        "filterflow_gradient_max_abs": 65.61469672303252,
        "gradient_delta": [
          649.039311259668,
          -1.0282122612073609e-15
        ],
        "gradient_explosion_ratio": 8.891675854257782,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 649.039311259668,
        "relative_gradient_delta": 9.891675854257782,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.852775876111991e-10,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 937.3354752860001,
        "filterflow_gradient_max_abs": 353.91086072731014,
        "gradient_delta": [
          583.42461455869,
          -1.3948992338582974e-15
        ],
        "gradient_explosion_ratio": 2.648507235295673,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 583.42461455869,
        "relative_gradient_delta": 1.648507235295673,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.191615860487218e-10,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1043.9106121566954,
        "filterflow_gradient_max_abs": 106.57513689011893,
        "gradient_delta": [
          937.3354752665764,
          -1.0449477019738595e-15
        ],
        "gradient_explosion_ratio": 9.795067054269776,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 937.3354752665764,
        "relative_gradient_delta": 8.795067054269776,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.87274212698685e-10,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1345.1614173621026,
        "filterflow_gradient_max_abs": 301.25080522517993,
        "gradient_delta": [
          1043.9106121369227,
          -2.343792419953187e-15
        ],
        "gradient_explosion_ratio": 4.4652541803385954,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1043.9106121369227,
        "relative_gradient_delta": 3.4652541803385954,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.1155345797960763e-10,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 939.0237370454602,
        "filterflow_gradient_max_abs": 406.1376803574301,
        "gradient_delta": [
          1345.1614174028903,
          -1.4994348183614262e-15
        ],
        "gradient_explosion_ratio": 2.3120822875115956,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1345.1614174028903,
        "relative_gradient_delta": 3.3120822875115956,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.641514005423232e-10,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1165.3363704987755,
        "filterflow_gradient_max_abs": 226.31263344208014,
        "gradient_delta": [
          939.0237370566954,
          -4.632237703069691e-15
        ],
        "gradient_explosion_ratio": 5.149232514220283,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 939.0237370566954,
        "relative_gradient_delta": 4.149232514220283,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.090381697911653e-10,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1172.1908021972026,
        "filterflow_gradient_max_abs": 6.85443174851973,
        "gradient_delta": [
          1165.3363704486828,
          -4.400825558314774e-15
        ],
        "gradient_explosion_ratio": 171.01210504435278,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1165.3363704486828,
        "relative_gradient_delta": 170.01210504435275,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.083187369971711e-10,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1252.9936807697406,
        "filterflow_gradient_max_abs": 80.80287856491722,
        "gradient_delta": [
          1172.1908022048235,
          -4.707701275573339e-15
        ],
        "gradient_explosion_ratio": 15.506795092245168,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1172.1908022048235,
        "relative_gradient_delta": 14.506795092245168,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.413411940935475e-10,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1448.041188390393,
        "filterflow_gradient_max_abs": 195.04750763879625,
        "gradient_delta": [
          1252.9936807515967,
          -2.1678049002639144e-15
        ],
        "gradient_explosion_ratio": 7.424043536470024,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1252.9936807515967,
        "relative_gradient_delta": 6.424043536470024,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.915747808809101e-10,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1676.040526216507,
        "filterflow_gradient_max_abs": 227.99933783381496,
        "gradient_delta": [
          1448.041188382692,
          -2.997237400004353e-15
        ],
        "gradient_explosion_ratio": 7.3510762888186365,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1448.041188382692,
        "relative_gradient_delta": 6.3510762888186365,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4428105638871784e-10,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1177.7306867266934,
        "filterflow_gradient_max_abs": 498.30983956509795,
        "gradient_delta": [
          1676.0405262917914,
          -1.3939957662629822e-15
        ],
        "gradient_explosion_ratio": 2.3634505948238207,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1676.0405262917914,
        "relative_gradient_delta": 3.3634505948238207,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.725002776875044e-10,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 829.1397341100858,
        "filterflow_gradient_max_abs": 348.59095258355785,
        "gradient_delta": [
          1177.7306866936437,
          -1.8494855796745042e-16
        ],
        "gradient_explosion_ratio": 2.378546339097368,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1177.7306866936437,
        "relative_gradient_delta": 3.3785463390973685,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.749836080009118e-10,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 853.6738848434729,
        "filterflow_gradient_max_abs": 24.53415070247347,
        "gradient_delta": [
          829.1397341409995,
          -5.979716631298713e-16
        ],
        "gradient_explosion_ratio": 34.79533060654949,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 829.1397341409995,
        "relative_gradient_delta": 33.79533060654949,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9053560385582387e-10,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1597.1694832174792,
        "filterflow_gradient_max_abs": 743.4955982984612,
        "gradient_delta": [
          853.673884919018,
          2.9230979749963776e-16
        ],
        "gradient_explosion_ratio": 2.148189561407905,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 853.673884919018,
        "relative_gradient_delta": 1.1481895614079047,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3861267689208034e-10,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 936.7540551705506,
        "filterflow_gradient_max_abs": 660.4154280128698,
        "gradient_delta": [
          1597.1694831834204,
          -1.8821638668183953e-15
        ],
        "gradient_explosion_ratio": 1.4184315136143302,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1597.1694831834204,
        "relative_gradient_delta": 2.41843151361433,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2236966995260445e-10,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1088.134491479866,
        "filterflow_gradient_max_abs": 151.38043625809377,
        "gradient_delta": [
          936.7540552217722,
          6.129810203075735e-16
        ],
        "gradient_explosion_ratio": 7.188078713319783,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 936.7540552217722,
        "relative_gradient_delta": 6.188078713319783,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.503508428868372e-10,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1166.4776378806146,
        "filterflow_gradient_max_abs": 78.34314644911912,
        "gradient_delta": [
          1088.1344914314955,
          -1.703206382972537e-15
        ],
        "gradient_explosion_ratio": 14.889338643530193,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1088.1344914314955,
        "relative_gradient_delta": 13.889338643530195,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4379963886312908e-10,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1541.6181759095725,
        "filterflow_gradient_max_abs": 375.1405380302191,
        "gradient_delta": [
          1166.4776378793536,
          9.750663292606e-16
        ],
        "gradient_explosion_ratio": 4.1094417148417826,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1166.4776378793536,
        "relative_gradient_delta": 3.109441714841783,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.290931888637715e-10,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1732.579550893977,
        "filterflow_gradient_max_abs": 190.9613749711765,
        "gradient_delta": [
          1541.6181759228007,
          2.166622295793501e-15
        ],
        "gradient_explosion_ratio": 9.072931901309836,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1541.6181759228007,
        "relative_gradient_delta": 8.072931901309838,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.651177055668086e-10,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1055.3767328838658,
        "filterflow_gradient_max_abs": 677.2028181986615,
        "gradient_delta": [
          1732.5795510825274,
          6.408557427455498e-16
        ],
        "gradient_explosion_ratio": 1.5584352346482184,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1732.5795510825274,
        "relative_gradient_delta": 2.5584352346482184,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.92969196177728e-10,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 902.7592585555794,
        "filterflow_gradient_max_abs": 152.6174741556563,
        "gradient_delta": [
          1055.3767327112357,
          2.974128236078781e-15
        ],
        "gradient_explosion_ratio": 5.915176250622815,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1055.3767327112357,
        "relative_gradient_delta": 6.915176250622815,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.625100468227174e-11,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1109.8193800484698,
        "filterflow_gradient_max_abs": 207.0601214499801,
        "gradient_delta": [
          902.7592585984897,
          2.5047968799318643e-15
        ],
        "gradient_explosion_ratio": 5.359889544528114,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 902.7592585984897,
        "relative_gradient_delta": 4.359889544528114,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.438458406890277e-10,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 563.3447167132949,
        "filterflow_gradient_max_abs": 546.4746634801378,
        "gradient_delta": [
          1109.8193801934326,
          4.78998863904953e-15
        ],
        "gradient_explosion_ratio": 1.0308706960460396,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1109.8193801934326,
        "relative_gradient_delta": 2.0308706960460396,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.842170943040401e-14,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 290.67028550163104,
        "filterflow_gradient_max_abs": 272.67443106070385,
        "gradient_delta": [
          563.344716562335,
          5.5205178728989325e-15
        ],
        "gradient_explosion_ratio": 1.0659975868324847,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 563.344716562335,
        "relative_gradient_delta": 2.065997586832485,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.5509905299259117e-10,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1240.3463546379205,
        "filterflow_gradient_max_abs": 949.676068984666,
        "gradient_delta": [
          290.6702856532545,
          7.007867122888347e-15
        ],
        "gradient_explosion_ratio": 1.3060730865462589,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 290.6702856532545,
        "relative_gradient_delta": 0.30607308654625875,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.264737647943548e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1138.7951017968467,
        "filterflow_gradient_max_abs": 101.55125271438094,
        "gradient_delta": [
          1240.3463545112277,
          5.40379053907732e-15
        ],
        "gradient_explosion_ratio": 11.21399363727966,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1240.3463545112277,
        "relative_gradient_delta": 12.21399363727966,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.427679308108054e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 960.9285510504076,
        "filterflow_gradient_max_abs": 177.86655077673558,
        "gradient_delta": [
          1138.795101827143,
          5.3908762632670765e-15
        ],
        "gradient_explosion_ratio": 5.402525358782041,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1138.795101827143,
        "relative_gradient_delta": 6.402525358782041,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3662173614648054e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1096.5194842302985,
        "filterflow_gradient_max_abs": 135.59093315487942,
        "gradient_delta": [
          960.9285510754191,
          7.078041475838398e-15
        ],
        "gradient_explosion_ratio": 8.086967607028662,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 960.9285510754191,
        "relative_gradient_delta": 7.0869676070286625,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.345853206657921e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1229.859540078577,
        "filterflow_gradient_max_abs": 133.34005587444113,
        "gradient_delta": [
          1096.519484204136,
          4.5401077962566956e-15
        ],
        "gradient_explosion_ratio": 9.2234815113372,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1096.519484204136,
        "relative_gradient_delta": 8.223481511337202,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4315730823000195e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1752.030747096847,
        "filterflow_gradient_max_abs": 522.1712070050679,
        "gradient_delta": [
          1229.8595400917793,
          9.228343562396008e-15
        ],
        "gradient_explosion_ratio": 3.3552802674542006,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1229.8595400917793,
        "relative_gradient_delta": 2.355280267454201,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3040164503763663e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1745.6154133698562,
        "filterflow_gradient_max_abs": 6.415333698704999,
        "gradient_delta": [
          1752.0307470685611,
          8.918651007550975e-15
        ],
        "gradient_explosion_ratio": 272.10048539208907,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1752.0307470685611,
        "relative_gradient_delta": 273.100485392089,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1294503110548249e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1548.1956489279191,
        "filterflow_gradient_max_abs": 197.4197643907813,
        "gradient_delta": [
          1745.6154133187003,
          7.832165581615847e-15
        ],
        "gradient_explosion_ratio": 7.842151233973479,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1745.6154133187003,
        "relative_gradient_delta": 8.842151233973478,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0837482022907352e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1863.7683396019022,
        "filterflow_gradient_max_abs": 315.57269054843385,
        "gradient_delta": [
          1548.1956490534683,
          8.126724268796435e-15
        ],
        "gradient_explosion_ratio": 5.905987417234548,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1548.1956490534683,
        "relative_gradient_delta": 4.905987417234548,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1401937172195176e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1923.7782206379836,
        "filterflow_gradient_max_abs": 60.009881084342744,
        "gradient_delta": [
          1863.7683395536408,
          8.829637252066209e-15
        ],
        "gradient_explosion_ratio": 32.05769093150093,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1863.7683395536408,
        "relative_gradient_delta": 31.05769093150093,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1782930187109741e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2071.412837150214,
        "filterflow_gradient_max_abs": 147.6346164990015,
        "gradient_delta": [
          1923.7782206512122,
          8.92364857452312e-15
        ],
        "gradient_explosion_ratio": 14.030671710142068,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1923.7782206512122,
        "relative_gradient_delta": 13.030671710142068,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2933298876305344e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2584.024231717407,
        "filterflow_gradient_max_abs": 512.611395216775,
        "gradient_delta": [
          2071.412836500632,
          1.2123740707479955e-14
        ],
        "gradient_explosion_ratio": 5.040902827812997,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2071.412836500632,
        "relative_gradient_delta": 4.040902827812997,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.554774583695689e-10,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2496.4423387575644,
        "filterflow_gradient_max_abs": 87.5818933878043,
        "gradient_delta": [
          2584.024232145369,
          1.3339008292481299e-14
        ],
        "gradient_explosion_ratio": 28.50409190976901,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2584.024232145369,
        "relative_gradient_delta": 29.50409190976901,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0234515457341331e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2438.6606505742575,
        "filterflow_gradient_max_abs": 57.78168821303872,
        "gradient_delta": [
          2496.442338787296,
          1.0732641600339955e-14
        ],
        "gradient_explosion_ratio": 42.204731741014825,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2496.442338787296,
        "relative_gradient_delta": 43.204731741014825,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.412825991399586e-10,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3177.5123784154857,
        "filterflow_gradient_max_abs": 738.8517276846384,
        "gradient_delta": [
          2438.6606507308475,
          1.1148651873488191e-14
        ],
        "gradient_explosion_ratio": 4.300608984664556,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2438.6606507308475,
        "relative_gradient_delta": 3.300608984664556,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1248317832723842e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4196.909674296832,
        "filterflow_gradient_max_abs": 1019.3972961264672,
        "gradient_delta": [
          3177.512378170365,
          3.111521833274225e-15
        ],
        "gradient_explosion_ratio": 4.117050035589029,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3177.512378170365,
        "relative_gradient_delta": 3.11705003558903,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.905196414663806e-10,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4074.6652730368924,
        "filterflow_gradient_max_abs": 122.24440141690243,
        "gradient_delta": [
          4196.909674453795,
          9.29319540430173e-15
        ],
        "gradient_explosion_ratio": 33.332121764338716,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4196.909674453795,
        "relative_gradient_delta": 34.332121764338716,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.500755489469157e-10,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4757.208133467044,
        "filterflow_gradient_max_abs": 682.5428603420182,
        "gradient_delta": [
          4074.6652731250256,
          7.357808565400034e-15
        ],
        "gradient_explosion_ratio": 6.969830628780198,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4074.6652731250256,
        "relative_gradient_delta": 5.969830628780198,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.193943136167945e-10,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5066.399858863406,
        "filterflow_gradient_max_abs": 309.19172560146353,
        "gradient_delta": [
          4757.208133261942,
          1.1148754518781556e-14
        ],
        "gradient_explosion_ratio": 16.38594903860333,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4757.208133261942,
        "relative_gradient_delta": 15.385949038603329,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.828742016296019e-10,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5133.304754346016,
        "filterflow_gradient_max_abs": 66.90489544481636,
        "gradient_delta": [
          5066.3998589012,
          1.676882920379929e-14
        ],
        "gradient_explosion_ratio": 76.72539834667259,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5066.3998589012,
        "relative_gradient_delta": 75.72539834667259,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.207851927480078e-10,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5883.680233127292,
        "filterflow_gradient_max_abs": 750.3754788438333,
        "gradient_delta": [
          5133.304754283458,
          1.4938761627784924e-15
        ],
        "gradient_explosion_ratio": 7.840981480621906,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5133.304754283458,
        "relative_gradient_delta": 6.840981480621906,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.709637207473861e-10,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5535.840060298762,
        "filterflow_gradient_max_abs": 347.8401730350442,
        "gradient_delta": [
          5883.680233333806,
          1.1039295703576058e-14
        ],
        "gradient_explosion_ratio": 15.914895660257844,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5883.680233333806,
        "relative_gradient_delta": 16.914895660257844,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.423448439818458e-10,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5977.343910509913,
        "filterflow_gradient_max_abs": 441.50385013274905,
        "gradient_delta": [
          5535.840060377164,
          1.3516148525017945e-14
        ],
        "gradient_explosion_ratio": 13.538599739759182,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5535.840060377164,
        "relative_gradient_delta": 12.538599739759182,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.418084007644211e-10,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6193.90458511569,
        "filterflow_gradient_max_abs": 216.5606746935064,
        "gradient_delta": [
          5977.343910422183,
          1.2262232206116851e-14
        ],
        "gradient_explosion_ratio": 28.60124348006298,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5977.343910422183,
        "relative_gradient_delta": 27.60124348006298,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.252687505068025e-10,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6786.342202980753,
        "filterflow_gradient_max_abs": 592.4376179231792,
        "gradient_delta": [
          6193.904585057574,
          1.1622025897640369e-14
        ],
        "gradient_explosion_ratio": 11.454948162762904,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6193.904585057574,
        "relative_gradient_delta": 10.454948162762904,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.707559118192876e-10,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7808.295813693738,
        "filterflow_gradient_max_abs": 1021.9536107722753,
        "gradient_delta": [
          6786.342202921463,
          1.3323606299244156e-14
        ],
        "gradient_explosion_ratio": 7.640557977766842,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6786.342202921463,
        "relative_gradient_delta": 6.640557977766842,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.629843589209486e-10,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8224.665574689967,
        "filterflow_gradient_max_abs": 416.36976112409496,
        "gradient_delta": [
          7808.295813565872,
          1.8369477425021684e-14
        ],
        "gradient_explosion_ratio": 19.753273034250643,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7808.295813565872,
        "relative_gradient_delta": 18.753273034250643,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.8334494446608e-10,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8151.457915787494,
        "filterflow_gradient_max_abs": 73.20765898029507,
        "gradient_delta": [
          8224.665574767789,
          1.6589422325885835e-14
        ],
        "gradient_explosion_ratio": 111.34706435540551,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8224.665574767789,
        "relative_gradient_delta": 112.3470643554055,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.958771336940117e-10,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8170.233472734813,
        "filterflow_gradient_max_abs": 18.775557058598526,
        "gradient_delta": [
          8151.457915676215,
          2.0584137194062994e-14
        ],
        "gradient_explosion_ratio": 435.1526533798976,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8151.457915676215,
        "relative_gradient_delta": 434.1526533798976,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.100187187665142e-10,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8659.705192060368,
        "filterflow_gradient_max_abs": 489.4717191114149,
        "gradient_delta": [
          8170.233472948953,
          1.979172098974604e-14
        ],
        "gradient_explosion_ratio": 17.6919418506572,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8170.233472948953,
        "relative_gradient_delta": 16.6919418506572,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.418758857762441e-10,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9262.895555996762,
        "filterflow_gradient_max_abs": 603.1903641588457,
        "gradient_delta": [
          8659.705191837917,
          2.938445924461068e-14
        ],
        "gradient_explosion_ratio": 15.356504523930768,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8659.705191837917,
        "relative_gradient_delta": 14.35650452393077,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0115144277733634e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10187.664097872987,
        "filterflow_gradient_max_abs": 924.7685421225882,
        "gradient_delta": [
          9262.895555750398,
          1.9075998084345898e-14
        ],
        "gradient_explosion_ratio": 11.0164475042475,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9262.895555750398,
        "relative_gradient_delta": 10.0164475042475,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2003482652289676e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9475.26288781972,
        "filterflow_gradient_max_abs": 712.4012104561216,
        "gradient_delta": [
          10187.66409827584,
          2.1382010255652815e-14
        ],
        "gradient_explosion_ratio": 13.300458714483504,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10187.66409827584,
        "relative_gradient_delta": 14.300458714483502,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.9136194850943866e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10661.802476451061,
        "filterflow_gradient_max_abs": 1186.5395908091443,
        "gradient_delta": [
          9475.262885641916,
          1.96437563968234e-14
        ],
        "gradient_explosion_ratio": 8.985627246690008,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9475.262885641916,
        "relative_gradient_delta": 7.985627246690008,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.708955086447531e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10506.608186995994,
        "filterflow_gradient_max_abs": 155.19429188795652,
        "gradient_delta": [
          10661.80247888395,
          2.0151984492328082e-14
        ],
        "gradient_explosion_ratio": 67.69970763216797,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10661.80247888395,
        "relative_gradient_delta": 68.69970763216797,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.22875973022019e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 10739.121134989962,
        "filterflow_gradient_max_abs": 232.51294890916668,
        "gradient_delta": [
          10506.608186080795,
          1.302750098855148e-14
        ],
        "gradient_explosion_ratio": 46.1871959620851,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10506.608186080795,
        "relative_gradient_delta": 45.1871959620851,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.486573056463385e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 12258.000916863783,
        "filterflow_gradient_max_abs": 1518.8797828290087,
        "gradient_delta": [
          10739.121134034775,
          2.1005763323520405e-14
        ],
        "gradient_explosion_ratio": 8.070422067263603,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 10739.121134034775,
        "relative_gradient_delta": 7.070422067263604,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.5804499627120094e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 12165.578118983432,
        "filterflow_gradient_max_abs": 92.4227988005718,
        "gradient_delta": [
          12258.000917784004,
          1.776250735075904e-14
        ],
        "gradient_explosion_ratio": 131.62962252673273,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 12258.000917784004,
        "relative_gradient_delta": 132.62962252673273,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.631609039686737e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 11670.097847102626,
        "filterflow_gradient_max_abs": 495.480272228227,
        "gradient_delta": [
          12165.578119330854,
          1.3017037034610926e-14
        ],
        "gradient_explosion_ratio": 23.55310292097194,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 12165.578119330854,
        "relative_gradient_delta": 24.55310292097194,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.181977596497745e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13575.55133600065,
        "filterflow_gradient_max_abs": 1905.453488616431,
        "gradient_delta": [
          11670.097847384219,
          1.646643230286197e-14
        ],
        "gradient_explosion_ratio": 7.124577648892387,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 11670.097847384219,
        "relative_gradient_delta": 6.124577648892387,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.158671794764814e-09,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 14111.703494175463,
        "filterflow_gradient_max_abs": 536.1521590308598,
        "gradient_delta": [
          13575.551335144602,
          1.6480075014406533e-14
        ],
        "gradient_explosion_ratio": 26.32033324212208,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13575.551335144602,
        "relative_gradient_delta": 25.32033324212208,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.624389925491414e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 14196.794465207919,
        "filterflow_gradient_max_abs": 85.09097085867334,
        "gradient_delta": [
          14111.703494349245,
          1.481678211991985e-14
        ],
        "gradient_explosion_ratio": 166.8425488855594,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 14111.703494349245,
        "relative_gradient_delta": 165.8425488855594,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.351314141284092e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 14483.161941059525,
        "filterflow_gradient_max_abs": 286.3674760142073,
        "gradient_delta": [
          14196.794465045317,
          1.8202619891787288e-14
        ],
        "gradient_explosion_ratio": 50.5754429331248,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 14196.794465045317,
        "relative_gradient_delta": 49.5754429331248,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.2123888255882775e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 16129.83273585493,
        "filterflow_gradient_max_abs": 1646.6707953160178,
        "gradient_delta": [
          14483.161940538912,
          1.422226041428853e-14
        ],
        "gradient_explosion_ratio": 9.795420421456738,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 14483.161940538912,
        "relative_gradient_delta": 8.795420421456738,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.9354371134977555e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 17836.05222155026,
        "filterflow_gradient_max_abs": 1706.2194857616348,
        "gradient_delta": [
          16129.832735788626,
          1.6254985595655022e-14
        ],
        "gradient_explosion_ratio": 10.453550888611773,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 16129.832735788626,
        "relative_gradient_delta": 9.453550888611774,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.4229368490487104e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 18327.82147462993,
        "filterflow_gradient_max_abs": 491.76925290563014,
        "gradient_delta": [
          17836.0522217243,
          1.3347178633800113e-14
        ],
        "gradient_explosion_ratio": 37.26914882607965,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 17836.0522217243,
        "relative_gradient_delta": 36.26914882607965,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.928541213506833e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 19280.85924445333,
        "filterflow_gradient_max_abs": 953.0377691516383,
        "gradient_delta": [
          18327.821475301695,
          1.9455737015659057e-14
        ],
        "gradient_explosion_ratio": 20.2309497782197,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 18327.821475301695,
        "relative_gradient_delta": 19.2309497782197,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.896453103559907e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 21224.280116982223,
        "filterflow_gradient_max_abs": 1943.4208738111502,
        "gradient_delta": [
          19280.85924317107,
          1.3950736649288742e-14
        ],
        "gradient_explosion_ratio": 10.921093008206862,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 19280.85924317107,
        "relative_gradient_delta": 9.921093008206862,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.690761887919507e-09,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_post_resample_state_stop_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 22174.945679855195,
        "filterflow_gradient_max_abs": 950.6655619127545,
        "gradient_delta": [
          21224.28011794244,
          2.2991130490743853e-14
        ],
        "gradient_explosion_ratio": 23.325706292798536,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 21224.28011794244,
        "relative_gradient_delta": 22.325706292798536,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.408061719615944e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_post_resample_state_stop_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      -5.608987982225019e+198,
      1.3245422940938783e+199
    ],
    "final_bayesfilter_gradient_max_abs": 1.3245422940938783e+199,
    "final_filterflow_gradient_diag": [
      7019.871883303286,
      713.5990730344417
    ],
    "final_filterflow_gradient_max_abs": 7019.871883303286,
    "final_gradient_delta": [
      -5.608987982225019e+198,
      1.3245422940938783e+199
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 1.3245422940938783e+199,
    "final_relative_gradient_delta": 1.8868468201596276e+195,
    "final_scalar_delta": 7.407919611068792e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "bayesfilter_gradient_max_abs": 3127913.9667580463,
      "filterflow_gradient_max_abs": 0.7972582915878877,
      "gradient_explosion_ratio": 3127913.9667580463,
      "resampling_flag": [
        true
      ],
      "status": "explosion",
      "time_index": 8,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 0.010911600127529116,
      "max_abs_gradient_delta": 0.002457259598004326,
      "relative_gradient_delta": 0.002457259598004326,
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
        "bayesfilter_gradient_max_abs": 0.010911600127529116,
        "filterflow_gradient_max_abs": 0.008924445612040184,
        "gradient_delta": [
          0.0019871545154889324,
          -0.002457259598004326
        ],
        "gradient_explosion_ratio": 0.010911600127529116,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.002457259598004326,
        "relative_gradient_delta": 0.002457259598004326,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 10.435667931681433,
        "filterflow_gradient_max_abs": 8.860476253579531,
        "gradient_delta": [
          -1.575191678101902,
          0.9189784014774831
        ],
        "gradient_explosion_ratio": 1.1777773150134614,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.575191678101902,
        "relative_gradient_delta": 0.17777731501346133,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8406609569865395e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.30693561984736,
        "filterflow_gradient_max_abs": 1.4056099396090884,
        "gradient_delta": [
          -9.712545559456448,
          0.6686712835384354
        ],
        "gradient_explosion_ratio": 5.909844108072818,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.712545559456448,
        "relative_gradient_delta": 6.909844108072817,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.5511147921642987e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 66.77733341825015,
        "filterflow_gradient_max_abs": 14.864972477668916,
        "gradient_delta": [
          -53.17907793246748,
          66.77733341825015
        ],
        "gradient_explosion_ratio": 4.492260817742327,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 66.77733341825015,
        "relative_gradient_delta": 4.492260817742327,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.2442492308982764e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 23.17227726501217,
        "filterflow_gradient_max_abs": 15.00462728219541,
        "gradient_delta": [
          -8.16764998281676,
          14.226251169565574
        ],
        "gradient_explosion_ratio": 1.5443420772276395,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 14.226251169565574,
        "relative_gradient_delta": 0.9481242620699107,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.779998453661392e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2359.9136515216273,
        "filterflow_gradient_max_abs": 6.525931066391355,
        "gradient_delta": [
          -1032.7165199827273,
          2359.9136515216273
        ],
        "gradient_explosion_ratio": 361.620989788755,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2359.9136515216273,
        "relative_gradient_delta": 361.620989788755,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.1093350116861984e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 29661.47346998244,
        "filterflow_gradient_max_abs": 2.686919378388484,
        "gradient_delta": [
          -12494.907808871441,
          29661.47346998244
        ],
        "gradient_explosion_ratio": 11039.21230705936,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 29661.47346998244,
        "relative_gradient_delta": 11039.21230705936,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4224179873708636e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 421970.9963891635,
        "filterflow_gradient_max_abs": 24.973165642495765,
        "gradient_delta": [
          177248.55885079893,
          -421970.9963891635
        ],
        "gradient_explosion_ratio": 16896.976636038227,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 421970.9963891635,
        "relative_gradient_delta": 16896.976636038227,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.5496940376542625e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3127913.9667580463,
        "filterflow_gradient_max_abs": 0.7972582915878877,
        "gradient_delta": [
          1317888.309965641,
          -3127913.9667580463
        ],
        "gradient_explosion_ratio": 3127913.9667580463,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3127913.9667580463,
        "relative_gradient_delta": 3127913.9667580463,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.66524613279762e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 24907633.981039956,
        "filterflow_gradient_max_abs": 49.77299487676166,
        "gradient_delta": [
          -10582032.015865736,
          24907633.981039956
        ],
        "gradient_explosion_ratio": 500424.6588478644,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 24907633.981039956,
        "relative_gradient_delta": 500424.6588478644,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.581402089977928e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6239561288.245247,
        "filterflow_gradient_max_abs": 91.01474473671405,
        "gradient_delta": [
          2642064345.9677567,
          -6239561288.245247
        ],
        "gradient_explosion_ratio": 68555499.51049082,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6239561288.245247,
        "relative_gradient_delta": 68555499.51049082,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.424994118489849e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 137704691350.4868,
        "filterflow_gradient_max_abs": 28.00263902728941,
        "gradient_delta": [
          58314947321.77371,
          -137704691350.4868
        ],
        "gradient_explosion_ratio": 4917561206.152372,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 137704691350.4868,
        "relative_gradient_delta": 4917561206.152372,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.85451720225683e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1723191105140.9077,
        "filterflow_gradient_max_abs": 40.13671871067378,
        "gradient_delta": [
          -729710620460.14,
          1723191105140.9077
        ],
        "gradient_explosion_ratio": 42933033902.51106,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1723191105140.9077,
        "relative_gradient_delta": 42933033902.51106,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3077183780296764e-10,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 13612827373315.756,
        "filterflow_gradient_max_abs": 49.010874255508995,
        "gradient_delta": [
          5764572674768.688,
          -13612827373315.756
        ],
        "gradient_explosion_ratio": 277751164003.8869,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 13612827373315.756,
        "relative_gradient_delta": 277751164003.8869,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4137313542050833e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 917164036395800.0,
        "filterflow_gradient_max_abs": 21.29035436921441,
        "gradient_delta": [
          388387846405927.0,
          -917164036395800.0
        ],
        "gradient_explosion_ratio": 43078852540003.18,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 917164036395800.0,
        "relative_gradient_delta": 43078852540003.18,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3353940175875323e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.241665144264061e+16,
        "filterflow_gradient_max_abs": 27.042811971633515,
        "gradient_delta": [
          -1.796200041421434e+16,
          4.241665144264061e+16
        ],
        "gradient_explosion_ratio": 1568500031991253.0,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.241665144264061e+16,
        "relative_gradient_delta": 1568500031991253.0,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.525606307950511e-10,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.8365088379824237e+17,
        "filterflow_gradient_max_abs": 18.468136147749064,
        "gradient_delta": [
          -7.776990392394842e+16,
          1.8365088379824237e+17
        ],
        "gradient_explosion_ratio": 9944202399689702.0,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.8365088379824237e+17,
        "relative_gradient_delta": 9944202399689702.0,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7488588355263346e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.435223214849999e+19,
        "filterflow_gradient_max_abs": 102.94637935328883,
        "gradient_delta": [
          -1.4547006375248525e+19,
          3.435223214849999e+19
        ],
        "gradient_explosion_ratio": 3.3369053253063763e+17,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.435223214849999e+19,
        "relative_gradient_delta": 3.3369053253063763e+17,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3816503496855148e-10,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4405711685385414e+21,
        "filterflow_gradient_max_abs": 113.77902775418237,
        "gradient_delta": [
          6.100330753656337e+20,
          -1.4405711685385414e+21
        ],
        "gradient_explosion_ratio": 1.2661130939270027e+19,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4405711685385414e+21,
        "relative_gradient_delta": 1.2661130939270027e+19,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.3455015707440907e-10,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.509792306925994e+22,
        "filterflow_gradient_max_abs": 165.42250820864194,
        "gradient_delta": [
          -1.062812031388938e+22,
          2.509792306925994e+22
        ],
        "gradient_explosion_ratio": 1.5172012165118883e+20,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.509792306925994e+22,
        "relative_gradient_delta": 1.5172012165118883e+20,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.92866184029117e-10,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.18776628896655e+23,
        "filterflow_gradient_max_abs": 73.77440324184383,
        "gradient_delta": [
          2.6203094459953943e+23,
          -6.18776628896655e+23
        ],
        "gradient_explosion_ratio": 8.387416254228586e+21,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.18776628896655e+23,
        "relative_gradient_delta": 8.387416254228586e+21,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4417447497835383e-10,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.429852140422673e+26,
        "filterflow_gradient_max_abs": 217.86217342911775,
        "gradient_delta": [
          3.146290726860547e+26,
          -7.429852140422673e+26
        ],
        "gradient_explosion_ratio": 3.4103451845163943e+24,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.429852140422673e+26,
        "relative_gradient_delta": 3.4103451845163943e+24,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.974509693056461e-10,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0160135304448185e+28,
        "filterflow_gradient_max_abs": 165.63087578642663,
        "gradient_delta": [
          -8.537134461066348e+27,
          2.0160135304448185e+28
        ],
        "gradient_explosion_ratio": 1.2171725355388298e+26,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0160135304448185e+28,
        "relative_gradient_delta": 1.2171725355388298e+26,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.2155079427175224e-10,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4681236793772244e+30,
        "filterflow_gradient_max_abs": 20.952482372929534,
        "gradient_delta": [
          -6.2170065167401074e+29,
          1.4681236793772244e+30
        ],
        "gradient_explosion_ratio": 7.006920007120637e+28,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4681236793772244e+30,
        "relative_gradient_delta": 7.006920007120637e+28,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.807603204426414e-10,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.912432437373322e+31,
        "filterflow_gradient_max_abs": 45.60764934214221,
        "gradient_delta": [
          4.197579395068676e+31,
          -9.912432437373322e+31
        ],
        "gradient_explosion_ratio": 2.173414455766321e+30,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.912432437373322e+31,
        "relative_gradient_delta": 2.173414455766321e+30,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.035900585426134e-10,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.744687962246969e+33,
        "filterflow_gradient_max_abs": 95.80515251122853,
        "gradient_delta": [
          -1.1622823871950351e+33,
          2.744687962246969e+33
        ],
        "gradient_explosion_ratio": 2.8648646657342224e+31,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.744687962246969e+33,
        "relative_gradient_delta": 2.8648646657342224e+31,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.194777941142092e-10,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.46662189039538e+35,
        "filterflow_gradient_max_abs": 162.31717661541148,
        "gradient_delta": [
          -1.891463082461257e+35,
          4.46662189039538e+35
        ],
        "gradient_explosion_ratio": 2.751786338040141e+33,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.46662189039538e+35,
        "relative_gradient_delta": 2.751786338040141e+33,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.324789415477426e-10,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.33449990444252e+36,
        "filterflow_gradient_max_abs": 65.61469672303252,
        "gradient_delta": [
          3.5293784132317617e+36,
          -8.33449990444252e+36
        ],
        "gradient_explosion_ratio": 1.270218460297613e+35,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.33449990444252e+36,
        "relative_gradient_delta": 1.270218460297613e+35,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.852775876111991e-10,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.777097170435062e+40,
        "filterflow_gradient_max_abs": 353.91086072731014,
        "gradient_delta": [
          -7.525404599507544e+39,
          1.777097170435062e+40
        ],
        "gradient_explosion_ratio": 5.021312900042147e+37,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.777097170435062e+40,
        "relative_gradient_delta": 5.021312900042147e+37,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.191615860487218e-10,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.361383335841656e+41,
        "filterflow_gradient_max_abs": 106.57513689011893,
        "gradient_delta": [
          -3.540762635865544e+41,
          8.361383335841656e+41
        ],
        "gradient_explosion_ratio": 7.845529060368375e+39,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.361383335841656e+41,
        "relative_gradient_delta": 7.845529060368375e+39,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.87274212698685e-10,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.58932392748513e+43,
        "filterflow_gradient_max_abs": 301.25080522517993,
        "gradient_delta": [
          -4.0607538850786346e+43,
          9.58932392748513e+43
        ],
        "gradient_explosion_ratio": 3.1831695587725555e+41,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.58932392748513e+43,
        "relative_gradient_delta": 3.1831695587725555e+41,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.1155345797960763e-10,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.856846620849115e+44,
        "filterflow_gradient_max_abs": 406.1376803574301,
        "gradient_delta": [
          -7.863116510222689e+43,
          1.856846620849115e+44
        ],
        "gradient_explosion_ratio": 4.5719634268235284e+41,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.856846620849115e+44,
        "relative_gradient_delta": 4.5719634268235284e+41,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.641514005423232e-10,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.274390638578713e+47,
        "filterflow_gradient_max_abs": 226.31263344208014,
        "gradient_delta": [
          -1.8100596583459354e+47,
          4.274390638578713e+47
        ],
        "gradient_explosion_ratio": 1.8887105742033846e+45,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.274390638578713e+47,
        "relative_gradient_delta": 1.8887105742033846e+45,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.090381697911653e-10,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.078712344861502e+49,
        "filterflow_gradient_max_abs": 6.85443174851973,
        "gradient_delta": [
          2.997594916296562e+49,
          -7.078712344861502e+49
        ],
        "gradient_explosion_ratio": 1.0327205236802025e+49,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.078712344861502e+49,
        "relative_gradient_delta": 1.0327205236802025e+49,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.083187369971711e-10,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.330082848561852e+51,
        "filterflow_gradient_max_abs": 80.80287856491722,
        "gradient_delta": [
          -2.680575681304412e+51,
          6.330082848561852e+51
        ],
        "gradient_explosion_ratio": 7.833981859292611e+49,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.330082848561852e+51,
        "relative_gradient_delta": 7.833981859292611e+49,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.413411940935475e-10,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.4961271577733456e+53,
        "filterflow_gradient_max_abs": 195.04750763879625,
        "gradient_delta": [
          1.4804914346428102e+53,
          -3.4961271577733456e+53
        ],
        "gradient_explosion_ratio": 1.7924490295193818e+51,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.4961271577733456e+53,
        "relative_gradient_delta": 1.7924490295193818e+51,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.915747808809101e-10,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.428202928663946e+55,
        "filterflow_gradient_max_abs": 227.99933783381496,
        "gradient_delta": [
          -1.4517278242639345e+55,
          3.428202928663946e+55
        ],
        "gradient_explosion_ratio": 1.5036021425477596e+53,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.428202928663946e+55,
        "relative_gradient_delta": 1.5036021425477596e+53,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4428105638871784e-10,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.59768033121097e+57,
        "filterflow_gradient_max_abs": 498.30983956509795,
        "gradient_delta": [
          -2.7938941514616373e+57,
          6.59768033121097e+57
        ],
        "gradient_explosion_ratio": 1.3240116504560946e+55,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.59768033121097e+57,
        "relative_gradient_delta": 1.3240116504560946e+55,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.725002776875044e-10,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0505602014713948e+60,
        "filterflow_gradient_max_abs": 348.59095258355785,
        "gradient_delta": [
          -4.448766619934974e+59,
          1.0505602014713948e+60
        ],
        "gradient_explosion_ratio": 3.013733413576113e+57,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0505602014713948e+60,
        "relative_gradient_delta": 3.013733413576113e+57,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.749836080009118e-10,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4965104242344354e+62,
        "filterflow_gradient_max_abs": 24.53415070247347,
        "gradient_delta": [
          6.33721476636404e+61,
          -1.4965104242344354e+62
        ],
        "gradient_explosion_ratio": 6.0997033986734294e+60,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4965104242344354e+62,
        "relative_gradient_delta": 6.0997033986734294e+60,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9053560385582387e-10,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.079826199327943e+64,
        "filterflow_gradient_max_abs": 743.4955982984612,
        "gradient_delta": [
          -8.807359500081292e+63,
          2.079826199327943e+64
        ],
        "gradient_explosion_ratio": 2.7973618190716426e+61,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.079826199327943e+64,
        "relative_gradient_delta": 2.7973618190716426e+61,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3861267689208034e-10,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.0895306266906845e+66,
        "filterflow_gradient_max_abs": 660.4154280128698,
        "gradient_delta": [
          1.3083115754849578e+66,
          -3.0895306266906845e+66
        ],
        "gradient_explosion_ratio": 4.67816240451378e+63,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.0895306266906845e+66,
        "relative_gradient_delta": 4.67816240451378e+63,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2236966995260445e-10,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.981330557436016e+68,
        "filterflow_gradient_max_abs": 151.38043625809377,
        "gradient_delta": [
          -2.109424769351198e+68,
          4.981330557436016e+68
        ],
        "gradient_explosion_ratio": 3.2906039119501367e+66,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.981330557436016e+68,
        "relative_gradient_delta": 3.2906039119501367e+66,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.503508428868372e-10,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.442996067162714e+70,
        "filterflow_gradient_max_abs": 78.34314644911912,
        "gradient_delta": [
          1.4579922173625185e+70,
          -3.442996067162714e+70
        ],
        "gradient_explosion_ratio": 4.394763579477636e+68,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.442996067162714e+70,
        "relative_gradient_delta": 4.394763579477636e+68,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4379963886312908e-10,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.8099888738489835e+72,
        "filterflow_gradient_max_abs": 375.1405380302191,
        "gradient_delta": [
          2.4603334990200266e+72,
          -5.8099888738489835e+72
        ],
        "gradient_explosion_ratio": 1.5487499443157927e+70,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.8099888738489835e+72,
        "relative_gradient_delta": 1.5487499443157927e+70,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.290931888637715e-10,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.887334544776174e+74,
        "filterflow_gradient_max_abs": 190.9613749711765,
        "gradient_delta": [
          3.340019029267958e+74,
          -7.887334544776174e+74
        ],
        "gradient_explosion_ratio": 4.130329783165145e+72,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.887334544776174e+74,
        "relative_gradient_delta": 4.130329783165145e+72,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.651177055668086e-10,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.984434871158189e+76,
        "filterflow_gradient_max_abs": 677.2028181986615,
        "gradient_delta": [
          2.11073934106691e+76,
          -4.984434871158189e+76
        ],
        "gradient_explosion_ratio": 7.360328009881339e+73,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.984434871158189e+76,
        "relative_gradient_delta": 7.360328009881339e+73,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.92969196177728e-10,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.696736555011643e+78,
        "filterflow_gradient_max_abs": 152.6174741556563,
        "gradient_delta": [
          -2.4123749779406833e+78,
          5.696736555011643e+78
        ],
        "gradient_explosion_ratio": 3.732689579963482e+76,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.696736555011643e+78,
        "relative_gradient_delta": 3.732689579963482e+76,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.625100468227174e-11,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.597820991426281e+80,
        "filterflow_gradient_max_abs": 207.0601214499801,
        "gradient_delta": [
          -1.5235553287418537e+80,
          3.597820991426281e+80
        ],
        "gradient_explosion_ratio": 1.7375731097962353e+78,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.597820991426281e+80,
        "relative_gradient_delta": 1.7375731097962353e+78,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.438458406890277e-10,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7116330685862404e+83,
        "filterflow_gradient_max_abs": 546.4746634801378,
        "gradient_delta": [
          -7.248186301402261e+82,
          1.7116330685862404e+83
        ],
        "gradient_explosion_ratio": 3.132136186673276e+80,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7116330685862404e+83,
        "relative_gradient_delta": 3.132136186673276e+80,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.842170943040401e-14,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.324341192275319e+84,
        "filterflow_gradient_max_abs": 272.67443106070385,
        "gradient_delta": [
          9.842797675993879e+83,
          -2.324341192275319e+84
        ],
        "gradient_explosion_ratio": 8.524235966069972e+81,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.324341192275319e+84,
        "relative_gradient_delta": 8.524235966069972e+81,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.5509905299259117e-10,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.183940044963513e+88,
        "filterflow_gradient_max_abs": 949.676068984666,
        "gradient_delta": [
          -2.1952230247707376e+88,
          5.183940044963513e+88
        ],
        "gradient_explosion_ratio": 5.458640281949882e+85,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.183940044963513e+88,
        "relative_gradient_delta": 5.458640281949882e+85,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.264737647943548e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4722791065536993e+90,
        "filterflow_gradient_max_abs": 101.55125271438094,
        "gradient_delta": [
          -6.234603343330777e+89,
          1.4722791065536993e+90
        ],
        "gradient_explosion_ratio": 1.4497892120489875e+88,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4722791065536993e+90,
        "relative_gradient_delta": 1.4497892120489875e+88,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.427679308108054e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3917533620272016e+92,
        "filterflow_gradient_max_abs": 177.86655077673558,
        "gradient_delta": [
          1.012826538184219e+92,
          -2.3917533620272016e+92
        ],
        "gradient_explosion_ratio": 1.3446897978189364e+90,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3917533620272016e+92,
        "relative_gradient_delta": 1.3446897978189364e+90,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3662173614648054e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4072679269114615e+93,
        "filterflow_gradient_max_abs": 135.59093315487942,
        "gradient_delta": [
          -1.0193964309217554e+93,
          2.4072679269114615e+93
        ],
        "gradient_explosion_ratio": 1.7753900433458537e+91,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4072679269114615e+93,
        "relative_gradient_delta": 1.7753900433458537e+91,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.345853206657921e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.752548263830752e+95,
        "filterflow_gradient_max_abs": 133.34005587444113,
        "gradient_delta": [
          3.7064077337942366e+95,
          -8.752548263830752e+95
        ],
        "gradient_explosion_ratio": 6.5640802431285435e+93,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.752548263830752e+95,
        "relative_gradient_delta": 6.5640802431285435e+93,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4315730823000195e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3237158080888737e+98,
        "filterflow_gradient_max_abs": 522.1712070050679,
        "gradient_delta": [
          9.840149385786978e+97,
          -2.3237158080888737e+98
        ],
        "gradient_explosion_ratio": 4.4501032935474e+95,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3237158080888737e+98,
        "relative_gradient_delta": 4.4501032935474e+95,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3040164503763663e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4261818930007978e+100,
        "filterflow_gradient_max_abs": 6.415333698704999,
        "gradient_delta": [
          6.039397257435909e+99,
          -1.4261818930007978e+100
        ],
        "gradient_explosion_ratio": 2.2230829446778226e+99,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4261818930007978e+100,
        "relative_gradient_delta": 2.2230829446778226e+99,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1294503110548249e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.97918210490066e+101,
        "filterflow_gradient_max_abs": 197.4197643907813,
        "gradient_delta": [
          -4.225845618400138e+101,
          9.97918210490066e+101
        ],
        "gradient_explosion_ratio": 5.054803978565911e+99,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.97918210490066e+101,
        "relative_gradient_delta": 5.054803978565911e+99,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0837482022907352e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.2978796714814e+104,
        "filterflow_gradient_max_abs": 315.57269054843385,
        "gradient_delta": [
          -2.2434725973731246e+104,
          5.2978796714814e+104
        ],
        "gradient_explosion_ratio": 1.6788143683391022e+102,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.2978796714814e+104,
        "relative_gradient_delta": 1.6788143683391022e+102,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1401937172195176e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.707543550063755e+107,
        "filterflow_gradient_max_abs": 60.009881084342744,
        "gradient_delta": [
          -7.230868575612755e+106,
          1.707543550063755e+107
        ],
        "gradient_explosion_ratio": 2.845437316670958e+105,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.707543550063755e+107,
        "relative_gradient_delta": 2.845437316670958e+105,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1782930187109741e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.487745704226963e+108,
        "filterflow_gradient_max_abs": 147.6346164990015,
        "gradient_delta": [
          2.323874431323701e+108,
          -5.487745704226963e+108
        ],
        "gradient_explosion_ratio": 3.717113123170593e+106,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.487745704226963e+108,
        "relative_gradient_delta": 3.717113123170593e+106,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2933298876305344e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4992862355900214e+111,
        "filterflow_gradient_max_abs": 512.611395216775,
        "gradient_delta": [
          6.348969387265033e+110,
          -1.4992862355900214e+111
        ],
        "gradient_explosion_ratio": 2.9248008327165607e+108,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4992862355900214e+111,
        "relative_gradient_delta": 2.9248008327165607e+108,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.554774583695689e-10,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.958924664605602e+111,
        "filterflow_gradient_max_abs": 87.5818933878043,
        "gradient_delta": [
          -1.2530043742722252e+111,
          2.958924664605602e+111
        ],
        "gradient_explosion_ratio": 3.3784661990621334e+109,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.958924664605602e+111,
        "relative_gradient_delta": 3.3784661990621334e+109,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0234515457341331e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.769192449717838e+115,
        "filterflow_gradient_max_abs": 57.78168821303872,
        "gradient_delta": [
          1.1726592076519046e+115,
          -2.769192449717838e+115
        ],
        "gradient_explosion_ratio": 4.792508726134721e+113,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.769192449717838e+115,
        "relative_gradient_delta": 4.792508726134721e+113,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.412825991399586e-10,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.967397561749268e+118,
        "filterflow_gradient_max_abs": 738.8517276846384,
        "gradient_delta": [
          -1.6800584884142136e+118,
          3.967397561749268e+118
        ],
        "gradient_explosion_ratio": 5.36968029320581e+115,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.967397561749268e+118,
        "relative_gradient_delta": 5.36968029320581e+115,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1248317832723842e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.734425870678799e+121,
        "filterflow_gradient_max_abs": 1019.3972961264672,
        "gradient_delta": [
          1.15793673900122e+121,
          -2.734425870678799e+121
        ],
        "gradient_explosion_ratio": 2.68239466699504e+118,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.734425870678799e+121,
        "relative_gradient_delta": 2.68239466699504e+118,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.905196414663806e-10,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1722657419258815e+122,
        "filterflow_gradient_max_abs": 122.24440141690243,
        "gradient_delta": [
          4.964148361101975e+121,
          -1.1722657419258815e+122
        ],
        "gradient_explosion_ratio": 9.58952498714428e+119,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1722657419258815e+122,
        "relative_gradient_delta": 9.58952498714428e+119,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.500755489469157e-10,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3822043829091949e+125,
        "filterflow_gradient_max_abs": 682.5428603420182,
        "gradient_delta": [
          -5.8531673977388045e+124,
          1.3822043829091949e+125
        ],
        "gradient_explosion_ratio": 2.025080713929936e+122,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3822043829091949e+125,
        "relative_gradient_delta": 2.025080713929936e+122,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.193943136167945e-10,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7961719265247086e+128,
        "filterflow_gradient_max_abs": 309.19172560146353,
        "gradient_delta": [
          -7.60617973077196e+127,
          1.7961719265247086e+128
        ],
        "gradient_explosion_ratio": 5.809249659028413e+125,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7961719265247086e+128,
        "relative_gradient_delta": 5.809249659028413e+125,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.828742016296019e-10,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.342523900026992e+130,
        "filterflow_gradient_max_abs": 66.90489544481636,
        "gradient_delta": [
          5.685133992835378e+129,
          -1.342523900026992e+130
        ],
        "gradient_explosion_ratio": 2.0066153472047727e+128,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.342523900026992e+130,
        "relative_gradient_delta": 2.0066153472047727e+128,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.207851927480078e-10,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.878433709886126e+133,
        "filterflow_gradient_max_abs": 750.3754788438333,
        "gradient_delta": [
          2.0658514396138477e+133,
          -4.878433709886126e+133
        ],
        "gradient_explosion_ratio": 6.501323467289655e+130,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.878433709886126e+133,
        "relative_gradient_delta": 6.501323467289655e+130,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.709637207473861e-10,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3603230408285576e+134,
        "filterflow_gradient_max_abs": 347.8401730350442,
        "gradient_delta": [
          -9.995168617271714e+133,
          2.3603230408285576e+134
        ],
        "gradient_explosion_ratio": 6.785653940526185e+131,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3603230408285576e+134,
        "relative_gradient_delta": 6.785653940526185e+131,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.423448439818458e-10,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.15013095513503e+136,
        "filterflow_gradient_max_abs": 441.50385013274905,
        "gradient_delta": [
          -3.451304407926481e+136,
          8.15013095513503e+136
        ],
        "gradient_explosion_ratio": 1.84599317824397e+134,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.15013095513503e+136,
        "relative_gradient_delta": 1.84599317824397e+134,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.418084007644211e-10,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.831018323448297e+138,
        "filterflow_gradient_max_abs": 216.5606746935064,
        "gradient_delta": [
          2.0457726294551806e+138,
          -4.831018323448297e+138
        ],
        "gradient_explosion_ratio": 2.2307920541370364e+136,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.831018323448297e+138,
        "relative_gradient_delta": 2.2307920541370364e+136,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.252687505068025e-10,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.774958077404285e+141,
        "filterflow_gradient_max_abs": 592.4376179231792,
        "gradient_delta": [
          2.8689652724328604e+141,
          -6.774958077404285e+141
        ],
        "gradient_explosion_ratio": 1.1435732425557735e+139,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.774958077404285e+141,
        "relative_gradient_delta": 1.1435732425557735e+139,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.707559118192876e-10,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.7883148621891674e+144,
        "filterflow_gradient_max_abs": 1021.9536107722753,
        "gradient_delta": [
          -1.6042230308273925e+144,
          3.7883148621891674e+144
        ],
        "gradient_explosion_ratio": 3.706934270065736e+141,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.7883148621891674e+144,
        "relative_gradient_delta": 3.706934270065736e+141,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.629843589209486e-10,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3694420443791777e+146,
        "filterflow_gradient_max_abs": 416.36976112409496,
        "gradient_delta": [
          -5.799123216772165e+145,
          1.3694420443791777e+146
        ],
        "gradient_explosion_ratio": 3.2890045633525937e+143,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3694420443791777e+146,
        "relative_gradient_delta": 3.2890045633525937e+143,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.8334494446608e-10,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.2431311272972106e+148,
        "filterflow_gradient_max_abs": 73.20765898029507,
        "gradient_delta": [
          1.3733561849177665e+148,
          -3.2431311272972106e+148
        ],
        "gradient_explosion_ratio": 4.430043485163414e+146,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.2431311272972106e+148,
        "relative_gradient_delta": 4.430043485163414e+146,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.958771336940117e-10,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3906479989189884e+150,
        "filterflow_gradient_max_abs": 18.775557058598526,
        "gradient_delta": [
          1.4358245835330023e+150,
          -3.3906479989189884e+150
        ],
        "gradient_explosion_ratio": 1.8058841015138852e+149,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3906479989189884e+150,
        "relative_gradient_delta": 1.8058841015138852e+149,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.100187187665142e-10,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.290280112333004e+152,
        "filterflow_gradient_max_abs": 489.4717191114149,
        "gradient_delta": [
          5.463899247347726e+151,
          -1.290280112333004e+152
        ],
        "gradient_explosion_ratio": 2.6360667265421865e+149,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.290280112333004e+152,
        "relative_gradient_delta": 2.6360667265421865e+149,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.418758857762441e-10,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.233532603248811e+155,
        "filterflow_gradient_max_abs": 603.1903641588457,
        "gradient_delta": [
          1.79275766427866e+155,
          -4.233532603248811e+155
        ],
        "gradient_explosion_ratio": 7.018568025622409e+152,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.233532603248811e+155,
        "relative_gradient_delta": 7.018568025622409e+152,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0115144277733634e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4752346332445077e+158,
        "filterflow_gradient_max_abs": 924.7685421225882,
        "gradient_delta": [
          -6.247118997805364e+157,
          1.4752346332445077e+158
        ],
        "gradient_explosion_ratio": 1.595247422515535e+155,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4752346332445077e+158,
        "relative_gradient_delta": 1.595247422515535e+155,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2003482652289676e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.344943155977586e+161,
        "filterflow_gradient_max_abs": 712.4012104561216,
        "gradient_delta": [
          5.695378722364462e+160,
          -1.344943155977586e+161
        ],
        "gradient_explosion_ratio": 1.8879012784333612e+158,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.344943155977586e+161,
        "relative_gradient_delta": 1.8879012784333612e+158,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.9136194850943866e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.865934873738686e+164,
        "filterflow_gradient_max_abs": 1186.5395908091443,
        "gradient_delta": [
          7.901602182944764e+163,
          -1.865934873738686e+164
        ],
        "gradient_explosion_ratio": 1.5725854309389182e+161,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.865934873738686e+164,
        "relative_gradient_delta": 1.5725854309389182e+161,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.708955086447531e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0928580761596228e+166,
        "filterflow_gradient_max_abs": 155.19429188795652,
        "gradient_delta": [
          4.627883792604971e+165,
          -1.0928580761596228e+166
        ],
        "gradient_explosion_ratio": 7.041870308919728e+163,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0928580761596228e+166,
        "relative_gradient_delta": 7.041870308919728e+163,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.22875973022019e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3833713621832666e+168,
        "filterflow_gradient_max_abs": 232.51294890916668,
        "gradient_delta": [
          1.4327431743410386e+168,
          -3.3833713621832666e+168
        ],
        "gradient_explosion_ratio": 1.4551324466255906e+166,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3833713621832666e+168,
        "relative_gradient_delta": 1.4551324466255906e+166,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.486573056463385e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.620004625560682e+170,
        "filterflow_gradient_max_abs": 1518.8797828290087,
        "gradient_delta": [
          -1.5329493464200153e+170,
          3.620004625560682e+170
        ],
        "gradient_explosion_ratio": 2.38333847516108e+167,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.620004625560682e+170,
        "relative_gradient_delta": 2.38333847516108e+167,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.5804499627120094e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.477274125707823e+172,
        "filterflow_gradient_max_abs": 92.4227988005718,
        "gradient_delta": [
          -1.4725078141306135e+172,
          3.477274125707823e+172
        ],
        "gradient_explosion_ratio": 3.7623553612686204e+170,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.477274125707823e+172,
        "relative_gradient_delta": 3.7623553612686204e+170,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.631609039686737e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.593217636352639e+174,
        "filterflow_gradient_max_abs": 495.480272228227,
        "gradient_delta": [
          6.746737054164293e+173,
          -1.593217636352639e+174
        ],
        "gradient_explosion_ratio": 3.2155016569837812e+171,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.593217636352639e+174,
        "relative_gradient_delta": 3.2155016569837812e+171,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.181977596497745e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.890465122428448e+177,
        "filterflow_gradient_max_abs": 1905.453488616431,
        "gradient_delta": [
          2.4944124644973406e+177,
          -5.890465122428448e+177
        ],
        "gradient_explosion_ratio": 3.091371769302841e+174,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.890465122428448e+177,
        "relative_gradient_delta": 3.091371769302841e+174,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.158671794764814e-09,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.790875873909602e+177,
        "filterflow_gradient_max_abs": 536.1521590308598,
        "gradient_delta": [
          3.2991720492897144e+177,
          -7.790875873909602e+177
        ],
        "gradient_explosion_ratio": 1.4531091114120041e+175,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.790875873909602e+177,
        "relative_gradient_delta": 1.4531091114120041e+175,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.624389925491414e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.912189746407254e+181,
        "filterflow_gradient_max_abs": 85.09097085867334,
        "gradient_delta": [
          -2.0801459777360977e+181,
          4.912189746407254e+181
        ],
        "gradient_explosion_ratio": 5.772868374678502e+179,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.912189746407254e+181,
        "relative_gradient_delta": 5.772868374678502e+179,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.351314141284092e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.03337740963062e+183,
        "filterflow_gradient_max_abs": 286.3674760142073,
        "gradient_delta": [
          8.610664608296478e+182,
          -2.03337740963062e+183
        ],
        "gradient_explosion_ratio": 7.100587810920748e+180,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.03337740963062e+183,
        "relative_gradient_delta": 7.100587810920748e+180,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.2123888255882775e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.87138407530169e+186,
        "filterflow_gradient_max_abs": 1646.6707953160178,
        "gradient_delta": [
          3.333264545700886e+186,
          -7.87138407530169e+186
        ],
        "gradient_explosion_ratio": 4.780180773043387e+183,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.87138407530169e+186,
        "relative_gradient_delta": 4.780180773043387e+183,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.9354371134977555e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.5369982048749057e+189,
        "filterflow_gradient_max_abs": 1706.2194857616348,
        "gradient_delta": [
          -1.074332809569102e+189,
          2.5369982048749057e+189
        ],
        "gradient_explosion_ratio": 1.4869119864390846e+186,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.5369982048749057e+189,
        "relative_gradient_delta": 1.4869119864390846e+186,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.4229368490487104e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.216401375885499e+191,
        "filterflow_gradient_max_abs": 491.76925290563014,
        "gradient_delta": [
          -3.055901557295611e+191,
          7.216401375885499e+191
        ],
        "gradient_explosion_ratio": 1.4674364721355032e+189,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.216401375885499e+191,
        "relative_gradient_delta": 1.4674364721355032e+189,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.928541213506833e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.245124644513601e+193,
        "filterflow_gradient_max_abs": 953.0377691516383,
        "gradient_delta": [
          -2.644598759493552e+193,
          6.245124644513601e+193
        ],
        "gradient_explosion_ratio": 6.5528616458430586e+190,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.245124644513601e+193,
        "relative_gradient_delta": 6.5528616458430586e+190,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.896453103559907e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.6625168549529255e+197,
        "filterflow_gradient_max_abs": 1943.4208738111502,
        "gradient_delta": [
          1.1274857064582365e+197,
          -2.6625168549529255e+197
        ],
        "gradient_explosion_ratio": 1.370015569366398e+194,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.6625168549529255e+197,
        "relative_gradient_delta": 1.370015569366398e+194,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.690761887919507e-09,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3245422940938783e+199,
        "filterflow_gradient_max_abs": 950.6655619127545,
        "gradient_delta": [
          -5.608987982225019e+198,
          1.3245422940938783e+199
        ],
        "gradient_explosion_ratio": 1.3932789270591413e+196,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3245422940938783e+199,
        "relative_gradient_delta": 1.3932789270591413e+196,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.408061719615944e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_raw_transport_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      1.3515114431922745e+218,
      -1.1290717972775883e+218
    ],
    "final_bayesfilter_gradient_max_abs": 1.3515114431922745e+218,
    "final_filterflow_gradient_diag": [
      7019.871883303286,
      713.5990730344417
    ],
    "final_filterflow_gradient_max_abs": 7019.871883303286,
    "final_gradient_delta": [
      1.3515114431922745e+218,
      -1.1290717972775883e+218
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 1.3515114431922745e+218,
    "final_relative_gradient_delta": 1.925265112611007e+214,
    "final_scalar_delta": 7.407919611068792e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "bayesfilter_gradient_max_abs": 9195505.610780967,
      "filterflow_gradient_max_abs": 0.7972582915878877,
      "gradient_explosion_ratio": 9195505.610780967,
      "resampling_flag": [
        true
      ],
      "status": "explosion",
      "time_index": 8,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 1.0061793068397484,
      "max_abs_gradient_delta": 0.05475160151717162,
      "relative_gradient_delta": 0.006179306839748326,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.8406609569865395e-11,
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
        "bayesfilter_gradient_max_abs": 0.008924445612040184,
        "filterflow_gradient_max_abs": 0.008924445612040184,
        "gradient_delta": [
          0.0,
          -5.795395272864551e-20
        ],
        "gradient_explosion_ratio": 0.008924445612040184,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 5.795395272864551e-20,
        "relative_gradient_delta": 5.795395272864551e-20,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.915227855096703,
        "filterflow_gradient_max_abs": 8.860476253579531,
        "gradient_delta": [
          -0.05475160151717162,
          0.03707418793594731
        ],
        "gradient_explosion_ratio": 1.0061793068397484,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.05475160151717162,
        "relative_gradient_delta": 0.006179306839748326,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8406609569865395e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.41460040326663,
        "filterflow_gradient_max_abs": 1.4056099396090884,
        "gradient_delta": [
          -7.820210342875718,
          -0.8607962633986631
        ],
        "gradient_explosion_ratio": 4.563570747835336,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.820210342875718,
        "relative_gradient_delta": 5.563570747835336,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.5511147921642987e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 84.91559161373418,
        "filterflow_gradient_max_abs": 14.864972477668916,
        "gradient_delta": [
          -99.7805640914031,
          73.5703394417855
        ],
        "gradient_explosion_ratio": 5.71246208099609,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 99.7805640914031,
        "relative_gradient_delta": 6.71246208099609,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.2442492308982764e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 18.44534233601806,
        "filterflow_gradient_max_abs": 15.00462728219541,
        "gradient_delta": [
          7.886961778604195,
          18.44534233601806
        ],
        "gradient_explosion_ratio": 1.2293102647011718,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 18.44534233601806,
        "relative_gradient_delta": 1.2293102647011718,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.779998453661392e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9743.94004421566,
        "filterflow_gradient_max_abs": 6.525931066391355,
        "gradient_delta": [
          -9737.414113149269,
          7903.79187901978
        ],
        "gradient_explosion_ratio": 1493.1110894500712,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9737.414113149269,
        "relative_gradient_delta": 1492.1110894500712,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.1093350116861984e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 258298.98288897768,
        "filterflow_gradient_max_abs": 2.686919378388484,
        "gradient_delta": [
          -258301.66980835606,
          214891.3498982717
        ],
        "gradient_explosion_ratio": 96132.0183130675,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 258301.66980835606,
        "relative_gradient_delta": 96133.01831306748,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4224179873708636e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 324900.69275483215,
        "filterflow_gradient_max_abs": 24.973165642495765,
        "gradient_delta": [
          -324875.7195891897,
          282705.93505387544
        ],
        "gradient_explosion_ratio": 13009.9923015752,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 324875.7195891897,
        "relative_gradient_delta": 13008.9923015752,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.5496940376542625e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9195505.610780967,
        "filterflow_gradient_max_abs": 0.7972582915878877,
        "gradient_delta": [
          9195506.408039259,
          -8036478.510680706
        ],
        "gradient_explosion_ratio": 9195505.610780967,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9195506.408039259,
        "relative_gradient_delta": 9195506.408039259,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.66524613279762e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 382875866.76590914,
        "filterflow_gradient_max_abs": 49.77299487676166,
        "gradient_delta": [
          -382875916.538904,
          319724090.65727
        ],
        "gradient_explosion_ratio": 7692441.809336828,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 382875916.538904,
        "relative_gradient_delta": 7692442.809336828,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.581402089977928e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 65321312046.92027,
        "filterflow_gradient_max_abs": 91.01474473671405,
        "gradient_delta": [
          65321311955.905525,
          -54459712435.14222
        ],
        "gradient_explosion_ratio": 717700326.8633087,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 65321311955.905525,
        "relative_gradient_delta": 717700325.8633085,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.424994118489849e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2257902832598.7676,
        "filterflow_gradient_max_abs": 28.00263902728941,
        "gradient_delta": [
          2257902832626.77,
          -1890282276023.0234
        ],
        "gradient_explosion_ratio": 80631787253.99324,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2257902832626.77,
        "relative_gradient_delta": 80631787254.99323,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.85451720225683e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 50905494744162.92,
        "filterflow_gradient_max_abs": 40.13671871067378,
        "gradient_delta": [
          50905494744122.79,
          -42548666239420.91
        ],
        "gradient_explosion_ratio": 1268302352046.166,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 50905494744122.79,
        "relative_gradient_delta": 1268302352045.1663,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3077183780296764e-10,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2550359035201362.5,
        "filterflow_gradient_max_abs": 49.010874255508995,
        "gradient_delta": [
          -2550359035201411.5,
          2126258070040169.0
        ],
        "gradient_explosion_ratio": 52036595427895.13,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2550359035201411.5,
        "relative_gradient_delta": 52036595427896.13,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4137313542050833e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.22009120619641e+17,
        "filterflow_gradient_max_abs": 21.29035436921441,
        "gradient_delta": [
          2.2200912061964096e+17,
          -1.854041819684387e+17
        ],
        "gradient_explosion_ratio": 1.0427685550441728e+16,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2200912061964096e+17,
        "relative_gradient_delta": 1.0427685550441726e+16,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3353940175875323e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.706375256531782e+17,
        "filterflow_gradient_max_abs": 27.042811971633515,
        "gradient_delta": [
          -8.706375256531782e+17,
          7.243383565198019e+17
        ],
        "gradient_explosion_ratio": 3.219478531176533e+16,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.706375256531782e+17,
        "relative_gradient_delta": 3.219478531176533e+16,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.525606307950511e-10,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.370660598464977e+19,
        "filterflow_gradient_max_abs": 18.468136147749064,
        "gradient_delta": [
          -6.370660598464977e+19,
          5.315640861968841e+19
        ],
        "gradient_explosion_ratio": 3.449541712005111e+18,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.370660598464977e+19,
        "relative_gradient_delta": 3.449541712005111e+18,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7488588355263346e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.011912285155395e+21,
        "filterflow_gradient_max_abs": 102.94637935328883,
        "gradient_delta": [
          3.011912285155395e+21,
          -2.516770194780696e+21
        ],
        "gradient_explosion_ratio": 2.9257097763673543e+19,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.011912285155395e+21,
        "relative_gradient_delta": 2.9257097763673543e+19,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3816503496855148e-10,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.31482827076068e+23,
        "filterflow_gradient_max_abs": 113.77902775418237,
        "gradient_delta": [
          -6.31482827076068e+23,
          5.275275400724121e+23
        ],
        "gradient_explosion_ratio": 5.550081060987582e+21,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.31482827076068e+23,
        "relative_gradient_delta": 5.550081060987582e+21,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.3455015707440907e-10,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0155851142378778e+26,
        "filterflow_gradient_max_abs": 165.42250820864194,
        "gradient_delta": [
          1.0155851142378778e+26,
          -8.484299961470961e+25
        ],
        "gradient_explosion_ratio": 6.139340560336287e+23,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0155851142378778e+26,
        "relative_gradient_delta": 6.139340560336287e+23,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.92866184029117e-10,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0562297990305144e+28,
        "filterflow_gradient_max_abs": 73.77440324184383,
        "gradient_delta": [
          -1.0562297990305144e+28,
          8.824128395905481e+27
        ],
        "gradient_explosion_ratio": 1.431702260698783e+26,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0562297990305144e+28,
        "relative_gradient_delta": 1.431702260698783e+26,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4417447497835383e-10,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4578552520243467e+30,
        "filterflow_gradient_max_abs": 217.86217342911775,
        "gradient_delta": [
          -2.4578552520243467e+30,
          2.0533233616255708e+30
        ],
        "gradient_explosion_ratio": 1.1281698026500314e+28,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4578552520243467e+30,
        "relative_gradient_delta": 1.1281698026500314e+28,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.974509693056461e-10,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.9335133257350875e+32,
        "filterflow_gradient_max_abs": 165.63087578642663,
        "gradient_delta": [
          1.9335133257350875e+32,
          -1.6152607457863307e+32
        ],
        "gradient_explosion_ratio": 1.1673628582561284e+30,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.9335133257350875e+32,
        "relative_gradient_delta": 1.1673628582561284e+30,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.2155079427175224e-10,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3310273104099154e+34,
        "filterflow_gradient_max_abs": 20.952482372929534,
        "gradient_delta": [
          3.3310273104099154e+34,
          -2.782766763308961e+34
        ],
        "gradient_explosion_ratio": 1.5898007935869118e+33,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3310273104099154e+34,
        "relative_gradient_delta": 1.5898007935869118e+33,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.807603204426414e-10,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.258944781661576e+36,
        "filterflow_gradient_max_abs": 45.60764934214221,
        "gradient_delta": [
          1.258944781661576e+36,
          -1.0517159399915034e+36
        ],
        "gradient_explosion_ratio": 2.7603807690616727e+34,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.258944781661576e+36,
        "relative_gradient_delta": 2.7603807690616727e+34,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.035900585426134e-10,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.642422919625248e+36,
        "filterflow_gradient_max_abs": 95.80515251122853,
        "gradient_delta": [
          -7.642422919625248e+36,
          6.384289096445762e+36
        ],
        "gradient_explosion_ratio": 7.97704791371168e+34,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.642422919625248e+36,
        "relative_gradient_delta": 7.97704791371168e+34,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.194777941142092e-10,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2397859825626116e+39,
        "filterflow_gradient_max_abs": 162.31717661541148,
        "gradient_delta": [
          -1.2397859825626116e+39,
          1.0357044710462055e+39
        ],
        "gradient_explosion_ratio": 7.638045513199852e+36,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2397859825626116e+39,
        "relative_gradient_delta": 7.638045513199852e+36,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.324789415477426e-10,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0970839154365316e+42,
        "filterflow_gradient_max_abs": 65.61469672303252,
        "gradient_delta": [
          1.0970839154365316e+42,
          -9.165201620151445e+41
        ],
        "gradient_explosion_ratio": 1.6720094281125065e+40,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0970839154365316e+42,
        "relative_gradient_delta": 1.6720094281125065e+40,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.852775876111991e-10,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.1770033331277535e+44,
        "filterflow_gradient_max_abs": 353.91086072731014,
        "gradient_delta": [
          -4.1770033331277535e+44,
          3.489526129093571e+44
        ],
        "gradient_explosion_ratio": 1.1802416361407323e+42,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.1770033331277535e+44,
        "relative_gradient_delta": 1.1802416361407323e+42,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.191615860487218e-10,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.940681213904315e+46,
        "filterflow_gradient_max_abs": 106.57513689011893,
        "gradient_delta": [
          -4.940681213904315e+46,
          4.127513820512493e+46
        ],
        "gradient_explosion_ratio": 4.6358666365104045e+44,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.940681213904315e+46,
        "relative_gradient_delta": 4.6358666365104045e+44,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.87274212698685e-10,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0781517771816635e+49,
        "filterflow_gradient_max_abs": 301.25080522517993,
        "gradient_delta": [
          -1.0781517771816635e+49,
          9.007032464050631e+48
        ],
        "gradient_explosion_ratio": 3.5789174949283975e+46,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0781517771816635e+49,
        "relative_gradient_delta": 3.5789174949283975e+46,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.1155345797960763e-10,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.963295192829389e+51,
        "filterflow_gradient_max_abs": 406.1376803574301,
        "gradient_delta": [
          3.963295192829389e+51,
          -3.310992916015757e+51
        ],
        "gradient_explosion_ratio": 9.758501573509277e+48,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.963295192829389e+51,
        "relative_gradient_delta": 9.758501573509277e+48,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.641514005423232e-10,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.053266233509728e+52,
        "filterflow_gradient_max_abs": 226.31263344208014,
        "gradient_delta": [
          9.053266233509728e+52,
          -7.563226732060607e+52
        ],
        "gradient_explosion_ratio": 4.000336214472409e+50,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.053266233509728e+52,
        "relative_gradient_delta": 4.000336214472409e+50,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.090381697911653e-10,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1522600742980565e+56,
        "filterflow_gradient_max_abs": 6.85443174851973,
        "gradient_delta": [
          1.1522600742980565e+56,
          -9.626143827227235e+55
        ],
        "gradient_explosion_ratio": 1.6810439093611174e+55,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1522600742980565e+56,
        "relative_gradient_delta": 1.6810439093611174e+55,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.083187369971711e-10,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1850256639856927e+58,
        "filterflow_gradient_max_abs": 80.80287856491722,
        "gradient_delta": [
          -1.1850256639856927e+58,
          9.899872210950648e+57
        ],
        "gradient_explosion_ratio": 1.4665636732652295e+56,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1850256639856927e+58,
        "relative_gradient_delta": 1.4665636732652295e+56,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.413411940935475e-10,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.245354262372143e+59,
        "filterflow_gradient_max_abs": 195.04750763879625,
        "gradient_delta": [
          4.245354262372143e+59,
          -3.5466290641739363e+59
        ],
        "gradient_explosion_ratio": 2.176574473452904e+57,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.245354262372143e+59,
        "relative_gradient_delta": 2.176574473452904e+57,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.915747808809101e-10,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.017030740742271e+60,
        "filterflow_gradient_max_abs": 227.99933783381496,
        "gradient_delta": [
          9.017030740742271e+60,
          -7.532955146784457e+60
        ],
        "gradient_explosion_ratio": 3.954849530008126e+58,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.017030740742271e+60,
        "relative_gradient_delta": 3.954849530008126e+58,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4428105638871784e-10,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.193090202333769e+64,
        "filterflow_gradient_max_abs": 498.30983956509795,
        "gradient_delta": [
          -7.193090202333769e+64,
          6.009209410434649e+64
        ],
        "gradient_explosion_ratio": 1.443497525276958e+62,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.193090202333769e+64,
        "relative_gradient_delta": 1.443497525276958e+62,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.725002776875044e-10,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0808088184907515e+67,
        "filterflow_gradient_max_abs": 348.59095258355785,
        "gradient_delta": [
          -1.0808088184907515e+67,
          9.029229913931143e+66
        ],
        "gradient_explosion_ratio": 3.100507372553451e+64,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0808088184907515e+67,
        "relative_gradient_delta": 3.100507372553451e+64,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.749836080009118e-10,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.6805934796623426e+69,
        "filterflow_gradient_max_abs": 24.53415070247347,
        "gradient_delta": [
          4.6805934796623426e+69,
          -3.91023407092197e+69
        ],
        "gradient_explosion_ratio": 1.9077870419987503e+68,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.6805934796623426e+69,
        "relative_gradient_delta": 1.9077870419987503e+68,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9053560385582387e-10,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.047728750233288e+70,
        "filterflow_gradient_max_abs": 743.4955982984612,
        "gradient_delta": [
          -3.047728750233288e+70,
          2.54611575432522e+70
        ],
        "gradient_explosion_ratio": 4.0991886935285376e+67,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.047728750233288e+70,
        "relative_gradient_delta": 4.0991886935285376e+67,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3861267689208034e-10,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.171811284141271e+73,
        "filterflow_gradient_max_abs": 660.4154280128698,
        "gradient_delta": [
          8.171811284141271e+73,
          -6.826846861023913e+73
        ],
        "gradient_explosion_ratio": 1.2373743764178118e+71,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.171811284141271e+73,
        "relative_gradient_delta": 1.2373743764178118e+71,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2236966995260445e-10,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.685283526648857e+75,
        "filterflow_gradient_max_abs": 151.38043625809377,
        "gradient_delta": [
          -7.685283526648857e+75,
          6.4203946831013196e+75
        ],
        "gradient_explosion_ratio": 5.07680101644439e+73,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.685283526648857e+75,
        "relative_gradient_delta": 5.07680101644439e+73,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.503508428868372e-10,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.327945692814475e+78,
        "filterflow_gradient_max_abs": 78.34314644911912,
        "gradient_delta": [
          2.327945692814475e+78,
          -1.944798795888549e+78
        ],
        "gradient_explosion_ratio": 2.9714733174858977e+76,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.327945692814475e+78,
        "relative_gradient_delta": 2.9714733174858977e+76,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4379963886312908e-10,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.268714929943253e+79,
        "filterflow_gradient_max_abs": 375.1405380302191,
        "gradient_delta": [
          5.268714929943253e+79,
          -4.401559058387549e+79
        ],
        "gradient_explosion_ratio": 1.404464299595059e+77,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.268714929943253e+79,
        "relative_gradient_delta": 1.404464299595059e+77,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.290931888637715e-10,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.907981783086711e+82,
        "filterflow_gradient_max_abs": 190.9613749711765,
        "gradient_delta": [
          2.907981783086711e+82,
          -2.4293691591139295e+82
        ],
        "gradient_explosion_ratio": 1.5228115023394854e+80,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.907981783086711e+82,
        "relative_gradient_delta": 1.5228115023394854e+80,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.651177055668086e-10,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.5909447060530045e+85,
        "filterflow_gradient_max_abs": 677.2028181986615,
        "gradient_delta": [
          2.5909447060530045e+85,
          -2.164511895660028e+85
        ],
        "gradient_explosion_ratio": 3.825950862025113e+82,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.5909447060530045e+85,
        "relative_gradient_delta": 3.825950862025113e+82,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.92969196177728e-10,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.589410897629186e+87,
        "filterflow_gradient_max_abs": 152.6174741556563,
        "gradient_delta": [
          -2.589410897629186e+87,
          2.1632305303837516e+87
        ],
        "gradient_explosion_ratio": 1.6966673783293098e+85,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.589410897629186e+87,
        "relative_gradient_delta": 1.6966673783293098e+85,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.625100468227174e-11,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.270190291123869e+88,
        "filterflow_gradient_max_abs": 207.0601214499801,
        "gradient_delta": [
          -8.270190291123869e+88,
          6.909034076522848e+88
        ],
        "gradient_explosion_ratio": 3.9941009563841654e+86,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.270190291123869e+88,
        "relative_gradient_delta": 3.9941009563841654e+86,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.438458406890277e-10,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1255836450916413e+92,
        "filterflow_gradient_max_abs": 546.4746634801378,
        "gradient_delta": [
          -2.1255836450916413e+92,
          1.775742675739998e+92
        ],
        "gradient_explosion_ratio": 3.889628901649706e+89,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1255836450916413e+92,
        "relative_gradient_delta": 3.889628901649706e+89,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.842170943040401e-14,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.338216768127066e+93,
        "filterflow_gradient_max_abs": 272.67443106070385,
        "gradient_delta": [
          4.338216768127066e+93,
          -3.624207717989915e+93
        ],
        "gradient_explosion_ratio": 1.5909877399400442e+91,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.338216768127066e+93,
        "relative_gradient_delta": 1.5909877399400442e+91,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.5509905299259117e-10,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.078540190736647e+97,
        "filterflow_gradient_max_abs": 949.676068984666,
        "gradient_delta": [
          -9.078540190736647e+97,
          7.584341029033797e+97
        ],
        "gradient_explosion_ratio": 9.559617734121542e+94,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.078540190736647e+97,
        "relative_gradient_delta": 9.559617734121542e+94,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.264737647943548e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.936627081914298e+99,
        "filterflow_gradient_max_abs": 101.55125271438094,
        "gradient_delta": [
          -9.936627081914298e+99,
          8.301198968581746e+99
        ],
        "gradient_explosion_ratio": 9.784839493670911e+97,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.936627081914298e+99,
        "relative_gradient_delta": 9.784839493670911e+97,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.427679308108054e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.095141432173635e+101,
        "filterflow_gradient_max_abs": 177.86655077673558,
        "gradient_delta": [
          -1.095141432173635e+101,
          9.14896659829114e+100
        ],
        "gradient_explosion_ratio": 6.157096021658932e+98,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.095141432173635e+101,
        "relative_gradient_delta": 6.157096021658932e+98,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3662173614648054e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.358543390700818e+103,
        "filterflow_gradient_max_abs": 135.59093315487942,
        "gradient_delta": [
          -5.358543390700818e+103,
          4.4766030264886e+103
        ],
        "gradient_explosion_ratio": 3.951992412781756e+101,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.358543390700818e+103,
        "relative_gradient_delta": 3.951992412781756e+101,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.345853206657921e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.5293097467796575e+106,
        "filterflow_gradient_max_abs": 133.34005587444113,
        "gradient_delta": [
          2.5293097467796575e+106,
          -2.1130211779212787e+106
        ],
        "gradient_explosion_ratio": 1.896886670845081e+104,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.5293097467796575e+106,
        "relative_gradient_delta": 1.896886670845081e+104,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4315730823000195e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.65112643231841e+107,
        "filterflow_gradient_max_abs": 522.1712070050679,
        "gradient_delta": [
          -6.65112643231841e+107,
          5.556445202654388e+107
        ],
        "gradient_explosion_ratio": 1.2737443855754112e+105,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.65112643231841e+107,
        "relative_gradient_delta": 1.2737443855754112e+105,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3040164503763663e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.000450307092154e+110,
        "filterflow_gradient_max_abs": 6.415333698704999,
        "gradient_delta": [
          -1.000450307092154e+110,
          8.3579035309341e+109
        ],
        "gradient_explosion_ratio": 1.559467292081946e+109,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.000450307092154e+110,
        "relative_gradient_delta": 1.559467292081946e+109,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1294503110548249e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4055924940469942e+111,
        "filterflow_gradient_max_abs": 197.4197643907813,
        "gradient_delta": [
          -1.4055924940469942e+111,
          1.1742518729586123e+111
        ],
        "gradient_explosion_ratio": 7.119816490433567e+108,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4055924940469942e+111,
        "relative_gradient_delta": 7.119816490433567e+108,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0837482022907352e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.295277464971095e+113,
        "filterflow_gradient_max_abs": 315.57269054843385,
        "gradient_delta": [
          1.295277464971095e+113,
          -1.0820931355888004e+113
        ],
        "gradient_explosion_ratio": 4.1045296496348655e+110,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.295277464971095e+113,
        "relative_gradient_delta": 4.1045296496348655e+110,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1401937172195176e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.031733243629689e+116,
        "filterflow_gradient_max_abs": 60.009881084342744,
        "gradient_delta": [
          8.031733243629689e+116,
          -6.709823682454014e+116
        ],
        "gradient_explosion_ratio": 1.338401792921609e+115,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.031733243629689e+116,
        "relative_gradient_delta": 1.338401792921609e+115,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1782930187109741e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.97076092639515e+118,
        "filterflow_gradient_max_abs": 147.6346164990015,
        "gradient_delta": [
          -6.97076092639515e+118,
          5.823472385085568e+118
        ],
        "gradient_explosion_ratio": 4.7216303951602674e+116,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.97076092639515e+118,
        "relative_gradient_delta": 4.7216303951602674e+116,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2933298876305344e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3965606638333068e+121,
        "filterflow_gradient_max_abs": 512.611395216775,
        "gradient_delta": [
          -1.3965606638333068e+121,
          1.1667065541058287e+121
        ],
        "gradient_explosion_ratio": 2.7244042502073603e+118,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3965606638333068e+121,
        "relative_gradient_delta": 2.7244042502073603e+118,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.554774583695689e-10,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2085689834560543e+123,
        "filterflow_gradient_max_abs": 87.5818933878043,
        "gradient_delta": [
          -2.2085689834560543e+123,
          1.845069802496302e+123
        ],
        "gradient_explosion_ratio": 2.521718700093318e+121,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2085689834560543e+123,
        "relative_gradient_delta": 2.521718700093318e+121,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0234515457341331e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.763958503547678e+125,
        "filterflow_gradient_max_abs": 57.78168821303872,
        "gradient_delta": [
          -4.763958503547678e+125,
          3.979878392336481e+125
        ],
        "gradient_explosion_ratio": 8.244754784566277e+123,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.763958503547678e+125,
        "relative_gradient_delta": 8.244754784566277e+123,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.412825991399586e-10,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.517392781099118e+128,
        "filterflow_gradient_max_abs": 738.8517276846384,
        "gradient_delta": [
          2.517392781099118e+128,
          -2.1030655760454686e+128
        ],
        "gradient_explosion_ratio": 3.407169106835477e+125,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.517392781099118e+128,
        "relative_gradient_delta": 3.407169106835477e+125,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1248317832723842e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3655045520491896e+131,
        "filterflow_gradient_max_abs": 1019.3972961264672,
        "gradient_delta": [
          -2.3655045520491896e+131,
          1.9761759987336824e+131
        ],
        "gradient_explosion_ratio": 2.320493257180195e+128,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3655045520491896e+131,
        "relative_gradient_delta": 2.320493257180195e+128,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.905196414663806e-10,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.255276366901258e+133,
        "filterflow_gradient_max_abs": 122.24440141690243,
        "gradient_delta": [
          -3.255276366901258e+133,
          2.7195039721832146e+133
        ],
        "gradient_explosion_ratio": 2.6629247058926323e+131,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.255276366901258e+133,
        "relative_gradient_delta": 2.6629247058926323e+131,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.500755489469157e-10,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1642182871878157e+136,
        "filterflow_gradient_max_abs": 682.5428603420182,
        "gradient_delta": [
          2.1642182871878157e+136,
          -1.8080186028203177e+136
        ],
        "gradient_explosion_ratio": 3.170816681172723e+133,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1642182871878157e+136,
        "relative_gradient_delta": 3.170816681172723e+133,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.193943136167945e-10,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3122920658181975e+138,
        "filterflow_gradient_max_abs": 309.19172560146353,
        "gradient_delta": [
          3.3122920658181975e+138,
          -2.767135694410542e+138
        ],
        "gradient_explosion_ratio": 1.071274484908958e+136,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3122920658181975e+138,
        "relative_gradient_delta": 1.071274484908958e+136,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.828742016296019e-10,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7028209769074936e+141,
        "filterflow_gradient_max_abs": 66.90489544481636,
        "gradient_delta": [
          -1.7028209769074936e+141,
          1.422560756346774e+141
        ],
        "gradient_explosion_ratio": 2.5451365936473103e+139,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7028209769074936e+141,
        "relative_gradient_delta": 2.5451365936473103e+139,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.207851927480078e-10,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.373764197360021e+143,
        "filterflow_gradient_max_abs": 750.3754788438333,
        "gradient_delta": [
          -4.373764197360021e+143,
          3.6539045437287463e+143
        ],
        "gradient_explosion_ratio": 5.828767491308548e+140,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.373764197360021e+143,
        "relative_gradient_delta": 5.828767491308548e+140,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.709637207473861e-10,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7385792313518547e+145,
        "filterflow_gradient_max_abs": 347.8401730350442,
        "gradient_delta": [
          -1.7385792313518547e+145,
          1.4524337084526334e+145
        ],
        "gradient_explosion_ratio": 4.998212875131868e+142,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7385792313518547e+145,
        "relative_gradient_delta": 4.998212875131868e+142,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.423448439818458e-10,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.406500081287934e+147,
        "filterflow_gradient_max_abs": 441.50385013274905,
        "gradient_delta": [
          4.406500081287934e+147,
          -3.681252564707878e+147
        ],
        "gradient_explosion_ratio": 9.980660598912129e+144,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.406500081287934e+147,
        "relative_gradient_delta": 9.980660598912129e+144,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.418084007644211e-10,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3807413991679678e+151,
        "filterflow_gradient_max_abs": 216.5606746935064,
        "gradient_delta": [
          2.3807413991679678e+151,
          -1.9889050765730885e+151
        ],
        "gradient_explosion_ratio": 1.0993415136600304e+149,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3807413991679678e+151,
        "relative_gradient_delta": 1.0993415136600304e+149,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.252687505068025e-10,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.052256830238403e+153,
        "filterflow_gradient_max_abs": 592.4376179231792,
        "gradient_delta": [
          8.052256830238403e+153,
          -6.726969377324458e+153
        ],
        "gradient_explosion_ratio": 1.359173790899033e+151,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.052256830238403e+153,
        "relative_gradient_delta": 1.359173790899033e+151,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.707559118192876e-10,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.571031831462472e+157,
        "filterflow_gradient_max_abs": 1021.9536107722753,
        "gradient_delta": [
          -1.571031831462472e+157,
          1.31246223808501e+157
        ],
        "gradient_explosion_ratio": 1.5372829205772523e+154,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.571031831462472e+157,
        "relative_gradient_delta": 1.5372829205772523e+154,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.629843589209486e-10,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.262837809926604e+158,
        "filterflow_gradient_max_abs": 416.36976112409496,
        "gradient_delta": [
          -4.262837809926604e+158,
          3.5612350689301207e+158
        ],
        "gradient_explosion_ratio": 1.0238106144927528e+156,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.262837809926604e+158,
        "relative_gradient_delta": 1.0238106144927528e+156,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.8334494446608e-10,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.262079356201493e+162,
        "filterflow_gradient_max_abs": 73.20765898029507,
        "gradient_delta": [
          1.262079356201493e+162,
          -1.0543589654317367e+162
        ],
        "gradient_explosion_ratio": 1.723971745280368e+160,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.262079356201493e+162,
        "relative_gradient_delta": 1.723971745280368e+160,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.958771336940117e-10,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.0558199250318157e+164,
        "filterflow_gradient_max_abs": 18.775557058598526,
        "gradient_delta": [
          4.0558199250318157e+164,
          -3.3882893964801176e+164
        ],
        "gradient_explosion_ratio": 2.1601595693664903e+163,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.0558199250318157e+164,
        "relative_gradient_delta": 2.1601595693664903e+163,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.100187187665142e-10,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.196782127210011e+166,
        "filterflow_gradient_max_abs": 489.4717191114149,
        "gradient_delta": [
          -2.196782127210011e+166,
          1.8352228958844447e+166
        ],
        "gradient_explosion_ratio": 4.488067525531487e+163,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.196782127210011e+166,
        "relative_gradient_delta": 4.488067525531487e+163,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.418758857762441e-10,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.082038981854977e+168,
        "filterflow_gradient_max_abs": 603.1903641588457,
        "gradient_delta": [
          1.082038981854977e+168,
          -9.039506872999548e+167
        ],
        "gradient_explosion_ratio": 1.7938598594224726e+165,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.082038981854977e+168,
        "relative_gradient_delta": 1.7938598594224726e+165,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0115144277733634e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5404613362590854e+172,
        "filterflow_gradient_max_abs": 924.7685421225882,
        "gradient_delta": [
          1.5404613362590854e+172,
          -1.286923213508624e+172
        ],
        "gradient_explosion_ratio": 1.665780426227864e+169,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5404613362590854e+172,
        "relative_gradient_delta": 1.665780426227864e+169,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2003482652289676e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.105923378516135e+174,
        "filterflow_gradient_max_abs": 712.4012104561216,
        "gradient_delta": [
          -5.105923378516135e+174,
          4.265560691166644e+174
        ],
        "gradient_explosion_ratio": 7.167201997378723e+171,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.105923378516135e+174,
        "relative_gradient_delta": 7.167201997378723e+171,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.9136194850943866e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1109753841152565e+178,
        "filterflow_gradient_max_abs": 1186.5395908091443,
        "gradient_delta": [
          -1.1109753841152565e+178,
          9.281245674926302e+177
        ],
        "gradient_explosion_ratio": 9.363154779838759e+174,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1109753841152565e+178,
        "relative_gradient_delta": 9.363154779838759e+174,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.708955086447531e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.0228776282893772e+180,
        "filterflow_gradient_max_abs": 155.19429188795652,
        "gradient_delta": [
          -3.0228776282893772e+180,
          2.525354775140694e+180
        ],
        "gradient_explosion_ratio": 1.9478020689522283e+178,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.0228776282893772e+180,
        "relative_gradient_delta": 1.9478020689522283e+178,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.22875973022019e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.94018094941109e+182,
        "filterflow_gradient_max_abs": 232.51294890916668,
        "gradient_delta": [
          -7.94018094941109e+182,
          6.63333959946754e+182
        ],
        "gradient_explosion_ratio": 3.414941398602705e+180,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.94018094941109e+182,
        "relative_gradient_delta": 3.414941398602705e+180,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.486573056463385e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.92326011592649e+186,
        "filterflow_gradient_max_abs": 1518.8797828290087,
        "gradient_delta": [
          -1.92326011592649e+186,
          1.6067187345394106e+186
        ],
        "gradient_explosion_ratio": 1.2662359046904275e+183,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.92326011592649e+186,
        "relative_gradient_delta": 1.2662359046904275e+183,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.5804499627120094e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.363693825366473e+188,
        "filterflow_gradient_max_abs": 92.4227988005718,
        "gradient_delta": [
          -6.363693825366473e+188,
          5.316319932711531e+188
        ],
        "gradient_explosion_ratio": 6.885415620336205e+186,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.363693825366473e+188,
        "relative_gradient_delta": 6.885415620336205e+186,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.631609039686737e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.896718775355686e+189,
        "filterflow_gradient_max_abs": 495.480272228227,
        "gradient_delta": [
          -9.896718775355686e+189,
          8.267859004174193e+189
        ],
        "gradient_explosion_ratio": 1.997399155944009e+187,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.896718775355686e+189,
        "relative_gradient_delta": 1.997399155944009e+187,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.181977596497745e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.4221068831516946e+194,
        "filterflow_gradient_max_abs": 1905.453488616431,
        "gradient_delta": [
          4.4221068831516946e+194,
          -3.6942907079798645e+194
        ],
        "gradient_explosion_ratio": 2.3207634873116904e+191,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.4221068831516946e+194,
        "relative_gradient_delta": 2.3207634873116904e+191,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.158671794764814e-09,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.53052295090967e+196,
        "filterflow_gradient_max_abs": 536.1521590308598,
        "gradient_delta": [
          5.53052295090967e+196,
          -4.62027718634726e+196
        ],
        "gradient_explosion_ratio": 1.0315211564020475e+194,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.53052295090967e+196,
        "relative_gradient_delta": 1.0315211564020475e+194,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.624389925491414e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.096191776557516e+199,
        "filterflow_gradient_max_abs": 85.09097085867334,
        "gradient_delta": [
          -5.096191776557516e+199,
          4.257430773089252e+199
        ],
        "gradient_explosion_ratio": 5.989109919807738e+197,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.096191776557516e+199,
        "relative_gradient_delta": 5.989109919807738e+197,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.351314141284092e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.428324101233285e+202,
        "filterflow_gradient_max_abs": 286.3674760142073,
        "gradient_delta": [
          1.428324101233285e+202,
          -1.1932421794855127e+202
        ],
        "gradient_explosion_ratio": 4.98773157173206e+199,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.428324101233285e+202,
        "relative_gradient_delta": 4.98773157173206e+199,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.2123888255882775e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.8722507085397855e+205,
        "filterflow_gradient_max_abs": 1646.6707953160178,
        "gradient_delta": [
          2.8722507085397855e+205,
          -2.399518913478762e+205
        ],
        "gradient_explosion_ratio": 1.7442774334189627e+202,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.8722507085397855e+205,
        "relative_gradient_delta": 1.7442774334189627e+202,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.9354371134977555e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.458655116980666e+208,
        "filterflow_gradient_max_abs": 1706.2194857616348,
        "gradient_delta": [
          -4.458655116980666e+208,
          3.7248236200498724e+208
        ],
        "gradient_explosion_ratio": 2.6131779376499024e+205,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.458655116980666e+208,
        "relative_gradient_delta": 2.6131779376499024e+205,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.4229368490487104e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1628491625680144e+211,
        "filterflow_gradient_max_abs": 491.76925290563014,
        "gradient_delta": [
          -1.1628491625680144e+211,
          9.714606565536994e+210
        ],
        "gradient_explosion_ratio": 2.364623562163134e+208,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1628491625680144e+211,
        "relative_gradient_delta": 2.364623562163134e+208,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.928541213506833e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.099859724449997e+213,
        "filterflow_gradient_max_abs": 953.0377691516383,
        "gradient_delta": [
          -4.099859724449997e+213,
          3.425080868525209e+213
        ],
        "gradient_explosion_ratio": 4.3018858823397445e+210,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.099859724449997e+213,
        "relative_gradient_delta": 4.3018858823397445e+210,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.896453103559907e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.22166327232064e+217,
        "filterflow_gradient_max_abs": 1943.4208738111502,
        "gradient_delta": [
          2.22166327232064e+217,
          -1.8560089568311628e+217
        ],
        "gradient_explosion_ratio": 1.1431714572272972e+214,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.22166327232064e+217,
        "relative_gradient_delta": 1.1431714572272972e+214,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.690761887919507e-09,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3515114431922745e+218,
        "filterflow_gradient_max_abs": 950.6655619127545,
        "gradient_delta": [
          1.3515114431922745e+218,
          -1.1290717972775883e+218
        ],
        "gradient_explosion_ratio": 1.4216476301855425e+215,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3515114431922745e+218,
        "relative_gradient_delta": 1.4216476301855425e+215,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.408061719615944e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_raw_transport_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      2.0723038706470447e+216,
      -1.896623537407829e+216
    ],
    "final_bayesfilter_gradient_max_abs": 2.0723038706470447e+216,
    "final_filterflow_gradient_diag": [
      7019.871883303286,
      713.5990730344417
    ],
    "final_filterflow_gradient_max_abs": 7019.871883303286,
    "final_gradient_delta": [
      2.0723038706470447e+216,
      -1.896623537407829e+216
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 2.0723038706470447e+216,
    "final_relative_gradient_delta": 2.9520536914299024e+212,
    "final_scalar_delta": 7.407919611068792e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "bayesfilter_gradient_max_abs": 394334960.921803,
      "filterflow_gradient_max_abs": 91.01474473671405,
      "gradient_explosion_ratio": 4332649.199451459,
      "resampling_flag": [
        true
      ],
      "status": "explosion",
      "time_index": 10,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 0.00039670643358147626,
      "max_abs_gradient_delta": 0.00932115204562166,
      "relative_gradient_delta": 0.00932115204562166,
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
        "bayesfilter_gradient_max_abs": 0.00039670643358147626,
        "filterflow_gradient_max_abs": 0.008924445612040184,
        "gradient_delta": [
          -0.00932115204562166,
          -8.419658157116119e-20
        ],
        "gradient_explosion_ratio": 0.00039670643358147626,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.00932115204562166,
        "relative_gradient_delta": 0.00932115204562166,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 0.09665815874320527,
        "filterflow_gradient_max_abs": 8.860476253579531,
        "gradient_delta": [
          8.763818094836326,
          3.0340091663460128e-05
        ],
        "gradient_explosion_ratio": 0.010908912340254451,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.763818094836326,
        "relative_gradient_delta": 0.9890910876597456,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8406609569865395e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 0.12881891670012915,
        "filterflow_gradient_max_abs": 1.4056099396090884,
        "gradient_delta": [
          -1.2767910229089592,
          -0.08101923335306094
        ],
        "gradient_explosion_ratio": 0.09164627616104845,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2767910229089592,
        "relative_gradient_delta": 0.9083537238389515,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.5511147921642987e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.465137344953979,
        "filterflow_gradient_max_abs": 14.864972477668916,
        "gradient_delta": [
          -17.227965401844436,
          2.4651373449539786
        ],
        "gradient_explosion_ratio": 0.1658353117476175,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 17.227965401844436,
        "relative_gradient_delta": 1.1589638277316259,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.2442492308982764e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 67.64306694947143,
        "filterflow_gradient_max_abs": 15.00462728219541,
        "gradient_delta": [
          -52.638439667276025,
          66.71300467259748
        ],
        "gradient_explosion_ratio": 4.508147098711152,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 66.71300467259748,
        "relative_gradient_delta": 4.446162068401364,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.779998453661392e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 108.43581450495073,
        "filterflow_gradient_max_abs": 6.525931066391355,
        "gradient_delta": [
          114.96174557134208,
          -101.44719594173655
        ],
        "gradient_explosion_ratio": 16.616144639252603,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 114.96174557134208,
        "relative_gradient_delta": 17.616144639252603,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.1093350116861984e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8710.263802535728,
        "filterflow_gradient_max_abs": 2.686919378388484,
        "gradient_delta": [
          -8712.950721914116,
          8049.011093381197
        ],
        "gradient_explosion_ratio": 3241.728751742386,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8712.950721914116,
        "relative_gradient_delta": 3242.7287517423856,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4224179873708636e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 12142.795726141618,
        "filterflow_gradient_max_abs": 24.973165642495765,
        "gradient_delta": [
          -12117.822560499122,
          11816.24110767075
        ],
        "gradient_explosion_ratio": 486.23373984589057,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 12117.822560499122,
        "relative_gradient_delta": 485.23373984589057,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.5496940376542625e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 111824.35836562379,
        "filterflow_gradient_max_abs": 0.7972582915878877,
        "gradient_delta": [
          111825.15562391537,
          -103946.33908763042
        ],
        "gradient_explosion_ratio": 111824.35836562379,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 111825.15562391537,
        "relative_gradient_delta": 111825.15562391537,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.66524613279762e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7736759.107752367,
        "filterflow_gradient_max_abs": 49.77299487676166,
        "gradient_delta": [
          7736709.33475749,
          -7065877.169932473
        ],
        "gradient_explosion_ratio": 155440.899767206,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7736709.33475749,
        "relative_gradient_delta": 155439.899767206,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.581402089977928e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 394334960.921803,
        "filterflow_gradient_max_abs": 91.01474473671405,
        "gradient_delta": [
          394334869.90705824,
          -358838096.3671521
        ],
        "gradient_explosion_ratio": 4332649.199451459,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 394334869.90705824,
        "relative_gradient_delta": 4332648.199451459,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.424994118489849e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 73337345701.70612,
        "filterflow_gradient_max_abs": 28.00263902728941,
        "gradient_delta": [
          -73337345673.70348,
          67286822531.57958
        ],
        "gradient_explosion_ratio": 2618944079.8860664,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 73337345673.70348,
        "relative_gradient_delta": 2618944078.8860664,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.85451720225683e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2499409355655.525,
        "filterflow_gradient_max_abs": 40.13671871067378,
        "gradient_delta": [
          -2499409355695.6616,
          2293010155218.471
        ],
        "gradient_explosion_ratio": 62272388873.45425,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2499409355695.6616,
        "relative_gradient_delta": 62272388874.45425,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3077183780296764e-10,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 106680526628192.34,
        "filterflow_gradient_max_abs": 49.010874255508995,
        "gradient_delta": [
          106680526628143.33,
          -97574918259886.39
        ],
        "gradient_explosion_ratio": 2176670550132.0674,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 106680526628143.33,
        "relative_gradient_delta": 2176670550131.0674,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4137313542050833e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5945786468392394.0,
        "filterflow_gradient_max_abs": 21.29035436921441,
        "gradient_delta": [
          5945786468392373.0,
          -5446788494628573.0
        ],
        "gradient_explosion_ratio": 279271371686979.9,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5945786468392373.0,
        "relative_gradient_delta": 279271371686978.94,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3353940175875323e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0120436458464744e+17,
        "filterflow_gradient_max_abs": 27.042811971633515,
        "gradient_delta": [
          -1.0120436458464741e+17,
          9.249548786857902e+16
        ],
        "gradient_explosion_ratio": 3742375781438908.0,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0120436458464741e+17,
        "relative_gradient_delta": 3742375781438907.0,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.525606307950511e-10,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.8656483559509007e+18,
        "filterflow_gradient_max_abs": 18.468136147749064,
        "gradient_delta": [
          -1.8656483559509007e+18,
          1.7067977682427218e+18
        ],
        "gradient_explosion_ratio": 1.0101985067823371e+17,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.8656483559509007e+18,
        "relative_gradient_delta": 1.0101985067823371e+17,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7488588355263346e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.880713304247451e+19,
        "filterflow_gradient_max_abs": 102.94637935328883,
        "gradient_delta": [
          3.880713304247451e+19,
          -3.5592861349817663e+19
        ],
        "gradient_explosion_ratio": 3.769645254768713e+17,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.880713304247451e+19,
        "relative_gradient_delta": 3.769645254768713e+17,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3816503496855148e-10,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.191577316497926e+22,
        "filterflow_gradient_max_abs": 113.77902775418237,
        "gradient_delta": [
          -2.191577316497926e+22,
          2.00586115114985e+22
        ],
        "gradient_explosion_ratio": 1.926169839693824e+20,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.191577316497926e+22,
        "relative_gradient_delta": 1.926169839693824e+20,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.3455015707440907e-10,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4011315035117939e+24,
        "filterflow_gradient_max_abs": 165.42250820864194,
        "gradient_delta": [
          -2.4011315035117939e+24,
          2.1977422126006683e+24
        ],
        "gradient_explosion_ratio": 1.4515143855051008e+22,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4011315035117939e+24,
        "relative_gradient_delta": 1.4515143855051008e+22,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.92866184029117e-10,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.681452109485903e+26,
        "filterflow_gradient_max_abs": 73.77440324184383,
        "gradient_delta": [
          -2.681452109485903e+26,
          2.454277809748883e+26
        ],
        "gradient_explosion_ratio": 3.6346645877916367e+24,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.681452109485903e+26,
        "relative_gradient_delta": 3.6346645877916367e+24,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4417447497835383e-10,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.115701779727552e+28,
        "filterflow_gradient_max_abs": 217.86217342911775,
        "gradient_delta": [
          -1.115701779727552e+28,
          1.0211757188321594e+28
        ],
        "gradient_explosion_ratio": 5.121135817964975e+25,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.115701779727552e+28,
        "relative_gradient_delta": 5.121135817964975e+25,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.974509693056461e-10,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.10993821613414e+30,
        "filterflow_gradient_max_abs": 165.63087578642663,
        "gradient_delta": [
          -6.10993821613414e+30,
          5.592239249083348e+30
        ],
        "gradient_explosion_ratio": 3.6888884316548707e+28,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.10993821613414e+30,
        "relative_gradient_delta": 3.6888884316548707e+28,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.2155079427175224e-10,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.608741705356017e+32,
        "filterflow_gradient_max_abs": 20.952482372929534,
        "gradient_delta": [
          -6.608741705356017e+32,
          6.0486222995024735e+32
        ],
        "gradient_explosion_ratio": 3.154156909777176e+31,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.608741705356017e+32,
        "relative_gradient_delta": 3.154156909777176e+31,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.807603204426414e-10,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.8087035893230604e+33,
        "filterflow_gradient_max_abs": 45.60764934214221,
        "gradient_delta": [
          -3.8087035893230604e+33,
          3.486012393001248e+33
        ],
        "gradient_explosion_ratio": 8.351019279136047e+31,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.8087035893230604e+33,
        "relative_gradient_delta": 8.351019279136047e+31,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.035900585426134e-10,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.0646516482815126e+35,
        "filterflow_gradient_max_abs": 95.80515251122853,
        "gradient_delta": [
          4.0646516482815126e+35,
          -3.720392579820372e+35
        ],
        "gradient_explosion_ratio": 4.242623221966197e+33,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.0646516482815126e+35,
        "relative_gradient_delta": 4.242623221966197e+33,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.194777941142092e-10,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0477200024767561e+38,
        "filterflow_gradient_max_abs": 162.31717661541148,
        "gradient_delta": [
          -1.0477200024767561e+38,
          9.589002273515357e+37
        ],
        "gradient_explosion_ratio": 6.4547697558785564e+35,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0477200024767561e+38,
        "relative_gradient_delta": 6.4547697558785564e+35,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.324789415477426e-10,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.537876486616941e+39,
        "filterflow_gradient_max_abs": 65.61469672303252,
        "gradient_delta": [
          -8.537876486616941e+39,
          7.814037723590829e+39
        ],
        "gradient_explosion_ratio": 1.3012140439597455e+38,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.537876486616941e+39,
        "relative_gradient_delta": 1.3012140439597455e+38,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.852775876111991e-10,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.844612695514922e+41,
        "filterflow_gradient_max_abs": 353.91086072731014,
        "gradient_delta": [
          -9.844612695514922e+41,
          9.01019196417287e+41
        ],
        "gradient_explosion_ratio": 2.7816644776833334e+39,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.844612695514922e+41,
        "relative_gradient_delta": 2.7816644776833334e+39,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.191615860487218e-10,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.37577874445559e+44,
        "filterflow_gradient_max_abs": 106.57513689011893,
        "gradient_delta": [
          -3.37577874445559e+44,
          3.0895925243040614e+44
        ],
        "gradient_explosion_ratio": 3.1675105873296554e+42,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.37577874445559e+44,
        "relative_gradient_delta": 3.1675105873296554e+42,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.87274212698685e-10,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.018617422974454e+46,
        "filterflow_gradient_max_abs": 301.25080522517993,
        "gradient_delta": [
          9.018617422974454e+46,
          -8.254062106425907e+46
        ],
        "gradient_explosion_ratio": 2.993723922574477e+44,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.018617422974454e+46,
        "relative_gradient_delta": 2.993723922574477e+44,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.1155345797960763e-10,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.6053782671254444e+49,
        "filterflow_gradient_max_abs": 406.1376803574301,
        "gradient_delta": [
          -2.6053782671254444e+49,
          2.3845064932142265e+49
        ],
        "gradient_explosion_ratio": 6.4150124283778e+46,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.6053782671254444e+49,
        "relative_gradient_delta": 6.4150124283778e+46,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.641514005423232e-10,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.233712902481971e+50,
        "filterflow_gradient_max_abs": 226.31263344208014,
        "gradient_delta": [
          -2.233712902481971e+50,
          2.044349785134365e+50
        ],
        "gradient_explosion_ratio": 9.870031860389455e+47,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.233712902481971e+50,
        "relative_gradient_delta": 9.870031860389455e+47,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.090381697911653e-10,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1957483023909774e+52,
        "filterflow_gradient_max_abs": 6.85443174851973,
        "gradient_delta": [
          2.1957483023909774e+52,
          -2.0096026251951146e+52
        ],
        "gradient_explosion_ratio": 3.2033994690590756e+51,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1957483023909774e+52,
        "relative_gradient_delta": 3.2033994690590756e+51,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.083187369971711e-10,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.218891825234532e+55,
        "filterflow_gradient_max_abs": 80.80287856491722,
        "gradient_delta": [
          4.218891825234532e+55,
          -3.861233740864992e+55
        ],
        "gradient_explosion_ratio": 5.221214763834267e+53,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.218891825234532e+55,
        "relative_gradient_delta": 5.221214763834267e+53,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.413411940935475e-10,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.711857919423923e+57,
        "filterflow_gradient_max_abs": 195.04750763879625,
        "gradient_delta": [
          -1.711857919423923e+57,
          1.566734527298207e+57
        ],
        "gradient_explosion_ratio": 8.77662032264504e+54,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.711857919423923e+57,
        "relative_gradient_delta": 8.77662032264504e+54,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.915747808809101e-10,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.9262913890224845e+59,
        "filterflow_gradient_max_abs": 227.99933783381496,
        "gradient_delta": [
          -4.9262913890224845e+59,
          4.508663194455116e+59
        ],
        "gradient_explosion_ratio": 2.160660393063588e+57,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.9262913890224845e+59,
        "relative_gradient_delta": 2.160660393063588e+57,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4428105638871784e-10,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.3074629337885355e+62,
        "filterflow_gradient_max_abs": 498.30983956509795,
        "gradient_delta": [
          -1.3074629337885355e+62,
          1.1966222762681397e+62
        ],
        "gradient_explosion_ratio": 2.6237951370368873e+59,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.3074629337885355e+62,
        "relative_gradient_delta": 2.6237951370368873e+59,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.725002776875044e-10,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.011096995688774e+65,
        "filterflow_gradient_max_abs": 348.59095258355785,
        "gradient_delta": [
          -1.011096995688774e+65,
          9.253808710262363e+64
        ],
        "gradient_explosion_ratio": 2.900525639564361e+62,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.011096995688774e+65,
        "relative_gradient_delta": 2.900525639564361e+62,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.749836080009118e-10,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2472703113779772e+67,
        "filterflow_gradient_max_abs": 24.53415070247347,
        "gradient_delta": [
          -2.2472703113779772e+67,
          2.0567571329269384e+67
        ],
        "gradient_explosion_ratio": 9.159764031087546e+65,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2472703113779772e+67,
        "relative_gradient_delta": 9.159764031087546e+65,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9053560385582387e-10,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.066673336445966e+69,
        "filterflow_gradient_max_abs": 743.4955982984612,
        "gradient_delta": [
          -4.066673336445966e+69,
          3.721919588083213e+69
        ],
        "gradient_explosion_ratio": 5.469666997024349e+66,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.066673336445966e+69,
        "relative_gradient_delta": 5.469666997024349e+66,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3861267689208034e-10,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.4522903324417857e+71,
        "filterflow_gradient_max_abs": 660.4154280128698,
        "gradient_delta": [
          2.4522903324417857e+71,
          -2.2443965051239617e+71
        ],
        "gradient_explosion_ratio": 3.7132541555252655e+68,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.4522903324417857e+71,
        "relative_gradient_delta": 3.7132541555252655e+68,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2236966995260445e-10,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2875069985878292e+74,
        "filterflow_gradient_max_abs": 151.38043625809377,
        "gradient_delta": [
          1.2875069985878292e+74,
          -1.1783581127760638e+74
        ],
        "gradient_explosion_ratio": 8.505108258458932e+71,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2875069985878292e+74,
        "relative_gradient_delta": 8.505108258458932e+71,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.503508428868372e-10,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2704129601021964e+76,
        "filterflow_gradient_max_abs": 78.34314644911912,
        "gradient_delta": [
          -1.2704129601021964e+76,
          1.1627132277773018e+76
        ],
        "gradient_explosion_ratio": 1.6216006347502026e+74,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2704129601021964e+76,
        "relative_gradient_delta": 1.6216006347502026e+74,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4379963886312908e-10,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7829178017295549e+78,
        "filterflow_gradient_max_abs": 375.1405380302191,
        "gradient_delta": [
          -1.7829178017295549e+78,
          1.6317702803727792e+78
        ],
        "gradient_explosion_ratio": 4.752666323643044e+75,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7829178017295549e+78,
        "relative_gradient_delta": 4.752666323643044e+75,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.290931888637715e-10,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.8324806759874804e+80,
        "filterflow_gradient_max_abs": 190.9613749711765,
        "gradient_delta": [
          -2.8324806759874804e+80,
          2.592356070663695e+80
        ],
        "gradient_explosion_ratio": 1.4832741314388902e+78,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.8324806759874804e+80,
        "relative_gradient_delta": 1.4832741314388902e+78,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.651177055668086e-10,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.8173229313451234e+83,
        "filterflow_gradient_max_abs": 677.2028181986615,
        "gradient_delta": [
          -1.8173229313451234e+83,
          1.663258702298376e+83
        ],
        "gradient_explosion_ratio": 2.6835726055883023e+80,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.8173229313451234e+83,
        "relative_gradient_delta": 2.6835726055883023e+80,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.92969196177728e-10,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.959011440979987e+85,
        "filterflow_gradient_max_abs": 152.6174741556563,
        "gradient_delta": [
          4.959011440979987e+85,
          -4.538609397231347e+85
        ],
        "gradient_explosion_ratio": 3.2493077666337435e+83,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.959011440979987e+85,
        "relative_gradient_delta": 3.2493077666337435e+83,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.625100468227174e-11,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.934684694730494e+86,
        "filterflow_gradient_max_abs": 207.0601214499801,
        "gradient_delta": [
          -8.934684694730494e+86,
          8.177243468669667e+86
        ],
        "gradient_explosion_ratio": 4.315019537399848e+84,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.934684694730494e+86,
        "relative_gradient_delta": 4.315019537399848e+84,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.438458406890277e-10,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5117528547116902e+90,
        "filterflow_gradient_max_abs": 546.4746634801378,
        "gradient_delta": [
          1.5117528547116902e+90,
          -1.3835934428354033e+90
        ],
        "gradient_explosion_ratio": 2.7663731838624144e+87,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5117528547116902e+90,
        "relative_gradient_delta": 2.7663731838624144e+87,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.842170943040401e-14,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.252698362249619e+92,
        "filterflow_gradient_max_abs": 272.67443106070385,
        "gradient_delta": [
          -5.252698362249619e+92,
          4.8073989002565903e+92
        ],
        "gradient_explosion_ratio": 1.9263626376028793e+90,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.252698362249619e+92,
        "relative_gradient_delta": 1.9263626376028793e+90,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.5509905299259117e-10,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.7787628767846796e+95,
        "filterflow_gradient_max_abs": 949.676068984666,
        "gradient_delta": [
          -2.7787628767846796e+95,
          2.543192217915105e+95
        ],
        "gradient_explosion_ratio": 2.9260112658788575e+92,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.7787628767846796e+95,
        "relative_gradient_delta": 2.9260112658788575e+92,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.264737647943548e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3415696071597807e+97,
        "filterflow_gradient_max_abs": 101.55125271438094,
        "gradient_delta": [
          3.3415696071597807e+97,
          -3.0582867978946597e+97
        ],
        "gradient_explosion_ratio": 3.290525244979644e+95,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3415696071597807e+97,
        "relative_gradient_delta": 3.290525244979644e+95,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.427679308108054e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.995709080265397e+99,
        "filterflow_gradient_max_abs": 177.86655077673558,
        "gradient_delta": [
          -4.995709080265397e+99,
          4.57219598046446e+99
        ],
        "gradient_explosion_ratio": 2.8086838466532073e+97,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.995709080265397e+99,
        "relative_gradient_delta": 2.8086838466532073e+97,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3662173614648054e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0763226491970963e+101,
        "filterflow_gradient_max_abs": 135.59093315487942,
        "gradient_delta": [
          1.0763226491970963e+101,
          -9.850769953322329e+100
        ],
        "gradient_explosion_ratio": 7.938013436102408e+98,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0763226491970963e+101,
        "relative_gradient_delta": 7.938013436102408e+98,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.345853206657921e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1370101729440923e+104,
        "filterflow_gradient_max_abs": 133.34005587444113,
        "gradient_delta": [
          -1.1370101729440923e+104,
          1.0406197116278036e+104
        ],
        "gradient_explosion_ratio": 8.52714636639084e+101,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1370101729440923e+104,
        "relative_gradient_delta": 8.52714636639084e+101,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4315730823000195e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.281724296764651e+105,
        "filterflow_gradient_max_abs": 522.1712070050679,
        "gradient_delta": [
          -3.281724296764651e+105,
          3.00351489600006e+105
        ],
        "gradient_explosion_ratio": 6.284766859488674e+102,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.281724296764651e+105,
        "relative_gradient_delta": 6.284766859488674e+102,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3040164503763663e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.22188117599524e+107,
        "filterflow_gradient_max_abs": 6.415333698704999,
        "gradient_delta": [
          6.22188117599524e+107,
          -5.69441887963212e+107
        ],
        "gradient_explosion_ratio": 9.698452907057961e+106,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.22188117599524e+107,
        "relative_gradient_delta": 9.698452907057961e+106,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1294503110548249e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4073159210710778e+109,
        "filterflow_gradient_max_abs": 197.4197643907813,
        "gradient_delta": [
          1.4073159210710778e+109,
          -1.2880101891807863e+109
        ],
        "gradient_explosion_ratio": 7.128546249733007e+106,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4073159210710778e+109,
        "relative_gradient_delta": 7.128546249733007e+106,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0837482022907352e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.314535927672507e+111,
        "filterflow_gradient_max_abs": 315.57269054843385,
        "gradient_delta": [
          5.314535927672507e+111,
          -4.863994163016256e+111
        ],
        "gradient_explosion_ratio": 1.6840924727790527e+109,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.314535927672507e+111,
        "relative_gradient_delta": 1.6840924727790527e+109,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1401937172195176e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.3486645956004206e+113,
        "filterflow_gradient_max_abs": 60.009881084342744,
        "gradient_delta": [
          -4.3486645956004206e+113,
          3.980004933220841e+113
        ],
        "gradient_explosion_ratio": 7.246580924712141e+111,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.3486645956004206e+113,
        "relative_gradient_delta": 7.246580924712141e+111,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1782930187109741e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2532211877297267e+115,
        "filterflow_gradient_max_abs": 147.6346164990015,
        "gradient_delta": [
          -2.2532211877297267e+115,
          2.062203521484468e+115
        ],
        "gradient_explosion_ratio": 1.5262146786183887e+113,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2532211877297267e+115,
        "relative_gradient_delta": 1.5262146786183887e+113,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2933298876305344e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.947764696657184e+117,
        "filterflow_gradient_max_abs": 512.611395216775,
        "gradient_delta": [
          -8.947764696657184e+117,
          8.18921460855451e+117
        ],
        "gradient_explosion_ratio": 1.7455259052275496e+115,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.947764696657184e+117,
        "relative_gradient_delta": 1.7455259052275496e+115,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.554774583695689e-10,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.0520159329832286e+120,
        "filterflow_gradient_max_abs": 87.5818933878043,
        "gradient_delta": [
          -5.0520159329832286e+120,
          4.6237293987505834e+120
        ],
        "gradient_explosion_ratio": 5.76833377033011e+118,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.0520159329832286e+120,
        "relative_gradient_delta": 5.76833377033011e+118,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0234515457341331e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.169293781890203e+122,
        "filterflow_gradient_max_abs": 57.78168821303872,
        "gradient_delta": [
          -6.169293781890203e+122,
          5.646289601468211e+122
        ],
        "gradient_explosion_ratio": 1.0676901234080025e+121,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.169293781890203e+122,
        "relative_gradient_delta": 1.0676901234080025e+121,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.412825991399586e-10,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.4272032060823065e+126,
        "filterflow_gradient_max_abs": 738.8517276846384,
        "gradient_delta": [
          -1.4272032060823065e+126,
          1.30621152219073e+126
        ],
        "gradient_explosion_ratio": 1.931650360424514e+123,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.4272032060823065e+126,
        "relative_gradient_delta": 1.931650360424514e+123,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1248317832723842e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0386183533564634e+128,
        "filterflow_gradient_max_abs": 1019.3972961264672,
        "gradient_delta": [
          2.0386183533564634e+128,
          -1.865793722404334e+128
        ],
        "gradient_explosion_ratio": 1.9998271146125848e+125,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0386183533564634e+128,
        "relative_gradient_delta": 1.9998271146125848e+125,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.905196414663806e-10,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.461989013123064e+130,
        "filterflow_gradient_max_abs": 122.24440141690243,
        "gradient_delta": [
          -2.461989013123064e+130,
          2.2532729766463773e+130
        ],
        "gradient_explosion_ratio": 2.0139891762623093e+128,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.461989013123064e+130,
        "relative_gradient_delta": 2.0139891762623093e+128,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.500755489469157e-10,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.384509284157884e+133,
        "filterflow_gradient_max_abs": 682.5428603420182,
        "gradient_delta": [
          -6.384509284157884e+133,
          5.843260129293586e+133
        ],
        "gradient_explosion_ratio": 9.354004935248526e+130,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.384509284157884e+133,
        "relative_gradient_delta": 9.354004935248526e+130,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.193943136167945e-10,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.210627472182697e+136,
        "filterflow_gradient_max_abs": 309.19172560146353,
        "gradient_delta": [
          2.210627472182697e+136,
          -2.023220704052905e+136
        ],
        "gradient_explosion_ratio": 7.149698032450301e+133,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.210627472182697e+136,
        "relative_gradient_delta": 7.149698032450301e+133,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.828742016296019e-10,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.905757827055886e+137,
        "filterflow_gradient_max_abs": 66.90489544481636,
        "gradient_delta": [
          4.905757827055886e+137,
          -4.4898703782817975e+137
        ],
        "gradient_explosion_ratio": 7.332434785885273e+135,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.905757827055886e+137,
        "relative_gradient_delta": 7.332434785885273e+135,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.207851927480078e-10,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0259549709715207e+141,
        "filterflow_gradient_max_abs": 750.3754788438333,
        "gradient_delta": [
          1.0259549709715207e+141,
          -9.389792558065294e+140
        ],
        "gradient_explosion_ratio": 1.3672554606292519e+138,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0259549709715207e+141,
        "relative_gradient_delta": 1.3672554606292519e+138,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.709637207473861e-10,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.4412988882499105e+143,
        "filterflow_gradient_max_abs": 347.8401730350442,
        "gradient_delta": [
          4.4412988882499105e+143,
          -4.064786119174651e+143
        ],
        "gradient_explosion_ratio": 1.2768217223151102e+141,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.4412988882499105e+143,
        "relative_gradient_delta": 1.2768217223151102e+141,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.423448439818458e-10,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.9092939321024668e+146,
        "filterflow_gradient_max_abs": 441.50385013274905,
        "gradient_delta": [
          -1.9092939321024668e+146,
          1.7474328271774243e+146
        ],
        "gradient_explosion_ratio": 4.324523855292293e+143,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.9092939321024668e+146,
        "relative_gradient_delta": 4.324523855292293e+143,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.418084007644211e-10,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.628460329473863e+147,
        "filterflow_gradient_max_abs": 216.5606746935064,
        "gradient_delta": [
          -5.628460329473863e+147,
          5.1513055066162826e+147
        ],
        "gradient_explosion_ratio": 2.599022346711701e+145,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.628460329473863e+147,
        "relative_gradient_delta": 2.599022346711701e+145,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.252687505068025e-10,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.5405294530595558e+151,
        "filterflow_gradient_max_abs": 592.4376179231792,
        "gradient_delta": [
          -2.5405294530595558e+151,
          2.3251551215054734e+151
        ],
        "gradient_explosion_ratio": 4.2882649180271726e+148,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.5405294530595558e+151,
        "relative_gradient_delta": 4.2882649180271726e+148,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.707559118192876e-10,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.157258179440637e+153,
        "filterflow_gradient_max_abs": 1021.9536107722753,
        "gradient_delta": [
          -4.157258179440637e+153,
          3.80482506735194e+153
        ],
        "gradient_explosion_ratio": 4.067951945782606e+150,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.157258179440637e+153,
        "relative_gradient_delta": 4.067951945782606e+150,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.629843589209486e-10,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.647142865869326e+156,
        "filterflow_gradient_max_abs": 416.36976112409496,
        "gradient_delta": [
          -4.647142865869326e+156,
          4.2531795968477544e+156
        ],
        "gradient_explosion_ratio": 1.1161095977102645e+154,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.647142865869326e+156,
        "relative_gradient_delta": 1.1161095977102645e+154,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.8334494446608e-10,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.216287402706544e+159,
        "filterflow_gradient_max_abs": 73.20765898029507,
        "gradient_delta": [
          -2.216287402706544e+159,
          2.0284008118564346e+159
        ],
        "gradient_explosion_ratio": 3.0273982716795943e+157,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.216287402706544e+159,
        "relative_gradient_delta": 3.0273982716795943e+157,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.958771336940117e-10,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.442812319829652e+161,
        "filterflow_gradient_max_abs": 18.775557058598526,
        "gradient_delta": [
          -2.442812319829652e+161,
          2.23572199467645e+161
        ],
        "gradient_explosion_ratio": 1.3010598365766902e+160,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.442812319829652e+161,
        "relative_gradient_delta": 1.3010598365766902e+160,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.100187187665142e-10,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.370972282466436e+163,
        "filterflow_gradient_max_abs": 489.4717191114149,
        "gradient_delta": [
          -4.370972282466436e+163,
          4.0004214776159313e+163
        ],
        "gradient_explosion_ratio": 8.929979224134709e+160,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.370972282466436e+163,
        "relative_gradient_delta": 8.929979224134709e+160,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.418758857762441e-10,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.701029742543945e+166,
        "filterflow_gradient_max_abs": 603.1903641588457,
        "gradient_delta": [
          6.701029742543945e+166,
          -6.13294744781347e+166
        ],
        "gradient_explosion_ratio": 1.1109311654685649e+164,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.701029742543945e+166,
        "relative_gradient_delta": 1.1109311654685649e+164,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0115144277733634e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.31636058388261e+168,
        "filterflow_gradient_max_abs": 924.7685421225882,
        "gradient_delta": [
          -9.31636058388261e+168,
          8.52656264201892e+168
        ],
        "gradient_explosion_ratio": 1.0074262001277747e+166,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.31636058388261e+168,
        "relative_gradient_delta": 1.0074262001277747e+166,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2003482652289676e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.40524554278159e+171,
        "filterflow_gradient_max_abs": 712.4012104561216,
        "gradient_delta": [
          8.40524554278159e+171,
          -7.692687718213004e+171
        ],
        "gradient_explosion_ratio": 1.1798471731119114e+169,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.40524554278159e+171,
        "relative_gradient_delta": 1.1798471731119114e+169,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.9136194850943866e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.948305982099034e+174,
        "filterflow_gradient_max_abs": 1186.5395908091443,
        "gradient_delta": [
          6.948305982099034e+174,
          -6.359260751969701e+174
        ],
        "gradient_explosion_ratio": 5.855941121493243e+171,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.948305982099034e+174,
        "relative_gradient_delta": 5.855941121493243e+171,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.708955086447531e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.29549912269116e+177,
        "filterflow_gradient_max_abs": 155.19429188795652,
        "gradient_delta": [
          9.29549912269116e+177,
          -8.507469718977633e+177
        ],
        "gradient_explosion_ratio": 5.98958828292609e+175,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.29549912269116e+177,
        "relative_gradient_delta": 5.98958828292609e+175,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.22875973022019e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2515780967828088e+180,
        "filterflow_gradient_max_abs": 232.51294890916668,
        "gradient_delta": [
          -1.2515780967828088e+180,
          1.1454750970093954e+180
        ],
        "gradient_explosion_ratio": 5.382831806377155e+177,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2515780967828088e+180,
        "relative_gradient_delta": 5.382831806377155e+177,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.486573056463385e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.822971113513915e+181,
        "filterflow_gradient_max_abs": 1518.8797828290087,
        "gradient_delta": [
          -6.822971113513915e+181,
          6.24455119359676e+181
        ],
        "gradient_explosion_ratio": 4.49210740089364e+178,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.822971113513915e+181,
        "relative_gradient_delta": 4.49210740089364e+178,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.5804499627120094e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.296667548227325e+185,
        "filterflow_gradient_max_abs": 92.4227988005718,
        "gradient_delta": [
          3.296667548227325e+185,
          -3.017191327748786e+185
        ],
        "gradient_explosion_ratio": 3.5669419136947077e+183,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.296667548227325e+185,
        "relative_gradient_delta": 3.5669419136947077e+183,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.631609039686737e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.8592871742432256e+187,
        "filterflow_gradient_max_abs": 495.480272228227,
        "gradient_delta": [
          -4.8592871742432256e+187,
          4.447339292386716e+187
        ],
        "gradient_explosion_ratio": 9.807226334946695e+184,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.8592871742432256e+187,
        "relative_gradient_delta": 9.807226334946695e+184,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.181977596497745e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.201050747742704e+190,
        "filterflow_gradient_max_abs": 1905.453488616431,
        "gradient_delta": [
          6.201050747742704e+190,
          -5.6753543587007914e+190
        ],
        "gradient_explosion_ratio": 3.2543700409320142e+187,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.201050747742704e+190,
        "relative_gradient_delta": 3.2543700409320142e+187,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.158671794764814e-09,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.1681588477283544e+193,
        "filterflow_gradient_max_abs": 536.1521590308598,
        "gradient_delta": [
          -5.1681588477283544e+193,
          4.730026254597294e+193
        ],
        "gradient_explosion_ratio": 9.639350995191806e+190,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.1681588477283544e+193,
        "relative_gradient_delta": 9.639350995191806e+190,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.624389925491414e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.7363791291437003e+195,
        "filterflow_gradient_max_abs": 85.09097085867334,
        "gradient_delta": [
          -2.7363791291437003e+195,
          2.504401568282078e+195
        ],
        "gradient_explosion_ratio": 3.2158278387592054e+193,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.7363791291437003e+195,
        "relative_gradient_delta": 3.2158278387592054e+193,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.351314141284092e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.20085726236264e+198,
        "filterflow_gradient_max_abs": 286.3674760142073,
        "gradient_delta": [
          1.20085726236264e+198,
          -1.0990541402371524e+198
        ],
        "gradient_explosion_ratio": 4.1934135785135845e+195,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.20085726236264e+198,
        "relative_gradient_delta": 4.1934135785135845e+195,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.2123888255882775e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0935194213429442e+202,
        "filterflow_gradient_max_abs": 1646.6707953160178,
        "gradient_delta": [
          -1.0935194213429442e+202,
          1.0008159047080509e+202
        ],
        "gradient_explosion_ratio": 6.640789552189049e+198,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0935194213429442e+202,
        "relative_gradient_delta": 6.640789552189049e+198,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.9354371134977555e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.027055526118829e+205,
        "filterflow_gradient_max_abs": 1706.2194857616348,
        "gradient_delta": [
          1.027055526118829e+205,
          -9.39986510980911e+204
        ],
        "gradient_explosion_ratio": 6.01948069805547e+201,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.027055526118829e+205,
        "relative_gradient_delta": 6.01948069805547e+201,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.4229368490487104e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.361025584964419e+207,
        "filterflow_gradient_max_abs": 491.76925290563014,
        "gradient_delta": [
          8.361025584964419e+207,
          -7.652216523806066e+207
        ],
        "gradient_explosion_ratio": 1.7001928314068242e+205,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.361025584964419e+207,
        "relative_gradient_delta": 1.7001928314068242e+205,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.928541213506833e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5521004253385232e+209,
        "filterflow_gradient_max_abs": 953.0377691516383,
        "gradient_delta": [
          1.5521004253385232e+209,
          -1.420520533119791e+209
        ],
        "gradient_explosion_ratio": 1.628582282442122e+206,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5521004253385232e+209,
        "relative_gradient_delta": 1.628582282442122e+206,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.896453103559907e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.52842417970598e+212,
        "filterflow_gradient_max_abs": 1943.4208738111502,
        "gradient_delta": [
          8.52842417970598e+212,
          -7.805423840268149e+212
        ],
        "gradient_explosion_ratio": 4.388356786032298e+209,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.52842417970598e+212,
        "relative_gradient_delta": 4.388356786032298e+209,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.690761887919507e-09,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0723038706470447e+216,
        "filterflow_gradient_max_abs": 950.6655619127545,
        "gradient_delta": [
          2.0723038706470447e+216,
          -1.896623537407829e+216
        ],
        "gradient_explosion_ratio": 2.1798453143474933e+213,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0723038706470447e+216,
        "relative_gradient_delta": 2.1798453143474933e+213,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.408061719615944e-09,
        "scalar_within_tolerance": true,
        "time_index": 99,
        "transport_status": "computed_raw_transport_gradient"
      }
    ]
  },
  {
    "final_bayesfilter_gradient_diag": [
      3.904188635142209e+214,
      -3.819553882087435e+214
    ],
    "final_bayesfilter_gradient_max_abs": 3.904188635142209e+214,
    "final_filterflow_gradient_diag": [
      7019.871883303286,
      713.5990730344417
    ],
    "final_filterflow_gradient_max_abs": 7019.871883303286,
    "final_gradient_delta": [
      3.904188635142209e+214,
      -3.819553882087435e+214
    ],
    "final_gradient_within_tolerance": false,
    "final_max_abs_gradient_delta": 3.904188635142209e+214,
    "final_relative_gradient_delta": 5.56162377326044e+210,
    "final_scalar_delta": 7.407919611068792e-09,
    "finite_values": true,
    "first_gradient_explosion": {
      "bayesfilter_gradient_max_abs": 8926508.791244011,
      "filterflow_gradient_max_abs": 0.7972582915878877,
      "gradient_explosion_ratio": 8926508.791244011,
      "resampling_flag": [
        true
      ],
      "status": "explosion",
      "time_index": 8,
      "transport_status": "computed_raw_transport_gradient"
    },
    "first_gradient_failure": {
      "gradient_explosion_ratio": 1.0042001498852535,
      "max_abs_gradient_delta": 0.03721532831976404,
      "relative_gradient_delta": 0.0042001498852535695,
      "resampling_flag": [
        true
      ],
      "scalar_delta": 1.8406609569865395e-11,
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
        "bayesfilter_gradient_max_abs": 0.008924445612040184,
        "filterflow_gradient_max_abs": 0.008924445612040184,
        "gradient_delta": [
          0.0,
          -5.795395272864551e-20
        ],
        "gradient_explosion_ratio": 0.008924445612040184,
        "gradient_within_tolerance": true,
        "max_abs_gradient_delta": 5.795395272864551e-20,
        "relative_gradient_delta": 5.795395272864551e-20,
        "resampling_flag": [
          false
        ],
        "scalar_delta": 0.0,
        "scalar_within_tolerance": true,
        "time_index": 0,
        "transport_status": "not_triggered"
      },
      {
        "bayesfilter_gradient_max_abs": 8.897691581899295,
        "filterflow_gradient_max_abs": 8.860476253579531,
        "gradient_delta": [
          -0.03721532831976404,
          0.037074187935947266
        ],
        "gradient_explosion_ratio": 1.0042001498852535,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 0.03721532831976404,
        "relative_gradient_delta": 0.0042001498852535695,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.8406609569865395e-11,
        "scalar_within_tolerance": true,
        "time_index": 1,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.502637734556598,
        "filterflow_gradient_max_abs": 1.4056099396090884,
        "gradient_delta": [
          -7.908247674165686,
          -0.8771424663336299
        ],
        "gradient_explosion_ratio": 4.626203579895739,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.908247674165686,
        "relative_gradient_delta": 5.626203579895739,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.5511147921642987e-11,
        "scalar_within_tolerance": true,
        "time_index": 2,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 64.59304962858053,
        "filterflow_gradient_max_abs": 14.864972477668916,
        "gradient_delta": [
          -76.16683491500798,
          64.59304962858053
        ],
        "gradient_explosion_ratio": 4.345319153844127,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 76.16683491500798,
        "relative_gradient_delta": 5.12391361836899,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.2442492308982764e-11,
        "scalar_within_tolerance": true,
        "time_index": 3,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 32.75752054059524,
        "filterflow_gradient_max_abs": 15.00462728219541,
        "gradient_delta": [
          2.3094910353148475,
          32.75752054059524
        ],
        "gradient_explosion_ratio": 2.1831612291673204,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 32.75752054059524,
        "relative_gradient_delta": 2.1831612291673204,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.779998453661392e-11,
        "scalar_within_tolerance": true,
        "time_index": 4,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5412.076133461694,
        "filterflow_gradient_max_abs": 6.525931066391355,
        "gradient_delta": [
          -5405.550202395302,
          5090.331132024891
        ],
        "gradient_explosion_ratio": 829.3186180488435,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5405.550202395302,
        "relative_gradient_delta": 828.3186180488435,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.1093350116861984e-11,
        "scalar_within_tolerance": true,
        "time_index": 5,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 132278.05127100894,
        "filterflow_gradient_max_abs": 2.686919378388484,
        "gradient_delta": [
          -132280.73819038732,
          129672.6566711459
        ],
        "gradient_explosion_ratio": 49230.375996746305,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 132280.73819038732,
        "relative_gradient_delta": 49231.375996746305,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4224179873708636e-11,
        "scalar_within_tolerance": true,
        "time_index": 6,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 253933.72990601152,
        "filterflow_gradient_max_abs": 24.973165642495765,
        "gradient_delta": [
          253958.70307165402,
          -234388.2501974079
        ],
        "gradient_explosion_ratio": 10168.263549011319,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 253958.70307165402,
        "relative_gradient_delta": 10169.263549011319,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.5496940376542625e-11,
        "scalar_within_tolerance": true,
        "time_index": 7,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8926508.791244011,
        "filterflow_gradient_max_abs": 0.7972582915878877,
        "gradient_delta": [
          8854536.979692169,
          -8926508.791244011
        ],
        "gradient_explosion_ratio": 8926508.791244011,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8926508.791244011,
        "relative_gradient_delta": 8926508.791244011,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.66524613279762e-11,
        "scalar_within_tolerance": true,
        "time_index": 8,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 185699026.36284417,
        "filterflow_gradient_max_abs": 49.77299487676166,
        "gradient_delta": [
          -185699076.13583905,
          181943301.65189776
        ],
        "gradient_explosion_ratio": 3730919.283089886,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 185699076.13583905,
        "relative_gradient_delta": 3730920.283089886,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.581402089977928e-11,
        "scalar_within_tolerance": true,
        "time_index": 9,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 37042281569.41087,
        "filterflow_gradient_max_abs": 91.01474473671405,
        "gradient_delta": [
          37042281478.396126,
          -36242082571.19103
        ],
        "gradient_explosion_ratio": 406992094.26523334,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 37042281478.396126,
        "relative_gradient_delta": 406992093.2652333,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.424994118489849e-11,
        "scalar_within_tolerance": true,
        "time_index": 10,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1034732710770.078,
        "filterflow_gradient_max_abs": 28.00263902728941,
        "gradient_delta": [
          1034732710798.0807,
          -1016813376706.4877
        ],
        "gradient_explosion_ratio": 36951256978.37622,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1034732710798.0807,
        "relative_gradient_delta": 36951256979.37622,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.85451720225683e-11,
        "scalar_within_tolerance": true,
        "time_index": 11,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 21619444469145.65,
        "filterflow_gradient_max_abs": 40.13671871067378,
        "gradient_delta": [
          21619444469105.51,
          -21181017255574.883
        ],
        "gradient_explosion_ratio": 538645040342.9782,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 21619444469105.51,
        "relative_gradient_delta": 538645040341.9782,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3077183780296764e-10,
        "scalar_within_tolerance": true,
        "time_index": 12,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 582324664903929.4,
        "filterflow_gradient_max_abs": 49.010874255508995,
        "gradient_delta": [
          -582324664903978.4,
          566871074033519.0
        ],
        "gradient_explosion_ratio": 11881540040850.71,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 582324664903978.4,
        "relative_gradient_delta": 11881540040851.71,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4137313542050833e-10,
        "scalar_within_tolerance": true,
        "time_index": 13,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.315321772385005e+16,
        "filterflow_gradient_max_abs": 21.29035436921441,
        "gradient_delta": [
          9.315321772385003e+16,
          -9.114803907305067e+16
        ],
        "gradient_explosion_ratio": 4375371875376037.0,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.315321772385003e+16,
        "relative_gradient_delta": 4375371875376036.0,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3353940175875323e-10,
        "scalar_within_tolerance": true,
        "time_index": 14,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.3106055965536845e+17,
        "filterflow_gradient_max_abs": 27.042811971633515,
        "gradient_delta": [
          -5.3106055965536845e+17,
          5.1694508969794726e+17
        ],
        "gradient_explosion_ratio": 1.9637771405297016e+16,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.3106055965536845e+17,
        "relative_gradient_delta": 1.9637771405297016e+16,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.525606307950511e-10,
        "scalar_within_tolerance": true,
        "time_index": 15,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.5467303033946096e+19,
        "filterflow_gradient_max_abs": 18.468136147749064,
        "gradient_delta": [
          -2.5467303033946096e+19,
          2.489457465568139e+19
        ],
        "gradient_explosion_ratio": 1.3789860996368118e+18,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.5467303033946096e+19,
        "relative_gradient_delta": 1.3789860996368118e+18,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.7488588355263346e-10,
        "scalar_within_tolerance": true,
        "time_index": 16,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.285582408817603e+20,
        "filterflow_gradient_max_abs": 102.94637935328883,
        "gradient_delta": [
          6.285582408817603e+20,
          -6.153656289223864e+20
        ],
        "gradient_explosion_ratio": 6.105685744660234e+18,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.285582408817603e+20,
        "relative_gradient_delta": 6.105685744660234e+18,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3816503496855148e-10,
        "scalar_within_tolerance": true,
        "time_index": 17,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5440831337054595e+23,
        "filterflow_gradient_max_abs": 113.77902775418237,
        "gradient_delta": [
          -1.5440831337054595e+23,
          1.5106405645011746e+23
        ],
        "gradient_explosion_ratio": 1.3570894075852227e+21,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5440831337054595e+23,
        "relative_gradient_delta": 1.3570894075852227e+21,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.3455015707440907e-10,
        "scalar_within_tolerance": true,
        "time_index": 18,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3665246444544312e+25,
        "filterflow_gradient_max_abs": 165.42250820864194,
        "gradient_delta": [
          2.3665246444544312e+25,
          -2.3154169709221254e+25
        ],
        "gradient_explosion_ratio": 1.4305941011785482e+23,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3665246444544312e+25,
        "relative_gradient_delta": 1.4305941011785482e+23,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.92866184029117e-10,
        "scalar_within_tolerance": true,
        "time_index": 19,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.1686343948445206e+27,
        "filterflow_gradient_max_abs": 73.77440324184383,
        "gradient_delta": [
          -2.1686343948445206e+27,
          2.1219595251578407e+27
        ],
        "gradient_explosion_ratio": 2.9395485419724833e+25,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.1686343948445206e+27,
        "relative_gradient_delta": 2.9395485419724833e+25,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4417447497835383e-10,
        "scalar_within_tolerance": true,
        "time_index": 20,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.2954662364620604e+29,
        "filterflow_gradient_max_abs": 217.86217342911775,
        "gradient_delta": [
          -5.2954662364620604e+29,
          5.1811717345788046e+29
        ],
        "gradient_explosion_ratio": 2.4306496869613575e+27,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.2954662364620604e+29,
        "relative_gradient_delta": 2.4306496869613575e+27,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.974509693056461e-10,
        "scalar_within_tolerance": true,
        "time_index": 21,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.602674462543881e+31,
        "filterflow_gradient_max_abs": 165.63087578642663,
        "gradient_delta": [
          3.602674462543881e+31,
          -3.5248194628941374e+31
        ],
        "gradient_explosion_ratio": 2.175122509881167e+29,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.602674462543881e+31,
        "relative_gradient_delta": 2.175122509881167e+29,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.2155079427175224e-10,
        "scalar_within_tolerance": true,
        "time_index": 22,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.87562773334145e+33,
        "filterflow_gradient_max_abs": 20.952482372929534,
        "gradient_delta": [
          6.87562773334145e+33,
          -6.727179808915495e+33
        ],
        "gradient_explosion_ratio": 3.2815337156540055e+32,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.87562773334145e+33,
        "relative_gradient_delta": 3.2815337156540055e+32,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.807603204426414e-10,
        "scalar_within_tolerance": true,
        "time_index": 23,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1895408731859126e+35,
        "filterflow_gradient_max_abs": 45.60764934214221,
        "gradient_delta": [
          1.1895408731859126e+35,
          -1.1637886831574663e+35
        ],
        "gradient_explosion_ratio": 2.608204742722308e+33,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1895408731859126e+35,
        "relative_gradient_delta": 2.608204742722308e+33,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.035900585426134e-10,
        "scalar_within_tolerance": true,
        "time_index": 24,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.092968985711093e+35,
        "filterflow_gradient_max_abs": 95.80515251122853,
        "gradient_delta": [
          2.092968985711093e+35,
          -2.0490933224139807e+35
        ],
        "gradient_explosion_ratio": 2.184610045337377e+33,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.092968985711093e+35,
        "relative_gradient_delta": 2.184610045337377e+33,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.194777941142092e-10,
        "scalar_within_tolerance": true,
        "time_index": 25,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.392215457627498e+38,
        "filterflow_gradient_max_abs": 162.31717661541148,
        "gradient_delta": [
          -2.392215457627498e+38,
          2.340473323014683e+38
        ],
        "gradient_explosion_ratio": 1.4737907025671892e+36,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.392215457627498e+38,
        "relative_gradient_delta": 1.4737907025671892e+36,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.324789415477426e-10,
        "scalar_within_tolerance": true,
        "time_index": 26,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.366644683184246e+40,
        "filterflow_gradient_max_abs": 65.61469672303252,
        "gradient_delta": [
          -4.366644683184246e+40,
          4.27205641091717e+40
        ],
        "gradient_explosion_ratio": 6.654979602536876e+38,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.366644683184246e+40,
        "relative_gradient_delta": 6.654979602536876e+38,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.852775876111991e-10,
        "scalar_within_tolerance": true,
        "time_index": 27,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 9.219185742814344e+42,
        "filterflow_gradient_max_abs": 353.91086072731014,
        "gradient_delta": [
          9.219185742814344e+42,
          -9.01912803503479e+42
        ],
        "gradient_explosion_ratio": 2.604945698436129e+40,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 9.219185742814344e+42,
        "relative_gradient_delta": 2.604945698436129e+40,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.191615860487218e-10,
        "scalar_within_tolerance": true,
        "time_index": 28,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.1403583610821243e+45,
        "filterflow_gradient_max_abs": 106.57513689011893,
        "gradient_delta": [
          1.1403583610821243e+45,
          -1.1156188059991632e+45
        ],
        "gradient_explosion_ratio": 1.0700041251252215e+43,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.1403583610821243e+45,
        "relative_gradient_delta": 1.0700041251252215e+43,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.87274212698685e-10,
        "scalar_within_tolerance": true,
        "time_index": 29,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.8575403821986467e+47,
        "filterflow_gradient_max_abs": 301.25080522517993,
        "gradient_delta": [
          2.8575403821986467e+47,
          -2.7955910974941915e+47
        ],
        "gradient_explosion_ratio": 9.485585872750391e+44,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.8575403821986467e+47,
        "relative_gradient_delta": 9.485585872750391e+44,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.1155345797960763e-10,
        "scalar_within_tolerance": true,
        "time_index": 30,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.233542257562334e+49,
        "filterflow_gradient_max_abs": 406.1376803574301,
        "gradient_delta": [
          -8.233542257562334e+49,
          8.055052684932331e+49
        ],
        "gradient_explosion_ratio": 2.0272785943713053e+47,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.233542257562334e+49,
        "relative_gradient_delta": 2.0272785943713053e+47,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.641514005423232e-10,
        "scalar_within_tolerance": true,
        "time_index": 31,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.27127612050947e+51,
        "filterflow_gradient_max_abs": 226.31263344208014,
        "gradient_delta": [
          -2.27127612050947e+51,
          2.2220386307325015e+51
        ],
        "gradient_explosion_ratio": 1.0036011184902562e+49,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.27127612050947e+51,
        "relative_gradient_delta": 1.0036011184902562e+49,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.090381697911653e-10,
        "scalar_within_tolerance": true,
        "time_index": 32,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.8578264264039307e+54,
        "filterflow_gradient_max_abs": 6.85443174851973,
        "gradient_delta": [
          -1.8578264264039307e+54,
          1.817552503470765e+54
        ],
        "gradient_explosion_ratio": 2.710401816759126e+53,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.8578264264039307e+54,
        "relative_gradient_delta": 2.710401816759126e+53,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.083187369971711e-10,
        "scalar_within_tolerance": true,
        "time_index": 33,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6706359401804237e+56,
        "filterflow_gradient_max_abs": 80.80287856491722,
        "gradient_delta": [
          1.6706359401804237e+56,
          -1.6344201012988188e+56
        ],
        "gradient_explosion_ratio": 2.067545079892458e+54,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6706359401804237e+56,
        "relative_gradient_delta": 2.067545079892458e+54,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.413411940935475e-10,
        "scalar_within_tolerance": true,
        "time_index": 34,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.7628590355505383e+57,
        "filterflow_gradient_max_abs": 195.04750763879625,
        "gradient_delta": [
          -2.7628590355505383e+57,
          2.7029656815294828e+57
        ],
        "gradient_explosion_ratio": 1.4165056857158154e+55,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.7628590355505383e+57,
        "relative_gradient_delta": 1.4165056857158154e+55,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.915747808809101e-10,
        "scalar_within_tolerance": true,
        "time_index": 35,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.652038620460993e+58,
        "filterflow_gradient_max_abs": 227.99933783381496,
        "gradient_delta": [
          -3.652038620460993e+58,
          3.572868341486066e+58
        ],
        "gradient_explosion_ratio": 1.6017759767016977e+56,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.652038620460993e+58,
        "relative_gradient_delta": 1.6017759767016977e+56,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.4428105638871784e-10,
        "scalar_within_tolerance": true,
        "time_index": 36,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0091363616976454e+63,
        "filterflow_gradient_max_abs": 498.30983956509795,
        "gradient_delta": [
          1.0091363616976454e+63,
          -9.872603672576495e+62
        ],
        "gradient_explosion_ratio": 2.0251182729571896e+60,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0091363616976454e+63,
        "relative_gradient_delta": 2.0251182729571896e+60,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.725002776875044e-10,
        "scalar_within_tolerance": true,
        "time_index": 37,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6540118178443532e+65,
        "filterflow_gradient_max_abs": 348.59095258355785,
        "gradient_delta": [
          1.6540118178443532e+65,
          -1.6181562536105369e+65
        ],
        "gradient_explosion_ratio": 4.744850104644881e+62,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6540118178443532e+65,
        "relative_gradient_delta": 4.744850104644881e+62,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 4.749836080009118e-10,
        "scalar_within_tolerance": true,
        "time_index": 38,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.643908711407914e+67,
        "filterflow_gradient_max_abs": 24.53415070247347,
        "gradient_delta": [
          -6.643908711407914e+67,
          6.499882480272626e+67
        ],
        "gradient_explosion_ratio": 2.7080247415037244e+66,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.643908711407914e+67,
        "relative_gradient_delta": 2.7080247415037244e+66,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.9053560385582387e-10,
        "scalar_within_tolerance": true,
        "time_index": 39,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.178971916910969e+69,
        "filterflow_gradient_max_abs": 743.4955982984612,
        "gradient_delta": [
          6.178971916910969e+69,
          -6.0450245570983776e+69
        ],
        "gradient_explosion_ratio": 8.310704099730993e+66,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.178971916910969e+69,
        "relative_gradient_delta": 8.310704099730993e+66,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3861267689208034e-10,
        "scalar_within_tolerance": true,
        "time_index": 40,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.3187612299834272e+72,
        "filterflow_gradient_max_abs": 660.4154280128698,
        "gradient_delta": [
          -2.3187612299834272e+72,
          2.268495271516468e+72
        ],
        "gradient_explosion_ratio": 3.511064599081777e+69,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.3187612299834272e+72,
        "relative_gradient_delta": 3.511064599081777e+69,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2236966995260445e-10,
        "scalar_within_tolerance": true,
        "time_index": 41,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7358178498246971e+74,
        "filterflow_gradient_max_abs": 151.38043625809377,
        "gradient_delta": [
          1.7358178498246971e+74,
          -1.6981889008638868e+74
        ],
        "gradient_explosion_ratio": 1.1466592993993232e+72,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7358178498246971e+74,
        "relative_gradient_delta": 1.1466592993993232e+72,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.503508428868372e-10,
        "scalar_within_tolerance": true,
        "time_index": 42,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.516449107465848e+76,
        "filterflow_gradient_max_abs": 78.34314644911912,
        "gradient_delta": [
          -6.516449107465848e+76,
          6.375185938051672e+76
        ],
        "gradient_explosion_ratio": 8.31782919479502e+74,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.516449107465848e+76,
        "relative_gradient_delta": 8.31782919479502e+74,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4379963886312908e-10,
        "scalar_within_tolerance": true,
        "time_index": 43,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2485914855954201e+78,
        "filterflow_gradient_max_abs": 375.1405380302191,
        "gradient_delta": [
          -1.2485914855954201e+78,
          1.2215245987704332e+78
        ],
        "gradient_explosion_ratio": 3.328329943096795e+75,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2485914855954201e+78,
        "relative_gradient_delta": 3.328329943096795e+75,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.290931888637715e-10,
        "scalar_within_tolerance": true,
        "time_index": 44,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.855155830840279e+80,
        "filterflow_gradient_max_abs": 190.9613749711765,
        "gradient_delta": [
          -5.855155830840279e+80,
          5.728228134941017e+80
        ],
        "gradient_explosion_ratio": 3.0661466653788233e+78,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.855155830840279e+80,
        "relative_gradient_delta": 3.0661466653788233e+78,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.651177055668086e-10,
        "scalar_within_tolerance": true,
        "time_index": 45,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.713228241738097e+83,
        "filterflow_gradient_max_abs": 677.2028181986615,
        "gradient_delta": [
          -5.713228241738097e+83,
          5.589377243096812e+83
        ],
        "gradient_explosion_ratio": 8.436509843439676e+80,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.713228241738097e+83,
        "relative_gradient_delta": 8.436509843439676e+80,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.92969196177728e-10,
        "scalar_within_tolerance": true,
        "time_index": 46,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.720919158761978e+85,
        "filterflow_gradient_max_abs": 152.6174741556563,
        "gradient_delta": [
          5.720919158761978e+85,
          -5.596901436913028e+85
        ],
        "gradient_explosion_ratio": 3.7485348191041e+83,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.720919158761978e+85,
        "relative_gradient_delta": 3.7485348191041e+83,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.625100468227174e-11,
        "scalar_within_tolerance": true,
        "time_index": 47,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.046383937456103e+87,
        "filterflow_gradient_max_abs": 207.0601214499801,
        "gradient_delta": [
          2.046383937456103e+87,
          -2.002022556537158e+87
        ],
        "gradient_explosion_ratio": 9.8830422928659e+84,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.046383937456103e+87,
        "relative_gradient_delta": 9.8830422928659e+84,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 3.438458406890277e-10,
        "scalar_within_tolerance": true,
        "time_index": 48,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.743117427841436e+90,
        "filterflow_gradient_max_abs": 546.4746634801378,
        "gradient_delta": [
          4.743117427841436e+90,
          -4.640296429747205e+90
        ],
        "gradient_explosion_ratio": 8.679482773520808e+87,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.743117427841436e+90,
        "relative_gradient_delta": 8.679482773520808e+87,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.842170943040401e-14,
        "scalar_within_tolerance": true,
        "time_index": 49,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.13884398543972e+91,
        "filterflow_gradient_max_abs": 272.67443106070385,
        "gradient_delta": [
          -8.13884398543972e+91,
          7.962410642896596e+91
        ],
        "gradient_explosion_ratio": 2.9848211120417883e+89,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.13884398543972e+91,
        "relative_gradient_delta": 2.9848211120417883e+89,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 2.5509905299259117e-10,
        "scalar_within_tolerance": true,
        "time_index": 50,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.8300644622348562e+96,
        "filterflow_gradient_max_abs": 949.676068984666,
        "gradient_delta": [
          1.8300644622348562e+96,
          -1.790392441154331e+96
        ],
        "gradient_explosion_ratio": 1.9270407268358844e+93,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.8300644622348562e+96,
        "relative_gradient_delta": 1.9270407268358844e+93,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.264737647943548e-09,
        "scalar_within_tolerance": true,
        "time_index": 51,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.915750193220945e+98,
        "filterflow_gradient_max_abs": 101.55125271438094,
        "gradient_delta": [
          1.915750193220945e+98,
          -1.8742206823108832e+98
        ],
        "gradient_explosion_ratio": 1.8864860275127366e+96,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.915750193220945e+98,
        "relative_gradient_delta": 1.8864860275127366e+96,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.427679308108054e-09,
        "scalar_within_tolerance": true,
        "time_index": 52,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.578485260745636e+98,
        "filterflow_gradient_max_abs": 177.86655077673558,
        "gradient_delta": [
          6.578485260745636e+98,
          -6.43587727543815e+98
        ],
        "gradient_explosion_ratio": 3.698551094636779e+96,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.578485260745636e+98,
        "relative_gradient_delta": 3.698551094636779e+96,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3662173614648054e-09,
        "scalar_within_tolerance": true,
        "time_index": 53,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0450795244193112e+102,
        "filterflow_gradient_max_abs": 135.59093315487942,
        "gradient_delta": [
          1.0450795244193112e+102,
          -1.0224243569215392e+102
        ],
        "gradient_explosion_ratio": 7.707591504113065e+99,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0450795244193112e+102,
        "relative_gradient_delta": 7.707591504113065e+99,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.345853206657921e-09,
        "scalar_within_tolerance": true,
        "time_index": 54,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.2805532946650015e+104,
        "filterflow_gradient_max_abs": 133.34005587444113,
        "gradient_delta": [
          -4.2805532946650015e+104,
          4.187759732445294e+104
        ],
        "gradient_explosion_ratio": 3.2102531130598586e+102,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.2805532946650015e+104,
        "relative_gradient_delta": 3.2102531130598586e+102,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.4315730823000195e-09,
        "scalar_within_tolerance": true,
        "time_index": 55,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.3364580640935954e+105,
        "filterflow_gradient_max_abs": 522.1712070050679,
        "gradient_delta": [
          -3.3364580640935954e+105,
          3.264130538268805e+105
        ],
        "gradient_explosion_ratio": 6.389586440872473e+102,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.3364580640935954e+105,
        "relative_gradient_delta": 6.389586440872473e+102,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.3040164503763663e-09,
        "scalar_within_tolerance": true,
        "time_index": 56,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.4117330514373793e+108,
        "filterflow_gradient_max_abs": 6.415333698704999,
        "gradient_delta": [
          -3.4117330514373793e+108,
          3.337773719222014e+108
        ],
        "gradient_explosion_ratio": 5.3180913287894476e+107,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.4117330514373793e+108,
        "relative_gradient_delta": 5.3180913287894476e+107,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1294503110548249e-09,
        "scalar_within_tolerance": true,
        "time_index": 57,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.6784254401663515e+109,
        "filterflow_gradient_max_abs": 197.4197643907813,
        "gradient_delta": [
          6.6784254401663515e+109,
          -6.533650958002027e+109
        ],
        "gradient_explosion_ratio": 3.3828555417312647e+107,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.6784254401663515e+109,
        "relative_gradient_delta": 3.3828555417312647e+107,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0837482022907352e-09,
        "scalar_within_tolerance": true,
        "time_index": 58,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.256599597334196e+111,
        "filterflow_gradient_max_abs": 315.57269054843385,
        "gradient_delta": [
          7.256599597334196e+111,
          -7.099291492543592e+111
        ],
        "gradient_explosion_ratio": 2.299501767634883e+109,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.256599597334196e+111,
        "relative_gradient_delta": 2.299501767634883e+109,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1401937172195176e-09,
        "scalar_within_tolerance": true,
        "time_index": 59,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.5810932666647745e+114,
        "filterflow_gradient_max_abs": 60.009881084342744,
        "gradient_delta": [
          1.5810932666647745e+114,
          -1.546818427335311e+114
        ],
        "gradient_explosion_ratio": 2.634721546011028e+112,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.5810932666647745e+114,
        "relative_gradient_delta": 2.634721546011028e+112,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1782930187109741e-09,
        "scalar_within_tolerance": true,
        "time_index": 60,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.116975491704309e+115,
        "filterflow_gradient_max_abs": 147.6346164990015,
        "gradient_delta": [
          4.116975491704309e+115,
          -4.027727958699586e+115
        ],
        "gradient_explosion_ratio": 2.7886247746863302e+113,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.116975491704309e+115,
        "relative_gradient_delta": 2.7886247746863302e+113,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2933298876305344e-09,
        "scalar_within_tolerance": true,
        "time_index": 61,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.052800443488689e+118,
        "filterflow_gradient_max_abs": 512.611395216775,
        "gradient_delta": [
          2.052800443488689e+118,
          -2.0082999659652955e+118
        ],
        "gradient_explosion_ratio": 4.0045938553913596e+115,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.052800443488689e+118,
        "relative_gradient_delta": 4.0045938553913596e+115,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.554774583695689e-10,
        "scalar_within_tolerance": true,
        "time_index": 62,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.114213039412783e+120,
        "filterflow_gradient_max_abs": 87.5818933878043,
        "gradient_delta": [
          7.114213039412783e+120,
          -6.959991581374017e+120
        ],
        "gradient_explosion_ratio": 8.122926742302458e+118,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.114213039412783e+120,
        "relative_gradient_delta": 8.122926742302458e+118,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0234515457341331e-09,
        "scalar_within_tolerance": true,
        "time_index": 63,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.085211673517886e+122,
        "filterflow_gradient_max_abs": 57.78168821303872,
        "gradient_delta": [
          7.085211673517886e+122,
          -6.931618905245736e+122
        ],
        "gradient_explosion_ratio": 1.2262036455901046e+121,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.085211673517886e+122,
        "relative_gradient_delta": 1.2262036455901046e+121,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.412825991399586e-10,
        "scalar_within_tolerance": true,
        "time_index": 64,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.852678050846857e+125,
        "filterflow_gradient_max_abs": 738.8517276846384,
        "gradient_delta": [
          -6.852678050846857e+125,
          6.704126131665301e+125
        ],
        "gradient_explosion_ratio": 9.274767580663712e+122,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.852678050846857e+125,
        "relative_gradient_delta": 9.274767580663712e+122,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.1248317832723842e-09,
        "scalar_within_tolerance": true,
        "time_index": 65,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.819109375676394e+128,
        "filterflow_gradient_max_abs": 1019.3972961264672,
        "gradient_delta": [
          5.819109375676394e+128,
          -5.6929630925342246e+128
        ],
        "gradient_explosion_ratio": 5.708382195821001e+125,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.819109375676394e+128,
        "relative_gradient_delta": 5.708382195821001e+125,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.905196414663806e-10,
        "scalar_within_tolerance": true,
        "time_index": 66,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.408078615031765e+130,
        "filterflow_gradient_max_abs": 122.24440141690243,
        "gradient_delta": [
          8.408078615031765e+130,
          -8.225808821292021e+130
        ],
        "gradient_explosion_ratio": 6.8780889084293075e+128,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.408078615031765e+130,
        "relative_gradient_delta": 6.8780889084293075e+128,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.500755489469157e-10,
        "scalar_within_tolerance": true,
        "time_index": 67,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.321027241338467e+133,
        "filterflow_gradient_max_abs": 682.5428603420182,
        "gradient_delta": [
          -5.321027241338467e+133,
          5.205678351042852e+133
        ],
        "gradient_explosion_ratio": 7.795887336177148e+130,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.321027241338467e+133,
        "relative_gradient_delta": 7.795887336177148e+130,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.193943136167945e-10,
        "scalar_within_tolerance": true,
        "time_index": 68,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.265778632551857e+135,
        "filterflow_gradient_max_abs": 309.19172560146353,
        "gradient_delta": [
          -8.265778632551857e+135,
          8.086593608786742e+135
        ],
        "gradient_explosion_ratio": 2.6733505291814093e+133,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.265778632551857e+135,
        "relative_gradient_delta": 2.6733505291814093e+133,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.828742016296019e-10,
        "scalar_within_tolerance": true,
        "time_index": 69,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.759876140867897e+138,
        "filterflow_gradient_max_abs": 66.90489544481636,
        "gradient_delta": [
          3.759876140867897e+138,
          -3.6783697848904806e+138
        ],
        "gradient_explosion_ratio": 5.619732481263751e+136,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.759876140867897e+138,
        "relative_gradient_delta": 5.619732481263751e+136,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.207851927480078e-10,
        "scalar_within_tolerance": true,
        "time_index": 70,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.035876197529241e+140,
        "filterflow_gradient_max_abs": 750.3754788438333,
        "gradient_delta": [
          7.035876197529241e+140,
          -6.8833529205692485e+140
        ],
        "gradient_explosion_ratio": 9.376474039863361e+137,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.035876197529241e+140,
        "relative_gradient_delta": 9.376474039863361e+137,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.709637207473861e-10,
        "scalar_within_tolerance": true,
        "time_index": 71,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.877687015474054e+141,
        "filterflow_gradient_max_abs": 347.8401730350442,
        "gradient_delta": [
          6.877687015474054e+141,
          -6.72859295354703e+141
        ],
        "gradient_explosion_ratio": 1.9772549431146763e+139,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.877687015474054e+141,
        "relative_gradient_delta": 1.9772549431146763e+139,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.423448439818458e-10,
        "scalar_within_tolerance": true,
        "time_index": 72,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7713578793147118e+145,
        "filterflow_gradient_max_abs": 441.50385013274905,
        "gradient_delta": [
          -1.7713578793147118e+145,
          1.7329584958069613e+145
        ],
        "gradient_explosion_ratio": 4.0121006391724766e+142,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7713578793147118e+145,
        "relative_gradient_delta": 4.0121006391724766e+142,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.418084007644211e-10,
        "scalar_within_tolerance": true,
        "time_index": 73,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.3562044790575933e+148,
        "filterflow_gradient_max_abs": 216.5606746935064,
        "gradient_delta": [
          -4.3562044790575933e+148,
          4.2617709552717487e+148
        ],
        "gradient_explosion_ratio": 2.011539946124953e+146,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.3562044790575933e+148,
        "relative_gradient_delta": 2.011539946124953e+146,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.252687505068025e-10,
        "scalar_within_tolerance": true,
        "time_index": 74,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.431352882602212e+151,
        "filterflow_gradient_max_abs": 592.4376179231792,
        "gradient_delta": [
          -1.431352882602212e+151,
          1.4003241058000733e+151
        ],
        "gradient_explosion_ratio": 2.4160398315351644e+148,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.431352882602212e+151,
        "relative_gradient_delta": 2.4160398315351644e+148,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.707559118192876e-10,
        "scalar_within_tolerance": true,
        "time_index": 75,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.2523184327294328e+154,
        "filterflow_gradient_max_abs": 1021.9536107722753,
        "gradient_delta": [
          2.2523184327294328e+154,
          -2.2034928169180117e+154
        ],
        "gradient_explosion_ratio": 2.2039341208720706e+151,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.2523184327294328e+154,
        "relative_gradient_delta": 2.2039341208720706e+151,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 9.629843589209486e-10,
        "scalar_within_tolerance": true,
        "time_index": 76,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.280459538182837e+155,
        "filterflow_gradient_max_abs": 416.36976112409496,
        "gradient_delta": [
          8.280459538182837e+155,
          -8.100956262678671e+155
        ],
        "gradient_explosion_ratio": 1.988727403216711e+153,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.280459538182837e+155,
        "relative_gradient_delta": 1.988727403216711e+153,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.8334494446608e-10,
        "scalar_within_tolerance": true,
        "time_index": 77,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.6044877263124534e+159,
        "filterflow_gradient_max_abs": 73.20765898029507,
        "gradient_delta": [
          -1.6044877263124534e+159,
          1.569705743374039e+159
        ],
        "gradient_explosion_ratio": 2.191693804529831e+157,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.6044877263124534e+159,
        "relative_gradient_delta": 2.191693804529831e+157,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.958771336940117e-10,
        "scalar_within_tolerance": true,
        "time_index": 78,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.767183790421171e+161,
        "filterflow_gradient_max_abs": 18.775557058598526,
        "gradient_delta": [
          -2.767183790421171e+161,
          2.707196956114191e+161
        ],
        "gradient_explosion_ratio": 1.4738224713039345e+160,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.767183790421171e+161,
        "relative_gradient_delta": 1.4738224713039345e+160,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.100187187665142e-10,
        "scalar_within_tolerance": true,
        "time_index": 79,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0619655340283867e+163,
        "filterflow_gradient_max_abs": 489.4717191114149,
        "gradient_delta": [
          1.0619655340283867e+163,
          -1.0389443126877586e+163
        ],
        "gradient_explosion_ratio": 2.1696157154008302e+160,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0619655340283867e+163,
        "relative_gradient_delta": 2.1696157154008302e+160,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.418758857762441e-10,
        "scalar_within_tolerance": true,
        "time_index": 80,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.31495744812511e+165,
        "filterflow_gradient_max_abs": 603.1903641588457,
        "gradient_delta": [
          -2.31495744812511e+165,
          2.2647739477197203e+165
        ],
        "gradient_explosion_ratio": 3.837855485893477e+162,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.31495744812511e+165,
        "relative_gradient_delta": 3.837855485893477e+162,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.0115144277733634e-09,
        "scalar_within_tolerance": true,
        "time_index": 81,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.273773656021657e+169,
        "filterflow_gradient_max_abs": 924.7685421225882,
        "gradient_delta": [
          -2.273773656021657e+169,
          2.2244829352435532e+169
        ],
        "gradient_explosion_ratio": 2.4587489219764607e+166,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.273773656021657e+169,
        "relative_gradient_delta": 2.4587489219764607e+166,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.2003482652289676e-09,
        "scalar_within_tolerance": true,
        "time_index": 82,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 7.461841601302876e+171,
        "filterflow_gradient_max_abs": 712.4012104561216,
        "gradient_delta": [
          7.461841601302876e+171,
          -7.300084273397254e+171
        ],
        "gradient_explosion_ratio": 1.0474212412588915e+169,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 7.461841601302876e+171,
        "relative_gradient_delta": 1.0474212412588915e+169,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 1.9136194850943866e-09,
        "scalar_within_tolerance": true,
        "time_index": 83,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.0218575863851483e+175,
        "filterflow_gradient_max_abs": 1186.5395908091443,
        "gradient_delta": [
          1.0218575863851483e+175,
          -9.997058225839854e+174
        ],
        "gradient_explosion_ratio": 8.61208167262507e+171,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.0218575863851483e+175,
        "relative_gradient_delta": 8.61208167262507e+171,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.708955086447531e-09,
        "scalar_within_tolerance": true,
        "time_index": 84,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.515152797929136e+177,
        "filterflow_gradient_max_abs": 155.19429188795652,
        "gradient_delta": [
          2.515152797929136e+177,
          -2.4606294754565274e+177
        ],
        "gradient_explosion_ratio": 1.6206477489165425e+175,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.515152797929136e+177,
        "relative_gradient_delta": 1.6206477489165425e+175,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.22875973022019e-09,
        "scalar_within_tolerance": true,
        "time_index": 85,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 6.183628915479302e+179,
        "filterflow_gradient_max_abs": 232.51294890916668,
        "gradient_delta": [
          6.183628915479302e+179,
          -6.049580600924723e+179
        ],
        "gradient_explosion_ratio": 2.659477222447079e+177,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 6.183628915479302e+179,
        "relative_gradient_delta": 2.659477222447079e+177,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.486573056463385e-09,
        "scalar_within_tolerance": true,
        "time_index": 86,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.2851252033709477e+183,
        "filterflow_gradient_max_abs": 1518.8797828290087,
        "gradient_delta": [
          1.2851252033709477e+183,
          -1.2572663409039186e+183
        ],
        "gradient_explosion_ratio": 8.461006709677322e+179,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.2851252033709477e+183,
        "relative_gradient_delta": 8.461006709677322e+179,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.5804499627120094e-09,
        "scalar_within_tolerance": true,
        "time_index": 87,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.762000369386439e+185,
        "filterflow_gradient_max_abs": 92.4227988005718,
        "gradient_delta": [
          3.762000369386439e+185,
          -3.6804479645182276e+185
        ],
        "gradient_explosion_ratio": 4.0704246335409227e+183,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.762000369386439e+185,
        "relative_gradient_delta": 4.0704246335409227e+183,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.631609039686737e-09,
        "scalar_within_tolerance": true,
        "time_index": 88,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.69035105746702e+186,
        "filterflow_gradient_max_abs": 495.480272228227,
        "gradient_delta": [
          -5.69035105746702e+186,
          5.566995988962206e+186
        ],
        "gradient_explosion_ratio": 1.1484515885722172e+184,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.69035105746702e+186,
        "relative_gradient_delta": 1.1484515885722172e+184,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.181977596497745e-09,
        "scalar_within_tolerance": true,
        "time_index": 89,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.7193688345298665e+191,
        "filterflow_gradient_max_abs": 1905.453488616431,
        "gradient_delta": [
          -1.7193688345298665e+191,
          1.6820964662301704e+191
        ],
        "gradient_explosion_ratio": 9.02341014777704e+187,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.7193688345298665e+191,
        "relative_gradient_delta": 9.02341014777704e+187,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.158671794764814e-09,
        "scalar_within_tolerance": true,
        "time_index": 90,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0514752337585018e+193,
        "filterflow_gradient_max_abs": 536.1521590308598,
        "gradient_delta": [
          -2.0514752337585018e+193,
          2.00700348404736e+193
        ],
        "gradient_explosion_ratio": 3.826292964047214e+190,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0514752337585018e+193,
        "relative_gradient_delta": 3.826292964047214e+190,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.624389925491414e-09,
        "scalar_within_tolerance": true,
        "time_index": 91,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 1.313801705305399e+196,
        "filterflow_gradient_max_abs": 85.09097085867334,
        "gradient_delta": [
          1.313801705305399e+196,
          -1.285321195452316e+196
        ],
        "gradient_explosion_ratio": 1.543996609801853e+194,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 1.313801705305399e+196,
        "relative_gradient_delta": 1.543996609801853e+194,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.351314141284092e-09,
        "scalar_within_tolerance": true,
        "time_index": 92,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.303694802293903e+198,
        "filterflow_gradient_max_abs": 286.3674760142073,
        "gradient_delta": [
          -4.303694802293903e+198,
          4.2103995799430515e+198
        ],
        "gradient_explosion_ratio": 1.5028573992391468e+196,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.303694802293903e+198,
        "relative_gradient_delta": 1.5028573992391468e+196,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.2123888255882775e-09,
        "scalar_within_tolerance": true,
        "time_index": 93,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 5.862393601186577e+201,
        "filterflow_gradient_max_abs": 1646.6707953160178,
        "gradient_delta": [
          -5.862393601186577e+201,
          5.735309005355246e+201
        ],
        "gradient_explosion_ratio": 3.560149131120958e+198,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 5.862393601186577e+201,
        "relative_gradient_delta": 3.560149131120958e+198,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.9354371134977555e-09,
        "scalar_within_tolerance": true,
        "time_index": 94,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.947263829541537e+204,
        "filterflow_gradient_max_abs": 1706.2194857616348,
        "gradient_delta": [
          8.947263829541537e+204,
          -8.753305612996097e+204
        ],
        "gradient_explosion_ratio": 5.243911410112393e+201,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.947263829541537e+204,
        "relative_gradient_delta": 5.243911410112393e+201,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 6.4229368490487104e-09,
        "scalar_within_tolerance": true,
        "time_index": 95,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 2.0748145290986924e+207,
        "filterflow_gradient_max_abs": 491.76925290563014,
        "gradient_delta": [
          2.0748145290986924e+207,
          -2.0298368316267756e+207
        ],
        "gradient_explosion_ratio": 4.219081442850691e+204,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 2.0748145290986924e+207,
        "relative_gradient_delta": 4.219081442850691e+204,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.928541213506833e-09,
        "scalar_within_tolerance": true,
        "time_index": 96,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 8.546188990734645e+209,
        "filterflow_gradient_max_abs": 953.0377691516383,
        "gradient_delta": [
          8.546188990734645e+209,
          -8.360925249049713e+209
        ],
        "gradient_explosion_ratio": 8.967314063892947e+206,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 8.546188990734645e+209,
        "relative_gradient_delta": 8.967314063892947e+206,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 5.896453103559907e-09,
        "scalar_within_tolerance": true,
        "time_index": 97,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 4.3138038644013484e+213,
        "filterflow_gradient_max_abs": 1943.4208738111502,
        "gradient_delta": [
          -4.3138038644013484e+213,
          4.220289498444735e+213
        ],
        "gradient_explosion_ratio": 2.219696166966527e+210,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 4.3138038644013484e+213,
        "relative_gradient_delta": 2.219696166966527e+210,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 8.690761887919507e-09,
        "scalar_within_tolerance": true,
        "time_index": 98,
        "transport_status": "computed_raw_transport_gradient"
      },
      {
        "bayesfilter_gradient_max_abs": 3.904188635142209e+214,
        "filterflow_gradient_max_abs": 950.6655619127545,
        "gradient_delta": [
          3.904188635142209e+214,
          -3.819553882087435e+214
        ],
        "gradient_explosion_ratio": 4.1067950618584716e+211,
        "gradient_within_tolerance": false,
        "max_abs_gradient_delta": 3.904188635142209e+214,
        "relative_gradient_delta": 4.1067950618584716e+211,
        "resampling_flag": [
          true
        ],
        "scalar_delta": 7.408061719615944e-09,
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
      "cumulative_mean_log_likelihood": -2.004090374815232,
      "ess_before_resampling": [
        49.99999999999999
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        0.008924445612040184,
        5.795395272864551e-20
      ],
      "gradient_matrix": [
        [
          0.008924445612040184,
          0.00016288542399612796
        ],
        [
          4.241522690094141e-19,
          5.795395272864551e-20
        ]
      ],
      "resampling_flag": [
        false
      ],
      "time_index": 0
    },
    {
      "cumulative_mean_log_likelihood": -17.2005020674398,
      "ess_before_resampling": [
        49.93670594480325
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        -8.860476253579531,
        -8.447956467094267e-18
      ],
      "gradient_matrix": [
        [
          -8.860476253579531,
          -8.682151923192851
        ],
        [
          -8.159528776878862e-18,
          -8.447956467094267e-18
        ]
      ],
      "resampling_flag": [
        true
      ],
      "time_index": 1
    },
    {
      "cumulative_mean_log_likelihood": -18.089399104816973,
      "ess_before_resampling": [
        5.942671242253685
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        1.4056099396090884,
        8.615017537909144e-17
      ],
      "gradient_matrix": [
        [
          1.4056099396090884,
          4.647586217291769
        ],
        [
          -2.5507771064645792e-17,
          8.615017537909144e-17
        ]
      ],
      "resampling_flag": [
        true
      ],
      "time_index": 2
    },
    {
      "cumulative_mean_log_likelihood": -20.756685012298828,
      "ess_before_resampling": [
        44.22504748606863
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        14.864972477668916,
        4.73893259029544e-16
      ],
      "gradient_matrix": [
        [
          14.864972477668916,
          13.36293464576029
        ],
        [
          3.249540791259622e-17,
          4.73893259029544e-16
        ]
      ],
      "resampling_flag": [
        true
      ],
      "time_index": 3
    },
    {
      "cumulative_mean_log_likelihood": -21.827449488050206,
      "ess_before_resampling": [
        22.4243293073044
      ],
      "finite_gradient": true,
      "finite_scalar": true,
      "gradient_diag": [
        -15.00462728219541,
        -7.409546384087077e-16
      ],
      "gradient_matrix": [
        [
          -15.00462728219541,
          -8.822616263902903
        ],
        [
          -3.559436518971483e-16,
          -7.409546384087077e-16
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
      34.31952836300358
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      7019.871883303286,
      713.5990730344417
    ],
    "gradient_matrix": [
      [
        7019.871883303286,
        119.37856499624878
      ],
      [
        12089.78489837936,
        713.5990730344417
      ]
    ],
    "mean_log_likelihood": -154.6799417288612
  },
  "initial_particles_checksum": -0.13359209100740663,
  "last_row": {
    "cumulative_mean_log_likelihood": -154.67994172886134,
    "ess_before_resampling": [
      16.836798718761134
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      950.6655619127545,
      1.0150842145940277e-16
    ],
    "gradient_matrix": [
      [
        950.6655619127545,
        49.57385434139307
      ],
      [
        -2.3237539828673774e-14,
        1.0150842145940277e-16
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
      0.9710526315789474,
      0.9842105263157894
    ]
  },
  "source_gradient_note": "FilterFlow RegularisedTransform transport uses @tf.custom_gradient and clips upstream d_transport to [-1, 1].",
  "status": "executed",
  "stderr_excerpt": "t computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.\n2026-06-03 19:39:28.752899: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\nWARNING: All log messages before absl::InitializeLog() is called are written to STDERR\nE0000 00:00:1780486768.762862     119 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\nE0000 00:00:1780486768.766103     119 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\nW0000 00:00:1780486768.773945     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780486768.773992     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780486768.773997     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\nW0000 00:00:1780486768.773999     119 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.\n2026-06-03 19:39:28.776548: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\nTo enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n2026-06-03 19:39:31.491858: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)\n"
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
        1.3515114431922745e+218,
        -1.1290717972775883e+218
      ],
      "final_gradient_max_abs": 1.3515114431922745e+218,
      "final_mean_log_likelihood": -154.67994172145328,
      "finite_values": true,
      "mode": "raw"
    },
    {
      "final_gradient_diag": [
        7025.174608954654,
        713.4652966764394
      ],
      "final_gradient_max_abs": 7025.174608954654,
      "final_mean_log_likelihood": -154.67994172145328,
      "finite_values": true,
      "mode": "transport_upstream_clip"
    },
    {
      "final_gradient_diag": [
        543.3812985353517,
        732.7210862949149
      ],
      "final_gradient_max_abs": 732.7210862949149,
      "final_mean_log_likelihood": -154.67994172145328,
      "finite_values": true,
      "mode": "transport_matrix_stop_gradient"
    },
    {
      "final_gradient_diag": [
        22174.945679855195,
        2.3092638912203256e-14
      ],
      "final_gradient_max_abs": 22174.945679855195,
      "final_mean_log_likelihood": -154.67994172145328,
      "finite_values": true,
      "mode": "post_resample_state_stop_gradient"
    },
    {
      "final_gradient_diag": [
        -5.608987982225019e+198,
        1.3245422940938783e+199
      ],
      "final_gradient_max_abs": 1.3245422940938783e+199,
      "final_mean_log_likelihood": -154.67994172145328,
      "finite_values": true,
      "mode": "proposal_mean_stop_gradient"
    },
    {
      "final_gradient_diag": [
        1.3515114431922745e+218,
        -1.1290717972775883e+218
      ],
      "final_gradient_max_abs": 1.3515114431922745e+218,
      "final_mean_log_likelihood": -154.67994172145328,
      "finite_values": true,
      "mode": "proposal_log_prob_stop_gradient"
    },
    {
      "final_gradient_diag": [
        2.0723038706470447e+216,
        -1.896623537407829e+216
      ],
      "final_gradient_max_abs": 2.0723038706470447e+216,
      "final_mean_log_likelihood": -154.67994172145328,
      "finite_values": true,
      "mode": "transition_log_prob_stop_gradient"
    },
    {
      "final_gradient_diag": [
        3.904188635142209e+214,
        -3.819553882087435e+214
      ],
      "final_gradient_max_abs": 3.904188635142209e+214,
      "final_mean_log_likelihood": -154.67994172145328,
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
