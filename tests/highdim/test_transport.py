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


def _product_basis(dimension: int) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 0)
            for _ in range(dimension)
        ],
        _convention(),
    )


def _density(dimension: int) -> highdim.SquaredTTDensity:
    product = _product_basis(dimension)
    cores = []
    for _ in range(dimension):
        cores.append(highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64)))
    ftt = highdim.FunctionalTT(cores, product, _convention())
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    branch_identity = highdim.SquaredTTDensity.expected_branch_identity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
    )
    return highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=branch_identity,
    )


def _transport(dimension: int) -> highdim.KRTransport:
    return highdim.KRTransport(
        density=_density(dimension),
        coordinate_order=tuple(range(dimension)),
        cdf_config=highdim.KRCDFConfig(
            grid_size=129,
            bisection_steps=24,
            monotonicity_tolerance=1e-12,
            bracket_tolerance=1e-12,
            denominator_floor=1e-12,
            max_floor_count=0,
        ),
    )


def test_one_dimensional_cdf_inverse_round_trip():
    transport = _transport(1)
    z = tf.constant([[-0.5], [0.0], [0.5]], dtype=tf.float64)
    u, log_det, forward_results = transport.forward(z)
    z_round, inverse_log_det, inverse_results = transport.inverse(u)

    tf.debugging.assert_near(u[:, 0], tf.constant([0.25, 0.5, 0.75], dtype=tf.float64), atol=2e-3)
    tf.debugging.assert_near(z_round, z, atol=2e-4)
    tf.debugging.assert_near(
        log_det,
        tf.fill([3], tf.math.log(tf.constant(0.5, dtype=tf.float64))),
        atol=1e-12,
    )
    tf.debugging.assert_near(
        inverse_log_det,
        tf.fill([3], tf.math.log(tf.constant(2.0, dtype=tf.float64))),
        atol=1e-12,
    )
    assert all(result.status is highdim.HighDimStatus.OK for result in forward_results)
    assert all(result.status is highdim.HighDimStatus.OK for result in inverse_results)


def test_separable_density_gives_independent_kr_maps():
    transport = _transport(2)
    z = tf.constant([[-0.5, 0.25]], dtype=tf.float64)
    u, _, _ = transport.forward(z)

    tf.debugging.assert_near(u, tf.constant([[0.25, 0.625]], dtype=tf.float64), atol=2e-3)


def test_kr_jacobian_identity_matches_log_conditional_sum():
    transport = _transport(2)
    z = tf.constant([[0.1, -0.3], [0.4, 0.7]], dtype=tf.float64)
    _, log_det, _ = transport.forward(z)

    tf.debugging.assert_near(transport.log_jacobian(z), log_det, atol=0.0)
    tf.debugging.assert_near(
        log_det,
        tf.fill([2], tf.math.log(tf.constant(0.25, dtype=tf.float64))),
        atol=1e-12,
    )


def test_bracket_failure_returns_veto_status():
    transport = _transport(1)
    _, _, results = transport.inverse(tf.constant([[1.2]], dtype=tf.float64))

    assert results[0].status is highdim.HighDimStatus.INVERSE_BRACKET_FAILURE


def test_transport_rejects_non_natural_coordinate_order():
    with pytest.raises(NotImplementedError, match="natural"):
        highdim.KRTransport(
            density=_density(2),
            coordinate_order=(1, 0),
            cdf_config=highdim.KRCDFConfig(
                grid_size=9,
                bisection_steps=4,
                monotonicity_tolerance=1e-12,
                bracket_tolerance=1e-12,
                denominator_floor=1e-12,
                max_floor_count=0,
            ),
        )


def test_transport_rejects_nonfinite_inputs():
    transport = _transport(1)

    with pytest.raises(ValueError, match=highdim.HighDimStatus.NONFINITE_VALUE.value):
        transport.forward(tf.constant([[float("nan")]], dtype=tf.float64))

    with pytest.raises(ValueError, match=highdim.HighDimStatus.NONFINITE_VALUE.value):
        transport.inverse(tf.constant([[float("nan")]], dtype=tf.float64))


def test_transport_cdf_path_reports_nonfinite_status():
    transport = _transport(1)
    _, _, status, _ = transport._cdf_at(
        0,
        tf.zeros([1, 0], dtype=tf.float64),
        tf.constant([float("nan")], dtype=tf.float64),
    )

    assert status is highdim.HighDimStatus.NONFINITE_VALUE
