from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-m0-governance-target-lock-manifest-2026-06-10.json"
)
MASTER_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-rank-calibrated-spatial-sir-master-program-2026-06-10.md"
)
RUNBOOK_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-visible-gated-execution-runbook-2026-06-10.md"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-m0-governance-target-lock-result-2026-06-10.md"
)
LEDGER_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-visible-execution-ledger-2026-06-10.md"
)
SUBPLAN_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-m0-governance-target-lock-subplan-2026-06-10.md"
)
P51_M3_MANIFEST = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-manifest-2026-06-09.json"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p52_m0_locks_to_p51_spatial_sir_route_blocker() -> None:
    manifest = _manifest()
    p51 = json.loads(P51_M3_MANIFEST.read_text(encoding="utf-8"))
    source = manifest["source_blocker"]

    assert manifest["schema_version"] == "p52.governance_target_lock.v1"
    assert manifest["status"] == "PASS_P52_M0_GOVERNANCE_TARGET_LOCK"
    assert source["id"] == "spatial_sir_production_route_architecture"
    assert source["token"] == p51["source_blocker"] == "BLOCKED_M4B_ROUTE_ARCHITECTURE"
    assert "all-axes retained-grid" in source["blocked_route"]
    assert "fixed-rank factorized" in source["replacement_target"]


def test_p52_m0_role_contract_keeps_codex_visible_and_claude_read_only() -> None:
    role = _manifest()["role_contract"]
    runbook = RUNBOOK_PATH.read_text(encoding="utf-8")

    assert role["supervisor_executor"] == "Codex"
    assert role["reviewer"] == "Claude Code read-only"
    assert role["claude_may_execute_or_edit"] is False
    assert role["detached_execution_allowed"] is False
    assert "A Claude worker process is a reviewer tool invocation" in runbook
    assert "Claude worker calls must not execute phases" in runbook


def test_p52_m0_evidence_classes_do_not_promote_ukf_or_preflight_to_truth() -> None:
    classes = {row["class"]: row for row in _manifest()["allowed_evidence_classes"]}
    subplan = SUBPLAN_PATH.read_text(encoding="utf-8")

    assert classes["correctness_reference"]["required_support"].startswith("exact")
    assert classes["rank_self_convergence"]["allowed_claim"].startswith(
        "fixed-route rank self-convergence"
    )
    assert classes["scout_baseline"]["required_support"].endswith("scout_not_truth")
    assert classes["memory_preflight"]["allowed_claim"] == (
        "memory and rank feasibility forecast only"
    )
    assert classes["scaling_stress"]["required_support"].startswith("d=18 prerequisites")
    assert "HMC readiness remains a forbidden overclaim for M0" in subplan
    assert "HMC-readiness diagnostic" not in subplan


def test_p52_m0_dimension_policy_caps_first_full_filtering_at_d50() -> None:
    rows = {int(row["dimension"]): row for row in _manifest()["dimension_policy"]}
    master = MASTER_PATH.read_text(encoding="utf-8")

    assert rows[18]["maximum_first_claim"] == "filtering_calibration_candidate"
    assert rows[50]["maximum_first_claim"] == "scaling_stress_or_rank_self_convergence"
    assert rows[100]["maximum_first_claim"] == "ukf_scout_and_memory_preflight"
    assert "The reasonable maximum first full filtering test is `d = 50`" in master
    assert "Dimension `100`\nis reasonable for UKF scouting and memory preflight" in master


def test_p52_m0_rank_policy_forbids_adaptive_hmc_rank_growth() -> None:
    rank = _manifest()["rank_policy"]

    assert rank["candidate_ranks"] == [2, 4, 8, 16, 32]
    assert rank["allow_rank_adaptation_inside_hmc_likelihood"] is False
    assert rank["memory_cap_gb"] == 32
    assert rank["requires_r_max_before_execution"] is True
    assert rank["requires_R_eff_source"] is True


def test_p52_m0_forbidden_claims_and_nonclaims_cover_known_overclaims() -> None:
    forbidden = set(_manifest()["forbidden_claims"])
    nonclaims = set(_manifest()["nonclaims"])
    result = RESULT_PATH.read_text(encoding="utf-8")
    ledger = LEDGER_PATH.read_text(encoding="utf-8")

    assert "UKF correctness oracle" in forbidden
    assert "d=100 filtering correctness from scout or preflight evidence" in forbidden
    assert "dense all-pairs route as production path" in forbidden
    assert "HMC readiness from finite values or finite gradients" in forbidden
    assert "no implementation completed by M0" in nonclaims
    assert "no production spatial SIR readiness" in nonclaims
    assert "no d=100 filtering correctness" in nonclaims
    assert "No implementation" in result
    assert "No filtering correctness" in result
    assert "No production spatial SIR readiness" in result
    assert "No HMC readiness" in result
    assert "No GPU readiness" in result
    assert "No d=100 filtering correctness" in result
    assert "no implementation, filtering correctness, HMC readiness" in ledger


def test_p52_m0_phase_tokens_are_complete_and_symmetric() -> None:
    tokens = _manifest()["required_phase_tokens"]

    assert set(tokens) == {f"P52-M{index}" for index in range(9)}
    for phase, pair in tokens.items():
        assert len(pair) == 2, phase
        assert pair[0].startswith(f"PASS_{phase.replace('-', '_')}")
        assert pair[1].startswith(f"BLOCK_{phase.replace('-', '_')}")


def test_p52_m0_human_stop_conditions_match_visible_runbook() -> None:
    stops = set(_manifest()["human_required_stop_conditions"])
    runbook = RUNBOOK_PATH.read_text(encoding="utf-8")
    result = RESULT_PATH.read_text(encoding="utf-8")
    ledger = LEDGER_PATH.read_text(encoding="utf-8")

    expected = {
        "project-direction decision not already in the reviewed plan",
        "package installation, network fetch, credentials, or environment setup",
        "destructive git or filesystem action",
        "changing pass/fail criteria after seeing results",
        "changing default policy",
        "modifying unrelated dirty user work",
        "interpreting GPU/special hardware results without trusted-context evidence",
        "continuing after Claude and Codex do not converge after five review rounds",
    }
    assert expected <= stops
    for phrase in expected:
        assert phrase in runbook
    assert "VALIDATION_PASSED_PENDING_CLAUDE" in ledger
    assert "status: PASS_P52_M0_GOVERNANCE_TARGET_LOCK" in result
