from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim


def _ready_manifest() -> dict[str, object]:
    manifest = {
        "target_id": highdim.P58_M9_AUTHOR_SIR_TARGET_ID,
        "pipeline_kind": highdim.P58_M9_SOURCE_ROUTE_PIPELINE_KIND,
        "route_class": "fixed_ttsirt_source_route",
        "storage_kind": "source_transport_object",
        "transition_interface": "sample_propagation",
        "m9_comparator_tier": "d18_execution_only",
        "rank_policy_status": "PASS_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION",
        "preconditioned_route_required": True,
        "preconditioned_route_status": "PASS_P57_M8_PRECONDITIONED_ALGORITHM5",
        "uses_contract_test_double": False,
        "uses_ukf_as_comparator": False,
        "uses_rank_memory_proxy_as_comparator": False,
    }
    manifest.update({flag: True for flag in highdim.P58_M9_REQUIRED_ASSEMBLY_FLAGS})
    return manifest


def test_p58_m9_ready_manifest_passes_only_when_all_assembly_flags_present() -> None:
    result = highdim.p58_m9_source_route_pipeline_readiness(_ready_manifest())

    assert result.status == highdim.P58_M9_READY_STATUS
    assert result.ready_for_phase9_launch is True
    assert result.blockers == ()
    assert result.manifest_payload()["allowed_comparator_tiers"] == (
        "d18_execution_only",
        "d18_same_route_rank_convergence",
        "d18_correctness_candidate",
    )


def test_p58_m9_missing_fit_artifacts_blocks_launch_readiness() -> None:
    manifest = _ready_manifest()
    manifest["has_fixed_ttsirt_fit_artifacts"] = False

    result = highdim.p58_m9_source_route_pipeline_readiness(manifest)

    assert result.status == highdim.P58_M9_BLOCK_MISSING_ASSEMBLY_STATUS
    assert result.ready_for_phase9_launch is False
    assert "missing_has_fixed_ttsirt_fit_artifacts" in result.blockers


def test_p58_m9_contract_double_or_old_route_is_source_drift() -> None:
    contract_double = _ready_manifest()
    contract_double["uses_contract_test_double"] = True
    contract_result = highdim.p58_m9_source_route_pipeline_readiness(contract_double)

    old_route = _ready_manifest()
    old_route["route_class"] = "all_grid_pairwise_transition"
    old_route["transition_interface"] = "all_grid_pairwise_transition"
    old_result = highdim.p58_m9_source_route_pipeline_readiness(old_route)

    assert contract_result.status == highdim.P58_M9_BLOCK_SOURCE_DRIFT_STATUS
    assert "contract_test_double_cannot_launch_phase9" in contract_result.blockers
    assert old_result.status == highdim.P58_M9_BLOCK_SOURCE_DRIFT_STATUS
    assert "forbidden_source_route_marker:all_grid_pairwise_transition" in old_result.blockers


def test_p58_m9_ukf_or_rank_memory_proxy_cannot_be_comparator() -> None:
    manifest = _ready_manifest()
    manifest["uses_ukf_as_comparator"] = True
    manifest["uses_rank_memory_proxy_as_comparator"] = True

    result = highdim.p58_m9_source_route_pipeline_readiness(manifest)

    assert result.status == highdim.P58_M9_BLOCK_SOURCE_DRIFT_STATUS
    assert "ukf_proxy_cannot_launch_phase9" in result.blockers
    assert "rank_memory_proxy_cannot_launch_phase9" in result.blockers


def test_p58_m9_invalid_comparator_or_missing_preconditioner_blocks() -> None:
    manifest = _ready_manifest()
    manifest["m9_comparator_tier"] = "ukf_correctness"
    manifest["preconditioned_route_status"] = "MISSING"

    result = highdim.p58_m9_source_route_pipeline_readiness(manifest)

    assert result.status == highdim.P58_M9_BLOCK_MISSING_ASSEMBLY_STATUS
    assert "missing_valid_m9_comparator_tier" in result.blockers
    assert "missing_required_preconditioned_route_pass" in result.blockers


def test_p58_m9_readiness_result_rejects_incoherent_status_payload() -> None:
    with pytest.raises(ValueError, match="ready status"):
        highdim.P58M9SourceRoutePipelineReadiness(
            status=highdim.P58_M9_READY_STATUS,
            blockers=("hidden_blocker",),
            manifest=_ready_manifest(),
        )

    with pytest.raises(ValueError, match="blocked status"):
        highdim.P58M9SourceRoutePipelineReadiness(
            status=highdim.P58_M9_BLOCK_MISSING_ASSEMBLY_STATUS,
            blockers=(),
            manifest=_ready_manifest(),
        )
