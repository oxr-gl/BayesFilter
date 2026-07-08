from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "docs" / "benchmarks" / "diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py"
ROUTE_LABEL = "contract_e_cholesky_fixed_ridge_manual_lgssm_tiny"
STAGE_A_ROUTE_LABEL = "contract_e_cholesky_fixed_ridge_manual_lgssm_t10"
MINIMAL_STAGE_A_ROUTE_LABEL = "contract_e_cholesky_minimal_ridge_replayed_manual_lgssm_t10"
SCORE_ROUTE = "manual_likelihood_reverse_scan_no_autodiff"
FULL_BLOCKER = "PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION"


def _source() -> str:
    return TARGET.read_text(encoding="utf-8")


def _function_source(name: str) -> str:
    source = _source()
    tree = ast.parse(source)
    lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            if node.end_lineno is None:
                raise AssertionError(f"missing end line for {name}")
            return "\n".join(lines[node.lineno - 1 : node.end_lineno])
    raise AssertionError(f"function not found: {name}")


def test_phase3_material_tiny_entrypoint_runs_manual_route(tmp_path: Path) -> None:
    output = tmp_path / "material_tiny.json"
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    command = [
        sys.executable,
        str(TARGET),
        "--device-scope",
        "cpu",
        "--num-particles",
        "4",
        "--seed-count",
        "1",
        "--time-steps",
        "2",
        "--state-dims",
        "1",
        "--settings",
        "0.55:2",
        "--contract-e-reset-factorization",
        "cholesky-ridge",
        "--chol-ridge-abs",
        "0.75",
        "--chol-ridge-rel",
        "0",
        "--chol-ridge-max-attempts",
        "1",
        "--gate-mode",
        "material",
        "--fd-steps",
        "1e-5,1e-5,1e-5",
        "--no-xla",
        "--output",
        str(output),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert '"status": "passed"' in completed.stdout
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["gate"]["status"] == "passed"
    assert payload["manifest"]["score_route"] == SCORE_ROUTE
    assert payload["manifest"]["route_label"] == ROUTE_LABEL
    assert payload["manifest"]["full_phase3_material_status"] == FULL_BLOCKER
    assert payload["device"]["device_scope"] == "cpu"
    assert payload["device"]["cuda_visible_devices"] == "-1"
    assert payload["device"]["logical_gpus"] == []
    assert payload["device"]["tf32_execution_enabled"] is False
    material = payload["material_tiny_manual_route"]
    assert payload["material_manual_route"]["fixtures"][0] == material
    assert material["score_route"] == SCORE_ROUTE
    assert material["route_label"] == ROUTE_LABEL
    assert material["diagnostics"]["material_entrypoint_executed"] is True
    assert material["diagnostics"]["outer_gradient_tape_used"] is False
    assert material["same_scalar_fd"]["status"] == "pass"
    for row in material["same_scalar_fd"]["parameters"]:
        assert row["pass"] is True
        assert row["branch_replay_ok"] is True
        assert row["abs_error"] <= material["same_scalar_fd"]["atol"]


def test_phase3_material_stage_a_entrypoint_runs_general_manual_route(tmp_path: Path) -> None:
    output = tmp_path / "material_stage_a.json"
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    command = [
        sys.executable,
        str(TARGET),
        "--device-scope",
        "cpu",
        "--num-particles",
        "16",
        "--seed-count",
        "3",
        "--time-steps",
        "10",
        "--state-dims",
        "1",
        "--settings",
        "0.55:2",
        "--contract-e-reset-factorization",
        "cholesky-ridge",
        "--chol-ridge-abs",
        "0.75",
        "--chol-ridge-rel",
        "0",
        "--chol-ridge-max-attempts",
        "1",
        "--gate-mode",
        "material",
        "--fd-steps",
        "1e-5,1e-5,1e-5",
        "--no-xla",
        "--output",
        str(output),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert '"status": "passed"' in completed.stdout
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["gate"]["status"] == "passed"
    assert payload["manifest"]["material_scope"] == "stage_a"
    assert payload["manifest"]["score_route"] == SCORE_ROUTE
    assert payload["manifest"]["route_label"] == STAGE_A_ROUTE_LABEL
    material = payload["material_manual_route"]["fixtures"][0]
    assert material["state_dim"] == 1
    assert material["material_scope"] == "stage_a"
    assert material["score_route"] == SCORE_ROUTE
    assert material["route_label"] == STAGE_A_ROUTE_LABEL
    assert material["diagnostics"]["outer_gradient_tape_used"] is False
    assert material["same_scalar_fd"]["status"] == "pass"
    for row in material["same_scalar_fd"]["parameters"]:
        assert row["pass"] is True
        assert row["branch_replay_ok"] is True


def test_phase3_material_stage_a_accepts_minimal_ridge_replayed_chart(tmp_path: Path) -> None:
    output = tmp_path / "material_stage_a_minimal_ridge.json"
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    command = [
        sys.executable,
        str(TARGET),
        "--device-scope",
        "cpu",
        "--num-particles",
        "16",
        "--seed-count",
        "3",
        "--time-steps",
        "10",
        "--state-dims",
        "1",
        "--settings",
        "0.55:2",
        "--contract-e-reset-factorization",
        "cholesky-ridge",
        "--chol-ridge-abs",
        "1e-10",
        "--chol-ridge-rel",
        "1e-8",
        "--chol-ridge-escalation",
        "10",
        "--chol-ridge-max-attempts",
        "12",
        "--gate-mode",
        "material",
        "--fd-steps",
        "1e-5,1e-5,1e-5",
        "--no-xla",
        "--output",
        str(output),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert '"status": "passed"' in completed.stdout
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["gate"]["status"] == "passed"
    assert payload["manifest"]["ridge_policy"] == "minimal_stabilizing_replayed_fixed_chart"
    assert payload["manifest"]["route_label"] == MINIMAL_STAGE_A_ROUTE_LABEL
    material = payload["material_manual_route"]["fixtures"][0]
    assert material["ridge_policy"] == "minimal_stabilizing_replayed_fixed_chart"
    assert material["route_label"] == MINIMAL_STAGE_A_ROUTE_LABEL
    assert material["diagnostics"]["contract_e_reset_factorization"] == "cholesky-ridge-replayed-fixed-chart"
    assert material["diagnostics"]["realized_ridge_max"] < 0.75
    assert material["diagnostics"]["all_ridge_charts_ok"] is True
    assert material["same_scalar_fd"]["status"] == "pass"
    for row in material["same_scalar_fd"]["parameters"]:
        assert row["pass"] is True
        assert row["branch_replay_ok"] is True
    branch = material["branch_record"]
    assert branch["replayed_ridge_by_batch"]
    assert branch["reselected_ridge_by_batch"]
    assert branch["replayed_ridge_by_batch"] == branch["reselected_ridge_by_batch"]


def test_phase3_material_route_static_audit_has_no_outer_tape_or_branchy_reset() -> None:
    material_functions = [
        "_configure_material_precision",
        "_material_tiny_fixture",
        "_material_harness_fixture",
        "_material_fixture_for_state_dim",
        "_material_transport_chart",
        "_material_transport_matrix_value",
        "_material_select_ridge",
        "_material_step_ridge_selection",
        "_material_fixed_ridge_step_forward",
        "_material_base_charts",
        "_material_forward_records",
        "_material_fixed_ridge_step_vjp",
        "_material_manual_value_and_score",
        "_material_branch_record",
        "_material_branch_records_match",
        "_material_fixture_gate",
        "_material_overall_gate",
        "_run_material_manual_fixture",
        "_run_material_tiny_manual_route",
        "_run_material_manual_route",
    ]
    forbidden = [
        "tf.GradientTape",
        "GradientTape",
        ".gradient(",
        ".jacobian(",
        "batch_jacobian",
        "ForwardAccumulator",
        "tf.gradients",
        "tf.compat.v1.gradients",
        'transport_ad_mode="full"',
        "transport_ad_mode='full'",
    ]
    for function_name in material_functions:
        source = _function_source(function_name)
        for token in forbidden:
            assert token not in source, f"{token} in {function_name}"


def test_phase3_material_dispatch_bypasses_taped_wrapper_and_full_gate_blocks_large_scope() -> None:
    parse_args = _function_source("_parse_args")
    main_source = _function_source("main")
    taped_wrapper = _function_source("_make_compiled_value_and_gradient")

    assert FULL_BLOCKER in _source()
    assert "MATERIAL_FULL_BLOCKER_CODE" in parse_args
    assert 'args.gate_mode == "material"' in main_source
    assert "_run_material_manual_route" in main_source
    assert "return" in main_source
    assert "tf.GradientTape" in taped_wrapper
    material_dispatch_prefix = main_source.split("records = []", maxsplit=1)[0]
    assert "tf.GradientTape" not in material_dispatch_prefix
    assert "base_compiled = _make_compiled_contract_e" not in material_dispatch_prefix
