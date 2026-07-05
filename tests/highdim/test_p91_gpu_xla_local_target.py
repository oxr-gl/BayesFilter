from __future__ import annotations

import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64
FINAL_TIME = 4


def _fixture_path(
    model: highdim.ParameterizedZhaoCuiSIRSSM,
    theta: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    states = [model.base_model.initial_mean]
    observations = []
    observation_offsets = tf.linspace(
        tf.constant(-0.2, dtype=DTYPE),
        tf.constant(0.2, dtype=DTYPE),
        model.observation_dim(),
    )
    for time_index in range(FINAL_TIME + 1):
        current = states[-1]
        observations.append(model.infectious_components(current)[0] + observation_offsets)
        if time_index < FINAL_TIME:
            transition_mean = model.transition_mean(theta, current[tf.newaxis, :])[0]
            perturbation = tf.linspace(
                tf.constant(-0.03, dtype=DTYPE),
                tf.constant(0.03, dtype=DTYPE),
                model.state_dim(),
            ) * tf.cast(time_index + 1, DTYPE)
            states.append(transition_mean + perturbation)
    return tf.stack(states), tf.stack(observations)


def _eager_complete_data_log_density(
    model: highdim.ParameterizedZhaoCuiSIRSSM,
    theta: tf.Tensor,
    states: tf.Tensor,
    observations: tf.Tensor,
) -> tf.Tensor:
    value = model.initial_log_density(theta, states[0:1])[0]
    for time_index in range(1, FINAL_TIME + 1):
        value = value + model.transition_log_density(
            theta,
            states[time_index - 1 : time_index],
            states[time_index : time_index + 1],
            t=time_index,
        )[0]
    for time_index in range(FINAL_TIME + 1):
        value = value + model.observation_log_density(
            theta,
            states[time_index : time_index + 1],
            observations[time_index],
            t=time_index,
        )[0]
    return value


def test_p91_gpu_xla_local_complete_data_helper_matches_eager_model() -> None:
    model = highdim.parameterized_zhao_cui_sir_austria_model()
    theta = tf.constant([0.0, 0.0, 0.0], dtype=DTYPE)
    states, observations = _fixture_path(model, theta)

    with tf.GradientTape() as eager_tape:
        eager_tape.watch(theta)
        eager_value = _eager_complete_data_log_density(model, theta, states, observations)
    eager_score = eager_tape.gradient(eager_value, theta)

    with tf.GradientTape() as helper_tape:
        helper_tape.watch(theta)
        helper_value = highdim.zhao_cui_sir_austria_local_complete_data_log_density_xla(
            theta,
            states,
            observations,
        )
    helper_score = helper_tape.gradient(helper_value, theta)

    assert eager_score is not None
    assert helper_score is not None
    tf.debugging.assert_near(helper_value, eager_value, atol=1e-9, rtol=1e-12)
    tf.debugging.assert_near(helper_score, eager_score, atol=1e-8, rtol=1e-9)


def test_p91_gpu_xla_batched_helper_matches_looped_single_helper() -> None:
    model = highdim.parameterized_zhao_cui_sir_austria_model()
    theta = tf.constant([0.0, 0.0, 0.0], dtype=DTYPE)
    states, observations = _fixture_path(model, theta)
    batched_states = tf.stack(
        [
            states,
            states
            + tf.linspace(
                tf.constant(-0.01, dtype=DTYPE),
                tf.constant(0.01, dtype=DTYPE),
                model.state_dim(),
            )[tf.newaxis, :],
        ]
    )
    batched_observations = tf.stack(
        [
            observations,
            observations
            + tf.linspace(
                tf.constant(-0.005, dtype=DTYPE),
                tf.constant(0.005, dtype=DTYPE),
                model.observation_dim(),
            )[tf.newaxis, :],
        ]
    )

    batched_values = highdim.zhao_cui_sir_austria_batched_local_complete_data_log_density_xla(
        theta,
        batched_states,
        batched_observations,
    )
    looped_values = tf.stack(
        [
            highdim.zhao_cui_sir_austria_local_complete_data_log_density_xla(
                theta,
                batched_states[index],
                batched_observations[index],
            )
            for index in range(2)
        ]
    )

    tf.debugging.assert_near(batched_values, looped_values, atol=1e-9, rtol=1e-12)
