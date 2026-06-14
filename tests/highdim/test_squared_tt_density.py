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


def _branch_identity(
    ftt: highdim.FunctionalTT,
    defensive_density: highdim.TensorProductReferenceDensity,
    tau: float = 0.0,
    normalizer_floor: float = 1e-12,
    denominator_floor: float = 1e-12,
) -> highdim.BranchIdentity:
    return highdim.SquaredTTDensity.expected_branch_identity(
        sqrt_tt=ftt,
        defensive_density=defensive_density,
        tau=tf.constant(tau, dtype=tf.float64),
        normalizer_floor=tf.constant(normalizer_floor, dtype=tf.float64),
        denominator_floor=tf.constant(denominator_floor, dtype=tf.float64),
        measure_convention=_convention(),
    )


def _constant_density(value: float = 1.0, tau: float = 0.0) -> highdim.SquaredTTDensity:
    product = _product_basis((0,))
    ftt = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[value]]], dtype=tf.float64))],
        product,
        _convention(),
    )
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    return highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(tau, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=_branch_identity(ftt, defensive, tau=tau),
    )


def test_constant_sqrt_tt_normalizes_to_one():
    density = _constant_density(1.0)
    points = tf.constant([[-0.5], [0.0], [0.75]], dtype=tf.float64)

    tf.debugging.assert_near(density.normalizer(), tf.constant(1.0, dtype=tf.float64), atol=0.0)
    tf.debugging.assert_near(
        tf.exp(density.log_density(points)),
        tf.ones([3], dtype=tf.float64),
        atol=1e-12,
    )


def test_pair_core_square_contraction_matches_dense_quadrature():
    product = _product_basis((1, 1))
    core0 = highdim.TTCore(tf.constant([[[1.0, 0.0], [0.0, 0.5]]], dtype=tf.float64))
    core1 = highdim.TTCore(tf.constant([[[1.0], [0.25]], [[0.75], [0.5]]], dtype=tf.float64))
    ftt = highdim.FunctionalTT([core0, core1], product, _convention())
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    density = highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=_branch_identity(ftt, defensive),
    )

    grid = tf.linspace(tf.constant(-1.0, dtype=tf.float64), tf.constant(1.0, dtype=tf.float64), 201)
    z0, z1 = tf.meshgrid(grid, grid, indexing="ij")
    points = tf.stack([tf.reshape(z0, [-1]), tf.reshape(z1, [-1])], axis=1)
    values = tf.reshape(tf.square(ftt.evaluate(points)), [201, 201])
    widths = grid[1:] - grid[:-1]
    inner = tf.reduce_sum(0.5 * (values[:, 1:] + values[:, :-1]) * widths[tf.newaxis, :], axis=1)
    dense = tf.reduce_sum(0.5 * (inner[1:] + inner[:-1]) * widths) / 4.0

    tf.debugging.assert_near(density.sqrt_square_normalizer(), dense, atol=3e-4)


def test_nonuniform_reference_missing_weight_trap_fails():
    product = _product_basis((0,))
    ftt = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64))],
        product,
        _convention(),
    )
    mismatched = highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_LEBESGUE,
        mass_measure=highdim.MassMeasure.REFERENCE_LEBESGUE,
        reference_weight_name="omega",
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.MEASURE_MISMATCH.value):
        highdim.SquaredTTDensity(
            sqrt_tt=ftt,
            defensive_density=highdim.TensorProductReferenceDensity(product, _convention()),
            tau=tf.constant(0.0, dtype=tf.float64),
            normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
            denominator_floor=tf.constant(1e-12, dtype=tf.float64),
            measure_convention=mismatched,
            branch_identity=_branch_identity(ftt, highdim.TensorProductReferenceDensity(product, _convention())),
        )


def test_defensive_density_rescues_declared_zero_corner():
    density = _constant_density(0.0, tau=0.25)
    points = tf.constant([[0.0]], dtype=tf.float64)

    tf.debugging.assert_near(density.normalizer(), tf.constant(0.25, dtype=tf.float64), atol=1e-12)
    tf.debugging.assert_near(tf.exp(density.log_density(points)), tf.ones([1], dtype=tf.float64), atol=1e-12)


def test_marginal_contraction_matches_dense_2d_reference():
    product = _product_basis((0, 0))
    ftt = highdim.FunctionalTT(
        [
            highdim.TTCore(tf.constant([[[2.0]]], dtype=tf.float64)),
            highdim.TTCore(tf.constant([[[3.0]]], dtype=tf.float64)),
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
        branch_identity=_branch_identity(ftt, defensive),
    )

    marginal = density.marginal_density([0])

    assert marginal.keep_axes == (0,)
    tf.debugging.assert_near(marginal.normalizer, tf.constant(36.0, dtype=tf.float64), atol=1e-12)
    assert marginal.branch_identity == marginal.contracted_density.branch_identity


def test_conditional_density_integrates_to_one_on_grid():
    density = _constant_density(1.0)
    grid = tf.linspace(tf.constant(-1.0, dtype=tf.float64), tf.constant(1.0, dtype=tf.float64), 101)
    conditional = density.conditional_density(0, tf.zeros([1, 0], dtype=tf.float64), grid)
    integral = tf.reduce_sum(0.5 * (conditional[1:] + conditional[:-1]) * (grid[1:] - grid[:-1]))

    tf.debugging.assert_near(integral, tf.constant(1.0, dtype=tf.float64), atol=1e-12)


def test_conditional_density_integrates_suffix_coordinates():
    product = _product_basis((1, 1))
    core0 = highdim.TTCore(tf.constant([[[1.0, 0.0], [0.0, 0.8]]], dtype=tf.float64))
    core1 = highdim.TTCore(tf.constant([[[1.0], [0.0]], [[0.0], [0.6]]], dtype=tf.float64))
    ftt = highdim.FunctionalTT([core0, core1], product, _convention())
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    density = highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=_branch_identity(ftt, defensive),
    )
    grid = tf.linspace(tf.constant(-1.0, dtype=tf.float64), tf.constant(1.0, dtype=tf.float64), 101)
    conditional = density.conditional_density(0, tf.zeros([1, 0], dtype=tf.float64), grid)
    slice_points = tf.stack([grid, tf.zeros_like(grid)], axis=1)
    slice_values = tf.exp(density.log_density(slice_points))
    slice_integral = tf.reduce_sum(
        0.5 * (slice_values[1:] + slice_values[:-1]) * (grid[1:] - grid[:-1])
    )
    slice_conditional = slice_values / slice_integral

    assert tf.reduce_max(tf.abs(conditional - slice_conditional)).numpy() > 1e-2
