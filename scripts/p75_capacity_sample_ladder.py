#!/usr/bin/env python
"""Phase 10 bounded P75 capacity/sample/prefit ladder.

This runner is a small diagnostic wrapper around
``p75_stochastic_density_training_pilot.py``.  It is not the large pilot, does
not run validation/HMC/scaling, and does not provide lower-gate repair
evidence.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Mapping

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp")

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import scripts.p75_stochastic_density_training_pilot as pilot


DEFAULT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p75-capacity-sample-ladder-2026-06-18.json"
)
PHASE10_SUBPLAN = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-subplan-2026-06-18.md"
)
MASTER_PROGRAM = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md"
)
RUNBOOK = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md"
)
COMMAND_PREFIX = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    "scripts/p75_capacity_sample_ladder.py"
)

DEFAULT_LADDER_ROWS: tuple[Mapping[str, int], ...] = (
    {
        "row_id": 1,
        "degree": 1,
        "rank": 1,
        "batch_size": 32,
        "batches": 2,
        "prefit_steps": 0,
        "seed": 7501,
    },
    {
        "row_id": 2,
        "degree": 1,
        "rank": 1,
        "batch_size": 32,
        "batches": 2,
        "prefit_steps": 5,
        "seed": 7501,
    },
    {
        "row_id": 3,
        "degree": 1,
        "rank": 2,
        "batch_size": 64,
        "batches": 2,
        "prefit_steps": 10,
        "seed": 7502,
    },
    {
        "row_id": 4,
        "degree": 2,
        "rank": 1,
        "batch_size": 32,
        "batches": 4,
        "prefit_steps": 5,
        "seed": 7503,
    },
    {
        "row_id": 5,
        "degree": 2,
        "rank": 2,
        "batch_size": 64,
        "batches": 4,
        "prefit_steps": 10,
        "seed": 7504,
    },
)


def _jsonable(value: Any) -> Any:
    if hasattr(value, "numpy"):
        return _jsonable(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, float):
        if math.isnan(value):
            return "nan"
        if math.isinf(value):
            return "inf" if value > 0.0 else "-inf"
        return value
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return str(value)


def _write_payload(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n")


def _as_float(value: Any) -> float:
    if hasattr(value, "numpy"):
        return float(value.numpy())
    return float(value)


def _contains_nonfinite_marker(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(_contains_nonfinite_marker(item) for item in value.values())
    if isinstance(value, (tuple, list)):
        return any(_contains_nonfinite_marker(item) for item in value)
    if isinstance(value, float):
        return not math.isfinite(value)
    if isinstance(value, str):
        return value.lower() in {"nan", "inf", "-inf"}
    return False


def _holdout_rms(payload: Mapping[str, Any], mode: str) -> float:
    return _as_float(
        payload["arms"][mode]["target_pilot"]["fresh_audit"]["holdout"][
            "rms_relative"
        ]
    )


def _line_rms(payload: Mapping[str, Any], mode: str) -> float:
    return _as_float(
        payload["arms"][mode]["target_pilot"]["fresh_audit"]["line_gate"][
            "line_residual_rms"
        ]
    )


def _same_draws_ok(payload: Mapping[str, Any]) -> bool:
    policy = payload.get("same_draws_policy", {})
    required = (
        "anchor_reused_for_all_arms",
        "training_batches_reused_for_all_arms",
        "audit_seeds_reused_for_all_arms",
        "audit_data_not_used_for_initialization",
    )
    return all(bool(policy.get(key)) for key in required)


def _provenance_ok(payload: Mapping[str, Any]) -> bool:
    source = payload["arms"][pilot.P75_SOURCE_GUIDED_PREFIT_INIT_MODE][
        "target_pilot"
    ]
    init = source["initialization"]
    prefit = init["prefit"]
    training_seed_policy = source["training_seed_policy"]
    audit_seed_policy = source["fresh_audit"]["audit_seed_policy"]
    return (
        bool(_same_draws_ok(payload))
        and bool(init.get("uses_audit_data") is False)
        and bool(prefit.get("uses_audit_data") is False)
        and bool(training_seed_policy.get("prefit_and_density_training_batches_disjoint"))
        and bool(audit_seed_policy.get("not_training_seeds"))
    )


def classify_ladder_row(row: Mapping[str, int], payload: Mapping[str, Any]) -> Mapping[str, Any]:
    """Classify one Phase 10 row under the frozen mechanism criterion."""
    prefit_steps = int(row["prefit_steps"])
    requested_batches = int(row["batches"])
    arms = payload["arms"]
    completed_batches = {
        mode: int(arm["target_pilot"]["completed_batches"])
        for mode, arm in arms.items()
    }
    mechanics_pass = all(value == requested_batches for value in completed_batches.values())
    same_draws_ok = _same_draws_ok(payload)
    nonfinite = _contains_nonfinite_marker(payload)
    classification: dict[str, Any] = {
        "row_id": int(row["row_id"]),
        "prefit_steps": prefit_steps,
        "completed_batches_by_arm": completed_batches,
        "mechanics_pass": mechanics_pass,
        "same_draws_ok": same_draws_ok,
        "nonfinite_detected": nonfinite,
        "criterion": (
            "mechanism_win requires finite declared steps, provenance "
            "separation, >=10 percent holdout RMS-relative improvement over "
            "calibrated_constant, and <=10 percent audit-line RMS worsening"
        ),
    }
    if prefit_steps == 0:
        return {
            **classification,
            "status": "baseline_only",
            "mechanism_win": False,
            "reason": "prefit_steps_0_calibrated_constant_reference_row",
            "calibrated_constant_holdout_rms_relative": _holdout_rms(
                payload, pilot.P75_CALIBRATED_CONSTANT_INIT_MODE
            ),
            "calibrated_constant_line_residual_rms": _line_rms(
                payload, pilot.P75_CALIBRATED_CONSTANT_INIT_MODE
            ),
        }
    prefit_init = arms[pilot.P75_SOURCE_GUIDED_PREFIT_INIT_MODE]["target_pilot"][
        "initialization"
    ]["prefit"]
    prefit_completed = int(prefit_init["completed_steps"]) == prefit_steps
    provenance_ok = _provenance_ok(payload)
    calibrated_holdout = _holdout_rms(payload, pilot.P75_CALIBRATED_CONSTANT_INIT_MODE)
    source_holdout = _holdout_rms(payload, pilot.P75_SOURCE_GUIDED_PREFIT_INIT_MODE)
    calibrated_line = _line_rms(payload, pilot.P75_CALIBRATED_CONSTANT_INIT_MODE)
    source_line = _line_rms(payload, pilot.P75_SOURCE_GUIDED_PREFIT_INIT_MODE)
    holdout_relative_ratio = source_holdout / max(calibrated_holdout, 1e-300)
    line_relative_ratio = source_line / max(calibrated_line, 1e-300)
    holdout_improved_10pct = holdout_relative_ratio <= 0.9
    line_not_worse_10pct = line_relative_ratio <= 1.1
    mechanism_win = (
        mechanics_pass
        and same_draws_ok
        and not nonfinite
        and prefit_completed
        and provenance_ok
        and holdout_improved_10pct
        and line_not_worse_10pct
    )
    reasons = []
    if not mechanics_pass:
        reasons.append("declared_density_batches_incomplete")
    if not same_draws_ok:
        reasons.append("same_draws_policy_failed")
    if nonfinite:
        reasons.append("nonfinite_payload_value")
    if not prefit_completed:
        reasons.append("prefit_steps_incomplete")
    if not provenance_ok:
        reasons.append("provenance_separation_failed")
    if not holdout_improved_10pct:
        reasons.append("holdout_improvement_less_than_10_percent")
    if not line_not_worse_10pct:
        reasons.append("audit_line_worse_by_more_than_10_percent")
    return {
        **classification,
        "status": "mechanism_win" if mechanism_win else "mechanism_loss",
        "mechanism_win": mechanism_win,
        "reasons": reasons,
        "prefit_completed_requested_steps": prefit_completed,
        "provenance_ok": provenance_ok,
        "calibrated_constant_holdout_rms_relative": calibrated_holdout,
        "source_guided_prefit_holdout_rms_relative": source_holdout,
        "holdout_relative_ratio": holdout_relative_ratio,
        "holdout_improved_at_least_10_percent": holdout_improved_10pct,
        "calibrated_constant_line_residual_rms": calibrated_line,
        "source_guided_prefit_line_residual_rms": source_line,
        "line_relative_ratio": line_relative_ratio,
        "audit_line_not_worse_by_more_than_10_percent": line_not_worse_10pct,
    }


def _run_one_row(
    row: Mapping[str, int],
    *,
    output: Path,
    max_seconds_per_row: float,
) -> Mapping[str, Any]:
    include_prefit = int(row["prefit_steps"]) > 0
    row_start = time.monotonic()
    pilot.RUN_START = row_start
    command = (
        f"{COMMAND_PREFIX} --output {output} "
        f"--max-seconds-per-row {float(max_seconds_per_row)}"
    )
    payload = pilot.compare_init_modes_payload(
        output,
        command,
        degree=int(row["degree"]),
        rank=int(row["rank"]),
        batch_size=int(row["batch_size"]),
        batches=int(row["batches"]),
        max_seconds=float(max_seconds_per_row),
        seed=int(row["seed"]),
        include_source_guided_prefit=include_prefit,
        prefit_steps=int(row["prefit_steps"]),
    )
    classification = classify_ladder_row(row, payload)
    elapsed = time.monotonic() - row_start
    return {
        "row_spec": dict(row),
        "elapsed_seconds": round(elapsed, 3),
        "arm_count": len(payload["arms"]),
        "classification": classification,
        "payload": payload,
    }


def ladder_payload(output: Path, *, max_seconds_per_row: float) -> Mapping[str, Any]:
    if len(DEFAULT_LADDER_ROWS) > 16:
        raise ValueError("Phase 10 row limit exceeded")
    target_pilot_arm_count = sum(
        3 if int(row["prefit_steps"]) > 0 else 2 for row in DEFAULT_LADDER_ROWS
    )
    if target_pilot_arm_count > 16:
        raise ValueError("Phase 10 target-pilot arm limit exceeded")
    rows = [
        _run_one_row(row, output=output, max_seconds_per_row=max_seconds_per_row)
        for row in DEFAULT_LADDER_ROWS
    ]
    classifications = [row["classification"] for row in rows]
    mechanism_rows = [item for item in classifications if item["prefit_steps"] > 0]
    wins = [item for item in mechanism_rows if item["mechanism_win"]]
    same_draws_ok = all(item["same_draws_ok"] for item in classifications)
    nonfinite_detected = any(item["nonfinite_detected"] for item in classifications)
    mechanics_pass = all(item["mechanics_pass"] for item in classifications)
    overall_status = (
        "block"
        if nonfinite_detected or not same_draws_ok
        else "diagnostic_completed"
    )
    return {
        "metadata_date": "2026-06-18",
        "status": "P75_PHASE10_CAPACITY_SAMPLE_LADDER_COMPLETED",
        "master_program": MASTER_PROGRAM,
        "runbook": RUNBOOK,
        "subplan": PHASE10_SUBPLAN,
        "diagnostic_scope": "p75_phase10_bounded_ladder_not_validation",
        "run_manifest": {
            "command": (
                f"{COMMAND_PREFIX} --output {output} "
                f"--max-seconds-per-row {float(max_seconds_per_row)}"
            ),
            "output": str(output),
            "script": "scripts/p75_capacity_sample_ladder.py",
            "cpu_gpu_status": (
                "cpu_only_cuda_visible_devices_minus_1"
                if os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
                else "not_cpu_hidden"
            ),
            "environment": {
                "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
                "MPLCONFIGDIR": os.environ.get("MPLCONFIGDIR"),
            },
            "git_state": pilot._git_state_summary(),
            "max_seconds_per_row": float(max_seconds_per_row),
        },
        "bounds": {
            "degree_values": sorted({int(row["degree"]) for row in DEFAULT_LADDER_ROWS}),
            "rank_values": sorted({int(row["rank"]) for row in DEFAULT_LADDER_ROWS}),
            "batch_size_values": sorted({int(row["batch_size"]) for row in DEFAULT_LADDER_ROWS}),
            "density_batch_values": sorted({int(row["batches"]) for row in DEFAULT_LADDER_ROWS}),
            "prefit_step_values": sorted({int(row["prefit_steps"]) for row in DEFAULT_LADDER_ROWS}),
            "row_count": len(DEFAULT_LADDER_ROWS),
            "target_pilot_arm_count": target_pilot_arm_count,
            "row_limit": 16,
            "target_pilot_arm_limit": 16,
            "large_pilot_forbidden": True,
            "degree_2_rank_4_batch_1024_batches_500_executed": False,
            "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        },
        "evidence_contract": {
            "question": (
                "Does a small increase in degree, rank, batch size, density "
                "batches, or prefit steps make source-guided prefit materially "
                "improve fresh diagnostics relative to calibrated constant?"
            ),
            "baseline": "calibrated_constant arm within the same row",
            "primary_row_win": (
                "source_guided_prefit improves holdout RMS-relative by at "
                "least 10 percent and does not worsen audit-line RMS by more "
                "than 10 percent"
            ),
            "vetoes": (
                "audit leakage, nonfinite terms, same-draw mismatch, "
                "lower-gate/validation/HMC/scaling/source-faithfulness "
                "overclaim, large-pilot launch"
            ),
            "nonclaims": pilot.P75_NONCLAIMS
            + (
                "Phase 10 ladder is not lower-gate repair evidence",
                "Phase 10 ladder is not validation or HMC readiness evidence",
                "Phase 10 ladder does not authorize the large pilot",
            ),
        },
        "rows": rows,
        "decision_summary": {
            "overall_status": overall_status,
            "mechanism_row_count": len(mechanism_rows),
            "mechanism_win_count": len(wins),
            "mechanism_loss_count": len(mechanism_rows) - len(wins),
            "baseline_only_count": len(classifications) - len(mechanism_rows),
            "same_draws_ok": same_draws_ok,
            "mechanics_pass": mechanics_pass,
            "nonfinite_detected": nonfinite_detected,
            "large_pilot_executed": False,
            "lower_gate_repair_claimed": False,
            "validation_or_hmc_claimed": False,
            "next_action": "write_phase10_result_and_phase11_handoff",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-seconds-per-row", type=float, default=180.0)
    args = parser.parse_args(argv)
    if float(args.max_seconds_per_row) > 180.0:
        parser.error("--max-seconds-per-row must be <= 180.0 for Phase 10")
    payload = ladder_payload(args.output, max_seconds_per_row=args.max_seconds_per_row)
    _write_payload(args.output, payload)
    print(
        json.dumps(
            {
                "p75_status": payload["status"],
                "decision_summary": _jsonable(payload["decision_summary"]),
            },
            sort_keys=True,
        )
    )
    return 0 if payload["decision_summary"]["overall_status"] != "block" else 1


if __name__ == "__main__":
    raise SystemExit(main())
