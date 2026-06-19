from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
import bayesfilter.highdim.source_route as source_route


def _load_phase4_script():
    script_path = (
        Path(__file__).resolve().parents[2]
        / "scripts"
        / "p72_support_certified_lower_gate_diagnostic.py"
    )
    spec = importlib.util.spec_from_file_location("p72_lower_gate_diagnostic", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class _LinearTT:
    def evaluate(self, points: tf.Tensor) -> tf.Tensor:
        tensor = tf.convert_to_tensor(points, dtype=tf.float64)
        return tensor[:, 0] + 2.0


class _HugeTT:
    def evaluate(self, points: tf.Tensor) -> tf.Tensor:
        tensor = tf.convert_to_tensor(points, dtype=tf.float64)
        return tf.ones([int(tensor.shape[0])], dtype=tf.float64) * 1e6


def _clouds():
    fit = tf.constant(
        [
            [-1.0, 0.0, 1.0],
            [-0.5, 0.0, 0.5],
        ],
        dtype=tf.float64,
    )
    guard = tf.constant(
        [
            [-0.75, 0.75],
            [-0.25, 0.25],
        ],
        dtype=tf.float64,
    )
    audit = tf.constant(
        [
            [-0.9, 0.9],
            [-0.1, 0.1],
        ],
        dtype=tf.float64,
    )
    return fit, guard, audit


def test_p72_policy_constants_match_phase2_contract():
    policy = highdim.p72_support_certified_policy()

    assert highdim.P72_GUARD_STEP1_PRIOR_SEED == 7321
    assert highdim.P72_GUARD_STEP1_PROCESS_SEED == 7601
    assert highdim.P72_GUARD_STEP2_PROCESS_SEED == 7602
    assert highdim.P72_AUDIT_STEP1_HOLDOUT_PRIOR_SEED == 7301
    assert highdim.P72_AUDIT_STEP1_HOLDOUT_PROCESS_SEED == 7401
    assert highdim.P72_AUDIT_STEP1_REPLAY_PRIOR_SEED == 7311
    assert highdim.P72_AUDIT_STEP1_REPLAY_PROCESS_SEED == 7501
    assert highdim.P72_AUDIT_STEP2_HOLDOUT_PROCESS_SEED == 7402
    assert highdim.P72_AUDIT_STEP2_REPLAY_PROCESS_SEED == 7502
    assert highdim.P72_LINE_FRACTIONS == (0.0, 0.25, 0.5, 0.75, 1.0)
    assert highdim.P72_GUARD_WEIGHT_ALPHA == 1.0
    assert highdim.P72_SHAPE_PENALTY_WEIGHT == 0.0
    assert highdim.P72_CONDITION_NUMBER_ADMISSION == 1e10
    assert source_route.P70_CONDITION_NUMBER_VETO == 1e14
    assert highdim.P72_EFFECTIVE_RANK_TOL == 1e-12
    assert highdim.P72_SQRT_SQUARE_NORMALIZER_FLOOR == 1e-14
    assert policy["low_level_condition_number_veto"] == 1e14
    assert policy["p72_condition_number_admission"] == 1e10
    assert "not a source-faithful adaptive Zhao-Cui reproduction" in policy["nonclaims"]


def test_training_batch_uses_fit_and_guard_but_excludes_audit():
    fit, guard, _audit = _clouds()

    batch, manifest = highdim.p72_training_batch_from_fit_and_guard(
        fit_points=fit,
        fit_target_values=tf.constant([1.0, 2.0, 3.0], dtype=tf.float64),
        fit_weights=tf.ones([3], dtype=tf.float64),
        guard_points=guard,
        guard_target_values=tf.constant([1.5, 2.5], dtype=tf.float64),
        guard_weights=tf.ones([2], dtype=tf.float64),
    )

    assert int(batch.points.shape[0]) == 5
    assert manifest["fit_point_count"] == 3
    assert manifest["guard_point_count"] == 2
    assert manifest["audit_point_count_used_for_training"] == 0
    assert "Z_audit never concatenated" in manifest["audit_exclusion_provenance"]
    assert manifest["fit_weight_mass"] == pytest.approx(1.0)
    assert manifest["guard_weight_mass_after_alpha"] == pytest.approx(1.0)


def test_support_clipping_blocks_missing_nonfinite_and_all_clipped_clouds():
    fit, guard, _audit = _clouds()

    missing = highdim.p72_support_clipping_coverage(
        role="holdout",
        points=None,
        fit_points=fit,
    )
    assert missing["status"] == "block"
    assert "missing_points" in missing["reasons"]

    nonfinite = highdim.p72_support_clipping_coverage(
        role="replay",
        points=tf.constant([[float("nan")], [0.0]], dtype=tf.float64),
        fit_points=fit,
    )
    assert nonfinite["status"] == "block"
    assert "nonfinite_cloud" in nonfinite["reasons"]

    clipped = highdim.p72_support_clipping_coverage(
        role="guard",
        points=guard,
        fit_points=fit,
        clip_fraction=1.0,
        local_max_abs_before_clip=2.0,
    )
    assert clipped["status"] == "block"
    assert "all_clipped_cloud" in clipped["reasons"]


def test_support_clipping_warns_for_positive_clipping_and_records_hashes():
    fit, guard, _audit = _clouds()

    coverage = highdim.p72_support_clipping_coverage(
        role="guard",
        points=guard,
        fit_points=fit,
        clip_fraction=0.2,
        local_max_abs_before_clip=1.4,
    )

    assert coverage["status"] == "warn"
    assert "positive_clip_fraction" in coverage["warnings"]
    assert coverage["point_hash"] is not None
    assert coverage["nearest_fit_distance_max"] is not None
    assert coverage["effective_support_role"] == "finite_cloud_diagnostic_not_continuum_support"


def test_full_normalizer_gate_passes_and_blocks_required_terms():
    good = highdim.p72_full_normalizer_gate(
        {
            "mixture_normalizer": 2.0,
            "sqrt_square_normalizer": 1.5,
            "defensive_tau": 1e-8,
            "defensive_normalizer": 1.0,
            "log_transport_normalizer": 0.25,
        }
    )
    assert good["status"] == "pass"
    assert good["fit_mass_fraction"] == pytest.approx(0.75)

    missing = highdim.p72_full_normalizer_gate(
        {
            "mixture_normalizer": 2.0,
            "sqrt_square_normalizer": 1e-16,
            "defensive_tau": 1e-8,
            "log_transport_normalizer": 1e7,
        }
    )
    assert missing["status"] == "block"
    assert "missing_defensive_normalizer" in missing["reasons"]
    assert "sqrt_square_normalizer_floor_veto" in missing["reasons"]
    assert "fit_mass_fraction_veto" in missing["reasons"]
    assert "log_transport_normalizer_abs_bound_veto" in missing["reasons"]

    exception = highdim.p72_full_normalizer_gate(
        {
            "mixture_normalizer": 1e-16,
            "sqrt_square_normalizer": 1e-18,
            "defensive_tau": 1e-8,
            "defensive_normalizer": 1e-8,
            "transport_normalizer": None,
            "normalizer_exception": "NORMALIZER_FLOOR_EXCEEDED",
            "log_transport_normalizer": -36.0,
        }
    )
    assert exception["status"] == "block"
    assert "normalizer_exception_veto" in exception["reasons"]
    assert exception["normalizer_exception"] == "NORMALIZER_FLOOR_EXCEEDED"


def test_line_gate_fails_absolute_growth_independently_of_fit_prediction_scale():
    fit, guard, _audit = _clouds()
    line_points, manifest = highdim.p72_guard_line_points(fit_points=fit, guard_points=guard)
    targets = tf.zeros([int(line_points.shape[1])], dtype=tf.float64)

    gate = highdim.p72_line_probe_diagnostics(
        fitted_tt=_HugeTT(),
        line_points=line_points,
        line_target_values=targets,
        start_prediction_values=tf.constant([1.0, 1.0, 1.0], dtype=tf.float64),
        line_start_indices=manifest["line_start_indices"],
        target_scale=1.0,
    )

    assert manifest["line_fractions"] == highdim.P72_LINE_FRACTIONS
    assert len(manifest["line_start_indices"]) == int(line_points.shape[1])
    assert gate["status"] == "block"
    assert "line_absolute_value_veto" in gate["reasons"]
    assert "line_endpoint_growth_veto" in gate["reasons"]
    assert gate["line_start_indices_available"] is True
    assert gate["direct_target_evaluation_required"] is True


def test_condition_effective_rank_gate_is_wrapper_admission_not_solver_veto():
    passing = highdim.p72_condition_effective_rank_gate(
        (
            {
                "scaled_augmented_condition_number": 1e5,
                "scaled_augmented_singular_values": (2.0, 1.0),
            },
        )
    )
    assert passing["status"] == "pass"
    assert passing["low_level_solver_veto_unchanged"] == 1e14
    assert passing["p72_gate_role"] == "wrapper_admission_not_low_level_solver_abort"

    failing = highdim.p72_condition_effective_rank_gate(
        (
            {
                "scaled_augmented_condition_number": 1e11,
                "effective_rank": 0.0,
            },
        )
    )
    assert failing["status"] == "block"
    assert "p72_condition_admission_veto" in failing["reasons"]
    assert "p72_effective_rank_veto" in failing["reasons"]


def test_provenance_and_gate_summary_require_hashes_and_nonclaims():
    fit, guard, audit = _clouds()
    line_points, _ = highdim.p72_guard_line_points(fit_points=fit, guard_points=guard)
    provenance = highdim.p72_provenance_manifest(
        branch_identity="branch-123",
        target_values=tf.constant([1.0, 2.0, 3.0], dtype=tf.float64),
        frame_hash="frame-abc",
        shift_constant=0.5,
        fit_points=fit,
        guard_points=guard,
        audit_points=audit,
        line_points=line_points,
    )
    support = {
        role: highdim.p72_support_clipping_coverage(
            role=role,
            points=cloud,
            fit_points=fit,
            clip_fraction=0.0,
            local_max_abs_before_clip=1.0,
        )
        for role, cloud in (("fit", fit), ("guard", guard), ("holdout", audit), ("replay", audit))
    }
    summary = highdim.p72_gate_summary(
        residual_gates={"rms_relative": 1.0, "max_relative": 2.0},
        support_gates=support,
        normalizer_gate=highdim.p72_full_normalizer_gate(
            {
                "mixture_normalizer": 2.0,
                "sqrt_square_normalizer": 1.5,
                "defensive_tau": 1e-8,
                "defensive_normalizer": 1.0,
                "log_transport_normalizer": 0.0,
            }
        ),
        line_gate=highdim.p72_line_probe_diagnostics(
            fitted_tt=_LinearTT(),
            line_points=line_points,
            line_target_values=_LinearTT().evaluate(tf.transpose(line_points)),
            target_scale=1.0,
        ),
        condition_gate=highdim.p72_condition_effective_rank_gate(
            ({"scaled_augmented_condition_number": 1e5, "effective_rank": 2.0},)
        ),
        rank_activity={"status": "ok"},
        provenance=provenance,
    )

    assert summary["status"] == source_route.P72_PASS_STATUS
    assert summary["missing_provenance_fields"] == ()
    assert provenance["audit_exclusion_provenance"].startswith("audit clouds")
    assert "gate pass is not d18 validation" in summary["nonclaims"]


def test_gate_summary_blocks_rank_activity_and_missing_provenance():
    summary = highdim.p72_gate_summary(
        residual_gates={"rms_relative": 1.0, "max_relative": 2.0},
        support_gates={},
        normalizer_gate={"status": "pass"},
        line_gate={"status": "pass"},
        condition_gate={"status": "pass"},
        rank_activity={"status": "rank_channel_activity_failed"},
        provenance={"branch_identity": "only-one-field"},
    )

    assert summary["status"] == source_route.P72_BLOCK_STATUS
    assert "rank_channel_activity_failed" in summary["reasons"]
    assert "provenance_missing" in summary["reasons"]


def test_p72_script_default_schema_is_p72_scoped_and_not_p70(tmp_path):
    module = _load_phase4_script()
    output = tmp_path / "p72.json"

    payload = module.p72_phase4_schema_payload(output)

    assert "p72_support_certified_lower_gate_diagnostic.py" in module.EXPECTED_COMMAND
    assert "p70_phase6" not in module.EXPECTED_COMMAND
    assert payload["status"] == "PHASE4_SCHEMA_READY_PHASE5_NOT_EXECUTED"
    assert payload["source_route_controls"]["phase5_diagnostic_executed"] is False
    assert payload["source_route_controls"]["policy"]["p72_condition_number_admission"] == 1e10
    assert "no repaired lower-gate pass claim" in payload["nonclaims"]


def test_p72_smoke_payload_is_non_schema_and_has_required_gate_fields(tmp_path):
    module = _load_phase4_script()
    output = tmp_path / "p72-smoke.json"

    payload = module.p72_smoke_payload(
        output,
        f"{module.EXPECTED_COMMAND} --output {output} --smoke-only",
    )
    row = payload["rows"]["p72_smoke_row"]

    assert payload["status"] == "P72_PHASE5A_SMOKE_COMPLETED_NOT_PHASE5_EVIDENCE"
    assert payload["gate_summary"]["schema_only_sentinel_present"] is False
    assert payload["source_route_controls"]["schema_only_default_path"] is False
    assert payload["source_route_controls"]["phase5_diagnostic_executed"] is False
    assert payload["diagnostic_scope"] == "p72_phase5a_smoke_real_gate_path_not_phase5_evidence"
    assert "--smoke-only" in payload["run_manifest"]["command"]
    assert row["smoke_only_not_phase5_evidence"] is True
    assert row["training_batch_manifest"]["audit_point_count_used_for_training"] == 0
    assert row["support_gates"]["fit"]["status"] == "pass"
    assert row["support_gates"]["guard"]["status"] == "pass"
    assert row["normalizer_gate"]["status"] == "pass"
    assert row["line_gate"]["status"] == "pass"
    assert row["line_gate"]["direct_target_evaluation_required"] is True
    assert row["condition_effective_rank_gate"]["p72_gate_role"] == (
        "wrapper_admission_not_low_level_solver_abort"
    )
    assert row["provenance"]["audit_exclusion_provenance"].startswith("audit clouds")
    assert "PHASE4_SCHEMA_READY_PHASE5_NOT_EXECUTED" not in json.dumps(
        module._jsonable(payload),
        sort_keys=True,
    )


def test_p72_default_main_routes_to_real_phase5_payload(monkeypatch, tmp_path):
    module = _load_phase4_script()
    output = tmp_path / "p72-default.json"

    def fake_phase5_payload(path, command):
        return {
            "status": module.P72_PHASE5_BLOCK_STATUS,
            "gate_summary": {
                "overall_status": "block",
                "phase5_diagnostic_executed": True,
                "smoke_only_not_phase5_evidence": False,
                "schema_only_sentinel_present": False,
            },
            "path_seen": str(path),
            "command_seen": command,
        }

    def fail_smoke_payload(_path, _command):
        raise AssertionError("default command must not route to smoke payload")

    monkeypatch.setattr(module, "p72_phase5_payload", fake_phase5_payload)
    monkeypatch.setattr(module, "p72_smoke_payload", fail_smoke_payload)

    assert module.main(["--output", str(output)]) == 0
    payload = json.loads(output.read_text())
    assert payload["status"] == module.P72_PHASE5_BLOCK_STATUS
    assert payload["gate_summary"]["phase5_diagnostic_executed"] is True
    assert payload["gate_summary"]["smoke_only_not_phase5_evidence"] is False
    assert payload["path_seen"] == str(output)


def test_p72_phase5_payload_shape_with_stubbed_rows(monkeypatch, tmp_path):
    module = _load_phase4_script()
    output = tmp_path / "p72-phase5.json"

    monkeypatch.setattr(
        module,
        "p72_phase5_rows",
        lambda: {
            "rank_candidate_1_2_fit36": {
                "status": source_route.P72_BLOCK_STATUS,
                "phase5_diagnostic_executed": True,
                "smoke_only_not_phase5_evidence": False,
            }
        },
    )

    payload = module.p72_phase5_payload(output, f"{module.EXPECTED_COMMAND} --output {output}")

    assert payload["status"] == module.P72_PHASE5_BLOCK_STATUS
    assert payload["diagnostic_scope"] == "p72_phase5_support_certified_lower_gate_real_bounded_rows"
    assert payload["source_route_controls"]["script_role"] == "p72_phase5_real_bounded_diagnostic_runner"
    assert payload["source_route_controls"]["phase5_diagnostic_executed"] is True
    assert payload["source_route_controls"]["smoke_only_not_phase5_evidence"] is False
    assert payload["gate_summary"]["schema_only_sentinel_present"] is False
    assert payload["gate_summary"]["failed_row_labels"] == ("rank_candidate_1_2_fit36",)
    assert "P70 Phase 6h" in payload["evidence_contract"]["baseline_comparator"]


def test_skipped_step_after_prior_gate_block_is_structured():
    module = _load_phase4_script()

    skipped = module._skipped_step_after_prior_gate_block(
        time_index=2,
        fit_degree=1,
        fit_rank=3,
        fit_sample_count=36,
        skipped_after_time_index=1,
        skipped_reasons=("normalizer_block",),
    )

    assert skipped["status"] == source_route.P72_BLOCK_STATUS
    assert skipped["skip_reason"] == "prior_step_gate_blocked_no_retained_object"
    assert skipped["normalizer_gate"]["status"] == "block"
    assert skipped["phase5_diagnostic_executed"] is True
