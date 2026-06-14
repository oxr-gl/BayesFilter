from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim


def _stress_manifest(
    *,
    decision_status: highdim.StressRunStatus = highdim.StressRunStatus.PASS_DIAGNOSTIC_ONLY,
    exact_reference_error: float = 0.0,
    wall_time_seconds: float = 0.01,
    resource_budgets: dict[str, int] | None = None,
) -> highdim.StressRunManifest:
    return highdim.StressRunManifest(
        {
            "git_commit": "test",
            "command": "pytest -q tests/highdim/test_p30_stress_ladders.py",
            "environment": "pytest CPU smoke",
            "cpu_gpu_status": "CPU_ONLY_CUDA_VISIBLE_DEVICES=-1_expected",
            "random_seeds": ("m5-stress-seed",),
            "dtype": "tf.float64",
            "model_equations": ("eq:p27-bf1", "eq:p27-bf2", "eq:p27-bf3", "eq:p27-bf4"),
            "dimension_rank_degree_horizon_grid": {
                "dimension": 2,
                "horizon": 3,
                "rank": 1,
                "basis": 4,
            },
            "resource_budgets": resource_budgets
            if resource_budgets is not None
            else {
                "row_budget": 128,
                "column_budget": 32,
                "dense_matrix_byte_budget": 32768,
                "normal_matrix_byte_budget": 8192,
                "retained_storage_byte_budget": 1_000_000,
            },
            "expected_memory_model": "dense_design_bytes=n_rows*n_cols*8",
            "measured_peak_memory": "not_available_in_pytest_smoke",
            "wall_time_seconds": wall_time_seconds,
            "exact_reference_error": exact_reference_error,
            "fit_residual": None,
            "holdout_residual": None,
            "normalizer_diagnostics": None,
            "branch_hash": "m5-branch",
            "deterministic_replay_status": "PASS",
            "decision_status": decision_status.value,
            "termination_reason": "m5_first_gate_schema_smoke",
            "stop_condition_triggered": "none",
            "what_is_not_concluded": (
                "correctness",
                "scalability",
                "GPU readiness",
                "HMC readiness",
                "DSGE readiness",
                "paper reproduction",
            ),
        }
    )


def _non_claims() -> tuple[str, ...]:
    return (
        "no correctness claim",
        "no scalability claim",
        "no GPU readiness claim",
        "no HMC readiness claim",
        "no DSGE readiness claim",
        "no paper reproduction claim",
    )


def _row_manifest(**overrides: object) -> highdim.P30StressLadderRowManifest:
    values = {
        "phase_id": "P37-M5",
        "stress_manifest": _stress_manifest(),
        "ladder_axis": "dimension",
        "varied_axes": ("dimension",),
        "fixed_axes": {"horizon": 3, "rank": 1, "basis": 4},
        "lower_phase_guardrail_status": "PASS_M0_TO_M4",
        "evidence_interpretation": "DIAGNOSTIC_ONLY",
        "promotion_decision": "RECORD_DIAGNOSTIC_ROW",
        "non_claims": _non_claims(),
    }
    values.update(overrides)
    return highdim.P30StressLadderRowManifest(**values)


def test_p30_stress_ladder_row_accepts_one_axis_diagnostic_manifest():
    row = _row_manifest()

    assert row.phase_id == "P37-M5"
    assert row.ladder_axis == "dimension"
    assert row.varied_axes == ("dimension",)
    assert row.stress_manifest.decision_status is highdim.StressRunStatus.PASS_DIAGNOSTIC_ONLY
    assert row.promotion_decision == "RECORD_DIAGNOSTIC_ROW"
    assert "horizon" in row.fixed_axes
    assert "dimension" not in row.fixed_axes


def test_p30_stress_ladder_row_accepts_exact_reference_only_with_exact_status():
    row = _row_manifest(
        stress_manifest=_stress_manifest(
            decision_status=highdim.StressRunStatus.PASS_EXACT_REFERENCE,
            exact_reference_error=1e-14,
        ),
        evidence_interpretation="EXACT_REFERENCE",
        promotion_decision="STRESS_SCHEMA_ONLY",
    )

    assert row.evidence_interpretation == "EXACT_REFERENCE"
    assert row.stress_manifest.decision_status is highdim.StressRunStatus.PASS_EXACT_REFERENCE


def test_p30_stress_ladder_rejects_multiple_axis_variation():
    with pytest.raises(ValueError, match="only one active ladder axis"):
        _row_manifest(
            ladder_axis="dimension",
            varied_axes=("dimension", "horizon"),
            fixed_axes={"rank": 1, "basis": 4},
        )

    with pytest.raises(ValueError, match="varied_axes must exactly match ladder_axis"):
        _row_manifest(
            ladder_axis="dimension",
            varied_axes=("horizon",),
            fixed_axes={"dimension": 2, "rank": 1, "basis": 4},
        )


def test_p30_stress_ladder_rejects_missing_fixed_axis_and_varied_axis_leak():
    with pytest.raises(ValueError, match="fixed_axes missing basis"):
        _row_manifest(fixed_axes={"horizon": 3, "rank": 1})

    with pytest.raises(ValueError, match="must not include varied_axes"):
        _row_manifest(fixed_axes={"dimension": 2, "horizon": 3, "rank": 1, "basis": 4})


def test_p30_stress_ladder_blocks_when_lower_phase_regresses():
    blocked = _row_manifest(
        stress_manifest=_stress_manifest(
            decision_status=highdim.StressRunStatus.BLOCKED_BY_PHASE_REGRESSION,
        ),
        lower_phase_guardrail_status="FAIL_M0_TO_M4",
    )
    assert blocked.stress_manifest.decision_status is highdim.StressRunStatus.BLOCKED_BY_PHASE_REGRESSION

    with pytest.raises(ValueError, match="lower phase regression must block"):
        _row_manifest(lower_phase_guardrail_status="FAIL_M0_TO_M4")


def test_p30_stress_ladder_rejects_regression_block_status_with_passing_guardrail():
    with pytest.raises(ValueError, match="passing lower phase guardrail"):
        _row_manifest(
            stress_manifest=_stress_manifest(
                decision_status=highdim.StressRunStatus.BLOCKED_BY_PHASE_REGRESSION,
            ),
            lower_phase_guardrail_status="PASS_M0_TO_M4",
        )


def test_p30_stress_ladder_requires_exact_interpretation_for_exact_status():
    with pytest.raises(ValueError, match="PASS_EXACT_REFERENCE status requires EXACT_REFERENCE"):
        _row_manifest(
            stress_manifest=_stress_manifest(
                decision_status=highdim.StressRunStatus.PASS_EXACT_REFERENCE,
                exact_reference_error=1e-14,
            ),
            evidence_interpretation="DIAGNOSTIC_ONLY",
        )


def test_p30_stress_ladder_rejects_first_gate_promotion_and_missing_nonclaim():
    with pytest.raises(ValueError, match="cannot promote correctness or scalability"):
        _row_manifest(promotion_decision="PROMOTE_SCALABILITY")

    with pytest.raises(ValueError, match="non_claims must include GPU"):
        _row_manifest(non_claims=("no correctness claim", "no scalability claim"))


def test_p30_stress_ladder_rejects_nonfinite_resource_or_exact_reference_fields():
    bad_budget = {
        "row_budget": 128,
        "column_budget": 32,
        "dense_matrix_byte_budget": -1,
        "normal_matrix_byte_budget": 8192,
        "retained_storage_byte_budget": 1_000_000,
    }
    with pytest.raises(ValueError, match="resource_budgets dense_matrix_byte_budget"):
        _row_manifest(stress_manifest=_stress_manifest(resource_budgets=bad_budget))

    with pytest.raises(ValueError, match="exact_reference_error"):
        _row_manifest(
            stress_manifest=_stress_manifest(
                decision_status=highdim.StressRunStatus.PASS_EXACT_REFERENCE,
                exact_reference_error=float("nan"),
            ),
            evidence_interpretation="EXACT_REFERENCE",
        )


def test_p30_stress_ladder_public_symbol_remains_subpackage_scoped():
    assert hasattr(highdim, "P30StressLadderRowManifest")
    assert "P30StressLadderRowManifest" in highdim.__all__
