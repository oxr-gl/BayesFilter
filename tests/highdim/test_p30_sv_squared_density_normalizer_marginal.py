from __future__ import annotations

import tensorflow as tf

import bayesfilter.highdim as highdim


FIXTURE_ID = "p37.m2p6a.sv.scalar.fixed-target.v1"
FIT_FIXTURE_ID = "p37.m2p6a.sv.fixed-design-fit.degree64.v2"
INITIAL_TARGET_ID = "p37.m2p6a.sv.initial.t0.v1"
TRANSITION_TARGET_ID = "p37.m2p6a.sv.transition.t1.v1"
NORMALIZER_AUDIT_FIXTURE_ID = "p37.m2p6b.sv.normalizer-audit.gl257.v1"
RETAINED_DENSITY_AUDIT_FIXTURE_ID = "p37.m2p6b.sv.retained-density-audit.mid173.v1"


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


def _basis() -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 64)],
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


def _scalar_sv_filter_config() -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(_coordinate_map(),),
        measure_convention=_convention(),
        deterministic_seed="p37-m2p6a-retained-t0",
        fit_quadrature_order=321,
    )


def _retained_after_y0() -> highdim.RetainedFilter:
    result = highdim.FixedBranchSquaredTTFilter(_scalar_sv_filter_config()).log_likelihood(
        _model(),
        _theta(),
        _observations()[:1],
    )
    return result.retained_filter


def _build_result(kind: str, order: int = 161) -> highdim.ScalarAdjacentTargetBuildResult:
    if kind == "initial":
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
            branch_seed="p37-m2p6b-initial-target",
        )
    if kind == "transition":
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
            branch_seed="p37-m2p6b-transition-target",
        )
    raise AssertionError(f"unknown target kind: {kind}")


def _manual_target_batch(
    build_result: highdim.ScalarAdjacentTargetBuildResult,
    reference_points: tf.Tensor,
    weights: tf.Tensor,
) -> highdim.AdjacentTargetBatch:
    kind = build_result.diagnostics["target_kind"]
    physical_points, log_abs_det = _coordinate_map().forward(reference_points)
    if kind == "initial":
        log_physical_target = _model().initial_log_density(
            _theta(),
            physical_points,
        ) + _model().observation_log_density(
            _theta(),
            physical_points,
            _observations()[0],
            t=0,
        )
        time_index = 0
    elif kind == "transition":
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
        time_index = 1
    else:
        raise AssertionError(f"unknown target kind: {kind}")
    log_reference_target = log_physical_target + log_abs_det - tf.math.log(tf.constant(0.5, dtype=tf.float64))
    return highdim.build_adjacent_target_batch(
        time_index=time_index,
        physical_points=physical_points,
        reference_points=reference_points,
        log_target=log_reference_target,
        weights=weights,
        measure_convention=_convention(),
        retained_filter=None,
        log_scale_shift=build_result.diagnostics["log_scale_shift"],
    )


def _fit_result(
    build_result: highdim.ScalarAdjacentTargetBuildResult,
    branch_seed: str,
) -> highdim.FixedTTFitResult:
    product_basis = _basis()
    fit = highdim.FixedTTFitter().fit(
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
    assert fit.status is highdim.HighDimStatus.OK
    assert FIT_FIXTURE_ID.endswith("degree64.v2")
    return fit


def _density(fit: highdim.FixedTTFitResult, tau: float = 0.0) -> highdim.SquaredTTDensity:
    defensive = highdim.TensorProductReferenceDensity(_basis(), _convention())
    tau_tensor = tf.constant(tau, dtype=tf.float64)
    normalizer_floor = tf.constant(1e-12, dtype=tf.float64)
    denominator_floor = tf.constant(1e-12, dtype=tf.float64)
    identity = highdim.SquaredTTDensity.expected_branch_identity(
        sqrt_tt=fit.fitted_tt,
        defensive_density=defensive,
        tau=tau_tensor,
        normalizer_floor=normalizer_floor,
        denominator_floor=denominator_floor,
        measure_convention=_convention(),
    )
    return highdim.SquaredTTDensity(
        sqrt_tt=fit.fitted_tt,
        defensive_density=defensive,
        tau=tau_tensor,
        normalizer_floor=normalizer_floor,
        denominator_floor=denominator_floor,
        measure_convention=_convention(),
        branch_identity=identity,
    )


def _normalizer_audit_grid() -> tuple[tf.Tensor, tf.Tensor]:
    nodes, weights = highdim.legendre_gauss_nodes_weights(257)
    return nodes[:, tf.newaxis], 0.5 * weights


def _retained_density_audit_grid() -> tuple[tf.Tensor, tf.Tensor]:
    n_points = 173
    indices = tf.cast(tf.range(n_points), tf.float64)
    points = -1.0 + 2.0 * (indices + 0.25) / tf.cast(n_points, tf.float64)
    weights = tf.ones([n_points], dtype=tf.float64) / tf.cast(n_points, tf.float64)
    return points[:, tf.newaxis], weights


def _assert_m2p6a_lineage(build_result: highdim.ScalarAdjacentTargetBuildResult) -> None:
    assert build_result.diagnostics["fixture_id"] == FIXTURE_ID
    assert build_result.diagnostics["coordinate_map"] == _coordinate_map().manifest_payload()
    product_basis = build_result.diagnostics["product_basis"]
    assert product_basis["family"] == "ProductBasis"
    assert product_basis["dimension"] == 1
    assert product_basis["basis_dim_tuple"] == (65,)
    assert product_basis["convention"] == {
        "density_measure": "REFERENCE_MEASURE",
        "mass_measure": "REFERENCE_MEASURE",
        "reference_weight_name": "omega",
        "physical_coordinate_name": "r",
        "reference_coordinate_name": "z",
        "dtype_name": "float64",
    }
    assert product_basis["bases"][0]["family"] == "LegendreBasis1D"
    assert float(product_basis["bases"][0]["left"].numpy()) == -1.0
    assert float(product_basis["bases"][0]["right"].numpy()) == 1.0
    assert product_basis["bases"][0]["max_degree"] == 64
    assert product_basis["bases"][0]["normalized"] is True
    assert build_result.diagnostics["max_log_scaling"] == "BAYESFILTER_EXTENSION"
    assert tf.convert_to_tensor(build_result.diagnostics["log_scale_shift"]).shape.rank == 0


def _assert_density_gate(kind: str) -> None:
    build_result = _build_result(kind)
    _assert_m2p6a_lineage(build_result)
    expected_target_id = INITIAL_TARGET_ID if kind == "initial" else TRANSITION_TARGET_ID
    assert build_result.diagnostics["target_id"] == expected_target_id
    if kind == "transition":
        assert build_result.diagnostics["retained_filter_hash"] == _retained_after_y0().branch_identity.hash.value
    fit = _fit_result(build_result, branch_seed=f"p37-m2p6b-{kind}-fit")
    density = _density(fit, tau=0.0)

    normalizer_points, normalizer_weights = _normalizer_audit_grid()
    normalizer_oracle = _manual_target_batch(
        build_result,
        reference_points=normalizer_points,
        weights=normalizer_weights,
    )
    dense_normalizer = tf.reduce_sum(normalizer_oracle.weights * tf.square(normalizer_oracle.sqrt_target))
    tt_normalizer = density.sqrt_square_normalizer()
    full_normalizer = density.normalizer()

    tf.debugging.assert_near(tt_normalizer, full_normalizer, atol=1e-12)
    tf.debugging.assert_near(tt_normalizer, dense_normalizer, atol=5e-5, rtol=5e-4)
    assert NORMALIZER_AUDIT_FIXTURE_ID.endswith("gl257.v1")

    aux_density = _density(fit, tau=1e-12)
    tf.debugging.assert_near(
        aux_density.normalizer(),
        tt_normalizer + tf.constant(1e-12, dtype=tf.float64),
        atol=1e-18,
        rtol=1e-12,
    )

    retained_points, retained_weights = _retained_density_audit_grid()
    retained_oracle = _manual_target_batch(
        build_result,
        reference_points=retained_points,
        weights=retained_weights,
    )
    dense_values = tf.square(retained_oracle.sqrt_target) / dense_normalizer
    tt_values = density.normalized_retained_density_values((0,), retained_points)
    max_error = tf.reduce_max(tf.abs(tt_values - dense_values))
    retained_integral = tf.reduce_sum(retained_weights * tt_values)

    tf.debugging.assert_less_equal(max_error, tf.constant(5e-3, dtype=tf.float64))
    tf.debugging.assert_near(retained_integral, tf.constant(1.0, dtype=tf.float64), atol=5e-4)
    assert RETAINED_DENSITY_AUDIT_FIXTURE_ID.endswith("mid173.v1")
    assert not tf.reduce_any(
        tf.reduce_all(tf.equal(retained_points[:, tf.newaxis, :], normalizer_points[tf.newaxis, :, :]), axis=2)
    ).numpy()


def test_p30_sv_initial_squared_density_normalizer_and_retained_density_match_dense_oracle():
    _assert_density_gate("initial")


def test_p30_sv_transition_squared_density_normalizer_and_retained_density_match_dense_oracle():
    _assert_density_gate("transition")


def test_p30_sv_retained_density_rejects_metadata_or_conditional_substitute():
    build_result = _build_result("initial")
    fit = _fit_result(build_result, branch_seed="p37-m2p6b-substitute-rejection-fit")
    density = _density(fit)
    marginal = density.marginal_density([0])
    assert marginal.diagnostics["semantics"] == "source_style_squared_tt_marginal"

    points, _ = _retained_density_audit_grid()
    promoted = marginal.normalized_retained_density_values(points)

    assert "grid integration is diagnostic only" in marginal.diagnostics["note"]
    tf.debugging.assert_equal(tf.shape(promoted), tf.shape(points[:, 0]))
    tf.debugging.assert_greater(tf.reduce_max(promoted), tf.constant(0.0, dtype=tf.float64))


def test_p30_sv_retained_density_helper_requires_all_axes_retained():
    product = highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 0),
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 0),
        ],
        _convention(),
    )
    ftt = highdim.FunctionalTT(
        [
            highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64)),
            highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64)),
        ],
        product,
        _convention(),
    )
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    identity = highdim.SquaredTTDensity.expected_branch_identity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
    )
    density = highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=identity,
    )

    try:
        density.normalized_retained_density_values((0,), tf.zeros([3, 1], dtype=tf.float64))
    except NotImplementedError as exc:
        assert "all axes retained" in str(exc)
    else:
        raise AssertionError("expected all-retained helper rejection")
