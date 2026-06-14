from __future__ import annotations

import math

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


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


def test_p41_exact_transform_rejects_zero_observations_and_uses_no_offset() -> None:
    transformed = highdim.exact_transformed_sv_observations(_observations(2))

    tf.debugging.assert_near(transformed, tf.math.log(tf.square(_observations(2))), atol=0.0)
    with pytest.raises(ValueError, match="nonzero"):
        highdim.exact_transformed_sv_observations(tf.constant([[0.0], [0.1]], dtype=tf.float64))


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
