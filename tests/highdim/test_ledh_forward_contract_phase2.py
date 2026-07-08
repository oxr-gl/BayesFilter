from __future__ import annotations

import pytest

from bayesfilter.highdim.ledh_forward_contract import (
    FIXED_SIR_AUSTRIA_ROW_ID,
    LEDH_CORRECTION_FORMULA,
    LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD,
    LGSSM_M3_T50_ROW_ID,
    MAIN_OBSERVED_DATA_ROW_SCOPE,
    PARAMETERIZED_SIR_DIAGNOSTIC_ROW_ID,
    SIR_LOG_SCALE_PARAMETER_ORDER,
    LEDHForwardLikelihoodContract,
    LEDHThetaContract,
    make_fixed_sir_logscale_forward_contract,
    make_lgssm_m3_t50_forward_contract,
    make_parameterized_sir_diagnostic_forward_contract,
    validate_ledh_forward_contract_manifest,
)
from docs.benchmarks import benchmark_two_lane_highdim_ledh_inclusive_results as inclusive


def test_lgssm_forward_contract_separates_target_and_proposal_fields() -> None:
    contract = make_lgssm_m3_t50_forward_contract(
        truth_theta=[0.72, 0.55, 0.35, 0.35, 0.45],
        time_steps=50,
        num_particles=1000,
        batch_seeds=[81120, 81121],
        full_leaderboard_row=True,
    ).to_manifest()

    assert contract["row_id"] == LGSSM_M3_T50_ROW_ID
    assert contract["target_scalar"] == LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD
    assert contract["output_tensor_field"] == "log_likelihood"
    assert contract["correction_formula"] == LEDH_CORRECTION_FORMULA
    assert set(contract["target_density_fields"]) == {
        "transition_log_density",
        "observation_log_density",
    }
    assert "pre_flow_log_density" in contract["proposal_flow_fields"]
    assert "forward_log_det" in contract["proposal_flow_fields"]
    assert not set(contract["target_density_fields"]).intersection(
        contract["proposal_flow_fields"]
    )
    assert validate_ledh_forward_contract_manifest(contract) == contract


def test_forward_contract_rejects_proposal_scalar_as_target() -> None:
    theta = LEDHThetaContract(
        row_id=LGSSM_M3_T50_ROW_ID,
        theta_coordinate_system="physical_benchmark_exact_oracle",
        theta_dimension=5,
        parameter_order=["phi1", "phi2", "phi3", "q_scale", "r_scale"],
        truth_theta=[0.72, 0.55, 0.35, 0.35, 0.45],
    )

    with pytest.raises(ValueError, match="proposal scalar"):
        LEDHForwardLikelihoodContract(
            row_id=LGSSM_M3_T50_ROW_ID,
            row_scope=MAIN_OBSERVED_DATA_ROW_SCOPE,
            theta_contract=theta,
            target_scalar="proposal_log_likelihood",
        )


def test_forward_contract_rejects_missing_target_density() -> None:
    theta = LEDHThetaContract(
        row_id=LGSSM_M3_T50_ROW_ID,
        theta_coordinate_system="physical_benchmark_exact_oracle",
        theta_dimension=5,
        parameter_order=["phi1", "phi2", "phi3", "q_scale", "r_scale"],
        truth_theta=[0.72, 0.55, 0.35, 0.35, 0.45],
    )

    with pytest.raises(ValueError, match="missing target density fields"):
        LEDHForwardLikelihoodContract(
            row_id=LGSSM_M3_T50_ROW_ID,
            row_scope=MAIN_OBSERVED_DATA_ROW_SCOPE,
            theta_contract=theta,
            target_density_fields=["observation_log_density"],
        )


def test_fixed_sir_forward_contract_enforces_amended_logscale_theta() -> None:
    contract = make_fixed_sir_logscale_forward_contract(
        time_steps=20,
        num_particles=10000,
        batch_seeds=[81120],
    ).to_manifest()

    theta = contract["theta_contract"]
    assert contract["row_id"] == FIXED_SIR_AUSTRIA_ROW_ID
    assert contract["row_scope"] == MAIN_OBSERVED_DATA_ROW_SCOPE
    assert theta["theta_coordinate_system"] == "sir_log_scale_theta"
    assert theta["theta_dimension"] == 3
    assert theta["parameter_order"] == list(SIR_LOG_SCALE_PARAMETER_ORDER)
    assert theta["truth_theta"] == [0.0, 0.0, 0.0]
    assert contract["target_scalar"] == LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD
    assert contract["score_status"] == "blocked_score_until_same_target_no_tape_gate"
    assert validate_ledh_forward_contract_manifest(contract) == contract


def test_fixed_sir_forward_contract_rejects_no_free_theta() -> None:
    with pytest.raises(ValueError, match="no_free_theta"):
        LEDHThetaContract(
            row_id=FIXED_SIR_AUSTRIA_ROW_ID,
            theta_coordinate_system="no_free_theta",
            theta_dimension=1,
            parameter_order=["none"],
            truth_theta=[0.0],
        )


def test_parameterized_sir_diagnostic_cannot_be_promoted_to_full_row() -> None:
    contract = make_parameterized_sir_diagnostic_forward_contract(
        time_steps=1,
        num_particles=10000,
        batch_seeds=[81120],
    ).to_manifest()
    assert contract["row_id"] == PARAMETERIZED_SIR_DIAGNOSTIC_ROW_ID
    assert contract["row_scope"] == "legacy_scoped_parameterized_sir_diagnostic"
    assert contract["full_leaderboard_row"] is False
    assert validate_ledh_forward_contract_manifest(contract) == contract

    theta = LEDHThetaContract(
        row_id=PARAMETERIZED_SIR_DIAGNOSTIC_ROW_ID,
        theta_coordinate_system="sir_log_scale_theta",
        theta_dimension=3,
        parameter_order=SIR_LOG_SCALE_PARAMETER_ORDER,
        truth_theta=[0.0, 0.0, 0.0],
    )
    with pytest.raises(ValueError, match="cannot be promoted"):
        LEDHForwardLikelihoodContract(
            row_id=PARAMETERIZED_SIR_DIAGNOSTIC_ROW_ID,
            row_scope=MAIN_OBSERVED_DATA_ROW_SCOPE,
            theta_contract=theta,
            full_leaderboard_row=True,
        )


def test_inclusive_rows_synthesize_forward_contract_for_older_artifacts() -> None:
    lgssm_artifact = {
        "average_log_likelihood_estimate": {"mean": -1.0, "mcse": None, "sample_sd": None},
        "total_log_likelihood_estimate": {"mean": -50.0, "mcse": None, "sample_sd": None},
        "target_identity": {
            "same_target_status": "same_target_ledh_value_score_capable",
            "truth_theta": [0.72, 0.55, 0.35, 0.35, 0.45],
            "full_leaderboard_row": True,
        },
        "score_status": "blocked_score_not_run",
        "value_status": "executed_same_target_value",
        "shape": {"num_particles": 1000, "time_steps": 50},
        "batch_seeds": [81120],
        "warm_call_timing_summary_seconds": {"mean": 0.1},
        "compile_and_first_call_seconds": 1.0,
        "exact_value_comparison": {},
        "ess_min_by_seed": [1.0],
        "nonclaims": [],
    }
    row = inclusive._lgssm_ledh_row(  # noqa: SLF001
        lgssm_artifact,
        artifact_path=inclusive.ROOT / "docs/plans/fake-lgssm.json",
    )
    assert row["target_scalar"] == LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD
    assert row["forward_contract"]["row_id"] == LGSSM_M3_T50_ROW_ID

    sir_artifact = {
        "log_likelihood": [-10.0],
        "shape": {"num_particles": 10000, "time_steps": 20},
        "batch_seeds": [81120],
        "score_status": "blocked_score_until_same_target_no_tape_gate",
        "warm_call_timing_summary_seconds": {"mean": 0.2},
        "compile_and_first_call_seconds": 1.2,
        "ess_min_by_seed": [1.0],
        "nonclaims": [],
    }
    row = inclusive._sir_ledh_row(  # noqa: SLF001
        sir_artifact,
        artifact_path=inclusive.ROOT / "docs/plans/fake-sir.json",
    )
    assert row["target_scalar"] == LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD
    assert row["forward_contract"]["row_id"] == FIXED_SIR_AUSTRIA_ROW_ID
    assert row["forward_contract"]["theta_contract"]["theta_coordinate_system"] == (
        "sir_log_scale_theta"
    )
