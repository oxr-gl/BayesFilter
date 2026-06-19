from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks.scalable_ot_wave2_positive_feature_diagnostics import (
    WAVE2_STATUS_PASS,
    build_wave2_positive_feature_result,
)


def test_wave2_positive_feature_result_contract() -> None:
    result = build_wave2_positive_feature_result()

    assert result["status"] == "PASS"
    assert result["wave2_status"] == WAVE2_STATUS_PASS
    assert result["owner"] == "current_agent"
    assert result["validity_pass"]
    assert result["hard_vetoes"] == []
    assert result["semantic_class"] == "semantic_replacement"
    assert result["candidate_record"]["candidate_id"] == "wave2_positive_feature_sinkhorn_diagnostic"
    assert result["candidate_record"]["transport_object"]["kind"] == "kernel_factors"
    assert result["candidate_record"]["transport_object"]["materialized"] is False
    assert result["summary"]["max_row_residual"] <= 5.0e-2
    assert result["summary"]["max_column_residual"] <= 5.0e-2
    assert "no ranking claim" in result["nonclaims"]
    assert "no speedup claim" in result["nonclaims"]
