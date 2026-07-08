from __future__ import annotations

import math
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
import bayesfilter.highdim.source_route as source_route_module


DTYPE = tf.float64
MODEL = highdim.parameterized_zhao_cui_sir_austria_model()
PARAMETER_DIM = MODEL.parameter_dim()
STATE_DIM = MODEL.state_dim()
POINT_DIM = PARAMETER_DIM + 2 * STATE_DIM
BASIS_FAMILY = "author_lagrangep_algebraic"
BASIS_ORDER = highdim.P85_AUTHOR_SIR_LAGRANGEP_ORDER
BASIS_ELEMENTS = highdim.P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS
TT_RANK_TUPLE = tuple([2] * (POINT_DIM + 1))
SAMPLE_COUNT = 4
SEED = 9002


class ShiftedGaussianTransport:
    def __init__(self, shift: tf.Tensor, log_normalizer: float) -> None:
        self.shift = tf.convert_to_tensor(shift, dtype=DTYPE)
        self._log_normalizer = tf.constant(log_normalizer, dtype=DTYPE)

    def manifest_payload(self) -> dict[str, object]:
        return {
            "family": "p90_shifted_gaussian_transport",
            "dimension": int(self.shift.shape[0]),
            "shift": self.shift,
            "source_contract_level": "contract_test_double",
        }

    def inverse_transport(self, reference_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(reference_points, dtype=DTYPE)
        return points + self.shift[:, tf.newaxis]

    def forward_transport(self, local_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(local_points, dtype=DTYPE)
        return points - self.shift[:, tf.newaxis]

    def conditional_inverse_transport(
        self,
        conditioning_points: tf.Tensor,
        reference_points: tf.Tensor,
    ) -> tf.Tensor:
        del conditioning_points
        return self.inverse_transport(reference_points)

    def log_reference_density(self, reference_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(reference_points, dtype=DTYPE)
        dimension = tf.cast(tf.shape(points)[0], dtype=DTYPE)
        normalizer = -0.5 * dimension * tf.math.log(
            tf.constant(2.0 * math.pi, dtype=DTYPE)
        )
        return normalizer - 0.5 * tf.reduce_sum(tf.square(points), axis=0)

    def eval_pdf(self, local_points: tf.Tensor) -> tf.Tensor:
        reference = self.forward_transport(local_points)
        return tf.exp(self.log_reference_density(reference))

    def potential(self, local_points: tf.Tensor) -> tf.Tensor:
        return -tf.math.log(self.eval_pdf(local_points))

    def proposal_log_density(
        self,
        *,
        local_points: tf.Tensor,
        reference_points: tf.Tensor,
    ) -> tf.Tensor:
        del reference_points
        return tf.math.log(self.eval_pdf(local_points))

    def marginalize(self, keep_axes: tuple[int, ...]) -> "ShiftedGaussianTransport":
        keep = tuple(int(axis) for axis in keep_axes)
        return ShiftedGaussianTransport(
            tf.gather(self.shift, keep),
            log_normalizer=float(self._log_normalizer.numpy()),
        )

    def log_normalizer(self) -> tf.Tensor:
        return self._log_normalizer


def _split_physical(points: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    values = tf.convert_to_tensor(points, dtype=DTYPE)
    if values.shape.rank != 2 or int(values.shape[0]) != POINT_DIM:
        raise ValueError("unexpected physical point shape")
    theta = values[:PARAMETER_DIM, 0]
    tf.debugging.assert_near(
        values[:PARAMETER_DIM, :],
        theta[:, tf.newaxis],
        atol=1e-12,
    )
    x_t = tf.transpose(values[PARAMETER_DIM : PARAMETER_DIM + STATE_DIM, :])
    x_prev = tf.transpose(values[PARAMETER_DIM + STATE_DIM :, :])
    return theta, x_t, x_prev


def _transition_log_density(points: tf.Tensor, time_index: int) -> tf.Tensor:
    theta, x_t, x_prev = _split_physical(points)
    return MODEL.transition_log_density(theta, x_prev, x_t, t=int(time_index))


def _likelihood_log_density(points: tf.Tensor, time_index: int) -> tf.Tensor:
    del time_index
    theta, x_t, _ = _split_physical(points)
    observation = MODEL.infectious_components(MODEL.base_model.initial_mean)[0]
    observation = observation + tf.linspace(
        tf.constant(-0.2, dtype=DTYPE),
        tf.constant(0.2, dtype=DTYPE),
        MODEL.observation_dim(),
    )
    return MODEL.observation_log_density(theta, x_t, observation, t=1)


def _wrong_likelihood_log_density(points: tf.Tensor, time_index: int) -> tf.Tensor:
    return _likelihood_log_density(points, time_index)


def _prior_log_density(points: tf.Tensor) -> tf.Tensor:
    values = tf.convert_to_tensor(points, dtype=DTYPE)
    theta = values[:PARAMETER_DIM, 0]
    tf.debugging.assert_near(
        values[:PARAMETER_DIM, :],
        theta[:, tf.newaxis],
        atol=1e-12,
    )
    x0 = tf.transpose(values[PARAMETER_DIM:, :])
    theta_log_prior = -0.5 * tf.reduce_sum(tf.square(theta))
    return MODEL.initial_log_density(theta, x0) + theta_log_prior


def _current_frame() -> highdim.SourceRouteCoordinateFrame:
    diag = tf.linspace(tf.constant(0.9, dtype=DTYPE), tf.constant(1.1, dtype=DTYPE), POINT_DIM)
    return highdim.SourceRouteCoordinateFrame(
        mu=tf.zeros([POINT_DIM], dtype=DTYPE),
        matrix=tf.linalg.diag(diag),
        expansion_factor=1.0,
    )


def _previous_frame() -> highdim.SourceRouteCoordinateFrame:
    previous_dim = PARAMETER_DIM + STATE_DIM
    diag = tf.fill([previous_dim], tf.constant(500.0, dtype=DTYPE))
    mu = tf.zeros([previous_dim], dtype=DTYPE)
    return highdim.SourceRouteCoordinateFrame(
        mu=mu,
        matrix=tf.linalg.diag(diag),
        expansion_factor=1.0,
    )


def _physical_points() -> tf.Tensor:
    theta = tf.constant([0.02, -0.01, 0.03], dtype=DTYPE)
    x_prev = MODEL.base_model.initial_mean + tf.linspace(
        tf.constant(-0.05, dtype=DTYPE),
        tf.constant(0.05, dtype=DTYPE),
        STATE_DIM,
    )
    x_t = MODEL.transition_mean(theta, x_prev[tf.newaxis, :])[0] + tf.linspace(
        tf.constant(-0.02, dtype=DTYPE),
        tf.constant(0.02, dtype=DTYPE),
        STATE_DIM,
    )
    return tf.concat([theta, x_t, x_prev], axis=0)[:, tf.newaxis]


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _transport_hash(transport: ShiftedGaussianTransport) -> str:
    return highdim.BranchManifest(
        version="p90.transport_branch.v1",
        payload=transport.manifest_payload(),
    ).sha256().value


def _previous_retained_object() -> highdim.SourceRouteRetainedObject:
    previous_dim = PARAMETER_DIM + STATE_DIM
    transport = ShiftedGaussianTransport(
        tf.linspace(
            tf.constant(-0.04, dtype=DTYPE),
            tf.constant(0.06, dtype=DTYPE),
            previous_dim,
        ),
        log_normalizer=0.3,
    )
    frame = _previous_frame()
    samples = tf.reshape(
        tf.linspace(
            tf.constant(-0.15, dtype=DTYPE),
            tf.constant(0.20, dtype=DTYPE),
            previous_dim * SAMPLE_COUNT,
        ),
        [previous_dim, SAMPLE_COUNT],
    )
    log_weights = highdim.normalize_log_weights(
        tf.constant([-0.1, -0.2, -0.4, -0.3], dtype=DTYPE)
    )
    diagnostics = highdim.SourceRouteSampleDiagnostics(
        sample_count=SAMPLE_COUNT,
        effective_sample_size=highdim.effective_sample_size_from_log_weights(log_weights),
    )
    normalizer = highdim.SourceRouteNormalizerContribution(
        log_transport_normalizer=transport.log_normalizer(),
        shift_constant=tf.constant(0.0, dtype=DTYPE),
        log_abs_det_policy="included_in_target",
    )
    retained_diagnostics = {
        "phase": "P90",
        "time_index": 1,
        "sequential_status": "contract_test_previous_retained_object",
    }
    identity = highdim.source_route_retained_object_identity(
        transport_object=transport,
        coordinate_frame=frame,
        samples=samples,
        log_weights=log_weights,
        sample_diagnostics=diagnostics,
        normalizer=normalizer,
        measure_convention=_convention(),
        route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
        storage_kind="source_transport_object",
        transition_interface="sample_propagation",
        diagnostics=retained_diagnostics,
    )
    return highdim.SourceRouteRetainedObject(
        transport_object=transport,
        coordinate_frame=frame,
        samples=samples,
        log_weights=log_weights,
        sample_diagnostics=diagnostics,
        normalizer=normalizer,
        measure_convention=_convention(),
        route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
        storage_kind="source_transport_object",
        transition_interface="sample_propagation",
        branch_identity=identity,
        diagnostics=retained_diagnostics,
    )


def _binding(
    *,
    time_index: int,
    physical_points: tf.Tensor,
    current_transport: ShiftedGaussianTransport,
    previous_retained: highdim.SourceRouteRetainedObject | None,
    current_frame: highdim.SourceRouteCoordinateFrame | None = None,
    previous_hash: str | None = None,
    comparator_label: str = highdim.P90_VALUE_BRIDGE_COMPARATOR_LABEL,
    tolerance_version: str = highdim.P90_VALUE_BRIDGE_TOLERANCE_VERSION,
    physical_ordering: tuple[str, ...] = highdim.P90_VALUE_BRIDGE_PHYSICAL_ORDERING,
    target_id: str = highdim.P90_VALUE_BRIDGE_TARGET_ID,
) -> highdim.SourceRouteValueBridgeBinding:
    frame = current_frame or _current_frame()
    if int(time_index) == 1:
        keep_axes = None
        input_axes = None
        retained_hash = None
        prior_id = highdim.source_route_callable_identity(_prior_log_density)
    else:
        keep_axes = tuple(range(PARAMETER_DIM + STATE_DIM))
        input_axes = tuple(range(PARAMETER_DIM)) + tuple(
            range(PARAMETER_DIM + STATE_DIM, POINT_DIM)
        )
        retained_hash = (
            previous_hash
            if previous_hash is not None
            else previous_retained.branch_identity.hash.value
        )
        prior_id = None
    return highdim.SourceRouteValueBridgeBinding(
        target_id=target_id,
        time_index=int(time_index),
        parameter_dim=PARAMETER_DIM,
        state_dim=STATE_DIM,
        physical_shape=tuple(int(item) for item in physical_points.shape),
        physical_ordering=physical_ordering,
        previous_retained_hash=retained_hash,
        previous_marginal_keep_axes=keep_axes,
        previous_marginal_input_axes=input_axes,
        basis_family=BASIS_FAMILY,
        basis_order=BASIS_ORDER,
        basis_elements=BASIS_ELEMENTS,
        tt_rank_tuple=TT_RANK_TUPLE,
        sample_count=SAMPLE_COUNT,
        seed=SEED,
        transport_branch_hash=_transport_hash(current_transport),
        coordinate_frame_hash=highdim.source_route_coordinate_frame_hash(frame),
        transition_log_density_id=highdim.source_route_callable_identity(
            _transition_log_density
        ),
        likelihood_log_density_id=highdim.source_route_callable_identity(
            _likelihood_log_density
        ),
        prior_log_density_id=prior_id,
        comparator_label=comparator_label,
        tolerance_version=tolerance_version,
    )


def _block_production_scalar_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked(*args, **kwargs):  # noqa: ANN002, ANN003
        del args, kwargs
        raise AssertionError("production scalar path must not be used by P90 bridge")

    monkeypatch.setattr(
        source_route_module,
        "source_route_sequential_negative_log_physical_density",
        blocked,
    )
    monkeypatch.setattr(
        source_route_module,
        "source_route_previous_marginal_log_density",
        blocked,
    )


def test_p90_t1_author_formula_replay_same_target_components(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _block_production_scalar_paths(monkeypatch)
    physical = _physical_points()
    current_transport = ShiftedGaussianTransport(
        tf.linspace(tf.constant(-0.02, dtype=DTYPE), tf.constant(0.02, dtype=DTYPE), POINT_DIM),
        log_normalizer=0.1,
    )
    current_frame = _current_frame()
    binding = _binding(
        time_index=1,
        physical_points=physical,
        current_transport=current_transport,
        previous_retained=None,
        current_frame=current_frame,
    )

    result = highdim.source_route_author_formula_negative_log_physical_density(
        physical_points=physical,
        binding=binding,
        transition_log_density_fn=_transition_log_density,
        likelihood_log_density_fn=_likelihood_log_density,
        prior_log_density_fn=_prior_log_density,
        previous_retained_object=None,
        current_transport_branch_hash=_transport_hash(current_transport),
        current_coordinate_frame=current_frame,
    )

    theta, _, x_prev = _split_physical(physical)
    expected_prior = MODEL.initial_log_density(theta, x_prev) - 0.5 * tf.reduce_sum(
        tf.square(theta)
    )
    expected_transition = _transition_log_density(physical, 1)
    expected_likelihood = _likelihood_log_density(physical, 1)
    tf.debugging.assert_near(result.prior_or_previous_log_density, expected_prior)
    tf.debugging.assert_near(result.transition_log_density, expected_transition)
    tf.debugging.assert_near(result.likelihood_log_density, expected_likelihood)
    tf.debugging.assert_near(
        result.negative_log_density,
        -expected_prior - expected_transition - expected_likelihood,
    )
    assert binding.target_id == highdim.P90_VALUE_BRIDGE_TARGET_ID
    assert binding.physical_ordering == highdim.P90_VALUE_BRIDGE_PHYSICAL_ORDERING
    assert binding.basis_family == BASIS_FAMILY
    assert binding.tt_rank_tuple == TT_RANK_TUPLE
    assert binding.sample_count == SAMPLE_COUNT
    assert binding.seed == SEED
    assert binding.tolerance_version == highdim.P90_VALUE_BRIDGE_TOLERANCE_VERSION


def test_p90_t2_author_formula_replay_previous_retained_marginal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _block_production_scalar_paths(monkeypatch)
    physical = _physical_points()
    previous = _previous_retained_object()
    current_transport = ShiftedGaussianTransport(
        tf.linspace(tf.constant(0.03, dtype=DTYPE), tf.constant(-0.01, dtype=DTYPE), POINT_DIM),
        log_normalizer=-0.2,
    )
    current_frame = _current_frame()
    binding = _binding(
        time_index=2,
        physical_points=physical,
        current_transport=current_transport,
        previous_retained=previous,
        current_frame=current_frame,
    )

    result = highdim.source_route_author_formula_negative_log_physical_density(
        physical_points=physical,
        binding=binding,
        transition_log_density_fn=_transition_log_density,
        likelihood_log_density_fn=_likelihood_log_density,
        previous_retained_object=previous,
        current_transport_branch_hash=_transport_hash(current_transport),
        current_coordinate_frame=current_frame,
    )

    prior_points = tf.gather(
        physical,
        tuple(range(PARAMETER_DIM)) + tuple(range(PARAMETER_DIM + STATE_DIM, POINT_DIM)),
        axis=0,
    )
    keep_axes = tuple(range(PARAMETER_DIM + STATE_DIM))
    prefix_matrix = previous.coordinate_frame.matrix
    prefix_mu = previous.coordinate_frame.mu
    manual_local = tf.linalg.solve(
        prefix_matrix,
        prior_points - prefix_mu[:, tf.newaxis],
    )
    manual_transport = previous.transport_object.marginalize(keep_axes)
    manual_previous = tf.math.log(manual_transport.eval_pdf(manual_local)) - tf.math.log(
        tf.abs(tf.linalg.det(prefix_matrix))
    )
    tf.debugging.assert_near(result.previous_marginal_local_points, manual_local)
    tf.debugging.assert_near(result.prior_or_previous_log_density, manual_previous)
    tf.debugging.assert_near(
        result.negative_log_density,
        -manual_previous
        - _transition_log_density(physical, 2)
        - _likelihood_log_density(physical, 2),
    )
    assert binding.previous_retained_hash == previous.branch_identity.hash.value
    assert binding.previous_marginal_keep_axes == keep_axes


def test_p90_value_bridge_binding_negative_controls_fail_closed() -> None:
    physical = _physical_points()
    current_transport = ShiftedGaussianTransport(tf.zeros([POINT_DIM], dtype=DTYPE), 0.0)
    previous = _previous_retained_object()

    with pytest.raises(ValueError, match="target_id"):
        _binding(
            time_index=1,
            physical_points=physical,
            current_transport=current_transport,
            previous_retained=None,
            target_id="proxy_target",
        )

    with pytest.raises(ValueError, match="physical ordering"):
        _binding(
            time_index=1,
            physical_points=physical,
            current_transport=current_transport,
            previous_retained=None,
            physical_ordering=("theta", "x_t_minus_1", "x_t"),
        )

    with pytest.raises(ValueError, match="tolerance version"):
        _binding(
            time_index=1,
            physical_points=physical,
            current_transport=current_transport,
            previous_retained=None,
            tolerance_version="p90.value_bridge.tolerances.changed",
        )

    with pytest.raises(ValueError, match="comparator label"):
        _binding(
            time_index=1,
            physical_points=physical,
            current_transport=current_transport,
            previous_retained=None,
            comparator_label="ukf_proxy",
        )

    with pytest.raises(ValueError, match="transition function identity"):
        binding = _binding(
            time_index=2,
            physical_points=physical,
            current_transport=current_transport,
            previous_retained=previous,
        )
        highdim.source_route_author_formula_negative_log_physical_density(
            physical_points=physical,
            binding=binding,
            transition_log_density_fn=_likelihood_log_density,
            likelihood_log_density_fn=_likelihood_log_density,
            previous_retained_object=previous,
            current_transport_branch_hash=_transport_hash(current_transport),
            current_coordinate_frame=_current_frame(),
        )


def test_p90_value_bridge_identity_negative_controls_fail_closed() -> None:
    physical = _physical_points()
    previous = _previous_retained_object()
    current_transport = ShiftedGaussianTransport(tf.zeros([POINT_DIM], dtype=DTYPE), 0.0)
    current_frame = _current_frame()
    binding = _binding(
        time_index=2,
        physical_points=physical,
        current_transport=current_transport,
        previous_retained=previous,
        current_frame=current_frame,
    )

    with pytest.raises(ValueError, match="transport branch hash"):
        highdim.source_route_author_formula_negative_log_physical_density(
            physical_points=physical,
            binding=binding,
            transition_log_density_fn=_transition_log_density,
            likelihood_log_density_fn=_likelihood_log_density,
            previous_retained_object=previous,
            current_transport_branch_hash="0" * 64,
            current_coordinate_frame=current_frame,
        )

    bad_frame = highdim.SourceRouteCoordinateFrame(
        mu=tf.ones([POINT_DIM], dtype=DTYPE),
        matrix=tf.eye(POINT_DIM, dtype=DTYPE),
        expansion_factor=1.0,
    )
    with pytest.raises(ValueError, match="coordinate frame hash"):
        highdim.source_route_author_formula_negative_log_physical_density(
            physical_points=physical,
            binding=binding,
            transition_log_density_fn=_transition_log_density,
            likelihood_log_density_fn=_likelihood_log_density,
            previous_retained_object=previous,
            current_transport_branch_hash=_transport_hash(current_transport),
            current_coordinate_frame=bad_frame,
        )

    wrong_previous_hash = "1" * 64
    wrong_previous_binding = _binding(
        time_index=2,
        physical_points=physical,
        current_transport=current_transport,
        previous_retained=previous,
        current_frame=current_frame,
        previous_hash=wrong_previous_hash,
    )
    with pytest.raises(ValueError, match="previous retained hash"):
        highdim.source_route_author_formula_negative_log_physical_density(
            physical_points=physical,
            binding=wrong_previous_binding,
            transition_log_density_fn=_transition_log_density,
            likelihood_log_density_fn=_likelihood_log_density,
            previous_retained_object=previous,
            current_transport_branch_hash=_transport_hash(current_transport),
            current_coordinate_frame=current_frame,
        )

    with pytest.raises(ValueError, match="likelihood function identity"):
        highdim.source_route_author_formula_negative_log_physical_density(
            physical_points=physical,
            binding=binding,
            transition_log_density_fn=_transition_log_density,
            likelihood_log_density_fn=_wrong_likelihood_log_density,
            previous_retained_object=previous,
            current_transport_branch_hash=_transport_hash(current_transport),
            current_coordinate_frame=current_frame,
        )


def run_p90_phase3_source_scalar_matches_author_formula_replay() -> None:
    physical = _physical_points()
    previous = _previous_retained_object()
    current_transport = ShiftedGaussianTransport(tf.zeros([POINT_DIM], dtype=DTYPE), 0.0)
    current_frame = _current_frame()
    binding = _binding(
        time_index=2,
        physical_points=physical,
        current_transport=current_transport,
        previous_retained=previous,
        current_frame=current_frame,
    )

    source_value = highdim.source_route_sequential_negative_log_physical_density(
        physical_points=physical,
        time_index=2,
        parameter_dim=PARAMETER_DIM,
        state_dim=STATE_DIM,
        transition_log_density_fn=_transition_log_density,
        likelihood_log_density_fn=_likelihood_log_density,
        previous_retained_object=previous,
    )
    replay = highdim.source_route_author_formula_negative_log_physical_density(
        physical_points=physical,
        binding=binding,
        transition_log_density_fn=_transition_log_density,
        likelihood_log_density_fn=_likelihood_log_density,
        previous_retained_object=previous,
        current_transport_branch_hash=_transport_hash(current_transport),
        current_coordinate_frame=current_frame,
    )
    residual = source_value - replay.negative_log_density
    tf.debugging.assert_near(
        source_value,
        replay.negative_log_density,
        atol=1.0e-9,
        rtol=0.0,
    )

    artifact = Path(
        "docs/plans/"
        "bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-2026-06-28.json"
    )
    artifact.write_text(
        highdim.BranchManifest(
            version="p90.value_bridge.execution.v1",
            payload={
                "target_id": binding.target_id,
                "time_index": int(binding.time_index),
                "binding_hash": binding.binding_hash,
                "previous_retained_hash": binding.previous_retained_hash,
                "transport_branch_hash": binding.transport_branch_hash,
                "coordinate_frame_hash": binding.coordinate_frame_hash,
                "tolerance_version": binding.tolerance_version,
                "source_value": source_value,
                "replay_value": replay.negative_log_density,
                "max_abs_residual": tf.reduce_max(tf.abs(residual)),
                "tolerance": 1.0e-9,
                "status": "P90_PHASE3_VALUE_BRIDGE_SOURCE_SCALAR_REPLAY_MATCH",
                "nonclaims": (
                    "no analytical-gradient correctness",
                    "no FD validation",
                    "no HMC readiness",
                    "no GPU/XLA readiness",
                    "no production readiness",
                    "no default-policy change",
                ),
            },
        )
        .to_canonical_bytes()
        .decode("utf-8"),
        encoding="utf-8",
    )
