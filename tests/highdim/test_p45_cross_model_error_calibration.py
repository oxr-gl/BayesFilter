from __future__ import annotations

import json
from pathlib import Path


CALIBRATION_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p45-cross-model-error-calibration-2026-06-08.json"
)


def _calibration() -> dict[str, object]:
    return json.loads(CALIBRATION_PATH.read_text(encoding="utf-8"))


def test_p45_m5_no_promoted_comparison_rows_are_reported() -> None:
    calibration = _calibration()

    assert calibration["schema_version"] == "p45.cross_model_error_calibration.v1"
    assert calibration["promoted_same_target_rows"] == []
    assert calibration["equality_metric_policy"] == "absent_for_blocked_or_diagnostic_rows"
    assert calibration["likelihood_variance_policy"] == "explanatory_only_not_bias_excuse"


def test_p45_m5_blocked_rows_have_no_value_or_gradient_gap_metrics() -> None:
    rows = _calibration()["rows"]
    assert {row["phase"] for row in rows} == {"P45-M2", "P45-M3", "P45-M4"}
    for row in rows:
        assert row["claim_class"] in {
            "BLOCKED_NATIVE_SAME_TARGET",
            "BLOCKED_CLOSURE_SAME_TARGET_PENDING_M1_AND_REFERENCE",
        }
        assert row["same_target_comparison_reached"] is False
        assert row["value_gap"] is None
        assert row["absolute_score_gap"] is None
        assert row["relative_score_error"] is None
        assert row["directional_residuals"] == []
        assert row["reference_refinement_estimate"] is None
        assert row["why_equality_metrics_absent"]
        assert "Zhao-Cui" in row["why_equality_metrics_absent"]


def test_p45_m5_nonclaims_preserve_tiny_fixture_and_hmc_boundaries() -> None:
    calibration = _calibration()
    nonclaims = set(calibration["nonclaims"])

    assert "no HMC readiness" in nonclaims
    assert "no production score API" in nonclaims
    assert "no long/high-dimensional conclusion from tiny fixtures" in nonclaims
    assert "no likelihood variance tolerance used to excuse systematic bias" in nonclaims
