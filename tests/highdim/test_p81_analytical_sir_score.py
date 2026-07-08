from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _initial_cores(product_basis: highdim.ProductBasis) -> tuple[highdim.TTCore, ...]:
    return tuple(
        highdim.TTCore(tf.ones([1, basis.basis_dim, 1], dtype=DTYPE))
        for basis in product_basis.bases
    )


def _p81_sir_d18_horizon0_config(
    model: highdim.ParameterizedZhaoCuiSIRSSM,
) -> highdim.FixedBranchFilterConfig:
    convention = _convention()
    product_basis = highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 0)
            for _ in range(model.state_dim())
        ],
        convention,
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=tuple([1] * (model.state_dim() + 1)),
            ridge=1e-8,
            max_sweeps=1,
            sweep_order=tuple(range(model.state_dim())),
            row_budget=300_000,
            column_budget=16,
            # The d=18 horizon-0 smoke evaluates a 2^18 degree-0 grid.  The
            # rank-1 TT evaluation estimate is about 151 MB, so this local
            # budget is deliberately above that gate without changing defaults.
            dense_matrix_byte_budget=192_000_000,
            normal_matrix_byte_budget=1_000_000,
            condition_number_warning=1e12,
            condition_number_veto=1e16,
            holdout_tolerance=1e-1,
        ),
        density_tau=1e-12,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=80_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=model.base_model.initial_mean,
                matrix=tf.linalg.diag(
                    tf.fill([model.state_dim()], tf.constant(0.25, dtype=DTYPE))
                ),
            ),
        ),
        measure_convention=convention,
        deterministic_seed="p81-sir-d18-horizon0",
        product_basis=product_basis,
        initial_cores=_initial_cores(product_basis),
        fit_quadrature_order=2,
    )


def test_parameterized_zhao_cui_sir_matches_p8p_p79_theta_convention() -> None:
    model = highdim.parameterized_zhao_cui_sir_austria_model()
    base = highdim.zhao_cui_sir_austria_model()
    theta = tf.constant([0.2, -0.1, 0.3], dtype=DTYPE)

    scaled = model.scaled_model(theta)

    assert model.parameter_dim() == 3
    assert model.state_dim() == 18
    assert model.observation_dim() == 9
    tf.debugging.assert_near(scaled.kappa, base.kappa * tf.exp(theta[0]))
    tf.debugging.assert_near(scaled.nu, base.nu * tf.exp(theta[1]))
    tf.debugging.assert_near(
        scaled.observation_covariance,
        base.observation_covariance
        * tf.exp(tf.constant(2.0, dtype=DTYPE) * theta[2]),
    )
    assert model.manifest_payload()["parameter_order"] == (
        "log_kappa_scale",
        "log_nu_scale",
        "log_obs_noise_scale",
    )


def test_parameterized_zhao_cui_sir_terms_are_sensitive_to_intended_theta_components() -> None:
    model = highdim.parameterized_zhao_cui_sir_austria_model()
    theta = tf.zeros([3], dtype=DTYPE)
    x_prev = model.base_model.initial_mean[tf.newaxis, :]
    perturbation = tf.linspace(
        tf.constant(-0.03, dtype=DTYPE),
        tf.constant(0.03, dtype=DTYPE),
        model.state_dim(),
    )[tf.newaxis, :]
    x_next = model.transition_mean(theta, x_prev) + perturbation
    observation = model.infectious_components(x_prev)[0] + tf.linspace(
        tf.constant(-0.2, dtype=DTYPE),
        tf.constant(0.2, dtype=DTYPE),
        model.observation_dim(),
    )

    with tf.GradientTape() as transition_tape:
        transition_tape.watch(theta)
        transition_value = model.transition_log_density(theta, x_prev, x_next, t=1)[0]
    transition_gradient = transition_tape.gradient(transition_value, theta)

    with tf.GradientTape() as observation_tape:
        observation_tape.watch(theta)
        observation_value = model.observation_log_density(theta, x_prev, observation, t=0)[0]
    observation_gradient = observation_tape.gradient(observation_value, theta)

    assert transition_gradient is not None
    assert observation_gradient is not None
    assert abs(float(transition_gradient[0].numpy())) > 1e-12
    assert abs(float(transition_gradient[1].numpy())) > 1e-12
    assert abs(float(observation_gradient[2].numpy())) > 1e-12


def test_multistate_fixed_design_tt_score_path_runs_on_sir_d18_horizon0_observation_term() -> None:
    model = highdim.parameterized_zhao_cui_sir_austria_model()
    theta = tf.zeros([3], dtype=DTYPE)
    observation = model.infectious_components(model.base_model.initial_mean)[0]
    config = _p81_sir_d18_horizon0_config(model)
    derivative_config = highdim.FixedBranchDerivativeConfig(
        parameter_indices=(2,),
        finite_difference_h=(1e-3,),
        solve_condition_number_veto=1e16,
    )

    result = highdim.multistate_nonlinear_fixed_design_tt_score_path(
        model,
        theta,
        observation[tf.newaxis, :],
        config,
        derivative_config,
        fixture_id="p81.score.sir-d18.horizon0.v1",
        initial_target_id="p81.score.sir-d18.initial.v1",
        transition_target_id="p81.score.sir-d18.transition.v1",
        branch_seed_prefix="p81-score-sir-d18-horizon0",
    )

    assert result.status is highdim.HighDimStatus.OK
    assert result.score.shape == (1,)
    assert bool(tf.math.is_finite(result.log_likelihood).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(result.score)).numpy())
    assert result.finite_difference_table.valid_rows()
    for row in result.finite_difference_table.rows:
        assert row.row_status is highdim.FiniteDifferenceRowStatus.VALID
        assert row.branch_hash_plus == row.branch_hash_base
        assert row.branch_hash_minus == row.branch_hash_base
    assert result.diagnostics["score_path"] == "multistate_nonlinear_fixed_design_tt_score_path"
    assert result.diagnostics["route_role"] == highdim.MULTISTATE_RETAINED_GRID_ROUTE_ROLE
    assert (
        result.diagnostics["leaderboard_admission"]
        == highdim.MULTISTATE_RETAINED_GRID_LEADERBOARD_ADMISSION
    )
    assert (
        result.diagnostics["production_zhao_cui_route"]
        == highdim.FIXED_VARIANT_ZHAO_CUI_PRODUCTION_ROUTE
    )
    assert result.diagnostics["state_dim"] == 18
    assert result.diagnostics["horizon"] == 0


def test_multistate_fixed_design_tt_score_path_blocks_sir_d18_two_row_all_grid_transition() -> None:
    model = highdim.parameterized_zhao_cui_sir_austria_model()
    theta = tf.zeros([3], dtype=DTYPE)
    first_state = model.base_model.initial_mean
    second_state = model.transition_mean(theta, first_state[tf.newaxis, :])[0]
    observations = tf.stack(
        [
            model.infectious_components(first_state)[0],
            model.infectious_components(second_state)[0],
        ],
        axis=0,
    )
    config = _p81_sir_d18_horizon0_config(model)
    derivative_config = highdim.FixedBranchDerivativeConfig(
        parameter_indices=(2,),
        finite_difference_h=(1e-3,),
        solve_condition_number_veto=1e16,
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.COMPLEXITY_GATE.value):
        highdim.multistate_nonlinear_fixed_design_tt_score_path(
            model,
            theta,
            observations,
            config,
            derivative_config,
            fixture_id="p81.score.sir-d18.two-row.v1",
            initial_target_id="p81.score.sir-d18.initial.v1",
            transition_target_id="p81.score.sir-d18.transition.v1",
            branch_seed_prefix="p81-score-sir-d18-two-row",
        )


def test_parameterized_sir_transition_mean_parameter_jacobian_matches_diagnostic_tape() -> None:
    model = highdim.parameterized_zhao_cui_sir_austria_model()
    theta = tf.constant([0.03, -0.02, 0.01], dtype=DTYPE)
    x_prev = model.base_model.initial_mean[tf.newaxis, :] + tf.linspace(
        tf.constant(-0.02, dtype=DTYPE),
        tf.constant(0.02, dtype=DTYPE),
        model.state_dim(),
    )[tf.newaxis, :]

    mean, jacobian = model.transition_mean_parameter_jacobian(theta, x_prev)

    with tf.GradientTape() as tape:
        tape.watch(theta)
        autodiff_mean = model.transition_mean(theta, x_prev)
    autodiff_jacobian = tape.jacobian(autodiff_mean, theta)

    tf.debugging.assert_near(mean, autodiff_mean)
    tf.debugging.assert_near(
        tf.transpose(autodiff_jacobian, [2, 0, 1]),
        jacobian,
        atol=1e-10,
        rtol=1e-10,
    )


def test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape() -> None:
    model = highdim.parameterized_zhao_cui_sir_austria_model()
    theta = tf.constant([0.02, -0.03, 0.04], dtype=DTYPE)
    x_prev = model.base_model.initial_mean[tf.newaxis, :]
    x_next = model.transition_mean(theta, x_prev) + tf.linspace(
        tf.constant(-0.01, dtype=DTYPE),
        tf.constant(0.01, dtype=DTYPE),
        model.state_dim(),
    )[tf.newaxis, :]
    observation = model.infectious_components(x_prev)[0] + tf.linspace(
        tf.constant(-0.2, dtype=DTYPE),
        tf.constant(0.2, dtype=DTYPE),
        model.observation_dim(),
    )

    transition_score = model.transition_log_density_parameter_score(
        theta,
        x_prev,
        x_next,
        t=1,
    )
    observation_score = model.observation_log_density_parameter_score(
        theta,
        x_prev,
        observation,
        t=0,
    )

    with tf.GradientTape() as transition_tape:
        transition_tape.watch(theta)
        transition_value = model.transition_log_density(theta, x_prev, x_next, t=1)[0]
    transition_gradient = transition_tape.gradient(transition_value, theta)

    with tf.GradientTape() as observation_tape:
        observation_tape.watch(theta)
        observation_value = model.observation_log_density(theta, x_prev, observation, t=0)[0]
    observation_gradient = observation_tape.gradient(observation_value, theta)

    assert transition_gradient is not None
    assert observation_gradient is not None
    tf.debugging.assert_near(transition_score[0], transition_gradient, atol=1e-10, rtol=1e-10)
    tf.debugging.assert_near(observation_score[0], observation_gradient, atol=1e-10, rtol=1e-10)


def test_parameterized_sir_infectious_components_vjp_scatter() -> None:
    model = highdim.parameterized_zhao_cui_sir_austria_model()
    cotangent = tf.reshape(
        tf.range(model.observation_dim(), dtype=DTYPE),
        [1, model.observation_dim()],
    )

    full_state_cotangent = model.infectious_components_vjp(cotangent)

    tf.debugging.assert_near(full_state_cotangent[:, 0::2], tf.zeros_like(cotangent))
    tf.debugging.assert_near(full_state_cotangent[:, 1::2], cotangent)
