from __future__ import annotations

import argparse
import math
import sys

import pytest
import tensorflow as tf

from docs.benchmarks import benchmark_p8p_regression_fd_reparameterization as harness
from docs.benchmarks import benchmark_p8p_parameterized_sir_gradient as p8p
from experiments.dpf_implementation.tf_tfp.filters import (
    experimental_batched_ledh_pfpf_ot_streaming_tf as streaming_tf,
)
from experiments.dpf_implementation.tf_tfp.filters import (
    experimental_batched_ledh_pfpf_ot_tf as core_tf,
)


DTYPE = harness.p8p.DTYPE


def _thirteen_offsets() -> str:
    return "-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6"


def test_p82_parse_offsets_accepts_thirteen_points() -> None:
    parsed = harness._parse_offsets(_thirteen_offsets())

    assert len(parsed) == 13
    assert parsed[0] == -6.0
    assert parsed[-1] == 6.0
    with pytest.raises(ValueError, match="7, 9, 13, 15, or 17"):
        harness._parse_offsets("-5,-4,-3,-2,-1,0,1,2,3,4,5")


def test_p82_default_seed_count_remains_five(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["prog", "--output", "/tmp/p82-no-run.json"])

    args = harness._parse_args()

    assert args.batch_seeds == [81120, 81121, 81122, 81123, 81124]


def test_p82_cli_accepts_governed_fd_protocol_switches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prog",
            "--output",
            "/tmp/p82-no-run.json",
            f"--regression-offsets={_thirteen_offsets()}",
            "--trim-extreme-offsets",
            "1",
            "--trim-extreme-mode",
            "value",
            "--fd-evaluation-mode",
            "batched-theta",
            "--fd-mode",
            "enabled",
            "--num-particles",
            "1000",
        ],
    )

    args = harness._parse_args()

    assert len(args.regression_offsets_values) == 13
    assert args.trim_extreme_offsets == 1
    assert args.trim_extreme_mode == "value"
    assert args.fd_evaluation_mode == "batched-theta"
    assert args.fd_mode == "enabled"
    assert args.num_particles == 1000


def test_p82_cli_accepts_ad_only_fd_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prog",
            "--output",
            "/tmp/p82-no-run.json",
            "--fd-mode",
            "ad-only",
        ],
    )

    args = harness._parse_args()

    assert args.fd_mode == "ad-only"


def test_p82_cli_accepts_manual_streaming_transport_gradient_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manual_mode = core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prog",
            "--output",
            "/tmp/p82-no-run.json",
            "--transport-plan-mode",
            "streaming",
            "--transport-ad-mode",
            "stabilized",
            "--transport-gradient-mode",
            manual_mode,
        ],
    )

    args = harness._parse_args()

    assert args.transport_gradient_mode == manual_mode


def test_s7_cli_accepts_blockwise_manual_streaming_transport_gradient_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blockwise_mode = core_tf.MANUAL_STREAMING_BLOCKWISE_VJP_FINITE_TRANSPORT_GRADIENT_MODE
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prog",
            "--output",
            "/tmp/s7-no-run.json",
            "--transport-plan-mode",
            "streaming",
            "--transport-ad-mode",
            "stabilized",
            "--transport-gradient-mode",
            blockwise_mode,
        ],
    )

    args = harness._parse_args()

    assert args.transport_gradient_mode == blockwise_mode


def test_p82_parameterized_cli_accepts_manual_streaming_transport_gradient_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manual_mode = core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prog",
            "--output",
            "/tmp/p82-no-run.json",
            "--transport-plan-mode",
            "streaming",
            "--transport-ad-mode",
            "stabilized",
            "--transport-gradient-mode",
            manual_mode,
        ],
    )

    args = p8p._parse_args()

    assert args.transport_gradient_mode == manual_mode


def test_p82_streaming_value_core_forwards_transport_gradient_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: list[str] = []
    manual_mode = core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE
    observations = tf.zeros([1, 1], dtype=DTYPE)
    initial_particles = tf.reshape(
        tf.constant([0.0, 1.0], dtype=DTYPE),
        [1, 2, 1],
    )
    fixed_resampling_mask = tf.constant([[True]], dtype=tf.bool)

    def observation_fn(points: tf.Tensor) -> tf.Tensor:
        return points

    def log_density(points: tf.Tensor, _other: tf.Tensor, _time: tf.Tensor) -> tf.Tensor:
        return tf.zeros(tf.shape(points)[:2], dtype=points.dtype)

    def fake_transport(
        particles: tf.Tensor,
        log_weights: tf.Tensor,
        fixed_resampling_mask: tf.Tensor,
        *,
        transport_gradient_mode: str,
        **_kwargs,
    ) -> core_tf.BatchedAnnealedTransportTensors:
        captured.append(transport_gradient_mode)
        return core_tf.BatchedAnnealedTransportTensors(
            particles=particles,
            log_weights=log_weights,
            transport_matrix=tf.zeros([1, 0, 0], dtype=particles.dtype),
            max_row_residual=tf.constant(0.0, dtype=particles.dtype),
            max_column_residual=tf.constant(0.0, dtype=particles.dtype),
        )

    monkeypatch.setattr(streaming_tf, "batched_annealed_transport_core_tf", fake_transport)

    result = streaming_tf.streaming_batched_ledh_pfpf_ot_value_core_tf(
        observations=observations,
        initial_particles=initial_particles,
        fixed_resampling_mask=fixed_resampling_mask,
        transition_matrix=tf.ones([1, 1, 1], dtype=DTYPE),
        transition_covariance=tf.ones([1, 1, 1], dtype=DTYPE),
        observation_covariance=tf.ones([1, 1, 1], dtype=DTYPE),
        observation_fn=observation_fn,
        observation_jacobian_fn=lambda points: tf.ones([tf.shape(points)[0], tf.shape(points)[1], 1, 1], dtype=points.dtype),
        observation_residual_fn=lambda points, observation: points - observation[None, None, :],
        transition_log_density_fn=log_density,
        observation_log_density_fn=log_density,
        pre_flow_step_fn=lambda particles, _time: particles,
        sinkhorn_iterations=2,
        transport_gradient_mode=manual_mode,
        transport_plan_mode="streaming",
        transport_ad_mode="stabilized",
        row_chunk_size=2,
        col_chunk_size=2,
        particle_chunk_size=2,
    )

    assert captured == [manual_mode]
    assert result.log_likelihood.shape == (1,)


def test_s7_streaming_value_core_forwards_blockwise_transport_gradient_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: list[str] = []
    blockwise_mode = core_tf.MANUAL_STREAMING_BLOCKWISE_VJP_FINITE_TRANSPORT_GRADIENT_MODE
    observations = tf.zeros([1, 1], dtype=DTYPE)
    initial_particles = tf.reshape(
        tf.constant([0.0, 1.0], dtype=DTYPE),
        [1, 2, 1],
    )
    fixed_resampling_mask = tf.constant([[True]], dtype=tf.bool)

    def observation_fn(points: tf.Tensor) -> tf.Tensor:
        return points

    def log_density(points: tf.Tensor, _other: tf.Tensor, _time: tf.Tensor) -> tf.Tensor:
        return tf.zeros(tf.shape(points)[:2], dtype=points.dtype)

    def fake_transport(
        particles: tf.Tensor,
        log_weights: tf.Tensor,
        fixed_resampling_mask: tf.Tensor,
        *,
        transport_gradient_mode: str,
        **_kwargs,
    ) -> core_tf.BatchedAnnealedTransportTensors:
        captured.append(transport_gradient_mode)
        return core_tf.BatchedAnnealedTransportTensors(
            particles=particles,
            log_weights=log_weights,
            transport_matrix=tf.zeros([1, 0, 0], dtype=particles.dtype),
            max_row_residual=tf.constant(0.0, dtype=particles.dtype),
            max_column_residual=tf.constant(0.0, dtype=particles.dtype),
        )

    monkeypatch.setattr(streaming_tf, "batched_annealed_transport_core_tf", fake_transport)

    result = streaming_tf.streaming_batched_ledh_pfpf_ot_value_core_tf(
        observations=observations,
        initial_particles=initial_particles,
        fixed_resampling_mask=fixed_resampling_mask,
        transition_matrix=tf.ones([1, 1, 1], dtype=DTYPE),
        transition_covariance=tf.ones([1, 1, 1], dtype=DTYPE),
        observation_covariance=tf.ones([1, 1, 1], dtype=DTYPE),
        observation_fn=observation_fn,
        observation_jacobian_fn=lambda points: tf.ones(
            [tf.shape(points)[0], tf.shape(points)[1], 1, 1],
            dtype=points.dtype,
        ),
        observation_residual_fn=lambda points, observation: points - observation[None, None, :],
        transition_log_density_fn=log_density,
        observation_log_density_fn=log_density,
        pre_flow_step_fn=lambda particles, _time: particles,
        sinkhorn_iterations=2,
        transport_gradient_mode=blockwise_mode,
        transport_plan_mode="streaming",
        transport_ad_mode="stabilized",
        row_chunk_size=2,
        col_chunk_size=2,
        particle_chunk_size=2,
    )

    assert captured == [blockwise_mode]
    assert result.log_likelihood.shape == (1,)


def test_p82_value_trim_drops_objective_extrema_not_extreme_offsets() -> None:
    xs = tf.constant([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6], dtype=DTYPE)
    y = tf.constant([0, 1, -10, 2, 3, 4, 5, 6, 12, 7, 8, 9, 10], dtype=DTYPE)
    theta_rows = tf.stack([xs, xs + 100.0, xs + 200.0], axis=1)

    fit_xs, fit_y, fit_theta_rows, trim_record = harness._trim_extreme_points(
        xs,
        y,
        theta_rows,
        1,
        trim_mode="value",
    )

    assert trim_record["trim_mode"] == "value"
    assert trim_record["evaluated_point_count"] == 13
    assert trim_record["fit_point_count"] == 11
    assert trim_record["dropped_low_value_points"] == [
        {"index": 2, "x": -4.0, "objective_value": -10.0}
    ]
    assert trim_record["dropped_high_value_points"] == [
        {"index": 8, "x": 2.0, "objective_value": 12.0}
    ]
    assert 0 in trim_record["fit_point_indices"]
    assert 12 in trim_record["fit_point_indices"]
    assert 2 not in trim_record["fit_point_indices"]
    assert 8 not in trim_record["fit_point_indices"]
    assert fit_xs.shape[0] == 11
    assert fit_y.shape[0] == 11
    assert fit_theta_rows.shape[0] == 11


def test_p82_value_trim_has_deterministic_tie_breaking() -> None:
    xs = tf.constant([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6], dtype=DTYPE)
    y = tf.constant([0, 0, 0, 0, -1, -1, 0, 10, 10, 0, 0, 0, 0], dtype=DTYPE)
    theta_rows = tf.stack([xs, xs, xs], axis=1)

    _fit_xs, _fit_y, _fit_theta_rows, trim_record = harness._trim_extreme_points(
        xs,
        y,
        theta_rows,
        1,
        trim_mode="value",
    )

    assert trim_record["dropped_low_value_points"] == [
        {"index": 4, "x": -2.0, "objective_value": -1.0}
    ]
    assert trim_record["dropped_high_value_points"] == [
        {"index": 7, "x": 1.0, "objective_value": 10.0}
    ]
    assert "original index" in trim_record["tie_break_rule"]


def test_p82_value_trim_preserves_raw_line_metadata_and_fits_eleven_points() -> None:
    xs = tf.constant([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6], dtype=DTYPE)
    y = 1.5 + 2.0 * xs
    y = tf.tensor_scatter_nd_update(
        y,
        indices=tf.constant([[3], [9]], dtype=tf.int32),
        updates=tf.constant([-100.0, 100.0], dtype=DTYPE),
    )
    theta_rows = tf.stack([xs, xs + 1.0, xs + 2.0], axis=1)

    fit_xs, fit_y, _fit_theta_rows, trim_record = harness._trim_extreme_points(
        xs,
        y,
        theta_rows,
        1,
        trim_mode="value",
    )
    fit = harness._linear_regression(fit_xs, fit_y)
    manual_fit = harness._linear_regression(
        tf.gather(xs, trim_record["fit_point_indices"]),
        tf.gather(y, trim_record["fit_point_indices"]),
    )

    assert len(y.numpy().tolist()) == 13
    assert trim_record["fit_point_count"] == 11
    assert len(trim_record["fit_point_indices"]) == 11
    assert len(trim_record["fit_x_values"]) == 11
    assert len(trim_record["fit_objective_values"]) == 11
    assert fit["slope"] == pytest.approx(manual_fit["slope"])
    assert fit["slope_standard_error"] == pytest.approx(
        manual_fit["slope_standard_error"]
    )


def test_p82_offset_trim_mode_is_preserved_for_existing_diagnostics() -> None:
    xs = tf.constant([-3, -2, -1, 0, 1, 2, 3], dtype=DTYPE)
    y = tf.constant([100, 5, 4, 3, 2, 1, -100], dtype=DTYPE)
    theta_rows = tf.stack([xs, xs, xs], axis=1)

    fit_xs, _fit_y, _fit_theta_rows, trim_record = harness._trim_extreme_points(
        xs,
        y,
        theta_rows,
        1,
        trim_mode="offset",
    )

    assert trim_record["trim_mode"] == "offset"
    assert trim_record["dropped_point_indices"] == [0, 6]
    assert fit_xs.numpy().tolist() == pytest.approx([-2, -1, 0, 1, 2])


def test_s7r_result_contract_metadata_emits_required_top_level_keys() -> None:
    args = argparse.Namespace(batch_seeds=[81120, 81121, 81122, 81123, 81124])
    metadata = harness._result_contract_metadata(
        args,
        objective=tf.constant(1.25, dtype=DTYPE),
        gradient=tf.constant([1.0, -2.0, 3.0], dtype=DTYPE),
        per_seed_gradient=tf.constant(
            [
                [1.0, -2.0, 3.0],
                [1.1, -2.1, 3.1],
                [0.9, -1.9, 2.9],
                [1.2, -2.2, 3.2],
                [0.8, -1.8, 2.8],
            ],
            dtype=DTYPE,
        ),
        gradients_connected=True,
    )

    assert metadata["status"] == "pass"
    assert metadata["primary_pass"] is True
    assert metadata["batch_seeds"] == [81120, 81121, 81122, 81123, 81124]
    assert metadata["gradient_values"] == pytest.approx([1.0, -2.0, 3.0])
    assert metadata["objective_finite"] is True
    assert metadata["gradient_finite"] is True
    assert metadata["monte_carlo_gradient_noise_mcse_finite"] is True
    for record in metadata["monte_carlo_gradient_noise"].values():
        assert math.isfinite(float(record["standard_error_of_batch_mean"]))


def test_s7r_result_contract_metadata_blocks_nonfinite_gradient() -> None:
    args = argparse.Namespace(batch_seeds=[81120, 81121, 81122, 81123, 81124])
    metadata = harness._result_contract_metadata(
        args,
        objective=tf.constant(1.25, dtype=DTYPE),
        gradient=tf.constant([1.0, float("nan"), 3.0], dtype=DTYPE),
        per_seed_gradient=tf.ones([5, 3], dtype=DTYPE),
        gradients_connected=True,
    )

    assert metadata["status"] == "blocked_or_failed"
    assert metadata["primary_pass"] is False
    assert metadata["gradient_finite"] is False


def test_s7r_transport_metadata_declares_no_dense_transport_matrix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blockwise_mode = core_tf.MANUAL_STREAMING_BLOCKWISE_VJP_FINITE_TRANSPORT_GRADIENT_MODE
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prog",
            "--output",
            "/tmp/s7r-no-run.json",
            "--transport-plan-mode",
            "streaming",
            "--transport-ad-mode",
            "stabilized",
            "--transport-gradient-mode",
            blockwise_mode,
        ],
    )

    args = harness._parse_args()
    transport = harness._transport_metadata(args)

    assert transport["transport_plan_mode"] == "streaming"
    assert transport["transport_ad_mode"] == "stabilized"
    assert transport["gradient_mode"] == blockwise_mode
    assert transport["dense_transport_matrix_materialized"] is False
