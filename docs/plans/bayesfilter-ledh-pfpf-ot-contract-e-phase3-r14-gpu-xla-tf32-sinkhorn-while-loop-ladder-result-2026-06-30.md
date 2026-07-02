# Contract E LGSSM GPU XLA TF32 Score Diagnostic

Date: 2026-06-29T22:21:41.888078+00:00

Status: `failed`

## Manifest

- num_particles: `1000`
- seed_count: `10`
- time_steps: `10`
- state_dims: `[2, 1]`
- settings: `[{'epsilon': 0.55, 'steps': 2, 'label': 'eps0.55_steps2'}, {'epsilon': 0.55, 'steps': 8, 'label': 'eps0.55_steps8'}, {'epsilon': 0.55, 'steps': 20, 'label': 'eps0.55_steps20'}]`
- device_scope: `visible`
- logical_gpus: `["LogicalDevice(name='/device:GPU:0', device_type='GPU')"]`
- xla: `True`
- tf32_execution_enabled: `True`
- reset_factorization: `cholesky-ridge`
- score_route: `manual-reverse-scan`
- chol_ridge_abs: `1e-10`
- chol_ridge_rel: `1e-08`

## Value Gate

| dim | value mean | Kalman | delta | sd | MCSE | z | status |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2 | -13.797056 | -13.784139 | -0.012917 | 0.019898 | 0.006292 | -2.053 | `False` |
| 2 | -13.797062 | -13.784139 | -0.012923 | 0.019897 | 0.006292 | -2.054 | `False` |
| 2 | -13.792094 | -13.784139 | -0.007956 | 0.019760 | 0.006249 | -1.273 | `True` |
| 1 | -6.918275 | -6.914505 | -0.003770 | 0.008133 | 0.002572 | -1.466 | `True` |
| 1 | -6.918541 | -6.914505 | -0.004036 | 0.007983 | 0.002525 | -1.599 | `True` |
| 1 | -6.916080 | -6.914505 | -0.001575 | 0.007330 | 0.002318 | -0.679 | `True` |

## Score Gate

| dim | parameter | score mean | Kalman | delta | sd | MCSE | z | status |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2 | `ar_coefficient` | -5.032490 | -4.971697 | -0.060793 | 0.051022 | 0.016135 | -3.768 | `False` |
| 2 | `log_transition_variance` | -3.936852 | -3.932431 | -0.004420 | 0.007085 | 0.002240 | -1.973 | `True` |
| 2 | `log_observation_variance` | -5.511692 | -5.503183 | -0.008510 | 0.008816 | 0.002788 | -3.052 | `False` |
| 2 | `ar_coefficient` | -5.032531 | -4.971697 | -0.060834 | 0.051323 | 0.016230 | -3.748 | `False` |
| 2 | `log_transition_variance` | -3.937205 | -3.932431 | -0.004774 | 0.007461 | 0.002359 | -2.023 | `False` |
| 2 | `log_observation_variance` | -5.511884 | -5.503183 | -0.008702 | 0.008767 | 0.002772 | -3.139 | `False` |
| 2 | `ar_coefficient` | -4.983512 | -4.971697 | -0.011816 | 0.052142 | 0.016489 | -0.717 | `True` |
| 2 | `log_transition_variance` | -3.930260 | -3.932431 | 0.002171 | 0.006548 | 0.002071 | 1.049 | `True` |
| 2 | `log_observation_variance` | -5.495856 | -5.503183 | 0.007327 | 0.009146 | 0.002892 | 2.533 | `False` |
| 1 | `ar_coefficient` | -2.525207 | -2.480625 | -0.044583 | 0.031003 | 0.009804 | -4.547 | `False` |
| 1 | `log_transition_variance` | -1.952369 | -1.952888 | 0.000520 | 0.002794 | 0.000883 | 0.588 | `True` |
| 1 | `log_observation_variance` | -2.748014 | -2.741817 | -0.006197 | 0.005078 | 0.001606 | -3.859 | `False` |
| 1 | `ar_coefficient` | -2.527891 | -2.480625 | -0.047267 | 0.029576 | 0.009353 | -5.054 | `False` |
| 1 | `log_transition_variance` | -1.952723 | -1.952888 | 0.000165 | 0.002692 | 0.000851 | 0.194 | `True` |
| 1 | `log_observation_variance` | -2.748885 | -2.741817 | -0.007068 | 0.005133 | 0.001623 | -4.354 | `False` |
| 1 | `ar_coefficient` | -2.511157 | -2.480625 | -0.030532 | 0.022314 | 0.007056 | -4.327 | `False` |
| 1 | `log_transition_variance` | -1.952898 | -1.952888 | -0.000009 | 0.003396 | 0.001074 | -0.009 | `True` |
| 1 | `log_observation_variance` | -2.745894 | -2.741817 | -0.004077 | 0.005228 | 0.001653 | -2.466 | `False` |

## Gate

```json
{
  "fixture_gates": [
    {
      "conditioning_ok": true,
      "covariance_restoration_ok": true,
      "finite_base": true,
      "kalman_value": -13.784138554721768,
      "parameter_gates": [
        {
          "delta_to_kalman": -0.06079328662973982,
          "gradient_mcse": 0.016134575235906768,
          "gradient_mean": -5.032489919662476,
          "gradient_sd": 0.051022006824813934,
          "kalman_gradient": -4.971696633032736,
          "parameter": "ar_coefficient",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -3.7678888809199704
        },
        {
          "delta_to_kalman": -0.004420423470757218,
          "gradient_mcse": 0.002240467761743477,
          "gradient_mean": -3.9368518829345702,
          "gradient_sd": 0.00708498115128885,
          "kalman_gradient": -3.932431459463813,
          "parameter": "log_transition_variance",
          "within_2_gradient_mcse_of_kalman": true,
          "z_over_gradient_mcse": -1.9729913307555704
        },
        {
          "delta_to_kalman": -0.008509824346304207,
          "gradient_mcse": 0.0027878477013662576,
          "gradient_mean": -5.511692380905151,
          "gradient_sd": 0.008815948505982284,
          "kalman_gradient": -5.503182556558847,
          "parameter": "log_observation_variance",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -3.0524710306569993
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps2",
      "state_dim": 2,
      "status": "fail",
      "value_delta_to_kalman": -0.012917452663486984,
      "value_mcse": 0.006292387774698677,
      "value_mean": -13.797056007385255,
      "value_sd": 0.019898277289046248,
      "value_within_2_mcse_of_kalman": false,
      "value_z_over_mcse": -2.0528697731292573
    },
    {
      "conditioning_ok": true,
      "covariance_restoration_ok": true,
      "finite_base": true,
      "kalman_value": -13.784138554721768,
      "parameter_gates": [
        {
          "delta_to_kalman": -0.06083448536020786,
          "gradient_mcse": 0.016229909492499504,
          "gradient_mean": -5.032531118392944,
          "gradient_sd": 0.051323480214685906,
          "kalman_gradient": -4.971696633032736,
          "parameter": "ar_coefficient",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -3.748294800308155
        },
        {
          "delta_to_kalman": -0.004773521386406632,
          "gradient_mcse": 0.002359453911761308,
          "gradient_mean": -3.9372049808502196,
          "gradient_sd": 0.007461248395359679,
          "kalman_gradient": -3.932431459463813,
          "parameter": "log_transition_variance",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -2.0231466961960054
        },
        {
          "delta_to_kalman": -0.008701560567618394,
          "gradient_mcse": 0.002772405669173266,
          "gradient_mean": -5.511884117126465,
          "gradient_sd": 0.008767116512550787,
          "kalman_gradient": -5.503182556558847,
          "parameter": "log_observation_variance",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -3.1386317898466882
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps8",
      "state_dim": 2,
      "status": "fail",
      "value_delta_to_kalman": -0.012923365444247992,
      "value_mcse": 0.006291966126516454,
      "value_mean": -13.797061920166016,
      "value_sd": 0.019896943920419154,
      "value_within_2_mcse_of_kalman": false,
      "value_z_over_mcse": -2.053947078606256
    },
    {
      "conditioning_ok": true,
      "covariance_restoration_ok": true,
      "finite_base": true,
      "kalman_value": -13.784138554721768,
      "parameter_gates": [
        {
          "delta_to_kalman": -0.01181572086435878,
          "gradient_mcse": 0.01648889609760247,
          "gradient_mean": -4.983512353897095,
          "gradient_sd": 0.05214246777028587,
          "kalman_gradient": -4.971696633032736,
          "parameter": "ar_coefficient",
          "within_2_gradient_mcse_of_kalman": true,
          "z_over_gradient_mcse": -0.7165865315918157
        },
        {
          "delta_to_kalman": 0.0021713018786688743,
          "gradient_mcse": 0.0020705921801712304,
          "gradient_mean": -3.930260157585144,
          "gradient_sd": 0.0065477873946748226,
          "kalman_gradient": -3.932431459463813,
          "parameter": "log_transition_variance",
          "within_2_gradient_mcse_of_kalman": true,
          "z_over_gradient_mcse": 1.0486381139956376
        },
        {
          "delta_to_kalman": 0.007326891351937981,
          "gradient_mcse": 0.0028921534903356225,
          "gradient_mean": -5.495855665206909,
          "gradient_sd": 0.009145792372266344,
          "kalman_gradient": -5.503182556558847,
          "parameter": "log_observation_variance",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": 2.533368777425338
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps20",
      "state_dim": 2,
      "status": "fail",
      "value_delta_to_kalman": -0.007955866664950406,
      "value_mcse": 0.006248746942521686,
      "value_mean": -13.792094421386718,
      "value_sd": 0.019760272860381792,
      "value_within_2_mcse_of_kalman": true,
      "value_z_over_mcse": -1.2731939280197209
    },
    {
      "conditioning_ok": true,
      "covariance_restoration_ok": true,
      "finite_base": true,
      "kalman_value": -6.914505014954087,
      "parameter_gates": [
        {
          "delta_to_kalman": -0.04458251504100508,
          "gradient_mcse": 0.009803895712229211,
          "gradient_mean": -2.5252070665359496,
          "gradient_sd": 0.031002640393403,
          "kalman_gradient": -2.4806245514949445,
          "parameter": "ar_coefficient",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -4.547428527355061
        },
        {
          "delta_to_kalman": 0.0005197721104652775,
          "gradient_mcse": 0.0008834921244349421,
          "gradient_mean": -1.9523685574531555,
          "gradient_sd": 0.0027938474080353194,
          "kalman_gradient": -1.9528883295636208,
          "parameter": "log_transition_variance",
          "within_2_gradient_mcse_of_kalman": true,
          "z_over_gradient_mcse": 0.5883154994705921
        },
        {
          "delta_to_kalman": -0.006196939128284118,
          "gradient_mcse": 0.0016058890455529877,
          "gradient_mean": -2.748013734817505,
          "gradient_sd": 0.005078267053461334,
          "kalman_gradient": -2.7418167956892208,
          "parameter": "log_observation_variance",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -3.8588837413422934
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps2",
      "state_dim": 1,
      "status": "fail",
      "value_delta_to_kalman": -0.0037704367060689137,
      "value_mcse": 0.002571848276326227,
      "value_mean": -6.918275451660156,
      "value_sd": 0.008132898349568981,
      "value_within_2_mcse_of_kalman": true,
      "value_z_over_mcse": -1.466041656024444
    },
    {
      "conditioning_ok": true,
      "covariance_restoration_ok": true,
      "finite_base": true,
      "kalman_value": -6.914505014954087,
      "parameter_gates": [
        {
          "delta_to_kalman": -0.04726663140453047,
          "gradient_mcse": 0.009352756694812921,
          "gradient_mean": -2.527891182899475,
          "gradient_sd": 0.02957601355699715,
          "kalman_gradient": -2.4806245514949445,
          "parameter": "ar_coefficient",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -5.053764675685913
        },
        {
          "delta_to_kalman": 0.00016541057634666956,
          "gradient_mcse": 0.0008513298438524837,
          "gradient_mean": -1.9527229189872741,
          "gradient_sd": 0.002692141346649344,
          "kalman_gradient": -1.9528883295636208,
          "parameter": "log_transition_variance",
          "within_2_gradient_mcse_of_kalman": true,
          "z_over_gradient_mcse": 0.19429669656374865
        },
        {
          "delta_to_kalman": -0.0070680014070316766,
          "gradient_mcse": 0.0016232902007311918,
          "gradient_mean": -2.7488847970962524,
          "gradient_sd": 0.005133294337742492,
          "kalman_gradient": -2.7418167956892208,
          "parameter": "log_observation_variance",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -4.354120664221332
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps8",
      "state_dim": 1,
      "status": "fail",
      "value_delta_to_kalman": -0.004036368789199329,
      "value_mcse": 0.0025245302593421663,
      "value_mean": -6.918541383743286,
      "value_sd": 0.007983265641536818,
      "value_within_2_mcse_of_kalman": true,
      "value_z_over_mcse": -1.5988593419558033
    },
    {
      "conditioning_ok": true,
      "covariance_restoration_ok": true,
      "finite_base": true,
      "kalman_value": -6.914505014954087,
      "parameter_gates": [
        {
          "delta_to_kalman": -0.030531983653676154,
          "gradient_mcse": 0.007056271092228891,
          "gradient_mean": -2.5111565351486207,
          "gradient_sd": 0.02231388843904735,
          "kalman_gradient": -2.4806245514949445,
          "parameter": "ar_coefficient",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -4.3269289479681685
        },
        {
          "delta_to_kalman": -9.266795632179026e-06,
          "gradient_mcse": 0.0010740620562484004,
          "gradient_mean": -1.952897596359253,
          "gradient_sd": 0.00339648244610883,
          "kalman_gradient": -1.9528883295636208,
          "parameter": "log_transition_variance",
          "within_2_gradient_mcse_of_kalman": true,
          "z_over_gradient_mcse": -0.008627802814808566
        },
        {
          "delta_to_kalman": -0.004077421801929049,
          "gradient_mcse": 0.0016533893053893199,
          "gradient_mean": -2.74589421749115,
          "gradient_sd": 0.0052284760639939604,
          "kalman_gradient": -2.7418167956892208,
          "parameter": "log_observation_variance",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -2.4660990540089087
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps20",
      "state_dim": 1,
      "status": "fail",
      "value_delta_to_kalman": -0.0015749830622704408,
      "value_mcse": 0.002317921393568206,
      "value_mean": -6.916079998016357,
      "value_sd": 0.007329911040907096,
      "value_within_2_mcse_of_kalman": true,
      "value_z_over_mcse": -0.6794807911263606
    }
  ],
  "gpu_visible": true,
  "manual_score_route": true,
  "primary_criterion": "GPU/XLA/TF32 batched Contract E seed-mean value and score are within 2 MCSE of exact FP64 Kalman for every requested fixture.",
  "route_ok": true,
  "status": "failed",
  "tf32_execution_enabled": true,
  "xla_enabled": true
}
```

## Nonclaims

- This is not a CPU LEDH result.
- This diagnostic does not run the 13-point finite-difference ladder.
- This diagnostic does not certify SIR/SV/nonlinear correctness, HMC readiness, or production readiness.
