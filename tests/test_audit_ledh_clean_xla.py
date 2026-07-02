from __future__ import annotations

import ast
from pathlib import Path
import argparse
import json

import tensorflow as tf

from docs.benchmarks import benchmark_p8p_parameterized_sir_gradient as p8p
from experiments.dpf_implementation.tf_tfp.resampling import annealed_transport_tf
from scripts import audit_ledh_clean_xla as audit


CURRENT_VETO_IDS = {
    pattern.id for pattern in audit.REQUIRED_PATTERNS if pattern.severity == "current_veto"
}
PHASE2_REMOVED_CURRENT_VETO_IDS = {"SIR-MANUAL-SEED-LOOP"}
PHASE3_REMOVED_CURRENT_VETO_IDS = {
    "SIR-RK4-FWD-LIST",
    "SIR-RK4-FWD-RANGE",
    "SIR-RK4-REV-REVERSED",
}
PHASE4_REMOVED_CURRENT_VETO_IDS = {
    "SIR-MANUAL-TIME-STATIC",
    "SIR-MANUAL-RECORD-LIST",
    "SIR-MANUAL-FWD-RANGE",
    "SIR-MANUAL-REV-REVERSED",
}
PHASE5_REMOVED_CURRENT_VETO_IDS = {
    "SINK-STOPPED-VALUE-RANGE",
    "SINK-TOTAL-VALUE-RANGE",
    "SINK-STOPPED-VJP-STATES",
}
PHASE5_TARGET_SINKHORN_SYMBOLS = {
    "_filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys",
    "_filterflow_streaming_finite_sinkhorn_potentials_total_vjp",
    "_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys",
}
PHASE4_BASELINE_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "plans"
    / "bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-preedit-manual-scan-baseline-2026-07-02.json"
)
PHASE5_BASELINE_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "plans"
    / "bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-preedit-sinkhorn-loop-baseline-2026-07-02.json"
)


def _write_synthetic_sources(tmp_path: Path, *, omit_symbol: str | None = None) -> tuple[Path, Path]:
    sir_functions = {
        "_sir_transition_mean_with_aux_tf": """
def _sir_transition_mean_with_aux_tf():
    return None
""",
        "_sir_transition_mean_vjp_tf": """
def _sir_transition_mean_vjp_tf():
    return None
""",
        "_manual_value_and_score_from_components": """
def _manual_value_and_score_from_components():
    return None
""",
    }
    transport_functions = {
        "_filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys": """
def _filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys():
    return None
""",
        "_filterflow_streaming_finite_sinkhorn_potentials_total_vjp": """
def _filterflow_streaming_finite_sinkhorn_potentials_total_vjp():
    return None
""",
        "_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys": """
def _filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys():
    return None
""",
        "_filterflow_manual_streaming_finite_transport_total_vjp": """
def _filterflow_manual_streaming_finite_transport_total_vjp():
    return None
""",
    }
    if omit_symbol in sir_functions:
        del sir_functions[omit_symbol]
    if omit_symbol in transport_functions:
        del transport_functions[omit_symbol]
    sir_path = tmp_path / "sir_fixture.py"
    transport_path = tmp_path / "transport_fixture.py"
    sir_path.write_text("\n".join(sir_functions.values()), encoding="utf-8")
    transport_path.write_text("\n".join(transport_functions.values()), encoding="utf-8")
    return sir_path, transport_path


def test_default_clean_xla_audit_reports_current_route_unclean_with_line_anchors() -> None:
    result = audit.audit_default()

    assert result["decision"] == "FAIL_CURRENT_ROUTE"
    assert result["missing_required_patterns"] == []
    found_current_veto_ids = {
        item["id"]
        for item in result["required_pattern_results"]
        if item["status"] == "FOUND_CURRENT_VETO"
    }
    removed_current_veto_ids = (
        PHASE2_REMOVED_CURRENT_VETO_IDS
        | PHASE3_REMOVED_CURRENT_VETO_IDS
        | PHASE4_REMOVED_CURRENT_VETO_IDS
        | PHASE5_REMOVED_CURRENT_VETO_IDS
    )
    assert found_current_veto_ids == CURRENT_VETO_IDS - removed_current_veto_ids
    assert {
        item["id"]
        for item in result["required_pattern_results"]
        if item["status"] == "ABSENT_CLEAN_OR_MOVED"
    } == removed_current_veto_ids
    assert result["current_veto_findings"]
    assert result["warning_findings"]
    assert "stopped partial derivatives are not scores" in result["nonclaims"]
    for finding in result["findings"]:
        assert finding["line"] > 0
        assert finding["symbol"]
        assert finding["path"] != ""


def test_phase5_sinkhorn_target_helpers_have_no_python_step_loop_or_state_list() -> None:
    spans = audit._load_function_spans_with_parent(audit.DEFAULT_TRANSPORT_PATH)  # noqa: SLF001

    for symbol in PHASE5_TARGET_SINKHORN_SYMBOLS:
        node = spans[symbol].node
        python_for_nodes = [
            inner
            for inner in ast.walk(node)
            if isinstance(inner, (ast.For, ast.AsyncFor))
        ]
        assert python_for_nodes == []
        for inner in ast.walk(node):
            if (
                isinstance(inner, ast.Assign)
                and isinstance(inner.value, ast.List)
                and not inner.value.elts
            ):
                target_names = [
                    target.id
                    for target in inner.targets
                    if isinstance(target, ast.Name)
                ]
                assert not any(
                    name in {"states"} or name.endswith("_states")
                    for name in target_names
                )
            if (
                isinstance(inner, ast.Call)
                and isinstance(inner.func, ast.Attribute)
                and inner.func.attr == "append"
            ):
                owner = inner.func.value
                owner_name = owner.id if isinstance(owner, ast.Name) else ""
                assert owner_name not in {"states"}


def test_clean_xla_audit_passes_synthetic_clean_symbol_spans(tmp_path: Path) -> None:
    sir_path, transport_path = _write_synthetic_sources(tmp_path)

    result = audit.audit_paths(sir_path=sir_path, transport_path=transport_path)

    assert result["decision"] == "PASS_STATIC_CLEAN_XLA_GUARDRAIL"
    assert result["findings"] == []
    assert result["missing_required_patterns"] == []
    absent_ids = {item["id"] for item in result["absent_current_veto_patterns"]}
    assert absent_ids == CURRENT_VETO_IDS


def test_clean_xla_audit_missing_current_veto_symbol_fails_configuration(tmp_path: Path) -> None:
    sir_path, transport_path = _write_synthetic_sources(
        tmp_path,
        omit_symbol="_manual_value_and_score_from_components",
    )

    result = audit.audit_paths(sir_path=sir_path, transport_path=transport_path)

    assert result["decision"] == "FAIL_AUDIT_CONFIGURATION"
    missing_ids = {item["id"] for item in result["missing_required_patterns"]}
    assert {
        "SIR-MANUAL-TIME-STATIC",
        "SIR-MANUAL-RECORD-LIST",
        "SIR-MANUAL-FWD-RANGE",
        "SIR-MANUAL-SEED-LOOP",
        "SIR-MANUAL-REV-REVERSED",
    }.issubset(missing_ids)


def test_clean_xla_audit_missing_warning_symbol_does_not_fail(tmp_path: Path) -> None:
    sir_path, transport_path = _write_synthetic_sources(
        tmp_path,
        omit_symbol="_filterflow_manual_streaming_finite_transport_total_vjp",
    )

    result = audit.audit_paths(sir_path=sir_path, transport_path=transport_path)

    assert result["decision"] == "PASS_STATIC_CLEAN_XLA_GUARDRAIL"
    assert result["missing_required_patterns"] == []
    assert [item["id"] for item in result["missing_warning_symbols"]] == [
        "SINK-TOTAL-CUSTOM-TAPE"
    ]


def test_phase2_transition_noise_tensor_matches_previous_stateless_policy() -> None:
    batch_seeds = [101, 202]
    time_steps = 2
    num_particles = 3
    state_dim = 4

    tensor = p8p._make_transition_noise_tensor(  # noqa: SLF001
        batch_seeds=batch_seeds,
        time_steps=time_steps,
        num_particles=num_particles,
        state_dim=state_dim,
    )

    expected_time_rows = []
    for time_index in range(time_steps):
        expected_batch_rows = []
        for seed in batch_seeds:
            seed_tensor = tf.stack(
                [
                    tf.constant(int(seed) % 2147483647, dtype=tf.int32),
                    tf.math.floormod(
                        tf.constant(1140 + int(time_index), dtype=tf.int32),
                        tf.constant(2147483647, dtype=tf.int32),
                    ),
                ]
            )
            expected_batch_rows.append(
                tf.random.stateless_normal(
                    [num_particles, state_dim],
                    seed=seed_tensor,
                    dtype=p8p.DTYPE,
                )
            )
        expected_time_rows.append(tf.stack(expected_batch_rows, axis=0))
    expected = tf.stack(expected_time_rows, axis=1)

    assert tensor.shape == (len(batch_seeds), time_steps, num_particles, state_dim)
    tf.debugging.assert_equal(tensor, expected)


def _reference_sir_transition_mean_with_aux(
    points: tf.Tensor,
    *,
    kappa: tf.Tensor,
    nu: tf.Tensor,
    adjacency: tf.Tensor,
    neighbor_degree: tf.Tensor,
    substeps: int,
    step_size: tf.Tensor,
) -> tuple[tf.Tensor, dict[str, tf.Tensor]]:
    state = tf.cast(points, p8p.DTYPE)
    aux: dict[str, list[tf.Tensor]] = {
        "state": [],
        "k1": [],
        "k2_input": [],
        "k2": [],
        "k3_input": [],
        "k3": [],
        "k4_input": [],
    }
    half = tf.constant(0.5, dtype=p8p.DTYPE)
    for _ in range(int(substeps)):
        start = state
        k1 = p8p._sir_rhs_tf(  # noqa: SLF001
            start,
            kappa=kappa,
            nu=nu,
            adjacency=adjacency,
            neighbor_degree=neighbor_degree,
        )
        k2_input = start + half * step_size * k1
        k2 = p8p._sir_rhs_tf(  # noqa: SLF001
            k2_input,
            kappa=kappa,
            nu=nu,
            adjacency=adjacency,
            neighbor_degree=neighbor_degree,
        )
        k3_input = start + half * step_size * k2
        k3 = p8p._sir_rhs_tf(  # noqa: SLF001
            k3_input,
            kappa=kappa,
            nu=nu,
            adjacency=adjacency,
            neighbor_degree=neighbor_degree,
        )
        k4_input = start + half * step_size * k3
        k4 = p8p._sir_rhs_tf(  # noqa: SLF001
            k4_input,
            kappa=kappa,
            nu=nu,
            adjacency=adjacency,
            neighbor_degree=neighbor_degree,
        )
        state = start + (step_size / tf.constant(6.0, dtype=p8p.DTYPE)) * (
            k1
            + tf.constant(2.0, dtype=p8p.DTYPE) * k2
            + tf.constant(2.0, dtype=p8p.DTYPE) * k3
            + k4
        )
        aux["state"].append(start)
        aux["k1"].append(k1)
        aux["k2_input"].append(k2_input)
        aux["k2"].append(k2)
        aux["k3_input"].append(k3_input)
        aux["k3"].append(k3)
        aux["k4_input"].append(k4_input)
    return state, {key: tf.stack(value, axis=0) for key, value in aux.items()}


def test_phase3_rk4_tf_loop_matches_independent_reference_and_tape_vjp() -> None:
    points = tf.reshape(
        tf.linspace(
            tf.constant(0.05, dtype=p8p.DTYPE),
            tf.constant(0.95, dtype=p8p.DTYPE),
            2 * 3 * 18,
        ),
        [2, 3, 18],
    )
    kappa = tf.linspace(
        tf.constant(0.04, dtype=p8p.DTYPE),
        tf.constant(0.12, dtype=p8p.DTYPE),
        9,
    )
    nu = tf.linspace(
        tf.constant(0.03, dtype=p8p.DTYPE),
        tf.constant(0.09, dtype=p8p.DTYPE),
        9,
    )
    adjacency = tf.cast(p8p._SIR_ADJACENCY_MATRIX, p8p.DTYPE)  # noqa: SLF001
    neighbor_degree = tf.cast(p8p._SIR_NEIGHBOR_DEGREE, p8p.DTYPE)  # noqa: SLF001
    substeps = 3
    step_size = tf.constant(0.125, dtype=p8p.DTYPE)
    upstream = tf.reshape(
        tf.linspace(
            tf.constant(-0.3, dtype=p8p.DTYPE),
            tf.constant(0.4, dtype=p8p.DTYPE),
            2 * 3 * 18,
        ),
        [2, 3, 18],
    )

    reference_state, reference_aux = _reference_sir_transition_mean_with_aux(
        points,
        kappa=kappa,
        nu=nu,
        adjacency=adjacency,
        neighbor_degree=neighbor_degree,
        substeps=substeps,
        step_size=step_size,
    )
    edited_state, edited_aux = p8p._sir_transition_mean_with_aux_tf(  # noqa: SLF001
        points,
        kappa=kappa,
        nu=nu,
        adjacency=adjacency,
        neighbor_degree=neighbor_degree,
        substeps=substeps,
        step_size=step_size,
    )

    tf.debugging.assert_near(edited_state, reference_state, atol=1.0e-6, rtol=1.0e-6)
    assert set(edited_aux) == set(reference_aux)
    for key in reference_aux:
        tf.debugging.assert_near(edited_aux[key], reference_aux[key], atol=1.0e-6, rtol=1.0e-6)

    edited_bar_points, edited_bar_kappa, edited_bar_nu = p8p._sir_transition_mean_vjp_tf(  # noqa: SLF001
        edited_aux,
        upstream,
        kappa=kappa,
        nu=nu,
        adjacency=adjacency,
        neighbor_degree=neighbor_degree,
        step_size=step_size,
    )

    points_var = tf.Variable(points)
    kappa_var = tf.Variable(kappa)
    nu_var = tf.Variable(nu)
    with tf.GradientTape() as tape:
        reference_for_tape, _ = _reference_sir_transition_mean_with_aux(
            points_var,
            kappa=kappa_var,
            nu=nu_var,
            adjacency=adjacency,
            neighbor_degree=neighbor_degree,
            substeps=substeps,
            step_size=step_size,
        )
        scalar = tf.reduce_sum(reference_for_tape * upstream)
    tape_bar_points, tape_bar_kappa, tape_bar_nu = tape.gradient(
        scalar,
        [points_var, kappa_var, nu_var],
    )

    tf.debugging.assert_near(edited_bar_points, tape_bar_points, atol=1.0e-5, rtol=1.0e-5)
    tf.debugging.assert_near(
        tf.reduce_sum(edited_bar_kappa, axis=0),
        tape_bar_kappa,
        atol=1.0e-5,
        rtol=1.0e-5,
    )
    tf.debugging.assert_near(
        tf.reduce_sum(edited_bar_nu, axis=0),
        tape_bar_nu,
        atol=1.0e-5,
        rtol=1.0e-5,
    )


def _phase4_args(payload: dict) -> argparse.Namespace:
    args_payload = payload["args"]
    return argparse.Namespace(
        batch_seeds=list(args_payload["batch_seeds"]),
        time_steps=int(args_payload["time_steps"]),
        num_particles=int(args_payload["num_particles"]),
        theta_values=[float(x) for x in args_payload["theta_values"]],
        transport_policy=str(args_payload["transport_policy"]),
        sinkhorn_iterations=int(args_payload["sinkhorn_iterations"]),
        sinkhorn_epsilon=float(args_payload["sinkhorn_epsilon"]),
        annealed_scaling=float(args_payload["annealed_scaling"]),
        annealed_convergence_threshold=1.0e-3,
        transport_plan_mode="streaming",
        transport_gradient_mode=str(args_payload["transport_gradient_mode"]),
        transport_ad_mode=str(args_payload["transport_ad_mode"]),
        row_chunk_size=2,
        col_chunk_size=2,
        particle_chunk_size=2,
        dtype=str(args_payload["dtype"]),
        tf32_mode="disabled" if args_payload["dtype"] == "float64" else "enabled",
        device="/CPU:0",
        device_scope="cpu",
        cuda_visible_devices=None,
        expect_device_kind="cpu",
        seed_microbatch_size=0,
    )


def test_phase4_manual_scan_loop_matches_preedit_baseline_fixture() -> None:
    payload = json.loads(PHASE4_BASELINE_PATH.read_text(encoding="utf-8"))
    args = _phase4_args(payload)
    p8p._configure_precision(args)  # noqa: SLF001
    tensors, _semantics = p8p._build_base_tensors(args)  # noqa: SLF001

    diagnostic = p8p._manual_value_and_score_from_components(  # noqa: SLF001
        tensors,
        args,
        p8p._theta_components(args.theta_values),  # noqa: SLF001
    )

    tf.debugging.assert_near(
        diagnostic["objective"],
        tf.constant(payload["objective"], dtype=p8p.DTYPE),
        atol=1.0e-6,
        rtol=1.0e-6,
    )
    tf.debugging.assert_near(
        diagnostic["log_likelihood"],
        tf.constant(payload["log_likelihood"], dtype=p8p.DTYPE),
        atol=1.0e-6,
        rtol=1.0e-6,
    )
    tf.debugging.assert_near(
        diagnostic["gradient_tensor"],
        tf.constant(payload["gradient_tensor"], dtype=p8p.DTYPE),
        atol=1.0e-5,
        rtol=1.0e-6,
    )
    tf.debugging.assert_near(
        diagnostic["per_seed_gradient"],
        tf.constant(payload["per_seed_gradient"], dtype=p8p.DTYPE),
        atol=1.0e-5,
        rtol=1.0e-6,
    )


def test_phase4_manual_scan_loop_matches_python_record_reference() -> None:
    payload = json.loads(PHASE4_BASELINE_PATH.read_text(encoding="utf-8"))
    args = _phase4_args(payload)
    p8p._configure_precision(args)  # noqa: SLF001
    tensors, _semantics = p8p._build_base_tensors(args)  # noqa: SLF001
    theta_components = p8p._theta_components(args.theta_values)  # noqa: SLF001

    loop_route = p8p._manual_value_and_score_from_components(  # noqa: SLF001
        tensors,
        args,
        theta_components,
    )
    reference = p8p._manual_value_and_score_from_components_python_record_reference(  # noqa: SLF001
        tensors,
        args,
        theta_components,
    )

    for key in ("objective", "log_likelihood", "gradient_tensor", "per_seed_gradient"):
        tf.debugging.assert_near(loop_route[key], reference[key], atol=1.0e-6, rtol=1.0e-6)


def _phase5_cotangent(shape: tuple[int, ...], scale: float) -> tf.Tensor:
    count = 1
    for dim in shape:
        count *= dim
    return tf.reshape(
        tf.linspace(tf.constant(-scale, p8p.DTYPE), tf.constant(scale, p8p.DTYPE), count),
        shape,
    )


def _phase5_sinkhorn_fixture(
    batch_size: int,
    num_particles: int,
    state_dim: int,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    x = tf.reshape(
        tf.linspace(
            tf.constant(-0.35, p8p.DTYPE),
            tf.constant(0.55, p8p.DTYPE),
            batch_size * num_particles * state_dim,
        ),
        [batch_size, num_particles, state_dim],
    )
    raw_alpha = tf.reshape(
        tf.linspace(
            tf.constant(-0.22, p8p.DTYPE),
            tf.constant(0.18, p8p.DTYPE),
            batch_size * num_particles,
        ),
        [batch_size, num_particles],
    )
    raw_beta = tf.reshape(
        tf.linspace(
            tf.constant(0.16, p8p.DTYPE),
            tf.constant(-0.19, p8p.DTYPE),
            batch_size * num_particles,
        ),
        [batch_size, num_particles],
    )
    log_alpha = raw_alpha - tf.reduce_logsumexp(raw_alpha, axis=1, keepdims=True)
    log_beta = raw_beta - tf.reduce_logsumexp(raw_beta, axis=1, keepdims=True)
    upstream_alpha = _phase5_cotangent((batch_size, num_particles), 0.041)
    upstream_beta = _phase5_cotangent((batch_size, num_particles), 0.027)
    epsilon = tf.constant(0.43, p8p.DTYPE)
    epsilon0 = tf.linspace(
        tf.constant(0.85, p8p.DTYPE),
        tf.constant(0.95, p8p.DTYPE),
        batch_size,
    )
    scaling = tf.constant(0.82, p8p.DTYPE)
    return log_alpha, log_beta, x, upstream_alpha, upstream_beta, epsilon, epsilon0, scaling


def test_phase5_streaming_sinkhorn_loop_state_matches_preedit_fixture() -> None:
    payload = json.loads(PHASE5_BASELINE_PATH.read_text(encoding="utf-8"))
    old_transport_dtype = annealed_transport_tf.DTYPE
    old_p8p_dtype = p8p.DTYPE
    annealed_transport_tf.DTYPE = tf.float64
    p8p.DTYPE = tf.float64
    try:
        for record in payload["records"]:
            case = record["case"]
            (
                log_alpha,
                log_beta,
                x,
                upstream_alpha,
                upstream_beta,
                epsilon,
                epsilon0,
                scaling,
            ) = _phase5_sinkhorn_fixture(
                int(case["batch_size"]),
                int(case["num_particles"]),
                int(case["state_dim"]),
            )
            stopped_alpha, stopped_beta = (
                annealed_transport_tf._filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys(  # noqa: SLF001
                    log_alpha,
                    log_beta,
                    x,
                    epsilon,
                    epsilon0,
                    scaling,
                    steps=int(case["steps"]),
                    row_chunk_size=int(case["row_chunk_size"]),
                    col_chunk_size=int(case["col_chunk_size"]),
                )
            )
            total_alpha, total_beta = (
                annealed_transport_tf._filterflow_streaming_finite_sinkhorn_potentials_total_vjp(  # noqa: SLF001
                    log_alpha,
                    log_beta,
                    x,
                    epsilon,
                    epsilon0,
                    scaling,
                    steps=int(case["steps"]),
                    row_chunk_size=int(case["row_chunk_size"]),
                    col_chunk_size=int(case["col_chunk_size"]),
                )
            )
            d_log_alpha, d_log_beta, d_x = (
                annealed_transport_tf._filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys(  # noqa: SLF001
                    log_alpha,
                    log_beta,
                    x,
                    upstream_alpha,
                    upstream_beta,
                    epsilon,
                    epsilon0,
                    scaling,
                    steps=int(case["steps"]),
                    row_chunk_size=int(case["row_chunk_size"]),
                    col_chunk_size=int(case["col_chunk_size"]),
                )
            )
            comparisons = {
                "stopped_alpha": stopped_alpha,
                "stopped_beta": stopped_beta,
                "total_alpha": total_alpha,
                "total_beta": total_beta,
                "vjp_d_log_alpha": d_log_alpha,
                "vjp_d_log_beta": d_log_beta,
                "vjp_d_x": d_x,
            }
            for key, value in comparisons.items():
                tf.debugging.assert_near(
                    value,
                    tf.constant(record[key], dtype=tf.float64),
                    atol=1.0e-10,
                    rtol=1.0e-10,
                )
    finally:
        annealed_transport_tf.DTYPE = old_transport_dtype
        p8p.DTYPE = old_p8p_dtype
