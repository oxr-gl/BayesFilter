from __future__ import annotations

import math

import pytest
import tensorflow as tf

import bayesfilter.highdim.filtering as filtering_module
import bayesfilter.highdim as highdim


FIXTURE_ID = "p37.m2p6c.sv.short-sequential-tt-value-path.v1"
DENSE_COMPARATOR_FIXTURE_ID = "p37.m2p6c.sv.dense-sequential-comparator.gl321.v1"
TT_RETAINED_MOMENT_FIXTURE_ID = "p37.m2p6c.sv.tt-retained-moment.gl257.v1"
TT_RETAINED_PROPAGATION_FIXTURE_ID = "p37.m2p6c.sv.tt-retained-propagation.gl321.v1"


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _model() -> highdim.StochasticVolatilitySSM:
    return highdim.StochasticVolatilitySSM(sigma=1.0)


def _theta() -> tf.Tensor:
    return _model().unconstrained_from_physical(gamma=0.6, beta=0.4)


def _observations() -> tf.Tensor:
    return tf.reshape(tf.constant((0.12, -0.08), dtype=tf.float64), [-1, 1])


def _coordinate_map() -> highdim.AffineCoordinateMap:
    return highdim.AffineCoordinateMap(
        offset=tf.constant([0.0], dtype=tf.float64),
        matrix=tf.constant([[8.0]], dtype=tf.float64),
    )


def _basis() -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 64)],
        _convention(),
    )


def _initial_cores(product_basis: highdim.ProductBasis) -> tuple[highdim.TTCore, ...]:
    return (
        highdim.TTCore(tf.ones([1, product_basis.bases[0].basis_dim, 1], dtype=tf.float64)),
    )


def _fit_config() -> highdim.FixedTTFitConfig:
    return highdim.FixedTTFitConfig(
        ranks=(1, 1),
        ridge=1e-12,
        max_sweeps=2,
        sweep_order=(0,),
        row_budget=256,
        column_budget=80,
        dense_matrix_byte_budget=100_000,
        normal_matrix_byte_budget=50_000,
        condition_number_warning=1e10,
        condition_number_veto=1e14,
        holdout_tolerance=2e-5,
    )


def _tt_config(seed: str = "p37-m2p6c-sv-short-tt") -> highdim.FixedBranchFilterConfig:
    product_basis = _basis()
    return highdim.FixedBranchFilterConfig(
        fit_config=_fit_config(),
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(_coordinate_map(),),
        measure_convention=_convention(),
        deterministic_seed=seed,
        product_basis=product_basis,
        initial_cores=_initial_cores(product_basis),
        fit_quadrature_order=161,
    )


def _normal_log_prob(value: tf.Tensor, loc: tf.Tensor, scale: tf.Tensor) -> tf.Tensor:
    return -0.5 * tf.square((value - loc) / scale) - tf.math.log(scale) - 0.5 * tf.math.log(
        tf.constant(2.0 * math.pi, dtype=tf.float64)
    )


def _legendre_interval_nodes_weights(
    *,
    order: int,
    left: float,
    right: float,
) -> tuple[tf.Tensor, tf.Tensor]:
    nodes, weights = highdim.legendre_gauss_nodes_weights(order)
    half_length = tf.constant(0.5 * (right - left), dtype=tf.float64)
    midpoint = tf.constant(0.5 * (right + left), dtype=tf.float64)
    return midpoint + half_length * nodes, half_length * weights


def _sequential_dense_grid_reference(order: int = 321, radius: float = 8.0) -> dict[str, tf.Tensor]:
    model = _model()
    theta = _theta()
    y = _observations()
    x_grid, weights = _legendre_interval_nodes_weights(order=order, left=-radius, right=radius)
    parameters = model.physical_parameters(theta)
    gamma = parameters["gamma"]
    beta = parameters["beta"]
    sigma = parameters["sigma"]
    prior_scale = sigma / tf.sqrt(1.0 - tf.square(gamma))
    log_prior = _normal_log_prob(x_grid, tf.constant(0.0, dtype=tf.float64), prior_scale)
    log_likelihood = _normal_log_prob(
        y[0, 0],
        tf.zeros_like(x_grid),
        beta * tf.exp(0.5 * x_grid),
    )
    log_density = log_prior + log_likelihood
    log_terms = []
    means = []
    variances = []

    for time_index in range(int(y.shape[0])):
        if time_index > 0:
            previous_density = tf.exp(log_density - log_terms[-1])
            transition_log = _normal_log_prob(
                x_grid[:, tf.newaxis],
                gamma * x_grid[tf.newaxis, :],
                sigma,
            )
            predictive = tf.reduce_sum(
                weights[tf.newaxis, :] * previous_density[tf.newaxis, :] * tf.exp(transition_log),
                axis=1,
            )
            observation_log = _normal_log_prob(
                y[time_index, 0],
                tf.zeros_like(x_grid),
                beta * tf.exp(0.5 * x_grid),
            )
            log_density = tf.math.log(predictive) + observation_log
        max_log = tf.reduce_max(log_density)
        evidence_increment = tf.reduce_sum(weights * tf.exp(log_density - max_log))
        log_normalizer = tf.math.log(evidence_increment) + max_log
        normalized_density = tf.exp(log_density - log_normalizer)
        mean = tf.reduce_sum(weights * x_grid * normalized_density)
        second = tf.reduce_sum(weights * tf.square(x_grid) * normalized_density)
        log_terms.append(log_normalizer)
        means.append(mean)
        variances.append(second - tf.square(mean))

    return {
        "log_evidence": tf.reduce_sum(tf.stack(log_terms)),
        "log_normalizers": tf.stack(log_terms),
        "mean_path": tf.stack(means),
        "variance_path": tf.stack(variances),
    }


def _tt_result(seed: str = "p37-m2p6c-sv-short-tt") -> highdim.FixedBranchFilterResult:
    return highdim.scalar_nonlinear_fixed_design_tt_value_path(
        _model(),
        _theta(),
        _observations(),
        _tt_config(seed),
        fixture_id=FIXTURE_ID,
        branch_seed_prefix=seed,
    )


def test_p30_sv_short_sequential_tt_value_path_matches_dense_oracle():
    reference = _sequential_dense_grid_reference()
    result = _tt_result()

    assert DENSE_COMPARATOR_FIXTURE_ID.endswith("gl321.v1")
    assert TT_RETAINED_MOMENT_FIXTURE_ID.endswith("gl257.v1")
    assert TT_RETAINED_PROPAGATION_FIXTURE_ID.endswith("gl321.v1")
    assert result.status is highdim.HighDimStatus.OK
    assert result.diagnostics["value_path"] == "scalar_nonlinear_fixed_design_tt_value_path"
    assert result.diagnostics["tt_artifacts_present"] is True
    assert result.diagnostics["promoted_horizon"] == 2
    assert result.retained_filter.storage_kind == "scalar_tt_grid"

    log_normalizers = tf.stack([step.log_normalizer for step in result.steps])
    mean_path = tf.concat([step.retained_filter.diagnostics["mean"] for step in result.steps], axis=0)
    variance_path = tf.stack([step.retained_filter.diagnostics["variance"] for step in result.steps])

    tf.debugging.assert_near(log_normalizers, reference["log_normalizers"], atol=5e-3, rtol=5e-3)
    tf.debugging.assert_near(result.log_likelihood, reference["log_evidence"], atol=1e-2, rtol=5e-3)
    tf.debugging.assert_near(mean_path, reference["mean_path"], atol=5e-2)
    tf.debugging.assert_near(variance_path, reference["variance_path"], atol=2e-1)

    for step in result.steps:
        assert step.fit_result is not None
        assert step.density is not None
        assert step.retained_filter.storage_kind == "scalar_tt_grid"
        assert step.diagnostics["value_path"] == "scalar_nonlinear_fixed_design_tt_value_path"
        assert step.diagnostics["density_hash"] == step.density.branch_identity.hash.value
        assert step.retained_filter.diagnostics["density_hash"] == step.density.branch_identity.hash.value
        tf.debugging.assert_near(
            step.diagnostics["retained_moment_mass"],
            tf.constant(1.0, dtype=tf.float64),
            atol=5e-4,
        )


def test_p30_sv_short_sequential_tt_value_path_replay_is_deterministic():
    left = _tt_result("p37-m2p6c-sv-short-tt-replay")
    right = _tt_result("p37-m2p6c-sv-short-tt-replay")

    tf.debugging.assert_near(left.log_likelihood, right.log_likelihood, atol=0.0)
    assert left.branch_identity.hash.value == right.branch_identity.hash.value
    assert left.retained_filter.branch_identity.hash.value == right.retained_filter.branch_identity.hash.value
    assert tuple(step.branch_identity.hash.value for step in left.steps) == tuple(
        step.branch_identity.hash.value for step in right.steps
    )


def test_p30_sv_short_sequential_tt_value_path_rejects_dense_lane_trigger():
    config = highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(_coordinate_map(),),
        measure_convention=_convention(),
        deterministic_seed="p37-m2p6c-dense-trigger",
        product_basis=None,
        fit_quadrature_order=161,
    )

    with pytest.raises(TypeError, match="requires fit_config and product_basis"):
        highdim.scalar_nonlinear_fixed_design_tt_value_path(_model(), _theta(), _observations(), config)


def test_p30_sv_short_sequential_tt_value_path_is_not_log_likelihood_dense_route():
    config = _tt_config("p37-m2p6c-old-dispatcher-rejection")

    with pytest.raises(TypeError, match="does not fit TT artifacts"):
        highdim.FixedBranchSquaredTTFilter(config).log_likelihood(_model(), _theta(), _observations())


def test_p30_sv_short_sequential_tt_value_path_does_not_call_dense_retained_helper(monkeypatch):
    def fail_dense_helper(*args, **kwargs):
        raise AssertionError("dense retained helper must not be used by scalar_tt_grid propagation")

    monkeypatch.setattr(filtering_module, "_scalar_dense_predictive_log_density_from_retained", fail_dense_helper)

    result = _tt_result("p37-m2p6c-no-dense-helper")

    assert result.diagnostics["value_path"] == "scalar_nonlinear_fixed_design_tt_value_path"
    assert result.steps[1].retained_filter.storage_kind == "scalar_tt_grid"


def test_p30_sv_scalar_tt_grid_retained_requires_density_hash_path():
    result = _tt_result("p37-m2p6c-retained-hash")
    retained = result.steps[0].retained_filter

    assert retained.storage_kind == "scalar_tt_grid"
    assert retained.diagnostics["density_hash"] == result.steps[0].density.branch_identity.hash.value
    assert retained.density is result.steps[0].density
