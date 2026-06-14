from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


class _DummyTransport:
    def manifest_payload(self) -> dict[str, object]:
        return {"family": "p49_dummy_transport", "version": 1}


class _HiddenTransport:
    pass


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _frame(dim: int = 2) -> highdim.SourceRouteCoordinateFrame:
    return highdim.SourceRouteCoordinateFrame(
        mu=tf.zeros([dim], dtype=DTYPE),
        matrix=tf.eye(dim, dtype=DTYPE),
        expansion_factor=1.25,
    )


def _samples() -> tf.Tensor:
    return tf.constant(
        [
            [0.0, 0.25, -0.5],
            [1.0, -0.25, 0.5],
        ],
        dtype=DTYPE,
    )


def _log_weights() -> tf.Tensor:
    return tf.math.log(tf.constant([0.2, 0.3, 0.5], dtype=DTYPE))


def _normalizer() -> highdim.SourceRouteNormalizerContribution:
    return highdim.SourceRouteNormalizerContribution(
        log_transport_normalizer=tf.math.log(tf.constant(2.5, dtype=DTYPE)),
        shift_constant=tf.constant(0.75, dtype=DTYPE),
        log_abs_det_policy="included_in_target",
    )


def _diagnostics() -> highdim.SourceRouteSampleDiagnostics:
    log_weights = _log_weights()
    return highdim.SourceRouteSampleDiagnostics(
        sample_count=3,
        effective_sample_size=highdim.effective_sample_size_from_log_weights(log_weights),
        enhancement_attempts=1,
    )


def _identity(
    *,
    route_label: str = highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
    storage_kind: str = "source_transport_object",
    transition_interface: str = "sample_propagation",
) -> highdim.BranchIdentity:
    return highdim.source_route_retained_object_identity(
        transport_object=_DummyTransport(),
        coordinate_frame=_frame(),
        samples=_samples(),
        log_weights=_log_weights(),
        sample_diagnostics=_diagnostics(),
        normalizer=_normalizer(),
        measure_convention=_convention(),
        route_label=route_label,
        storage_kind=storage_kind,
        transition_interface=transition_interface,
        diagnostics={"phase": "P49-M2"},
    )


def _retained_object(
    *,
    route_label: str = highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
    storage_kind: str = "source_transport_object",
    transition_interface: str = "sample_propagation",
) -> highdim.SourceRouteRetainedObject:
    return highdim.SourceRouteRetainedObject(
        transport_object=_DummyTransport(),
        coordinate_frame=_frame(),
        samples=_samples(),
        log_weights=_log_weights(),
        sample_diagnostics=_diagnostics(),
        normalizer=_normalizer(),
        measure_convention=_convention(),
        route_label=route_label,
        storage_kind=storage_kind,
        transition_interface=transition_interface,
        branch_identity=_identity(
            route_label=route_label,
            storage_kind=storage_kind,
            transition_interface=transition_interface,
        ),
        diagnostics={"phase": "P49-M2"},
    )


def test_p49_source_route_retained_object_accepts_transport_skeleton() -> None:
    retained = _retained_object()

    assert retained.route_label == highdim.SOURCE_FAITHFUL_ROUTE_LABEL
    assert retained.storage_kind == "source_transport_object"
    assert retained.transition_interface == "sample_propagation"
    assert retained.samples.shape == (2, 3)
    assert retained.log_weights.shape == (3,)
    assert retained.coordinate_frame.log_abs_det().shape == ()
    tf.debugging.assert_near(
        retained.normalizer.log_increment(),
        tf.math.log(tf.constant(2.5, dtype=DTYPE)) - tf.constant(0.75, dtype=DTYPE),
    )
    assert retained.branch_identity.hash.value == _identity().hash.value


@pytest.mark.parametrize(
    "storage_kind",
    [
        "scalar_dense_grid",
        "scalar_tt_grid",
        "multistate_tt_grid",
        "all_axes_tensor_product_grid",
    ],
)
def test_p49_source_route_retained_object_rejects_all_grid_storage(storage_kind: str) -> None:
    with pytest.raises(ValueError, match="all-grid retained storage"):
        _identity(storage_kind=storage_kind)


@pytest.mark.parametrize(
    "transition_interface",
    [
        "pairwise_grid_transition",
        "all_grid_pairwise_transition",
        "multistate_grid_pairwise_transition",
    ],
)
def test_p49_source_route_retained_object_rejects_pairwise_grid_transition(
    transition_interface: str,
) -> None:
    with pytest.raises(ValueError, match="pairwise grid propagation"):
        _identity(transition_interface=transition_interface)


def test_p49_fixed_branch_route_label_can_still_describe_grid_retention() -> None:
    retained = _retained_object(
        route_label=highdim.GRADIENT_ADAPTATION_ROUTE_LABEL,
        storage_kind="multistate_tt_grid",
        transition_interface="pairwise_grid_transition",
    )

    assert retained.route_label == highdim.GRADIENT_ADAPTATION_ROUTE_LABEL
    assert retained.storage_kind == "multistate_tt_grid"
    assert retained.transition_interface == "pairwise_grid_transition"


def test_p49_source_route_retained_object_rejects_branch_mismatch() -> None:
    good_identity = _identity()
    bad_identity = highdim.BranchIdentity(
        manifest=highdim.BranchManifest(
            version=good_identity.manifest.version,
            payload={**good_identity.manifest.payload, "route_label": "blocked"},
        ),
        hash=highdim.BranchManifest(
            version=good_identity.manifest.version,
            payload={**good_identity.manifest.payload, "route_label": "blocked"},
        ).sha256(),
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_BRANCH_MISMATCH.value):
        highdim.SourceRouteRetainedObject(
            transport_object=_DummyTransport(),
            coordinate_frame=_frame(),
            samples=_samples(),
            log_weights=_log_weights(),
            sample_diagnostics=_diagnostics(),
            normalizer=_normalizer(),
            measure_convention=_convention(),
            route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
            storage_kind="source_transport_object",
            transition_interface="sample_propagation",
            branch_identity=bad_identity,
            diagnostics={"phase": "P49-M2"},
        )


def test_p49_source_route_retained_object_rejects_bad_sample_shape() -> None:
    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_SHAPE.value):
        highdim.SourceRouteRetainedObject(
            transport_object=_DummyTransport(),
            coordinate_frame=_frame(),
            samples=tf.zeros([3, 3], dtype=DTYPE),
            log_weights=_log_weights(),
            sample_diagnostics=_diagnostics(),
            normalizer=_normalizer(),
            measure_convention=_convention(),
            route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
            storage_kind="source_transport_object",
            transition_interface="sample_propagation",
            branch_identity=_identity(),
            diagnostics={"phase": "P49-M2"},
        )


def test_p49_source_route_retained_object_requires_transport_manifest() -> None:
    with pytest.raises(TypeError, match="manifest_payload"):
        highdim.source_route_retained_object_identity(
            transport_object=_HiddenTransport(),
            coordinate_frame=_frame(),
            samples=_samples(),
            log_weights=_log_weights(),
            sample_diagnostics=_diagnostics(),
            normalizer=_normalizer(),
            measure_convention=_convention(),
            route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
            storage_kind="source_transport_object",
            transition_interface="sample_propagation",
            diagnostics={"phase": "P49-M2"},
        )
