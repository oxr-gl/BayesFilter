"""Value-decomposition diagnostic for the LEDH-PFPF-OT LGSSM gap.

This script localizes the value mismatch observed in
``tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py``.  It is diagnostic
only: it does not certify gradients, posterior correctness, or production
readiness.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import math
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HARNESS_PATH = ROOT / "tests" / "test_ledh_pfpf_ot_lgssm_kalman_statistical.py"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--num-particles", type=int, default=1000)
    parser.add_argument("--seed-count", type=int, default=10)
    parser.add_argument("--state-dims", type=int, nargs="+", default=[1, 2])
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default="visible")
    parser.add_argument("--cuda-visible-devices", default="0")
    parser.add_argument("--xla", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--tf32-mode", choices=("enabled", "disabled"), default="enabled")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", default=None)
    args = parser.parse_args()
    if args.num_particles <= 1:
        raise ValueError("--num-particles must be greater than one")
    if args.seed_count != 10:
        raise ValueError("this diagnostic currently reuses the harness SEED_COUNT=10 contract")
    if any(dim not in (1, 2) for dim in args.state_dims):
        raise ValueError("--state-dims currently supports only 1 and 2")
    return args


def _configure_import_environment(args: argparse.Namespace) -> None:
    if args.device_scope == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = str(args.cuda_visible_devices)
    os.environ["BAYESFILTER_RUN_LEDHPFPFOT_LGSSM_N1000"] = "1"
    os.environ["BAYESFILTER_LEDHPFPFOT_LGSSM_NUM_PARTICLES"] = str(args.num_particles)
    os.environ.setdefault("TF_FORCE_GPU_ALLOW_GROWTH", "true")
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")


def _load_harness() -> Any:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location("ledh_lgssm_harness", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load harness from {HARNESS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _configure_tensorflow(harness: Any, args: argparse.Namespace) -> dict[str, Any]:
    tf = harness.tf
    tf.config.experimental.enable_tensor_float_32_execution(args.tf32_mode == "enabled")
    physical_gpus = tf.config.list_physical_devices("GPU")
    for gpu in physical_gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            pass
    logical_gpus = tf.config.list_logical_devices("GPU")
    return {
        "device_scope": args.device_scope,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "physical_gpus": [str(device) for device in physical_gpus],
        "logical_gpus": [str(device) for device in logical_gpus],
        "tf32_execution_enabled": bool(
            tf.config.experimental.tensor_float_32_execution_enabled()
        ),
        "xla": bool(args.xla),
    }


def _kalman_transition_first_increments(harness: Any, state_dim: int, observations: Any) -> Any:
    np = harness.np
    theta = harness.THETA.numpy().astype(np.float64)
    a = float(theta[0])
    q = float(np.exp(theta[1]))
    r = float(np.exp(theta[2]))
    y = observations.astype(np.float64)
    mean = np.zeros(state_dim, dtype=np.float64)
    covariance = 0.7 * np.eye(state_dim, dtype=np.float64)
    transition = a * np.eye(state_dim, dtype=np.float64)
    transition_covariance = q * np.eye(state_dim, dtype=np.float64)
    observation_covariance = r * np.eye(state_dim, dtype=np.float64)
    increments = []
    for obs in y:
        predicted_mean = transition @ mean
        predicted_covariance = transition @ covariance @ transition.T + transition_covariance
        innovation = obs - predicted_mean
        innovation_covariance = predicted_covariance + observation_covariance
        sign, logdet = np.linalg.slogdet(innovation_covariance)
        if sign <= 0:
            raise RuntimeError("non-positive innovation covariance")
        increments.append(
            -0.5
            * (
                state_dim * math.log(2.0 * math.pi)
                + logdet
                + innovation @ np.linalg.solve(innovation_covariance, innovation)
            )
        )
        gain = predicted_covariance @ np.linalg.inv(innovation_covariance)
        left = np.eye(state_dim, dtype=np.float64) - gain
        mean = predicted_mean + gain @ innovation
        covariance = (
            left @ predicted_covariance @ left.T
            + gain @ observation_covariance @ gain.T
        )
    return np.asarray(increments, dtype=np.float64)


def _kalman_observe_initial_first_increments(
    harness: Any,
    state_dim: int,
    observations: Any,
) -> Any:
    np = harness.np
    theta = harness.THETA.numpy().astype(np.float64)
    a = float(theta[0])
    q = float(np.exp(theta[1]))
    r = float(np.exp(theta[2]))
    y = observations.astype(np.float64)
    mean = np.zeros(state_dim, dtype=np.float64)
    covariance = 0.7 * np.eye(state_dim, dtype=np.float64)
    transition = a * np.eye(state_dim, dtype=np.float64)
    transition_covariance = q * np.eye(state_dim, dtype=np.float64)
    observation_covariance = r * np.eye(state_dim, dtype=np.float64)
    increments = []
    for obs in y:
        innovation = obs - mean
        innovation_covariance = covariance + observation_covariance
        sign, logdet = np.linalg.slogdet(innovation_covariance)
        if sign <= 0:
            raise RuntimeError("non-positive innovation covariance")
        increments.append(
            -0.5
            * (
                state_dim * math.log(2.0 * math.pi)
                + logdet
                + innovation @ np.linalg.solve(innovation_covariance, innovation)
            )
        )
        gain = covariance @ np.linalg.inv(innovation_covariance)
        left = np.eye(state_dim, dtype=np.float64) - gain
        mean = mean + gain @ innovation
        covariance = left @ covariance @ left.T + gain @ observation_covariance @ gain.T
        mean = transition @ mean
        covariance = transition @ covariance @ transition.T + transition_covariance
    return np.asarray(increments, dtype=np.float64)


def _make_compiled_decomposition(harness: Any, state_dim: int, *, xla: bool):
    tf = harness.tf
    core = harness.core_ledh
    dtype = harness.DTYPE
    batch_size = harness.SEED_COUNT
    num_particles = harness.NUM_PARTICLES
    time_steps = harness.TIME_STEPS

    def ledh_step(
        time_index: Any,
        current_particles: Any,
        current_log_weights: Any,
        transition_matrix: Any,
        transition_covariance: Any,
        observation_covariance: Any,
        transition_std: Any,
        observations: Any,
        transition_noise: Any,
        h_jac: Any,
        *,
        use_transport: bool,
    ) -> tuple[Any, Any, Any]:
        observation = observations[time_index]
        prior_mean = tf.einsum("bnj,bdj->bnd", current_particles, transition_matrix)
        noise = transition_noise[:, time_index, :, :]
        pre_flow = prior_mean + noise * transition_std[:, None, :]
        residual = observation[None, None, :] - pre_flow
        flow, _flow_aux = core._batched_ledh_linearized_flow_with_aux_tf(
            pre_flow_particles=pre_flow,
            prior_means=prior_mean,
            observation_jacobian=h_jac,
            observation_residual=residual,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
        )
        post_flow = flow.post_flow_particles
        transition_log_density = harness._diag_gaussian_logpdf(
            post_flow - prior_mean,
            transition_covariance,
        )
        observation_log_density = harness._diag_gaussian_logpdf(
            post_flow - observation[None, None, :],
            observation_covariance,
        )
        corrected_log_weights = (
            current_log_weights
            + transition_log_density
            + observation_log_density
            - flow.pre_flow_log_density
            + flow.forward_log_det
        )
        weights, increment = core._normalize_log_weights(corrected_log_weights)
        normalized_log_weights = tf.math.log(tf.maximum(weights, core._log_weight_floor()))
        if use_transport:
            next_particles, next_log_weights = harness._transport_forward(
                post_flow,
                normalized_log_weights,
            )
        else:
            next_particles = post_flow
            next_log_weights = normalized_log_weights
        return next_particles, next_log_weights, increment

    @tf.function(
        input_signature=[
            tf.TensorSpec([batch_size, 3], dtype),
            tf.TensorSpec([batch_size, num_particles, state_dim], dtype),
            tf.TensorSpec([batch_size, time_steps, num_particles, state_dim], dtype),
            tf.TensorSpec([time_steps, state_dim], dtype),
        ],
        jit_compile=xla,
        reduce_retracing=True,
    )
    def compiled(
        values: Any,
        initial_particles: Any,
        transition_noise: Any,
        observations: Any,
    ) -> dict[str, Any]:
        transition_matrix, transition_covariance, observation_covariance = (
            harness._theta_to_lgssm(values, state_dim)
        )
        transition_std = tf.sqrt(tf.linalg.diag_part(transition_covariance))
        h_jac = tf.tile(
            tf.eye(state_dim, dtype=dtype)[None, None, :, :],
            [batch_size, num_particles, 1, 1],
        )
        initial_log_weights = core.uniform_log_weights(batch_size, num_particles)
        sis_particles = initial_particles
        sis_log_weights = initial_log_weights
        ledh_no_ot_particles = initial_particles
        ledh_no_ot_log_weights = initial_log_weights
        ledh_ot_particles = initial_particles
        ledh_ot_log_weights = initial_log_weights
        sis_increments = tf.TensorArray(
            dtype=dtype,
            size=time_steps,
            element_shape=tf.TensorShape([batch_size]),
        )
        ledh_no_ot_increments = tf.TensorArray(
            dtype=dtype,
            size=time_steps,
            element_shape=tf.TensorShape([batch_size]),
        )
        ledh_ot_increments = tf.TensorArray(
            dtype=dtype,
            size=time_steps,
            element_shape=tf.TensorShape([batch_size]),
        )

        def cond(time_index, *_loop_vars):
            return time_index < tf.constant(time_steps, dtype=tf.int32)

        def body(
            time_index,
            sis_particles_current,
            sis_log_weights_current,
            ledh_no_ot_particles_current,
            ledh_no_ot_log_weights_current,
            ledh_ot_particles_current,
            ledh_ot_log_weights_current,
            sis_increment_ta,
            ledh_no_ot_increment_ta,
            ledh_ot_increment_ta,
        ):
            observation = observations[time_index]
            sis_prior_mean = tf.einsum(
                "bnj,bdj->bnd",
                sis_particles_current,
                transition_matrix,
            )
            noise = transition_noise[:, time_index, :, :]
            sis_particles_next = sis_prior_mean + noise * transition_std[:, None, :]
            sis_observation_log_density = harness._diag_gaussian_logpdf(
                sis_particles_next - observation[None, None, :],
                observation_covariance,
            )
            sis_corrected = sis_log_weights_current + sis_observation_log_density
            sis_weights, sis_increment = core._normalize_log_weights(sis_corrected)
            sis_log_weights_next = tf.math.log(
                tf.maximum(sis_weights, core._log_weight_floor())
            )
            (
                ledh_no_ot_particles_next,
                ledh_no_ot_log_weights_next,
                ledh_no_ot_increment,
            ) = ledh_step(
                time_index,
                ledh_no_ot_particles_current,
                ledh_no_ot_log_weights_current,
                transition_matrix,
                transition_covariance,
                observation_covariance,
                transition_std,
                observations,
                transition_noise,
                h_jac,
                use_transport=False,
            )
            (
                ledh_ot_particles_next,
                ledh_ot_log_weights_next,
                ledh_ot_increment,
            ) = ledh_step(
                time_index,
                ledh_ot_particles_current,
                ledh_ot_log_weights_current,
                transition_matrix,
                transition_covariance,
                observation_covariance,
                transition_std,
                observations,
                transition_noise,
                h_jac,
                use_transport=True,
            )
            return (
                time_index + 1,
                sis_particles_next,
                sis_log_weights_next,
                ledh_no_ot_particles_next,
                ledh_no_ot_log_weights_next,
                ledh_ot_particles_next,
                ledh_ot_log_weights_next,
                sis_increment_ta.write(time_index, sis_increment),
                ledh_no_ot_increment_ta.write(time_index, ledh_no_ot_increment),
                ledh_ot_increment_ta.write(time_index, ledh_ot_increment),
            )

        (
            _,
            _sis_particles,
            _sis_log_weights,
            _ledh_no_ot_particles,
            _ledh_no_ot_log_weights,
            _ledh_ot_particles,
            _ledh_ot_log_weights,
            sis_increments,
            ledh_no_ot_increments,
            ledh_ot_increments,
        ) = tf.while_loop(
            cond,
            body,
            loop_vars=(
                tf.constant(0, dtype=tf.int32),
                sis_particles,
                sis_log_weights,
                ledh_no_ot_particles,
                ledh_no_ot_log_weights,
                ledh_ot_particles,
                ledh_ot_log_weights,
                sis_increments,
                ledh_no_ot_increments,
                ledh_ot_increments,
            ),
            parallel_iterations=1,
            maximum_iterations=time_steps,
        )
        return {
            "sis_no_transport": tf.transpose(sis_increments.stack(), [1, 0]),
            "ledh_no_ot": tf.transpose(ledh_no_ot_increments.stack(), [1, 0]),
            "ledh_ot": tf.transpose(ledh_ot_increments.stack(), [1, 0]),
        }

    return compiled


def _summarize_arm(harness: Any, samples_by_time: Any, reference_prefix: Any) -> dict[str, Any]:
    np = harness.np
    samples = np.asarray(samples_by_time, dtype=np.float64)
    prefix_samples = np.cumsum(samples, axis=1)
    means = prefix_samples.mean(axis=0)
    sds = prefix_samples.std(axis=0, ddof=1)
    mcses = sds / math.sqrt(samples.shape[0])
    deltas = means - reference_prefix
    z_scores = np.abs(deltas) / np.maximum(mcses, 1.0e-8)
    seed_sd_units = np.abs(deltas) / np.maximum(sds, 1.0e-8)
    failure_mask = (z_scores > 2.0) & (seed_sd_units > 2.0)
    first_failure_time = None
    if np.any(failure_mask):
        first_failure_time = int(np.argmax(failure_mask))
    total_values = prefix_samples[:, -1]
    return {
        "seed_values": total_values.tolist(),
        "increment_seed_values": samples.tolist(),
        "prefix_seed_values": prefix_samples.tolist(),
        "total_mean": float(means[-1]),
        "total_sd": float(sds[-1]),
        "total_mcse": float(mcses[-1]),
        "total_delta_to_reference": float(deltas[-1]),
        "total_abs_z": float(z_scores[-1]),
        "total_abs_seed_sd_units": float(seed_sd_units[-1]),
        "increment_means": samples.mean(axis=0).tolist(),
        "prefix_means": means.tolist(),
        "prefix_sds": sds.tolist(),
        "prefix_mcses": mcses.tolist(),
        "prefix_deltas_to_reference": deltas.tolist(),
        "prefix_abs_z": z_scores.tolist(),
        "prefix_abs_seed_sd_units": seed_sd_units.tolist(),
        "first_failure_time": first_failure_time,
    }


def _run_state_dim(harness: Any, state_dim: int, *, xla: bool) -> dict[str, Any]:
    tf = harness.tf
    np = harness.np
    observations_tf = harness._observations(state_dim)
    observations_np = observations_tf.numpy().astype(np.float64)
    initial_noise, transition_noise = harness._stateless_seeded_normals_batch(state_dim)
    initial_particles = tf.sqrt(tf.constant(0.7, harness.DTYPE)) * initial_noise
    theta_batch = tf.tile(harness.THETA[None, :], [harness.SEED_COUNT, 1])
    compiled = _make_compiled_decomposition(harness, state_dim, xla=xla)
    increments = compiled(theta_batch, initial_particles, transition_noise, observations_tf)
    transition_first = _kalman_transition_first_increments(
        harness,
        state_dim,
        observations_np,
    )
    observe_initial_first = _kalman_observe_initial_first_increments(
        harness,
        state_dim,
        observations_np,
    )
    convention_probes = {
        "transition_first_total": float(np.sum(transition_first)),
        "observe_initial_first_total": float(np.sum(observe_initial_first)),
        "transition_first_prefix": np.cumsum(transition_first).tolist(),
        "observe_initial_first_prefix": np.cumsum(observe_initial_first).tolist(),
    }
    if observations_np.shape[0] > 1:
        convention_probes["transition_first_drop_first_total"] = float(
            np.sum(
                _kalman_transition_first_increments(
                    harness,
                    state_dim,
                    observations_np[1:],
                )
            )
        )
        convention_probes["transition_first_drop_last_total"] = float(
            np.sum(
                _kalman_transition_first_increments(
                    harness,
                    state_dim,
                    observations_np[:-1],
                )
            )
        )
    reference_prefix = np.cumsum(transition_first)
    arm_summaries = {
        name: _summarize_arm(harness, value.numpy(), reference_prefix)
        for name, value in increments.items()
    }
    return {
        "state_dim": state_dim,
        "kalman_reference": convention_probes,
        "arms": arm_summaries,
    }


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# LEDH-PFPF-OT LGSSM Value-Decomposition Diagnostic Result",
        "",
        f"Date: {payload['timestamp']}",
        "",
        "## Manifest",
        "",
        "| Field | Value |",
        "|---|---|",
    ]
    manifest = payload["manifest"]
    for key in (
        "num_particles",
        "seed_count",
        "time_steps",
        "xla",
        "device_scope",
        "cuda_visible_devices",
        "tf32_execution_enabled",
        "runtime_seconds",
    ):
        lines.append(f"| {key} | `{manifest.get(key)}` |")
    lines.extend(
        [
            "",
            "## Decision Table",
            "",
            "| Field | Status |",
            "|---|---|",
            f"| Decision | {payload['decision']['decision']} |",
            f"| Primary criterion | {payload['decision']['primary_criterion']} |",
            f"| Main uncertainty | {payload['decision']['main_uncertainty']} |",
            f"| Next action | {payload['decision']['next_action']} |",
            f"| Not concluded | {payload['decision']['not_concluded']} |",
            "",
            "## Arm Totals",
            "",
            "| State dim | Arm | Mean | Kalman | Delta | SD | MCSE | abs z | abs seed-SD units | First failing prefix |",
            "|---:|---|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for state in payload["states"]:
        kalman_total = state["kalman_reference"]["transition_first_total"]
        for arm_name, arm in state["arms"].items():
            lines.append(
                "| "
                f"{state['state_dim']} | {arm_name} | "
                f"{arm['total_mean']:.6f} | {kalman_total:.6f} | "
                f"{arm['total_delta_to_reference']:.6f} | "
                f"{arm['total_sd']:.6f} | {arm['total_mcse']:.6f} | "
                f"{arm['total_abs_z']:.3f} | "
                f"{arm['total_abs_seed_sd_units']:.3f} | "
                f"{arm['first_failure_time']} |"
            )
    lines.extend(["", "## Convention Probes", ""])
    for state in payload["states"]:
        probes = state["kalman_reference"]
        lines.extend(
            [
                f"State dim {state['state_dim']}:",
                "",
                f"- transition-first total: `{probes['transition_first_total']:.6f}`",
                f"- observe-initial-first total: `{probes['observe_initial_first_total']:.6f}`",
                f"- transition-first drop-first total: `{probes.get('transition_first_drop_first_total'):.6f}`",
                f"- transition-first drop-last total: `{probes.get('transition_first_drop_last_total'):.6f}`",
                "",
            ]
        )
    lines.extend(["## Interpretation", ""])
    for item in payload["interpretation"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _interpret(payload: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    items = []
    ledh_no_ot_fails = []
    ledh_ot_fails = []
    sis_fails = []
    for state in payload["states"]:
        arms = state["arms"]
        sis_fails.append(arms["sis_no_transport"]["first_failure_time"] is not None)
        ledh_no_ot_fails.append(arms["ledh_no_ot"]["first_failure_time"] is not None)
        ledh_ot_fails.append(arms["ledh_ot"]["first_failure_time"] is not None)
        items.append(
            "state_dim="
            f"{state['state_dim']}: first failures "
            f"SIS={arms['sis_no_transport']['first_failure_time']}, "
            f"LEDH-no-OT={arms['ledh_no_ot']['first_failure_time']}, "
            f"LEDH+OT={arms['ledh_ot']['first_failure_time']}."
        )
    if any(ledh_no_ot_fails):
        decision = (
            "Value gap appears before OT in the LEDH-no-OT arm; prioritize "
            "LEDH proposal density/log-det correction."
        )
        next_action = "Inspect LEDH proposal correction and per-time increment formula."
        uncertainty = "Whether OT adds additional bias after the pre-OT value issue."
    elif any(ledh_ot_fails) and not any(ledh_no_ot_fails):
        decision = (
            "Value gap appears only after OT/reset; prioritize transport/resampling "
            "semantics."
        )
        next_action = "Inspect whether OT reset preserves the marginal likelihood estimator."
        uncertainty = "Whether finite Sinkhorn epsilon or reset-to-uniform is the dominant OT effect."
    elif any(sis_fails):
        decision = "Plain SIS also fails; particle/noise/comparator setup remains suspect."
        next_action = "Recheck fixture, time indexing, and Kalman reference before LEDH-specific work."
        uncertainty = "Whether the previous no-transport SIS diagnostic was too noisy or inconsistent."
    else:
        decision = "No arm fails by the quantitative rule; evidence is ambiguous."
        next_action = "Increase seeds or sharpen tolerance before changing code."
        uncertainty = "Current seed count may be insufficient for localization."
    return (
        {
            "decision": decision,
            "primary_criterion": (
                "Failure requires abs(delta)/MCSE > 2 and abs(delta)/seed_sd > 2 "
                "at the same prefix."
            ),
            "main_uncertainty": uncertainty,
            "next_action": next_action,
            "not_concluded": (
                "No gradient correctness, SIR correctness, posterior correctness, "
                "HMC readiness, or production validity."
            ),
        },
        items,
    )


def main() -> None:
    args = _parse_args()
    _configure_import_environment(args)
    harness = _load_harness()
    tf_metadata = _configure_tensorflow(harness, args)
    start = time.perf_counter()
    states = [_run_state_dim(harness, dim, xla=args.xla) for dim in args.state_dims]
    runtime_seconds = time.perf_counter() - start
    manifest = {
        "script": str(Path(__file__).relative_to(ROOT)),
        "plan": "docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-value-decomposition-hypothesis-test-plan-2026-06-26.md",
        "source_result": "docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-kalman-n1000-xla-statistical-result-2026-06-26.md",
        "python": sys.version,
        "platform": platform.platform(),
        "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "num_particles": args.num_particles,
        "seed_count": args.seed_count,
        "time_steps": harness.TIME_STEPS,
        "state_dims": args.state_dims,
        "dtype": harness.DTYPE.name,
        "tf_version": harness.tf.__version__,
        "runtime_seconds": runtime_seconds,
        **tf_metadata,
    }
    payload = {
        "timestamp": manifest["timestamp_utc"],
        "manifest": manifest,
        "states": states,
    }
    decision, interpretation = _interpret(payload)
    payload["decision"] = decision
    payload["interpretation"] = interpretation
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    if args.markdown_output:
        _write_markdown(Path(args.markdown_output), payload)


if __name__ == "__main__":
    main()
