from __future__ import annotations

import json
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64
REGISTRY_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json")


class _TwoStateNonlinearModel:
    def parameter_dim(self) -> int:
        return 0

    def state_dim(self) -> int:
        return 2

    def observation_dim(self) -> int:
        return 1

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        del theta
        x0 = tf.convert_to_tensor(x0, dtype=DTYPE)
        return -0.5 * tf.reduce_sum(tf.square(x0), axis=1)

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del theta, x_prev, t
        x_next = tf.convert_to_tensor(x_next, dtype=DTYPE)
        return -0.5 * tf.reduce_sum(tf.square(x_next), axis=1)

    def observation_log_density(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del theta, t
        x_t = tf.convert_to_tensor(x_t, dtype=DTYPE)
        y_t = tf.reshape(tf.convert_to_tensor(y_t, dtype=DTYPE), [1])
        residual = y_t[0] - x_t[:, 0]
        return -0.5 * tf.square(residual)

    def manifest_payload(self) -> dict[str, object]:
        return {"family": "p45_two_state_nonlinear_blocker_fixture"}


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _dense_config() -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(2),),
        measure_convention=_convention(),
        deterministic_seed="p45-m1-two-state-dense-route-blocked",
    )


def _tt_config() -> highdim.FixedBranchFilterConfig:
    product_basis = highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 4),
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 4),
        ],
        _convention(),
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=(1, 1, 1),
            ridge=1e-12,
            max_sweeps=1,
            sweep_order=(0, 1),
            row_budget=16,
            column_budget=16,
            dense_matrix_byte_budget=50_000,
            normal_matrix_byte_budget=25_000,
            condition_number_warning=1e10,
            condition_number_veto=1e14,
            holdout_tolerance=1e-3,
        ),
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(2),),
        measure_convention=_convention(),
        deterministic_seed="p45-m1-two-state-tt-route-blocked",
        product_basis=product_basis,
        fit_quadrature_order=5,
    )


def test_p45_m1_fixed_branch_filter_rejects_two_state_nonlinear_dense_path() -> None:
    with pytest.raises(TypeError, match="scalar nonlinear dense value path requires state_dim == 1"):
        highdim.FixedBranchSquaredTTFilter(_dense_config()).log_likelihood(
            _TwoStateNonlinearModel(),
            tf.zeros([0], dtype=DTYPE),
            tf.constant([[0.25], [0.15]], dtype=DTYPE),
        )


def test_p45_m1_fixed_design_tt_rejects_two_state_nonlinear_path() -> None:
    with pytest.raises(TypeError, match="scalar nonlinear fixed-design TT value path requires state_dim == 1"):
        highdim.scalar_nonlinear_fixed_design_tt_value_path(
            _TwoStateNonlinearModel(),
            tf.zeros([0], dtype=DTYPE),
            tf.constant([[0.25], [0.15]], dtype=DTYPE),
            _tt_config(),
        )


def test_p45_m1_registry_keeps_multistate_zhaocui_rows_blocked() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    rows = {row["target_id"]: row for row in registry["rows"]}
    for target_id in (
        "generalized_sv_native_raw_observation",
        "generalized_sv_transformed_residual_diagnostic",
        "generalized_sv_gaussian_mixture_or_moment_matched_approximation",
        "spatial_sir_additive_gaussian_closure",
        "predator_prey_additive_gaussian_rk4_closure",
    ):
        row = rows[target_id]
        assert row["same_target_comparison_authorized"] is False
        assert row["route_statuses"]["zhao_cui"] == "blocked_current_scalar_nonlinear_route_requires_state_dim_1"
