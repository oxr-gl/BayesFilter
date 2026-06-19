from __future__ import annotations

from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter.highdim import stochastic_density_training as p75
from bayesfilter.highdim import ukf_initializer as p76
from bayesfilter.highdim.ukf_scout import P52_UKF_SCOUT_CLAIM, UKFScoutResult


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _basis(dimension: int, degree: int = 2) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree)
            for _ in range(dimension)
        ],
        _convention(),
    )


def _scout() -> UKFScoutResult:
    mean_path = tf.constant([[1.0, 2.0], [3.0, 4.0]], dtype=tf.float64)
    covariance_path = tf.constant(
        [
            [[1.0, 0.1], [0.1, 2.0]],
            [[3.0, 0.2], [0.2, 4.0]],
        ],
        dtype=tf.float64,
    )
    return UKFScoutResult(
        dimension=2,
        compartments=1,
        horizon=1,
        sigma_point_count=5,
        mean_path=mean_path,
        covariance_path=covariance_path,
        scale_path=tf.sqrt(tf.linalg.diag_part(covariance_path)),
        covariance_eigenvalues=tf.linalg.eigvalsh(covariance_path),
        effective_dimension_path=tf.constant([2, 2], dtype=tf.int32),
        max_abs_correlation_path=tf.constant([0.1, 0.1], dtype=tf.float64),
        process_covariance_shape=(2, 2),
        process_covariance_diagonal_range=(1.0, 1.0),
        observation_covariance_shape=(1, 1),
        observation_covariance_diagonal_range=(1.0, 1.0),
        initial_covariance_shape=(2, 2),
        initial_covariance_diagonal_range=(1.0, 2.0),
        status="PASS_P52_UKF_SCOUT",
        claim_class=P52_UKF_SCOUT_CLAIM,
        nonclaims=(
            "scout_not_truth",
            "no filtering correctness",
            "no exact likelihood",
            "no HMC readiness",
        ),
    )


def test_adjacent_moments_use_time_one_and_path_zero_previous_block() -> None:
    moments = p76.p76_adjacent_moments_from_scout(_scout(), time_index=1)

    expected_center = tf.constant([3.0, 4.0, 1.0, 2.0], dtype=tf.float64)
    expected_covariance = tf.constant(
        [
            [3.0, 0.2, 0.0, 0.0],
            [0.2, 4.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.1],
            [0.0, 0.0, 0.1, 2.0],
        ],
        dtype=tf.float64,
    )

    tf.debugging.assert_near(moments.center, expected_center)
    tf.debugging.assert_near(moments.covariance, expected_covariance)
    assert moments.previous_time_index == 0
    assert moments.claim_class == "scout_not_truth"


def test_covariance_stabilization_floors_tiny_negative_eigenvalue() -> None:
    stabilized = p76.p76_stabilize_covariance(
        tf.constant([[-1e-12, 0.0], [0.0, 2.0]], dtype=tf.float64),
        abs_floor=1e-9,
        rel_floor=1e-8,
    )

    assert float(stabilized.eigen_floor.numpy()) == pytest.approx(2e-8)
    assert bool(tf.reduce_all(stabilized.floored_eigenvalues > 0.0).numpy())
    assert bool(tf.reduce_all(tf.linalg.eigvalsh(stabilized.covariance) > 0.0).numpy())


def test_degree_one_basis_is_rejected_for_curvature_initializer() -> None:
    with pytest.raises(ValueError, match="degree"):
        p76.P76UKFInitializerConfig(
            product_basis=_basis(4, degree=1),
            ranks=(1, 1, 1, 1, 1),
        )


def test_degree_two_rank_one_initializer_returns_finite_core_shapes() -> None:
    config = p76.P76UKFInitializerConfig(
        product_basis=_basis(4, degree=2),
        ranks=(1, 1, 1, 1, 1),
        quadrature_order=16,
    )

    result = p76.p76_build_ukf_initializer(_scout(), config)

    assert len(result.cores) == 4
    assert [tuple(core.values.shape) for core in result.cores] == [
        (1, 3, 1),
        (1, 3, 1),
        (1, 3, 1),
        (1, 3, 1),
    ]
    assert all(bool(tf.reduce_all(tf.math.is_finite(core.values)).numpy()) for core in result.cores)


def test_rank_four_embedding_returns_finite_seeded_core_shapes() -> None:
    coefficients = (
        tf.constant([1.0, 0.0, -0.1], dtype=tf.float64),
        tf.constant([0.9, 0.0, -0.2], dtype=tf.float64),
        tf.constant([0.8, 0.0, -0.3], dtype=tf.float64),
    )

    cores = p76.p76_embed_rank_one_with_seeded_channels(
        coefficients,
        ranks=(1, 4, 4, 1),
        seed_epsilon=1e-6,
    )

    assert [tuple(core.values.shape) for core in cores] == [
        (1, 3, 4),
        (4, 3, 4),
        (4, 3, 1),
    ]
    assert all(bool(tf.reduce_all(tf.math.is_finite(core.values)).numpy()) for core in cores)
    assert float(tf.reduce_sum(tf.abs(cores[0].values[:, :, 1:])).numpy()) > 0.0


def test_manifest_records_nonclaims_and_no_forbidden_data_use() -> None:
    config = p76.P76UKFInitializerConfig(
        product_basis=_basis(4, degree=2),
        ranks=(1, 2, 2, 2, 1),
        quadrature_order=16,
    )

    result = p76.p76_build_ukf_initializer(_scout(), config)
    manifest = dict(result.manifest)

    assert manifest["initializer_rule"] == p76.P76_UKF_INITIALIZER_RULE
    assert manifest["claim_class"] == "scout_not_truth"
    assert manifest["source_route_prefit_used"] is False
    assert manifest["audit_data_used"] is False
    assert manifest["default_behavior_changed"] is False
    assert "not HMC readiness evidence" in manifest["nonclaims"]


def test_initializer_cores_instantiate_trainable_tt_with_finite_density_values() -> None:
    product_basis = _basis(4, degree=2)
    config = p76.P76UKFInitializerConfig(
        product_basis=product_basis,
        ranks=(1, 2, 2, 2, 1),
        quadrature_order=16,
    )
    result = p76.p76_build_ukf_initializer(_scout(), config)
    trainer_config = p75.P75TrainableTTConfig(
        product_basis=product_basis,
        ranks=config.ranks,
        tau=tf.constant(1e-6, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-14, dtype=tf.float64),
        denominator_floor=tf.constant(1e-300, dtype=tf.float64),
    )
    trainer = p75.TrainableFunctionalTT(trainer_config, initial_cores=result.cores)
    points = tf.constant(
        [
            [0.0, 0.0, 0.0, 0.0],
            [0.25, -0.25, 0.50, -0.50],
        ],
        dtype=tf.float64,
    )

    rho = trainer.rho_theta(points)
    log_density = trainer.log_density(points)

    assert bool(tf.reduce_all(tf.math.is_finite(rho)).numpy())
    assert bool(tf.math.is_finite(trainer.normalizer()).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(log_density)).numpy())


def test_downstream_objective_batch_still_rejects_audit_records() -> None:
    points = tf.zeros([2, 4], dtype=tf.float64)
    with pytest.raises(ValueError, match="audit role"):
        p75.P75ObjectiveBatch(
            points=points,
            target_values=tf.ones([2], dtype=tf.float64),
            weights=tf.ones([2], dtype=tf.float64),
            point_records=(
                {"point_id": "a0", "cloud_hash": "audit-cloud", "role": "audit"},
                {"point_id": "a1", "cloud_hash": "fit-cloud", "role": "fit"},
            ),
        )


def test_initializer_module_has_no_failed_method_call_names() -> None:
    source = (Path(__file__).resolve().parents[2] / "bayesfilter/highdim/ukf_initializer.py").read_text()
    forbidden = (
        "_".join(["square", "root", "prefit"]),
        "_".join(["source", "guided", "prefit"]),
        "source-route" + " prefit",
    )

    for text in forbidden:
        assert text not in source
