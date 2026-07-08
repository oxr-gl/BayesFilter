from __future__ import annotations

import math

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


def _reference_convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def test_p86_algebraic_map_jacobian_log_density_directions() -> None:
    scale = tf.constant(2.0, dtype=tf.float64)
    mapping = highdim.AlgebraicMap(scale)
    points = tf.constant([-3.0, -0.5, 0.0, 0.5, 3.0], dtype=tf.float64)
    reference = mapping.to_reference(points)
    scaled = points / scale

    expected_reference = scaled / tf.sqrt(1.0 + tf.square(scaled))
    expected_log_dzdx = -1.5 * tf.math.log1p(tf.square(scaled)) - tf.math.log(scale)
    expected_log_dxdz = -1.5 * tf.math.log(1.0 - tf.square(reference)) + tf.math.log(scale)

    tf.debugging.assert_near(reference, expected_reference)
    tf.debugging.assert_near(mapping.from_reference(reference), points)
    tf.debugging.assert_near(mapping.domain_to_reference_log_density(points), expected_log_dzdx)
    tf.debugging.assert_near(
        mapping.reference_to_domain_log_density(reference),
        expected_log_dxdz,
    )
    tf.debugging.assert_near(
        mapping.domain_to_reference_log_density(points)
        + mapping.reference_to_domain_log_density(reference),
        tf.zeros_like(points),
    )


def test_p86_physical_to_reference_density_identity_on_gaussian_fixture() -> None:
    mapping = highdim.AlgebraicMap(1.5)
    reference = tf.constant([-0.75, -0.25, 0.25, 0.75], dtype=tf.float64)
    physical = mapping.from_reference(reference)
    log_two_pi = tf.constant(math.log(2.0 * math.pi), dtype=tf.float64)

    log_p_x = -0.5 * tf.square(physical) - 0.5 * log_two_pi
    log_p_z = log_p_x + mapping.reference_to_domain_log_density(reference)
    recovered_log_p_x = log_p_z + mapping.domain_to_reference_log_density(physical)

    tf.debugging.assert_near(recovered_log_p_x, log_p_x, atol=1e-12)


def test_p86_reference_to_physical_density_identity_on_gaussian_fixture() -> None:
    mapping = highdim.AlgebraicMap(0.75)
    physical = tf.constant([-2.0, -0.25, 0.25, 2.0], dtype=tf.float64)
    reference = mapping.to_reference(physical)
    log_two_pi = tf.constant(math.log(2.0 * math.pi), dtype=tf.float64)

    log_p_z = -0.5 * tf.square(reference) - 0.5 * log_two_pi
    log_p_x = log_p_z + mapping.domain_to_reference_log_density(physical)
    recovered_log_p_z = log_p_x + mapping.reference_to_domain_log_density(reference)

    tf.debugging.assert_near(recovered_log_p_z, log_p_z, atol=1e-12)


def test_p86_author_manifest_preserves_algebraic_measure_names() -> None:
    spec = highdim.p85_author_sir_lagrangep_algebraic_product_basis_spec(
        dimension=2,
        convention=_reference_convention(),
    )
    payload = spec.manifest_payload()

    assert payload["basis_family"] == ("lagrangep", "lagrangep")
    assert payload["domain_map_family"] == ("algebraic", "algebraic")
    assert payload["convention"]["density_measure"] == "REFERENCE_MEASURE"
    assert payload["convention"]["mass_measure"] == "REFERENCE_MEASURE"
    assert payload["convention"]["physical_coordinate_name"] == "r"
    assert payload["convention"]["reference_coordinate_name"] == "z"
    assert payload["axis_specs"][0]["domain_map"]["scale"] == 1.0
    assert "no fitting evidence" in payload["nonclaims"]


def test_p86_mixed_reference_conventions_remain_rejected() -> None:
    convention = highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_LEBESGUE,
        reference_weight_name="omega",
    )
    basis = highdim.LagrangePiecewiseBasis1D(highdim.AlgebraicMap(1.0), 1, 1)

    with pytest.raises(ValueError, match=highdim.HighDimStatus.MEASURE_MISMATCH.value):
        highdim.ProductBasis([basis], convention)
