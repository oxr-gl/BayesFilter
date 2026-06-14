from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-manifest-2026-06-09.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-result-2026-06-09.md"
)
P47_M5B_MANIFEST = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-m5b-production-row-manifest-2026-06-09.json"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p51_m4_manifest_uses_same_p47_p50_horizon25_target_and_tolerances() -> None:
    manifest = _manifest()
    source = json.loads(P47_M5B_MANIFEST.read_text(encoding="utf-8"))

    assert manifest["schema_version"] == "p51.predator_prey_production_tuning.v1"
    assert manifest["status"] == "PASS_P51_M4_PREDATOR_PREY_PRODUCTION_TUNING"
    assert manifest["target_id"] == source["target_id"] == "predator_prey_production_filtering"
    assert manifest["source_blocker"] == "BLOCKED_M5B_PRODUCTION_ACCURACY_TUNING"
    assert manifest["target_family"] == source["target_family"]
    assert manifest["production_tolerances"] == source["production_tolerances"]
    assert manifest["reference"]["horizon"] == 25
    assert manifest["reference"]["reference_order"] == 9


def test_p51_m4_candidate_ladder_passes_only_order9_rank10() -> None:
    rows = {row["candidate_id"]: row for row in _manifest()["candidate_ladder"]}

    assert rows["P51-M4-0"]["decision"] == "FAIL_PRESERVED_PRODUCTION_TOLERANCES"
    assert rows["P51-M4-1"]["decision"] == "FAIL_PRESERVED_PRODUCTION_TOLERANCES"
    assert rows["P51-M4-2"]["decision"] == "PASS_PRESERVED_PRODUCTION_TOLERANCES"
    assert rows["P51-M4-2"]["fit_order"] == 9
    assert rows["P51-M4-2"]["rank"] == 10
    assert all(rows["P51-M4-2"]["passes"].values())
    assert rows["P51-M4-2"]["deterministic_replay"] is True
    assert rows["P51-M4-2"]["abs_log_likelihood_gap"] < 5.0
    assert rows["P51-M4-2"]["max_step_log_normalizer_gap"] < 1.0
    assert rows["P51-M4-2"]["max_state_mean_component_error"] < 5.0
    assert rows["P51-M4-2"]["max_covariance_entry_error"] < 8.0


def test_p51_m4_tolerances_were_not_loosened_after_results() -> None:
    manifest = _manifest()

    assert manifest["criterion_change_after_results"] == "forbidden_not_performed"
    assert manifest["tuning_ladder_predeclared_in_ledger"] is True
    assert manifest["promotion_basis"] == "all preserved P47/P50 production tolerances pass"
    for row in manifest["candidate_ladder"]:
        assert set(row["passes"]) == {
            "abs_log_likelihood_gap_lt",
            "max_step_log_normalizer_gap_lt",
            "max_state_mean_component_error_lt",
            "max_covariance_entry_error_lt",
            "truth_path_prey_rmse_lt",
            "truth_path_predator_rmse_lt",
            "deterministic_replay_required",
        }


def test_p51_m4_nonclaims_exclude_hmc_preconditioning_and_native_claims() -> None:
    nonclaims = set(_manifest()["nonclaims"])

    assert "no HMC readiness" in nonclaims
    assert "no production HMC readiness" in nonclaims
    assert "no nonlinear preconditioning usefulness claim" in nonclaims
    assert "no native non-Gaussian predator-prey correctness" in nonclaims
    assert "no source-faithful adaptive TT/SIRT filtering" in nonclaims
    assert "no S&P 500 reproduction" in nonclaims


def test_p51_m4_result_emits_token_once_and_promoted_candidate_is_visible() -> None:
    text = RESULT_PATH.read_text(encoding="utf-8")

    assert text.count("status: PASS_P51_M4_PREDATOR_PREY_PRODUCTION_TUNING") == 1
    assert "P51-M4-2" in text
    assert "fit order 9" in text
    assert "rank 10" in text
    assert "No HMC readiness" in text
