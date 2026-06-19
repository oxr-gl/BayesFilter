from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


def _load_smoke_module():
    script_path = (
        Path(__file__).resolve().parents[2]
        / "scripts/p76_corrected_heldout_metric_smoke.py"
    )
    spec = importlib.util.spec_from_file_location("p76_corrected_metric_smoke", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _expected_corrected_alpha() -> list[float]:
    return [0.0, 0.125, 0.375, 0.5]


def _expected_historical_alpha() -> list[float]:
    return [2.5 / 16.5, 5.5 / 16.5, 5.25 / 16.5, 3.25 / 16.5]


def test_phase9_smoke_payload_hand_checks_metric_wiring() -> None:
    module = _load_smoke_module()
    payload = module.run_smoke(
        run_manifest={
            "command": "unit-test",
            "cpu_only": True,
            "cuda_visible_devices": "-1",
        }
    )

    assert payload["status"] == module.STATUS
    assert payload["schema_version"] == module.SCHEMA_VERSION
    assert payload["train_step_count"] == 0
    assert payload["optimizer_used"] is False
    assert payload["generated_target_cloud_used"] is False
    assert payload["default_behavior_changed"] is False
    assert payload["fixture"]["role"] == "heldout_metric"
    assert payload["fixture"]["provenance_label"] == "manual_metric_fixture"
    assert payload["fixture"]["tau"] == pytest.approx(2.5)
    assert payload["fixture"]["defensive_q0_values"] == pytest.approx([1.0, 1.0, 1.0, 1.0])
    assert payload["corrected_alpha"] == pytest.approx(_expected_corrected_alpha())
    assert payload["expected_corrected_alpha"] == pytest.approx(_expected_corrected_alpha())
    assert payload["corrected_alpha_max_abs_error"] == pytest.approx(0.0)
    boundary = payload["historical_helper_boundary_only"]
    assert boundary["label"] == "historical_helper_boundary_only"
    assert boundary["alpha"] == pytest.approx(_expected_historical_alpha())
    assert boundary["expected_alpha"] == pytest.approx(_expected_historical_alpha())
    assert boundary["alpha_max_abs_error"] == pytest.approx(0.0)
    assert boundary["alpha_l1_distance_from_corrected"] > 0.0
    rho = payload["rho_theta_values"]
    normalizer = payload["normalizer"]
    corrected_alpha = payload["corrected_alpha"]
    expected_ce = -sum(
        alpha * module.math.log(rho_value)
        for alpha, rho_value in zip(corrected_alpha, rho)
    ) + module.math.log(normalizer)
    assert payload["reconstructed_heldout_cross_entropy"] == pytest.approx(expected_ce)
    assert payload["metric_payload"]["heldout_cross_entropy"] == pytest.approx(expected_ce)
    assert payload["heldout_cross_entropy_reconstruction_abs_error"] == pytest.approx(0.0)
    assert payload["manual_fixture_hand_checks"] == {
        "corrected_alpha_matches_expected": True,
        "historical_alpha_matches_expected": True,
        "ce_reconstruction_matches_metric": True,
        "old_new_alpha_separated": True,
    }
    assert all(payload["finite_flags"].values())
    assert payload["metric_payload"]["role"] == "heldout_metric"
    assert payload["metric_payload"]["provenance_label"] == "manual_metric_fixture"
    assert payload["metric_payload"]["not_training_or_selection"] is True
    assert "not fit-quality evidence" in payload["nonclaims"]


def test_phase9_smoke_cli_writes_parseable_json(tmp_path) -> None:
    module = _load_smoke_module()
    output = tmp_path / "phase9-smoke.json"

    assert module.main(["--output", str(output)]) == 0

    payload = json.loads(output.read_text())
    assert payload["status"] == module.STATUS
    assert payload["corrected_alpha"] == pytest.approx(_expected_corrected_alpha())
    assert payload["historical_helper_boundary_only"]["alpha"] == pytest.approx(
        _expected_historical_alpha()
    )
    assert payload["manual_fixture_hand_checks"]["old_new_alpha_separated"] is True
