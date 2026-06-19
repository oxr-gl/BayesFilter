from __future__ import annotations

import json
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter.nonlinear.fixed_sgqf_derivatives_tf import tf_fixed_sgqf_same_branch_signature, tf_fixed_sgqf_score
from bayesfilter.nonlinear.fixed_sgqf_structural_adapter_tf import tf_predator_prey_to_fixed_sgqf_model
from bayesfilter.nonlinear.fixed_sgqf_tf import TFFixedSGQFBranchConfig, tf_fixed_sgqf_cloud, tf_fixed_sgqf_filter
from bayesfilter.nonlinear.sigma_points_tf import tf_svd_sigma_point_filter
from bayesfilter.nonlinear.svd_cut_tf import tf_svd_cut4_filter
from bayesfilter.structural import StatePartition, StructuralFilterConfig
from bayesfilter.structural_tf import TFStructuralStateSpace


DTYPE = tf.float64
TARGET_MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-predator-prey-filtering-target-manifest-2026-06-08.json"
)
REGISTRY_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p47-target-registry-2026-06-08.json")


def _model() -> highdim.PredatorPreySSM:
    return highdim.p30_predator_prey_fixture_model()


def _theta() -> tf.Tensor:
    return _model().true_parameters()


def _observations() -> tf.Tensor:
    return tf.constant([[51.0, 4.6], [80.0, 3.8]], dtype=DTYPE)


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _basis(dim: int, degree: int) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree) for _ in range(dim)],
        _convention(),
    )


def _initial_cores(product_basis: highdim.ProductBasis, ranks: tuple[int, ...]) -> tuple[highdim.TTCore, ...]:
    return tuple(
        highdim.TTCore(tf.ones([ranks[axis], basis.basis_dim, ranks[axis + 1]], dtype=DTYPE))
        for axis, basis in enumerate(product_basis.bases)
    )


def _tt_config(seed: str, *, order: int = 7) -> highdim.FixedBranchFilterConfig:
    model = _model()
    dim = model.state_dim()
    product_basis = _basis(dim, degree=max(7, int(order) - 1))
    ranks = (1, 6, 1)
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=ranks,
            ridge=1e-10,
            max_sweeps=4,
            sweep_order=tuple(range(dim)),
            row_budget=800,
            column_budget=160,
            dense_matrix_byte_budget=600_000,
            normal_matrix_byte_budget=160_000,
            condition_number_warning=1e11,
            condition_number_veto=1e16,
            holdout_tolerance=2e-2,
        ),
        density_tau=1e-12,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.constant([65.0, 6.0], dtype=DTYPE),
                matrix=tf.linalg.diag(tf.constant([45.0, 6.0], dtype=DTYPE)),
            ),
        ),
        measure_convention=_convention(),
        deterministic_seed=seed,
        product_basis=product_basis,
        initial_cores=_initial_cores(product_basis, ranks),
        fit_quadrature_order=int(order),
    )


def _reference_grid(config: highdim.FixedBranchFilterConfig) -> tuple[tf.Tensor, tf.Tensor]:
    nodes_1d, weights_1d = highdim.legendre_gauss_nodes_weights(config.fit_quadrature_order)
    axis_nodes = []
    axis_weights = []
    for basis in config.product_basis.bases:
        half_length = 0.5 * basis.domain.length
        midpoint = 0.5 * (basis.domain.left + basis.domain.right)
        axis_nodes.append(midpoint + half_length * nodes_1d)
        axis_weights.append(0.5 * weights_1d)
    mesh_nodes = tf.meshgrid(*axis_nodes, indexing="ij")
    mesh_weights = tf.meshgrid(*axis_weights, indexing="ij")
    points = tf.stack([tf.reshape(axis, [-1]) for axis in mesh_nodes], axis=1)
    weights = tf.ones([tf.shape(points)[0]], dtype=DTYPE)
    for axis_weight in mesh_weights:
        weights = weights * tf.reshape(axis_weight, [-1])
    return points, weights


def _log_uniform_reference_weight_density(product_basis: highdim.ProductBasis) -> tf.Tensor:
    log_density = tf.constant(0.0, dtype=DTYPE)
    for basis in product_basis.bases:
        log_density = log_density - tf.math.log(basis.domain.length)
    return log_density


def _grid(config: highdim.FixedBranchFilterConfig) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    reference_points, reference_weights = _reference_grid(config)
    physical_points, log_abs_det = config.coordinate_maps[0].forward(reference_points)
    return reference_points, reference_weights, physical_points, log_abs_det


def _logsumexp_weighted(log_values: tf.Tensor, weights: tf.Tensor) -> tf.Tensor:
    max_value = tf.reduce_max(log_values)
    return tf.math.log(tf.reduce_sum(weights * tf.exp(log_values - max_value))) + max_value


def _dense_reference(order: int = 7) -> dict[str, tf.Tensor]:
    model = _model()
    theta = _theta()
    observations = _observations()
    config = _tt_config("p47-predator-prey-dense-reference", order=order)
    _, weights, physical_points, log_abs_det = _grid(config)
    log_reference_weight = _log_uniform_reference_weight_density(config.product_basis)
    log_terms = []
    means = []
    covariances = []
    log_posterior_physical = None

    for time_index in range(int(observations.shape[0])):
        if time_index == 0:
            log_unnormalized = model.initial_log_density(
                theta,
                physical_points,
            ) + model.observation_log_density(
                theta,
                physical_points,
                observations[time_index],
                t=time_index,
            )
        else:
            count = int(physical_points.shape[0])
            next_points = tf.repeat(physical_points, repeats=count, axis=0)
            previous_points = tf.tile(physical_points, [count, 1])
            transition_log = tf.reshape(
                model.transition_log_density(
                    theta,
                    previous_points,
                    next_points,
                    t=time_index,
                ),
                [count, count],
            )
            log_predictive = tf.reduce_logsumexp(
                tf.math.log(weights)[tf.newaxis, :]
                + log_abs_det[tf.newaxis, :]
                - log_reference_weight
                + log_posterior_physical[tf.newaxis, :]
                + transition_log,
                axis=1,
            )
            log_unnormalized = log_predictive + model.observation_log_density(
                theta,
                physical_points,
                observations[time_index],
                t=time_index,
            )
        log_increment = _logsumexp_weighted(log_unnormalized + log_abs_det - log_reference_weight, weights)
        log_posterior_physical = log_unnormalized - log_increment
        mass = weights * tf.exp(log_posterior_physical + log_abs_det - log_reference_weight)
        mean = tf.reduce_sum(physical_points * mass[:, tf.newaxis], axis=0)
        centered = physical_points - mean[tf.newaxis, :]
        covariance = tf.einsum("n,ni,nj->ij", mass, centered, centered)
        log_terms.append(log_increment)
        means.append(mean)
        covariances.append(covariance)

    return {
        "log_likelihood": tf.reduce_sum(tf.stack(log_terms)),
        "log_normalizers": tf.stack(log_terms),
        "mean_path": tf.stack(means),
        "covariance_path": tf.stack(covariances),
    }


def _zhaocui_result(order: int = 7) -> highdim.FixedBranchFilterResult:
    return highdim.multistate_nonlinear_fixed_design_tt_value_path(
        _model(),
        _theta(),
        _observations(),
        _tt_config("p47-predator-prey-zhaocui-lower-rung", order=order),
        fixture_id="p47.predator-prey.lower-rung.v1",
        branch_seed_prefix="p47-predator-prey-lower-rung",
        retained_moment_order=order,
        retained_propagation_order=order,
    )


def _structural_closure(theta: tf.Tensor | None = None) -> TFStructuralStateSpace:
    model = _model()
    theta = _theta() if theta is None else tf.convert_to_tensor(theta, dtype=DTYPE)
    process_chol = tf.linalg.cholesky(model.process_covariance)

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = tf.convert_to_tensor(previous_state, dtype=DTYPE)
        innov = tf.convert_to_tensor(innovation, dtype=DTYPE)
        return model.transition_mean(theta, previous) + innov @ tf.transpose(process_chol)

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        return tf.convert_to_tensor(state_points, dtype=DTYPE)

    return TFStructuralStateSpace(
        partition=StatePartition(
            state_names=("prey", "predator"),
            stochastic_indices=(0, 1),
            deterministic_indices=(),
            innovation_dim=2,
        ),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="p47_m5_predator_prey_additive_gaussian_closure",
        ),
        initial_mean=model.initial_mean,
        initial_covariance=model.initial_covariance,
        innovation_covariance=tf.eye(2, dtype=DTYPE),
        observation_covariance=model.observation_covariance,
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="p47_m5_predator_prey_additive_gaussian_closure",
    )


def _cut4_result():
    return tf_svd_cut4_filter(
        _observations(),
        _structural_closure(),
        innovation_floor=tf.constant(1e-12, dtype=DTYPE),
        return_filtered=True,
    )


def _fixed_sgqf_result(theta: tf.Tensor | None = None, *, sparse_level: int = 2):
    model = _model()
    parameter = _theta() if theta is None else tf.convert_to_tensor(theta, dtype=DTYPE)
    adapted = tf_predator_prey_to_fixed_sgqf_model(model, parameter)
    assert adapted.eligible and adapted.model is not None
    cloud = tf_fixed_sgqf_cloud(dim=2, sparse_level=sparse_level)
    result = tf_fixed_sgqf_filter(
        _observations(),
        adapted.model,
        cloud=cloud,
        branch_config=TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10),
        return_filtered=True,
    )
    return adapted, cloud, result



def _ukf_result(theta: tf.Tensor | None = None):
    parameter = _theta() if theta is None else tf.convert_to_tensor(theta, dtype=DTYPE)
    structural = _structural_closure(theta=parameter)
    result = tf_svd_sigma_point_filter(
        _observations(),
        structural,
        backend="tf_svd_ukf",
        innovation_floor=tf.constant(1e-12, dtype=DTYPE),
        return_filtered=True,
    )
    return structural, result



def _dense_value_and_score(theta: tf.Tensor | None = None, *, order: int = 7) -> tuple[dict[str, tf.Tensor], tf.Tensor]:
    parameter = _theta() if theta is None else tf.convert_to_tensor(theta, dtype=DTYPE)

    def value_fn(current_theta: tf.Tensor) -> tf.Tensor:
        model = _model()
        observations = _observations()
        config = _tt_config("p47-predator-prey-dense-reference-score", order=order)
        _, weights, physical_points, log_abs_det = _grid(config)
        log_reference_weight = _log_uniform_reference_weight_density(config.product_basis)
        log_terms = []
        log_posterior_physical = None

        for time_index in range(int(observations.shape[0])):
            if time_index == 0:
                log_unnormalized = model.initial_log_density(
                    current_theta,
                    physical_points,
                ) + model.observation_log_density(
                    current_theta,
                    physical_points,
                    observations[time_index],
                    t=time_index,
                )
            else:
                count = int(physical_points.shape[0])
                next_points = tf.repeat(physical_points, repeats=count, axis=0)
                previous_points = tf.tile(physical_points, [count, 1])
                transition_log = tf.reshape(
                    model.transition_log_density(
                        current_theta,
                        previous_points,
                        next_points,
                        t=time_index,
                    ),
                    [count, count],
                )
                log_predictive = tf.reduce_logsumexp(
                    tf.math.log(weights)[tf.newaxis, :]
                    + log_abs_det[tf.newaxis, :]
                    - log_reference_weight
                    + log_posterior_physical[tf.newaxis, :]
                    + transition_log,
                    axis=1,
                )
                log_unnormalized = log_predictive + model.observation_log_density(
                    current_theta,
                    physical_points,
                    observations[time_index],
                    t=time_index,
                )
            log_increment = _logsumexp_weighted(log_unnormalized + log_abs_det - log_reference_weight, weights)
            log_posterior_physical = log_unnormalized - log_increment
            log_terms.append(log_increment)
        return tf.reduce_sum(tf.stack(log_terms))

    theta_tensor = tf.convert_to_tensor(parameter, dtype=DTYPE)
    with tf.GradientTape() as tape:
        tape.watch(theta_tensor)
        log_likelihood = value_fn(theta_tensor)
    score = tape.gradient(log_likelihood, theta_tensor)
    if score is None:
        raise AssertionError("Dense predator-prey score tape returned None")
    return _dense_reference(order=order), score



def _matched_settings(**overrides: object) -> dict[str, object]:
    settings = {
        "observations_seed": 4401,
        "truth_seed": 4402,
        "prior": "theta_uniform_box_x0_normal",
        "parameter_box": tuple(_model().parameter_box().values()),
        "initial_state_prior": "N((50,5), I_2)",
        "delta": 2.0,
        "rk4_internal_step": 0.1,
        "process_covariance": "4 I_2",
        "observation_covariance": "4 I_2",
        "dtype": "tf.float64",
        "target_id": "p47.predator-prey.lower-rung.v1",
        "observations": "near_rk4_replayable_two_observation_path",
        "theta": "p30_true_parameters",
        "basis_family": "legendre",
        "basis_size": 8,
        "nominal_rank_cap": 6,
        "quadrature_order": 7,
        "sweep_count": 4,
        "stopping_tolerance": 1e-8,
        "sample_count": 128,
        "wall_time_accounting_policy": "include_target_evaluations_and_ode_solves",
    }
    settings.update(overrides)
    return settings



def _metrics(**overrides: object) -> dict[str, float]:
    metrics = {
        "q_ess_linear_0p50": 42.0,
        "q_ess_nonlinear_0p50": 43.0,
        "wall_time_linear_seconds": 2.0,
        "wall_time_nonlinear_seconds": 4.0,
        "delta_ess": 1.0,
        "delta_cost": -10.25,
        "trajectory_rmse_linear": 0.5,
        "trajectory_rmse_nonlinear": 0.4,
    }
    metrics.update(overrides)
    return metrics


def test_p47_m5_manifest_and_registry_split_reference_from_production() -> None:
    manifest = json.loads(TARGET_MANIFEST_PATH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    rows = {row["target_id"]: row for row in registry["rows"]}

    assert manifest["target_class"] == "lower_rung_reference_filtering_not_production"
    assert manifest["m1_route_label"] == "documented-deviation fixed-design substitute"
    assert manifest["production_state"].startswith("blocked_until")
    assert "PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING" in manifest["production_prerequisites"]
    assert "not nonlinear preconditioning usefulness" in manifest["nonclaims"]
    assert manifest["promoted_observation_fixture"] == "near_rk4_replayable_two_observation_path"
    assert (
        manifest["diagnostic_stress_fixture_not_promoted"]["status"]
        == "diagnostic_transition_approximation_stress_not_reference_filtering_pass"
    )

    lower = rows["predator_prey_reference_filtering"]
    production = rows["predator_prey_production_filtering"]
    assert lower["pass_tokens"] == ["PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING"]
    assert "PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING" in lower["forbidden_tokens"]
    assert "PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING" in production["prerequisite_tokens"]


def test_p47_m5_predator_prey_domain_policy_parameter_box_and_reference_grid() -> None:
    model = _model()
    _, _, physical_points, _ = _grid(_tt_config("p47-predator-prey-domain-grid", order=7))
    diagnostics = model.domain_diagnostics(physical_points)

    assert model.state_dim() == 2
    assert model.observation_dim() == 2
    assert model.parameter_dim() == 6
    assert model.validate_parameter_box(_theta())
    assert diagnostics["domain_policy"] == "diagnose_negative_after_noise"
    assert diagnostics["has_negative_state"] is False
    assert float(diagnostics["min_state"].numpy()) > 0.0


def test_p47_m5_zhaocui_matches_dense_reference_value_and_state_moments() -> None:
    reference = _dense_reference(order=7)
    result = _zhaocui_result(order=7)
    log_normalizers = tf.stack([step.log_normalizer for step in result.steps])
    mean_path = tf.stack([step.diagnostics["retained_mean"] for step in result.steps])
    covariance_path = tf.stack([step.diagnostics["retained_covariance"] for step in result.steps])
    state_error = tf.reduce_max(tf.abs(mean_path - reference["mean_path"]), axis=0)
    covariance_error = tf.reduce_max(tf.abs(covariance_path - reference["covariance_path"]))

    assert result.status is highdim.HighDimStatus.OK
    assert result.diagnostics["value_path"] == "multistate_nonlinear_fixed_design_tt_value_path"
    assert result.diagnostics["state_dim"] == 2
    assert result.retained_filter.storage_kind == "multistate_tt_grid"
    assert "production" not in result.branch_identity.manifest.payload["scope"]
    tf.debugging.assert_near(result.log_likelihood, reference["log_likelihood"], atol=2e-3, rtol=2e-4)
    tf.debugging.assert_near(log_normalizers, reference["log_normalizers"], atol=2e-3, rtol=2e-4)
    tf.debugging.assert_less(state_error[0], tf.constant(1e-5, dtype=DTYPE))
    tf.debugging.assert_less(state_error[1], tf.constant(1e-5, dtype=DTYPE))
    tf.debugging.assert_less(covariance_error, tf.constant(1e-5, dtype=DTYPE))
    for step in result.steps:
        tf.debugging.assert_near(
            step.diagnostics["retained_moment_mass"],
            tf.constant(1.0, dtype=DTYPE),
            atol=2e-2,
        )


def test_p47_m5_cut4_closure_is_same_target_value_diagnostic_not_state_promotion() -> None:
    reference = _dense_reference(order=7)
    cut4 = _cut4_result()

    assert cut4.metadata.approximation_label == "p47_m5_predator_prey_additive_gaussian_closure"
    assert cut4.metadata.differentiability_status == "value_only"
    assert int(cut4.diagnostics.extra["augmented_dim"].numpy()) == 4
    assert int(cut4.diagnostics.extra["polynomial_degree"].numpy()) == 5
    assert bool(tf.math.is_finite(cut4.log_likelihood).numpy())
    assert bool(tf.math.is_finite(reference["log_likelihood"]).numpy())


def test_p47_m5_cut4_closure_is_same_target_value_diagnostic_not_state_promotion() -> None:
    reference = _dense_reference(order=7)
    cut4 = _cut4_result()

    assert cut4.metadata.approximation_label == "p47_m5_predator_prey_additive_gaussian_closure"
    assert cut4.metadata.differentiability_status == "value_only"
    assert int(cut4.diagnostics.extra["augmented_dim"].numpy()) == 4
    assert int(cut4.diagnostics.extra["polynomial_degree"].numpy()) == 5
    assert bool(tf.math.is_finite(cut4.log_likelihood).numpy())
    assert bool(tf.math.is_finite(reference["log_likelihood"]).numpy())



def test_p47_m5_fixed_sgqf_adapter_is_same_target_value_diagnostic() -> None:
    model = _model()
    theta = _theta()
    adapted = tf_predator_prey_to_fixed_sgqf_model(model, theta)
    observations = _observations()
    reference = _dense_reference(order=7)

    assert adapted.eligible is True
    assert adapted.model is not None

    result = tf_fixed_sgqf_filter(
        observations,
        adapted.model,
        cloud=tf_fixed_sgqf_cloud(dim=2, sparse_level=2),
        return_filtered=True,
    )

    assert result.failure is None
    assert bool(tf.math.is_finite(result.log_likelihood).numpy())
    assert bool(tf.math.is_finite(reference["log_likelihood"]).numpy())



def test_p47_m5_fixed_sgqf_adapter_is_same_target_value_diagnostic() -> None:
    model = _model()
    theta = _theta()
    adapted = tf_predator_prey_to_fixed_sgqf_model(model, theta)
    observations = _observations()
    reference = _dense_reference(order=7)

    assert adapted.eligible is True
    assert adapted.model is not None

    result = tf_fixed_sgqf_filter(
        observations,
        adapted.model,
        cloud=tf_fixed_sgqf_cloud(dim=2, sparse_level=2),
        return_filtered=True,
    )

    assert result.failure is None
    assert bool(tf.math.is_finite(result.log_likelihood).numpy())
    assert bool(tf.math.is_finite(reference["log_likelihood"]).numpy())



def test_p47_m5_fixed_sgqf_matches_dense_reference_full_path_value() -> None:
    reference = _dense_reference(order=7)
    _adapted, _cloud, result = _fixed_sgqf_result(sparse_level=2)

    assert result.failure is None
    assert bool(tf.math.is_finite(result.log_likelihood).numpy())
    assert bool(tf.math.is_finite(reference["log_likelihood"]).numpy())

    absolute_gap = tf.abs(result.log_likelihood - reference["log_likelihood"])
    relative_gap = absolute_gap / tf.maximum(tf.constant(1.0, dtype=DTYPE), tf.abs(reference["log_likelihood"]))
    state_error = tf.reduce_max(tf.abs(result.filtered_means - reference["mean_path"]), axis=0)
    covariance_error = tf.reduce_max(tf.abs(result.filtered_covariances - reference["covariance_path"]))

    assert bool(tf.reduce_all(tf.math.is_finite(state_error)).numpy())
    assert bool(tf.math.is_finite(covariance_error).numpy())
    assert bool(tf.math.is_finite(absolute_gap).numpy())
    assert bool(tf.math.is_finite(relative_gap).numpy())

    tf.debugging.assert_less(absolute_gap, tf.constant(5.0e1, dtype=DTYPE))
    tf.debugging.assert_less(relative_gap, tf.constant(3.1, dtype=DTYPE))
    tf.debugging.assert_less(state_error[0], tf.constant(2.0e1, dtype=DTYPE))
    tf.debugging.assert_less(state_error[1], tf.constant(3.0, dtype=DTYPE))
    tf.debugging.assert_less(covariance_error, tf.constant(4.0e1, dtype=DTYPE))



def test_p47_m5_fixed_sgqf_matches_dense_reference_first_step_value() -> None:
    reference = _dense_reference(order=7)
    _adapted, _cloud, result = _fixed_sgqf_result(sparse_level=2)
    step = result.step_results[0]

    assert result.failure is None
    assert bool(tf.math.is_finite(step.log_likelihood_increment).numpy())

    absolute_gap = tf.abs(step.log_likelihood_increment - reference["log_normalizers"][0])
    relative_gap = absolute_gap / tf.maximum(tf.constant(1.0, dtype=DTYPE), tf.abs(reference["log_normalizers"][0]))
    state_error = tf.abs(step.filtered_mean - reference["mean_path"][0])
    covariance_error = tf.reduce_max(tf.abs(step.filtered_covariance - reference["covariance_path"][0]))

    assert bool(tf.reduce_all(tf.math.is_finite(state_error)).numpy())
    assert bool(tf.math.is_finite(covariance_error).numpy())
    assert bool(tf.math.is_finite(absolute_gap).numpy())
    assert bool(tf.math.is_finite(relative_gap).numpy())

    tf.debugging.assert_less(absolute_gap, tf.constant(5.0e1, dtype=DTYPE))
    tf.debugging.assert_less(relative_gap, tf.constant(6.0, dtype=DTYPE))
    tf.debugging.assert_less(state_error[0], tf.constant(2.0e1, dtype=DTYPE))
    tf.debugging.assert_less(state_error[1], tf.constant(3.0, dtype=DTYPE))
    tf.debugging.assert_less(covariance_error, tf.constant(4.0e1, dtype=DTYPE))



def test_p47_m5_fixed_sgqf_matches_dense_reference_first_step_value() -> None:
    reference = _dense_reference(order=7)
    _adapted, _cloud, result = _fixed_sgqf_result(sparse_level=2)
    step = result.step_results[0]

    assert result.failure is None
    assert bool(tf.math.is_finite(step.log_likelihood_increment).numpy())
    absolute_gap = tf.abs(step.log_likelihood_increment - reference["log_normalizers"][0])
    relative_gap = absolute_gap / tf.maximum(tf.constant(1.0, dtype=DTYPE), tf.abs(reference["log_normalizers"][0]))
    state_error = tf.abs(step.filtered_mean - reference["mean_path"][0])
    covariance_error = tf.reduce_max(tf.abs(step.filtered_covariance - reference["covariance_path"][0]))

    assert bool(tf.reduce_all(tf.math.is_finite(state_error)).numpy())
    assert bool(tf.math.is_finite(covariance_error).numpy())
    assert bool(tf.math.is_finite(absolute_gap).numpy())
    assert bool(tf.math.is_finite(relative_gap).numpy())

    tf.debugging.assert_less(absolute_gap, tf.constant(5.0e1, dtype=DTYPE))
    tf.debugging.assert_less(relative_gap, tf.constant(6.0, dtype=DTYPE))
    tf.debugging.assert_less(state_error[0], tf.constant(2.0e1, dtype=DTYPE))
    tf.debugging.assert_less(state_error[1], tf.constant(3.0, dtype=DTYPE))
    tf.debugging.assert_less(covariance_error, tf.constant(4.0e1, dtype=DTYPE))



def test_p47_m5_predator_prey_ukf_is_same_target_value_diagnostic() -> None:
    reference = _dense_reference(order=7)
    _structural, ukf = _ukf_result()

    assert bool(tf.math.is_finite(ukf.log_likelihood).numpy())
    assert bool(tf.math.is_finite(reference["log_likelihood"]).numpy())
    assert ukf.metadata.approximation_label == "p47_m5_predator_prey_additive_gaussian_closure"



def test_p47_m5_predator_prey_ukf_matches_dense_reference_full_path_value() -> None:
    reference = _dense_reference(order=7)
    _structural, ukf = _ukf_result()

    assert bool(tf.math.is_finite(ukf.log_likelihood).numpy())
    absolute_gap = tf.abs(ukf.log_likelihood - reference["log_likelihood"])
    relative_gap = absolute_gap / tf.maximum(tf.constant(1.0, dtype=DTYPE), tf.abs(reference["log_likelihood"]))
    state_error = tf.reduce_max(tf.abs(ukf.filtered_means - reference["mean_path"]), axis=0)
    covariance_error = tf.reduce_max(tf.abs(ukf.filtered_covariances - reference["covariance_path"]))

    assert bool(tf.reduce_all(tf.math.is_finite(state_error)).numpy())
    assert bool(tf.math.is_finite(covariance_error).numpy())
    tf.debugging.assert_less(absolute_gap, tf.constant(5.0e1, dtype=DTYPE))
    tf.debugging.assert_less(relative_gap, tf.constant(3.1, dtype=DTYPE))
    tf.debugging.assert_less(state_error[0], tf.constant(2.0e1, dtype=DTYPE))
    tf.debugging.assert_less(state_error[1], tf.constant(3.0, dtype=DTYPE))
    tf.debugging.assert_less(covariance_error, tf.constant(4.0e1, dtype=DTYPE))



def test_p47_m5_predator_prey_fixed_sgqf_vs_ukf_same_target_value_row() -> None:
    reference = _dense_reference(order=7)
    _adapted, _cloud, sgqf = _fixed_sgqf_result(sparse_level=2)
    _structural, ukf = _ukf_result()

    sgqf_gap = tf.abs(sgqf.log_likelihood - reference["log_likelihood"])
    ukf_gap = tf.abs(ukf.log_likelihood - reference["log_likelihood"])

    assert bool(tf.math.is_finite(sgqf_gap).numpy())
    assert bool(tf.math.is_finite(ukf_gap).numpy())



def test_p47_m5_fixed_sgqf_predator_prey_single_parameter_score_matches_fd_same_branch() -> None:
    model = _model()
    theta = _theta()
    adapted = tf_predator_prey_to_fixed_sgqf_model(model, theta, with_derivatives=True)
    assert adapted.eligible and adapted.model is not None and adapted.derivatives is not None
    cloud = tf_fixed_sgqf_cloud(dim=2, sparse_level=2)
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    value = tf_fixed_sgqf_filter(_observations(), adapted.model, cloud=cloud, branch_config=branch, return_filtered=True)
    score = tf_fixed_sgqf_score(
        _observations(),
        adapted.model,
        adapted.derivatives,
        cloud=cloud,
        branch_config=branch,
        expected_branch_identity=value.branch_identity,
    )

    assert value.failure is None
    assert score.failure is None

    def value_at(theta_value: tf.Tensor):
        shifted = tf_predator_prey_to_fixed_sgqf_model(model, theta_value)
        assert shifted.eligible and shifted.model is not None
        result = tf_fixed_sgqf_filter(_observations(), shifted.model, cloud=cloud, branch_config=branch, return_filtered=True)
        return result

    step = 1e-4
    plus_theta = tf.tensor_scatter_nd_add(theta, [[0]], [step])
    minus_theta = tf.tensor_scatter_nd_add(theta, [[0]], [-step])
    plus = value_at(plus_theta)
    minus = value_at(minus_theta)

    assert plus.failure is None
    assert minus.failure is None
    assert tf_fixed_sgqf_same_branch_signature(branch_identity=value.branch_identity, failure=value.failure) == tf_fixed_sgqf_same_branch_signature(branch_identity=plus.branch_identity, failure=plus.failure)
    assert tf_fixed_sgqf_same_branch_signature(branch_identity=value.branch_identity, failure=value.failure) == tf_fixed_sgqf_same_branch_signature(branch_identity=minus.branch_identity, failure=minus.failure)

    finite_difference = (float(plus.log_likelihood.numpy()) - float(minus.log_likelihood.numpy())) / (2.0 * step)
    tf.debugging.assert_near(score.score[0], tf.constant(finite_difference, dtype=DTYPE), atol=5e-2, rtol=5e-2)



def test_p47_m5_fixed_sgqf_predator_prey_multistep_score_matches_fd_for_all_parameters() -> None:
    model = _model()
    theta = _theta()
    adapted = tf_predator_prey_to_fixed_sgqf_model(model, theta, with_derivatives=True)
    assert adapted.eligible and adapted.model is not None and adapted.derivatives is not None
    cloud = tf_fixed_sgqf_cloud(dim=2, sparse_level=2)
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    value = tf_fixed_sgqf_filter(_observations(), adapted.model, cloud=cloud, branch_config=branch, return_filtered=True)
    score = tf_fixed_sgqf_score(
        _observations(),
        adapted.model,
        adapted.derivatives,
        cloud=cloud,
        branch_config=branch,
        expected_branch_identity=value.branch_identity,
    )

    assert value.failure is None
    assert score.failure is None

    def value_at(theta_value: tf.Tensor):
        shifted = tf_predator_prey_to_fixed_sgqf_model(model, theta_value)
        assert shifted.eligible and shifted.model is not None
        result = tf_fixed_sgqf_filter(_observations(), shifted.model, cloud=cloud, branch_config=branch, return_filtered=True)
        if result.failure is not None:
            raise AssertionError(f"finite-difference evaluation left accepted branch at {result.failure.stage}")
        return float(result.log_likelihood.numpy())

    step = 1e-4
    fd = []
    for index in range(int(theta.shape[0])):
        plus_theta = tf.tensor_scatter_nd_add(theta, [[index]], [step])
        minus_theta = tf.tensor_scatter_nd_add(theta, [[index]], [-step])
        fd.append((value_at(plus_theta) - value_at(minus_theta)) / (2.0 * step))
    tf.debugging.assert_near(score.score, tf.constant(fd, dtype=DTYPE), atol=2e-1, rtol=1e-1)



def test_p47_m5_fixed_sgqf_predator_prey_fd_ladder_preserves_same_branch_contract() -> None:
    model = _model()
    theta = _theta()
    _adapted, cloud, value = _fixed_sgqf_result(sparse_level=2)
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    assert value.failure is None
    base_signature = tf_fixed_sgqf_same_branch_signature(branch_identity=value.branch_identity, failure=value.failure)

    for step in (1e-3, 3e-4, 1e-4):
        plus_theta = tf.tensor_scatter_nd_add(theta, [[0]], [step])
        minus_theta = tf.tensor_scatter_nd_add(theta, [[0]], [-step])
        plus = tf_fixed_sgqf_filter(_observations(), tf_predator_prey_to_fixed_sgqf_model(model, plus_theta).model, cloud=cloud, branch_config=branch, return_filtered=True)
        minus = tf_fixed_sgqf_filter(_observations(), tf_predator_prey_to_fixed_sgqf_model(model, minus_theta).model, cloud=cloud, branch_config=branch, return_filtered=True)
        assert plus.failure is None
        assert minus.failure is None
        assert base_signature == tf_fixed_sgqf_same_branch_signature(branch_identity=plus.branch_identity, failure=plus.failure)
        assert base_signature == tf_fixed_sgqf_same_branch_signature(branch_identity=minus.branch_identity, failure=minus.failure)



def test_p47_m5_fixed_sgqf_predator_prey_fd_ladder_preserves_same_branch_contract() -> None:
    model = _model()
    theta = _theta()
    _adapted, cloud, value = _fixed_sgqf_result(sparse_level=2)
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    assert value.failure is None
    base_signature = tf_fixed_sgqf_same_branch_signature(branch_identity=value.branch_identity, failure=value.failure)

    for step in (1e-3, 3e-4, 1e-4):
        plus_theta = tf.tensor_scatter_nd_add(theta, [[0]], [step])
        minus_theta = tf.tensor_scatter_nd_add(theta, [[0]], [-step])
        plus = tf_fixed_sgqf_filter(_observations(), tf_predator_prey_to_fixed_sgqf_model(model, plus_theta).model, cloud=cloud, branch_config=branch, return_filtered=True)
        minus = tf_fixed_sgqf_filter(_observations(), tf_predator_prey_to_fixed_sgqf_model(model, minus_theta).model, cloud=cloud, branch_config=branch, return_filtered=True)
        assert plus.failure is None
        assert minus.failure is None
        assert base_signature == tf_fixed_sgqf_same_branch_signature(branch_identity=plus.branch_identity, failure=plus.failure)
        assert base_signature == tf_fixed_sgqf_same_branch_signature(branch_identity=minus.branch_identity, failure=minus.failure)



def test_p47_m5_fixed_sgqf_score_gap_to_dense_score_is_finite() -> None:
    model = _model()
    theta = _theta()
    adapted = tf_predator_prey_to_fixed_sgqf_model(model, theta, with_derivatives=True)
    assert adapted.eligible and adapted.model is not None and adapted.derivatives is not None
    cloud = tf_fixed_sgqf_cloud(dim=2, sparse_level=2)
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    value = tf_fixed_sgqf_filter(_observations(), adapted.model, cloud=cloud, branch_config=branch, return_filtered=True)
    score = tf_fixed_sgqf_score(
        _observations(),
        adapted.model,
        adapted.derivatives,
        cloud=cloud,
        branch_config=branch,
        expected_branch_identity=value.branch_identity,
    )
    _dense_reference_payload, dense_score = _dense_value_and_score(theta)

    assert value.failure is None
    assert score.failure is None
    score_gap = score.score - dense_score
    assert bool(tf.reduce_all(tf.math.is_finite(score_gap)).numpy())



def test_p47_m5_predator_prey_ukf_score_gap_to_dense_score_is_finite() -> None:
    theta = _theta()
    _structural, ukf = _ukf_result(theta=theta)
    _dense_reference_payload, dense_score = _dense_value_and_score(theta)

    assert bool(tf.math.is_finite(ukf.log_likelihood).numpy())
    with tf.GradientTape() as tape:
        theta_t = tf.convert_to_tensor(theta, dtype=DTYPE)
        tape.watch(theta_t)
        _structural_theta, ukf_theta = _ukf_result(theta=theta_t)
        value = ukf_theta.log_likelihood
    score = tape.gradient(value, theta_t)
    if score is None:
        raise AssertionError("UKF predator-prey score tape returned None")
    score_gap = score - dense_score
    assert bool(tf.reduce_all(tf.math.is_finite(score_gap)).numpy())



def test_p47_m5_fixed_sgqf_vs_ukf_score_gap_is_finite() -> None:
    model = _model()
    theta = _theta()
    adapted = tf_predator_prey_to_fixed_sgqf_model(model, theta, with_derivatives=True)
    assert adapted.eligible and adapted.model is not None and adapted.derivatives is not None
    cloud = tf_fixed_sgqf_cloud(dim=2, sparse_level=2)
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    value = tf_fixed_sgqf_filter(_observations(), adapted.model, cloud=cloud, branch_config=branch, return_filtered=True)
    sgqf_score = tf_fixed_sgqf_score(
        _observations(),
        adapted.model,
        adapted.derivatives,
        cloud=cloud,
        branch_config=branch,
        expected_branch_identity=value.branch_identity,
    )
    with tf.GradientTape() as tape:
        theta_t = tf.convert_to_tensor(theta, dtype=DTYPE)
        tape.watch(theta_t)
        _structural_theta, ukf_theta = _ukf_result(theta=theta_t)
        ukf_value = ukf_theta.log_likelihood
    ukf_score = tape.gradient(ukf_value, theta_t)
    if ukf_score is None:
        raise AssertionError("UKF predator-prey score tape returned None")

    assert sgqf_score.failure is None
    score_gap = sgqf_score.score - ukf_score
    assert bool(tf.reduce_all(tf.math.is_finite(score_gap)).numpy())



def test_p47_track_b_sgqf_sparse_level_ladder_value_vs_dense() -> None:
    reference = _dense_reference(order=7)
    levels = (1, 2, 3, 4)
    total_gaps = []
    step0_gaps = []

    for level in levels:
        _adapted, cloud, result = _fixed_sgqf_result(sparse_level=level)
        assert result.failure is None
        assert bool(tf.math.is_finite(result.log_likelihood).numpy())
        total_gaps.append(abs(float(result.log_likelihood.numpy() - reference["log_likelihood"].numpy())))
        step0_gaps.append(abs(float(result.step_results[0].log_likelihood_increment.numpy() - reference["log_normalizers"][0].numpy())))
        assert cloud.point_count > 0

    assert total_gaps[1] <= total_gaps[0] + 1e-9
    assert step0_gaps[1] <= step0_gaps[0] + 1e-9



def test_p47_track_b_sgqf_sparse_level_ladder_score_vs_dense() -> None:
    theta = _theta()
    _reference, dense_score = _dense_value_and_score(theta)
    levels = (1, 2, 3, 4)
    score_gaps = []

    for level in levels:
        adapted = tf_predator_prey_to_fixed_sgqf_model(_model(), theta, with_derivatives=True)
        assert adapted.eligible and adapted.model is not None and adapted.derivatives is not None
        cloud = tf_fixed_sgqf_cloud(dim=2, sparse_level=level)
        branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
        value = tf_fixed_sgqf_filter(_observations(), adapted.model, cloud=cloud, branch_config=branch, return_filtered=True)
        assert value.failure is None
        score = tf_fixed_sgqf_score(
            _observations(),
            adapted.model,
            adapted.derivatives,
            cloud=cloud,
            branch_config=branch,
            expected_branch_identity=value.branch_identity,
        )
        assert score.failure is None
        gap = tf.linalg.norm(score.score - dense_score)
        assert bool(tf.math.is_finite(gap).numpy())
        score_gaps.append(float(gap.numpy()))

    assert score_gaps[1] <= score_gaps[0] + 1e-9



def test_p47_m5_preconditioning_schema_remains_proxy_only_without_downstream_promotion() -> None:
    manifest = highdim.P30PredatorPreyComparisonManifest(
        version="p47.m5.predator_prey.reference_filtering_schema.v1",
        linear_settings=_matched_settings(),
        nonlinear_settings=_matched_settings(),
        metrics=_metrics(),
        promotion_decision="FIRST_GATE_SCHEMA_ONLY",
        non_claims=(
            "no nonlinear preconditioning usefulness claim",
            "no matched linear/nonlinear comparison success claim",
        ),
    )

    assert manifest.model_id is highdim.P30ModelSuiteModelID.PREDATOR_PREY
    assert manifest.promotion_decision == "FIRST_GATE_SCHEMA_ONLY"

    with pytest.raises(ValueError, match="unmatched comparison settings"):
        highdim.P30PredatorPreyComparisonManifest(
            version="p47.m5.predator_prey.bad_budget.v1",
            linear_settings=_matched_settings(),
            nonlinear_settings=_matched_settings(nominal_rank_cap=8),
            metrics=_metrics(),
            promotion_decision="FIRST_GATE_SCHEMA_ONLY",
            non_claims=(
                "no nonlinear preconditioning usefulness claim",
                "no matched linear/nonlinear comparison success claim",
            ),
        )

    with pytest.raises(ValueError, match="promotion requires positive delta_ess and delta_cost"):
        highdim.P30PredatorPreyComparisonManifest(
            version="p47.m5.predator_prey.bad_proxy_promotion.v1",
            linear_settings=_matched_settings(),
            nonlinear_settings=_matched_settings(),
            metrics=_metrics(),
            promotion_decision="PROMOTE_NONLINEAR_USEFULNESS",
            non_claims=(
                "no nonlinear preconditioning usefulness claim",
                "no matched linear/nonlinear comparison success claim",
            ),
        )
