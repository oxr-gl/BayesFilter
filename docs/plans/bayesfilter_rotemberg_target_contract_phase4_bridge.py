#!/usr/bin/env python3
"""Run the Rotemberg Phase 4 bridge rerun in read-only mode.

This helper classifies the two embedded Rotemberg dense-IAF candidates from the
Phase 1 inventory against the validated Phase 2 manifest. It does not load
historical artifacts as reusable, execute legacy model code, export payloads,
or run HMC/training/GPU jobs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import socket
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "bayesfilter.rotemberg_target_contract_reconstruction.phase4_bridge.v1"
STATUS = "PHASE4_BLOCKED_NO_BRIDGEABLE_TARGET_SIGNATURE"
REQUIRED_FIELDS = (
    "problem_id",
    "static_shape",
    "data_signature",
    "chart",
    "prior",
    "filter_program",
)
EXPECTED_EMBEDDED_CANDIDATES = 2


class BridgeRerunError(ValueError):
    """Raised when the read-only bridge rerun cannot be classified safely."""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Phase 1 inventory JSON")
    parser.add_argument("--manifest", required=True, help="Phase 2 manifest JSON")
    parser.add_argument("--output", required=True, help="Phase 4 bridge JSON")
    args = parser.parse_args()

    inventory_path = Path(args.input)
    manifest_path = Path(args.manifest)
    output_path = Path(args.output)

    inventory = _read_json(inventory_path)
    manifest = _read_json(manifest_path)
    payload = _build_payload(inventory, manifest, inventory_path, manifest_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output_path),
                "status": payload["status"],
                "embedded_payload_candidate_count": payload["embedded_payload_candidate_count"],
                "bridgeable_count": payload["bridgeable_count"],
                "candidate_status_counts": payload["candidate_status_counts"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _build_payload(
    inventory: dict[str, Any],
    manifest: dict[str, Any],
    inventory_path: Path,
    manifest_path: Path,
) -> dict[str, Any]:
    if inventory.get("schema") != "bayesfilter.rotemberg_target_contract_reconstruction.phase1_inventory.v1":
        raise BridgeRerunError("input is not the expected Phase 1 inventory schema")
    if manifest.get("status") != "PHASE2_MANIFEST_DRAFT_READY_FOR_PHASE3_VALIDATION":
        raise BridgeRerunError("manifest is not the expected Phase 2 draft")
    target_contract_manifest = manifest.get("target_contract_manifest")
    if not isinstance(target_contract_manifest, dict):
        raise BridgeRerunError("Phase 2 manifest is missing target_contract_manifest")
    if "frozen_transport" in target_contract_manifest:
        raise BridgeRerunError("Phase 2 manifest must not include frozen_transport")
    canonical_field_set = tuple(REQUIRED_FIELDS)
    _require_canonical_sections(target_contract_manifest)

    embedded_rows = [
        row
        for row in inventory.get("rotemberg_embedded_payload_candidates", [])
        if row.get("is_embedded_payload_candidate")
    ]
    if len(embedded_rows) != EXPECTED_EMBEDDED_CANDIDATES:
        raise BridgeRerunError(
            f"expected {EXPECTED_EMBEDDED_CANDIDATES} embedded candidates, found {len(embedded_rows)}"
        )

    bridge_candidates = [
        _classify_candidate(row, canonical_field_set, target_contract_manifest)
        for row in embedded_rows
    ]
    candidate_status_counts = dict(sorted(Counter(row["bridge_status"] for row in bridge_candidates).items()))
    bridgeable_count = sum(row["bridge_status"] == "bridgeable_signature_defined" for row in bridge_candidates)

    if bridgeable_count == 0:
        status = STATUS
    else:
        status = "PHASE4_BRIDGE_SIGNATURE_DEFINED"

    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "created_at_local_date": "2026-07-04",
        "hostname": socket.gethostname(),
        "status": status,
        "phase1_inventory_path": str(inventory_path),
        "phase1_inventory_sha256": _file_sha256(inventory_path),
        "phase2_manifest_path": str(manifest_path),
        "phase2_manifest_sha256": _file_sha256(manifest_path),
        "canonical_field_set": canonical_field_set,
        "required_field_count": len(canonical_field_set),
        "bridge_population_count": len(embedded_rows),
        "embedded_payload_candidate_count": len(embedded_rows),
        "bridgeable_count": bridgeable_count,
        "candidate_status_counts": candidate_status_counts,
        "bridge_candidates": bridge_candidates,
        "cpu_gpu_status": "CPU-only/read-only bridge rerun; no GPU/CUDA device was probed or used",
        "network_status": "No network fetch",
        "external_mutation": "None; /home/chakwong/python was not modified",
        "nonclaims": [
            "read-only bridge rerun only",
            "no historical artifact loaded through BayesFilter",
            "no payload export success",
            "no HMC convergence claim",
            "no posterior correctness claim",
            "no sampler superiority claim",
            "no GPU readiness claim",
            "no default policy change",
        ],
    }
    return payload


def _require_canonical_sections(target_contract_manifest: dict[str, Any]) -> None:
    problem = target_contract_manifest.get("problem")
    chart = target_contract_manifest.get("chart")
    prior = target_contract_manifest.get("prior")
    filter_program = target_contract_manifest.get("filter_program")
    if not isinstance(problem, dict) or not isinstance(chart, dict) or not isinstance(prior, dict) or not isinstance(filter_program, dict):
        raise BridgeRerunError("Phase 2 manifest is missing a canonical section")
    for section in (problem, chart, prior, filter_program):
        if not section:
            raise BridgeRerunError("canonical section must be nonempty")


def _classify_candidate(
    row: dict[str, Any],
    canonical_field_set: tuple[str, ...],
    target_contract_manifest: dict[str, Any],
) -> dict[str, Any]:
    missing_fields = list(row.get("missing_fields", []))
    observed_fields = row.get("observed_contract_fields", {})
    if not isinstance(observed_fields, dict):
        raise BridgeRerunError("observed_contract_fields must be a mapping")

    present_fields = tuple(sorted(observed_fields.keys()))
    expected_present_fields = tuple(sorted(set(canonical_field_set) - set(missing_fields)))
    if present_fields != expected_present_fields:
        raise BridgeRerunError(
            f"candidate field coverage mismatch for {row.get('path')}: "
            f"present={present_fields!r} expected={expected_present_fields!r}"
        )

    bridge_status = str(row.get("bridge_status"))
    canonical_signature = None
    ssm_target_contract_manifest = None
    veto_reason = row.get("veto_reason")
    notes = row.get("notes")

    if missing_fields:
        if bridge_status != "missing_static_shape":
            bridge_status = "invented_field_required"
            veto_reason = (
                "candidate is missing required canonical fields: "
                + ", ".join(sorted(missing_fields))
            )
    else:
        manifest_signature = target_contract_manifest.get("manifest_payload_sha256")
        candidate_signature = row.get("canonical_signature")
        candidate_manifest = row.get("ssm_target_contract_manifest")
        if candidate_signature and candidate_manifest:
            bridge_status = "bridgeable_signature_defined"
            canonical_signature = str(candidate_signature)
            ssm_target_contract_manifest = candidate_manifest
        else:
            bridge_status = "invented_field_required"
            veto_reason = (
                "no canonical signature evidence present for a bridgeable row; "
                f"manifest payload hash is {manifest_signature}"
            )

    return {
        "path": row.get("path"),
        "phase1_status": row.get("phase1_status"),
        "payload_status": row.get("payload_status"),
        "transport_kinds": row.get("transport_kinds", []),
        "is_embedded_payload_candidate": True,
        "bridge_status": bridge_status,
        "missing_fields": missing_fields,
        "observed_contract_fields": observed_fields,
        "canonical_signature": canonical_signature,
        "ssm_target_contract_manifest": ssm_target_contract_manifest,
        "veto_reason": veto_reason,
        "notes": notes,
    }


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
