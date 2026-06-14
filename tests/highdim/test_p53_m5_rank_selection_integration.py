from __future__ import annotations

import json
from pathlib import Path

import pytest

import bayesfilter.highdim as highdim


M4D_MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4d-scaling-route-admission-manifest-2026-06-10.json"
)
M5_MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m5-rank-selection-integration-manifest-2026-06-10.json"
)
M5_RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m5-rank-selection-integration-result-2026-06-10.md"
)


def _admitted_route() -> dict[str, object]:
    manifest = json.loads(M4D_MANIFEST_PATH.read_text(encoding="utf-8"))
    route = dict(manifest["route"])
    route["admission_token"] = "PASS_P53_M4D_SCALING_ROUTE_ADMISSION"
    return route


def test_p53_m5_rank_selection_requires_m4d_admission_token() -> None:
    route = _admitted_route()
    route.pop("admission_token")

    with pytest.raises(ValueError, match="PASS_P53_M4D_SCALING_ROUTE_ADMISSION"):
        highdim.p53_select_fixed_rank_from_admitted_route(
            route,
            dimension=18,
        )


def test_p53_m5_rank_selection_blocks_when_no_candidate_rank_feasible() -> None:
    result = highdim.p53_select_fixed_rank_from_admitted_route(
        _admitted_route(),
        dimension=18,
        candidate_ranks=(1, 2, 4, 8, 16, 32),
    )
    payload = result.manifest_payload()

    assert payload["status"] == "BLOCK_P53_M5_RANK_SELECTION_INTEGRATION"
    assert payload["selected_rank"] is None
    assert payload["feasible_ranks"] == ()
    assert payload["preflight"]["r_max"] == 0
    assert payload["blocker"] == "no candidate rank is below the hard memory ceiling"
    assert payload["rank_mutation_allowed_in_likelihood"] is False
    assert payload["claim_class"] == highdim.P53_RANK_SELECTION_CLAIM
    assert "no filtering correctness" in payload["nonclaims"]
    assert "no d=18 spatial SIR result" in payload["nonclaims"]


def test_p53_m5_direct_d18_local_route_metadata_exceeds_cap() -> None:
    model = highdim.p30_spatial_sir_fixture_model(9)

    with pytest.raises(ValueError, match="memory forecast exceeds cap"):
        highdim.spatial_sir_local_scaling_route_metadata(
            model,
            highdim.LocalNeighborhoodScalingRouteConfig(
                basis_order=3,
                tt_rank_left=1,
                tt_rank_right=1,
                memory_cap_bytes=32 * 1024**3,
                branch_id="p53-m5-d18-min-rank-probe",
            ),
        )


def test_p53_m5_result_manifest_preserves_blocker_and_forbids_downstream_tokens() -> None:
    manifest = json.loads(M5_MANIFEST_PATH.read_text(encoding="utf-8"))
    result = M5_RESULT_PATH.read_text(encoding="utf-8")

    assert manifest["schema_version"] == "p53.rank_selection_integration.v1"
    assert manifest["status"] == "BLOCK_P53_M5_RANK_SELECTION_INTEGRATION"
    assert manifest["rank_selection"]["status"] == "BLOCK_P53_M5_RANK_SELECTION_INTEGRATION"
    assert manifest["rank_selection"]["selected_rank"] is None
    assert manifest["rank_selection"]["feasible_ranks"] == []
    assert manifest["rank_selection"]["preflight"]["r_max"] == 0
    assert manifest["rank_selection"]["rank_mutation_allowed_in_likelihood"] is False
    assert manifest["tokens_emitted"] == ["BLOCK_P53_M5_RANK_SELECTION_INTEGRATION"]
    assert "PASS_P53_M5_RANK_SELECTION_INTEGRATION" in manifest["forbidden_tokens"]
    assert "PASS_P53_M6_SPATIAL_SIR_D18" in manifest["forbidden_tokens"]
    assert "BLOCK_P53_M5_RANK_SELECTION_INTEGRATION" in result
    assert "P53-M6 must not start" in result
