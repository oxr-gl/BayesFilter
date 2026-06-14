from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim


def test_p59_9c_author_sir_selects_full_sol_from_source() -> None:
    result = highdim.p59_author_sir_route_decision()
    payload = result.manifest_payload()
    manifest = payload["manifest"]

    assert result.status == highdim.P59_9C_PASS_STATUS
    assert result.route_decision == highdim.P59_9C_FULL_ROUTE_SELECTED
    assert result.preconditioned_route_required is False
    assert (
        result.preconditioned_route_status
        == highdim.P59_9C_NOT_REQUIRED_PRECONDITIONED_STATUS
    )
    assert result.unlocks_step_spec_assembly is True
    assert manifest["source_selected_matlab_constructor"] == "full_sol"
    assert manifest["source_evidence"]["mainscript_selects_full_sol"] is True
    assert manifest["source_evidence"]["mainscript_selects_pre_sol"] is False
    assert manifest["source_evidence"]["full_sol_source_boundary_verified"] is True
    assert manifest["source_evidence"]["pre_sol_boundary_verified"] is True
    assert manifest["source_evidence"]["precond_boundary_verified"] is True


def test_p59_9c_manifest_blocks_9b_9d_without_promoting_proxies() -> None:
    result = highdim.p59_author_sir_route_decision()
    manifest = result.manifest

    assert manifest["pipeline_phase"] == "P59-9c"
    assert manifest["artifact_role"] == "source_route_decision_gate"
    assert manifest["unlocks_after_consumed_by"] == ("P59-9b", "P59-9d")
    assert "P59-9b and P59-9d must block" in manifest["fail_closed_rule"]
    assert "no Phase-9 validation launch" in manifest["nonclaims"]
    assert "no preconditioned route claim for author SIR" in manifest["nonclaims"]
    assert "no UKF route substitute" in manifest["nonclaims"]
    assert any("full_sol.m" in anchor for anchor in result.source_anchors)
    assert any("pre_sol.m" in anchor for anchor in result.source_anchors)
    assert any("precond.m" in anchor for anchor in result.source_anchors)


def test_p59_9c_blocks_when_source_files_are_missing(tmp_path) -> None:
    result = highdim.p59_author_sir_route_decision(source_root=tmp_path / "missing")

    assert result.status == highdim.P59_9C_BLOCK_STATUS
    assert result.route_decision == highdim.P59_9C_ROUTE_DECISION_BLOCKED
    assert result.unlocks_step_spec_assembly is False
    assert "missing_source_file:mainscript" in result.blockers
    assert "author_sir_mainscript_does_not_select_full_sol" in result.blockers
    assert result.manifest["fail_closed_rule"] == "P59-9b and P59-9d must not proceed."


def test_p59_9c_blocks_contradictory_route_evidence(tmp_path) -> None:
    root = tmp_path / "source"
    (root / "eg3_sir").mkdir(parents=True)
    (root / "models" / "tensordot").mkdir(parents=True)
    (root / "eg3_sir" / "mainscript.m").write_text(
        "mySol_unbounded = full_sol(myModel, sqr, poly2, opt, lowopt, N, 4);\n"
        "mySol_pre = pre_sol(myModel, poly2, opt, lowopt, N, 4, precond);\n"
        "mySol_unbounded = solve(mySol_unbounded);\n",
        encoding="utf-8",
    )
    (root / "models" / "full_sol.m").write_text(
        "classdef full_sol < Y_sol\n"
        "sol.samples = zeros(model.d+2*model.m, N, model.T+1);\n"
        "[r, ~] = eval_irt(sol.SIRTs{t}, z);\n"
        "w = exp(-fun_post(r))./eval_pdf(sol.SIRTs{t}, r);\n",
        encoding="utf-8",
    )
    (root / "models" / "pre_sol.m").write_text(
        "classdef pre_sol < full_sol\n"
        "function sol = pre_sol(model, poly, opt, lowopt, N, epd, precond)\n"
        "sol.precond = precond;\n",
        encoding="utf-8",
    )
    (root / "models" / "tensordot" / "precond.m").write_text(
        "function [C, Sigmak] = precond(Sigma1,Sigma2)\n"
        "Sigma3 = Sigma1\\Sigma2full;\n"
        "Sigmak = 1;\n",
        encoding="utf-8",
    )

    result = highdim.p59_author_sir_route_decision(source_root=root)

    assert result.status == highdim.P59_9C_BLOCK_STATUS
    assert "author_sir_mainscript_also_mentions_pre_sol" in result.blockers


def test_p59_9c_rejects_incoherent_result_payloads() -> None:
    with pytest.raises(ValueError, match="pass cannot carry blockers"):
        highdim.P59AuthorSIRRouteDecisionResult(
            status=highdim.P59_9C_PASS_STATUS,
            blockers=("hidden_blocker",),
            route_decision=highdim.P59_9C_FULL_ROUTE_SELECTED,
            preconditioned_route_required=False,
            preconditioned_route_status=highdim.P59_9C_NOT_REQUIRED_PRECONDITIONED_STATUS,
            source_anchors=("source.m:1",),
            manifest={},
        )

    with pytest.raises(ValueError, match="requires P57-M8 pass"):
        highdim.P59AuthorSIRRouteDecisionResult(
            status=highdim.P59_9C_PASS_STATUS,
            blockers=(),
            route_decision=highdim.P59_9C_PRECONDITIONED_ROUTE_REQUIRED,
            preconditioned_route_required=True,
            preconditioned_route_status="missing",
            source_anchors=("source.m:1",),
            manifest={},
        )
