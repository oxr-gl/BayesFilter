from __future__ import annotations

import json
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64
REGISTRY_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json")


class _GeneralizedSVStateDimOnlyModel:
    def parameter_dim(self) -> int:
        return 1

    def state_dim(self) -> int:
        return 2

    def observation_dim(self) -> int:
        return 1

    def manifest_payload(self) -> dict[str, object]:
        return {"family": "p45_generalized_sv_state_dim_blocker"}


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _tt_config() -> highdim.FixedBranchFilterConfig:
    basis = highdim.ProductBasis(
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
        retained_storage_byte_budget=1_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(2),),
        measure_convention=_convention(),
        deterministic_seed="p45-m2-generalized-sv-zhaocui-blocked",
        product_basis=basis,
        fit_quadrature_order=5,
    )


def _rows() -> dict[str, dict[str, object]]:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {row["target_id"]: row for row in registry["rows"]}


def test_p45_m2_generalized_sv_native_route_is_not_authorized_for_equality() -> None:
    native = _rows()["generalized_sv_native_raw_observation"]

    assert native["same_target_comparison_authorized"] is False
    assert native["claim_class"] == "BLOCKED_NATIVE_SAME_TARGET"
    assert native["route_statuses"]["reference"] == "blocked_native_dense_reference_missing"
    assert native["route_statuses"]["cut4"].startswith("blocked_native")
    assert native["route_statuses"]["zhao_cui"] == "blocked_current_scalar_nonlinear_route_requires_state_dim_1"
    assert "raw-observation generalized SV likelihood" in native["target_identity"]


def test_p45_m2_transformed_and_approximation_routes_remain_nonexact() -> None:
    rows = _rows()
    transformed = rows["generalized_sv_transformed_residual_diagnostic"]
    approximation = rows["generalized_sv_gaussian_mixture_or_moment_matched_approximation"]

    assert transformed["claim_class"] == "DIAGNOSTIC_ONLY_NO_EQUALITY_CLAIM"
    assert transformed["same_target_comparison_authorized"] is False
    assert "conditioning" in transformed["transformation_jacobian_terms"].lower()
    assert "not exact native generalized SV" in " ".join(transformed["nonclaims"])

    assert approximation["claim_class"] == "APPROXIMATION_ONLY_NO_NATIVE_EXACT_CLAIM"
    assert approximation["same_target_comparison_authorized"] is False
    assert "not exact native generalized SV" in " ".join(approximation["nonclaims"])
    assert "moment-matched Kalman is diagnostic only" in approximation["nonclaims"]


def test_p45_m2_generalized_sv_zhaocui_two_state_route_remains_blocked() -> None:
    with pytest.raises(TypeError, match="state_dim == 1"):
        highdim.scalar_nonlinear_fixed_design_tt_value_path(
            _GeneralizedSVStateDimOnlyModel(),
            tf.constant([0.3], dtype=DTYPE),
            tf.constant([[0.18], [0.11]], dtype=DTYPE),
            _tt_config(),
        )
