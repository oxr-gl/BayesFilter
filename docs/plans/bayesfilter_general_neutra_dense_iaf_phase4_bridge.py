"""Build the Phase 4 target-signature bridge inventory.

This is read-only classification. It does not execute legacy model code and
does not load historical artifacts through BayesFilter.
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE1_JSON = Path(
    "docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-2026-07-04.json"
)
PHASE2_SCHEMA = Path(
    "docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-2026-07-04.md"
)
REQUIRED_CONTRACT_FIELDS = (
    "problem_id",
    "static_shape",
    "data_signature",
    "chart",
    "prior",
    "filter_program",
)
STATUS_BY_MISSING_FIELD = {
    "problem_id": "missing_problem_manifest",
    "static_shape": "missing_static_shape",
    "data_signature": "missing_data_signature",
    "chart": "missing_chart",
    "prior": "missing_prior",
    "filter_program": "missing_filter_program",
}
FIXED_STATUSES = (
    "bridgeable_signature_defined",
    "missing_problem_manifest",
    "missing_static_shape",
    "missing_data_signature",
    "missing_chart",
    "missing_prior",
    "missing_filter_program",
    "phase2_rule_mismatch",
    "invented_field_required",
    "legacy_identity_only",
    "requires_legacy_code_execution",
    "not_embedded_payload_candidate",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    phase1 = json.loads(PHASE1_JSON.read_text())
    schema_text = PHASE2_SCHEMA.read_text()
    candidates = [classify_candidate(item, schema_text) for item in phase1["candidate_artifacts"]]
    counts = Counter(item["bridge_status"] for item in candidates)
    payload = {
        "schema": "bayesfilter.general_neutra_dense_iaf_artifact_migration.phase4_target_signature_bridge.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "created_at_local_date": "2026-07-04",
        "hostname": socket.gethostname(),
        "python_executable": sys.executable,
        "phase1_taxonomy": str(PHASE1_JSON),
        "phase2_schema": str(PHASE2_SCHEMA),
        "cpu_gpu_status": "CPU-only/read-only bridge classification; no GPU/CUDA device was probed or used",
        "fixed_statuses": FIXED_STATUSES,
        "classification_counts": dict(sorted(counts.items())),
        "candidate_count": len(candidates),
        "embedded_payload_candidate_count": sum(
            item["is_embedded_payload_candidate"] for item in candidates
        ),
        "bridge_candidates": candidates,
        "nonclaims": [
            "target-signature bridge classification only",
            "no historical artifact loaded through BayesFilter",
            "no payload export success",
            "no HMC convergence claim",
            "no posterior correctness claim",
            "no sampler superiority claim",
            "no GPU readiness claim",
            "no default policy change",
        ],
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": args.output,
        "candidate_count": len(candidates),
        "embedded_payload_candidate_count": payload["embedded_payload_candidate_count"],
        "classification_counts": payload["classification_counts"],
    }, indent=2, sort_keys=True))
    return 0


def classify_candidate(item: dict[str, Any], schema_text: str) -> dict[str, Any]:
    embedded = item.get("payload_status") == "embedded_transport_payload_present"
    out: dict[str, Any] = {
        "path": item["path"],
        "phase1_status": item["status"],
        "payload_status": item.get("payload_status"),
        "transport_kinds": item.get("transport_kinds", []),
        "is_embedded_payload_candidate": embedded,
        "bridge_status": "not_embedded_payload_candidate",
        "missing_fields": [],
        "observed_contract_fields": {},
        "canonical_signature": None,
        "ssm_target_contract_manifest": None,
        "veto_reason": None,
        "notes": "",
    }
    if not embedded:
        out["notes"] = "Outside Phase 4 bridge population; provenance or non-payload artifact."
        return out
    if "stable_ssm_target_signature(SSMTargetContract" not in schema_text:
        out["bridge_status"] = "phase2_rule_mismatch"
        out["veto_reason"] = "Phase 2 schema artifact does not expose expected canonical signature rule."
        return out
    contract = infer_contract_fields(item)
    out["observed_contract_fields"] = contract
    missing = [field for field in REQUIRED_CONTRACT_FIELDS if field not in contract]
    out["missing_fields"] = missing
    if missing:
        out["bridge_status"] = STATUS_BY_MISSING_FIELD[missing[0]]
        out["veto_reason"] = (
            "Cannot define canonical SSMTargetContract without inventing fields: "
            + ", ".join(missing)
        )
        out["notes"] = (
            "Legacy payload has dense-IAF tensors, but generic target metadata is "
            "insufficient for canonical target_signature."
        )
        return out
    out["bridge_status"] = "invented_field_required"
    out["veto_reason"] = "No reviewed path in Phase 4 may synthesize full contract fields."
    return out


def infer_contract_fields(item: dict[str, Any]) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    path = item["path"].lower()
    kinds = item.get("transport_kinds", [])
    if "dense_autoregressive_iaf" in kinds:
        fields["chart"] = {
            "parameter_dim_inferred_from_payload": "present_but_names_and_transform_not_canonical"
        }
    if "rotemberg" in path:
        fields["problem_id"] = "legacy_rotemberg_name_only_not_canonical"
    elif "nk" in path:
        fields["problem_id"] = "legacy_nk_name_only_not_canonical"
    elif "sgu" in path:
        fields["problem_id"] = "legacy_sgu_name_only_not_canonical"
    return fields


if __name__ == "__main__":
    raise SystemExit(main())
