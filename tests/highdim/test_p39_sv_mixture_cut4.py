from __future__ import annotations

import math

import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter.nonlinear.cut_tf import tf_cut4g_sigma_point_rule


def _model() -> highdim.StochasticVolatilitySSM:
    return highdim.StochasticVolatilitySSM(sigma=1.0)


def _theta() -> tf.Tensor:
    return _model().unconstrained_from_physical(gamma=0.6, beta=0.4)


def _observations(values: tuple[float, ...] = (0.12, -0.08)) -> tf.Tensor:
    return tf.reshape(tf.constant(values, dtype=tf.float64), [-1, 1])


def test_p39_ksc_mixture_invariants_and_transform_are_finite() -> None:
    mixture = highdim.ksc_1998_log_chi_square_mixture()
    transformed = highdim.transformed_sv_observations(_observations((0.12, -0.08, 0.05)))
    mixture_mean = tf.reduce_sum(mixture.weights * mixture.means)
    mixture_variance = tf.reduce_sum(mixture.weights * (mixture.variances + tf.square(mixture.means - mixture_mean)))

    tf.debugging.assert_near(tf.reduce_sum(mixture.weights), tf.constant(1.0, dtype=tf.float64), atol=1e-14)
    tf.debugging.assert_near(mixture_mean, tf.constant(-1.2704, dtype=tf.float64), atol=5e-5)
    tf.debugging.assert_near(mixture_variance, tf.constant(math.pi**2 / 2.0, dtype=tf.float64), atol=1e-4)
    assert mixture.component_count == 7
    assert bool(tf.reduce_all(mixture.weights > 0.0).numpy())
    assert bool(tf.reduce_all(mixture.variances > 0.0).numpy())
    assert "shifted_by_minus_1p2704" in mixture.source
    assert bool(tf.reduce_all(tf.math.is_finite(transformed)).numpy())


def test_p39_one_step_mixture_cut4_matches_dense_mixture_reference() -> None:
    dense = highdim.scalar_sv_mixture_dense_reference(
        _model(),
        _theta(),
        _observations((0.12,)),
        order=401,
        radius=8.0,
    )
    cut4 = highdim.scalar_sv_mixture_cut4_filter(_model(), _theta(), _observations((0.12,)))

    tf.debugging.assert_near(cut4.log_likelihood, dense.log_likelihood, atol=5e-3, rtol=5e-3)
    tf.debugging.assert_near(cut4.mean_path, dense.mean_path, atol=2e-2)
    tf.debugging.assert_near(cut4.variance_path, dense.variance_path, atol=5e-2)
    tf.debugging.assert_near(
        tf.reduce_sum(cut4.component_weights, axis=1),
        tf.ones([1], dtype=tf.float64),
        atol=1e-12,
    )
    assert cut4.diagnostics["backend"] == "cut4_transformed_sv_gaussian_mixture"
    assert cut4.diagnostics["cut4_point_counts"] == ((14, 14, 14, 14, 14, 14, 14),)
    assert cut4.diagnostics["max_cut4_point_count"] == 14
    assert set(cut4.diagnostics["cut4_augmented_dims"]) == {3}
    assert set(cut4.diagnostics["cut4_polynomial_degrees"]) == {5}
    assert "inert innovation" in cut4.diagnostics["cut4_padding"]


def test_p39_two_step_mixture_cut4_matches_dense_mixture_reference_statistically() -> None:
    observations = _observations((0.12, -0.08))
    dense = highdim.scalar_sv_mixture_dense_reference(
        _model(),
        _theta(),
        observations,
        order=401,
        radius=8.0,
    )
    cut4 = highdim.scalar_sv_mixture_cut4_filter(_model(), _theta(), observations)

    errors = tf.stack(
        [
            cut4.log_likelihood - dense.log_likelihood,
            tf.reduce_max(tf.abs(cut4.log_normalizers - dense.log_normalizers)),
            tf.reduce_max(tf.abs(cut4.mean_path - dense.mean_path)),
        ]
    )
    assert bool(tf.reduce_all(tf.math.is_finite(errors)).numpy())
    tf.debugging.assert_near(cut4.log_likelihood, dense.log_likelihood, atol=2e-2, rtol=8e-3)
    tf.debugging.assert_near(cut4.log_normalizers, dense.log_normalizers, atol=2e-2, rtol=8e-3)
    tf.debugging.assert_near(cut4.mean_path, dense.mean_path, atol=8e-2)
    tf.debugging.assert_near(cut4.variance_path, dense.variance_path, atol=2.5e-1)
    tf.debugging.assert_near(
        tf.reduce_sum(cut4.component_weights, axis=1),
        tf.ones([2], dtype=tf.float64),
        atol=1e-12,
    )


def test_p39_native_sv_and_transformed_mixture_gap_is_explanatory_not_equivalence() -> None:
    model = _model()
    theta = _theta()
    observations = _observations((0.12, -0.08))
    native = highdim.FixedBranchSquaredTTFilter(
        highdim.FixedBranchFilterConfig(
            fit_config=None,
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
            measure_convention=highdim.MeasureConvention(
                density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
                mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
                reference_weight_name="omega",
            ),
            deterministic_seed="p39-native-explanatory",
            fit_quadrature_order=321,
        )
    ).log_likelihood(model, theta, observations)
    mixture = highdim.scalar_sv_mixture_cut4_filter(model, theta, observations)

    assert bool(tf.math.is_finite(native.log_likelihood).numpy())
    assert bool(tf.math.is_finite(mixture.log_likelihood).numpy())
    assert "not exact native SV likelihood" in mixture.diagnostics["non_claims"]
    assert abs(float((native.log_likelihood - mixture.log_likelihood).numpy())) > 0.0


def test_p39_exports_are_highdim_scoped() -> None:
    assert "scalar_sv_mixture_cut4_filter" in highdim.__all__
    assert hasattr(highdim, "SVLogChiSquareGaussianMixture")
    import bayesfilter

    assert not hasattr(bayesfilter, "scalar_sv_mixture_cut4_filter")


def test_p39_cut4_padding_is_required_by_cut4g_dimension_boundary() -> None:
    try:
        tf_cut4g_sigma_point_rule(2)
    except ValueError as exc:
        assert "dim >= 3" in str(exc)
    else:
        raise AssertionError("CUT4-G dim < 3 boundary did not fail")

    rule = tf_cut4g_sigma_point_rule(3)
    assert int(rule.offsets.shape[0]) == 14
    assert rule.polynomial_degree == 5
