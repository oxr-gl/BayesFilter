from __future__ import annotations

import json
import subprocess
import sys

import pytest

import bayesfilter.highdim as highdim

FIT_SAMPLE_COUNT = highdim.P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT


def test_p59_9d_runner_manifest_passes_p58_after_9a_9b_9c() -> None:
    result = highdim.p59_author_sir_runner_manifest_path(
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )

    assert result.status == highdim.P59_9D_PASS_STATUS
    assert result.ready_for_validation_ladder is True
    assert result.readiness.status == highdim.P58_M9_READY_STATUS
    assert result.readiness.ready_for_phase9_launch is True
    assert result.assembly_result is not None
    assert result.assembly_result.status == highdim.P59_9B_PASS_STATUS
    assert result.manifest["consumed_artifacts"]["p59_9a_status"] == highdim.P59_9A_PASS_STATUS
    assert result.manifest["consumed_artifacts"]["p59_9b_status"] == highdim.P59_9B_PASS_STATUS
    assert result.manifest["consumed_artifacts"]["p59_9c_status"] == highdim.P59_9C_PASS_STATUS
    assert result.manifest["p58_manifest"]["has_m9_runner_manifest_path"] is True
    assert result.manifest["fit_sample_count"] == FIT_SAMPLE_COUNT
    assert all(
        row["row_count"] == FIT_SAMPLE_COUNT
        and row["status"] != "branch_fit_row_adequacy_failed"
        for row in result.manifest["row_adequacy_by_step"]
    )


def test_p59_9d_runner_manifest_preserves_claim_boundary() -> None:
    result = highdim.p59_author_sir_runner_manifest_path(
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )

    assert result.manifest["ready_for_validation_ladder"] is True
    assert "no P59-9e validation has been run" in result.manifest["nonclaims"]
    assert "no d18 filtering accuracy claim" in result.manifest["nonclaims"]
    assert result.manifest["p58_manifest"]["uses_contract_test_double"] is False
    assert result.manifest["p58_manifest"]["uses_ukf_as_comparator"] is False
    assert result.manifest["p58_manifest"]["uses_rank_memory_proxy_as_comparator"] is False
    assert result.manifest["p58_manifest"]["route_class"] == "fixed_ttsirt_source_route"


def test_p59_9d_blocks_invalid_comparator_tier() -> None:
    result = highdim.p59_author_sir_runner_manifest_path(
        comparator_tier="ukf_correctness",
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )

    assert result.status == highdim.P59_9D_BLOCK_STATUS
    assert result.ready_for_validation_ladder is False
    assert "invalid_m9_comparator_tier" in result.blockers
    assert "missing_valid_m9_comparator_tier" in result.blockers


def test_p59_9d_script_writes_manifest(tmp_path) -> None:
    output = tmp_path / "p59-9d-manifest.json"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/p59_author_sir_m9_runner_manifest.py",
            "--output",
            str(output),
            "--sample-count",
            "1",
        ],
        check=True,
        cwd=".",
        text=True,
        capture_output=True,
    )
    data = json.loads(output.read_text(encoding="utf-8"))

    assert highdim.P59_9D_PASS_STATUS in completed.stdout
    assert data["status"] == highdim.P59_9D_PASS_STATUS
    assert data["p58_readiness"]["status"] == highdim.P58_M9_READY_STATUS
    assert data["ready_for_validation_ladder"] is True
    assert data["fit_sample_count"] == FIT_SAMPLE_COUNT
    assert all(
        row["row_count"] == FIT_SAMPLE_COUNT
        for row in data["row_adequacy_by_step"]
    )


def test_p59_9d_explicit_under_rowed_fit_count_fails_closed() -> None:
    with pytest.raises(ValueError, match="branch_fit_row_adequacy_failed"):
        highdim.p59_author_sir_runner_manifest_path(
            sample_count=1,
            fit_sample_count=2,
        )


def test_p59_9d_rejects_incoherent_result_payload() -> None:
    assembly = highdim.p59_author_sir_step_spec_assembly(
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )
    readiness = highdim.p58_m9_source_route_pipeline_readiness(
        assembly.manifest["p58_partial_manifest"]
    )

    with pytest.raises(ValueError, match="P58 ready"):
        highdim.P59AuthorSIRRunnerManifestResult(
            status=highdim.P59_9D_PASS_STATUS,
            blockers=(),
            assembly_result=assembly,
            readiness=readiness,
            manifest_path="manifest.json",
            manifest={},
        )
