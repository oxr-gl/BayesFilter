from __future__ import annotations

import json
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
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


def _structural_closure() -> TFStructuralStateSpace:
    model = _model()
    theta = _theta()
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
