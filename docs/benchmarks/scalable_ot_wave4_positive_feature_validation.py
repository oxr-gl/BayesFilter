"""Wave 4 positive-feature downstream validation diagnostics.

This harness is a current-agent lane artifact.  It tests the positive-feature
transport as a resampling-step candidate by comparing uniform estimates after
transport with exact weighted estimates before transport on deterministic
seeded fixtures.  It does not rank algorithms or assess posterior correctness.
"""

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
from experiments.dpf_implementation.tf_tfp.resampling.positive_feature_transport_tf import (  # noqa: E402
    positive_feature_transport_resample_tf,
)


DTYPE = tf.float64
LANE_ID = "current_agent_positive_feature"
CANDIDATE_ID = "positive_feature_sinkhorn"
WAVE4_POSITIVE_PASS = "WAVE4_POSITIVE_FEATURE_VALIDATION_PASSED_HARD_SCREEN_NO_RANKING"
WAVE4_POSITIVE_FAIL = "WAVE4_POSITIVE_FEATURE_VALIDATION_FAILED_HARD_SCREEN"
WAVE2_POSITIVE_JSON = Path("docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.json")
WAVE3_SMOKE_JSON = Path("docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.json")
PLAN_PATH = "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p02-current-positive-feature-validation-subplan-2026-06-20.md"
RESULT_PATH = "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-positive-feature-result-2026-06-20.md"

DEFAULT_SEEDS = (101, 202, 303)
SMOKE_SEEDS = (101,)
SMOKE_FIXTURES = ("weighted_curve",)
FULL_FIXTURES = ("weighted_curve", "bimodal_tail", "high_dim_low_rank")

LOG_WEIGHT_NORM_THRESHOLD = 1.0e-10
RESIDUAL_THRESHOLD = 5.0e-2
MEAN_ERROR_THRESHOLD = 3.0e-1
SECOND_MOMENT_ERROR_THRESHOLD = 1.0

NONCLAIMS = (
    "Wave 4 positive-feature lane hard screen only",
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
    parser.add_argument("--mode", choices=("smoke", "full"), default="full")
    parser.add_argument("--seeds", default=",".join(str(seed) for seed in DEFAULT_SEEDS))
    parser.add_argument("--num-features", type=int, default=128)
    parser.add_argument("--epsilon", type=float, default=0.5)
    parser.add_argument("--max-iterations", type=int, default=160)
    parser.add_argument("--convergence-threshold", type=float, default=1.0e-4)
    parser.add_argument("--device", default="/CPU:0")
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default=_PRE_ARGS.device_scope)
    parser.add_argument("--cuda-visible-devices", default=_PRE_ARGS.cuda_visible_devices)
    parser.add_argument("--plan-path", default=PLAN_PATH)
    parser.add_argument("--result-path", default=RESULT_PATH)
    parser.add_argument("--program-id", default="wave4_positive_feature_validation")
    parser.add_argument("--pass-status", default=WAVE4_POSITIVE_PASS)
    parser.add_argument("--fail-status", default=WAVE4_POSITIVE_FAIL)
    parser.add_argument("--report-title", default="Wave 4 Positive-Feature Validation")
    parser.add_argument(
        "--next-evidence-needed",
        default="peer lane result and final merge before any larger validation decision",
    )
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    if args.num_features <= 0:
        raise ValueError("num_features must be positive")
    if args.epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if args.max_iterations <= 0:
        raise ValueError("max_iterations must be positive")
    if args.convergence_threshold <= 0.0:
        raise ValueError("convergence_threshold must be positive")
    _parse_seeds(args.seeds)
    return args


def _parse_seeds(raw: str) -> list[int]:
    seeds = [int(part.strip()) for part in raw.split(",") if part.strip()]
    if not seeds:
        raise ValueError("at least one seed is required")
    return seeds


def _git_commit() -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return completed.stdout.strip()


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


def _entry_audit() -> dict[str, Any]:
    hard_vetoes: list[str] = []
    records: dict[str, Any] = {}
    if not WAVE2_POSITIVE_JSON.exists():
        hard_vetoes.append("wave2_positive_json_missing")
        records["wave2_positive"] = {"exists": False, "path": str(WAVE2_POSITIVE_JSON)}
    else:
        data = _load_json(WAVE2_POSITIVE_JSON)
        record = data.get("candidate_record")
        schema_warnings: list[str] = []
        if not isinstance(record, dict):
            hard_vetoes.append("wave2_positive_candidate_record_missing")
        else:
            try:
                schema_warnings = validate_candidate_result(record)
            except Exception as exc:  # noqa: BLE001
                hard_vetoes.append(f"wave2_positive_schema_error:{type(exc).__name__}")
        if data.get("wave2_status") != "POSITIVE_FEATURE_SINKHORN_PASSED_DIAGNOSTIC_ONLY":
            hard_vetoes.append("wave2_positive_unexpected_status")
        if data.get("hard_vetoes") != []:
            hard_vetoes.append("wave2_positive_prior_hard_vetoes")
        records["wave2_positive"] = {
            "exists": True,
            "path": str(WAVE2_POSITIVE_JSON),
            "wave2_status": data.get("wave2_status"),
            "hard_vetoes": data.get("hard_vetoes"),
            "schema_warnings": schema_warnings,
        }
    if not WAVE3_SMOKE_JSON.exists():
        hard_vetoes.append("wave3_smoke_json_missing")
        records["wave3_smoke"] = {"exists": False, "path": str(WAVE3_SMOKE_JSON)}
    else:
        data = _load_json(WAVE3_SMOKE_JSON)
        if data.get("wave3_status") != "WAVE3_DOWNSTREAM_SMOKE_PASSED_NO_RANKING":
            hard_vetoes.append("wave3_smoke_unexpected_status")
        if data.get("hard_vetoes") != []:
            hard_vetoes.append("wave3_prior_hard_vetoes")
        records["wave3_smoke"] = {
            "exists": True,
            "path": str(WAVE3_SMOKE_JSON),
            "wave3_status": data.get("wave3_status"),
            "hard_vetoes": data.get("hard_vetoes"),
        }
    return {
        "entry_audit_pass": not hard_vetoes,
        "entry_hard_vetoes": hard_vetoes,
        "records": records,
    }


def _normalized_log_weights(raw: np.ndarray) -> np.ndarray:
    shifted = raw - np.max(raw, axis=1, keepdims=True)
    weights = np.exp(shifted)
    weights = weights / np.sum(weights, axis=1, keepdims=True)
    return np.log(weights)


def _weighted_curve(seed: int) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    rng = np.random.default_rng(seed)
    num_particles, state_dim = 16, 4
    t = np.linspace(-1.0, 1.0, num_particles, dtype=np.float64)
    phase = 0.05 * (seed % 11)
    particles = np.stack(
        [
            t,
            np.sin(1.4 * np.pi * t + phase),
            np.cos(0.9 * np.pi * t - phase),
            0.5 * t * t + 0.03 * rng.normal(size=num_particles),
        ],
        axis=1,
    )
    raw = (0.65 * t + 0.25 * np.sin(2.0 * np.pi * t + phase))[None, :]
    return particles[None, :, :], _normalized_log_weights(raw), {
        "fixture": "weighted_curve",
        "seed": seed,
        "num_particles": num_particles,
        "state_dim": state_dim,
        "seeded_pseudorandom_terms": "small fourth-coordinate perturbation",
    }


def _bimodal_tail(seed: int) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    rng = np.random.default_rng(seed + 1000)
    num_particles, state_dim = 20, 6
    cluster = np.where(np.arange(num_particles) < num_particles // 2, -1.0, 1.0)
    base = rng.normal(scale=0.08, size=(num_particles, state_dim))
    directions = np.linspace(0.2, 1.1, state_dim, dtype=np.float64)
    particles = base + cluster[:, None] * directions[None, :]
    particles[:, 0] += np.linspace(-0.4, 0.4, num_particles)
    particles[:, 3] += 0.2 * np.sin(np.linspace(0.0, 2.0 * np.pi, num_particles))
    raw = (0.8 * cluster + 0.05 * np.arange(num_particles, dtype=np.float64))[None, :]
    return particles[None, :, :], _normalized_log_weights(raw), {
        "fixture": "bimodal_tail",
        "seed": seed,
        "num_particles": num_particles,
        "state_dim": state_dim,
        "seeded_pseudorandom_terms": "small clustered Gaussian perturbation",
    }


def _high_dim_low_rank(seed: int) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    rng = np.random.default_rng(seed + 2000)
    num_particles, state_dim, latent_dim = 24, 12, 3
    t = np.linspace(-1.0, 1.0, num_particles, dtype=np.float64)
    latent = np.stack(
        [
            t,
            np.sin(1.1 * np.pi * t + 0.03 * (seed % 17)),
            np.cos(0.7 * np.pi * t) - np.mean(np.cos(0.7 * np.pi * t)),
        ],
        axis=1,
    )
    basis_raw = rng.normal(size=(state_dim, latent_dim))
    basis, _ = np.linalg.qr(basis_raw)
    particles = latent @ basis[:, :latent_dim].T
    particles += 0.025 * rng.normal(size=(num_particles, state_dim))
    raw = (-0.35 * t + 0.18 * latent[:, 1] - 0.07 * latent[:, 2])[None, :]
    return particles[None, :, :], _normalized_log_weights(raw), {
        "fixture": "high_dim_low_rank",
        "seed": seed,
        "num_particles": num_particles,
        "state_dim": state_dim,
        "latent_dim": latent_dim,
        "seeded_pseudorandom_terms": "orthonormal basis and small noise",
    }


def _make_fixture(name: str, seed: int) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    if name == "weighted_curve":
        return _weighted_curve(seed)
    if name == "bimodal_tail":
        return _bimodal_tail(seed)
    if name == "high_dim_low_rank":
        return _high_dim_low_rank(seed)
    raise ValueError(f"unknown fixture: {name}")


def _weighted_stats(particles: np.ndarray, log_weights: np.ndarray) -> dict[str, np.ndarray]:
    weights = np.exp(log_weights)
    mean = np.sum(weights[:, :, None] * particles, axis=1)
    second = np.sum(weights[:, :, None] * particles * particles, axis=1)
    return {"mean": mean, "second_moment": second}


def _uniform_stats(particles: np.ndarray) -> dict[str, np.ndarray]:
    return {
        "mean": np.mean(particles, axis=1),
        "second_moment": np.mean(particles * particles, axis=1),
    }


def _max_abs_delta(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.max(np.abs(left - right)))


def _row(
    fixture_name: str,
    seed: int,
    particles_np: np.ndarray,
    log_weights_np: np.ndarray,
    fixture_summary: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    particles = tf.constant(particles_np, dtype=DTYPE)
    log_weights = tf.constant(log_weights_np, dtype=DTYPE)
    start = time.perf_counter()
    with tf.device(args.device):
        result = positive_feature_transport_resample_tf(
            particles,
            log_weights,
            num_features=args.num_features,
            epsilon=args.epsilon,
            max_iterations=args.max_iterations,
            convergence_threshold=args.convergence_threshold,
        )
    wall_time = time.perf_counter() - start
    output = tf.convert_to_tensor(result.particles, dtype=DTYPE)
    output_log_weights = tf.convert_to_tensor(result.log_weights, dtype=DTYPE)
    weighted_ref = _weighted_stats(particles_np, log_weights_np)
    candidate_stats = _uniform_stats(output.numpy())
    naive_stats = _uniform_stats(particles_np)
    candidate_mean_error = _max_abs_delta(candidate_stats["mean"], weighted_ref["mean"])
    candidate_second_error = _max_abs_delta(candidate_stats["second_moment"], weighted_ref["second_moment"])
    naive_mean_error = _max_abs_delta(naive_stats["mean"], weighted_ref["mean"])
    naive_second_error = _max_abs_delta(naive_stats["second_moment"], weighted_ref["second_moment"])
    log_norm = float(tf.reduce_max(tf.abs(tf.reduce_logsumexp(output_log_weights, axis=-1))).numpy())
    finite_particles = bool(tf.reduce_all(tf.math.is_finite(output)).numpy())
    shape_match = output.shape == particles.shape
    diagnostics = dict(result.diagnostics)
    max_residual = max(float(diagnostics["max_row_residual"]), float(diagnostics["max_column_residual"]))
    hard_vetoes = []
    if not finite_particles or not bool(diagnostics["finite_particles"]):
        hard_vetoes.append("nonfinite_transported_particles")
    if not bool(diagnostics["finite_features"]):
        hard_vetoes.append("nonfinite_feature_or_scaling_object")
    if not bool(diagnostics["positive_features"]):
        hard_vetoes.append("nonpositive_features")
    if not shape_match:
        hard_vetoes.append("transported_particle_shape_mismatch")
    if log_norm > LOG_WEIGHT_NORM_THRESHOLD:
        hard_vetoes.append("log_weight_normalization_veto")
    if max_residual > RESIDUAL_THRESHOLD:
        hard_vetoes.append("transport_residual_threshold_veto")
    if candidate_mean_error > MEAN_ERROR_THRESHOLD:
        hard_vetoes.append("weighted_mean_screen_veto")
    if candidate_second_error > SECOND_MOMENT_ERROR_THRESHOLD:
        hard_vetoes.append("weighted_second_moment_screen_veto")
    return {
        "fixture": fixture_name,
        "seed": seed,
        "lane_id": LANE_ID,
        "candidate_id": CANDIDATE_ID,
        "validity_pass": not hard_vetoes,
        "hard_vetoes": hard_vetoes,
        "fixture_summary": fixture_summary,
        "particles_shape": output.shape.as_list(),
        "finite_particles": finite_particles,
        "shape_match": bool(shape_match),
        "log_weight_normalization_residual": log_norm,
        "candidate_weighted_mean_error": candidate_mean_error,
        "candidate_weighted_second_moment_error": candidate_second_error,
        "naive_uniform_mean_error_explanatory": naive_mean_error,
        "naive_uniform_second_moment_error_explanatory": naive_second_error,
        "candidate_minus_naive_mean_error_explanatory": candidate_mean_error - naive_mean_error,
        "candidate_minus_naive_second_moment_error_explanatory": candidate_second_error - naive_second_error,
        "wall_time_seconds_explanatory": wall_time,
        "transport_diagnostics": {
            "finite_features": bool(diagnostics["finite_features"]),
            "positive_features": bool(diagnostics["positive_features"]),
            "max_row_residual": float(diagnostics["max_row_residual"]),
            "max_column_residual": float(diagnostics["max_column_residual"]),
            "iterations_used": int(diagnostics["iterations_used"]),
            "transport_object_kind": diagnostics["transport_object_kind"],
            "transport_matrix_materialized": bool(diagnostics["transport_matrix_materialized"]),
        },
    }


def build_result(args: argparse.Namespace) -> dict[str, Any]:
    build_start = time.perf_counter()
    entry = _entry_audit()
    all_hard_vetoes = list(entry["entry_hard_vetoes"])
    rows: list[dict[str, Any]] = []
    fixtures = SMOKE_FIXTURES if args.mode == "smoke" else FULL_FIXTURES
    seeds = SMOKE_SEEDS if args.mode == "smoke" else _parse_seeds(args.seeds)
    if entry["entry_audit_pass"]:
        for fixture_name in fixtures:
            for seed in seeds:
                particles_np, log_weights_np, fixture_summary = _make_fixture(fixture_name, seed)
                row = _row(fixture_name, seed, particles_np, log_weights_np, fixture_summary, args)
                rows.append(row)
                all_hard_vetoes.extend(f"{fixture_name}:seed{seed}:{veto}" for veto in row["hard_vetoes"])
    else:
        all_hard_vetoes.append("entry_audit_failed_before_validation")
    status = "PASS" if not all_hard_vetoes else "FAIL"
    max_candidate_mean = max([row["candidate_weighted_mean_error"] for row in rows] or [0.0])
    max_candidate_second = max([row["candidate_weighted_second_moment_error"] for row in rows] or [0.0])
    max_residual = max(
        [
            max(
                row["transport_diagnostics"]["max_row_residual"],
                row["transport_diagnostics"]["max_column_residual"],
            )
            for row in rows
        ]
        or [0.0]
    )
    summary = {
        "num_rows": len(rows),
        "num_hard_vetoes": len(all_hard_vetoes),
        "max_candidate_weighted_mean_error": max_candidate_mean,
        "max_candidate_weighted_second_moment_error": max_candidate_second,
        "max_transport_residual": max_residual,
        "max_wall_time_seconds_explanatory": max([row["wall_time_seconds_explanatory"] for row in rows] or [0.0]),
        "ranking_statistically_supported": False,
        "viable_for_later_validation": status == "PASS",
    }
    total_wall_time = time.perf_counter() - build_start
    program_status = args.pass_status if status == "PASS" else args.fail_status
    return {
        "status": status,
        "wave4_status": WAVE4_POSITIVE_PASS if status == "PASS" else WAVE4_POSITIVE_FAIL,
        "program_id": str(args.program_id),
        "program_status": str(program_status),
        "report_title": str(args.report_title),
        "mode": args.mode,
        "lane_id": LANE_ID,
        "candidate_id": CANDIDATE_ID,
        "hard_vetoes": all_hard_vetoes,
        "entry_audit": entry,
        "settings": {
            "fixtures": list(fixtures),
            "seeds": list(seeds),
            "num_features": int(args.num_features),
            "epsilon": float(args.epsilon),
            "max_iterations": int(args.max_iterations),
            "convergence_threshold": float(args.convergence_threshold),
            "thresholds": {
                "log_weight_normalization": LOG_WEIGHT_NORM_THRESHOLD,
                "transport_residual": RESIDUAL_THRESHOLD,
                "weighted_mean_error": MEAN_ERROR_THRESHOLD,
                "weighted_second_moment_error": SECOND_MOMENT_ERROR_THRESHOLD,
            },
        },
        "summary": summary,
        "rows": rows,
        "inference_status": {
            "hard_veto_screen": "passed" if status == "PASS" else "failed",
            "statistically_supported_ranking": "none",
            "descriptive_only_differences": [
                "naive uniform estimator errors",
                "candidate minus naive deltas",
                "wall time",
                "per-seed tables",
            ],
            "default_readiness": "not assessed",
            "next_evidence_needed": str(args.next_evidence_needed),
        },
        "evidence_contract": {
            "question": "Does the positive-feature lane remain viable under replicated downstream resampling screens?",
            "baseline_comparator": "exact weighted input estimates; naive uniform-no-transport is explanatory only",
            "primary_pass_criterion": "empty hard vetoes across entry audit, transport validity, residual, and moment screens",
            "ranking_rule": "no ranking in current lane",
        },
        "manifest": {
            "git_commit": _git_commit(),
            "timestamp_utc": _dt.datetime.now(tz=_dt.UTC).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "tensorflow_version": tf.__version__,
            "program_id": str(args.program_id),
            "device_scope": args.device_scope,
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "device": args.device,
            "command": " ".join(sys.argv),
            "argv": list(sys.argv),
            "plan_path": str(args.plan_path),
            "result_path": str(args.result_path),
            "json_output_path": str(args.output),
            "markdown_output_path": str(args.markdown_output),
            "fixtures": list(fixtures),
            "seeds": list(seeds),
            "total_wall_time_seconds": total_wall_time,
            "cpu_only_note": "CUDA_VISIBLE_DEVICES=-1 hides GPU devices for deliberate CPU-scoped diagnostics when device_scope=cpu",
        },
        "nonclaims": list(NONCLAIMS),
    }


def _write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        f"# {result['report_title']}",
        "",
        f"- Status: `{result['status']}`",
        f"- Program status: `{result['program_status']}`",
        f"- Wave 4 status: `{result['wave4_status']}`",
        f"- Lane: `{result['lane_id']}`",
        f"- Candidate: `{result['candidate_id']}`",
        f"- Hard vetoes: `{result['hard_vetoes']}`",
        "",
        "## Evidence Contract",
        "",
        "| Field | Value |",
        "| --- | --- |",
    ]
    for key, value in result["evidence_contract"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Value | Role |",
            "| --- | ---: | --- |",
            f"| rows | `{result['summary']['num_rows']}` | hard-veto context |",
            f"| hard vetoes | `{result['summary']['num_hard_vetoes']}` | hard veto |",
            f"| max candidate weighted mean error | `{result['summary']['max_candidate_weighted_mean_error']:.6e}` | hard veto |",
            f"| max candidate weighted second moment error | `{result['summary']['max_candidate_weighted_second_moment_error']:.6e}` | hard veto |",
            f"| max transport residual | `{result['summary']['max_transport_residual']:.6e}` | hard veto |",
            f"| max wall time seconds | `{result['summary']['max_wall_time_seconds_explanatory']:.6e}` | explanatory |",
            f"| ranking statistically supported | `{result['summary']['ranking_statistically_supported']}` | inference status |",
            "",
            "## Rows",
            "",
            "| Fixture | Seed | Valid | Hard vetoes | Mean error | Second moment error | Naive mean error | Naive second error | Max residual |",
            "| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in result["rows"]:
        max_residual = max(
            row["transport_diagnostics"]["max_row_residual"],
            row["transport_diagnostics"]["max_column_residual"],
        )
        lines.append(
            "| {fixture} | `{seed}` | `{valid}` | `{vetoes}` | `{mean:.6e}` | `{second:.6e}` | `{naive_mean:.6e}` | `{naive_second:.6e}` | `{residual:.6e}` |".format(
                fixture=row["fixture"],
                seed=row["seed"],
                valid=row["validity_pass"],
                vetoes=row["hard_vetoes"],
                mean=row["candidate_weighted_mean_error"],
                second=row["candidate_weighted_second_moment_error"],
                naive_mean=row["naive_uniform_mean_error_explanatory"],
                naive_second=row["naive_uniform_second_moment_error_explanatory"],
                residual=max_residual,
            )
        )
    lines.extend(
        [
            "",
            "## Inference Status",
            "",
            "| Evidence class | Status |",
            "| --- | --- |",
        ]
    )
    for key, value in result["inference_status"].items():
        lines.append(f"| {key} | `{value}` |")
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
