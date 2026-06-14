from __future__ import annotations

import math

import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _filter_config(seed: str = "p50-m3-sequential") -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(2),),
        measure_convention=_convention(),
        deterministic_seed=seed,
    )


def _lgssm() -> highdim.LinearGaussianSSM:
    return highdim.LinearGaussianSSM(
        initial_mean=tf.constant([0.1, -0.2], dtype=DTYPE),
        initial_covariance=tf.constant([[1.0, 0.2], [0.2, 0.7]], dtype=DTYPE),
        transition_matrix=tf.constant([[0.8, 0.1], [-0.05, 0.6]], dtype=DTYPE),
        transition_covariance=tf.constant([[0.12, 0.02], [0.02, 0.10]], dtype=DTYPE),
        observation_matrix=tf.constant([[1.0, 0.3]], dtype=DTYPE),
        observation_covariance=tf.constant([[0.16]], dtype=DTYPE),
    )


def _observations() -> tf.Tensor:
    return tf.constant([[0.15], [-0.05], [0.08]], dtype=DTYPE)


def _mvn_log_prob_zero_mean(value: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    chol = tf.linalg.cholesky(covariance)
    solve = tf.linalg.cholesky_solve(chol, tf.reshape(value, [-1, 1]))[:, 0]
    dim = tf.cast(tf.shape(value)[0], DTYPE)
    log_det = 2.0 * tf.reduce_sum(tf.math.log(tf.linalg.diag_part(chol)))
    return -0.5 * (
        dim * tf.math.log(tf.constant(2.0 * math.pi, dtype=DTYPE))
        + log_det
        + tf.reduce_sum(value * solve)
    )


def _symmetrize(matrix: tf.Tensor) -> tf.Tensor:
    return 0.5 * (matrix + tf.transpose(matrix))


def _independent_kalman(
    model: highdim.LinearGaussianSSM,
    observations: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    y = tf.convert_to_tensor(observations, dtype=DTYPE)
    mean = model.initial_mean
    covariance = model.initial_covariance
    log_terms = []
    for time_index in range(int(y.shape[0])):
        if time_index > 0:
            mean = model.transition_offset + tf.linalg.matvec(model.transition_matrix, mean)
            covariance = _symmetrize(
                model.transition_matrix @ covariance @ tf.transpose(model.transition_matrix)
                + model.transition_covariance
            )
        predictive_mean = model.observation_offset + tf.linalg.matvec(
            model.observation_matrix,
            mean,
        )
        innovation = y[time_index] - predictive_mean
        innovation_covariance = _symmetrize(
            model.observation_matrix @ covariance @ tf.transpose(model.observation_matrix)
            + model.observation_covariance
        )
        log_terms.append(_mvn_log_prob_zero_mean(innovation, innovation_covariance))
        gain_rhs = covariance @ tf.transpose(model.observation_matrix)
        chol = tf.linalg.cholesky(innovation_covariance)
        kalman_gain = tf.transpose(tf.linalg.cholesky_solve(chol, tf.transpose(gain_rhs)))
        mean = mean + tf.linalg.matvec(kalman_gain, innovation)
        left = tf.eye(model.state_dim(), dtype=DTYPE) - kalman_gain @ model.observation_matrix
        covariance = _symmetrize(
            left @ covariance @ tf.transpose(left)
            + kalman_gain @ model.observation_covariance @ tf.transpose(kalman_gain)
        )
    stacked_terms = tf.stack(log_terms)
    return tf.reduce_sum(stacked_terms), stacked_terms, mean, covariance


def test_p50_sequential_likelihood_matches_independent_kalman_reference() -> None:
    model = _lgssm()
    observations = _observations()
    result = highdim.FixedBranchSquaredTTFilter(_filter_config()).log_likelihood(
        model,
        tf.zeros([0], dtype=DTYPE),
        observations,
    )
    reference_log_likelihood, reference_terms, reference_mean, reference_covariance = (
        _independent_kalman(model, observations)
    )
    step_terms = tf.stack([step.log_normalizer for step in result.steps])

    assert len(result.steps) == int(observations.shape[0])
    tf.debugging.assert_near(result.log_likelihood, reference_log_likelihood, atol=2e-12)
    tf.debugging.assert_near(step_terms, reference_terms, atol=2e-12)
    tf.debugging.assert_near(result.log_likelihood, tf.reduce_sum(step_terms), atol=0.0)
    tf.debugging.assert_near(result.retained_filter.diagnostics["mean"], reference_mean, atol=2e-12)
    tf.debugging.assert_near(
        result.retained_filter.diagnostics["covariance"],
        reference_covariance,
        atol=2e-12,
    )
    assert result.log_likelihood.shape.rank == 0
    assert step_terms.dtype == DTYPE


def test_p50_sequential_likelihood_replays_branch_identities_for_tested_path() -> None:
    model = _lgssm()
    observations = _observations()
    runner = highdim.FixedBranchSquaredTTFilter(_filter_config(seed="p50-m3-replay"))

    first = runner.log_likelihood(model, tf.zeros([0], dtype=DTYPE), observations)
    second = runner.log_likelihood(model, tf.zeros([0], dtype=DTYPE), observations)

    tf.debugging.assert_equal(first.log_likelihood, second.log_likelihood)
    assert first.branch_identity.hash.value == second.branch_identity.hash.value
    assert (
        first.retained_filter.branch_identity.hash.value
        == second.retained_filter.branch_identity.hash.value
    )
    assert tuple(step.branch_identity.hash.value for step in first.steps) == tuple(
        step.branch_identity.hash.value for step in second.steps
    )
    assert first.branch_identity.manifest.payload["scope"] == "phase4_exact_small_model_value_path"
    assert "derivative_correctness" in first.branch_identity.manifest.payload["what_is_not_claimed"]
