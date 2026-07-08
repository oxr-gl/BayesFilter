from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

from bayesfilter.testing.neutra_gpu_training_preflight_tf import (
    ADMITTED_NEUTRA_GPU_PREFLIGHT_ROUTE_IDS,
    DEFERRED_NEUTRA_GPU_PREFLIGHT_ROUTE_IDS,
    LGSSM_QR_ROUTE_ID,
    MODEL_B_SVD_CUBATURE_ROUTE_ID,
    MODEL_B_SVD_UKF_ROUTE_ID,
    NEUTRA_GPU_PREFLIGHT_NONCLAIMS,
    NeuTraGPUPreflightError,
    NeuTraGPUTrainingPreflightConfig,
    admitted_neutra_gpu_preflight_route_ids,
    neutra_gpu_preflight_route_inventory,
    phase9_error_payload,
    run_neutra_gpu_training_preflight,
)


PHASE9_PASS_ARTIFACT = Path(
    "docs/plans/"
    "bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-"
    "2026-07-07.json"
)
PHASE9_XLA_BLOCKER_ARTIFACT = Path(
    "docs/plans/"
    "bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-"
    "xla-blocker-2026-07-07.json"
)


def test_neutra_gpu_preflight_route_inventory_is_fail_closed() -> None:
    inventory = neutra_gpu_preflight_route_inventory()
    by_route = {entry["route_id"]: entry for entry in inventory}

    assert admitted_neutra_gpu_preflight_route_ids() == (
        LGSSM_QR_ROUTE_ID,
        MODEL_B_SVD_UKF_ROUTE_ID,
        MODEL_B_SVD_CUBATURE_ROUTE_ID,
    )
    for route_id in ADMITTED_NEUTRA_GPU_PREFLIGHT_ROUTE_IDS:
        assert by_route[route_id]["status"] == "admitted"
    for route_id in DEFERRED_NEUTRA_GPU_PREFLIGHT_ROUTE_IDS:
        assert by_route[route_id]["status"] == "deferred"


def test_neutra_gpu_preflight_config_records_training_policy(tmp_path) -> None:
    config = NeuTraGPUTrainingPreflightConfig(output_path=tmp_path / "preflight.json")
    payload = config.normalized()

    assert payload["training_execution_target"] == "gpu_required"
    assert payload["cpu_training_fallback_policy"] == "forbidden"
    assert payload["external_sample_generation_policy"] == (
        "multicore_cpu_separate_phase_not_run_here"
    )
    assert payload["jit_compile"] is False
    assert payload["xla_readiness_policy"] == (
        "deferred_to_explicit_gate_not_required_for_phase9_preflight"
    )
    assert payload["full_training_executed"] is False
    assert payload["optimizer_step_executed"] is False
    assert payload["hmc_executed"] is False
    assert payload["nonclaims"] == NEUTRA_GPU_PREFLIGHT_NONCLAIMS


def test_neutra_gpu_preflight_rejects_cpu_hidden_training(tmp_path) -> None:
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"

    with pytest.raises(NeuTraGPUPreflightError, match="CUDA_VISIBLE_DEVICES=-1"):
        run_neutra_gpu_training_preflight(
            NeuTraGPUTrainingPreflightConfig(output_path=tmp_path / "blocked.json")
        )


@pytest.mark.parametrize("route_id", DEFERRED_NEUTRA_GPU_PREFLIGHT_ROUTE_IDS)
def test_neutra_gpu_preflight_rejects_deferred_routes(route_id: str, tmp_path) -> None:
    config = NeuTraGPUTrainingPreflightConfig(
        route_ids=(route_id,),
        output_path=tmp_path / "blocked.json",
    )

    with pytest.raises(NeuTraGPUPreflightError, match="not admitted"):
        run_neutra_gpu_training_preflight(config)


def test_neutra_gpu_preflight_rejects_unknown_routes(tmp_path) -> None:
    config = NeuTraGPUTrainingPreflightConfig(
        route_ids=("not-a-route",),
        output_path=tmp_path / "blocked.json",
    )

    with pytest.raises(NeuTraGPUPreflightError, match="unknown Phase 9 route id"):
        run_neutra_gpu_training_preflight(config)


def test_phase9_error_payload_preserves_nonclaims(tmp_path) -> None:
    config = NeuTraGPUTrainingPreflightConfig(output_path=tmp_path / "blocked.json")
    payload = phase9_error_payload(RuntimeError("example"), config=config)

    assert payload["passed"] is False
    assert payload["decision"] == "BLOCK_PHASE9_GPU_NEUTRA_TRAINING_PREFLIGHT"
    assert payload["full_training_executed"] is False
    assert payload["optimizer_step_executed"] is False
    assert payload["hmc_executed"] is False
    assert payload["external_sample_generation_executed"] is False
    assert payload["nonclaims"] == NEUTRA_GPU_PREFLIGHT_NONCLAIMS


def test_phase9_gpu_preflight_artifact_records_passed_gpu_boundary() -> None:
    payload = json.loads(PHASE9_PASS_ARTIFACT.read_text(encoding="utf-8"))
    normalized = dict(payload)
    normalized.pop("artifact_hash", None)
    normalized.pop("artifact_hash_semantics", None)
    stable_hash = hashlib.sha256(
        json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    assert payload["passed"] is True
    assert payload["decision"] == "PASS_PHASE9_GPU_NEUTRA_TRAINING_PREFLIGHT"
    assert payload["config"]["training_execution_target"] == "gpu_required"
    assert payload["config"]["cpu_training_fallback_policy"] == "forbidden"
    assert payload["config"]["jit_compile"] is False
    assert payload["artifact_hash"] == f"sha256:{stable_hash}"
    assert payload["artifact_hash_semantics"] == (
        "stable_json_sha256_excluding_artifact_hash_fields"
    )
    assert len(payload["route_results"]) == len(ADMITTED_NEUTRA_GPU_PREFLIGHT_ROUTE_IDS)
    for row in payload["route_results"]:
        assert row["passed"] is True
        assert row["full_training_executed"] is False
        assert row["optimizer_step_executed"] is False
        assert row["hmc_executed"] is False
        assert row["external_sample_generation_executed"] is False
        assert row["finite_checks"] == {
            "loss_finite": True,
            "shift_gradient_finite": True,
            "raw_scale_gradient_finite": True,
        }
        assert row["device_checks"]["all_outputs_on_gpu"] is True
        assert all("GPU" in device for device in row["device_checks"]["output_devices"])


def test_phase9_xla_blocker_artifact_preserves_separate_jit_failure() -> None:
    payload = json.loads(PHASE9_XLA_BLOCKER_ARTIFACT.read_text(encoding="utf-8"))

    assert payload["passed"] is False
    assert payload["decision"] == "BLOCK_PHASE9_GPU_NEUTRA_TRAINING_PREFLIGHT"
    assert payload["config"]["jit_compile"] is True
    assert "fixed tensor list size" in payload["error_message"]
    assert payload["full_training_executed"] is False
    assert payload["optimizer_step_executed"] is False
    assert payload["hmc_executed"] is False
    assert payload["external_sample_generation_executed"] is False
    assert payload["nonclaims"] == list(NEUTRA_GPU_PREFLIGHT_NONCLAIMS)
