from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


def test_p49_source_route_sample_batch_records_ess_and_normalized_weights() -> None:
    log_weights = tf.math.log(tf.constant([0.2, 0.3, 0.5], dtype=DTYPE))
    batch = highdim.SourceRouteSampleBatch(
        samples=tf.constant([[0.0, 1.0, 2.0]], dtype=DTYPE),
        log_weights=log_weights,
        time_index=0,
        route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
        sample_origin="prior",
    )

    tf.debugging.assert_near(
        tf.exp(batch.normalized_log_weights()),
        tf.constant([0.2, 0.3, 0.5], dtype=DTYPE),
    )
    tf.debugging.assert_near(
        batch.effective_sample_size(),
        1.0 / tf.reduce_sum(tf.square(tf.constant([0.2, 0.3, 0.5], dtype=DTYPE))),
    )
    diagnostics = batch.diagnostics(enhancement_attempts=2)
    assert diagnostics.sample_count == 3
    assert diagnostics.enhancement_attempts == 2


def test_p49_source_route_push_sample_batch_advances_time_without_grid_fallback() -> None:
    previous = highdim.SourceRouteSampleBatch(
        samples=tf.constant([[0.0, 1.0, 2.0]], dtype=DTYPE),
        log_weights=tf.zeros([3], dtype=DTYPE),
        time_index=1,
        route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
        sample_origin="retained",
    )

    propagated = highdim.source_route_push_sample_batch(
        previous_batch=previous,
        propagated_samples=tf.constant([[0.1, 1.1, 2.1], [0.0, 1.0, 2.0]], dtype=DTYPE),
        log_weights=tf.math.log(tf.constant([0.25, 0.25, 0.5], dtype=DTYPE)),
        time_index=2,
    )

    assert propagated.route_label == highdim.SOURCE_FAITHFUL_ROUTE_LABEL
    assert propagated.sample_origin == "propagated"
    assert propagated.time_index == 2
    assert propagated.samples.shape == (2, 3)
    assert propagated.sample_count == previous.sample_count

    with pytest.raises(ValueError, match="sample count"):
        highdim.source_route_push_sample_batch(
            previous_batch=previous,
            propagated_samples=tf.ones([2, 4], dtype=DTYPE),
            log_weights=tf.zeros([4], dtype=DTYPE),
            time_index=2,
        )


def test_p54_source_route_push_and_augment_matches_author_shape_and_weights() -> None:
    previous = highdim.SourceRouteSampleBatch(
        samples=tf.constant(
            [
                [0.4, 0.6, 0.8],
                [1.0, 2.0, 3.0],
            ],
            dtype=DTYPE,
        ),
        log_weights=tf.math.log(tf.constant([0.2, 0.3, 0.5], dtype=DTYPE)),
        time_index=0,
        route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
        sample_origin="prior",
    )

    def transition_fn(samples: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        theta = samples[:1, :]
        state = samples[1:, :]
        return state + theta

    def log_likelihood_fn(samples: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        next_state = samples[1, :]
        return -0.5 * tf.square(next_state - 2.5)

    result = highdim.source_route_push_and_augment_samples(
        previous_batch=previous,
        transition_fn=transition_fn,
        log_likelihood_fn=log_likelihood_fn,
        parameter_dim=1,
        state_dim=1,
        time_index=1,
    )

    expected_next = previous.samples[1:, :] + previous.samples[:1, :]
    expected_log_weights = highdim.normalize_log_weights(
        previous.log_weights + log_likelihood_fn(
            tf.concat([previous.samples[:1, :], expected_next], axis=0),
            1,
        )
    )

    tf.debugging.assert_near(result.propagated_batch.samples[1:, :], expected_next)
    tf.debugging.assert_near(result.propagated_batch.log_weights, expected_log_weights)
    tf.debugging.assert_near(result.augmented_batch.log_weights, expected_log_weights)
    tf.debugging.assert_near(
        result.augmented_batch.samples,
        tf.concat([previous.samples[:1, :], expected_next, previous.samples[1:, :]], axis=0),
    )
    assert result.augmented_batch.samples.shape == (3, 3)
    assert result.augmented_batch.sample_origin == "augmented_propagated"
    assert result.diagnostics.sample_count == previous.sample_count


def test_p54_source_route_push_and_augment_rejects_non_source_route() -> None:
    previous = highdim.SourceRouteSampleBatch(
        samples=tf.zeros([1, 2], dtype=DTYPE),
        log_weights=tf.zeros([2], dtype=DTYPE),
        time_index=0,
        route_label=highdim.GRADIENT_ADAPTATION_ROUTE_LABEL,
        sample_origin="prior",
    )

    with pytest.raises(ValueError, match="source_faithful_filtering"):
        highdim.source_route_push_and_augment_samples(
            previous_batch=previous,
            transition_fn=lambda samples, t: samples,
            log_likelihood_fn=lambda samples, t: tf.zeros([2], dtype=DTYPE),
            parameter_dim=0,
            state_dim=1,
            time_index=1,
        )


def test_p49_source_route_ess_gate_uses_sample_count_fraction() -> None:
    assert highdim.source_route_needs_enhancement(
        effective_sample_size=tf.constant(1.9, dtype=DTYPE),
        sample_count=4,
        min_ess_fraction=0.5,
    )
    assert not highdim.source_route_needs_enhancement(
        effective_sample_size=tf.constant(2.0, dtype=DTYPE),
        sample_count=4,
        min_ess_fraction=0.5,
    )

    with pytest.raises(ValueError, match="min_ess_fraction"):
        highdim.source_route_needs_enhancement(
            effective_sample_size=tf.constant(2.0, dtype=DTYPE),
            sample_count=4,
            min_ess_fraction=0.0,
        )


def test_p49_source_route_proposal_correction_matches_exact_discrete_reference() -> None:
    proposal_mass = tf.constant([0.10, 0.20, 0.30, 0.40], dtype=DTYPE)
    unnormalized_target = tf.constant([0.03, 0.18, 0.24, 0.56], dtype=DTYPE)
    expected_log_z = tf.math.log(tf.reduce_sum(unnormalized_target))

    log_proposal = tf.math.log(proposal_mass)
    log_target = tf.math.log(unnormalized_target)
    correction = highdim.source_route_proposal_log_weights(
        log_target_density=log_target,
        log_proposal_density=log_proposal,
    )

    tf.debugging.assert_near(correction, log_target - log_proposal)
    tf.debugging.assert_near(
        highdim.source_route_discrete_log_normalizer_from_correction(
            log_proposal_density=log_proposal,
            correction_log_weights=correction,
        ),
        expected_log_z,
    )
    tf.debugging.assert_near(
        highdim.effective_sample_size_from_log_weights(correction),
        1.0
        / tf.reduce_sum(
            tf.square(
                unnormalized_target / proposal_mass
                / tf.reduce_sum(unnormalized_target / proposal_mass)
            )
        ),
    )


def test_p49_source_route_negative_log_target_conversion_is_explicit() -> None:
    log_target = tf.constant([-1.0, -0.25, -2.0], dtype=DTYPE)
    log_proposal = tf.constant([-0.75, -0.75, -0.75], dtype=DTYPE)

    from_log_density = highdim.source_route_proposal_log_weights(
        log_target_density=log_target,
        log_proposal_density=log_proposal,
    )
    from_negative_log = highdim.source_route_proposal_log_weights_from_negative_log_target(
        negative_log_target=-log_target,
        log_proposal_density=log_proposal,
    )

    tf.debugging.assert_near(from_negative_log, from_log_density)


def test_p49_source_route_equal_weight_log_normalizer_estimate() -> None:
    correction = tf.math.log(tf.constant([0.5, 1.0, 1.5, 2.0], dtype=DTYPE))

    tf.debugging.assert_near(
        highdim.source_route_equal_weight_log_normalizer_estimate(correction),
        tf.math.log(tf.reduce_mean(tf.exp(correction))),
    )


def test_p49_source_route_proposal_correction_rejects_bad_shapes_and_nonfinite() -> None:
    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_SHAPE.value):
        highdim.source_route_proposal_log_weights(
            log_target_density=tf.zeros([2, 1], dtype=DTYPE),
            log_proposal_density=tf.zeros([2, 1], dtype=DTYPE),
        )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_SHAPE.value):
        highdim.source_route_proposal_log_weights(
            log_target_density=tf.zeros([2], dtype=DTYPE),
            log_proposal_density=tf.zeros([3], dtype=DTYPE),
        )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.NONFINITE_VALUE.value):
        highdim.source_route_proposal_log_weights(
            log_target_density=tf.constant([0.0, float("nan")], dtype=DTYPE),
            log_proposal_density=tf.zeros([2], dtype=DTYPE),
        )
