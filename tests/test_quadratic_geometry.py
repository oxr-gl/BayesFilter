from __future__ import annotations

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.inference.quadratic_geometry import (
    LOW_RANK_SPD_QUADRATIC_GEOMETRY_NONCLAIMS,
    LowRankSPDQuadraticGeometryConfig,
    fit_low_rank_spd_quadratic_geometry,
)


def _quadratic_target(
    precision: np.ndarray,
    *,
    mode: np.ndarray | None = None,
    shift: float = 0.0,
):
    precision_tf = tf.constant(precision, dtype=tf.float64)
    mode_tf = tf.zeros([precision.shape[0]], dtype=tf.float64) if mode is None else tf.constant(mode, dtype=tf.float64)

    def value_and_score(theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        theta = tf.reshape(tf.convert_to_tensor(theta, dtype=tf.float64), [-1])
        delta = theta - mode_tf
        value = tf.constant(float(shift), dtype=tf.float64) - 0.5 * tf.tensordot(
            delta,
            tf.linalg.matvec(precision_tf, delta),
            axes=1,
        )
        score = -tf.linalg.matvec(precision_tf, delta)
        return value, score

    return value_and_score


def test_synthetic_low_rank_spd_quadratic_recovers_precision() -> None:
    q = np.eye(4, 2)
    true_precision = 1.4 * np.eye(4) + (q * np.array([2.0, 0.7])) @ q.T
    result = fit_low_rank_spd_quadratic_geometry(
        _quadratic_target(true_precision),
        np.zeros(4),
        config=LowRankSPDQuadraticGeometryConfig(
            rank=2,
            sample_count=260,
            pilot_direction_count=512,
            trust_radius=0.8,
            eigenvalue_floor=0.2,
            max_condition_number=100.0,
            holdout_rmse_abs_tolerance=5.0e-2,
            holdout_rmse_rel_tolerance=5.0e-2,
            seed=(11, 22),
        ),
    )

    assert result.accepted is True
    assert result.status == "usable"
    assert result.precision is not None
    np.testing.assert_allclose(result.precision, true_precision, rtol=0.12, atol=0.18)
    assert result.payload()["precision_eigen_summary"]["positive"] is True
    assert result.payload()["diagnostics"]["holdout_rmse"] < 5.0e-2
    assert result.payload()["diagnostics"]["finite_sample_count"] >= 5 * (
        1 + 4 + 1 + 2
    )


def test_undersampled_regression_is_rejected() -> None:
    result = fit_low_rank_spd_quadratic_geometry(
        _quadratic_target(np.eye(3)),
        np.zeros(3),
        config=LowRankSPDQuadraticGeometryConfig(
            rank=1,
            sample_count=10,
            min_samples_per_parameter=5,
            seed=(1, 2),
        ),
    )

    assert result.accepted is False
    assert result.status == "insufficient_finite_samples"
    diagnostics = result.payload()["diagnostics"]
    assert diagnostics["finite_sample_count"] < diagnostics["required_finite_samples"]


def test_spd_and_condition_cap_are_enforced_by_construction() -> None:
    result = fit_low_rank_spd_quadratic_geometry(
        _quadratic_target(np.diag([1.0, 4.0, 9.0])),
        np.zeros(3),
        config=LowRankSPDQuadraticGeometryConfig(
            rank=2,
            sample_count=180,
            eigenvalue_floor=0.5,
            max_condition_number=3.0,
            holdout_rmse_abs_tolerance=10.0,
            seed=(3, 4),
        ),
    )

    assert result.accepted is True
    summary = result.payload()["precision_eigen_summary"]
    assert summary["positive"] is True
    assert summary["min"] >= 0.5 - 1.0e-8
    assert summary["condition_number"] <= 3.0 * (1.0 + 1.0e-6)


def test_nonfinite_values_do_not_silently_pass_sample_gate() -> None:
    def value_and_score(theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        theta = tf.reshape(tf.convert_to_tensor(theta, dtype=tf.float64), [-1])
        value = -0.5 * tf.reduce_sum(tf.square(theta))
        value = tf.where(theta[0] > 0.0, tf.constant(np.nan, dtype=tf.float64), value)
        return value, -theta

    result = fit_low_rank_spd_quadratic_geometry(
        value_and_score,
        np.zeros(2),
        config=LowRankSPDQuadraticGeometryConfig(
            rank=1,
            sample_count=20,
            min_samples_per_parameter=5,
            seed=(5, 6),
        ),
    )

    assert result.accepted is False
    assert result.status == "insufficient_finite_samples"
    diagnostics = result.payload()["diagnostics"]
    assert diagnostics["nonfinite_sample_count"] > 0


def test_bad_holdout_fit_is_rejected() -> None:
    def quartic_target(theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        theta = tf.reshape(tf.convert_to_tensor(theta, dtype=tf.float64), [-1])
        value = -tf.reduce_sum(tf.pow(theta, 4))
        score = -4.0 * tf.pow(theta, 3)
        return value, score

    result = fit_low_rank_spd_quadratic_geometry(
        quartic_target,
        np.zeros(2),
        config=LowRankSPDQuadraticGeometryConfig(
            rank=1,
            sample_count=100,
            trust_radius=1.0,
            eigenvalue_floor=0.1,
            holdout_rmse_abs_tolerance=1.0e-8,
            holdout_rmse_rel_tolerance=1.0e-8,
            seed=(7, 8),
        ),
    )

    assert result.accepted is False
    assert result.status == "holdout_fit_rejected"
    assert result.payload()["diagnostics"]["holdout_passed"] is False


def test_center_refinement_accepts_nearby_mode() -> None:
    precision = np.diag([2.0, 3.0])
    mode = np.array([0.1, -0.05])
    result = fit_low_rank_spd_quadratic_geometry(
        _quadratic_target(precision, mode=mode),
        np.zeros(2),
        config=LowRankSPDQuadraticGeometryConfig(
            rank=1,
            sample_count=160,
            trust_radius=1.0,
            eigenvalue_floor=0.2,
            max_condition_number=20.0,
            holdout_rmse_abs_tolerance=1.0e-4,
            seed=(9, 10),
        ),
    )

    assert result.accepted is True
    assert result.center_refinement_accepted is True
    assert result.refined_center is not None
    np.testing.assert_allclose(result.refined_center, mode, atol=0.08)


def test_center_refinement_rejects_out_of_trust_mode() -> None:
    precision = np.eye(2)
    mode = np.array([3.0, 0.0])
    result = fit_low_rank_spd_quadratic_geometry(
        _quadratic_target(precision, mode=mode),
        np.zeros(2),
        config=LowRankSPDQuadraticGeometryConfig(
            rank=1,
            sample_count=160,
            trust_radius=0.5,
            eigenvalue_floor=0.2,
            max_condition_number=20.0,
            holdout_rmse_abs_tolerance=1.0e-4,
            seed=(12, 13),
        ),
    )

    assert result.accepted is True
    assert result.center_refinement_accepted is False
    assert result.refined_center is None
    assert "outside_trust_radius" in result.payload()["diagnostics"]["center_refinement"]["reason"]


def test_seed_and_payload_are_deterministic() -> None:
    kwargs = {
        "value_and_score_fn": _quadratic_target(np.diag([1.5, 2.0, 3.0])),
        "center": np.zeros(3),
        "config": LowRankSPDQuadraticGeometryConfig(
            rank=2,
            sample_count=180,
            seed=(123, 456),
        ),
    }
    result_a = fit_low_rank_spd_quadratic_geometry(**kwargs)
    result_b = fit_low_rank_spd_quadratic_geometry(**kwargs)

    assert result_a.status == result_b.status
    assert result_a.payload()["diagnostics"]["artifact_hash"] == result_b.payload()["diagnostics"]["artifact_hash"]
    assert LOW_RANK_SPD_QUADRATIC_GEOMETRY_NONCLAIMS[-1] == (
        "not source-faithful Zhao-Cui evidence"
    )
