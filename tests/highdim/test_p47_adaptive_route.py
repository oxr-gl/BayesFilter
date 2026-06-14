from __future__ import annotations

import json
from pathlib import Path


REGISTRY_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p47-target-registry-2026-06-08.json")
P46_RESULT_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-result-2026-06-08.md")


def _registry() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _rows() -> list[dict[str, object]]:
    rows = _registry()["rows"]
    assert isinstance(rows, list)
    return rows


def test_p47_m1_route_decision_is_documented_deviation_fixed_design() -> None:
    registry = _registry()

    assert registry["m1_route_decision"] == "documented-deviation fixed-design substitute"
    assert "P46 bounded multistate fixed-design TT adapter passed" in registry["m1_route_decision_source"]
    assert "no adaptive MATLAB TT-cross/SIRT reproduction evidence exists" in registry["m1_route_decision_source"]

    for row in _rows():
        assert row["m1_route_label"] == "documented-deviation fixed-design substitute"


def test_p47_m1_p46_source_evidence_exists_and_is_bounded() -> None:
    text = P46_RESULT_PATH.read_text(encoding="utf-8")

    assert "PASS_P46_RESUME_GOVERNANCE" in text
    assert "bounded multistate adapter" in text
    assert "No adaptive TT-cross/SIRT" in text or "no adaptive TT-cross/SIRT" in text
    assert "not P45 generalized-SV/SIR/predator-prey equality" in text


def test_p47_m1_no_adaptive_reproduction_token_or_claim() -> None:
    registry = _registry()
    registry_text = json.dumps(registry, sort_keys=True)

    assert "PASS_ADAPTIVE_MATLAB_TT_CROSS_SIRT_REPRODUCTION" in registry_text
    assert registry_text.count("PASS_ADAPTIVE_MATLAB_TT_CROSS_SIRT_REPRODUCTION") == 1

    for row in _rows():
        assert "PASS_ADAPTIVE_MATLAB_TT_CROSS_SIRT_REPRODUCTION" not in row["pass_tokens"]
        if row["target_id"] == "adaptive_tt_sirt_route_label":
            assert any("not adaptive MATLAB TT-cross/SIRT reproduction" in item for item in row["nonclaims"])


def test_p47_m1_downstream_route_prose_preserves_documented_deviation() -> None:
    for row in _rows():
        if row["target_id"] == "adaptive_tt_sirt_route_label":
            continue
        assert "Documented-deviation fixed-design substitute" in row["zhao_cui_route"], row["target_id"]
        assert "adaptive MATLAB TT-cross/SIRT reproduction" not in row["zhao_cui_route"]
