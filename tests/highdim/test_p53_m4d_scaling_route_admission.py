from __future__ import annotations

import json
from pathlib import Path


M0_MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m0-planning-failure-lock-manifest-2026-06-10.json"
)
M4A_MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-manifest-2026-06-10.json"
)
M4B_MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4b-scaling-route-implementation-manifest-2026-06-10.json"
)
M4C_MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-manifest-2026-06-10.json"
)
M4D_MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4d-scaling-route-admission-manifest-2026-06-10.json"
)
M4D_RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4d-scaling-route-admission-result-2026-06-10.md"
)


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def test_p53_m4d_reconciles_m4a_m4b_m4c_route_identity() -> None:
    m4a = _load(M4A_MANIFEST_PATH)
    m4b = _load(M4B_MANIFEST_PATH)
    m4c = _load(M4C_MANIFEST_PATH)
    m4d = _load(M4D_MANIFEST_PATH)

    m4a_route = m4a["selected_route"]
    m4b_route = m4b["route"]
    m4c_route = m4c["route"]
    m4d_route = m4d["route"]
    for field in ("route_id", "route_class", "selected_design"):
        values = {
            m4a_route[field],
            m4b_route[field],
            m4c_route[field],
            m4d_route[field],
        }
        assert len(values) == 1, field

    assert m4a["status"] == "PASS_P53_M4A_SCALING_ROUTE_DERIVATION"
    assert m4b["status"] == "PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION"
    assert m4c["status"] == "PASS_P53_M4C_SCALING_ROUTE_TIEOUT"
    assert m4d["status"] == "PASS_P53_M4D_SCALING_ROUTE_ADMISSION"
    assert m4d_route["route_width_bound_name"] == "R_eff"
    assert int(m4d_route["example_j3_R_eff"]) > 0
    assert int(m4d_route["example_j3_memory_forecast_bytes"]) > 0


def test_p53_m4d_prerequisite_evidence_paths_and_statuses_are_pinned() -> None:
    manifest = _load(M4D_MANIFEST_PATH)
    evidence = manifest["prerequisite_evidence"]

    assert evidence["P53-M4A"]["artifact"] == str(M4A_MANIFEST_PATH)
    assert evidence["P53-M4B"]["artifact"] == str(M4B_MANIFEST_PATH)
    assert evidence["P53-M4C"]["artifact"] == str(M4C_MANIFEST_PATH)
    assert evidence["P53-M4A"]["required_status"] == "PASS_P53_M4A_SCALING_ROUTE_DERIVATION"
    assert evidence["P53-M4B"]["required_status"] == "PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION"
    assert evidence["P53-M4C"]["required_status"] == "PASS_P53_M4C_SCALING_ROUTE_TIEOUT"
    assert evidence["P53-M4C"]["evidence_class"] == "scaling_route_tieout"


def test_p53_m4d_emits_only_admission_token_and_preserves_nonclaims() -> None:
    manifest = _load(M4D_MANIFEST_PATH)
    result = M4D_RESULT_PATH.read_text(encoding="utf-8")

    assert manifest["schema_version"] == "p53.scaling_route_admission.v1"
    assert manifest["admission_scope"] == (
        "rank_selection_and_dimension_phase_entry_not_filtering_correctness"
    )
    assert manifest["tokens_emitted"] == ["PASS_P53_M4D_SCALING_ROUTE_ADMISSION"]
    assert "PASS_P53_M5_RANK_SELECTION_INTEGRATION" in manifest["forbidden_tokens"]
    assert "PASS_P53_M8_INTEGRATION_CLOSEOUT" in manifest["forbidden_tokens"]
    assert "PASS_P53_M4_SCALING_ROUTE_GATE" in manifest["forbidden_tokens"]
    assert "no rank-selection result" in manifest["nonclaims"]
    assert "no d=18 spatial SIR result" in manifest["nonclaims"]
    assert "PASS_P53_M4D_SCALING_ROUTE_ADMISSION" in result
    assert "This admission is not a filtering-correctness claim" in result


def test_p53_m4d_downstream_admission_uses_new_m4d_token_not_old_m4_gate() -> None:
    m0_manifest = _load(M0_MANIFEST_PATH)
    lower_rung_tokens = {
        "PASS_P53_M0_PLANNING_FAILURE_LOCK",
        "PASS_P53_M1_ROUTE_DESIGN_MATH",
        "PASS_P53_M2_ROUTE_IMPLEMENTATION",
        "PASS_P53_M3_LOWER_RUNG_DENSE_TIEOUT",
        "PASS_P53_M4A_SCALING_ROUTE_DERIVATION",
        "PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION",
        "PASS_P53_M4C_SCALING_ROUTE_TIEOUT",
    }
    old_gate_tokens = lower_rung_tokens | {"PASS_P53_M4_SCALING_ROUTE_GATE"}
    m4d_tokens = lower_rung_tokens | {"PASS_P53_M4D_SCALING_ROUTE_ADMISSION"}

    assert not _can_admit_phase(
        phase="P53-M5",
        emitted_tokens=old_gate_tokens,
        m0_manifest=m0_manifest,
    )
    assert _can_admit_phase(
        phase="P53-M5",
        emitted_tokens=m4d_tokens,
        m0_manifest=m0_manifest,
    )
    assert not _can_admit_phase(
        phase="P53-M8",
        emitted_tokens=m4d_tokens,
        m0_manifest=m0_manifest,
    )

    substantive_tokens = m4d_tokens | {
        "PASS_P53_M5_RANK_SELECTION_INTEGRATION",
        "PASS_P53_M6_SPATIAL_SIR_D18",
        "PASS_P53_M7_SPATIAL_SIR_D50_D100",
    }
    assert _can_admit_phase(
        phase="P53-M8",
        emitted_tokens=substantive_tokens,
        m0_manifest=m0_manifest,
    )


def test_p53_m4d_m5_m8_downstream_policy_is_explicit() -> None:
    manifest = _load(M4D_MANIFEST_PATH)

    assert manifest["downstream_phase_admission"]["P53-M5"] == (
        "admitted_after_PASS_P53_M4D_SCALING_ROUTE_ADMISSION"
    )
    assert manifest["downstream_phase_admission"]["P53-M6"] == (
        "blocked_until_PASS_P53_M5_RANK_SELECTION_INTEGRATION"
    )
    assert manifest["downstream_phase_admission"]["P53-M7"] == (
        "blocked_until_PASS_P53_M6_SPATIAL_SIR_D18"
    )
    assert manifest["downstream_phase_admission"]["P53-M8"] == (
        "blocked_until_PASS_P53_M5_M6_M7_OUTCOMES"
    )
