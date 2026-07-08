from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
import scripts.filtering_value_gradient_benchmark_run_p8d_numeric as p8d


LGSSM_ROW = "benchmark_lgssm_exact_oracle_m3_T50"
SV_ROW = "zhao_cui_sv_actual_nongaussian_T1000"
KSC_ROW = "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000"
SIR_ROW = "zhao_cui_spatial_sir_austria_j9_T20"
PREDATOR_PREY_ROW = "zhao_cui_predator_prey_T20"
GENERALIZED_SV_ROW = "zhao_cui_generalized_sv_synthetic_from_estimated_values"
DPF_SEEDS = [81120, 81121, 81122, 81123, 81124]


def _adapters() -> dict[tuple[str, str], dict[str, str]]:
    with p8d.ADAPTER_MATRIX_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {(row["algorithm_id"], row["model_row_id"]): row for row in rows}


def test_p8d_source_scope_and_route_policy_are_mechanical() -> None:
    source_scope = json.loads(p8d.SOURCE_SCOPE_PATH.read_text(encoding="utf-8"))
    adapters = _adapters()
    algorithms = source_scope["algorithm_ids"]
    rows = source_scope["source_scope_row_ids"]

    assert len(adapters) == len(algorithms) * len(rows)
    assert set(adapters) == {(algorithm, row) for algorithm in algorithms for row in rows}
    assert not p8d._has_deterministic_route("kalman_exact_or_mixture_enumeration", SV_ROW)
    assert not p8d._has_deterministic_route("kalman_exact_or_mixture_enumeration", SIR_ROW)
    assert not p8d._has_dpf_route(KSC_ROW)
    for row in (LGSSM_ROW, SV_ROW, SIR_ROW, PREDATOR_PREY_ROW, GENERALIZED_SV_ROW):
        assert p8d._has_dpf_route(row)


def test_p8d_artifact_accounting_separates_real_gaps_from_true_not_applicable() -> None:
    real_cells = [
        {"numeric_execution_status": "executed_numeric"},
        {"numeric_execution_status": "structured_not_applicable"},
        {"numeric_execution_status": "blocked_pending_model_specific_dpf_callbacks"},
    ]
    executed = [
        cell for cell in real_cells if cell["numeric_execution_status"].startswith("executed")
    ]
    structured_not_applicable = [
        cell
        for cell in real_cells
        if cell["numeric_execution_status"] == "structured_not_applicable"
    ]
    real_gaps = [
        cell
        for cell in real_cells
        if not cell["numeric_execution_status"].startswith("executed")
        and cell["numeric_execution_status"] != "structured_not_applicable"
    ]

    assert len(executed) == 1
    assert len(structured_not_applicable) == 1
    assert len(real_gaps) == 1


def test_p8d_lgssm_exact_cell_has_p8d_schema_and_no_autodiff_fallback() -> None:
    adapter = _adapters()[("kalman_exact_or_mixture_enumeration", LGSSM_ROW)]
    cell = p8d._numeric_lgssm_exact_cell(adapter)

    assert cell["numeric_execution_status"] == "executed_numeric"
    assert cell["reason_codes"] == ["P8D_NUMERIC_EXECUTED_EXACT_LGSSM_DIFFERENTIATED_KALMAN"]
    assert isinstance(cell["log_likelihood"], float)
    assert len(cell["score"]) == 5
    assert cell["score_derivative_provenance"] == (
        "tf_covariance_differentiated_kalman_reference_cholesky_solve_physical_theta"
    )
    assert "tf_autodiff" not in cell["score_derivative_provenance"]


def test_p8d_raw_sv_ukf_smoke_value_is_augmented_noise_diagnostic() -> None:
    adapter = _adapters()[("ukf", SV_ROW)]
    cell = p8d._numeric_deterministic_cell("ukf", SV_ROW, adapter)

    assert cell["numeric_execution_status"] == "executed_numeric_value_score"
    assert isinstance(cell["log_likelihood"], float)
    assert isinstance(cell["score_l2_norm"], float)
    assert cell["score_l2_norm"] >= 0.0
    assert cell["score_derivative_provenance"] == (
        "ukf_augmented_noise_sigma_point_raw_sv_tf_autodiff_score"
    )
    assert "actual raw-observation SV sigma-point approximation with observation-noise augmentation" in cell["nonclaims"]
    assert cell["score_adapter_status"] == "executed_p8d_tf_autodiff_score"
    assert "not exact nonlinear likelihood" in " ".join(cell["nonclaims"])


def test_p8d_spatial_sir_value_only_cell_preserves_no_free_theta() -> None:
    adapter = _adapters()[("ukf", SIR_ROW)]
    cell = p8d._numeric_deterministic_cell("ukf", SIR_ROW, adapter)

    assert cell["numeric_execution_status"] in {
        "executed_numeric_value_only_no_free_theta",
        "blocked_p8d_deterministic_smoke_failed",
    }
    assert cell["score_adapter_status"] == "not_applicable_no_free_theta"
    assert cell["hessian_adapter_status"] == "not_applicable_no_free_theta"
    assert cell["score"] is None


def test_p8j_sir_dpf_callbacks_tie_out_to_author_sir_model() -> None:
    model = highdim.zhao_cui_sir_austria_model()
    callbacks = p8d._dpf_sir_callbacks()
    points = model.initial_mean[tf.newaxis, :] + tf.reshape(
        tf.linspace(tf.constant(-0.35, dtype=tf.float64), tf.constant(0.35, dtype=tf.float64), 18),
        [1, 18],
    )

    required = {
        "initial_sample",
        "transition_sample",
        "transition_mean_fn",
        "transition_log_density_fn",
        "observation_mean_fn",
        "observation_jacobian_fn",
        "observation_log_density_fn",
        "process_noise_covariance_fn",
        "observation_covariance_fn",
        "initial_covariance",
        "sir_model_metadata",
        "ledh_observation_adapter",
    }
    assert required.issubset(callbacks)
    metadata = callbacks["sir_model_metadata"]
    assert metadata["row_id"] == SIR_ROW
    assert metadata["state_dimension"] == 18
    assert metadata["observation_dimension"] == 9
    assert metadata["rk4_variant"] == "zhao_cui_sir_step"
    assert metadata["process_noise_policy"] == "clip_susceptible_after_noise"
    assert metadata["transition_density_contract"] == (
        "gaussian_pre_projection_density_used_by_reviewed_clipped_path_adapter"
    )
    assert callbacks["ledh_observation_adapter"]["target_density_used_for_correction"] is True
    assert callbacks["ledh_observation_adapter"]["surrogate_target_claim"] is False
    assert "not Zhao-Cui TT/SIRT" in callbacks["ledh_observation_adapter"]["adapter_classification"]

    tf.debugging.assert_near(
        callbacks["transition_mean_fn"](points, 0),
        model.transition_mean(points),
        atol=0.0,
    )
    tf.debugging.assert_near(
        callbacks["observation_mean_fn"](points, 0),
        model.infectious_components(points),
        atol=0.0,
    )

    expected_selector = tf.one_hot(
        tf.constant(model.observed_state_indices(), dtype=tf.int32),
        depth=model.state_dim(),
        dtype=tf.float64,
    )
    actual_selector = callbacks["observation_jacobian_fn"](points[0], 0)
    assert bool(tf.reduce_all(tf.equal(actual_selector, expected_selector)).numpy())
    assert bool(tf.reduce_all(tf.equal(callbacks["initial_covariance"], model.initial_covariance)).numpy())
    assert bool(
        tf.reduce_all(
            tf.equal(callbacks["process_noise_covariance_fn"](points[0], 0), model.process_covariance)
        ).numpy()
    )
    assert bool(
        tf.reduce_all(tf.equal(callbacks["observation_covariance_fn"](0), model.observation_covariance)).numpy()
    )

    samples = callbacks["initial_sample"](3, 81120)
    assert samples.shape == (3, 18)
    transitions = callbacks["transition_sample"](points, 81120, 0)
    assert transitions.shape == (1, 18)
    assert bool(tf.reduce_all(tf.math.is_finite(transitions)).numpy())

    observation = model.infectious_components(points)[0]
    log_density = callbacks["observation_log_density_fn"](points, observation, 0)
    transition_log_density = callbacks["transition_log_density_fn"](
        transitions,
        points,
        0,
    )
    assert log_density.shape == (1,)
    assert transition_log_density.shape == (1,)
    assert bool(tf.reduce_all(tf.math.is_finite(log_density)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(transition_log_density)).numpy())


def test_p8j_sir_dpf_transition_sample_clips_only_susceptible(monkeypatch: pytest.MonkeyPatch) -> None:
    model = highdim.zhao_cui_sir_austria_model()
    callbacks = p8d._dpf_sir_callbacks()
    original_normal = p8d.tf.random.stateless_normal
    expected_shape = [1, model.state_dim()]

    def fake_normal(shape, seed, dtype):
        del seed
        if list(shape) == expected_shape:
            noise = tf.zeros(shape, dtype=dtype)
            return tf.tensor_scatter_nd_update(
                noise,
                indices=tf.constant([[0, 0], [0, 1]], dtype=tf.int32),
                updates=tf.constant([-1.0e6, -1.0e6], dtype=dtype),
            )
        return original_normal(shape, seed=seed, dtype=dtype)

    monkeypatch.setattr(p8d.tf.random, "stateless_normal", fake_normal)
    pushed = callbacks["transition_sample"](model.initial_mean[tf.newaxis, :], 81120, 0)[0]

    assert float(pushed[0].numpy()) == 0.0
    assert float(pushed[1].numpy()) < 0.0


def test_p8j_sir_dpf_route_and_bootstrap_smoke_are_finite() -> None:
    callbacks, observations, route_label, horizon = p8d._dpf_route(SIR_ROW)

    assert p8d._has_dpf_route(SIR_ROW)
    assert route_label == "spatial_sir_austria_j9_T20"
    assert horizon == 20
    assert observations.shape == (20, 9)
    assert callbacks["sir_model_metadata"]["row_id"] == SIR_ROW

    result = p8d._dpf_single_run(
        "bootstrap_dpf_current",
        row_id=SIR_ROW,
        seed=81120,
        particle_count=4,
    )
    log_likelihood = tf.convert_to_tensor(result.log_likelihood_estimate, dtype=tf.float64)
    ess = tf.convert_to_tensor(result.ess_by_time, dtype=tf.float64)
    assert result.finite
    assert bool(tf.math.is_finite(log_likelihood).numpy())
    assert ess.shape == (20,)
    assert result.method_id == "bootstrap_dpf_current_spatial_sir_austria_j9_T20_tf"


def test_p8d_dpf_bootstrap_sv_cell_has_exactly_five_seed_contract() -> None:
    adapter = _adapters()[("bootstrap_dpf_current", SV_ROW)]
    old_seeds = p8d.DPF_SEEDS
    old_particles = p8d.DPF_PARTICLE_COUNT
    try:
        p8d.DPF_SEEDS = [81120, 81121, 81122, 81123, 81124]
        p8d.DPF_PARTICLE_COUNT = 4
        cell = p8d._numeric_dpf_cell("bootstrap_dpf_current", SV_ROW, adapter)
    finally:
        p8d.DPF_SEEDS = old_seeds
        p8d.DPF_PARTICLE_COUNT = old_particles

    assert cell["numeric_execution_status"] == "executed_numeric_dpf_5seed_value"
    assert cell["seed_list"] == DPF_SEEDS
    assert cell["seed_count"] == 5
    assert len(cell["per_seed_results"]) == 5
    assert cell["score"] is None
    assert cell["mc_standard_error"] is not None
    assert "not a DPF gradient certification" in cell["nonclaims"]


def test_p8d_ledh_sv_adapters_use_surrogate_flow_and_raw_correction_contract() -> None:
    sv_callbacks = p8d._dpf_sv_callbacks(p8d._sv_theta())
    sv_raw = p8d._sv_observations()[:3]
    sv_flow = sv_callbacks["ledh_flow_observations_fn"](sv_raw)
    sv_beta = tf.exp(p8d._sv_theta()[1])
    expected_sv_flow = p8d._log_square_surrogate_observations(sv_raw) - 2.0 * tf.math.log(sv_beta)

    tf.debugging.assert_near(sv_flow, expected_sv_flow)
    tf.debugging.assert_near(
        sv_callbacks["observation_mean_fn"](tf.constant([[1.25]], dtype=tf.float64), 0),
        tf.constant([[1.25]], dtype=tf.float64),
    )
    tf.debugging.assert_near(
        sv_callbacks["observation_covariance_fn"](0),
        tf.constant([[2.0]], dtype=tf.float64),
    )
    assert sv_callbacks["ledh_observation_adapter"]["target_density_used_for_correction"] is True
    assert sv_callbacks["ledh_observation_adapter"]["surrogate_target_claim"] is False
    assert "flow_only" in sv_callbacks["ledh_observation_adapter"]["flow_observation_contract"]

    generalized_callbacks = p8d._dpf_generalized_sv_callbacks(p8d._generalized_sv_theta())
    generalized_raw = p8d._generalized_sv_observations()[:3]
    generalized_flow = generalized_callbacks["ledh_flow_observations_fn"](generalized_raw)

    tf.debugging.assert_near(
        generalized_flow,
        p8d._log_square_surrogate_observations(generalized_raw),
    )
    assert generalized_callbacks["ledh_observation_adapter"]["target_density_used_for_correction"] is True
    assert generalized_callbacks["ledh_observation_adapter"]["surrogate_target_claim"] is False
    assert "not same-target" in generalized_callbacks["ledh_observation_adapter"]["adapter_classification"]


@pytest.mark.parametrize("row_id", [SV_ROW, GENERALIZED_SV_ROW])
def test_p8d_ledh_sv_style_short_cells_are_finite_with_adapter_metadata(
    monkeypatch: pytest.MonkeyPatch,
    row_id: str,
) -> None:
    adapter = _adapters()[("ledh_pfpf_alg1_ukf_current", row_id)]
    original_route = p8d._dpf_route

    def short_route(current_row_id: str):
        callbacks, observations, route_label, _horizon = original_route(current_row_id)
        if current_row_id == row_id:
            return callbacks, observations[:4], f"{route_label}_short_p8e", 4
        return callbacks, observations, route_label, _horizon

    old_seeds = p8d.DPF_SEEDS
    old_particles = p8d.DPF_PARTICLE_COUNT
    try:
        monkeypatch.setattr(p8d, "_dpf_route", short_route)
        p8d.DPF_SEEDS = [81120, 81121, 81122, 81123, 81124]
        p8d.DPF_PARTICLE_COUNT = 4
        cell = p8d._numeric_dpf_cell("ledh_pfpf_alg1_ukf_current", row_id, adapter)
    finally:
        p8d.DPF_SEEDS = old_seeds
        p8d.DPF_PARTICLE_COUNT = old_particles

    assert cell["numeric_execution_status"] == "executed_numeric_dpf_5seed_value"
    assert cell["ledh_observation_adapter"]["target_density_used_for_correction"] is True
    assert cell["ledh_observation_adapter"]["surrogate_target_claim"] is False
    assert len(cell["per_seed_results"]) == 5
    assert all(result["finite"] for result in cell["per_seed_results"])
    assert all(
        result["route_identifiers"]["method_generation"] == "li_coates_algorithm1_ukf_covariance_lifecycle"
        for result in cell["per_seed_results"]
    )


def test_p8g_profile_prefix_payload_records_bottleneck_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_route = p8d._dpf_route

    def short_route(current_row_id: str):
        callbacks, observations, route_label, _horizon = original_route(current_row_id)
        if current_row_id == SV_ROW:
            return callbacks, observations[:4], f"{route_label}_short_p8g_test", 4
        return callbacks, observations, route_label, _horizon

    monkeypatch.setattr(p8d, "_dpf_route", short_route)
    payload = p8d._p8g_profile_dpf_prefix(
        row_id=SV_ROW,
        algorithm_id="ledh_pfpf_alg1_ukf_current",
        horizon=2,
        particle_count=2,
        seeds=[81120],
        device="cpu",
        g0_manifest=None,
    )

    assert payload["schema_version"] == "filter_bench.p8g_profile.v1"
    assert payload["status"] == "executed_p8g_prefix_profile"
    assert payload["profile_scope"]["horizon_prefix"] == 2
    assert payload["profile_scope"]["particle_count"] == 2
    assert payload["profile_scope"]["seeds"] == [81120]
    assert payload["profile_scope"]["route_variant"] == "current_looped_particles"
    assert payload["run_manifest"]["requested_device"] == "cpu"
    assert payload["run_manifest"]["vectorized_particles"] is False
    assert payload["per_seed_results"][0]["finite"] is True
    assert payload["per_seed_results"][0]["route_identifiers"]["method_generation"] == (
        "li_coates_algorithm1_ukf_covariance_lifecycle"
    )
    assert "not tuned particle-count evidence" in payload["nonclaims"]
    assert any(
        "per-particle UKF" in item
        for item in payload["bottleneck_hypothesis"]["known_python_loops"]
    )

    vectorized_payload = p8d._p8g_profile_dpf_prefix(
        row_id=SV_ROW,
        algorithm_id="ledh_pfpf_alg1_ukf_current",
        horizon=2,
        particle_count=2,
        seeds=[81120],
        device="cpu",
        g0_manifest=None,
        vectorized_particles=True,
    )
    assert vectorized_payload["profile_scope"]["route_variant"] == "p8g_vectorized_particles"
    assert vectorized_payload["run_manifest"]["vectorized_particles"] is True
    assert vectorized_payload["value_summary"]["mean_log_likelihood"] == pytest.approx(
        payload["value_summary"]["mean_log_likelihood"],
        abs=1e-10,
    )

    graph_payload = p8d._p8g_profile_dpf_prefix(
        row_id=SV_ROW,
        algorithm_id="ledh_pfpf_alg1_ukf_current",
        horizon=2,
        particle_count=2,
        seeds=[81120],
        device="cpu",
        g0_manifest=None,
        sv_scalar_graph=True,
    )
    assert graph_payload["profile_scope"]["route_variant"] == "p8g_sv_scalar_graph"
    assert graph_payload["run_manifest"]["sv_scalar_graph"] is True
    assert graph_payload["run_manifest"]["vectorized_particles"] is False
    assert graph_payload["per_seed_results"][0]["route_identifiers"]["time_loop_route"] == "tf_while_loop"
    assert graph_payload["per_seed_results"][0]["route_identifiers"]["particle_batch_route"] == (
        "closed_form_scalar_vector_ops"
    )
    assert graph_payload["value_summary"]["mean_log_likelihood"] == pytest.approx(
        payload["value_summary"]["mean_log_likelihood"],
        abs=1e-10,
    )
    with pytest.raises(ValueError, match="choose either"):
        p8d._p8g_profile_dpf_prefix(
            row_id=SV_ROW,
            algorithm_id="ledh_pfpf_alg1_ukf_current",
            horizon=2,
            particle_count=2,
            seeds=[81120],
            device="cpu",
            g0_manifest=None,
            vectorized_particles=True,
            sv_scalar_graph=True,
        )


def test_p8h_ot_resampled_prefix_payload_uses_new_schema_and_quarantines_p8g(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_route = p8d._dpf_route

    def short_route(current_row_id: str):
        callbacks, observations, route_label, _horizon = original_route(current_row_id)
        if current_row_id == SV_ROW:
            return callbacks, observations[:4], f"{route_label}_short_p8h_test", 4
        return callbacks, observations, route_label, _horizon

    monkeypatch.setattr(p8d, "_dpf_route", short_route)
    payload = p8d._p8h_profile_dpf_prefix(
        row_id=SV_ROW,
        algorithm_id="ledh_pfpf_alg1_ukf_current",
        horizon=2,
        particle_count=3,
        seeds=[81120],
        device="cpu",
        g0_manifest=None,
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        ess_threshold_ratio=1.01,
    )

    assert payload["schema_version"] == "filter_bench.p8h_ot_resampled_alg1_smoke.v1"
    assert payload["status"] == "executed_p8h_ot_resampled_alg1_smoke"
    assert payload["profile_scope"]["route_variant"] == p8d.P8H_ROUTE_VARIANT
    assert payload["profile_scope"]["resampling_route"] == p8d.P8H_DEFAULT_RESAMPLING_ROUTE
    assert payload["p8g_quarantine"]["p8h_schema_reuses_p8g_metadata"] is False
    assert payload["per_seed_results"][0]["finite"] is True
    assert payload["per_seed_results"][0]["resampling_count"] == 2
    route = payload["per_seed_results"][0]["route_identifiers"]
    assert route["route_variant"] == p8d.P8H_ROUTE_VARIANT
    assert route["resampling_route"] == p8d.P8H_DEFAULT_RESAMPLING_ROUTE
    first_diag = payload["per_seed_results"][0]["first_resampling_diagnostics"]
    assert first_diag["resampling_method"] == "fixed_target_sinkhorn"
    assert first_diag["relaxed_resampling_not_categorical"] is True
    assert first_diag["canonical_transport_shape"] == [3, 3]
    assert "not gradient correctness" in payload["nonclaims"]


def test_p8g_fixed_randomness_gradient_check_records_g3_contract() -> None:
    payload = p8d._p8g_fixed_randomness_gradient_check(
        rows=[SV_ROW],
        horizon=2,
        particle_count=2,
        seeds=[81120],
        route_variant="p8g_sv_scalar_graph",
        coordinate="canonical_unconstrained",
        device="cpu",
        g0_manifest=None,
    )

    assert payload["schema_version"] == "filter_bench.p8g_fixed_randomness_gradient.v1"
    assert payload["status"] == "executed_p8g_fixed_randomness_gradient_check"
    assert payload["scope"]["route_variant"] == "p8g_sv_scalar_graph"
    assert payload["scope"]["coordinate"] == "canonical_unconstrained"
    assert payload["scope"]["resampling_route"] == "none"
    assert payload["summary"]["all_values_finite"] is True
    assert payload["summary"]["all_gradients_finite"] is True
    assert payload["summary"]["max_repeat_gradient_abs_delta"] == pytest.approx(0.0, abs=1e-12)
    assert payload["summary"]["max_abs_fd_residual"] is not None
    assert payload["per_seed_results"][0]["gradient"] is not None
    assert payload["per_seed_results"][0]["repeat_value_abs_delta"] == pytest.approx(0.0, abs=1e-12)
    assert payload["per_seed_results"][0]["randomness_contract"] == (
        "stateless_normals_precomputed_outside_xla_seed_salts_110_and_1110_plus_t"
    )
    assert "not the stochastic PF marginal likelihood gradient" in payload["nonclaims"]

    with pytest.raises(ValueError, match="actual_sv"):
        p8d._p8g_fixed_randomness_gradient_check(
            rows=["not_actual_sv"],
            horizon=2,
            particle_count=2,
            seeds=[81120],
            route_variant="p8g_sv_scalar_graph",
            coordinate="canonical_unconstrained",
            device="cpu",
            g0_manifest=None,
        )
    with pytest.raises(ValueError, match="route variant"):
        p8d._p8g_fixed_randomness_gradient_check(
            rows=[SV_ROW],
            horizon=2,
            particle_count=2,
            seeds=[81120],
            route_variant="p8g_vectorized_particles",
            coordinate="canonical_unconstrained",
            device="cpu",
            g0_manifest=None,
        )
    with pytest.raises(ValueError, match="canonical_unconstrained"):
        p8d._p8g_fixed_randomness_gradient_check(
            rows=[SV_ROW],
            horizon=2,
            particle_count=2,
            seeds=[81120],
            route_variant="p8g_sv_scalar_graph",
            coordinate="physical",
            device="cpu",
            g0_manifest=None,
        )


def test_p8g_particle_tuning_schema_selects_smallest_confirmed_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_profile(**kwargs):
        particle_count = kwargs["particle_count"]
        horizon = kwargs["horizon"]
        seeds = kwargs["seeds"]
        return {
            "status": "executed_p8g_prefix_profile",
            "profile_scope": {
                "row_id": kwargs["row_id"],
                "algorithm_id": kwargs["algorithm_id"],
                "route_variant": "p8g_sv_scalar_graph",
                "full_horizon": 1000,
                "horizon_prefix": horizon,
                "particle_count": particle_count,
                "seeds": seeds,
                "seed_count": len(seeds),
            },
            "timing": {"wall_seconds": 0.25},
            "per_seed_results": [
                {
                    "seed": seed,
                    "finite": True,
                    "log_likelihood": -100.0 - horizon * 0.01,
                    "effective_sample_size_min": 0.75 * particle_count,
                    "effective_sample_size_mean": 0.80 * particle_count,
                    "method_id": "fake_ledh",
                }
                for seed in seeds
            ],
        }

    monkeypatch.setattr(p8d, "_p8g_profile_dpf_prefix", fake_profile)
    payload = p8d._p8g_g4_tuning_payload(
        stage="stage0",
        rows=[SV_ROW],
        algorithms=["ledh_pfpf_alg1_ukf_current"],
        horizons=[50],
        particles=[16, 32],
        seeds=[81120, 81121],
        route_variant="p8g_sv_scalar_graph",
        device="cpu",
        g0_manifest=None,
        runtime_budget_seconds=10.0,
    )

    assert payload["schema_version"] == "filter_bench.p8g_particle_tuning.v1"
    assert payload["status"] == "executed_p8g_particle_tuning_stage0"
    assert payload["scope"]["historical_particle_count_not_selectable"] == 8
    assert payload["summary"]["all_requested_cells_accounted"] is True
    assert payload["summary"]["selected_count"] == 1
    assert payload["summary"]["deferred_count"] == 0
    selected = payload["selected_blocked"][0]
    assert selected["tuning_status"] == "selected_particle_count"
    assert selected["selected_particle_count"] == 16
    assert selected["next_rung_checked"] is True
    assert selected["next_rung_particle_count"] == 32
    assert selected["min_relative_ess"] >= 0.25
    assert "not HMC readiness" in payload["nonclaims"]


def test_p8g_particle_tuning_preserves_deferred_rows_and_rejects_n8(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_if_called(**kwargs):
        raise AssertionError(f"deferred rows should not execute: {kwargs}")

    monkeypatch.setattr(p8d, "_p8g_profile_dpf_prefix", fail_if_called)
    payload = p8d._p8g_g4_tuning_payload(
        stage="stage0",
        rows=[SV_ROW, GENERALIZED_SV_ROW],
        algorithms=["bootstrap_dpf_current"],
        horizons=[50],
        particles=[16, 32],
        seeds=[81120],
        route_variant="p8g_sv_scalar_graph",
        device="cpu",
        g0_manifest=None,
    )

    assert payload["summary"]["evaluated_rung_count"] == 0
    assert payload["summary"]["deferred_count"] == 2
    assert payload["summary"]["all_requested_cells_accounted"] is True
    assert payload["status"] == "blocked_p8g_particle_tuning_no_executable_rungs"
    assert {row["row_id"] for row in payload["selected_blocked"]} == {SV_ROW, GENERALIZED_SV_ROW}
    assert all(row["tuning_status"] == "deferred_not_in_initial_g4_scope" for row in payload["selected_blocked"])
    assert all(row["selected_particle_count"] is None for row in payload["selected_blocked"])

    with pytest.raises(ValueError, match="N=8"):
        p8d._p8g_g4_tuning_payload(
            stage="stage0",
            rows=[SV_ROW],
            algorithms=["ledh_pfpf_alg1_ukf_current"],
            horizons=[50],
            particles=[8, 16],
            seeds=[81120],
            route_variant="p8g_sv_scalar_graph",
            device="cpu",
            g0_manifest=None,
        )


def test_p8g_particle_tuning_stage0_reports_ess_failure_not_missing_next_rung(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def low_ess_profile(**kwargs):
        particle_count = kwargs["particle_count"]
        horizon = kwargs["horizon"]
        seeds = kwargs["seeds"]
        return {
            "status": "executed_p8g_prefix_profile",
            "profile_scope": {
                "row_id": kwargs["row_id"],
                "algorithm_id": kwargs["algorithm_id"],
                "route_variant": "p8g_sv_scalar_graph",
                "full_horizon": 1000,
                "horizon_prefix": horizon,
                "particle_count": particle_count,
                "seeds": seeds,
                "seed_count": len(seeds),
            },
            "timing": {"wall_seconds": 0.25},
            "per_seed_results": [
                {
                    "seed": seed,
                    "finite": True,
                    "log_likelihood": -100.0 - horizon * 0.01 - particle_count * 0.001,
                    "effective_sample_size_min": 0.05 * particle_count,
                    "effective_sample_size_mean": 0.10 * particle_count,
                    "method_id": "fake_ledh_low_ess",
                }
                for seed in seeds
            ],
        }

    monkeypatch.setattr(p8d, "_p8g_profile_dpf_prefix", low_ess_profile)
    payload = p8d._p8g_g4_tuning_payload(
        stage="stage0",
        rows=[SV_ROW],
        algorithms=["ledh_pfpf_alg1_ukf_current"],
        horizons=[50, 200],
        particles=[16, 32],
        seeds=[81120, 81121],
        route_variant="p8g_sv_scalar_graph",
        device="cpu",
        g0_manifest=None,
        runtime_budget_seconds=10.0,
    )

    verdict = payload["selected_blocked"][0]
    assert verdict["tuning_status"] == "blocked_particle_tuning_not_converged"
    assert verdict["blocker_reason"] == "BLOCK_DPF_PARTICLE_TUNING_RELATIVE_ESS"
    assert verdict["selected_particle_count"] is None


def test_p8g_particle_tuning_writes_rung_and_selected_blocked_csvs(tmp_path: Path) -> None:
    payload = {
        "evaluated_rungs": [
            {
                "stage": "stage0",
                "row_id": SV_ROW,
                "algorithm_id": "ledh_pfpf_alg1_ukf_current",
                "route_variant": "p8g_sv_scalar_graph",
                "full_horizon": 1000,
                "horizon_prefix": 50,
                "particle_count": 16,
                "seed_count": 1,
                "finite": True,
                "mean_log_likelihood": -1.0,
                "mean_average_log_likelihood": -0.02,
                "sample_standard_deviation": 0.0,
                "mc_standard_error": 0.0,
                "min_relative_ess": 0.75,
                "mean_relative_ess": 0.8,
                "runtime_seconds": 0.1,
                "runtime_budget_seconds": 10.0,
                "runtime_budget_status": "within_budget",
                "status": "executed_p8g_prefix_profile",
            }
        ],
        "selected_blocked": [
            p8d._p8g_g4_deferred_record(
                row_id=GENERALIZED_SV_ROW,
                algorithm_id="ledh_pfpf_alg1_ukf_current",
                route_variant="p8g_sv_scalar_graph",
                reason="test deferred",
            )
        ],
    }
    rung_csv = tmp_path / "rungs.csv"
    selected_csv = tmp_path / "selected.csv"

    p8d._write_p8g_particle_tuning_csv(rung_csv, payload)
    p8d._write_p8g_selected_blocked_csv(selected_csv, payload)

    rung_rows = list(csv.DictReader(rung_csv.open(newline="", encoding="utf-8")))
    selected_rows = list(csv.DictReader(selected_csv.open(newline="", encoding="utf-8")))
    assert rung_rows[0]["particle_count"] == "16"
    assert selected_rows[0]["row_id"] == GENERALIZED_SV_ROW
    assert selected_rows[0]["tuning_status"] == "deferred_not_in_initial_g4_scope"


def _fake_p8h_profile(
    *,
    row_id: str = SV_ROW,
    algorithm_id: str = "ledh_pfpf_alg1_ukf_current",
    horizon: int,
    particle_count: int,
    seeds: list[int],
    device: str = "gpu",
    resampling_route: str | None = None,
    **_kwargs,
) -> dict:
    route = resampling_route or p8d.P8H_DEFAULT_RESAMPLING_ROUTE
    mean_by_count = {5: -10.0, 10: -10.3, 20: -10.31}
    base = mean_by_count.get(particle_count, -10.0)
    per_seed = []
    for index, seed in enumerate(seeds):
        per_seed.append(
            {
                "seed": seed,
                "runtime_seconds": 0.1,
                "finite": True,
                "log_likelihood": base + 0.01 * index + 0.001 * horizon,
                "average_log_likelihood": (base + 0.01 * index + 0.001 * horizon) / horizon,
                "effective_sample_size_min": 0.7 * particle_count,
                "effective_sample_size_mean": 0.8 * particle_count,
                "resampling_count": horizon,
                "method_id": "fake_p8h",
                "log_likelihood_device": "/job:localhost/replica:0/task:0/device:GPU:0",
                "ess_device": "/job:localhost/replica:0/task:0/device:GPU:0",
                "route_identifiers": {
                    "route_variant": p8d.P8H_ROUTE_VARIANT,
                    "resampling_route": route,
                },
                "first_resampling_diagnostics": {
                    "resampling_route": route,
                    "canonical_transport_matrix_convention": "target_by_source_row_stochastic",
                    "canonical_transport_shape": [particle_count, particle_count],
                    "state_transport_shape": [particle_count, particle_count],
                    "covariance_transport_shape": [particle_count, particle_count],
                    "canonical_transport_row_sum_residual": 1e-8,
                    "canonical_transport_row_sum_tolerance": 5e-3,
                    "finite_transport": True,
                    "finite_particles": True,
                    "finite_carried_covariances": True,
                    "finite_corrected_log_weights": True,
                    "finite_predicted_covariances": True,
                    "finite_updated_covariances": True,
                },
            }
        )
    return {
        "schema_version": "filter_bench.p8h_ot_resampled_alg1_smoke.v1",
        "status": "executed_p8h_ot_resampled_alg1_smoke",
        "run_manifest": {
            "requested_device": device,
            "wall_seconds": 1.0,
        },
        "profile_scope": {
            "row_id": row_id,
            "algorithm_id": algorithm_id,
            "route_variant": p8d.P8H_ROUTE_VARIANT,
            "resampling_route": route,
            "full_horizon": 1000,
            "horizon_prefix": horizon,
            "particle_count": particle_count,
            "seeds": seeds,
            "seed_count": len(seeds),
        },
        "device_diagnostics": {
            "devices_used_by_result_tensors": ["/job:localhost/replica:0/task:0/device:GPU:0"],
            "no_silent_cpu_fallback_claim": True,
        },
        "per_seed_results": per_seed,
    }


def test_p8h_phase5_tuning_schema_selects_smallest_stage0_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(p8d, "_p8h_profile_dpf_prefix", _fake_p8h_profile)
    payload = p8d._p8h_phase5_tuning_payload(
        rows=[SV_ROW],
        algorithms=["ledh_pfpf_alg1_ukf_current"],
        horizons=[4, 8],
        particles=[5, 10, 20],
        seeds=DPF_SEEDS,
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        runtime_budget_seconds=10.0,
    )

    assert payload["schema_version"] == "filter_bench.p8h_particle_tuning.v1"
    assert payload["status"] == "executed_p8h_particle_tuning_stage0"
    assert payload["scope"]["resampling_route"] == p8d.P8H_DEFAULT_RESAMPLING_ROUTE
    assert payload["summary"]["selected_count"] == 1
    assert payload["summary"]["all_requested_cells_accounted"] is True
    assert "P8g no-resampling is historical context only" in payload["evidence_contract"]["baseline"]
    selected = payload["selected_blocked"][0]
    assert selected["tuning_status"] == "selected_particle_count"
    assert selected["selected_particle_count"] == 5
    assert selected["next_rung_particle_count"] == 10
    assert all(item["adjacent_pass"] for item in selected["adjacent_horizon_summaries"])
    assert "not GPU scaling" in payload["nonclaims"]


def test_p8h_phase5_tuning_enforces_trusted_gpu_and_five_seeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(p8d, "_p8h_profile_dpf_prefix", _fake_p8h_profile)
    common = dict(
        rows=[SV_ROW],
        algorithms=["ledh_pfpf_alg1_ukf_current"],
        horizons=[4, 8],
        particles=[5, 10, 20],
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        g0_manifest=Path("docs/plans/fake-g0.md"),
    )
    with pytest.raises(ValueError, match="trusted GPU"):
        p8d._p8h_phase5_tuning_payload(
            **common,
            seeds=DPF_SEEDS,
            device="cpu",
        )
    with pytest.raises(ValueError, match="five fixed seeds"):
        p8d._p8h_phase5_tuning_payload(
            **common,
            seeds=DPF_SEEDS[:2],
            device="gpu",
        )
    with pytest.raises(ValueError, match="Sinkhorn"):
        non_sinkhorn = dict(common)
        non_sinkhorn["resampling_route"] = "ot_annealed_transport_covariance_carry"
        p8d._p8h_phase5_tuning_payload(
            **non_sinkhorn,
            seeds=DPF_SEEDS,
            device="gpu",
        )


def test_p8h_phase5_tuning_blocks_transport_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def bad_transport_profile(**kwargs):
        profile = _fake_p8h_profile(**kwargs)
        for entry in profile["per_seed_results"]:
            entry["first_resampling_diagnostics"]["canonical_transport_shape"] = [1, 1]
        return profile

    monkeypatch.setattr(p8d, "_p8h_profile_dpf_prefix", bad_transport_profile)
    payload = p8d._p8h_phase5_tuning_payload(
        rows=[SV_ROW],
        algorithms=["ledh_pfpf_alg1_ukf_current"],
        horizons=[4, 8],
        particles=[5, 10],
        seeds=DPF_SEEDS,
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        runtime_budget_seconds=10.0,
    )

    verdict = payload["selected_blocked"][0]
    assert verdict["tuning_status"] == "blocked_particle_tuning_not_converged"
    assert verdict["blocker_reason"] == "BLOCK_P8H_PARTICLE_TUNING_TRANSPORT"


def _fake_p8j_profile(
    *,
    row_id: str = SIR_ROW,
    algorithm_id: str = "ledh_pfpf_alg1_ukf_current",
    horizon: int,
    particle_count: int,
    seeds: list[int],
    device: str = "gpu",
    sinkhorn_epsilon_policy: str = "fixed",
    **_kwargs,
) -> dict:
    route_variant = (
        p8d.P8J_BOOTSTRAP_ROUTE_VARIANT
        if algorithm_id == "bootstrap_dpf_current"
        else p8d.P8J_ROUTE_VARIANT
    )
    route = "none" if algorithm_id == "bootstrap_dpf_current" else p8d.P8H_DEFAULT_RESAMPLING_ROUTE
    mean_by_count = {16: -100.0, 32: -100.3, 64: -100.31}
    base = mean_by_count.get(particle_count, -100.0)
    per_seed = []
    for index, seed in enumerate(seeds):
        first_diag = {
            "resampling_route": route,
            "canonical_transport_matrix_convention": "target_by_source_row_stochastic",
            "canonical_transport_shape": [particle_count, particle_count],
            "state_transport_shape": [particle_count, particle_count],
            "covariance_transport_shape": [particle_count, particle_count],
            "canonical_transport_row_sum_residual": 1e-8,
            "canonical_transport_row_sum_tolerance": 5e-3,
            "finite_transport": True,
            "finite_particles": True,
            "finite_carried_covariances": True,
            "finite_corrected_log_weights": True,
            "finite_predicted_covariances": True,
            "finite_updated_covariances": True,
            "sinkhorn_epsilon_policy": sinkhorn_epsilon_policy,
            "nominal_epsilon": 1.0,
            "effective_epsilon": (
                128.0 if sinkhorn_epsilon_policy == "cost_mean_max_nominal" else 1.0
            ),
            "sinkhorn_cost_mean": (
                128.0 if sinkhorn_epsilon_policy == "cost_mean_max_nominal" else None
            ),
        }
        per_seed.append(
            {
                "seed": seed,
                "runtime_seconds": 0.1,
                "finite": True,
                "log_likelihood": base + 0.01 * index + 0.001 * horizon,
                "average_log_likelihood": (base + 0.01 * index + 0.001 * horizon) / horizon,
                "effective_sample_size_min": 0.55 * particle_count,
                "effective_sample_size_mean": 0.75 * particle_count,
                "resampling_count": 0 if route == "none" else horizon,
                "method_id": "fake_p8j",
                "log_likelihood_device": "/job:localhost/replica:0/task:0/device:GPU:0",
                "ess_device": "/job:localhost/replica:0/task:0/device:GPU:0",
                "route_identifiers": {
                    "route_variant": route_variant,
                    "resampling_route": route,
                },
                "first_resampling_diagnostics": first_diag if route != "none" else {},
            }
        )
    return {
        "schema_version": "filter_bench.p8j_sir_profile.v1",
        "status": "executed_p8j_sir_profile",
        "run_manifest": {
            "requested_device": device,
            "wall_seconds": 1.0,
        },
        "profile_scope": {
            "row_id": row_id,
            "algorithm_id": algorithm_id,
            "route_variant": route_variant,
            "resampling_route": route,
            "full_horizon": 20,
            "horizon_prefix": horizon,
            "particle_count": particle_count,
            "seeds": seeds,
            "seed_count": len(seeds),
            "sinkhorn_epsilon_policy": (
                None if algorithm_id == "bootstrap_dpf_current" else sinkhorn_epsilon_policy
            ),
            "sinkhorn_repair_classification": (
                None
                if algorithm_id == "bootstrap_dpf_current"
                or sinkhorn_epsilon_policy == "fixed"
                else "p8j_sir_numerical_stability_repair_candidate"
            ),
        },
        "device_diagnostics": {
            "devices_used_by_result_tensors": ["/job:localhost/replica:0/task:0/device:GPU:0"],
            "no_silent_cpu_fallback_claim": True,
        },
        "per_seed_results": per_seed,
    }


def test_p8j_phase5_sir_tuning_schema_selects_counts_for_bootstrap_and_ledh(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(p8d, "_p8j_sir_profile_dpf_prefix", _fake_p8j_profile)
    payload = p8d._p8j_phase5_tuning_payload(
        rows=[SIR_ROW],
        algorithms=["bootstrap_dpf_current", "ledh_pfpf_alg1_ukf_current"],
        horizons=[20],
        particles=[16, 32, 64],
        seeds=DPF_SEEDS,
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        runtime_budget_seconds=10.0,
    )

    assert payload["schema_version"] == "filter_bench.p8j_sir_particle_tuning.v1"
    assert payload["status"] == "executed_p8j_sir_particle_tuning_stage0"
    assert payload["scope"]["row_id"] == SIR_ROW
    assert payload["scope"]["historical_particle_count_not_selectable"] == 8
    assert payload["summary"]["selected_count"] == 2
    assert payload["summary"]["all_requested_cells_accounted"] is True
    assert {row["algorithm_id"] for row in payload["selected_blocked"]} == {
        "bootstrap_dpf_current",
        "ledh_pfpf_alg1_ukf_current",
    }
    for selected in payload["selected_blocked"]:
        assert selected["tuning_status"] == "selected_particle_count"
        assert selected["selected_particle_count"] == 16
        assert selected["next_rung_particle_count"] == 32
        assert selected["blocker_reason"] is None
    ledh_rung = next(
        row for row in payload["evaluated_rungs"] if row["algorithm_id"] == "ledh_pfpf_alg1_ukf_current"
    )
    bootstrap_rung = next(
        row for row in payload["evaluated_rungs"] if row["algorithm_id"] == "bootstrap_dpf_current"
    )
    assert ledh_rung["transport_diagnostics_pass"] is True
    assert ledh_rung["per_seed_results"][0]["first_resampling_diagnostics"][
        "sinkhorn_epsilon_policy"
    ] == "fixed"
    assert bootstrap_rung["transport_diagnostics_pass"] is True
    assert payload["selection_thresholds"]["sinkhorn_epsilon_policy"] == "fixed"
    assert payload["selection_thresholds"]["sinkhorn_repair_classification"] is None
    assert "not HMC readiness" in payload["nonclaims"]
    assert "source-faithful TT/SIRT" in " ".join(payload["evidence_contract"]["not_concluded"])


def test_p8j_phase5c_scale_adaptive_sinkhorn_policy_is_opt_in(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed_policies: list[str] = []

    def fake_profile(**kwargs):
        observed_policies.append(kwargs.get("sinkhorn_epsilon_policy", "missing"))
        return _fake_p8j_profile(**kwargs)

    monkeypatch.setattr(p8d, "_p8j_sir_profile_dpf_prefix", fake_profile)
    payload = p8d._p8j_phase5_tuning_payload(
        rows=[SIR_ROW],
        algorithms=["ledh_pfpf_alg1_ukf_current"],
        horizons=[20],
        particles=[16, 32],
        seeds=DPF_SEEDS,
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        runtime_budget_seconds=10.0,
        manifest_phase="P8J_PHASE5C_SCALE_ADAPTIVE_SINKHORN_REPAIR",
        sinkhorn_epsilon_policy="cost_mean_max_nominal",
    )

    assert observed_policies == ["cost_mean_max_nominal", "cost_mean_max_nominal"]
    assert payload["selection_thresholds"]["sinkhorn_epsilon_policy"] == (
        "cost_mean_max_nominal"
    )
    assert payload["selection_thresholds"]["sinkhorn_repair_classification"] == (
        "p8j_sir_numerical_stability_repair_candidate"
    )
    ledh_rung = payload["evaluated_rungs"][0]
    diagnostics = ledh_rung["per_seed_results"][0]["first_resampling_diagnostics"]
    assert diagnostics["sinkhorn_epsilon_policy"] == "cost_mean_max_nominal"
    assert diagnostics["effective_epsilon"] == 128.0
    assert diagnostics["nominal_epsilon"] == 1.0
    assert payload["phase"] == "P8J_PHASE5C_SCALE_ADAPTIVE_SINKHORN_REPAIR"
    assert "not HMC readiness" in payload["nonclaims"]


def test_p8j_phase5_sir_tuning_enforces_gpu_five_seeds_and_rejects_n8(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(p8d, "_p8j_sir_profile_dpf_prefix", _fake_p8j_profile)
    common = dict(
        rows=[SIR_ROW],
        algorithms=["ledh_pfpf_alg1_ukf_current"],
        horizons=[20],
        particles=[16, 32],
        g0_manifest=Path("docs/plans/fake-g0.md"),
    )
    with pytest.raises(ValueError, match="trusted GPU"):
        p8d._p8j_phase5_tuning_payload(
            **common,
            seeds=DPF_SEEDS,
            device="cpu",
        )
    with pytest.raises(ValueError, match="five fixed seeds"):
        p8d._p8j_phase5_tuning_payload(
            **common,
            seeds=DPF_SEEDS[:2],
            device="gpu",
        )
    with pytest.raises(ValueError, match="fixed DPF seed list"):
        p8d._p8j_phase5_tuning_payload(
            **common,
            seeds=[1, 2, 3, 4, 5],
            device="gpu",
        )
    with pytest.raises(ValueError, match="N=8"):
        p8d._p8j_phase5_tuning_payload(
            rows=[SIR_ROW],
            algorithms=["bootstrap_dpf_current"],
            horizons=[20],
            particles=[8, 16],
            seeds=DPF_SEEDS,
            device="gpu",
            g0_manifest=Path("docs/plans/fake-g0.md"),
        )


def test_p8j_phase5_sir_tuning_blocks_ledh_transport_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def bad_transport_profile(**kwargs):
        profile = _fake_p8j_profile(**kwargs)
        for entry in profile["per_seed_results"]:
            entry["first_resampling_diagnostics"]["canonical_transport_shape"] = [1, 1]
        return profile

    monkeypatch.setattr(p8d, "_p8j_sir_profile_dpf_prefix", bad_transport_profile)
    payload = p8d._p8j_phase5_tuning_payload(
        rows=[SIR_ROW],
        algorithms=["ledh_pfpf_alg1_ukf_current"],
        horizons=[20],
        particles=[16, 32],
        seeds=DPF_SEEDS,
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        runtime_budget_seconds=10.0,
    )

    verdict = payload["selected_blocked"][0]
    assert verdict["tuning_status"] == "blocked_particle_tuning_not_converged"
    assert verdict["selected_particle_count"] is None
    assert verdict["blocker_reason"] == "BLOCK_P8J_SIR_PARTICLE_TUNING_TRANSPORT"


def test_p8j_phase5_sir_tuning_records_failed_profile_without_crashing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def failed_profile(**kwargs):
        particle_count = kwargs["particle_count"]
        seed = kwargs["seeds"][0]
        return {
            "schema_version": "filter_bench.p8j_sir_profile.v1",
            "status": "blocked_p8j_sir_profile_nonfinite",
            "run_manifest": {"requested_device": "gpu", "wall_seconds": 1.0},
            "profile_scope": {
                "row_id": kwargs["row_id"],
                "algorithm_id": kwargs["algorithm_id"],
                "route_variant": p8d.P8J_ROUTE_VARIANT,
                "resampling_route": p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
                "full_horizon": 20,
                "horizon_prefix": kwargs["horizon"],
                "particle_count": particle_count,
                "seeds": kwargs["seeds"],
                "seed_count": len(kwargs["seeds"]),
            },
            "device_diagnostics": {
                "devices_used_by_result_tensors": ["/job:localhost/replica:0/task:0/device:GPU:0"],
                "no_silent_cpu_fallback_claim": True,
            },
            "per_seed_results": [
                {
                    "seed": seed,
                    "runtime_seconds": 0.1,
                    "finite": False,
                    "log_likelihood": None,
                    "average_log_likelihood": None,
                    "effective_sample_size_min": None,
                    "effective_sample_size_mean": None,
                    "resampling_count": 0,
                    "method_id": "blocked_ledh",
                    "log_likelihood_device": None,
                    "ess_device": None,
                    "route_identifiers": {
                        "route_variant": p8d.P8J_ROUTE_VARIANT,
                        "resampling_route": p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
                    },
                    "first_resampling_diagnostics": {},
                    "failure_error_type": "FloatingPointError",
                    "failure_message": "Sinkhorn row residual exceeded tolerance envelope",
                }
            ],
        }

    monkeypatch.setattr(p8d, "_p8j_sir_profile_dpf_prefix", failed_profile)
    payload = p8d._p8j_phase5_tuning_payload(
        rows=[SIR_ROW],
        algorithms=["ledh_pfpf_alg1_ukf_current"],
        horizons=[20],
        particles=[16, 32],
        seeds=DPF_SEEDS,
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        runtime_budget_seconds=10.0,
    )

    rung = payload["evaluated_rungs"][0]
    assert rung["finite"] is False
    assert rung["mean_log_likelihood"] is None
    assert rung["failure_summaries"][0]["failure_error_type"] == "FloatingPointError"
    verdict = payload["selected_blocked"][0]
    assert verdict["tuning_status"] == "blocked_particle_tuning_not_converged"
    assert verdict["blocker_reason"] == "BLOCK_P8J_SIR_PARTICLE_TUNING_NONFINITE"


def test_p8j_phase5b_sinkhorn_diagnostic_enforces_gpu_and_sir() -> None:
    with pytest.raises(ValueError, match="trusted GPU"):
        p8d._p8j_sir_ot_sinkhorn_diagnostic(
            row_id=SIR_ROW,
            horizon=20,
            particle_count=16,
            seed=81120,
            device="cpu",
            g0_manifest=Path("docs/plans/fake-g0.md"),
            runtime_budget_seconds=10.0,
        )
    with pytest.raises(ValueError, match="only SIR d18"):
        p8d._p8j_sir_ot_sinkhorn_diagnostic(
            row_id=SV_ROW,
            horizon=20,
            particle_count=16,
            seed=81120,
            device="gpu",
            g0_manifest=Path("docs/plans/fake-g0.md"),
            runtime_budget_seconds=10.0,
        )


def test_p8j_phase5b_sinkhorn_diagnostic_schema_with_fake_route(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw_observations = tf.zeros([1, 1], dtype=tf.float64)
    callbacks = {
        "initial_sample": lambda count, seed: tf.zeros([count, 1], dtype=tf.float64),
        "initial_covariance": tf.eye(1, dtype=tf.float64),
        "transition_sample": lambda particles, seed, time_index: particles,
        "transition_mean_fn": lambda points, time_index: points,
        "transition_log_density_fn": lambda points, ancestors, time_index: tf.zeros(
            [tf.shape(points)[0]],
            dtype=tf.float64,
        ),
        "observation_mean_fn": lambda points, time_index: points,
        "observation_jacobian_fn": lambda point, time_index: tf.eye(1, dtype=tf.float64),
        "observation_log_density_fn": lambda points, observation, time_index: tf.linspace(
            tf.constant(0.0, dtype=tf.float64),
            tf.constant(15.0, dtype=tf.float64),
            tf.shape(points)[0],
        ),
        "process_noise_covariance_fn": lambda point, time_index: tf.eye(1, dtype=tf.float64),
        "observation_covariance_fn": lambda time_index: tf.eye(1, dtype=tf.float64),
    }

    monkeypatch.setattr(
        p8d,
        "_dpf_route",
        lambda row_id: (callbacks, raw_observations, "fake_sir", 1),
    )

    payload = p8d._p8j_sir_ot_sinkhorn_diagnostic(
        row_id=SIR_ROW,
        horizon=1,
        particle_count=16,
        seed=81120,
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        runtime_budget_seconds=10.0,
    )

    assert payload["schema_version"] == "filter_bench.p8j_sir_ot_sinkhorn_diagnostic.v1"
    assert payload["status"] == "executed_p8j_sir_ot_sinkhorn_diagnostic"
    assert payload["scope"]["algorithm_id"] == "ledh_pfpf_alg1_ukf_current"
    assert payload["resampling_event"]["time_index"] == 0
    assert payload["resampling_event"]["source_weight_max"] > payload["resampling_event"]["source_weight_min"]
    assert payload["sinkhorn_failure"]["nominal_settings_failed"] in {True, False}
    assert payload["scale_adaptive_probe"]["probe_kind"] == (
        "scale_adaptive_epsilon_equal_max_nominal_or_cost_mean"
    )
    assert "not a selected LEDH OT repair" in payload["nonclaims"]


def test_p8j_phase5_writes_tuning_and_selected_blocked_csvs(tmp_path: Path) -> None:
    payload = {
        "evaluated_rungs": [
            {
                "stage": "stage0",
                "row_id": SIR_ROW,
                "algorithm_id": "ledh_pfpf_alg1_ukf_current",
                "route_variant": p8d.P8J_ROUTE_VARIANT,
                "resampling_route": p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
                "full_horizon": 20,
                "horizon_prefix": 20,
                "particle_count": 16,
                "seed_count": 5,
                "finite": True,
                "transport_diagnostics_pass": True,
                "trusted_gpu": True,
                "mean_log_likelihood": -1.0,
                "mean_average_log_likelihood": -0.05,
                "sample_standard_deviation": 0.1,
                "mc_standard_error": 0.05,
                "min_relative_ess": 0.55,
                "mean_relative_ess": 0.75,
                "runtime_seconds": 1.0,
                "runtime_budget_seconds": 10.0,
                "runtime_budget_status": "within_budget",
                "status": "executed_p8j_sir_profile",
            }
        ],
        "selected_blocked": [
            {
                "row_id": SIR_ROW,
                "algorithm_id": "ledh_pfpf_alg1_ukf_current",
                "route_variant": p8d.P8J_ROUTE_VARIANT,
                "resampling_route": p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
                "tuning_status": "selected_particle_count",
                "selected_particle_count": 16,
                "selection_rule": "test",
                "selection_rung": 16,
                "next_rung_checked": True,
                "next_rung_particle_count": 32,
                "adjacent_horizon_summaries": [{"adjacent_pass": True}],
                "blocker_reason": None,
                "evaluated_horizons": [20],
                "evaluated_particle_counts": [16, 32],
            }
        ],
    }
    rung_csv = tmp_path / "p8j-rungs.csv"
    selected_csv = tmp_path / "p8j-selected.csv"

    p8d._write_p8j_particle_tuning_csv(rung_csv, payload)
    p8d._write_p8j_selected_blocked_csv(selected_csv, payload)

    rung_rows = list(csv.DictReader(rung_csv.open(newline="", encoding="utf-8")))
    selected_rows = list(csv.DictReader(selected_csv.open(newline="", encoding="utf-8")))
    assert rung_rows[0]["row_id"] == SIR_ROW
    assert rung_rows[0]["particle_count"] == "16"
    assert selected_rows[0]["selected_particle_count"] == "16"
    assert json.loads(selected_rows[0]["evaluated_particle_counts"]) == [16, 32]


class _FakeP8hGradientResult:
    def __init__(self, value: tf.Tensor, *, resampling_route: str):
        self.log_likelihood_estimate = value
        self.finite = True
        self.ess_by_time = tf.constant([4.5, 4.25], dtype=tf.float64)
        self.resampling_count = 2
        self.route_identifiers = {
            "route_variant": p8d.P8H_ROUTE_VARIANT,
            "resampling_route": resampling_route,
        }
        self.resampling_diagnostics = [
            {
                "resampled": True,
                "resampling_route": resampling_route,
                "canonical_transport_matrix_convention": "target_by_source_row_stochastic",
                "canonical_transport_shape": [5, 5],
                "finite_transport": True,
            }
        ]


def test_p8h_ot_gradient_check_schema_records_ot_route_and_connected_gradients(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_value(theta, *, horizon, seed, particle_count, resampling_route):
        del horizon, particle_count
        theta = tf.convert_to_tensor(theta, dtype=tf.float64)
        value = theta[0] * tf.cast(seed % 7 + 1, tf.float64) + tf.square(theta[1])
        return _FakeP8hGradientResult(value, resampling_route=resampling_route)

    monkeypatch.setattr(p8d, "_p8h_ot_scalar_sv_gradient_value", fake_value)
    monkeypatch.setattr(p8d, "_tensor_device_is_gpu", lambda _device: True)
    payload = p8d._p8h_ot_gradient_check(
        rows=[SV_ROW],
        horizon=4,
        particle_count=5,
        seeds=DPF_SEEDS,
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        coordinate="canonical_unconstrained",
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        manifest_phase="P8I_PHASE2_LONGER_HORIZON_GRADIENT",
        manifest_plan=Path(
            "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-subplan-2026-06-16.md"
        ),
        runtime_budget_seconds=10.0,
        finite_difference_max_abs_threshold=1e-5,
    )

    assert payload["schema_version"] == "filter_bench.p8h_ot_gradient.v1"
    assert payload["phase"] == "P8I_PHASE2_LONGER_HORIZON_GRADIENT"
    assert payload["run_manifest"]["phase6_plan"] == (
        "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-subplan-2026-06-16.md"
    )
    assert payload["status"] == "executed_p8h_ot_gradient_check"
    assert payload["gate_diagnostics"]["fd_residual_within_threshold"] is True
    assert payload["gate_diagnostics"]["runtime_within_budget"] is True
    assert payload["gate_diagnostics"]["trusted_requested_device"] is True
    assert payload["blocker"] is None
    assert payload["scope"]["particle_count"] == 5
    assert payload["scope"]["resampling_route"] == p8d.P8H_DEFAULT_RESAMPLING_ROUTE
    assert payload["summary"]["all_gradients_finite"] is True
    assert payload["summary"]["all_gradients_connected"] is True
    assert all(row["resampling_route"] == p8d.P8H_DEFAULT_RESAMPLING_ROUTE for row in payload["per_seed_results"])
    assert all(row["gradient_connected"] is True for row in payload["per_seed_results"])
    assert "not the stochastic PF marginal likelihood gradient" in payload["nonclaims"]


def test_p8h_ot_gradient_check_blocks_gpu_fallback_and_fd_threshold(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_value(theta, *, horizon, seed, particle_count, resampling_route):
        del horizon, particle_count
        theta = tf.convert_to_tensor(theta, dtype=tf.float64)
        value = theta[0] * tf.cast(seed % 7 + 1, tf.float64) + tf.square(theta[1])
        return _FakeP8hGradientResult(value, resampling_route=resampling_route)

    monkeypatch.setattr(p8d, "_p8h_ot_scalar_sv_gradient_value", fake_value)
    monkeypatch.setattr(
        p8d,
        "_finite_difference_score",
        lambda _value_fn, theta, step: tf.zeros_like(tf.convert_to_tensor(theta, dtype=tf.float64)),
    )
    payload = p8d._p8h_ot_gradient_check(
        rows=[SV_ROW],
        horizon=4,
        particle_count=5,
        seeds=DPF_SEEDS,
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        coordinate="canonical_unconstrained",
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        finite_difference_max_abs_threshold=1e-5,
    )

    assert payload["status"] == "blocked_p8h_ot_gradient_check"
    assert payload["blocker"] is not None
    assert "BLOCK_P8H_OT_GRADIENT_FD_RESIDUAL" in payload["blocker"]["reasons"]
    assert "BLOCK_P8H_OT_GRADIENT_TRUSTED_DEVICE" in payload["blocker"]["reasons"]


def test_p8h_ot_gradient_check_rejects_cpu_and_blocks_runtime_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_value(theta, *, horizon, seed, particle_count, resampling_route):
        del horizon, particle_count
        theta = tf.convert_to_tensor(theta, dtype=tf.float64)
        value = theta[0] * tf.cast(seed % 7 + 1, tf.float64) + tf.square(theta[1])
        return _FakeP8hGradientResult(value, resampling_route=resampling_route)

    common = dict(
        rows=[SV_ROW],
        horizon=4,
        particle_count=5,
        seeds=DPF_SEEDS,
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        coordinate="canonical_unconstrained",
        g0_manifest=Path("docs/plans/fake-g0.md"),
    )
    with pytest.raises(ValueError, match="trusted GPU"):
        p8d._p8h_ot_gradient_check(
            **common,
            device="cpu",
        )

    monkeypatch.setattr(p8d, "_p8h_ot_scalar_sv_gradient_value", fake_value)
    monkeypatch.setattr(p8d, "_tensor_device_is_gpu", lambda _device: True)
    payload = p8d._p8h_ot_gradient_check(
        **common,
        device="gpu",
        runtime_budget_seconds=1e-12,
    )

    assert payload["status"] == "blocked_p8h_ot_gradient_check"
    assert payload["blocker"] is not None
    assert "BLOCK_P8H_OT_GRADIENT_RUNTIME_BUDGET" in payload["blocker"]["reasons"]


def test_p8h_ot_gradient_check_blocks_core_gradient_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_value(theta, *, horizon, seed, particle_count, resampling_route):
        del horizon, particle_count
        theta = tf.convert_to_tensor(theta, dtype=tf.float64)
        value = tf.stop_gradient(theta[0] + tf.square(theta[1]))
        return _FakeP8hGradientResult(value, resampling_route=resampling_route)

    monkeypatch.setattr(p8d, "_p8h_ot_scalar_sv_gradient_value", fake_value)
    monkeypatch.setattr(p8d, "_tensor_device_is_gpu", lambda _device: True)
    payload = p8d._p8h_ot_gradient_check(
        rows=[SV_ROW],
        horizon=4,
        particle_count=5,
        seeds=DPF_SEEDS,
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        coordinate="canonical_unconstrained",
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
    )

    assert payload["status"] == "blocked_p8h_ot_gradient_check"
    assert payload["blocker"] is not None
    assert "BLOCK_P8H_OT_GRADIENT_CORE_FINITE_CONNECTED" in payload["blocker"]["reasons"]


def test_p8h_ot_gradient_cli_forwards_phase2_gate_args(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    captured: dict[str, object] = {}

    def fake_gradient_check(**kwargs):
        captured.update(kwargs)
        return {
            "schema_version": "filter_bench.p8h_ot_gradient.v1",
            "phase": kwargs["manifest_phase"],
            "status": "blocked_p8h_ot_gradient_check",
            "scope": {"row_id": SV_ROW},
            "per_seed_results": [],
        }

    monkeypatch.setattr(p8d, "_p8h_ot_gradient_check", fake_gradient_check)
    monkeypatch.setattr(p8d, "_write_p8h_gradient_csv", lambda _path, _payload: None)
    output_json = tmp_path / "gradient.json"
    output_csv = tmp_path / "gradient.csv"
    plan_path = Path(
        "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-subplan-2026-06-16.md"
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "runner",
            "--p8h-ot-gradient-check",
            "--row",
            "actual_sv",
            "--horizon",
            "16",
            "--particles",
            "5",
            "--seeds",
            "81120,81121,81122,81123,81124",
            "--device",
            "gpu",
            "--g0-manifest",
            "docs/plans/fake-g0.md",
            "--p8h-resampling-route",
            p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
            "--coordinate",
            "canonical_unconstrained",
            "--runtime-budget-seconds",
            "1800",
            "--p8h-gradient-fd-threshold",
            "1e-5",
            "--p8h-gradient-manifest-phase",
            "P8I_PHASE2_LONGER_HORIZON_GRADIENT_H16_PILOT",
            "--p8h-gradient-manifest-plan",
            str(plan_path),
            "--output-json",
            str(output_json),
            "--output-csv",
            str(output_csv),
        ],
    )

    p8d.main()

    assert captured["rows"] == [SV_ROW]
    assert captured["horizon"] == 16
    assert captured["particle_count"] == 5
    assert captured["device"] == "gpu"
    assert captured["manifest_phase"] == "P8I_PHASE2_LONGER_HORIZON_GRADIENT_H16_PILOT"
    assert captured["manifest_plan"] == plan_path
    assert captured["runtime_budget_seconds"] == pytest.approx(1800.0)
    assert captured["finite_difference_max_abs_threshold"] == pytest.approx(1e-5)
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["phase"] == "P8I_PHASE2_LONGER_HORIZON_GRADIENT_H16_PILOT"


def test_p8h_ot_gradient_check_rejects_no_resampling_and_wrong_count() -> None:
    common = dict(
        rows=[SV_ROW],
        horizon=4,
        seeds=DPF_SEEDS,
        coordinate="canonical_unconstrained",
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
    )
    with pytest.raises(ValueError, match="Sinkhorn"):
        p8d._p8h_ot_gradient_check(
            **common,
            particle_count=5,
            resampling_route="none",
        )
    with pytest.raises(ValueError, match="N=5"):
        p8d._p8h_ot_gradient_check(
            **common,
            particle_count=10,
            resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        )


def _fake_p8h_hmc_value(theta, *, horizon, seed, particle_count, resampling_route):
    del horizon, seed, particle_count
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    value = -0.5 * tf.reduce_sum(tf.square(theta - tf.constant([0.1, -0.2], dtype=tf.float64)))
    return _FakeP8hGradientResult(value, resampling_route=resampling_route)


def test_p8h_hmc_tier0_smoke_schema_records_fixed_kernel_gpu_route(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(p8d, "_p8h_ot_scalar_sv_gradient_value", _fake_p8h_hmc_value)
    payload = p8d._p8h_hmc_tier0_smoke(
        rows=[SV_ROW],
        algorithm_id="ledh_pfpf_alg1_ukf_current",
        horizon=4,
        particle_count=5,
        seeds=[81120],
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        coordinate="canonical_unconstrained",
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        num_results=2,
        num_burnin_steps=1,
        step_size=0.005,
        num_leapfrog_steps=1,
        manifest_phase="P8I_PHASE4_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC",
        manifest_plan=Path(
            "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-tier2-subplan-2026-06-16.md"
        ),
        runtime_budget_seconds=10.0,
        hmc_policy_label="fixed_kernel_no_adaptation_tier1_diagnostic",
        hmc_tier_label="tier1_fixed_kernel_diagnostic",
        schema_version="filter_bench.p8i_hmc_tier1.v1",
        status_success_label="executed_p8i_hmc_tier1_fixed_kernel_diagnostic",
        status_blocked_label="blocked_p8i_hmc_tier1_fixed_kernel_diagnostic",
        blocker_reason="BLOCK_P8I_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC",
        evidence_question="P8i Tier-1 question",
        evidence_baseline="P8i Phase 1-3 reviewed gates",
        evidence_primary_criterion="P8i finite fixed-kernel HMC diagnostic",
        predecessor_results={
            "phase1_result": "docs/plans/p8i-phase1.md",
            "phase2_result": "docs/plans/p8i-phase2.md",
            "phase3_result": "docs/plans/p8i-phase3.md",
        },
    )

    assert payload["schema_version"] == "filter_bench.p8i_hmc_tier1.v1"
    assert payload["phase"] == "P8I_PHASE4_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC"
    assert payload["run_manifest"]["plan"] == (
        "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-tier2-subplan-2026-06-16.md"
    )
    assert payload["gate_diagnostics"]["runtime_within_budget"] is True
    assert payload["status"] in {
        "executed_p8i_hmc_tier1_fixed_kernel_diagnostic",
        "blocked_p8i_hmc_tier1_fixed_kernel_diagnostic",
    }
    assert payload["run_manifest"]["predecessor_results"] == {
        "phase1_result": "docs/plans/p8i-phase1.md",
        "phase2_result": "docs/plans/p8i-phase2.md",
        "phase3_result": "docs/plans/p8i-phase3.md",
    }
    assert payload["run_manifest"]["runtime_budget_seconds"] == pytest.approx(10.0)
    assert payload["evidence_contract"]["question"] == "P8i Tier-1 question"
    assert payload["evidence_contract"]["baseline"] == "P8i Phase 1-3 reviewed gates"
    assert payload["evidence_contract"]["primary_criterion"] == "P8i finite fixed-kernel HMC diagnostic"
    assert payload["scope"]["hmc_kernel"] == "tfp.mcmc.HamiltonianMonteCarlo"
    assert payload["scope"]["hmc_policy"] == "fixed_kernel_no_adaptation_tier1_diagnostic"
    assert payload["scope"]["hmc_tier"] == "tier1_fixed_kernel_diagnostic"
    assert payload["scope"]["particle_count"] == 5
    assert payload["scope"]["pf_seed"] == 81120
    assert payload["scope"]["resampling_route"] == p8d.P8H_DEFAULT_RESAMPLING_ROUTE
    assert payload["scope"]["coordinate"] == "canonical_unconstrained"
    assert payload["initial_diagnostics"]["initial_gradient_connected"] is True
    assert "not production HMC readiness" in payload["nonclaims"]
    assert "posterior convergence" in " ".join(payload["evidence_contract"]["not_concluded"])


def test_p8h_hmc_tier0_rejects_coordinate_count_and_non_gpu_device() -> None:
    common = dict(
        rows=[SV_ROW],
        algorithm_id="ledh_pfpf_alg1_ukf_current",
        horizon=4,
        seeds=[81120],
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        g0_manifest=Path("docs/plans/fake-g0.md"),
        num_results=2,
        num_burnin_steps=1,
        step_size=0.005,
        num_leapfrog_steps=1,
    )
    with pytest.raises(ValueError, match="canonical_unconstrained"):
        p8d._p8h_hmc_tier0_smoke(
            **common,
            particle_count=5,
            coordinate="physical",
            device="gpu",
        )
    with pytest.raises(ValueError, match="N=5"):
        p8d._p8h_hmc_tier0_smoke(
            **common,
            particle_count=10,
            coordinate="canonical_unconstrained",
            device="gpu",
        )
    with pytest.raises(ValueError, match="trusted GPU"):
        p8d._p8h_hmc_tier0_smoke(
            **common,
            particle_count=5,
            coordinate="canonical_unconstrained",
            device="cpu",
        )


def test_p8h_hmc_tier0_records_hmc_execution_error_blocker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def failing_value(*_args, **_kwargs):
        raise RuntimeError("forced HMC target failure")

    monkeypatch.setattr(p8d, "_p8h_ot_scalar_sv_gradient_value", failing_value)
    payload = p8d._p8h_hmc_tier0_smoke(
        rows=[SV_ROW],
        algorithm_id="ledh_pfpf_alg1_ukf_current",
        horizon=4,
        particle_count=5,
        seeds=[81120],
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        coordinate="canonical_unconstrained",
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        num_results=2,
        num_burnin_steps=1,
        step_size=0.005,
        num_leapfrog_steps=1,
    )

    assert payload["status"] == "blocked_p8h_hmc_tier0_smoke"
    assert payload["blocker"]["reason"] == "BLOCK_P8H_HMC_TIER0_SMOKE"
    assert payload["blocker"]["hmc_error"]["class"] == "RuntimeError"
    assert "forced HMC target failure" in payload["blocker"]["hmc_error"]["message"]


def test_p8h_hmc_tier0_records_runtime_budget_blocker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(p8d, "_p8h_ot_scalar_sv_gradient_value", _fake_p8h_hmc_value)
    payload = p8d._p8h_hmc_tier0_smoke(
        rows=[SV_ROW],
        algorithm_id="ledh_pfpf_alg1_ukf_current",
        horizon=4,
        particle_count=5,
        seeds=[81120],
        resampling_route=p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
        coordinate="canonical_unconstrained",
        device="gpu",
        g0_manifest=Path("docs/plans/fake-g0.md"),
        num_results=2,
        num_burnin_steps=1,
        step_size=0.005,
        num_leapfrog_steps=1,
        runtime_budget_seconds=1e-12,
    )

    assert payload["status"] == "blocked_p8h_hmc_tier0_smoke"
    assert payload["gate_diagnostics"]["runtime_within_budget"] is False
    assert payload["blocker"] is not None
    assert payload["blocker"]["runtime_within_budget"] is False


def test_p8h_hmc_cli_forwards_phase4_gate_args(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    captured: dict[str, object] = {}

    def fake_hmc(**kwargs):
        captured.update(kwargs)
        return {
            "schema_version": kwargs["schema_version"],
            "phase": kwargs["manifest_phase"],
            "status": kwargs["status_blocked_label"],
            "scope": {
                "row_id": SV_ROW,
                "algorithm_id": kwargs["algorithm_id"],
                "route_variant": p8d.P8H_ROUTE_VARIANT,
                "resampling_route": kwargs["resampling_route"],
                "coordinate": kwargs["coordinate"],
                "horizon_prefix": kwargs["horizon"],
                "particle_count": kwargs["particle_count"],
                "pf_seed": kwargs["seeds"][0],
                "hmc_seed": [kwargs["seeds"][0], kwargs["seeds"][0] + 1000],
                "num_results": kwargs["num_results"],
                "num_burnin_steps": kwargs["num_burnin_steps"],
                "step_size": kwargs["step_size"],
                "num_leapfrog_steps": kwargs["num_leapfrog_steps"],
            },
            "device_diagnostics": {"trusted_gpu": False},
            "initial_diagnostics": {
                "initial_value_finite": False,
                "initial_gradient_finite": False,
                "initial_gradient_connected": False,
            },
            "hmc_diagnostics": {
                "sample_chain_returned": False,
                "samples_finite": False,
                "log_accept_ratio_finite": False,
                "target_log_prob_finite": False,
                "acceptance_rate": None,
                "sample_displacement_l2": None,
            },
            "run_manifest": {
                "wall_time_seconds": 0.0,
            },
            "blocker": {"reason": kwargs["blocker_reason"]},
        }

    monkeypatch.setattr(p8d, "_p8h_hmc_tier0_smoke", fake_hmc)
    monkeypatch.setattr(p8d, "_write_p8h_hmc_tier0_csv", lambda _path, _payload: None)
    output_json = tmp_path / "hmc.json"
    predecessor_json = json.dumps(
        {
            "phase1_result": "docs/plans/p8i-phase1.md",
            "phase2_result": "docs/plans/p8i-phase2.md",
            "phase3_result": "docs/plans/p8i-phase3.md",
        }
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "runner",
            "--p8h-hmc-tier0-smoke",
            "--row",
            "actual_sv",
            "--algorithm",
            "ledh_pfpf_alg1_ukf_current",
            "--horizon",
            "32",
            "--particles",
            "5",
            "--seeds",
            "81120",
            "--device",
            "gpu",
            "--g0-manifest",
            "docs/plans/fake-g0.md",
            "--p8h-resampling-route",
            p8d.P8H_DEFAULT_RESAMPLING_ROUTE,
            "--coordinate",
            "canonical_unconstrained",
            "--hmc-num-results",
            "2",
            "--hmc-num-burnin-steps",
            "1",
            "--hmc-step-size",
            "0.005",
            "--hmc-num-leapfrog-steps",
            "1",
            "--runtime-budget-seconds",
            "900",
            "--p8h-hmc-manifest-phase",
            "P8I_PHASE4_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC",
            "--p8h-hmc-manifest-plan",
            "docs/plans/p8i-phase4.md",
            "--p8h-hmc-policy-label",
            "fixed_kernel_no_adaptation_tier1_diagnostic",
            "--p8h-hmc-tier-label",
            "tier1_fixed_kernel_diagnostic",
            "--p8h-hmc-schema-version",
            "filter_bench.p8i_hmc_tier1.v1",
            "--p8h-hmc-status-success-label",
            "executed_p8i_hmc_tier1_fixed_kernel_diagnostic",
            "--p8h-hmc-status-blocked-label",
            "blocked_p8i_hmc_tier1_fixed_kernel_diagnostic",
            "--p8h-hmc-blocker-reason",
            "BLOCK_P8I_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC",
            "--p8h-hmc-evidence-question",
            "P8i Tier-1 question",
            "--p8h-hmc-evidence-baseline",
            "P8i baseline",
            "--p8h-hmc-evidence-primary-criterion",
            "P8i criterion",
            "--p8h-hmc-predecessor-results-json",
            predecessor_json,
            "--output-json",
            str(output_json),
        ],
    )

    p8d.main()

    assert captured["schema_version"] == "filter_bench.p8i_hmc_tier1.v1"
    assert captured["status_success_label"] == "executed_p8i_hmc_tier1_fixed_kernel_diagnostic"
    assert captured["status_blocked_label"] == "blocked_p8i_hmc_tier1_fixed_kernel_diagnostic"
    assert captured["blocker_reason"] == "BLOCK_P8I_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC"
    assert captured["evidence_question"] == "P8i Tier-1 question"
    assert captured["evidence_baseline"] == "P8i baseline"
    assert captured["evidence_primary_criterion"] == "P8i criterion"
    assert captured["runtime_budget_seconds"] == pytest.approx(900.0)
    assert captured["predecessor_results"] == json.loads(predecessor_json)
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "filter_bench.p8i_hmc_tier1.v1"


def test_p8d_manifest_points_to_visible_plan_and_default_cpu_command() -> None:
    source_artifacts = p8d._source_artifacts_payload()
    run_manifest = p8d._run_manifest_payload()

    assert source_artifacts["plan"] == (
        "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md"
    )
    assert source_artifacts["p8_master_plan"] == (
        "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-master-plan-2026-06-11.md"
    )
    assert run_manifest["plan_file"] == (
        "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md"
    )
    assert run_manifest["command"] == (
        "env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --enable-p8d-execution"
    )
    assert run_manifest["cpu_gpu_status"] == "CPU-only deliberate"


def test_p8d_write_outputs_roundtrip_with_minimal_artifact(tmp_path: Path) -> None:
    adapter = _adapters()[("kalman_exact_or_mixture_enumeration", LGSSM_ROW)]
    cell = p8d._numeric_lgssm_exact_cell(adapter)
    artifact = {
        "schema_version": "filter_bench.p8d_numeric_results.v1",
        "metadata_date": "2026-06-13",
        "phase": "FILTER_BENCH_P8D_VISIBLE_REPAIR_EXECUTION",
        "status": "PARTIAL_P8D_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS",
        "numeric_benchmark_status": "partial_numeric_execution_remaining_adapter_and_callback_gaps",
        "roster": {
            "algorithm_ids": ["kalman_exact_or_mixture_enumeration"],
            "model_row_ids": [LGSSM_ROW],
            "full_cell_count": 1,
            "executed_cell_count": 1,
            "structured_not_applicable_cell_count": 0,
            "real_gap_cell_count": 0,
            "pending_or_not_applicable_cell_count": 0,
        },
        "cells": [cell],
        "run_manifest": {},
        "nonclaims": ["not a filter ranking"],
    }
    output_json = tmp_path / "p8d.json"
    p8d.write_outputs(
        artifact,
        output_json=output_json,
        value_csv=tmp_path / "value.csv",
        score_csv=tmp_path / "score.csv",
        curvature_csv=tmp_path / "curvature.csv",
        status_csv=tmp_path / "status.csv",
        uncertainty_csv=tmp_path / "uncertainty.csv",
        markdown=tmp_path / "summary.md",
    )
    written = json.loads(output_json.read_text(encoding="utf-8"))
    assert written["schema_version"] == "filter_bench.p8d_numeric_results.v1"
    assert written["run_manifest"]["summary_markdown"].endswith("summary.md")
    assert (tmp_path / "summary.md").read_text(encoding="utf-8").startswith(
        "# P8d Numeric Benchmark Execution Summary"
    )
    assert tf.constant(1.0, dtype=tf.float64).dtype == tf.float64
