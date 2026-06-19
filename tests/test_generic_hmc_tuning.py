from __future__ import annotations

import json

import numpy as np

import bayesfilter
from bayesfilter.inference import (
    GenericHMCCandidateResult,
    GenericHMCTuningConfig,
    GenericHMCTuningResult,
    PrecomputedMassArtifact,
    run_generic_hmc_tuning_orchestration,
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
