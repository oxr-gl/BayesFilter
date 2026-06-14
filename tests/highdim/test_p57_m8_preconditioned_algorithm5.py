from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


class DiagonalGaussianTransport:
    def __init__(self, scale: tuple[float, ...], log_normalizer: float = 0.0) -> None:
        self.scale = tf.constant(scale, dtype=DTYPE)
        self._log_normalizer = tf.constant(log_normalizer, dtype=DTYPE)

    def manifest_payload(self) -> dict[str, object]:
        return {
            "family": "DiagonalGaussianTransport",
            "source_contract_level": "contract_test_double",
            "scale": self.scale,
        }

    def inverse_transport(self, reference_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(reference_points, dtype=DTYPE)
        return self.scale[:, tf.newaxis] * points

    def forward_transport(self, local_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(local_points, dtype=DTYPE)
        return points / self.scale[:, tf.newaxis]

    def conditional_inverse_transport(
        self,
        conditioning_points: tf.Tensor,
        reference_points: tf.Tensor,
    ) -> tf.Tensor:
        del conditioning_points
        return self.inverse_transport(reference_points)

    def eval_pdf(self, local_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(local_points, dtype=DTYPE)
        return tf.exp(-0.5 * tf.reduce_sum(tf.square(points), axis=0))

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

    def marginalize(self, keep_axes: tuple[int, ...]) -> "DiagonalGaussianTransport":
        keep = tuple(int(axis) for axis in keep_axes)
        return DiagonalGaussianTransport(
            tuple(float(self.scale[axis].numpy()) for axis in keep),
            float(self._log_normalizer.numpy()),
        )

    def log_normalizer(self) -> tf.Tensor:
        return self._log_normalizer


def _standard_logr(points: tf.Tensor) -> tf.Tensor:
    values = tf.convert_to_tensor(points, dtype=DTYPE)
    return -0.5 * tf.reduce_sum(tf.square(values), axis=0)


def _preconditioned_map() -> highdim.SourceRoutePreconditionedMap:
    frame = highdim.SourceRouteCoordinateFrame(
        mu=tf.constant([0.5, -1.0], dtype=DTYPE),
        matrix=tf.constant([[1.5, 0.2], [-0.1, 1.25]], dtype=DTYPE),
        expansion_factor=1.0,
    )
    return highdim.SourceRoutePreconditionedMap(
        preconditioner_transport=highdim.SourceRouteTransportProtocol(
            DiagonalGaussianTransport((1.2, 0.75), log_normalizer=0.4)
        ),
        preconditioner_frame=frame,
        reference_forward_fn=lambda u: tf.convert_to_tensor(u, dtype=DTYPE),
        reference_inverse_fn=lambda z: tf.convert_to_tensor(z, dtype=DTYPE),
        reference_log_density_fn=_standard_logr,
    )


def test_p57_m8_linear_preconditioner_matches_author_precond_invariants() -> None:
    sigma1 = tf.constant(
        [
            [4.0, 0.2, 0.1],
            [0.2, 2.0, 0.3],
            [0.1, 0.3, 1.5],
        ],
        dtype=DTYPE,
    )
    sigma2 = tf.constant(
        [
            [0.9, 0.15],
            [0.15, 0.7],
        ],
        dtype=DTYPE,
    )

    result = highdim.source_route_linear_preconditioner_from_covariances(
        sigma1=sigma1,
        sigma2=sigma2,
    )
    c_matrix = result.matrix
    sigma_k = result.sigma_k
    d = result.parameter_dim
    m = result.state_dim

    tf.debugging.assert_near(
        c_matrix[:d, :d] @ sigma1[:d, :d] @ tf.transpose(c_matrix[:d, :d]),
        tf.eye(d, dtype=DTYPE),
    )
    tf.debugging.assert_near(
        tf.linalg.diag_part(c_matrix @ sigma1 @ tf.transpose(c_matrix)),
        tf.ones([d + m], dtype=DTYPE),
    )
    tf.debugging.assert_near(sigma_k[:d, :], tf.zeros([d, d + m], dtype=DTYPE))
    tf.debugging.assert_near(sigma_k[:, :d], tf.zeros([d + m, d], dtype=DTYPE))
    tf.debugging.assert_near(
        sigma_k[d:, d:],
        tf.linalg.diag(
            tf.linalg.diag_part(c_matrix[d:, d:] @ sigma2 @ tf.transpose(c_matrix[d:, d:]))
        ),
    )
    assert m == 2
    assert "precond.m:43-56" in result.manifest_payload()["source_anchor"]


def test_p57_m8_tu2x_tx2u_roundtrip_matches_source_map_contract() -> None:
    pre_map = _preconditioned_map()
    residual = tf.constant([[0.1, -0.4, 0.7], [0.3, 0.2, -0.6]], dtype=DTYPE)

    physical = pre_map.Tu2x(residual)
    roundtrip = pre_map.Tx2u(physical)

    tf.debugging.assert_near(roundtrip, residual)
    tf.debugging.assert_near(
        pre_map.map_roundtrip_error(residual),
        tf.constant(0.0, dtype=DTYPE),
        atol=1e-12,
    )
    assert pre_map.manifest_payload()["forward_map_label"] == "Tu2x"
    assert "pre_sol.m:212-213" in pre_map.manifest_payload()["source_anchor"]


def test_p57_m8_proposal_correction_matches_author_pre_sol_density_identity() -> None:
    pre_map = _preconditioned_map()
    residual_transport = highdim.SourceRouteTransportProtocol(
        DiagonalGaussianTransport((0.5, 1.4), log_normalizer=0.1)
    )
    reference = tf.constant([[0.2, 0.6, -0.5], [0.4, -0.3, 0.8]], dtype=DTYPE)

    def full_negative_log_density(points: tf.Tensor) -> tf.Tensor:
        centered = tf.convert_to_tensor(points, dtype=DTYPE) - tf.constant(
            [[0.25], [-0.75]],
            dtype=DTYPE,
        )
        return 0.7 + 0.5 * tf.reduce_sum(tf.square(centered), axis=0)

    result = highdim.source_route_preconditioned_proposal_correction(
        preconditioned_map=pre_map,
        residual_transport=residual_transport,
        reference_samples=reference,
        full_negative_log_density_fn=full_negative_log_density,
    )

    residual_local = residual_transport.inverse_transport(reference)
    physical = pre_map.Tu2x(residual_local)
    expected_residual_log = residual_transport.proposal_log_density(
        local_points=residual_local,
        reference_points=reference,
    )
    expected_pre_log = pre_map.preconditioner_log_density(physical)
    expected_ref_log = _standard_logr(residual_local)
    expected_proposal = expected_residual_log + expected_pre_log - expected_ref_log
    expected_target = -full_negative_log_density(physical)

    tf.debugging.assert_near(result.residual_local_samples, residual_local)
    tf.debugging.assert_near(result.physical_samples, physical)
    tf.debugging.assert_near(result.residual_log_density, expected_residual_log)
    tf.debugging.assert_near(result.preconditioner_log_density, expected_pre_log)
    tf.debugging.assert_near(result.reference_log_density, expected_ref_log)
    tf.debugging.assert_near(result.proposal_log_density, expected_proposal)
    tf.debugging.assert_near(result.target_log_density, expected_target)
    tf.debugging.assert_near(
        result.correction_log_weights,
        expected_target - expected_proposal,
    )
    assert "pre_sol.m:245-255" in result.manifest_payload()["source_anchor"]


def test_p57_m8_rejects_bad_preconditioned_shapes_and_non_source_transports() -> None:
    pre_map = _preconditioned_map()
    residual_transport = highdim.SourceRouteTransportProtocol(
        DiagonalGaussianTransport((1.0, 1.0))
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_SHAPE.value):
        pre_map.Tu2x(tf.ones([3, 2], dtype=DTYPE))

    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_SHAPE.value):
        highdim.source_route_linear_preconditioner_from_covariances(
            sigma1=tf.eye(2, dtype=DTYPE),
            sigma2=tf.ones([2], dtype=DTYPE),
        )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_SHAPE.value):
        highdim.source_route_preconditioned_proposal_correction(
            preconditioned_map=pre_map,
            residual_transport=residual_transport,
            reference_samples=tf.ones([1, 2], dtype=DTYPE),
            full_negative_log_density_fn=lambda x: tf.zeros([2], dtype=DTYPE),
        )

    with pytest.raises(ValueError, match="source_faithful_filtering"):
        highdim.SourceRouteTransportProtocol(
            DiagonalGaussianTransport((1.0, 1.0)),
            route_label=highdim.GRADIENT_ADAPTATION_ROUTE_LABEL,
        )
