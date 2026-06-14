from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m0-planning-failure-lock-manifest-2026-06-10.json"
)
MASTER_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-factorized-transition-repair-master-program-2026-06-10.md"
)
RUNBOOK_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-visible-gated-execution-runbook-2026-06-10.md"
)
M0_SUBPLAN_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m0-planning-failure-lock-subplan-2026-06-10.md"
)
M4A_SUBPLAN_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-subplan-2026-06-10.md"
)
M4D_SUBPLAN_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4d-scaling-route-admission-subplan-2026-06-10.md"
)
P52_STOP_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-visible-stop-handoff-2026-06-10.md"
)
REVIEW_LEDGER_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-claude-review-ledger-2026-06-10.md"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _can_admit_phase(
    *,
    phase: str,
    emitted_tokens: set[str],
    manifest: dict[str, object],
) -> bool:
    dag = manifest["dependency_dag"]
    required_tokens = manifest["required_gate_tokens"]
    for predecessor in dag[phase]:
        predecessor_pass = required_tokens[predecessor][0]
        if predecessor_pass not in emitted_tokens:
            return False
    return True


def test_p53_m0_preserves_p52_stop_as_source_failure() -> None:
    manifest = _manifest()
    p52_stop = P52_STOP_PATH.read_text(encoding="utf-8")

    assert manifest["schema_version"] == "p53.planning_failure_lock.v1"
    assert manifest["status"] == "PASS_P53_M0_PLANNING_FAILURE_LOCK"
    assert manifest["source_failure"]["stop_token"] == (
        "BLOCK_P52_FACTORIZED_TRANSITION_ROUTE"
    )
    assert "BLOCK_P52_FACTORIZED_TRANSITION_ROUTE" in p52_stop
    assert "route contract gate" in manifest["source_failure"]["planning_error"]


def test_p53_m0_dependency_dag_requires_scaling_route_before_rank_and_scaling() -> None:
    manifest = _manifest()
    dag = manifest["dependency_dag"]
    master = MASTER_PATH.read_text(encoding="utf-8")
    runbook = RUNBOOK_PATH.read_text(encoding="utf-8")

    assert dag["P53-M4A"] == ["P53-M1", "P53-M2", "P53-M3"]
    assert dag["P53-M4B"] == ["P53-M4A"]
    assert dag["P53-M4C"] == ["P53-M4B"]
    assert dag["P53-M4D"] == ["P53-M4C"]
    assert dag["P53-M5"] == ["P53-M4D"]
    assert dag["P53-M6"] == ["P53-M4D", "P53-M5"]
    assert dag["P53-M7"] == ["P53-M4D", "P53-M6"]
    assert dag["P53-M8"] == [
        "P53-M0",
        "P53-M1",
        "P53-M2",
        "P53-M3",
        "P53-M4D",
        "P53-M5",
        "P53-M6",
        "P53-M7",
    ]
    assert "PASS_P53_M4D_SCALING_ROUTE_ADMISSION" in master
    assert "PASS_P53_M4D_SCALING_ROUTE_ADMISSION" in runbook
    assert "P53-M5 through P53-M8 may not start" in runbook


def test_p53_m0_evidence_classes_separate_lower_rung_from_scaling_route() -> None:
    manifest = _manifest()
    classes = {row["class"]: row for row in manifest["evidence_classes"]}
    master = MASTER_PATH.read_text(encoding="utf-8")
    m4a_subplan = M4A_SUBPLAN_PATH.read_text(encoding="utf-8")
    m4d_subplan = M4D_SUBPLAN_PATH.read_text(encoding="utf-8")

    assert classes["lower_rung_dense_equivalent_implementation"]["phase"] == "P53-M2"
    assert classes["lower_rung_dense_tieout"]["phase"] == "P53-M3"
    assert classes["scaling_route_choice_derivation"]["phase"] == "P53-M4A"
    assert classes["scaling_route_implementation"]["phase"] == "P53-M4B"
    assert classes["scaling_route_tieout"]["phase"] == "P53-M4C"
    assert classes["scaling_route_admission"]["phase"] == "P53-M4D"
    assert "lower_rung_dense_equivalent" in master
    assert "scaling_route" in master
    assert "Route choice deferred to M4B" in m4a_subplan
    assert "Only `PASS_P53_M4D_SCALING_ROUTE_ADMISSION`" in m4d_subplan


def test_p53_m0_hard_rules_forbid_repeating_p52_logical_error() -> None:
    rules = _manifest()["hard_rules"]
    m0_subplan = M0_SUBPLAN_PATH.read_text(encoding="utf-8")

    assert rules["contract_only_cannot_pass_implementation"] is True
    assert rules["lower_rung_dense_equivalent_cannot_unlock_rank_or_scaling"] is True
    assert rules["rank_selection_requires_m4d_scaling_route_admission"] is True
    assert rules["d18_requires_m4d_scaling_route_admission"] is True
    assert rules["d50_d100_requires_m4d_scaling_route_admission"] is True
    assert rules["m4a_derivation_required_before_m4b_implementation"] is True
    assert rules["m4b_implementation_required_before_m4c_tieout"] is True
    assert rules["m4c_tieout_required_before_m4d_admission"] is True
    assert "lower-rung streaming dense-equivalent evidence is promoted" in m0_subplan


def test_p53_m0_phase_admission_blocks_rank_and_scaling_without_m4_pass() -> None:
    manifest = _manifest()
    lower_rung_tokens = {
        "PASS_P53_M0_PLANNING_FAILURE_LOCK",
        "PASS_P53_M1_ROUTE_DESIGN_MATH",
        "PASS_P53_M2_ROUTE_IMPLEMENTATION",
        "PASS_P53_M3_LOWER_RUNG_DENSE_TIEOUT",
    }

    assert _can_admit_phase(
        phase="P53-M4A",
        emitted_tokens=lower_rung_tokens,
        manifest=manifest,
    )
    assert not _can_admit_phase(
        phase="P53-M4B",
        emitted_tokens=lower_rung_tokens,
        manifest=manifest,
    )
    assert not _can_admit_phase(
        phase="P53-M5",
        emitted_tokens=lower_rung_tokens,
        manifest=manifest,
    )
    assert not _can_admit_phase(
        phase="P53-M6",
        emitted_tokens=lower_rung_tokens,
        manifest=manifest,
    )
    assert not _can_admit_phase(
        phase="P53-M7",
        emitted_tokens=lower_rung_tokens,
        manifest=manifest,
    )
    assert not _can_admit_phase(
        phase="P53-M8",
        emitted_tokens=lower_rung_tokens,
        manifest=manifest,
    )

    scaling_route_tokens = lower_rung_tokens | {
        "PASS_P53_M4A_SCALING_ROUTE_DERIVATION",
        "PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION",
        "PASS_P53_M4C_SCALING_ROUTE_TIEOUT",
        "PASS_P53_M4D_SCALING_ROUTE_ADMISSION",
    }
    assert _can_admit_phase(
        phase="P53-M5",
        emitted_tokens=scaling_route_tokens,
        manifest=manifest,
    )
    assert not _can_admit_phase(
        phase="P53-M8",
        emitted_tokens=scaling_route_tokens,
        manifest=manifest,
    )

    all_substantive_tokens = scaling_route_tokens | {
        "PASS_P53_M5_RANK_SELECTION_INTEGRATION",
        "PASS_P53_M6_SPATIAL_SIR_D18",
        "PASS_P53_M7_SPATIAL_SIR_D50_D100",
    }
    assert _can_admit_phase(
        phase="P53-M8",
        emitted_tokens=all_substantive_tokens,
        manifest=manifest,
    )


def test_p53_m0_review_loop_converged_and_runbook_is_visible() -> None:
    review = REVIEW_LEDGER_PATH.read_text(encoding="utf-8")
    runbook = RUNBOOK_PATH.read_text(encoding="utf-8")
    manifest = _manifest()

    assert "Iteration 1" in review
    assert "VERDICT: REVISE" in review
    assert "Iteration 2" in review
    assert "VERDICT: AGREE" in review
    assert "Codex in the current conversation is the supervisor and executor" in runbook
    assert "Claude is a read-only reviewer only" in runbook
    assert "Do not use:" in runbook
    assert manifest["hard_rules"]["claude_read_only"] is True
    assert manifest["hard_rules"]["detached_execution_allowed"] is False


def test_p53_m0_phase_tokens_are_complete() -> None:
    tokens = _manifest()["required_gate_tokens"]

    expected = {f"P53-M{index}" for index in range(4)}
    expected |= {"P53-M4A", "P53-M4B", "P53-M4C", "P53-M4D"}
    expected |= {"P53-M5", "P53-M6", "P53-M7", "P53-M8"}
    assert set(tokens) == expected
    for phase, pair in tokens.items():
        assert len(pair) == 2, phase
        assert pair[0].startswith(f"PASS_{phase.replace('-', '_')}")
        assert pair[1].startswith(f"BLOCK_{phase.replace('-', '_')}")
