from __future__ import annotations

from dataclasses import dataclass

import tensorflow as tf

from bayesfilter.highdim.models import PredatorPreySSM
from bayesfilter.nonlinear.fixed_sgqf_derivatives_tf import TFFixedSGQFDerivatives
from bayesfilter.nonlinear.fixed_sgqf_tf import TFFixedSGQFNonlinearModel
from bayesfilter.structural_tf import TFStructuralStateSpace


@dataclass(frozen=True)
class TFFixedSGQFStructuralAdapterResult:
    eligible: bool
    reason: str | None
    model: TFFixedSGQFNonlinearModel | None
    derivatives: TFFixedSGQFDerivatives | None = None


def tf_predator_prey_to_fixed_sgqf_model(
    model: PredatorPreySSM,
    theta: tf.Tensor,
    *,
    with_derivatives: bool = False,
) -> TFFixedSGQFStructuralAdapterResult:
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)

    def transition_fn(points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        return model.transition_mean(theta, values)

    def observation_fn(points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        return values

    fixed_model = TFFixedSGQFNonlinearModel(
        initial_mean=model.initial_mean,
        initial_covariance=model.initial_covariance,
        process_covariance=model.process_covariance,
        observation_covariance=model.observation_covariance,
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="fixed_sgqf_predator_prey_adapter",
    )

    if not with_derivatives:
        return TFFixedSGQFStructuralAdapterResult(
            eligible=True,
            reason=None,
            model=fixed_model,
            derivatives=None,
        )

    parameter_dim = int(theta.shape[0])
    state_dim = fixed_model.state_dim
    observation_dim = fixed_model.observation_dim

    def transition_state_jacobian_fn(points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        if values.shape.rank == 1:
            values = values[tf.newaxis, :]
        with tf.GradientTape() as tape:
            tape.watch(values)
            outputs = transition_fn(values)
        return tape.batch_jacobian(outputs, values)

    def d_transition_fn(points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        if values.shape.rank == 1:
            values = values[tf.newaxis, :]
        with tf.GradientTape() as tape:
            tape.watch(theta)
            outputs = model.transition_mean(theta, values)
        jacobian = tape.jacobian(outputs, theta)
        return tf.transpose(tf.convert_to_tensor(jacobian, dtype=tf.float64), perm=[2, 0, 1])

    def observation_state_jacobian_fn(points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        if values.shape.rank == 1:
            values = values[tf.newaxis, :]
        point_count = tf.shape(values)[0]
        return tf.broadcast_to(tf.eye(observation_dim, dtype=tf.float64), [point_count, observation_dim, state_dim])

    def d_observation_fn(points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        if values.shape.rank == 1:
            values = values[tf.newaxis, :]
        return tf.zeros([parameter_dim, tf.shape(values)[0], observation_dim], dtype=tf.float64)

    fixed_derivatives = TFFixedSGQFDerivatives(
        d_initial_mean=tf.zeros([parameter_dim, state_dim], dtype=tf.float64),
        d_initial_covariance=tf.zeros([parameter_dim, state_dim, state_dim], dtype=tf.float64),
        d_process_covariance=tf.zeros([parameter_dim, state_dim, state_dim], dtype=tf.float64),
        d_observation_covariance=tf.zeros([parameter_dim, observation_dim, observation_dim], dtype=tf.float64),
        transition_state_jacobian_fn=transition_state_jacobian_fn,
        d_transition_fn=d_transition_fn,
        observation_state_jacobian_fn=observation_state_jacobian_fn,
        d_observation_fn=d_observation_fn,
        name="fixed_sgqf_predator_prey_adapter_derivatives",
    )

    return TFFixedSGQFStructuralAdapterResult(
        eligible=True,
        reason=None,
        model=fixed_model,
        derivatives=fixed_derivatives,
    )


def tf_structural_to_fixed_sgqf_model(
    model: TFStructuralStateSpace,
    *,
    derivatives=None,
) -> TFFixedSGQFStructuralAdapterResult:
    if model.name != "model_c_autonomous_nonlinear_growth":
        return TFFixedSGQFStructuralAdapterResult(
            eligible=False,
            reason="current fixed SGQF structural adapter only supports the autonomous phase nonlinear growth fixture exactly; model_b remains exact-ineligible under the additive-state lane",
            model=None,
            derivatives=None,
        )

    process_variance = tf.convert_to_tensor(model.innovation_covariance[0, 0], dtype=tf.float64)
    observation_covariance = tf.convert_to_tensor(model.observation_covariance, dtype=tf.float64)
    initial_mean = tf.convert_to_tensor(model.initial_mean, dtype=tf.float64)
    initial_covariance = tf.convert_to_tensor(model.initial_covariance, dtype=tf.float64)

    def transition_fn(points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        if values.shape.rank == 1:
            values = values[tf.newaxis, :]
        x_prev = values[:, 0]
        tau_prev = values[:, 1]
        x_next = (
            0.5 * x_prev
            + 25.0 * x_prev / (1.0 + tf.square(x_prev))
            + 8.0 * tf.math.cos(1.2 * tau_prev)
        )
        tau_next = tau_prev + 1.0
        return tf.stack([x_next, tau_next], axis=1)

    def observation_fn(points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        if values.shape.rank == 1:
            values = values[tf.newaxis, :]
        return tf.square(values[:, :1]) / 20.0

    fixed_model = TFFixedSGQFNonlinearModel(
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        process_covariance=tf.convert_to_tensor(
            [[process_variance, 0.0], [0.0, 0.0]],
            dtype=tf.float64,
        ),
        observation_covariance=observation_covariance,
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="fixed_sgqf_model_c_structural_adapter",
    )

    if derivatives is None:
        return TFFixedSGQFStructuralAdapterResult(
            eligible=True,
            reason=None,
            model=fixed_model,
            derivatives=None,
        )

    parameter_dim = int(derivatives.d_initial_mean.shape[0])
    fixed_derivatives = TFFixedSGQFDerivatives(
        d_initial_mean=tf.convert_to_tensor(derivatives.d_initial_mean, dtype=tf.float64),
        d_initial_covariance=tf.convert_to_tensor(derivatives.d_initial_covariance, dtype=tf.float64),
        d_process_covariance=tf.convert_to_tensor(
            [
                [[derivatives.d_innovation_covariance[i, 0, 0], 0.0], [0.0, 0.0]]
                for i in range(parameter_dim)
            ],
            dtype=tf.float64,
        ),
        d_observation_covariance=tf.convert_to_tensor(derivatives.d_observation_covariance, dtype=tf.float64),
        transition_state_jacobian_fn=lambda points: tf.convert_to_tensor(
            derivatives.transition_state_jacobian_fn(
                tf.convert_to_tensor(points, dtype=tf.float64),
                tf.zeros([tf.shape(tf.convert_to_tensor(points, dtype=tf.float64))[0], 1], dtype=tf.float64),
            ),
            dtype=tf.float64,
        ),
        d_transition_fn=lambda points: tf.convert_to_tensor(
            derivatives.d_transition_fn(
                tf.convert_to_tensor(points, dtype=tf.float64),
                tf.zeros([tf.shape(tf.convert_to_tensor(points, dtype=tf.float64))[0], 1], dtype=tf.float64),
            ),
            dtype=tf.float64,
        ),
        observation_state_jacobian_fn=lambda points: tf.convert_to_tensor(
            derivatives.observation_state_jacobian_fn(tf.convert_to_tensor(points, dtype=tf.float64)),
            dtype=tf.float64,
        ),
        d_observation_fn=lambda points: tf.convert_to_tensor(
            derivatives.d_observation_fn(tf.convert_to_tensor(points, dtype=tf.float64)),
            dtype=tf.float64,
        ),
        name="fixed_sgqf_model_c_structural_adapter_derivatives",
    )
    return TFFixedSGQFStructuralAdapterResult(
        eligible=True,
        reason=None,
        model=fixed_model,
        derivatives=fixed_derivatives,
    )
