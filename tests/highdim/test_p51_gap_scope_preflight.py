from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m0-gap-scope-preflight-manifest-2026-06-09.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m0-gap-scope-preflight-result-2026-06-09.md"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p51_m0_gap_list_matches_p50_actionable_gaps_without_non_goals() -> None:
    manifest = _manifest()
    gap_ids = {row["id"] for row in manifest["actionable_gaps"]}

    assert gap_ids == {
        "native_generalized_sv_same_target_reference",
        "spatial_sir_production_route_architecture",
        "predator_prey_production_accuracy_tuning",
        "hmc_tier2_tier3_sampler_evidence",
        "stable_top_level_score_api",
        "smoother_if_latent_path_inference_becomes_target",
    }
    assert manifest["explicit_non_goals_not_gaps"] == [
        "adaptive TT/SIRT source-faithful filtering",
        "S&P 500 reproduction",
    ]
    assert all("adaptive" not in gap_id for gap_id in gap_ids)
    assert all("sp500" not in gap_id.lower() and "s&p" not in gap_id.lower() for gap_id in gap_ids)


def test_p51_m0_score_api_gap_preserves_original_top_level_row() -> None:
    score_gap = next(row for row in _manifest()["actionable_gaps"] if row["id"] == "stable_top_level_score_api")
    split = score_gap["split"]

    assert score_gap["p51_phase"] == "P51-M1"
    assert "BLOCKED_PUBLIC_API_DECISION" in score_gap["required_outcome"]
    assert "top-level" in score_gap["required_outcome"]
    assert split["subpackage_contract_lane"]["scope"] == "bayesfilter.highdim score API contract"
    assert split["subpackage_contract_lane"]["may_pass_without_root_export"] is True
    assert split["root_public_export_lane"]["scope"] == "root-level bayesfilter public API export"
    assert split["root_public_export_lane"]["requires_separate_policy_approval"] is True
    assert split["root_public_export_lane"]["unapproved_outcome"] == "BLOCKED_PUBLIC_API_DECISION"


def test_p51_m0_phase_tokens_are_complete_and_route_prefight_is_scoped() -> None:
    tokens = _manifest()["required_phase_tokens"]

    assert set(tokens) == {f"P51-M{index}" for index in range(9)}
    assert tokens["P51-M3"] == [
        "PASS_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT",
        "BLOCK_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT",
    ]
    assert "PASS_P51_M3_SPATIAL_SIR_PRODUCTION_ROUTE" not in tokens["P51-M3"]
    for phase_tokens in tokens.values():
        assert len(phase_tokens) == 2
        assert phase_tokens[0].startswith("PASS_")
        assert phase_tokens[1].startswith("BLOCK_")


def test_p51_m0_approval_assumptions_block_gpu_network_and_detached_execution() -> None:
    approvals = _manifest()["approval_assumptions"]

    assert approvals["cpu_only_validation"] == "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp"
    assert approvals["narrow_python_diagnostics"] == (
        "allowed only with exact paths recorded before execution"
    )
    assert approvals["gpu_runs"] == "not approved"
    assert approvals["network_fetches"] == "not approved"
    assert approvals["package_installation"] == "not approved"
    assert approvals["detached_execution"] == "not approved"


def test_p51_m0_manifest_locks_stop_conditions_and_invalid_stop_reasons() -> None:
    manifest = _manifest()
    stop_conditions = set(manifest["stop_conditions"])
    invalid_stop_reasons = set(manifest["invalid_stop_reasons"])

    assert "package installation, network fetch, credentials, or external runtime setup" in stop_conditions
    assert "changing pass/fail criteria after seeing results" in stop_conditions
    assert "changing default backend or numerical policy" in stop_conditions
    assert "modifying unrelated dirty user work" in stop_conditions
    assert "GPU or special-hardware claims without trusted-context evidence" in stop_conditions
    assert (
        "continuing after Claude and Codex do not converge after five review rounds"
        in stop_conditions
    )
    assert "fixable local test failure" in invalid_stop_reasons
    assert "concrete Claude revision request" in invalid_stop_reasons
    assert "stalled Claude prompt when a narrower read-only prompt can be tried" in invalid_stop_reasons


def test_p51_m0_result_emits_token_once_and_nonclaims_are_visible() -> None:
    text = RESULT_PATH.read_text(encoding="utf-8")

    assert text.count("status: PASS_P51_M0_GAP_SCOPE_PREFLIGHT") == 1
    assert "No HMC readiness" in text
    assert "No production readiness" in text
    assert "No smoothing support" in text
    assert "No source-faithful adaptive TT/SIRT filtering" in text
    assert "No S&P 500 reproduction" in text
