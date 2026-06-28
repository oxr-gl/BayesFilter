from __future__ import annotations

import json

import numpy as np

import bayesfilter
from bayesfilter.inference import (
    GenericHMCFixedGridScaleSelection,
    GenericHMCCandidateResult,
    GenericHMCTuningConfig,
    GenericHMCTuningResult,
    PrecomputedMassArtifact,
    classify_hmc_fixed_grid_acceptance,
    run_generic_hmc_tuning_orchestration,
    select_hmc_fixed_grid_scale,
)
from bayesfilter.inference.fixed_trajectory_hmc_tuning_v2 import (
    run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2,
)


class _ToyGaussianAdapter:
    parameter_dim = 2
    parameter_names = ("x0", "x1")

    def adapter_signature(self) -> str:
        return "toy_gaussian_generic_hmc_adapter_v1"


def _mass_artifact() -> PrecomputedMassArtifact:
    return PrecomputedMassArtifact.from_covariance(
        position=np.zeros(2),
        covariance=np.array([[1.0, 0.2], [0.2, 1.5]], dtype=float),
        adapter_signature="toy_gaussian_generic_hmc_adapter_v1",
        position_role="map",
        covariance_source="toy_gaussian_exact_covariance",
        source="toy_gaussian_map_mass",
        jitter=0.0,
    )


def _config() -> GenericHMCTuningConfig:
    return GenericHMCTuningConfig(
        step_size_candidates=(0.20, 0.25),
        num_leapfrog_step_candidates=(3,),
        acceptance_band=(0.65, 0.75),
        tuning_seed=(20260614, 11),
        heldout_seed=(20260614, 12),
        policy_source="tests/test_generic_hmc_tuning.py",
    )


def test_generic_hmc_tuning_artifact_selects_and_serializes_stably():
    result = run_generic_hmc_tuning_orchestration(
        _ToyGaussianAdapter(),
        _mass_artifact(),
        _config(),
        candidate_acceptance_rates=(0.62, 0.72),
        heldout_acceptance_rate=0.70,
        checkpoint_root="artifacts/generic-hmc",
    )
    payload = result.payload()

    assert isinstance(result, GenericHMCTuningResult)
    assert result.passed is True
    assert isinstance(result.selected_candidate, GenericHMCCandidateResult)
    assert payload["adapter_signature"] == "toy_gaussian_generic_hmc_adapter_v1"
    assert payload["target_dimension"] == 2
    assert payload["map_provenance"]["position_role"] == "map"
    assert payload["mass_provenance"]["mass_artifact_signature"]
    assert payload["selected_mass"]["adapter_signature"] == (
        "toy_gaussian_generic_hmc_adapter_v1"
    )
    assert payload["selected_step_size"] == 0.25
    assert payload["selected_num_leapfrog_steps"] == 3
    assert payload["selected_trajectory_length"] == 0.75
    assert payload["selected_seed"] == (20260614, 11)
    assert payload["no_further_adaptation"] is True
    assert payload["candidate_results"][1]["candidate_index"] == 1
    assert payload["candidate_results"][1]["checkpoint_payload_hash"]
    assert payload["checkpoint_paths"]["selected_candidate"].endswith(
        "tuning_candidate_0001.json"
    )
    assert payload["checkpoint_paths"]["heldout_candidate"].endswith(
        "heldout_candidate_0001.json"
    )
    assert payload["checkpoint_payload"]["selected_seed"] == (20260614, 11)
    assert payload["checkpoint_payload"]["no_further_adaptation"] is True
    assert payload["checkpoint_payload"]["candidate_payload_hash"]
    assert payload["heldout_confirmation"]["status"] == "passed"
    assert payload["diagnostic_roles"]["heldout_confirmation"] == (
        "promotion_veto_repair_trigger"
    )
    assert payload["reports_posterior_convergence"] is False
    assert "no posterior convergence claim" in payload["nonclaims"]
    assert json.loads(json.dumps(payload, sort_keys=True))
    assert result.artifact_hash == run_generic_hmc_tuning_orchestration(
        _ToyGaussianAdapter(),
        _mass_artifact(),
        _config(),
        candidate_acceptance_rates=(0.62, 0.72),
        heldout_acceptance_rate=0.70,
        checkpoint_root="artifacts/generic-hmc",
    ).artifact_hash


def test_generic_hmc_tuning_is_exported_and_not_private_v2_fixture():
    assert bayesfilter.GenericHMCCandidateResult is GenericHMCCandidateResult
    assert bayesfilter.GenericHMCTuningConfig is GenericHMCTuningConfig
    assert bayesfilter.GenericHMCTuningResult is GenericHMCTuningResult
    assert bayesfilter.run_generic_hmc_tuning_orchestration is (
        run_generic_hmc_tuning_orchestration
    )
    assert run_generic_hmc_tuning_orchestration.__module__ == (
        "bayesfilter.inference.generic_hmc_tuning"
    )

    assert run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2.__module__ == (
        "bayesfilter.inference.fixed_trajectory_hmc_tuning_v2"
    )
    assert run_generic_hmc_tuning_orchestration is not (
        run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2
    )


def test_fixed_grid_scale_selector_expands_grid_until_acceptance_not_too_high():
    selection = select_hmc_fixed_grid_scale(
        base_step_size_candidates=(0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.5),
        num_leapfrog_step_candidates=(1, 2, 3, 4, 8, 16, 32),
        scale_candidates=(1.0, 2.0, 4.0, 8.0),
        pilot_acceptance_rates=(0.97, 0.91, 0.82, 0.60),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
        pilot_base_step_size=0.5,
        pilot_num_leapfrog_steps=8,
    )

    assert isinstance(selection, GenericHMCFixedGridScaleSelection)
    assert selection.passed is True
    assert selection.selected_scale == 4.0
    assert selection.status == "scale_selected_warning_band"
    assert selection.scaled_step_size_candidates == (
        0.2, 0.3, 0.4, 0.6, 0.8, 1.2, 2.0)
    payload = selection.payload()
    assert payload["artifact_type"] == "bayesfilter_hmc_fixed_grid_scale_selection"
    assert payload["probes"][0]["acceptance_class"] == "too_high"
    assert payload["probes"][2]["pilot_step_size"] == 2.0
    assert payload["passed"] is True
    assert "no posterior convergence claim" in payload["nonclaims"]


def test_fixed_grid_scale_selector_fails_closed_when_all_pilots_too_high():
    selection = select_hmc_fixed_grid_scale(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(8,),
        scale_candidates=(1.0, 2.0, 4.0),
        pilot_acceptance_rates=(0.98, 0.96, 0.91),
    )

    assert selection.passed is False
    assert selection.selected_scale is None
    assert selection.scaled_step_size_candidates == ()
    assert selection.status == "scale_search_failed_high_acceptance"
    assert selection.vetoes == (
        "all_pilot_acceptance_rates_above_fallback_max_or_invalid",)


def test_fixed_grid_scale_selector_is_public_and_classifies_boundaries():
    assert bayesfilter.select_hmc_fixed_grid_scale is select_hmc_fixed_grid_scale
    assert bayesfilter.classify_hmc_fixed_grid_acceptance is (
        classify_hmc_fixed_grid_acceptance
    )
    assert classify_hmc_fixed_grid_acceptance(0.65) == "in_band"
    assert classify_hmc_fixed_grid_acceptance(0.75) == "in_band"
    assert classify_hmc_fixed_grid_acceptance(0.8501) == "too_high"
    assert classify_hmc_fixed_grid_acceptance(None) == "invalid"
