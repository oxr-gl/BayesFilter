from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4-scaling-route-gate-manifest-2026-06-10.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4-scaling-route-gate-result-2026-06-10.md"
)
RUNBOOK_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-visible-gated-execution-runbook-2026-06-10.md"
)
M0_MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m0-planning-failure-lock-manifest-2026-06-10.json"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _can_admit_phase(
    *,
    phase: str,
    emitted_tokens: set[str],
    m0_manifest: dict[str, object],
) -> bool:
    required_tokens = m0_manifest["required_gate_tokens"]
    for predecessor in m0_manifest["dependency_dag"][phase]:
        pass_token = required_tokens[predecessor][0]
        if pass_token not in emitted_tokens:
            return False
    return True


def test_p53_m4_blocks_when_only_lower_rung_dense_equivalent_route_exists() -> None:
    manifest = _manifest()
    result = RESULT_PATH.read_text(encoding="utf-8")

    assert manifest["schema_version"] == "p53.scaling_route_gate.v1"
    assert manifest["status"] == "BLOCK_P53_M4_SCALING_ROUTE_GATE"
    assert manifest["amendment_status"] == (
        "historical_blocker_superseded_by_P53_M4A_M4D_phase_split"
    )
    assert manifest["active_resume_target"] == "P53-M4A"
    assert manifest["lower_rung_evidence_available"]["route_class"] == (
        "lower_rung_dense_equivalent"
    )
    assert manifest["lower_rung_evidence_available"]["claim_class"] == (
        "interface_tieout_only_not_scaling"
    )
    assert "BLOCK_P53_M4_SCALING_ROUTE_GATE" in result
    assert "This is a successful gated behavior" in result


def test_p53_m4_manifest_names_missing_scaling_route_requirements() -> None:
    manifest = _manifest()
    required = manifest["scaling_route_required"]
    blocker = manifest["blocker"]

    assert required["route_class"] == "scaling_route"
    assert "local-neighborhood sparse transition contraction" in required["allowed_designs"]
    assert "TT-MPO factorized transition contraction" in required["allowed_designs"]
    assert "R_eff or conservative route-width bound" in required["required_properties"]
    assert "No local-neighborhood sparse contraction has been implemented." in blocker["why_not_pass"]
    assert "No TT-MPO transition operator has been implemented." in blocker["why_not_pass"]
    assert "Only the lower-rung dense-equivalent streaming route has passed" in blocker["summary"]


def test_p53_m4_block_token_does_not_admit_m5_m6_m7() -> None:
    m0_manifest = json.loads(M0_MANIFEST_PATH.read_text(encoding="utf-8"))
    lower_rung_plus_block = {
        "PASS_P53_M0_PLANNING_FAILURE_LOCK",
        "PASS_P53_M1_ROUTE_DESIGN_MATH",
        "PASS_P53_M2_ROUTE_IMPLEMENTATION",
        "PASS_P53_M3_LOWER_RUNG_DENSE_TIEOUT",
        "BLOCK_P53_M4_SCALING_ROUTE_GATE",
    }

    assert not _can_admit_phase(
        phase="P53-M5",
        emitted_tokens=lower_rung_plus_block,
        m0_manifest=m0_manifest,
    )
    assert not _can_admit_phase(
        phase="P53-M6",
        emitted_tokens=lower_rung_plus_block,
        m0_manifest=m0_manifest,
    )
    assert not _can_admit_phase(
        phase="P53-M7",
        emitted_tokens=lower_rung_plus_block,
        m0_manifest=m0_manifest,
    )


def test_p53_m4_forbidden_tokens_and_runbook_stop_discipline_are_consistent() -> None:
    manifest = _manifest()
    runbook = RUNBOOK_PATH.read_text(encoding="utf-8")

    assert manifest["tokens_emitted"] == ["BLOCK_P53_M4_SCALING_ROUTE_GATE"]
    assert "PASS_P53_M4_SCALING_ROUTE_GATE" in manifest["forbidden_tokens"]
    assert "PASS_P53_M5_RANK_SELECTION_INTEGRATION" in manifest["forbidden_tokens"]
    assert manifest["downstream_phase_admission"]["P53-M5"] == (
        "blocked_without_PASS_P53_M4D_SCALING_ROUTE_ADMISSION"
    )
    assert "A clean phase boundary is not a stop condition" in runbook
    assert "a human-required blocker from the stop-condition list" in runbook
