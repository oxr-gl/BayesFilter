#!/usr/bin/env python
"""P67 bounded adjacent fixed-branch diagnostics for the author SIR route."""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Any, Mapping

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import bayesfilter.highdim.source_route as source_route


THRESHOLDS = {
    "log_marginal_abs_delta": 5.0,
    "normalizer_increment_abs_delta": 5.0,
    "probe_log_density_median_abs_delta": 10.0,
    "retained_log_density_median_abs_delta": 10.0,
}

PASS_STATUS = "P67_ADJACENT_FIXED_BUDGET_SCREEN_PASSED"
BLOCK_STATUS = "P67_ADJACENT_FIXED_BUDGET_SCREEN_BLOCKED"
INCONCLUSIVE_STATUS = "P67_ADJACENT_FIXED_BUDGET_SCREEN_INCONCLUSIVE"
RUNNING_STATUS = "P67_ADJACENT_FIXED_BUDGET_SCREEN_RUNNING"
NOT_EXECUTED_STATUS = "P67_ROW_NOT_EXECUTED"

RUN_START = time.monotonic()
RUN_EVENTS: list[Mapping[str, Any]] = []
PARTIAL_ROWS: dict[str, Mapping[str, Any]] = {}
PARTIAL_SENTINEL: Any | None = None
PARTIAL_RANK_LADDER: Mapping[str, Any] | None = None
PARTIAL_DEGREE_LADDER: Mapping[str, Any] | None = None

ROW_SPECS = (
    ("base_candidate_1_2_fit16", 1, 2, 16),
    ("rank_candidate_1_2_fit36", 1, 2, 36),
    ("rank_stronger_1_3_fit36", 1, 3, 36),
    ("degree_candidate_1_2_fit24", 1, 2, 24),
    ("degree_stronger_2_2_fit24", 2, 2, 24),
)


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


def _event(stage: str, status: str, **detail: Any) -> Mapping[str, Any]:
    payload = {
        "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
        "stage": stage,
        "status": status,
        **detail,
    }
    RUN_EVENTS.append(payload)
    print(json.dumps({"p67_progress": _jsonable(payload)}, sort_keys=True), flush=True)
    return payload


def _write_payload(path: Path | None, payload: Mapping[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n")


def _planned_row_payload(
    *,
    label: str,
    degree: int,
    rank: int,
    fit_sample_count: int,
    blockers: tuple[str, ...] = ("row_not_executed_yet",),
) -> Mapping[str, Any]:
    return {
        "label": label,
        "status": NOT_EXECUTED_STATUS,
        "blockers": blockers,
        "degree": degree,
        "rank": rank,
        "fit_sample_count": fit_sample_count,
        "rank_tuple": source_route._source_route_rank_tuple(
            source_route.P59_9A_AUTHOR_SIR_TARGET_DIMENSION,
            rank,
        ),
        "fit_branch_hashes": None,
        "density_branch_hashes": None,
        "sample_adequacy": _sample_adequacy(
            degree=degree,
            rank=rank,
            fit_sample_count=fit_sample_count,
        ),
        "source_invariants": {
            "expected": {},
            "observed": {},
            "mismatches": ("row_not_executed",),
            "passed": False,
        },
        "normalizer_terms_by_step": (),
        "defensive_only_steps": (),
        "core_diagnostics_by_step": (),
        "near_zero_core_counts": (),
        "effective_sample_size_by_step": (),
        "correction_log_weight_ranges": (),
        "budget_limitation_diagnostics": {
            "status": "not_executed",
            "limitation": "row has not executed in this visible attempt",
        },
        "budget_limited": True,
    }


def _planned_ladder_payload(
    *,
    name: str,
    candidate_label: str,
    stronger_label: str,
    blockers: tuple[str, ...] = ("ladder_not_executed_yet",),
) -> Mapping[str, Any]:
    return {
        "name": name,
        "status": NOT_EXECUTED_STATUS,
        "blockers": blockers,
        "bounded_screen_only": True,
        "candidate_row": candidate_label,
        "stronger_row": stronger_label,
        "authorized_comparison_difference_field": (
            "fit_rank" if name == "rank_ladder" else "fit_degree"
        ),
        "comparison_invariants": None,
        "deltas": None,
        "thresholds": THRESHOLDS,
        "threshold_blockers": (),
        "p60_manifest_payload": None,
    }


def _failed_fit_row_payload(
    *,
    label: str,
    degree: int,
    rank: int,
    fit_sample_count: int,
    error: source_route.P70FixedFitDiagnosticError,
) -> Mapping[str, Any]:
    return {
        **_planned_row_payload(
            label=label,
            degree=degree,
            rank=rank,
            fit_sample_count=fit_sample_count,
            blockers=(str(error),),
        ),
        "label": label,
        "status": "P67_ROW_BLOCKED_ON_FAILED_FIT",
        "blockers": (str(error),),
        "degree": degree,
        "rank": rank,
        "fit_sample_count": fit_sample_count,
        "failed_fit_diagnostics": error.payload,
        "transport_returned": False,
        "success_payload_emitted": False,
        "budget_limitation_diagnostics": {
            "status": "failed_fit_diagnostics_captured",
            "limitation": "condition-vetoed fit is inadmissible and no transport was returned",
            "fit_status": error.payload.get("fit_status"),
            "stop_condition_triggered": error.payload.get("stop_condition_triggered"),
            "condition_number_veto": error.payload.get("condition_number_veto"),
        },
        "budget_limited": True,
        "source_invariants": {
            "expected": {},
            "observed": {},
            "mismatches": ("failed_fit_before_source_invariant_capture",),
            "passed": False,
        },
    }


def _sample_adequacy(*, degree: int, rank: int, fit_sample_count: int) -> Mapping[str, Any]:
    return source_route.p66_fixed_branch_sample_adequacy(
        fit_degree=degree,
        fit_rank=rank,
        fit_sample_count=fit_sample_count,
    )


def _assemble_row(*, label: str, degree: int, rank: int, fit_sample_count: int):
    result = source_route.p59_author_sir_step_spec_assembly(
        sample_count=1,
        fit_sample_count=fit_sample_count,
        fit_degree=degree,
        fit_rank=rank,
    )
    return result, _row_payload(
        label=label,
        result=result,
        degree=degree,
        rank=rank,
        fit_sample_count=fit_sample_count,
    )


def _row_payload(
    *,
    label: str,
    result: Any,
    degree: int,
    rank: int,
    fit_sample_count: int,
) -> Mapping[str, Any]:
    adequacy = _sample_adequacy(
        degree=degree,
        rank=rank,
        fit_sample_count=fit_sample_count,
    )
    manifest = result.manifest
    sequential = result.sequential_result
    if sequential is None:
        normalizer_terms: tuple[Mapping[str, Any], ...] = ()
        defensive_only_steps: tuple[int, ...] = ()
        core_diagnostics: tuple[Mapping[str, Any], ...] = ()
        ess: tuple[float, ...] = ()
        correction_ranges: tuple[tuple[float, float], ...] = ()
    else:
        normalizer_terms = source_route._p64_normalizer_terms_by_step(sequential)
        defensive_only_steps = source_route._p64_defensive_only_steps(normalizer_terms)
        core_diagnostics = source_route._p65_sqrt_tt_core_diagnostics_by_step(sequential)
        ess = source_route._p60_ess_by_step(sequential)
        correction_ranges = source_route._p60_correction_ranges(sequential)
    source_invariants = _source_invariant_payload(result)
    budget_diagnostics = _budget_diagnostics(manifest)
    budget_limited = _budget_limited(
        result=result,
        adequacy=adequacy,
        defensive_only_steps=defensive_only_steps,
        core_diagnostics=core_diagnostics,
        budget_diagnostics=budget_diagnostics,
    )
    return {
        "label": label,
        "status": result.status,
        "blockers": result.blockers,
        "degree": degree,
        "rank": rank,
        "fit_sample_count": fit_sample_count,
        "rank_tuple": manifest.get("rank_tuple"),
        "fit_branch_hashes": manifest.get("fit_branch_hashes"),
        "density_branch_hashes": manifest.get("density_branch_hashes"),
        "sample_adequacy": adequacy,
        "source_invariants": source_invariants,
        "normalizer_terms_by_step": normalizer_terms,
        "defensive_only_steps": defensive_only_steps,
        "core_diagnostics_by_step": core_diagnostics,
        "near_zero_core_counts": tuple(
            row.get("near_zero_core_count") for row in core_diagnostics if row.get("available")
        ),
        "effective_sample_size_by_step": ess,
        "correction_log_weight_ranges": correction_ranges,
        "budget_limitation_diagnostics": budget_diagnostics,
        "budget_limited": budget_limited,
    }


def _budget_diagnostics(manifest: Mapping[str, Any]) -> Mapping[str, Any]:
    fit_data_manifests = tuple(manifest.get("fit_data_manifests", ()))
    fit_quality_by_step = tuple(manifest.get("fit_quality_diagnostics_by_step", ()))
    holdout_replay_by_step = tuple(manifest.get("holdout_replay_diagnostics_by_step", ()))
    exposed_fields = {
        key: manifest.get(key)
        for key in (
            "fit_status",
            "transport_manifest",
            "fit_branch_hashes",
            "density_branch_hashes",
            "fit_quality_diagnostics_by_step",
            "holdout_replay_diagnostics_by_step",
            "fit_initialization_rule",
            "fixed_branch_adaptation_class",
        )
        if key in manifest
    }
    missing_fit_resolution_fields: list[str] = []
    non_ok_fit_steps: list[int] = []
    fit_residual_unavailable_steps: list[int] = []
    nonfinite_fit_residual_steps: list[int] = []
    fitter_internal_holdout_unavailable_steps: list[int] = []
    holdout_unavailable_steps: list[int] = []
    holdout_nonfinite_steps: list[int] = []
    replay_unavailable_steps: list[int] = []
    replay_nonfinite_steps: list[int] = []
    branch_identity_drift_steps: list[int] = []
    route_mismatch_steps: list[int] = []
    diagnostic_only_steps: list[int] = []
    condition_warning_steps: list[int] = []
    condition_veto_steps: list[int] = []
    if not fit_quality_by_step:
        missing_fit_resolution_fields.append("fit_quality_diagnostics_by_step")
    if not holdout_replay_by_step:
        missing_fit_resolution_fields.append("holdout_replay_diagnostics_by_step")
    for step_index, diagnostics in enumerate(fit_quality_by_step, start=1):
        if not isinstance(diagnostics, Mapping):
            missing_fit_resolution_fields.append(f"step{step_index}_fit_quality_mapping")
            continue
        for field in (
            "status",
            "stop_condition_triggered",
            "fit_residual",
            "fit_residual_available",
            "holdout_available",
            "holdout_status",
            "condition_number_summary",
            "per_core_update_statuses",
        ):
            if field not in diagnostics:
                missing_fit_resolution_fields.append(f"step{step_index}_{field}")
        if diagnostics.get("status") != source_route.HighDimStatus.OK.value:
            non_ok_fit_steps.append(step_index)
        if diagnostics.get("fit_residual_available") is not True:
            fit_residual_unavailable_steps.append(step_index)
        residual = diagnostics.get("fit_residual")
        if residual is not None:
            residual_float = _float_or_none(residual)
            if residual_float is None or not math.isfinite(residual_float):
                nonfinite_fit_residual_steps.append(step_index)
        if diagnostics.get("holdout_available") is not True:
            fitter_internal_holdout_unavailable_steps.append(step_index)
        summary = diagnostics.get("condition_number_summary", {})
        if not isinstance(summary, Mapping):
            missing_fit_resolution_fields.append(
                f"step{step_index}_condition_number_summary_mapping"
            )
            continue
        for field in (
            "max_condition_number",
            "condition_number_warning",
            "condition_number_veto",
        ):
            if field not in summary:
                missing_fit_resolution_fields.append(
                    f"step{step_index}_condition_summary_{field}"
                )
        if summary.get("condition_warning_core_indices"):
            condition_warning_steps.append(step_index)
        if summary.get("condition_veto_core_indices"):
            condition_veto_steps.append(step_index)
    for step_index, diagnostics in enumerate(holdout_replay_by_step, start=1):
        if not isinstance(diagnostics, Mapping):
            missing_fit_resolution_fields.append(
                f"step{step_index}_holdout_replay_mapping"
            )
            continue
        for field in (
            "diagnostic_role",
            "diagnostic_classification",
            "holdout_available",
            "holdout_residual_available",
            "holdout_nonfinite",
            "replay_available",
            "replay_residual_available",
            "replay_nonfinite",
            "branch_identity_unchanged_by_diagnostics",
            "source_route_invariants",
        ):
            if field not in diagnostics:
                missing_fit_resolution_fields.append(f"step{step_index}_{field}")
        if diagnostics.get("diagnostic_role") == "post_fit_diagnostic_only":
            diagnostic_only_steps.append(step_index)
        if (
            diagnostics.get("holdout_available") is not True
            or diagnostics.get("holdout_residual_available") is not True
        ):
            holdout_unavailable_steps.append(step_index)
        if diagnostics.get("holdout_nonfinite") is True:
            holdout_nonfinite_steps.append(step_index)
        if (
            diagnostics.get("replay_available") is not True
            or diagnostics.get("replay_residual_available") is not True
        ):
            replay_unavailable_steps.append(step_index)
        if diagnostics.get("replay_nonfinite") is True:
            replay_nonfinite_steps.append(step_index)
        if diagnostics.get("branch_identity_unchanged_by_diagnostics") is not True:
            branch_identity_drift_steps.append(step_index)
        invariants = diagnostics.get("source_route_invariants", {})
        if isinstance(invariants, Mapping) and invariants.get("route_mismatch") is True:
            route_mismatch_steps.append(step_index)
        for key in ("holdout_residual", "replay_residual"):
            residual = diagnostics.get(key)
            if residual is not None:
                residual_float = _float_or_none(residual)
                if residual_float is None or not math.isfinite(residual_float):
                    if key == "holdout_residual" and step_index not in holdout_nonfinite_steps:
                        holdout_nonfinite_steps.append(step_index)
                    if key == "replay_residual" and step_index not in replay_nonfinite_steps:
                        replay_nonfinite_steps.append(step_index)
    holdout_replay_resolution_status = "available"
    if not holdout_replay_by_step:
        holdout_replay_resolution_status = "missing"
    elif branch_identity_drift_steps:
        holdout_replay_resolution_status = source_route.P69_BRANCH_IDENTITY_DRIFT_STATUS
    elif route_mismatch_steps:
        holdout_replay_resolution_status = source_route.P69_HOLDOUT_REPLAY_ROUTE_MISMATCH_STATUS
    elif holdout_nonfinite_steps or replay_nonfinite_steps:
        holdout_replay_resolution_status = source_route.P69_HOLDOUT_REPLAY_NONFINITE_STATUS
    elif holdout_unavailable_steps or replay_unavailable_steps:
        holdout_replay_resolution_status = source_route.P69_HOLDOUT_REPLAY_MISSING_STATUS
    else:
        holdout_replay_resolution_status = source_route.P69_HOLDOUT_REPLAY_AVAILABLE_STATUS
    return {
        "exposed_fields": exposed_fields,
        "fit_data_manifest_count": len(fit_data_manifests),
        "fit_data_manifests_present": bool(fit_data_manifests),
        "fit_quality_diagnostics_by_step": fit_quality_by_step,
        "fit_quality_diagnostics_present": bool(fit_quality_by_step),
        "holdout_replay_diagnostics_by_step": holdout_replay_by_step,
        "holdout_replay_diagnostics_present": bool(holdout_replay_by_step),
        "missing_fit_resolution_fields": tuple(missing_fit_resolution_fields),
        "non_ok_fit_steps": tuple(non_ok_fit_steps),
        "fit_residual_unavailable_steps": tuple(fit_residual_unavailable_steps),
        "nonfinite_fit_residual_steps": tuple(nonfinite_fit_residual_steps),
        "fitter_internal_holdout_unavailable_steps": tuple(
            fitter_internal_holdout_unavailable_steps
        ),
        "holdout_unavailable_steps": tuple(holdout_unavailable_steps),
        "holdout_nonfinite_steps": tuple(holdout_nonfinite_steps),
        "replay_unavailable_steps": tuple(replay_unavailable_steps),
        "replay_nonfinite_steps": tuple(replay_nonfinite_steps),
        "branch_identity_drift_steps": tuple(branch_identity_drift_steps),
        "route_mismatch_steps": tuple(route_mismatch_steps),
        "diagnostic_only_steps": tuple(diagnostic_only_steps),
        "holdout_replay_resolution_status": holdout_replay_resolution_status,
        "condition_warning_steps": tuple(condition_warning_steps),
        "condition_veto_steps": tuple(condition_veto_steps),
        "limitation": (
            "Step-level fit-quality diagnostics are interpreted as veto or "
            "inconclusive evidence only; they do not prove convergence or "
            "filtering correctness."
        ),
    }


def _float_or_none(value: Any) -> float | None:
    if hasattr(value, "numpy"):
        value = value.numpy()
        if getattr(value, "shape", ()) == ():
            value = value.item()
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _budget_limited(
    *,
    result: Any,
    adequacy: Mapping[str, Any],
    defensive_only_steps: tuple[int, ...],
    core_diagnostics: tuple[Mapping[str, Any], ...],
    budget_diagnostics: Mapping[str, Any],
) -> bool:
    if result.status != source_route.P59_9B_PASS_STATUS:
        return True
    if adequacy["status"] != source_route.P66_SAMPLE_ADEQUATE_STATUS:
        return True
    if defensive_only_steps:
        return True
    if any(row.get("near_zero_core_count", 0) for row in core_diagnostics if row.get("available")):
        return True
    if budget_diagnostics["missing_fit_resolution_fields"]:
        return True
    for key in (
        "non_ok_fit_steps",
        "fit_residual_unavailable_steps",
        "nonfinite_fit_residual_steps",
        "holdout_unavailable_steps",
        "holdout_nonfinite_steps",
        "replay_unavailable_steps",
        "replay_nonfinite_steps",
        "branch_identity_drift_steps",
        "route_mismatch_steps",
        "condition_warning_steps",
        "condition_veto_steps",
    ):
        if budget_diagnostics[key]:
            return True
    return False


def _source_invariant_payload(result: Any) -> Mapping[str, Any]:
    manifest = result.manifest
    expected = {
        "target_dimension": source_route.P59_9A_AUTHOR_SIR_TARGET_DIMENSION,
        "source_target_order": "[theta, x_t, x_{t-1}]",
        "previous_marginal_keep_axes": tuple(range(18)),
        "previous_marginal_input_axes": tuple(range(18, 36)),
        "fit_data_mode": source_route.P63_AUTHOR_SIR_SOURCE_FIT_DATA_MODE,
        "defensive_tau": source_route.P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU,
        "fit_initialization_rule": source_route.P70_FIXED_BRANCH_INITIALIZATION_RULE,
        "fixed_branch_adaptation_class": source_route.P65_FIXED_BRANCH_ADAPTATION_CLASS,
    }
    observed = {key: manifest.get(key) for key in expected}
    mismatches = tuple(
        key for key, expected_value in expected.items() if observed.get(key) != expected_value
    )
    return {
        "expected": expected,
        "observed": observed,
        "mismatches": mismatches,
        "passed": not mismatches,
    }


def _ladder_payload(
    *,
    name: str,
    candidate: Any,
    stronger: Any,
    candidate_row: Mapping[str, Any],
    stronger_row: Mapping[str, Any],
    authorized_field: str,
) -> Mapping[str, Any]:
    manifest = source_route._p60_rank_comparator_manifest(candidate, stronger)
    deltas = {
        "log_marginal_abs_delta": manifest["log_marginal_abs_delta"],
        "normalizer_increment_abs_deltas": manifest["normalizer_increment_abs_deltas"],
        "probe_log_density_median_abs_delta": manifest["probe_log_density_median_abs_delta"],
        "retained_log_density_median_abs_delta": manifest[
            "retained_log_density_median_abs_delta"
        ],
    }
    threshold_blockers = tuple(
        blocker
        for blocker in manifest["veto_blockers"]
        if blocker
        in (
            "log_marginal_delta_threshold_exceeded",
            "normalizer_increment_delta_threshold_exceeded",
            "probe_log_density_delta_threshold_exceeded",
            "retained_log_density_delta_threshold_exceeded",
            "retained_density_delta_unavailable",
        )
    )
    invariant_check = _comparison_invariants(
        candidate_row=candidate_row,
        stronger_row=stronger_row,
        authorized_field=authorized_field,
    )
    blockers: list[str] = []
    if candidate_row["budget_limited"]:
        blockers.append("candidate_row_budget_limited_or_unresolved")
    if stronger_row["budget_limited"]:
        blockers.append("stronger_row_budget_limited_or_unresolved")
    if not candidate_row["source_invariants"]["passed"]:
        blockers.append("candidate_source_invariant_drift")
    if not stronger_row["source_invariants"]["passed"]:
        blockers.append("stronger_source_invariant_drift")
    if invariant_check["unauthorized_differences"]:
        blockers.append("unauthorized_comparison_difference")
    blockers.extend(threshold_blockers)
    status = PASS_STATUS if not blockers else BLOCK_STATUS
    if any("budget_limited" in blocker for blocker in blockers):
        status = INCONCLUSIVE_STATUS
    return {
        "name": name,
        "status": status,
        "blockers": tuple(blockers),
        "bounded_screen_only": True,
        "candidate_row": candidate_row["label"],
        "stronger_row": stronger_row["label"],
        "authorized_comparison_difference_field": authorized_field,
        "comparison_invariants": invariant_check,
        "deltas": deltas,
        "thresholds": THRESHOLDS,
        "threshold_blockers": threshold_blockers,
        "p60_manifest_payload": manifest,
    }


def _comparison_invariants(
    *,
    candidate_row: Mapping[str, Any],
    stronger_row: Mapping[str, Any],
    authorized_field: str,
) -> Mapping[str, Any]:
    fields = (
        "target_dimension",
        "source_target_order",
        "previous_marginal_keep_axes",
        "previous_marginal_input_axes",
        "fit_data_mode",
        "defensive_tau",
        "fit_initialization_rule",
        "fixed_branch_adaptation_class",
        "fit_degree",
        "fit_rank",
    )
    candidate = {
        "target_dimension": candidate_row["source_invariants"]["observed"]["target_dimension"],
        "source_target_order": candidate_row["source_invariants"]["observed"][
            "source_target_order"
        ],
        "previous_marginal_keep_axes": candidate_row["source_invariants"]["observed"][
            "previous_marginal_keep_axes"
        ],
        "previous_marginal_input_axes": candidate_row["source_invariants"]["observed"][
            "previous_marginal_input_axes"
        ],
        "fit_data_mode": candidate_row["source_invariants"]["observed"]["fit_data_mode"],
        "defensive_tau": candidate_row["source_invariants"]["observed"]["defensive_tau"],
        "fit_initialization_rule": candidate_row["source_invariants"]["observed"][
            "fit_initialization_rule"
        ],
        "fixed_branch_adaptation_class": candidate_row["source_invariants"]["observed"][
            "fixed_branch_adaptation_class"
        ],
        "fit_degree": candidate_row["degree"],
        "fit_rank": candidate_row["rank"],
    }
    stronger = {
        "target_dimension": stronger_row["source_invariants"]["observed"]["target_dimension"],
        "source_target_order": stronger_row["source_invariants"]["observed"][
            "source_target_order"
        ],
        "previous_marginal_keep_axes": stronger_row["source_invariants"]["observed"][
            "previous_marginal_keep_axes"
        ],
        "previous_marginal_input_axes": stronger_row["source_invariants"]["observed"][
            "previous_marginal_input_axes"
        ],
        "fit_data_mode": stronger_row["source_invariants"]["observed"]["fit_data_mode"],
        "defensive_tau": stronger_row["source_invariants"]["observed"]["defensive_tau"],
        "fit_initialization_rule": stronger_row["source_invariants"]["observed"][
            "fit_initialization_rule"
        ],
        "fixed_branch_adaptation_class": stronger_row["source_invariants"]["observed"][
            "fixed_branch_adaptation_class"
        ],
        "fit_degree": stronger_row["degree"],
        "fit_rank": stronger_row["rank"],
    }
    differences = tuple(key for key in fields if candidate.get(key) != stronger.get(key))
    unauthorized = tuple(key for key in differences if key != authorized_field)
    return {
        "candidate": candidate,
        "stronger": stronger,
        "differences": differences,
        "unauthorized_differences": unauthorized,
        "authorized_comparison_difference": authorized_field in differences,
        "authorized_comparison_difference_field": authorized_field,
    }


def run_diagnostics(output_path: Path | None = None) -> Mapping[str, Any]:
    global PARTIAL_SENTINEL, PARTIAL_RANK_LADDER, PARTIAL_DEGREE_LADDER
    planned_rows = {
        label: _planned_row_payload(
            label=label,
            degree=degree,
            rank=rank,
            fit_sample_count=fit_count,
        )
        for label, degree, rank, fit_count in ROW_SPECS
    }
    PARTIAL_ROWS.clear()
    PARTIAL_ROWS.update(planned_rows)
    PARTIAL_RANK_LADDER = _planned_ladder_payload(
        name="rank_ladder",
        candidate_label="rank_candidate_1_2_fit36",
        stronger_label="rank_stronger_1_3_fit36",
    )
    PARTIAL_DEGREE_LADDER = _planned_ladder_payload(
        name="degree_ladder",
        candidate_label="degree_candidate_1_2_fit24",
        stronger_label="degree_stronger_2_2_fit24",
    )
    _event("run", "start", row_count=len(ROW_SPECS))
    _write_payload(
        output_path,
        _result_payload(
            status=RUNNING_STATUS,
            blockers=("run_started_no_rows_completed_yet",),
            rows=PARTIAL_ROWS,
            sentinel=None,
            rank_ladder=PARTIAL_RANK_LADDER,
            degree_ladder=PARTIAL_DEGREE_LADDER,
        ),
    )
    _event("sentinel", "start")
    sentinel = source_route.p60_author_sir_same_route_rank_comparator(
        sample_count=1,
        fit_sample_count=2,
        low_fit_degree=0,
        high_fit_degree=1,
        low_fit_rank=1,
        high_fit_rank=2,
    )
    PARTIAL_SENTINEL = sentinel
    _event("sentinel", "done", status_value=sentinel.status)
    _write_payload(
        output_path,
        _result_payload(
            status=RUNNING_STATUS,
            blockers=("sentinel_completed_rows_pending",),
            rows=PARTIAL_ROWS,
            sentinel=sentinel,
            rank_ladder=PARTIAL_RANK_LADDER,
            degree_ladder=PARTIAL_DEGREE_LADDER,
        ),
    )
    rows: dict[str, Mapping[str, Any]] = {}
    row_results: dict[str, Any] = {}
    blockers: list[str] = []
    for label, degree, rank, fit_count in ROW_SPECS:
        _event(
            "row",
            "start",
            label=label,
            degree=degree,
            rank=rank,
            fit_sample_count=fit_count,
        )
        try:
            result, row = _assemble_row(
                label=label,
                degree=degree,
                rank=rank,
                fit_sample_count=fit_count,
            )
            row_results[label] = result
            rows[label] = row
            PARTIAL_ROWS[label] = row
            _event("row", "done", label=label, status_value=result.status)
            if result.status != source_route.P59_9B_PASS_STATUS:
                blockers.append(f"{label}_assembly_failed")
        except source_route.P70FixedFitDiagnosticError as exc:
            blockers.append(f"{label}_exception_{type(exc).__name__}_{exc}")
            rows[label] = _failed_fit_row_payload(
                label=label,
                degree=degree,
                rank=rank,
                fit_sample_count=fit_count,
                error=exc,
            )
            PARTIAL_ROWS[label] = rows[label]
            _event("row", "exception", label=label, exception=type(exc).__name__)
        except Exception as exc:  # pragma: no cover - preserved in JSON result
            blockers.append(f"{label}_exception_{type(exc).__name__}_{exc}")
            rows[label] = {
                **_planned_row_payload(
                    label=label,
                    degree=degree,
                    rank=rank,
                    fit_sample_count=fit_count,
                    blockers=(str(exc),),
                ),
                "label": label,
                "status": "EXCEPTION",
                "blockers": (str(exc),),
                "degree": degree,
                "rank": rank,
                "fit_sample_count": fit_count,
            }
            PARTIAL_ROWS[label] = rows[label]
            _event("row", "exception", label=label, exception=type(exc).__name__)
        _write_payload(
            output_path,
            _result_payload(
                status=RUNNING_STATUS if not blockers else BLOCK_STATUS,
                blockers=tuple(blockers) or ("rows_pending",),
                rows=PARTIAL_ROWS,
                sentinel=sentinel,
                rank_ladder=PARTIAL_RANK_LADDER,
                degree_ladder=PARTIAL_DEGREE_LADDER,
            ),
        )
    if blockers:
        return _result_payload(
            status=BLOCK_STATUS,
            blockers=tuple(blockers),
            rows=PARTIAL_ROWS,
            sentinel=sentinel,
            rank_ladder=PARTIAL_RANK_LADDER,
            degree_ladder=PARTIAL_DEGREE_LADDER,
        )
    _event("rank_ladder", "start")
    rank_ladder = _ladder_payload(
        name="rank_ladder",
        candidate=row_results["rank_candidate_1_2_fit36"],
        stronger=row_results["rank_stronger_1_3_fit36"],
        candidate_row=rows["rank_candidate_1_2_fit36"],
        stronger_row=rows["rank_stronger_1_3_fit36"],
        authorized_field="fit_rank",
    )
    PARTIAL_RANK_LADDER = rank_ladder
    _event("rank_ladder", "done", status_value=rank_ladder["status"])
    _write_payload(
        output_path,
        _result_payload(
            status=RUNNING_STATUS,
            blockers=("degree_ladder_pending",),
            rows=PARTIAL_ROWS,
            sentinel=sentinel,
            rank_ladder=PARTIAL_RANK_LADDER,
            degree_ladder=PARTIAL_DEGREE_LADDER,
        ),
    )
    _event("degree_ladder", "start")
    degree_ladder = _ladder_payload(
        name="degree_ladder",
        candidate=row_results["degree_candidate_1_2_fit24"],
        stronger=row_results["degree_stronger_2_2_fit24"],
        candidate_row=rows["degree_candidate_1_2_fit24"],
        stronger_row=rows["degree_stronger_2_2_fit24"],
        authorized_field="fit_degree",
    )
    PARTIAL_DEGREE_LADDER = degree_ladder
    _event("degree_ladder", "done", status_value=degree_ladder["status"])
    status = PASS_STATUS
    if rank_ladder["status"] == BLOCK_STATUS or degree_ladder["status"] == BLOCK_STATUS:
        status = BLOCK_STATUS
    if (
        rank_ladder["status"] == INCONCLUSIVE_STATUS
        or degree_ladder["status"] == INCONCLUSIVE_STATUS
    ):
        status = INCONCLUSIVE_STATUS
    result_blockers = tuple(rank_ladder["blockers"]) + tuple(degree_ladder["blockers"])
    return _result_payload(
        status=status,
        blockers=result_blockers,
        rows=PARTIAL_ROWS,
        sentinel=sentinel,
        rank_ladder=rank_ladder,
        degree_ladder=degree_ladder,
    )


def _result_payload(
    *,
    status: str,
    blockers: tuple[str, ...],
    rows: Mapping[str, Any],
    sentinel: Any | None,
    rank_ladder: Mapping[str, Any] | None,
    degree_ladder: Mapping[str, Any] | None,
) -> Mapping[str, Any]:
    return {
        "status": status,
        "blockers": blockers,
        "rows": rows,
        "sentinel": (
            {
                "status": sentinel.status,
                "blockers": sentinel.blockers,
                "interpretation": "explanatory_sentinel_not_primary_gate",
                "manifest": sentinel.manifest,
            }
            if sentinel is not None
            else {
                "status": NOT_EXECUTED_STATUS,
                "blockers": ("sentinel_not_executed_yet",),
                "interpretation": "explanatory_sentinel_not_primary_gate",
                "manifest": None,
            }
        ),
        "rank_ladder": rank_ladder,
        "degree_ladder": degree_ladder,
        "thresholds": THRESHOLDS,
        "source_invariants": {
            label: row.get("source_invariants") for label, row in rows.items()
        },
        "nonclaims": (
            "bounded fixed-budget screen only",
            "no structural rank/degree convergence proof",
            "no d18 correctness claim",
            "no d50 or d100 scaling claim",
            "no HMC production readiness claim",
            "no adaptive Zhao-Cui parity claim",
        ),
        "run_manifest": {
            "script": "scripts/p67_author_sir_adjacent_ladder_diagnostics.py",
            "cpu_only_intent": "CUDA_VISIBLE_DEVICES=-1",
            "sample_count": 1,
            "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
            "fit_budgets": {
                "base_candidate": 16,
                "rank_pair": 36,
                "degree_pair": 24,
            },
            "bounded_screen_only": True,
            "events": tuple(RUN_EVENTS),
        },
    }


def check_artifact(payload: Mapping[str, Any]) -> tuple[str, ...]:
    blockers: list[str] = []
    required = (
        "status",
        "blockers",
        "rows",
        "sentinel",
        "rank_ladder",
        "degree_ladder",
        "thresholds",
        "source_invariants",
        "nonclaims",
        "run_manifest",
    )
    for key in required:
        if key not in payload:
            blockers.append(f"missing_top_level_{key}")
    rows = payload.get("rows", {})
    if not isinstance(rows, Mapping) or not rows:
        blockers.append("missing_rows")
    else:
        for label, row in rows.items():
            for key in (
                "source_invariants",
                "sample_adequacy",
                "defensive_only_steps",
                "budget_limitation_diagnostics",
            ):
                if key not in row:
                    blockers.append(f"{label}_missing_{key}")
    for ladder_name in ("rank_ladder", "degree_ladder"):
        ladder = payload.get(ladder_name)
        if ladder is None:
            blockers.append(f"missing_{ladder_name}")
            continue
        if "candidate_row" not in ladder or "stronger_row" not in ladder:
            blockers.append(f"{ladder_name}_missing_pair_rows")
        if ladder.get("bounded_screen_only") is not True:
            blockers.append(f"{ladder_name}_missing_bounded_screen_flag")
        if payload.get("status") == PASS_STATUS and ladder.get("status") != PASS_STATUS:
            blockers.append(f"{ladder_name}_not_passed_for_pass_status")
    nonclaims = tuple(payload.get("nonclaims", ()))
    for phrase in (
        "no structural rank/degree convergence proof",
        "no d18 correctness claim",
        "no HMC production readiness claim",
        "no adaptive Zhao-Cui parity claim",
    ):
        if phrase not in nonclaims:
            blockers.append(f"missing_nonclaim_{phrase}")
    return tuple(blockers)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    output = Path(args.output)
    if args.check_only:
        payload = json.loads(output.read_text())
    else:
        payload = run_diagnostics(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n")
    blockers = check_artifact(payload)
    if blockers:
        print(json.dumps({"artifact_check": "FAIL", "blockers": blockers}, indent=2))
        return 2
    print(json.dumps({"artifact_check": "PASS", "status": payload["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
