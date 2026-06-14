from __future__ import annotations

import math

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


class IdentityGaussianTransport:
    def __init__(self, dimension: int, log_normalizer: float = 0.0) -> None:
        self.dimension = int(dimension)
        self._log_normalizer = tf.constant(log_normalizer, dtype=DTYPE)

    def manifest_payload(self) -> dict[str, object]:
        return {
            "family": "IdentityGaussianTransport",
            "dimension": self.dimension,
            "source": "p55 analytic reference transport",
            "source_contract_level": "contract_test_double",
        }

    def inverse_transport(self, reference_points: tf.Tensor) -> tf.Tensor:
        return tf.convert_to_tensor(reference_points, dtype=DTYPE)

    def forward_transport(self, local_points: tf.Tensor) -> tf.Tensor:
        return tf.convert_to_tensor(local_points, dtype=DTYPE)

    def conditional_inverse_transport(
        self,
        conditioning_points: tf.Tensor,
        reference_points: tf.Tensor,
    ) -> tf.Tensor:
        del conditioning_points
        return tf.convert_to_tensor(reference_points, dtype=DTYPE)

    def log_reference_density(self, reference_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(reference_points, dtype=DTYPE)
        normalizer = -0.5 * tf.cast(self.dimension, DTYPE) * tf.math.log(
            tf.constant(2.0 * math.pi, dtype=DTYPE)
        )
        return normalizer - 0.5 * tf.reduce_sum(tf.square(points), axis=0)

    def eval_pdf(self, local_points: tf.Tensor) -> tf.Tensor:
        return tf.exp(self.log_reference_density(local_points))

    def potential(self, local_points: tf.Tensor) -> tf.Tensor:
        return -self.log_reference_density(local_points)

    def proposal_log_density(
        self,
        *,
        local_points: tf.Tensor,
        reference_points: tf.Tensor,
    ) -> tf.Tensor:
        del reference_points
        return tf.math.log(self.eval_pdf(local_points))

    def marginalize(self, keep_axes: tuple[int, ...]) -> "IdentityGaussianTransport":
        return IdentityGaussianTransport(len(tuple(keep_axes)), float(self._log_normalizer.numpy()))

    def log_normalizer(self) -> tf.Tensor:
        return self._log_normalizer


class BaseDensityOnlyTransport:
    def manifest_payload(self) -> dict[str, object]:
        return {
            "family": "BaseDensityOnlyTransport",
            "source_contract_level": "contract_test_double",
        }

    def inverse_transport(self, reference_points: tf.Tensor) -> tf.Tensor:
        return tf.convert_to_tensor(reference_points, dtype=DTYPE)

    def log_normalizer(self) -> tf.Tensor:
        return tf.constant(0.0, dtype=DTYPE)


def _identity_frame(dimension: int = 2) -> highdim.SourceRouteCoordinateFrame:
    return highdim.SourceRouteCoordinateFrame(
        mu=tf.zeros([dimension], dtype=DTYPE),
        matrix=tf.eye(dimension, dtype=DTYPE),
        expansion_factor=1.0,
    )


def test_p55_source_route_target_applies_shift_and_affine_determinant() -> None:
    frame = highdim.SourceRouteCoordinateFrame(
        mu=tf.constant([1.0, -0.5], dtype=DTYPE),
        matrix=tf.constant([[2.0, 0.0], [0.25, 1.5]], dtype=DTYPE),
        expansion_factor=1.0,
    )

    def negative_log_physical(points: tf.Tensor) -> tf.Tensor:
        return 0.5 * tf.reduce_sum(tf.square(points), axis=0)

    target = highdim.build_source_route_target(
        negative_log_physical_density_fn=negative_log_physical,
        coordinate_frame=frame,
        shift_constant=tf.constant(0.75, dtype=DTYPE),
        time_index=1,
    )
    reference = tf.constant([[0.0, 0.5], [1.0, -1.0]], dtype=DTYPE)
    physical = frame.matrix @ reference + frame.mu[:, tf.newaxis]
    expected = (
        negative_log_physical(physical)
        - frame.log_abs_det()
        - tf.constant(0.75, dtype=DTYPE)
    )

    tf.debugging.assert_near(target.negative_log_density(reference), expected)
    assert target.source_terms == ("prior_or_previous", "transition", "likelihood")
    assert target.log_abs_det_policy == "included_in_target"


def test_p55_transport_protocol_requires_source_transport_methods() -> None:
    transport = highdim.SourceRouteTransportProtocol(
        IdentityGaussianTransport(dimension=2, log_normalizer=1.25)
    )

    payload = transport.manifest_payload()
    assert payload["family"] == "SourceRouteTransportProtocol"
    assert payload["proposal_density_semantics"] == "transport_eval_pdf_equivalent_on_local_samples"
    assert "eval_pdf" in payload["required_source_methods"]
    tf.debugging.assert_near(transport.log_normalizer(), tf.constant(1.25, dtype=DTYPE))

    with pytest.raises(TypeError, match="missing required methods"):
        highdim.SourceRouteTransportProtocol(object())

    class MissingContractLevel(IdentityGaussianTransport):
        def manifest_payload(self) -> dict[str, object]:
            payload = dict(super().manifest_payload())
            payload.pop("source_contract_level")
            return payload

    with pytest.raises(ValueError, match="source_contract_level"):
        highdim.SourceRouteTransportProtocol(MissingContractLevel(dimension=2))

    with pytest.raises(TypeError, match="missing required methods"):
        highdim.SourceRouteTransportProtocol(BaseDensityOnlyTransport())

    with pytest.raises(ValueError, match="source_faithful_filtering"):
        highdim.SourceRouteTransportProtocol(
            IdentityGaussianTransport(dimension=2),
            route_label=highdim.GRADIENT_ADAPTATION_ROUTE_LABEL,
        )


def test_p55_recenter_prunes_nonfinite_columns_like_computeL() -> None:
    clean_samples = tf.constant([[0.0, 2.0], [1.0, 3.0]], dtype=DTYPE)
    samples = tf.constant(
        [
            [0.0, float("nan"), 2.0, 5.0],
            [1.0, 4.0, 3.0, float("inf")],
        ],
        dtype=DTYPE,
    )
    log_weights = tf.math.log(tf.constant([0.25, 0.25, 0.75, 0.25], dtype=DTYPE))
    clean_log_weights = tf.math.log(tf.constant([0.25, 0.75], dtype=DTYPE))

    pruned = highdim.source_route_recenter(
        samples=samples,
        log_weights=log_weights,
        expansion_factor=1.0,
        covariance_jitter=1e-8,
        use_quantile_scale=False,
    )
    expected = highdim.source_route_recenter(
        samples=clean_samples,
        log_weights=clean_log_weights,
        expansion_factor=1.0,
        covariance_jitter=1e-8,
        use_quantile_scale=False,
    )

    tf.debugging.assert_near(pruned.mu, expected.mu)
    tf.debugging.assert_near(pruned.matrix, expected.matrix)


def test_p55_recenter_rejects_all_invalid_or_nonfinite_weight_columns() -> None:
    with pytest.raises(ValueError, match=highdim.HighDimStatus.NONFINITE_VALUE.value):
        highdim.source_route_recenter(
            samples=tf.constant([[float("nan"), float("inf")]], dtype=DTYPE),
            log_weights=tf.zeros([2], dtype=DTYPE),
            expansion_factor=1.0,
        )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.NONFINITE_VALUE.value):
        highdim.source_route_recenter(
            samples=tf.constant([[0.0, 1.0]], dtype=DTYPE),
            log_weights=tf.constant([float("nan"), float("inf")], dtype=DTYPE),
            expansion_factor=1.0,
        )


def test_p55_target_rejects_missing_source_terms() -> None:
    with pytest.raises(ValueError, match="source_terms missing transition"):
        highdim.build_source_route_target(
            negative_log_physical_density_fn=lambda points: tf.zeros(
                [tf.shape(points)[1]],
                dtype=DTYPE,
            ),
            coordinate_frame=_identity_frame(),
            shift_constant=tf.constant(0.0, dtype=DTYPE),
            time_index=1,
            source_terms=("prior_or_previous", "likelihood"),
        )
