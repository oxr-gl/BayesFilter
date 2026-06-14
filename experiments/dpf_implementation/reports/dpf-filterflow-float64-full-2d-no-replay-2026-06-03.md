# Filterflow Float64 Full 2D No-Replay Comparison

## Decision

`filterflow_float64_full_2d_no_replay_pass`

## Reference

| Key | Value |
| --- | --- |
| `future_comparator` | `filterflow_float64_reference_branch` |
| `branch` | `bayesfilter-py311-float64-reference` |
| `commit` | `1e5fbc288c1c11fc18ba01bb4842832e2088b800` |
| `upstream_base` | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| `dtype` | `float64` |
| `local_reference_status` | `BayesFilter audit reference code, not pristine upstream` |
| `transition_covariance` | `I_2 executable reproduction setting` |
| `fixed_target_sinkhorn` | `local BayesFilter diagnostic/comparator only` |

## Trace Gate

```json
{
  "official_trace_deltas": {
    "log_likelihoods": 9.947598300641403e-14,
    "log_weights": 0.0,
    "particles": 0.0
  },
  "official_trace_match": true,
  "tolerance": 5e-05
}
```

## Comparison

```json
{
  "finite_bayesfilter_no_replay": true,
  "first_failure": {
    "status": "no_failure"
  },
  "implementation_agreement": true,
  "per_time_deltas": [
    {
      "deltas": {
        "log_likelihood_increment": 4.440892098500626e-16,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 4.440892098500626e-16,
        "post_update_log_weights": 3.1086244689504383e-15,
        "post_update_particles": 0.0,
        "proposal_log_likelihoods": 3.552713678800501e-15,
        "proposal_particles": 0.0,
        "seed2": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 0
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.7127635955112055e-12,
        "observation_log_likelihoods": 6.550315845288424e-14,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.121147867408581e-13,
        "post_update_log_likelihoods": 5.7127635955112055e-12,
        "post_update_log_weights": 9.666933920016163e-12,
        "post_update_particles": 6.52811138479592e-13,
        "proposal_log_likelihoods": 1.3322676295501878e-15,
        "proposal_particles": 6.52811138479592e-13,
        "seed2": 0.0,
        "transition_log_likelihoods": 5.778488798569015e-12,
        "transport_matrix": 1.5163564848208466e-13
      },
      "failing_fields": [],
      "time_index": 1
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.715250743307479e-13,
        "observation_log_likelihoods": 1.0036416142611415e-13,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.541434061091422e-13,
        "post_update_log_likelihoods": 4.8405723873656825e-12,
        "post_update_log_weights": 6.8833827526759706e-15,
        "post_update_particles": 2.682298827494378e-13,
        "proposal_log_likelihoods": 3.552713678800501e-15,
        "proposal_particles": 2.682298827494378e-13,
        "seed2": 0.0,
        "transition_log_likelihoods": 8.855138844410249e-13,
        "transport_matrix": 6.661338147750939e-16
      },
      "failing_fields": [],
      "time_index": 2
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.161915174132446e-13,
        "observation_log_likelihoods": 1.4344081478157023e-13,
        "post_resample_log_weights": 6.8833827526759706e-15,
        "post_resample_particles": 2.682298827494378e-13,
        "post_update_log_likelihoods": 5.158540261618327e-12,
        "post_update_log_weights": 7.842615445952106e-13,
        "post_update_particles": 9.769962616701378e-14,
        "proposal_log_likelihoods": 1.1546319456101628e-14,
        "proposal_particles": 9.769962616701378e-14,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.769962616701378e-13
      },
      "failing_fields": [],
      "time_index": 3
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.2922996006636822e-13,
        "observation_log_likelihoods": 2.942091015256665e-13,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.2896350654045818e-12,
        "post_update_log_likelihoods": 5.286437954055145e-12,
        "post_update_log_weights": 3.7627678750595805e-12,
        "post_update_particles": 2.1600499167107046e-12,
        "proposal_log_likelihoods": 5.773159728050814e-15,
        "proposal_particles": 2.1600499167107046e-12,
        "seed2": 0.0,
        "transition_log_likelihoods": 4.022115973612017e-12,
        "transport_matrix": 2.310374114244951e-13
      },
      "failing_fields": [],
      "time_index": 4
    },
    {
      "deltas": {
        "log_likelihood_increment": 9.562128866491548e-12,
        "observation_log_likelihoods": 3.2303049124493555e-12,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.1176840543121216e-12,
        "post_update_log_likelihoods": 1.4850343177386094e-11,
        "post_update_log_weights": 4.18616252773063e-11,
        "post_update_particles": 7.936762358440319e-12,
        "proposal_log_likelihoods": 2.708944180085382e-14,
        "proposal_particles": 7.936762358440319e-12,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.9096725029376103e-11,
        "transport_matrix": 2.2848112291029565e-12
      },
      "failing_fields": [],
      "time_index": 5
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.491607169005874e-12,
        "observation_log_likelihoods": 1.7323920076250943e-12,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.0761169733086717e-11,
        "post_update_log_likelihoods": 9.36140054363932e-12,
        "post_update_log_weights": 4.199751657552042e-12,
        "post_update_particles": 1.3557155398302712e-11,
        "proposal_log_likelihoods": 1.7763568394002505e-15,
        "proposal_particles": 1.3557155398302712e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.0734080291285863e-11,
        "transport_matrix": 3.4413027982793665e-12
      },
      "failing_fields": [],
      "time_index": 6
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.8401725415960755e-12,
        "observation_log_likelihoods": 1.9626522629323517e-12,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.971756091734278e-11,
        "post_update_log_likelihoods": 1.220001877300092e-11,
        "post_update_log_weights": 2.851452407526267e-11,
        "post_update_particles": 2.4350299554498633e-11,
        "proposal_log_likelihoods": 7.549516567451064e-15,
        "proposal_particles": 2.4350299554498633e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.983790992061586e-11,
        "transport_matrix": 4.240052753345935e-12
      },
      "failing_fields": [],
      "time_index": 7
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.83795250924868e-12,
        "observation_log_likelihoods": 1.3169465518103607e-12,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.093258899549255e-11,
        "post_update_log_likelihoods": 4.359179683888215e-12,
        "post_update_log_weights": 1.5649703755116207e-11,
        "post_update_particles": 1.460875864722766e-11,
        "proposal_log_likelihoods": 2.220446049250313e-15,
        "proposal_particles": 1.460875864722766e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.4806823262224498e-11,
        "transport_matrix": 1.5029477662409363e-11
      },
      "failing_fields": [],
      "time_index": 8
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.036149027162537e-11,
        "observation_log_likelihoods": 1.3932854869835865e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.674438365739661e-11,
        "post_update_log_likelihoods": 2.4719781777093885e-11,
        "post_update_log_weights": 1.341149413747189e-10,
        "post_update_particles": 1.8260948309034575e-11,
        "proposal_log_likelihoods": 2.0872192862952943e-14,
        "proposal_particles": 1.8260948309034575e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.984102433691078e-11,
        "transport_matrix": 4.921452134709625e-12
      },
      "failing_fields": [],
      "time_index": 9
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.497158284129e-11,
        "observation_log_likelihoods": 1.1270095967574889e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.8137492336099967e-11,
        "post_update_log_likelihoods": 3.0251356974986265e-11,
        "post_update_log_weights": 1.8251666844548708e-10,
        "post_update_particles": 3.9747760638420004e-11,
        "proposal_log_likelihoods": 2.7533531010703882e-14,
        "proposal_particles": 3.9747760638420004e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.162714369229434e-10,
        "transport_matrix": 8.907874438079944e-12
      },
      "failing_fields": [],
      "time_index": 10
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.0232703573365143e-11,
        "observation_log_likelihoods": 1.87845294874478e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.572786676566466e-11,
        "post_update_log_likelihoods": 4.048317236993171e-11,
        "post_update_log_weights": 1.5300205546964207e-10,
        "post_update_particles": 3.7829295251867734e-11,
        "proposal_log_likelihoods": 4.75175454539567e-14,
        "proposal_particles": 3.7829295251867734e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.4451106977730888e-10,
        "transport_matrix": 4.8127724028290686e-11
      },
      "failing_fields": [],
      "time_index": 11
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.511191420419891e-11,
        "observation_log_likelihoods": 1.0669243266647754e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.113420880637932e-11,
        "post_update_log_likelihoods": 8.559553066334047e-11,
        "post_update_log_weights": 1.1824274892546782e-10,
        "post_update_particles": 6.502887117676437e-11,
        "proposal_log_likelihoods": 3.952393967665557e-14,
        "proposal_particles": 6.502887117676437e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.7401591279053719e-10,
        "transport_matrix": 5.0659587635948355e-11
      },
      "failing_fields": [],
      "time_index": 12
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.106959465374985e-11,
        "observation_log_likelihoods": 6.728173573833374e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.0795098148719262e-10,
        "post_update_log_likelihoods": 1.4523493518936448e-11,
        "post_update_log_weights": 1.2682299654898088e-10,
        "post_update_particles": 6.52562448522076e-11,
        "proposal_log_likelihoods": 3.5083047578154947e-14,
        "proposal_particles": 6.52562448522076e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.5945111897508468e-10,
        "transport_matrix": 5.285527571174953e-11
      },
      "failing_fields": [],
      "time_index": 13
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.013367498918342e-11,
        "observation_log_likelihoods": 2.3288926342956984e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.673683827784771e-11,
        "post_update_log_likelihoods": 3.560884920261742e-11,
        "post_update_log_weights": 1.0098188951701559e-10,
        "post_update_particles": 4.503419859247515e-11,
        "proposal_log_likelihoods": 6.483702463810914e-14,
        "proposal_particles": 4.503419859247515e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.3420020650301012e-10,
        "transport_matrix": 2.6914803719080282e-11
      },
      "failing_fields": [],
      "time_index": 14
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.741452006688633e-12,
        "observation_log_likelihoods": 8.801182005413466e-12,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.346123461118623e-11,
        "post_update_log_likelihoods": 2.686917355276819e-11,
        "post_update_log_weights": 1.9819701435608295e-11,
        "post_update_particles": 2.69579913947382e-11,
        "proposal_log_likelihoods": 2.886579864025407e-14,
        "proposal_particles": 2.69579913947382e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.5796254021770437e-11,
        "transport_matrix": 7.04021285713452e-11
      },
      "failing_fields": [],
      "time_index": 15
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.0858093030540203e-11,
        "observation_log_likelihoods": 4.8683279629813114e-12,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.586819730116986e-11,
        "post_update_log_likelihoods": 4.772715556100593e-11,
        "post_update_log_weights": 1.9777335324988599e-10,
        "post_update_particles": 5.367439825931797e-11,
        "proposal_log_likelihoods": 4.884981308350689e-14,
        "proposal_particles": 5.367439825931797e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.1379253922759744e-10,
        "transport_matrix": 3.344985399778011e-11
      },
      "failing_fields": [],
      "time_index": 16
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.839773109528323e-14,
        "observation_log_likelihoods": 2.1100454716815875e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.134914715654304e-11,
        "post_update_log_likelihoods": 4.778399897986674e-11,
        "post_update_log_weights": 5.696532134891186e-11,
        "post_update_particles": 3.2670754990249407e-11,
        "proposal_log_likelihoods": 3.774758283725532e-14,
        "proposal_particles": 3.2670754990249407e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 7.810863067447826e-11,
        "transport_matrix": 6.546407860241743e-11
      },
      "failing_fields": [],
      "time_index": 17
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.382272322800418e-11,
        "observation_log_likelihoods": 5.196509889060508e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.2082782531215344e-11,
        "post_update_log_likelihoods": 9.161027492154972e-11,
        "post_update_log_weights": 3.771543077846218e-10,
        "post_update_particles": 8.736833478906192e-11,
        "proposal_log_likelihoods": 6.039613253960852e-14,
        "proposal_particles": 8.736833478906192e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.814264377093423e-10,
        "transport_matrix": 4.135963793672204e-11
      },
      "failing_fields": [],
      "time_index": 18
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.0911894438313539e-10,
        "observation_log_likelihoods": 6.073230807146501e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.2896350654045818e-10,
        "post_update_log_likelihoods": 3.007301074831048e-10,
        "post_update_log_weights": 7.229905563121974e-10,
        "post_update_particles": 1.88606463780161e-10,
        "proposal_log_likelihoods": 1.2079226507921703e-13,
        "proposal_particles": 1.88606463780161e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 4.531539588015221e-10,
        "transport_matrix": 1.0499509595085499e-10
      },
      "failing_fields": [],
      "time_index": 19
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.1737877336770453e-10,
        "observation_log_likelihoods": 3.530598036149968e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.2092550839024625e-10,
        "post_update_log_likelihoods": 4.1811176743067335e-10,
        "post_update_log_weights": 3.977280726985555e-10,
        "post_update_particles": 1.4924239621905144e-10,
        "proposal_log_likelihoods": 4.529709940470639e-14,
        "proposal_particles": 1.4924239621905144e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 5.429914295973504e-10,
        "transport_matrix": 1.72159397848759e-10
      },
      "failing_fields": [],
      "time_index": 20
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.8891133102272306e-10,
        "observation_log_likelihoods": 2.994493542018972e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.545430450278218e-10,
        "post_update_log_likelihoods": 2.2919977027413552e-10,
        "post_update_log_weights": 1.0449485721153451e-10,
        "post_update_particles": 8.614620128355455e-11,
        "proposal_log_likelihoods": 5.595524044110789e-14,
        "proposal_particles": 8.614620128355455e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 3.1793501165111593e-10,
        "transport_matrix": 1.055499021518358e-10
      },
      "failing_fields": [],
      "time_index": 21
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.7948176278537176e-10,
        "observation_log_likelihoods": 2.596323156467406e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.3384227059987097e-10,
        "post_update_log_likelihoods": 4.086828653271368e-10,
        "post_update_log_weights": 1.0327161348300251e-10,
        "post_update_particles": 8.631673154013697e-11,
        "proposal_log_likelihoods": 4.085620730620576e-14,
        "proposal_particles": 8.631673154013697e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.803264287365437e-10,
        "transport_matrix": 1.4734435893615228e-10
      },
      "failing_fields": [],
      "time_index": 22
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.983413764454326e-11,
        "observation_log_likelihoods": 6.175482347714478e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.448974935821752e-11,
        "post_update_log_likelihoods": 4.685176691054949e-10,
        "post_update_log_weights": 5.075762032902276e-10,
        "post_update_particles": 1.5785417417646386e-10,
        "proposal_log_likelihoods": 7.416289804496046e-14,
        "proposal_particles": 1.5785417417646386e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 6.292388832207507e-10,
        "transport_matrix": 9.603207118402679e-11
      },
      "failing_fields": [],
      "time_index": 23
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.3931080167803884e-11,
        "observation_log_likelihoods": 1.1810108446752565e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.4300827189117626e-10,
        "post_update_log_likelihoods": 5.024460847380396e-10,
        "post_update_log_weights": 1.361577517400292e-12,
        "post_update_particles": 1.8349055608268827e-10,
        "proposal_log_likelihoods": 3.019806626980426e-14,
        "proposal_particles": 1.8349055608268827e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 4.59288163057181e-11,
        "transport_matrix": 1.6105294875501386e-10
      },
      "failing_fields": [],
      "time_index": 24
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.958034314332508e-11,
        "observation_log_likelihoods": 1.5853096613227535e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.1144418721187321e-10,
        "post_update_log_likelihoods": 4.128608566134062e-10,
        "post_update_log_weights": 2.4817259358655974e-10,
        "post_update_particles": 6.625100468227174e-11,
        "proposal_log_likelihoods": 3.597122599785507e-14,
        "proposal_particles": 6.625100468227174e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 3.21927373647668e-10,
        "transport_matrix": 1.2545264826968605e-10
      },
      "failing_fields": [],
      "time_index": 25
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.222156206410091e-11,
        "observation_log_likelihoods": 2.511058028176194e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.1821388312682757e-10,
        "post_update_log_likelihoods": 4.850804202760628e-10,
        "post_update_log_weights": 9.970957393079516e-11,
        "post_update_particles": 1.0714984455262311e-10,
        "proposal_log_likelihoods": 4.263256414560601e-14,
        "proposal_particles": 1.0714984455262311e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.467777011043836e-10,
        "transport_matrix": 8.29279978020736e-11
      },
      "failing_fields": [],
      "time_index": 26
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.378542304399161e-11,
        "observation_log_likelihoods": 6.177836020526684e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.553210893234791e-10,
        "post_update_log_likelihoods": 5.688676196768938e-10,
        "post_update_log_weights": 3.308362472864701e-10,
        "post_update_particles": 1.3639578355650883e-10,
        "proposal_log_likelihoods": 7.194245199571014e-14,
        "proposal_particles": 1.3639578355650883e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 3.527715897178041e-10,
        "transport_matrix": 9.997452865562195e-11
      },
      "failing_fields": [],
      "time_index": 27
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.926193035245888e-11,
        "observation_log_likelihoods": 3.6380898293941755e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.2032508323045477e-10,
        "post_update_log_likelihoods": 4.89599472075497e-10,
        "post_update_log_weights": 2.2399193611022383e-10,
        "post_update_particles": 1.0490452950762119e-10,
        "proposal_log_likelihoods": 1.1102230246251565e-13,
        "proposal_particles": 1.0490452950762119e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.668336662736692e-10,
        "transport_matrix": 1.2185696895983256e-10
      },
      "failing_fields": [],
      "time_index": 28
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.99054139627242e-12,
        "observation_log_likelihoods": 6.128653140535789e-12,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.967315861558745e-11,
        "post_update_log_likelihoods": 4.955893473379547e-10,
        "post_update_log_weights": 7.975287097394812e-11,
        "post_update_particles": 9.382006282976363e-11,
        "proposal_log_likelihoods": 1.092459456231154e-13,
        "proposal_particles": 9.382006282976363e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 8.988942923338072e-11,
        "transport_matrix": 2.3229135281965796e-10
      },
      "failing_fields": [],
      "time_index": 29
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.4640736379951704e-12,
        "observation_log_likelihoods": 1.5721246526823052e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.4149037497190875e-10,
        "post_update_log_likelihoods": 5.010534209759498e-10,
        "post_update_log_weights": 1.1844907277236416e-09,
        "post_update_particles": 2.142428456863854e-10,
        "proposal_log_likelihoods": 1.8740564655672642e-13,
        "proposal_particles": 2.142428456863854e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.0329284094723334e-09,
        "transport_matrix": 6.50269837976225e-11
      },
      "failing_fields": [],
      "time_index": 30
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.357403575269927e-10,
        "observation_log_likelihoods": 7.06088520985304e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.0411494716654488e-10,
        "post_update_log_likelihoods": 2.346851601942035e-10,
        "post_update_log_weights": 9.268141809570807e-10,
        "post_update_particles": 1.0436451702844352e-10,
        "proposal_log_likelihoods": 1.4077627952246985e-13,
        "proposal_particles": 1.0436451702844352e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.097362863030867e-10,
        "transport_matrix": 2.2167231938929888e-10
      },
      "failing_fields": [],
      "time_index": 31
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.19284804256381e-10,
        "observation_log_likelihoods": 9.951239832162173e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.7966696453395343e-10,
        "post_update_log_likelihoods": 3.539639692462515e-10,
        "post_update_log_weights": 6.956266673796563e-10,
        "post_update_particles": 1.8678747437661514e-10,
        "proposal_log_likelihoods": 2.233768725545815e-13,
        "proposal_particles": 1.8678747437661514e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.146479129640284e-10,
        "transport_matrix": 3.234997825174446e-10
      },
      "failing_fields": [],
      "time_index": 32
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.2261081039355304e-11,
        "observation_log_likelihoods": 1.644950842205617e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.1354917006656251e-10,
        "post_update_log_likelihoods": 3.417071070543898e-10,
        "post_update_log_weights": 2.7060131913003715e-10,
        "post_update_particles": 1.234070623468142e-10,
        "proposal_log_likelihoods": 1.0658141036401503e-13,
        "proposal_particles": 1.234070623468142e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.760147665981094e-10,
        "transport_matrix": 1.8649026767292298e-10
      },
      "failing_fields": [],
      "time_index": 33
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.5365045053813446e-11,
        "observation_log_likelihoods": 9.86135617608852e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.112000043387525e-11,
        "post_update_log_likelihoods": 2.963389533761074e-10,
        "post_update_log_weights": 2.018585298912967e-10,
        "post_update_particles": 1.6689227777533233e-10,
        "proposal_log_likelihoods": 2.1893598045608087e-13,
        "proposal_particles": 1.6689227777533233e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.4882894916468103e-10,
        "transport_matrix": 2.2390855836107448e-10
      },
      "failing_fields": [],
      "time_index": 34
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.984723993104126e-12,
        "observation_log_likelihoods": 8.467093692843264e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.8897505782433655e-10,
        "post_update_log_likelihoods": 2.8835245302616386e-10,
        "post_update_log_weights": 1.8902479581583975e-10,
        "post_update_particles": 1.7627144188736565e-10,
        "proposal_log_likelihoods": 1.412203687323199e-13,
        "proposal_particles": 1.7627144188736565e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.354010320004818e-10,
        "transport_matrix": 3.5551639410158486e-10
      },
      "failing_fields": [],
      "time_index": 35
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.73605599182747e-11,
        "observation_log_likelihoods": 1.554045780949309e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.857882736544525e-10,
        "post_update_log_likelihoods": 2.409947796877532e-10,
        "post_update_log_weights": 1.9073320700613294e-10,
        "post_update_particles": 1.425064510840457e-10,
        "proposal_log_likelihoods": 4.085620730620576e-14,
        "proposal_particles": 1.425064510840457e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.2475044048064774e-10,
        "transport_matrix": 2.873166149441886e-10
      },
      "failing_fields": [],
      "time_index": 36
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.5564949329416322e-10,
        "observation_log_likelihoods": 2.965139245247883e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.934985918860548e-11,
        "post_update_log_likelihoods": 3.9664627138336073e-10,
        "post_update_log_weights": 4.4363623885601555e-10,
        "post_update_particles": 6.861000656499527e-11,
        "proposal_log_likelihoods": 1.7319479184152442e-14,
        "proposal_particles": 6.861000656499527e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 3.176303664531588e-10,
        "transport_matrix": 1.0513251380572797e-10
      },
      "failing_fields": [],
      "time_index": 37
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.239579550116332e-10,
        "observation_log_likelihoods": 2.5925928071046656e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.0108447412449095e-10,
        "post_update_log_likelihoods": 2.7269209113001125e-10,
        "post_update_log_weights": 1.7308665611892593e-10,
        "post_update_particles": 1.4841816664556973e-10,
        "proposal_log_likelihoods": 1.5276668818842154e-13,
        "proposal_particles": 1.4841816664556973e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.255990949606712e-10,
        "transport_matrix": 8.9239227119009e-11
      },
      "failing_fields": [],
      "time_index": 38
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.0690159868431692e-10,
        "observation_log_likelihoods": 8.201328505208494e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.0229595776299902e-10,
        "post_update_log_likelihoods": 3.795932457251183e-10,
        "post_update_log_weights": 4.464673075688097e-10,
        "post_update_particles": 9.214318197336979e-11,
        "proposal_log_likelihoods": 8.348877145181177e-14,
        "proposal_particles": 9.214318197336979e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 4.713354151419935e-10,
        "transport_matrix": 1.7085255432647273e-10
      },
      "failing_fields": [],
      "time_index": 39
    },
    {
      "deltas": {
        "log_likelihood_increment": 6.354410331255167e-10,
        "observation_log_likelihoods": 1.3914513985469057e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.651585535000777e-10,
        "post_update_log_likelihoods": 1.015031614315376e-09,
        "post_update_log_weights": 1.0286305140994045e-09,
        "post_update_particles": 2.6898305804934353e-10,
        "proposal_log_likelihoods": 1.8740564655672642e-13,
        "proposal_particles": 2.6898305804934353e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.0373373271477249e-09,
        "transport_matrix": 2.740420668168042e-10
      },
      "failing_fields": [],
      "time_index": 40
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.8725860861934507e-09,
        "observation_log_likelihoods": 2.182904967895638e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.314522486647547e-10,
        "post_update_log_likelihoods": 2.8876172564196168e-09,
        "post_update_log_weights": 3.550627791781835e-09,
        "post_update_particles": 6.288018994382583e-10,
        "proposal_log_likelihoods": 1.141309269314661e-13,
        "proposal_particles": 6.288018994382583e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 5.506093359031183e-09,
        "transport_matrix": 8.785475680284094e-10
      },
      "failing_fields": [],
      "time_index": 41
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.899236820207989e-11,
        "observation_log_likelihoods": 3.258615599577297e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.212097337585874e-10,
        "post_update_log_likelihoods": 2.808633325912524e-09,
        "post_update_log_weights": 9.215050944533232e-11,
        "post_update_particles": 5.624656296276953e-10,
        "proposal_log_likelihoods": 1.7141843500212417e-13,
        "proposal_particles": 5.624656296276953e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.0373702724896248e-10,
        "transport_matrix": 7.280447911206522e-10
      },
      "failing_fields": [],
      "time_index": 42
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.4756774408274396e-10,
        "observation_log_likelihoods": 9.855205540532097e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.074611924589135e-10,
        "post_update_log_likelihoods": 2.56106602591899e-09,
        "post_update_log_weights": 6.610458846978418e-10,
        "post_update_particles": 4.090452421223745e-10,
        "proposal_log_likelihoods": 6.750155989720952e-14,
        "proposal_particles": 4.090452421223745e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 8.10013389695996e-10,
        "transport_matrix": 4.3766171242687335e-10
      },
      "failing_fields": [],
      "time_index": 43
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.8755419439742127e-10,
        "observation_log_likelihoods": 6.784617312405317e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.296221239348142e-10,
        "post_update_log_likelihoods": 2.7486066755955108e-09,
        "post_update_log_weights": 1.3171070900597215e-09,
        "post_update_particles": 2.573870006017387e-10,
        "proposal_log_likelihoods": 8.126832540256146e-14,
        "proposal_particles": 2.573870006017387e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.5329204572367416e-09,
        "transport_matrix": 5.179152107182006e-10
      },
      "failing_fields": [],
      "time_index": 44
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.192912518239609e-12,
        "observation_log_likelihoods": 8.380229843396592e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.523918934433823e-10,
        "post_update_log_likelihoods": 2.750795147221652e-09,
        "post_update_log_weights": 9.27091736713237e-11,
        "post_update_particles": 1.177795638795942e-10,
        "proposal_log_likelihoods": 1.318944953254686e-13,
        "proposal_particles": 1.177795638795942e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.6883250353316726e-10,
        "transport_matrix": 9.057418148827878e-10
      },
      "failing_fields": [],
      "time_index": 45
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.032289809188569e-10,
        "observation_log_likelihoods": 1.5724088697766092e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.617479483684292e-10,
        "post_update_log_likelihoods": 2.8540227958728792e-09,
        "post_update_log_weights": 1.0191092414402192e-09,
        "post_update_particles": 2.6921043172478676e-10,
        "proposal_log_likelihoods": 1.412203687323199e-13,
        "proposal_particles": 2.6921043172478676e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.01857366985314e-09,
        "transport_matrix": 7.681161262595992e-11
      },
      "failing_fields": [],
      "time_index": 46
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.097717968918005e-10,
        "observation_log_likelihoods": 6.271672070568002e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.7846258632280296e-10,
        "post_update_log_likelihoods": 3.5637981454783585e-09,
        "post_update_log_weights": 7.456000261640838e-10,
        "post_update_particles": 2.4436985768261366e-10,
        "proposal_log_likelihoods": 2.304822999121825e-13,
        "proposal_particles": 2.4436985768261366e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.4327063979635568e-09,
        "transport_matrix": 1.5529399988167825e-10
      },
      "failing_fields": [],
      "time_index": 47
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.0485014512748876e-10,
        "observation_log_likelihoods": 9.370970666111589e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.5410206444244068e-10,
        "post_update_log_likelihoods": 3.868649400828872e-09,
        "post_update_log_weights": 3.425633110509807e-10,
        "post_update_particles": 2.4704149836907163e-10,
        "proposal_log_likelihoods": 1.2256862191861728e-13,
        "proposal_particles": 2.4704149836907163e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 5.017737336743266e-10,
        "transport_matrix": 5.453953955125712e-10
      },
      "failing_fields": [],
      "time_index": 48
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.3750825184929454e-10,
        "observation_log_likelihoods": 4.882916293524886e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.9115199140505865e-10,
        "post_update_log_likelihoods": 4.306158984945796e-09,
        "post_update_log_weights": 2.1556969542757543e-09,
        "post_update_particles": 4.895355232292786e-10,
        "proposal_log_likelihoods": 9.947598300641403e-14,
        "proposal_particles": 4.895355232292786e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.6339339598280276e-09,
        "transport_matrix": 2.779272367803287e-10
      },
      "failing_fields": [],
      "time_index": 49
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.065637047138807e-11,
        "observation_log_likelihoods": 2.4153123945325206e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.3559965650333794e-10,
        "post_update_log_likelihoods": 4.3868197963092825e-09,
        "post_update_log_weights": 3.268780801590765e-10,
        "post_update_particles": 1.247713043994736e-10,
        "proposal_log_likelihoods": 8.08242361927114e-14,
        "proposal_particles": 1.247713043994736e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 4.3168757457578977e-10,
        "transport_matrix": 1.0555606388962246e-10
      },
      "failing_fields": [],
      "time_index": 50
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.5369217837578617e-10,
        "observation_log_likelihoods": 3.5774938567101344e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.4671286407974549e-10,
        "post_update_log_likelihoods": 4.133127617933496e-09,
        "post_update_log_weights": 1.2857963582746379e-09,
        "post_update_particles": 2.2026824808563106e-10,
        "proposal_log_likelihoods": 1.7186252421197423e-13,
        "proposal_particles": 2.2026824808563106e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.963354585806883e-10,
        "transport_matrix": 9.941913958755322e-11
      },
      "failing_fields": [],
      "time_index": 51
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.0007774043383506e-11,
        "observation_log_likelihoods": 5.667510905027484e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.8654011668672865e-10,
        "post_update_log_likelihoods": 4.103128503629705e-09,
        "post_update_log_weights": 1.2041545538465925e-10,
        "post_update_particles": 3.263949110987596e-10,
        "proposal_log_likelihoods": 2.078337502098293e-13,
        "proposal_particles": 3.263949110987596e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.359935049246815e-11,
        "transport_matrix": 1.2934542326092924e-10
      },
      "failing_fields": [],
      "time_index": 52
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.873412867174466e-11,
        "observation_log_likelihoods": 1.1515166598030646e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.913982388719205e-10,
        "post_update_log_likelihoods": 4.161861966167635e-09,
        "post_update_log_weights": 7.870535334575379e-10,
        "post_update_particles": 2.1594814825220965e-10,
        "proposal_log_likelihoods": 1.4299672557172016e-13,
        "proposal_particles": 2.1594814825220965e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 7.443858862643538e-10,
        "transport_matrix": 2.7043256523029413e-10
      },
      "failing_fields": [],
      "time_index": 53
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.0442403325660052e-10,
        "observation_log_likelihoods": 1.702771257328095e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.8416108355244774e-10,
        "post_update_log_likelihoods": 4.366285111245816e-09,
        "post_update_log_weights": 6.743254843399882e-10,
        "post_update_particles": 1.716671249596402e-10,
        "proposal_log_likelihoods": 3.1796787425264483e-13,
        "proposal_particles": 1.716671249596402e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 7.085465547618242e-10,
        "transport_matrix": 1.2998871423697267e-10
      },
      "failing_fields": [],
      "time_index": 54
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.711586676364732e-11,
        "observation_log_likelihoods": 1.3999690295918299e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.0953171702965392e-10,
        "post_update_log_likelihoods": 4.4134083054814255e-09,
        "post_update_log_weights": 1.4967205252958138e-10,
        "post_update_particles": 9.629275155020878e-11,
        "proposal_log_likelihoods": 5.595524044110789e-14,
        "proposal_particles": 9.629275155020878e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.4812062687497018e-10,
        "transport_matrix": 3.949456317542399e-10
      },
      "failing_fields": [],
      "time_index": 55
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.03490582559607e-11,
        "observation_log_likelihoods": 5.860223417641919e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.9096546566288453e-10,
        "post_update_log_likelihoods": 4.363059247225465e-09,
        "post_update_log_weights": 1.0643610437455209e-09,
        "post_update_particles": 2.96381585940253e-10,
        "proposal_log_likelihoods": 1.1102230246251565e-13,
        "proposal_particles": 2.96381585940253e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.553495772252063e-10,
        "transport_matrix": 2.6205171366200375e-10
      },
      "failing_fields": [],
      "time_index": 56
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.885383043604861e-10,
        "observation_log_likelihoods": 8.33648705622636e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.871436587450262e-10,
        "post_update_log_likelihoods": 4.651596441362926e-09,
        "post_update_log_weights": 5.615794496094395e-10,
        "post_update_particles": 4.028493094665464e-10,
        "proposal_log_likelihoods": 4.618527782440651e-14,
        "proposal_particles": 4.028493094665464e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.334617523393263e-10,
        "transport_matrix": 2.943327803706097e-10
      },
      "failing_fields": [],
      "time_index": 57
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.349764909899022e-11,
        "observation_log_likelihoods": 2.717310820798957e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.454365930608219e-10,
        "post_update_log_likelihoods": 4.685105636781373e-09,
        "post_update_log_weights": 2.3170656504589715e-09,
        "post_update_particles": 3.255422598158475e-10,
        "proposal_log_likelihoods": 1.5143442055887135e-13,
        "proposal_particles": 3.255422598158475e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.0118076093922355e-09,
        "transport_matrix": 6.533305008105117e-10
      },
      "failing_fields": [],
      "time_index": 58
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.457567565590125e-10,
        "observation_log_likelihoods": 2.4374458007514477e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.708466784184793e-10,
        "post_update_log_likelihoods": 4.339355541560508e-09,
        "post_update_log_weights": 8.466964906972407e-10,
        "post_update_particles": 4.714024726126809e-10,
        "proposal_log_likelihoods": 2.1405099914773018e-13,
        "proposal_particles": 4.714024726126809e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.489227181802562e-10,
        "transport_matrix": 2.90206081388078e-10
      },
      "failing_fields": [],
      "time_index": 59
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.143056843095792e-10,
        "observation_log_likelihoods": 1.4908341228192512e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.7929703822214833e-10,
        "post_update_log_likelihoods": 4.553669441520469e-09,
        "post_update_log_weights": 1.5965229138714676e-09,
        "post_update_particles": 3.312266017019283e-10,
        "proposal_log_likelihoods": 2.0294876890147862e-13,
        "proposal_particles": 3.312266017019283e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.2357435075216472e-09,
        "transport_matrix": 5.42640155032359e-10
      },
      "failing_fields": [],
      "time_index": 60
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.302891707501203e-11,
        "observation_log_likelihoods": 1.1982903558305225e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.21752624543592e-10,
        "post_update_log_likelihoods": 4.6367034656213946e-09,
        "post_update_log_weights": 4.229627759144705e-10,
        "post_update_particles": 2.6341240300098434e-10,
        "proposal_log_likelihoods": 1.6919798895287386e-13,
        "proposal_particles": 2.6341240300098434e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 3.859934594174774e-10,
        "transport_matrix": 6.153517695395294e-10
      },
      "failing_fields": [],
      "time_index": 61
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.793965555753402e-11,
        "observation_log_likelihoods": 1.5201668812636626e-09,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.902506927668583e-09,
        "post_update_log_likelihoods": 4.5487666966437246e-09,
        "post_update_log_weights": 1.8203278884243446e-08,
        "post_update_particles": 8.506845006195363e-09,
        "proposal_log_likelihoods": 1.6786572132332367e-13,
        "proposal_particles": 8.506845006195363e-09,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.659514259344519e-08,
        "transport_matrix": 3.2962088614141294e-10
      },
      "failing_fields": [],
      "time_index": 62
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.6839418748304524e-11,
        "observation_log_likelihoods": 3.814628612985871e-09,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.506830908468373e-09,
        "post_update_log_likelihoods": 4.53192683380621e-09,
        "post_update_log_weights": 1.4386998703486142e-08,
        "post_update_particles": 2.5236772671632934e-09,
        "proposal_log_likelihoods": 1.829647544582258e-13,
        "proposal_particles": 2.5236772671632934e-09,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.3774725360349294e-08,
        "transport_matrix": 5.1135535528157305e-09
      },
      "failing_fields": [],
      "time_index": 63
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.4659897740187944e-09,
        "observation_log_likelihoods": 9.584402160811578e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.7701517463517575e-09,
        "post_update_log_likelihoods": 5.997904395371734e-09,
        "post_update_log_weights": 1.5960994748098756e-09,
        "post_update_particles": 3.1389504329126794e-09,
        "proposal_log_likelihoods": 2.5002222514558525e-13,
        "proposal_particles": 3.1389504329126794e-09,
        "seed2": 0.0,
        "transition_log_likelihoods": 4.020556332307024e-09,
        "transport_matrix": 5.059486829495086e-09
      },
      "failing_fields": [],
      "time_index": 64
    },
    {
      "deltas": {
        "log_likelihood_increment": 6.757256976186454e-10,
        "observation_log_likelihoods": 5.938005642747157e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.352993882543842e-09,
        "post_update_log_likelihoods": 6.673630537079589e-09,
        "post_update_log_weights": 1.101389335289582e-08,
        "post_update_particles": 9.32061539060669e-10,
        "proposal_log_likelihoods": 2.566835632933362e-13,
        "proposal_particles": 9.32061539060669e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.1616357653565501e-08,
        "transport_matrix": 2.6649190909555642e-09
      },
      "failing_fields": [],
      "time_index": 65
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.5348874110875386e-09,
        "observation_log_likelihoods": 1.3151235656039262e-09,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.3513936636400103e-09,
        "post_update_log_likelihoods": 4.138740905546001e-09,
        "post_update_log_weights": 6.118779705133193e-09,
        "post_update_particles": 1.4367174117069226e-09,
        "proposal_log_likelihoods": 4.627409566637652e-13,
        "proposal_particles": 1.4367174117069226e-09,
        "seed2": 0.0,
        "transition_log_likelihoods": 7.339005847484259e-09,
        "transport_matrix": 3.492464317744748e-09
      },
      "failing_fields": [],
      "time_index": 66
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.638043200027141e-10,
        "observation_log_likelihoods": 1.1190492976709265e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.243805389909539e-10,
        "post_update_log_likelihoods": 3.774928813982115e-09,
        "post_update_log_weights": 1.4049807983695928e-09,
        "post_update_particles": 8.905089998734184e-10,
        "proposal_log_likelihoods": 7.460698725481052e-14,
        "proposal_particles": 8.905089998734184e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.8806960433437325e-09,
        "transport_matrix": 2.855387370992446e-09
      },
      "failing_fields": [],
      "time_index": 67
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.299698457861268e-10,
        "observation_log_likelihoods": 1.7922774375733752e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.8911984745482187e-10,
        "post_update_log_likelihoods": 4.304894218876143e-09,
        "post_update_log_weights": 5.178684148177126e-10,
        "post_update_particles": 2.1009327610954642e-10,
        "proposal_log_likelihoods": 6.88338275267597e-14,
        "proposal_particles": 2.1009327610954642e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.892127117439031e-10,
        "transport_matrix": 6.667869034693297e-10
      },
      "failing_fields": [],
      "time_index": 68
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.2410650285232805e-10,
        "observation_log_likelihoods": 5.0821569175241166e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.212345862062648e-10,
        "post_update_log_likelihoods": 4.428997613104002e-09,
        "post_update_log_weights": 2.1538326677728037e-10,
        "post_update_particles": 3.6413894122233614e-10,
        "proposal_log_likelihoods": 1.7497114868092467e-13,
        "proposal_particles": 3.6413894122233614e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 3.6762681787649854e-10,
        "transport_matrix": 3.6695788074858626e-10
      },
      "failing_fields": [],
      "time_index": 69
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.813926952034308e-11,
        "observation_log_likelihoods": 1.2036127650105755e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.338378628039209e-10,
        "post_update_log_likelihoods": 4.3908556790484e-09,
        "post_update_log_weights": 6.608176228439788e-10,
        "post_update_particles": 3.594209374568891e-10,
        "proposal_log_likelihoods": 1.7852386235972517e-13,
        "proposal_particles": 3.594209374568891e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 5.352678300596381e-10,
        "transport_matrix": 5.06575337233528e-10
      },
      "failing_fields": [],
      "time_index": 70
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.7355228365545372e-11,
        "observation_log_likelihoods": 1.3864820402886835e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.701971979490736e-10,
        "post_update_log_likelihoods": 4.373504225441138e-09,
        "post_update_log_weights": 9.911813592111685e-10,
        "post_update_particles": 2.532942744437605e-10,
        "proposal_log_likelihoods": 2.2382096176443156e-13,
        "proposal_particles": 2.532942744437605e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.1126983778808608e-09,
        "transport_matrix": 3.8034042582069105e-10
      },
      "failing_fields": [],
      "time_index": 71
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.497158201388629e-10,
        "observation_log_likelihoods": 1.5074985704188748e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.3570125285441463e-10,
        "post_update_log_likelihoods": 3.923787517123856e-09,
        "post_update_log_weights": 1.994831855256507e-09,
        "post_update_particles": 4.75495198770659e-10,
        "proposal_log_likelihoods": 1.745270594710746e-13,
        "proposal_particles": 4.75495198770659e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.2937420851576462e-09,
        "transport_matrix": 4.127990171909346e-10
      },
      "failing_fields": [],
      "time_index": 72
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.48843826153211e-10,
        "observation_log_likelihoods": 4.5915271584817674e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.914788410635083e-10,
        "post_update_log_likelihoods": 3.774957235691545e-09,
        "post_update_log_weights": 7.542593216669502e-10,
        "post_update_particles": 2.2851054382044822e-10,
        "proposal_log_likelihoods": 1.0258460747536446e-13,
        "proposal_particles": 2.2851054382044822e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 8.572706988729806e-10,
        "transport_matrix": 4.1870673594957e-10
      },
      "failing_fields": [],
      "time_index": 73
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.9551738006384767e-10,
        "observation_log_likelihoods": 1.8504797694163244e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.044391405637725e-10,
        "post_update_log_likelihoods": 3.970470174863294e-09,
        "post_update_log_weights": 7.239231436528826e-10,
        "post_update_particles": 2.7989699447061867e-10,
        "proposal_log_likelihoods": 1.7985612998927536e-13,
        "proposal_particles": 2.7989699447061867e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.038503279157339e-10,
        "transport_matrix": 2.37410702208507e-10
      },
      "failing_fields": [],
      "time_index": 74
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.3788527531442014e-11,
        "observation_log_likelihoods": 4.8824055909335584e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.667084248424544e-10,
        "post_update_log_likelihoods": 3.936690973205259e-09,
        "post_update_log_weights": 7.021676573515379e-10,
        "post_update_particles": 1.049329512170516e-10,
        "proposal_log_likelihoods": 3.7836400679225335e-13,
        "proposal_particles": 1.049329512170516e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 6.870415347748349e-10,
        "transport_matrix": 3.3699310009183137e-10
      },
      "failing_fields": [],
      "time_index": 75
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.8147750796847504e-10,
        "observation_log_likelihoods": 3.346354304767374e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.959268385893665e-10,
        "post_update_log_likelihoods": 4.21817958340398e-09,
        "post_update_log_weights": 2.5516810886472285e-09,
        "post_update_particles": 5.002220859751105e-10,
        "proposal_log_likelihoods": 1.3500311979441904e-13,
        "proposal_particles": 5.002220859751105e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.935452687007455e-09,
        "transport_matrix": 4.3906878133270766e-10
      },
      "failing_fields": [],
      "time_index": 76
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.285421155245331e-10,
        "observation_log_likelihoods": 1.4482726129472212e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.055703080510284e-09,
        "post_update_log_likelihoods": 4.9467274720882415e-09,
        "post_update_log_weights": 1.5881265191808325e-09,
        "post_update_particles": 1.0148824003408663e-09,
        "proposal_log_likelihoods": 1.936228954946273e-13,
        "proposal_particles": 1.0148824003408663e-09,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.195750248290551e-09,
        "transport_matrix": 8.460995237768998e-10
      },
      "failing_fields": [],
      "time_index": 77
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.1265523503520853e-10,
        "observation_log_likelihoods": 2.9662272638120157e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.2273133620510635e-09,
        "post_update_log_likelihoods": 4.634074457499082e-09,
        "post_update_log_weights": 1.550189754340181e-09,
        "post_update_particles": 4.714593160315417e-10,
        "proposal_log_likelihoods": 4.04121180963557e-13,
        "proposal_particles": 4.714593160315417e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.1594015464643235e-09,
        "transport_matrix": 1.1222924811704615e-09
      },
      "failing_fields": [],
      "time_index": 78
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.0365598924220194e-10,
        "observation_log_likelihoods": 4.248779106319489e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.0815099926730909e-09,
        "post_update_log_likelihoods": 4.330416913944646e-09,
        "post_update_log_weights": 1.1767398166995235e-09,
        "post_update_particles": 4.6270542952697724e-10,
        "proposal_log_likelihoods": 3.659295089164516e-13,
        "proposal_particles": 4.6270542952697724e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.7480101810463111e-09,
        "transport_matrix": 7.559716186378296e-10
      },
      "failing_fields": [],
      "time_index": 79
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.0211762546674663e-09,
        "observation_log_likelihoods": 2.8524937967233654e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 8.798597406212139e-10,
        "post_update_log_likelihoods": 5.3515947229243466e-09,
        "post_update_log_weights": 9.547644896912288e-10,
        "post_update_particles": 9.055156624526717e-10,
        "proposal_log_likelihoods": 3.348432642269472e-13,
        "proposal_particles": 9.055156624526717e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.4161409822577298e-09,
        "transport_matrix": 9.243693727123414e-10
      },
      "failing_fields": [],
      "time_index": 80
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.7645529482024358e-10,
        "observation_log_likelihoods": 2.0385559906799244e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.012804062838768e-09,
        "post_update_log_likelihoods": 5.175138539925683e-09,
        "post_update_log_weights": 8.94982310484238e-10,
        "post_update_particles": 4.632738637155853e-10,
        "proposal_log_likelihoods": 3.9479530755670567e-13,
        "proposal_particles": 4.632738637155853e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 6.594387258473944e-10,
        "transport_matrix": 6.873331348522527e-10
      },
      "failing_fields": [],
      "time_index": 81
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.782743090459007e-10,
        "observation_log_likelihoods": 1.5247558771136482e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 7.180123162697782e-10,
        "post_update_log_likelihoods": 5.653419066220522e-09,
        "post_update_log_weights": 2.293046641455021e-09,
        "post_update_particles": 5.522906576516107e-10,
        "proposal_log_likelihoods": 3.0020430585864233e-13,
        "proposal_particles": 5.522906576516107e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.914450902835597e-09,
        "transport_matrix": 3.780708524026011e-10
      },
      "failing_fields": [],
      "time_index": 82
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.863567657613203e-10,
        "observation_log_likelihoods": 2.4880320026454683e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.256826085542343e-10,
        "post_update_log_likelihoods": 4.7670596359239426e-09,
        "post_update_log_weights": 1.074647038024068e-09,
        "post_update_particles": 4.2086867324542254e-10,
        "proposal_log_likelihoods": 4.773959005888173e-13,
        "proposal_particles": 4.2086867324542254e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.0363408737011923e-09,
        "transport_matrix": 9.51496159640186e-10
      },
      "failing_fields": [],
      "time_index": 83
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.6475620867595353e-10,
        "observation_log_likelihoods": 3.6482816767602344e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.0756731323199347e-10,
        "post_update_log_likelihoods": 4.6022989863558905e-09,
        "post_update_log_weights": 1.904128410501471e-09,
        "post_update_particles": 5.790070645161904e-10,
        "proposal_log_likelihoods": 3.4283687000424834e-13,
        "proposal_particles": 5.790070645161904e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.0514629994750067e-09,
        "transport_matrix": 3.0249225346778985e-10
      },
      "failing_fields": [],
      "time_index": 84
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.8950174762721872e-10,
        "observation_log_likelihoods": 7.412825908659215e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.2861713350484933e-10,
        "post_update_log_likelihoods": 4.412811449583387e-09,
        "post_update_log_weights": 2.9311273408438865e-09,
        "post_update_particles": 3.1252511689672247e-10,
        "proposal_log_likelihoods": 2.62456723021387e-13,
        "proposal_particles": 3.1252511689672247e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.8050184397443445e-09,
        "transport_matrix": 3.17815065931093e-10
      },
      "failing_fields": [],
      "time_index": 85
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.484365963477785e-10,
        "observation_log_likelihoods": 8.921041683151998e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.9627321989901247e-10,
        "post_update_log_likelihoods": 4.264364861228387e-09,
        "post_update_log_weights": 4.047762125480858e-11,
        "post_update_particles": 9.78843672783114e-11,
        "proposal_log_likelihoods": 4.227729277772596e-13,
        "proposal_particles": 9.78843672783114e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.907878299789445e-10,
        "transport_matrix": 5.386952550701096e-10
      },
      "failing_fields": [],
      "time_index": 86
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.2746492750181915e-10,
        "observation_log_likelihoods": 1.4909184997691227e-11,
        "post_resample_log_weights": 4.047762125480858e-11,
        "post_resample_particles": 9.78843672783114e-11,
        "post_update_log_likelihoods": 4.391836228023749e-09,
        "post_update_log_weights": 2.744089400152916e-10,
        "post_update_particles": 3.6266101233195513e-11,
        "proposal_log_likelihoods": 9.281464485866309e-14,
        "proposal_particles": 3.6266101233195513e-11,
        "seed2": 0.0,
        "transition_log_likelihoods": 3.7202063651875505e-10
      },
      "failing_fields": [],
      "time_index": 87
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.8285374042980038e-11,
        "observation_log_likelihoods": 7.520983835718198e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.8266989577095956e-10,
        "post_update_log_likelihoods": 4.420144250616431e-09,
        "post_update_log_weights": 1.0020757557072102e-09,
        "post_update_particles": 5.355786925065331e-10,
        "proposal_log_likelihoods": 1.7985612998927536e-13,
        "proposal_particles": 5.355786925065331e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.549823154486603e-10,
        "transport_matrix": 6.247646844315113e-11
      },
      "failing_fields": [],
      "time_index": 88
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.787494845004403e-10,
        "observation_log_likelihoods": 1.2519829617474443e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.863664943537515e-10,
        "post_update_log_likelihoods": 4.898879524262156e-09,
        "post_update_log_weights": 1.1868763749589561e-09,
        "post_update_particles": 2.45449882640969e-10,
        "proposal_log_likelihoods": 9.681144774731365e-14,
        "proposal_particles": 2.45449882640969e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.7908874383465445e-09,
        "transport_matrix": 4.672113251835697e-10
      },
      "failing_fields": [],
      "time_index": 89
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.539257610261302e-09,
        "observation_log_likelihoods": 1.9977353105105067e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.986375591262913e-10,
        "post_update_log_likelihoods": 3.3596450066397665e-09,
        "post_update_log_weights": 4.971223432903571e-10,
        "post_update_particles": 2.388560460531153e-10,
        "proposal_log_likelihoods": 6.181721801112872e-13,
        "proposal_particles": 2.388560460531153e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 2.0167920666835926e-09,
        "transport_matrix": 4.594698510551609e-10
      },
      "failing_fields": [],
      "time_index": 90
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.250666402720981e-11,
        "observation_log_likelihoods": 1.443534181078121e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.356035449542105e-10,
        "post_update_log_likelihoods": 3.3271305710513843e-09,
        "post_update_log_weights": 5.122009483216061e-10,
        "post_update_particles": 4.126832209294662e-10,
        "proposal_log_likelihoods": 5.924150059399835e-13,
        "proposal_particles": 4.126832209294662e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 5.027365190812816e-10,
        "transport_matrix": 1.850363751110251e-10
      },
      "failing_fields": [],
      "time_index": 91
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.8910339960598321e-10,
        "observation_log_likelihoods": 7.518652367366485e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.2166448110947385e-10,
        "post_update_log_likelihoods": 3.516220203891862e-09,
        "post_update_log_weights": 7.483813568853748e-10,
        "post_update_particles": 6.267555363592692e-10,
        "proposal_log_likelihoods": 6.03073146976385e-13,
        "proposal_particles": 6.267555363592692e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 9.176583937176019e-10,
        "transport_matrix": 7.449741934451026e-10
      },
      "failing_fields": [],
      "time_index": 92
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.1984114528805776e-10,
        "observation_log_likelihoods": 6.125255858080436e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.396696423076719e-10,
        "post_update_log_likelihoods": 3.736062126336037e-09,
        "post_update_log_weights": 8.880483015616392e-10,
        "post_update_particles": 8.159304343280382e-10,
        "proposal_log_likelihoods": 3.4150460237469815e-13,
        "proposal_particles": 8.159304343280382e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.1688001677612192e-09,
        "transport_matrix": 8.281402785748071e-10
      },
      "failing_fields": [],
      "time_index": 93
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.2111860403507535e-09,
        "observation_log_likelihoods": 1.9514612148441302e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.723901435634616e-10,
        "post_update_log_likelihoods": 2.5248709789593704e-09,
        "post_update_log_weights": 7.414673319772191e-10,
        "post_update_particles": 4.0972736314870417e-10,
        "proposal_log_likelihoods": 4.2721381987576024e-13,
        "proposal_particles": 4.0972736314870417e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.4361676292651282e-09,
        "transport_matrix": 4.970599487563732e-10
      },
      "failing_fields": [],
      "time_index": 94
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.3040286628296371e-09,
        "observation_log_likelihoods": 8.339995360984176e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.388098855974022e-10,
        "post_update_log_likelihoods": 3.828887429335737e-09,
        "post_update_log_weights": 5.656639601170355e-10,
        "post_update_particles": 3.5356606531422585e-10,
        "proposal_log_likelihoods": 1.4721557306529576e-13,
        "proposal_particles": 3.5356606531422585e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.7279511155265936e-09,
        "transport_matrix": 2.8672662855111497e-10
      },
      "failing_fields": [],
      "time_index": 95
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.671482952048109e-10,
        "observation_log_likelihoods": 1.855213760393326e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.0102854370616114e-10,
        "post_update_log_likelihoods": 3.996035502495943e-09,
        "post_update_log_weights": 2.891351602585246e-10,
        "post_update_particles": 4.970388545189053e-10,
        "proposal_log_likelihoods": 1.5853984791647235e-13,
        "proposal_particles": 4.970388545189053e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 3.1574343140050587e-10,
        "transport_matrix": 8.432630704824362e-10
      },
      "failing_fields": [],
      "time_index": 96
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.1881907397158784e-10,
        "observation_log_likelihoods": 9.521494703790268e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 8.729994505074501e-10,
        "post_update_log_likelihoods": 4.214854243400623e-09,
        "post_update_log_weights": 1.312591813018571e-09,
        "post_update_particles": 5.48652678844519e-10,
        "proposal_log_likelihoods": 2.646771690706373e-13,
        "proposal_particles": 5.48652678844519e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 1.4211698484700719e-09,
        "transport_matrix": 6.835944310612518e-10
      },
      "failing_fields": [],
      "time_index": 97
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.738254316156599e-11,
        "observation_log_likelihoods": 1.3619372296602705e-10,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.550120363295719e-10,
        "post_update_log_likelihoods": 4.157470812060637e-09,
        "post_update_log_weights": 3.333330056420891e-09,
        "post_update_particles": 6.120899342931807e-10,
        "proposal_log_likelihoods": 8.384404281969182e-13,
        "proposal_particles": 6.120899342931807e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 3.526990255409146e-09,
        "transport_matrix": 6.578678990454279e-10
      },
      "failing_fields": [],
      "time_index": 98
    },
    {
      "deltas": {
        "log_likelihood_increment": 6.417819609083608e-10,
        "observation_log_likelihoods": 8.723999300741525e-11,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.886811038635642e-10,
        "post_update_log_likelihoods": 3.5156801914126845e-09,
        "post_update_log_weights": 1.2056289300232947e-10,
        "post_update_particles": 1.8042101146420464e-10,
        "proposal_log_likelihoods": 3.494982081519993e-13,
        "proposal_particles": 1.8042101146420464e-10,
        "seed2": 0.0,
        "transition_log_likelihoods": 6.477596237175476e-10,
        "transport_matrix": 3.4614591748471923e-10
      },
      "failing_fields": [],
      "time_index": 99
    }
  ],
  "resampling_flags_match": true,
  "series_deltas": {
    "log_likelihoods": 6.673630537079589e-09,
    "log_weights": 1.8203278884243446e-08,
    "particles": 8.506845006195363e-09
  },
  "status": "compared"
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow reference agree in this bounded full 2D run without proposal replay.

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
- No smoothness-surface gradient correctness is concluded.
- No production dtype default is concluded.
