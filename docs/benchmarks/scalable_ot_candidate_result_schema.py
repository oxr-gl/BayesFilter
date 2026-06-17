"""Schema helpers for scalable OT candidate result artifacts.

This module is Phase 3 infrastructure for the LEDH-PFPF-OT scalable OT
program.  It validates reporting records only; it does not implement an OT
candidate and does not provide execution-value evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA_VERSION = "scalable_ot_candidate_result_v1"

SOURCE_STATUSES = {
    "source_locked",
    "source_reference_only",
    "source_partial_user_needed",
    "paper_note_code_mismatch",
}

SEMANTIC_CLASSES = {
    "exact_semantics",
    "approximate_kernel",
    "semantic_replacement",
    "reference_only",
    "blocked",
}

TRANSPORT_OBJECT_KINDS = {
    "dense_matrix",
    "streaming_nonmaterialized",
    "lazy_operator",
    "kernel_factors",
    "low_rank_coupling_factors",
    "sparse_plan",
    "projection_plan",
    "projected_output",
    "blocked",
}

SOURCE_ROUTES = {
    "source_faithful",
    "fixed_hmc_adaptation",
    "extension_or_invention",
}

DIAGNOSTIC_ROLES = {
    "hard_veto",
    "promotion_criterion",
    "promotion_veto",
    "continuation_veto",
    "repair_trigger",
    "explanatory",
}

NONCLAIMS = (
    "schema/harness validation only",
    "no candidate algorithm implemented",
    "no candidate correctness claim",
    "no speedup claim",
    "no ranking claim",
    "no production default change",
)


class SchemaValidationError(ValueError):
    """Raised when a candidate result record violates the Phase 3 schema."""


@dataclass(frozen=True)
class TransportObjectRecord:
    kind: str
    materialized: bool
    shape: list[int] | None = None
    factor_shapes: dict[str, list[int]] = field(default_factory=dict)
    not_materialized_reason: str | None = None
    orientation: str = "source_rows_target_columns"
    semantic_output: str = "full_state_particles"
    blocked_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "materialized": self.materialized,
            "shape": self.shape,
            "factor_shapes": dict(self.factor_shapes),
            "not_materialized_reason": self.not_materialized_reason,
            "orientation": self.orientation,
            "semantic_output": self.semantic_output,
            "blocked_reason": self.blocked_reason,
        }


@dataclass(frozen=True)
class CandidateResultRecord:
    candidate_id: str
    source_status: str
    semantic_class: str
    source_route: str
    baseline_comparator: str
    transport_object: TransportObjectRecord
    diagnostics: dict[str, Any]
    diagnostic_roles: dict[str, str]
    execution_manifest: dict[str, Any]
    nonclaims: list[str] = field(default_factory=lambda: list(NONCLAIMS))
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "candidate_id": self.candidate_id,
            "source_status": self.source_status,
            "semantic_class": self.semantic_class,
            "source_route": self.source_route,
            "baseline_comparator": self.baseline_comparator,
            "transport_object": self.transport_object.to_dict(),
            "diagnostics": dict(self.diagnostics),
            "diagnostic_roles": dict(self.diagnostic_roles),
            "execution_manifest": dict(self.execution_manifest),
            "nonclaims": list(self.nonclaims),
        }


def validate_candidate_result(record: Mapping[str, Any]) -> list[str]:
    """Validate a candidate result record and return warning strings.

    Raises
    ------
    SchemaValidationError
        If required fields, enum values, or diagnostic role assignments are
        invalid.
    """

    errors: list[str] = []
    warnings: list[str] = []
    required = {
        "schema_version",
        "candidate_id",
        "source_status",
        "semantic_class",
        "source_route",
        "baseline_comparator",
        "transport_object",
        "diagnostics",
        "diagnostic_roles",
        "execution_manifest",
        "nonclaims",
    }
    missing = sorted(required.difference(record))
    if missing:
        errors.append(f"missing required fields: {missing}")
    if errors:
        raise SchemaValidationError("; ".join(errors))

    if record["schema_version"] != SCHEMA_VERSION:
        errors.append(f"unsupported schema_version: {record['schema_version']!r}")
    if record["source_status"] not in SOURCE_STATUSES:
        errors.append(f"invalid source_status: {record['source_status']!r}")
    if record["semantic_class"] not in SEMANTIC_CLASSES:
        errors.append(f"invalid semantic_class: {record['semantic_class']!r}")
    if record["source_route"] not in SOURCE_ROUTES:
        errors.append(f"invalid source_route: {record['source_route']!r}")

    transport = record["transport_object"]
    if not isinstance(transport, Mapping):
        errors.append("transport_object must be a mapping")
    else:
        kind = transport.get("kind")
        if kind not in TRANSPORT_OBJECT_KINDS:
            errors.append(f"invalid transport_object.kind: {kind!r}")
        if "materialized" not in transport:
            errors.append("transport_object.materialized is required")
        elif not isinstance(transport["materialized"], bool):
            errors.append("transport_object.materialized must be bool")
        if kind == "streaming_nonmaterialized" and not transport.get("not_materialized_reason"):
            errors.append("streaming_nonmaterialized requires not_materialized_reason")
        if kind == "blocked" and not transport.get("blocked_reason"):
            errors.append("blocked transport object requires blocked_reason")
        if kind in {"kernel_factors", "low_rank_coupling_factors"} and not transport.get("factor_shapes"):
            errors.append(f"{kind} requires factor_shapes")
        if kind == "dense_matrix" and not transport.get("shape"):
            errors.append("dense_matrix requires shape")
        if kind in {"lazy_operator", "projection_plan", "projected_output", "sparse_plan"} and not transport.get("shape"):
            errors.append(f"{kind} requires shape")

    diagnostic_roles = record["diagnostic_roles"]
    diagnostics = record["diagnostics"]
    if not isinstance(diagnostics, Mapping):
        errors.append("diagnostics must be a mapping")
    if not isinstance(diagnostic_roles, Mapping):
        errors.append("diagnostic_roles must be a mapping")
    else:
        for name, role in diagnostic_roles.items():
            if role not in DIAGNOSTIC_ROLES:
                errors.append(f"invalid diagnostic role for {name}: {role!r}")
            if isinstance(diagnostics, Mapping) and name not in diagnostics:
                warnings.append(f"diagnostic role without diagnostic value: {name}")

    nonclaims = record["nonclaims"]
    if not isinstance(nonclaims, list) or not nonclaims:
        errors.append("nonclaims must be a non-empty list")
    else:
        for required_nonclaim in ("no speedup claim", "no ranking claim", "no production default change"):
            if required_nonclaim not in nonclaims:
                errors.append(f"missing nonclaim: {required_nonclaim}")

    if not str(record["baseline_comparator"]).startswith("phase1_dense_streaming"):
        warnings.append("baseline_comparator does not start with phase1_dense_streaming")
    if record["source_status"] == "source_partial_user_needed" and record["semantic_class"] != "blocked":
        errors.append("source_partial_user_needed records must remain semantic_class=blocked in Phase 3")

    if errors:
        raise SchemaValidationError("; ".join(errors))
    return warnings


def validate_json_file(path: Path) -> list[str]:
    """Load and validate a JSON record from ``path``."""

    return validate_candidate_result(json.loads(path.read_text(encoding="utf-8")))


def write_json_record(record: CandidateResultRecord, path: Path) -> None:
    """Validate and write a candidate result record."""

    data = record.to_dict()
    validate_candidate_result(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
