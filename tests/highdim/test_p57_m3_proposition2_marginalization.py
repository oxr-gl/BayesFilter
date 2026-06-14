from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _product_basis(degrees: tuple[int, ...]) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree) for degree in degrees],
        _convention(),
    )


def _identity(
    ftt: highdim.FunctionalTT,
    defensive: highdim.TensorProductReferenceDensity,
    tau: float,
) -> highdim.BranchIdentity:
    return highdim.SquaredTTDensity.expected_branch_identity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(tau, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
    )


def _density(tau: float = 0.25) -> highdim.SquaredTTDensity:
    product = _product_basis((1, 1))
    core0 = highdim.TTCore(tf.constant([[[1.0, 0.35], [0.2, -0.15]]], dtype=tf.float64))
    core1 = highdim.TTCore(tf.constant([[[1.1], [0.25]], [[-0.4], [0.8]]], dtype=tf.float64))
    ftt = highdim.FunctionalTT([core0, core1], product, _convention())
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    return highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(tau, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=_identity(ftt, defensive, tau),
    )


def test_p57_m3_prefix_marginal_matches_independent_dense_grid() -> None:
    density = _density(tau=0.1)
    marginal = density.marginal_density([0])
    grid = tf.linspace(tf.constant(-1.0, dtype=tf.float64), tf.constant(1.0, dtype=tf.float64), 401)
    retained = tf.constant([[-0.75], [-0.1], [0.4], [0.9]], dtype=tf.float64)

    actual = marginal.normalized_retained_density_values(retained)
    dense_rows = []
    for x0 in tf.unstack(retained[:, 0]):
        full_points = tf.stack([tf.fill(tf.shape(grid), x0), grid], axis=1)
        values = tf.exp(density.log_density(full_points))
        dense_rows.append(0.5 * highdim.trapezoid_integral(grid, values))
    dense = tf.stack(dense_rows)

    assert marginal.diagnostics["semantics"] == "source_style_squared_tt_marginal"
    tf.debugging.assert_near(actual, dense, atol=5e-5)


def test_p57_m3_suffix_marginal_matches_independent_dense_grid() -> None:
    density = _density(tau=0.1)
    marginal = density.marginal_density([1])
    grid = tf.linspace(tf.constant(-1.0, dtype=tf.float64), tf.constant(1.0, dtype=tf.float64), 401)
    retained = tf.constant([[-0.8], [0.0], [0.55]], dtype=tf.float64)

    actual = marginal.normalized_retained_density_values(retained)
    dense_rows = []
    for x1 in tf.unstack(retained[:, 0]):
        full_points = tf.stack([grid, tf.fill(tf.shape(grid), x1)], axis=1)
        values = tf.exp(density.log_density(full_points))
        dense_rows.append(0.5 * highdim.trapezoid_integral(grid, values))
    dense = tf.stack(dense_rows)

    tf.debugging.assert_near(actual, dense, atol=5e-5)


def test_p57_m3_non_prefix_suffix_marginal_is_not_promoted() -> None:
    product = _product_basis((0, 0, 0))
    ftt = highdim.FunctionalTT(
        [
            highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64)),
            highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64)),
            highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64)),
        ],
        product,
        _convention(),
    )
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    density = highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=_identity(ftt, defensive, 0.0),
    )

    with pytest.raises(NotImplementedError, match="retained prefix or suffix"):
        density.marginal_density([0, 2])
