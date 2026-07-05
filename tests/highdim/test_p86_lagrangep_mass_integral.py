from __future__ import annotations

import tensorflow as tf

import bayesfilter.highdim as highdim


def test_p86_order1_one_element_matches_closed_form_micro_baseline() -> None:
    basis = highdim.LagrangePiecewiseBasis1D(highdim.AlgebraicMap(1.0), 1, 1)

    expected_lebesgue_mass = tf.constant(
        [[2.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, 2.0 / 3.0]],
        dtype=tf.float64,
    )
    expected_measure_mass = expected_lebesgue_mass / 2.0
    expected_lebesgue_integral = tf.constant([1.0, 1.0], dtype=tf.float64)
    expected_measure_integral = expected_lebesgue_integral / 2.0

    tf.debugging.assert_near(
        basis.mass_matrix(highdim.MassMeasure.REFERENCE_LEBESGUE),
        expected_lebesgue_mass,
    )
    tf.debugging.assert_near(
        basis.mass_matrix(highdim.MassMeasure.REFERENCE_MEASURE),
        expected_measure_mass,
    )
    tf.debugging.assert_near(
        basis.integral_vector(highdim.MassMeasure.REFERENCE_LEBESGUE),
        expected_lebesgue_integral,
    )
    tf.debugging.assert_near(
        basis.integral_vector(highdim.MassMeasure.REFERENCE_MEASURE),
        expected_measure_integral,
    )


def test_p86_lagrangep_mass_is_symmetric_positive_definite_for_author_setup() -> None:
    basis = highdim.LagrangePiecewiseBasis1D(highdim.AlgebraicMap(1.0), 4, 8)
    mass = basis.mass_matrix(highdim.MassMeasure.REFERENCE_MEASURE)
    eigenvalues = tf.linalg.eigvalsh(mass)

    assert mass.shape == (33, 33)
    tf.debugging.assert_near(mass, tf.transpose(mass), atol=1e-12)
    tf.debugging.assert_positive(eigenvalues)


def test_p86_lagrangep_integral_vector_integrates_partition_of_unity() -> None:
    basis = highdim.LagrangePiecewiseBasis1D(highdim.AlgebraicMap(1.0), 4, 8)
    reference_nodes = tf.linspace(
        tf.constant(-1.0, dtype=tf.float64),
        tf.constant(1.0, dtype=tf.float64),
        17,
    )
    physical_nodes = basis.domain.from_reference(reference_nodes)
    basis_values = basis.evaluate(physical_nodes)
    integral = basis.integral_vector(highdim.MassMeasure.REFERENCE_MEASURE)
    lebesgue_integral = basis.integral_vector(highdim.MassMeasure.REFERENCE_LEBESGUE)

    tf.debugging.assert_near(
        tf.reduce_sum(basis_values, axis=1),
        tf.ones([17], dtype=tf.float64),
        atol=1e-12,
    )
    tf.debugging.assert_near(tf.reduce_sum(integral), tf.constant(1.0, dtype=tf.float64))
    tf.debugging.assert_near(
        tf.reduce_sum(lebesgue_integral),
        tf.constant(2.0, dtype=tf.float64),
    )


def test_p86_lagrangep_bounded_interval_lebesgue_scales_with_interval_length() -> None:
    reference = highdim.LagrangePiecewiseBasis1D(highdim.BoundedInterval(-1.0, 1.0), 1, 1)
    stretched = highdim.LagrangePiecewiseBasis1D(highdim.BoundedInterval(2.0, 6.0), 1, 1)

    tf.debugging.assert_near(
        stretched.mass_matrix(highdim.MassMeasure.REFERENCE_LEBESGUE),
        2.0 * reference.mass_matrix(highdim.MassMeasure.REFERENCE_LEBESGUE),
    )
    tf.debugging.assert_near(
        stretched.mass_matrix(highdim.MassMeasure.REFERENCE_MEASURE),
        reference.mass_matrix(highdim.MassMeasure.REFERENCE_MEASURE),
    )
    tf.debugging.assert_near(
        stretched.integral_vector(highdim.MassMeasure.REFERENCE_LEBESGUE),
        2.0 * reference.integral_vector(highdim.MassMeasure.REFERENCE_LEBESGUE),
    )
    tf.debugging.assert_near(
        stretched.integral_vector(highdim.MassMeasure.REFERENCE_MEASURE),
        reference.integral_vector(highdim.MassMeasure.REFERENCE_MEASURE),
    )


def test_p86_legendre_mass_and_integral_behavior_is_unchanged() -> None:
    basis = highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 4)

    tf.debugging.assert_equal(
        basis.mass_matrix(highdim.MassMeasure.REFERENCE_MEASURE),
        tf.eye(5, dtype=tf.float64),
    )
    tf.debugging.assert_equal(
        basis.integral_vector(highdim.MassMeasure.REFERENCE_MEASURE),
        tf.constant([1.0, 0.0, 0.0, 0.0, 0.0], dtype=tf.float64),
    )
