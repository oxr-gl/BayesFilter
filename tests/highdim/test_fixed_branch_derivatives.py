from __future__ import annotations

from dataclasses import dataclass

import pytest
import tensorflow as tf
import tensorflow_probability as tfp

import bayesfilter.highdim as highdim
import bayesfilter.highdim.filtering as filtering_module


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


def _multistate_score_config(seed: str = "p81-multistate-score") -> highdim.FixedBranchFilterConfig:
    convention = _convention()
    product_basis = highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 3),
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 3),
        ],
        convention,
    )
    ranks = (1, 1, 1)
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=ranks,
            ridge=1e-10,
            max_sweeps=2,
            sweep_order=(0, 1),
            row_budget=256,
            column_budget=128,
            dense_matrix_byte_budget=200_000,
            normal_matrix_byte_budget=100_000,
            condition_number_warning=1e10,
            condition_number_veto=1e14,
            holdout_tolerance=5e-3,
        ),
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.zeros([2], dtype=tf.float64),
                matrix=2.0 * tf.eye(2, dtype=tf.float64),
            ),
        ),
        measure_convention=convention,
        deterministic_seed=seed,
        product_basis=product_basis,
        initial_cores=(
            highdim.TTCore(tf.ones([1, product_basis.bases[0].basis_dim, 1], dtype=tf.float64)),
            highdim.TTCore(tf.ones([1, product_basis.bases[1].basis_dim, 1], dtype=tf.float64)),
        ),
        fit_quadrature_order=5,
    )


@dataclass(frozen=True)
class _ParameterizedIndependentGaussianMultistateModel:
    dim: int = 2

    def parameter_dim(self) -> int:
        return 1

    def state_dim(self) -> int:
        return int(self.dim)

    def observation_dim(self) -> int:
        return int(self.dim)

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        del theta
        values = tf.convert_to_tensor(x0, dtype=tf.float64)
        return tf.reduce_sum(
            tfp.distributions.Normal(
                tf.constant(0.0, dtype=tf.float64),
                tf.constant(1.0, dtype=tf.float64),
            ).log_prob(values),
            axis=1,
        )

    def initial_log_density_parameter_score(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(x0, dtype=tf.float64)
        del theta
        return tf.zeros([tf.shape(values)[0], self.parameter_dim()], dtype=tf.float64)

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del t
        previous = tf.convert_to_tensor(x_prev, dtype=tf.float64)
        current = tf.convert_to_tensor(x_next, dtype=tf.float64)
        loc = 0.55 * previous + 0.08 * theta[0] * tf.square(previous)
        return tf.reduce_sum(
            tfp.distributions.Normal(loc, tf.constant(0.7, dtype=tf.float64)).log_prob(current),
            axis=1,
        )

    def transition_log_density_parameter_score(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del t
        previous = tf.convert_to_tensor(x_prev, dtype=tf.float64)
        current = tf.convert_to_tensor(x_next, dtype=tf.float64)
        loc = 0.55 * previous + 0.08 * theta[0] * tf.square(previous)
        d_loc = 0.08 * tf.square(previous)
        score = tf.reduce_sum((current - loc) * d_loc / tf.square(tf.constant(0.7, dtype=tf.float64)), axis=1)
        return score[:, tf.newaxis]

    def observation_log_density(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del t
        values = tf.convert_to_tensor(x_t, dtype=tf.float64)
        observation = tf.reshape(tf.convert_to_tensor(y_t, dtype=tf.float64), [self.dim])
        loc = 0.3 * values + 0.05 * theta[0] * tf.square(values)
        return tf.reduce_sum(
            tfp.distributions.Normal(loc, tf.constant(0.6, dtype=tf.float64)).log_prob(observation[tf.newaxis, :]),
            axis=1,
        )

    def observation_log_density_parameter_score(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del t
        values = tf.convert_to_tensor(x_t, dtype=tf.float64)
        observation = tf.reshape(tf.convert_to_tensor(y_t, dtype=tf.float64), [self.dim])
        loc = 0.3 * values + 0.05 * theta[0] * tf.square(values)
        d_loc = 0.05 * tf.square(values)
        score = tf.reduce_sum(
            (observation[tf.newaxis, :] - loc)
            * d_loc
            / tf.square(tf.constant(0.6, dtype=tf.float64)),
            axis=1,
        )
        return score[:, tf.newaxis]

    def manifest_payload(self) -> dict[str, object]:
        return {"family": "p81_parameterized_independent_gaussian_multistate_fixture", "dim": int(self.dim)}


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
    assert result.diagnostics["target_derivative_backend"] == "model_parameter_score_methods_only"
    assert float(result.finite_difference_table.max_abs_error().numpy()) < 5e-2


def test_scalar_fixed_design_tt_score_path_rejects_missing_manual_model_score_method() -> None:
    class _MissingObservationScore(highdim.ExactTransformedSVSSM):
        observation_log_density_parameter_score = None

    observations = _observations()
    gamma, beta, sigma = _physical_parameters()
    theta = _theta_from_physical(gamma, beta)
    model = _MissingObservationScore(sigma=sigma[0])
    z = highdim.exact_transformed_sv_observations(observations)
    config = _score_config("p37-score-no-fallback")
    derivative_config = highdim.FixedBranchDerivativeConfig(parameter_indices=(0,))

    with pytest.raises(ValueError, match="requires explicit model parameter-score methods"):
        highdim.scalar_nonlinear_fixed_design_tt_score_path(
            model,
            theta,
            z,
            config,
            derivative_config,
            fixture_id="p37.score.no-fallback.v1",
            initial_target_id="p37.score.no-fallback.initial.v1",
            transition_target_id="p37.score.no-fallback.transition.v1",
            branch_seed_prefix="p37-score-no-fallback",
        )


def test_stochastic_volatility_local_parameter_scores_match_tape_jacobians() -> None:
    model = highdim.StochasticVolatilitySSM(sigma=1.0)
    theta = model.unconstrained_from_physical(gamma=0.60, beta=0.40)
    previous = tf.constant([[-0.30], [0.20], [0.80]], dtype=tf.float64)
    current = tf.constant([[0.15], [-0.10], [0.40]], dtype=tf.float64)
    observation = tf.constant([0.25], dtype=tf.float64)

    def _jacobian(value_fn):
        with tf.GradientTape() as tape:
            tape.watch(theta)
            values = value_fn(theta)
        return tape.jacobian(values, theta)

    tf.debugging.assert_near(
        model.initial_log_density_parameter_score(theta, current),
        _jacobian(lambda th: model.initial_log_density(th, current)),
        atol=2e-10,
        rtol=2e-10,
    )
    tf.debugging.assert_near(
        model.transition_log_density_parameter_score(theta, previous, current, t=1),
        _jacobian(lambda th: model.transition_log_density(th, previous, current, t=1)),
        atol=2e-10,
        rtol=2e-10,
    )
    tf.debugging.assert_near(
        model.observation_log_density_parameter_score(theta, current, observation, t=1),
        _jacobian(lambda th: model.observation_log_density(th, current, observation, t=1)),
        atol=2e-10,
        rtol=2e-10,
    )


def test_transformed_sv_local_observation_scores_match_tape_jacobians() -> None:
    theta = highdim.StochasticVolatilitySSM(sigma=1.0).unconstrained_from_physical(
        gamma=0.60,
        beta=0.40,
    )
    values = tf.constant([[-0.35], [0.20], [0.75]], dtype=tf.float64)
    raw_observation = tf.constant([[0.25]], dtype=tf.float64)
    exact_observation = highdim.exact_transformed_sv_observations(raw_observation)[0]
    ksc_observation = highdim.transformed_sv_panel_observations(raw_observation)[0]

    for model, observation in (
        (highdim.ExactTransformedSVSSM(sigma=1.0), exact_observation),
        (highdim.KSCMixtureTransformedSVSSM(sigma=1.0), ksc_observation),
    ):
        with tf.GradientTape() as tape:
            tape.watch(theta)
            target = model.observation_log_density(theta, values, observation, t=1)
        expected = tape.jacobian(target, theta)
        actual = model.observation_log_density_parameter_score(theta, values, observation, t=1)
        tf.debugging.assert_near(actual, expected, atol=2e-10, rtol=2e-10)


def test_multistate_fixed_design_tt_score_path_matches_same_branch_fd_for_tiny_horizon0_fixture() -> None:
    model = _ParameterizedIndependentGaussianMultistateModel()
    theta = tf.constant([0.2], dtype=tf.float64)
    observations = tf.constant([[0.10, -0.04]], dtype=tf.float64)
    config = _multistate_score_config("p81-multistate-score-test")
    derivative_config = highdim.FixedBranchDerivativeConfig(
        parameter_indices=(0,),
        finite_difference_h=(3e-3, 1e-3),
        solve_condition_number_veto=1e16,
    )

    result = highdim.multistate_nonlinear_fixed_design_tt_score_path(
        model,
        theta,
        observations,
        config,
        derivative_config,
        fixture_id="p81.score.multistate.fixture.v1",
        initial_target_id="p81.score.multistate.initial.v1",
        transition_target_id="p81.score.multistate.transition.v1",
        branch_seed_prefix="p81-score-multistate",
    )

    assert result.status is highdim.HighDimStatus.OK
    assert result.score.shape == (1,)
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
    assert result.diagnostics["fixed_branch_only"] is True
    assert result.diagnostics["state_dim"] == 2
    assert float(result.finite_difference_table.max_abs_error().numpy()) < 2e-1


def test_multistate_fixed_design_tt_score_path_matches_same_branch_fd_for_tiny_two_row_fixture() -> None:
    model = _ParameterizedIndependentGaussianMultistateModel()
    theta = tf.constant([0.2], dtype=tf.float64)
    observations = tf.constant([[0.10, -0.04], [0.03, 0.08]], dtype=tf.float64)
    config = _multistate_score_config("p81-multistate-score-two-row-test")
    derivative_config = highdim.FixedBranchDerivativeConfig(
        parameter_indices=(0,),
        finite_difference_h=(3e-3, 1e-3),
        solve_condition_number_veto=1e16,
    )

    result = highdim.multistate_nonlinear_fixed_design_tt_score_path(
        model,
        theta,
        observations,
        config,
        derivative_config,
        fixture_id="p81.score.multistate.two-row.fixture.v1",
        initial_target_id="p81.score.multistate.initial.v1",
        transition_target_id="p81.score.multistate.transition.v1",
        branch_seed_prefix="p81-score-multistate-two-row",
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
    assert result.diagnostics["fixed_branch_only"] is True
    assert result.diagnostics["state_dim"] == 2
    assert result.diagnostics["observation_count"] == 2
    assert result.diagnostics["last_time_index"] == 1
    assert float(result.finite_difference_table.max_abs_error().numpy()) < 5e-1


def test_multistate_streaming_predictive_matches_dense_for_tiny_fixture() -> None:
    model = _ParameterizedIndependentGaussianMultistateModel()
    theta = tf.constant([0.2], dtype=tf.float64)
    observations = tf.constant([[0.10, -0.04]], dtype=tf.float64)
    config = _multistate_score_config("p81-multistate-streaming-parity")

    value_result = highdim.multistate_nonlinear_fixed_design_tt_value_path(
        model,
        theta,
        observations,
        config,
        fixture_id="p81.value.multistate.streaming-parity.v1",
        initial_target_id="p81.value.multistate.initial.v1",
        transition_target_id="p81.value.multistate.transition.v1",
        branch_seed_prefix="p81-value-multistate-streaming-parity",
    )
    retained = value_result.retained_filter
    reference_points, _ = filtering_module._tensor_product_reference_quadrature(
        config.product_basis,
        config.fit_quadrature_order,
    )
    current_physical, _ = config.coordinate_maps[0].forward(reference_points)
    previous_log_density = tf.convert_to_tensor(retained.diagnostics["log_density_physical"], dtype=tf.float64)
    previous_weights = tf.convert_to_tensor(retained.diagnostics["weights"], dtype=tf.float64)
    previous_reference = tf.convert_to_tensor(retained.diagnostics["reference_points"], dtype=tf.float64)
    previous_physical = tf.convert_to_tensor(retained.diagnostics["physical_points"], dtype=tf.float64)
    _, previous_log_abs_det = config.coordinate_maps[0].forward(previous_reference)
    log_reference_weight = filtering_module._log_uniform_reference_weight_density(config.product_basis)
    base_terms = tf.math.log(previous_weights) + previous_log_abs_det - log_reference_weight + previous_log_density

    dense = filtering_module._multistate_grid_predictive_log_density_from_retained(
        model=model,
        theta=theta,
        current_physical_points=current_physical,
        retained_filter=retained,
        coordinate_map=config.coordinate_maps[0],
        time_index=1,
    )
    streaming = filtering_module._multistate_grid_predictive_log_density_from_retained_streaming(
        model=model,
        theta=theta,
        current_physical_points=current_physical,
        previous_physical_points=previous_physical,
        base_previous_log_terms=base_terms,
        time_index=1,
        current_chunk_size=3,
        previous_chunk_size=4,
        chunk_byte_budget=100_000,
    )

    tf.debugging.assert_near(streaming, dense, atol=1e-10, rtol=1e-10)


def test_multistate_streaming_predictive_derivative_matches_dense_for_tiny_fixture() -> None:
    model = _ParameterizedIndependentGaussianMultistateModel()
    theta = tf.constant([0.2], dtype=tf.float64)
    observations = tf.constant([[0.10, -0.04]], dtype=tf.float64)
    config = _multistate_score_config("p81-multistate-streaming-derivative-parity")
    retained = highdim.multistate_nonlinear_fixed_design_tt_value_path(
        model,
        theta,
        observations,
        config,
        fixture_id="p81.value.multistate.streaming-derivative-parity.v1",
        initial_target_id="p81.value.multistate.initial.v1",
        transition_target_id="p81.value.multistate.transition.v1",
        branch_seed_prefix="p81-value-multistate-streaming-derivative-parity",
    ).retained_filter
    reference_points, _ = filtering_module._tensor_product_reference_quadrature(
        config.product_basis,
        config.fit_quadrature_order,
    )
    current_physical, _ = config.coordinate_maps[0].forward(reference_points)
    previous_log_density = tf.convert_to_tensor(retained.diagnostics["log_density_physical"], dtype=tf.float64)
    previous_weights = tf.convert_to_tensor(retained.diagnostics["weights"], dtype=tf.float64)
    previous_reference = tf.convert_to_tensor(retained.diagnostics["reference_points"], dtype=tf.float64)
    previous_physical = tf.convert_to_tensor(retained.diagnostics["physical_points"], dtype=tf.float64)
    _, previous_log_abs_det = config.coordinate_maps[0].forward(previous_reference)
    log_reference_weight = filtering_module._log_uniform_reference_weight_density(config.product_basis)
    base_terms = tf.math.log(previous_weights) + previous_log_abs_det - log_reference_weight + previous_log_density
    dot_previous = tf.linspace(
        tf.constant(-0.03, dtype=tf.float64),
        tf.constant(0.04, dtype=tf.float64),
        int(previous_reference.shape[0]),
    )

    dense_value, dense_dot = filtering_module._multistate_grid_predictive_log_density_and_derivative_from_retained(
        model=model,
        theta=theta,
        current_physical_points=current_physical,
        retained_filter=retained,
        coordinate_map=config.coordinate_maps[0],
        time_index=1,
        dot_retained_filter_values=dot_previous,
        parameter_index=0,
    )
    streaming_value, streaming_dot = filtering_module._multistate_grid_predictive_log_density_and_derivative_from_retained_streaming(
        model=model,
        theta=theta,
        current_physical_points=current_physical,
        previous_physical_points=previous_physical,
        base_previous_log_terms=base_terms,
        dot_previous_density=dot_previous,
        time_index=1,
        parameter_index=0,
        current_chunk_size=3,
        previous_chunk_size=4,
        chunk_byte_budget=100_000,
    )

    tf.debugging.assert_near(streaming_value, dense_value, atol=1e-10, rtol=1e-10)
    tf.debugging.assert_near(streaming_dot, dense_dot, atol=1e-10, rtol=1e-10)


def test_multistate_score_path_uses_streaming_fallback_when_dense_gate_trips(monkeypatch) -> None:
    model = _ParameterizedIndependentGaussianMultistateModel()
    theta = tf.constant([0.2], dtype=tf.float64)
    observations = tf.constant([[0.10, -0.04], [0.03, 0.08]], dtype=tf.float64)
    config = _multistate_score_config("p81-multistate-score-streaming-fallback")
    derivative_config = highdim.FixedBranchDerivativeConfig(
        parameter_indices=(0,),
        finite_difference_h=(3e-3,),
        solve_condition_number_veto=1e16,
    )
    calls = {"value": 0, "derivative": 0}
    original_value_streaming = filtering_module._multistate_grid_predictive_log_density_from_retained_streaming
    original_derivative_streaming = (
        filtering_module._multistate_grid_predictive_log_density_and_derivative_from_retained_streaming
    )
    original_budget = filtering_module._check_pairwise_transition_tensor_budget

    def tiny_dense_budget(current_count: int, previous_count: int, state_dim: int, byte_budget: int = 256_000_000) -> None:
        del byte_budget
        return original_budget(current_count, previous_count, state_dim, byte_budget=1024)

    def counted_value_streaming(*args, **kwargs):
        calls["value"] += 1
        return original_value_streaming(*args, **kwargs)

    def counted_derivative_streaming(*args, **kwargs):
        calls["derivative"] += 1
        return original_derivative_streaming(*args, **kwargs)

    monkeypatch.setattr(filtering_module, "_check_pairwise_transition_tensor_budget", tiny_dense_budget)
    monkeypatch.setattr(
        filtering_module,
        "_multistate_grid_predictive_log_density_from_retained_streaming",
        counted_value_streaming,
    )
    monkeypatch.setattr(
        filtering_module,
        "_multistate_grid_predictive_log_density_and_derivative_from_retained_streaming",
        counted_derivative_streaming,
    )

    result = highdim.multistate_nonlinear_fixed_design_tt_score_path(
        model,
        theta,
        observations,
        config,
        derivative_config,
        fixture_id="p81.score.multistate.streaming-fallback.v1",
        initial_target_id="p81.score.multistate.initial.v1",
        transition_target_id="p81.score.multistate.transition.v1",
        branch_seed_prefix="p81-score-multistate-streaming-fallback",
    )

    assert result.status is highdim.HighDimStatus.OK
    assert result.finite_difference_table.valid_rows()
    assert calls["value"] >= 1
    assert calls["derivative"] >= 1
