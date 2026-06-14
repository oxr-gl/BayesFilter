from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


def _weighted_mean_covariance(
    samples: tf.Tensor,
    weights: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    mean = tf.reduce_sum(samples * weights[tf.newaxis, :], axis=1)
    centered = samples - mean[:, tf.newaxis]
    covariance = tf.einsum("n,in,jn->ij", weights, centered, centered)
    return mean, 0.5 * (covariance + tf.transpose(covariance))


def test_p49_source_route_recenter_matches_weighted_moments_and_det() -> None:
    samples = tf.constant(
        [
            [-2.0, 0.0, 1.0, 3.0],
            [1.0, -1.0, 0.5, 2.0],
        ],
        dtype=DTYPE,
    )
    log_weights = tf.math.log(tf.constant([0.1, 0.2, 0.3, 0.4], dtype=DTYPE))
    expansion = 1.5

    frame = highdim.source_route_recenter(
        samples=samples,
        log_weights=log_weights,
        expansion_factor=expansion,
        covariance_jitter=0.0,
        use_quantile_scale=False,
    )
    expected_mu, expected_covariance = _weighted_mean_covariance(
        samples,
        tf.exp(highdim.normalize_log_weights(log_weights)),
    )
    expected_matrix = tf.linalg.cholesky(expected_covariance) * tf.constant(
        expansion,
        dtype=DTYPE,
    )

    tf.debugging.assert_near(frame.mu, expected_mu)
    tf.debugging.assert_near(frame.matrix, expected_matrix)
    tf.debugging.assert_near(
        frame.log_abs_det(),
        tf.math.log(tf.abs(tf.linalg.det(expected_matrix))),
    )


def test_p54_source_route_recenter_uses_author_computeL_quantile_scale_when_ess_large() -> None:
    grid = tf.cast(tf.range(2001), dtype=DTYPE)
    values = (grid - 1000.0) / 100.0
    samples = tf.stack([values, 2.0 * values], axis=0)
    log_weights = tf.zeros([2001], dtype=DTYPE)

    no_quantile = highdim.source_route_recenter(
        samples=samples,
        log_weights=log_weights,
        expansion_factor=1.0,
        covariance_jitter=1e-5,
        use_quantile_scale=False,
    )
    with_quantile = highdim.source_route_recenter(
        samples=samples,
        log_weights=log_weights,
        expansion_factor=1.0,
        covariance_jitter=1e-5,
        use_quantile_scale=True,
        min_ess_for_quantile_scale=1000.0,
        quantile_fraction=0.01,
    )

    assert float(highdim.effective_sample_size_from_log_weights(log_weights).numpy()) > 1000.0
    assert not bool(
        tf.reduce_all(tf.abs(with_quantile.matrix - no_quantile.matrix) < 1e-10).numpy()
    )


def test_p49_source_route_recenter_fixed_rule_is_not_result_selected() -> None:
    samples = tf.constant(
        [[-1.0, 0.0, 1.0], [0.0, 2.0, 4.0]],
        dtype=DTYPE,
    )
    log_weights_left = tf.math.log(tf.constant([0.6, 0.3, 0.1], dtype=DTYPE))
    log_weights_right = tf.math.log(tf.constant([0.1, 0.3, 0.6], dtype=DTYPE))

    frame_left = highdim.source_route_recenter(
        samples=samples,
        log_weights=log_weights_left,
        expansion_factor=1.0,
        covariance_jitter=1e-9,
    )
    frame_right = highdim.source_route_recenter(
        samples=samples,
        log_weights=log_weights_right,
        expansion_factor=1.0,
        covariance_jitter=1e-9,
    )

    assert float(frame_left.mu[0].numpy()) < float(frame_right.mu[0].numpy())
    assert float(frame_left.mu[1].numpy()) < float(frame_right.mu[1].numpy())


def test_p49_source_route_reference_log_density_adds_affine_jacobian() -> None:
    frame = highdim.SourceRouteCoordinateFrame(
        mu=tf.constant([1.0, -1.0], dtype=DTYPE),
        matrix=tf.constant([[2.0, 0.0], [0.3, 1.5]], dtype=DTYPE),
        expansion_factor=1.0,
    )
    log_physical = tf.constant([-3.0, -2.0, -1.0], dtype=DTYPE)

    reference = highdim.source_route_reference_log_density_from_physical(
        log_physical_density=log_physical,
        coordinate_frame=frame,
    )

    tf.debugging.assert_near(reference, log_physical + frame.log_abs_det())


def test_p49_source_route_shifted_target_preserves_final_normalizer() -> None:
    negative_log_target = tf.constant([2.0, 0.5, 1.25, 3.0], dtype=DTYPE)
    original_log_z = tf.reduce_logsumexp(-negative_log_target)

    for shift in (0.0, 1.7, -0.4):
        shift_constant = tf.constant(shift, dtype=DTYPE)
        shifted = highdim.source_route_shifted_negative_log_target(
            negative_log_target=negative_log_target,
            shift_constant=shift_constant,
        )
        shifted_log_z = tf.reduce_logsumexp(-shifted)

        tf.debugging.assert_near(
            highdim.source_route_log_normalizer_update(
                log_transport_normalizer=shifted_log_z,
                shift_constant=shift_constant,
            ),
            original_log_z,
        )


def test_p49_source_route_normalizer_contribution_records_shift_and_policy() -> None:
    contribution = highdim.SourceRouteNormalizerContribution(
        log_transport_normalizer=tf.constant(4.25, dtype=DTYPE),
        shift_constant=tf.constant(0.75, dtype=DTYPE),
        log_abs_det_policy="included_in_target",
    )

    tf.debugging.assert_near(
        contribution.log_increment(),
        tf.constant(3.5, dtype=DTYPE),
    )
    payload = contribution.manifest_payload()
    assert payload["log_abs_det_policy"] == "included_in_target"


def test_p49_source_route_recenter_and_shift_reject_bad_inputs() -> None:
    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_SHAPE.value):
        highdim.source_route_recenter(
            samples=tf.zeros([2, 2], dtype=DTYPE),
            log_weights=tf.zeros([3], dtype=DTYPE),
            expansion_factor=1.0,
        )

    with pytest.raises(ValueError, match="expansion_factor"):
        highdim.source_route_recenter(
            samples=tf.zeros([2, 3], dtype=DTYPE),
            log_weights=tf.zeros([3], dtype=DTYPE),
            expansion_factor=0.0,
        )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_SHAPE.value):
        highdim.source_route_reference_log_density_from_physical(
            log_physical_density=tf.zeros([2, 1], dtype=DTYPE),
            coordinate_frame=highdim.SourceRouteCoordinateFrame(
                mu=tf.zeros([1], dtype=DTYPE),
                matrix=tf.eye(1, dtype=DTYPE),
                expansion_factor=1.0,
            ),
        )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_SHAPE.value):
        highdim.source_route_shifted_negative_log_target(
            negative_log_target=tf.zeros([2], dtype=DTYPE),
            shift_constant=tf.zeros([1], dtype=DTYPE),
        )
