from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "docs" / "benchmarks" / "diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("contract_e_gpu_score_gate", TARGET)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {TARGET}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_hmc_direction_gate_accepts_within_2_mcse() -> None:
    module = _load_module()
    gate = module._component_hmc_direction_gate(delta=3.0, reference=100.0, mcse=2.0)

    assert gate["within_2_mcse_of_kalman"] is True
    assert gate["hmc_direction_gate"] is True
    assert gate["hmc_direction_gate_reason"] == "within_2_mcse"


def test_hmc_direction_gate_requires_certificate_for_4_mcse_arm() -> None:
    module = _load_module()
    without_certificate = module._component_hmc_direction_gate(
        delta=3.5,
        reference=1.0,
        mcse=1.0,
        mcse_decreases_with_n_certificate=False,
    )
    with_certificate = module._component_hmc_direction_gate(
        delta=3.5,
        reference=1.0,
        mcse=1.0,
        mcse_decreases_with_n_certificate=True,
    )

    assert without_certificate["within_4_mcse_of_kalman"] is True
    assert without_certificate["within_4_mcse_with_n_ladder_mcse_decrease"] is False
    assert without_certificate["within_1pct_relative_error_to_kalman"] is False
    assert without_certificate["hmc_direction_gate"] is False
    assert with_certificate["within_4_mcse_with_n_ladder_mcse_decrease"] is True
    assert with_certificate["hmc_direction_gate"] is True
    assert (
        with_certificate["hmc_direction_gate_reason"]
        == "within_4_mcse_with_n_ladder_mcse_decrease"
    )


def test_hmc_direction_gate_accepts_one_percent_relative_error() -> None:
    module = _load_module()
    gate = module._component_hmc_direction_gate(delta=0.9, reference=100.0, mcse=0.1)

    assert gate["within_2_mcse_of_kalman"] is False
    assert gate["within_4_mcse_of_kalman"] is False
    assert gate["relative_error_to_kalman"] == pytest.approx(0.009)
    assert gate["within_1pct_relative_error_to_kalman"] is True
    assert gate["hmc_direction_gate"] is True
    assert gate["hmc_direction_gate_reason"] == "within_1pct_relative_error"
