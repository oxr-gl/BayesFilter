from __future__ import annotations

import importlib.util
from pathlib import Path

import tensorflow as tf


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py"
DTYPE = tf.float64


def _load_module():
    spec = importlib.util.spec_from_file_location("phase2_generalized_sv_leaderboard", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load highdim leaderboard module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generalized_sv_source_row_uses_generated_t1008_target_and_theta_coordinate() -> None:
    module = _load_module()
    theta = module._generalized_sv_theta()
    observations = module._generalized_sv_observations()
    model = module.highdim.GeneralizedSVPriorMeanSSM()
    physical = model.physical_parameters(theta)

    assert observations.shape == (1008, 1)
    assert theta.shape == (3,)
    assert module._generalized_sv_prior_mean_dataset(81105)["truth_theta_coordinate"] == (
        "source_route_active_transformed_prior_mean"
    )
    tf.debugging.assert_near(physical["gamma"], tf.constant(2.0 * 20.0 / 21.5 - 1.0, dtype=DTYPE))
    tf.debugging.assert_near(physical["tau"], tf.sqrt(tf.constant(0.005 * 3.141592653589793, dtype=DTYPE)))
    tf.debugging.assert_near(physical["mu"], tf.constant(0.0, dtype=DTYPE))


def test_generalized_sv_manual_local_density_scores_match_diagnostic_tape() -> None:
    module = _load_module()
    model = module.highdim.GeneralizedSVPriorMeanSSM()
    theta = module._generalized_sv_theta()
    previous = tf.constant([[-1.0], [0.25], [1.2]], dtype=DTYPE)
    current = tf.constant([[-0.7], [0.1], [1.0]], dtype=DTYPE)
    observation = tf.constant([0.2], dtype=DTYPE)

    with tf.GradientTape() as tape:
        tape.watch(theta)
        initial_values = model.initial_log_density(theta, previous)
    expected_initial = tape.jacobian(initial_values, theta)

    with tf.GradientTape() as tape:
        tape.watch(theta)
        transition_values = model.transition_log_density(theta, previous, current, t=1)
    expected_transition = tape.jacobian(transition_values, theta)

    with tf.GradientTape() as tape:
        tape.watch(theta)
        observation_values = model.observation_log_density(theta, current, observation, t=1)
    expected_observation = tape.jacobian(observation_values, theta)

    tf.debugging.assert_near(
        model.initial_log_density_parameter_score(theta, previous),
        expected_initial,
        atol=1e-8,
        rtol=1e-8,
    )
    tf.debugging.assert_near(
        model.transition_log_density_parameter_score(theta, previous, current, t=1),
        expected_transition,
        atol=1e-8,
        rtol=1e-8,
    )
    tf.debugging.assert_near(
        model.observation_log_density_parameter_score(theta, current, observation, t=1),
        expected_observation,
        atol=1e-8,
        rtol=1e-8,
    )


def test_generalized_sv_zhaocui_row_local_artifact_is_full_horizon_manual_score() -> None:
    path = ROOT / "docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-zhaocui-row-2026-07-02.json"
    assert path.exists()
    import json

    rows = json.loads(path.read_text(encoding="utf-8"))
    assert len(rows) == 1
    row = rows[0]

    assert row["row_id"] == "zhao_cui_generalized_sv_synthetic_from_estimated_values"
    assert row["algorithm_id"] == "zhao_cui_scalar_or_multistate"
    assert row["comparison_status"] == "executed_value_score"
    assert row["numeric_execution_status"] == (
        "executed_zhao_cui_generalized_sv_prior_mean_scalar_tt_value_score"
    )
    assert isinstance(row["log_likelihood"], float)
    assert isinstance(row["average_log_likelihood"], float)
    assert isinstance(row["score"], list)
    assert len(row["score"]) == 3
    assert row["score_coordinate_system"].startswith("theta=(z_gamma,log_tau,mu_over_tau)")
    assert bool(tf.math.is_finite(tf.constant(row["log_likelihood"], dtype=DTYPE)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(tf.constant(row["score"], dtype=DTYPE))).numpy())

    provenance = str(row["score_derivative_provenance"]).lower()
    assert "manual_parameter_score_methods_only" in provenance
    assert "autodiff" not in provenance
    assert "gradienttape" not in provenance
    assert "gradient_tape" not in provenance
    assert "forwardaccumulator" not in provenance
    assert "finite_difference" not in provenance
    assert "fd_" not in provenance
    assert any("not actual-SV, KSC, precursor, auxiliary, or native-oracle" in item for item in row["nonclaims"])
    assert any("full source horizon T1008" in item for item in row["nonclaims"])
