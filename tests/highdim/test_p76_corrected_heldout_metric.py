from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter.highdim import stochastic_density_training as p75


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


def _config(*, tau: float = 2.5) -> p75.P75TrainableTTConfig:
    return p75.P75TrainableTTConfig(
        product_basis=_basis(),
        ranks=(1, 2, 1),
        tau=tf.constant(tau, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-14, dtype=tf.float64),
        denominator_floor=tf.constant(1e-300, dtype=tf.float64),
        l2_weight=tf.constant(0.0, dtype=tf.float64),
        learning_rate=1e-3,
        gradient_clip_norm=10.0,
        seed=7608,
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


def _metric_records(role: str = "heldout_metric") -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "point_id": f"p76-metric-{index}",
            "role": role,
            "provenance_label": "unit_test_reviewed_target_bridge",
        }
        for index in range(4)
    )


def _metric_batch(
    *,
    points: tf.Tensor | None = None,
    target_sqrt_values: tf.Tensor | None = None,
    integration_weights: tf.Tensor | None = None,
    role: str = "heldout_metric",
    provenance_label: str = "unit_test_reviewed_target_bridge",
    point_records: tuple[dict[str, str], ...] | None = None,
) -> p75.P76CorrectedHeldoutMetricBatch:
    return p75.P76CorrectedHeldoutMetricBatch(
        points=_points() if points is None else points,
        target_sqrt_values=(
            tf.constant([0.0, 0.5, 1.0, 2.0], dtype=tf.float64)
            if target_sqrt_values is None
            else target_sqrt_values
        ),
        integration_weights=(
            tf.constant([1.0, 2.0, 1.5, 0.5], dtype=tf.float64)
            if integration_weights is None
            else integration_weights
        ),
        role=role,
        provenance_label=provenance_label,
        point_records=_metric_records(role) if point_records is None else point_records,
    )


def test_corrected_metric_uses_target_only_alpha_and_exact_ce_decomposition() -> None:
    trainer = p75.TrainableFunctionalTT(_config(), initial_cores=_initial_cores())
    batch = _metric_batch()

    terms = trainer.corrected_heldout_density_metric(batch)
    alpha = trainer.corrected_heldout_metric_weights(batch)
    raw = batch.integration_weights * tf.square(batch.target_sqrt_values)
    expected_alpha = raw / tf.reduce_sum(raw)
    rho = trainer.rho_theta(batch.points)
    expected_ce = -tf.reduce_sum(expected_alpha * tf.math.log(rho)) + tf.math.log(
        trainer.normalizer()
    )

    assert alpha.numpy() == pytest.approx(expected_alpha.numpy())
    assert float(terms.heldout_cross_entropy.numpy()) == pytest.approx(
        float(expected_ce.numpy())
    )
    assert float(terms.negative_weighted_log_rho.numpy()) == pytest.approx(
        float((-tf.reduce_sum(expected_alpha * tf.math.log(rho))).numpy())
    )
    assert float(terms.log_normalizer.numpy()) == pytest.approx(
        float(tf.math.log(trainer.normalizer()).numpy())
    )
    assert float(terms.alpha_sum.numpy()) == pytest.approx(1.0)


def test_corrected_metric_differs_from_historical_tau_q0_training_helper() -> None:
    trainer = p75.TrainableFunctionalTT(_config(tau=5.0), initial_cores=_initial_cores())
    metric_batch = _metric_batch()
    training_batch = p75.P75ObjectiveBatch(
        points=metric_batch.points,
        target_values=metric_batch.target_sqrt_values,
        weights=metric_batch.integration_weights,
    )

    corrected_alpha = trainer.corrected_heldout_metric_weights(metric_batch)
    historical_alpha = trainer.weighted_empirical_cross_entropy_weights(training_batch)
    expected_raw = metric_batch.integration_weights * tf.square(
        metric_batch.target_sqrt_values
    )
    expected_corrected = expected_raw / tf.reduce_sum(expected_raw)

    assert corrected_alpha.numpy() == pytest.approx(expected_corrected.numpy())
    assert historical_alpha.numpy() != pytest.approx(corrected_alpha.numpy())
    assert float(corrected_alpha[0].numpy()) == pytest.approx(0.0)
    assert float(historical_alpha[0].numpy()) > 0.0


def test_metric_batch_is_not_duck_compatible_with_training_objective_batch() -> None:
    batch = _metric_batch()

    assert not isinstance(batch, p75.P75ObjectiveBatch)
    assert not hasattr(batch, "target_values")
    assert not hasattr(batch, "weights")


@pytest.mark.parametrize("role", ["", "fit", "train", "training", "prefit", "audit"])
def test_metric_batch_rejects_missing_or_training_roles(role: str) -> None:
    with pytest.raises(ValueError, match="metric role"):
        _metric_batch(role=role, point_records=_metric_records("heldout_metric"))


@pytest.mark.parametrize(
    "provenance",
    [
        "",
        "train_cloud",
        "fit_cloud",
        "source_prefit",
        "source-guided-prefit",
        "selection_metric",
        "stopping_metric",
        "tuning_metric",
        "unreviewed_target_bridge",
        "unknown_metric_source",
    ],
)
def test_metric_batch_rejects_missing_forbidden_or_unreviewed_provenance(
    provenance: str,
) -> None:
    with pytest.raises(ValueError, match="provenance"):
        _metric_batch(provenance_label=provenance)


def test_metric_batch_rejects_bad_point_record_role_and_provenance() -> None:
    missing_role_records = tuple(
        {
            "point_id": f"missing-role-{index}",
            "provenance_label": "unit_test_reviewed_target_bridge",
        }
        for index in range(4)
    )
    with pytest.raises(ValueError, match="metric role"):
        _metric_batch(point_records=missing_role_records)

    bad_role_records = tuple(
        {
            "point_id": f"bad-role-{index}",
            "role": "fit" if index == 0 else "heldout_metric",
            "provenance_label": "unit_test_reviewed_target_bridge",
        }
        for index in range(4)
    )
    with pytest.raises(ValueError, match="metric role"):
        _metric_batch(point_records=bad_role_records)

    bad_provenance_records = tuple(
        {
            "point_id": f"bad-prov-{index}",
            "role": "heldout_metric",
            "provenance_label": "train_cloud" if index == 0 else "unit_test_reviewed_target_bridge",
        }
        for index in range(4)
    )
    with pytest.raises(ValueError, match="provenance"):
        _metric_batch(point_records=bad_provenance_records)

    missing_provenance_records = tuple(
        {
            "point_id": f"missing-prov-{index}",
            "role": "heldout_metric",
        }
        for index in range(4)
    )
    with pytest.raises(ValueError, match="provenance"):
        _metric_batch(point_records=missing_provenance_records)


def test_metric_batch_vetoes_zero_target_mass_but_accepts_zero_positive_mix() -> None:
    _metric_batch(target_sqrt_values=tf.constant([0.0, 0.0, 1.0, 0.0], dtype=tf.float64))

    with pytest.raises(ValueError, match="target mass"):
        _metric_batch(target_sqrt_values=tf.zeros([4], dtype=tf.float64))


def test_metric_batch_vetoes_nonfinite_negative_and_shape_errors() -> None:
    with pytest.raises(ValueError, match="points"):
        _metric_batch(
            points=tf.constant(
                [
                    [0.0, 0.0],
                    [float("nan"), 0.0],
                    [0.25, -0.5],
                    [0.75, 0.25],
                ],
                dtype=tf.float64,
            )
        )

    with pytest.raises(ValueError, match="target_sqrt_values"):
        _metric_batch(target_sqrt_values=tf.constant([0.0, 1.0, float("nan"), 2.0], dtype=tf.float64))

    with pytest.raises(ValueError, match="integration_weights"):
        _metric_batch(integration_weights=tf.constant([1.0, 1.0, float("nan"), 1.0], dtype=tf.float64))

    with pytest.raises(ValueError, match="nonnegative"):
        _metric_batch(integration_weights=tf.constant([1.0, -1.0, 1.0, 1.0], dtype=tf.float64))

    with pytest.raises(ValueError, match="target_sqrt_values"):
        _metric_batch(target_sqrt_values=tf.ones([3], dtype=tf.float64))

    with pytest.raises(ValueError, match="points"):
        trainer = p75.TrainableFunctionalTT(_config(), initial_cores=_initial_cores())
        bad_dimension_batch = p75.P76CorrectedHeldoutMetricBatch(
            points=tf.zeros([4, 3], dtype=tf.float64),
            target_sqrt_values=tf.ones([4], dtype=tf.float64),
            integration_weights=tf.ones([4], dtype=tf.float64),
            role="heldout_metric",
            provenance_label="unit_test_reviewed_target_bridge",
        )
        trainer.corrected_heldout_density_metric(bad_dimension_batch)


def test_metric_payload_preserves_boundary_and_nonclaims() -> None:
    trainer = p75.TrainableFunctionalTT(_config(), initial_cores=_initial_cores())
    terms = trainer.corrected_heldout_density_metric(_metric_batch(role="audit_metric"))
    payload = p75.corrected_heldout_metric_terms_payload(terms)

    assert payload["schema_version"] == p75.P76_CORRECTED_HELDOUT_METRIC_SCHEMA_VERSION
    assert payload["status"] == p75.P76_CORRECTED_HELDOUT_METRIC_STATUS
    assert payload["classification"] == "extension_or_invention"
    assert payload["role"] == "audit_metric"
    assert payload["provenance_label"] == "unit_test_reviewed_target_bridge"
    assert payload["explanatory_only"] is True
    assert payload["not_training_or_selection"] is True
    assert payload["finite_flags"] == {
        "heldout_cross_entropy": True,
        "normalizer": True,
        "target_mass": True,
        "alpha": True,
        "rho": True,
    }
    assert "not fit-quality evidence" in payload["nonclaims"]
    assert "not source-faithful Zhao-Cui" in payload["nonclaims"]
