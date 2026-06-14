from __future__ import annotations

from pathlib import Path


P30_PATH = Path(
    "docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex"
)
M1_SUBPLAN_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m1-route-design-math-subplan-2026-06-10.md"
)
MASTER_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-factorized-transition-repair-master-program-2026-06-10.md"
)


def _p30() -> str:
    return P30_PATH.read_text(encoding="utf-8")


def _compact(text: str) -> str:
    return " ".join(text.split())


def test_p53_p30_defines_route_classes_and_gate() -> None:
    text = _p30()
    compact = _compact(text)
    master = MASTER_PATH.read_text(encoding="utf-8")

    assert "\\label{sec:p53-spatial-sir-route-class-repair}" in text
    assert "\\label{eq:p53-route-classes}" in text
    assert "\\mathsf C_{\\rm low}" in text
    assert "\\mathsf C_{\\rm scale}" in text
    assert "lower-rung dense-equivalent streaming route" in text
    assert "local-neighborhood or TT--MPO scaling route" in text
    assert "\\label{eq:p53-scaling-route-gate}" in text
    assert "if only }\\mathsf C_{\\rm low}\\text{ has passed" in compact
    assert "PASS_P53_M4D_SCALING_ROUTE_ADMISSION" in master


def test_p53_p30_documents_streaming_dense_equivalent_route_without_scaling_overclaim() -> None:
    text = _p30()
    compact = _compact(text)

    assert "\\label{eq:p53-streaming-predictive}" in text
    assert "\\label{eq:p53-low-route-identity}" in text
    assert "\\label{eq:p53-low-route-memory}" in text
    assert "B_c,B_p" in text
    assert "stable log-sum-exp reduction" in text
    assert "not a scalability proof" in text
    assert "dense-equivalent pair semantics" in compact


def test_p53_p30_documents_scaling_route_options_and_metadata() -> None:
    text = _p30()
    compact = _compact(text)

    assert "\\label{eq:p53-local-transition-factor}" in text
    assert "\\label{eq:p53-mpo-transition-factor}" in text
    assert "\\label{eq:p53-scale-route-identity}" in text
    assert "\\mathcal N_m" in text
    assert "MPO cores" in text
    assert "conservative" in text
    assert "route-width bound \\(R_{\\rm eff}\\)" in text
    assert "lower-rung tie-out, replay, and metadata checks" in compact


def test_p53_m1_subplan_forbids_deferred_route_choice_and_p30_drift() -> None:
    subplan = M1_SUBPLAN_PATH.read_text(encoding="utf-8")

    assert "Route choice deferred to implementation" in subplan
    assert "streaming dense-equivalent route promoted to high-dimensional scalability" in subplan
    assert "P30 not updated or amended" in subplan
    assert "State exact formulas" in subplan
