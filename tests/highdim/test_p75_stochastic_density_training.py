from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter.highdim import source_route
from bayesfilter.highdim import stochastic_density_training as p75


def _load_script(name: str, relative: str):
    script_path = Path(__file__).resolve().parents[2] / relative
    spec = importlib.util.spec_from_file_location(name, script_path)
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


def _basis(dimension: int = 2, degree: int = 1) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree) for _ in range(dimension)],
        _convention(),
    )


def _config() -> p75.P75TrainableTTConfig:
    return p75.P75TrainableTTConfig(
        product_basis=_basis(),
        ranks=(1, 2, 1),
        tau=tf.constant(1e-6, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-14, dtype=tf.float64),
        denominator_floor=tf.constant(1e-300, dtype=tf.float64),
        l2_weight=tf.constant(1e-6, dtype=tf.float64),
        learning_rate=1e-3,
        gradient_clip_norm=10.0,
        seed=7501,
    )


def _initial_cores() -> tuple[tf.Tensor, tf.Tensor]:
    return (
        tf.constant(
            [
                [[0.4, -0.1], [0.2, 0.3]],
            ],
            dtype=tf.float64,
        ),
        tf.constant(
            [
                [[0.5], [0.1]],
                [[-0.2], [0.4]],
            ],
            dtype=tf.float64,
        ),
    )


def _points() -> tf.Tensor:
    return tf.constant(
        [
            [-0.75, -0.25],
            [-0.25, 0.50],
            [0.25, -0.50],
            [0.75, 0.25],
        ],
        dtype=tf.float64,
    )


def _batch() -> p75.P75ObjectiveBatch:
    points = _points()
    target_values = tf.exp(-0.25 * tf.reduce_sum(tf.square(points), axis=1))
    records = tuple(
        {
            "point_id": f"p75-test-{index}",
            "cloud_hash": "train-cloud",
            "role": "fit",
        }
        for index in range(int(points.shape[0]))
    )
    forbidden = ({"point_id": "audit-0", "cloud_hash": "audit-cloud", "role": "audit"},)
    return p75.P75ObjectiveBatch(
        points=points,
        target_values=target_values,
        weights=tf.constant([1.0, 2.0, 1.5, 0.5], dtype=tf.float64),
        point_records=records,
        forbidden_audit_records=forbidden,
        provenance_label="unit_test_training_only",
    )


def test_trainable_variables_are_watched_and_gradients_are_finite():
    trainer = p75.TrainableFunctionalTT(_config(), initial_cores=_initial_cores())
    batch = _batch()

    with tf.GradientTape() as tape:
        terms = trainer.objective(batch)
    gradients = tape.gradient(terms.total_loss, trainer.variables)

    assert len(gradients) == len(trainer.variables)
    assert all(gradient is not None for gradient in gradients)
    assert all(bool(tf.reduce_all(tf.math.is_finite(gradient)).numpy()) for gradient in gradients)
    assert bool(tf.math.is_finite(terms.total_loss).numpy())


def test_trainable_normalizer_rho_and_log_density_match_snapshot_density():
    trainer = p75.TrainableFunctionalTT(_config(), initial_cores=_initial_cores())
    density = trainer.snapshot_density()
    points = _points()

    assert trainer.normalizer().numpy() == pytest.approx(density.normalizer().numpy())
    assert trainer.rho_theta(points).numpy() == pytest.approx(
        density.unnormalized_density(points).numpy()
    )
    assert trainer.log_density(points).numpy() == pytest.approx(
        density.log_density(points).numpy()
    )


def test_weighted_empirical_cross_entropy_weights_match_formula():
    trainer = p75.TrainableFunctionalTT(_config(), initial_cores=_initial_cores())
    batch = _batch()

    alpha = trainer.weighted_empirical_cross_entropy_weights(batch)
    q0 = tf.exp(trainer.defensive_density.log_density(batch.points))
    expected_raw = batch.weights * (tf.square(batch.target_values) + trainer.config.tau * q0)
    expected = expected_raw / tf.reduce_sum(expected_raw)

    assert alpha.numpy() == pytest.approx(expected.numpy())
    assert float(tf.reduce_sum(alpha).numpy()) == pytest.approx(1.0)


def test_uniform_constant_special_case_is_unweighted():
    trainer = p75.TrainableFunctionalTT(_config(), initial_cores=_initial_cores())
    points = _points()
    batch = p75.P75ObjectiveBatch(
        points=points,
        target_values=tf.ones([int(points.shape[0])], dtype=tf.float64),
        weights=tf.ones([int(points.shape[0])], dtype=tf.float64),
    )

    alpha = trainer.weighted_empirical_cross_entropy_weights(batch)

    assert alpha.numpy() == pytest.approx([0.25, 0.25, 0.25, 0.25])


def test_one_adam_step_changes_a_core_finitely():
    trainer = p75.TrainableFunctionalTT(_config(), initial_cores=_initial_cores())
    optimizer = p75.make_adam_optimizer(trainer.config)
    before = tuple(tf.identity(core) for core in trainer.variables)

    terms = trainer.train_step(_batch(), optimizer)
    deltas = [tf.norm(new - old) for old, new in zip(before, trainer.variables)]

    assert terms.gradient_norm is not None
    assert bool(tf.reduce_all(tf.math.is_finite(tf.stack(deltas))).numpy())
    assert bool(tf.reduce_any(tf.stack(deltas) > 0.0).numpy())


def test_l1_regularization_is_validated_reported_and_added_to_objective():
    base_config = _config()
    l1_weight = tf.constant(0.25, dtype=tf.float64)
    l2_weight = tf.constant(0.125, dtype=tf.float64)
    config = p75.P75TrainableTTConfig(
        product_basis=base_config.product_basis,
        ranks=base_config.ranks,
        tau=base_config.tau,
        normalizer_floor=base_config.normalizer_floor,
        denominator_floor=base_config.denominator_floor,
        l1_weight=l1_weight,
        l2_weight=l2_weight,
        learning_rate=base_config.learning_rate,
        gradient_clip_norm=base_config.gradient_clip_norm,
        seed=base_config.seed,
    )
    trainer = p75.TrainableFunctionalTT(config, initial_cores=_initial_cores())
    batch = _batch()

    terms = trainer.objective(batch)
    payload = p75.config_payload(config)
    l1 = tf.add_n([tf.reduce_sum(tf.abs(core)) for core in trainer.variables])
    l2 = tf.add_n([tf.reduce_sum(tf.square(core)) for core in trainer.variables])
    expected_regularization = l1_weight * l1 + l2_weight * l2

    assert payload["l1_weight"] == pytest.approx(0.25)
    assert payload["l2_weight"] == pytest.approx(0.125)
    assert float(terms.regularization.numpy()) == pytest.approx(
        float(expected_regularization.numpy())
    )


@pytest.mark.parametrize(
    "bad_weight",
    [
        tf.constant(-1.0, dtype=tf.float64),
        tf.constant(float("nan"), dtype=tf.float64),
        tf.constant([0.0], dtype=tf.float64),
    ],
)
def test_l1_regularization_weight_rejects_invalid_scalars(bad_weight):
    with pytest.raises(ValueError):
        p75.P75TrainableTTConfig(
            product_basis=_basis(),
            ranks=(1, 2, 1),
            l1_weight=bad_weight,
        )


def test_square_root_prefit_step_reduces_synthetic_training_loss():
    config = _config()
    trainer = p75.TrainableFunctionalTT(config, initial_cores=_initial_cores())
    batch = _batch()
    optimizer = p75.make_adam_optimizer(config)
    reference = tuple(tf.identity(core) for core in trainer.variables)

    before = trainer.square_root_prefit_objective(
        batch,
        reference_cores=reference,
        reference_l2_weight=tf.constant(0.0, dtype=tf.float64),
    )
    step = trainer.square_root_prefit_step(
        batch,
        optimizer,
        reference_cores=reference,
        reference_l2_weight=tf.constant(0.0, dtype=tf.float64),
    )
    after = trainer.square_root_prefit_objective(
        batch,
        reference_cores=reference,
        reference_l2_weight=tf.constant(0.0, dtype=tf.float64),
    )

    assert step.gradient_norm is not None
    assert bool(tf.math.is_finite(step.total_loss).numpy())
    assert float(after.normalized_weighted_square_error.numpy()) < float(
        before.normalized_weighted_square_error.numpy()
    )
    payload = p75.prefit_terms_payload(step)
    assert payload["gradient_norm"] is not None
    assert payload["normalized_weighted_square_error"] >= 0.0


def test_audit_records_and_hash_overlap_are_rejected():
    points = _points()
    with pytest.raises(ValueError, match="audit role"):
        p75.P75ObjectiveBatch(
            points=points,
            target_values=tf.ones([4], dtype=tf.float64),
            weights=tf.ones([4], dtype=tf.float64),
            point_records=(
                {"point_id": "a0", "cloud_hash": "audit-cloud", "role": "audit"},
                {"point_id": "a1", "cloud_hash": "audit-cloud", "role": "fit"},
                {"point_id": "a2", "cloud_hash": "audit-cloud", "role": "fit"},
                {"point_id": "a3", "cloud_hash": "audit-cloud", "role": "fit"},
            ),
        )

    with pytest.raises(ValueError, match="forbidden audit cloud"):
        p75.P75ObjectiveBatch(
            points=points,
            target_values=tf.ones([4], dtype=tf.float64),
            weights=tf.ones([4], dtype=tf.float64),
            point_records=tuple(
                {"point_id": f"f{index}", "cloud_hash": "shared", "role": "fit"}
                for index in range(4)
            ),
            forbidden_audit_records=(
                {"point_id": "a0", "cloud_hash": "shared", "role": "audit"},
            ),
        )


def test_p75_is_not_exported_by_highdim_default_namespace():
    assert "P75TrainableTTConfig" not in highdim.__all__
    assert not hasattr(highdim, "P75TrainableTTConfig")


def test_p73_blocked_status_and_p72_p73_import_paths_remain_unchanged():
    status = source_route.p73_density_aware_optimizer_status()
    assert status["status"] == source_route.P73_B_OPTIMIZER_BLOCKED

    p72_script = _load_script(
        "p72_support_certified_lower_gate_diagnostic",
        "scripts/p72_support_certified_lower_gate_diagnostic.py",
    )
    p73_script = _load_script(
        "p73_density_aware_renewal_diagnostic",
        "scripts/p73_density_aware_renewal_diagnostic.py",
    )
    assert hasattr(p72_script, "main")
    assert hasattr(p73_script, "main")

    p72_text = (Path(__file__).resolve().parents[2] / "scripts/p72_support_certified_lower_gate_diagnostic.py").read_text()
    p73_text = (Path(__file__).resolve().parents[2] / "scripts/p73_density_aware_renewal_diagnostic.py").read_text()
    assert "stochastic_density_training" not in p72_text
    assert "stochastic_density_training" not in p73_text


def test_p75_script_schema_and_smoke_are_cpu_only_and_not_pilot(tmp_path):
    module = _load_script(
        "p75_stochastic_density_training_pilot",
        "scripts/p75_stochastic_density_training_pilot.py",
    )
    schema_output = tmp_path / "p75-schema.json"
    smoke_output = tmp_path / "p75-smoke.json"

    assert module.main(["--schema-only", "--output", str(schema_output)]) == 0
    schema = json.loads(schema_output.read_text())
    assert schema["status"] == p75.P75_SCHEMA_STATUS
    assert schema["smoke_bounds"]["max_optimizer_steps"] == 2
    assert schema["smoke_bounds"]["max_batch_size"] == 8
    assert schema["smoke_bounds"]["zhao_cui_fresh_batches_allowed"] is False
    assert schema["gate_summary"]["phase4_target_pilot_executed"] is False

    assert module.main(["--smoke-only", "--output", str(smoke_output)]) == 0
    smoke = json.loads(smoke_output.read_text())
    assert smoke["status"] == p75.P75_SMOKE_STATUS
    assert smoke["run_manifest"]["environment"]["CUDA_VISIBLE_DEVICES"] == "-1"
    assert smoke["smoke_only_not_pilot_evidence"] is True
    assert smoke["phase4_target_pilot_executed"] is False
    assert smoke["smoke_bounds"]["optimizer_steps"] == 1
    assert smoke["smoke_bounds"]["zhao_cui_fresh_batches_used"] is False
    assert smoke["gate_summary"]["p73_b_optimizer_status"] == (
        source_route.P73_B_OPTIMIZER_BLOCKED
    )


def test_target_batch_and_line_target_orientation_contracts():
    module = _load_script(
        "p75_stochastic_density_training_pilot_orientation",
        "scripts/p75_stochastic_density_training_pilot.py",
    )

    class _Frame:
        dimension = 2
        matrix = tf.eye(2, dtype=tf.float64)
        mu = tf.zeros([2], dtype=tf.float64)

        @staticmethod
        def log_abs_det():
            return tf.constant(0.0, dtype=tf.float64)

    class _Components:
        @staticmethod
        def negative_log_physical_density(*, physical_points, time_index, previous_retained_object):
            del time_index, previous_retained_object
            points = tf.convert_to_tensor(physical_points, dtype=tf.float64)
            assert points.shape == (2, 3)
            return tf.reduce_sum(tf.square(points), axis=0)

    class _Data:
        local_fit_points = tf.constant(
            [[0.0, 0.5, -0.5], [1.0, -1.0, 0.25]],
            dtype=tf.float64,
        )
        target_values = tf.constant([1.0, 2.0, 3.0], dtype=tf.float64)
        fit_weights = tf.constant([1.0, 1.0, 1.0], dtype=tf.float64)

    batch = module._target_batch_from_data(_Data, label="orientation_test")
    assert batch.points.shape == (3, 2)
    assert batch.points.numpy() == pytest.approx(tf.transpose(_Data.local_fit_points).numpy())

    column_major_targets = module._target_values_for_reference_cloud(
        local_points=_Data.local_fit_points,
        frame=_Frame(),
        shift_constant=tf.constant(0.0, dtype=tf.float64),
        components=_Components(),
    )
    row_major_targets = module._target_values_for_points(
        points=tf.transpose(_Data.local_fit_points),
        frame=_Frame(),
        shift_constant=tf.constant(0.0, dtype=tf.float64),
        components=_Components(),
    )

    assert column_major_targets.shape == (3,)
    assert row_major_targets.numpy() == pytest.approx(column_major_targets.numpy())


def test_calibrated_constant_initializer_escapes_defensive_floor_on_synthetic_anchor():
    module = _load_script(
        "p75_stochastic_density_training_pilot_calibrated_init",
        "scripts/p75_stochastic_density_training_pilot.py",
    )
    config = module._synthetic_config()
    batch = module._synthetic_batch()

    cores, payload = module._calibrated_constant_initial_cores(config, batch)
    trainer = p75.TrainableFunctionalTT(config, initial_cores=cores)
    rho = trainer.rho_theta(batch.points)

    assert payload["mode"] == module.P75_CALIBRATED_CONSTANT_INIT_MODE
    assert payload["uses_audit_data"] is False
    assert float(tf.reduce_max(rho).numpy()) > 10.0 * float(config.tau.numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(rho)).numpy())


def test_source_guided_prefit_runner_mode_uses_training_only_batches():
    module = _load_script(
        "p75_stochastic_density_training_pilot_source_guided_prefit",
        "scripts/p75_stochastic_density_training_pilot.py",
    )
    context = module._target_context(batch_size=4, batches=1, prefit_batches=1)
    payload = module._target_pilot_payload_from_context(
        Path("/tmp/p75-source-guided-prefit-unit.json"),
        "unit-test-command",
        degree=1,
        rank=1,
        batch_size=4,
        batches=1,
        max_seconds=180.0,
        seed=7501,
        init_mode=module.P75_SOURCE_GUIDED_PREFIT_INIT_MODE,
        prefit_steps=1,
        context=context,
    )

    target = payload["target_pilot"]
    init = target["initialization"]
    prefit = init["prefit"]

    assert target["init_mode"] == module.P75_SOURCE_GUIDED_PREFIT_INIT_MODE
    assert init["uses_audit_data"] is False
    assert prefit["uses_audit_data"] is False
    assert prefit["completed_steps"] == 1
    assert target["completed_batches"] == 1
    assert target["training_seed_policy"]["density_training_batches_reused_for_all_arms"] is True
    assert target["training_seed_policy"]["prefit_and_density_training_batches_disjoint"] is True
    assert target["fresh_audit"]["audit_seed_policy"]["not_training_seeds"] is True


def test_phase10_ladder_schedule_stays_inside_reviewed_bounds():
    module = _load_script(
        "p75_capacity_sample_ladder_schedule",
        "scripts/p75_capacity_sample_ladder.py",
    )
    rows = module.DEFAULT_LADDER_ROWS
    arm_count = sum(3 if row["prefit_steps"] > 0 else 2 for row in rows)

    assert len(rows) <= 16
    assert arm_count <= 16
    assert {row["degree"] for row in rows} == {1, 2}
    assert {row["rank"] for row in rows} == {1, 2}
    assert {row["batch_size"] for row in rows} == {32, 64}
    assert {row["batches"] for row in rows} == {2, 4}
    assert {row["prefit_steps"] for row in rows} == {0, 5, 10}


def test_phase10_ladder_classifier_applies_frozen_10_percent_rule():
    module = _load_script(
        "p75_capacity_sample_ladder_classifier",
        "scripts/p75_capacity_sample_ladder.py",
    )
    row = {
        "row_id": 99,
        "degree": 1,
        "rank": 1,
        "batch_size": 32,
        "batches": 2,
        "prefit_steps": 5,
        "seed": 7501,
    }
    payload = {
        "same_draws_policy": {
            "anchor_reused_for_all_arms": True,
            "training_batches_reused_for_all_arms": True,
            "audit_seeds_reused_for_all_arms": True,
            "audit_data_not_used_for_initialization": True,
        },
        "arms": {
            module.pilot.P75_CALIBRATED_CONSTANT_INIT_MODE: {
                "target_pilot": {
                    "completed_batches": 2,
                    "fresh_audit": {
                        "holdout": {"rms_relative": 1.0},
                        "line_gate": {"line_residual_rms": 10.0},
                    },
                }
            },
            module.pilot.P75_SOURCE_GUIDED_PREFIT_INIT_MODE: {
                "target_pilot": {
                    "completed_batches": 2,
                    "training_seed_policy": {
                        "prefit_and_density_training_batches_disjoint": True,
                    },
                    "initialization": {
                        "uses_audit_data": False,
                        "prefit": {
                            "uses_audit_data": False,
                            "completed_steps": 5,
                            "final_terms": {"status": "ok"},
                        },
                    },
                    "fresh_audit": {
                        "audit_seed_policy": {"not_training_seeds": True},
                        "holdout": {"rms_relative": 0.89},
                        "line_gate": {"line_residual_rms": 10.9},
                    },
                }
            },
        },
    }

    win = module.classify_ladder_row(row, payload)
    assert win["status"] == "mechanism_win"
    assert win["holdout_improved_at_least_10_percent"] is True
    assert win["audit_line_not_worse_by_more_than_10_percent"] is True

    payload["arms"][module.pilot.P75_SOURCE_GUIDED_PREFIT_INIT_MODE][
        "target_pilot"
    ]["fresh_audit"]["holdout"]["rms_relative"] = 0.91
    loss = module.classify_ladder_row(row, payload)
    assert loss["status"] == "mechanism_loss"
    assert "holdout_improvement_less_than_10_percent" in loss["reasons"]
