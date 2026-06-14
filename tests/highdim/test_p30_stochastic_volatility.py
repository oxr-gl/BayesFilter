from __future__ import annotations

import math
import time

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


def _model() -> highdim.StochasticVolatilitySSM:
    return highdim.StochasticVolatilitySSM(sigma=1.0)


def _theta(gamma: float = 0.6, beta: float = 0.4) -> tf.Tensor:
    return _model().unconstrained_from_physical(gamma=gamma, beta=beta)


def _observations(values: tuple[float, ...] = (0.12, -0.08, 0.05)) -> tf.Tensor:
    return tf.reshape(tf.constant(values, dtype=tf.float64), [-1, 1])


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _scalar_sv_filter_config(
    *,
    order: int = 321,
    radius: float = 8.0,
    seed: str = "p37-m2p5-sv-scalar-dense",
) -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.constant([0.0], dtype=tf.float64),
                matrix=tf.constant([[radius]], dtype=tf.float64),
            ),
        ),
        measure_convention=_convention(),
        deterministic_seed=seed,
        fit_quadrature_order=order,
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


def _sv_joint_log_integrand(
    model: highdim.StochasticVolatilitySSM,
    theta: tf.Tensor,
    x_path: tf.Tensor,
    y: tf.Tensor,
) -> tf.Tensor:
    log_value = model.initial_log_density(theta, x_path[0])[0]
    log_value = log_value + model.observation_log_density(theta, x_path[0], y[0], t=0)[0]
    for time_index in range(1, int(x_path.shape[0])):
        log_value = log_value + model.transition_log_density(
            theta,
            x_path[time_index - 1],
            x_path[time_index],
            t=time_index,
        )[0]
        log_value = log_value + model.observation_log_density(
            theta,
            x_path[time_index],
            y[time_index],
            t=time_index,
        )[0]
    return log_value


def _tiny_joint_dense_log_evidence(
    model: highdim.StochasticVolatilitySSM,
    theta: tf.Tensor,
    observations: tf.Tensor,
    *,
    order: int = 29,
    radius: float = 8.0,
) -> tf.Tensor:
    nodes, weights = _legendre_interval_nodes_weights(order=order, left=-radius, right=radius)
    final_time = int(tf.convert_to_tensor(observations).shape[0]) - 1
    mesh_nodes = tf.meshgrid(*([nodes] * (final_time + 1)), indexing="ij")
    mesh_weights = tf.meshgrid(*([weights] * (final_time + 1)), indexing="ij")
    flat_paths = tf.stack([tf.reshape(axis, [-1]) for axis in mesh_nodes], axis=1)
    flat_weights = tf.ones([tf.shape(flat_paths)[0]], dtype=tf.float64)
    for axis_weight in mesh_weights:
        flat_weights = flat_weights * tf.reshape(axis_weight, [-1])
    log_values = []
    for row_index in range(int(flat_paths.shape[0])):
        log_values.append(
            _sv_joint_log_integrand(
                model,
                theta,
                tf.reshape(flat_paths[row_index], [-1, 1]),
                observations,
            )
        )
    log_values_tensor = tf.stack(log_values)
    max_log = tf.reduce_max(log_values_tensor)
    integral = tf.reduce_sum(flat_weights * tf.exp(log_values_tensor - max_log))
    return tf.math.log(integral) + max_log


def _sequential_dense_grid_reference(
    model: highdim.StochasticVolatilitySSM,
    theta: tf.Tensor,
    observations: tf.Tensor,
    *,
    order: int = 181,
    radius: float = 8.0,
) -> dict[str, tf.Tensor]:
    x_grid, weights = _legendre_interval_nodes_weights(order=order, left=-radius, right=radius)
    y = tf.convert_to_tensor(observations, dtype=tf.float64)
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
        "grid_size": tf.constant(order, dtype=tf.int32),
    }


def test_p30_sv_transform_and_log_densities_match_equations():
    model = _model()
    theta = _theta(gamma=0.6, beta=0.4)
    parameters = model.physical_parameters(theta)
    x0 = tf.constant([[0.25], [-0.5]], dtype=tf.float64)
    x1 = tf.constant([[0.40], [-0.25]], dtype=tf.float64)
    y0 = tf.constant([0.12], dtype=tf.float64)

    tf.debugging.assert_near(parameters["gamma"], tf.constant(0.6, dtype=tf.float64), atol=2e-15)
    tf.debugging.assert_near(parameters["beta"], tf.constant(0.4, dtype=tf.float64), atol=2e-15)
    tf.debugging.assert_near(parameters["sigma"], tf.constant(1.0, dtype=tf.float64), atol=0.0)

    stationary_scale = tf.constant(1.0 / math.sqrt(1.0 - 0.6**2), dtype=tf.float64)
    expected_initial = _normal_log_prob(x0[:, 0], tf.constant(0.0, dtype=tf.float64), stationary_scale)
    expected_transition = _normal_log_prob(x1[:, 0], 0.6 * x0[:, 0], tf.constant(1.0, dtype=tf.float64))
    expected_observation = _normal_log_prob(
        tf.constant(0.12, dtype=tf.float64),
        tf.zeros([2], dtype=tf.float64),
        0.4 * tf.exp(0.5 * x0[:, 0]),
    )

    tf.debugging.assert_near(model.initial_log_density(theta, x0), expected_initial, atol=2e-14)
    tf.debugging.assert_near(
        model.transition_log_density(theta, x0, x1, t=1),
        expected_transition,
        atol=2e-14,
    )
    tf.debugging.assert_near(
        model.observation_log_density(theta, x0, y0, t=0),
        expected_observation,
        atol=2e-14,
    )
    assert (
        model.manifest_payload()["dimension_convention"]
        == "synthetic row includes x_0:x_T; joint dimension is 2+(T+1)"
    )


def test_p30_sv_tiny_dense_joint_reference_matches_sequential_grid():
    model = _model()
    theta = _theta(gamma=0.6, beta=0.4)
    y = _observations((0.12, -0.08))

    joint = _tiny_joint_dense_log_evidence(model, theta, y, order=27, radius=8.0)
    sequential = _sequential_dense_grid_reference(model, theta, y, order=321, radius=8.0)

    tf.debugging.assert_near(joint, sequential["log_evidence"], atol=3e-6)
    assert bool(tf.math.is_finite(sequential["log_evidence"]).numpy())
    assert bool(tf.reduce_all(sequential["variance_path"] > 0.0).numpy())


def test_p30_sv_bounded_reference_smoke_records_finite_diagnostics():
    model = _model()
    theta = _theta(gamma=0.6, beta=0.4)
    _x_path, y = model.simulate(theta, final_time=10, seed=3702)

    start = time.perf_counter()
    reference = _sequential_dense_grid_reference(model, theta, y, order=181, radius=8.0)
    wall_time_seconds = time.perf_counter() - start

    assert bool(tf.math.is_finite(reference["log_evidence"]).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(reference["mean_path"])).numpy())
    assert bool(tf.reduce_all(reference["variance_path"] > 0.0).numpy())
    assert wall_time_seconds < 10.0

    manifest = highdim.P30ModelSuiteResultManifest(
        version="p37.m2.sv.reference.result.v1",
        fixture_version="p37.m2.sv.reference.fixture.v1",
        model_id=highdim.P30ModelSuiteModelID.STOCHASTIC_VOLATILITY_SYNTHETIC,
        source_governance_status=highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION,
        bayesfilter_evidence_anchors=(
            "tests/highdim/test_p30_stochastic_volatility.py::"
            "test_p30_sv_scalar_nonlinear_value_path_matches_dense_reference",
        ),
        accuracy_metrics={
            "tiny_reference_log_evidence": float(reference["log_evidence"].numpy()),
            "reference_grid_order": int(reference["grid_size"].numpy()),
        },
        resource_metrics={"wall_time_seconds": float(wall_time_seconds), "horizon": 10},
        finite_diagnostics={
            "log_evidence_finite": bool(tf.math.is_finite(reference["log_evidence"]).numpy()),
            "mean_path_finite": bool(tf.reduce_all(tf.math.is_finite(reference["mean_path"])).numpy()),
            "variance_positive": bool(tf.reduce_all(reference["variance_path"] > 0.0).numpy()),
        },
        branch_replay_status="not_applicable_reference_only",
        failure_classification="scalar_dense_value_path_available_tt_sirt_pending",
        clean_room_status="P30 equations only; MATLAB paths are behavioral anchors only",
        non_claims=(
            "not TT posterior accuracy",
            "not Zhao--Cui T=1000 reproduction",
            "not SMC reference evidence",
        ),
    )

    assert manifest.source_governance_status is highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION
    assert "not TT posterior accuracy" in manifest.non_claims


def test_p30_sv_fixture_manifest_states_transform_and_dimension_convention():
    manifest = highdim.P30ModelSuiteFixtureManifest(
        version="p37.m2.sv.fixture.v1",
        model_id=highdim.P30ModelSuiteModelID.STOCHASTIC_VOLATILITY_SYNTHETIC,
        source_equations=("eq:p27-sv1", "eq:p27-sv2", "eq:p27-sv3", "eq:p27-sv5a", "eq:p27-sv6"),
        paper_anchor="Zhao--Cui stochastic-volatility benchmark, Section 6.2",
        matlab_anchor="eg2_sv/mainscript.m",
        parameter_values={
            "gamma_true": 0.6,
            "beta_true": 0.4,
            "sigma_fixed": 1.0,
            "theta_prime": "(Phi^{-1}(gamma), log beta)",
        },
        prior={"synthetic_truth": "fixed truth used for simulator/reference rows"},
        state_dimension=1,
        parameter_dimension=2,
        horizon=10,
        basis={"family": "not_used_dense_reference", "future_paper_scale_ell": 33},
        rank=(1, 1),
        sweeps=0,
        seed="p37-m2-sv-reference",
        dtype="tf.float64",
        reference_method="tiny dense joint quadrature and sequential dense-grid reference",
        expected_metrics=("log_evidence_finite", "filter_mean_finite", "filter_variance_positive"),
        vetoes=("transform_domain_error", "nonfinite_likelihood", "missing_x0_convention"),
        non_claims=(
            "not TT posterior accuracy",
            "not Zhao--Cui T=1000 reproduction",
            "not SMC reference evidence",
        ),
        clean_room_status="P30-derived fixture contract, MATLAB audit reference only",
        dimension_convention="synthetic row includes x_0:x_T; joint dimension is 2+(T+1)",
    )

    assert manifest.parameter_values["theta_prime"] == "(Phi^{-1}(gamma), log beta)"
    assert manifest.dimension_convention == "synthetic row includes x_0:x_T; joint dimension is 2+(T+1)"


def test_p30_sv_registry_marks_scalar_value_path_as_partial_not_tt_validation():
    row = highdim.p30_model_suite_registry()["stochastic_volatility_synthetic"]

    assert row.status is highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION
    assert "StochasticVolatilitySSM" in highdim.__all__
    assert "test_p30_stochastic_volatility.py" in row.bayesfilter_test_anchor
    assert any("not TT posterior accuracy" in claim for claim in row.non_claims)


def test_p30_sv_scalar_nonlinear_value_path_matches_dense_reference():
    model = _model()
    theta = _theta(gamma=0.6, beta=0.4)
    y = _observations((0.12, -0.08, 0.05))
    reference = _sequential_dense_grid_reference(model, theta, y, order=321, radius=8.0)

    result = highdim.FixedBranchSquaredTTFilter(
        _scalar_sv_filter_config(order=321, radius=8.0)
    ).log_likelihood(model, theta, y)

    tf.debugging.assert_near(result.log_likelihood, reference["log_evidence"], atol=2e-10)
    tf.debugging.assert_near(
        tf.stack([step.log_normalizer for step in result.steps]),
        reference["log_normalizers"],
        atol=2e-10,
    )
    tf.debugging.assert_near(
        tf.concat([step.retained_filter.diagnostics["mean"] for step in result.steps], axis=0),
        reference["mean_path"],
        atol=2e-10,
    )
    tf.debugging.assert_near(
        tf.stack([step.retained_filter.diagnostics["variance"] for step in result.steps]),
        reference["variance_path"],
        atol=2e-10,
    )
    tf.debugging.assert_near(
        result.retained_filter.diagnostics["mean"],
        reference["mean_path"][-1:],
        atol=2e-10,
    )
    tf.debugging.assert_near(
        result.retained_filter.diagnostics["variance"],
        reference["variance_path"][-1],
        atol=2e-10,
    )
    assert result.status is highdim.HighDimStatus.OK
    assert result.retained_filter.storage_kind == "scalar_dense_grid"
    assert result.diagnostics["value_path"] == "scalar_nonlinear_dense_quadrature_value_path"
    assert result.diagnostics["integration_grid_size"] == 321
    assert result.diagnostics["tt_artifacts_present"] is False


def test_p30_sv_scalar_nonlinear_value_path_replay_is_deterministic():
    model = _model()
    theta = _theta(gamma=0.6, beta=0.4)
    y = _observations((0.12, -0.08))
    config = _scalar_sv_filter_config(order=181, radius=8.0, seed="p37-m2p5-replay")

    left = highdim.FixedBranchSquaredTTFilter(config).log_likelihood(model, theta, y)
    right = highdim.FixedBranchSquaredTTFilter(config).log_likelihood(model, theta, y)

    tf.debugging.assert_near(left.log_likelihood, right.log_likelihood, atol=0.0)
    assert left.branch_identity.hash.value == right.branch_identity.hash.value
    assert left.retained_filter.branch_identity.hash.value == right.retained_filter.branch_identity.hash.value


def test_p30_sv_scalar_nonlinear_value_path_blocks_tt_artifact_request():
    model = _model()
    theta = _theta(gamma=0.6, beta=0.4)
    product_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 4)],
        _convention(),
    )
    fit_config = highdim.FixedTTFitConfig(
        ranks=(1, 1),
        ridge=1e-10,
        max_sweeps=1,
        sweep_order=(0,),
        row_budget=64,
        column_budget=16,
        dense_matrix_byte_budget=50_000,
        normal_matrix_byte_budget=10_000,
        condition_number_warning=1e8,
        condition_number_veto=1e12,
        holdout_tolerance=1e6,
    )
    config = highdim.FixedBranchFilterConfig(
        fit_config=fit_config,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(1),),
        measure_convention=_convention(),
        deterministic_seed="p37-m2p5-block-tt",
        product_basis=product_basis,
    )

    with pytest.raises(TypeError, match="does not fit TT artifacts"):
        highdim.FixedBranchSquaredTTFilter(config).log_likelihood(
            model,
            theta,
            _observations((0.12,)),
        )
