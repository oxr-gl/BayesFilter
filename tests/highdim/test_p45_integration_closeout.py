from __future__ import annotations

import json
from pathlib import Path


CLOSEOUT_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p45-integration-closeout-ledger-2026-06-08.json")


def _closeout() -> dict[str, object]:
    return json.loads(CLOSEOUT_PATH.read_text(encoding="utf-8"))


def test_p45_m6_closeout_has_all_prior_phase_artifacts() -> None:
    closeout = _closeout()

    assert closeout["schema_version"] == "p45.integration_closeout.v1"
    assert closeout["run_id"] == "p45-codex-supervised-20260608-055034"
    phases = closeout["phase_statuses"]
    assert [row["phase"] for row in phases] == [f"P45-M{index}" for index in range(6)]
    for row in phases:
        assert row["status"] == f"PASS_{row['phase'].replace('-', '_')}_CODE_GOVERNANCE"
        for key in ("result_note", "evidence_manifest", "claude_review_ledger"):
            assert Path(row[key]).exists(), row[key]


def test_p45_m6_closeout_separates_promoted_from_blocked_rows() -> None:
    closeout = _closeout()

    assert closeout["promoted_comparisons"] == []
    blocked = set(closeout["diagnostic_or_blocked_rows"])
    assert "generalized_sv_native_raw_observation" in blocked
    assert "spatial_sir_additive_gaussian_closure" in blocked
    assert "predator_prey_additive_gaussian_rk4_closure" in blocked
    assert len(blocked) == 7


def test_p45_m6_closeout_classifies_blockers_and_nonclaims() -> None:
    closeout = _closeout()

    blocker_classes = {row["class"] for row in closeout["blockers"]}
    assert blocker_classes == {
        "implementation",
        "numerical_reference",
        "target_definition",
        "scientific_evidence",
    }
    nonclaims = set(closeout["nonclaims"])
    assert "no CUT4--Zhao-Cui equality" in nonclaims
    assert "no HMC readiness" in nonclaims
    assert "no production score API" in nonclaims
    assert "no stable public API" in nonclaims
    assert "no paper-scale Zhao-Cui reproduction" in nonclaims
