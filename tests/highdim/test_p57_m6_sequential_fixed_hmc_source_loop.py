from __future__ import annotations

import math

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


class ShiftedGaussianTransport:
    def __init__(self, shift: tf.Tensor, log_normalizer: float) -> None:
        self.shift = tf.convert_to_tensor(shift, dtype=DTYPE)
        self._log_normalizer = tf.constant(log_normalizer, dtype=DTYPE)

    def manifest_payload(self) -> dict[str, object]:
        return {
            "family": "p57_m6_shifted_gaussian_transport",
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


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _frame() -> highdim.SourceRouteCoordinateFrame:
    return highdim.SourceRouteCoordinateFrame(
        mu=tf.constant([0.5, -0.25, 0.75], dtype=DTYPE),
        matrix=tf.constant(
            [
                [1.5, 0.0, 0.0],
                [0.1, 1.25, 0.0],
                [0.2, -0.1, 1.1],
            ],
            dtype=DTYPE,
        ),
        expansion_factor=1.0,
    )


def _transition_log_density(points: tf.Tensor, time_index: int) -> tf.Tensor:
    del time_index
    return -0.5 * tf.square(points[1, :] - points[2, :])


def _likelihood_log_density(points: tf.Tensor, time_index: int) -> tf.Tensor:
    del time_index
    return -0.25 * tf.square(points[1, :] - 1.0)


def _prior_log_density(points: tf.Tensor) -> tf.Tensor:
    center = tf.constant([[0.25], [-0.1]], dtype=DTYPE)
    return -0.5 * tf.reduce_sum(tf.square(points - center), axis=0)


def _components(
    *,
    include_prior: bool,
) -> highdim.SourceRouteSequentialDensityComponents:
    return highdim.SourceRouteSequentialDensityComponents(
        parameter_dim=1,
        state_dim=1,
        transition_log_density_fn=_transition_log_density,
        likelihood_log_density_fn=_likelihood_log_density,
        prior_log_density_fn=_prior_log_density if include_prior else None,
    )


def _target(
    *,
    time_index: int,
    shift_constant: float,
    components: highdim.SourceRouteSequentialDensityComponents | None = None,
) -> highdim.SourceRouteTarget:

    def negative_log_physical(points: tf.Tensor) -> tf.Tensor:
        if components is None:
            return tf.zeros([int(points.shape[1])], dtype=DTYPE)
        return components.negative_log_physical_density(
            physical_points=points,
            time_index=time_index,
            previous_retained_object=None,
        )

    return highdim.build_source_route_target(
        negative_log_physical_density_fn=negative_log_physical,
        coordinate_frame=_frame(),
        shift_constant=tf.constant(shift_constant, dtype=DTYPE),
        time_index=time_index,
    )


def _transport(shift: tuple[float, float, float], log_normalizer: float) -> highdim.SourceRouteTransportProtocol:
    return highdim.SourceRouteTransportProtocol(
        ShiftedGaussianTransport(tf.constant(shift, dtype=DTYPE), log_normalizer)
    )


def _specs() -> tuple[highdim.SourceRouteSequentialStepSpec, highdim.SourceRouteSequentialStepSpec]:
    components1 = _components(include_prior=True)
    spec1 = highdim.SourceRouteSequentialStepSpec(
        target=_target(
            time_index=1,
            shift_constant=0.2,
            components=components1,
        ),
        transport=_transport((0.1, -0.2, 0.3), log_normalizer=0.7),
        reference_samples=tf.constant(
            [
                [-0.5, 0.25, 0.8],
                [0.1, -0.3, 0.4],
                [0.2, 0.5, -0.6],
            ],
            dtype=DTYPE,
        ),
        measure_convention=_convention(),
        density_components=components1,
    )
    components2 = _components(include_prior=False)
    spec2 = highdim.SourceRouteSequentialStepSpec(
        target=_target(
            time_index=2,
            shift_constant=-0.3,
            components=None,
        ),
        transport=_transport((0.05, 0.1, -0.1), log_normalizer=1.1),
        reference_samples=tf.constant(
            [
                [0.2, 0.6, -0.1],
                [-0.4, 0.3, 0.7],
                [0.5, -0.2, 0.1],
            ],
            dtype=DTYPE,
        ),
        measure_convention=_convention(),
        density_components=components2,
        previous_marginal_keep_axes=(0, 1),
        previous_marginal_input_axes=(0, 2),
    )
    return spec1, spec2


def test_p57_m6_sequential_loop_carries_previous_retained_marginal() -> None:
    spec1, spec2 = _specs()

    result = highdim.source_route_run_sequential_fixed_hmc(step_specs=(spec1, spec2))

    assert result.sequential_status == "sequential_fixed_hmc_source_loop"
    assert result.branch_audit.status == "PASS_SOURCE_ROUTE_OPERATION_COVERAGE"
    assert len(result.steps) == 2
    assert result.steps[0].previous_retained_object is None
    assert result.steps[1].previous_retained_object is result.steps[0].retained_object
    assert result.steps[1].previous_marginal_density is not None
    assert result.steps[1].previous_marginal_density.keep_axes == (0, 1)

    expected_log_like = (tf.constant(0.7, dtype=DTYPE) - spec1.target.shift_constant) + (
        tf.constant(1.1, dtype=DTYPE) - spec2.target.shift_constant
    )
    tf.debugging.assert_near(result.log_marginal_likelihood, expected_log_like)

    current_local = spec2.transport.inverse_transport(spec2.reference_samples)
    current_physical = result.steps[1].target.physical_points_from_reference(current_local)
    previous_physical = tf.gather(current_physical, (0, 2), axis=0)
    previous_frame = result.steps[0].retained_object.coordinate_frame
    prefix_matrix = previous_frame.matrix[:2, :2]
    prefix_mu = previous_frame.mu[:2]
    manual_local = tf.linalg.solve(
        prefix_matrix,
        previous_physical - prefix_mu[:, tf.newaxis],
    )
    manual_transport = result.steps[0].retained_object.transport_object.marginalize((0, 1))
    manual_log_density = tf.math.log(manual_transport.eval_pdf(manual_local)) - tf.math.log(
        tf.abs(tf.linalg.det(prefix_matrix))
    )

    tf.debugging.assert_near(
        result.steps[1].previous_marginal_density.physical_points,
        previous_physical,
    )
    tf.debugging.assert_near(
        result.steps[1].previous_marginal_density.local_points,
        manual_local,
    )
    tf.debugging.assert_near(
        result.steps[1].previous_marginal_density.log_density,
        manual_log_density,
    )


def test_p57_m6_sequential_negative_log_density_uses_previous_sirt_marginal() -> None:
    result = highdim.source_route_run_sequential_fixed_hmc(step_specs=_specs())
    previous = result.steps[0].retained_object
    physical = tf.constant(
        [
            [0.1, 0.4],
            [1.5, 1.7],
            [-0.2, 0.3],
        ],
        dtype=DTYPE,
    )

    def transition_log_density(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        return -0.5 * tf.square(points[1, :] - points[2, :])

    def likelihood_log_density(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        return -0.25 * tf.square(points[1, :] - 1.0)

    value = highdim.source_route_sequential_negative_log_physical_density(
        physical_points=physical,
        time_index=2,
        parameter_dim=1,
        state_dim=1,
        transition_log_density_fn=transition_log_density,
        likelihood_log_density_fn=likelihood_log_density,
        previous_retained_object=previous,
    )
    previous_prior = highdim.source_route_previous_marginal_log_density(
        previous_retained_object=previous,
        physical_points=tf.gather(physical, (0, 2), axis=0),
        keep_axes=(0, 1),
    )
    expected = (
        -previous_prior.log_density
        - transition_log_density(physical, 2)
        - likelihood_log_density(physical, 2)
    )

    tf.debugging.assert_near(value, expected)

    with pytest.raises(TypeError, match="previous_retained_object"):
        highdim.source_route_sequential_negative_log_physical_density(
            physical_points=physical,
            time_index=2,
            parameter_dim=1,
            state_dim=1,
            transition_log_density_fn=transition_log_density,
            likelihood_log_density_fn=likelihood_log_density,
        )


def test_p57_m6_rejects_missing_previous_marginalization_evidence() -> None:
    spec1, _ = _specs()
    with pytest.raises(ValueError, match="previous_marginal_keep_axes"):
        highdim.SourceRouteSequentialStepSpec(
            target=_target(time_index=2, shift_constant=0.0),
            transport=_transport((0.0, 0.0, 0.0), log_normalizer=0.0),
            reference_samples=tf.zeros([3, 2], dtype=DTYPE),
            measure_convention=_convention(),
            density_components=_components(include_prior=False),
        )

    with pytest.raises(ValueError, match="previous_marginal_input_axes"):
        highdim.SourceRouteSequentialStepSpec(
            target=_target(time_index=2, shift_constant=0.0),
            transport=_transport((0.0, 0.0, 0.0), log_normalizer=0.0),
            reference_samples=tf.zeros([3, 2], dtype=DTYPE),
            measure_convention=_convention(),
            density_components=_components(include_prior=False),
            previous_marginal_keep_axes=(0, 1),
        )

    with pytest.raises(ValueError, match="at least two steps"):
        highdim.source_route_run_sequential_fixed_hmc(step_specs=(spec1,))

    spec3 = highdim.SourceRouteSequentialStepSpec(
        target=_target(time_index=3, shift_constant=0.0),
        transport=_transport((0.0, 0.0, 0.0), log_normalizer=0.0),
        reference_samples=tf.zeros([3, 2], dtype=DTYPE),
        measure_convention=_convention(),
        density_components=_components(include_prior=False),
        previous_marginal_keep_axes=(0, 1),
        previous_marginal_input_axes=(0, 2),
    )
    with pytest.raises(ValueError, match="consecutive"):
        highdim.source_route_run_sequential_fixed_hmc(
            step_specs=(spec1, spec3)
        )


def test_p57_m6_rejects_incomplete_branch_audit_and_one_step_promotion() -> None:
    spec1, spec2 = _specs()
    incomplete = highdim.SourceRouteImplementationAudit(
        records=tuple(
            highdim.SourceRouteOperationRecord(
                operation_id=operation_id,
                source_anchor="third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-130",
                implementation_status="implemented",
            )
            for operation_id in highdim.SOURCE_ROUTE_REQUIRED_OPERATION_IDS
            if operation_id != "previous_retained_object_marginalization"
        )
    )

    with pytest.raises(ValueError, match="branch_audit"):
        highdim.source_route_run_sequential_fixed_hmc(
            step_specs=(spec1, spec2),
            branch_audit=incomplete,
        )

    with pytest.raises(ValueError, match="t=1"):
        highdim.source_route_one_step_reapproximation(
            target=spec2.target,
            transport=spec2.transport,
            reference_samples=spec2.reference_samples,
            time_index=2,
        )
