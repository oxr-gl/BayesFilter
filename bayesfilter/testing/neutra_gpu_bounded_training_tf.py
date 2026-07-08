"""Bounded GPU-only NeuTra optimizer-training gate for LGSSM targets.

This Phase 10 fixture runs a small affine-diagonal NeuTra-style optimizer
training loop for one admitted non-DSGE route.  It is deliberately narrower
than a full transport-training or HMC-validation workflow: no HMC, no external
sample generation, no XLA/JIT claim, and no posterior correctness claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tensorflow as tf

from bayesfilter.ssm import (
    stable_ssm_posterior_adapter_signature,
    stable_ssm_target_signature,
)
from bayesfilter.testing.lgssm_generic_target_adapter_tf import (
    make_lgssm_generic_target_fixture,
)
from bayesfilter.testing.neutra_gpu_training_preflight_tf import (
    ADMITTED_NEUTRA_GPU_PREFLIGHT_ROUTE_IDS,
    DEFERRED_NEUTRA_GPU_PREFLIGHT_ROUTE_IDS,
    LGSSM_QR_ROUTE_ID,
    MODEL_B_SVD_CUBATURE_ROUTE_ID,
    MODEL_B_SVD_UKF_ROUTE_ID,
)


NEUTRA_GPU_BOUNDED_TRAINING_NONCLAIMS = (
    "Phase 10 bounded GPU affine NeuTra optimizer-training gate only",
    "no full NeuTra training claim",
    "no dense IAF training claim",
    "no frozen transport payload promotion",
    "no external sample generation claim",
    "no HMC tuning or sampling claim",
    "no posterior convergence claim",
    "no XLA readiness claim",
    "no route ranking claim",
    "no production readiness claim",
    "no default execution readiness claim",
    "no scientific validity claim",
)

DEFAULT_PHASE10_ARTIFACT_DIR = Path(
    "docs/plans/artifacts/lgssm-first-neutra-gpu-training-2026-07-07"
)
DEFAULT_SEED = 20260707
DEFAULT_STEPS = 12
DEFAULT_BATCH_SIZE = 16
DEFAULT_LEARNING_RATE = 0.03
DEFAULT_INITIAL_RAW_SCALE = -1.3862943611198906


class NeuTraGPUBoundedTrainingError(RuntimeError):
    """Raised when the Phase 10 bounded GPU training contract is violated."""


@dataclass(frozen=True)
class NeuTraGPUBoundedTrainingConfig:
    """Configuration for Phase 10 bounded GPU-only optimizer training."""

    route_id: str = LGSSM_QR_ROUTE_ID
    seed: int = DEFAULT_SEED
    steps: int = DEFAULT_STEPS
    batch_size: int = DEFAULT_BATCH_SIZE
    learning_rate: float = DEFAULT_LEARNING_RATE
    initial_raw_scale: float = DEFAULT_INITIAL_RAW_SCALE
    device: str = "/GPU:0"
    jit_compile: bool = False
    require_gpu: bool = True
    disallow_soft_placement: bool = True
    artifact_dir: Path = DEFAULT_PHASE10_ARTIFACT_DIR

    @property
    def training_state_path(self) -> Path:
        route_slug = str(self.route_id).replace("/", "_").replace("-", "_")
        return self.artifact_dir / (
            f"{route_slug}_affine_neutra_gpu_training_state_seed{int(self.seed)}.json"
        )

    def normalized(self) -> Mapping[str, Any]:
        return {
            "schema": "bayesfilter.neutra.gpu_bounded_training_config.v1",
            "route_id": str(self.route_id),
            "seed": int(self.seed),
            "steps": int(self.steps),
            "batch_size": int(self.batch_size),
            "learning_rate": float(self.learning_rate),
            "optimizer": "tf.keras.optimizers.Adam",
            "initial_raw_scale": float(self.initial_raw_scale),
            "device": str(self.device),
            "jit_compile": bool(self.jit_compile),
            "xla_readiness_policy": (
                "phase9_xla_blocker_inherited_jit_compile_false_required"
            ),
            "require_gpu": bool(self.require_gpu),
            "disallow_soft_placement": bool(self.disallow_soft_placement),
            "artifact_dir": str(self.artifact_dir),
            "training_state_path": str(self.training_state_path),
            "training_execution_target": "gpu_required",
            "cpu_training_fallback_policy": "forbidden",
            "external_sample_generation_policy": (
                "multicore_cpu_separate_phase_not_run_here"
            ),
            "hmc_policy": "not_run_not_authorized_for_phase10",
            "full_neutra_training_executed": False,
            "bounded_optimizer_training_executed": True,
            "hmc_executed": False,
            "external_sample_generation_executed": False,
            "nonclaims": NEUTRA_GPU_BOUNDED_TRAINING_NONCLAIMS,
        }


def run_neutra_gpu_bounded_training(
    config: NeuTraGPUBoundedTrainingConfig | None = None,
) -> Mapping[str, Any]:
    """Run Phase 10 bounded optimizer training and write the state artifact."""

    cfg = NeuTraGPUBoundedTrainingConfig() if config is None else config
    start = time.monotonic()
    _validate_config(cfg)
    previous_soft_placement = tf.config.get_soft_device_placement()
    if cfg.disallow_soft_placement:
        tf.config.set_soft_device_placement(False)
    try:
        gpu_manifest = _gpu_manifest(
            require_gpu=bool(cfg.require_gpu),
            requested_device=str(cfg.device),
            jit_compile=bool(cfg.jit_compile),
        )
        payload = _train_lgssm_route(cfg, gpu_manifest=gpu_manifest)
    finally:
        tf.config.set_soft_device_placement(previous_soft_placement)

    payload = {
        **payload,
        "elapsed_seconds": time.monotonic() - start,
    }
    payload = {
        **payload,
        "artifact_hash": f"sha256:{_stable_payload_sha256(payload)}",
        "artifact_hash_semantics": "stable_json_sha256_excluding_artifact_hash_fields",
    }
    cfg.training_state_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(cfg.training_state_path, payload)
    return payload


def phase10_error_payload(
    error: BaseException,
    *,
    config: NeuTraGPUBoundedTrainingConfig,
) -> Mapping[str, Any]:
    """Build a Phase 10 blocker payload without converting failure into evidence."""

    return {
        "schema": "bayesfilter.neutra.gpu_bounded_training_state.v1",
        "phase": "phase10_bounded_gpu_neutra_training",
        "passed": False,
        "decision": "BLOCK_PHASE10_BOUNDED_GPU_NEUTRA_TRAINING",
        "config": config.normalized(),
        "error_type": type(error).__name__,
        "error_message": str(error),
        "optimizer_steps_executed": 0,
        "full_neutra_training_executed": False,
        "hmc_executed": False,
        "external_sample_generation_executed": False,
        "jit_compile": bool(config.jit_compile),
        "nonclaims": NEUTRA_GPU_BOUNDED_TRAINING_NONCLAIMS,
    }


def _train_lgssm_route(
    config: NeuTraGPUBoundedTrainingConfig,
    *,
    gpu_manifest: Mapping[str, Any],
) -> Mapping[str, Any]:
    fixture = make_lgssm_generic_target_fixture()
    adapter = fixture.adapter
    target_signature = stable_ssm_target_signature(fixture.contract)
    adapter_signature = stable_ssm_posterior_adapter_signature(adapter)
    initial_shift = tf.cast(fixture.initial_batch[0], tf.float64)
    parameter_dim = int(initial_shift.shape[0])
    if parameter_dim <= 0:
        raise NeuTraGPUBoundedTrainingError("parameter dimension must be positive")

    losses: list[float] = []
    gradient_norm_history: list[Mapping[str, float]] = []
    per_step_devices: list[Mapping[str, Any]] = []

    with tf.device(config.device):
        tf.random.set_seed(int(config.seed))
        shift = tf.Variable(initial_shift, name="phase10_lgssm_shift")
        raw_scale = tf.Variable(
            tf.fill(tf.shape(initial_shift), tf.cast(config.initial_raw_scale, tf.float64)),
            name="phase10_lgssm_raw_scale",
        )
        optimizer = tf.keras.optimizers.Adam(learning_rate=float(config.learning_rate))
        objective = tf.function(
            lambda shift_arg, raw_scale_arg, z_arg: _reverse_kl_style_loss(
                adapter,
                z_arg,
                shift=shift_arg,
                raw_scale=raw_scale_arg,
            ),
            jit_compile=bool(config.jit_compile),
        )

        for step in range(int(config.steps)):
            z = tf.random.stateless_normal(
                shape=(int(config.batch_size), parameter_dim),
                seed=tf.constant([int(config.seed), int(step)], dtype=tf.int32),
                dtype=tf.float64,
            )
            with tf.GradientTape() as tape:
                loss = objective(shift, raw_scale, z)
            gradients = tape.gradient(loss, [shift, raw_scale])
            if any(gradient is None for gradient in gradients):
                raise NeuTraGPUBoundedTrainingError("training gradient must be available")
            _require_finite_tensor(loss, "training loss")
            for name, gradient in zip(("shift", "raw_scale"), gradients):
                _require_finite_tensor(gradient, f"{name} gradient")
            optimizer.apply_gradients(zip(gradients, [shift, raw_scale]))
            _require_finite_tensor(shift, "learned shift")
            _require_finite_tensor(raw_scale, "learned raw_scale")

            loss_value = float(loss.numpy())
            losses.append(loss_value)
            gradient_norm_history.append(
                {
                    "step": int(step),
                    "shift": float(tf.linalg.global_norm([gradients[0]]).numpy()),
                    "raw_scale": float(tf.linalg.global_norm([gradients[1]]).numpy()),
                    "global": float(tf.linalg.global_norm(gradients).numpy()),
                }
            )
            per_step_devices.append(
                {
                    "step": int(step),
                    "loss": _placement(loss),
                    "z": _placement(z),
                    "shift": _placement(shift),
                    "raw_scale": _placement(raw_scale),
                    "shift_gradient": _placement(gradients[0]),
                    "raw_scale_gradient": _placement(gradients[1]),
                }
            )

    output_devices = tuple(
        str(device)
        for row in per_step_devices
        for key, device in row.items()
        if key != "step"
    )
    objective_outputs_on_gpu = all("GPU" in device.upper() for device in output_devices)
    if not objective_outputs_on_gpu:
        raise NeuTraGPUBoundedTrainingError("Phase 10 objective tensors must stay on GPU")

    optimizer_variable_devices = tuple(
        _placement(variable) for variable in getattr(optimizer, "variables", ())
    )
    if not optimizer_variable_devices:
        raise NeuTraGPUBoundedTrainingError("optimizer state must be materialized")
    finite_losses = all(_is_finite_number(item) for item in losses)
    if not finite_losses:
        raise NeuTraGPUBoundedTrainingError("loss history must be finite")
    learned_shift = tuple(float(item) for item in shift.numpy().tolist())
    learned_raw_scale = tuple(float(item) for item in raw_scale.numpy().tolist())
    payload = {
        "schema": "bayesfilter.neutra.gpu_bounded_training_state.v1",
        "phase": "phase10_bounded_gpu_neutra_training",
        "passed": True,
        "decision": "PASS_PHASE10_BOUNDED_GPU_NEUTRA_TRAINING",
        "route": {
            "route_id": LGSSM_QR_ROUTE_ID,
            "target_family": "lgssm_static_qr",
            "filter_id": "tf-qr-exact-lgssm-loglikelihood",
            "filter_backend": "tf_qr_exact_kalman",
            "status": "selected_from_phase9_admitted_routes",
        },
        "config": config.normalized(),
        "gpu_manifest": gpu_manifest,
        "target_signature": target_signature,
        "adapter_signature": adapter_signature,
        "parameter_dim": parameter_dim,
        "parameter_names": list(adapter.parameter_names),
        "initial_shift": [float(item) for item in initial_shift.numpy().tolist()],
        "initial_raw_scale": [float(config.initial_raw_scale)] * parameter_dim,
        "final_shift": list(learned_shift),
        "final_raw_scale": list(learned_raw_scale),
        "initial_loss": float(losses[0]),
        "final_loss": float(losses[-1]),
        "loss_history": [float(item) for item in losses],
        "gradient_norm_history": list(gradient_norm_history),
        "finite_checks": {
            "loss_history_finite": bool(finite_losses),
            "final_shift_finite": bool(_sequence_is_finite(learned_shift)),
            "final_raw_scale_finite": bool(_sequence_is_finite(learned_raw_scale)),
        },
        "device_checks": {
            "expected_device": str(config.device),
            "per_step_devices": per_step_devices,
            "objective_output_devices": list(output_devices),
            "all_objective_outputs_on_gpu": bool(objective_outputs_on_gpu),
            "optimizer_variable_devices": list(optimizer_variable_devices),
            "soft_device_placement": bool(tf.config.get_soft_device_placement()),
        },
        "optimizer": {
            "name": "tf.keras.optimizers.Adam",
            "learning_rate": float(config.learning_rate),
            "variable_count": len(optimizer_variable_devices),
        },
        "optimizer_steps_executed": int(config.steps),
        "full_neutra_training_executed": False,
        "bounded_optimizer_training_executed": True,
        "hmc_executed": False,
        "external_sample_generation_executed": False,
        "frozen_transport_payload_written": False,
        "training_objective": (
            "reverse_kl_style_mean_negative_log_p_forward_transport_plus_logdet"
        ),
        "loss_interpretation": "explanatory_training_diagnostic_only",
        "jit_compile": bool(config.jit_compile),
        "xla_blocker_status": {
            "phase9_xla_blocker_inherited": True,
            "phase10_jit_compile": bool(config.jit_compile),
            "xla_readiness_claimed": False,
            "blocker_artifact": (
                "docs/plans/"
                "bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-"
                "preflight-xla-blocker-2026-07-07.json"
            ),
        },
        "evidence_contract": {
            "question": (
                "Can BayesFilter run bounded GPU NeuTra optimizer training for "
                "one admitted non-DSGE route without CPU fallback, HMC, or "
                "sample generation?"
            ),
            "primary_criterion": (
                "predeclared bounded optimizer steps complete on GPU with "
                "finite loss and gradient diagnostics and a written training "
                "state artifact"
            ),
            "vetoes": (
                "missing trusted TensorFlow GPU",
                "CPU training fallback",
                "nonfinite loss or gradient",
                "non-GPU objective tensor",
                "unreviewed XLA/JIT requirement",
                "hidden HMC",
                "hidden external sample generation",
            ),
            "not_concluded": NEUTRA_GPU_BOUNDED_TRAINING_NONCLAIMS,
        },
        "phase9_inherited_route_inventory": {
            "admitted": list(ADMITTED_NEUTRA_GPU_PREFLIGHT_ROUTE_IDS),
            "deferred": list(DEFERRED_NEUTRA_GPU_PREFLIGHT_ROUTE_IDS),
        },
        "nonclaims": NEUTRA_GPU_BOUNDED_TRAINING_NONCLAIMS,
    }
    return payload


def _reverse_kl_style_loss(
    adapter: Any,
    z: tf.Tensor,
    *,
    shift: tf.Tensor,
    raw_scale: tf.Tensor,
) -> tf.Tensor:
    scale = tf.exp(raw_scale)
    theta = shift[tf.newaxis, :] + scale[tf.newaxis, :] * z
    value, _score = adapter.log_prob_and_grad(theta)
    logdet = tf.reduce_sum(raw_scale)
    loss = -tf.reduce_mean(value + logdet)
    tf.debugging.assert_all_finite(loss, "Phase 10 NeuTra training loss must be finite")
    return loss


def _gpu_manifest(
    *,
    require_gpu: bool,
    requested_device: str,
    jit_compile: bool,
) -> Mapping[str, Any]:
    physical_gpus = tf.config.list_physical_devices("GPU")
    for gpu in physical_gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            pass
    logical_gpus = tf.config.list_logical_devices("GPU")
    manifest = {
        "physical_gpus": [str(device) for device in physical_gpus],
        "physical_gpu_details": [_device_details(device) for device in physical_gpus],
        "logical_gpus": [str(device) for device in logical_gpus],
        "tensorflow_version": tf.__version__,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "unset"),
        "tf_force_gpu_allow_growth": os.environ.get("TF_FORCE_GPU_ALLOW_GROWTH", "unset"),
        "tf32_execution_enabled": bool(_tf32_execution_enabled()),
        "jit_compile": bool(jit_compile),
        "requested_device": requested_device,
        "soft_device_placement": bool(tf.config.get_soft_device_placement()),
        "trusted_gpu_context_required": True,
        "managed_trusted_execution_basis": (
            "GPU commands require trusted/escalated execution per AGENTS.md"
        ),
        "training_execution_target": "gpu_required",
        "cpu_training_fallback_policy": "forbidden",
    }
    if require_gpu and not physical_gpus:
        raise NeuTraGPUBoundedTrainingError("trusted TensorFlow GPU visibility is required")
    return manifest


def _validate_config(config: NeuTraGPUBoundedTrainingConfig) -> None:
    route_id = str(config.route_id)
    if route_id != LGSSM_QR_ROUTE_ID:
        if route_id in {MODEL_B_SVD_UKF_ROUTE_ID, MODEL_B_SVD_CUBATURE_ROUTE_ID}:
            raise NeuTraGPUBoundedTrainingError(
                "Phase 10 selects only the LGSSM QR route; simple nonlinear "
                "routes remain admitted for preflight but not this bounded run"
            )
        if route_id in set(DEFERRED_NEUTRA_GPU_PREFLIGHT_ROUTE_IDS):
            raise NeuTraGPUBoundedTrainingError(f"Phase 10 route is deferred: {route_id}")
        raise NeuTraGPUBoundedTrainingError(f"unknown Phase 10 route id: {route_id}")
    if int(config.seed) < 0:
        raise NeuTraGPUBoundedTrainingError("seed must be nonnegative")
    if int(config.steps) <= 0 or int(config.steps) > 200:
        raise NeuTraGPUBoundedTrainingError("steps must be in 1..200")
    if int(config.batch_size) <= 0 or int(config.batch_size) > 2048:
        raise NeuTraGPUBoundedTrainingError("batch_size must be in 1..2048")
    if float(config.learning_rate) <= 0.0:
        raise NeuTraGPUBoundedTrainingError("learning_rate must be positive")
    if str(config.device).upper().find("GPU") < 0:
        raise NeuTraGPUBoundedTrainingError("Phase 10 bounded training requires a GPU device")
    if bool(config.require_gpu) is not True:
        raise NeuTraGPUBoundedTrainingError("Phase 10 forbids CPU training fallback")
    if bool(config.jit_compile):
        raise NeuTraGPUBoundedTrainingError(
            "Phase 10 inherits the Phase 9 XLA blocker and requires jit_compile=false"
        )
    if os.environ.get("CUDA_VISIBLE_DEVICES") == "-1":
        raise NeuTraGPUBoundedTrainingError(
            "CUDA_VISIBLE_DEVICES=-1 is forbidden for GPU NeuTra training"
        )


def _require_finite_tensor(tensor: tf.Tensor, name: str) -> None:
    if not bool(tf.reduce_all(tf.math.is_finite(tensor)).numpy()):
        raise NeuTraGPUBoundedTrainingError(f"{name} became nonfinite")


def _placement(value: Any) -> str:
    device = getattr(value, "device", None)
    if device is not None:
        return str(device)
    handle = getattr(value, "handle", None)
    handle_device = getattr(handle, "device", None)
    if handle_device is not None:
        return str(handle_device)
    try:
        return str(tf.convert_to_tensor(value).device)
    except (TypeError, ValueError):
        return "unknown"


def _sequence_is_finite(values: Sequence[float]) -> bool:
    return all(_is_finite_number(float(item)) for item in values)


def _is_finite_number(value: float) -> bool:
    return value == value and abs(value) < float("inf")


def _tf32_execution_enabled() -> bool:
    try:
        return bool(tf.config.experimental.tensor_float_32_execution_enabled())
    except AttributeError:
        return False


def _device_details(device: Any) -> Mapping[str, Any]:
    try:
        details = tf.config.experimental.get_device_details(device)
    except (RuntimeError, ValueError):
        details = {}
    return {
        "device": str(device),
        "details": _json_safe(details),
    }


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(_json_safe(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _json_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if hasattr(value, "numpy"):
        return _json_safe(value.numpy())
    if hasattr(value, "tolist") and hasattr(value, "shape"):
        return _json_safe(value.tolist())
    if hasattr(value, "item"):
        try:
            return value.item()
        except (TypeError, ValueError):
            pass
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def _stable_payload_sha256(payload: Mapping[str, Any]) -> str:
    normalized = dict(_json_safe(payload))
    normalized.pop("artifact_hash", None)
    normalized.pop("artifact_hash_semantics", None)
    blob = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint for trusted Phase 10 GPU bounded training."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-dir", type=Path, default=DEFAULT_PHASE10_ARTIFACT_DIR)
    parser.add_argument("--route", default=LGSSM_QR_ROUTE_ID)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--learning-rate", type=float, default=DEFAULT_LEARNING_RATE)
    parser.add_argument("--initial-raw-scale", type=float, default=DEFAULT_INITIAL_RAW_SCALE)
    parser.add_argument("--device", default="/GPU:0")
    parser.add_argument(
        "--jit-compile",
        action="store_true",
        help="Rejected until the inherited Phase 9 XLA blocker is repaired.",
    )
    args = parser.parse_args(argv)
    config = NeuTraGPUBoundedTrainingConfig(
        route_id=str(args.route),
        seed=int(args.seed),
        steps=int(args.steps),
        batch_size=int(args.batch_size),
        learning_rate=float(args.learning_rate),
        initial_raw_scale=float(args.initial_raw_scale),
        device=str(args.device),
        jit_compile=bool(args.jit_compile),
        require_gpu=True,
        artifact_dir=args.artifact_dir,
    )
    try:
        payload = run_neutra_gpu_bounded_training(config)
    except BaseException as exc:
        payload = phase10_error_payload(exc, config=config)
        config.training_state_path.parent.mkdir(parents=True, exist_ok=True)
        _write_json(config.training_state_path, payload)
        print(json.dumps(_json_safe(payload), sort_keys=True))
        return 1
    print(
        json.dumps(
            {
                "passed": bool(payload["passed"]),
                "decision": payload["decision"],
                "training_state_path": str(config.training_state_path),
                "route_id": str(config.route_id),
                "steps": int(config.steps),
                "jit_compile": bool(config.jit_compile),
                "nonclaims": NEUTRA_GPU_BOUNDED_TRAINING_NONCLAIMS,
            },
            sort_keys=True,
        )
    )
    return 0 if bool(payload["passed"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
