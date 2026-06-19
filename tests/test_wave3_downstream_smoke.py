from __future__ import annotations

import argparse
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks.scalable_ot_wave3_downstream_smoke import (
    WAVE3_ARTIFACT_AUDIT_PASS,
    WAVE3_SMOKE_PASS,
    build_result,
)


def _args(mode: str) -> argparse.Namespace:
    return argparse.Namespace(
        mode=mode,
        low_rank_json="docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.json",
        positive_feature_json="docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.json",
        low_rank_rank=3,
        low_rank_assignment_epsilon=0.45,
        positive_feature_count=128,
        epsilon=0.5,
        device="/CPU:0",
        device_scope="cpu",
        cuda_visible_devices=None,
        output="/tmp/wave3.json",
        markdown_output="/tmp/wave3.md",
    )


def test_wave3_artifact_audit_passes_existing_wave2_outputs() -> None:
    result = build_result(_args("artifact-audit"))

    assert result["status"] == "PASS"
    assert result["wave3_status"] == WAVE3_ARTIFACT_AUDIT_PASS
    assert result["hard_vetoes"] == []
    assert result["artifact_audit"]["artifact_audit_pass"]


def test_wave3_smoke_preserves_no_ranking_contract() -> None:
    result = build_result(_args("smoke"))

    assert result["status"] == "PASS"
    assert result["wave3_status"] == WAVE3_SMOKE_PASS
    assert result["hard_vetoes"] == []
    assert len(result["rows"]) == 4
    assert "no ranking claim" in result["nonclaims"]
    assert "no speedup claim" in result["nonclaims"]
