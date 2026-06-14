from __future__ import annotations

from pathlib import Path


P30_PATH = Path(
    "docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex"
)
SUBPLAN_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-m1-p30-latex-rank-calibration-subplan-2026-06-10.md"
)
RUNBOOK_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-visible-gated-execution-runbook-2026-06-10.md"
)


def _p30() -> str:
    return P30_PATH.read_text(encoding="utf-8")


def _compact(text: str) -> str:
    return " ".join(text.split())


def test_p52_p30_documents_dense_all_pairs_route_blocker() -> None:
    text = _p30()

    assert "\\label{sec:p52-rank-calibrated-spatial-sir-route}" in text
    assert "\\label{eq:p52-dense-grid-count}" in text
    assert "\\label{eq:p52-dense-pair-count}" in text
    assert "N_{\\rm pairs}=N_{\\rm dense}^2=n^{2d}" in text
    assert "N_{\\rm pairs}=3^{36}=150094635296999121" in text
    assert "route blocker, not a reason to abandon fixed branches" in text


def test_p52_p30_contains_memory_rank_ceiling_model() -> None:
    text = _p30()
    compact = _compact(text)

    assert "\\label{eq:p52-state-memory}" in text
    assert "M_{\\rm state}\\approx 8\\,d\\,n\\,r^2" in text
    assert "\\label{eq:p52-step-memory}" in text
    assert "M_{\\rm step}\\approx" in text
    assert "8\\,d\\,n\\,(R_{\\rm eff}r)^2\\,\\omega" in text
    assert "\\label{eq:p52-rank-ceiling}" in text
    assert "M_{\\rm step}^{\\rm cap}" in text
    assert "R_{\\rm eff}\\) is unknown" in text
    assert "preflight blocker rather than an invitation to launch" in compact


def test_p52_p30_defines_fixed_rank_branch_as_target() -> None:
    text = _p30()

    assert "\\label{eq:p52-fixed-rank-branch}" in text
    assert "r,\\," in text
    assert "b_{1:d},\\," in text
    assert "c_{1:d},\\," in text
    assert "s_{1:d},\\," in text
    assert "\\Pi_{\\rm contract}" in text
    assert "\\Pi_{\\rm trunc}" in text
    assert "These choices are part of the scalar being differentiated" in text
    assert "cannot change during an HMC" in text


def test_p52_p30_keeps_ukf_scout_not_truth() -> None:
    text = _p30()

    for label in [
        "eq:p52-ukf-pred-mean",
        "eq:p52-ukf-pred-cov",
        "eq:p52-ukf-obs-mean",
        "eq:p52-ukf-obs-cov",
        "eq:p52-ukf-cross-cov",
        "eq:p52-ukf-update",
    ]:
        assert f"\\label{{{label}}}" in text
    assert "not a correctness oracle" in text
    assert "not an exact likelihood" in text
    assert "not evidence of HMC readiness" in text


def test_p52_p30_contains_rank_protocol_and_stop_rules() -> None:
    text = _p30()
    compact = _compact(text)
    subplan = SUBPLAN_PATH.read_text(encoding="utf-8")

    assert "\\label{eq:p52-rank-protocol}" in text
    assert "\\mathcal R_0=\\{2,4,8,16,32\\}" in text
    assert "rank-budget blocker" in compact
    assert "Freeze }\\mathcal B" in text
    assert "The ladder cannot pass self-convergence at its largest feasible rank" in text
    assert "rank, coordinate, factorization, or reference-strategy blocker" in text
    assert "`PASS_P52_M1_P30_LATEX_RANK_CALIBRATION`" in subplan


def test_p52_p30_records_dimension_policy_without_d100_overclaim() -> None:
    text = _p30()
    compact = _compact(text)
    runbook = RUNBOOK_PATH.read_text(encoding="utf-8")

    assert "\\label{eq:p52-dimension-policy}" in text
    assert "18 & 9" in text
    assert "50 & 25" in text
    assert "100 & 50" in text
    assert "d=50" in text
    assert "first reasonable full filtering stress target" in text
    assert (
        "Dimension \\(d=100\\) may become a bounded filtering stress row only "
        "after the lower gates pass"
    ) in compact
    assert "d=100 filtering-correctness claim without reviewed reference strategy" in runbook
