from __future__ import annotations

import inspect
import json
from pathlib import Path

import tensorflow as tf

import bayesfilter.highdim as highdim
import bayesfilter.highdim.filtering as filtering_module


DTYPE = tf.float64
VALUE_ATOL = 1e-8
GRADIENT_ATOL = 1e-6
MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-manifest-2026-06-10.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-result-2026-06-10.md"
)


def _config() -> highdim.LocalNeighborhoodScalingRouteConfig:
    return highdim.LocalNeighborhoodScalingRouteConfig(
        basis_order=3,
        tt_rank_left=2,
        tt_rank_right=2,
        memory_cap_bytes=100_000_000,
        branch_id="p53-m4c-tieout-branch",
    )


def _spatial_sir_points(
    model: highdim.SpatialSIRSSM,
    count: int,
    offset_scale: float,
) -> tf.Tensor:
    dim = int(model.state_dim())
    base = tf.convert_to_tensor(model.initial_mean, dtype=DTYPE)
    direction = 0.001 * tf.cast(tf.range(1, dim + 1), dtype=DTYPE)
    center = 0.5 * tf.cast(int(count) - 1, dtype=DTYPE)
    rows = []
    for index in range(int(count)):
        signed = tf.cast(index, dtype=DTYPE) - center
        rows.append(base + tf.constant(offset_scale, dtype=DTYPE) + signed * direction)
    return tf.stack(rows)


def _previous_log_terms(
    model: highdim.SpatialSIRSSM,
    previous: tf.Tensor,
) -> tf.Tensor:
    count = int(previous.shape[0])
    raw_weights = tf.cast(tf.range(1, count + 1), dtype=DTYPE)
    weights = raw_weights / tf.reduce_sum(raw_weights)
    return tf.math.log(weights) + model.initial_log_density(
        tf.zeros([0], dtype=DTYPE),
        previous,
    )


def _dense_transition(
    model: highdim.SpatialSIRSSM,
    current: tf.Tensor,
    previous: tf.Tensor,
) -> tf.Tensor:
    return filtering_module._multistate_pairwise_transition_between_grids_log_density(
        model=model,
        theta=tf.zeros([0], dtype=DTYPE),
        current_physical_points=current,
        previous_physical_points=previous,
        time_index=1,
    )


def _dense_predictive(
    model: highdim.SpatialSIRSSM,
    current: tf.Tensor,
    previous: tf.Tensor,
    previous_terms: tf.Tensor,
) -> tf.Tensor:
    transition_log = _dense_transition(model, current, previous)
    return tf.reduce_logsumexp(previous_terms[tf.newaxis, :] + transition_log, axis=1)


def _one_step_log_increment(
    model: highdim.SpatialSIRSSM,
    current: tf.Tensor,
    predictive: tf.Tensor,
) -> tf.Tensor:
    count = int(current.shape[0])
    raw_weights = tf.cast(tf.range(1, count + 1), dtype=DTYPE)
    weights = raw_weights / tf.reduce_sum(raw_weights)
    observation = model.infectious_components(current)[0]
    observation_log = model.observation_log_density(
        tf.zeros([0], dtype=DTYPE),
        current,
        observation,
        t=1,
    )
    return tf.reduce_logsumexp(tf.math.log(weights) + predictive + observation_log)


def test_p53_m4c_local_scaling_route_ties_out_transition_predictive_and_increment() -> None:
    for compartments in (1, 2, 3):
        model = highdim.p30_spatial_sir_fixture_model(compartments)
        current = _spatial_sir_points(model, count=compartments + 2, offset_scale=0.025)
        previous = _spatial_sir_points(model, count=compartments + 3, offset_scale=-0.015)
        previous_terms = _previous_log_terms(model, previous)

        dense_transition = _dense_transition(model, current, previous)
        dense_predictive = _dense_predictive(model, current, previous, previous_terms)
        local = highdim.spatial_sir_local_predictive_log_density(
            model=model,
            theta=tf.zeros([0], dtype=DTYPE),
            current_physical_points=current,
            previous_physical_points=previous,
            previous_log_terms=previous_terms,
            time_index=1,
            config=_config(),
        )

        tf.debugging.assert_near(local.transition_log_density, dense_transition, atol=VALUE_ATOL)
        tf.debugging.assert_near(local.predictive_log_density, dense_predictive, atol=VALUE_ATOL)
        tf.debugging.assert_near(
            _one_step_log_increment(model, current, local.predictive_log_density),
            _one_step_log_increment(model, current, dense_predictive),
            atol=VALUE_ATOL,
        )
        assert local.metadata.route_class == "scaling_route"
        assert local.metadata.route_id == highdim.P53_LOCAL_SCALING_ROUTE_ID
        assert local.metadata.R_eff > 0
        assert local.metadata.memory_forecast_bytes <= _config().memory_cap_bytes
        assert local.tieout_adapter_scope == "lower_rung_diagnostic_not_production_contraction"


def test_p53_m4c_current_gradients_match_dense_reference() -> None:
    for compartments in (1, 2, 3):
        model = highdim.p30_spatial_sir_fixture_model(compartments)
        current = _spatial_sir_points(model, count=compartments + 2, offset_scale=0.025)
        previous = _spatial_sir_points(model, count=compartments + 3, offset_scale=-0.015)
        previous_terms = _previous_log_terms(model, previous)

        dense_current = tf.Variable(current)
        with tf.GradientTape() as dense_tape:
            dense_objective = tf.reduce_sum(
                _dense_predictive(model, dense_current, previous, previous_terms)
            )
        dense_gradient = dense_tape.gradient(dense_objective, dense_current)

        local_current = tf.Variable(current)
        with tf.GradientTape() as local_tape:
            local_objective = tf.reduce_sum(
                highdim.spatial_sir_local_predictive_log_density(
                    model=model,
                    theta=tf.zeros([0], dtype=DTYPE),
                    current_physical_points=local_current,
                    previous_physical_points=previous,
                    previous_log_terms=previous_terms,
                    time_index=1,
                    config=_config(),
                ).predictive_log_density
            )
        local_gradient = local_tape.gradient(local_objective, local_current)

        assert dense_gradient is not None
        assert local_gradient is not None
        assert bool(tf.reduce_all(tf.math.is_finite(dense_gradient)).numpy())
        assert bool(tf.reduce_all(tf.math.is_finite(local_gradient)).numpy())
        tf.debugging.assert_near(local_gradient, dense_gradient, atol=GRADIENT_ATOL)


def test_p53_m4c_tieout_adapter_source_has_no_global_repeat_or_tile() -> None:
    pairwise_source = inspect.getsource(highdim.spatial_sir_local_pairwise_transition_log_density)
    predictive_source = inspect.getsource(highdim.spatial_sir_local_predictive_log_density)

    assert "tf.repeat" not in pairwise_source
    assert "tf.tile" not in pairwise_source
    assert "_multistate_pairwise_transition_between_grids_log_density" not in pairwise_source
    assert "tf.repeat" not in predictive_source
    assert "tf.tile" not in predictive_source


def test_p53_m4c_manifest_and_result_emit_only_tieout_token() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    result = RESULT_PATH.read_text(encoding="utf-8")

    assert manifest["schema_version"] == "p53.scaling_route_tieout.v1"
    assert manifest["status"] == "PASS_P53_M4C_SCALING_ROUTE_TIEOUT"
    assert manifest["route"]["route_class"] == "scaling_route"
    assert manifest["tieout_adapter_scope"] == "lower_rung_diagnostic_not_production_contraction"
    assert manifest["tolerances"]["predictive_log_density_atol"] == VALUE_ATOL
    assert manifest["tolerances"]["one_step_log_increment_atol"] == VALUE_ATOL
    assert manifest["tolerances"]["gradient_atol"] == GRADIENT_ATOL
    assert manifest["tokens_emitted"] == ["PASS_P53_M4C_SCALING_ROUTE_TIEOUT"]
    assert "PASS_P53_M4D_SCALING_ROUTE_ADMISSION" in manifest["forbidden_tokens"]
    assert "PASS_P53_M4C_SCALING_ROUTE_TIEOUT" in result
    assert "does not emit `PASS_P53_M4D_SCALING_ROUTE_ADMISSION`" in result
