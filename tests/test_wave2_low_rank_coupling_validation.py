from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks.scalable_ot_wave2_low_rank_coupling_validation import (
    WAVE2_STATUS_PASS,
    ValidationSettings,
    build_wave2_low_rank_validation_result,
)


def test_wave2_low_rank_validation_result_contract() -> None:
    result = build_wave2_low_rank_validation_result(ValidationSettings())

    assert result["status"] == "PASS"
    assert result["wave2_status"] == WAVE2_STATUS_PASS
    assert result["owner"] == "peer_agent"
    assert result["validity_pass"]
    assert result["hard_vetoes"] == []
    assert result["source_route"] == "extension_or_invention"
    assert result["candidate_record"]["candidate_id"] == "wave2_low_rank_coupling_validation"
    assert result["candidate_record"]["transport_object"]["kind"] == "low_rank_coupling_factors"
    assert result["candidate_record"]["transport_object"]["materialized"] is False
    assert result["summary"]["max_factor_marginal_residual"] <= 5.0e-3
    assert result["summary"]["max_induced_row_residual"] <= 5.0e-3
    assert result["summary"]["max_induced_column_residual"] <= 5.0e-3
    assert result["summary"]["max_materialized_tiny_apply_parity"] <= 1.0e-10
    assert "no ranking claim" in result["nonclaims"]
    assert "no speedup claim" in result["nonclaims"]


def test_wave2_low_rank_validation_rows_preserve_source_boundary() -> None:
    result = build_wave2_low_rank_validation_result(ValidationSettings())

    assert len(result["rows"]) == 3
    for row in result["rows"]:
        assert row["validity_pass"]
        assert row["hard_vetoes"] == []
        assert row["finite_factors"]
        assert row["finite_particles"]
        assert row["nonnegative_factors"]
        assert row["positive_g"]
        assert row["source_route"] == "extension_or_invention"
        assert row["source_route_components"]["cost_nudged_assignment_kernel"] == "extension_or_invention"
        assert row["source_route_components"]["dykstra_style_projection"] == "source_faithful"
