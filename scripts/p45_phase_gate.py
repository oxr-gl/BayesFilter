from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path


STATUS_RE = re.compile(r"^\s*status:\s*`([^`]+)`\s*\.?\s*$", re.IGNORECASE)
STATUS_CAP_RE = re.compile(r"^\s*Status:\s*`([^`]+)`\s*\.?\s*$")
VERDICT_RE = re.compile(r"^\s*Verdict:\s*`([^`]+)`\s*\.?\s*$", re.IGNORECASE)
RUN_ID_RE = re.compile(r"^\s*run_id:\s*`([^`]+)`\s*\.?\s*$", re.IGNORECASE)
REVIEW_CYCLE_RE = re.compile(r"^\s*review_cycle:\s*`?([0-9]+)`?\s*\.?\s*$", re.IGNORECASE)
REVIEW_ITERATION_RE = re.compile(r"^\s*review_iteration:\s*`?([0-9]+)`?\s*\.?\s*$", re.IGNORECASE)
REVIEW_TYPE_RE = re.compile(r"^\s*review_type:\s*`?([A-Za-z0-9_.-]+)`?\s*\.?\s*$", re.IGNORECASE)
GENERIC_MARKER_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+):\s*`?([^`]+?)`?\s*\.?\s*$")


PHASE_SLUGS = {
    "P45-M0": "target-governance",
    "P45-M1": "multistate-zhaocui-route",
    "P45-M2": "generalized-sv-comparison",
    "P45-M3": "spatial-sir-comparison",
    "P45-M4": "predator-prey-comparison",
    "P45-M5": "cross-model-error-calibration",
    "P45-M6": "integration-closeout",
}


REQUIRED_EVIDENCE_STATES = (
    "PHASE_PLAN_CONFIRMED",
    "SKEPTICAL_AUDIT_RECORDED",
    "CLAUDE_PLAN_OR_REPAIR_REVIEW_PASS",
    "IMPLEMENTED",
    "LOCAL_EVIDENCE_RUN",
    "EVIDENCE_AUDIT_RECORDED",
    "RESULT_NOTE_WRITTEN",
    "CLAUDE_CODE_GOVERNANCE_PASS",
    "TRACEABILITY_UPDATED_OR_NONCLAIM_RECORDED",
    "PHASE_PASS",
)

REQUIRED_EVIDENCE_CONTRACT_FIELDS = (
    "question",
    "baseline_or_comparator",
    "primary_promotion_criterion",
    "veto_diagnostics",
    "explanatory_only_diagnostics",
    "nonclaims",
)


def _marker(path: Path, key: str) -> str | None:
    latest: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        marker_match = GENERIC_MARKER_RE.match(line)
        if marker_match and marker_match.group(1).lower() == key.lower():
            latest = marker_match.group(2).strip()
    return latest


def _latest_status(path: Path) -> str | None:
    latest: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        status_match = STATUS_RE.match(line) or STATUS_CAP_RE.match(line)
        if status_match:
            latest = status_match.group(1)
    return latest


def _status_equals(path: Path, expected: str) -> bool:
    return _latest_status(path) == expected


def _latest_status_or_verdict(path: Path) -> str | None:
    latest: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        status_match = STATUS_RE.match(line) or STATUS_CAP_RE.match(line) or VERDICT_RE.match(line)
        if status_match:
            latest = status_match.group(1)
    return latest


def _latest_review_cycle(path: Path) -> int | None:
    latest: int | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        cycle_match = REVIEW_CYCLE_RE.match(line)
        if cycle_match:
            latest = int(cycle_match.group(1))
    return latest


def _latest_review_iteration(path: Path) -> int | None:
    latest: int | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        iteration_match = REVIEW_ITERATION_RE.match(line)
        if iteration_match:
            latest = int(iteration_match.group(1))
    return latest


def _review_records(path: Path) -> list[dict[str, int | str | None]]:
    records: list[dict[str, int | str | None]] = []
    current_cycle: int | None = None
    current_iteration: int | None = None
    current_type: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        cycle_match = REVIEW_CYCLE_RE.match(line)
        if cycle_match:
            current_cycle = int(cycle_match.group(1))
            current_iteration = None
            current_type = None
            continue
        type_match = REVIEW_TYPE_RE.match(line)
        if type_match:
            current_type = type_match.group(1).strip().lower()
            continue
        iteration_match = REVIEW_ITERATION_RE.match(line)
        if iteration_match:
            current_iteration = int(iteration_match.group(1))
            continue
        status_match = STATUS_RE.match(line) or STATUS_CAP_RE.match(line) or VERDICT_RE.match(line)
        if status_match:
            records.append(
                {
                    "cycle": current_cycle,
                    "iteration": current_iteration,
                    "type": current_type,
                    "status": status_match.group(1),
                }
            )
    return records


def _cycle_records(path: Path, cycle: int) -> list[dict[str, int | str | None]]:
    return [
        record
        for record in _review_records(path)
        if record["cycle"] == cycle and isinstance(record["iteration"], int)
    ]


def _validated_latest_cycle_record(
    path: Path,
    cycle: int,
    expected_status: str,
    max_iteration: int,
) -> dict[str, int | str | None] | None:
    records = _cycle_records(path, cycle)
    if not records:
        print(f"{path} has no review records for cycle {cycle}", file=sys.stderr)
        return None

    previous_iteration = 0
    seen_iterations: set[int] = set()
    for record in records:
        iteration = record["iteration"]
        if not isinstance(iteration, int):
            print(f"{path} has non-integer review iteration in record {record!r}", file=sys.stderr)
            return None
        if iteration < 1 or iteration > max_iteration:
            print(f"{path} review iteration {iteration} is outside 1..{max_iteration}", file=sys.stderr)
            return None
        if iteration <= previous_iteration:
            print(f"{path} review iteration history is not strictly increasing at {record!r}", file=sys.stderr)
            return None
        if iteration in seen_iterations:
            print(f"{path} review iteration {iteration} is duplicated", file=sys.stderr)
            return None
        seen_iterations.add(iteration)
        previous_iteration = iteration

    latest = records[-1]
    if latest["status"] != expected_status:
        print(f"{path} latest cycle {cycle} record is {latest!r}, not {expected_status}", file=sys.stderr)
        return None
    if latest["iteration"] != max(seen_iterations):
        print(f"{path} latest cycle {cycle} record is not the max iteration record", file=sys.stderr)
        return None
    return latest


def _validated_latest_review_record(
    records: Sequence[dict[str, int | str | None]],
    expected_status: str,
    label: str,
    max_iteration: int = 5,
) -> dict[str, int | str | None] | None:
    if not records:
        print(f"{label} has no machine-parseable review records", file=sys.stderr)
        return None

    previous_iteration = 0
    seen_iterations: set[int] = set()
    for record in records:
        if record.get("cycle") is None:
            print(f"{label} review record lacks review_cycle: {record!r}", file=sys.stderr)
            return None
        iteration = record["iteration"]
        if not isinstance(iteration, int):
            print(f"{label} has non-integer review iteration in {record!r}", file=sys.stderr)
            return None
        if iteration < 1 or iteration > max_iteration:
            print(f"{label} review iteration {iteration} is outside 1..{max_iteration}", file=sys.stderr)
            return None
        if iteration <= previous_iteration:
            print(f"{label} review iteration history is not strictly increasing at {record!r}", file=sys.stderr)
            return None
        if iteration in seen_iterations:
            print(f"{label} review iteration {iteration} is duplicated", file=sys.stderr)
            return None
        seen_iterations.add(iteration)
        previous_iteration = iteration

    latest = records[-1]
    if latest["status"] != expected_status:
        print(f"{label} latest review record is {latest!r}, not {expected_status}", file=sys.stderr)
        return None
    if latest["iteration"] != max(seen_iterations):
        print(f"{label} latest review record is not the max iteration record", file=sys.stderr)
        return None
    return latest


def _latest_run_id(path: Path) -> str | None:
    latest: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        run_id_match = RUN_ID_RE.match(line)
        if run_id_match:
            latest = run_id_match.group(1)
    return latest


def _phase_artifacts(root: Path, phase: str, run_id: str) -> tuple[Path, Path, Path]:
    phase_upper = phase.upper()
    if phase_upper not in PHASE_SLUGS:
        known = ", ".join(sorted(PHASE_SLUGS))
        raise ValueError(f"unknown phase {phase!r}; expected one of {known}")
    phase_num = phase_upper.split("M", 1)[1]
    slug = PHASE_SLUGS[phase_upper]
    docs = root / "docs" / "plans"
    stem = f"bayesfilter-highdim-zhao-cui-p45-phase{phase_num}-{slug}"
    return (
        docs / f"{stem}-result-2026-06-08.md",
        docs / f"{stem}-claude-review-ledger-2026-06-08.md",
        docs / f"{stem}-evidence-manifest-{run_id}.json",
    )


def _nonempty(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return len(value) > 0
    if isinstance(value, Mapping):
        return len(value) > 0
    return value is not None


def _is_relative_repo_path(value: object) -> bool:
    return isinstance(value, str) and value.strip() and not Path(value).is_absolute() and ".." not in Path(value).parts


def _path_exists(root: Path, value: object) -> bool:
    return _is_relative_repo_path(value) and (root / str(value)).exists()


def _require_manifest(root: Path, manifest_path: Path, phase: str, token: str, run_id: str, result: Path, review: Path) -> bool:
    if not manifest_path.exists():
        print(f"missing phase evidence manifest: {manifest_path}", file=sys.stderr)
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"invalid phase evidence manifest JSON: {manifest_path}: {exc}", file=sys.stderr)
        return False
    if not isinstance(manifest, dict):
        print("phase evidence manifest must be a JSON object", file=sys.stderr)
        return False

    expected = {
        "schema_version": "p45.phase_evidence.v1",
        "run_id": run_id,
        "phase": phase.upper(),
        "pass_token": token,
        "status": token,
    }
    for key, expected_value in expected.items():
        if manifest.get(key) != expected_value:
            print(f"manifest {key} is {manifest.get(key)!r}, not {expected_value!r}", file=sys.stderr)
            return False

    expected_paths = {
        "result_note": result.relative_to(root).as_posix(),
        "claude_review_ledger": review.relative_to(root).as_posix(),
        "evidence_manifest": manifest_path.relative_to(root).as_posix(),
    }
    paths = manifest.get("artifact_paths")
    if not isinstance(paths, dict):
        print("manifest artifact_paths must be an object", file=sys.stderr)
        return False
    for key, expected_path in expected_paths.items():
        if paths.get(key) != expected_path:
            print(f"manifest artifact_paths.{key} is {paths.get(key)!r}, not {expected_path!r}", file=sys.stderr)
            return False
        if not _path_exists(root, paths.get(key)):
            print(f"manifest artifact_paths.{key} does not exist: {paths.get(key)!r}", file=sys.stderr)
            return False

    manifest_rel = manifest_path.relative_to(root).as_posix()
    result_required_markers = {
        "p45_evidence_manifest": manifest_rel,
        "p45_local_evidence_run": "COMPLETE",
        "p45_evidence_audit": "COMPLETE",
        "p45_result_note_substance": "COMPLETE",
        "p45_traceability_or_nonclaim": "COMPLETE",
    }
    for marker, expected_value in result_required_markers.items():
        actual_value = _marker(result, marker)
        if actual_value != expected_value:
            print(f"phase result marker {marker} is {actual_value!r}, not {expected_value!r}", file=sys.stderr)
            return False

    review_required_markers = {
        "p45_evidence_manifest": manifest_rel,
        "p45_claude_code_governance_verdict": token,
    }
    for marker, expected_value in review_required_markers.items():
        actual_value = _marker(review, marker)
        if actual_value != expected_value:
            print(f"phase review marker {marker} is {actual_value!r}, not {expected_value!r}", file=sys.stderr)
            return False

    states = manifest.get("evidence_chain")
    if not isinstance(states, dict):
        print("manifest evidence_chain must be an object", file=sys.stderr)
        return False
    for state in REQUIRED_EVIDENCE_STATES:
        if states.get(state) is not True:
            print(f"manifest evidence_chain.{state} is not true", file=sys.stderr)
            return False

    contract = manifest.get("evidence_contract")
    if not isinstance(contract, dict):
        print("manifest evidence_contract must be an object", file=sys.stderr)
        return False
    for field in REQUIRED_EVIDENCE_CONTRACT_FIELDS:
        if not _nonempty(contract.get(field)):
            print(f"manifest evidence_contract.{field} is empty", file=sys.stderr)
            return False

    commands = manifest.get("commands")
    if not isinstance(commands, list) or not commands:
        print("manifest commands must be a nonempty list", file=sys.stderr)
        return False
    result_command_count = _marker(result, "p45_command_count")
    if result_command_count != str(len(commands)):
        print(f"phase result marker p45_command_count is {result_command_count!r}, not {len(commands)!r}", file=sys.stderr)
        return False
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            print(f"manifest commands[{index}] must be an object", file=sys.stderr)
            return False
        for key in ("purpose", "command", "exit_code"):
            if key not in command:
                print(f"manifest commands[{index}].{key} is missing", file=sys.stderr)
                return False
        if not _nonempty(command["purpose"]) or not _nonempty(command["command"]):
            print(f"manifest commands[{index}] purpose/command is empty", file=sys.stderr)
            return False
        if command["exit_code"] != 0:
            print(f"manifest commands[{index}].exit_code is {command['exit_code']!r}, not 0", file=sys.stderr)
            return False
        log_path = command.get("log_path")
        if not _path_exists(root, log_path):
            print(f"manifest commands[{index}].log_path does not exist: {log_path!r}", file=sys.stderr)
            return False
        log_file = root / str(log_path)
        command_markers = {
            "p45_run_id": run_id,
            "p45_phase": phase.upper(),
            "p45_command_index": str(index),
            "p45_command_exit_code": "0",
        }
        for marker, expected_value in command_markers.items():
            actual_value = _marker(log_file, marker)
            if actual_value != expected_value:
                print(
                    f"command log {log_path!r} marker {marker} is {actual_value!r}, not {expected_value!r}",
                    file=sys.stderr,
                )
                return False

    diagnostics = manifest.get("diagnostics")
    if not isinstance(diagnostics, dict):
        print("manifest diagnostics must be an object", file=sys.stderr)
        return False
    if diagnostics.get("veto_status") not in {"PASS", "NONCLAIM_RECORDED"}:
        print("manifest diagnostics.veto_status must be PASS or NONCLAIM_RECORDED", file=sys.stderr)
        return False
    if not _nonempty(diagnostics.get("summary")):
        print("manifest diagnostics.summary is empty", file=sys.stderr)
        return False

    reviews = manifest.get("review_loops")
    if not isinstance(reviews, dict):
        print("manifest review_loops must be an object", file=sys.stderr)
        return False
    for key in ("claude_code_governance", "repair"):
        loop = reviews.get(key)
        if not isinstance(loop, dict):
            print(f"manifest review_loops.{key} must be an object", file=sys.stderr)
            return False
        iterations = loop.get("iterations")
        if not isinstance(iterations, int) or iterations < 0 or iterations > 5:
            print(f"manifest review_loops.{key}.iterations must be between 0 and 5", file=sys.stderr)
            return False
    code_loop = reviews["claude_code_governance"]
    if code_loop.get("iterations", 0) < 1 or code_loop.get("verdict") != token:
        print("manifest Claude code/governance loop lacks required pass verdict", file=sys.stderr)
        return False
    review_iterations = _marker(review, "p45_claude_code_governance_iterations")
    if review_iterations != str(code_loop.get("iterations")):
        print(
            f"phase review marker p45_claude_code_governance_iterations is {review_iterations!r}, "
            f"not {code_loop.get('iterations')!r}",
            file=sys.stderr,
        )
        return False
    phase_records = _review_records(review)
    phase_code = phase.upper().replace("-", "_")
    code_records = [
        record
        for record in phase_records
        if (
            isinstance(record.get("iteration"), int)
            and record.get("cycle") is not None
            and record.get("type") == "code_governance"
            and record.get("status") in {token, f"BLOCKED_{phase_code}_CODE_GOVERNANCE"}
        )
    ]
    latest_code_record = _validated_latest_review_record(
        code_records,
        token,
        "phase code/governance review ledger",
    )
    if latest_code_record is None:
        return False
    if latest_code_record["iteration"] != code_loop.get("iterations"):
        print(
            f"manifest code/governance iterations {code_loop.get('iterations')!r} do not match "
            f"latest phase review iteration {latest_code_record['iteration']!r}",
            file=sys.stderr,
        )
        return False
    repair_loop = reviews["repair"]
    if repair_loop.get("iterations", 0) > 0:
        repair_verdict = repair_loop.get("verdict")
        repair_iterations = repair_loop.get("iterations")
        expected_repair_verdict = f"PASS_{phase_code}_REPAIR_REVIEW"
        if repair_verdict != expected_repair_verdict:
            print(
                f"manifest repair loop verdict is {repair_verdict!r}, not {expected_repair_verdict!r}",
                file=sys.stderr,
            )
            return False
        repair_records = [
            record
            for record in phase_records
            if (
                isinstance(record.get("iteration"), int)
                and record.get("cycle") is not None
                and record.get("type") == "repair"
                and record.get("status")
                in {
                    expected_repair_verdict,
                    f"BLOCKED_{phase_code}_REPAIR_REVIEW",
                }
            )
        ]
        latest_repair = _validated_latest_review_record(
            repair_records,
            repair_verdict,
            "phase repair review ledger",
        )
        if latest_repair is None:
            return False
        if latest_repair["iteration"] != repair_iterations:
            print(
                f"manifest repair iterations {repair_iterations!r} do not match "
                f"latest repair review iteration {latest_repair['iteration']!r}",
                file=sys.stderr,
            )
            return False

    long_run = manifest.get("long_run_controls")
    if not isinstance(long_run, dict):
        print("manifest long_run_controls must be an object", file=sys.stderr)
        return False
    if long_run.get("long_run_used") is True:
        if not _nonempty(long_run.get("resource_caps")) or not _nonempty(long_run.get("pre_mortem")):
            print("manifest long_run_controls needs resource_caps and pre_mortem for long runs", file=sys.stderr)
            return False
        long_run_markers = {
            "p45_long_run_used": "true",
            "p45_long_run_resource_caps": "COMPLETE",
            "p45_long_run_pre_mortem": "COMPLETE",
        }
    else:
        long_run_markers = {"p45_long_run_used": "false"}
    for marker, expected_value in long_run_markers.items():
        actual_value = _marker(result, marker)
        if actual_value != expected_value:
            print(f"phase result marker {marker} is {actual_value!r}, not {expected_value!r}", file=sys.stderr)
            return False

    return True


def _require_phase_token(root: Path, token: str, phase: str, run_id: str) -> bool:
    try:
        result, review, manifest = _phase_artifacts(root, phase, run_id)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return False

    for label, path in (("phase result", result), ("phase Claude review ledger", review)):
        if not path.exists():
            print(f"missing {label}: {path}", file=sys.stderr)
            return False
        latest = _latest_status_or_verdict(path)
        if latest != token:
            print(f"{label} latest status/verdict is {latest!r}, not {token}", file=sys.stderr)
            return False
        artifact_run_id = _latest_run_id(path)
        if artifact_run_id != run_id:
            print(f"{label} run_id is {artifact_run_id!r}, not {run_id!r}", file=sys.stderr)
            return False
    if not _require_manifest(root, manifest, phase, token, run_id, result, review):
        return False
    return True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="P45 overnight launch/phase gate.")
    parser.add_argument("--root", default="/home/chakwong/BayesFilter")
    parser.add_argument("--runbook-ledger")
    parser.add_argument("--execution-result")
    parser.add_argument("--phase")
    parser.add_argument("--token")
    parser.add_argument("--run-id")
    parser.add_argument("--review-cycle", type=int)
    parser.add_argument("--max-review-iteration", type=int)
    parser.add_argument("--check-runbook-pass", action="store_true")
    parser.add_argument("--check-plan-pass", action="store_true")
    parser.add_argument("--check-execution-ready", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if args.check_runbook_pass or args.check_plan_pass:
        ledger = Path(args.runbook_ledger) if args.runbook_ledger else root / "docs/plans/bayesfilter-highdim-zhao-cui-p45-generalized-sv-sir-predator-prey-comparison-claude-review-ledger-2026-06-08.md"
        if not ledger.exists():
            print(f"missing P45 plan review ledger: {ledger}", file=sys.stderr)
            return 2
        latest = _latest_status_or_verdict(ledger)
        if latest != "PASS_P45_PLAN_GOVERNANCE":
            print(
                f"P45 plan review ledger latest status/verdict is {latest!r}, not PASS_P45_PLAN_GOVERNANCE",
                file=sys.stderr,
            )
            return 2
        runbook_record = None
        if args.review_cycle is not None:
            runbook_record = _validated_latest_cycle_record(
                ledger,
                args.review_cycle,
                "PASS_P45_PLAN_GOVERNANCE",
                args.max_review_iteration or 5,
            )
            if runbook_record is None:
                return 2

    if args.check_execution_ready:
        result = Path(args.execution_result) if args.execution_result else root / "docs/plans/bayesfilter-highdim-zhao-cui-p45-overnight-gated-self-recovery-execution-result-2026-06-08.md"
        if not result.exists():
            print(f"missing execution result: {result}", file=sys.stderr)
            return 2
        latest = _latest_status_or_verdict(result)
        if latest != "READY_TO_LAUNCH_AFTER_P45_PLAN_PASS":
            print(
                f"execution result latest status/verdict is {latest!r}, not READY_TO_LAUNCH_AFTER_P45_PLAN_PASS",
                file=sys.stderr,
            )
            return 2
        execution_record = None
        if args.review_cycle is not None:
            execution_record = _validated_latest_cycle_record(
                result,
                args.review_cycle,
                "READY_TO_LAUNCH_AFTER_P45_PLAN_PASS",
                args.max_review_iteration or 5,
            )
            if execution_record is None:
                return 2

    if (args.check_runbook_pass or args.check_plan_pass) and args.check_execution_ready and args.review_cycle is not None:
        ledger = Path(args.runbook_ledger) if args.runbook_ledger else root / "docs/plans/bayesfilter-highdim-zhao-cui-p45-generalized-sv-sir-predator-prey-comparison-claude-review-ledger-2026-06-08.md"
        result = Path(args.execution_result) if args.execution_result else root / "docs/plans/bayesfilter-highdim-zhao-cui-p45-overnight-gated-self-recovery-execution-result-2026-06-08.md"
        runbook_record = _validated_latest_cycle_record(
            ledger,
            args.review_cycle,
            "PASS_P45_PLAN_GOVERNANCE",
            args.max_review_iteration or 5,
        )
        execution_record = _validated_latest_cycle_record(
            result,
            args.review_cycle,
            "READY_TO_LAUNCH_AFTER_P45_PLAN_PASS",
            args.max_review_iteration or 5,
        )
        if runbook_record is None or execution_record is None:
            return 2
        if runbook_record["iteration"] != execution_record["iteration"]:
            print(
                f"runbook pass iteration {runbook_record['iteration']!r} does not match "
                f"execution ready iteration {execution_record['iteration']!r}",
                file=sys.stderr,
            )
            return 2

    if args.phase or args.token:
        if not args.phase or not args.token or not args.run_id:
            print("--phase, --token, and --run-id must be provided together", file=sys.stderr)
            return 2
        if not _require_phase_token(root, args.token, args.phase, args.run_id):
            print(f"missing required token {args.token} for {args.phase}", file=sys.stderr)
            return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
