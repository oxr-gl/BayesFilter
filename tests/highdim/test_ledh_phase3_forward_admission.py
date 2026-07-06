from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bayesfilter.highdim.ledh_forward_contract import (
    ACTUAL_SV_ROW_ID,
    FIXED_SIR_AUSTRIA_ROW_ID,
    GENERALIZED_SV_ROW_ID,
    LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD,
    LGSSM_M3_T50_ROW_ID,
    KSC_SV_ROW_ID,
    PREDATOR_PREY_ROW_ID,
    make_actual_sv_forward_contract,
    make_fixed_sir_logscale_forward_contract,
    make_generalized_sv_forward_contract,
    make_ksc_sv_forward_contract,
    make_lgssm_m3_t50_forward_contract,
    make_predator_prey_forward_contract,
    validate_ledh_forward_contract_manifest,
)


ROOT = Path(__file__).resolve().parents[2]
LGSSM_N10000_ARTIFACT = (
    ROOT
    / "docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N10000-2026-07-03.json"
)
SIR_N10000_ARTIFACT = (
    ROOT
    / "docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N10000-2026-07-03.json"
)
SIR_TINY_CONTRACT_ARTIFACT = (
    ROOT / "docs/plans/ledh-phase3-fixed-sir-forward-contract-tiny-2026-07-06.json"
)
LGSSM_TINY_CONTRACT_ARTIFACT = (
    ROOT / "docs/plans/ledh-phase3-lgssm-forward-contract-tiny-2026-07-06.json"
)
LEDGER_PATH = (
    ROOT
    / "docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json"
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _ledger_rows() -> dict[str, dict[str, Any]]:
    return {row["row_id"]: row for row in _load(LEDGER_PATH)["rows"]}


def test_phase3_lgssm_old_full_gpu_value_artifact_normalizes_to_forward_contract() -> None:
    artifact = _load(LGSSM_N10000_ARTIFACT)
    identity = artifact["target_identity"]
    contract = make_lgssm_m3_t50_forward_contract(
        truth_theta=identity["truth_theta"],
        time_steps=artifact["shape"]["time_steps"],
        num_particles=artifact["shape"]["num_particles"],
        batch_seeds=artifact["batch_seeds"],
        full_leaderboard_row=bool(identity["full_leaderboard_row"]),
    ).to_manifest()

    assert artifact["primary_pass_same_target_value_execution"] is True
    assert artifact["runtime_gate_applicable"] is True
    assert artifact["finite_output"] is True
    assert identity["exact_value_comparator"] == (
        "tf_kalman_log_likelihood on same observations/model"
    )
    assert contract["row_id"] == LGSSM_M3_T50_ROW_ID
    assert contract["target_scalar"] == LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD
    assert contract["full_leaderboard_row"] is True
    assert validate_ledh_forward_contract_manifest(contract) == contract


def test_phase3_lgssm_current_tiny_artifact_emits_forward_contract_but_is_not_full_row() -> None:
    artifact = _load(LGSSM_TINY_CONTRACT_ARTIFACT)
    contract = artifact["target_identity"]["forward_contract"]

    assert artifact["value_status"] == "executed_prefix_value_not_full_row"
    assert artifact["primary_pass_same_target_value_execution"] is False
    assert artifact["runtime_gate_applicable"] is False
    assert contract["row_id"] == LGSSM_M3_T50_ROW_ID
    assert contract["target_scalar"] == LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD
    assert contract["full_leaderboard_row"] is False
    assert validate_ledh_forward_contract_manifest(contract) == contract


def test_phase3_fixed_sir_old_gpu_value_artifact_is_not_amended_forward_admission() -> None:
    artifact = _load(SIR_N10000_ARTIFACT)
    semantics = artifact["sir_semantics"]
    contract = make_fixed_sir_logscale_forward_contract(
        time_steps=artifact["shape"]["time_steps"],
        num_particles=artifact["shape"]["num_particles"],
        batch_seeds=artifact["batch_seeds"],
        full_leaderboard_row=True,
    ).to_manifest()

    assert artifact["primary_pass_5x_runtime_gate"] is True
    assert artifact["finite_output"] is True
    assert semantics["row_id"] == FIXED_SIR_AUSTRIA_ROW_ID
    assert semantics["target_density_used_for_correction"] is True
    assert "forward_contract" not in artifact
    assert "theta_contract" not in semantics
    assert "not exact likelihood correctness" in artifact["nonclaims"]
    assert contract["theta_contract"]["theta_coordinate_system"] == "sir_log_scale_theta"
    assert contract["theta_contract"]["theta_dimension"] == 3
    assert validate_ledh_forward_contract_manifest(contract) == contract


def test_phase3_fixed_sir_current_tiny_artifact_emits_amended_forward_contract() -> None:
    artifact = _load(SIR_TINY_CONTRACT_ARTIFACT)
    contract = artifact["forward_contract"]

    assert artifact["finite_output"] is True
    assert artifact["target_scalar"] == LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD
    assert artifact["target_output_tensor_field"] == "log_likelihood"
    assert "transition_log_density" in artifact["target_density_fields"]
    assert "observation_log_density" in artifact["target_density_fields"]
    assert "pre_flow_log_density" in artifact["proposal_flow_fields"]
    assert "forward_log_det" in artifact["proposal_flow_fields"]
    assert contract["row_id"] == FIXED_SIR_AUSTRIA_ROW_ID
    assert contract["target_scalar"] == LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD
    assert contract["full_leaderboard_row"] is False
    assert contract["theta_contract"]["theta_coordinate_system"] == "sir_log_scale_theta"
    assert contract["theta_contract"]["theta_dimension"] == 3
    assert contract["theta_contract"]["parameter_order"] == [
        "log_kappa_scale",
        "log_nu_scale",
        "log_obs_noise_scale",
    ]
    assert validate_ledh_forward_contract_manifest(contract) == contract


def test_phase3_remaining_model_contracts_validate_but_current_rows_stay_blocked() -> None:
    rows = _ledger_rows()
    contract_by_row = {
        ACTUAL_SV_ROW_ID: make_actual_sv_forward_contract(time_steps=1000).to_manifest(),
        KSC_SV_ROW_ID: make_ksc_sv_forward_contract(time_steps=1000).to_manifest(),
        PREDATOR_PREY_ROW_ID: make_predator_prey_forward_contract(time_steps=20).to_manifest(),
        GENERALIZED_SV_ROW_ID: make_generalized_sv_forward_contract(time_steps=1008).to_manifest(),
    }

    for row_id, contract in contract_by_row.items():
        assert contract["row_id"] == row_id
        assert contract["target_scalar"] == LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD
        assert validate_ledh_forward_contract_manifest(contract) == contract
        assert rows[row_id]["ledh_row_scope_decision"] == "blocked_value"
        assert "blocked" in rows[row_id]["value_status"]
        assert rows[row_id]["score_status"] == "blocked_score"

    assert contract_by_row[ACTUAL_SV_ROW_ID]["theta_contract"]["parameter_order"] == [
        "gamma_unconstrained",
        "log_beta",
    ]
    assert contract_by_row[KSC_SV_ROW_ID]["metadata"]["target_observation_policy"] == (
        "ksc_log_chi_square_gaussian_mixture_surrogate"
    )
    assert contract_by_row[PREDATOR_PREY_ROW_ID]["theta_contract"]["parameter_order"] == [
        "r",
        "K",
        "a",
        "s",
        "u",
        "v",
    ]
    assert contract_by_row[GENERALIZED_SV_ROW_ID]["theta_contract"]["parameter_order"] == [
        "gamma_unconstrained",
        "log_tau",
        "mu",
    ]
