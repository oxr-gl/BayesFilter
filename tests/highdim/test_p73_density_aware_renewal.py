from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
import bayesfilter.highdim.source_route as source_route


def _load_p73_script():
    script_path = (
        Path(__file__).resolve().parents[2]
        / "scripts"
        / "p73_density_aware_renewal_diagnostic.py"
    )
    spec = importlib.util.spec_from_file_location("p73_density_aware_renewal", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _product_basis(degrees: tuple[int, ...]) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree) for degree in degrees],
        _convention(),
    )


def _branch_identity(
    ftt: highdim.FunctionalTT,
    defensive_density: highdim.TensorProductReferenceDensity,
    tau: float = 0.0,
) -> highdim.BranchIdentity:
    return highdim.SquaredTTDensity.expected_branch_identity(
        sqrt_tt=ftt,
        defensive_density=defensive_density,
        tau=tf.constant(tau, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
    )


def _constant_density(value: float = 1.0, tau: float = 0.0) -> highdim.SquaredTTDensity:
    product = _product_basis((0,))
    ftt = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[value]]], dtype=tf.float64))],
        product,
        _convention(),
    )
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    return highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(tau, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=_branch_identity(ftt, defensive, tau=tau),
    )


def _record(
    point_id: str,
    *,
    role: str = "fit",
    cloud_hash: str = "fit-hash",
    entered_training_round: int | None = 1,
    audit_round: int | None = None,
    source_channel: str = "fit",
) -> dict[str, object]:
    return dict(
        highdim.p73_renewal_role_record(
            point_id=point_id,
            cloud_hash=cloud_hash,
            role=role,
            created_round=1,
            entered_training_round=entered_training_round,
            audit_round=audit_round,
            source_channel=source_channel,
            seed_or_constructor_label="test",
        )
    )


def test_policy_constants_and_exports_match_phase2_contract():
    policy = highdim.p73_density_aware_renewal_policy()

    assert highdim.P73_RENEWAL_COUNT == 1
    assert highdim.P73_LAMBDA_CE == pytest.approx(0.1)
    assert highdim.P73_DENSITY_AWARE_OBJECTIVE_STATUS == (
        "included_as_opt_in_diagnostic_arm"
    )
    assert policy["renewal_count"] == 1
    assert policy["lambda_ce"] == pytest.approx(0.1)
    assert policy["p73_b_optimizer_status"] == highdim.P73_B_OPTIMIZER_BLOCKED
    assert policy["rank_promotion"] == "deferred"
    assert policy["inherited_p72_thresholds"]["condition_number_admission"] == 1e10
    assert policy["inherited_p72_thresholds"]["low_level_condition_number_veto"] == 1e14
    assert "not a source-faithful adaptive Zhao-Cui reproduction" in policy["nonclaims"]


def test_renewal_role_record_requires_human_readable_provenance_fields():
    record = highdim.p73_renewal_role_record(
        point_id="f1-0",
        cloud_hash="fit-hash",
        role="fresh",
        created_round=1,
        entered_training_round=1,
        audit_round=None,
        source_channel="fresh",
        parent_point_ids=("g0-0",),
        seed_or_constructor_label="seed-123",
    )

    assert record["point_id"] == "f1-0"
    assert record["role"] == "fresh"
    assert record["created_round"] == 1
    assert record["entered_training_round"] == 1
    assert record["parent_point_ids"] == ("g0-0",)

    with pytest.raises(ValueError, match="role"):
        highdim.p73_renewal_role_record(
            point_id="bad",
            cloud_hash="fit-hash",
            role="not-a-role",
            created_round=1,
            entered_training_round=1,
            audit_round=None,
            source_channel="fit",
        )


def test_no_audit_coefficient_selection_passes_clean_f1_and_fails_closed():
    clean = [_record("f1-0"), _record("f1-1", role="fresh", source_channel="fresh")]
    audit = [
        _record(
            "a1-0",
            role="audit",
            cloud_hash="audit-hash",
            entered_training_round=None,
            audit_round=1,
            source_channel="audit",
        )
    ]

    good = highdim.p73_no_audit_coefficient_selection(
        renewal_round=1,
        coefficient_records=clean,
        audit_records=audit,
        coefficient_cloud_hashes=("fit-hash",),
        audit_cloud_hashes=("audit-hash",),
    )
    assert good["status"] == "pass"
    assert good["NO_AUDIT_COEFFICIENT_SELECTION"] is True

    audit_in_coefficients = highdim.p73_no_audit_coefficient_selection(
        renewal_round=1,
        coefficient_records=clean + audit,
        audit_records=audit,
        coefficient_cloud_hashes=("fit-hash", "audit-hash"),
        audit_cloud_hashes=("audit-hash",),
    )
    assert audit_in_coefficients["status"] == "block"
    assert "audit_role_in_coefficient_selection" in audit_in_coefficients["reasons"]
    assert "current_or_prior_audit_record_in_coefficients" in audit_in_coefficients["reasons"]
    assert "same_round_audit_hash_overlap" in audit_in_coefficients["reasons"]

    missing_fields = highdim.p73_no_audit_coefficient_selection(
        renewal_round=1,
        coefficient_records=({"point_id": "x"},),
    )
    assert missing_fields["status"] == "block"
    assert "missing_coefficient_record_fields" in missing_fields["reasons"]


def test_training_batch_is_built_from_f1_only_and_excludes_audit_guard():
    records = [_record("f1-0"), _record("f1-1", role="fresh", source_channel="fresh")]

    batch, manifest = highdim.p73_training_batch_from_renewed_fit(
        fit_points=tf.constant([[-0.5, 0.5]], dtype=tf.float64),
        fit_target_values=tf.constant([1.0, 1.25], dtype=tf.float64),
        fit_weights=tf.ones([2], dtype=tf.float64),
        fit_records=records,
    )

    assert int(batch.points.shape[0]) == 2
    assert int(batch.points.shape[1]) == 1
    assert manifest["fit_point_count"] == 2
    assert manifest["guard_point_count_used_for_training"] == 0
    assert manifest["audit_point_count_used_for_training"] == 0
    assert manifest["audit_line_point_count_used_for_training"] == 0
    assert manifest["no_audit_coefficient_selection"]["status"] == "pass"


def test_training_batch_rejects_audit_record_in_f1():
    records = [
        _record(
            "a1-0",
            role="audit",
            cloud_hash="audit-hash",
            entered_training_round=1,
            audit_round=1,
            source_channel="audit",
        )
    ]

    with pytest.raises(ValueError, match="NO_AUDIT_COEFFICIENT_SELECTION"):
        highdim.p73_training_batch_from_renewed_fit(
            fit_points=tf.constant([[0.0]], dtype=tf.float64),
            fit_target_values=tf.constant([1.0], dtype=tf.float64),
            fit_weights=tf.ones([1], dtype=tf.float64),
            fit_records=records,
        )


def test_training_batch_rejects_same_round_audit_hash_overlap():
    records = [_record("f1-0", cloud_hash="shared-hash")]
    audit = [
        _record(
            "a1-0",
            role="audit",
            cloud_hash="shared-hash",
            entered_training_round=None,
            audit_round=1,
            source_channel="audit",
        )
    ]

    with pytest.raises(ValueError, match="NO_AUDIT_COEFFICIENT_SELECTION"):
        highdim.p73_training_batch_from_renewed_fit(
            fit_points=tf.constant([[0.0]], dtype=tf.float64),
            fit_target_values=tf.constant([1.0], dtype=tf.float64),
            fit_weights=tf.ones([1], dtype=tf.float64),
            fit_records=records,
            audit_records=audit,
            coefficient_cloud_hashes=("shared-hash",),
            audit_cloud_hashes=("shared-hash",),
        )


def test_enrichment_boundary_allows_guard_sources_and_rejects_audit_sources():
    guard_enrichment = [
        _record(
            "e0-0",
            role="enrichment",
            cloud_hash="enrich-hash",
            entered_training_round=1,
            source_channel="guard",
        ),
        _record(
            "e0-1",
            role="enrichment",
            cloud_hash="enrich-hash",
            entered_training_round=1,
            source_channel="guard_line",
        ),
    ]
    assert highdim.p73_validate_enrichment_boundary(
        enrichment_records=guard_enrichment
    )["status"] == "pass"

    audit_enrichment = [
        _record(
            "bad",
            role="audit_line",
            cloud_hash="audit-line-hash",
            entered_training_round=1,
            audit_round=1,
            source_channel="audit_line",
        )
    ]
    failed = highdim.p73_validate_enrichment_boundary(enrichment_records=audit_enrichment)
    assert failed["status"] == "block"
    assert "enrichment_from_non_guard_channel" in failed["reasons"]
    assert "audit_role_in_enrichment" in failed["reasons"]


def test_density_aware_cross_entropy_is_finite_and_uses_no_audit_predicate():
    density = _constant_density(1.0)
    records = [_record("f1-0"), _record("f1-1")]

    ce = highdim.p73_density_aware_cross_entropy(
        density=density,
        support_points=tf.constant([[-0.5, 0.5]], dtype=tf.float64),
        target_values=tf.constant([1.0, 1.0], dtype=tf.float64),
        support_weights=tf.ones([2], dtype=tf.float64),
        point_records=records,
    )

    assert ce["status"] == "pass"
    assert ce["lambda_ce"] == pytest.approx(0.1)
    assert ce["cross_entropy"] == pytest.approx(0.0, abs=1e-12)
    assert ce["weighted_cross_entropy"] == pytest.approx(0.0, abs=1e-12)
    assert ce["alpha_sum"] == pytest.approx(1.0)
    assert ce["no_audit_coefficient_selection"]["status"] == "pass"
    assert ce["p73_b_optimizer_status"] == highdim.P73_B_OPTIMIZER_BLOCKED


def test_density_aware_cross_entropy_blocks_audit_inputs():
    density = _constant_density(1.0)
    records = [
        _record(
            "a1-0",
            role="audit",
            cloud_hash="audit-hash",
            entered_training_round=1,
            audit_round=1,
            source_channel="audit",
        )
    ]

    ce = highdim.p73_density_aware_cross_entropy(
        density=density,
        support_points=tf.constant([[0.0]], dtype=tf.float64),
        target_values=tf.constant([1.0], dtype=tf.float64),
        support_weights=tf.ones([1], dtype=tf.float64),
        point_records=records,
    )

    assert ce["status"] == "block"
    assert "no_audit_coefficient_selection_failed" in ce["reasons"]
    assert ce["p73_b_optimizer_status"] == highdim.P73_B_OPTIMIZER_BLOCKED


def test_density_aware_cross_entropy_blocks_same_round_audit_hash_overlap():
    density = _constant_density(1.0)
    records = [_record("f1-0", cloud_hash="shared-hash")]
    audit = [
        _record(
            "a1-0",
            role="audit",
            cloud_hash="shared-hash",
            entered_training_round=None,
            audit_round=1,
            source_channel="audit",
        )
    ]

    ce = highdim.p73_density_aware_cross_entropy(
        density=density,
        support_points=tf.constant([[0.0]], dtype=tf.float64),
        target_values=tf.constant([1.0], dtype=tf.float64),
        support_weights=tf.ones([1], dtype=tf.float64),
        point_records=records,
        audit_records=audit,
        coefficient_cloud_hashes=("shared-hash",),
        audit_cloud_hashes=("shared-hash",),
    )

    assert ce["status"] == "block"
    assert "no_audit_coefficient_selection_failed" in ce["reasons"]
    assert "same_round_audit_hash_overlap" in ce["no_audit_coefficient_selection"]["reasons"]


def test_p73_b_optimizer_status_is_explicitly_blocked():
    status = highdim.p73_density_aware_optimizer_status()

    assert status["status"] == highdim.P73_B_OPTIMIZER_BLOCKED
    assert status["phase5_runnable"] is False
    assert status["density_aware_objective_status"] == (
        highdim.P73_DENSITY_AWARE_OBJECTIVE_STATUS
    )


def test_p73_script_schema_and_smoke_payload_are_not_phase5_evidence(tmp_path):
    module = _load_p73_script()
    output = tmp_path / "p73.json"

    payload = module.p73_phase4_schema_payload(output)

    assert payload["status"] == "P73_PHASE4_SCHEMA_READY_PHASE5_NOT_EXECUTED"
    assert payload["source_route_controls"]["phase5_diagnostic_executed"] is False
    assert payload["source_route_controls"]["smoke_only_not_phase5_evidence"] is True
    assert payload["arms"]["p73_b_density_aware_optin"]["status"] == (
        source_route.P73_B_OPTIMIZER_BLOCKED
    )
    assert "no P73 lower-gate pass claim" in payload["nonclaims"]

    smoke = module.p73_smoke_payload(
        output,
        f"{module.EXPECTED_COMMAND} --output {output}",
    )
    row = smoke["rows"]["p73_smoke_row"]

    assert smoke["status"] == "P73_PHASE4_SMOKE_COMPLETED_NOT_PHASE5_EVIDENCE"
    assert row["phase5_diagnostic_executed"] is False
    assert row["smoke_only_not_phase5_evidence"] is True
    assert row["no_audit_coefficient_selection"]["status"] == "pass"
    assert row["training_batch_manifest"]["audit_point_count_used_for_training"] == 0
    assert row["arms"]["p73_b_density_aware_optin"]["phase5_runnable"] is False


def test_p73_script_main_writes_json_without_running_phase5(tmp_path):
    module = _load_p73_script()
    output = tmp_path / "p73-smoke.json"

    assert module.main(["--output", str(output), "--smoke-only"]) == 0
    payload = json.loads(output.read_text())

    assert payload["status"] == "P73_PHASE4_SMOKE_COMPLETED_NOT_PHASE5_EVIDENCE"
    assert payload["gate_summary"]["phase5_diagnostic_executed"] is False
    assert payload["gate_summary"]["smoke_only_not_phase5_evidence"] is True
    assert payload["gate_summary"]["p73_b_optimizer_status"] == (
        source_route.P73_B_OPTIMIZER_BLOCKED
    )


def test_p73_default_main_routes_to_phase5_payload(monkeypatch, tmp_path):
    module = _load_p73_script()
    output = tmp_path / "p73-phase5.json"

    def fake_phase5_payload(path, command):
        return {
            "status": module.P73_PHASE5_BLOCK_STATUS,
            "gate_summary": {
                "overall_status": "block",
                "phase5_diagnostic_executed": True,
                "smoke_only_not_phase5_evidence": False,
                "schema_only_sentinel_present": False,
                "p73_b_optimizer_status": source_route.P73_B_OPTIMIZER_BLOCKED,
            },
            "path_seen": str(path),
            "command_seen": command,
        }

    def fail_smoke_payload(_path, _command):
        raise AssertionError("default command must not route to smoke payload")

    monkeypatch.setattr(module, "p73_phase5_payload", fake_phase5_payload)
    monkeypatch.setattr(module, "p73_smoke_payload", fail_smoke_payload)

    assert module.main(["--output", str(output)]) == 0
    payload = json.loads(output.read_text())
    assert payload["status"] == module.P73_PHASE5_BLOCK_STATUS
    assert payload["gate_summary"]["phase5_diagnostic_executed"] is True
    assert payload["gate_summary"]["smoke_only_not_phase5_evidence"] is False
    assert payload["path_seen"] == str(output)


def test_p73_phase5_payload_shape_with_stubbed_rows(monkeypatch, tmp_path):
    module = _load_p73_script()
    output = tmp_path / "p73-phase5.json"

    monkeypatch.setattr(
        module,
        "p73_phase5_rows",
        lambda: {
            "rank_candidate_1_2_fit36": {
                "status": source_route.P73_BLOCK_STATUS,
                "phase5_diagnostic_executed": True,
                "smoke_only_not_phase5_evidence": False,
            }
        },
    )

    payload = module.p73_phase5_payload(output, f"{module.EXPECTED_COMMAND} --output {output}")

    assert payload["status"] == module.P73_PHASE5_BLOCK_STATUS
    assert payload["diagnostic_scope"] == "p73_phase5_bounded_renewal_real_p73_a_rows"
    assert payload["source_route_controls"]["script_role"] == (
        "p73_phase5_real_bounded_renewal_diagnostic_runner"
    )
    assert payload["source_route_controls"]["phase5_diagnostic_executed"] is True
    assert payload["source_route_controls"]["smoke_only_not_phase5_evidence"] is False
    assert payload["source_route_controls"]["p73_b_optimizer_status"] == (
        source_route.P73_B_OPTIMIZER_BLOCKED
    )
    assert payload["gate_summary"]["schema_only_sentinel_present"] is False
    assert payload["gate_summary"]["failed_row_labels"] == ("rank_candidate_1_2_fit36",)
