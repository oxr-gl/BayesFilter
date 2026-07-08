from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64
_CONTRACT_TEST_PATH = Path(__file__).with_name("test_p90_value_bridge_contract.py")
_SPEC = importlib.util.spec_from_file_location(
    "p90_value_bridge_contract_helpers_for_derivatives",
    _CONTRACT_TEST_PATH,
)
assert _SPEC is not None
assert _SPEC.loader is not None
_HELPERS = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_HELPERS)


def _phase3_fixture():
    physical = _HELPERS._physical_points()
    previous = _HELPERS._previous_retained_object()
    current_transport = _HELPERS.ShiftedGaussianTransport(
        tf.zeros([_HELPERS.POINT_DIM], dtype=DTYPE),
        0.0,
    )
    current_frame = _HELPERS._current_frame()
    value_binding = _HELPERS._binding(
        time_index=2,
        physical_points=physical,
        current_transport=current_transport,
        previous_retained=previous,
        current_frame=current_frame,
    )
    replay = highdim.source_route_author_formula_negative_log_physical_density(
        physical_points=physical,
        binding=value_binding,
        transition_log_density_fn=_HELPERS._transition_log_density,
        likelihood_log_density_fn=_HELPERS._likelihood_log_density,
        previous_retained_object=previous,
        current_transport_branch_hash=_HELPERS._transport_hash(current_transport),
        current_coordinate_frame=current_frame,
    )
    derivative_binding = highdim.SourceRouteDerivativeBinding(
        value_bridge_binding=value_binding,
        value_bridge_binding_hash=value_binding.binding_hash,
        parameter_indices=(0, 1, 2),
    )
    return physical, previous, value_binding, replay, derivative_binding


def _component_carries():
    physical, previous, value_binding, replay, derivative_binding = _phase3_fixture()
    theta, x_t, x_prev = _HELPERS._split_physical(physical)
    transition_score = _HELPERS.MODEL.transition_log_density_parameter_score(
        theta,
        x_prev,
        x_t,
        t=value_binding.time_index,
    )
    likelihood_observation = _HELPERS.MODEL.infectious_components(
        _HELPERS.MODEL.base_model.initial_mean
    )[0] + tf.linspace(
        tf.constant(-0.2, dtype=DTYPE),
        tf.constant(0.2, dtype=DTYPE),
        _HELPERS.MODEL.observation_dim(),
    )
    likelihood_score = _HELPERS.MODEL.observation_log_density_parameter_score(
        theta,
        x_t,
        likelihood_observation,
        t=value_binding.time_index,
    )
    zero_previous_score = tf.zeros_like(transition_score)
    previous_carry = highdim.SourceRouteComponentDerivativeCarry(
        binding=derivative_binding,
        component_name="previous_marginal",
        component_value=replay.prior_or_previous_log_density,
        parameter_score=zero_previous_score,
        callable_identity="previous_retained_marginal_contract_double",
        classification="fixed_hmc_adaptation_blocker",
        owner_status="BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED",
    )
    transition_carry = highdim.SourceRouteComponentDerivativeCarry(
        binding=derivative_binding,
        component_name="transition",
        component_value=replay.transition_log_density,
        parameter_score=transition_score,
        callable_identity=highdim.source_route_callable_identity(
            _HELPERS._transition_log_density
        ),
        classification="local_parameterized_sir_component",
        owner_status="READY_P90_TRANSITION_PARAMETER_SCORE_CARRY",
    )
    likelihood_carry = highdim.SourceRouteComponentDerivativeCarry(
        binding=derivative_binding,
        component_name="likelihood",
        component_value=replay.likelihood_log_density,
        parameter_score=likelihood_score,
        callable_identity=highdim.source_route_callable_identity(
            _HELPERS._likelihood_log_density
        ),
        classification="local_parameterized_sir_component",
        owner_status="READY_P90_LIKELIHOOD_PARAMETER_SCORE_CARRY",
    )
    return (
        physical,
        previous,
        replay,
        derivative_binding,
        previous_carry,
        transition_carry,
        likelihood_carry,
    )


def test_p90_derivative_binding_preserves_value_bridge_hash_and_blocker() -> None:
    _, _, value_binding, _, derivative_binding = _phase3_fixture()

    assert derivative_binding.value_bridge_binding_hash == value_binding.binding_hash
    assert derivative_binding.target_id == highdim.P90_VALUE_BRIDGE_TARGET_ID
    assert derivative_binding.parameter_indices == (0, 1, 2)
    assert derivative_binding.fixed_ttsirt_transport_derivative_status.startswith("BLOCK_")

    with pytest.raises(ValueError, match="hash mismatch"):
        highdim.SourceRouteDerivativeBinding(
            value_bridge_binding=value_binding,
            value_bridge_binding_hash="0" * 64,
            parameter_indices=(0, 1, 2),
        )

    with pytest.raises(ValueError, match="must remain a blocker"):
        highdim.SourceRouteDerivativeBinding(
            value_bridge_binding=value_binding,
            value_bridge_binding_hash=value_binding.binding_hash,
            parameter_indices=(0, 1, 2),
            fixed_ttsirt_transport_derivative_status="READY_NOT_ALLOWED",
        )


def test_p90_transition_and_likelihood_score_carry_match_tensorflow_tape() -> None:
    (
        physical,
        _previous,
        _replay,
        _binding,
        _previous_carry,
        transition_carry,
        likelihood_carry,
    ) = _component_carries()
    theta, x_t, x_prev = _HELPERS._split_physical(physical)
    observation = _HELPERS.MODEL.infectious_components(
        _HELPERS.MODEL.base_model.initial_mean
    )[0] + tf.linspace(
        tf.constant(-0.2, dtype=DTYPE),
        tf.constant(0.2, dtype=DTYPE),
        _HELPERS.MODEL.observation_dim(),
    )

    with tf.GradientTape() as transition_tape:
        transition_tape.watch(theta)
        transition_value = _HELPERS.MODEL.transition_log_density(
            theta,
            x_prev,
            x_t,
            t=2,
        )[0]
    transition_tape_score = transition_tape.gradient(transition_value, theta)

    with tf.GradientTape() as likelihood_tape:
        likelihood_tape.watch(theta)
        likelihood_value = _HELPERS.MODEL.observation_log_density(
            theta,
            x_t,
            observation,
            t=2,
        )[0]
    likelihood_tape_score = likelihood_tape.gradient(likelihood_value, theta)

    tf.debugging.assert_near(
        transition_carry.parameter_score[0],
        transition_tape_score,
        atol=1e-10,
        rtol=1e-10,
    )
    tf.debugging.assert_near(
        likelihood_carry.parameter_score[0],
        likelihood_tape_score,
        atol=1e-10,
        rtol=1e-10,
    )
    assert transition_carry.owner_status.startswith("READY_")
    assert likelihood_carry.owner_status.startswith("READY_")


def test_p90_negative_log_assembly_derivative_carry_uses_component_signs() -> None:
    (
        _physical,
        _previous,
        replay,
        derivative_binding,
        previous_carry,
        transition_carry,
        likelihood_carry,
    ) = _component_carries()

    assembly = highdim.source_route_negative_log_assembly_derivative_carry(
        binding=derivative_binding,
        prior_or_previous=previous_carry,
        transition=transition_carry,
        likelihood=likelihood_carry,
    )

    tf.debugging.assert_near(assembly.component_value, replay.negative_log_density)
    tf.debugging.assert_near(
        assembly.parameter_score,
        -(
            previous_carry.parameter_score
            + transition_carry.parameter_score
            + likelihood_carry.parameter_score
        ),
    )
    assert assembly.classification == "source_formula_assembly"


def test_p90_previous_marginal_carry_keeps_blocker_and_branch_identity() -> None:
    (
        _physical,
        previous,
        replay,
        derivative_binding,
        _previous_carry,
        _transition_carry,
        _likelihood_carry,
    ) = _component_carries()
    value_binding = derivative_binding.value_bridge_binding
    log_det = previous.coordinate_frame.log_abs_det()

    carry = highdim.SourceRoutePreviousMarginalDerivativeCarry(
        binding=derivative_binding,
        previous_retained_hash=previous.branch_identity.hash.value,
        keep_axes=value_binding.previous_marginal_keep_axes,
        input_axes=value_binding.previous_marginal_input_axes,
        local_prefix_points=replay.previous_marginal_local_points,
        log_density=replay.prior_or_previous_log_density,
        affine_log_det=log_det,
    )

    assert carry.derivative_owner_status.startswith("BLOCK_")
    assert carry.previous_retained_hash == value_binding.previous_retained_hash

    with pytest.raises(ValueError, match="retained hash mismatch"):
        highdim.SourceRoutePreviousMarginalDerivativeCarry(
            binding=derivative_binding,
            previous_retained_hash="1" * 64,
            keep_axes=value_binding.previous_marginal_keep_axes,
            input_axes=value_binding.previous_marginal_input_axes,
            local_prefix_points=replay.previous_marginal_local_points,
            log_density=replay.prior_or_previous_log_density,
            affine_log_det=log_det,
        )

    with pytest.raises(ValueError, match="owner must remain a blocker"):
        highdim.SourceRoutePreviousMarginalDerivativeCarry(
            binding=derivative_binding,
            previous_retained_hash=previous.branch_identity.hash.value,
            keep_axes=value_binding.previous_marginal_keep_axes,
            input_axes=value_binding.previous_marginal_input_axes,
            local_prefix_points=replay.previous_marginal_local_points,
            log_density=replay.prior_or_previous_log_density,
            affine_log_det=log_det,
            derivative_owner_status="READY_NOT_ALLOWED",
        )


def test_p90_derivative_carry_rejects_component_shape_and_binding_drift() -> None:
    (
        _physical,
        _previous,
        _replay,
        derivative_binding,
        previous_carry,
        transition_carry,
        likelihood_carry,
    ) = _component_carries()
    other_binding = highdim.SourceRouteDerivativeBinding(
        value_bridge_binding=derivative_binding.value_bridge_binding,
        value_bridge_binding_hash=derivative_binding.value_bridge_binding_hash,
        parameter_indices=(0, 1),
    )
    drifted_transition = highdim.SourceRouteComponentDerivativeCarry(
        binding=other_binding,
        component_name="transition",
        component_value=transition_carry.component_value,
        parameter_score=transition_carry.parameter_score[:, :2],
        callable_identity=transition_carry.callable_identity,
        classification=transition_carry.classification,
        owner_status=transition_carry.owner_status,
    )

    with pytest.raises(ValueError, match="parameter_score"):
        highdim.SourceRouteComponentDerivativeCarry(
            binding=derivative_binding,
            component_name="transition",
            component_value=transition_carry.component_value,
            parameter_score=tf.zeros([2, 3], dtype=DTYPE),
            callable_identity=transition_carry.callable_identity,
            classification=transition_carry.classification,
            owner_status=transition_carry.owner_status,
        )

    with pytest.raises(ValueError, match="binding hash mismatch"):
        highdim.source_route_negative_log_assembly_derivative_carry(
            binding=derivative_binding,
            prior_or_previous=previous_carry,
            transition=drifted_transition,
            likelihood=likelihood_carry,
        )
