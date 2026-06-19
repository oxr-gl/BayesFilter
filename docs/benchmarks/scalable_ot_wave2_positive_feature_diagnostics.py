"""Wave 2 diagnostics for the positive-feature Sinkhorn route."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import platform
import subprocess
import sys
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

from docs.benchmarks.scalable_ot_candidate_result_schema import (  # noqa: E402
    CandidateResultRecord,
    TransportObjectRecord,
    validate_candidate_result,
)
from docs.benchmarks.scalable_ot_p05_positive_feature_prototype_diagnostics import (  # noqa: E402
    _build_result as _build_phase5_result,
    _json_ready,
)


WAVE2_STATUS_PASS = "POSITIVE_FEATURE_SINKHORN_PASSED_DIAGNOSTIC_ONLY"
WAVE2_STATUS_FAIL = "POSITIVE_FEATURE_SINKHORN_FAILED_HARD_VETO"
BASELINE_COMPARATOR = "phase1_dense_streaming_baseline_context_only_not_promotion"
NONCLAIMS = (
    "Wave 2 current-agent positive-feature Sinkhorn diagnostics only",
    "semantic replacement unless a separate approximation contract is reviewed",
    "no dense Gibbs equivalence claim",
    "no speedup claim",
    "no ranking claim",
    "no production default change",
    "no posterior correctness claim",
    "no HMC readiness claim",
    "no public API readiness claim",
    "no broad scalable-OT selection claim",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--epsilon", type=float, default=0.5)
    parser.add_argument("--baseline-scaling", type=float, default=0.9)
    parser.add_argument("--baseline-convergence-threshold", type=float, default=1.0e-3)
    parser.add_argument("--baseline-max-iterations", type=int, default=12)
    parser.add_argument("--feature-max-iterations", type=int, default=120)
    parser.add_argument("--feature-convergence-threshold", type=float, default=1.0e-4)
    parser.add_argument("--denominator-floor", type=float, default=1.0e-30)
    parser.add_argument("--num-features", type=int, default=128)
    parser.add_argument("--device", default="/CPU:0")
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default=_PRE_ARGS.device_scope)
    parser.add_argument("--cuda-visible-devices", default=_PRE_ARGS.cuda_visible_devices)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    if args.epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if args.num_features <= 0:
        raise ValueError("num_features must be positive")
    if args.baseline_max_iterations <= 0 or args.feature_max_iterations <= 0:
        raise ValueError("iteration counts must be positive")
    if args.denominator_floor <= 0.0:
        raise ValueError("denominator_floor must be positive")
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


def build_wave2_positive_feature_result(args: argparse.Namespace | None = None) -> dict[str, Any]:
    if args is None:
        args = argparse.Namespace(
            epsilon=0.5,
            baseline_scaling=0.9,
            baseline_convergence_threshold=1.0e-3,
            baseline_max_iterations=12,
            feature_max_iterations=120,
            feature_convergence_threshold=1.0e-4,
            denominator_floor=1.0e-30,
            num_features=128,
            device="/CPU:0",
            device_scope=_PRE_ARGS.device_scope,
            cuda_visible_devices=_PRE_ARGS.cuda_visible_devices,
        )
    phase5 = _build_phase5_result(args)
    hard_vetoes = list(phase5["hard_vetoes"])
    validity_pass = bool(phase5["validity_pass"]) and not hard_vetoes
    wave2_status = WAVE2_STATUS_PASS if validity_pass else WAVE2_STATUS_FAIL
    status = "PASS" if validity_pass else "FAIL"
    phase5_record = phase5["candidate_record"]
    transport = phase5_record["transport_object"]
    manifest = {
        "git_commit": _git_commit(),
        "timestamp_utc": _dt.datetime.now(tz=_dt.UTC).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "device_scope": args.device_scope,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "device": args.device,
        "command": "scalable_ot_wave2_positive_feature_diagnostics.py",
        "plan_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-master-program-2026-06-19.md",
        "phase5_replay_command": "scalable_ot_p05_positive_feature_prototype_diagnostics.py",
    }
    result: dict[str, Any] = {
        "status": status,
        "wave2_status": wave2_status,
        "owner": "current_agent",
        "algorithm_family": "positive_feature_sinkhorn_route",
        "entry_context_status": phase5["phase5_status"],
        "validity_pass": validity_pass,
        "semantic_class": "semantic_replacement",
        "source_status": "source_locked",
        "source_route": phase5_record["source_route"],
        "hard_vetoes": hard_vetoes,
        "summary": phase5["summary"],
        "thresholds": phase5["thresholds"],
        "settings": phase5["settings"],
        "source_route_components": phase5["source_route_components"],
        "fixtures": phase5["fixtures"],
        "phase5_replay_status": phase5["status"],
        "phase5_candidate_record": phase5_record,
        "manifest": manifest,
        "nonclaims": list(NONCLAIMS),
    }
    candidate_record = CandidateResultRecord(
        candidate_id="wave2_positive_feature_sinkhorn_diagnostic",
        source_status="source_locked",
        semantic_class="semantic_replacement",
        source_route=phase5_record["source_route"],
        baseline_comparator=BASELINE_COMPARATOR,
        transport_object=TransportObjectRecord(
            kind=transport["kind"],
            materialized=transport["materialized"],
            shape=transport.get("shape"),
            factor_shapes=dict(transport.get("factor_shapes", {})),
            not_materialized_reason=transport.get("not_materialized_reason"),
            orientation=transport.get("orientation", "source_rows_target_columns"),
            semantic_output="semantic_replacement_feature_kernel_particles",
        ),
        diagnostics={
            "wave2_status": wave2_status,
            "entry_context_status": phase5["phase5_status"],
            "hard_vetoes": hard_vetoes,
            "validity_pass": validity_pass,
            "max_row_residual": phase5["summary"]["max_row_residual"],
            "max_column_residual": phase5["summary"]["max_column_residual"],
            "max_dense_reference_particle_error_explanatory": phase5["summary"][
                "max_dense_reference_particle_error_explanatory"
            ],
            "max_dense_reference_rms_error_explanatory": phase5["summary"][
                "max_dense_reference_rms_error_explanatory"
            ],
            "algorithm_complete_lane": "current_agent_positive_feature_sinkhorn",
            "source_route_components": phase5["source_route_components"],
        },
        diagnostic_roles={
            "wave2_status": "hard_veto",
            "hard_vetoes": "continuation_veto",
            "validity_pass": "hard_veto",
            "max_row_residual": "hard_veto",
            "max_column_residual": "hard_veto",
            "max_dense_reference_particle_error_explanatory": "explanatory",
            "max_dense_reference_rms_error_explanatory": "explanatory",
            "algorithm_complete_lane": "explanatory",
            "source_route_components": "explanatory",
        },
        execution_manifest=manifest,
        nonclaims=list(NONCLAIMS),
    ).to_dict()
    validate_candidate_result(candidate_record)
    result["candidate_record"] = candidate_record
    return result


def _write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Wave 2 Positive-Feature Sinkhorn Diagnostics",
        "",
        f"- Status: `{result['status']}`",
        f"- Wave 2 status: `{result['wave2_status']}`",
        f"- Owner: `{result['owner']}`",
        f"- Semantic class: `{result['semantic_class']}`",
        f"- Validity pass: `{result['validity_pass']}`",
        f"- Hard vetoes: `{result['hard_vetoes']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| max row residual | `{result['summary']['max_row_residual']:.6e}` |",
        f"| max column residual | `{result['summary']['max_column_residual']:.6e}` |",
        f"| max dense-reference particle error, explanatory | `{result['summary']['max_dense_reference_particle_error_explanatory']:.6e}` |",
        f"| max dense-reference RMS error, explanatory | `{result['summary']['max_dense_reference_rms_error_explanatory']:.6e}` |",
        "",
        "## Fixture Rows",
        "",
        "| Fixture | Features | Valid | Row residual | Column residual | Max dense error, explanatory | RMS dense error, explanatory |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for fixture_name, fixture in result["fixtures"].items():
        row = fixture["positive_feature"]
        lines.append(
            "| {fixture} | {features} | `{valid}` | `{row_res:.6e}` | `{col_res:.6e}` | `{max_err:.6e}` | `{rms_err:.6e}` |".format(
                fixture=fixture_name,
                features=row["num_features"],
                valid=row["validity_pass"],
                row_res=row["max_row_residual"],
                col_res=row["max_column_residual"],
                max_err=row["dense_reference_max_abs_particle_error_explanatory"],
                rms_err=row["dense_reference_rms_particle_error_explanatory"],
            )
        )
    lines.extend(["", "## Non-Claims", ""])
    for nonclaim in result["nonclaims"]:
        lines.append(f"- {nonclaim}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = _parse_args()
    result = build_wave2_positive_feature_result(args)
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
