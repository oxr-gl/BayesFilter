from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-hmc-readiness-tier-manifest-2026-06-09.json"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p50_m7_tiers_are_ordered_and_production_hmc_is_not_passed() -> None:
    manifest = _manifest()
    tiers = {row["tier"]: row for row in manifest["tiers"]}

    assert manifest["schema_version"] == "p50.hmc_readiness_tiers.v1"
    assert list(tiers) == [
        "TIER_0_VALUE_PATH",
        "TIER_1_LOCAL_VALUE_AND_GRADIENT",
        "TIER_2_HAMILTONIAN_LEAPFROG",
        "TIER_3_SHORT_CHAIN_SAMPLER",
        "TIER_4_PRODUCTION_HMC",
    ]
    assert tiers["TIER_2_HAMILTONIAN_LEAPFROG"]["pass_status"] == "not_run"
    assert tiers["TIER_3_SHORT_CHAIN_SAMPLER"]["pass_status"] == "not_run"
    assert tiers["TIER_4_PRODUCTION_HMC"]["pass_status"] == "not_passed"


def test_p50_m7_promotion_rule_blocks_finite_gradient_and_short_chain_proxies() -> None:
    rule = _manifest()["promotion_rule"]

    assert rule["finite_gradient_is_not_hmc_ready"] is True
    assert rule["short_chain_without_veto_checks_is_not_hmc_ready"] is True
    assert rule["cpu_only_runs_make_no_gpu_claim"] is True
    assert "TIER_2_HAMILTONIAN_LEAPFROG" in rule["hmc_ready_requires"]
    assert "TIER_3_SHORT_CHAIN_SAMPLER" in rule["hmc_ready_requires"]
    assert rule["production_hmc_ready_requires"] == ["TIER_4_PRODUCTION_HMC"]


def test_p50_m7_rows_do_not_promote_m5_m6_diagnostics_to_hmc_readiness() -> None:
    rows = {row["row_id"]: row for row in _manifest()["rows"]}

    sv = rows["sv_strict_rows"]
    generalized = rows["generalized_sv_native"]
    nonlinear = rows["spatial_sir_predator_prey_lower_rung"]

    assert sv["highest_supported_tier"] == "TIER_1_LOCAL_VALUE_AND_GRADIENT"
    assert sv["hmc_readiness_status"] == "blocked_tier2_tier3_not_run"
    assert "no HMC readiness" in sv["nonclaims"]
    assert generalized["hmc_readiness_status"] == "blocked_reference_missing"
    assert "no native generalized SV same-target equality" in generalized["nonclaims"]
    assert nonlinear["hmc_readiness_status"] == "blocked_uncertified_gradient_or_production_blocker"
    assert "no certified nonlinear-model gradient correctness" in nonlinear["nonclaims"]


def test_p50_m7_nonclaims_exclude_hmc_gpu_source_and_sp500() -> None:
    manifest = _manifest()
    nonclaims = set(manifest["nonclaims"])
    decision = manifest["phase_decision"]

    assert decision["status"] == "PASS_TIER_DEFINITIONS_AND_GUARDS_NO_HMC_READY_PROMOTION"
    assert "Tier 2, Tier 3, and production HMC readiness are not run or passed" in decision["reason"]
    assert "no HMC readiness" in nonclaims
    assert "no production HMC readiness" in nonclaims
    assert "no GPU readiness" in nonclaims
    assert "no source-faithful adaptive TT/SIRT filtering" in nonclaims
    assert "no S&P 500 reproduction" in nonclaims
