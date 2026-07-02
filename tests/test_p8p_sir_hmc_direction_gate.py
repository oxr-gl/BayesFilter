from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import diagnose_p8p_sir_sinkhorn_budget as sir_budget


def test_sir_hmc_direction_gate_accepts_precise_two_combined_se() -> None:
    gate = sir_budget._sir_hmc_direction_gate(
        manual_gradient=10.0,
        regression_fd_slope=9.8,
        regression_slope_standard_error=0.1,
        seed_gradient_standard_error=0.1,
        row_residual_pass=True,
    )

    assert gate["direction_pass"] is True
    assert gate["direction_gate_reason"] == "within_2_combined_se"
    assert gate["precision_pass"] is True
    assert gate["near_equal_supportive"] is False


def test_sir_hmc_direction_gate_rejects_large_uncertainty_band() -> None:
    gate = sir_budget._sir_hmc_direction_gate(
        manual_gradient=1.0,
        regression_fd_slope=1.0,
        regression_slope_standard_error=1.0,
        seed_gradient_standard_error=1.0,
        row_residual_pass=True,
    )

    assert gate["direction_pass"] is False
    assert gate["direction_gate_reason"] == "inconclusive_precision_veto"
    assert gate["precision_pass"] is False


def test_sir_hmc_direction_gate_keeps_relative_error_supportive_only() -> None:
    gate = sir_budget._sir_hmc_direction_gate(
        manual_gradient=100.5,
        regression_fd_slope=100.0,
        regression_slope_standard_error=0.01,
        seed_gradient_standard_error=0.01,
        row_residual_pass=True,
    )

    assert gate["near_equal_supportive"] is True
    assert gate["direction_pass"] is False
    assert gate["direction_gate_reason"] == "failed_hmc_direction_gate"


def test_sir_hmc_direction_gate_requires_ladder_for_four_se_arm() -> None:
    without_certificate = sir_budget._sir_hmc_direction_gate(
        manual_gradient=10.0,
        regression_fd_slope=9.55,
        regression_slope_standard_error=0.1,
        seed_gradient_standard_error=0.1,
        row_residual_pass=True,
    )
    with_certificate = sir_budget._sir_hmc_direction_gate(
        manual_gradient=10.0,
        regression_fd_slope=9.55,
        regression_slope_standard_error=0.1,
        seed_gradient_standard_error=0.1,
        row_residual_pass=True,
        ladder_certificate=True,
    )

    assert without_certificate["within_4_combined_se"] is True
    assert without_certificate["direction_pass"] is False
    assert (
        without_certificate["direction_gate_reason"]
        == "within_4_combined_se_requires_ladder_certificate"
    )
    assert with_certificate["direction_pass"] is True
    assert (
        with_certificate["direction_gate_reason"]
        == "within_4_combined_se_with_ladder_certificate"
    )


def test_sir_hmc_direction_gate_vetoes_row_residual_before_support() -> None:
    gate = sir_budget._sir_hmc_direction_gate(
        manual_gradient=10.0,
        regression_fd_slope=10.0,
        regression_slope_standard_error=0.01,
        seed_gradient_standard_error=0.01,
        row_residual_pass=False,
    )

    assert gate["direction_pass"] is False
    assert gate["direction_gate_reason"] == "row_residual_veto"


def test_sir_hmc_direction_gate_vetoes_failed_route_prerequisite() -> None:
    gate = sir_budget._sir_hmc_direction_gate(
        manual_gradient=10.0,
        regression_fd_slope=10.0,
        regression_slope_standard_error=0.01,
        seed_gradient_standard_error=0.01,
        row_residual_pass=True,
        route_prerequisite_pass=False,
        route_prerequisite_failed_checks=["outputs_on_gpu"],
    )

    assert gate["numeric_direction_pass"] is True
    assert gate["numeric_direction_gate_reason"] == "within_2_combined_se"
    assert gate["direction_pass"] is False
    assert gate["direction_gate_reason"] == "route_prerequisite_veto"
    assert gate["route_prerequisite_failed_checks"] == ["outputs_on_gpu"]
