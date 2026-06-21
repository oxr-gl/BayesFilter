from __future__ import annotations

import pytest
import tensorflow as tf
import tensorflow_probability as tfp

import bayesfilter.highdim as highdim


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _product_basis(degrees: tuple[int, ...]) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree) for degree in degrees],
        _convention(),
    )


def _branch_identity(
    ftt: highdim.FunctionalTT,
    defensive_density: highdim.TensorProductReferenceDensity,
    tau: float = 0.0,
    normalizer_floor: float = 1e-12,
    denominator_floor: float = 1e-12,
) -> highdim.BranchIdentity:
    return highdim.SquaredTTDensity.expected_branch_identity(
        sqrt_tt=ftt,
        defensive_density=defensive_density,
        tau=tf.constant(tau, dtype=tf.float64),
        normalizer_floor=tf.constant(normalizer_floor, dtype=tf.float64),
        denominator_floor=tf.constant(denominator_floor, dtype=tf.float64),
        measure_convention=_convention(),
    )


def _rank_two_tt(product: highdim.ProductBasis) -> highdim.FunctionalTT:
    return highdim.FunctionalTT(
        [
            highdim.TTCore(
                tf.constant(
                    [[[0.8, 0.3], [0.2, -0.1]]],
                    dtype=tf.float64,
                )
            ),
            highdim.TTCore(
                tf.constant(
                    [
                        [[1.1], [0.4]],
                        [[-0.2], [0.7]],
                    ],
                    dtype=tf.float64,
                )
            ),
        ],
        product,
        _convention(),
    )


def _dot_tt(product: highdim.ProductBasis) -> tuple[highdim.TTCore, ...]:
    del product
    return (
        highdim.TTCore(tf.constant([[[0.1, -0.05], [0.03, 0.02]]], dtype=tf.float64)),
        highdim.TTCore(tf.constant([[[0.02], [-0.04]], [[0.06], [0.01]]], dtype=tf.float64)),
    )


def _score_config(seed: str = "p37-score") -> highdim.FixedBranchFilterConfig:
    convention = _convention()
    product_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 48)],
        convention,
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=(1, 1),
            ridge=1e-12,
            max_sweeps=2,
            sweep_order=(0,),
            row_budget=512,
            column_budget=128,
            dense_matrix_byte_budget=200_000,
            normal_matrix_byte_budget=100_000,
            condition_number_warning=1e10,
            condition_number_veto=1e14,
            holdout_tolerance=5e-4,
        ),
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
        measure_convention=convention,
        deterministic_seed=seed,
        product_basis=product_basis,
        initial_cores=(
            highdim.TTCore(tf.ones([1, product_basis.bases[0].basis_dim, 1], dtype=tf.float64)),
        ),
        fit_quadrature_order=141,
    )


def _observations() -> tf.Tensor:
    return tf.constant([[0.12], [-0.07]], dtype=tf.float64)


def _physical_parameters() -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    gamma = tf.constant([0.60], dtype=tf.float64)
    beta = tf.constant([0.40], dtype=tf.float64)
    sigma = tf.constant([1.00], dtype=tf.float64)
    return gamma, beta, sigma


def _theta_from_physical(gamma: tf.Tensor, beta: tf.Tensor) -> tf.Tensor:
    standard_normal = tfp.distributions.Normal(
        loc=tf.constant(0.0, dtype=tf.float64),
        scale=tf.constant(1.0, dtype=tf.float64),
    )
    return tf.reshape(tf.stack([standard_normal.quantile(gamma), tf.math.log(beta)], axis=1), [-1])


def test_target_derivative_matches_finite_difference():
    theta = tf.constant(0.4, dtype=tf.float64)
    x = tf.constant([-0.5, 0.25, 0.9], dtype=tf.float64)
    y = tf.constant(0.1, dtype=tf.float64)
    h = tf.constant(1e-6, dtype=tf.float64)

    def log_target(theta_value: tf.Tensor) -> tf.Tensor:
        residual = y - theta_value * tf.sin(x)
        return -0.5 * tf.square(residual) / 0.25

    analytic = (y - theta * tf.sin(x)) * tf.sin(x) / 0.25
    centered = (log_target(theta + h) - log_target(theta - h)) / (2.0 * h)

    tf.debugging.assert_near(analytic, centered, atol=2e-10)


def test_environment_derivatives_match_finite_difference():
    product = _product_basis((1, 1))
    ftt = _rank_two_tt(product)
    dot_cores = _dot_tt(product)
    points = tf.constant([[-0.4, 0.2], [0.5, -0.25]], dtype=tf.float64)
    h = tf.constant(1e-6, dtype=tf.float64)
    plus = highdim.FunctionalTT(
        [
            highdim.TTCore(core.values + h * dot_core.values)
            for core, dot_core in zip(ftt.cores, dot_cores)
        ],
        product,
        _convention(),
    )
    minus = highdim.FunctionalTT(
        [
            highdim.TTCore(core.values - h * dot_core.values)
            for core, dot_core in zip(ftt.cores, dot_cores)
        ],
        product,
        _convention(),
    )

    analytic = highdim.tt_evaluation_derivative(product, points, ftt.cores, dot_cores)
    centered = (plus.evaluate(points) - minus.evaluate(points)) / (2.0 * h)

    tf.debugging.assert_near(analytic, centered, atol=1e-9)


def test_design_matrix_dotA_matches_finite_difference():
    product = _product_basis((1, 1))
    ftt = _rank_two_tt(product)
    dot_cores = _dot_tt(product)
    points = tf.constant([[-0.5, 0.1], [0.25, -0.4], [0.75, 0.2]], dtype=tf.float64)
    h = tf.constant(1e-6, dtype=tf.float64)
    fitter = highdim.FixedTTFitter()
    config = highdim.FixedTTFitConfig(
        ranks=(1, 2, 1),
        ridge=1e-8,
        max_sweeps=1,
        sweep_order=(0, 1),
        row_budget=100,
        column_budget=20,
        dense_matrix_byte_budget=100_000,
        normal_matrix_byte_budget=100_000,
        condition_number_warning=1e10,
        condition_number_veto=1e14,
        holdout_tolerance=1e6,
    )
    plus_cores = [
        highdim.TTCore(core.values + h * dot_core.values)
        for core, dot_core in zip(ftt.cores, dot_cores)
    ]
    minus_cores = [
        highdim.TTCore(core.values - h * dot_core.values)
        for core, dot_core in zip(ftt.cores, dot_cores)
    ]
    plus = fitter.build_core_update_system(
        product,
        points,
        tf.ones([3], dtype=tf.float64),
        tf.ones([3], dtype=tf.float64),
        plus_cores,
        core_index=1,
        config=config,
    ).design_matrix
    minus = fitter.build_core_update_system(
        product,
        points,
        tf.ones([3], dtype=tf.float64),
        tf.ones([3], dtype=tf.float64),
        minus_cores,
        core_index=1,
        config=config,
    ).design_matrix

    analytic = highdim.differentiate_design_matrix(product, points, ftt.cores, dot_cores, core_index=1)
    centered = (plus - minus) / (2.0 * h)

    tf.debugging.assert_near(analytic, centered, atol=1e-9)


def test_normal_equation_dotN_dotd_dotc_matches_finite_difference():
    design = tf.constant([[1.0, 0.2], [0.3, 1.1], [0.7, -0.4]], dtype=tf.float64)
    dot_design = tf.constant([[0.1, -0.05], [0.03, 0.02], [-0.04, 0.07]], dtype=tf.float64)
    target = tf.constant([0.4, -0.2, 0.7], dtype=tf.float64)
    dot_target = tf.constant([0.05, -0.03, 0.02], dtype=tf.float64)
    weights = tf.constant([1.0, 0.8, 1.2], dtype=tf.float64)
    ridge = 1e-4
    h = tf.constant(1e-6, dtype=tf.float64)

    normal = tf.matmul(design, design * weights[:, tf.newaxis], transpose_a=True)
    normal = normal + ridge * tf.eye(2, dtype=tf.float64)
    rhs = tf.linalg.matvec(design, weights * target, transpose_a=True)
    coeff = tf.linalg.solve(normal, rhs[:, tf.newaxis])[:, 0]
    result = highdim.fixed_design_lsq_derivative(
        design_matrix=design,
        target_values=target,
        weights=weights,
        coefficients=coeff,
        dot_target_values=dot_target,
        ridge=ridge,
        dot_design_matrix=dot_design,
    )

    def solve_for(eps: tf.Tensor) -> tf.Tensor:
        a = design + eps * dot_design
        y = target + eps * dot_target
        n = tf.matmul(a, a * weights[:, tf.newaxis], transpose_a=True)
        n = n + ridge * tf.eye(2, dtype=tf.float64)
        b = tf.linalg.matvec(a, weights * y, transpose_a=True)
        return tf.linalg.solve(n, b[:, tf.newaxis])[:, 0]

    centered = (solve_for(h) - solve_for(-h)) / (2.0 * h)

    assert result.status is highdim.HighDimStatus.OK
    tf.debugging.assert_near(result.dot_coefficients, centered, atol=1e-8)


def test_tt_evaluation_derivative_matches_finite_difference():
    product = _product_basis((1, 1))
    ftt = _rank_two_tt(product)
    dot_cores = _dot_tt(product)
    points = tf.constant([[-0.1, 0.3], [0.6, -0.5]], dtype=tf.float64)
    h = tf.constant(1e-6, dtype=tf.float64)

    analytic = highdim.tt_evaluation_derivative(product, points, ftt.cores, dot_cores)
    plus = highdim.FunctionalTT(
        [highdim.TTCore(c.values + h * dc.values) for c, dc in zip(ftt.cores, dot_cores)],
        product,
        _convention(),
    )
    minus = highdim.FunctionalTT(
        [highdim.TTCore(c.values - h * dc.values) for c, dc in zip(ftt.cores, dot_cores)],
        product,
        _convention(),
    )
    centered = (plus.evaluate(points) - minus.evaluate(points)) / (2.0 * h)

    tf.debugging.assert_near(analytic, centered, atol=1e-9)


def test_log_normalizer_derivative_matches_finite_difference():
    product = _product_basis((1, 1))
    ftt = _rank_two_tt(product)
    dot_cores = _dot_tt(product)
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    density = highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=_branch_identity(ftt, defensive),
    )
    h = tf.constant(1e-6, dtype=tf.float64)

    def log_normalizer(eps: tf.Tensor) -> tf.Tensor:
        perturbed = highdim.FunctionalTT(
            [highdim.TTCore(c.values + eps * dc.values) for c, dc in zip(ftt.cores, dot_cores)],
            product,
            _convention(),
        )
        local_density = highdim.SquaredTTDensity(
            sqrt_tt=perturbed,
            defensive_density=defensive,
            tau=tf.constant(0.0, dtype=tf.float64),
            normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
            denominator_floor=tf.constant(1e-12, dtype=tf.float64),
            measure_convention=_convention(),
            branch_identity=_branch_identity(perturbed, defensive),
        )
        return tf.math.log(local_density.normalizer())

    analytic = highdim.squared_tt_log_normalizer_derivative(density, dot_cores)
    centered = (log_normalizer(h) - log_normalizer(-h)) / (2.0 * h)

    tf.debugging.assert_near(analytic, centered, atol=1e-8)


def test_retained_filter_quotient_derivative_matches_finite_difference():
    numerator = tf.constant([2.0, -0.5], dtype=tf.float64)
    dot_numerator = tf.constant([0.3, 0.1], dtype=tf.float64)
    normalizer = tf.constant(1.7, dtype=tf.float64)
    dot_normalizer = tf.constant(-0.2, dtype=tf.float64)
    h = tf.constant(1e-6, dtype=tf.float64)

    analytic = highdim.retained_filter_quotient_derivative(
        numerator,
        dot_numerator,
        normalizer,
        dot_normalizer,
    )
    plus = (numerator + h * dot_numerator) / (normalizer + h * dot_normalizer)
    minus = (numerator - h * dot_numerator) / (normalizer - h * dot_normalizer)
    centered = (plus - minus) / (2.0 * h)

    tf.debugging.assert_near(analytic, centered, atol=2e-10)


def test_replay_tape_reconstructs_pre_and_post_update_core_states():
    manifest = highdim.BranchManifest("phase5-test-branch.v1", {"branch": "base"})
    identity = highdim.BranchIdentity(manifest=manifest, hash=manifest.sha256())
    tape = highdim.FixedBranchReplayTape(
        version="fixed_branch_replay_tape.phase5.v1",
        branch_identity=identity,
        entries=(
            {
                "manifest_version": "fixed_tt_fit.v1",
                "pre_replay_branch_hash": identity.hash.value,
                "initial_core_hashes": ("a" * 64,),
                "post_update_core_hashes": ("b" * 64,),
                "moving_basis_supported": False,
            },
        ),
    )

    tape.assert_matches_branch(identity)
    assert tape.manifest_payload()["branch_hash"] == identity.hash.value
    assert tape.sha256().value != identity.hash.value


def test_reverse_sweep_uses_post_update_right_environment():
    diagnostic = highdim.SweepDerivativeDiagnostics(
        time_index=0,
        sweep_index=1,
        sweep_direction="reverse",
        core_index=0,
        status=highdim.HighDimStatus.OK,
        condition_number=2.0,
        normal_matrix_hash="a" * 64,
        rhs_hash="b" * 64,
        coefficient_hash="c" * 64,
        environment_provenance={
            "right_environment_source": "post_update_right_core",
            "stale_environment_rejected": True,
        },
    )

    assert diagnostic.environment_provenance["right_environment_source"] == "post_update_right_core"
    assert diagnostic.environment_provenance["stale_environment_rejected"] is True


def test_replay_environment_cache_invalidation_is_enforced():
    manifest = highdim.BranchManifest("phase5-test-branch.v1", {"branch": "base"})
    identity = highdim.BranchIdentity(manifest=manifest, hash=manifest.sha256())
    other_manifest = highdim.BranchManifest("phase5-test-branch.v1", {"branch": "other"})
    other = highdim.BranchIdentity(manifest=other_manifest, hash=other_manifest.sha256())
    tape = highdim.FixedBranchReplayTape(
        version="fixed_branch_replay_tape.phase5.v1",
        branch_identity=identity,
        entries=({"environment_hash": "a" * 64},),
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.REPLAY_TAPE_MISMATCH.value):
        tape.assert_matches_branch(other)


def test_one_step_scalar_kalman_score_exact():
    log_evidence, score = highdim.scalar_one_step_lgssm_prior_mean_score()

    tf.debugging.assert_near(log_evidence, tf.constant(-0.980376005178410, dtype=tf.float64), atol=2e-10)
    tf.debugging.assert_near(score, tf.constant(0.183486238532110, dtype=tf.float64), atol=2e-10)


def test_two_step_scalar_kalman_score_exact():
    _, score = highdim.scalar_two_step_lgssm_transition_score()

    tf.debugging.assert_near(score, tf.constant(-0.241250978551728, dtype=tf.float64), atol=2e-10)


def test_scalar_nonlinear_dense_quadrature_score():
    log_evidence, score = highdim.scalar_nonlinear_dense_quadrature_score()

    tf.debugging.assert_near(log_evidence, tf.constant(-0.373000101795619, dtype=tf.float64), atol=5e-10)
    tf.debugging.assert_near(score, tf.constant(-0.608378439103854, dtype=tf.float64), atol=5e-10)


def test_branch_mismatch_invalidates_fd_row():
    row = highdim.make_finite_difference_row(
        parameter_index=0,
        h=1e-3,
        value_plus=tf.constant(1.1, dtype=tf.float64),
        value_minus=tf.constant(0.9, dtype=tf.float64),
        branch_hash_plus="a" * 64,
        branch_hash_minus="b" * 64,
        branch_hash_base="a" * 64,
        analytic_gradient=tf.constant(100.0, dtype=tf.float64),
    )
    table = highdim.FiniteDifferenceTable((row,))

    assert row.row_status is highdim.FiniteDifferenceRowStatus.INVALID_BRANCH_MISMATCH
    assert table.valid_rows() == ()
    assert bool(tf.math.is_nan(table.max_abs_error()).numpy())


def test_derivative_replay_rejects_adaptive_branch_change():
    config = highdim.FixedBranchDerivativeConfig(parameter_indices=(0,))
    base = highdim.fixed_branch_compatibility_hash(
        {
            "sample_set_hash": "s",
            "basis_hash": "b",
            "ranks": (1, 1),
            "sweep_order": (0,),
            "ridge": 1e-8,
        }
    )
    changed = highdim.fixed_branch_compatibility_hash(
        {
            "sample_set_hash": "s",
            "basis_hash": "b",
            "ranks": (1, 2, 1),
            "sweep_order": (0, 1),
            "ridge": 1e-8,
        }
    )
    row = highdim.make_finite_difference_row(
        parameter_index=config.parameter_indices[0],
        h=1e-3,
        value_plus=tf.constant(1.0, dtype=tf.float64),
        value_minus=tf.constant(0.99, dtype=tf.float64),
        branch_hash_plus=changed,
        branch_hash_minus=base,
        branch_hash_base=base,
        analytic_gradient=tf.constant(5.0, dtype=tf.float64),
    )

    assert row.row_status is highdim.FiniteDifferenceRowStatus.INVALID_BRANCH_MISMATCH


def test_unsupported_moving_basis_derivative_status():
    config = highdim.FixedBranchDerivativeConfig(
        parameter_indices=(0,),
        allow_moving_basis=True,
    )

    result = config.unsupported_status()

    assert result.status is highdim.HighDimStatus.UNSUPPORTED_MOVING_BASIS_DERIVATIVE


def test_derivative_solve_failure_status():
    design = tf.constant([[1.0, 1.0], [1.0, 1.0]], dtype=tf.float64)
    weights = tf.ones([2], dtype=tf.float64)
    target = tf.ones([2], dtype=tf.float64)
    coeff = tf.zeros([2], dtype=tf.float64)
    result = highdim.fixed_design_lsq_derivative(
        design_matrix=design,
        target_values=target,
        weights=weights,
        coefficients=coeff,
        dot_target_values=tf.ones([2], dtype=tf.float64),
        ridge=0.0,
        condition_number_veto=10.0,
    )

    assert result.status is highdim.HighDimStatus.DERIVATIVE_SOLVE_FAILURE


def test_scalar_fixed_design_tt_score_path_matches_same_branch_fd_for_exact_transformed_sv() -> None:
    observations = _observations()
    gamma, beta, sigma = _physical_parameters()
    theta = _theta_from_physical(gamma, beta)
    model = highdim.ExactTransformedSVSSM(sigma=sigma[0])
    z = highdim.exact_transformed_sv_observations(observations)
    config = _score_config("p37-score-exact")
    derivative_config = highdim.FixedBranchDerivativeConfig(parameter_indices=(0,))

    result = highdim.scalar_nonlinear_fixed_design_tt_score_path(
        model,
        theta,
        z,
        config,
        derivative_config,
        fixture_id="p37.score.exact-transformed.v1",
        initial_target_id="p37.score.exact.initial.v1",
        transition_target_id="p37.score.exact.transition.v1",
        branch_seed_prefix="p37-score-exact",
    )

    assert result.status is highdim.HighDimStatus.OK
    assert result.score.shape == (1,)
    assert result.finite_difference_table.valid_rows()
    assert result.diagnostics["score_path"] == "scalar_nonlinear_fixed_design_tt_score_path"
    assert result.diagnostics["fixed_branch_only"] is True
    assert float(result.finite_difference_table.max_abs_error().numpy()) < 5e-2
