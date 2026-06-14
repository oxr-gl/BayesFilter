from __future__ import annotations

import json
from pathlib import Path

import tensorflow as tf

import bayesfilter.highdim as highdim
import bayesfilter.highdim.filtering as filtering_module


DTYPE = tf.float64
VALUE_ATOL = 1e-10
GRADIENT_ATOL = 1e-8
MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m3-lower-rung-dense-tieout-manifest-2026-06-10.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m3-lower-rung-dense-tieout-result-2026-06-10.md"
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


def _dense_predictive(
    model: highdim.SpatialSIRSSM,
    current: tf.Tensor,
    previous: tf.Tensor,
    previous_terms: tf.Tensor,
) -> tf.Tensor:
    transition_log = filtering_module._multistate_pairwise_transition_between_grids_log_density(
        model=model,
        theta=tf.zeros([0], dtype=DTYPE),
        current_physical_points=current,
        previous_physical_points=previous,
        time_index=1,
    )
    return tf.reduce_logsumexp(previous_terms[tf.newaxis, :] + transition_log, axis=1)


def _streaming_predictive(
    model: highdim.SpatialSIRSSM,
    current: tf.Tensor,
    previous: tf.Tensor,
    previous_terms: tf.Tensor,
) -> highdim.LowerRungStreamingRouteResult:
    return highdim.lower_rung_streaming_predictive_log_density(
        model=model,
        theta=tf.zeros([0], dtype=DTYPE),
        current_physical_points=current,
        previous_physical_points=previous,
        previous_log_terms=previous_terms,
        time_index=1,
        config=highdim.LowerRungStreamingRouteConfig(
            current_block_size=2,
            previous_block_size=2,
        ),
    )


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


def test_p53_m3_spatial_sir_j1_j2_j3_predictive_and_likelihood_tieout() -> None:
    for compartments in (1, 2, 3):
        model = highdim.p30_spatial_sir_fixture_model(compartments)
        current = _spatial_sir_points(model, count=compartments + 2, offset_scale=0.025)
        previous = _spatial_sir_points(model, count=compartments + 3, offset_scale=-0.015)
        previous_terms = _previous_log_terms(model, previous)

        dense = _dense_predictive(model, current, previous, previous_terms)
        streaming_result = _streaming_predictive(model, current, previous, previous_terms)
        streaming = streaming_result.predictive_log_density

        tf.debugging.assert_near(streaming, dense, atol=VALUE_ATOL)
        tf.debugging.assert_near(
            _one_step_log_increment(model, current, streaming),
            _one_step_log_increment(model, current, dense),
            atol=VALUE_ATOL,
        )
        assert streaming_result.metadata.route_class == "lower_rung_dense_equivalent"
        assert streaming_result.metadata.claim_class == "interface_tieout_only_not_scaling"
        assert streaming_result.metadata.route_width_proxy == int(previous.shape[0])
        assert streaming_result.metadata.materializes_full_dense_pairs is False


def test_p53_m3_spatial_sir_j1_j2_j3_current_gradients_match_dense_reference() -> None:
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

        streaming_current = tf.Variable(current)
        with tf.GradientTape() as streaming_tape:
            streaming_objective = tf.reduce_sum(
                _streaming_predictive(
                    model,
                    streaming_current,
                    previous,
                    previous_terms,
                ).predictive_log_density
            )
        streaming_gradient = streaming_tape.gradient(streaming_objective, streaming_current)

        assert dense_gradient is not None
        assert streaming_gradient is not None
        assert bool(tf.reduce_all(tf.math.is_finite(dense_gradient)).numpy())
        assert bool(tf.reduce_all(tf.math.is_finite(streaming_gradient)).numpy())
        tf.debugging.assert_near(streaming_gradient, dense_gradient, atol=GRADIENT_ATOL)


def test_p53_m3_manifest_and_result_preserve_tolerances_and_nonpromotion() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    result = RESULT_PATH.read_text(encoding="utf-8")

    assert manifest["schema_version"] == "p53.lower_rung_dense_tieout.v1"
    assert manifest["status"] == "PASS_P53_M3_LOWER_RUNG_DENSE_TIEOUT"
    assert manifest["tolerances"]["predictive_log_density_atol"] == VALUE_ATOL
    assert manifest["tolerances"]["one_step_log_increment_atol"] == VALUE_ATOL
    assert manifest["tolerances"]["current_gradient_atol"] == GRADIENT_ATOL
    assert manifest["route_class"] == "lower_rung_dense_equivalent"
    assert manifest["claim_class"] == "interface_tieout_only_not_scaling"
    assert manifest["phase_evidence_class"] == "lower_rung_dense_tieout_not_scaling"
    assert "PASS_P53_M4D_SCALING_ROUTE_ADMISSION" not in manifest["tokens_emitted"]
    assert "PASS_P53_M3_LOWER_RUNG_DENSE_TIEOUT" in result
    assert "does not emit `PASS_P53_M4D_SCALING_ROUTE_ADMISSION`" in result
