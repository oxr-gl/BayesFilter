#!/usr/bin/env python
"""P71 Phase 3 finite numeric evaluator probe for the author SIR d=18 route."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tensorflow as tf

import bayesfilter.highdim as highdim


PASS_STATUS = "PASS_P71_PHASE3_NUMERIC_EVALUATOR_VALUE_FINITE"
BLOCK_STATUS = "BLOCK_P71_PHASE3_NUMERIC_EVALUATOR_VALUE_FINITE"

DEFAULT_PHASE2_ARTIFACT = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-"
    "2026-06-16.json"
)
EXPECTED_PHASE2_ROW_ADEQUACY_STATUS = "diagnostic_only_below_preferred_rows"


def _jsonable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_jsonable(item) for item in value]
    if hasattr(value, "numpy"):
        array = value.numpy()
        if getattr(array, "shape", ()) == ():
            return _jsonable(array.item())
        return _jsonable(array.tolist())
    if isinstance(value, float):
        if math.isfinite(value):
            return value
        return str(value)
    return value


def _finite_summary(name: str, value: Any) -> Mapping[str, Any]:
    tensor = tf.convert_to_tensor(value, dtype=tf.float64)
    finite = tf.math.is_finite(tensor)
    all_finite = bool(tf.reduce_all(finite).numpy())
    payload: dict[str, Any] = {
        "name": name,
        "shape": tuple(int(dim) for dim in tensor.shape),
        "all_finite": all_finite,
    }
    if tensor.shape.rank == 0:
        payload["value"] = float(tensor.numpy())
        return payload
    if int(tf.size(tensor).numpy()) == 0:
        payload["count"] = 0
        return payload
    payload.update(
        {
            "count": int(tf.size(tensor).numpy()),
            "min": float(tf.reduce_min(tensor).numpy()),
            "max": float(tf.reduce_max(tensor).numpy()),
        }
    )
    return payload


def _max_abs_diff(lhs: Any, rhs: Any) -> float:
    left = tf.convert_to_tensor(lhs, dtype=tf.float64)
    right = tf.convert_to_tensor(rhs, dtype=tf.float64)
    if left.shape != right.shape:
        return math.inf
    return float(tf.reduce_max(tf.abs(left - right)).numpy())


def _load_phase2_artifact(path: Path) -> Mapping[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"phase2 artifact not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, Mapping):
        raise ValueError("phase2 artifact must contain a JSON object")
    return data


def _step_payload(index: int, step: Any) -> Mapping[str, Any]:
    spec = step.spec
    reference = spec.reference_samples
    local = spec.transport.inverse_transport(reference)
    target_log_density = step.target.log_target_density(local)
    eval_pdf = spec.transport.eval_pdf(local)
    potential = spec.transport.potential(local)
    proposal_log_density = spec.transport.proposal_log_density(
        local_points=local,
        reference_points=reference,
    )
    log_normalizer = spec.transport.log_normalizer()
    positive_eval_pdf = bool(tf.reduce_all(eval_pdf > 0.0).numpy())
    target_replay_max_abs_diff = _max_abs_diff(
        target_log_density,
        step.retained_samples.target_log_density,
    )
    proposal_replay_max_abs_diff = _max_abs_diff(
        proposal_log_density,
        step.retained_samples.proposal_log_density,
    )
    return {
        "step_index": index,
        "time_index": int(step.time_index),
        "target_log_density": _finite_summary(
            "target_log_density",
            target_log_density,
        ),
        "transport_eval_pdf": {
            **_finite_summary("transport_eval_pdf", eval_pdf),
            "strictly_positive": positive_eval_pdf,
        },
        "transport_potential": _finite_summary("transport_potential", potential),
        "proposal_log_density": _finite_summary(
            "proposal_log_density",
            proposal_log_density,
        ),
        "transport_log_normalizer": _finite_summary(
            "transport_log_normalizer",
            log_normalizer,
        ),
        "retained_correction_log_weights": _finite_summary(
            "retained_correction_log_weights",
            step.retained_samples.correction_log_weights,
        ),
        "normalizer_increment": _finite_summary(
            "normalizer_increment",
            step.normalizer_increment,
        ),
        "target_replay_max_abs_diff": target_replay_max_abs_diff,
        "proposal_replay_max_abs_diff": proposal_replay_max_abs_diff,
        "previous_marginal_present": step.previous_marginal_density is not None,
        "retained_object_branch_hash": step.retained_object.branch_identity.hash.value,
    }


def _all_step_values_finite(step_rows: tuple[Mapping[str, Any], ...]) -> bool:
    summary_keys = (
        "target_log_density",
        "transport_eval_pdf",
        "transport_potential",
        "proposal_log_density",
        "transport_log_normalizer",
        "retained_correction_log_weights",
        "normalizer_increment",
    )
    for row in step_rows:
        for key in summary_keys:
            if row[key]["all_finite"] is not True:
                return False
        if row["transport_eval_pdf"]["strictly_positive"] is not True:
            return False
        if float(row["target_replay_max_abs_diff"]) > 1e-10:
            return False
        if float(row["proposal_replay_max_abs_diff"]) > 1e-10:
            return False
    return True


def build_payload(
    *,
    sample_count: int,
    fit_sample_count: int,
    phase2_artifact: Path,
) -> Mapping[str, Any]:
    started = time.monotonic()
    blockers: list[str] = []
    phase2 = _load_phase2_artifact(phase2_artifact)
    result = highdim.p59_author_sir_validation_ladder(
        tier="d18_execution_only",
        sample_count=int(sample_count),
        fit_sample_count=int(fit_sample_count),
    )
    manifest = result.manifest
    runner = result.runner_result
    assembly = None if runner is None else runner.assembly_result
    sequential = None if assembly is None else assembly.sequential_result

    if result.status != highdim.P59_9E_D18_EXECUTION_ONLY_PASS_STATUS:
        blockers.append("phase2_execution_only_status_not_pass")
    if assembly is None or sequential is None:
        blockers.append("missing_phase2_sequential_result")

    fit_hashes = tuple(str(item) for item in manifest.get("fit_branch_hashes", ()))
    density_hashes = tuple(str(item) for item in manifest.get("density_branch_hashes", ()))
    phase2_fit_hashes = tuple(str(item) for item in phase2.get("fit_branch_hashes", ()))
    phase2_density_hashes = tuple(
        str(item) for item in phase2.get("density_branch_hashes", ())
    )
    phase2_row_adequacy = tuple(phase2.get("row_adequacy_by_step", ()))
    phase2_row_statuses = tuple(
        str(row.get("status", "")) for row in phase2_row_adequacy
    )
    if fit_hashes != phase2_fit_hashes:
        blockers.append("fit_branch_hash_drift_from_phase2")
    if density_hashes != phase2_density_hashes:
        blockers.append("density_branch_hash_drift_from_phase2")

    row_adequacy = tuple(manifest.get("row_adequacy_by_step", ()))
    row_statuses = tuple(str(row.get("status", "")) for row in row_adequacy)
    if row_statuses != phase2_row_statuses:
        blockers.append("row_adequacy_drift_from_phase2_artifact")
    if not row_statuses or any(
        status != EXPECTED_PHASE2_ROW_ADEQUACY_STATUS for status in row_statuses
    ):
        blockers.append("phase2_row_adequacy_boundary_drift")

    step_rows: tuple[Mapping[str, Any], ...] = ()
    if sequential is not None:
        step_rows = tuple(
            _step_payload(index=index, step=step)
            for index, step in enumerate(sequential.steps, start=1)
        )
        if not _all_step_values_finite(step_rows):
            blockers.append("nonfinite_or_inconsistent_evaluator_value")

    status = PASS_STATUS if not blockers else BLOCK_STATUS
    return {
        "metadata_date": "2026-06-16",
        "status": status,
        "blockers": tuple(blockers),
        "phase": "P71 Phase 3",
        "question": (
            "Can the reviewed d18 source route provide finite numeric target, "
            "proposal, and transport values on the Phase 2 evaluator path?"
        ),
        "primary_criterion": (
            "finite value/evaluator output with exact Phase 2 branch identity "
            "and preserved nonclaims"
        ),
        "sample_count": int(sample_count),
        "fit_sample_count": int(fit_sample_count),
        "phase2_status": result.status,
        "phase2_baseline_artifact": str(phase2_artifact),
        "phase2_baseline_artifact_status": phase2.get("status"),
        "phase2_branch_identity": {
            "fit_branch_hashes": fit_hashes,
            "density_branch_hashes": density_hashes,
            "phase2_artifact_fit_branch_hashes": phase2_fit_hashes,
            "phase2_artifact_density_branch_hashes": phase2_density_hashes,
            "fit_hashes_match_phase2": fit_hashes == phase2_fit_hashes,
            "density_hashes_match_phase2": density_hashes == phase2_density_hashes,
        },
        "phase2_artifact_row_adequacy_by_step": phase2_row_adequacy,
        "row_adequacy_by_step": row_adequacy,
        "row_adequacy_matches_phase2_artifact": row_statuses == phase2_row_statuses,
        "step_evaluator_rows": step_rows,
        "log_marginal_likelihood": manifest.get("log_marginal_likelihood"),
        "normalizer_increments": manifest.get("normalizer_increments"),
        "runner_manifest_path": manifest.get("runner_manifest_path"),
        "environment": {
            "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "MPLCONFIGDIR": os.environ.get("MPLCONFIGDIR"),
            "cpu_only_intent": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        },
        "wall_time_seconds": round(time.monotonic() - started, 3),
        "veto_diagnostics": {
            "nonfinite_value": "nonfinite_or_inconsistent_evaluator_value" in blockers,
            "fit_branch_hash_drift": "fit_branch_hash_drift_from_phase2" in blockers,
            "density_branch_hash_drift": (
                "density_branch_hash_drift_from_phase2" in blockers
            ),
            "row_adequacy_boundary_drift": (
                "phase2_row_adequacy_boundary_drift" in blockers
                or "row_adequacy_drift_from_phase2_artifact" in blockers
            ),
        },
        "carried_forward_boundaries": {
            "row_adequacy": EXPECTED_PHASE2_ROW_ADEQUACY_STATUS,
            "p60_high_rank_comparator": "condition-vetoed; not repaired in Phase 3",
        },
        "nonclaims": (
            "no d18 filtering accuracy claim",
            "no same-route rank convergence claim",
            "no d50 or d100 scaling claim",
            "no HMC readiness claim",
            "finite numeric values are not correctness evidence",
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the P71 Phase 3 finite numeric evaluator probe."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="JSON artifact path.",
    )
    parser.add_argument(
        "--sample-count",
        type=int,
        default=1,
        help="Frozen retained reference sample count.",
    )
    parser.add_argument(
        "--fit-sample-count",
        type=int,
        default=highdim.P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT,
        help="Frozen Phase 2 fit sample count.",
    )
    parser.add_argument(
        "--phase2-artifact",
        default=DEFAULT_PHASE2_ARTIFACT,
        help="P71 Phase 2 execution-only JSON artifact used as the baseline.",
    )
    args = parser.parse_args(argv)

    payload = build_payload(
        sample_count=int(args.sample_count),
        fit_sample_count=int(args.fit_sample_count),
        phase2_artifact=Path(args.phase2_artifact),
    )
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(payload["status"])
    print(output_path)
    for blocker in payload["blockers"]:
        print(blocker, file=sys.stderr)
    return 0 if payload["status"] == PASS_STATUS else 1


if __name__ == "__main__":
    raise SystemExit(main())
