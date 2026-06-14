from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


class BaseOnlyTransport:
    def manifest_payload(self) -> dict[str, object]:
        return {
            "family": "BaseOnlyTransport",
            "source_contract_level": "contract_test_double",
        }

    def inverse_transport(self, reference_points: tf.Tensor) -> tf.Tensor:
        return tf.convert_to_tensor(reference_points, dtype=DTYPE)

    def log_reference_density(self, reference_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(reference_points, dtype=DTYPE)
        return -0.5 * tf.reduce_sum(tf.square(points), axis=0)

    def log_normalizer(self) -> tf.Tensor:
        return tf.constant(0.0, dtype=DTYPE)


class SourceSurfaceTransport:
    def __init__(self, scale: float = 2.0) -> None:
        self.scale = tf.constant(scale, dtype=DTYPE)

    def manifest_payload(self) -> dict[str, object]:
        return {
            "family": "SourceSurfaceTransport",
            "scale": float(self.scale.numpy()),
            "source_contract_level": "contract_test_double",
        }

    def inverse_transport(self, reference_points: tf.Tensor) -> tf.Tensor:
        return self.scale * tf.convert_to_tensor(reference_points, dtype=DTYPE)

    def forward_transport(self, local_points: tf.Tensor) -> tf.Tensor:
        return tf.convert_to_tensor(local_points, dtype=DTYPE) / self.scale

    def conditional_inverse_transport(
        self,
        conditioning_points: tf.Tensor,
        reference_points: tf.Tensor,
    ) -> tf.Tensor:
        del conditioning_points
        return self.inverse_transport(reference_points)

    def eval_pdf(self, local_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(local_points, dtype=DTYPE)
        return tf.exp(-tf.reduce_sum(tf.square(points), axis=0))

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

    def marginalize(self, keep_axes: tuple[int, ...]) -> "SourceSurfaceTransport":
        del keep_axes
        return SourceSurfaceTransport(float(self.scale.numpy()))

    def log_normalizer(self) -> tf.Tensor:
        return tf.constant(0.7, dtype=DTYPE)


def _target() -> highdim.SourceRouteTarget:
    frame = highdim.SourceRouteCoordinateFrame(
        mu=tf.zeros([2], dtype=DTYPE),
        matrix=tf.eye(2, dtype=DTYPE),
        expansion_factor=1.0,
    )

    def negative_log(points: tf.Tensor) -> tf.Tensor:
        return 0.25 * tf.reduce_sum(tf.square(points), axis=0)

    return highdim.build_source_route_target(
        negative_log_physical_density_fn=negative_log,
        coordinate_frame=frame,
        shift_constant=tf.constant(0.1, dtype=DTYPE),
        time_index=1,
    )


def test_p57_m2_rejects_base_density_only_transport_contract() -> None:
    with pytest.raises(TypeError, match="missing required methods"):
        highdim.SourceRouteTransportProtocol(BaseOnlyTransport())


def test_p57_m2_fixed_ttsirt_level_requires_tt_and_defensive_metadata() -> None:
    class MissingTTMetadataTransport(SourceSurfaceTransport):
        def manifest_payload(self) -> dict[str, object]:
            payload = dict(super().manifest_payload())
            payload["source_contract_level"] = "fixed_ttsirt"
            return payload

    class DeclaredFixedTTSIRTTransport(SourceSurfaceTransport):
        def manifest_payload(self) -> dict[str, object]:
            payload = dict(super().manifest_payload())
            payload["source_contract_level"] = "fixed_ttsirt"
            payload["tt_cores_declared"] = True
            payload["defensive_density_declared"] = True
            return payload

    with pytest.raises(ValueError, match="tt_cores_declared"):
        highdim.SourceRouteTransportProtocol(MissingTTMetadataTransport())

    transport = highdim.SourceRouteTransportProtocol(DeclaredFixedTTSIRTTransport())
    assert transport.manifest_payload()["source_contract_level"] == "fixed_ttsirt"


def test_p57_m2_contract_exposes_author_surface_methods() -> None:
    transport = highdim.SourceRouteTransportProtocol(SourceSurfaceTransport())
    reference = tf.constant([[0.2, -0.3], [0.4, 0.1]], dtype=DTYPE)
    local = transport.inverse_transport(reference)

    payload = transport.manifest_payload()
    assert payload["proposal_density_semantics"] == "transport_eval_pdf_equivalent_on_local_samples"
    assert set(payload["required_source_methods"]) >= {
        "inverse_transport",
        "forward_transport",
        "conditional_inverse_transport",
        "eval_pdf",
        "potential",
        "proposal_log_density",
        "marginalize",
        "log_normalizer",
    }
    tf.debugging.assert_near(transport.forward_transport(local), reference)
    tf.debugging.assert_near(transport.potential(local), -tf.math.log(transport.eval_pdf(local)))
    assert transport.marginalize((0, 1)) is not None


def test_p57_m2_retained_sampling_uses_transport_eval_pdf_semantics() -> None:
    target = _target()
    transport = highdim.SourceRouteTransportProtocol(SourceSurfaceTransport())
    reference = tf.constant([[0.2, -0.3], [0.4, 0.1]], dtype=DTYPE)

    result = highdim.source_route_generate_retained_samples(
        target=target,
        transport=transport,
        reference_samples=reference,
        time_index=1,
    )
    local = transport.inverse_transport(reference)

    expected = tf.math.log(transport.eval_pdf(local))
    tf.debugging.assert_near(result.proposal_log_density, expected)
    assert result.retained_batch.sample_origin == "retained_from_transport"
