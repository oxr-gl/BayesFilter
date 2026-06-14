from __future__ import annotations

from pathlib import Path
import math

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter.nonlinear.svd_cut_tf import tf_svd_cut4_filter
from bayesfilter.structural import StatePartition, StructuralFilterConfig
from bayesfilter.structural_tf import TFStructuralStateSpace


DTYPE = tf.float64
TARGET_NOTE = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-definition-2026-06-08.md"
)


class _StateDimOnlyNonlinearModel:
    def __init__(self, dim: int) -> None:
        self._dim = int(dim)

    def state_dim(self) -> int:
        return self._dim

    def parameter_dim(self) -> int:
        return 0

    def observation_dim(self) -> int:
        return 1


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _tt_config(seed: str) -> highdim.FixedBranchFilterConfig:
    convention = _convention()
    product_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 16)],
        convention,
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=(1, 1),
            ridge=1e-12,
            max_sweeps=1,
            sweep_order=(0,),
            row_budget=64,
            column_budget=32,
            dense_matrix_byte_budget=50_000,
            normal_matrix_byte_budget=25_000,
            condition_number_warning=1e10,
            condition_number_veto=1e14,
            holdout_tolerance=1e-3,
        ),
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=1_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.constant([0.0], dtype=DTYPE),
                matrix=tf.constant([[8.0]], dtype=DTYPE),
            ),
        ),
        measure_convention=convention,
        deterministic_seed=seed,
        product_basis=product_basis,
        initial_cores=(
            highdim.TTCore(tf.ones([1, product_basis.bases[0].basis_dim, 1], dtype=DTYPE)),
        ),
        fit_quadrature_order=41,
    )


def _generalized_sv_diagnostic_model(*, observation: tf.Tensor, beta: tf.Tensor) -> TFStructuralStateSpace:
    gamma_s = tf.constant(0.55, dtype=DTYPE)
    gamma_h = tf.constant(0.65, dtype=DTYPE)
    sigma_s = tf.constant(0.30, dtype=DTYPE)
    sigma_h = tf.constant(0.45, dtype=DTYPE)
    initial_covariance = tf.linalg.diag(
        tf.stack(
            [
                tf.square(sigma_s) / (1.0 - tf.square(gamma_s)),
                tf.square(sigma_h) / (1.0 - tf.square(gamma_h)),
            ]
        )
    )
    observed_scalar = tf.reshape(tf.convert_to_tensor(observation, dtype=DTYPE), [])

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        return tf.convert_to_tensor(previous_state, dtype=DTYPE)

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(state_points, dtype=DTYPE)
        if points.shape.rank == 1:
            points = points[tf.newaxis, :]
        residual = observed_scalar - beta * points[:, 0]
        transformed_residual = tf.math.log(tf.square(residual) + tf.constant(1e-8, dtype=DTYPE)) - points[:, 1]
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
            approximation_label="p44_m7_generalized_sv_transformed_residual_diagnostic_not_exact",
        ),
        initial_mean=tf.zeros([2], dtype=DTYPE),
        initial_covariance=initial_covariance,
        innovation_covariance=tf.eye(2, dtype=DTYPE),
        observation_covariance=tf.reshape(tf.constant(1.0, dtype=DTYPE), [1, 1]),
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="p44_m7_generalized_sv_diagnostic_not_exact",
    )


def _moment_matched_kalman_one_step(*, observation: tf.Tensor, beta: float) -> dict[str, tf.Tensor]:
    mean = tf.zeros([2], dtype=DTYPE)
    covariance = tf.linalg.diag(tf.constant([0.30**2 / (1.0 - 0.55**2), 0.45**2 / (1.0 - 0.65**2)], dtype=DTYPE))
    observation_matrix = tf.constant([[float(beta), 0.0]], dtype=DTYPE)
    observation_noise = tf.exp(mean[1] + 0.5 * covariance[1, 1])
    innovation = tf.reshape(tf.convert_to_tensor(observation, dtype=DTYPE), [1]) - tf.linalg.matvec(
        observation_matrix,
        mean,
    )
    innovation_covariance = observation_matrix @ covariance @ tf.transpose(observation_matrix) + tf.reshape(
        observation_noise,
        [1, 1],
    )
    log_likelihood = -0.5 * (
        tf.math.log(tf.constant(2.0 * math.pi, dtype=DTYPE))
        + tf.math.log(innovation_covariance[0, 0])
        + tf.square(innovation[0]) / innovation_covariance[0, 0]
    )
    return {
        "log_likelihood": log_likelihood,
        "non_claim": tf.constant("moment_matched_raw_observation_approximation_not_exact"),
    }


def test_p44_m7_target_definition_table_is_complete_and_class_d() -> None:
    text = TARGET_NOTE.read_text(encoding="utf-8")

    for field in (
        "state_law_s",
        "state_law_h",
        "state_dependence",
        "observation_law",
        "target_route",
        "parameterization",
        "jacobian_terms",
        "reference_route",
        "claim_class",
    ):
        assert f"`{field}`" in text
    assert "`diagnostic-only`" in text
    assert "`P42 Class D diagnostic only`" in text
    assert "not made additive-Gaussian by `log(y_t^2)`" in text
    assert "state-dependent" in text
    assert "no same-target CUT4/Zhao--Cui equality is approved" in text


def test_p44_m7_generalized_sv_cut4_diagnostic_value_and_gradient_are_finite() -> None:
    theta = tf.constant(math.log(0.35), dtype=DTYPE)

    with tf.GradientTape() as tape:
        tape.watch(theta)
        beta = tf.exp(theta)
        model = _generalized_sv_diagnostic_model(
            observation=tf.constant(0.18, dtype=DTYPE),
            beta=beta,
        )
        result = tf_svd_cut4_filter(
            tf.constant([[0.0]], dtype=DTYPE),
            model,
            return_filtered=True,
        )
        value = result.log_likelihood
    score = tape.gradient(value, theta)

    print(
        "P44_M7_GENERALIZED_SV_DIAGNOSTIC "
        f"value={float(value.numpy()):.6e} "
        f"score={float(score.numpy()):.6e}"
    )
    assert bool(tf.math.is_finite(value).numpy())
    assert score is not None
    assert bool(tf.math.is_finite(score).numpy())
    assert result.metadata.approximation_label == "p44_m7_generalized_sv_transformed_residual_diagnostic_not_exact"
    assert int(result.diagnostics.extra["augmented_dim"].numpy()) == 4
    assert int(result.diagnostics.extra["point_count"].numpy()) == 24


def test_p44_m7_moment_matched_kalman_is_nonexact_diagnostic_only() -> None:
    diagnostic = _moment_matched_kalman_one_step(
        observation=tf.constant(0.18, dtype=DTYPE),
        beta=0.35,
    )

    assert bool(tf.math.is_finite(diagnostic["log_likelihood"]).numpy())
    assert diagnostic["non_claim"].numpy().decode("utf-8") == (
        "moment_matched_raw_observation_approximation_not_exact"
    )


def test_p44_m7_zhaocui_generalized_sv_equality_route_is_blocked() -> None:
    with pytest.raises(TypeError, match="state_dim == 1"):
        highdim.scalar_nonlinear_fixed_design_tt_value_path(
            _StateDimOnlyNonlinearModel(2),
            tf.zeros([0], dtype=DTYPE),
            tf.constant([[0.18], [0.11]], dtype=DTYPE),
            _tt_config(seed="p44-m7-generalized-sv-zhaocui-blocked"),
        )
