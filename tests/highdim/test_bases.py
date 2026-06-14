from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


def _basis(max_degree: int = 5) -> highdim.LegendreBasis1D:
    return highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), max_degree)


def _reference_convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def test_legendre_basis_dim_is_max_degree_plus_one():
    assert _basis(0).basis_dim == 1
    assert _basis(5).basis_dim == 6


def test_normalized_legendre_reference_mass_identity_degrees_0_to_5():
    basis = _basis(5)
    mass = basis.mass_matrix(highdim.MassMeasure.REFERENCE_MEASURE)

    tf.debugging.assert_equal(mass, tf.eye(6, dtype=tf.float64))


def test_legendre_lebesgue_mass_has_interval_length_factor():
    basis = highdim.LegendreBasis1D(highdim.BoundedInterval(2.0, 5.0), 3)
    mass = basis.mass_matrix(highdim.MassMeasure.REFERENCE_LEBESGUE)

    tf.debugging.assert_equal(mass, 3.0 * tf.eye(4, dtype=tf.float64))


def test_integral_vector_is_unit_constant_under_reference_measure():
    integral = _basis(4).integral_vector(highdim.MassMeasure.REFERENCE_MEASURE)

    tf.debugging.assert_equal(
        integral,
        tf.constant([1.0, 0.0, 0.0, 0.0, 0.0], dtype=tf.float64),
    )


def test_basis_derivative_matches_finite_difference():
    basis = _basis(4)
    points = tf.constant([-0.4, 0.2, 0.7], dtype=tf.float64)
    h = tf.constant(1e-6, dtype=tf.float64)
    centered = (basis.evaluate(points + h) - basis.evaluate(points - h)) / (2.0 * h)

    tf.debugging.assert_near(basis.derivative(points), centered, atol=1e-5)


def test_product_basis_rejects_mixed_measure_conventions():
    convention = highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_LEBESGUE,
        reference_weight_name="omega",
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.MEASURE_MISMATCH.value):
        highdim.ProductBasis([_basis(1)], convention)


def test_invalid_interval_and_negative_degree_fail():
    with pytest.raises(ValueError, match="right"):
        highdim.BoundedInterval(1.0, 1.0)
    with pytest.raises(ValueError, match="max_degree"):
        highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), -1)


def test_product_basis_axis_evaluation_shape():
    product = highdim.ProductBasis([_basis(2), _basis(1)], _reference_convention())
    values = product.evaluate_axis(0, tf.constant([0.0, 0.5], dtype=tf.float64))

    assert values.shape == (2, 3)
