from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim


def _records(status: str = "implemented") -> tuple[highdim.SourceRouteOperationRecord, ...]:
    return tuple(
        highdim.SourceRouteOperationRecord(
            operation_id=operation_id,
            source_anchor="full_sol.m / pre_sol.m clean-room operation table",
            implementation_status=status,
            notes="P54 source-route drift audit fixture",
        )
        for operation_id in highdim.SOURCE_ROUTE_REQUIRED_OPERATION_IDS
    )


def test_p54_source_route_operation_audit_passes_only_complete_source_coverage() -> None:
    audit = highdim.SourceRouteImplementationAudit(records=_records())
    payload = audit.manifest_payload()

    assert audit.status == "PASS_SOURCE_ROUTE_OPERATION_COVERAGE"
    assert payload["missing_required_operations"] == ()
    assert payload["incomplete_required_operations"] == ()
    assert payload["drift_markers"] == ()
    audit.assert_no_drift()


def test_p54_source_route_operation_audit_blocks_missing_or_partial_operations() -> None:
    missing = highdim.SourceRouteImplementationAudit(records=_records()[:-1])
    partial = highdim.SourceRouteImplementationAudit(records=_records(status="partial"))

    assert missing.status == "BLOCK_SOURCE_ROUTE_INCOMPLETE"
    assert missing.missing_required_operations == ("proposal_correction",)
    assert partial.status == "BLOCK_SOURCE_ROUTE_INCOMPLETE"
    assert "initialize_samples" in partial.incomplete_required_operations


def test_p54_source_route_operation_audit_blocks_known_drift_markers() -> None:
    audit = highdim.SourceRouteImplementationAudit(
        records=_records(),
        drift_markers=(
            "pairwise_grid_transition",
            "local_neighborhood_rank_multiplier",
            "q_power_dependency_width",
            "all_grid_retained_storage",
            "retained_grid_only_route",
        ),
    )

    assert audit.status == "BLOCK_SOURCE_ROUTE_DRIFT"
    with pytest.raises(ValueError, match="drift markers"):
        audit.assert_no_drift()


def test_p54_source_route_operation_list_keeps_previous_retained_object_explicit() -> None:
    assert (
        "previous_retained_object_marginalization"
        in highdim.SOURCE_ROUTE_REQUIRED_OPERATION_IDS
    )


def test_p54_source_route_operation_record_rejects_unknown_operation() -> None:
    with pytest.raises(ValueError, match="unknown source-route operation_id"):
        highdim.SourceRouteOperationRecord(
            operation_id="local_neighborhood_shortcut",
            source_anchor="P53 local-neighborhood route",
            implementation_status="implemented",
        )
