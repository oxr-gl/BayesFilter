"""Prepare scalar SSL-LSTM filtering geometry mass handoff.

This script converts the accepted Phase 1 whitened precision into a whitened
covariance/mass candidate for a later HMC mechanics canary. It does not run HMC
and does not claim convergence, posterior correctness, or default readiness.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bayesfilter.inference.mass_matrix import covariance_from_precision  # noqa: E402


SCRIPT_NAME = "prepare_scalar_ssl_lstm_filtering_mass_handoff_2026_07_08.py"
SCHEMA_VERSION = "scalar_ssl_lstm.filtering_mass_handoff.v1"
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md"
)
SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-subplan-2026-07-08.md"
)
RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-result-2026-07-08.md"
)
DEFAULT_GEOMETRY_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json"
)
DEFAULT_JSON_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json"
)
DEFAULT_MARKDOWN_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.md"
)
NONCLAIMS = (
    "geometry-to-mass handoff artifact only",
    "not an HMC run",
    "not HMC readiness evidence",
    "not HMC convergence evidence",
    "not posterior correctness evidence",
    "not a MAP covariance claim",
    "not sampler superiority evidence",
    "not statistical ranking evidence",
    "not GPU/XLA production-readiness evidence",
    "not default-readiness evidence",
    "not Zhao-Cui source-faithfulness evidence",
)


def prepare_mass_handoff(
    geometry_payload: Mapping[str, Any],
    *,
    eigenvalue_floor: float = 1.0e-6,
    max_condition_number: float = 1.0e5,
    jitter: float = 0.0,
) -> Mapping[str, Any]:
    start = time.perf_counter()
    vetoes: list[str] = []
    decision = geometry_payload.get("decision", {})
    low_rank = geometry_payload.get("low_rank_geometry", {})
    diagnostics = low_rank.get("diagnostics", {})

    if geometry_payload.get("schema_version") != "scalar_ssl_lstm.filtering_geometry.v1":
        vetoes.append("phase1_schema_mismatch")
    if decision.get("geometry_sanity_passed") is not True:
        vetoes.append("phase1_geometry_not_passed")
    if decision.get("vetoes"):
        vetoes.append("phase1_vetoes_present")
    if low_rank.get("accepted") is not True:
        vetoes.append("phase1_low_rank_not_accepted")
    coordinate_system = diagnostics.get("coordinate_system")
    if coordinate_system != "whitened_center_plus_scale_times_z":
        vetoes.append("coordinate_system_mismatch")
    center = np.asarray(geometry_payload.get("center", {}).get("free_parameter_values"), dtype=float)
    scale = np.asarray(geometry_payload.get("target", {}).get("free_parameter_dim", []))
    scale = np.asarray(geometry_payload.get("settings", {}).get("free_parameter_scale"), dtype=float)
    precision = np.asarray(low_rank.get("precision"), dtype=float)
    reported_covariance = np.asarray(low_rank.get("covariance"), dtype=float)
    if center.shape != (4,):
        vetoes.append("center_shape_mismatch")
    if scale.shape != (4,) or not np.all(scale > 0.0):
        vetoes.append("scale_shape_or_value_mismatch")
    if precision.shape != (4, 4):
        vetoes.append("precision_shape_mismatch")
    if reported_covariance.shape != (4, 4):
        vetoes.append("covariance_shape_mismatch")
    if not vetoes:
        try:
            mass = covariance_from_precision(
                precision,
                source="phase1_low_rank_whitened_precision",
                jitter=float(jitter),
                eigenvalue_floor=float(eigenvalue_floor),
                max_condition_number=float(max_condition_number),
                dense=True,
            )
            mass_covariance = np.asarray(mass.covariance, dtype=float)
            regularized_precision = np.asarray(mass.regularized_precision, dtype=float)
            reconstruction_error = float(
                np.max(np.abs(regularized_precision @ mass_covariance - np.eye(precision.shape[0])))
            )
            reported_covariance_error = float(
                np.max(np.abs(mass_covariance - reported_covariance))
            )
        except Exception as exc:  # noqa: BLE001 - fail-closed artifact path.
            vetoes.append(f"mass_conversion_exception:{type(exc).__name__}")
            mass = None
            mass_covariance = None
            regularized_precision = None
            reconstruction_error = None
            reported_covariance_error = None
    else:
        mass = None
        mass_covariance = None
        regularized_precision = None
        reconstruction_error = None
        reported_covariance_error = None

    if mass is not None:
        if not mass.precision_eigen_summary.get("positive", False):
            vetoes.append("regularized_precision_not_spd")
        if not mass.covariance_eigen_summary.get("positive", False):
            vetoes.append("mass_covariance_not_spd")
        if float(mass.precision_eigen_summary["condition_number"]) > float(max_condition_number) * (1.0 + 1.0e-8):
            vetoes.append("regularized_precision_condition_above_cap")
        if reconstruction_error is None or reconstruction_error > 1.0e-8:
            vetoes.append("precision_covariance_reconstruction_failed")

    passed = bool(not vetoes)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "artifact_role": "cpu_hidden_scalar_filtering_geometry_mass_handoff",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "script": f"docs/benchmarks/{SCRIPT_NAME}",
        "plan_path": PLAN_PATH,
        "subplan_path": SUBPLAN_PATH,
        "result_path": RESULT_PATH,
        "source_geometry_artifact": geometry_payload.get("script"),
        "classification": "extension_or_invention",
        "coordinate_contract": {
            "coordinate_system": "whitened_center_plus_scale_times_z",
            "theta_from_z": "theta = center + scale * z",
            "center_role": geometry_payload.get("center", {}).get("position_role"),
            "scale": scale,
            "free_parameter_names": geometry_payload.get("target", {}).get("free_parameter_names"),
            "free_parameter_indices": geometry_payload.get("target", {}).get("free_parameter_indices"),
            "refined_center_used": False,
            "refined_center_reason": (
                "phase1_center_refinement_rejected; mass handoff uses declared center"
            ),
        },
        "matrix_convention": {
            "K_z": "whitened precision from Phase 1 low-rank geometry",
            "M_z": "whitened covariance/mass candidate equal to inv(regularized K_z)",
            "hmc_handoff_matrix": "M_z",
            "inverse_mass_for_formula": "K_z",
            "original_coordinate_mass": "not used for handoff",
        },
        "regularization_policy": {
            "jitter": float(jitter),
            "eigenvalue_floor": float(eigenvalue_floor),
            "max_condition_number": float(max_condition_number),
            "helper": "bayesfilter.inference.mass_matrix.covariance_from_precision",
        },
        "source_geometry_summary": {
            "geometry_sanity_passed": decision.get("geometry_sanity_passed"),
            "phase1_vetoes": decision.get("vetoes"),
            "center_score_norm": geometry_payload.get("center", {}).get("score_norm"),
            "center_refinement": diagnostics.get("center_refinement"),
            "phase1_precision_eigen_summary": low_rank.get("precision_eigen_summary"),
            "phase1_covariance_eigen_summary": low_rank.get("covariance_eigen_summary"),
        },
        "mass_handoff": {
            "regularized_precision_K_z": regularized_precision,
            "mass_covariance_M_z": mass_covariance,
            "factor": None if mass_covariance is None else np.linalg.cholesky(mass_covariance),
            "regularization_report": None if mass is None else mass.regularization_report,
            "precision_eigen_summary": None if mass is None else mass.precision_eigen_summary,
            "mass_covariance_eigen_summary": None if mass is None else mass.covariance_eigen_summary,
            "precision_covariance_identity_max_abs_error": reconstruction_error,
            "reported_covariance_max_abs_error": reported_covariance_error,
        },
        "decision": {
            "mass_handoff_passed": passed,
            "vetoes": tuple(vetoes),
            "viable_for_phase3_mechanics_canary": passed,
            "next_justified_action": (
                "draft HMC mechanics canary subplan"
                if passed
                else "repair mass handoff before any HMC mechanics"
            ),
        },
        "metric_roles": {
            "mass_handoff_passed": "primary_phase2_pass_fail",
            "regularized_precision_spd": "promotion_veto",
            "mass_covariance_spd": "promotion_veto",
            "condition_number": "promotion_veto",
            "reconstruction_error": "promotion_veto",
            "center_score_norm": "explanatory_only",
            "center_refinement": "boundary_guard_explanatory",
        },
        "inference_status": {
            "hard_veto_screen": "passed" if passed else "failed",
            "statistically_supported_ranking": "none; single mass handoff target",
            "default_readiness": "not assessed",
            "hmc_readiness": "not assessed; Phase 2 does not run HMC",
            "next_evidence_needed": "HMC mechanics canary only if mass_handoff_passed is true",
        },
        "run_manifest": {
            "command": (
                "env CUDA_VISIBLE_DEVICES=-1 python "
                "docs/benchmarks/prepare_scalar_ssl_lstm_filtering_mass_handoff_2026_07_08.py"
            ),
            "conda_env": os.environ.get("CONDA_DEFAULT_ENV", "N/A"),
            "cpu_gpu_status": "CPU-hidden debug/reference exception",
            "wall_time_seconds": float(time.perf_counter() - start),
            "plan_file": PLAN_PATH,
            "subplan_file": SUBPLAN_PATH,
            "result_file": RESULT_PATH,
        },
        "nonclaims": NONCLAIMS,
    }
    return json_ready(payload)


def render_markdown(payload: Mapping[str, Any]) -> str:
    decision = payload["decision"]
    handoff = payload["mass_handoff"]
    lines = [
        "# Scalar SSL-LSTM Filtering Mass Handoff - 2026-07-08",
        "",
        "## Decision",
        "",
        f"- mass_handoff_passed: `{decision['mass_handoff_passed']}`",
        f"- vetoes: `{decision['vetoes']}`",
        f"- next_justified_action: {decision['next_justified_action']}",
        "",
        "## Matrix Convention",
        "",
        "- `K_z`: whitened precision from Phase 1.",
        "- `M_z`: whitened covariance/mass candidate, `inv(K_z)` after regularization.",
        "- HMC handoff matrix: `M_z`.",
        "",
        "## Eigen Summaries",
        "",
        f"- precision: `{handoff.get('precision_eigen_summary')}`",
        f"- mass covariance: `{handoff.get('mass_covariance_eigen_summary')}`",
        "",
        "## Nonclaims",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["nonclaims"])
    lines.append("")
    return "\n".join(lines)


def write_artifacts(
    payload: Mapping[str, Any],
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--geometry-json", type=Path, default=DEFAULT_GEOMETRY_PATH)
    parser.add_argument("--json-path", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--markdown-path", type=Path, default=DEFAULT_MARKDOWN_PATH)
    parser.add_argument("--eigenvalue-floor", type=float, default=1.0e-6)
    parser.add_argument("--max-condition-number", type=float, default=1.0e5)
    parser.add_argument("--jitter", type=float, default=0.0)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    geometry = json.loads(Path(args.geometry_json).read_text(encoding="utf-8"))
    payload = prepare_mass_handoff(
        geometry,
        eigenvalue_floor=float(args.eigenvalue_floor),
        max_condition_number=float(args.max_condition_number),
        jitter=float(args.jitter),
    )
    write_artifacts(
        payload,
        json_path=Path(args.json_path),
        markdown_path=Path(args.markdown_path),
    )
    print(json.dumps(payload["decision"], sort_keys=True))
    return 0 if payload["decision"]["mass_handoff_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
