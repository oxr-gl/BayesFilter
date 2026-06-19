#!/usr/bin/env python
"""P70 Phase 6 bounded rank-channel and normalizer diagnostic.

This script reuses the bounded four-row reconstruction mechanics from the P69
Phase 5c diagnostic, but writes a P70 Phase 6 artifact and applies the P70
predeclared gates.  It is intended to be run only after explicit user approval
for the exact command.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp")

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from bayesfilter.highdim import source_route


RUN_START = time.monotonic()
SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostics-2026-06-16.json"
)
EXPECTED_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    "scripts/p70_phase6_rank_channel_normalizer_diagnostic.py"
)
NONCLAIMS = (
    "no d18 correctness claim",
    "no rank/degree promotion",
    "no scaling claim",
    "no HMC readiness claim",
    "no adaptive Zhao-Cui parity claim",
    "no author-code failure claim",
    "no claim that the original bug is fixed",
)


def _load_p69_diagnostic_module():
    script_path = REPO_ROOT / "scripts" / "p69_phase5c_rank_activity_degree_normalizer_diagnostic.py"
    spec = importlib.util.spec_from_file_location("p69_phase5c_diagnostic", script_path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("could not load P69 diagnostic module")
    spec.loader.exec_module(module)
    return module


_P69 = _load_p69_diagnostic_module()
ROW_SPECS = tuple(_P69.ROW_SPECS)


def _jsonable(value: Any) -> Any:
    return _P69._jsonable(value)


def _write_payload(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n")


def _event(stage: str, status: str, **detail: Any) -> Mapping[str, Any]:
    payload = {
        "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
        "stage": stage,
        "status": status,
        **detail,
    }
    print(json.dumps({"p70_phase6_progress": _jsonable(payload)}, sort_keys=True), flush=True)
    return payload


def _git_state_summary() -> Mapping[str, Any]:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        porcelain = subprocess.check_output(
            ["git", "status", "--short"],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).splitlines()
        return {
            "head": commit,
            "dirty": bool(porcelain),
            "status_short_count": len(porcelain),
        }
    except (OSError, subprocess.CalledProcessError) as exc:
        return {
            "head": "unknown",
            "dirty": "unknown",
            "status_error": str(exc),
        }


def _base_payload(
    *,
    rows: Mapping[str, Mapping[str, Any]],
    output: Path,
    status: str,
    command: str,
    gate_summary: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    return {
        "status": status,
        "metadata_date": "2026-06-16",
        "diagnostic_scope": "p70_phase6_bounded_four_row_repaired_fixed_fit",
        "master_program": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md"
        ),
        "subplan": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-subplan-2026-06-16.md"
        ),
        "evidence_contract": {
            "question": (
                "Does the Phase 5 repaired fixed fitting machinery activate declared "
                "rank channels and keep normalizer/holdout/replay/condition diagnostics "
                "bounded on the bounded diagnostic rows?"
            ),
            "baseline_comparator": "P69 Phase 5c constant-path one-sweep diagnosis.",
            "primary_criterion": (
                "For every executed repaired diagnostic row: row adequacy is not "
                "hard-failed; the fitter returns HighDimStatus.OK; extra declared "
                "channels pass the Phase 4 activity predicate; normalizer predicates "
                "pass; holdout and replay diagnostics exist, are finite, are disjoint "
                "from fit rows, and have normalized residuals at most 10; no "
                "condition-number veto."
            ),
            "veto_diagnostics": (
                "hard row-adequacy failure",
                "nonfinite target or fit output",
                "rank_channel_activity_failed",
                "defensive-only or nonfinite normalizer",
                "normalized holdout/replay residual above 10",
                "branch identity drift",
                "condition-number veto",
                "missing diagnostic row identity",
                "threshold mismatch from Phase 4/5",
            ),
            "explanatory_only": (
                "fit residual",
                "per-channel scores",
                "basis-channel norms",
                "raw holdout/replay residuals",
                "target-value scale summaries",
                "weighted ESS",
                "condition warnings",
                "below-preferred row status",
            ),
            "nonclaims": NONCLAIMS,
        },
        "terminal_scope": {
            "exact_approved_command": command,
            "one_command_one_assessment": True,
            "post_output_retuning_forbidden": True,
            "same_approval_second_variant_forbidden": True,
        },
        "source_route_controls": {
            "script_role": "p70_phase6_terminal_diagnostic",
            "row_specs": ROW_SPECS,
            "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
            "thresholds_changed": False,
            "source_route_semantics_changed": False,
            "p69_mechanics_reused": True,
            "p70_result_contract_added": True,
        },
        "run_manifest": {
            "command": command,
            "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
            "output": str(output),
            "script": str(SCRIPT_PATH.relative_to(REPO_ROOT)),
            "cpu_gpu_status": (
                "cpu_only_cuda_visible_devices_minus_1"
                if os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
                else "not_cpu_hidden"
            ),
            "environment": {
                "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
                "MPLCONFIGDIR": os.environ.get("MPLCONFIGDIR"),
            },
            "git_state": _git_state_summary(),
            "random_seeds": {
                "model_simulation": 5901,
                "step1_holdout_prior": 7301,
                "step1_holdout_process_noise": 7401,
                "step1_replay_prior": 7311,
                "step1_replay_process_noise": 7501,
                "step2_holdout_process_noise": 7402,
                "step2_replay_process_noise": 7502,
            },
        },
        "rows": rows,
        "gate_summary": {} if gate_summary is None else dict(gate_summary),
        "nonclaims": NONCLAIMS,
    }


def _finite_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if hasattr(value, "numpy"):
        value = value.numpy()
    if hasattr(value, "shape") and getattr(value, "shape", ()) == ():
        value = value.item()
    if not isinstance(value, (int, float)):
        return None
    number = float(value)
    if not math.isfinite(number):
        return None
    return number


def _target_scale(step: Mapping[str, Any]) -> float | None:
    stats = step.get("fit_target_stats")
    if not isinstance(stats, Mapping):
        return None
    for key in ("rms", "std", "mean", "max_abs"):
        value = _finite_float(stats.get(key))
        if value is not None and abs(value) > 1e-300:
            return abs(value)
    return None


def _normalizer_gate(normalizer: Mapping[str, Any]) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    mixture = _finite_float(normalizer.get("mixture_normalizer"))
    sqrt_norm = _finite_float(
        normalizer.get(
            "sqrt_square_normalizer",
            normalizer.get("sqrt_tt_normalizer"),
        )
    )
    log_transport = _finite_float(normalizer.get("log_transport_normalizer"))
    defensive_tau = _finite_float(normalizer.get("defensive_tau"))
    if mixture is None or mixture <= 0.0:
        reasons.append("nonfinite_or_nonpositive_mixture_normalizer")
    if sqrt_norm is None:
        reasons.append("missing_sqrt_tt_normalizer")
    elif sqrt_norm <= source_route.P70_DEFENSIVE_ONLY_SQRT_NORMALIZER_TOL:
        reasons.append("defensive_only_sqrt_normalizer")
    if log_transport is None:
        reasons.append("nonfinite_log_transport_normalizer")
    elif abs(log_transport) > source_route.P70_LOG_INCREMENT_ABS_BOUND:
        reasons.append("log_transport_normalizer_bound_exceeded")
    if defensive_tau is not None and mixture is not None and mixture > 0.0:
        fit_fraction = max(mixture - defensive_tau, 0.0) / mixture
        if fit_fraction < source_route.P70_FIT_MASS_FRACTION_MIN:
            reasons.append("fit_mass_fraction_below_min")
    return not reasons, tuple(reasons)


def _holdout_replay_gate(
    diagnostics: Mapping[str, Any],
    step: Mapping[str, Any],
) -> tuple[bool, Mapping[str, Any]]:
    scale = _target_scale(step)
    details: dict[str, Any] = {"target_scale": scale}
    reasons: list[str] = []
    for channel in ("holdout", "replay"):
        available = diagnostics.get(f"{channel}_available") is True
        nonfinite = diagnostics.get(f"{channel}_nonfinite") is True
        disjoint = diagnostics.get(f"{channel}_disjoint_from_fit") is True
        raw = _finite_float(diagnostics.get(f"{channel}_residual"))
        normalized = None if raw is None or scale is None else raw / scale
        details[channel] = {
            "available": available,
            "nonfinite": nonfinite,
            "disjoint_from_fit": disjoint,
            "raw_residual": raw,
            "normalized_residual": normalized,
        }
        if not available:
            reasons.append(f"{channel}_diagnostic_missing_or_route_mismatch")
        if nonfinite or raw is None:
            reasons.append(f"{channel}_residual_nonfinite")
        if not disjoint:
            reasons.append(f"{channel}_not_disjoint_from_fit")
        if scale is None:
            reasons.append(f"{channel}_target_scale_missing")
        elif normalized is None or normalized > source_route.P70_HOLDOUT_REPLAY_NORMALIZED_RESIDUAL_VETO:
            reasons.append(f"{channel}_normalized_residual_veto")
    branch_unchanged = diagnostics.get("branch_identity_unchanged_by_diagnostics") is True
    details["branch_identity_unchanged_by_diagnostics"] = branch_unchanged
    if not branch_unchanged:
        reasons.append("branch_identity_drift")
    details["reasons"] = tuple(reasons)
    return not reasons, details


def _row_gate(row: Mapping[str, Any]) -> Mapping[str, Any]:
    row_reasons: list[str] = []
    step_gates = []
    failed_fit = row.get("failed_fit_diagnostics")
    if isinstance(failed_fit, Mapping):
        return {
            "label": row.get("label"),
            "status": "fail",
            "reasons": (
                "row_assembly_status_not_pass",
                "captured_failed_fit",
                str(failed_fit.get("stop_condition_triggered", "unknown_stop_condition")),
            ),
            "step_gates": (),
            "failed_fit_diagnostics": failed_fit,
        }
    row_status_ok = row.get("status") == source_route.P59_9B_PASS_STATUS
    if not row_status_ok:
        row_reasons.append("row_assembly_status_not_pass")
    if row.get("fit_initialization_rule") != source_route.P70_FIXED_BRANCH_INITIALIZATION_RULE:
        row_reasons.append("threshold_mismatch_initialization_rule")
    if row.get("fixed_branch_adaptation_class") != source_route.P65_FIXED_BRANCH_ADAPTATION_CLASS:
        row_reasons.append("fixed_branch_adaptation_class_mismatch")
    for step in row.get("step_diagnostics", ()):
        quality = step.get("fit_quality", {})
        policy = quality.get("p70_fixed_fitting_policy", {}) if isinstance(quality, Mapping) else {}
        row_adequacy = policy.get("row_adequacy", {}) if isinstance(policy, Mapping) else {}
        channel_activity = policy.get("channel_activity", {}) if isinstance(policy, Mapping) else {}
        normalizer = step.get("normalizer_terms", {})
        holdout_replay = step.get("holdout_replay_diagnostics", {})
        condition = step.get("condition_summary", {})
        step_reasons: list[str] = []
        if quality.get("status") != source_route.HighDimStatus.OK.value:
            step_reasons.append("fit_status_not_ok")
        if row_adequacy.get("status") == "branch_fit_row_adequacy_failed":
            step_reasons.append("branch_fit_row_adequacy_failed")
        if not row_adequacy:
            step_reasons.append("row_adequacy_missing")
        if channel_activity.get("status") != "ok":
            step_reasons.append("rank_channel_activity_failed")
        normalizer_ok, normalizer_reasons = _normalizer_gate(normalizer)
        if not normalizer_ok:
            step_reasons.extend(normalizer_reasons)
        holdout_ok, holdout_details = _holdout_replay_gate(holdout_replay, step)
        if not holdout_ok:
            step_reasons.extend(holdout_details["reasons"])
        veto_indices = condition.get("condition_veto_core_indices")
        if veto_indices:
            step_reasons.append("condition_number_veto")
        step_gate = {
            "time_index": step.get("time_index"),
            "status": "pass" if not step_reasons else "fail",
            "reasons": tuple(step_reasons),
            "fit_status": quality.get("status"),
            "row_adequacy_status": row_adequacy.get("status"),
            "channel_activity_status": channel_activity.get("status"),
            "normalizer_ok": normalizer_ok,
            "normalizer_reasons": normalizer_reasons,
            "holdout_replay_ok": holdout_ok,
            "holdout_replay": holdout_details,
            "condition_veto_core_indices": veto_indices,
            "condition_warning_core_indices": condition.get("condition_warning_core_indices"),
            "explanatory_only": {
                "fit_residual": quality.get("fit_residual"),
                "rank_channel_summary": step.get("rank_channel_summary"),
                "degree_activity_summary": step.get("degree_activity_summary"),
                "condition_summary": condition,
            },
        }
        step_gates.append(step_gate)
    if not step_gates:
        row_reasons.append("missing_step_diagnostics")
    if any(gate["status"] != "pass" for gate in step_gates):
        row_reasons.append("one_or_more_step_gates_failed")
    return {
        "label": row.get("label"),
        "status": "pass" if not row_reasons else "fail",
        "reasons": tuple(row_reasons),
        "step_gates": tuple(step_gates),
    }


def p70_phase6_gate_summary(rows: Mapping[str, Mapping[str, Any]]) -> Mapping[str, Any]:
    row_gates = tuple(_row_gate(row) for row in rows.values())
    failed = tuple(gate for gate in row_gates if gate["status"] != "pass")
    return {
        "overall_status": "pass" if not failed and row_gates else "fail",
        "primary_criterion_status_by_row": row_gates,
        "veto_status": {
            "any_veto_failed": bool(failed) or not row_gates,
            "failed_row_labels": tuple(gate.get("label") for gate in failed),
        },
        "thresholds": {
            "normalizer_defensive_only_sqrt_tol": source_route.P70_DEFENSIVE_ONLY_SQRT_NORMALIZER_TOL,
            "fit_mass_fraction_min": source_route.P70_FIT_MASS_FRACTION_MIN,
            "log_increment_abs_bound": source_route.P70_LOG_INCREMENT_ABS_BOUND,
            "holdout_replay_normalized_residual_veto": (
                source_route.P70_HOLDOUT_REPLAY_NORMALIZED_RESIDUAL_VETO
            ),
            "condition_number_veto": source_route.P70_CONDITION_NUMBER_VETO,
        },
        "next_justified_action": (
            "write_phase6_result_and_prepare_phase7_subplan_only_after_claude_and_user_gates"
            if not failed and row_gates
            else "write_phase6_blocker_result_and_return_to_planning"
        ),
        "nonclaims": NONCLAIMS,
    }


def _failed_row_payload(
    *,
    label: str,
    degree: int,
    rank: int,
    fit_sample_count: int,
    error: source_route.P70FixedFitDiagnosticError,
) -> Mapping[str, Any]:
    return {
        "label": str(label),
        "status": "P70_PHASE6_ROW_BLOCKED",
        "blockers": (str(error),),
        "degree": int(degree),
        "rank": int(rank),
        "fit_sample_count": int(fit_sample_count),
        "failed_fit_diagnostics": error.payload,
        "transport_returned": False,
        "success_payload_emitted": False,
        "nonclaims": NONCLAIMS,
    }


def _aborted_payload(
    *,
    rows: Mapping[str, Mapping[str, Any]],
    output: Path,
    command: str,
    failed_label: str,
) -> Mapping[str, Any]:
    gate_summary = p70_phase6_gate_summary(rows)
    return _base_payload(
        rows=rows,
        output=output,
        status="P70_PHASE6_DIAGNOSTIC_ABORTED_ON_FAILED_FIT",
        command=command,
        gate_summary={
            **gate_summary,
            "terminal_status": "P70_PHASE6_DIAGNOSTIC_ABORTED_ON_FAILED_FIT",
            "failed_label": str(failed_label),
            "exit_status": 1,
            "continued_after_failed_row": False,
        },
    )


def _run_rows(
    *,
    row_specs: tuple[tuple[str, int, int, int], ...],
    row_builder,
    output: Path,
    command: str,
) -> tuple[int, Mapping[str, Mapping[str, Any]], Mapping[str, Any]]:
    rows: dict[str, Mapping[str, Any]] = {}
    for label, degree, rank, fit_sample_count in row_specs:
        try:
            rows[label] = row_builder(label, degree, rank, fit_sample_count)
        except source_route.P70FixedFitDiagnosticError as exc:
            rows[label] = _failed_row_payload(
                label=label,
                degree=degree,
                rank=rank,
                fit_sample_count=fit_sample_count,
                error=exc,
            )
            payload = _aborted_payload(
                rows=rows,
                output=output,
                command=command,
                failed_label=label,
            )
            _write_payload(output, payload)
            return 1, rows, payload
        gate_summary = p70_phase6_gate_summary(rows)
        _write_payload(
            output,
            _base_payload(
                rows=rows,
                output=output,
                status="P70_PHASE6_DIAGNOSTIC_RUNNING",
                command=command,
                gate_summary=gate_summary,
            ),
        )
    gate_summary = p70_phase6_gate_summary(rows)
    payload = {
        **_base_payload(
            rows=rows,
            output=output,
            status="P70_PHASE6_DIAGNOSTIC_COMPLETED",
            command=command,
            gate_summary=gate_summary,
        ),
        "pair_summary": _P69._pair_summary(rows),
    }
    _write_payload(output, payload)
    return 0, rows, payload


def _command_for_output(output: Path) -> str:
    if Path(output) == DEFAULT_OUTPUT:
        return EXPECTED_COMMAND
    return f"{EXPECTED_COMMAND} --output {output}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    command = _command_for_output(args.output)

    _event("run_start", "RUNNING", output=str(args.output), cpu_only=os.environ.get("CUDA_VISIBLE_DEVICES") == "-1")
    rows: dict[str, Mapping[str, Any]] = {}
    _write_payload(
        args.output,
        _base_payload(
            rows=rows,
            output=args.output,
            status="P70_PHASE6_DIAGNOSTIC_RUNNING",
            command=command,
        ),
    )
    exit_status, rows, payload = _run_rows(
        row_specs=ROW_SPECS,
        row_builder=_P69._row_payload,
        output=args.output,
        command=command,
    )
    terminal_status = str(payload.get("status", "unknown"))
    _event("run_done", terminal_status, output=str(args.output))
    return int(exit_status)


if __name__ == "__main__":
    raise SystemExit(main())
