from __future__ import annotations

import math

import tensorflow as tf

import bayesfilter.highdim as highdim


FIXTURE_ID = "p37.m2p6a.sv.scalar.fixed-target.v1"
FIT_FIXTURE_ID = "p37.m2p6a.sv.fixed-design-fit.degree64.v2"
FAILED_ORIGINAL_FIT_FIXTURE_ID = "p37.m2p6a.sv.fixed-design-fit.degree12.v1"
INITIAL_TARGET_ID = "p37.m2p6a.sv.initial.t0.v1"
TRANSITION_TARGET_ID = "p37.m2p6a.sv.transition.t1.v1"


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
    return tf.reshape(tf.constant((0.12, -0.08, 0.05), dtype=tf.float64), [-1, 1])


def _coordinate_map() -> highdim.AffineCoordinateMap:
    return highdim.AffineCoordinateMap(
        offset=tf.constant([0.0], dtype=tf.float64),
        matrix=tf.constant([[8.0]], dtype=tf.float64),
    )


def _basis(max_degree: int = 64) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), max_degree)],
        _convention(),
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


def _initial_cores(product_basis: highdim.ProductBasis) -> tuple[highdim.TTCore, ...]:
    return (
        highdim.TTCore(tf.ones([1, product_basis.bases[0].basis_dim, 1], dtype=tf.float64)),
    )


def _scalar_sv_filter_config(
    *,
    order: int = 321,
    seed: str = "p37-m2p6a-retained-t0",
) -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(_coordinate_map(),),
        measure_convention=_convention(),
        deterministic_seed=seed,
        fit_quadrature_order=order,
    )


def _retained_after_y0() -> highdim.RetainedFilter:
    result = highdim.FixedBranchSquaredTTFilter(_scalar_sv_filter_config()).log_likelihood(
        _model(),
        _theta(),
        _observations()[:1],
    )
    return result.retained_filter


def _fit_target(
    build_result: highdim.ScalarAdjacentTargetBuildResult,
    *,
    branch_seed: str,
) -> highdim.FixedTTFitResult:
    product_basis = _basis()
    return highdim.FixedTTFitter().fit(
        product_basis=product_basis,
        samples=highdim.FixedTTFitSampleBatch(
            points=build_result.target_batch.reference_points,
            target_values=build_result.target_batch.sqrt_target,
            weights=build_result.target_batch.weights,
        ),
        config=_fit_config(),
        initial_cores=_initial_cores(product_basis),
        branch_seed=branch_seed,
        measure_convention=_convention(),
    )


def _reference_weights(order: int) -> tuple[tf.Tensor, tf.Tensor]:
    nodes, weights = highdim.legendre_gauss_nodes_weights(order)
    return nodes[:, tf.newaxis], 0.5 * weights


def _audit_points_weights() -> tuple[tf.Tensor, tf.Tensor]:
    n_points = 149
    indices = tf.cast(tf.range(n_points), tf.float64)
    points = -1.0 + 2.0 * (indices + 0.5) / tf.cast(n_points, tf.float64)
    weights = tf.ones([n_points], dtype=tf.float64) / tf.cast(n_points, tf.float64)
    return points[:, tf.newaxis], weights


def _initial_build_result(order: int = 161) -> highdim.ScalarAdjacentTargetBuildResult:
    return highdim.scalar_nonlinear_initial_adjacent_target_batch(
        model=_model(),
        theta=_theta(),
        observation=_observations()[0],
        product_basis=_basis(),
        coordinate_map=_coordinate_map(),
        quadrature_order=order,
        measure_convention=_convention(),
        fixture_id=FIXTURE_ID,
        target_id=INITIAL_TARGET_ID,
        branch_seed="p37-m2p6a-initial-target",
    )


def _transition_build_result(order: int = 161) -> highdim.ScalarAdjacentTargetBuildResult:
    return highdim.scalar_nonlinear_transition_adjacent_target_batch(
        model=_model(),
        theta=_theta(),
        observation=_observations()[1],
        retained_filter=_retained_after_y0(),
        product_basis=_basis(),
        coordinate_map=_coordinate_map(),
        quadrature_order=order,
        measure_convention=_convention(),
        fixture_id=FIXTURE_ID,
        target_id=TRANSITION_TARGET_ID,
        branch_seed="p37-m2p6a-transition-target",
    )


def _target_result_like(
    build_result: highdim.ScalarAdjacentTargetBuildResult,
    *,
    quadrature_order: int,
    branch_seed: str,
    log_scale_shift: tf.Tensor,
) -> highdim.ScalarAdjacentTargetBuildResult:
    if build_result.diagnostics["target_kind"] == "initial":
        return highdim.scalar_nonlinear_initial_adjacent_target_batch(
            model=_model(),
            theta=_theta(),
            observation=_observations()[0],
            product_basis=_basis(),
            coordinate_map=_coordinate_map(),
            quadrature_order=quadrature_order,
            measure_convention=_convention(),
            fixture_id=FIXTURE_ID,
            target_id=INITIAL_TARGET_ID,
            branch_seed=branch_seed,
            log_scale_shift=log_scale_shift,
        )
    if build_result.diagnostics["target_kind"] == "transition":
        return highdim.scalar_nonlinear_transition_adjacent_target_batch(
            model=_model(),
            theta=_theta(),
            observation=_observations()[1],
            retained_filter=_retained_after_y0(),
            product_basis=_basis(),
            coordinate_map=_coordinate_map(),
            quadrature_order=quadrature_order,
            measure_convention=_convention(),
            fixture_id=FIXTURE_ID,
            target_id=TRANSITION_TARGET_ID,
            branch_seed=branch_seed,
            log_scale_shift=log_scale_shift,
        )
    raise AssertionError("unknown target kind")


def _manual_target_result_like(
    build_result: highdim.ScalarAdjacentTargetBuildResult,
    *,
    reference_points: tf.Tensor,
    weights: tf.Tensor,
    branch_seed: str,
) -> highdim.AdjacentTargetBatch:
    if build_result.diagnostics["target_kind"] == "initial":
        dense = highdim.scalar_nonlinear_initial_adjacent_target_batch(
            model=_model(),
            theta=_theta(),
            observation=_observations()[0],
            product_basis=_basis(),
            coordinate_map=_coordinate_map(),
            quadrature_order=161,
            measure_convention=_convention(),
            fixture_id=FIXTURE_ID,
            target_id=INITIAL_TARGET_ID,
            branch_seed=branch_seed,
            log_scale_shift=build_result.diagnostics["log_scale_shift"],
        )
    elif build_result.diagnostics["target_kind"] == "transition":
        dense = highdim.scalar_nonlinear_transition_adjacent_target_batch(
            model=_model(),
            theta=_theta(),
            observation=_observations()[1],
            retained_filter=_retained_after_y0(),
            product_basis=_basis(),
            coordinate_map=_coordinate_map(),
            quadrature_order=161,
            measure_convention=_convention(),
            fixture_id=FIXTURE_ID,
            target_id=TRANSITION_TARGET_ID,
            branch_seed=branch_seed,
            log_scale_shift=build_result.diagnostics["log_scale_shift"],
        )
    else:
        raise AssertionError("unknown target kind")
    physical_points, log_abs_det = _coordinate_map().forward(reference_points)
    if build_result.diagnostics["target_kind"] == "initial":
        log_physical_target = _model().initial_log_density(
            _theta(),
            physical_points,
        ) + _model().observation_log_density(
            _theta(),
            physical_points,
            _observations()[0],
            t=0,
        )
    else:
        retained = _retained_after_y0()
        previous_physical = retained.diagnostics["physical_points"]
        previous_reference = retained.diagnostics["reference_points"]
        previous_weights = retained.diagnostics["weights"]
        previous_log_density = retained.diagnostics["log_density_physical"]
        previous_physical_from_map, previous_log_abs_det = _coordinate_map().forward(previous_reference)
        tf.debugging.assert_near(previous_physical_from_map, previous_physical, atol=1e-10)
        current_count = int(physical_points.shape[0])
        previous_count = int(previous_physical.shape[0])
        next_points = tf.repeat(physical_points, repeats=previous_count, axis=0)
        previous_points = tf.tile(previous_physical, [current_count, 1])
        transition_log = tf.reshape(
            _model().transition_log_density(_theta(), previous_points, next_points, t=1),
            [current_count, previous_count],
        )
        log_predictive = tf.reduce_logsumexp(
            tf.math.log(previous_weights)[tf.newaxis, :]
            + previous_log_abs_det[tf.newaxis, :]
            + previous_log_density[tf.newaxis, :]
            + transition_log,
            axis=1,
        )
        log_physical_target = log_predictive + _model().observation_log_density(
            _theta(),
            physical_points,
            _observations()[1],
            t=1,
        )
    log_reference_target = log_physical_target + log_abs_det - tf.math.log(tf.constant(0.5, dtype=tf.float64))
    target_batch = highdim.build_adjacent_target_batch(
        time_index=int(dense.target_batch.time_index),
        physical_points=physical_points,
        reference_points=reference_points,
        log_target=log_reference_target,
        weights=weights,
        measure_convention=_convention(),
        retained_filter=None,
        log_scale_shift=build_result.diagnostics["log_scale_shift"],
    )
    return target_batch


def _weighted_rms(values: tf.Tensor, target: tf.Tensor, weights: tf.Tensor) -> tf.Tensor:
    return tf.sqrt(tf.reduce_sum(weights * tf.square(values - target)) / tf.reduce_sum(weights))


def _max_relative_square_error(predicted_sqrt: tf.Tensor, target_sqrt: tf.Tensor) -> tf.Tensor:
    predicted_square = tf.square(predicted_sqrt)
    target_square = tf.square(target_sqrt)
    denominator = tf.maximum(tf.constant(1e-12, dtype=tf.float64), tf.abs(target_square))
    return tf.reduce_max(tf.abs(predicted_square - target_square) / denominator)


def _assert_target_fit_passes(
    build_result: highdim.ScalarAdjacentTargetBuildResult,
    *,
    branch_seed: str,
) -> None:
    fit = _fit_target(build_result, branch_seed=branch_seed)
    assert fit.status is highdim.HighDimStatus.OK
    assert fit.holdout_residual is None
    train_prediction = fit.fitted_tt.evaluate(build_result.target_batch.reference_points)
    train_rms = _weighted_rms(
        train_prediction,
        build_result.target_batch.sqrt_target,
        build_result.target_batch.weights,
    )
    tf.debugging.assert_less_equal(train_rms, tf.constant(2e-5, dtype=tf.float64))

    tuning_holdout = _target_result_like(
        build_result,
        quadrature_order=121,
        branch_seed=f"{branch_seed}-tuning-holdout",
        log_scale_shift=build_result.diagnostics["log_scale_shift"],
    )
    tuning_prediction = fit.fitted_tt.evaluate(tuning_holdout.target_batch.reference_points)
    tuning_rms = _weighted_rms(
        tuning_prediction,
        tuning_holdout.target_batch.sqrt_target,
        tuning_holdout.target_batch.weights,
    )
    tf.debugging.assert_less_equal(tuning_rms, tf.constant(2e-5, dtype=tf.float64))

    audit_points, audit_weights = _audit_points_weights()
    audit = _manual_target_result_like(
        build_result,
        reference_points=audit_points,
        weights=audit_weights,
        branch_seed=f"{branch_seed}-audit-holdout",
    )
    audit_prediction = fit.fitted_tt.evaluate(audit.reference_points)
    audit_rms = _weighted_rms(
        audit_prediction,
        audit.sqrt_target,
        audit.weights,
    )
    relative_error = _max_relative_square_error(
        audit_prediction,
        audit.sqrt_target,
    )

    tf.debugging.assert_less_equal(audit_rms, tf.constant(2e-5, dtype=tf.float64))
    tf.debugging.assert_less_equal(relative_error, tf.constant(2e-3, dtype=tf.float64))
    assert math.isfinite(float(fit.core_update_statuses[0]["condition_number"]))
    assert build_result.diagnostics["max_log_scaling"] == "BAYESFILTER_EXTENSION"
    assert build_result.diagnostics["fixture_id"] == FIXTURE_ID
    assert FIT_FIXTURE_ID.endswith("degree64.v2")
    assert FAILED_ORIGINAL_FIT_FIXTURE_ID.endswith("degree12.v1")


def test_p30_sv_initial_fixed_design_tt_target_fit_matches_dense_oracle():
    _assert_target_fit_passes(_initial_build_result(), branch_seed="p37-m2p6a-initial-fit")


def test_p30_sv_transition_fixed_design_tt_target_fit_matches_dense_oracle():
    _assert_target_fit_passes(_transition_build_result(), branch_seed="p37-m2p6a-transition-fit")


def test_p30_sv_fixed_design_target_build_and_fit_replay_are_deterministic():
    left = _transition_build_result()
    right = _transition_build_result()

    assert left.branch_identity.hash.value == right.branch_identity.hash.value
    tf.debugging.assert_near(
        left.target_batch.sqrt_target,
        right.target_batch.sqrt_target,
        atol=0.0,
    )

    left_fit = _fit_target(left, branch_seed="p37-m2p6a-transition-replay")
    right_fit = _fit_target(right, branch_seed="p37-m2p6a-transition-replay")
    assert left_fit.branch_identity.hash.value == right_fit.branch_identity.hash.value
    tf.debugging.assert_near(
        left_fit.fitted_tt.evaluate(left.target_batch.reference_points),
        right_fit.fitted_tt.evaluate(right.target_batch.reference_points),
        atol=0.0,
    )


def test_p30_sv_transition_target_rejects_wrong_retained_storage_kind():
    retained = highdim.gaussian_retained_filter(
        mean=tf.constant([0.0], dtype=tf.float64),
        covariance=tf.eye(1, dtype=tf.float64),
        retained_axes=(2,),
        retained_coordinate_names=("x0",),
        measure_convention=_convention(),
        normalizer=tf.constant(1.0, dtype=tf.float64),
        storage_byte_budget=1_000,
        stage="bad_retained",
    )

    try:
        highdim.scalar_nonlinear_transition_adjacent_target_batch(
            model=_model(),
            theta=_theta(),
            observation=_observations()[1],
            retained_filter=retained,
            product_basis=_basis(),
            coordinate_map=_coordinate_map(),
            quadrature_order=161,
            measure_convention=_convention(),
            fixture_id=FIXTURE_ID,
            target_id=TRANSITION_TARGET_ID,
            branch_seed="p37-m2p6a-bad-retained",
        )
    except ValueError as exc:
        assert "scalar_dense_grid" in str(exc)
    else:
        raise AssertionError("expected scalar_dense_grid retained-filter rejection")
