from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "docs" / "benchmarks" / "diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py"
TRANSPORT_TARGET = (
    ROOT
    / "experiments"
    / "dpf_implementation"
    / "tf_tfp"
    / "resampling"
    / "annealed_transport_tf.py"
)
FULL_BLOCKER_CODE = "PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION"
ROUTE_LABEL = "contract_e_cholesky_fixed_ridge_manual_lgssm_tiny"
STAGE_A_ROUTE_LABEL = "contract_e_cholesky_fixed_ridge_manual_lgssm_t10"
SCORE_ROUTE = "manual_likelihood_reverse_scan_no_autodiff"
R12_SCORE_ROUTE = "manual-reverse-scan"


def _source() -> str:
    return TARGET.read_text(encoding="utf-8")


def _function_source(name: str) -> str:
    source = _source()
    return _function_source_from_text(source, name)


def _transport_function_source(name: str) -> str:
    source = TRANSPORT_TARGET.read_text(encoding="utf-8")
    return _function_source_from_text(source, name)


def _function_source_from_text(source: str, name: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            if node.end_lineno is None:
                raise AssertionError(f"missing end line for {name}")
            return "\n".join(lines[node.lineno - 1 : node.end_lineno])
    raise AssertionError(f"function not found: {name}")


def test_phase3_route_names_separate_smoke_transport_probe_from_material_manual_route() -> None:
    source = _source()

    assert "manual-transport-vjp-only" in source
    assert SCORE_ROUTE in source
    assert ROUTE_LABEL in source
    assert STAGE_A_ROUTE_LABEL in source
    assert FULL_BLOCKER_CODE in source


def test_phase3_material_tiny_dispatch_uses_manual_route_before_taped_smoke_wrapper() -> None:
    source = _source()
    gradient_function = _function_source("_make_compiled_value_and_gradient")
    parse_args = _function_source("_parse_args")
    main_source = _function_source("main")

    assert "tf.GradientTape" in gradient_function
    assert "tape.gradient" in gradient_function
    assert "args.gate_mode == \"material\"" in parse_args
    assert FULL_BLOCKER_CODE in source
    assert "MATERIAL_FULL_BLOCKER_CODE" in parse_args
    assert "_run_material_manual_route" in main_source
    material_dispatch_prefix = main_source.split("records = []", maxsplit=1)[0]
    assert "tf.GradientTape" not in material_dispatch_prefix


def test_phase3_full_material_guard_removed_only_with_manual_score_route() -> None:
    source = _source()
    has_full_material_blocker = FULL_BLOCKER_CODE in _function_source("_parse_args")

    if not has_full_material_blocker:
        assert SCORE_ROUTE in source
        assert ROUTE_LABEL in source
        assert STAGE_A_ROUTE_LABEL in source
        assert "tf.GradientTape" not in _function_source("_run_material_manual_fixture")


def test_phase3_r12_gpu_manual_score_route_is_explicit_reverse_scan() -> None:
    manual_route = _function_source("_make_compiled_contract_e_manual_value_and_score")
    base_dispatch = _function_source("_run_base_gradient")

    assert R12_SCORE_ROUTE in base_dispatch
    assert "_make_compiled_contract_e_manual_value_and_score" in base_dispatch
    assert "tf.while_loop" in manual_route
    assert "forward_body" in manual_route
    assert "reverse_body" in manual_route
    assert "tf.GradientTape" not in manual_route
    assert "tape.gradient" not in manual_route
    assert "contract_e_cholesky_ridge_reset_fixed_ridge_vjp" in manual_route
    assert "_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys" in manual_route
    assert "_normalize_log_weights_vjp" in manual_route
    assert "_log_weight_correction_vjp" in manual_route
    assert "_transition_gaussian_log_density_vjp" in manual_route
    assert "_observation_gaussian_log_density_vjp" in manual_route
    assert "_batched_ledh_linearized_flow_vjp" in manual_route


def test_phase3_r14_manual_dense_sinkhorn_recursions_use_tf_while_loop() -> None:
    for name in (
        "_filterflow_manual_dense_finite_sinkhorn_outputs",
        "_filterflow_manual_dense_finite_sinkhorn_vjp",
    ):
        source = _transport_function_source(name)
        assert "tf.while_loop" in source
        assert "range(steps)" not in source
        assert "tf.GradientTape" not in source
        assert "tape.gradient" not in source
