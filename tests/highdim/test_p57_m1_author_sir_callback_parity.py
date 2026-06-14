from __future__ import annotations

import tensorflow as tf

import bayesfilter.highdim as highdim


def _author_neighbor_sets() -> tuple[tuple[int, ...], ...]:
    return (
        (1,),
        (0, 2, 3),
        (1, 3, 4, 5),
        (1, 2, 4),
        (2, 3, 5, 6, 8),
        (2, 4, 6),
        (4, 5, 7, 8),
        (6,),
        (4, 6),
    )


def _author_sir_rk4_rhs(
    state: tf.Tensor,
    neighbor_sets: tuple[tuple[int, ...], ...],
) -> tf.Tensor:
    values = tf.reshape(tf.convert_to_tensor(state, dtype=tf.float64), [1, -1])
    susceptible = values[:, 0::2]
    infectious = values[:, 1::2]
    adjacency = tf.constant(
        [[1.0 if col in neighbors else 0.0 for col in range(9)] for neighbors in neighbor_sets],
        dtype=tf.float64,
    )
    degree = tf.reduce_sum(adjacency, axis=1)
    susceptible_neighbor = tf.linalg.matmul(susceptible, adjacency, transpose_b=True) - susceptible * degree
    infectious_neighbor = tf.linalg.matmul(infectious, adjacency, transpose_b=True) - infectious * degree
    infection = tf.constant(0.1, dtype=tf.float64) * susceptible * infectious
    return tf.reshape(
        tf.stack(
            [
                -infection + 0.5 * susceptible_neighbor,
                infection - tf.constant(18.0, dtype=tf.float64) * infectious + 0.5 * infectious_neighbor,
            ],
            axis=2,
        ),
        [-1],
    )


def _author_sir_step(state: tf.Tensor) -> tf.Tensor:
    current = tf.convert_to_tensor(state, dtype=tf.float64)
    h = tf.constant(0.005, dtype=tf.float64)
    for _ in range(4):
        fp1 = _author_sir_rk4_rhs(current, _author_neighbor_sets())
        fp2 = _author_sir_rk4_rhs(current + fp1 * h / 2.0, _author_neighbor_sets())
        fp3 = _author_sir_rk4_rhs(current + fp2 * h / 2.0, _author_neighbor_sets())
        fp4 = _author_sir_rk4_rhs(current + fp3 * h / 2.0, _author_neighbor_sets())
        current = current + (fp1 + 2.0 * fp2 + 2.0 * fp3 + fp4) * h / 6.0
    return current


def test_p57_m1_author_sir_factory_matches_source_setup_contract() -> None:
    model = highdim.zhao_cui_sir_austria_model()
    payload = model.manifest_payload()

    expected_initial = []
    for index in range(1, 10):
        expected_initial.extend([486.0 + index, 14.0 - index])

    assert model.parameter_dim() == 0
    assert model.state_dim() == 18
    assert model.observation_dim() == 9
    assert model.neighbor_sets == _author_neighbor_sets()
    assert model.observed_state_indices() == tuple(range(1, 18, 2))
    assert payload["rk4_variant"] == "zhao_cui_sir_step"
    assert payload["process_noise_policy"] == "clip_susceptible_after_noise"
    tf.debugging.assert_near(
        model.initial_mean,
        tf.constant(expected_initial, dtype=tf.float64),
        atol=0.0,
    )
    assert float(tf.reduce_max(tf.abs(model.process_covariance - tf.eye(18, dtype=tf.float64))).numpy()) == 0.0
    assert float(
        tf.reduce_max(tf.abs(model.observation_covariance - 100.0 * tf.eye(9, dtype=tf.float64))).numpy()
    ) == 0.0
    assert float(tf.reduce_max(tf.abs(model.initial_covariance - tf.eye(18, dtype=tf.float64))).numpy()) == 0.0


def test_p57_m1_author_sir_transition_mean_matches_mlx_sir_step() -> None:
    model = highdim.zhao_cui_sir_austria_model()
    state = model.initial_mean + tf.linspace(
        tf.constant(-0.45, dtype=tf.float64),
        tf.constant(0.45, dtype=tf.float64),
        18,
    )

    expected = _author_sir_step(state)
    actual = model.transition_mean(state)[0]

    tf.debugging.assert_near(actual, expected, atol=3e-11)


def test_p57_m1_author_sir_likelihood_uses_source_observation_matrix() -> None:
    model = highdim.zhao_cui_sir_austria_model()
    state = model.initial_mean[tf.newaxis, :]
    observation = model.initial_mean[1::2] + tf.linspace(
        tf.constant(-1.0, dtype=tf.float64),
        tf.constant(1.0, dtype=tf.float64),
        9,
    )

    actual = model.observation_log_density(tf.zeros([0], dtype=tf.float64), state, observation, t=1)[0]
    changed_susceptible = tf.identity(model.initial_mean).numpy()
    changed_susceptible[0::2] += 1000.0
    unchanged = model.observation_log_density(
        tf.zeros([0], dtype=tf.float64),
        tf.constant(changed_susceptible[tf.newaxis, :], dtype=tf.float64),
        observation,
        t=1,
    )[0]

    tf.debugging.assert_near(actual, unchanged, atol=0.0)


def test_p57_m1_author_sir_push_clips_only_susceptible_after_noise() -> None:
    model = highdim.zhao_cui_sir_austria_model()
    noise = tf.zeros([1, 18], dtype=tf.float64)
    noise = tf.tensor_scatter_nd_update(
        noise,
        indices=tf.constant([[0, 0], [0, 1]], dtype=tf.int32),
        updates=tf.constant([-1.0e6, -1.0e6], dtype=tf.float64),
    )

    pushed = model.transition_push_from_standard_normal(
        tf.zeros([0], dtype=tf.float64),
        model.initial_mean,
        noise,
        t=1,
    )[0]

    assert float(pushed[0].numpy()) == 0.0
    assert float(pushed[1].numpy()) < 0.0


def test_p57_m1_old_p30_fixture_is_explicitly_not_author_sir_austria() -> None:
    author = highdim.zhao_cui_sir_austria_model()
    old_fixture = highdim.p30_spatial_sir_fixture_model(9)

    assert old_fixture.neighbor_sets != author.neighbor_sets
    assert old_fixture.manifest_payload()["rk4_variant"] == "classical"
    assert old_fixture.manifest_payload()["process_noise_policy"] == "diagnose_negative_after_noise"
