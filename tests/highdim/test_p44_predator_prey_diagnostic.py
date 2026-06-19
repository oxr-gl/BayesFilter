from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter.nonlinear.svd_cut_tf import tf_svd_cut4_filter
from bayesfilter.structural import StatePartition, StructuralFilterConfig
from bayesfilter.structural_tf import TFStructuralStateSpace


DTYPE = tf.float64


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _model() -> highdim.PredatorPreySSM:
    return highdim.p30_predator_prey_fixture_model()


def _theta0() -> tf.Tensor:
    return _model().true_parameters()


def _observations() -> tf.Tensor:
    return tf.constant([[51.0, 4.6], [51.7, 5.1]], dtype=DTYPE)


def _structural_closure(theta: tf.Tensor) -> TFStructuralStateSpace:
    theta = tf.convert_to_tensor(theta, dtype=DTYPE)
    model = _model()
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
            approximation_label="p44_m6_predator_prey_additive_gaussian_diagnostic_closure",
        ),
        initial_mean=model.initial_mean,
        initial_covariance=model.initial_covariance,
        innovation_covariance=tf.eye(2, dtype=DTYPE),
        observation_covariance=model.observation_covariance,
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="p44_m6_predator_prey_cut4_diagnostic_closure",
    )


def _cut4_value(theta: tf.Tensor):
    return tf_svd_cut4_filter(
        _observations(),
        _structural_closure(theta),
        innovation_floor=tf.constant(1e-12, dtype=DTYPE),
        return_filtered=True,
    )


def _relative_error(candidate: tf.Tensor, reference: tf.Tensor) -> tf.Tensor:
    return tf.abs(candidate - reference) / tf.maximum(tf.constant(1.0, dtype=DTYPE), tf.abs(reference))


def _directions(dim: int) -> list[tf.Tensor]:
    directions = []
    for index in range(dim):
        directions.append(tf.one_hot(index, dim, dtype=DTYPE))
    directions.append(tf.ones([dim], dtype=DTYPE))
    directions.append(tf.constant([1.0 if i % 2 == 0 else -1.0 for i in range(dim)], dtype=DTYPE))
    return directions


def _value_and_score(theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    theta = tf.convert_to_tensor(theta, dtype=DTYPE)
    with tf.GradientTape() as tape:
        tape.watch(theta)
        result = _cut4_value(theta)
        value = result.log_likelihood
    score = tape.gradient(value, theta)
    if score is None:
        raise AssertionError("GradientTape returned None")
    return value, score


def _fd_gradient(theta: tf.Tensor, step: float) -> tf.Tensor:
    theta = tf.convert_to_tensor(theta, dtype=DTYPE)
    box = _model().parameter_box()
    grads = []
    for index, key in enumerate(("r", "K", "a", "s", "u", "v")):
        lower, upper = box[key]
        plus = tf.tensor_scatter_nd_add(theta, [[index]], [step])
        minus = tf.tensor_scatter_nd_add(theta, [[index]], [-step])
        if not (lower <= float(plus[index].numpy()) <= upper and lower <= float(minus[index].numpy()) <= upper):
            raise AssertionError(f"finite-difference perturbation left parameter box for {key}")
        value_plus = _cut4_value(plus).log_likelihood
        value_minus = _cut4_value(minus).log_likelihood
        grads.append((float(value_plus.numpy()) - float(value_minus.numpy())) / (2.0 * step))
    return tf.constant(grads, dtype=DTYPE)



def test_p44_m6_cut4_closure_has_finite_value_and_parameter_score() -> None:
    value, score = _value_and_score(_theta0())

    print(
        "P44_M6_PREDATOR_PREY_CUT4_DIAGNOSTIC "
        f"value={float(value.numpy()):.6e} "
        f"score_norm={float(tf.linalg.norm(score).numpy()):.6e}"
    )
    assert bool(tf.math.is_finite(value).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(score)).numpy())
    assert float(tf.linalg.norm(score).numpy()) > 0.0



def test_p44_m6_cut4_parameter_score_matches_centered_fd_componentwise() -> None:
    theta = _theta0()
    _value, score = _value_and_score(theta)
    fd = _fd_gradient(theta, step=1e-4)
    rel = _relative_error(score, fd)

    assert bool(tf.reduce_all(tf.math.is_finite(fd)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(rel)).numpy())
    tf.debugging.assert_less(tf.reduce_max(rel), tf.constant(5e-2, dtype=DTYPE))



def test_p44_m6_cut4_parameter_score_matches_centered_fd_in_directional_residuals() -> None:
    theta = _theta0()
    _value, score = _value_and_score(theta)
    fd = _fd_gradient(theta, step=1e-4)

    for direction in _directions(int(theta.shape[0])):
        direction = tf.math.l2_normalize(direction)
        score_proj = tf.tensordot(score, direction, axes=1)
        fd_proj = tf.tensordot(fd, direction, axes=1)
        residual = _relative_error(score_proj, fd_proj)
        cosine = (score_proj * fd_proj) / (
            tf.maximum(tf.constant(1e-12, dtype=DTYPE), tf.abs(score_proj) * tf.abs(fd_proj))
        )
        tf.debugging.assert_less(residual, tf.constant(5e-2, dtype=DTYPE))
        tf.debugging.assert_greater_equal(cosine, tf.constant(0.995, dtype=DTYPE))



def test_p44_m6_cut4_fd_ladder_stays_inside_parameter_box() -> None:
    theta = _theta0()
    for step in (1e-3, 3e-4, 1e-4):
        fd = _fd_gradient(theta, step)
        assert bool(tf.reduce_all(tf.math.is_finite(fd)).numpy())



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
        "basis_family": "legendre",
        "basis_size": 9,
        "nominal_rank_cap": 10,
        "sweep_count": 1,
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


def test_p44_m6_predator_prey_model_contract_anchor_and_domain_policy() -> None:
    model = _model()
    payload = model.manifest_payload()

    assert model.state_dim() == 2
    assert model.observation_dim() == 2
    assert model.parameter_dim() == 6
    assert model.validate_parameter_box(_theta0())
    assert payload["dimension_convention"] == "state is (P,Q); parameter is (r,K,a,s,u,v)"
    assert payload["domain_policy"] == "diagnose_negative_after_noise"
    assert "eq:p27-pp4" in payload["source_equations"]
    assert "eq:p27-pp8" in payload["source_equations"]
    assert "nonlinear_preconditioning_usefulness" in payload["what_is_not_claimed"]

    diagnostics = model.domain_diagnostics(tf.constant([[50.0, 5.0], [-0.2, 4.8]], dtype=DTYPE))
    assert diagnostics["domain_policy"] == "diagnose_negative_after_noise"
    assert diagnostics["has_negative_state"] is True


def test_p44_m6_cut4_closure_has_finite_value_and_parameter_score() -> None:
    value, score = _value_and_score(_theta0())

    print(
        "P44_M6_PREDATOR_PREY_CUT4_DIAGNOSTIC "
        f"value={float(value.numpy()):.6e} "
        f"score_norm={float(tf.linalg.norm(score).numpy()):.6e}"
    )
    assert bool(tf.math.is_finite(value).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(score)).numpy())
    assert float(tf.linalg.norm(score).numpy()) > 0.0


def test_p44_m6_cut4_metadata_preserves_diagnostic_closure_boundary() -> None:
    result = _cut4_value(_theta0())

    assert result.metadata.approximation_label == "p44_m6_predator_prey_additive_gaussian_diagnostic_closure"
    assert result.metadata.differentiability_status == "value_only"
    assert int(result.diagnostics.extra["augmented_dim"].numpy()) == 4
    assert int(result.diagnostics.extra["point_count"].numpy()) == 24
    assert int(result.diagnostics.extra["polynomial_degree"].numpy()) == 5
    assert int(result.diagnostics.extra["innovation_floor_count"].numpy()) == 0
    reason = result.diagnostics.extra["derivative_status_reason"]
    if hasattr(reason, "numpy"):
        reason = reason.numpy().decode()
    assert "derivatives are not certified" in str(reason)


def test_p44_m6_no_matched_zhaocui_equality_route_for_predator_prey_closure() -> None:
    config = highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(2),),
        measure_convention=_convention(),
        deterministic_seed="p44-m6-predator-prey-no-zhaocui-equality-route",
    )

    try:
        highdim.FixedBranchSquaredTTFilter(config).log_likelihood(
            _model(),
            _theta0(),
            _observations(),
        )
    except TypeError as exc:
        assert "scalar nonlinear dense value path requires state_dim == 1" in str(exc)
    else:
        raise AssertionError("Predator-prey closure unexpectedly found a matched Zhao-Cui equality route")


def test_p44_m6_fair_preconditioning_manifest_blocks_proxy_promotion() -> None:
    manifest = highdim.P30PredatorPreyComparisonManifest(
        version="p44.m6.predator_prey.schema_only.v1",
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
            version="p44.m6.predator_prey.bad_budget.v1",
            linear_settings=_matched_settings(),
            nonlinear_settings=_matched_settings(nominal_rank_cap=20),
            metrics=_metrics(),
            promotion_decision="FIRST_GATE_SCHEMA_ONLY",
            non_claims=(
                "no nonlinear preconditioning usefulness claim",
                "no matched linear/nonlinear comparison success claim",
            ),
        )

    with pytest.raises(ValueError, match="promotion requires positive delta_ess and delta_cost"):
        highdim.P30PredatorPreyComparisonManifest(
            version="p44.m6.predator_prey.bad_proxy_promotion.v1",
            linear_settings=_matched_settings(),
            nonlinear_settings=_matched_settings(),
            metrics=_metrics(),
            promotion_decision="PROMOTE_NONLINEAR_USEFULNESS",
            non_claims=(
                "no nonlinear preconditioning usefulness claim",
                "no matched linear/nonlinear comparison success claim",
            ),
        )
