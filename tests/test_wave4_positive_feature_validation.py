from __future__ import annotations

import argparse
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks.scalable_ot_wave4_positive_feature_validation import (  # noqa: E402
    LANE_ID,
    WAVE4_POSITIVE_PASS,
    build_result,
)


def _args(mode: str) -> argparse.Namespace:
    return argparse.Namespace(
        mode=mode,
        seeds="101,202,303",
        num_features=128,
        epsilon=0.5,
        max_iterations=160,
        convergence_threshold=1.0e-4,
        device="/CPU:0",
        device_scope="cpu",
        cuda_visible_devices=None,
        output="/tmp/wave4-positive.json",
        markdown_output="/tmp/wave4-positive.md",
    )


def test_wave4_positive_feature_smoke_contract() -> None:
    result = build_result(_args("smoke"))

    assert result["status"] == "PASS"
    assert result["wave4_status"] == WAVE4_POSITIVE_PASS
    assert result["lane_id"] == LANE_ID
    assert result["hard_vetoes"] == []
    assert result["summary"]["num_rows"] == 1
    assert result["summary"]["ranking_statistically_supported"] is False
    assert "no ranking claim" in result["nonclaims"]
    assert "no speedup claim" in result["nonclaims"]


def test_wave4_positive_feature_full_contract_has_no_ranking() -> None:
    result = build_result(_args("full"))

    assert result["status"] == "PASS"
    assert result["hard_vetoes"] == []
    assert result["entry_audit"]["entry_audit_pass"]
    assert result["summary"]["num_rows"] == 9
    assert result["inference_status"]["statistically_supported_ranking"] == "none"
    for row in result["rows"]:
        assert row["validity_pass"]
        assert row["transport_diagnostics"]["transport_matrix_materialized"] is False

