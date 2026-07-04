"""Build the Phase 1 dense-IAF migration taxonomy.

This script is intentionally read-only with respect to /home/chakwong/python.
It uses only the Python standard library, never imports legacy model code, and
does not load any artifact through BayesFilter.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import socket
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LEGACY_ROOT = Path("/home/chakwong/python")
ARTIFACT_ROOT = LEGACY_ROOT / "docs/plans/artifacts"
PRIOR_INVENTORY = Path(
    "docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-inventory-2026-07-03.json"
)
PRIOR_HANDOFF = Path(
    "docs/plans/bayesfilter-general-neutra-ssm-interface-visible-stop-handoff-2026-07-03.md"
)
MAX_DEPTH = 6
MAX_JSON_BYTES = 25_000_000
HASH_CHUNK_BYTES = 1024 * 1024
ARTIFACT_NAME_MARKERS = (
    "training_state",
    "replay_state",
    "dense_iaf",
    "paper_dense_iaf",
    "plain_dense_iaf",
)
SOURCE_MARKERS = (
    "paper_dense_iaf",
    "plain_dense_iaf",
    "dense_autoregressive_iaf",
    "DenseAutoregressiveIAFTransport",
    "_set_dense_iaf_params",
    "_reconstruct_transport",
    "training_state",
    "replay_state",
)
PROCESS_LOCAL_PATTERNS = (
    re.compile(r"\b0x[0-9a-fA-F]{6,}\b"),
    re.compile(r"\bobject at\b"),
    re.compile(r"\bid\s*\("),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    root = Path.cwd()
    output = Path(args.output)
    artifact_paths = discover_artifact_candidates()
    prior_paths = discover_prior_inventory_paths(root / PRIOR_INVENTORY)
    merged_paths = sorted(set(artifact_paths) | set(prior_paths), key=str)
    candidates = [classify_candidate(path, root / PRIOR_INVENTORY) for path in merged_paths]
    source_surfaces = discover_source_surfaces()
    counts = Counter(item["status"] for item in candidates)

    payload = {
        "schema": "bayesfilter.general_neutra_dense_iaf_artifact_migration.phase1_taxonomy.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "created_at_local_date": "2026-07-04",
        "hostname": socket.gethostname(),
        "python_executable": sys.executable,
        "cpu_gpu_status": "CPU-only/read-only taxonomy; no GPU/CUDA device was probed or used",
        "legacy_root": str(LEGACY_ROOT),
        "prior_inventory": str(PRIOR_INVENTORY),
        "prior_handoff": str(PRIOR_HANDOFF),
        "discovery_scope": {
            "artifact_root": str(ARTIFACT_ROOT),
            "max_depth": MAX_DEPTH,
            "artifact_name_markers": ARTIFACT_NAME_MARKERS,
            "source_markers": SOURCE_MARKERS,
            "json_parse_limit_bytes": MAX_JSON_BYTES,
            "notebook_scope": (
                "Notebook files are outside Phase 1 unless a discovered source "
                "or result artifact explicitly references one as required evidence."
            ),
        },
        "discovery_commands": [
            "find /home/chakwong/python/docs/plans/artifacts -maxdepth 6 "
            "\\( -iname '*training_state*.json' -o -iname '*replay_state*.json' "
            "-o -iname '*dense*iaf*.json' -o -iname '*paper_dense_iaf*.json' "
            "-o -iname '*plain_dense_iaf*.json' \\)",
            "rg -n \"paper_dense_iaf|plain_dense_iaf|dense_autoregressive_iaf|"
            "DenseAutoregressiveIAFTransport|training_state|replay_state\" "
            "/home/chakwong/python -g '*.py' -g '*.md' -g '*.json'",
        ],
        "classification_counts": dict(sorted(counts.items())),
        "candidate_count": len(candidates),
        "source_surface_count": len(source_surfaces),
        "candidate_artifacts": candidates,
        "source_surfaces": source_surfaces,
        "nonclaims": [
            "taxonomy only",
            "no BayesFilter loader reuse claim",
            "no migrated dense-IAF payload claim",
            "no HMC convergence claim",
            "no posterior correctness claim",
            "no sampler superiority claim",
            "no default policy change",
        ],
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output),
        "candidate_count": len(candidates),
        "source_surface_count": len(source_surfaces),
        "classification_counts": dict(sorted(counts.items())),
    }, indent=2, sort_keys=True))
    return 0


def discover_artifact_candidates() -> list[Path]:
    if not ARTIFACT_ROOT.exists():
        return []
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ARTIFACT_ROOT):
        current = Path(dirpath)
        depth = len(current.relative_to(ARTIFACT_ROOT).parts)
        if depth >= MAX_DEPTH:
            dirnames[:] = []
        for filename in filenames:
            lower = filename.lower()
            if lower.endswith(".json") and any(marker in lower for marker in ARTIFACT_NAME_MARKERS):
                out.append(current / filename)
    return out


def discover_prior_inventory_paths(prior_path: Path) -> list[Path]:
    if not prior_path.exists():
        return []
    try:
        data = json.loads(prior_path.read_text())
    except (OSError, json.JSONDecodeError):
        return []
    out: list[Path] = []
    for item in data.get("user_named_evidence_cells", []):
        add_existing_path(out, item.get("source_path"))
        add_existing_path(out, item.get("referenced_training_state_path"))
        add_existing_path(out, item.get("per_parameter_statistics_path"))
    for item in data.get("additional_artifacts_checked", []):
        add_existing_path(out, item.get("path"))
        add_existing_path(out, item.get("referenced_training_state_path"))
    return out


def add_existing_path(out: list[Path], value: Any) -> None:
    if not value:
        return
    path = Path(str(value))
    if not path.is_absolute():
        path = LEGACY_ROOT / path
    if path.exists():
        out.append(path)


def discover_source_surfaces() -> list[dict[str, Any]]:
    roots = [
        LEGACY_ROOT / "src",
        LEGACY_ROOT / "scripts",
        LEGACY_ROOT / "tests",
        LEGACY_ROOT / "docs/plans",
    ]
    out: list[dict[str, Any]] = []
    for base in roots:
        if not base.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            if any(part in {".git", "__pycache__", ".mypy_cache", ".pytest_cache"} for part in Path(dirpath).parts):
                dirnames[:] = []
                continue
            for filename in filenames:
                if not filename.endswith((".py", ".md", ".json")):
                    continue
                path = Path(dirpath) / filename
                try:
                    text = path.read_text(errors="ignore")
                except OSError:
                    continue
                markers = tuple(marker for marker in SOURCE_MARKERS if marker in text)
                if not markers:
                    continue
                try:
                    stat = path.stat()
                except OSError:
                    continue
                out.append({
                    "path": str(path),
                    "size_bytes": stat.st_size,
                    "sha256": sha256_file(path) if stat.st_size <= MAX_JSON_BYTES else None,
                    "markers": markers,
                    "role": classify_source_surface_role(path, markers),
                    "status": "not_migration_candidate",
                    "notes": "Source/result surface used for schema design or provenance, not a frozen transport payload.",
                })
    return sorted(out, key=lambda item: item["path"])


def classify_source_surface_role(path: Path, markers: tuple[str, ...]) -> str:
    text = str(path)
    if text.endswith("_transports.py"):
        return "legacy_transport_implementation_surface"
    if "_reconstruct_transport" in markers or "_set_dense_iaf_params" in markers:
        return "legacy_replay_helper_surface"
    if "/docs/plans/" in text:
        return "legacy_result_or_plan_surface"
    return "legacy_reference_surface"


def classify_candidate(path: Path, prior_path: Path) -> dict[str, Any]:
    item: dict[str, Any] = {
        "path": str(path),
        "status": "not_readable",
        "classification_reason": "",
        "size_bytes": None,
        "sha256": None,
        "json_parse_status": "not_attempted",
        "payload_status": "not_checked",
        "target_signature_status": "not_checked",
        "schema_status": "not_checked",
        "transport_kinds": [],
        "arm": None,
        "kind": None,
        "candidate_index": None,
        "step_size": None,
        "leapfrog": None,
        "max_rhat": None,
        "referenced_paths": [],
        "nonclaims": [
            "classification only",
            "not loaded through BayesFilter",
            "not HMC/posterior validity evidence",
        ],
    }
    try:
        stat = path.stat()
    except OSError as exc:
        item["classification_reason"] = f"stat failed: {exc}"
        return item
    item["size_bytes"] = stat.st_size
    try:
        item["sha256"] = sha256_file(path)
    except OSError as exc:
        item["classification_reason"] = f"hash failed: {exc}"
        return item
    if contains_process_local_identity(path):
        item["status"] = "unsafe_identity"
        item["classification_reason"] = "file text contains process-local identity pattern"
        return item
    if path.suffix.lower() != ".json":
        return classify_note_candidate(item, path, prior_path)
    if stat.st_size > MAX_JSON_BYTES:
        item["status"] = "too_large_for_bounded_payload_inspection"
        item["json_parse_status"] = "skipped_too_large"
        item["classification_reason"] = "JSON payload exceeds bounded parse limit"
        return item
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        item["status"] = "not_readable"
        item["json_parse_status"] = f"failed: {exc}"
        item["classification_reason"] = "JSON parse failed"
        return item
    item["json_parse_status"] = "parsed"
    item["arm"] = scalar_text(data.get("arm") or data.get("candidate_arm"))
    item["kind"] = scalar_text(data.get("kind") or data.get("schema") or data.get("schema_version"))
    item["candidate_index"] = first_scalar(data, ("candidate_index", "candidate"))
    item["step_size"] = first_scalar(data, ("step_size", "epsilon", "epsilon_final"))
    item["leapfrog"] = first_scalar(data, ("leapfrog", "l_final", "L"))
    item["max_rhat"] = first_scalar(data, ("max_rhat", "rhat_max"))
    item["transport_kinds"] = sorted(find_transport_kinds(data))
    item["referenced_paths"] = resolve_referenced_paths(data)
    if not all_finite_json_scalars(data):
        item["status"] = "ambiguous_needs_manual_review"
        item["classification_reason"] = "JSON contains nonfinite numeric scalar"
        return item
    has_dense_marker = has_dense_iaf_marker(path, data, item["transport_kinds"])
    has_embedded_transport = isinstance(data, dict) and (
        "transport_state" in data or "transport" in data
    )
    has_generic_signature = has_key_recursive(data, {
        "target_signature",
        "generic_target_signature",
        "ssm_target_signature",
    })
    has_legacy_target = has_key_recursive(data, {"target", "target_identity", "target_constants"})
    if not has_dense_marker:
        item["status"] = "not_migration_candidate"
        item["payload_status"] = "no_dense_iaf_marker"
        item["target_signature_status"] = "not_applicable"
        item["schema_status"] = "not_applicable"
        item["classification_reason"] = "No dense-IAF marker found in name or payload"
        return item
    if has_embedded_transport:
        item["payload_status"] = "embedded_transport_payload_present"
        item["schema_status"] = "legacy_training_or_replay_schema"
        if has_generic_signature:
            item["status"] = "schema_candidate"
            item["target_signature_status"] = "generic_signature_present_not_checked_for_match"
            item["classification_reason"] = "Embedded dense-IAF payload and generic target signature are present; schema compatibility still not checked"
        else:
            item["status"] = "missing_target_signature"
            item["target_signature_status"] = (
                "legacy target metadata present but generic SSMTargetContract target_signature absent"
                if has_legacy_target
                else "generic SSMTargetContract target_signature absent"
            )
            item["classification_reason"] = "Embedded dense-IAF payload exists but generic target signature is missing"
        return item
    if item["referenced_paths"]:
        item["payload_status"] = "references_external_payload_or_replay"
        item["schema_status"] = "summary_or_diagnostic_schema"
        item["target_signature_status"] = "generic SSMTargetContract target_signature absent"
        item["status"] = "missing_payload"
        item["classification_reason"] = "Artifact is a summary/diagnostic or latest state that references payload elsewhere"
        return item
    if "per_parameter_statistics" in path.name:
        item["payload_status"] = "diagnostic_statistics_only"
        item["schema_status"] = "not_transport_payload"
        item["target_signature_status"] = "not_applicable"
        item["status"] = "not_migration_candidate"
        item["classification_reason"] = "Per-parameter statistics are diagnostics, not a frozen transport payload"
        return item
    item["status"] = "missing_payload"
    item["payload_status"] = "dense_iaf_marker_without_embedded_transport"
    item["schema_status"] = "not_transport_payload"
    item["target_signature_status"] = "generic SSMTargetContract target_signature absent"
    item["classification_reason"] = "Dense-IAF marker found but no embedded transport payload was found"
    return item


def classify_note_candidate(item: dict[str, Any], path: Path, prior_path: Path) -> dict[str, Any]:
    item["json_parse_status"] = "not_json"
    item["schema_status"] = "result_note_not_transport_payload"
    item["target_signature_status"] = "generic SSMTargetContract target_signature absent"
    item["payload_status"] = "result_note_or_plan_only"
    prior = load_prior_by_path(prior_path, str(path))
    prior_classification = prior.get("classification")
    if prior_classification == "missing_payload":
        item["status"] = "missing_payload"
        item["classification_reason"] = "Prior inventory classified referenced payload as missing"
    elif prior_classification:
        item["status"] = "missing_target_signature"
        item["classification_reason"] = f"Prior inventory classification: {prior_classification}"
    else:
        item["status"] = "not_migration_candidate"
        item["classification_reason"] = "Result note is provenance only"
    for field in ("candidate_index", "step_size", "leapfrog", "max_rhat"):
        if field in prior:
            item[field] = prior[field]
    item["kind"] = "markdown_result_note"
    return item


def load_prior_by_path(prior_path: Path, wanted: str) -> dict[str, Any]:
    if not prior_path.exists():
        return {}
    try:
        data = json.loads(prior_path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    for group in ("user_named_evidence_cells", "additional_artifacts_checked"):
        for item in data.get(group, []):
            paths = [
                item.get("source_path"),
                item.get("path"),
                item.get("referenced_training_state_path"),
                item.get("per_parameter_statistics_path"),
            ]
            if wanted in {str(path) for path in paths if path}:
                return item
    return {}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(HASH_CHUNK_BYTES)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def contains_process_local_identity(path: Path) -> bool:
    try:
        text = path.read_text(errors="ignore")
    except OSError:
        return False
    return any(pattern.search(text) for pattern in PROCESS_LOCAL_PATTERNS)


def scalar_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    return None


def first_scalar(data: Any, keys: tuple[str, ...]) -> Any:
    for key in keys:
        found = find_key_values(data, key)
        for value in found:
            if isinstance(value, (str, int, float, bool)) or value is None:
                return value
    return None


def find_transport_kinds(value: Any) -> set[str]:
    out: set[str] = set()
    if isinstance(value, dict):
        type_value = value.get("type")
        if isinstance(type_value, str):
            out.add(type_value)
        for item in value.values():
            out.update(find_transport_kinds(item))
    elif isinstance(value, list):
        for item in value:
            out.update(find_transport_kinds(item))
    return out


def resolve_referenced_paths(data: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for key in (
        "replay_state_path",
        "training_state_path",
        "source_json_output",
        "latest_json",
        "progress_jsonl",
    ):
        for value in find_key_values(data, key):
            if not isinstance(value, str) or not value:
                continue
            path = Path(value)
            if not path.is_absolute():
                path = LEGACY_ROOT / path
            out.append({
                "field": key,
                "path": str(path),
                "exists": path.exists(),
                "size_bytes": path.stat().st_size if path.exists() else None,
            })
    return out


def find_key_values(value: Any, key: str) -> list[Any]:
    out: list[Any] = []
    if isinstance(value, dict):
        if key in value:
            out.append(value[key])
        for item in value.values():
            out.extend(find_key_values(item, key))
    elif isinstance(value, list):
        for item in value:
            out.extend(find_key_values(item, key))
    return out


def has_key_recursive(value: Any, keys: set[str]) -> bool:
    if isinstance(value, dict):
        if any(key in value for key in keys):
            return True
        return any(has_key_recursive(item, keys) for item in value.values())
    if isinstance(value, list):
        return any(has_key_recursive(item, keys) for item in value)
    return False


def has_dense_iaf_marker(path: Path, data: Any, transport_kinds: list[str]) -> bool:
    lower = path.name.lower()
    if any(marker in lower for marker in ARTIFACT_NAME_MARKERS):
        return True
    if any("dense" in kind and "iaf" in kind for kind in transport_kinds):
        return True
    arm_values = find_key_values(data, "arm") + find_key_values(data, "candidate_arm")
    return any(isinstance(value, str) and "dense_iaf" in value for value in arm_values)


def all_finite_json_scalars(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(all_finite_json_scalars(item) for item in value.values())
    if isinstance(value, list):
        return all(all_finite_json_scalars(item) for item in value)
    return True


if __name__ == "__main__":
    raise SystemExit(main())
