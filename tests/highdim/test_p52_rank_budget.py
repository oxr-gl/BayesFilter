from __future__ import annotations

import json
from pathlib import Path

import pytest

from bayesfilter import highdim
from bayesfilter.highdim.rank_budget import P52_GIB


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-m2-memory-rank-ceiling-manifest-2026-06-10.json"
)
MASTER_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-rank-calibrated-spatial-sir-master-program-2026-06-10.md"
)
P30_PATH = Path(
    "docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex"
)


def test_p52_rank_budget_formulas_match_p30_memory_model() -> None:
    config = highdim.RankBudgetConfig(
        dimension=18,
        basis_size=3,
        effective_transition_rank_multiplier=16,
        workspace_multiplier=8,
        step_cap_bytes=8 * P52_GIB,
    )

    assert highdim.state_memory_bytes(config, 4) == 8 * 18 * 3 * 4**2
    assert highdim.step_memory_bytes(config, 4) == 8 * 18 * 3 * (16 * 4) ** 2 * 8
    expected = int(
        (
            (8 * P52_GIB)
            / (8 * 18 * 3 * 8 * 16**2)
        )
        ** 0.5
    )
    assert highdim.rank_ceiling(config) == expected

    p30 = P30_PATH.read_text(encoding="utf-8")
    assert "M_{\\rm state}\\approx 8\\,d\\,n\\,r^2" in p30
    assert "M_{\\rm step}\\approx" in p30
    assert "\\label{eq:p52-rank-ceiling}" in p30


def test_p52_rank_budget_monotonicity_for_dimension_reff_and_workspace() -> None:
    base = highdim.RankBudgetConfig(dimension=18, basis_size=3)
    larger_d = highdim.RankBudgetConfig(dimension=50, basis_size=3)
    larger_reff = highdim.RankBudgetConfig(
        dimension=18,
        basis_size=3,
        effective_transition_rank_multiplier=32,
    )
    larger_workspace = highdim.RankBudgetConfig(
        dimension=18,
        basis_size=3,
        workspace_multiplier=16,
    )

    assert highdim.rank_ceiling(larger_d) <= highdim.rank_ceiling(base)
    assert highdim.rank_ceiling(larger_reff) <= highdim.rank_ceiling(base)
    assert highdim.rank_ceiling(larger_workspace) <= highdim.rank_ceiling(base)


def test_p52_rank_budget_requires_explicit_reff_source_and_nonpromoted_claim() -> None:
    with pytest.raises(ValueError, match="reff_source"):
        highdim.RankBudgetConfig(dimension=18, basis_size=3, reff_source="unknown")

    with pytest.raises(ValueError, match="stronger claims"):
        highdim.RankBudgetConfig(
            dimension=18,
            basis_size=3,
            claim_class="filtering correctness",
        )


def test_p52_rank_budget_truncates_candidates_and_blocks_empty_budget() -> None:
    passing = highdim.evaluate_rank_budget(
        highdim.RankBudgetConfig(
            dimension=18,
            basis_size=3,
            effective_transition_rank_multiplier=16,
            workspace_multiplier=8,
            candidate_ranks=(2, 4, 8, 16, 32),
        )
    )
    assert passing.status == "PASS_P52_MEMORY_PREFLIGHT"
    assert passing.feasible_ranks
    assert all(rank <= passing.r_max for rank in passing.feasible_ranks)
    assert all(
        row.within_step_cap == (row.rank <= passing.r_max)
        for row in passing.forecasts
    )

    blocked = highdim.evaluate_rank_budget(
        highdim.RankBudgetConfig(
            dimension=100,
            basis_size=3,
            effective_transition_rank_multiplier=4096,
            workspace_multiplier=32,
            candidate_ranks=(2, 4),
        )
    )
    assert blocked.status == "BLOCK_P52_RANK_BUDGET_EMPTY"
    assert blocked.feasible_ranks == ()
    assert blocked.blocker == "no candidate rank is below the hard memory ceiling"


def test_p52_spatial_sir_rank_budget_manifest_preserves_claim_boundaries() -> None:
    manifest = highdim.p52_spatial_sir_rank_budget_manifest()
    rows = {int(row["dimension"]): row for row in manifest["rows"]}
    master = MASTER_PATH.read_text(encoding="utf-8")

    assert manifest["schema_version"] == "p52.rank_budget_preflight.v1"
    assert manifest["status"] == "PASS_P52_M2_MEMORY_RANK_CEILING"
    assert manifest["claim_class"] == highdim.P52_MEMORY_PREFLIGHT_CLAIM
    assert set(rows) == {18, 50, 100}
    assert rows[18]["r_max"] >= rows[50]["r_max"] >= rows[100]["r_max"]
    assert rows[100]["claim_class"] == highdim.P52_MEMORY_PREFLIGHT_CLAIM
    assert "no filtering correctness" in manifest["nonclaims"]
    assert "no HMC readiness" in manifest["nonclaims"]
    assert "no d=100 filtering correctness" in manifest["nonclaims"]
    assert "memory feasibility" in master


def test_p52_m2_persisted_manifest_matches_protocol() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected = highdim.p52_spatial_sir_rank_budget_manifest()

    assert manifest["schema_version"] == expected["schema_version"]
    assert manifest["status"] == "PASS_P52_M2_MEMORY_RANK_CEILING"
    assert manifest["claim_class"] == highdim.P52_MEMORY_PREFLIGHT_CLAIM
    assert manifest["dimensions"] == [18, 50, 100]
    assert manifest["rows"] == [
        {
            **dict(row),
            "candidate_ranks": list(row["candidate_ranks"]),
            "feasible_ranks": list(row["feasible_ranks"]),
            "nonclaims": list(row["nonclaims"]),
        }
        for row in expected["rows"]
    ]
    assert "no production spatial SIR readiness" in manifest["nonclaims"]

