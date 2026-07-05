from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest
import tensorflow as tf


def _load_runner():
    script_path = (
        Path(__file__).resolve().parents[2]
        / "scripts/p86_author_lagrangep_phase5_budget_fit.py"
    )
    spec = importlib.util.spec_from_file_location(
        "p86_author_lagrangep_phase5_budget_fit",
        script_path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _default_basis_args(runner) -> dict[str, int]:
    return {
        "basis_order": runner.P85_AUTHOR_SIR_LAGRANGEP_ORDER,
        "basis_num_elems": runner.P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS,
    }


def test_p86_phase5_preflight_freezes_author_rung_f_budget() -> None:
    runner = _load_runner()
    payload = runner.build_preflight_payload()

    assert payload["status"] == runner.STATUS_PREFLIGHT_READY
    assert payload["preflight_only"] is True
    assert payload["fit_executed"] is False
    assert payload["training_backend"] == runner.TRAINING_BACKEND
    assert payload["historical_als_training_status"] == (
        runner.HISTORICAL_ALS_TRAINING_STATUS
    )
    assert payload["rank_budget"]["rung"] == "author_basis_rung_F"
    assert payload["rank_budget"]["target_dimension"] == 36
    assert payload["rank_budget"]["fit_rank"] == 4
    assert payload["rank_budget"]["P_theta"] == 18216
    assert payload["rank_budget"]["minimum_training_samples"] == 364320
    assert payload["rank_budget"]["training_sample_count"] == 364320
    assert payload["basis_config"]["basis_order"] == 4
    assert payload["basis_config"]["basis_num_elems"] == 8
    assert payload["basis_config"]["basis_expected_dim_per_dimension"] == 33
    assert payload["basis_config"]["basis_is_author_default"] is True
    assert payload["optimizer_budget"]["optimizer_batch_size"] == 4096
    assert payload["optimizer_budget"]["prefit_steps"] == 0
    assert payload["optimizer_budget"]["train_steps"] == 89
    assert payload["optimizer_budget"]["planned_training_sample_visits"] >= 364320
    assert payload["regularization_budget"]["l1_weight"] == pytest.approx(0.0)
    assert payload["regularization_budget"]["l2_weight"] == pytest.approx(1e-8)
    assert payload["regularization_budget"]["logz_anchor_weight"] == pytest.approx(0.0)
    assert payload["core_status_fields"]["parameter_count_status"] == "ok"
    assert payload["core_status_fields"]["sample_budget_status"] == "ok"
    assert payload["core_status_fields"]["sample_visit_budget_status"] == "ok"
    assert payload["core_status_fields"]["regularization_weight_status"] == "ok"


def test_p86_phase5_preflight_preserves_author_lagrangep_algebraic_route() -> None:
    runner = _load_runner()
    payload = runner.build_preflight_payload()
    route = payload["route_manifest"]

    assert payload["core_status_fields"]["route_manifest_ok"] is True
    assert route["basis_family"] == "lagrangep"
    assert route["basis_order"] == 4
    assert route["basis_num_elems"] == 8
    assert route["basis_dim_per_dimension"] == 33
    assert tuple(route["basis_dim_tuple"]) == (33,) * 36
    assert payload["basis_config"]["basis_order"] == 4
    assert payload["basis_config"]["basis_num_elems"] == 8
    assert payload["basis_config"]["basis_expected_dim_per_dimension"] == 33
    assert payload["basis_config"]["basis_is_author_default"] is True
    assert route["domain_map"] == "algebraic"
    assert route["domain_scale"] == 1.0
    assert route["route_changing_cli"] is False
    assert route["classification"] == "source_faithful"
    assert "legacy bounded Legendre" in payload["author_coordinate_policy"]["forbidden_substitute"]


def test_p86_phase5_preflight_freezes_exact_paths_and_fit_command() -> None:
    runner = _load_runner()
    payload = runner.build_preflight_payload()

    assert payload["command"] == runner.PREFLIGHT_COMMAND
    assert payload["candidate_fit_command"] == runner.FIT_COMMAND
    assert str(runner.PREFLIGHT_OUTPUT) in payload["candidate_fit_command"]
    assert str(runner.FIT_OUTPUT) in payload["candidate_fit_command"]
    assert "--fit" in payload["candidate_fit_command"]
    assert "--optimizer-batch-size 4096" in payload["candidate_fit_command"]
    assert "--train-steps 89" in payload["candidate_fit_command"]
    assert "--preflight-only" not in payload["candidate_fit_command"]
    assert payload["core_status_fields"]["command_fidelity_status"] == "ok"
    assert payload["core_status_fields"]["reserved_preflight_output_path_status"] == "ok"
    assert payload["core_status_fields"]["reserved_fit_output_path_status"] == "ok"


def test_p86_phase5_preflight_clouds_are_disjoint_and_audit_not_tuning() -> None:
    runner = _load_runner()
    payload = runner.build_preflight_payload()
    clouds = payload["clouds"]

    assert payload["cloud_policy"]["cloud_separation_status"] == "ok"
    assert payload["cloud_policy"]["audit_cloud_used_for_tuning"] is False
    assert len({cloud["cloud_label"] for cloud in clouds}) == len(clouds)
    assert len(
        {
            (cloud.get("prior_seed"), cloud.get("process_noise_seed"))
            for cloud in clouds
        }
    ) == len(clouds)
    assert clouds[-1]["role"] == "audit_reserved_not_used_for_phase5_tuning"
    assert clouds[-1]["may_fit_or_tune"] is False


def test_p86_phase5_preflight_memory_envelope_is_schema_tight() -> None:
    runner = _load_runner()
    payload = runner.build_preflight_payload()
    memory = payload["memory_envelope"]

    assert memory["memory_model"] == "p86_phase5_training_base_optimizer_batch_memory_model_v1"
    assert memory["optimizer_batch_size"] == 4096
    assert memory["active_batch_size"] == 4096
    assert memory["max_core_columns"] == 528
    assert memory["point_batch_bytes"] == 4096 * 36 * 8
    assert memory["persistent_cloud_bytes"] == (364320 + 65536) * (36 + 2) * 8
    assert memory["planned_under_cap"] is True
    assert payload["core_status_fields"]["planned_memory_envelope_status"] == "ok"
    assert payload["core_status_fields"]["memory_diagnostic_source_status"] == "ok"
    assert "ru_maxrss" in memory["diagnostic_source"]


def test_p86_phase5_fit_arg_guard_rejects_command_drift() -> None:
    runner = _load_runner()
    preflight = runner.build_preflight_payload()
    args = SimpleNamespace(
        output=runner.FIT_OUTPUT,
        preflight_json=runner.PREFLIGHT_OUTPUT,
        target_dimension=36,
        fit_rank=4,
        training_sample_count=364320,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=8605,
        optimizer_batch_size=4096,
        prefit_steps=0,
        train_steps=89,
        learning_rate=0.001,
        l1_weight=0.0,
        l2_weight=1e-8,
        logz_anchor_weight=0.0,
        max_seconds=14400,
        memory_cap_mib=12288,
        **_default_basis_args(runner),
        train_prior_seed=6301,
        train_process_seed=6401,
        holdout_prior_seed=7301,
        holdout_process_seed=7401,
        audit_prior_seed=7311,
        audit_process_seed=7501,
        adaptive_training=False,
        validation_check_every=0,
        plateau_patience=0,
        plateau_min_delta=0.0,
        lr_reduction_factor=0.5,
        min_learning_rate=1e-6,
        early_stop_after_lr_drops=0,
        serialize_trained_cores=False,
    )

    runner._guard_exact_fit_args(args, preflight)
    args.fit_rank = 8
    with pytest.raises(ValueError, match="fit_rank"):
        runner._guard_exact_fit_args(args, preflight)
    args.fit_rank = 4
    args.adaptive_training = True
    with pytest.raises(ValueError, match="adaptive_training"):
        runner._guard_exact_fit_args(args, preflight)
    args.adaptive_training = False
    args.basis_order = 3
    with pytest.raises(ValueError, match="basis_order"):
        runner._guard_exact_fit_args(args, preflight)


def test_p86_phase6_rank_preflight_freezes_rank5_comparator_budget() -> None:
    runner = _load_runner()
    payload = runner.build_phase6_rank_preflight_payload()

    assert payload["status"] == runner.STATUS_PHASE6_RANK_PREFLIGHT_READY
    assert payload["preflight_only"] is True
    assert payload["fit_executed"] is False
    assert payload["candidate_fit_command"] == runner.PHASE6_RANK5_FIT_COMMAND
    assert str(runner.PHASE6_RANK_PREFLIGHT_OUTPUT) in payload["candidate_fit_command"]
    assert str(runner.PHASE6_RANK5_FIT_OUTPUT) in payload["candidate_fit_command"]
    assert "--fit-rank 5" in payload["candidate_fit_command"]
    assert "--training-sample-count 567600" in payload["candidate_fit_command"]
    assert "--train-steps 139" in payload["candidate_fit_command"]
    assert payload["rank_budget"]["fit_rank"] == 5
    assert payload["rank_budget"]["P_theta"] == 28380
    assert payload["rank_budget"]["minimum_training_samples"] == 567600
    assert payload["rank_budget"]["training_sample_count"] == 567600
    assert payload["optimizer_budget"]["planned_training_sample_visits"] == 569344
    assert payload["core_status_fields"]["parameter_count_status"] == "ok"
    assert payload["core_status_fields"]["sample_budget_status"] == "ok"
    assert payload["core_status_fields"]["sample_visit_budget_status"] == "ok"
    assert payload["phase6_status_fields"]["lower_rung_status"] == "ok"
    assert payload["phase6_status_fields"]["degree_convergence_status"] == (
        "blocked_pending_reviewed_configurable_basis_path"
    )
    assert payload["convergence_artifact_gap"]["status"] == "known_gap_not_preflight_blocker"


def test_p86_phase6_rank5_fit_arg_guard_accepts_exact_comparator_and_rejects_drift() -> None:
    runner = _load_runner()
    preflight = runner.build_phase6_rank_preflight_payload()
    args = SimpleNamespace(
        output=runner.PHASE6_RANK5_FIT_OUTPUT,
        preflight_json=runner.PHASE6_RANK_PREFLIGHT_OUTPUT,
        target_dimension=36,
        fit_rank=5,
        training_sample_count=567600,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=8606,
        optimizer_batch_size=4096,
        prefit_steps=0,
        train_steps=139,
        learning_rate=0.001,
        l1_weight=0.0,
        l2_weight=1e-8,
        logz_anchor_weight=0.0,
        max_seconds=14400,
        memory_cap_mib=12288,
        **_default_basis_args(runner),
        train_prior_seed=8301,
        train_process_seed=8401,
        holdout_prior_seed=9301,
        holdout_process_seed=9401,
        audit_prior_seed=9311,
        audit_process_seed=9501,
        adaptive_training=False,
        validation_check_every=0,
        plateau_patience=0,
        plateau_min_delta=0.0,
        lr_reduction_factor=0.5,
        min_learning_rate=1e-6,
        early_stop_after_lr_drops=0,
        serialize_trained_cores=False,
    )

    runner._guard_exact_fit_args(args, preflight)
    args.train_steps = 140
    with pytest.raises(ValueError, match="train_steps"):
        runner._guard_exact_fit_args(args, preflight)
    args.train_steps = 139
    args.adaptive_training = True
    with pytest.raises(ValueError, match="adaptive_training"):
        runner._guard_exact_fit_args(args, preflight)


def test_p86_fit_exit_success_accepts_phase5_and_phase6_completed_statuses() -> None:
    runner = _load_runner()

    assert runner._fit_status_succeeded(runner.STATUS_TRAINING_BASE_COMPLETED)
    assert runner._fit_status_succeeded(runner.STATUS_PHASE6_RANK5_COMPLETED)
    assert runner._fit_status_succeeded(runner.STATUS_PHASE6S_ADAPTIVE_RANK5_COMPLETED)
    assert runner._fit_status_succeeded(runner.STATUS_PHASE6T_L1_TUNING_COMPLETED)
    assert runner._fit_status_succeeded(runner.STATUS_PHASE6V_L1_SELECTION_COMPLETED)
    assert not runner._fit_status_succeeded(runner.STATUS_TRAINING_BASE_BLOCKED)
    assert not runner._fit_status_succeeded(runner.STATUS_PHASE6_RANK5_BLOCKED)
    assert not runner._fit_status_succeeded(runner.STATUS_PHASE6S_ADAPTIVE_RANK5_BLOCKED)
    assert not runner._fit_status_succeeded(runner.STATUS_PHASE6T_L1_TUNING_BLOCKED)
    assert not runner._fit_status_succeeded(runner.STATUS_PHASE6V_L1_SELECTION_BLOCKED)


def test_p86_phase6r_training_protocol_defaults_preserve_fixed_budget_path() -> None:
    runner = _load_runner()

    defaults = runner._training_protocol_defaults()

    assert defaults["adaptive_training"] is False
    assert defaults["validation_check_every"] == 0
    assert defaults["plateau_patience"] == 0
    assert defaults["serialize_trained_cores"] is False


def test_p86_phase6r_convergence_status_flags_fixed_budget_exhaustion() -> None:
    runner = _load_runner()
    trace = (
        {"phase": "density", "step": 130, "terms": {"total_loss": -23.0}},
        {"phase": "density", "step": 139, "terms": {"total_loss": -25.0}},
    )

    status = runner._training_convergence_status(
        requested_steps=139,
        completed_steps=139,
        stop_reason="optimizer_steps_completed",
        adaptive_training=False,
        trace=trace,
        plateau_min_delta=1e-3,
    )

    assert status["status"] == "fixed_budget_exhausted_no_plateau_test"
    assert status["loss_still_improving_at_stop"] is True
    assert status["convergence_claim_allowed"] is False


def test_p86_phase6r_protocol_completed_accepts_scheduler_plateau_stop_only() -> None:
    runner = _load_runner()
    fixed_exhausted = {
        "completed_prefit_steps": 0,
        "completed_train_steps": 139,
        "training_convergence": {"status": "fixed_budget_exhausted_no_plateau_test"},
    }
    adaptive_plateau = {
        "completed_prefit_steps": 0,
        "completed_train_steps": 272,
        "training_convergence": {"status": "scheduler_stopped_after_plateau"},
    }
    incomplete_wall_clock = {
        "completed_prefit_steps": 0,
        "completed_train_steps": 272,
        "training_convergence": {"status": "unknown"},
    }

    assert runner._training_protocol_completed(
        fixed_exhausted,
        requested_prefit_steps=0,
        requested_train_steps=139,
    )
    assert runner._training_protocol_completed(
        adaptive_plateau,
        requested_prefit_steps=0,
        requested_train_steps=1024,
    )
    assert not runner._training_protocol_completed(
        incomplete_wall_clock,
        requested_prefit_steps=0,
        requested_train_steps=1024,
    )


def test_p86_phase6r_adaptive_state_reduces_lr_on_plateau_and_can_stop() -> None:
    runner = _load_runner()
    state = runner._adaptive_training_initial_state(learning_rate=1e-3)
    state = runner._update_adaptive_training_state(
        state,
        {"step": 10, "monitor_value": 1.0},
        plateau_patience=1,
        plateau_min_delta=1e-3,
        lr_reduction_factor=0.5,
        min_learning_rate=1e-5,
        early_stop_after_lr_drops=2,
    )
    state = runner._update_adaptive_training_state(
        state,
        {"step": 20, "monitor_value": 1.0005},
        plateau_patience=1,
        plateau_min_delta=1e-3,
        lr_reduction_factor=0.5,
        min_learning_rate=1e-5,
        early_stop_after_lr_drops=2,
    )
    state = runner._update_adaptive_training_state(
        state,
        {"step": 30, "monitor_value": 1.0004},
        plateau_patience=1,
        plateau_min_delta=1e-3,
        lr_reduction_factor=0.5,
        min_learning_rate=1e-5,
        early_stop_after_lr_drops=2,
    )

    assert state["lr_drop_count"] == 2
    assert state["current_learning_rate"] == pytest.approx(2.5e-4)
    assert state["stop_reason"] == "early_stop_after_plateau_lr_drop_limit"
    assert [event["event"] for event in state["events"]] == [
        "monitor_improved",
        "learning_rate_reduced_on_plateau",
        "learning_rate_reduced_on_plateau",
    ]


def test_p86_phase6r_trained_core_serialization_payload_can_include_values() -> None:
    runner = _load_runner()
    cores = (
        tf.constant([[[1.0], [2.0]]], dtype=tf.float64),
        tf.constant([[[3.0], [4.0]]], dtype=tf.float64),
    )

    metadata = runner._trained_core_serialization_payload(cores, include_values=False)
    with_values = runner._trained_core_serialization_payload(cores, include_values=True)

    assert metadata["status"] == "metadata_hash_only"
    assert metadata["core_count"] == 2
    assert metadata["total_values"] == 4
    assert "values" not in metadata["cores"][0]
    assert with_values["status"] == "serialized_with_values"
    assert with_values["cores"][0]["values"] == [[[1.0], [2.0]]]
    assert with_values["global_sha256"] == metadata["global_sha256"]


def test_p86_phase6r_adaptive_smoke_command_is_frozen() -> None:
    runner = _load_runner()

    assert runner.PHASE6R_ADAPTIVE_SMOKE_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py "
        "--phase6r-adaptive-smoke --target-dimension 36 --fit-rank 1 "
        "--training-sample-count 64 --holdout-sample-count 32 --seed 8615 "
        "--optimizer-batch-size 32 --prefit-steps 1 --train-steps 6 "
        "--learning-rate 0.001 --max-seconds 120 --memory-cap-mib 12288 "
        "--adaptive-training --validation-check-every 2 --plateau-patience 1 "
        "--plateau-min-delta 0.0 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 2 "
        "--serialize-trained-cores --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-tiny-adaptive-training-smoke-2026-06-24.json"
    )


def test_p86_phase6r_adaptive_smoke_arg_guard_accepts_exact_command_and_rejects_drift() -> None:
    runner = _load_runner()
    args = SimpleNamespace(
        output=runner.PHASE6R_ADAPTIVE_SMOKE_OUTPUT,
        target_dimension=36,
        fit_rank=1,
        training_sample_count=64,
        holdout_sample_count=32,
        seed=8615,
        optimizer_batch_size=32,
        prefit_steps=1,
        train_steps=6,
        learning_rate=0.001,
        l1_weight=0.0,
        l2_weight=1e-8,
        logz_anchor_weight=0.0,
        max_seconds=120,
        memory_cap_mib=12288,
        adaptive_training=True,
        validation_check_every=2,
        plateau_patience=1,
        plateau_min_delta=0.0,
        lr_reduction_factor=0.5,
        min_learning_rate=1e-6,
        early_stop_after_lr_drops=2,
        serialize_trained_cores=True,
    )

    runner._guard_phase6r_adaptive_smoke_args(args)
    args.validation_check_every = 3
    with pytest.raises(ValueError, match="validation_check_every"):
        runner._guard_phase6r_adaptive_smoke_args(args)


def _phase6s_adaptive_rank5_args(runner):
    return SimpleNamespace(
        output=runner.PHASE6S_RANK5_ADAPTIVE_FIT_OUTPUT,
        preflight_json=runner.PHASE6S_RANK5_ADAPTIVE_PREFLIGHT_OUTPUT,
        target_dimension=36,
        fit_rank=5,
        training_sample_count=567600,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=8606,
        optimizer_batch_size=4096,
        prefit_steps=0,
        train_steps=1024,
        learning_rate=0.001,
        l1_weight=0.0,
        l2_weight=1e-8,
        logz_anchor_weight=0.0,
        max_seconds=14400,
        memory_cap_mib=12288,
        **_default_basis_args(runner),
        train_prior_seed=8301,
        train_process_seed=8401,
        holdout_prior_seed=9301,
        holdout_process_seed=9401,
        audit_prior_seed=9311,
        audit_process_seed=9501,
        adaptive_training=True,
        validation_check_every=16,
        plateau_patience=4,
        plateau_min_delta=1e-6,
        lr_reduction_factor=0.5,
        min_learning_rate=1e-6,
        early_stop_after_lr_drops=4,
        serialize_trained_cores=True,
    )


def test_p86_phase6s_adaptive_rank5_command_is_frozen() -> None:
    runner = _load_runner()

    assert runner.PHASE6S_RANK5_ADAPTIVE_FIT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py --fit "
        "--preflight-json "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-preflight-2026-06-25.json "
        "--target-dimension 36 --fit-rank 5 --training-sample-count 567600 "
        "--holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 "
        "--optimizer-batch-size 4096 --prefit-steps 0 --train-steps 1024 "
        "--learning-rate 0.001 --max-seconds 14400 --memory-cap-mib 12288 "
        "--adaptive-training --validation-check-every 16 --plateau-patience 4 "
        "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
        "--serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 "
        "--holdout-prior-seed 9301 --holdout-process-seed 9401 "
        "--audit-prior-seed 9311 --audit-process-seed 9501 --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json"
    )
    assert runner.PHASE6S_RANK5_ADAPTIVE_PREFLIGHT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py "
        "--phase6s-adaptive-rank5-preflight --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-preflight-2026-06-25.json"
    )


def test_p86_phase6s_adaptive_rank5_preflight_freezes_protocol() -> None:
    runner = _load_runner()
    payload = runner.build_phase6s_adaptive_rank5_preflight_payload()

    assert payload["status"] == runner.STATUS_PHASE6S_ADAPTIVE_RANK5_PREFLIGHT_READY
    assert payload["preflight_only"] is True
    assert payload["fit_executed"] is False
    assert payload["candidate_fit_command"] == runner.PHASE6S_RANK5_ADAPTIVE_FIT_COMMAND
    assert payload["rank_budget"]["fit_rank"] == 5
    assert payload["rank_budget"]["P_theta"] == 28380
    assert payload["rank_budget"]["training_sample_count"] == 567600
    assert payload["optimizer_budget"]["max_train_steps"] == 1024
    assert payload["optimizer_budget"]["planned_training_sample_visits"] == 4096 * 1024
    assert payload["adaptive_training_protocol"]["optimizer_identity"] == runner.TRAINING_BACKEND
    assert payload["adaptive_training_protocol"]["optimizer"] == "Adam"
    assert payload["adaptive_training_protocol"]["adaptive_training"] is True
    assert payload["adaptive_training_protocol"]["validation_check_every"] == 16
    assert payload["adaptive_training_protocol"]["plateau_patience"] == 4
    assert payload["adaptive_training_protocol"]["plateau_min_delta"] == pytest.approx(1e-6)
    assert payload["adaptive_training_protocol"]["early_stop_after_lr_drops"] == 4
    assert payload["adaptive_training_protocol"]["serialize_trained_cores"] is True
    assert payload["cloud_policy"]["audit_cloud_used_for_tuning"] is False
    assert payload["phase6s_status_fields"]["phase6r_smoke_status"] == "ok"
    assert payload["phase6s_status_fields"]["old_rank5_interpretation_status"] == (
        "undertrained_protocol_incomplete_diagnostic_only"
    )
    assert payload["phase6s_status_fields"]["convergence_interpretation_status"] == (
        "preflight_only_no_rank_convergence_claim"
    )


def test_p86_phase6s_adaptive_rank5_guard_rejects_all_frozen_drift() -> None:
    runner = _load_runner()
    preflight = runner.build_phase6s_adaptive_rank5_preflight_payload()
    base_args = _phase6s_adaptive_rank5_args(runner)

    runner._guard_exact_fit_args(base_args, preflight)
    drifts = {
        "output": runner.PHASE6_RANK5_FIT_OUTPUT,
        "preflight_json": runner.PHASE6_RANK_PREFLIGHT_OUTPUT,
        "target_dimension": 35,
        "fit_rank": 4,
        "training_sample_count": 567599,
        "holdout_sample_count": 65535,
        "audit_sample_count": 65535,
        "seed": 8607,
        "optimizer_batch_size": 2048,
        "prefit_steps": 1,
        "train_steps": 1025,
        "learning_rate": 0.0005,
        "max_seconds": 14399,
        "memory_cap_mib": 12287,
        "train_prior_seed": 8302,
        "train_process_seed": 8402,
        "holdout_prior_seed": 9302,
        "holdout_process_seed": 9402,
        "audit_prior_seed": 9312,
        "audit_process_seed": 9502,
        "adaptive_training": False,
        "validation_check_every": 32,
        "plateau_patience": 5,
        "plateau_min_delta": 2e-6,
        "lr_reduction_factor": 0.25,
        "min_learning_rate": 2e-6,
        "early_stop_after_lr_drops": 5,
        "serialize_trained_cores": False,
    }
    for field, drift_value in drifts.items():
        args = _phase6s_adaptive_rank5_args(runner)
        setattr(args, field, drift_value)
        with pytest.raises(ValueError, match=field):
            runner._guard_exact_fit_args(args, preflight)


def _phase6t_l1_tuning_args(runner):
    return SimpleNamespace(
        output=runner.PHASE6T_L1_TUNING_DIAGNOSTIC_OUTPUT,
        preflight_json=runner.PHASE6T_L1_TUNING_PREFLIGHT_OUTPUT,
        target_dimension=36,
        fit_rank=5,
        training_sample_count=567600,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=8606,
        optimizer_batch_size=4096,
        prefit_steps=0,
        train_steps=512,
        learning_rate=0.0003,
        l1_weight=1e-9,
        l2_weight=1e-8,
        logz_anchor_weight=0.0,
        max_seconds=7200,
        memory_cap_mib=12288,
        **_default_basis_args(runner),
        train_prior_seed=8301,
        train_process_seed=8401,
        holdout_prior_seed=9301,
        holdout_process_seed=9401,
        audit_prior_seed=9311,
        audit_process_seed=9501,
        adaptive_training=True,
        validation_check_every=16,
        plateau_patience=4,
        plateau_min_delta=1e-6,
        lr_reduction_factor=0.5,
        min_learning_rate=1e-6,
        early_stop_after_lr_drops=4,
        serialize_trained_cores=True,
    )


def test_p86_phase6t_l1_tuning_command_is_frozen() -> None:
    runner = _load_runner()

    assert runner.PHASE6T_L1_TUNING_PREFLIGHT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py "
        "--phase6t-l1-tuning-preflight --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-preflight-2026-06-25.json"
    )
    assert runner.PHASE6T_L1_TUNING_FIT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py --fit "
        "--preflight-json "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-preflight-2026-06-25.json "
        "--target-dimension 36 --fit-rank 5 --training-sample-count 567600 "
        "--holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 "
        "--optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 "
        "--learning-rate 0.0003 --l1-weight 0.000000001 "
        "--l2-weight 0.00000001 --logz-anchor-weight 0.0 "
        "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
        "--validation-check-every 16 --plateau-patience 4 "
        "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
        "--serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 "
        "--holdout-prior-seed 9301 --holdout-process-seed 9401 "
        "--audit-prior-seed 9311 --audit-process-seed 9501 --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-diagnostic-2026-06-25.json"
    )


def test_p86_phase6t_l1_tuning_preflight_freezes_regularization_protocol() -> None:
    runner = _load_runner()
    payload = runner.build_phase6t_l1_tuning_preflight_payload()
    policy = payload["zhao_cui_regularization_default_policy"]

    assert payload["status"] == runner.STATUS_PHASE6T_L1_TUNING_PREFLIGHT_READY
    assert payload["preflight_only"] is True
    assert payload["fit_executed"] is False
    assert payload["candidate_fit_command"] == runner.PHASE6T_L1_TUNING_FIT_COMMAND
    assert payload["rank_budget"]["fit_rank"] == 5
    assert payload["optimizer_budget"]["train_steps"] == 512
    assert payload["optimizer_budget"]["learning_rate"] == pytest.approx(3e-4)
    assert payload["regularization_budget"]["l1_weight"] == pytest.approx(1e-9)
    assert payload["regularization_budget"]["l2_weight"] == pytest.approx(1e-8)
    assert payload["regularization_budget"]["logz_anchor_weight"] == pytest.approx(0.0)
    assert payload["regularization_budget"]["regularization_weight_status"] == "ok"
    assert payload["regularization_protocol"]["grid_execution_status"] == (
        "metadata_only_not_executed"
    )
    assert payload["regularization_protocol"]["default_policy"] == (
        runner.ZHAO_CUI_L1_TUNING_DEFAULT_POLICY
    )
    assert payload["regularization_protocol"]["selection_status"] == (
        runner.ZHAO_CUI_L1_TUNING_SELECTION_STATUS
    )
    assert policy["policy"] == runner.ZHAO_CUI_L1_TUNING_DEFAULT_POLICY
    assert policy["scope"] == "zhao_cui_training_base_route_only_not_global_p75_default"
    assert policy["global_p75_l1_scalar_default"] == pytest.approx(0.0)
    assert policy["allowed_l1_comparator_arm"] == pytest.approx(0.0)
    assert policy["selection_status"] == runner.ZHAO_CUI_L1_TUNING_SELECTION_STATUS
    assert "no production readiness claim" in policy["nonclaims"]
    assert tuple(payload["regularization_protocol"]["candidate_l1_grid"]) == (
        0.0,
        1e-10,
        3e-10,
        1e-9,
        3e-9,
        1e-8,
    )
    assert payload["cloud_policy"]["audit_cloud_used_for_tuning"] is False
    assert payload["phase6t_status_fields"]["audit_tuning_status"] == (
        "not_used_for_tuning"
    )
    assert payload["phase6t_status_fields"]["grid_execution_status"] == "not_executed"
    assert payload["phase6t_status_fields"]["convergence_interpretation_status"] == (
        "preflight_only_no_rank_convergence_claim"
    )


def test_p86_phase6t_l1_tuning_guard_rejects_regularization_drift() -> None:
    runner = _load_runner()
    preflight = runner.build_phase6t_l1_tuning_preflight_payload()
    base_args = _phase6t_l1_tuning_args(runner)

    runner._guard_exact_fit_args(base_args, preflight)
    drifts = {
        "l1_weight": 3e-9,
        "l2_weight": 3e-8,
        "logz_anchor_weight": 1e-6,
        "learning_rate": 1e-4,
        "train_steps": 1024,
        "max_seconds": 7201,
    }
    for field, drift_value in drifts.items():
        args = _phase6t_l1_tuning_args(runner)
        setattr(args, field, drift_value)
        with pytest.raises(ValueError, match=field):
            runner._guard_exact_fit_args(args, preflight)


def _phase6v_l1_selection_args(runner, *, output, l1_weight):
    return SimpleNamespace(
        output=output,
        preflight_json=runner.PHASE6V_L1_SELECTION_PREFLIGHT_OUTPUT,
        target_dimension=36,
        fit_rank=5,
        training_sample_count=567600,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=8606,
        optimizer_batch_size=4096,
        prefit_steps=0,
        train_steps=512,
        learning_rate=0.0003,
        l1_weight=l1_weight,
        l2_weight=1e-8,
        logz_anchor_weight=0.0,
        max_seconds=7200,
        memory_cap_mib=12288,
        **_default_basis_args(runner),
        train_prior_seed=8301,
        train_process_seed=8401,
        holdout_prior_seed=9301,
        holdout_process_seed=9401,
        audit_prior_seed=9311,
        audit_process_seed=9501,
        adaptive_training=True,
        validation_check_every=16,
        plateau_patience=4,
        plateau_min_delta=1e-6,
        lr_reduction_factor=0.5,
        min_learning_rate=1e-6,
        early_stop_after_lr_drops=4,
        serialize_trained_cores=True,
    )


def test_p86_phase6v_l1_selection_commands_are_frozen() -> None:
    runner = _load_runner()

    assert runner.PHASE6V_L1_SELECTION_PREFLIGHT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py "
        "--phase6v-l1-selection-preflight --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-2026-06-25.json"
    )
    assert runner.PHASE6V_L1_SELECTION_L1_0_FIT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py --fit "
        "--preflight-json "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-2026-06-25.json "
        "--target-dimension 36 --fit-rank 5 --training-sample-count 567600 "
        "--holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 "
        "--optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 "
        "--learning-rate 0.0003 --l1-weight 0.0 "
        "--l2-weight 0.00000001 --logz-anchor-weight 0.0 "
        "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
        "--validation-check-every 16 --plateau-patience 4 "
        "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
        "--serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 "
        "--holdout-prior-seed 9301 --holdout-process-seed 9401 "
        "--audit-prior-seed 9311 --audit-process-seed 9501 --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-0-fit-2026-06-25.json"
    )
    assert "--l1-weight 0.0000000003" in (
        runner.PHASE6V_L1_SELECTION_L1_3E_10_FIT_COMMAND
    )
    assert "--l1-weight 0.000000003" in (
        runner.PHASE6V_L1_SELECTION_L1_3E_9_FIT_COMMAND
    )


def test_p86_phase6v_l1_selection_preflight_freezes_policy_and_reuse() -> None:
    runner = _load_runner()
    payload = runner.build_phase6v_l1_selection_preflight_payload()

    assert payload["status"] == runner.STATUS_PHASE6V_L1_SELECTION_PREFLIGHT_READY
    assert payload["preflight_only"] is True
    assert payload["fit_executed"] is False
    assert payload["candidate_fit_commands"]["rank5_lr3e-4_l1_0"] == (
        runner.PHASE6V_L1_SELECTION_L1_0_FIT_COMMAND
    )
    assert payload["candidate_fit_commands"]["rank5_lr3e-4_l1_3e-10"] == (
        runner.PHASE6V_L1_SELECTION_L1_3E_10_FIT_COMMAND
    )
    assert payload["candidate_fit_commands"]["rank5_lr3e-4_l1_3e-9"] == (
        runner.PHASE6V_L1_SELECTION_L1_3E_9_FIT_COMMAND
    )
    assert tuple(arm["l1_weight"] for arm in payload["candidate_arms"]) == (
        0.0,
        3e-10,
        1e-9,
        3e-9,
    )
    assert payload["regularization_protocol"]["default_policy"] == (
        runner.ZHAO_CUI_L1_TUNING_DEFAULT_POLICY
    )
    assert payload["regularization_protocol"]["grid_execution_status"] == (
        "not_executed_preflight_only"
    )
    assert payload["selection_rule"]["veto_first"] is True
    assert payload["selection_rule"]["holdout_threshold"] == pytest.approx(
        0.5 * 0.22090990401849483
    )
    assert payload["reuse_arm_validation"]["status"] == "ok"
    assert payload["reuse_arm_validation"]["validation_kind"] == (
        "manifest_protocol_equivalence_not_command_acceptance"
    )
    assert all(payload["reuse_arm_validation"]["field_statuses"].values())
    assert payload["cloud_policy"]["audit_cloud_used_for_tuning"] is False
    assert payload["phase6v_status_fields"]["fit_execution_status"] == "not_executed"
    assert payload["phase6v_status_fields"]["phase7_status"] == (
        "blocked_until_later_same_policy_rank_degree_gate"
    )


def test_p86_phase6v_l1_selection_guard_accepts_new_candidate_arms() -> None:
    runner = _load_runner()
    preflight = runner.build_phase6v_l1_selection_preflight_payload()

    for output, l1_weight in (
        (runner.PHASE6V_L1_SELECTION_L1_0_OUTPUT, 0.0),
        (runner.PHASE6V_L1_SELECTION_L1_3E_10_OUTPUT, 3e-10),
        (runner.PHASE6V_L1_SELECTION_L1_3E_9_OUTPUT, 3e-9),
    ):
        args = _phase6v_l1_selection_args(
            runner,
            output=output,
            l1_weight=l1_weight,
        )
        runner._guard_exact_fit_args(args, preflight)


def test_p86_phase6v_l1_selection_guard_rejects_frozen_drift() -> None:
    runner = _load_runner()
    preflight = runner.build_phase6v_l1_selection_preflight_payload()
    drifts = {
        "output": runner.PHASE6T_L1_TUNING_DIAGNOSTIC_OUTPUT,
        "preflight_json": runner.PHASE6T_L1_TUNING_PREFLIGHT_OUTPUT,
        "target_dimension": 35,
        "fit_rank": 4,
        "training_sample_count": 567599,
        "holdout_sample_count": 65535,
        "audit_sample_count": 65535,
        "seed": 8607,
        "optimizer_batch_size": 2048,
        "prefit_steps": 1,
        "train_steps": 513,
        "learning_rate": 0.0001,
        "l1_weight": 1e-9,
        "l2_weight": 3e-8,
        "logz_anchor_weight": 1e-6,
        "max_seconds": 7201,
        "memory_cap_mib": 12287,
        "train_prior_seed": 8302,
        "train_process_seed": 8402,
        "holdout_prior_seed": 9302,
        "holdout_process_seed": 9402,
        "audit_prior_seed": 9312,
        "audit_process_seed": 9502,
        "adaptive_training": False,
        "validation_check_every": 32,
        "plateau_patience": 5,
        "plateau_min_delta": 2e-6,
        "lr_reduction_factor": 0.25,
        "min_learning_rate": 2e-6,
        "early_stop_after_lr_drops": 5,
        "serialize_trained_cores": False,
    }
    for field, drift_value in drifts.items():
        args = _phase6v_l1_selection_args(
            runner,
            output=runner.PHASE6V_L1_SELECTION_L1_0_OUTPUT,
            l1_weight=0.0,
        )
        setattr(args, field, drift_value)
        with pytest.raises(ValueError, match=field):
            runner._guard_exact_fit_args(args, preflight)


def test_p86_phase6v_reuse_arm_validation_rejects_protocol_drift() -> None:
    runner = _load_runner()
    artifact = Path(runner.PHASE6T_L1_TUNING_DIAGNOSTIC_OUTPUT)
    payload = runner.json.loads(artifact.read_text())

    ok = runner.validate_phase6v_reuse_arm(payload)
    assert ok["status"] == "ok"

    drifted = {
        **payload,
        "training_summary": {
            **payload["training_summary"],
            "training_protocol": {
                **payload["training_summary"]["training_protocol"],
                "l1_weight": 3e-9,
            },
        },
    }
    blocked = runner.validate_phase6v_reuse_arm(drifted)
    assert blocked["status"] == "block"
    assert blocked["field_statuses"]["l1_weight"] is False


def _phase6w_rank4_args(runner, *, output, l1_weight):
    return SimpleNamespace(
        output=output,
        preflight_json=runner.PHASE6W_SAME_POLICY_RANK_PREFLIGHT_OUTPUT,
        target_dimension=36,
        fit_rank=4,
        training_sample_count=364320,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=8606,
        optimizer_batch_size=4096,
        prefit_steps=0,
        train_steps=512,
        learning_rate=0.0003,
        l1_weight=l1_weight,
        l2_weight=1e-8,
        logz_anchor_weight=0.0,
        max_seconds=7200,
        memory_cap_mib=12288,
        **_default_basis_args(runner),
        train_prior_seed=8301,
        train_process_seed=8401,
        holdout_prior_seed=9301,
        holdout_process_seed=9401,
        audit_prior_seed=9311,
        audit_process_seed=9501,
        adaptive_training=True,
        validation_check_every=16,
        plateau_patience=4,
        plateau_min_delta=1e-6,
        lr_reduction_factor=0.5,
        min_learning_rate=1e-6,
        early_stop_after_lr_drops=4,
        serialize_trained_cores=True,
    )


def test_p86_phase6w_same_policy_rank_commands_are_frozen() -> None:
    runner = _load_runner()

    assert runner.PHASE6W_SAME_POLICY_RANK_PREFLIGHT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py "
        "--phase6w-same-policy-rank-preflight --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-2026-06-25.json"
    )
    assert runner.PHASE6W_RANK4_L1_0_FIT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py --fit "
        "--preflight-json "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-2026-06-25.json "
        "--target-dimension 36 --fit-rank 4 --training-sample-count 364320 "
        "--holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 "
        "--optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 "
        "--learning-rate 0.0003 --l1-weight 0.0 "
        "--l2-weight 0.00000001 --logz-anchor-weight 0.0 "
        "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
        "--validation-check-every 16 --plateau-patience 4 "
        "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
        "--serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 "
        "--holdout-prior-seed 9301 --holdout-process-seed 9401 "
        "--audit-prior-seed 9311 --audit-process-seed 9501 --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-0-fit-2026-06-25.json"
    )
    assert "--l1-weight 0.0000000003" in runner.PHASE6W_RANK4_L1_3E_10_FIT_COMMAND
    assert "--l1-weight 0.000000001" in runner.PHASE6W_RANK4_L1_1E_9_FIT_COMMAND
    assert "--l1-weight 0.000000003" in runner.PHASE6W_RANK4_L1_3E_9_FIT_COMMAND


def test_p86_phase6w_preflight_freezes_same_policy_rank4_and_rank5_reuse() -> None:
    runner = _load_runner()
    payload = runner.build_phase6w_same_policy_rank_preflight_payload()

    assert payload["status"] == runner.STATUS_PHASE6W_SAME_POLICY_RANK_PREFLIGHT_READY
    assert payload["preflight_only"] is True
    assert payload["fit_executed"] is False
    assert payload["rank_budget"]["fit_rank"] == 4
    assert payload["rank_budget"]["P_theta"] == 18216
    assert payload["rank_budget"]["minimum_training_samples"] == 364320
    assert payload["rank_budget"]["training_sample_count"] == 364320
    assert payload["optimizer_budget"]["train_steps"] == 512
    assert payload["optimizer_budget"]["learning_rate"] == pytest.approx(3e-4)
    assert payload["optimizer_budget"]["planned_training_sample_visits"] == 4096 * 512
    assert payload["regularization_protocol"]["default_policy"] == (
        runner.ZHAO_CUI_L1_TUNING_DEFAULT_POLICY
    )
    assert tuple(arm["l1_weight"] for arm in payload["candidate_arms"]) == (
        0.0,
        3e-10,
        1e-9,
        3e-9,
    )
    assert payload["candidate_fit_commands"]["rank4_lr3e-4_l1_0"] == (
        runner.PHASE6W_RANK4_L1_0_FIT_COMMAND
    )
    assert payload["candidate_fit_commands"]["rank4_lr3e-4_l1_1e-9"] == (
        runner.PHASE6W_RANK4_L1_1E_9_FIT_COMMAND
    )
    assert payload["rank4_selection_rule"]["zero_l1_comparator_required"] is True
    assert payload["rank4_selection_rule"]["audit_cloud_selection"] == "forbidden"
    assert payload["adjacent_rank_stability_rule"]["selected_rank5_artifact"] == (
        str(runner.PHASE6V_L1_SELECTION_L1_0_OUTPUT)
    )
    assert payload["selected_rank5_reuse_validation"]["status"] == "ok"
    assert all(payload["selected_rank5_reuse_validation"]["field_statuses"].values())
    assert payload["phase6v_selection_ledger_validation"]["status"] == "ok"
    assert payload["phase5_rank4_historical_context"]["same_policy_lower_rung_status"] == (
        "not_allowed"
    )
    assert payload["phase6w_status_fields"]["phase5_rank4_context_status"] == (
        "historical_only_not_same_policy_lower_rung"
    )
    assert payload["phase6w_status_fields"]["phase7_status"] == (
        "blocked_until_same_policy_rank_degree_gate_passes_or_owner_reframes"
    )
    assert payload["cloud_policy"]["audit_cloud_used_for_tuning"] is False


def test_p86_degree_comparator_preflight_supports_nondefault_static_basis() -> None:
    runner = _load_runner()
    preflight_output = Path(
        "docs/plans/"
        "bayesfilter-highdim-zhao-cui-p86-phase6x-degree-order3-preflight-2026-06-26.json"
    )
    fit_output = Path(
        "docs/plans/"
        "bayesfilter-highdim-zhao-cui-p86-phase6x-degree-order3-rank4-fit-2026-06-26.json"
    )
    command = (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py "
        "--phase6x-degree-comparator-preflight "
        "--basis-order 3 --basis-num-elems 8 --output "
        f"{preflight_output}"
    )
    candidate_fit_command = (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py --fit "
        f"--preflight-json {preflight_output} "
        "--target-dimension 36 --fit-rank 4 --basis-order 3 --basis-num-elems 8 "
        "--training-sample-count 276000 --holdout-sample-count 65536 "
        "--audit-sample-count 65536 --seed 8608 --optimizer-batch-size 4096 "
        "--prefit-steps 0 --train-steps 512 --learning-rate 0.0003 "
        "--l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 "
        "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
        "--validation-check-every 16 --plateau-patience 4 "
        "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
        "--serialize-trained-cores --train-prior-seed 8303 "
        "--train-process-seed 8403 --holdout-prior-seed 9303 "
        "--holdout-process-seed 9403 --audit-prior-seed 9313 "
        f"--audit-process-seed 9503 --output {fit_output}"
    )

    payload = runner.build_degree_comparator_preflight_payload(
        output=preflight_output,
        target_dimension=36,
        fit_rank=4,
        basis_order=3,
        basis_num_elems=8,
        training_sample_count=276000,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=8608,
        optimizer_batch_size=4096,
        prefit_steps=0,
        train_steps=512,
        learning_rate=0.0003,
        l1_weight=0.0,
        l2_weight=1e-8,
        logz_anchor_weight=0.0,
        max_seconds=7200,
        memory_cap_mib=12288,
        command=command,
        candidate_fit_command=candidate_fit_command,
        expected_output=preflight_output,
        expected_fit_output=fit_output,
        expected_p_theta=13800,
        status_ready="P86_PHASE6X_DEGREE_COMPARATOR_PREFLIGHT_READY_NOT_FIT",
        block_status="BLOCK_P86_PHASE6X_DEGREE_COMPARATOR_PREFLIGHT",
        schema_version="p86_phase6x_degree_comparator_preflight.v1",
        phase_name="P86 Phase 6X degree comparator preflight",
        phase_subplan=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6x-degree-comparator-subplan-2026-06-26.md"
        ),
        phase_result=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6x-degree-comparator-result-2026-06-26.md"
        ),
        rank_rung="author_basis_rung_F_rank4_degree_order3_comparator",
        label_prefix="p86-phase6x-degree-order3-rank4",
        train_prior_seed=8303,
        train_process_seed=8403,
        holdout_prior_seed=9303,
        holdout_process_seed=9403,
        audit_prior_seed=9313,
        audit_process_seed=9503,
        nonclaims=runner.PHASE6W_PREFLIGHT_NONCLAIMS,
        lower_rung_artifact=str(runner.PHASE6W_RANK4_L1_0_OUTPUT),
    )

    assert payload["status"] == "P86_PHASE6X_DEGREE_COMPARATOR_PREFLIGHT_READY_NOT_FIT"
    assert payload["route_manifest"]["basis_order"] == 3
    assert payload["route_manifest"]["basis_num_elems"] == 8
    assert payload["route_manifest"]["basis_dim_per_dimension"] == 25
    assert payload["route_manifest"]["classification"] == "extension_or_invention"
    assert payload["route_manifest"]["classification_subtype"] == (
        "setup_static_degree_comparator_config"
    )
    assert payload["rank_budget"]["P_theta"] == 13800
    assert payload["rank_budget"]["minimum_training_samples"] == 276000
    assert payload["rank_budget"]["training_sample_count"] == 276000
    assert payload["basis_config"]["basis_order"] == 3
    assert payload["basis_config"]["basis_num_elems"] == 8
    assert payload["basis_config"]["basis_expected_dim_per_dimension"] == 25
    assert payload["basis_config"]["basis_is_author_default"] is False
    assert payload["basis_config"]["degree_comparator_classification"] == (
        "extension_or_invention"
    )
    assert payload["basis_config"]["degree_comparator_subtype"] == (
        "setup_static_degree_comparator_config"
    )
    assert payload["core_status_fields"]["command_fidelity_status"] == "ok"
    assert payload["gate_summary"]["overall_status"] == "ready_for_exact_claude_agreed_execution"


def test_p86_phase6w_selected_rank5_reuse_validation_rejects_drift() -> None:
    runner = _load_runner()
    artifact = Path(runner.PHASE6V_L1_SELECTION_L1_0_OUTPUT)
    payload = runner.json.loads(artifact.read_text())

    ok = runner.validate_phase6w_selected_rank5_reuse_arm(payload)
    assert ok["status"] == "ok"

    drifted = {
        **payload,
        "output": str(runner.PHASE6V_L1_SELECTION_L1_3E_9_OUTPUT),
    }
    blocked = runner.validate_phase6w_selected_rank5_reuse_arm(drifted)
    assert blocked["status"] == "block"
    assert blocked["field_statuses"]["artifact_path"] is False

    drifted_l1 = {
        **payload,
        "training_summary": {
            **payload["training_summary"],
            "training_protocol": {
                **payload["training_summary"]["training_protocol"],
                "l1_weight": 1e-9,
            },
        },
    }
    blocked_l1 = runner.validate_phase6w_selected_rank5_reuse_arm(drifted_l1)
    assert blocked_l1["status"] == "block"
    assert blocked_l1["field_statuses"]["selected_l1_weight"] is False


def test_p86_phase6w_exact_guard_accepts_all_rank4_candidate_arms() -> None:
    runner = _load_runner()
    preflight = runner.build_phase6w_same_policy_rank_preflight_payload()

    for output, l1_weight in (
        (runner.PHASE6W_RANK4_L1_0_OUTPUT, 0.0),
        (runner.PHASE6W_RANK4_L1_3E_10_OUTPUT, 3e-10),
        (runner.PHASE6W_RANK4_L1_1E_9_OUTPUT, 1e-9),
        (runner.PHASE6W_RANK4_L1_3E_9_OUTPUT, 3e-9),
    ):
        args = _phase6w_rank4_args(
            runner,
            output=output,
            l1_weight=l1_weight,
        )
        runner._guard_exact_fit_args(args, preflight)


def test_p86_phase6w_exact_guard_rejects_frozen_drift() -> None:
    runner = _load_runner()
    preflight = runner.build_phase6w_same_policy_rank_preflight_payload()
    drifts = {
        "output": runner.PHASE6V_L1_SELECTION_L1_0_OUTPUT,
        "preflight_json": runner.PHASE6V_L1_SELECTION_PREFLIGHT_OUTPUT,
        "target_dimension": 35,
        "fit_rank": 5,
        "training_sample_count": 364319,
        "holdout_sample_count": 65535,
        "audit_sample_count": 65535,
        "seed": 8607,
        "optimizer_batch_size": 2048,
        "prefit_steps": 1,
        "train_steps": 513,
        "learning_rate": 0.0001,
        "l1_weight": 1e-9,
        "l2_weight": 3e-8,
        "logz_anchor_weight": 1e-6,
        "max_seconds": 7201,
        "memory_cap_mib": 12287,
        "train_prior_seed": 8302,
        "train_process_seed": 8402,
        "holdout_prior_seed": 9302,
        "holdout_process_seed": 9402,
        "audit_prior_seed": 9312,
        "audit_process_seed": 9502,
        "adaptive_training": False,
        "validation_check_every": 32,
        "plateau_patience": 5,
        "plateau_min_delta": 2e-6,
        "lr_reduction_factor": 0.25,
        "min_learning_rate": 2e-6,
        "early_stop_after_lr_drops": 5,
        "serialize_trained_cores": False,
    }
    for field, drift_value in drifts.items():
        args = _phase6w_rank4_args(
            runner,
            output=runner.PHASE6W_RANK4_L1_0_OUTPUT,
            l1_weight=0.0,
        )
        setattr(args, field, drift_value)
        with pytest.raises(ValueError, match=field):
            runner._guard_exact_fit_args(args, preflight)


def _phase6y_order3_args(runner):
    return SimpleNamespace(
        output=runner.PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_OUTPUT,
        preflight_json=runner.PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT,
        target_dimension=36,
        fit_rank=4,
        training_sample_count=276000,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=8608,
        optimizer_batch_size=4096,
        prefit_steps=0,
        train_steps=512,
        learning_rate=0.0003,
        l1_weight=0.0,
        l2_weight=1e-8,
        logz_anchor_weight=0.0,
        max_seconds=7200,
        memory_cap_mib=12288,
        basis_order=3,
        basis_num_elems=8,
        train_prior_seed=8303,
        train_process_seed=8403,
        holdout_prior_seed=9303,
        holdout_process_seed=9403,
        audit_prior_seed=9313,
        audit_process_seed=9503,
        adaptive_training=True,
        validation_check_every=16,
        plateau_patience=4,
        plateau_min_delta=1e-6,
        lr_reduction_factor=0.5,
        min_learning_rate=1e-6,
        early_stop_after_lr_drops=4,
        serialize_trained_cores=True,
    )


def _p88_phase2_order3_args(runner):
    args = _phase6y_order3_args(runner)
    args.output = runner.P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_OUTPUT
    args.preflight_json = runner.P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT
    return args


def test_p86_phase6y_degree_comparator_commands_are_frozen() -> None:
    runner = _load_runner()

    assert runner.PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py "
        "--phase6y-degree-comparator-preflight --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-2026-06-26.json"
    )
    assert runner.PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py --fit "
        "--preflight-json "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-2026-06-26.json "
        "--target-dimension 36 --fit-rank 4 --basis-order 3 --basis-num-elems 8 "
        "--training-sample-count 276000 --holdout-sample-count 65536 "
        "--audit-sample-count 65536 --seed 8608 --optimizer-batch-size 4096 "
        "--prefit-steps 0 --train-steps 512 --learning-rate 0.0003 "
        "--l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 "
        "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
        "--validation-check-every 16 --plateau-patience 4 "
        "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
        "--serialize-trained-cores --train-prior-seed 8303 "
        "--train-process-seed 8403 --holdout-prior-seed 9303 "
        "--holdout-process-seed 9403 --audit-prior-seed 9313 "
        "--audit-process-seed 9503 --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-26.json"
    )


def test_p88_phase2_degree_comparator_commands_are_frozen() -> None:
    runner = _load_runner()

    assert runner.P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py "
        "--p88-phase2-degree-comparator-preflight --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json"
    )
    assert runner.P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py --fit "
        "--preflight-json "
        "docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json "
        "--target-dimension 36 --fit-rank 4 --basis-order 3 --basis-num-elems 8 "
        "--training-sample-count 276000 --holdout-sample-count 65536 "
        "--audit-sample-count 65536 --seed 8608 --optimizer-batch-size 4096 "
        "--prefit-steps 0 --train-steps 512 --learning-rate 0.0003 "
        "--l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 "
        "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
        "--validation-check-every 16 --plateau-patience 4 "
        "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
        "--serialize-trained-cores --train-prior-seed 8303 "
        "--train-process-seed 8403 --holdout-prior-seed 9303 "
        "--holdout-process-seed 9403 --audit-prior-seed 9313 "
        "--audit-process-seed 9503 --output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json"
    )


def test_p86_phase6y_preflight_freezes_degree_comparator_protocol() -> None:
    runner = _load_runner()
    payload = runner.build_phase6y_degree_comparator_preflight_payload()

    assert payload["status"] == runner.STATUS_PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_READY
    assert payload["preflight_only"] is True
    assert payload["fit_executed"] is False
    assert payload["candidate_fit_command"] == (
        runner.PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND
    )
    assert payload["candidate_fit_commands"] == {
        "degree_order3_rank4_lr3e-4_l1_0": (
            runner.PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND
        )
    }
    assert payload["rank_budget"]["fit_rank"] == 4
    assert payload["rank_budget"]["P_theta"] == 13800
    assert payload["rank_budget"]["minimum_training_samples"] == 276000
    assert payload["rank_budget"]["training_sample_count"] == 276000
    assert payload["route_manifest"]["basis_order"] == 3
    assert payload["route_manifest"]["basis_num_elems"] == 8
    assert payload["route_manifest"]["basis_dim_per_dimension"] == 25
    assert payload["route_manifest"]["classification"] == "extension_or_invention"
    assert payload["basis_config"]["degree_comparator_classification"] == (
        "extension_or_invention"
    )
    assert payload["basis_config"]["degree_comparator_subtype"] == (
        "setup_static_degree_comparator_config"
    )
    assert payload["optimizer_budget"]["train_steps"] == 512
    assert payload["optimizer_budget"]["learning_rate"] == pytest.approx(3e-4)
    assert payload["optimizer_budget"]["adaptive_training"] is True
    assert payload["optimizer_budget"]["serialize_trained_cores"] is True
    assert payload["regularization_budget"]["l1_weight"] == pytest.approx(0.0)
    assert payload["regularization_budget"]["l2_weight"] == pytest.approx(1e-8)
    assert payload["cloud_seed_policy"]["train_prior_seed"] == 8303
    assert payload["cloud_seed_policy"]["audit_process_seed"] == 9503
    assert payload["reference_artifact_validation"]["status"] == "ok"
    assert payload["degree_comparator_protocol"]["future_fit_output_path_status"] == (
        "reserved_not_created_in_phase6y"
    )
    assert payload["phase6y_status_fields"]["phase7_status"] == (
        "blocked_until_degree_gate_reviewed_or_owner_reframed"
    )
    assert payload["gate_summary"]["overall_status"] == "ready_for_exact_claude_agreed_execution"
    assert any("does not run any fitting command" in item for item in payload["nonclaims"])
    assert any("no production readiness claim" in item for item in payload["nonclaims"])


def test_p88_phase2_preflight_uses_p88_named_artifact_identity() -> None:
    runner = _load_runner()
    payload = runner.build_p88_phase2_degree_comparator_preflight_payload()

    assert payload["status"] == runner.STATUS_P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY
    assert payload["preflight_only"] is True
    assert payload["fit_executed"] is False
    assert payload["phase_name"] == "P88 Phase 2 degree comparator preflight"
    assert payload["schema_version"] == "p88_phase2_degree_comparator_preflight.v1"
    assert payload["output"] == str(runner.P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT)
    assert payload["candidate_fit_command"] == (
        runner.P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND
    )
    assert str(runner.P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT) in (
        payload["candidate_fit_command"]
    )
    assert str(runner.P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_OUTPUT) in (
        payload["candidate_fit_command"]
    )
    assert str(runner.PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT) not in (
        payload["candidate_fit_command"]
    )
    assert str(runner.PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_OUTPUT) not in (
        payload["candidate_fit_command"]
    )
    assert payload["candidate_fit_commands"] == {
        "degree_order3_rank4_lr3e-4_l1_0": (
            runner.P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND
        )
    }
    assert payload["core_status_fields"]["reserved_preflight_output_path_status"] == "ok"
    assert payload["core_status_fields"]["reserved_fit_output_path_status"] == "ok"
    assert payload["degree_comparator_protocol"]["future_fit_output_path_status"] == (
        "reserved_not_created_in_p88_phase2"
    )
    assert payload["phase_subplan"] == (
        "docs/plans/"
        "bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-subplan-2026-06-27.md"
    )
    assert payload["phase_result"] == (
        "docs/plans/"
        "bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-result-2026-06-27.md"
    )
    assert payload["rank_budget"]["P_theta"] == 13800
    assert payload["gate_summary"]["overall_status"] == "ready_for_exact_claude_agreed_execution"


def test_p86_phase6y_reference_validation_rejects_default_basis_drift() -> None:
    runner = _load_runner()
    artifact = Path(runner.PHASE6W_RANK4_L1_0_OUTPUT)
    payload = runner.json.loads(artifact.read_text())

    ok = runner.validate_phase6y_default_order_reference_artifact(payload)
    assert ok["status"] == "ok"

    drifted = {
        **payload,
        "route_manifest": {
            **payload["route_manifest"],
            "basis_order": 3,
            "classification": "extension_or_invention",
        },
    }
    blocked = runner.validate_phase6y_default_order_reference_artifact(drifted)
    assert blocked["status"] == "block"
    assert blocked["field_statuses"]["basis_order"] is False
    assert blocked["field_statuses"]["basis_classification"] is False


def test_p86_phase6y_exact_guard_accepts_reserved_degree_arm() -> None:
    runner = _load_runner()
    preflight = runner.build_phase6y_degree_comparator_preflight_payload()

    runner._guard_exact_fit_args(_phase6y_order3_args(runner), preflight)


def test_p88_phase2_exact_guard_accepts_p88_reserved_degree_arm() -> None:
    runner = _load_runner()
    preflight = runner.build_p88_phase2_degree_comparator_preflight_payload()

    runner._guard_exact_fit_args(_p88_phase2_order3_args(runner), preflight)


def test_p88_phase2_exact_guard_rejects_p86_output_for_p88_preflight() -> None:
    runner = _load_runner()
    preflight = runner.build_p88_phase2_degree_comparator_preflight_payload()
    args = _p88_phase2_order3_args(runner)
    args.output = runner.PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_OUTPUT

    with pytest.raises(ValueError):
        runner._guard_exact_fit_args(args, preflight)


def test_p86_phase6y_exact_guard_rejects_frozen_drift() -> None:
    runner = _load_runner()
    preflight = runner.build_phase6y_degree_comparator_preflight_payload()
    drifts = {
        "output": runner.PHASE6W_RANK4_L1_0_OUTPUT,
        "preflight_json": runner.PHASE6W_SAME_POLICY_RANK_PREFLIGHT_OUTPUT,
        "target_dimension": 35,
        "fit_rank": 5,
        "training_sample_count": 275999,
        "holdout_sample_count": 65535,
        "audit_sample_count": 65535,
        "seed": 8609,
        "optimizer_batch_size": 2048,
        "prefit_steps": 1,
        "train_steps": 513,
        "learning_rate": 0.0001,
        "l1_weight": 1e-9,
        "l2_weight": 3e-8,
        "logz_anchor_weight": 1e-6,
        "max_seconds": 7201,
        "memory_cap_mib": 12287,
        "basis_order": 4,
        "basis_num_elems": 7,
        "train_prior_seed": 8304,
        "train_process_seed": 8404,
        "holdout_prior_seed": 9304,
        "holdout_process_seed": 9404,
        "audit_prior_seed": 9314,
        "audit_process_seed": 9504,
        "adaptive_training": False,
        "validation_check_every": 32,
        "plateau_patience": 5,
        "plateau_min_delta": 2e-6,
        "lr_reduction_factor": 0.25,
        "min_learning_rate": 2e-6,
        "early_stop_after_lr_drops": 5,
        "serialize_trained_cores": False,
    }
    for field, drift_value in drifts.items():
        args = _phase6y_order3_args(runner)
        setattr(args, field, drift_value)
        with pytest.raises(ValueError):
            runner._guard_exact_fit_args(args, preflight)


def test_p86_phase6y_cli_writes_no_fit_preflight_without_future_fit(
    tmp_path,
    monkeypatch,
) -> None:
    runner = _load_runner()
    preflight_output = tmp_path / "phase6y-degree-preflight.json"
    fit_output = tmp_path / "phase6y-degree-fit.json"
    preflight_command = (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py "
        f"--phase6y-degree-comparator-preflight --output {preflight_output}"
    )
    fit_command = (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py --fit "
        f"--preflight-json {preflight_output} "
        "--target-dimension 36 --fit-rank 4 --basis-order 3 --basis-num-elems 8 "
        "--training-sample-count 276000 --holdout-sample-count 65536 "
        "--audit-sample-count 65536 --seed 8608 --optimizer-batch-size 4096 "
        "--prefit-steps 0 --train-steps 512 --learning-rate 0.0003 "
        "--l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 "
        "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
        "--validation-check-every 16 --plateau-patience 4 "
        "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
        "--serialize-trained-cores --train-prior-seed 8303 "
        "--train-process-seed 8403 --holdout-prior-seed 9303 "
        "--holdout-process-seed 9403 --audit-prior-seed 9313 "
        f"--audit-process-seed 9503 --output {fit_output}"
    )
    monkeypatch.setattr(
        runner,
        "PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT",
        preflight_output,
    )
    monkeypatch.setattr(
        runner,
        "PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_OUTPUT",
        fit_output,
    )
    monkeypatch.setattr(
        runner,
        "PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_COMMAND",
        preflight_command,
    )
    monkeypatch.setattr(
        runner,
        "PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND",
        fit_command,
    )

    rc = runner.main(
        [
            "--phase6y-degree-comparator-preflight",
            "--output",
            str(preflight_output),
        ]
    )

    assert rc == 0
    payload = runner.json.loads(preflight_output.read_text())
    assert payload["status"] == runner.STATUS_PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_READY
    assert payload["fit_executed"] is False
    assert payload["candidate_fit_command"] == fit_command
    assert payload["degree_comparator_protocol"]["future_fit_output_path_status"] == (
        "reserved_not_created_in_phase6y"
    )
    assert not fit_output.exists()


def test_p88_phase2_cli_writes_no_fit_preflight_without_future_fit(
    tmp_path,
    monkeypatch,
) -> None:
    runner = _load_runner()
    preflight_output = tmp_path / "p88-phase2-degree-preflight.json"
    fit_output = tmp_path / "p88-phase2-degree-fit.json"
    preflight_command = (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py "
        f"--p88-phase2-degree-comparator-preflight --output {preflight_output}"
    )
    fit_command = (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_phase5_budget_fit.py --fit "
        f"--preflight-json {preflight_output} "
        "--target-dimension 36 --fit-rank 4 --basis-order 3 --basis-num-elems 8 "
        "--training-sample-count 276000 --holdout-sample-count 65536 "
        "--audit-sample-count 65536 --seed 8608 --optimizer-batch-size 4096 "
        "--prefit-steps 0 --train-steps 512 --learning-rate 0.0003 "
        "--l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 "
        "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
        "--validation-check-every 16 --plateau-patience 4 "
        "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
        "--serialize-trained-cores --train-prior-seed 8303 "
        "--train-process-seed 8403 --holdout-prior-seed 9303 "
        "--holdout-process-seed 9403 --audit-prior-seed 9313 "
        f"--audit-process-seed 9503 --output {fit_output}"
    )
    monkeypatch.setattr(
        runner,
        "P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT",
        preflight_output,
    )
    monkeypatch.setattr(
        runner,
        "P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_OUTPUT",
        fit_output,
    )
    monkeypatch.setattr(
        runner,
        "P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_COMMAND",
        preflight_command,
    )
    monkeypatch.setattr(
        runner,
        "P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND",
        fit_command,
    )

    rc = runner.main(
        [
            "--p88-phase2-degree-comparator-preflight",
            "--output",
            str(preflight_output),
        ]
    )

    assert rc == 0
    payload = runner.json.loads(preflight_output.read_text())
    assert payload["status"] == runner.STATUS_P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY
    assert payload["fit_executed"] is False
    assert payload["candidate_fit_command"] == fit_command
    assert payload["degree_comparator_protocol"]["future_fit_output_path_status"] == (
        "reserved_not_created_in_p88_phase2"
    )
    assert not fit_output.exists()


def test_p86_fit_exit_success_accepts_phase6w_completed_status() -> None:
    runner = _load_runner()

    assert runner._fit_status_succeeded(runner.STATUS_PHASE6W_RANK4_SAME_POLICY_COMPLETED)
    assert runner._fit_status_succeeded(runner.STATUS_PHASE6Y_DEGREE_ORDER3_COMPLETED)
    assert runner._fit_status_succeeded(runner.STATUS_P88_PHASE2_DEGREE_ORDER3_COMPLETED)
    assert not runner._fit_status_succeeded(
        runner.STATUS_PHASE6W_RANK4_SAME_POLICY_BLOCKED
    )


def test_p86_zhao_cui_l1_tuning_default_policy_is_procedure_not_scalar() -> None:
    runner = _load_runner()
    policy = runner._zhao_cui_regularization_default_policy()

    assert runner.DEFAULT_L1_WEIGHT == pytest.approx(0.0)
    assert policy["policy"] == runner.ZHAO_CUI_L1_TUNING_DEFAULT_POLICY
    assert policy["default_procedure"] == (
        "tune_l1_weight_under_reviewed_validation_audit_split"
    )
    assert policy["global_p75_l1_scalar_default"] == pytest.approx(0.0)
    assert policy["allowed_l1_comparator_arm"] == pytest.approx(0.0)
    assert 0.0 in tuple(policy["candidate_l1_grid"])
    assert 1e-9 in tuple(policy["candidate_l1_grid"])
    assert policy["validation_holdout_role"] == (
        "candidate_selection_and_veto_not_audit_not_production"
    )
    assert policy["audit_cloud_role"] == "reserved_final_only_not_tuning"
    assert policy["selection_status"] == runner.ZHAO_CUI_L1_TUNING_SELECTION_STATUS


def test_p86_phase5_runner_forbids_historical_als_training_route() -> None:
    runner = _load_runner()
    source = Path(runner.__file__).read_text()

    assert "FixedTTFitter" not in source
    assert "FixedTTFitConfig" not in source
    assert "FixedTTFitSampleBatch" not in source
    assert "TrainableFunctionalTT" in source
    assert runner.TRAINING_BASE_SMOKE_COMMAND.startswith(
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    )
    assert "--training-base-smoke" in runner.TRAINING_BASE_SMOKE_COMMAND


def test_p86_phase5_training_base_initializer_activates_lagrangep_constant_path() -> None:
    runner = _load_runner()
    product_basis = runner.p85_author_sir_lagrangep_algebraic_product_basis_spec(
        dimension=2,
        convention=runner._convention(),
    ).build_product_basis()
    ranks = (1, 1, 1)
    cores = runner._training_base_initial_cores(
        product_basis=product_basis,
        ranks=ranks,
        constant_value=tf.constant(0.5, dtype=tf.float64),
    )
    config = runner._trainer_config(
        product_basis=product_basis,
        ranks=ranks,
        seed=8605,
        learning_rate=0.001,
    )
    trainer = runner.TrainableFunctionalTT(config, initial_cores=cores)
    points = tf.zeros([3, 2], dtype=tf.float64)

    values = trainer.evaluate(points)

    assert bool(tf.reduce_all(tf.math.is_finite(values)).numpy())
    tf.debugging.assert_near(values, tf.ones([3], dtype=tf.float64) * 0.5)
    assert runner._trainable_component_active(trainer.sqrt_square_normalizer())


def test_p86_phase5_source_fit_batch_feeds_physical_coordinates_to_algebraic_basis(monkeypatch) -> None:
    runner = _load_runner()

    class _Model:
        @staticmethod
        def simulate(final_time, seed):
            del final_time, seed
            return None, [None, object()]

        @staticmethod
        def parameter_dim():
            return 1

        @staticmethod
        def state_dim():
            return 1

    class _Batch:
        samples = tf.constant(
            [
                [0.0, 1.0, -1.0],
                [0.5, -0.5, 0.25],
                [2.0, -2.0, 0.0],
            ],
            dtype=tf.float64,
        )
        log_weights = tf.zeros([3], dtype=tf.float64)

    class _Push:
        augmented_batch = _Batch()

    class _Frame:
        matrix = tf.eye(3, dtype=tf.float64)
        mu = tf.zeros([3], dtype=tf.float64)

        @staticmethod
        def log_abs_det():
            return tf.constant(0.0, dtype=tf.float64)

    class _Components:
        def __init__(self, **_kwargs):
            pass

        @staticmethod
        def negative_log_physical_density(*, physical_points, time_index, previous_retained_object):
            del time_index, previous_retained_object
            return tf.reduce_sum(tf.square(physical_points), axis=0)

    monkeypatch.setattr(runner, "zhao_cui_sir_austria_model", lambda: _Model())
    monkeypatch.setattr(
        runner,
        "_p59_author_sir_prior_sample_batch",
        lambda **_kwargs: object(),
    )
    monkeypatch.setattr(
        runner,
        "_p59_author_sir_source_push_result",
        lambda **_kwargs: _Push(),
    )
    monkeypatch.setattr(runner, "source_route_recenter", lambda **_kwargs: _Frame())
    monkeypatch.setattr(
        runner,
        "_p59_author_sir_deterministic_weighted_resample",
        lambda *, samples, log_weights: (samples, tf.range(tf.shape(samples)[1])),
    )
    monkeypatch.setattr(
        runner,
        "_p59_author_sir_source_density_callbacks",
        lambda *_args: (lambda *_: 0.0, lambda *_: 0.0, lambda *_: 0.0),
    )
    monkeypatch.setattr(runner, "SourceRouteSequentialDensityComponents", _Components)

    payload = runner._source_fit_batch(sample_count=3, holdout_sample_count=0)

    expected_physical_points = tf.transpose(_Batch.samples)
    expected_reference_points = runner.product_basis_domain_map().to_reference(
        expected_physical_points,
    )
    assert payload["points"].numpy() == pytest.approx(expected_physical_points.numpy())
    assert tuple(payload["fit_data_manifest"]["basis_points_shape"]) == (3, 3)
    assert tuple(payload["fit_data_manifest"]["reference_points_shape"]) == (3, 3)
    assert bool(
        tf.reduce_any(
            tf.abs(payload["points"] - expected_reference_points) > 1e-12
        ).numpy()
    )
