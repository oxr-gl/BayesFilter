from __future__ import annotations

import json
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64
REGISTRY_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json")


def _rows() -> dict[str, dict[str, object]]:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {row["target_id"]: row for row in registry["rows"]}


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def test_p45_m3_spatial_sir_closure_remains_blocked_for_equality() -> None:
    row = _rows()["spatial_sir_additive_gaussian_closure"]

    assert row["same_target_comparison_authorized"] is False
    assert row["claim_class"] == "BLOCKED_CLOSURE_SAME_TARGET_PENDING_M1_AND_REFERENCE"
    assert row["route_statuses"]["reference"] == "pending_dense_refined_closure_reference"
    assert row["route_statuses"]["cut4"] == "available_diagnostic_only"
    assert row["route_statuses"]["zhao_cui"] == "blocked_current_scalar_nonlinear_route_requires_state_dim_1"
    assert "closure likelihood is not native SIR filtering correctness" in row["nonclaims"]
    assert "J=2,3 are factorized/replicated panels" in row["dimension_panel_convention"]


def test_p45_m3_native_sir_route_is_not_defined_or_authorized() -> None:
    row = _rows()["spatial_sir_native_or_nongaussian_route"]

    assert row["same_target_comparison_authorized"] is False
    assert row["claim_class"] == "BLOCKED_NATIVE_ROUTE_UNSPECIFIED"
    assert row["blocker_class"] == "BLOCKED_NATIVE_TARGET_REFERENCE_AND_IMPLEMENTATION"
    assert all(str(status).startswith("blocked") for status in row["route_statuses"].values())
    assert "Blocked pending scientific target definition" in row["parameterization"]


def test_p45_m3_spatial_sir_j1_state_dim2_zhaocui_route_remains_blocked() -> None:
    model = highdim.p30_spatial_sir_fixture_model(1)
    config = highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(model.state_dim()),),
        measure_convention=_convention(),
        deterministic_seed="p45-m3-spatial-sir-zhaocui-blocked",
    )

    assert model.state_dim() == 2
    with pytest.raises(TypeError, match="scalar nonlinear dense value path requires state_dim == 1"):
        highdim.FixedBranchSquaredTTFilter(config).log_likelihood(
            model,
            tf.zeros([0], dtype=DTYPE),
            tf.constant([[14.10], [11.85]], dtype=DTYPE),
        )
