#!/usr/bin/env python3
"""Build the Rotemberg Phase 2 target-contract manifest draft.

This helper assembles only metadata already classified in the Phase 1
inventory.  It does not import BayesFilter contract classes, execute legacy
model code, load transports, or prove a stable SSMTargetContract signature.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "bayesfilter.rotemberg_target_contract_reconstruction.phase2_manifest.v1"
STATUS = "PHASE2_MANIFEST_DRAFT_READY_FOR_PHASE3_VALIDATION"
PROCESS_LOCAL_PATTERNS = (
    re.compile(r"\b0x[0-9a-fA-F]+\b"),
    re.compile(r"\bobject at\b"),
    re.compile(r"\bid\s*\("),
)
REQUIRED_MANIFEST_SECTIONS = (
    "problem",
    "chart",
    "prior",
    "filter_program",
)
REQUIRED_CLASSIFICATION_PREFIXES = (
    "SSMTargetContract.problem.",
    "SSMTargetContract.chart.",
    "SSMTargetContract.prior.",
    "SSMTargetContract.filter_program.",
)
FORBIDDEN_PHASE2_FIELDS = ("frozen_transport",)


class ManifestDraftError(ValueError):
    """Raised when Phase 1 evidence cannot safely form a Phase 2 draft."""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Phase 1 inventory JSON")
    parser.add_argument("--output", required=True, help="Phase 2 manifest JSON")
    args = parser.parse_args()

    inventory_path = Path(args.input)
    output_path = Path(args.output)
    inventory = _read_json(inventory_path)

    manifest = _build_manifest(inventory, inventory_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output_path),
                "status": manifest["status"],
                "manifest_payload_sha256": manifest["manifest_payload_sha256"],
                "state_dim": manifest["target_contract_manifest"]["problem"][
                    "static_shape"
                ]["state_dim"],
                "structural_state_dim": manifest["target_contract_manifest"][
                    "problem"
                ]["model_manifest"]["structural_state_dim"],
                "frozen_transport_present": "frozen_transport"
                in manifest["target_contract_manifest"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _build_manifest(inventory: dict[str, Any], inventory_path: Path) -> dict[str, Any]:
    if inventory.get("schema") != "bayesfilter.rotemberg_target_contract_reconstruction.phase1_inventory.v1":
        raise ManifestDraftError("input is not the expected Phase 1 inventory schema")

    draft = _copy_jsonable(inventory.get("draft_contract_manifest"))
    if not isinstance(draft, dict):
        raise ManifestDraftError("Phase 1 inventory missing draft_contract_manifest")
    if draft.get("status") != "draft_not_canonical_signature":
        raise ManifestDraftError("Phase 1 draft status is not fail-closed")
    for field in FORBIDDEN_PHASE2_FIELDS:
        if field in draft:
            raise ManifestDraftError(f"Phase 2 draft must not include {field}")
    for section in REQUIRED_MANIFEST_SECTIONS:
        if section not in draft:
            raise ManifestDraftError(f"target_contract_manifest missing {section}")

    _validate_static_decision(draft, inventory)
    _validate_field_coverage(inventory)
    _reject_process_local_identity(draft)

    payload_hash = _stable_hash(draft)
    classifications = inventory.get("required_field_classifications", {})
    state_dim_classification = classifications.get(
        "SSMTargetContract.problem.static_shape.state_dim", {}
    )
    field_status_counts = _status_counts(classifications)

    out: dict[str, Any] = {
        "schema": SCHEMA,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "created_at_local_date": "2026-07-04",
        "hostname": socket.gethostname(),
        "python_executable": sys.executable,
        "status": STATUS,
        "phase1_inventory_path": str(inventory_path),
        "phase1_inventory_sha256": _file_sha256(inventory_path),
        "target_contract_manifest": draft,
        "manifest_payload_sha256": payload_hash,
        "state_dimension_decision": {
            "decision": "use_bayesfilter_computational_state_dim_for_generic_signature",
            "generic_target_state_dim": draft["problem"]["static_shape"]["state_dim"],
            "model_manifest_structural_state_dim": draft["problem"][
                "model_manifest"
            ]["structural_state_dim"],
            "state_dim_candidates": inventory["field_support"]["static_shape"][
                "state_dim_candidates"
            ],
            "evidence": state_dim_classification.get("evidence", []),
            "note": state_dim_classification.get("note"),
        },
        "field_coverage": {
            "required_field_count": len(classifications),
            "status_counts": field_status_counts,
            "unsupported_required_fields": [
                name
                for name, row in sorted(classifications.items())
                if row.get("status")
                not in {
                    "supported",
                    "supported_with_semantic_decision_required",
                    "not_applicable_untransported_signature",
                }
            ],
            "transport_field_status": classifications.get(
                "SSMTargetContract.frozen_transport"
            ),
        },
        "source_records": inventory.get("source_records", {}),
        "source_anchors": inventory.get("source_anchors", {}),
        "artifact_presence": inventory.get("artifact_presence", {}),
        "blockers_carried_forward": _carried_blockers(inventory),
        "validation_limits": [
            "Phase 2 validates manifest shape and evidence coverage only",
            "BayesFilter SSMTargetContract instantiation is reserved for Phase 3",
            "stable_ssm_target_signature is reserved for Phase 3",
            "frozen transport binding is absent from the Phase 2 manifest",
        ],
        "cpu_gpu_status": (
            "CPU-only metadata manifest draft; no GPU/CUDA device was probed or used"
        ),
        "network_status": "No network fetch",
        "external_mutation": "None; /home/chakwong/python was not modified",
        "nonclaims": [
            "manifest draft only",
            "no canonical SSMTargetContract validation claim",
            "no stable target signature proof",
            "no historical transport payload exported",
            "no historical artifact loaded through BayesFilter",
            "no HMC convergence claim",
            "no posterior correctness claim",
            "no sampler superiority claim",
            "no GPU readiness claim",
            "no default policy change",
        ],
    }
    _reject_process_local_identity(out)
    return out


def _validate_static_decision(draft: dict[str, Any], inventory: dict[str, Any]) -> None:
    static_shape = draft["problem"]["static_shape"]
    model_manifest = draft["problem"]["model_manifest"]
    expected_shape = {
        "horizon": 40,
        "state_dim": 6,
        "observation_dim": 3,
        "innovation_dim": 3,
        "parameter_dim": 15,
    }
    if static_shape != expected_shape:
        raise ManifestDraftError(
            f"unexpected static_shape {static_shape!r}; expected {expected_shape!r}"
        )
    if model_manifest.get("structural_state_dim") != 4:
        raise ManifestDraftError("structural_state_dim=4 must be preserved as metadata")
    if inventory["field_support"]["static_shape"]["status"] != (
        "supported_with_semantic_decision_required"
    ):
        raise ManifestDraftError("state_dim decision status missing from Phase 1")


def _validate_field_coverage(inventory: dict[str, Any]) -> None:
    classifications = inventory.get("required_field_classifications")
    if not isinstance(classifications, dict) or not classifications:
        raise ManifestDraftError("required field classifications are missing")
    covered_prefixes = {
        prefix
        for prefix in REQUIRED_CLASSIFICATION_PREFIXES
        if any(key.startswith(prefix) for key in classifications)
    }
    missing_prefixes = set(REQUIRED_CLASSIFICATION_PREFIXES) - covered_prefixes
    if missing_prefixes:
        raise ManifestDraftError(
            "missing required classification prefixes: "
            + ", ".join(sorted(missing_prefixes))
        )
    frozen = classifications.get("SSMTargetContract.frozen_transport")
    if frozen is None:
        raise ManifestDraftError("frozen_transport non-applicability is not recorded")
    if frozen.get("status") != "not_applicable_untransported_signature":
        raise ManifestDraftError("frozen_transport must remain not applicable in Phase 2")
    unsupported = [
        key
        for key, row in classifications.items()
        if row.get("status")
        not in {
            "supported",
            "supported_with_semantic_decision_required",
            "not_applicable_untransported_signature",
        }
    ]
    if unsupported:
        raise ManifestDraftError(
            "unsupported required fields remain: " + ", ".join(sorted(unsupported))
        )


def _carried_blockers(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    blockers = []
    for item in inventory.get("blockers", []):
        copied = dict(item)
        if item.get("code") == "BLOCK_STATE_DIM_SEMANTIC_DECISION":
            copied["phase2_resolution"] = (
                "resolved for manifest draft by using computational state_dim=6 "
                "and preserving structural_state_dim=4 as model metadata"
            )
        elif item.get("code") == "BLOCK_SERIOUS_BASELINE_PAYLOAD_ABSENT_LOCALLY":
            copied["phase2_resolution"] = (
                "not resolved; payload export/load remains out of scope"
            )
        blockers.append(copied)
    return blockers


def _status_counts(classifications: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in classifications.values():
        status = str(row.get("status"))
        counts[status] = counts.get(status, 0) + 1
    return dict(sorted(counts.items()))


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_jsonable(value: Any) -> Any:
    return json.loads(json.dumps(value, sort_keys=True))


def _stable_hash(payload: Any) -> str:
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    _reject_process_local_identity(blob)
    return "sha256:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _reject_process_local_identity(value: Any) -> None:
    text = json.dumps(value, sort_keys=True, default=str)
    if any(pattern.search(text) for pattern in PROCESS_LOCAL_PATTERNS):
        raise ManifestDraftError("manifest contains process-local identity")


if __name__ == "__main__":
    raise SystemExit(main())
