from __future__ import annotations

import math

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
import bayesfilter.highdim.sv_mixture_cut4 as sv_mixture_cut4_module
from bayesfilter.nonlinear.fixed_sgqf_tf import tf_fixed_sgqf_cloud


def _observations(dim: int) -> tf.Tensor:
    values = tf.constant(
        [
            [0.12, -0.08, 0.05],
            [-0.07, 0.11, -0.04],
        ],
        dtype=tf.float64,
    )
    return values[:, : int(dim)]


def _parameters(dim: int) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    gamma = tf.constant([0.60, 0.52, 0.47], dtype=tf.float64)[: int(dim)]
    beta = tf.constant([0.40, 0.35, 0.45], dtype=tf.float64)[: int(dim)]
    sigma = tf.constant([1.00, 0.85, 0.75], dtype=tf.float64)[: int(dim)]
    return gamma, beta, sigma


def _longer_observations(dim: int) -> tf.Tensor:
    values = tf.constant(
        [
            [0.12, -0.08, 0.05],
            [-0.07, 0.11, -0.04],
            [0.09, -0.06, 0.07],
            [-0.05, 0.10, -0.03],
        ],
        dtype=tf.float64,
    )
    return values[:, : int(dim)]


def _nearby_parameters(case_id: str, dim: int) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    if case_id == "nearby_a":
        gamma = tf.constant([0.58, 0.55, 0.50], dtype=tf.float64)
        beta = tf.constant([0.42, 0.33, 0.47], dtype=tf.float64)
        sigma = tf.constant([0.95, 0.88, 0.78], dtype=tf.float64)
        return gamma[: int(dim)], beta[: int(dim)], sigma[: int(dim)]
    if case_id == "nearby_b":
        gamma = tf.constant([0.63, 0.49, 0.44], dtype=tf.float64)
        beta = tf.constant([0.38, 0.37, 0.43], dtype=tf.float64)
        sigma = tf.constant([1.05, 0.82, 0.70], dtype=tf.float64)
        return gamma[: int(dim)], beta[: int(dim)], sigma[: int(dim)]
    raise ValueError(f"unknown nearby parameter case: {case_id}")


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _tt_config(seed: str = "p41-exact-transformed-sv") -> highdim.FixedBranchFilterConfig:
    convention = _convention()
    product_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 48)],
        convention,
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=(1, 1),
            ridge=1e-12,
            max_sweeps=2,
            sweep_order=(0,),
            row_budget=512,
            column_budget=128,
            dense_matrix_byte_budget=200_000,
            normal_matrix_byte_budget=100_000,
            condition_number_warning=1e10,
            condition_number_veto=1e14,
            holdout_tolerance=5e-4,
        ),
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.constant([0.0], dtype=tf.float64),
                matrix=tf.constant([[8.0]], dtype=tf.float64),
            ),
        ),
        measure_convention=convention,
        deterministic_seed=seed,
        product_basis=product_basis,
        initial_cores=(
            highdim.TTCore(tf.ones([1, product_basis.bases[0].basis_dim, 1], dtype=tf.float64)),
        ),
        fit_quadrature_order=141,
    )


def _native_scalar_dense_reference(
    observations: tf.Tensor,
    *,
    gamma: tf.Tensor,
    beta: tf.Tensor,
    sigma: tf.Tensor,
    order: int = 401,
    radius: float = 8.0,
) -> tf.Tensor:
    y = tf.convert_to_tensor(observations, dtype=tf.float64)
    if y.shape.rank == 1:
        y = y[:, tf.newaxis]
    if int(y.shape[1]) != 1:
        raise ValueError("scalar native dense reference requires scalar observations")
    nodes, weights = highdim.legendre_gauss_nodes_weights(order)
    x_grid = radius * nodes
    scaled_weights = radius * weights
    prior_scale = sigma / tf.sqrt(1.0 - tf.square(gamma))
    log_density = _normal_log_prob(x_grid, tf.constant(0.0, dtype=tf.float64), prior_scale)
    log_terms = []
    for time_index in range(int(y.shape[0])):
        if time_index > 0:
            previous_density = tf.exp(log_density - log_terms[-1])
            transition_log = _normal_log_prob(
                x_grid[:, tf.newaxis],
                gamma * x_grid[tf.newaxis, :],
                sigma,
            )
            predictive = tf.reduce_sum(
                scaled_weights[tf.newaxis, :] * previous_density[tf.newaxis, :] * tf.exp(transition_log),
                axis=1,
            )
            log_density = tf.math.log(predictive)
        observation_log = _normal_log_prob(
            y[time_index, 0],
            tf.zeros_like(x_grid),
            beta * tf.exp(0.5 * x_grid),
        )
        log_density = log_density + observation_log
        log_terms.append(_logsumexp_weighted(log_density, scaled_weights))
    return tf.reduce_sum(tf.stack(log_terms))


def _native_panel_dense_reference(
    observations: tf.Tensor,
    *,
    gamma: tf.Tensor,
    beta: tf.Tensor,
    sigma: tf.Tensor,
) -> tf.Tensor:
    values = []
    for axis in range(int(observations.shape[1])):
        values.append(
            _native_scalar_dense_reference(
                observations[:, axis : axis + 1],
                gamma=gamma[axis],
                beta=beta[axis],
                sigma=sigma[axis],
            )
        )
    return tf.reduce_sum(tf.stack(values))


def _normal_log_prob(value: tf.Tensor, loc: tf.Tensor, scale: tf.Tensor) -> tf.Tensor:
    return -0.5 * tf.square((value - loc) / scale) - tf.math.log(scale) - 0.5 * tf.math.log(
        tf.constant(2.0 * math.pi, dtype=tf.float64)
    )


def _logsumexp_weighted(log_values: tf.Tensor, weights: tf.Tensor) -> tf.Tensor:
    max_log = tf.reduce_max(log_values)
    return tf.math.log(tf.reduce_sum(weights * tf.exp(log_values - max_log))) + max_log


def _panel_dense_mean_variance_paths(
    result: sv_mixture_cut4_module.ExactTransformedSVPanelResult,
) -> tuple[tf.Tensor, tf.Tensor]:
    mean_path = tf.stack([coordinate.mean_path for coordinate in result.coordinate_results], axis=1)
    variance_path = tf.stack([coordinate.variance_path for coordinate in result.coordinate_results], axis=1)
    return mean_path, variance_path


def _exact_transformed_dense_and_sgqf(
    observations: tf.Tensor,
    *,
    gamma: tf.Tensor,
    beta: tf.Tensor,
    sigma: tf.Tensor,
    sparse_level: int = 2,
    order: int = 401,
    radius: float = 8.0,
) -> tuple[sv_mixture_cut4_module.ExactTransformedSVPanelResult, sv_mixture_cut4_module.ExactTransformedSVPanelFilterResult]:
    dense = highdim.exact_transformed_sv_independent_panel_dense_reference(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        order=order,
        radius=radius,
    )
    sgqf = sv_mixture_cut4_module.exact_transformed_sv_independent_panel_fixed_sgqf_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        sparse_level=sparse_level,
    )
    return dense, sgqf


def _exact_transformed_gap_summary(
    dense: sv_mixture_cut4_module.ExactTransformedSVPanelResult,
    sgqf: sv_mixture_cut4_module.ExactTransformedSVPanelFilterResult,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    dense_mean_path, dense_variance_path = _panel_dense_mean_variance_paths(dense)
    sgqf_variance_path = tf.linalg.diag_part(sgqf.covariance_path)
    sgqf_offdiag = sgqf.covariance_path - tf.linalg.diag(sgqf_variance_path)
    log_gap = tf.abs(sgqf.log_likelihood - dense.log_likelihood)
    step_gap = tf.reduce_max(tf.abs(sgqf.log_normalizers - dense.log_normalizers))
    mean_gap = tf.reduce_max(tf.abs(sgqf.mean_path - dense_mean_path))
    variance_gap = tf.reduce_max(tf.abs(sgqf_variance_path - dense_variance_path))
    offdiag_gap = tf.reduce_max(tf.abs(sgqf_offdiag))
    return log_gap, step_gap, mean_gap, variance_gap, offdiag_gap


def _actual_transformed_augmented_noise_dense_and_sgqf(
    observations: tf.Tensor,
    *,
    gamma: tf.Tensor,
    beta: tf.Tensor,
    sigma: tf.Tensor,
    sparse_level: int = 2,
    order: int = 81,
    radius: float = 7.0,
) -> tuple[highdim.ActualTransformedSVPanelFilterResult, highdim.ActualTransformedSVPanelFilterResult]:
    dense = highdim.actual_transformed_sv_independent_panel_augmented_noise_dense_gaussian_closure_reference(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        order=order,
        radius=radius,
    )
    sgqf = highdim.actual_transformed_sv_independent_panel_augmented_noise_fixed_sgqf_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        sparse_level=sparse_level,
    )
    return dense, sgqf


def _actual_transformed_augmented_noise_gap_summary(
    observations: tf.Tensor,
    dense: highdim.ActualTransformedSVPanelFilterResult,
    sgqf: highdim.ActualTransformedSVPanelFilterResult,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    del observations
    dense_variance_path = tf.linalg.diag_part(dense.covariance_path)
    sgqf_variance_path = tf.linalg.diag_part(sgqf.covariance_path)
    dense_offdiag = dense.covariance_path - tf.linalg.diag(dense_variance_path)
    sgqf_offdiag = sgqf.covariance_path - tf.linalg.diag(sgqf_variance_path)
    log_gap = tf.abs(sgqf.log_likelihood - dense.log_likelihood)
    step_gap = tf.reduce_max(tf.abs(sgqf.log_normalizers - dense.log_normalizers))
    mean_gap = tf.reduce_max(tf.abs(sgqf.mean_path - dense.mean_path))
    variance_gap = tf.reduce_max(tf.abs(sgqf_variance_path - dense_variance_path))
    offdiag_gap = tf.reduce_max(tf.abs(sgqf_offdiag - dense_offdiag))
    return log_gap, step_gap, mean_gap, variance_gap, offdiag_gap


def test_p41_exact_transform_rejects_zero_observations_and_uses_no_offset() -> None:
    transformed = highdim.exact_transformed_sv_observations(_observations(2))

    tf.debugging.assert_near(transformed, tf.math.log(tf.square(_observations(2))), atol=0.0)
    with pytest.raises(ValueError, match="nonzero"):
        highdim.exact_transformed_sv_observations(tf.constant([[0.0], [0.1]], dtype=tf.float64))


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p41_actual_transformed_augmented_noise_fixed_sgqf_lane_b_short_prefix_is_finite_and_bounded(dim: int) -> None:
    observations = _observations(dim)[:1]
    gamma, beta, sigma = _parameters(dim)
    dense, sgqf = _actual_transformed_augmented_noise_dense_and_sgqf(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        sparse_level=4,
    )
    log_gap, step_gap, mean_gap, variance_gap, offdiag_gap = _actual_transformed_augmented_noise_gap_summary(
        observations,
        dense,
        sgqf,
    )

    assert bool(tf.math.is_finite(sgqf.log_likelihood).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.log_normalizers)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.mean_path)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.covariance_path)).numpy())
    assert sgqf.diagnostics["backend"] == "fixed_sgqf_independent_panel_actual_transformed_sv_augmented_noise_gaussian_closure"
    assert sgqf.diagnostics["panel_dim"] == dim
    assert sgqf.diagnostics["target_scope"] == "actual_transformed_sv_augmented_noise_gaussian_closure_tiny_fixture"
    assert sgqf.diagnostics["fixed_sgqf_sparse_level"] == 4
    assert "not KSC Gaussian mixture approximation" in sgqf.diagnostics["non_claims"]
    assert "not exact transformed same-target admission" in sgqf.diagnostics["non_claims"]
    assert "not direct actual-SV likelihood quadrature" in sgqf.diagnostics["non_claims"]
    assert bool(tf.math.is_finite(log_gap).numpy())
    assert bool(tf.math.is_finite(step_gap).numpy())
    assert bool(tf.math.is_finite(mean_gap).numpy())
    assert bool(tf.math.is_finite(variance_gap).numpy())
    assert bool(tf.math.is_finite(offdiag_gap).numpy())

    tf.debugging.assert_less(log_gap, tf.constant(2.5e-1, dtype=tf.float64))
    tf.debugging.assert_less(step_gap, tf.constant(2.5e-1, dtype=tf.float64))
    tf.debugging.assert_less(mean_gap, tf.constant(6.0e-1, dtype=tf.float64))
    tf.debugging.assert_less(variance_gap, tf.constant(3.0e-1, dtype=tf.float64))
    tf.debugging.assert_less(offdiag_gap, tf.constant(1.0e-12, dtype=tf.float64))


def test_p41_actual_transformed_augmented_noise_fixed_sgqf_lane_b_rejects_wrong_cloud_dim() -> None:
    observations = _observations(1)[:1]
    gamma, beta, sigma = _parameters(1)
    bad_cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=2)

    with pytest.raises(ValueError, match="two-dimensional cloud"):
        highdim.actual_transformed_sv_independent_panel_augmented_noise_fixed_sgqf_filter(
            observations,
            gamma=gamma,
            beta=beta,
            sigma=sigma,
            cloud=bad_cloud,
        )


def test_p41_actual_transformed_augmented_noise_dense_lane_b_reference_matches_sgqf_on_short_prefix() -> None:
    observations = _observations(1)[:1]
    gamma, beta, sigma = _parameters(1)
    dense = highdim.actual_transformed_sv_independent_panel_augmented_noise_dense_gaussian_closure_reference(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        order=81,
        radius=7.0,
    )
    sgqf = highdim.actual_transformed_sv_independent_panel_augmented_noise_fixed_sgqf_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        sparse_level=4,
    )
    tf.debugging.assert_near(sgqf.log_likelihood, dense.log_likelihood, atol=2.5e-1, rtol=2.5e-1)
    tf.debugging.assert_near(sgqf.log_normalizers, dense.log_normalizers, atol=2.5e-1, rtol=2.5e-1)
    assert dense.diagnostics["backend"] == "dense_actual_transformed_sv_augmented_noise_gaussian_closure"
    assert dense.diagnostics["lane_id"] == "lane_b_augmented_noise_gaussian_closure"


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p41_exact_transformed_fixed_sgqf_matches_dense_on_tiny_panel(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _parameters(dim)
    dense = highdim.exact_transformed_sv_independent_panel_dense_reference(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        order=401,
        radius=8.0,
    )
    sgqf = sv_mixture_cut4_module.exact_transformed_sv_independent_panel_fixed_sgqf_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        sparse_level=2,
    )

    dense_mean_path, dense_variance_path = _panel_dense_mean_variance_paths(dense)
    sgqf_variance_path = tf.linalg.diag_part(sgqf.covariance_path)
    sgqf_offdiag = sgqf.covariance_path - tf.linalg.diag(sgqf_variance_path)
    log_gap = tf.abs(sgqf.log_likelihood - dense.log_likelihood)
    step_gap = tf.reduce_max(tf.abs(sgqf.log_normalizers - dense.log_normalizers))
    mean_gap = tf.reduce_max(tf.abs(sgqf.mean_path - dense_mean_path))
    variance_gap = tf.reduce_max(tf.abs(sgqf_variance_path - dense_variance_path))
    offdiag_gap = tf.reduce_max(tf.abs(sgqf_offdiag))

    assert bool(tf.math.is_finite(sgqf.log_likelihood).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.log_normalizers)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.mean_path)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.covariance_path)).numpy())
    assert sgqf.diagnostics["backend"] == "fixed_sgqf_independent_panel_exact_transformed_sv"
    assert sgqf.diagnostics["panel_dim"] == dim
    assert sgqf.diagnostics["transform_offset"] == 0.0
    assert sgqf.diagnostics["target_scope"] == "independent_product_exact_transformed_sv_panel_tiny_fixture"
    assert "not coupled multivariate Zhao-Cui TT" in sgqf.diagnostics["non_claims"]
    assert "no analytical score claim" in sgqf.diagnostics["non_claims"]
    assert bool(tf.math.is_finite(log_gap).numpy())
    assert bool(tf.math.is_finite(step_gap).numpy())
    assert bool(tf.math.is_finite(mean_gap).numpy())
    assert bool(tf.math.is_finite(variance_gap).numpy())
    assert bool(tf.math.is_finite(offdiag_gap).numpy())

    tf.debugging.assert_less(log_gap, tf.constant(2.0e-2, dtype=tf.float64))
    tf.debugging.assert_less(step_gap, tf.constant(2.0e-2, dtype=tf.float64))
    tf.debugging.assert_less(mean_gap, tf.constant(6.0e-2, dtype=tf.float64))
    tf.debugging.assert_less(variance_gap, tf.constant(1.5e-1, dtype=tf.float64))
    tf.debugging.assert_less(offdiag_gap, tf.constant(1.0e-12, dtype=tf.float64))


def test_p41_exact_transformed_fixed_sgqf_rejects_non_scalar_cloud() -> None:
    observations = _observations(2)
    gamma, beta, sigma = _parameters(2)
    bad_cloud = tf_fixed_sgqf_cloud(dim=2, sparse_level=2)

    with pytest.raises(ValueError, match="one-dimensional cloud"):
        sv_mixture_cut4_module.exact_transformed_sv_independent_panel_fixed_sgqf_filter(
            observations,
            gamma=gamma,
            beta=beta,
            sigma=sigma,
            cloud=bad_cloud,
        )


def test_p41_exact_transformed_fixed_sgqf_dim1_matches_scalar_dense_reference_layout() -> None:
    observations = _observations(1)
    gamma, beta, sigma = _parameters(1)
    dense, sgqf = _exact_transformed_dense_and_sgqf(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        sparse_level=4,
    )
    scalar_dense = dense.coordinate_results[0]
    sgqf_variance = tf.reshape(tf.linalg.diag_part(sgqf.covariance_path), [-1])

    assert sgqf.mean_path.shape == (int(observations.shape[0]), 1)
    assert sgqf.covariance_path.shape == (int(observations.shape[0]), 1, 1)
    assert sgqf.log_normalizers.shape == scalar_dense.log_normalizers.shape
    assert sgqf_variance.shape == scalar_dense.variance_path.shape
    tf.debugging.assert_less(tf.abs(sgqf.log_likelihood - scalar_dense.log_likelihood), tf.constant(2.0e-2, dtype=tf.float64))
    tf.debugging.assert_less(
        tf.reduce_max(tf.abs(sgqf.log_normalizers - scalar_dense.log_normalizers)),
        tf.constant(2.0e-2, dtype=tf.float64),
    )
    tf.debugging.assert_less(
        tf.reduce_max(tf.abs(tf.reshape(sgqf.mean_path, [-1]) - scalar_dense.mean_path)),
        tf.constant(6.0e-2, dtype=tf.float64),
    )
    tf.debugging.assert_less(
        tf.reduce_max(tf.abs(sgqf_variance - scalar_dense.variance_path)),
        tf.constant(1.5e-1, dtype=tf.float64),
    )


@pytest.mark.parametrize("case_id", ["nearby_a", "nearby_b"])
@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p41_exact_transformed_fixed_sgqf_nearby_parameter_ladder_matches_dense(case_id: str, dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _nearby_parameters(case_id, dim)
    dense, sgqf = _exact_transformed_dense_and_sgqf(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        sparse_level=4,
    )
    log_gap, step_gap, mean_gap, variance_gap, offdiag_gap = _exact_transformed_gap_summary(dense, sgqf)

    assert bool(tf.math.is_finite(sgqf.log_likelihood).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.log_normalizers)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.mean_path)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.covariance_path)).numpy())
    assert sgqf.diagnostics["panel_dim"] == dim
    assert sgqf.diagnostics["transform_offset"] == 0.0
    assert "no analytical score claim" in sgqf.diagnostics["non_claims"]

    tf.debugging.assert_less(log_gap, tf.constant(2.0e-2, dtype=tf.float64))
    tf.debugging.assert_less(step_gap, tf.constant(2.0e-2, dtype=tf.float64))
    tf.debugging.assert_less(mean_gap, tf.constant(8.0e-2, dtype=tf.float64))
    tf.debugging.assert_less(variance_gap, tf.constant(2.1e-1, dtype=tf.float64))
    tf.debugging.assert_less(offdiag_gap, tf.constant(1.0e-12, dtype=tf.float64))


@pytest.mark.parametrize("dim", [1, 3])
def test_p41_exact_transformed_fixed_sgqf_longer_horizon_ladder_matches_dense(dim: int) -> None:
    observations = _longer_observations(dim)
    gamma, beta, sigma = _parameters(dim)
    dense, sgqf = _exact_transformed_dense_and_sgqf(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        sparse_level=4,
    )
    log_gap, step_gap, mean_gap, variance_gap, offdiag_gap = _exact_transformed_gap_summary(dense, sgqf)

    assert bool(tf.math.is_finite(sgqf.log_likelihood).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.log_normalizers)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.mean_path)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(sgqf.covariance_path)).numpy())
    assert sgqf.diagnostics["panel_dim"] == dim
    assert sgqf.diagnostics["target_scope"] == "independent_product_exact_transformed_sv_panel_tiny_fixture"

    tf.debugging.assert_less(log_gap, tf.constant(7.0e-2, dtype=tf.float64))
    tf.debugging.assert_less(step_gap, tf.constant(3.1e-2, dtype=tf.float64))
    tf.debugging.assert_less(mean_gap, tf.constant(8.1e-2, dtype=tf.float64))
    tf.debugging.assert_less(variance_gap, tf.constant(1.7e-1, dtype=tf.float64))
    tf.debugging.assert_less(offdiag_gap, tf.constant(1.0e-12, dtype=tf.float64))


def test_p41_exact_transformed_fixed_sgqf_sparse_level_ladder_improves_on_representative_case() -> None:
    observations = _longer_observations(1)
    gamma, beta, sigma = _parameters(1)
    dense = highdim.exact_transformed_sv_independent_panel_dense_reference(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        order=401,
        radius=8.0,
    )
    level1 = sv_mixture_cut4_module.exact_transformed_sv_independent_panel_fixed_sgqf_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        sparse_level=1,
    )
    level2 = sv_mixture_cut4_module.exact_transformed_sv_independent_panel_fixed_sgqf_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        sparse_level=3,
    )
    level3 = sv_mixture_cut4_module.exact_transformed_sv_independent_panel_fixed_sgqf_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        sparse_level=4,
    )

    level1_gaps = _exact_transformed_gap_summary(dense, level1)
    level2_gaps = _exact_transformed_gap_summary(dense, level2)
    level3_gaps = _exact_transformed_gap_summary(dense, level3)

    for result in (level1, level2, level3):
        assert bool(tf.math.is_finite(result.log_likelihood).numpy())
        assert bool(tf.reduce_all(tf.math.is_finite(result.log_normalizers)).numpy())
        assert bool(tf.reduce_all(tf.math.is_finite(result.mean_path)).numpy())
        assert bool(tf.reduce_all(tf.math.is_finite(result.covariance_path)).numpy())

    tf.debugging.assert_greater(level1_gaps[0], level2_gaps[0])
    tf.debugging.assert_greater(level2_gaps[0], level3_gaps[0])
    tf.debugging.assert_greater(level1_gaps[1], level2_gaps[1])
    tf.debugging.assert_less(level3_gaps[1], tf.constant(2.0e-3, dtype=tf.float64))
    tf.debugging.assert_greater(level1_gaps[2], level2_gaps[2])
    tf.debugging.assert_less(level2_gaps[2], tf.constant(5.0e-3, dtype=tf.float64))
    tf.debugging.assert_less(level3_gaps[2], tf.constant(6.0e-3, dtype=tf.float64))
    tf.debugging.assert_greater(level1_gaps[3], level2_gaps[3])
    tf.debugging.assert_less(level2_gaps[3], tf.constant(2.0e-2, dtype=tf.float64))
    tf.debugging.assert_less(level3_gaps[3], tf.constant(2.0e-2, dtype=tf.float64))
    tf.debugging.assert_equal(level1_gaps[4], tf.constant(0.0, dtype=tf.float64))
    tf.debugging.assert_equal(level2_gaps[4], tf.constant(0.0, dtype=tf.float64))
    tf.debugging.assert_equal(level3_gaps[4], tf.constant(0.0, dtype=tf.float64))


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p41_exact_transformed_zhaocui_factorized_tt_matches_dense(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _parameters(dim)
    dense = highdim.exact_transformed_sv_independent_panel_dense_reference(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        order=401,
        radius=8.0,
    )
    tt = highdim.exact_transformed_sv_independent_panel_zhaocui_tt_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        config=_tt_config(seed=f"p41-exact-transformed-tt-dim-{dim}"),
        branch_seed_prefix=f"p41-exact-transformed-tt-dim-{dim}",
    )

    tf.debugging.assert_near(tt.log_likelihood, dense.log_likelihood, atol=2e-8, rtol=2e-8)
    tf.debugging.assert_near(tt.log_normalizers, dense.log_normalizers, atol=2e-8, rtol=2e-8)
    assert dense.diagnostics["transform_offset"] == 0.0
    assert tt.diagnostics["transform_offset"] == 0.0
    assert tt.diagnostics["panel_dim"] == dim
    assert tt.diagnostics["backend"] == "factorized_scalar_zhaocui_tt_exact_transformed_sv"
    assert "not coupled multivariate Zhao-Cui TT" in tt.diagnostics["non_claims"]


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p41_raw_native_sv_matches_exact_transformed_dense_after_jacobian(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _parameters(dim)
    exact_transformed = highdim.exact_transformed_sv_independent_panel_dense_reference(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        order=401,
        radius=8.0,
    )
    native = _native_panel_dense_reference(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    )
    jacobian = highdim.exact_transformed_sv_jacobian_log_abs_det(observations)

    tf.debugging.assert_near(native, exact_transformed.log_likelihood - jacobian, atol=2e-8, rtol=2e-8)


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p41_ksc_mixture_cut4_and_kalman_are_approximation_comparators(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _parameters(dim)
    exact_transformed = highdim.exact_transformed_sv_independent_panel_dense_reference(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        order=401,
        radius=8.0,
    )
    ksc_kalman = highdim.independent_panel_sv_mixture_kalman_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    )
    ksc_cut4 = highdim.independent_panel_sv_mixture_cut4_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    )
    mixture_gap = ksc_kalman.log_likelihood - exact_transformed.log_likelihood

    assert bool(tf.math.is_finite(mixture_gap).numpy())
    tf.debugging.assert_near(ksc_cut4.log_likelihood, ksc_kalman.log_likelihood, atol=2e-6, rtol=2e-6)
    assert abs(float(mixture_gap.numpy())) > 0.0
    assert "not exact native SV likelihood" in ksc_kalman.diagnostics["non_claims"]
    assert "linear-Gaussian component fixtures do not validate nonlinear CUT4 accuracy" in ksc_cut4.diagnostics[
        "non_claims"
    ]


def test_p41_exports_are_highdim_scoped() -> None:
    assert "ExactTransformedSVSSM" in highdim.__all__
    assert "exact_transformed_sv_independent_panel_zhaocui_tt_filter" in highdim.__all__
    assert "exact_transformed_sv_observations" in highdim.__all__
    import bayesfilter

    assert not hasattr(bayesfilter, "ExactTransformedSVSSM")
