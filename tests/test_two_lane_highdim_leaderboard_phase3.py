from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("benchmark_two_lane_highdim_leaderboard", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load highdim leaderboard module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_phase3_zhao_cui_lgssm_exact_oracle_adapter_executes_without_source_faithful_tt_claim() -> None:
    module = _load_module()
    row = module._zhao_cui_lgssm_exact_oracle_adapter()

    assert row["comparison_status"] == "executed_value_score"
    assert row["numeric_execution_status"] == "executed_lgssm_exact_oracle_adapter_value_score"
    assert row["target_contract_status"] == "target_compatible_user_amended_lgssm_exact_oracle_adapter"
    assert row["absolute_value_gap_to_kalman"] < 1e-7
    assert isinstance(row["score"], list)
    assert len(row["score"]) == 5
    assert row["score_coordinate_system"] == "physical_theta"
    assert "tf_covariance_differentiated_kalman_reference" in row["score_derivative_provenance"]
    joined = " ".join(row["reason_codes"] + row["nonclaims"] + [row["score_derivative_provenance"]]).lower()
    assert "als" in joined
    assert "historical als training used" in joined
    assert "source-faithful" not in joined
    assert "paper-scale zhao-cui tt-cross" in joined
