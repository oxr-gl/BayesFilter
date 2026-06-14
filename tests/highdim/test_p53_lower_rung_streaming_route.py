from __future__ import annotations

import inspect
import json
from pathlib import Path

import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64
MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m2-route-implementation-manifest-2026-06-10.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m2-route-implementation-result-2026-06-10.md"
)


class _ThetaShiftTransitionModel:
    def parameter_dim(self) -> int:
        return 1

    def state_dim(self) -> int:
        return 2

    def observation_dim(self) -> int:
        return 1

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        del theta
        x0 = tf.convert_to_tensor(x0, dtype=DTYPE)
        return -0.5 * tf.reduce_sum(tf.square(x0), axis=1)

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del t
        theta = tf.reshape(tf.convert_to_tensor(theta, dtype=DTYPE), [1])
        previous = tf.convert_to_tensor(x_prev, dtype=DTYPE)
        current = tf.convert_to_tensor(x_next, dtype=DTYPE)
        drift = tf.stack([theta[0], -0.5 * theta[0]])[tf.newaxis, :]
        residual = current - previous - drift
        return -0.5 * tf.reduce_sum(tf.square(residual), axis=1)

    def observation_log_density(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del theta, t
        x_t = tf.convert_to_tensor(x_t, dtype=DTYPE)
        y_t = tf.reshape(tf.convert_to_tensor(y_t, dtype=DTYPE), [1])
        return -0.5 * tf.square(y_t[0] - x_t[:, 0])


def _fixture_points() -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    current = tf.constant(
        [
            [-0.75, 0.15],
            [0.10, -0.30],
            [0.65, 0.45],
        ],
        dtype=DTYPE,
    )
    previous = tf.constant(
        [
            [-0.50, -0.20],
            [0.20, 0.10],
            [0.75, -0.35],
            [-0.15, 0.70],
        ],
        dtype=DTYPE,
    )
    previous_log_terms = tf.math.log(
        tf.constant([0.10, 0.20, 0.30, 0.40], dtype=DTYPE)
    )
    return current, previous, previous_log_terms


def _dense_reference(
    model: _ThetaShiftTransitionModel,
    theta: tf.Tensor,
    current: tf.Tensor,
    previous: tf.Tensor,
    previous_log_terms: tf.Tensor,
) -> tf.Tensor:
    rows = []
    previous_count = int(previous.shape[0])
    for index in range(int(current.shape[0])):
        current_rows = tf.broadcast_to(current[index : index + 1], [previous_count, 2])
        transition_log = model.transition_log_density(
            theta,
            previous,
            current_rows,
            t=3,
        )
        rows.append(tf.reduce_logsumexp(previous_log_terms + transition_log))
    return tf.stack(rows)


def test_p53_m2_route_manifest_preserves_lower_rung_nonclaims() -> None:
    config = highdim.LowerRungStreamingRouteConfig(
        current_block_size=2,
        previous_block_size=3,
    )
    manifest = highdim.p53_lower_rung_streaming_route_manifest(config)
    route = manifest["route"]

    assert manifest["schema_version"] == "p53.lower_rung_streaming_route.v1"
    assert route["route_class"] == highdim.P53_LOWER_RUNG_ROUTE_CLASS
    assert route["claim_class"] == highdim.P53_LOWER_RUNG_CLAIM_CLASS
    assert route["materializes_full_dense_pairs"] is False
    assert "no scaling-route readiness" in route["nonclaims"]
    assert "no d=18 spatial SIR readiness" in route["nonclaims"]


def test_p53_m2_route_source_avoids_full_dense_pair_materialization() -> None:
    source = inspect.getsource(highdim.lower_rung_streaming_predictive_log_density)

    assert "tf.repeat" not in source
    assert "tf.tile" not in source
    assert "current_count, previous_count" not in source
    assert "materializes_full_dense_pairs" not in source


def test_p53_m2_streaming_values_match_dense_reference_on_tiny_grid() -> None:
    model = _ThetaShiftTransitionModel()
    current, previous, previous_log_terms = _fixture_points()
    theta = tf.constant([0.35], dtype=DTYPE)
    config = highdim.LowerRungStreamingRouteConfig(
        current_block_size=2,
        previous_block_size=2,
    )

    result = highdim.lower_rung_streaming_predictive_log_density(
        model=model,
        theta=theta,
        current_physical_points=current,
        previous_physical_points=previous,
        previous_log_terms=previous_log_terms,
        time_index=3,
        config=config,
    )
    expected = _dense_reference(model, theta, current, previous, previous_log_terms)

    tf.debugging.assert_near(result.predictive_log_density, expected, atol=1e-12)
    assert result.metadata.route_class == "lower_rung_dense_equivalent"
    assert result.metadata.claim_class == "interface_tieout_only_not_scaling"
    assert result.metadata.route_width_proxy == int(previous.shape[0])
    assert result.metadata.max_transition_rows_per_call == 2
    assert result.metadata.materializes_full_dense_pairs is False
    assert result.metadata.exposes_reff_bound is False


def test_p53_m2_streaming_route_preserves_tensorflow_gradients() -> None:
    model = _ThetaShiftTransitionModel()
    current, previous, previous_log_terms = _fixture_points()
    theta = tf.Variable([0.35], dtype=DTYPE)

    with tf.GradientTape() as tape:
        result = highdim.lower_rung_streaming_predictive_log_density(
            model=model,
            theta=theta,
            current_physical_points=current,
            previous_physical_points=previous,
            previous_log_terms=previous_log_terms,
            time_index=3,
            config=highdim.LowerRungStreamingRouteConfig(
                current_block_size=1,
                previous_block_size=2,
            ),
        )
        objective = tf.reduce_sum(result.predictive_log_density)

    gradient = tape.gradient(objective, theta)
    assert gradient is not None
    assert gradient.shape == theta.shape
    assert bool(tf.reduce_all(tf.math.is_finite(gradient)).numpy())
    assert abs(float(gradient[0].numpy())) > 1e-8


def test_p53_m2_persisted_manifest_and_result_emit_pass_token() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    result = RESULT_PATH.read_text(encoding="utf-8")

    assert manifest["schema_version"] == "p53.lower_rung_streaming_route.v1"
    assert manifest["status"] == "PASS_P53_M2_ROUTE_IMPLEMENTATION"
    assert manifest["route"]["route_class"] == "lower_rung_dense_equivalent"
    assert manifest["route"]["claim_class"] == "interface_tieout_only_not_scaling"
    assert "PASS_P53_M2_ROUTE_IMPLEMENTATION" in result
    assert "PASS_P53_M4D_SCALING_ROUTE_ADMISSION" in result
