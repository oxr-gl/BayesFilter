"""Phase 3 smoke checks for scalable OT candidate result schema."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docs.benchmarks.scalable_ot_candidate_result_schema import (  # noqa: E402
    CandidateResultRecord,
    NONCLAIMS,
    TransportObjectRecord,
    validate_candidate_result,
)


BASELINE_COMPARATOR = "phase1_dense_streaming_baseline_2026_06_17"


def _manifest(candidate_id: str) -> dict[str, Any]:
    return {
        "phase": "phase3_schema_smoke",
        "candidate_id": candidate_id,
        "backend": "schema_only",
        "dtype": "N/A",
        "device": "N/A",
        "seed": "N/A",
        "command": "schema smoke examples only",
        "timestamp_utc": _dt.datetime.now(tz=_dt.UTC).isoformat(),
        "baseline_artifact": "docs/benchmarks/scalable-ot-p01-baseline-fixture-diagnostics-2026-06-17.json",
    }


def _record(
    *,
    candidate_id: str,
    source_status: str,
    semantic_class: str,
    source_route: str,
    transport_object: TransportObjectRecord,
    diagnostics: dict[str, Any],
    diagnostic_roles: dict[str, str],
) -> CandidateResultRecord:
    return CandidateResultRecord(
        candidate_id=candidate_id,
        source_status=source_status,
        semantic_class=semantic_class,
        source_route=source_route,
        baseline_comparator=BASELINE_COMPARATOR,
        transport_object=transport_object,
        diagnostics=diagnostics,
        diagnostic_roles=diagnostic_roles,
        execution_manifest=_manifest(candidate_id),
        nonclaims=list(NONCLAIMS),
    )


def _examples() -> list[CandidateResultRecord]:
    return [
        _record(
            candidate_id="dense_baseline_schema_example",
            source_status="source_locked",
            semantic_class="exact_semantics",
            source_route="source_faithful",
            transport_object=TransportObjectRecord(
                kind="dense_matrix",
                materialized=True,
                shape=[1, 8, 8],
            ),
            diagnostics={
                "finite_particles": True,
                "row_residual": 0.0,
                "column_residual": 0.0,
                "dense_reference_particle_error": 0.0,
            },
            diagnostic_roles={
                "finite_particles": "hard_veto",
                "row_residual": "hard_veto",
                "column_residual": "hard_veto",
                "dense_reference_particle_error": "promotion_criterion",
            },
        ),
        _record(
            candidate_id="streaming_baseline_schema_example",
            source_status="source_locked",
            semantic_class="exact_semantics",
            source_route="source_faithful",
            transport_object=TransportObjectRecord(
                kind="streaming_nonmaterialized",
                materialized=False,
                shape=[1, 0, 0],
                not_materialized_reason="streaming_no_dense_matrix",
            ),
            diagnostics={
                "finite_particles": True,
                "dense_streaming_particle_error": 0.0,
            },
            diagnostic_roles={
                "finite_particles": "hard_veto",
                "dense_streaming_particle_error": "promotion_criterion",
            },
        ),
        _record(
            candidate_id="nystrom_schema_example",
            source_status="source_locked",
            semantic_class="approximate_kernel",
            source_route="source_faithful",
            transport_object=TransportObjectRecord(
                kind="kernel_factors",
                materialized=False,
                factor_shapes={"V": [64, 8], "A": [8, 8], "scaling_u": [64], "scaling_v": [64]},
            ),
            diagnostics={
                "finite_particles": True,
                "rank": 8,
                "marginal_residual": 0.0,
                "dense_reference_particle_error": 0.0,
            },
            diagnostic_roles={
                "finite_particles": "hard_veto",
                "marginal_residual": "hard_veto",
                "dense_reference_particle_error": "promotion_criterion",
                "rank": "explanatory",
            },
        ),
        _record(
            candidate_id="exact_online_lazy_operator_schema_example",
            source_status="source_reference_only",
            semantic_class="exact_semantics",
            source_route="source_faithful",
            transport_object=TransportObjectRecord(
                kind="lazy_operator",
                materialized=False,
                shape=[1, 64, 64],
                not_materialized_reason="operator_application_without_dense_plan",
            ),
            diagnostics={
                "finite_particles": True,
                "operator_apply_finite": True,
                "dense_reference_particle_error": 0.0,
            },
            diagnostic_roles={
                "finite_particles": "hard_veto",
                "operator_apply_finite": "hard_veto",
                "dense_reference_particle_error": "promotion_criterion",
            },
        ),
        _record(
            candidate_id="low_rank_coupling_schema_example",
            source_status="source_locked",
            semantic_class="semantic_replacement",
            source_route="extension_or_invention",
            transport_object=TransportObjectRecord(
                kind="low_rank_coupling_factors",
                materialized=False,
                factor_shapes={"Q": [64, 4], "R": [64, 4], "g": [4]},
            ),
            diagnostics={
                "finite_particles": True,
                "factor_marginal_residual": 0.0,
                "dense_reference_particle_error": 0.0,
            },
            diagnostic_roles={
                "finite_particles": "hard_veto",
                "factor_marginal_residual": "hard_veto",
                "dense_reference_particle_error": "explanatory",
            },
        ),
        _record(
            candidate_id="sparse_schema_example",
            source_status="source_reference_only",
            semantic_class="reference_only",
            source_route="source_faithful",
            transport_object=TransportObjectRecord(
                kind="sparse_plan",
                materialized=True,
                shape=[64, 64],
            ),
            diagnostics={
                "support_fraction": 0.1,
                "captured_mass": 0.99,
                "locality_gate_passed": False,
            },
            diagnostic_roles={
                "support_fraction": "explanatory",
                "captured_mass": "repair_trigger",
                "locality_gate_passed": "continuation_veto",
            },
        ),
        _record(
            candidate_id="sliced_schema_example",
            source_status="source_locked",
            semantic_class="semantic_replacement",
            source_route="extension_or_invention",
            transport_object=TransportObjectRecord(
                kind="projection_plan",
                materialized=True,
                shape=[8, 64, 2],
                semantic_output="projected_transport_not_full_state_coupling",
            ),
            diagnostics={
                "projection_count": 8,
                "projected_transport_finite": True,
                "dense_reference_particle_error": 0.0,
            },
            diagnostic_roles={
                "projected_transport_finite": "hard_veto",
                "projection_count": "explanatory",
                "dense_reference_particle_error": "explanatory",
            },
        ),
        _record(
            candidate_id="projected_output_schema_example",
            source_status="source_locked",
            semantic_class="semantic_replacement",
            source_route="extension_or_invention",
            transport_object=TransportObjectRecord(
                kind="projected_output",
                materialized=True,
                shape=[1, 64, 8],
                semantic_output="projected_particles_not_full_state_transport",
            ),
            diagnostics={
                "projected_particles_finite": True,
                "full_state_transport_available": False,
            },
            diagnostic_roles={
                "projected_particles_finite": "hard_veto",
                "full_state_transport_available": "explanatory",
            },
        ),
        _record(
            candidate_id="minibatch_blocked_schema_example",
            source_status="source_partial_user_needed",
            semantic_class="blocked",
            source_route="extension_or_invention",
            transport_object=TransportObjectRecord(
                kind="blocked",
                materialized=False,
                blocked_reason="clean_source_archive_required_before_decision_grade_use",
            ),
            diagnostics={
                "clean_source_available": False,
                "transport_semantics_defined": False,
            },
            diagnostic_roles={
                "clean_source_available": "continuation_veto",
                "transport_semantics_defined": "continuation_veto",
            },
        ),
    ]


def _write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Phase 3 Common Interface Schema Smoke",
        "",
        f"- Status: `{result['status']}`",
        f"- Schema version: `{result['schema_version']}`",
        f"- Example count: `{len(result['examples'])}`",
        "",
        "## Examples",
        "",
        "| Candidate | Object kind | Source status | Semantic class | Warnings |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in result["examples"]:
        lines.append(
            "| {candidate} | `{kind}` | `{source}` | `{semantic}` | `{warnings}` |".format(
                candidate=item["candidate_id"],
                kind=item["transport_object"]["kind"],
                source=item["source_status"],
                semantic=item["semantic_class"],
                warnings=item["warnings"],
            )
        )
    lines.extend(["", "## Non-Claims", ""])
    for nonclaim in NONCLAIMS:
        lines.append(f"- {nonclaim}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()

    examples = []
    hard_vetoes: list[str] = []
    for record in _examples():
        data = record.to_dict()
        try:
            warnings = validate_candidate_result(data)
        except Exception as exc:  # pragma: no cover - smoke command reports this.
            hard_vetoes.append(f"{record.candidate_id}: {exc}")
            warnings = []
        data["warnings"] = warnings
        examples.append(data)

    result = {
        "status": "PASS" if not hard_vetoes else "FAIL",
        "schema_version": "scalable_ot_candidate_result_v1",
        "timestamp_utc": _dt.datetime.now(tz=_dt.UTC).isoformat(),
        "hard_vetoes": hard_vetoes,
        "examples": examples,
        "nonclaims": list(NONCLAIMS),
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_markdown(result, Path(args.markdown_output))
    if hard_vetoes:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
