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


def _lebesgue_convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_LEBESGUE,
        mass_measure=highdim.MassMeasure.REFERENCE_LEBESGUE,
        reference_weight_name="omega",
    )


def _filter_config(state_dim: int = 1, seed: str = "phase4-fixture") -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(state_dim),),
        measure_convention=_convention(),
        deterministic_seed=seed,
    )


def _tt_filter_config(seed: str = "phase4-tt-fixture") -> highdim.FixedBranchFilterConfig:
    product_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 6)],
        _convention(),
    )
    fit_config = highdim.FixedTTFitConfig(
        ranks=(1, 1),
        ridge=1e-10,
        max_sweeps=1,
        sweep_order=(0,),
        row_budget=256,
        column_budget=32,
        dense_matrix_byte_budget=100_000,
        normal_matrix_byte_budget=10_000,
        condition_number_warning=1e10,
        condition_number_veto=1e14,
        holdout_tolerance=1e6,
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=fit_config,
        density_tau=1e-12,
        normalizer_floor=1e-14,
        denominator_floor=1e-14,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(1),),
        measure_convention=_convention(),
        deterministic_seed=seed,
        product_basis=product_basis,
        fit_quadrature_order=24,
    )


def _scalar_model(
    transition_scale: float = 0.7,
    transition_variance: float = 0.25,
) -> highdim.LinearGaussianSSM:
    return highdim.LinearGaussianSSM(
        initial_mean=tf.constant([0.0], dtype=tf.float64),
        initial_covariance=tf.constant([[1.0]], dtype=tf.float64),
        transition_matrix=tf.constant([[transition_scale]], dtype=tf.float64),
        transition_covariance=tf.constant([[transition_variance]], dtype=tf.float64),
        observation_matrix=tf.constant([[1.0]], dtype=tf.float64),
        observation_covariance=tf.constant([[0.09]], dtype=tf.float64),
    )


def _theta0() -> tf.Tensor:
    return tf.zeros([0], dtype=tf.float64)


def test_model_protocol_shapes_and_broadcasting():
    model = _scalar_model()
    theta = _theta0()
    x_rows = tf.constant([[-0.5], [0.25], [1.25]], dtype=tf.float64)
    x_next = tf.constant([[-0.3], [0.1], [0.8]], dtype=tf.float64)

    initial = model.initial_log_density(theta, x_rows)
    transition = model.transition_log_density(theta, x_rows, x_next, t=1)
    observation = model.observation_log_density(
        theta,
        x_rows,
        tf.constant([0.2], dtype=tf.float64),
        t=0,
    )
    single = model.initial_log_density(theta, tf.constant([0.0], dtype=tf.float64))

    assert model.parameter_dim() == 0
    assert model.state_dim() == 1
    assert model.observation_dim() == 1
    assert initial.shape == (3,)
    assert transition.shape == (3,)
    assert observation.shape == (3,)
    assert single.shape == (1,)


def test_one_step_scalar_kalman_evidence():
    result = highdim.FixedBranchSquaredTTFilter(_filter_config()).log_likelihood(
        _scalar_model(),
        _theta0(),
        tf.constant([0.2], dtype=tf.float64),
    )

    tf.debugging.assert_near(
        result.log_likelihood,
        tf.constant(-0.980376005178410, dtype=tf.float64),
        atol=2e-10,
    )
    tf.debugging.assert_near(
        result.retained_filter.diagnostics["mean"],
        tf.constant([0.183486238532110], dtype=tf.float64),
        atol=2e-10,
    )
    tf.debugging.assert_near(
        result.retained_filter.diagnostics["covariance"],
        tf.constant([[0.082568807339450]], dtype=tf.float64),
        atol=2e-10,
    )
    assert result.status is highdim.HighDimStatus.OK
    assert result.retained_filter.measure_convention == _convention()
    assert result.retained_filter.retained_axes == (0,)
    assert result.retained_filter.storage_kind == "gaussian_moment"


def test_one_step_scalar_builds_real_fixed_branch_tt_density_artifacts():
    result = highdim.FixedBranchSquaredTTFilter(_tt_filter_config()).log_likelihood(
        _scalar_model(),
        _theta0(),
        tf.constant([0.2], dtype=tf.float64),
    )
    step = result.steps[0]

    tf.debugging.assert_near(
        result.log_likelihood,
        tf.constant(-0.980376005178410, dtype=tf.float64),
        atol=2e-10,
    )
    assert isinstance(step.fit_result, highdim.FixedTTFitResult)
    assert isinstance(step.density, highdim.SquaredTTDensity)
    assert step.fit_result.status is highdim.HighDimStatus.OK
    assert step.density.branch_identity == highdim.SquaredTTDensity.expected_branch_identity(
        sqrt_tt=step.fit_result.fitted_tt,
        defensive_density=step.density.defensive_density,
        tau=tf.constant(1e-12, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-14, dtype=tf.float64),
        denominator_floor=tf.constant(1e-14, dtype=tf.float64),
        measure_convention=_convention(),
    )
    assert isinstance(step.diagnostics["adjacent_target_batch"], highdim.AdjacentTargetBatch)
    assert step.diagnostics["tt_artifact_status"] == highdim.HighDimStatus.OK.value
    assert step.retained_filter.density == step.density
    assert step.retained_filter.storage_kind == "gaussian_moment_plus_squared_tt_density"
    assert result.diagnostics["tt_artifacts_present"] is True


def test_two_step_scalar_kalman_evidence_and_retained_marginal():
    result = highdim.FixedBranchSquaredTTFilter(_filter_config()).log_likelihood(
        _scalar_model(),
        _theta0(),
        tf.constant([0.2, -0.1], dtype=tf.float64),
    )

    tf.debugging.assert_near(
        result.log_likelihood,
        tf.constant(-1.484707421612687, dtype=tf.float64),
        atol=2e-10,
    )
    tf.debugging.assert_near(
        result.retained_filter.diagnostics["mean"],
        tf.constant([-0.045960935616108], dtype=tf.float64),
        atol=2e-10,
    )
    tf.debugging.assert_near(
        result.retained_filter.diagnostics["covariance"],
        tf.constant([[0.068709910778876]], dtype=tf.float64),
        atol=2e-10,
    )
    assert len(result.steps) == 2
    assert result.steps[-1].retained_filter.branch_identity == result.retained_filter.branch_identity


def test_multivariate_kalman_evidence_and_marginal():
    model = highdim.LinearGaussianSSM(
        initial_mean=tf.constant([0.1, -0.2], dtype=tf.float64),
        initial_covariance=tf.constant([[1.0, 0.2], [0.2, 0.7]], dtype=tf.float64),
        transition_matrix=tf.constant([[0.8, 0.1], [-0.05, 0.6]], dtype=tf.float64),
        transition_covariance=tf.constant([[0.12, 0.02], [0.02, 0.10]], dtype=tf.float64),
        observation_matrix=tf.constant([[1.0, 0.3]], dtype=tf.float64),
        observation_covariance=tf.constant([[0.16]], dtype=tf.float64),
    )

    result = highdim.FixedBranchSquaredTTFilter(_filter_config(state_dim=2)).log_likelihood(
        model,
        _theta0(),
        tf.constant([[0.15], [-0.05]], dtype=tf.float64),
    )

    tf.debugging.assert_near(
        result.steps[0].log_normalizer,
        tf.constant(-1.070896331885871, dtype=tf.float64),
        atol=2e-10,
    )
    tf.debugging.assert_near(
        result.log_likelihood,
        tf.constant(-1.550790276990481, dtype=tf.float64),
        atol=2e-10,
    )
    tf.debugging.assert_near(
        result.retained_filter.diagnostics["mean"],
        tf.constant([0.05354198, -0.14118922], dtype=tf.float64),
        atol=1e-8,
    )
    tf.debugging.assert_near(
        result.retained_filter.diagnostics["covariance"],
        tf.constant(
            [[0.10101319, -0.05495946], [-0.05495946, 0.29692253]],
            dtype=tf.float64,
        ),
        atol=1e-8,
    )
    assert result.retained_filter.retained_axes == (0, 1)
    assert result.retained_filter.retained_coordinate_names == ("x0", "x1")


def test_affine_map_nonuniform_reference_recursive_fixture():
    coordinate_map = highdim.AffineCoordinateMap(
        offset=tf.constant([0.5], dtype=tf.float64),
        matrix=tf.constant([[2.0]], dtype=tf.float64),
    )
    physical, log_abs_det = coordinate_map.forward(tf.constant([[-1.0], [0.25]], dtype=tf.float64))
    reference, inverse_log_abs_det = coordinate_map.inverse(physical)
    fixture = highdim.affine_nonuniform_reference_scalar_fixture()

    tf.debugging.assert_near(
        physical,
        tf.constant([[-1.5], [1.0]], dtype=tf.float64),
        atol=1e-12,
    )
    tf.debugging.assert_near(reference, tf.constant([[-1.0], [0.25]], dtype=tf.float64), atol=1e-12)
    tf.debugging.assert_near(log_abs_det, tf.math.log(tf.constant([2.0, 2.0], dtype=tf.float64)), atol=1e-12)
    tf.debugging.assert_near(inverse_log_abs_det, -log_abs_det, atol=1e-12)
    tf.debugging.assert_near(
        fixture["log_evidence"],
        tf.constant(-0.980376007510876, dtype=tf.float64),
        atol=5e-10,
    )
    tf.debugging.assert_near(
        fixture["filter_mean"],
        tf.constant(0.183486242567321, dtype=tf.float64),
        atol=5e-10,
    )
    tf.debugging.assert_near(
        fixture["filter_variance"],
        tf.constant(0.082568800546224, dtype=tf.float64),
        atol=5e-10,
    )
    assert (
        abs(
            float(
                (
                    fixture["wrong_log_evidence_without_omega_division"]
                    - fixture["log_evidence"]
                ).numpy()
            )
        )
        > 1e-2
    )


def test_dense_scalar_nonlinear_oracle_is_quadrature_stable():
    coarse = highdim.dense_scalar_nonlinear_observation_oracle(
        observation=0.7,
        quadrature_order=128,
    )
    fine = highdim.dense_scalar_nonlinear_observation_oracle(
        observation=0.7,
        quadrature_order=192,
    )

    tf.debugging.assert_near(coarse, fine, atol=2e-10)


def test_retained_filter_storage_rejects_dense_product_when_over_budget():
    with pytest.raises(
        ValueError,
        match=highdim.HighDimStatus.RETAINED_STORAGE_BUDGET_EXCEEDED.value,
    ):
        highdim.gaussian_retained_filter(
            mean=tf.zeros([2], dtype=tf.float64),
            covariance=tf.eye(2, dtype=tf.float64),
            retained_axes=(0, 1),
            retained_coordinate_names=("x0", "x1"),
            measure_convention=_convention(),
            normalizer=tf.constant(1.0, dtype=tf.float64),
            storage_byte_budget=16,
            stage="storage-budget-test",
        )


def test_next_step_target_rejects_measure_mismatch():
    retained = highdim.gaussian_retained_filter(
        mean=tf.zeros([1], dtype=tf.float64),
        covariance=tf.eye(1, dtype=tf.float64),
        retained_axes=(0,),
        retained_coordinate_names=("x0",),
        measure_convention=_convention(),
        normalizer=tf.constant(1.0, dtype=tf.float64),
        storage_byte_budget=1_000,
        stage="measure-test",
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.RETAINED_MEASURE_MISMATCH.value):
        highdim.build_adjacent_target_batch(
            time_index=1,
            physical_points=tf.constant([[0.0]], dtype=tf.float64),
            reference_points=tf.constant([[0.0]], dtype=tf.float64),
            log_target=tf.constant([0.0], dtype=tf.float64),
            weights=tf.constant([1.0], dtype=tf.float64),
            measure_convention=_lebesgue_convention(),
            retained_filter=retained,
            expected_retained_axes=(0,),
        )


def test_next_step_target_rejects_retained_axes_mismatch():
    retained = highdim.gaussian_retained_filter(
        mean=tf.zeros([1], dtype=tf.float64),
        covariance=tf.eye(1, dtype=tf.float64),
        retained_axes=(0,),
        retained_coordinate_names=("x0",),
        measure_convention=_convention(),
        normalizer=tf.constant(1.0, dtype=tf.float64),
        storage_byte_budget=1_000,
        stage="axes-test",
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.RETAINED_AXES_MISMATCH.value):
        highdim.build_adjacent_target_batch(
            time_index=1,
            physical_points=tf.constant([[0.0]], dtype=tf.float64),
            reference_points=tf.constant([[0.0]], dtype=tf.float64),
            log_target=tf.constant([0.0], dtype=tf.float64),
            weights=tf.constant([1.0], dtype=tf.float64),
            measure_convention=_convention(),
            retained_filter=retained,
            expected_retained_axes=(1,),
        )


def test_deterministic_replay_same_seed_observations_branch_value_retained():
    model = _scalar_model()
    observations = tf.constant([0.2, -0.1], dtype=tf.float64)
    config = _filter_config(seed="deterministic-replay")
    filter_runner = highdim.FixedBranchSquaredTTFilter(config)

    first = filter_runner.log_likelihood(model, _theta0(), observations)
    second = filter_runner.log_likelihood(model, _theta0(), observations)

    assert first.branch_identity.hash == second.branch_identity.hash
    assert first.retained_filter.branch_identity.hash == second.retained_filter.branch_identity.hash
    tf.debugging.assert_equal(first.log_likelihood, second.log_likelihood)
    tf.debugging.assert_equal(
        first.retained_filter.diagnostics["mean"],
        second.retained_filter.diagnostics["mean"],
    )
    tf.debugging.assert_equal(
        first.retained_filter.diagnostics["covariance"],
        second.retained_filter.diagnostics["covariance"],
    )


def test_p10_stage_sanity_is_labeled_stage_sanity_only():
    result = highdim.FixedBranchSquaredTTFilter(_filter_config()).log_likelihood(
        _scalar_model(),
        _theta0(),
        tf.constant([0.2], dtype=tf.float64),
    )

    assert result.diagnostics["p10_stage_sanity"] == highdim.HighDimStatus.STAGE_SANITY_ONLY.value
    assert result.branch_identity.manifest.payload["scope"] == "phase4_exact_small_model_value_path"
    assert "adaptive_tt_cross" in result.branch_identity.manifest.payload["what_is_not_claimed"]
