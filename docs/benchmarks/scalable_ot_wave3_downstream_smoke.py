"""Wave 3 downstream smoke diagnostics for two Wave 2 OT candidates."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


_PRE = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
_PRE.add_argument("--device-scope", choices=("cpu", "visible"), default="cpu")
_PRE.add_argument("--cuda-visible-devices", default=None)
_PRE_ARGS, _ = _PRE.parse_known_args()
if _PRE_ARGS.cuda_visible_devices is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = _PRE_ARGS.cuda_visible_devices
elif _PRE_ARGS.device_scope == "cpu":
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
import tensorflow as tf  # noqa: E402

from docs.benchmarks.scalable_ot_candidate_result_schema import validate_candidate_result  # noqa: E402
from experiments.dpf_implementation.tf_tfp.resampling.low_rank_coupling_solver_tf import (  # noqa: E402
    low_rank_coupling_solver_resample_tf,
)
from experiments.dpf_implementation.tf_tfp.resampling.positive_feature_transport_tf import (  # noqa: E402
    positive_feature_transport_resample_tf,
)


DTYPE = tf.float64
WAVE3_ARTIFACT_AUDIT_PASS = "WAVE3_ARTIFACT_AUDIT_PASSED"
WAVE3_SMOKE_PASS = "WAVE3_DOWNSTREAM_SMOKE_PASSED_NO_RANKING"
WAVE3_FAIL = "WAVE3_DOWNSTREAM_SMOKE_FAILED_HARD_VETO"
WAVE2_LOW_RANK_JSON = Path("docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.json")
WAVE2_POSITIVE_JSON = Path("docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.json")
NONCLAIMS = (
    "Wave 3 downstream smoke diagnostics only",
    "no ranking claim",
    "no speedup claim",
    "no production default change",
    "no posterior correctness claim",
    "no HMC readiness claim",
    "no public API readiness claim",
    "no dense Sinkhorn equivalence claim",
    "no broad scalable-OT selection claim",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--mode", choices=("artifact-audit", "smoke"), default="smoke")
    parser.add_argument("--low-rank-json", default=str(WAVE2_LOW_RANK_JSON))
    parser.add_argument("--positive-feature-json", default=str(WAVE2_POSITIVE_JSON))
    parser.add_argument("--low-rank-rank", type=int, default=3)
    parser.add_argument("--low-rank-assignment-epsilon", type=float, default=0.45)
    parser.add_argument("--positive-feature-count", type=int, default=128)
    parser.add_argument("--epsilon", type=float, default=0.5)
    parser.add_argument("--device", default="/CPU:0")
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default=_PRE_ARGS.device_scope)
    parser.add_argument("--cuda-visible-devices", default=_PRE_ARGS.cuda_visible_devices)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    if args.low_rank_rank <= 0:
        raise ValueError("low_rank_rank must be positive")
    if args.low_rank_assignment_epsilon <= 0.0:
        raise ValueError("low_rank_assignment_epsilon must be positive")
    if args.positive_feature_count <= 0:
        raise ValueError("positive_feature_count must be positive")
    if args.epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    return args


def _git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _fixture_tiny_manual() -> tuple[np.ndarray, np.ndarray]:
    particles = np.array(
        [[[-0.40, 0.10, 0.00], [-0.15, -0.20, 0.05], [0.10, 0.18, -0.10], [0.35, -0.02, 0.15], [0.60, 0.12, -0.05]]],
        dtype=np.float64,
    )
    weights = np.array([[0.10, 0.16, 0.22, 0.25, 0.27]], dtype=np.float64)
    return particles, np.log(weights)


def _fixture_wider_state() -> tuple[np.ndarray, np.ndarray]:
    particles = np.array(
        [
            [
                [-0.50, 0.10, 0.20, -0.10],
                [-0.30, -0.15, 0.05, 0.00],
                [-0.05, 0.20, -0.05, 0.15],
                [0.18, -0.08, 0.12, -0.20],
                [0.42, 0.04, -0.18, 0.08],
                [0.70, 0.18, 0.02, -0.04],
            ]
        ],
        dtype=np.float64,
    )
    weights = np.array([[0.08, 0.12, 0.17, 0.19, 0.21, 0.23]], dtype=np.float64)
    return particles, np.log(weights)


def _fixtures() -> dict[str, tuple[np.ndarray, np.ndarray]]:
    return {
        "tiny_manual_common": _fixture_tiny_manual(),
        "wider_state_common": _fixture_wider_state(),
    }


def _artifact_audit(low_rank_path: Path, positive_path: Path) -> dict[str, Any]:
    hard_vetoes: list[str] = []
    artifacts = {}
    for lane, path, expected_status, expected_kind in (
        ("low_rank_coupling", low_rank_path, "LOW_RANK_COUPLING_VALIDATION_PASSED_DIAGNOSTIC_ONLY", "low_rank_coupling_factors"),
        ("positive_feature", positive_path, "POSITIVE_FEATURE_SINKHORN_PASSED_DIAGNOSTIC_ONLY", "kernel_factors"),
    ):
        if not path.exists():
            hard_vetoes.append(f"{lane}:missing_json")
            artifacts[lane] = {"path": str(path), "exists": False}
            continue
        data = _load_json(path)
        record = data.get("candidate_record")
        if not isinstance(record, dict):
            hard_vetoes.append(f"{lane}:missing_candidate_record")
            schema_warnings: list[str] = []
        else:
            try:
                schema_warnings = validate_candidate_result(record)
            except Exception as exc:  # noqa: BLE001
                hard_vetoes.append(f"{lane}:schema_validation_failed:{type(exc).__name__}")
                schema_warnings = []
        wave2_status = data.get("wave2_status")
        if wave2_status != expected_status:
            hard_vetoes.append(f"{lane}:unexpected_wave2_status")
        if data.get("hard_vetoes") != []:
            hard_vetoes.append(f"{lane}:wave2_hard_vetoes_not_empty")
        transport = (record or {}).get("transport_object", {}) if isinstance(record, dict) else {}
        if transport.get("kind") != expected_kind:
            hard_vetoes.append(f"{lane}:unexpected_transport_kind")
        if transport.get("materialized") is not False:
            hard_vetoes.append(f"{lane}:transport_should_be_nonmaterialized")
        artifacts[lane] = {
            "path": str(path),
            "exists": True,
            "status": data.get("status"),
            "wave2_status": wave2_status,
            "hard_vetoes": data.get("hard_vetoes"),
            "candidate_id": (record or {}).get("candidate_id") if isinstance(record, dict) else None,
            "semantic_class": (record or {}).get("semantic_class") if isinstance(record, dict) else None,
            "source_route": (record or {}).get("source_route") if isinstance(record, dict) else None,
            "transport_kind": transport.get("kind"),
            "transport_materialized": transport.get("materialized"),
            "schema_warnings": schema_warnings,
        }
    return {
        "artifact_audit_pass": not hard_vetoes,
        "artifact_hard_vetoes": hard_vetoes,
        "artifacts": artifacts,
    }


def _moment_diagnostics(input_particles: tf.Tensor, output_particles: tf.Tensor) -> dict[str, float]:
    input_mean = tf.reduce_mean(input_particles, axis=1)
    output_mean = tf.reduce_mean(output_particles, axis=1)
    input_var = tf.math.reduce_variance(input_particles, axis=1)
    output_var = tf.math.reduce_variance(output_particles, axis=1)
    mean_delta = tf.reduce_max(tf.abs(output_mean - input_mean))
    var_delta = tf.reduce_max(tf.abs(output_var - input_var))
    max_abs_particle = tf.reduce_max(tf.abs(output_particles))
    return {
        "max_mean_delta_from_input_explanatory": float(mean_delta.numpy()),
        "max_variance_delta_from_input_explanatory": float(var_delta.numpy()),
        "max_abs_output_particle_explanatory": float(max_abs_particle.numpy()),
    }


def _run_candidate(
    candidate: str,
    particles_np: np.ndarray,
    log_weights_np: np.ndarray,
    args: argparse.Namespace,
) -> dict[str, Any]:
    particles = tf.constant(particles_np, dtype=DTYPE)
    log_weights = tf.constant(log_weights_np, dtype=DTYPE)
    start = time.perf_counter()
    with tf.device(args.device):
        if candidate == "low_rank_coupling":
            result = low_rank_coupling_solver_resample_tf(
                particles,
                log_weights,
                rank=min(args.low_rank_rank, int(particles_np.shape[1])),
                assignment_epsilon=args.low_rank_assignment_epsilon,
            )
            residual_keys = {
                "max_factor_marginal_residual": result.diagnostics["max_factor_marginal_residual"],
                "max_induced_row_residual": result.diagnostics["max_induced_row_residual"],
                "max_induced_column_residual": result.diagnostics["max_induced_column_residual"],
            }
            finite_object = bool(result.diagnostics["finite_factors"])
            sign_object = bool(result.diagnostics["nonnegative_factors"]) and bool(result.diagnostics["positive_g"])
            transport_kind = "low_rank_coupling_factors"
        elif candidate == "positive_feature":
            result = positive_feature_transport_resample_tf(
                particles,
                log_weights,
                num_features=args.positive_feature_count,
                epsilon=args.epsilon,
            )
            residual_keys = {
                "max_row_residual": result.diagnostics["max_row_residual"],
                "max_column_residual": result.diagnostics["max_column_residual"],
            }
            finite_object = bool(result.diagnostics["finite_features"])
            sign_object = bool(result.diagnostics["positive_features"])
            transport_kind = "kernel_factors"
        else:
            raise ValueError(f"unknown candidate: {candidate}")
    wall_time = time.perf_counter() - start
    output = tf.convert_to_tensor(result.particles, dtype=DTYPE)
    logw = tf.convert_to_tensor(result.log_weights, dtype=DTYPE)
    log_weight_norm = tf.reduce_max(tf.abs(tf.reduce_logsumexp(logw, axis=-1))).numpy()
    finite_particles = bool(tf.reduce_all(tf.math.is_finite(output)).numpy())
    shape_match = output.shape == particles.shape
    hard_vetoes = []
    if not finite_particles:
        hard_vetoes.append("nonfinite_transported_particles")
    if not finite_object:
        hard_vetoes.append("nonfinite_transport_object_factors")
    if not sign_object:
        hard_vetoes.append("transport_object_sign_veto")
    if not shape_match:
        hard_vetoes.append("transported_particle_shape_mismatch")
    if float(log_weight_norm) > 1.0e-10:
        hard_vetoes.append("log_weight_normalization_veto")
    diagnostics = {
        **residual_keys,
        **_moment_diagnostics(particles, output),
        "wall_time_seconds_explanatory": wall_time,
        "log_weight_normalization_residual": float(log_weight_norm),
    }
    return {
        "candidate": candidate,
        "transport_kind": transport_kind,
        "validity_pass": not hard_vetoes,
        "hard_vetoes": hard_vetoes,
        "particles_shape": output.shape.as_list(),
        "finite_particles": finite_particles,
        "finite_transport_object": finite_object,
        "sign_check_pass": sign_object,
        "diagnostics": diagnostics,
    }


def build_result(args: argparse.Namespace) -> dict[str, Any]:
    low_rank_path = Path(args.low_rank_json)
    positive_path = Path(args.positive_feature_json)
    audit = _artifact_audit(low_rank_path, positive_path)
    all_hard_vetoes = list(audit["artifact_hard_vetoes"])
    rows: list[dict[str, Any]] = []
    if args.mode == "smoke" and audit["artifact_audit_pass"]:
        for fixture_name, (particles_np, log_weights_np) in _fixtures().items():
            for candidate in ("low_rank_coupling", "positive_feature"):
                row = _run_candidate(candidate, particles_np, log_weights_np, args)
                row["fixture"] = fixture_name
                rows.append(row)
                all_hard_vetoes.extend(f"{fixture_name}:{candidate}:{veto}" for veto in row["hard_vetoes"])
    elif args.mode == "smoke":
        all_hard_vetoes.append("artifact_audit_failed_before_smoke")
    status = "PASS" if not all_hard_vetoes else "FAIL"
    wave3_status = WAVE3_ARTIFACT_AUDIT_PASS if args.mode == "artifact-audit" and status == "PASS" else (
        WAVE3_SMOKE_PASS if status == "PASS" else WAVE3_FAIL
    )
    summary = {
        "num_rows": len(rows),
        "num_hard_vetoes": len(all_hard_vetoes),
        "max_mean_delta_from_input_explanatory": max(
            [row["diagnostics"]["max_mean_delta_from_input_explanatory"] for row in rows] or [0.0]
        ),
        "max_variance_delta_from_input_explanatory": max(
            [row["diagnostics"]["max_variance_delta_from_input_explanatory"] for row in rows] or [0.0]
        ),
        "max_wall_time_seconds_explanatory": max(
            [row["diagnostics"]["wall_time_seconds_explanatory"] for row in rows] or [0.0]
        ),
    }
    return {
        "status": status,
        "wave3_status": wave3_status,
        "mode": args.mode,
        "hard_vetoes": all_hard_vetoes,
        "artifact_audit": audit,
        "summary": summary,
        "rows": rows,
        "settings": {
            "low_rank_rank": args.low_rank_rank,
            "low_rank_assignment_epsilon": args.low_rank_assignment_epsilon,
            "positive_feature_count": args.positive_feature_count,
            "epsilon": args.epsilon,
        },
        "manifest": {
            "git_commit": _git_commit(),
            "timestamp_utc": _dt.datetime.now(tz=_dt.UTC).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "tensorflow_version": tf.__version__,
            "device_scope": args.device_scope,
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "device": args.device,
            "command": "scalable_ot_wave3_downstream_smoke.py",
            "plan_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-master-program-2026-06-19.md",
        },
        "nonclaims": list(NONCLAIMS),
    }


def _write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Wave 3 Downstream Smoke Diagnostics",
        "",
        f"- Mode: `{result['mode']}`",
        f"- Status: `{result['status']}`",
        f"- Wave 3 status: `{result['wave3_status']}`",
        f"- Hard vetoes: `{result['hard_vetoes']}`",
        "",
        "## Artifact Audit",
        "",
        f"- Artifact audit pass: `{result['artifact_audit']['artifact_audit_pass']}`",
        f"- Artifact hard vetoes: `{result['artifact_audit']['artifact_hard_vetoes']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value | Role |",
        "| --- | ---: | --- |",
        f"| num rows | `{result['summary']['num_rows']}` | hard-veto context |",
        f"| num hard vetoes | `{result['summary']['num_hard_vetoes']}` | hard veto |",
        f"| max mean delta from input | `{result['summary']['max_mean_delta_from_input_explanatory']:.6e}` | explanatory |",
        f"| max variance delta from input | `{result['summary']['max_variance_delta_from_input_explanatory']:.6e}` | explanatory |",
        f"| max wall time seconds | `{result['summary']['max_wall_time_seconds_explanatory']:.6e}` | explanatory |",
    ]
    if result["rows"]:
        lines.extend(
            [
                "",
                "## Rows",
                "",
                "| Fixture | Candidate | Valid | Hard vetoes | Transport kind | Mean delta, explanatory | Variance delta, explanatory |",
                "| --- | --- | --- | --- | --- | ---: | ---: |",
            ]
        )
        for row in result["rows"]:
            lines.append(
                "| {fixture} | {candidate} | `{valid}` | `{vetoes}` | `{kind}` | `{mean:.6e}` | `{var:.6e}` |".format(
                    fixture=row["fixture"],
                    candidate=row["candidate"],
                    valid=row["validity_pass"],
                    vetoes=row["hard_vetoes"],
                    kind=row["transport_kind"],
                    mean=row["diagnostics"]["max_mean_delta_from_input_explanatory"],
                    var=row["diagnostics"]["max_variance_delta_from_input_explanatory"],
                )
            )
    lines.extend(["", "## Non-Claims", ""])
    for nonclaim in result["nonclaims"]:
        lines.append(f"- {nonclaim}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = _parse_args()
    result = build_result(args)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(_json_ready(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown = Path(args.markdown_output)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    _write_markdown(result, markdown)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
