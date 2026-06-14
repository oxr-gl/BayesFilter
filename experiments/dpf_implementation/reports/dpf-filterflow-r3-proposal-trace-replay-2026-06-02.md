# Filterflow R3 Proposal Trace Replay

## Decision

`filterflow_r3_trace_replay_transport_matrix_delta_localized`

## Trace Validation

```json
{
  "official_trace_deltas": {
    "log_likelihoods": 3.0517578125e-05,
    "log_weights": 0.0,
    "particles": 0.0
  },
  "official_trace_match": true,
  "tolerance": 5e-05
}
```

## Replay Comparison

### Computed Resampling State

```json
{
  "finite_bayesfilter_replay": true,
  "first_failure": {
    "delta": 8.130073547363281e-05,
    "field": "post_update_log_weights",
    "time_index": 7
  },
  "implementation_agreement": false,
  "per_time_deltas": [
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 0
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.1920928955078125e-07,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 1.9073486328125e-06,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [],
      "time_index": 1
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 7.450580596923828e-09
      },
      "failing_fields": [],
      "time_index": 2
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.2351741790771484e-08
      },
      "failing_fields": [],
      "time_index": 3
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.6689300537109375e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.5367431640625e-07,
        "post_update_log_likelihoods": 1.9073486328125e-06,
        "post_update_log_weights": 7.867813110351562e-06,
        "proposal_log_likelihoods": 5.7220458984375e-06,
        "transition_log_likelihoods": 3.814697265625e-06,
        "transport_matrix": 1.4901161193847656e-08
      },
      "failing_fields": [],
      "time_index": 4
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.9073486328125e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.9073486328125e-06,
        "post_update_log_likelihoods": 3.814697265625e-06,
        "post_update_log_weights": 2.1457672119140625e-06,
        "proposal_log_likelihoods": 5.4836273193359375e-06,
        "transition_log_likelihoods": 1.9073486328125e-06,
        "transport_matrix": 2.86102294921875e-06
      },
      "failing_fields": [],
      "time_index": 5
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.76837158203125e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.9073486328125e-06,
        "post_update_log_likelihoods": 1.9073486328125e-06,
        "post_update_log_weights": 1.621246337890625e-05,
        "proposal_log_likelihoods": 2.765655517578125e-05,
        "transition_log_likelihoods": 6.67572021484375e-06,
        "transport_matrix": 1.1026859283447266e-06
      },
      "failing_fields": [],
      "time_index": 6
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.1682510375976562e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.0503997802734375e-05,
        "post_update_log_likelihoods": 1.33514404296875e-05,
        "post_update_log_weights": 8.130073547363281e-05,
        "proposal_log_likelihoods": 4.982948303222656e-05,
        "transition_log_likelihoods": 4.291534423828125e-05,
        "transport_matrix": 9.967014193534851e-06
      },
      "failing_fields": [
        "post_update_log_weights"
      ],
      "time_index": 7
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.0265579223632812e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 1.52587890625e-05,
        "post_update_log_weights": 1.633167266845703e-05,
        "proposal_log_likelihoods": 3.0994415283203125e-06,
        "transition_log_likelihoods": 1.5735626220703125e-05,
        "transport_matrix": 2.154707908630371e-05
      },
      "failing_fields": [],
      "time_index": 8
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.821487426757812e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.814697265625e-06,
        "post_update_log_likelihoods": 2.47955322265625e-05,
        "post_update_log_weights": 9.775161743164062e-06,
        "proposal_log_likelihoods": 4.38690185546875e-05,
        "transition_log_likelihoods": 2.5272369384765625e-05,
        "transport_matrix": 6.884336471557617e-06
      },
      "failing_fields": [],
      "time_index": 9
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.827976226806641e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.76837158203125e-06,
        "post_update_log_likelihoods": 3.0517578125e-05,
        "post_update_log_weights": 1.5497207641601562e-05,
        "proposal_log_likelihoods": 2.4557113647460938e-05,
        "transition_log_likelihoods": 1.7642974853515625e-05,
        "transport_matrix": 5.453824996948242e-06
      },
      "failing_fields": [],
      "time_index": 10
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.5497207641601562e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.814697265625e-06,
        "post_update_log_likelihoods": 2.86102294921875e-05,
        "post_update_log_weights": 5.3882598876953125e-05,
        "proposal_log_likelihoods": 5.459785461425781e-05,
        "transition_log_likelihoods": 8.58306884765625e-06,
        "transport_matrix": 5.0067901611328125e-06
      },
      "failing_fields": [
        "post_update_log_weights",
        "proposal_log_likelihoods"
      ],
      "time_index": 11
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.0371208190917969e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.71661376953125e-05,
        "post_update_log_likelihoods": 4.00543212890625e-05,
        "post_update_log_weights": 2.6464462280273438e-05,
        "proposal_log_likelihoods": 4.601478576660156e-05,
        "transition_log_likelihoods": 7.367134094238281e-05,
        "transport_matrix": 2.300739288330078e-05
      },
      "failing_fields": [
        "transition_log_likelihoods"
      ],
      "time_index": 12
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.887580871582031e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 7.62939453125e-06,
        "post_update_log_likelihoods": 3.62396240234375e-05,
        "post_update_log_weights": 1.823902130126953e-05,
        "proposal_log_likelihoods": 4.0531158447265625e-05,
        "transition_log_likelihoods": 2.5272369384765625e-05,
        "transport_matrix": 7.510185241699219e-06
      },
      "failing_fields": [],
      "time_index": 13
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.0503997802734375e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.1444091796875e-05,
        "post_update_log_likelihoods": 1.52587890625e-05,
        "post_update_log_weights": 7.796287536621094e-05,
        "proposal_log_likelihoods": 5.936622619628906e-05,
        "transition_log_likelihoods": 8.344650268554688e-06,
        "transport_matrix": 7.867813110351562e-06
      },
      "failing_fields": [
        "post_update_log_weights",
        "proposal_log_likelihoods"
      ],
      "time_index": 14
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.933906555175781e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.6702880859375e-05,
        "post_update_log_likelihoods": 1.9073486328125e-05,
        "post_update_log_weights": 1.2040138244628906e-05,
        "proposal_log_likelihoods": 5.5789947509765625e-05,
        "transition_log_likelihoods": 4.2438507080078125e-05,
        "transport_matrix": 3.331899642944336e-05
      },
      "failing_fields": [
        "proposal_log_likelihoods"
      ],
      "time_index": 15
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.0503997802734375e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 7.62939453125e-06,
        "post_update_log_likelihoods": 1.9073486328125e-06,
        "post_update_log_weights": 4.0531158447265625e-05,
        "proposal_log_likelihoods": 7.486343383789062e-05,
        "transition_log_likelihoods": 1.3828277587890625e-05,
        "transport_matrix": 5.543231964111328e-06
      },
      "failing_fields": [
        "proposal_log_likelihoods"
      ],
      "time_index": 16
    },
    {
      "deltas": {
        "log_likelihood_increment": 9.5367431640625e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.239776611328125e-05,
        "post_update_log_likelihoods": 3.814697265625e-06,
        "post_update_log_weights": 2.8848648071289062e-05,
        "proposal_log_likelihoods": 3.9577484130859375e-05,
        "transition_log_likelihoods": 5.984306335449219e-05,
        "transport_matrix": 1.5050172805786133e-05
      },
      "failing_fields": [
        "transition_log_likelihoods"
      ],
      "time_index": 17
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.0848045349121094e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.1444091796875e-05,
        "post_update_log_likelihoods": 1.52587890625e-05,
        "post_update_log_weights": 2.7298927307128906e-05,
        "proposal_log_likelihoods": 1.1444091796875e-05,
        "transition_log_likelihoods": 4.9591064453125e-05,
        "transport_matrix": 1.4886260032653809e-05
      },
      "failing_fields": [],
      "time_index": 18
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00017523765563964844,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.866455078125e-05,
        "post_update_log_likelihoods": 0.00016021728515625,
        "post_update_log_weights": 0.00046181678771972656,
        "proposal_log_likelihoods": 0.00010395050048828125,
        "transition_log_likelihoods": 0.0003905296325683594,
        "transport_matrix": 1.6897916793823242e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 19
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.0728836059570312e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.621246337890625e-05,
        "post_update_log_likelihoods": 0.00016021728515625,
        "post_update_log_weights": 3.3736228942871094e-05,
        "proposal_log_likelihoods": 0.0001583099365234375,
        "transition_log_likelihoods": 0.00012350082397460938,
        "transport_matrix": 8.225440979003906e-05
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 20
    },
    {
      "deltas": {
        "log_likelihood_increment": 9.489059448242188e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 6.4849853515625e-05,
        "post_update_log_weights": 8.58306884765625e-05,
        "proposal_log_likelihoods": 0.0001900196075439453,
        "transition_log_likelihoods": 0.00013446807861328125,
        "transport_matrix": 1.1742115020751953e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 21
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.3909759521484375e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 7.2479248046875e-05,
        "post_update_log_weights": 2.9802322387695312e-05,
        "proposal_log_likelihoods": 7.104873657226562e-05,
        "transition_log_likelihoods": 5.0067901611328125e-05,
        "transport_matrix": 4.887580871582031e-06
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 22
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.344650268554688e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 2.9802322387695312e-05,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 7.2479248046875e-05,
        "post_update_log_weights": 2.8967857360839844e-05,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 23
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.296966552734375e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.866455078125e-05,
        "post_update_log_likelihoods": 1.1444091796875e-05,
        "post_update_log_weights": 0.00025081634521484375,
        "proposal_log_likelihoods": 0.0001456737518310547,
        "transition_log_likelihoods": 0.00014162063598632812,
        "transport_matrix": 1.2159347534179688e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 24
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.2901763916015625e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.814697265625e-05,
        "post_update_log_likelihoods": 2.288818359375e-05,
        "post_update_log_weights": 0.00010037422180175781,
        "proposal_log_likelihoods": 0.00011301040649414062,
        "transition_log_likelihoods": 9.09566879272461e-05,
        "transport_matrix": 4.646182060241699e-05
      },
      "failing_fields": [
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 25
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.225440979003906e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.765655517578125e-05,
        "post_update_log_likelihoods": 3.4332275390625e-05,
        "post_update_log_weights": 4.088878631591797e-05,
        "proposal_log_likelihoods": 0.000125885009765625,
        "transition_log_likelihoods": 7.677078247070312e-05,
        "transport_matrix": 4.121661186218262e-05
      },
      "failing_fields": [
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 26
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.344650268554688e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.57763671875e-05,
        "post_update_log_likelihoods": 3.4332275390625e-05,
        "post_update_log_weights": 7.605552673339844e-05,
        "proposal_log_likelihoods": 6.365776062011719e-05,
        "transition_log_likelihoods": 2.5033950805664062e-05,
        "transport_matrix": 2.1755695343017578e-05
      },
      "failing_fields": [
        "post_update_log_weights",
        "proposal_log_likelihoods"
      ],
      "time_index": 27
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.702278137207031e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.337860107421875e-05,
        "post_update_log_likelihoods": 0.000118255615234375,
        "post_update_log_weights": 0.0001442432403564453,
        "proposal_log_likelihoods": 0.0002484321594238281,
        "transition_log_likelihoods": 6.532669067382812e-05,
        "transport_matrix": 3.808736801147461e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 28
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.066394805908203e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0001373291015625,
        "post_update_log_likelihoods": 6.866455078125e-05,
        "post_update_log_weights": 0.00015294551849365234,
        "proposal_log_likelihoods": 6.0558319091796875e-05,
        "transition_log_likelihoods": 0.00020647048950195312,
        "transport_matrix": 7.665157318115234e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 29
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.269050598144531e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.0001220703125,
        "post_update_log_weights": 5.507469177246094e-05,
        "proposal_log_likelihoods": 1.5735626220703125e-05,
        "transition_log_likelihoods": 8.296966552734375e-05,
        "transport_matrix": 8.064508438110352e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 30
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.390975952148438e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 5.054473876953125e-05,
        "post_update_log_likelihoods": 4.57763671875e-05,
        "post_update_log_weights": 0.000362396240234375,
        "proposal_log_likelihoods": 3.981590270996094e-05,
        "transition_log_likelihoods": 0.0002880096435546875,
        "transport_matrix": 4.845857620239258e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_weights",
        "transition_log_likelihoods"
      ],
      "time_index": 31
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.0279159545898438e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 1.52587890625e-05,
        "post_update_log_weights": 0.00010132789611816406,
        "proposal_log_likelihoods": 0.00010824203491210938,
        "transition_log_likelihoods": 0.00015211105346679688,
        "transport_matrix": 5.751848220825195e-06
      },
      "failing_fields": [
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 32
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.086162567138672e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.57763671875e-05,
        "post_update_log_likelihoods": 3.4332275390625e-05,
        "post_update_log_weights": 8.761882781982422e-05,
        "proposal_log_likelihoods": 0.00043964385986328125,
        "transition_log_likelihoods": 0.00042057037353515625,
        "transport_matrix": 1.481175422668457e-05
      },
      "failing_fields": [
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 33
    },
    {
      "deltas": {
        "log_likelihood_increment": 9.775161743164062e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 2.288818359375e-05,
        "post_update_log_weights": 6.699562072753906e-05,
        "proposal_log_likelihoods": 6.747245788574219e-05,
        "transition_log_likelihoods": 3.0040740966796875e-05,
        "transport_matrix": 2.9712915420532227e-05
      },
      "failing_fields": [
        "post_update_log_weights",
        "proposal_log_likelihoods"
      ],
      "time_index": 34
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.947185516357422e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 2.6702880859375e-05,
        "post_update_log_weights": 7.617473602294922e-05,
        "proposal_log_likelihoods": 0.00015544891357421875,
        "transition_log_likelihoods": 0.0001583099365234375,
        "transport_matrix": 1.895427703857422e-05
      },
      "failing_fields": [
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 35
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.5735626220703125e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 4.57763671875e-05,
        "post_update_log_weights": 4.839897155761719e-05,
        "proposal_log_likelihoods": 0.00010538101196289062,
        "transition_log_likelihoods": 6.031990051269531e-05,
        "transport_matrix": 3.24249267578125e-05
      },
      "failing_fields": [
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 36
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.082389831542969e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.000125885009765625,
        "post_update_log_weights": 1.6450881958007812e-05,
        "proposal_log_likelihoods": 0.00022029876708984375,
        "transition_log_likelihoods": 0.0003032684326171875,
        "transport_matrix": 2.6304274797439575e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 37
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0002703666687011719,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.00014495849609375,
        "post_update_log_weights": 0.0004429817199707031,
        "proposal_log_likelihoods": 0.0005095005035400391,
        "transition_log_likelihoods": 0.0004067420959472656,
        "transport_matrix": 1.4275312423706055e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 38
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.7550926208496094e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0001220703125,
        "post_update_log_likelihoods": 0.0001068115234375,
        "post_update_log_weights": 0.00010502338409423828,
        "proposal_log_likelihoods": 0.0003101825714111328,
        "transition_log_likelihoods": 0.0003371238708496094,
        "transport_matrix": 7.812678813934326e-05
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 39
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.2874603271484375e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.00011444091796875,
        "post_update_log_weights": 0.00014543533325195312,
        "proposal_log_likelihoods": 0.00013208389282226562,
        "transition_log_likelihoods": 9.012222290039062e-05,
        "transport_matrix": 4.088878631591797e-05
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 40
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0010118484497070312,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0002593994140625,
        "post_update_log_likelihoods": 0.00089263916015625,
        "post_update_log_weights": 0.0016794204711914062,
        "proposal_log_likelihoods": 0.0009150505065917969,
        "transition_log_likelihoods": 0.001293182373046875,
        "transport_matrix": 0.00010266900062561035
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 41
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0004957914352416992,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00039958953857421875,
        "post_update_log_likelihoods": 0.000396728515625,
        "post_update_log_weights": 0.0009251832962036133,
        "proposal_log_likelihoods": 0.0018558502197265625,
        "transition_log_likelihoods": 0.00089263916015625,
        "transport_matrix": 0.00041100382804870605
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 42
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0003695487976074219,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0010113716125488281,
        "post_update_log_likelihoods": 0.000762939453125,
        "post_update_log_weights": 0.0009541511535644531,
        "proposal_log_likelihoods": 0.00048160552978515625,
        "transition_log_likelihoods": 0.0011525154113769531,
        "transport_matrix": 0.000698089599609375
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 43
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00016498565673828125,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00013136863708496094,
        "post_update_log_likelihoods": 0.00060272216796875,
        "post_update_log_weights": 0.00014591217041015625,
        "proposal_log_likelihoods": 5.1975250244140625e-05,
        "transition_log_likelihoods": 0.00023794174194335938,
        "transport_matrix": 0.00042623281478881836
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 44
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.504753112792969e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0002593994140625,
        "post_update_log_likelihoods": 0.000640869140625,
        "post_update_log_weights": 0.0002396106719970703,
        "proposal_log_likelihoods": 0.001071929931640625,
        "transition_log_likelihoods": 0.0010519027709960938,
        "transport_matrix": 7.110834121704102e-05
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 45
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.390975952148438e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.0005645751953125,
        "post_update_log_weights": 0.00014781951904296875,
        "proposal_log_likelihoods": 0.0003070831298828125,
        "transition_log_likelihoods": 0.00013971328735351562,
        "transport_matrix": 6.398558616638184e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 46
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0001392364501953125,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.00042724609375,
        "post_update_log_weights": 0.0002474784851074219,
        "proposal_log_likelihoods": 0.0002951622009277344,
        "transition_log_likelihoods": 0.00018262863159179688,
        "transport_matrix": 2.199411392211914e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 47
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.4497509002685547e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.036064147949219e-05,
        "post_update_log_likelihoods": 0.00040435791015625,
        "post_update_log_weights": 6.556510925292969e-05,
        "proposal_log_likelihoods": 8.20159912109375e-05,
        "transition_log_likelihoods": 2.2411346435546875e-05,
        "transport_matrix": 0.0001323223114013672
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 48
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.6743621826171875e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.0003509521484375,
        "post_update_log_weights": 0.00016927719116210938,
        "proposal_log_likelihoods": 8.749961853027344e-05,
        "transition_log_likelihoods": 0.00019550323486328125,
        "transport_matrix": 2.2649765014648438e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 49
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.358457565307617e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.19739294052124e-05,
        "post_update_log_likelihoods": 0.00029754638671875,
        "post_update_log_weights": 0.0001233816146850586,
        "proposal_log_likelihoods": 0.00022149085998535156,
        "transition_log_likelihoods": 7.891654968261719e-05,
        "transport_matrix": 9.998679161071777e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 50
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00035262107849121094,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00018310546875,
        "post_update_log_likelihoods": 0.0006561279296875,
        "post_update_log_weights": 0.0012590885162353516,
        "proposal_log_likelihoods": 0.0003814697265625,
        "transition_log_likelihoods": 0.0008730888366699219,
        "transport_matrix": 4.538893699645996e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 51
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0001862049102783203,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0002288818359375,
        "post_update_log_likelihoods": 0.0008392333984375,
        "post_update_log_weights": 0.00019800662994384766,
        "proposal_log_likelihoods": 0.0009665489196777344,
        "transition_log_likelihoods": 0.0006289482116699219,
        "transport_matrix": 0.00016951560974121094
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 52
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00013697147369384766,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00010907649993896484,
        "post_update_log_likelihoods": 0.00070953369140625,
        "post_update_log_weights": 0.00027692317962646484,
        "proposal_log_likelihoods": 0.00039768218994140625,
        "transition_log_likelihoods": 0.0003285408020019531,
        "transport_matrix": 9.250640869140625e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 53
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.2479248046875e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00020813941955566406,
        "post_update_log_likelihoods": 0.000640869140625,
        "post_update_log_weights": 8.082389831542969e-05,
        "proposal_log_likelihoods": 0.0005269050598144531,
        "transition_log_likelihoods": 0.0006632804870605469,
        "transport_matrix": 0.00024127960205078125
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 54
    },
    {
      "deltas": {
        "log_likelihood_increment": 6.264448165893555e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.86522912979126e-05,
        "post_update_log_likelihoods": 0.000701904296875,
        "post_update_log_weights": 8.416175842285156e-05,
        "proposal_log_likelihoods": 0.000125885009765625,
        "transition_log_likelihoods": 0.00018405914306640625,
        "transport_matrix": 4.029273986816406e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 55
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.368492126464844e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.00078582763671875,
        "post_update_log_weights": 0.00011134147644042969,
        "proposal_log_likelihoods": 0.00017976760864257812,
        "transition_log_likelihoods": 6.4849853515625e-05,
        "transport_matrix": 4.374980926513672e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 56
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.968311309814453e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 7.700920104980469e-05,
        "post_update_log_likelihoods": 0.00081634521484375,
        "post_update_log_weights": 6.902217864990234e-05,
        "proposal_log_likelihoods": 0.00044274330139160156,
        "transition_log_likelihoods": 0.0004563331604003906,
        "transport_matrix": 5.549192428588867e-05
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 57
    },
    {
      "deltas": {
        "log_likelihood_increment": 9.751319885253906e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0002593994140625,
        "post_update_log_likelihoods": 0.00091552734375,
        "post_update_log_weights": 0.0012085437774658203,
        "proposal_log_likelihoods": 0.0004220008850097656,
        "transition_log_likelihoods": 0.0009026527404785156,
        "transport_matrix": 3.9249658584594727e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 58
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0007717609405517578,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00022685527801513672,
        "post_update_log_likelihoods": 0.00014495849609375,
        "post_update_log_weights": 0.0009124279022216797,
        "proposal_log_likelihoods": 0.001880645751953125,
        "transition_log_likelihoods": 0.0005474090576171875,
        "transport_matrix": 0.0005021095275878906
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 59
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00054931640625,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0006916522979736328,
        "post_update_log_likelihoods": 0.00069427490234375,
        "post_update_log_weights": 0.0010981559753417969,
        "proposal_log_likelihoods": 0.00016570091247558594,
        "transition_log_likelihoods": 0.0008537769317626953,
        "transport_matrix": 0.0006479024887084961
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 60
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.647804260253906e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.000244140625,
        "post_update_log_likelihoods": 0.00066375732421875,
        "post_update_log_weights": 0.0004825592041015625,
        "proposal_log_likelihoods": 0.0008592605590820312,
        "transition_log_likelihoods": 0.0012378692626953125,
        "transport_matrix": 0.0003534555435180664
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 61
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0002079010009765625,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.771087646484375e-05,
        "post_update_log_likelihoods": 0.0008697509765625,
        "post_update_log_weights": 0.00024366378784179688,
        "proposal_log_likelihoods": 0.0003185272216796875,
        "transition_log_likelihoods": 0.000274658203125,
        "transport_matrix": 0.00025272369384765625
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 62
    },
    {
      "deltas": {
        "log_likelihood_increment": 6.115436553955078e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00013208389282226562,
        "post_update_log_likelihoods": 0.0008087158203125,
        "post_update_log_weights": 5.805492401123047e-05,
        "proposal_log_likelihoods": 0.00018477439880371094,
        "transition_log_likelihoods": 0.0003039836883544922,
        "transport_matrix": 0.00017702579498291016
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 63
    },
    {
      "deltas": {
        "log_likelihood_increment": 6.771087646484375e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0001220703125,
        "post_update_log_likelihoods": 0.00074005126953125,
        "post_update_log_weights": 0.000392913818359375,
        "proposal_log_likelihoods": 0.0004401206970214844,
        "transition_log_likelihoods": 0.00045418739318847656,
        "transport_matrix": 4.217028617858887e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 64
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.000240325927734375,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.365776062011719e-05,
        "post_update_log_likelihoods": 0.00049591064453125,
        "post_update_log_weights": 0.00033283233642578125,
        "proposal_log_likelihoods": 0.000278472900390625,
        "transition_log_likelihoods": 0.0006761550903320312,
        "transport_matrix": 0.0001958608627319336
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 65
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0001360177993774414,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00014972686767578125,
        "post_update_log_likelihoods": 0.00035858154296875,
        "post_update_log_weights": 0.0003790855407714844,
        "proposal_log_likelihoods": 0.00030517578125,
        "transition_log_likelihoods": 0.0004551410675048828,
        "transport_matrix": 0.0001761913299560547
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 66
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.7523765563964844e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.00034332275390625,
        "post_update_log_weights": 6.639957427978516e-05,
        "proposal_log_likelihoods": 0.0005211830139160156,
        "transition_log_likelihoods": 0.0004372596740722656,
        "transport_matrix": 4.2304396629333496e-05
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 67
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.3947486877441406e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 7.343292236328125e-05,
        "post_update_log_likelihoods": 0.00032806396484375,
        "post_update_log_weights": 8.690357208251953e-05,
        "proposal_log_likelihoods": 0.00014853477478027344,
        "transition_log_likelihoods": 0.00022172927856445312,
        "transport_matrix": 5.905330181121826e-05
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 68
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.9802322387695312e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.00029754638671875,
        "post_update_log_weights": 0.0002071857452392578,
        "proposal_log_likelihoods": 0.0003294944763183594,
        "transition_log_likelihoods": 0.0005669593811035156,
        "transport_matrix": 3.001093864440918e-05
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 69
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.1365623474121094e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.000335693359375,
        "post_update_log_weights": 0.00014293193817138672,
        "proposal_log_likelihoods": 8.928775787353516e-05,
        "transition_log_likelihoods": 9.512901306152344e-05,
        "transport_matrix": 1.4424324035644531e-05
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 70
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0005639791488647461,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 8.726119995117188e-05,
        "post_update_log_likelihoods": 0.0002288818359375,
        "post_update_log_weights": 0.0003064870834350586,
        "proposal_log_likelihoods": 0.0005466938018798828,
        "transition_log_likelihoods": 0.00023412704467773438,
        "transport_matrix": 0.00010445713996887207
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 71
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00021648406982421875,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.9591064453125e-05,
        "post_update_log_likelihoods": 0.0004425048828125,
        "post_update_log_weights": 0.0007452964782714844,
        "proposal_log_likelihoods": 0.0005745887756347656,
        "transition_log_likelihoods": 0.0003871917724609375,
        "transport_matrix": 0.0001645982265472412
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 72
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00012671947479248047,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00014638900756835938,
        "post_update_log_likelihoods": 0.0005645751953125,
        "post_update_log_weights": 0.0007867813110351562,
        "proposal_log_likelihoods": 0.00019359588623046875,
        "transition_log_likelihoods": 0.0008535385131835938,
        "transport_matrix": 0.00020518898963928223
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 73
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.24249267578125e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.00060272216796875,
        "post_update_log_weights": 9.72747802734375e-05,
        "proposal_log_likelihoods": 5.8650970458984375e-05,
        "transition_log_likelihoods": 0.00016117095947265625,
        "transport_matrix": 0.00011220574378967285
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 74
    },
    {
      "deltas": {
        "log_likelihood_increment": 6.556510925292969e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.00066375732421875,
        "post_update_log_weights": 0.00024199485778808594,
        "proposal_log_likelihoods": 0.00037980079650878906,
        "transition_log_likelihoods": 9.298324584960938e-05,
        "transport_matrix": 6.654858589172363e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 75
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.225440979003906e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.0006561279296875,
        "post_update_log_weights": 0.0001291036605834961,
        "proposal_log_likelihoods": 0.00021409988403320312,
        "transition_log_likelihoods": 0.0003008842468261719,
        "transport_matrix": 0.0001544356346130371
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 76
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.559226989746094e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.00057220458984375,
        "post_update_log_weights": 0.00040459632873535156,
        "proposal_log_likelihoods": 0.00046515464782714844,
        "transition_log_likelihoods": 5.555152893066406e-05,
        "transport_matrix": 6.335973739624023e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 77
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.8715858459472656e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.1552734375e-05,
        "post_update_log_likelihoods": 0.0005950927734375,
        "post_update_log_weights": 9.167194366455078e-05,
        "proposal_log_likelihoods": 0.0003304481506347656,
        "transition_log_likelihoods": 0.0003368854522705078,
        "transport_matrix": 0.00014254450798034668
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 78
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.6862831115722656e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0001220703125,
        "post_update_log_likelihoods": 0.00054168701171875,
        "post_update_log_weights": 0.00021791458129882812,
        "proposal_log_likelihoods": 0.0002627372741699219,
        "transition_log_likelihoods": 0.00023937225341796875,
        "transport_matrix": 4.0531158447265625e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 79
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.410743713378906e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 7.343292236328125e-05,
        "post_update_log_likelihoods": 0.0005950927734375,
        "post_update_log_weights": 0.00012564659118652344,
        "proposal_log_likelihoods": 0.00013780593872070312,
        "transition_log_likelihoods": 0.0002493858337402344,
        "transport_matrix": 0.00014418363571166992
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 80
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0002218484878540039,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.1552734375e-05,
        "post_update_log_likelihoods": 0.000823974609375,
        "post_update_log_weights": 2.8014183044433594e-05,
        "proposal_log_likelihoods": 0.00046634674072265625,
        "transition_log_likelihoods": 0.0006995201110839844,
        "transport_matrix": 9.042024612426758e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 81
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.14984130859375e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.0008697509765625,
        "post_update_log_weights": 0.00019550323486328125,
        "proposal_log_likelihoods": 0.0001480579376220703,
        "transition_log_likelihoods": 0.0003504753112792969,
        "transport_matrix": 1.7583370208740234e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 82
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00017595291137695312,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.1552734375e-05,
        "post_update_log_likelihoods": 0.0006866455078125,
        "post_update_log_weights": 0.0003275871276855469,
        "proposal_log_likelihoods": 0.0003838539123535156,
        "transition_log_likelihoods": 0.00044536590576171875,
        "transport_matrix": 9.563565254211426e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 83
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00011348724365234375,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.1552734375e-05,
        "post_update_log_likelihoods": 0.00079345703125,
        "post_update_log_weights": 0.0004222393035888672,
        "proposal_log_likelihoods": 0.0005626678466796875,
        "transition_log_likelihoods": 0.0008153915405273438,
        "transport_matrix": 0.00019489973783493042
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 84
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0003854036331176758,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00020599365234375,
        "post_update_log_likelihoods": 0.0011749267578125,
        "post_update_log_weights": 0.00018787384033203125,
        "proposal_log_likelihoods": 0.0005846023559570312,
        "transition_log_likelihoods": 0.0009965896606445312,
        "transport_matrix": 0.00012487173080444336
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 85
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0001308917999267578,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.1552734375e-05,
        "post_update_log_likelihoods": 0.0010528564453125,
        "post_update_log_weights": 0.0013606548309326172,
        "proposal_log_likelihoods": 0.0006737709045410156,
        "transition_log_likelihoods": 0.0008177757263183594,
        "transport_matrix": 6.0617923736572266e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 86
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.001873016357421875,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.000396728515625,
        "post_update_log_likelihoods": 0.000823974609375,
        "post_update_log_weights": 0.0028047561645507812,
        "proposal_log_likelihoods": 0.0003337860107421875,
        "transition_log_likelihoods": 0.0018243789672851562,
        "transport_matrix": 0.0003254711627960205
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 87
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0006036758422851562,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0005054473876953125,
        "post_update_log_likelihoods": 0.000213623046875,
        "post_update_log_weights": 0.0026445388793945312,
        "proposal_log_likelihoods": 0.0014166831970214844,
        "transition_log_likelihoods": 0.0015339851379394531,
        "transport_matrix": 0.0005972981452941895
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 88
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0007169246673583984,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.000457763671875,
        "post_update_log_likelihoods": 0.0009307861328125,
        "post_update_log_weights": 0.0017032623291015625,
        "proposal_log_likelihoods": 0.0019211769104003906,
        "transition_log_likelihoods": 0.003067493438720703,
        "transport_matrix": 0.0006383657455444336
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 89
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.0067901611328125e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00054931640625,
        "post_update_log_likelihoods": 0.000946044921875,
        "post_update_log_weights": 0.003458738327026367,
        "proposal_log_likelihoods": 0.0008795261383056641,
        "transition_log_likelihoods": 0.004342555999755859,
        "transport_matrix": 0.0005817711353302002
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 90
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00023186206817626953,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00038433074951171875,
        "post_update_log_likelihoods": 0.001190185546875,
        "post_update_log_weights": 0.0013407468795776367,
        "proposal_log_likelihoods": 0.0004696846008300781,
        "transition_log_likelihoods": 0.0012850761413574219,
        "transport_matrix": 0.0005508363246917725
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 91
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00030243396759033203,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00070953369140625,
        "post_update_log_likelihoods": 0.001495361328125,
        "post_update_log_weights": 0.001006484031677246,
        "proposal_log_likelihoods": 0.0003085136413574219,
        "transition_log_likelihoods": 0.0012624263763427734,
        "transport_matrix": 0.0004782676696777344
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 92
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.177757263183594e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0003604888916015625,
        "post_update_log_likelihoods": 0.0014190673828125,
        "post_update_log_weights": 0.0003666877746582031,
        "proposal_log_likelihoods": 0.0009131431579589844,
        "transition_log_likelihoods": 0.0011017322540283203,
        "transport_matrix": 0.0005702972412109375
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 93
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00023871660232543945,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00011730194091796875,
        "post_update_log_likelihoods": 0.00164794921875,
        "post_update_log_weights": 0.00079345703125,
        "proposal_log_likelihoods": 0.0003821849822998047,
        "transition_log_likelihoods": 0.000392913818359375,
        "transport_matrix": 0.0001589059829711914
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 94
    },
    {
      "deltas": {
        "log_likelihood_increment": 9.1552734375e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0001220703125,
        "post_update_log_likelihoods": 0.001556396484375,
        "post_update_log_weights": 0.0004591941833496094,
        "proposal_log_likelihoods": 0.00036144256591796875,
        "transition_log_likelihoods": 0.0006818771362304688,
        "transport_matrix": 0.00012105703353881836
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 95
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0001894235610961914,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 8.487701416015625e-05,
        "post_update_log_likelihoods": 0.001739501953125,
        "post_update_log_weights": 0.0003134012222290039,
        "proposal_log_likelihoods": 0.0005435943603515625,
        "transition_log_likelihoods": 0.0004687309265136719,
        "transport_matrix": 0.00019669532775878906
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 96
    },
    {
      "deltas": {
        "log_likelihood_increment": 6.073713302612305e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.00020313262939453125,
        "post_update_log_likelihoods": 0.001800537109375,
        "post_update_log_weights": 7.802248001098633e-05,
        "proposal_log_likelihoods": 0.000949859619140625,
        "transition_log_likelihoods": 0.0008111000061035156,
        "transport_matrix": 0.0002008974552154541
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 97
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00028777122497558594,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0001220703125,
        "post_update_log_likelihoods": 0.0020904541015625,
        "post_update_log_weights": 0.0009124279022216797,
        "proposal_log_likelihoods": 0.0009546279907226562,
        "transition_log_likelihoods": 0.0003771781921386719,
        "transport_matrix": 9.077787399291992e-05
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 98
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.00012356042861938477,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.000244140625,
        "post_update_log_likelihoods": 0.0019683837890625,
        "post_update_log_weights": 0.0005087852478027344,
        "proposal_log_likelihoods": 0.0005862712860107422,
        "transition_log_likelihoods": 0.0006895065307617188,
        "transport_matrix": 0.0005056262016296387
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods",
        "transport_matrix"
      ],
      "time_index": 99
    }
  ],
  "resampling_flags_match": true,
  "series_deltas": {
    "log_likelihoods": 0.0020904541015625,
    "log_weights": 0.003458738327026367,
    "particles": 0.0
  },
  "status": "compared"
}
```

### Traced Resampling State

```json
{
  "finite_bayesfilter_replay": true,
  "first_failure": {
    "status": "no_failure"
  },
  "implementation_agreement": true,
  "per_time_deltas": [
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 0
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 1
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 2
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 3
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 4
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 5
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 6
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 7
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 8
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 9
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 10
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 11
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 12
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 13
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 14
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 15
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 16
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 17
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 18
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 19
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 20
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 21
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 22
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 23
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 24
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 25
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 26
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 27
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 28
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 29
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 30
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 31
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 32
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 33
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 34
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 35
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 36
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 37
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 38
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 39
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 40
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 41
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 42
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 43
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 44
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 45
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 46
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 47
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 48
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 49
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 50
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 51
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 52
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 53
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 54
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 55
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 56
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 57
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 58
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 59
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 60
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 61
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 62
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 63
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 64
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 65
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 66
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 67
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 68
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 69
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 70
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 71
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 72
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 73
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 74
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 75
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 76
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 77
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 78
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 79
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 80
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 81
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 82
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 83
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 84
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 85
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 86
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 87
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 88
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 89
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 90
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 91
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 92
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 93
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 94
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 95
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 96
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 97
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 98
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 99
    }
  ],
  "resampling_flags_match": true,
  "series_deltas": {
    "log_likelihoods": 0.0,
    "log_weights": 0.0,
    "particles": 0.0
  },
  "status": "compared"
}
```

### Traced Input, Computed Resampling State

```json
{
  "finite_bayesfilter_replay": true,
  "first_failure": {
    "delta": 7.486343383789062e-05,
    "field": "proposal_log_likelihoods",
    "time_index": 16
  },
  "implementation_agreement": false,
  "per_time_deltas": [
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 0
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.1920928955078125e-07,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 1.9073486328125e-06,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [],
      "time_index": 1
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 7.450580596923828e-09
      },
      "failing_fields": [],
      "time_index": 2
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.2351741790771484e-08
      },
      "failing_fields": [],
      "time_index": 3
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.6689300537109375e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.5367431640625e-07,
        "post_update_log_likelihoods": 1.9073486328125e-06,
        "post_update_log_weights": 7.867813110351562e-06,
        "proposal_log_likelihoods": 5.7220458984375e-06,
        "transition_log_likelihoods": 3.814697265625e-06,
        "transport_matrix": 1.4901161193847656e-08
      },
      "failing_fields": [],
      "time_index": 4
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.5762786865234375e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.5367431640625e-07,
        "post_update_log_likelihoods": 1.9073486328125e-06,
        "post_update_log_weights": 8.344650268554688e-07,
        "proposal_log_likelihoods": 3.5762786865234375e-06,
        "transition_log_likelihoods": 4.76837158203125e-06,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [],
      "time_index": 5
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.0265579223632812e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.9073486328125e-06,
        "post_update_log_likelihoods": 1.9073486328125e-06,
        "post_update_log_weights": 5.602836608886719e-06,
        "proposal_log_likelihoods": 3.337860107421875e-06,
        "transition_log_likelihoods": 7.62939453125e-06,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [],
      "time_index": 6
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 1.9073486328125e-06,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [],
      "time_index": 7
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.5762786865234375e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.9073486328125e-06,
        "post_update_log_likelihoods": 1.9073486328125e-06,
        "post_update_log_weights": 4.76837158203125e-07,
        "proposal_log_likelihoods": 4.291534423828125e-06,
        "transition_log_likelihoods": 4.0531158447265625e-06,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [],
      "time_index": 8
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.3113021850585938e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.9073486328125e-06,
        "post_update_log_likelihoods": 3.814697265625e-06,
        "post_update_log_weights": 1.0013580322265625e-05,
        "proposal_log_likelihoods": 7.271766662597656e-06,
        "transition_log_likelihoods": 1.8596649169921875e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [],
      "time_index": 9
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.7881393432617188e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.76837158203125e-07,
        "post_update_log_likelihoods": 3.814697265625e-06,
        "post_update_log_weights": 7.152557373046875e-07,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 9.5367431640625e-07,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [],
      "time_index": 10
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 3.814697265625e-06,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [],
      "time_index": 11
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 3.814697265625e-06,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 0.0
      },
      "failing_fields": [],
      "time_index": 12
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.1457672119140625e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.814697265625e-06,
        "post_update_log_likelihoods": 7.62939453125e-06,
        "post_update_log_weights": 9.298324584960938e-06,
        "proposal_log_likelihoods": 3.337860107421875e-05,
        "transition_log_likelihoods": 3.24249267578125e-05,
        "transport_matrix": 1.1920928955078125e-07
      },
      "failing_fields": [],
      "time_index": 13
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 7.62939453125e-06,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 1.4901161193847656e-08
      },
      "failing_fields": [],
      "time_index": 14
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.5762786865234375e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.814697265625e-06,
        "post_update_log_likelihoods": 7.62939453125e-06,
        "post_update_log_weights": 1.3113021850585938e-06,
        "proposal_log_likelihoods": 4.291534423828125e-06,
        "transition_log_likelihoods": 2.6226043701171875e-06,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [],
      "time_index": 15
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.990795135498047e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 7.62939453125e-06,
        "post_update_log_likelihoods": 1.33514404296875e-05,
        "post_update_log_weights": 4.1484832763671875e-05,
        "proposal_log_likelihoods": 7.486343383789062e-05,
        "transition_log_likelihoods": 1.3470649719238281e-05,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "proposal_log_likelihoods"
      ],
      "time_index": 16
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.76837158203125e-07,
        "post_update_log_likelihoods": 1.52587890625e-05,
        "post_update_log_weights": 9.5367431640625e-07,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 9.5367431640625e-07,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [],
      "time_index": 17
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.62939453125e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 7.62939453125e-06,
        "post_update_log_likelihoods": 2.288818359375e-05,
        "post_update_log_weights": 7.62939453125e-06,
        "proposal_log_likelihoods": 1.5497207641601562e-05,
        "transition_log_likelihoods": 1.9073486328125e-06,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [],
      "time_index": 18
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 2.288818359375e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 1.0913936421275139e-10
      },
      "failing_fields": [],
      "time_index": 19
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 2.288818359375e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [],
      "time_index": 20
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 2.288818359375e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 4.656612873077393e-10
      },
      "failing_fields": [],
      "time_index": 21
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.9073486328125e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 7.62939453125e-06,
        "post_update_log_likelihoods": 1.9073486328125e-05,
        "post_update_log_weights": 5.7220458984375e-06,
        "proposal_log_likelihoods": 1.8596649169921875e-05,
        "transition_log_likelihoods": 1.0967254638671875e-05,
        "transport_matrix": 5.587935447692871e-09
      },
      "failing_fields": [],
      "time_index": 22
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 1.9073486328125e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 23
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.384185791015625e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 1.52587890625e-05,
        "post_update_log_weights": 3.0994415283203125e-05,
        "proposal_log_likelihoods": 3.337860107421875e-05,
        "transition_log_likelihoods": 7.152557373046875e-06,
        "transport_matrix": 8.940696716308594e-08
      },
      "failing_fields": [],
      "time_index": 24
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.76837158203125e-07,
        "post_update_log_likelihoods": 1.52587890625e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [],
      "time_index": 25
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 1.52587890625e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.2351741790771484e-08
      },
      "failing_fields": [],
      "time_index": 26
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.6808509826660156e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 3.0517578125e-05,
        "post_update_log_weights": 2.0503997802734375e-05,
        "proposal_log_likelihoods": 7.402896881103516e-05,
        "transition_log_likelihoods": 3.6716461181640625e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "proposal_log_likelihoods"
      ],
      "time_index": 27
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.1920928955078125e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.76837158203125e-07,
        "post_update_log_likelihoods": 3.0517578125e-05,
        "post_update_log_weights": 1.1920928955078125e-06,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 1.430511474609375e-06,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [],
      "time_index": 28
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.125999450683594e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 2.6702880859375e-05,
        "post_update_log_weights": 1.9669532775878906e-05,
        "proposal_log_likelihoods": 1.6689300537109375e-06,
        "transition_log_likelihoods": 2.6464462280273438e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [],
      "time_index": 29
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 2.6702880859375e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 0.0
      },
      "failing_fields": [],
      "time_index": 30
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 2.6702880859375e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [],
      "time_index": 31
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 2.6702880859375e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [],
      "time_index": 32
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 2.6702880859375e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 1.0186340659856796e-10
      },
      "failing_fields": [],
      "time_index": 33
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 2.6702880859375e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.2351741790771484e-08
      },
      "failing_fields": [],
      "time_index": 34
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.7344951629638672e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 1.1444091796875e-05,
        "post_update_log_weights": 8.618831634521484e-05,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.00010347366333007812,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_weights",
        "transition_log_likelihoods"
      ],
      "time_index": 35
    },
    {
      "deltas": {
        "log_likelihood_increment": 6.985664367675781e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 6.103515625e-05,
        "post_update_log_weights": 0.0002810955047607422,
        "proposal_log_likelihoods": 0.00031185150146484375,
        "transition_log_likelihoods": 3.910064697265625e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods"
      ],
      "time_index": 36
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 6.103515625e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 5.587935447692871e-09
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 37
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.76837158203125e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 6.103515625e-05,
        "post_update_log_weights": 3.5762786865234375e-05,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 3.62396240234375e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 38
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0001672506332397461,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.0002288818359375,
        "post_update_log_weights": 0.0001894235610961914,
        "proposal_log_likelihoods": 0.0002415180206298828,
        "transition_log_likelihoods": 0.00011515617370605469,
        "transport_matrix": 8.940696716308594e-08
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 39
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0002288818359375,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 1.1175870895385742e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 40
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.9073486328125e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 0.0002288818359375,
        "post_update_log_weights": 6.961822509765625e-05,
        "proposal_log_likelihoods": 6.961822509765625e-05,
        "transition_log_likelihoods": 0.000141143798828125,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 41
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.4066696166992188e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 0.000213623046875,
        "post_update_log_weights": 0.0002567768096923828,
        "proposal_log_likelihoods": 0.0002300739288330078,
        "transition_log_likelihoods": 0.0001125335693359375,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 42
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.000213623046875,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 1.4901161193847656e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 43
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.000213623046875,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 1.1175870895385742e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 44
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.000213623046875,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 45
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.76837158203125e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.76837158203125e-07,
        "post_update_log_likelihoods": 0.000213623046875,
        "post_update_log_weights": 9.5367431640625e-07,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 1.430511474609375e-06,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 46
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.8715858459472656e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 0.00023651123046875,
        "post_update_log_weights": 4.470348358154297e-05,
        "proposal_log_likelihoods": 7.224082946777344e-05,
        "transition_log_likelihoods": 6.747245788574219e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 47
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.231929779052734e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.00023651123046875,
        "post_update_log_weights": 0.00010728836059570312,
        "proposal_log_likelihoods": 3.695487976074219e-05,
        "transition_log_likelihoods": 7.486343383789062e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "transition_log_likelihoods"
      ],
      "time_index": 48
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.47955322265625e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 0.0002593994140625,
        "post_update_log_weights": 4.3392181396484375e-05,
        "proposal_log_likelihoods": 4.3392181396484375e-05,
        "transition_log_likelihoods": 2.47955322265625e-05,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 49
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0002593994140625,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 0.0
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 50
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.3113021850585938e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 0.00025177001953125,
        "post_update_log_weights": 7.414817810058594e-05,
        "proposal_log_likelihoods": 0.00012683868408203125,
        "transition_log_likelihoods": 0.00015497207641601562,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 51
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.933906555175781e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 0.000244140625,
        "post_update_log_weights": 9.5367431640625e-06,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 1.3470649719238281e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 52
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.000244140625,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 1.7462298274040222e-10
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 53
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.1920928955078125e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 0.000244140625,
        "post_update_log_weights": 1.7881393432617188e-06,
        "proposal_log_likelihoods": 6.079673767089844e-06,
        "transition_log_likelihoods": 4.649162292480469e-06,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 54
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 7.450580596923828e-09,
        "post_update_log_likelihoods": 0.000244140625,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 55
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.000244140625,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 1.4901161193847656e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 56
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.463859558105469e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 0.00025177001953125,
        "post_update_log_weights": 1.5854835510253906e-05,
        "proposal_log_likelihoods": 4.553794860839844e-05,
        "transition_log_likelihoods": 2.1219253540039062e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 57
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.838539123535156e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.0002899169921875,
        "post_update_log_weights": 3.838539123535156e-05,
        "proposal_log_likelihoods": 4.291534423828125e-05,
        "transition_log_likelihoods": 3.337860107421875e-05,
        "transport_matrix": 8.940696716308594e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 58
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.291534423828125e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.57763671875e-05,
        "post_update_log_likelihoods": 0.000244140625,
        "post_update_log_weights": 0.00024127960205078125,
        "proposal_log_likelihoods": 0.00020456314086914062,
        "transition_log_likelihoods": 7.963180541992188e-05,
        "transport_matrix": 8.940696716308594e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 59
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.7418136596679688e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 0.000213623046875,
        "post_update_log_weights": 0.0002014636993408203,
        "proposal_log_likelihoods": 0.00016570091247558594,
        "transition_log_likelihoods": 6.29425048828125e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 60
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.499622344970703e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 1.52587890625e-05,
        "post_update_log_likelihoods": 0.00012969970703125,
        "post_update_log_weights": 0.0003241300582885742,
        "proposal_log_likelihoods": 0.000335693359375,
        "transition_log_likelihoods": 7.367134094238281e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 61
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.014636993408203e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.0001068115234375,
        "post_update_log_weights": 6.401538848876953e-05,
        "proposal_log_likelihoods": 1.0609626770019531e-05,
        "transition_log_likelihoods": 9.489059448242188e-05,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "transition_log_likelihoods"
      ],
      "time_index": 62
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0001068115234375,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 0.0
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 63
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.1920928955078125e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.384185791015625e-07,
        "post_update_log_likelihoods": 0.0001068115234375,
        "post_update_log_weights": 8.344650268554688e-07,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 9.5367431640625e-07,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 64
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 2.384185791015625e-07,
        "post_update_log_likelihoods": 0.0001068115234375,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 65
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.76837158203125e-07,
        "post_update_log_likelihoods": 0.0001068115234375,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 66
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.1920928955078125e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.76837158203125e-07,
        "post_update_log_likelihoods": 0.0001068115234375,
        "post_update_log_weights": 7.152557373046875e-07,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 1.1920928955078125e-06,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 67
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0001068115234375,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 68
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.5497207641601562e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 9.1552734375e-05,
        "post_update_log_weights": 4.38690185546875e-05,
        "proposal_log_likelihoods": 6.556510925292969e-06,
        "transition_log_likelihoods": 6.604194641113281e-05,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 69
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.1696090698242188e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 6.866455078125e-05,
        "post_update_log_weights": 4.1484832763671875e-05,
        "proposal_log_likelihoods": 0.00019311904907226562,
        "transition_log_likelihoods": 0.00023031234741210938,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 70
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 4.76837158203125e-07,
        "post_update_log_likelihoods": 6.866455078125e-05,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 71
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0002608299255371094,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.00032806396484375,
        "post_update_log_weights": 0.000408172607421875,
        "proposal_log_likelihoods": 0.0006799697875976562,
        "transition_log_likelihoods": 4.673004150390625e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods"
      ],
      "time_index": 72
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.00032806396484375,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 3.259629011154175e-09
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 73
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.000102996826171875,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.00022125244140625,
        "post_update_log_weights": 0.0004057884216308594,
        "proposal_log_likelihoods": 0.0005474090576171875,
        "transition_log_likelihoods": 9.202957153320312e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 74
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.800060272216797e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.000244140625,
        "post_update_log_weights": 8.809566497802734e-05,
        "proposal_log_likelihoods": 5.888938903808594e-05,
        "transition_log_likelihoods": 4.7206878662109375e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods"
      ],
      "time_index": 75
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.000244140625,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.2351741790771484e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 76
    },
    {
      "deltas": {
        "log_likelihood_increment": 4.76837158203125e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.5367431640625e-07,
        "post_update_log_likelihoods": 0.000244140625,
        "post_update_log_weights": 1.1920928955078125e-06,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 1.6689300537109375e-06,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 77
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.1920928955078125e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.00025177001953125,
        "post_update_log_weights": 2.1696090698242188e-05,
        "proposal_log_likelihoods": 0.000164031982421875,
        "transition_log_likelihoods": 0.0001304149627685547,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 78
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.5762786865234375e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.00025177001953125,
        "post_update_log_weights": 4.458427429199219e-05,
        "proposal_log_likelihoods": 8.702278137207031e-05,
        "transition_log_likelihoods": 4.7206878662109375e-05,
        "transport_matrix": 1.1920928955078125e-07
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "proposal_log_likelihoods"
      ],
      "time_index": 79
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.7789344787597656e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.0002899169921875,
        "post_update_log_weights": 9.59634780883789e-05,
        "proposal_log_likelihoods": 0.00020956993103027344,
        "transition_log_likelihoods": 0.00034332275390625,
        "transport_matrix": 8.940696716308594e-08
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 80
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.6868114471435547e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.000274658203125,
        "post_update_log_weights": 7.557868957519531e-05,
        "proposal_log_likelihoods": 0.00024127960205078125,
        "transition_log_likelihoods": 0.00015592575073242188,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 81
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.1920928955078125e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.5367431640625e-07,
        "post_update_log_likelihoods": 0.000274658203125,
        "post_update_log_weights": 1.6689300537109375e-06,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 1.9073486328125e-06,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 82
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.000274658203125,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 3.725290298461914e-09
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 83
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.0728836059570312e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.0002899169921875,
        "post_update_log_weights": 4.267692565917969e-05,
        "proposal_log_likelihoods": 0.00013303756713867188,
        "transition_log_likelihoods": 0.00018644332885742188,
        "transport_matrix": 2.9802322387695312e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 84
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.960464477539062e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.0002899169921875,
        "post_update_log_weights": 0.000118255615234375,
        "proposal_log_likelihoods": 0.00010418891906738281,
        "transition_log_likelihoods": 0.0002231597900390625,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 85
    },
    {
      "deltas": {
        "log_likelihood_increment": 5.9604644775390625e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.000274658203125,
        "post_update_log_weights": 0.00011229515075683594,
        "proposal_log_likelihoods": 6.175041198730469e-05,
        "transition_log_likelihoods": 0.00017976760864257812,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 86
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.000274658203125,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 1.4901161193847656e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 87
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.384185791015625e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.5367431640625e-07,
        "post_update_log_likelihoods": 0.000274658203125,
        "post_update_log_weights": 2.384185791015625e-07,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 2.384185791015625e-07,
        "transport_matrix": 1.4901161193847656e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 88
    },
    {
      "deltas": {
        "log_likelihood_increment": 3.814697265625e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.000274658203125,
        "post_update_log_weights": 4.124641418457031e-05,
        "proposal_log_likelihoods": 6.723403930664062e-05,
        "transition_log_likelihoods": 0.00011229515075683594,
        "transport_matrix": 2.2351741790771484e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 89
    },
    {
      "deltas": {
        "log_likelihood_increment": 8.440017700195312e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.0001983642578125,
        "post_update_log_weights": 8.440017700195312e-05,
        "proposal_log_likelihoods": 0.0001494884490966797,
        "transition_log_likelihoods": 9.72747802734375e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 90
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0001983642578125,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 2.3646862246096134e-11
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 91
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0001983642578125,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 7.450580596923828e-09
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 92
    },
    {
      "deltas": {
        "log_likelihood_increment": 9.417533874511719e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 3.0517578125e-05,
        "post_update_log_likelihoods": 0.0001983642578125,
        "post_update_log_weights": 1.8477439880371094e-05,
        "proposal_log_likelihoods": 4.363059997558594e-05,
        "transition_log_likelihoods": 7.152557373046875e-05,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 93
    },
    {
      "deltas": {
        "log_likelihood_increment": 6.318092346191406e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.0001373291015625,
        "post_update_log_weights": 0.0001811981201171875,
        "proposal_log_likelihoods": 0.00038242340087890625,
        "transition_log_likelihoods": 0.0001895427703857422,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "log_likelihood_increment",
        "post_resample_particles",
        "post_update_log_likelihoods",
        "post_update_log_weights",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 94
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0001373291015625,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0,
        "transport_matrix": 0.0
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 95
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.9550323486328125e-05,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.0001068115234375,
        "post_update_log_weights": 4.863739013671875e-05,
        "proposal_log_likelihoods": 0.00027179718017578125,
        "transition_log_likelihoods": 0.0002033710479736328,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 96
    },
    {
      "deltas": {
        "log_likelihood_increment": 1.5497207641601562e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.5367431640625e-07,
        "post_update_log_likelihoods": 0.0001068115234375,
        "post_update_log_weights": 2.2649765014648438e-06,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 3.814697265625e-06,
        "transport_matrix": 7.450580596923828e-09
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 97
    },
    {
      "deltas": {
        "log_likelihood_increment": 2.384185791015625e-07,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 9.5367431640625e-07,
        "post_update_log_likelihoods": 0.0001068115234375,
        "post_update_log_weights": 1.6689300537109375e-06,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 1.9073486328125e-06,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_update_log_likelihoods"
      ],
      "time_index": 98
    },
    {
      "deltas": {
        "log_likelihood_increment": 7.212162017822266e-06,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 6.103515625e-05,
        "post_update_log_likelihoods": 0.0001220703125,
        "post_update_log_weights": 1.138448715209961e-05,
        "proposal_log_likelihoods": 0.00016736984252929688,
        "transition_log_likelihoods": 0.000148773193359375,
        "transport_matrix": 5.960464477539063e-08
      },
      "failing_fields": [
        "post_resample_particles",
        "post_update_log_likelihoods",
        "proposal_log_likelihoods",
        "transition_log_likelihoods"
      ],
      "time_index": 99
    }
  ],
  "resampling_flags_match": true,
  "series_deltas": {
    "log_likelihoods": 0.00032806396484375,
    "log_weights": 0.000408172607421875,
    "particles": 0.0
  },
  "status": "compared"
}
```

### Traced Input, Traced Transport Matrix

```json
{
  "finite_bayesfilter_replay": true,
  "first_failure": {
    "status": "no_failure"
  },
  "implementation_agreement": true,
  "per_time_deltas": [
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 0
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 1
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 2
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 3
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 4
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 5
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 6
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 7
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 8
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 9
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 10
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 11
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 12
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 13
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 14
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 15
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 16
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 17
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 18
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 19
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 20
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 21
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 22
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 23
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 24
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 25
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 26
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 27
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 28
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 29
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 30
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 31
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 32
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 33
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 34
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 35
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 36
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 37
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 38
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 39
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 40
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 41
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 42
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 43
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 44
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 45
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 46
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 47
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 48
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 49
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 50
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 51
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 52
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 53
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 54
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 55
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 56
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 57
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 58
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 59
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 60
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 61
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 62
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 63
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 64
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 65
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 66
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 67
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 68
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 69
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 70
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 71
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 72
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 73
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 74
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 75
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 76
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 77
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 78
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 79
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 80
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 81
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 82
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 83
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 84
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 85
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 86
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 87
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 88
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 89
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 90
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 91
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 92
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 93
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 94
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 95
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 96
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 97
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 98
    },
    {
      "deltas": {
        "log_likelihood_increment": 0.0,
        "observation_log_likelihoods": 0.0,
        "post_resample_log_weights": 0.0,
        "post_resample_particles": 0.0,
        "post_update_log_likelihoods": 0.0,
        "post_update_log_weights": 0.0,
        "proposal_log_likelihoods": 0.0,
        "transition_log_likelihoods": 0.0
      },
      "failing_fields": [],
      "time_index": 99
    }
  ],
  "resampling_flags_match": true,
  "series_deltas": {
    "log_likelihoods": 0.0,
    "log_weights": 0.0,
    "particles": 0.0
  },
  "status": "compared"
}
```

## Interpretation

BayesFilter matches filterflow when filterflow's traced transport matrix is applied from the exact pre-resampling state, but not when BayesFilter computes that matrix. The remaining discrepancy is localized to tiny transport-matrix deltas in the 2D RegularisedTransform mirror; those deltas are amplified by the proposal-density terms.

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
