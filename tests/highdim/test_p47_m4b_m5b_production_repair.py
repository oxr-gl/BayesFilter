from __future__ import annotations

import json
from pathlib import Path

import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64
MASTER_PLAN = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-m5b-production-repair-master-program-2026-06-09.md"
)
M4B_SUBPLAN = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-spatial-sir-production-row-subplan-2026-06-09.md"
)
M5B_SUBPLAN = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-m5b-predator-prey-production-row-subplan-2026-06-09.md"
)
M4B_MANIFEST = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-production-row-manifest-2026-06-09.json"
)
M5B_MANIFEST = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-m5b-production-row-manifest-2026-06-09.json"
)
CLAUDE_LEDGER = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-m5b-production-repair-claude-review-ledger-2026-06-09.md"
)


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _basis(dim: int, degree: int) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree) for _ in range(dim)],
        _convention(),
    )


def _initial_cores(product_basis: highdim.ProductBasis, ranks: tuple[int, ...]) -> tuple[highdim.TTCore, ...]:
    return tuple(
        highdim.TTCore(tf.ones([ranks[axis], basis.basis_dim, ranks[axis + 1]], dtype=DTYPE))
        for axis, basis in enumerate(product_basis.bases)
    )


def _reference_grid(product_basis: highdim.ProductBasis, order: int) -> tuple[tf.Tensor, tf.Tensor]:
    nodes_1d, weights_1d = highdim.legendre_gauss_nodes_weights(order)
    axis_nodes = []
    axis_weights = []
    for basis in product_basis.bases:
        half_length = 0.5 * basis.domain.length
        midpoint = 0.5 * (basis.domain.left + basis.domain.right)
        axis_nodes.append(midpoint + half_length * nodes_1d)
        axis_weights.append(0.5 * weights_1d)
    mesh_nodes = tf.meshgrid(*axis_nodes, indexing="ij")
    mesh_weights = tf.meshgrid(*axis_weights, indexing="ij")
    points = tf.stack([tf.reshape(axis, [-1]) for axis in mesh_nodes], axis=1)
    weights = tf.ones([tf.shape(points)[0]], dtype=DTYPE)
    for axis_weight in mesh_weights:
        weights = weights * tf.reshape(axis_weight, [-1])
    return points, weights


def _log_uniform_reference_weight_density(product_basis: highdim.ProductBasis) -> tf.Tensor:
    log_density = tf.constant(0.0, dtype=DTYPE)
    for basis in product_basis.bases:
        log_density = log_density - tf.math.log(basis.domain.length)
    return log_density


def _logsumexp_weighted(log_values: tf.Tensor, weights: tf.Tensor) -> tf.Tensor:
    max_value = tf.reduce_max(log_values)
    return tf.math.log(tf.reduce_sum(weights * tf.exp(log_values - max_value))) + max_value


def _m5b_model() -> highdim.PredatorPreySSM:
    return highdim.p30_predator_prey_fixture_model()


def _m5b_theta() -> tf.Tensor:
    return _m5b_model().true_parameters()


def _m5b_observations_and_truth(horizon: int) -> tuple[tf.Tensor, tf.Tensor]:
    model = _m5b_model()
    theta = _m5b_theta()
    state = model.initial_mean
    states = []
    observations = []
    for _ in range(int(horizon)):
        states.append(state)
        observations.append(state)
        state = model.transition_mean(theta, state)[0]
    return tf.stack(observations), tf.stack(states)


def _m5b_config(seed: str, *, order: int = 7, rank: int = 8) -> highdim.FixedBranchFilterConfig:
    dim = 2
    product_basis = _basis(dim, degree=max(7, int(order) - 1))
    ranks = (1, int(rank), 1)
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=ranks,
            ridge=1e-10,
            max_sweeps=5,
            sweep_order=(0, 1),
            row_budget=1400,
            column_budget=220,
            dense_matrix_byte_budget=1_200_000,
            normal_matrix_byte_budget=320_000,
            condition_number_warning=1e11,
            condition_number_veto=1e16,
            holdout_tolerance=3e-2,
        ),
        density_tau=1e-12,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=20_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.constant([70.0, 5.5], dtype=DTYPE),
                matrix=tf.linalg.diag(tf.constant([60.0, 5.5], dtype=DTYPE)),
            ),
        ),
        measure_convention=_convention(),
        deterministic_seed=seed,
        product_basis=product_basis,
        initial_cores=_initial_cores(product_basis, ranks),
        fit_quadrature_order=int(order),
    )


def _m5b_grid(config: highdim.FixedBranchFilterConfig) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    reference_points, reference_weights = _reference_grid(config.product_basis, config.fit_quadrature_order)
    physical_points, log_abs_det = config.coordinate_maps[0].forward(reference_points)
    return reference_points, reference_weights, physical_points, log_abs_det


def _m5b_dense_reference(horizon: int, *, order: int = 9) -> dict[str, tf.Tensor]:
    model = _m5b_model()
    theta = _m5b_theta()
    observations, _truth = _m5b_observations_and_truth(horizon)
    config = _m5b_config("p47-m5b-dense-reference", order=order, rank=8)
    _, weights, physical_points, log_abs_det = _m5b_grid(config)
    log_reference_weight = _log_uniform_reference_weight_density(config.product_basis)
    log_terms = []
    means = []
    covariances = []
    log_posterior_physical = None

    for time_index in range(int(observations.shape[0])):
        if time_index == 0:
            log_unnormalized = model.initial_log_density(
                theta,
                physical_points,
            ) + model.observation_log_density(
                theta,
                physical_points,
                observations[time_index],
                t=time_index,
            )
        else:
            count = int(physical_points.shape[0])
            next_points = tf.repeat(physical_points, repeats=count, axis=0)
            previous_points = tf.tile(physical_points, [count, 1])
            transition_log = tf.reshape(
                model.transition_log_density(
                    theta,
                    previous_points,
                    next_points,
                    t=time_index,
                ),
                [count, count],
            )
            log_predictive = tf.reduce_logsumexp(
                tf.math.log(weights)[tf.newaxis, :]
                + log_abs_det[tf.newaxis, :]
                - log_reference_weight
                + log_posterior_physical[tf.newaxis, :]
                + transition_log,
                axis=1,
            )
            log_unnormalized = log_predictive + model.observation_log_density(
                theta,
                physical_points,
                observations[time_index],
                t=time_index,
            )
        log_increment = _logsumexp_weighted(log_unnormalized + log_abs_det - log_reference_weight, weights)
        log_posterior_physical = log_unnormalized - log_increment
        mass = weights * tf.exp(log_posterior_physical + log_abs_det - log_reference_weight)
        mean = tf.reduce_sum(physical_points * mass[:, tf.newaxis], axis=0)
        centered = physical_points - mean[tf.newaxis, :]
        covariance = tf.einsum("n,ni,nj->ij", mass, centered, centered)
        log_terms.append(log_increment)
        means.append(mean)
        covariances.append(covariance)

    return {
        "log_likelihood": tf.reduce_sum(tf.stack(log_terms)),
        "log_normalizers": tf.stack(log_terms),
        "mean_path": tf.stack(means),
        "covariance_path": tf.stack(covariances),
    }


def _m5b_zhaocui_result(horizon: int) -> highdim.FixedBranchFilterResult:
    observations, _truth = _m5b_observations_and_truth(horizon)
    return highdim.multistate_nonlinear_fixed_design_tt_value_path(
        _m5b_model(),
        _m5b_theta(),
        observations,
        _m5b_config("p47-m5b-zhaocui-production-candidate", order=7, rank=8),
        fixture_id="p47.predator-prey.m5b.production-candidate.v1",
        branch_seed_prefix="p47-m5b-predator-prey-production-candidate",
        retained_moment_order=7,
        retained_propagation_order=7,
    )


def _m4b_grid_points(sites: int, order: int) -> int:
    return int(order) ** (2 * int(sites))


def test_p47_production_repair_plan_has_readonly_claude_and_no_sp500_scope() -> None:
    text = MASTER_PLAN.read_text(encoding="utf-8")
    ledger = CLAUDE_LEDGER.read_text(encoding="utf-8")

    assert "Codex remains supervisor and execution agent" in text
    assert "Claude is read-only reviewer" in text
    assert "S&P 500 reproduction remains out of scope" in text
    assert "PASS_P47_PRODUCTION_REPAIR_PLAN" in text
    assert "BLOCK_P47_PRODUCTION_REPAIR_PLAN" in ledger


def test_p47_m4b_manifest_preflight_blocks_current_j9_all_grid_route() -> None:
    manifest = json.loads(M4B_MANIFEST.read_text(encoding="utf-8"))
    cap = int(manifest["preflight_gate"]["max_pairwise_transition_evaluations_cpu"])
    candidates = {row["candidate_id"]: row for row in manifest["candidate_ladder"]}

    assert manifest["status"] == "blocked_current_route_architecture_after_preflight"
    assert manifest["production_token_emitted"] is False
    assert manifest["expected_current_route_blocker"] == "BLOCKED_M4B_ROUTE_ARCHITECTURE"
    assert "PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY" in manifest["prerequisite_tokens"]
    assert "PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING" == manifest["pass_token"]

    j3_grid = _m4b_grid_points(candidates["M4b-0"]["sites"], candidates["M4b-0"]["order"])
    j5_grid = _m4b_grid_points(candidates["M4b-1"]["sites"], candidates["M4b-1"]["order"])
    j9_grid = _m4b_grid_points(candidates["M4b-2"]["sites"], candidates["M4b-2"]["order"])

    assert j3_grid * j3_grid < cap
    assert j5_grid * j5_grid > cap
    assert j9_grid * j9_grid > cap
    assert "BLOCKED_M4B_ROUTE_ARCHITECTURE" in M4B_SUBPLAN.read_text(encoding="utf-8")


def test_p47_m5b_manifest_defines_horizon25_same_target_production_gate() -> None:
    manifest = json.loads(M5B_MANIFEST.read_text(encoding="utf-8"))
    candidates = {row["candidate_id"]: row for row in manifest["candidate_ladder"]}

    assert manifest["target_family"] == "M5a additive-Gaussian RK4 predator-prey closure"
    assert manifest["status"] == "blocked_accuracy_tuning_after_initial_horizon25_candidate"
    assert manifest["production_token_emitted"] is False
    assert manifest["current_blocker"] == "BLOCKED_M5B_PRODUCTION_ACCURACY_TUNING"
    assert manifest["pass_token"] == "PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING"
    assert "PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING" in manifest["prerequisite_tokens"]
    assert candidates["M5b-3"]["horizon"] == 25
    assert candidates["M5b-3"]["reference_order"] == 9
    assert manifest["production_tolerances"]["deterministic_replay_required"] is True
    assert "no nonlinear preconditioning usefulness claim" in manifest["nonclaims"]
    assert "horizon-25 row" in M5B_SUBPLAN.read_text(encoding="utf-8")


def test_p47_m5b_predator_prey_horizon25_records_blocker_when_tolerances_fail() -> None:
    manifest = json.loads(M5B_MANIFEST.read_text(encoding="utf-8"))
    tolerances = manifest["production_tolerances"]
    recorded = manifest["initial_horizon25_result"]
    reference = _m5b_dense_reference(25, order=9)
    result = _m5b_zhaocui_result(25)
    replay = _m5b_zhaocui_result(25)
    observations, truth = _m5b_observations_and_truth(25)
    del observations

    log_normalizers = tf.stack([step.log_normalizer for step in result.steps])
    mean_path = tf.stack([step.diagnostics["retained_mean"] for step in result.steps])
    covariance_path = tf.stack([step.diagnostics["retained_covariance"] for step in result.steps])
    log_gap = tf.abs(result.log_likelihood - reference["log_likelihood"])
    step_gap = tf.reduce_max(tf.abs(log_normalizers - reference["log_normalizers"]))
    mean_error = tf.reduce_max(tf.abs(mean_path - reference["mean_path"]))
    covariance_error = tf.reduce_max(tf.abs(covariance_path - reference["covariance_path"]))
    truth_rmse = tf.sqrt(tf.reduce_mean(tf.square(mean_path - truth), axis=0))

    assert result.status is highdim.HighDimStatus.OK
    assert result.diagnostics["promoted_horizon"] == 25
    assert result.branch_identity.hash.value == replay.branch_identity.hash.value
    tf.debugging.assert_near(result.log_likelihood, replay.log_likelihood, atol=0.0)

    assert float(log_gap.numpy()) > float(tolerances["abs_log_likelihood_gap_lt"])
    assert float(step_gap.numpy()) > float(tolerances["max_step_log_normalizer_gap_lt"])
    assert float(mean_error.numpy()) > float(tolerances["max_state_mean_component_error_lt"])
    assert float(covariance_error.numpy()) > float(tolerances["max_covariance_entry_error_lt"])
    assert float(truth_rmse[0].numpy()) < float(tolerances["truth_path_prey_rmse_lt"]), truth_rmse.numpy()
    assert float(truth_rmse[1].numpy()) < float(tolerances["truth_path_predator_rmse_lt"]), truth_rmse.numpy()

    assert recorded["decision"] == "BLOCKED_M5B_PRODUCTION_ACCURACY_TUNING"
    assert recorded["deterministic_replay"] == "PASS"
    assert abs(float(recorded["abs_log_likelihood_gap"]) - float(log_gap.numpy())) < 1e-9
    assert abs(float(recorded["max_step_log_normalizer_gap"]) - float(step_gap.numpy())) < 1e-9
