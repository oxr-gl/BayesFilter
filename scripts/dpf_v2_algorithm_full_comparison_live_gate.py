from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


EXPECTED_ROWS = (
    "lgssm_2d_h25_rich",
    "sv_1d_h18_rich",
    "range_bearing_4d_h20_rich",
    "structural_ar1_quadratic_h16",
    "spatial_sir_j3_rk4",
    "predator_prey_rk4",
)

PLAN_READY_TOKEN = "CLAUDE_REVIEWED_LAUNCH_READY"
PLAN_REVIEW_PASS_TOKEN = "PASS_LIVE_GATED_EXECUTION_PLAN_READY"
HUMAN_RISK_ACCEPTED_TOKEN = "HUMAN_RISK_ACCEPTED_LAUNCH_READY"
PLAN_REVIEW_STOP_TOKEN = "STOP_MAX_REVIEW_ROUNDS_WITH_MATERIAL_BLOCKERS"

STATUS_RE = re.compile(r"^\s*(?:status|Status|Verdict):\s*`?([^`]+?)`?\s*\.?\s*$")
RUN_ID_RE = re.compile(r"^\s*run_id:\s*`?([^`]+?)`?\s*\.?\s*$", re.IGNORECASE)


PHASES = {
    "P0": {
        "token": "PASS_P0_READY_FOR_P1",
        "result": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-result-2026-06-07.md",
        "review": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-claude-review-ledger-2026-06-07.md",
        "json": "experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p0_governance_2026-06-07.json",
    },
    "P1": {
        "token": "PASS_P1_ARCHITECTURE_READY_FOR_P2",
        "result": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-result-2026-06-07.md",
        "review": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-claude-review-ledger-2026-06-07.md",
        "json": "experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p1_architecture_2026-06-07.json",
    },
    "P2": {
        "token": "PASS_P2_BOOTSTRAP_OT_CONTRACTS_READY_FOR_P3",
        "result": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p2-bootstrap-ot-contracts-result-2026-06-07.md",
        "review": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p2-bootstrap-ot-contracts-claude-review-ledger-2026-06-07.md",
        "json": "experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_contracts_2026-06-07.json",
    },
    "P3": {
        "token": "PASS_P3_BOOTSTRAP_OT_VALUES_READY_FOR_P4",
        "result": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p3-bootstrap-ot-values-result-2026-06-07.md",
        "review": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p3-bootstrap-ot-values-claude-review-ledger-2026-06-07.md",
        "json": "experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_values_2026-06-07.json",
    },
    "P4": {
        "token": "PASS_P4_BOOTSTRAP_OT_GRADIENTS_READY_FOR_P5",
        "result": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-result-2026-06-07.md",
        "review": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-claude-review-ledger-2026-06-07.md",
        "json": "experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_gradients_2026-06-07.json",
    },
    "P5": {
        "token": "PASS_P5_LEDH_PFPF_OT_CONTRACTS_READY_FOR_P6",
        "result": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-result-2026-06-07.md",
        "review": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-claude-review-ledger-2026-06-07.md",
        "json": "experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_contracts_2026-06-07.json",
    },
    "P6": {
        "token": "PASS_P6_LEDH_PFPF_OT_VALUES_READY_FOR_P7",
        "result": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-result-2026-06-07.md",
        "review": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-claude-review-ledger-2026-06-07.md",
        "json": "experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_values_2026-06-07.json",
    },
    "P7": {
        "token": "PASS_P7_LEDH_PFPF_OT_GRADIENTS_READY_FOR_P8",
        "result": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-result-2026-06-07.md",
        "review": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-claude-review-ledger-2026-06-07.md",
        "json": "experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_gradients_2026-06-07.json",
    },
    "P8": {
        "token": "PASS_FULL_COMPARISON",
        "alternate_token": "BLOCKED_WITH_REVIEWED_CLASSIFICATION",
        "result": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-closeout-result-2026-06-07.md",
        "review": "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-closeout-claude-review-ledger-2026-06-07.md",
        "json": "experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_closeout_2026-06-07.json",
    },
}


def latest_status(path: Path) -> str | None:
    latest: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        match = STATUS_RE.match(line)
        if match:
            latest = match.group(1).strip()
    return latest


def latest_run_id(path: Path) -> str | None:
    latest: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        match = RUN_ID_RE.match(line)
        if match:
            latest = match.group(1).strip()
    return latest


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def json_has_expected_rows(payload: object) -> bool:
    return isinstance(payload, dict) and payload.get("required_v2_model_ids") == list(EXPECTED_ROWS)


def require_row_status_map(payload: dict[str, Any], key: str, phase: str) -> int:
    statuses = payload.get(key)
    if not isinstance(statuses, dict):
        return fail(f"{phase} JSON artifact lacks {key} map")
    missing = [row for row in EXPECTED_ROWS if row not in statuses]
    if missing:
        return fail(f"{phase} {key} missing rows: {missing}")
    bad = {row: statuses[row] for row in EXPECTED_ROWS if statuses[row] != "PASS"}
    if bad:
        return fail(f"{phase} {key} has non-PASS rows: {bad}")
    return 0


def require_gradient_knobs(payload: dict[str, Any], phase: str) -> int:
    knobs = payload.get("required_gradient_knobs_by_row")
    if not isinstance(knobs, dict):
        return fail(f"{phase} JSON artifact lacks required_gradient_knobs_by_row")
    missing = [row for row in EXPECTED_ROWS if row not in knobs]
    if missing:
        return fail(f"{phase} gradient knob map missing rows: {missing}")
    empty = [row for row in EXPECTED_ROWS if not isinstance(knobs[row], list) or not knobs[row]]
    if empty:
        return fail(f"{phase} gradient knob map has empty/non-list rows: {empty}")
    return 0


def require_algorithm_gradient_knobs(payload: dict[str, Any], phase: str) -> int:
    knobs = payload.get("required_gradient_knobs_by_algorithm_and_row")
    if not isinstance(knobs, dict):
        return fail(f"{phase} JSON lacks required_gradient_knobs_by_algorithm_and_row")
    for algorithm in ("bootstrap_ot", "ledh_pfpf_ot"):
        by_row = knobs.get(algorithm)
        if not isinstance(by_row, dict):
            return fail(f"{phase} gradient knob map lacks algorithm {algorithm}")
        missing = [row for row in EXPECTED_ROWS if row not in by_row]
        if missing:
            return fail(f"{phase} {algorithm} gradient knob map missing rows: {missing}")
        empty = [row for row in EXPECTED_ROWS if not isinstance(by_row[row], list) or not by_row[row]]
        if empty:
            return fail(f"{phase} {algorithm} gradient knob map has empty/non-list rows: {empty}")
    return 0


def check_phase_specific_payload(payload: dict[str, Any], phase: str, acceptable: set[str]) -> int:
    if not json_has_expected_rows(payload):
        return fail(f"{phase} JSON required_v2_model_ids does not exactly match expected rows")
    if phase == "P0":
        return require_row_status_map(payload, "governance_gate_status_by_row", phase)
    if phase == "P1":
        return require_row_status_map(payload, "architecture_gate_status_by_row", phase)
    if phase in {"P2", "P5"}:
        return require_row_status_map(payload, "contract_gate_status_by_row", phase)
    if phase in {"P3", "P6"}:
        return require_row_status_map(payload, "value_gate_status_by_row", phase)
    if phase in {"P4", "P7"}:
        status = require_row_status_map(payload, "gradient_gate_status_by_row", phase)
        if status:
            return status
        return require_gradient_knobs(payload, phase)
    if phase == "P8":
        final_status = payload.get("final_status") or payload.get("status") or payload.get("decision")
        if final_status not in acceptable:
            return fail(f"P8 final status {final_status!r} not in {sorted(acceptable)}")
        phase_statuses = payload.get("phase_gate_statuses")
        if not isinstance(phase_statuses, dict):
            return fail("P8 JSON lacks phase_gate_statuses")
        for prior in ("P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"):
            expected = PHASES[prior]["token"]
            if phase_statuses.get(prior) != expected:
                return fail(f"P8 phase_gate_statuses[{prior!r}] is not {expected!r}")
        if final_status == "PASS_FULL_COMPARISON":
            for key in (
                "bootstrap_ot_value_gate_status_by_row",
                "bootstrap_ot_gradient_gate_status_by_row",
                "ledh_pfpf_ot_value_gate_status_by_row",
                "ledh_pfpf_ot_gradient_gate_status_by_row",
            ):
                status = require_row_status_map(payload, key, "P8")
                if status:
                    return status
            status = require_algorithm_gradient_knobs(payload, "P8")
            if status:
                return status
        else:
            if payload.get("blocker_classification_reviewed") is not True:
                return fail("P8 blocked closeout lacks blocker_classification_reviewed true")
            blocked_items = payload.get("blocked_items")
            if not isinstance(blocked_items, list) or not blocked_items:
                return fail("P8 blocked closeout lacks nonempty blocked_items")
        return 0
    return fail(f"unknown phase for payload validation: {phase}")


def check_phase(root: Path, phase: str, run_id: str) -> int:
    spec = PHASES[phase]
    expected = spec["token"]
    alternate = spec.get("alternate_token")
    acceptable = {expected}
    if alternate:
        acceptable.add(alternate)

    paths = {key: root / spec[key] for key in ("result", "review", "json")}
    for label, path in paths.items():
        if not path.is_file():
            return fail(f"{phase} missing {label} artifact: {path}")
        if path.stat().st_size == 0:
            return fail(f"{phase} empty {label} artifact: {path}")

    result_status = latest_status(paths["result"])
    review_status = latest_status(paths["review"])
    if result_status not in acceptable:
        return fail(f"{phase} result status {result_status!r} not in {sorted(acceptable)}")
    if review_status not in acceptable:
        return fail(f"{phase} review status {review_status!r} not in {sorted(acceptable)}")

    result_run_id = latest_run_id(paths["result"])
    review_run_id = latest_run_id(paths["review"])
    if result_run_id != run_id:
        return fail(f"{phase} result run_id {result_run_id!r} != {run_id!r}")
    if review_run_id != run_id:
        return fail(f"{phase} review run_id {review_run_id!r} != {run_id!r}")

    try:
        payload = json.loads(paths["json"].read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"{phase} invalid JSON artifact {paths['json']}: {exc}")

    payload_run_id = payload.get("run_id") if isinstance(payload, dict) else None
    if payload_run_id != run_id:
        return fail(f"{phase} JSON run_id {payload_run_id!r} != {run_id!r}")
    payload_status = (payload.get("status") or payload.get("decision")) if isinstance(payload, dict) else None
    if not isinstance(payload_status, str):
        return fail(f"{phase} JSON artifact lacks string status or decision")
    if payload_status not in acceptable:
        return fail(f"{phase} JSON status/decision {payload_status!r} not in {sorted(acceptable)}")
    if not isinstance(payload, dict):
        return fail(f"{phase} JSON artifact is not an object")
    phase_specific_status = check_phase_specific_payload(payload, phase, acceptable)
    if phase_specific_status:
        return phase_specific_status

    return 0


def check_plan_review(root: Path) -> int:
    plan = root / "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-live-gated-execution-plan-2026-06-07.md"
    ledger = root / "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-live-gated-execution-claude-review-ledger-2026-06-07.md"
    amendment = root / "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-live-gated-execution-human-risk-acceptance-amendment-2026-06-08.md"
    for path in (plan, ledger):
        if not path.is_file():
            return fail(f"missing plan review artifact: {path}")
    plan_text = plan.read_text(encoding="utf-8")
    ledger_status = latest_status(ledger)
    if PLAN_READY_TOKEN in plan_text:
        if ledger_status != PLAN_REVIEW_PASS_TOKEN:
            return fail(f"plan review ledger latest status is {ledger_status!r}")
        return 0

    if HUMAN_RISK_ACCEPTED_TOKEN not in plan_text:
        return fail(f"execution plan is not launch-ready: {plan}")
    if ledger_status != PLAN_REVIEW_STOP_TOKEN:
        return fail(
            "human risk override requires stopped Claude review ledger status, "
            f"got {ledger_status!r}"
        )
    if not amendment.is_file():
        return fail(f"missing human risk acceptance amendment: {amendment}")
    amendment_text = amendment.read_text(encoding="utf-8")
    if latest_status(amendment) != HUMAN_RISK_ACCEPTED_TOKEN:
        return fail(f"human risk acceptance amendment status is {latest_status(amendment)!r}")
    for required_text in (
        "does not relabel the Claude review as PASS",
        "governance controls",
        "rename/copy source paths",
        "PASS_FOR_HUMAN_RISK_ACCEPTED_LAUNCH_PREFLIGHT_ONLY",
    ):
        if required_text not in amendment_text:
            return fail(f"human risk acceptance amendment lacks {required_text!r}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--phase", choices=sorted(PHASES))
    parser.add_argument("--run-id")
    parser.add_argument("--run-dir")
    parser.add_argument("--check-plan-review", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if args.check_plan_review:
        return check_plan_review(root)
    if not args.phase or not args.run_id:
        parser.error("--phase and --run-id are required unless --check-plan-review is used")
    status = check_phase(root, args.phase, args.run_id)
    if status:
        return status
    if args.run_dir:
        manifest = Path(args.run_dir).resolve() / f"{args.phase}-command-manifest.json"
        if not manifest.is_file():
            return fail(f"{args.phase} missing command manifest: {manifest}")
        try:
            manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return fail(f"{args.phase} invalid command manifest JSON {manifest}: {exc}")
        if manifest_payload.get("run_id") != args.run_id:
            return fail(f"{args.phase} command manifest run_id mismatch")
        if manifest_payload.get("phase") != args.phase:
            return fail(f"{args.phase} command manifest phase mismatch")
        commands = manifest_payload.get("commands")
        if not isinstance(commands, list) or not commands:
            return fail(f"{args.phase} command manifest has no commands")
        for index, command_record in enumerate(commands):
            if not isinstance(command_record, dict):
                return fail(f"{args.phase} command manifest command {index} is not an object")
            if not command_record.get("command"):
                return fail(f"{args.phase} command manifest command {index} lacks command")
            if command_record.get("exit_code") != 0:
                return fail(f"{args.phase} command manifest command {index} exit_code is not 0")
            log_path = command_record.get("log_path")
            if not isinstance(log_path, str) or not log_path:
                return fail(f"{args.phase} command manifest command {index} lacks log_path")
            if Path(log_path).is_absolute():
                return fail(f"{args.phase} command manifest command {index} log_path must be relative")
            log_file = (Path(args.run_dir).resolve() / log_path).resolve()
            try:
                log_file.relative_to(Path(args.run_dir).resolve())
            except ValueError:
                return fail(f"{args.phase} command log escapes run_dir: {log_path}")
            if not log_file.is_file():
                return fail(f"{args.phase} command log missing: {log_file}")
            log_text = log_file.read_text(encoding="utf-8", errors="replace")
            for marker in (
                f"run_id: {args.run_id}",
                f"phase: {args.phase}",
                f"command_index: {index}",
                "exit_code: 0",
            ):
                if marker not in log_text:
                    return fail(f"{args.phase} command log {log_file} lacks marker {marker!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
