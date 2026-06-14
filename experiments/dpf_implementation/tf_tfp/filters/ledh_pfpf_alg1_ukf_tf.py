"""Li-Coates Algorithm 1 LEDH PF-PF with per-particle UKF covariance state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

import tensorflow as tf

from bayesfilter.linear.svd_factor_tf import eigh_solve, floor_count, psd_eigh, symmetrize
from bayesfilter.nonlinear.sigma_points_tf import (
    TFSigmaPointRule,
    tf_svd_sigma_point_placement,
    tf_unit_sigma_point_rule,
)
from experiments.dpf_implementation.tf_tfp.filters.bootstrap_pf_tf import (
    DTYPE,
    normalize_log_weights_tf,
    weighted_mean_and_variance_tf,
)


METHOD_GENERATION = "li_coates_algorithm1_ukf_covariance_lifecycle"
FLOW_SOURCE_ROUTE = "li_coates_2017_algorithm1_ledh_pfpf"
COVARIANCE_ROUTE = "per_particle_ukf_prediction_update"
FLOW_ANCHOR_ROUTE = "zero_noise_transition"
PREVIOUS_LEDHPFPF_OT_EVIDENCE_STATUS = "quarantined"
DEFAULT_COVARIANCE_FLOOR = 1e-10
DEFAULT_RANK_TOLERANCE = 1e-12


TransitionMeanFn = Callable[[tf.Tensor, int], tf.Tensor]
TransitionSampleFn = Callable[[tf.Tensor, int, int], tf.Tensor]
TransitionLogDensityFn = Callable[[tf.Tensor, tf.Tensor, int], tf.Tensor]
ObservationMeanFn = Callable[[tf.Tensor, int], tf.Tensor]
ObservationJacobianFn = Callable[[tf.Tensor, int], tf.Tensor]
ObservationLogDensityFn = Callable[[tf.Tensor, tf.Tensor, int], tf.Tensor]
ProcessNoiseCovarianceFn = Callable[[tf.Tensor, int], tf.Tensor]
ObservationCovarianceFn = Callable[[int], tf.Tensor]


@dataclass(frozen=True)
class UKFSingleStepResult:
    mean: tf.Tensor
    covariance: tf.Tensor
    diagnostics: Mapping[str, tf.Tensor]


@dataclass(frozen=True)
class LedhAlg1TimeStepResult:
    pre_flow_particles: tf.Tensor
    post_flow_particles: tf.Tensor
    predicted_means: tf.Tensor
    predicted_covariances: tf.Tensor
    updated_means: tf.Tensor
    updated_covariances: tf.Tensor
    auxiliary_anchors: tf.Tensor
    auxiliary_terminal_states: tf.Tensor
    flow_matrices_by_particle_step: tf.Tensor
    flow_offsets_by_particle_step: tf.Tensor
    pseudo_time_steps: tf.Tensor
    forward_log_det: tf.Tensor
    pre_flow_log_density: tf.Tensor
    diagnostics: dict[str, Any]


@dataclass(frozen=True)
class LedhPFPFAlg1UKFTFResult:
    method_id: str
    route_identifiers: Mapping[str, str]
    seed: int
    num_particles: int
    log_likelihood_estimate: tf.Tensor
    filtered_means: tf.Tensor
    filtered_variances: tf.Tensor
    particle_covariances_by_time: tf.Tensor
    predicted_covariances_by_time: tf.Tensor
    corrected_log_weights_by_time: tf.Tensor
    ess_by_time: tf.Tensor
    resampling_count: int
    resampling_diagnostics: list[dict[str, Any]]
    finite: bool


def algorithm1_route_identifiers(
    *,
    resampling_route: str = "none",
) -> dict[str, str]:
    """Return the source-route identifiers required by the reviewed plan."""

    return {
        "method_generation": METHOD_GENERATION,
        "flow_source_route": FLOW_SOURCE_ROUTE,
        "covariance_route": COVARIANCE_ROUTE,
        "flow_anchor_route": FLOW_ANCHOR_ROUTE,
        "resampling_route": str(resampling_route),
        "previous_ledh_pfpf_ot_evidence_status": PREVIOUS_LEDHPFPF_OT_EVIDENCE_STATUS,
    }


def validate_algorithm1_route_identifiers(route: Mapping[str, str]) -> None:
    """Fail closed when an artifact claims Algorithm 1 but names an old route."""

    if route.get("method_generation") != METHOD_GENERATION:
        return
    expected = algorithm1_route_identifiers(
        resampling_route=route.get("resampling_route", "none")
    )
    for key in (
        "flow_source_route",
        "covariance_route",
        "flow_anchor_route",
        "previous_ledh_pfpf_ot_evidence_status",
    ):
        if route.get(key) != expected[key]:
            raise ValueError(f"Algorithm 1 route has wrong {key}: {route.get(key)!r}")
    if "ledh_pfpf_ot" in str(route.get("flow_source_route", "")):
        raise ValueError("old LEDH-PFPF-OT route cannot claim Algorithm 1 generation")


def ukf_predict_additive_tf(
    *,
    previous_state: tf.Tensor,
    previous_covariance: tf.Tensor,
    transition_mean_fn: TransitionMeanFn,
    process_noise_covariance: tf.Tensor,
    time_index: int,
    sigma_rule: TFSigmaPointRule | None = None,
    alpha: float = 1.0,
    beta: float = 2.0,
    kappa: float = 0.0,
    covariance_floor: float | tf.Tensor = DEFAULT_COVARIANCE_FLOOR,
    rank_tolerance: float | tf.Tensor = DEFAULT_RANK_TOLERANCE,
) -> UKFSingleStepResult:
    """Per-particle additive-noise UKF prediction for Algorithm 1."""

    previous_state = tf.reshape(tf.cast(previous_state, DTYPE), [-1])
    previous_covariance = symmetrize(previous_covariance)
    process_noise_covariance = symmetrize(process_noise_covariance)
    rule = sigma_rule or tf_unit_sigma_point_rule(
        int(previous_state.shape[0]),
        rule="unscented",
        alpha=alpha,
        beta=beta,
        kappa=kappa,
    )
    sigma_points, placement = tf_svd_sigma_point_placement(
        previous_state,
        previous_covariance,
        rule,
        singular_floor=tf.cast(covariance_floor, DTYPE),
        rank_tolerance=tf.cast(rank_tolerance, DTYPE),
    )
    predicted_points = tf.cast(transition_mean_fn(sigma_points, int(time_index)), DTYPE)
    predicted_mean = tf.linalg.matvec(
        tf.transpose(predicted_points),
        rule.mean_weights,
    )
    centered = predicted_points - predicted_mean[tf.newaxis, :]
    raw_covariance = _weighted_covariance(centered, rule.covariance_weights)
    implemented_covariance, covariance_diag = stabilize_covariance_tf(
        raw_covariance + process_noise_covariance,
        covariance_floor=covariance_floor,
    )
    diagnostics = {
        "ukf_rule": tf.constant(rule.name),
        "ukf_point_count": tf.constant(rule.point_count, dtype=tf.int32),
        "ukf_alpha": tf.constant(alpha, dtype=DTYPE),
        "ukf_beta": tf.constant(beta, dtype=DTYPE),
        "ukf_kappa": tf.constant(kappa, dtype=DTYPE),
        "placement_floor_count": placement.floor_count,
        "placement_psd_projection_residual": placement.psd_projection_residual,
        "prediction_floor_count": covariance_diag["floor_count"],
        "prediction_min_raw_eigenvalue": covariance_diag["min_raw_eigenvalue"],
        "prediction_psd_projection_residual": covariance_diag["psd_projection_residual"],
    }
    return UKFSingleStepResult(
        mean=predicted_mean,
        covariance=implemented_covariance,
        diagnostics=diagnostics,
    )


def ukf_update_additive_tf(
    *,
    predicted_mean: tf.Tensor,
    predicted_covariance: tf.Tensor,
    observation: tf.Tensor,
    observation_mean_fn: ObservationMeanFn,
    observation_covariance: tf.Tensor,
    time_index: int,
    sigma_rule: TFSigmaPointRule | None = None,
    alpha: float = 1.0,
    beta: float = 2.0,
    kappa: float = 0.0,
    covariance_floor: float | tf.Tensor = DEFAULT_COVARIANCE_FLOOR,
    rank_tolerance: float | tf.Tensor = DEFAULT_RANK_TOLERANCE,
) -> UKFSingleStepResult:
    """Per-particle additive-noise UKF update for Algorithm 1."""

    predicted_mean = tf.reshape(tf.cast(predicted_mean, DTYPE), [-1])
    predicted_covariance = symmetrize(predicted_covariance)
    observation = tf.reshape(tf.cast(observation, DTYPE), [-1])
    observation_covariance = symmetrize(observation_covariance)
    state_dim = int(predicted_mean.shape[0])
    rule = sigma_rule or tf_unit_sigma_point_rule(
        state_dim,
        rule="unscented",
        alpha=alpha,
        beta=beta,
        kappa=kappa,
    )
    sigma_points, placement = tf_svd_sigma_point_placement(
        predicted_mean,
        predicted_covariance,
        rule,
        singular_floor=tf.cast(covariance_floor, DTYPE),
        rank_tolerance=tf.cast(rank_tolerance, DTYPE),
    )
    placed_covariance = placement.implemented_covariance
    observation_points = tf.cast(observation_mean_fn(sigma_points, int(time_index)), DTYPE)
    observation_mean = tf.linalg.matvec(
        tf.transpose(observation_points),
        rule.mean_weights,
    )
    centered_x = sigma_points - predicted_mean[tf.newaxis, :]
    centered_y = observation_points - observation_mean[tf.newaxis, :]
    innovation_covariance_raw = (
        _weighted_covariance(centered_y, rule.covariance_weights)
        + observation_covariance
    )
    innovation_covariance, innovation_diag = stabilize_covariance_tf(
        innovation_covariance_raw,
        covariance_floor=covariance_floor,
    )
    cross_covariance = tf.transpose(centered_x) @ (
        centered_y * rule.covariance_weights[:, tf.newaxis]
    )
    eigenvalues, floored, eigenvectors, implemented_innovation, _residual = psd_eigh(
        innovation_covariance,
        tf.cast(covariance_floor, DTYPE),
    )
    innovation_precision = eigh_solve(
        eigenvectors,
        floored,
        tf.eye(int(observation.shape[0]), dtype=DTYPE),
    )
    kalman_gain = cross_covariance @ innovation_precision
    innovation = observation - observation_mean
    updated_mean = predicted_mean + tf.linalg.matvec(kalman_gain, innovation)
    updated_covariance_raw = (
        placed_covariance
        - kalman_gain
        @ implemented_innovation
        @ tf.transpose(kalman_gain)
    )
    updated_covariance, update_diag = stabilize_covariance_tf(
        updated_covariance_raw,
        covariance_floor=covariance_floor,
    )
    diagnostics = {
        "ukf_rule": tf.constant(rule.name),
        "ukf_point_count": tf.constant(rule.point_count, dtype=tf.int32),
        "ukf_alpha": tf.constant(alpha, dtype=DTYPE),
        "ukf_beta": tf.constant(beta, dtype=DTYPE),
        "ukf_kappa": tf.constant(kappa, dtype=DTYPE),
        "placement_floor_count": placement.floor_count,
        "placement_psd_projection_residual": placement.psd_projection_residual,
        "innovation_floor_count": floor_count(eigenvalues, tf.cast(covariance_floor, DTYPE)),
        "innovation_min_raw_eigenvalue": innovation_diag["min_raw_eigenvalue"],
        "innovation_psd_projection_residual": innovation_diag["psd_projection_residual"],
        "update_floor_count": update_diag["floor_count"],
        "update_min_raw_eigenvalue": update_diag["min_raw_eigenvalue"],
        "update_psd_projection_residual": update_diag["psd_projection_residual"],
    }
    return UKFSingleStepResult(
        mean=updated_mean,
        covariance=updated_covariance,
        diagnostics=diagnostics,
    )


def li_coates_ledh_alg1_time_step_tf(
    *,
    ancestors: tf.Tensor,
    previous_covariances: tf.Tensor,
    pre_flow_particles: tf.Tensor,
    observation: tf.Tensor,
    transition_mean_fn: TransitionMeanFn,
    transition_log_density_fn: TransitionLogDensityFn,
    observation_mean_fn: ObservationMeanFn,
    observation_jacobian_fn: ObservationJacobianFn,
    process_noise_covariance_fn: ProcessNoiseCovarianceFn,
    observation_covariance_fn: ObservationCovarianceFn,
    time_index: int,
    pseudo_time_steps: tf.Tensor,
    alpha: float = 1.0,
    beta: float = 2.0,
    kappa: float = 0.0,
    covariance_floor: float | tf.Tensor = DEFAULT_COVARIANCE_FLOOR,
    rank_tolerance: float | tf.Tensor = DEFAULT_RANK_TOLERANCE,
) -> LedhAlg1TimeStepResult:
    """Run one source-form Algorithm 1 LEDH PF-PF time step."""

    ancestors = tf.cast(ancestors, DTYPE)
    previous_covariances = tf.cast(previous_covariances, DTYPE)
    pre_flow_particles = tf.cast(pre_flow_particles, DTYPE)
    observation = tf.reshape(tf.cast(observation, DTYPE), [-1])
    pseudo_time_steps = validate_pseudo_time_steps_tf(pseudo_time_steps)
    num_particles = int(ancestors.shape[0])
    state_dim = int(ancestors.shape[1])
    obs_covariance = symmetrize(observation_covariance_fn(int(time_index)))
    identity = tf.eye(state_dim, dtype=DTYPE)

    predicted_means = []
    predicted_covariances = []
    updated_means = []
    updated_covariances = []
    auxiliary_anchors = []
    auxiliary_terminal_states = []
    flow_matrices_by_particle_step = []
    flow_offsets_by_particle_step = []
    post_flow_particles = []
    forward_log_dets = []
    min_predicted_eigenvalues = []
    max_prediction_floor_counts = []
    determinant_signs = []

    for i in range(num_particles):
        ancestor_i = ancestors[i]
        previous_covariance_i = symmetrize(previous_covariances[i])
        process_covariance_i = symmetrize(
            process_noise_covariance_fn(ancestor_i, int(time_index))
        )
        prediction = ukf_predict_additive_tf(
            previous_state=ancestor_i,
            previous_covariance=previous_covariance_i,
            transition_mean_fn=transition_mean_fn,
            process_noise_covariance=process_covariance_i,
            time_index=int(time_index),
            alpha=alpha,
            beta=beta,
            kappa=kappa,
            covariance_floor=covariance_floor,
            rank_tolerance=rank_tolerance,
        )
        predicted_means.append(prediction.mean)
        predicted_covariances.append(prediction.covariance)
        max_prediction_floor_counts.append(prediction.diagnostics["prediction_floor_count"])
        min_predicted_eigenvalues.append(
            tf.reduce_min(tf.linalg.eigvalsh(symmetrize(prediction.covariance)))
        )

        anchor_i = tf.reshape(
            transition_mean_fn(ancestor_i[tf.newaxis, :], int(time_index))[0],
            [-1],
        )
        auxiliary_state_i = tf.identity(anchor_i)
        eta_i = tf.reshape(pre_flow_particles[i], [-1])
        log_det_i = tf.constant(0.0, dtype=DTYPE)
        lambda_value = tf.constant(0.0, dtype=DTYPE)
        sign_product_i = tf.constant(1.0, dtype=DTYPE)
        a_matrices_i = []
        b_vectors_i = []
        for eps in tf.unstack(pseudo_time_steps, axis=0):
            lambda_value = lambda_value + eps
            coefficients = ledh_alg1_coefficients_tf(
                auxiliary_state=auxiliary_state_i,
                zero_noise_anchor=anchor_i,
                predicted_covariance=prediction.covariance,
                observation=observation,
                observation_mean_fn=observation_mean_fn,
                observation_jacobian_fn=observation_jacobian_fn,
                observation_covariance=obs_covariance,
                lambda_value=lambda_value,
                time_index=int(time_index),
                covariance_floor=covariance_floor,
            )
            a_matrix = coefficients["A"]
            b_vector = coefficients["b"]
            a_matrices_i.append(a_matrix)
            b_vectors_i.append(b_vector)
            auxiliary_state_i = auxiliary_state_i + eps * (
                tf.linalg.matvec(a_matrix, auxiliary_state_i) + b_vector
            )
            eta_i = eta_i + eps * (tf.linalg.matvec(a_matrix, eta_i) + b_vector)
            step_map = identity + eps * a_matrix
            sign, log_abs_det = tf.linalg.slogdet(step_map)
            sign_product_i = sign_product_i * sign
            log_det_i = log_det_i + log_abs_det
        update = ukf_update_additive_tf(
            predicted_mean=prediction.mean,
            predicted_covariance=prediction.covariance,
            observation=observation,
            observation_mean_fn=observation_mean_fn,
            observation_covariance=obs_covariance,
            time_index=int(time_index),
            alpha=alpha,
            beta=beta,
            kappa=kappa,
            covariance_floor=covariance_floor,
            rank_tolerance=rank_tolerance,
        )
        updated_means.append(update.mean)
        updated_covariances.append(update.covariance)
        auxiliary_anchors.append(anchor_i)
        auxiliary_terminal_states.append(auxiliary_state_i)
        flow_matrices_by_particle_step.append(tf.stack(a_matrices_i, axis=0))
        flow_offsets_by_particle_step.append(tf.stack(b_vectors_i, axis=0))
        post_flow_particles.append(eta_i)
        forward_log_dets.append(log_det_i)
        determinant_signs.append(sign_product_i)

    predicted_means_tensor = tf.stack(predicted_means, axis=0)
    predicted_covariances_tensor = tf.stack(predicted_covariances, axis=0)
    updated_means_tensor = tf.stack(updated_means, axis=0)
    updated_covariances_tensor = tf.stack(updated_covariances, axis=0)
    anchors_tensor = tf.stack(auxiliary_anchors, axis=0)
    auxiliary_terminal_tensor = tf.stack(auxiliary_terminal_states, axis=0)
    flow_matrices_tensor = tf.stack(flow_matrices_by_particle_step, axis=0)
    flow_offsets_tensor = tf.stack(flow_offsets_by_particle_step, axis=0)
    post_flow_tensor = tf.stack(post_flow_particles, axis=0)
    forward_log_det_tensor = tf.stack(forward_log_dets, axis=0)
    pre_flow_log_density = tf.cast(
        transition_log_density_fn(pre_flow_particles, ancestors, int(time_index)),
        DTYPE,
    )
    diagnostics = {
        "component_id": "li_coates_algorithm1_ledh_pfpf_ukf_time_step",
        "method_generation": METHOD_GENERATION,
        "flow_source_route": FLOW_SOURCE_ROUTE,
        "covariance_route": COVARIANCE_ROUTE,
        "flow_anchor_route": FLOW_ANCHOR_ROUTE,
        "pseudo_time_step_count": int(pseudo_time_steps.shape[0]),
        "pseudo_time_sum": _float(tf.reduce_sum(pseudo_time_steps)),
        "min_predicted_covariance_eigenvalue": _float(
            tf.reduce_min(tf.stack(min_predicted_eigenvalues, axis=0))
        ),
        "max_prediction_floor_count": int(
            tf.reduce_max(tf.stack(max_prediction_floor_counts, axis=0)).numpy()
        ),
        "min_forward_log_det": _float(tf.reduce_min(forward_log_det_tensor)),
        "max_forward_log_det": _float(tf.reduce_max(forward_log_det_tensor)),
        "finite_forward_log_det": _finite_bool(forward_log_det_tensor),
        "finite_post_flow": _finite_bool(post_flow_tensor),
        "finite_auxiliary_terminal": _finite_bool(auxiliary_terminal_tensor),
        "finite_predicted_covariances": _finite_bool(predicted_covariances_tensor),
        "finite_updated_covariances": _finite_bool(updated_covariances_tensor),
        "min_determinant_sign_product": _float(tf.reduce_min(tf.stack(determinant_signs))),
        "same_affine_trace_available": True,
        "backend": "tensorflow",
    }
    if not diagnostics["finite_forward_log_det"]:
        raise FloatingPointError("Algorithm 1 LEDH determinant product is non-finite")
    if not diagnostics["finite_post_flow"]:
        raise FloatingPointError("Algorithm 1 LEDH flow emitted non-finite particles")
    return LedhAlg1TimeStepResult(
        pre_flow_particles=pre_flow_particles,
        post_flow_particles=post_flow_tensor,
        predicted_means=predicted_means_tensor,
        predicted_covariances=predicted_covariances_tensor,
        updated_means=updated_means_tensor,
        updated_covariances=updated_covariances_tensor,
        auxiliary_anchors=anchors_tensor,
        auxiliary_terminal_states=auxiliary_terminal_tensor,
        flow_matrices_by_particle_step=flow_matrices_tensor,
        flow_offsets_by_particle_step=flow_offsets_tensor,
        pseudo_time_steps=pseudo_time_steps,
        forward_log_det=forward_log_det_tensor,
        pre_flow_log_density=pre_flow_log_density,
        diagnostics=diagnostics,
    )


def ledh_alg1_coefficients_tf(
    *,
    auxiliary_state: tf.Tensor,
    zero_noise_anchor: tf.Tensor,
    predicted_covariance: tf.Tensor,
    observation: tf.Tensor,
    observation_mean_fn: ObservationMeanFn,
    observation_jacobian_fn: ObservationJacobianFn,
    observation_covariance: tf.Tensor,
    lambda_value: tf.Tensor,
    time_index: int,
    covariance_floor: float | tf.Tensor = DEFAULT_COVARIANCE_FLOOR,
) -> Mapping[str, tf.Tensor]:
    """Compute source-form Li-Coates LEDH coefficients for one particle."""

    auxiliary_state = tf.reshape(tf.cast(auxiliary_state, DTYPE), [-1])
    zero_noise_anchor = tf.reshape(tf.cast(zero_noise_anchor, DTYPE), [-1])
    predicted_covariance = symmetrize(predicted_covariance)
    observation = tf.reshape(tf.cast(observation, DTYPE), [-1])
    observation_covariance = symmetrize(observation_covariance)
    h_value = tf.reshape(
        tf.cast(observation_mean_fn(auxiliary_state[tf.newaxis, :], int(time_index))[0], DTYPE),
        [-1],
    )
    h_jacobian = tf.cast(observation_jacobian_fn(auxiliary_state, int(time_index)), DTYPE)
    residual_intercept = h_value - tf.linalg.matvec(h_jacobian, auxiliary_state)
    hpht = h_jacobian @ predicted_covariance @ tf.transpose(h_jacobian)
    lambda_tensor = tf.cast(lambda_value, DTYPE)
    flow_covariance = lambda_tensor * hpht + observation_covariance
    flow_eigenvalues, flow_floored, flow_eigenvectors, _implemented, _residual = psd_eigh(
        flow_covariance,
        tf.cast(covariance_floor, DTYPE),
    )
    solved_h = eigh_solve(flow_eigenvectors, flow_floored, h_jacobian)
    a_matrix = (
        -0.5
        * predicted_covariance
        @ tf.transpose(h_jacobian)
        @ solved_h
    )
    obs_eigenvalues, obs_floored, obs_eigenvectors, _obs_impl, _obs_residual = psd_eigh(
        observation_covariance,
        tf.cast(covariance_floor, DTYPE),
    )
    shifted_observation = observation - residual_intercept
    obs_precision_residual = eigh_solve(obs_eigenvectors, obs_floored, shifted_observation)
    identity = tf.eye(int(auxiliary_state.shape[0]), dtype=DTYPE)
    inner = tf.linalg.matvec(
        (identity + lambda_tensor * a_matrix)
        @ predicted_covariance
        @ tf.transpose(h_jacobian),
        obs_precision_residual,
    ) + tf.linalg.matvec(a_matrix, zero_noise_anchor)
    b_vector = tf.linalg.matvec(identity + 2.0 * lambda_tensor * a_matrix, inner)
    return {
        "A": a_matrix,
        "b": b_vector,
        "H": h_jacobian,
        "e": residual_intercept,
        "flow_floor_count": floor_count(flow_eigenvalues, tf.cast(covariance_floor, DTYPE)),
        "observation_floor_count": floor_count(obs_eigenvalues, tf.cast(covariance_floor, DTYPE)),
    }


def run_ledh_pfpf_alg1_ukf_tf(
    *,
    observations: tf.Tensor,
    initial_sample: Callable[[int, int], tf.Tensor],
    initial_covariance: tf.Tensor,
    transition_sample: TransitionSampleFn,
    transition_mean_fn: TransitionMeanFn,
    transition_log_density_fn: TransitionLogDensityFn,
    observation_mean_fn: ObservationMeanFn,
    observation_jacobian_fn: ObservationJacobianFn,
    observation_log_density_fn: ObservationLogDensityFn,
    process_noise_covariance_fn: ProcessNoiseCovarianceFn,
    observation_covariance_fn: ObservationCovarianceFn,
    seed: int,
    num_particles: int,
    pseudo_time_steps: tf.Tensor | None = None,
    resampling_route: str = "none",
    ess_threshold_ratio: float = 0.5,
    alpha: float = 1.0,
    beta: float = 2.0,
    kappa: float = 0.0,
    covariance_floor: float | tf.Tensor = DEFAULT_COVARIANCE_FLOOR,
    rank_tolerance: float | tf.Tensor = DEFAULT_RANK_TOLERANCE,
    method_id: str = "ledh_pfpf_alg1_ukf_tf",
) -> LedhPFPFAlg1UKFTFResult:
    """Run the source-faithful Algorithm 1 core without OT resampling."""

    if resampling_route not in {"none", "classical_resampling"}:
        raise ValueError("Algorithm 1 core supports only none/classical_resampling")
    route = algorithm1_route_identifiers(resampling_route=resampling_route)
    validate_algorithm1_route_identifiers(route)
    particles = tf.cast(initial_sample(num_particles, seed), DTYPE)
    initial_covariance = symmetrize(initial_covariance)
    covariances = tf.tile(initial_covariance[tf.newaxis, :, :], [num_particles, 1, 1])
    log_weights = tf.fill([num_particles], -tf.math.log(tf.cast(num_particles, DTYPE)))
    pseudo_time = (
        tf.constant([1.0], dtype=DTYPE)
        if pseudo_time_steps is None
        else validate_pseudo_time_steps_tf(pseudo_time_steps)
    )
    filtered_means = []
    filtered_variances = []
    particle_covariances_by_time = []
    predicted_covariances_by_time = []
    corrected_log_weights_by_time = []
    ess_by_time = []
    diagnostics: list[dict[str, Any]] = []
    resampling_count = 0
    log_likelihood = tf.constant(0.0, dtype=DTYPE)

    for t, observation in enumerate(tf.unstack(tf.cast(observations, DTYPE), axis=0)):
        ancestors = tf.identity(particles)
        previous_covariances = tf.identity(covariances)
        pre_flow = tf.cast(transition_sample(ancestors, seed, int(t)), DTYPE)
        step = li_coates_ledh_alg1_time_step_tf(
            ancestors=ancestors,
            previous_covariances=previous_covariances,
            pre_flow_particles=pre_flow,
            observation=observation,
            transition_mean_fn=transition_mean_fn,
            transition_log_density_fn=transition_log_density_fn,
            observation_mean_fn=observation_mean_fn,
            observation_jacobian_fn=observation_jacobian_fn,
            process_noise_covariance_fn=process_noise_covariance_fn,
            observation_covariance_fn=observation_covariance_fn,
            time_index=int(t),
            pseudo_time_steps=pseudo_time,
            alpha=alpha,
            beta=beta,
            kappa=kappa,
            covariance_floor=covariance_floor,
            rank_tolerance=rank_tolerance,
        )
        post_flow = step.post_flow_particles
        target_transition = tf.cast(
            transition_log_density_fn(post_flow, ancestors, int(t)),
            DTYPE,
        )
        target_observation = tf.cast(
            observation_log_density_fn(post_flow, observation, int(t)),
            DTYPE,
        )
        corrected_log_weights = (
            log_weights
            + target_transition
            + target_observation
            - step.pre_flow_log_density
            + step.forward_log_det
        )
        corrected_log_weights_by_time.append(corrected_log_weights)
        weights, incremental = normalize_log_weights_tf(corrected_log_weights)
        log_likelihood = log_likelihood + incremental
        ess = 1.0 / tf.reduce_sum(weights * weights)
        mean, variance = weighted_mean_and_variance_tf(post_flow, weights)
        filtered_means.append(mean)
        filtered_variances.append(variance)
        particle_covariances_by_time.append(step.updated_covariances)
        predicted_covariances_by_time.append(step.predicted_covariances)
        ess_by_time.append(ess)
        if not _finite_bool(corrected_log_weights):
            raise FloatingPointError("Algorithm 1 corrected log weights are non-finite")

        if resampling_route == "classical_resampling" and bool(
            (ess < ess_threshold_ratio * num_particles).numpy()
        ):
            indices = tf.random.stateless_categorical(
                tf.reshape(tf.math.log(tf.maximum(weights, 1e-300)), [1, -1]),
                num_particles,
                seed=_seed_pair(seed, 9000 + t),
                dtype=tf.int32,
            )[0]
            particles, covariances = apply_classical_resampling_state_tf(
                particles=post_flow,
                covariances=step.updated_covariances,
                ancestor_indices=indices,
            )
            log_weights = tf.fill([num_particles], -tf.math.log(tf.cast(num_particles, DTYPE)))
            resampling_count += 1
            resampling_diag = {
                "resampled": True,
                "resampling_method": "stateless_multinomial_with_covariance_gather",
                "ancestor_indices": [int(v) for v in tf.unstack(indices)],
            }
        else:
            particles = post_flow
            covariances = step.updated_covariances
            log_weights = tf.math.log(tf.maximum(weights, tf.constant(1e-300, dtype=DTYPE)))
            resampling_diag = {
                "resampled": False,
                "resampling_method": "none",
            }
        diagnostics.append(
            {
                "time_index": int(t),
                "ess": _float(ess),
                "ess_ratio": _float(ess / tf.cast(num_particles, DTYPE)),
                "pfpf_correction": "log_target_transition_plus_observation_minus_q0_plus_forward_logdet",
                "finite_corrected_log_weights": _finite_bool(corrected_log_weights),
                "min_corrected_log_weight": _float(tf.reduce_min(corrected_log_weights)),
                "max_corrected_log_weight": _float(tf.reduce_max(corrected_log_weights)),
                **step.diagnostics,
                **resampling_diag,
            }
        )

    filtered_means_tensor = tf.stack(filtered_means, axis=0)
    filtered_variances_tensor = tf.stack(filtered_variances, axis=0)
    particle_covariances_tensor = tf.stack(particle_covariances_by_time, axis=0)
    predicted_covariances_tensor = tf.stack(predicted_covariances_by_time, axis=0)
    corrected_log_weights_tensor = tf.stack(corrected_log_weights_by_time, axis=0)
    ess_tensor = tf.stack(ess_by_time, axis=0)
    finite = bool(
        tf.math.is_finite(log_likelihood).numpy()
        and _finite_bool(filtered_means_tensor)
        and _finite_bool(filtered_variances_tensor)
        and _finite_bool(particle_covariances_tensor)
        and _finite_bool(predicted_covariances_tensor)
        and _finite_bool(corrected_log_weights_tensor)
        and _finite_bool(ess_tensor)
    )
    return LedhPFPFAlg1UKFTFResult(
        method_id=method_id,
        route_identifiers=route,
        seed=int(seed),
        num_particles=int(num_particles),
        log_likelihood_estimate=log_likelihood,
        filtered_means=filtered_means_tensor,
        filtered_variances=filtered_variances_tensor,
        particle_covariances_by_time=particle_covariances_tensor,
        predicted_covariances_by_time=predicted_covariances_tensor,
        corrected_log_weights_by_time=corrected_log_weights_tensor,
        ess_by_time=ess_tensor,
        resampling_count=int(resampling_count),
        resampling_diagnostics=diagnostics,
        finite=finite,
    )


def apply_classical_resampling_state_tf(
    *,
    particles: tf.Tensor,
    covariances: tf.Tensor,
    ancestor_indices: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    """Gather states and Algorithm 1 covariance state with the same ancestry."""

    indices = tf.cast(ancestor_indices, tf.int32)
    return tf.gather(tf.cast(particles, DTYPE), indices), tf.gather(
        tf.cast(covariances, DTYPE),
        indices,
    )


def stabilize_covariance_tf(
    covariance: tf.Tensor,
    *,
    covariance_floor: float | tf.Tensor = DEFAULT_COVARIANCE_FLOOR,
) -> tuple[tf.Tensor, Mapping[str, tf.Tensor]]:
    """Symmetrize and project a covariance through the declared PSD floor."""

    covariance = symmetrize(covariance)
    floor = tf.cast(covariance_floor, DTYPE)
    eigenvalues, floored, eigenvectors, implemented, residual = psd_eigh(covariance, floor)
    diagnostics = {
        "covariance_floor": floor,
        "min_raw_eigenvalue": tf.reduce_min(eigenvalues),
        "floor_count": floor_count(eigenvalues, floor),
        "psd_projection_residual": residual,
        "implemented_covariance": implemented,
        "covariance_floor_policy": tf.constant("declared_diagnostic_psd_floor_not_promotion_threshold"),
    }
    return implemented, diagnostics


def validate_pseudo_time_steps_tf(
    pseudo_time_steps: tf.Tensor,
    *,
    atol: float | tf.Tensor = 1e-12,
) -> tf.Tensor:
    """Validate the Algorithm 1 pseudo-time grid increments."""

    steps = tf.reshape(tf.cast(pseudo_time_steps, DTYPE), [-1])
    if int(tf.size(steps).numpy()) == 0:
        raise ValueError("Algorithm 1 pseudo-time grid must contain at least one step")
    if not _finite_bool(steps):
        raise ValueError("Algorithm 1 pseudo-time grid contains non-finite steps")
    if bool(tf.reduce_any(steps <= tf.constant(0.0, dtype=DTYPE)).numpy()):
        raise ValueError("Algorithm 1 pseudo-time increments must be positive")
    step_sum = tf.reduce_sum(steps)
    if float(tf.abs(step_sum - tf.constant(1.0, dtype=DTYPE)).numpy()) > float(
        tf.cast(atol, DTYPE).numpy()
    ):
        raise ValueError("Algorithm 1 pseudo-time increments must sum to 1")
    return steps


def _weighted_covariance(centered: tf.Tensor, weights: tf.Tensor) -> tf.Tensor:
    return symmetrize(tf.transpose(centered) @ (centered * weights[:, tf.newaxis]))


def _seed_pair(seed: int, salt: int) -> tf.Tensor:
    return tf.constant([int(seed) % 2147483647, int(salt) % 2147483647], dtype=tf.int32)


def _finite_bool(value: tf.Tensor) -> bool:
    return bool(tf.reduce_all(tf.math.is_finite(tf.cast(value, DTYPE))).numpy())


def _float(value: tf.Tensor) -> float:
    return float(tf.cast(value, DTYPE).numpy())
