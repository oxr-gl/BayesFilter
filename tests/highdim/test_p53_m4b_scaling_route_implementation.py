from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64
MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4b-scaling-route-implementation-manifest-2026-06-10.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4b-scaling-route-implementation-result-2026-06-10.md"
)


def _config() -> highdim.LocalNeighborhoodScalingRouteConfig:
    return highdim.LocalNeighborhoodScalingRouteConfig(
        basis_order=3,
        tt_rank_left=2,
        tt_rank_right=2,
        memory_cap_bytes=100_000_000,
        branch_id="p53-m4b-test-branch",
    )


def _previous_points(model: highdim.SpatialSIRSSM) -> tf.Tensor:
    base = tf.convert_to_tensor(model.initial_mean, dtype=DTYPE)
    direction = 0.001 * tf.cast(tf.range(1, int(model.state_dim()) + 1), dtype=DTYPE)
    return tf.stack([base - direction, base, base + direction])


def test_p53_m4b_metadata_is_scaling_route_not_c_low_relabel() -> None:
    model = highdim.p30_spatial_sir_fixture_model(3)
    metadata = highdim.spatial_sir_local_scaling_route_metadata(model, _config())
    payload = metadata.manifest_payload()

    assert payload["route_id"] == highdim.P53_LOCAL_SCALING_ROUTE_ID
    assert payload["route_class"] == highdim.P53_SCALING_ROUTE_CLASS
    assert payload["selected_design"] == highdim.P53_LOCAL_SCALING_SELECTED_DESIGN
    assert payload["route_id"] != "p53_lower_rung_streaming_dense_equivalent"
    assert payload["covariance_scope"] == "diagonal_process_covariance"
    assert payload["R_eff"] > 0
    assert payload["memory_forecast_bytes"] > 0
    assert "no scaling-route admission yet" in payload["nonclaims"]


def test_p53_m4b_replay_identity_pins_required_fields() -> None:
    model = highdim.p30_spatial_sir_fixture_model(2)
    metadata = highdim.spatial_sir_local_scaling_route_metadata(model, _config())
    replay = metadata.replay_identity

    for field in (
        "route_id",
        "route_class",
        "selected_design",
        "rk4_substeps",
        "dependency_neighborhoods",
        "basis_order",
        "tt_rank_metadata",
        "R_eff",
        "memory_forecast_bytes",
        "covariance_scope",
        "dtype",
        "branch_id",
    ):
        assert field in replay
    assert replay["route_class"] == "scaling_route"
    assert replay["branch_id"] == "p53-m4b-test-branch"


def test_p53_m4b_local_coordinate_factor_matches_transition_coordinate_density() -> None:
    model = highdim.p30_spatial_sir_fixture_model(2)
    previous = _previous_points(model)
    coordinate = 1
    means = model.transition_mean(previous)[:, coordinate]
    current_values = tf.constant(
        [
            float(means[0].numpy()) - 0.01,
            float(means[1].numpy()),
            float(means[2].numpy()) + 0.02,
        ],
        dtype=DTYPE,
    )

    result = highdim.spatial_sir_local_coordinate_log_factor(
        model=model,
        theta=tf.zeros([0], dtype=DTYPE),
        previous_physical_points=previous,
        current_coordinate_values=current_values,
        coordinate_index=coordinate,
        config=_config(),
    )
    variance = tf.linalg.diag_part(model.process_covariance)[coordinate]
    expected = -0.5 * (
        tf.math.log(tf.constant(2.0 * 3.141592653589793, dtype=DTYPE))
        + tf.math.log(variance)
        + tf.square(current_values[:, tf.newaxis] - means[tf.newaxis, :]) / variance
    )

    tf.debugging.assert_near(result.log_factor, expected, atol=1e-12)
    assert result.metadata.route_class == "scaling_route"
    assert coordinate in result.dependency_neighborhood


def test_p53_m4b_local_coordinate_factor_preserves_current_value_gradients() -> None:
    model = highdim.p30_spatial_sir_fixture_model(1)
    previous = _previous_points(model)
    current_values = tf.Variable([486.0, 486.1], dtype=DTYPE)

    with tf.GradientTape() as tape:
        result = highdim.spatial_sir_local_coordinate_log_factor(
            model=model,
            theta=tf.zeros([0], dtype=DTYPE),
            previous_physical_points=previous,
            current_coordinate_values=current_values,
            coordinate_index=0,
            config=_config(),
        )
        objective = tf.reduce_sum(result.log_factor)

    gradient = tape.gradient(objective, current_values)
    assert gradient is not None
    assert gradient.shape == current_values.shape
    assert bool(tf.reduce_all(tf.math.is_finite(gradient)).numpy())


def test_p53_m4b_blocks_non_diagonal_process_covariance() -> None:
    model = highdim.SpatialSIRSSM(
        kappa=tf.constant([0.1], dtype=DTYPE),
        nu=tf.constant([18.0], dtype=DTYPE),
        initial_mean=tf.constant([486.0, 14.0], dtype=DTYPE),
        neighbor_sets=((),),
        process_covariance=tf.constant([[1.0, 0.2], [0.2, 1.0]], dtype=DTYPE),
    )

    with pytest.raises(ValueError, match="diagonal process covariance"):
        highdim.spatial_sir_local_scaling_route_metadata(model, _config())


def test_p53_m4b_source_avoids_global_pairwise_route_patterns() -> None:
    source = inspect.getsource(highdim.spatial_sir_local_coordinate_log_factor)

    assert "tf.repeat" not in source
    assert "tf.tile" not in source
    assert "lower_rung_streaming_predictive_log_density" not in source
    assert "previous_count" not in source
    assert "current_count" not in source


def test_p53_m4b_persisted_manifest_and_result_emit_only_m4b_token() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    result = RESULT_PATH.read_text(encoding="utf-8")

    assert manifest["schema_version"] == "p53.local_scaling_route.v1"
    assert manifest["status"] == "PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION"
    assert manifest["route"]["route_class"] == "scaling_route"
    assert manifest["route"]["selected_design"] == "local-neighborhood sparse transition contraction"
    assert manifest["tokens_emitted"] == ["PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION"]
    assert "PASS_P53_M4C_SCALING_ROUTE_TIEOUT" in manifest["forbidden_tokens"]
    assert "PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION" in result
