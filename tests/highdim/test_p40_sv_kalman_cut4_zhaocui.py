from __future__ import annotations

from dataclasses import dataclass
import math

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter.nonlinear.svd_cut_tf import tf_svd_cut4_filter
from bayesfilter.structural import StatePartition, StructuralFilterConfig
from bayesfilter.structural_tf import TFStructuralStateSpace


def _panel_observations(dim: int) -> tf.Tensor:
    values = tf.constant(
        [
            [0.12, -0.08, 0.05],
            [-0.07, 0.11, -0.04],
        ],
        dtype=tf.float64,
    )
    return values[:, : int(dim)]


def _panel_parameters(dim: int) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    gamma = tf.constant([0.60, 0.52, 0.47], dtype=tf.float64)[: int(dim)]
    beta = tf.constant([0.40, 0.35, 0.45], dtype=tf.float64)[: int(dim)]
    sigma = tf.constant([1.00, 0.85, 0.75], dtype=tf.float64)[: int(dim)]
    return gamma, beta, sigma


def _scalar_sv_model() -> highdim.StochasticVolatilitySSM:
    return highdim.StochasticVolatilitySSM(sigma=1.0)


def _scalar_sv_theta() -> tf.Tensor:
    return _scalar_sv_model().unconstrained_from_physical(gamma=0.6, beta=0.4)


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _zhao_cui_scalar_tt_config(seed: str = "p40-zhao-cui-scalar-tt") -> highdim.FixedBranchFilterConfig:
    convention = _convention()
    product_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 32)],
        convention,
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
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
            holdout_tolerance=1e-4,
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
        fit_quadrature_order=101,
    )


@dataclass(frozen=True)
class _StateDimOnlyNonlinearModel:
    dim: int

    def state_dim(self) -> int:
        return int(self.dim)

    def parameter_dim(self) -> int:
        return 0

    def observation_dim(self) -> int:
        return 1


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p40_independent_panel_cut4_matches_kalman_mixture_projection(dim: int) -> None:
    gamma, beta, sigma = _panel_parameters(dim)
    observations = _panel_observations(dim)

    kalman = highdim.independent_panel_sv_mixture_kalman_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    )
    cut4 = highdim.independent_panel_sv_mixture_cut4_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    )

    atol = 5e-7 if dim < 3 else 2e-6
    tf.debugging.assert_near(cut4.log_likelihood, kalman.log_likelihood, atol=atol, rtol=atol)
    tf.debugging.assert_near(cut4.log_normalizers, kalman.log_normalizers, atol=atol, rtol=atol)
    tf.debugging.assert_near(cut4.mean_path, kalman.mean_path, atol=atol, rtol=atol)
    tf.debugging.assert_near(
        tf.linalg.diag_part(cut4.covariance_path),
        tf.linalg.diag_part(kalman.covariance_path),
        atol=2e-6,
        rtol=2e-6,
    )
    tf.debugging.assert_near(cut4.component_weights, kalman.component_weights, atol=3e-6, rtol=3e-6)
    tf.debugging.assert_near(
        tf.reduce_sum(cut4.component_weights, axis=1),
        tf.ones([2], dtype=tf.float64),
        atol=1e-12,
    )
    assert kalman.diagnostics["component_tuple_count"] == 7**dim
    assert cut4.diagnostics["component_tuple_count"] == 7**dim
    assert cut4.diagnostics["max_cut4_point_count"] == {1: 14, 2: 24, 3: 76}[dim]
    assert set(cut4.diagnostics["cut4_augmented_dims"]) == {{1: 3, 2: 4, 3: 6}[dim]}
    assert "not exact native SV likelihood" in cut4.diagnostics["non_claims"]
    assert "linear-Gaussian component fixtures do not validate nonlinear CUT4 accuracy" in cut4.diagnostics[
        "non_claims"
    ]


def test_p40_scalar_panel_kalman_ties_to_existing_scalar_cut4_and_dense_secondary_reference() -> None:
    observations = _panel_observations(1)
    kalman = highdim.independent_panel_sv_mixture_kalman_filter(
        observations,
        gamma=0.6,
        beta=0.4,
        sigma=1.0,
    )
    scalar_cut4 = highdim.scalar_sv_mixture_cut4_filter(
        _scalar_sv_model(),
        _scalar_sv_theta(),
        observations,
    )
    dense = highdim.scalar_sv_mixture_dense_reference(
        _scalar_sv_model(),
        _scalar_sv_theta(),
        observations,
        order=401,
        radius=8.0,
    )

    tf.debugging.assert_near(scalar_cut4.log_likelihood, kalman.log_likelihood, atol=1e-8, rtol=1e-8)
    tf.debugging.assert_near(scalar_cut4.log_normalizers, kalman.log_normalizers, atol=1e-8, rtol=1e-8)
    tf.debugging.assert_near(scalar_cut4.mean_path, kalman.mean_path[:, 0], atol=1e-8, rtol=1e-8)
    tf.debugging.assert_near(
        scalar_cut4.variance_path,
        tf.linalg.diag_part(kalman.covariance_path)[:, 0],
        atol=1e-8,
        rtol=1e-8,
    )
    tf.debugging.assert_near(dense.log_likelihood, kalman.log_likelihood, atol=2e-2, rtol=8e-3)
    assert dense.diagnostics["backend"] == "dense_transformed_sv_gaussian_mixture"


def test_p40_scalar_zhao_cui_native_sv_is_finite_but_not_same_target_as_mixture_kalman() -> None:
    observations = _panel_observations(1)
    zhao_cui = highdim.scalar_nonlinear_fixed_design_tt_value_path(
        _scalar_sv_model(),
        _scalar_sv_theta(),
        observations,
        _zhao_cui_scalar_tt_config(),
        fixture_id="p40.scalar-native-sv.zhao-cui-explanatory.v1",
        branch_seed_prefix="p40-zhao-cui-scalar-native-sv",
    )
    kalman = highdim.independent_panel_sv_mixture_kalman_filter(
        observations,
        gamma=0.6,
        beta=0.4,
        sigma=1.0,
    )

    assert bool(tf.math.is_finite(zhao_cui.log_likelihood).numpy())
    assert zhao_cui.diagnostics["value_path"] == "scalar_nonlinear_fixed_design_tt_value_path"
    assert bool(tf.math.is_finite(kalman.log_likelihood).numpy())
    assert abs(float((zhao_cui.log_likelihood - kalman.log_likelihood).numpy())) > 0.0
    assert "not exact native SV likelihood" in kalman.diagnostics["non_claims"]


@pytest.mark.parametrize("dim", [2, 3])
def test_p40_zhao_cui_sv_dimension_two_and_three_are_explicitly_blocked_from_scalar_lane(dim: int) -> None:
    with pytest.raises(TypeError, match="state_dim == 1"):
        highdim.scalar_nonlinear_fixed_design_tt_value_path(
            _StateDimOnlyNonlinearModel(dim),
            tf.zeros([0], dtype=tf.float64),
            _panel_observations(1),
            _zhao_cui_scalar_tt_config(seed=f"p40-zhao-cui-blocked-dim-{dim}"),
        )


def _generalized_sv_transformed_residual_cut4_model(
    *,
    observation: tf.Tensor,
    beta: float,
    mixture_component: int = 4,
    transform_offset: float = 1e-8,
) -> TFStructuralStateSpace:
    mixture = highdim.ksc_1998_log_chi_square_mixture()
    gamma_s = tf.constant(0.55, dtype=tf.float64)
    gamma_h = tf.constant(0.65, dtype=tf.float64)
    sigma_s = tf.constant(0.30, dtype=tf.float64)
    sigma_h = tf.constant(0.45, dtype=tf.float64)
    initial_covariance = tf.linalg.diag(
        tf.stack(
            [
                tf.square(sigma_s) / (1.0 - tf.square(gamma_s)),
                tf.square(sigma_h) / (1.0 - tf.square(gamma_h)),
            ]
        )
    )
    observed_scalar = tf.reshape(tf.convert_to_tensor(observation, dtype=tf.float64), [])
    beta_tensor = tf.constant(float(beta), dtype=tf.float64)
    mixture_mean = mixture.means[int(mixture_component)]
    mixture_variance = mixture.variances[int(mixture_component)]
    offset = tf.constant(float(transform_offset), dtype=tf.float64)

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        return tf.convert_to_tensor(previous_state, dtype=tf.float64)

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(state_points, dtype=tf.float64)
        if points.shape.rank == 1:
            points = points[tf.newaxis, :]
        residual = observed_scalar - beta_tensor * points[:, 0]
        transformed_residual = tf.math.log(tf.square(residual) + offset) - points[:, 1] - mixture_mean
        return transformed_residual[:, tf.newaxis]

    return TFStructuralStateSpace(
        partition=StatePartition(
            state_names=("s", "h"),
            stochastic_indices=(0, 1),
            deterministic_indices=(),
            innovation_dim=2,
        ),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="p40_generalized_sv_transformed_residual_cut4_diagnostic",
        ),
        initial_mean=tf.zeros([2], dtype=tf.float64),
        initial_covariance=initial_covariance,
        innovation_covariance=tf.eye(2, dtype=tf.float64),
        observation_covariance=tf.reshape(mixture_variance, [1, 1]),
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="p40_generalized_sv_transformed_residual_cut4_diagnostic",
    )


def _generalized_sv_moment_matched_kalman_one_step(
    *,
    observation: tf.Tensor,
    beta: float,
) -> dict[str, tf.Tensor]:
    mean = tf.zeros([2], dtype=tf.float64)
    covariance = tf.linalg.diag(tf.constant([0.30**2 / (1.0 - 0.55**2), 0.45**2 / (1.0 - 0.65**2)], dtype=tf.float64))
    observation_matrix = tf.constant([[float(beta), 0.0]], dtype=tf.float64)
    observation_noise = tf.exp(mean[1] + 0.5 * covariance[1, 1])
    innovation = tf.reshape(tf.convert_to_tensor(observation, dtype=tf.float64), [1]) - tf.linalg.matvec(
        observation_matrix,
        mean,
    )
    innovation_covariance = observation_matrix @ covariance @ tf.transpose(observation_matrix) + tf.reshape(
        observation_noise,
        [1, 1],
    )
    log_likelihood = -0.5 * (
        tf.math.log(tf.constant(2.0 * math.pi, dtype=tf.float64))
        + tf.math.log(innovation_covariance[0, 0])
        + tf.square(innovation[0]) / innovation_covariance[0, 0]
    )
    kalman_gain = covariance @ tf.transpose(observation_matrix) / innovation_covariance[0, 0]
    updated_mean = mean + tf.reshape(kalman_gain, [2]) * innovation[0]
    updated_covariance = covariance - kalman_gain @ observation_matrix @ covariance
    return {
        "log_likelihood": log_likelihood,
        "mean": updated_mean,
        "covariance": 0.5 * (updated_covariance + tf.transpose(updated_covariance)),
        "non_claim": tf.constant("moment_matched_raw_observation_approximation_not_exact"),
    }


def test_p40_generalized_sv_cut4_is_finite_and_zhao_cui_path_is_explicitly_blocked() -> None:
    observation = tf.constant(0.18, dtype=tf.float64)
    cut4_model = _generalized_sv_transformed_residual_cut4_model(observation=observation, beta=0.35)
    cut4 = tf_svd_cut4_filter(
        tf.constant([[0.0]], dtype=tf.float64),
        cut4_model,
        return_filtered=True,
    )
    moment_matched = _generalized_sv_moment_matched_kalman_one_step(
        observation=observation,
        beta=0.35,
    )

    assert bool(tf.math.is_finite(cut4.log_likelihood).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(cut4.filtered_means)).numpy())
    assert bool(tf.math.is_finite(moment_matched["log_likelihood"]).numpy())
    assert cut4.metadata.approximation_label == "p40_generalized_sv_transformed_residual_cut4_diagnostic"
    assert int(cut4.diagnostics.extra["augmented_dim"].numpy()) == 4
    assert int(cut4.diagnostics.extra["polynomial_degree"].numpy()) == 5
    assert (
        moment_matched["non_claim"].numpy().decode("utf-8")
        == "moment_matched_raw_observation_approximation_not_exact"
    )
    with pytest.raises(TypeError, match="state_dim == 1"):
        highdim.scalar_nonlinear_fixed_design_tt_value_path(
            _StateDimOnlyNonlinearModel(2),
            tf.zeros([0], dtype=tf.float64),
            tf.constant([[0.18], [0.11]], dtype=tf.float64),
            _zhao_cui_scalar_tt_config(seed="p40-generalized-sv-zhao-cui-blocked"),
        )


def test_p40_exports_are_highdim_scoped() -> None:
    assert "independent_panel_sv_mixture_kalman_filter" in highdim.__all__
    assert "independent_panel_sv_mixture_cut4_filter" in highdim.__all__
    assert "transformed_sv_panel_observations" in highdim.__all__
    import bayesfilter

    assert not hasattr(bayesfilter, "independent_panel_sv_mixture_kalman_filter")
