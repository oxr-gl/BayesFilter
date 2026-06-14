from __future__ import annotations

import math

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


class ShiftedGaussianTransport:
    def __init__(self, shift: tf.Tensor, log_normalizer: float = 0.4) -> None:
        self.shift = tf.convert_to_tensor(shift, dtype=DTYPE)
        self._log_normalizer = tf.constant(log_normalizer, dtype=DTYPE)

    def manifest_payload(self) -> dict[str, object]:
        return {
            "family": "ShiftedGaussianTransport",
            "dimension": int(self.shift.shape[0]),
            "source": "p55 analytic reference transport",
            "source_contract_level": "contract_test_double",
        }

    def inverse_transport(self, reference_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(reference_points, dtype=DTYPE)
        return points + self.shift[:, tf.newaxis]

    def forward_transport(self, local_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(local_points, dtype=DTYPE)
        return points - self.shift[:, tf.newaxis]

    def conditional_inverse_transport(
        self,
        conditioning_points: tf.Tensor,
        reference_points: tf.Tensor,
    ) -> tf.Tensor:
        del conditioning_points
        return self.inverse_transport(reference_points)

    def log_reference_density(self, reference_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(reference_points, dtype=DTYPE)
        dimension = tf.cast(tf.shape(points)[0], dtype=DTYPE)
        normalizer = -0.5 * dimension * tf.math.log(tf.constant(2.0 * math.pi, dtype=DTYPE))
        return normalizer - 0.5 * tf.reduce_sum(tf.square(points), axis=0)

    def eval_pdf(self, local_points: tf.Tensor) -> tf.Tensor:
        reference = self.forward_transport(local_points)
        return tf.exp(self.log_reference_density(reference))

    def potential(self, local_points: tf.Tensor) -> tf.Tensor:
        return -tf.math.log(self.eval_pdf(local_points))

    def proposal_log_density(
        self,
        *,
        local_points: tf.Tensor,
        reference_points: tf.Tensor,
    ) -> tf.Tensor:
        del reference_points
        return tf.math.log(self.eval_pdf(local_points))

    def marginalize(self, keep_axes: tuple[int, ...]) -> "ShiftedGaussianTransport":
        keep = tuple(int(axis) for axis in keep_axes)
        return ShiftedGaussianTransport(tf.gather(self.shift, keep), float(self._log_normalizer.numpy()))

    def log_normalizer(self) -> tf.Tensor:
        return self._log_normalizer


def _target(time_index: int = 1) -> highdim.SourceRouteTarget:
    frame = highdim.SourceRouteCoordinateFrame(
        mu=tf.constant([1.0, -1.0], dtype=DTYPE),
        matrix=tf.constant([[1.5, 0.0], [0.2, 1.1]], dtype=DTYPE),
        expansion_factor=1.0,
    )

    def negative_log_physical(points: tf.Tensor) -> tf.Tensor:
        return 0.5 * tf.reduce_sum(tf.square(points), axis=0) + tf.constant(0.25, dtype=DTYPE)

    return highdim.build_source_route_target(
        negative_log_physical_density_fn=negative_log_physical,
        coordinate_frame=frame,
        shift_constant=tf.constant(0.3, dtype=DTYPE),
        time_index=time_index,
    )


def test_p55_generate_retained_samples_applies_transport_correction_and_normalizer() -> None:
    target = _target()
    transport = highdim.SourceRouteTransportProtocol(
        ShiftedGaussianTransport(tf.constant([0.25, -0.5], dtype=DTYPE))
    )
    reference = tf.constant(
        [
            [-0.5, 0.0, 1.0],
            [0.25, -0.25, 0.75],
        ],
        dtype=DTYPE,
    )

    result = highdim.source_route_generate_retained_samples(
        target=target,
        transport=transport,
        reference_samples=reference,
        time_index=1,
    )

    local = transport.inverse_transport(reference)
    physical = target.physical_points_from_reference(local)
    expected_proposal = transport.proposal_log_density(local_points=local, reference_points=reference)
    expected_target = target.log_target_density(local)

    tf.debugging.assert_near(result.retained_batch.samples, physical)
    tf.debugging.assert_near(result.proposal_log_density, expected_proposal)
    tf.debugging.assert_near(result.target_log_density, expected_target)
    tf.debugging.assert_near(result.correction_log_weights, expected_target - expected_proposal)
    tf.debugging.assert_near(
        result.retained_batch.log_weights,
        highdim.normalize_log_weights(expected_target - expected_proposal),
    )
    tf.debugging.assert_near(
        result.normalizer.log_increment(),
        tf.constant(0.4, dtype=DTYPE) - target.shift_constant,
    )
    assert result.retained_batch.sample_origin == "retained_from_transport"
    assert result.diagnostics.sample_count == 3


def test_p55_one_step_reapproximation_is_t1_only_and_records_protocol() -> None:
    target = _target(time_index=1)
    transport = highdim.SourceRouteTransportProtocol(
        ShiftedGaussianTransport(tf.constant([0.0, 0.0], dtype=DTYPE))
    )
    reference = tf.zeros([2, 4], dtype=DTYPE)

    result = highdim.source_route_one_step_reapproximation(
        target=target,
        transport=transport,
        reference_samples=reference,
        time_index=1,
    )

    payload = result.manifest_payload()
    assert payload["sequential_status"] == "one_step_t1_only"
    assert result.retained_samples.retained_batch.sample_count == 4

    with pytest.raises(ValueError, match="t=1"):
        highdim.source_route_one_step_reapproximation(
            target=_target(time_index=2),
            transport=transport,
            reference_samples=reference,
            time_index=2,
        )

    with pytest.raises(ValueError, match="previous retained-object marginalization"):
        highdim.source_route_one_step_reapproximation(
            target=target,
            transport=transport,
            reference_samples=reference,
            time_index=1,
            previous_retained_object=object(),
        )


def test_p55_retained_sampling_requires_transport_protocol() -> None:
    with pytest.raises(TypeError, match="transport must be SourceRouteTransportProtocol"):
        highdim.source_route_generate_retained_samples(
            target=_target(),
            transport=object(),
            reference_samples=tf.zeros([2, 2], dtype=DTYPE),
            time_index=1,
        )
