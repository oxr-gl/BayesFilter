from __future__ import annotations

import time

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _lgssm(state_dim: int) -> highdim.LinearGaussianSSM:
    initial_mean = tf.linspace(
        tf.constant(0.05, dtype=tf.float64),
        tf.constant(0.05 * float(state_dim), dtype=tf.float64),
        state_dim,
    )
    diagonal = tf.linspace(
        tf.constant(0.8, dtype=tf.float64),
        tf.constant(1.1, dtype=tf.float64),
        state_dim,
    )
    initial_covariance = tf.linalg.diag(diagonal)
    transition_matrix = 0.65 * tf.eye(state_dim, dtype=tf.float64)
    transition_matrix = transition_matrix + 0.03 * _neighbor_matrix(state_dim)
    transition_covariance = 0.08 * tf.eye(state_dim, dtype=tf.float64)
    observation_matrix = tf.reshape(
        tf.linspace(
            tf.constant(0.7, dtype=tf.float64),
            tf.constant(1.0, dtype=tf.float64),
            state_dim,
        ),
        [1, state_dim],
    )
    observation_covariance = tf.constant([[0.15]], dtype=tf.float64)
    return highdim.LinearGaussianSSM(
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        transition_matrix=transition_matrix,
        transition_covariance=transition_covariance,
        observation_matrix=observation_matrix,
        observation_covariance=observation_covariance,
    )


def _neighbor_matrix(state_dim: int) -> tf.Tensor:
    rows = []
    for row in range(state_dim):
        values = []
        for col in range(state_dim):
            values.append(1.0 if abs(row - col) == 1 else 0.0)
        rows.append(values)
    return tf.constant(rows, dtype=tf.float64)


def _observations(horizon: int) -> tf.Tensor:
    return tf.reshape(
        tf.linspace(
            tf.constant(-0.10, dtype=tf.float64),
            tf.constant(0.15, dtype=tf.float64),
            horizon,
        ),
        [horizon, 1],
    )


def _filter_config(
    state_dim: int,
    seed: str,
    retained_storage_byte_budget: int = 10_000_000,
) -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=retained_storage_byte_budget,
        coordinate_maps=(highdim.IdentityCoordinateMap(state_dim),),
        measure_convention=_convention(),
        deterministic_seed=seed,
    )


def _tt_filter_config(seed: str) -> highdim.FixedBranchFilterConfig:
    product_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 4)],
        _convention(),
    )
    fit_config = highdim.FixedTTFitConfig(
        ranks=(1, 1),
        ridge=1e-10,
        max_sweeps=1,
        sweep_order=(0,),
        row_budget=256,
        column_budget=32,
        dense_matrix_byte_budget=100_000,
        normal_matrix_byte_budget=10_000,
        condition_number_warning=1e10,
        condition_number_veto=1e14,
        holdout_tolerance=1e6,
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=fit_config,
        density_tau=1e-12,
        normalizer_floor=1e-14,
        denominator_floor=1e-14,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(1),),
        measure_convention=_convention(),
        deterministic_seed=seed,
        product_basis=product_basis,
        fit_quadrature_order=16,
    )


def _theta0() -> tf.Tensor:
    return tf.zeros([0], dtype=tf.float64)


def _kalman_reference_log_likelihood(
    model: highdim.LinearGaussianSSM,
    observations: tf.Tensor,
) -> tf.Tensor:
    observation_matrix = tf.convert_to_tensor(observations, dtype=tf.float64)
    mean = model.initial_mean
    covariance = model.initial_covariance
    log_terms = []
    for time_index in range(int(observation_matrix.shape[0])):
        if time_index > 0:
            mean = model.transition_offset + tf.linalg.matvec(model.transition_matrix, mean)
            covariance = _symmetrize(
                model.transition_matrix @ covariance @ tf.transpose(model.transition_matrix)
                + model.transition_covariance
            )
        innovation = observation_matrix[time_index] - (
            model.observation_offset + tf.linalg.matvec(model.observation_matrix, mean)
        )
        innovation_covariance = _symmetrize(
            model.observation_matrix @ covariance @ tf.transpose(model.observation_matrix)
            + model.observation_covariance
        )
        log_terms.append(_mvn_log_prob_zero_mean(innovation, innovation_covariance))
        gain_rhs = covariance @ tf.transpose(model.observation_matrix)
        chol = tf.linalg.cholesky(innovation_covariance)
        kalman_gain = tf.transpose(tf.linalg.cholesky_solve(chol, tf.transpose(gain_rhs)))
        mean = mean + tf.linalg.matvec(kalman_gain, innovation)
        left = tf.eye(model.state_dim(), dtype=tf.float64) - kalman_gain @ model.observation_matrix
        covariance = _symmetrize(
            left @ covariance @ tf.transpose(left)
            + kalman_gain @ model.observation_covariance @ tf.transpose(kalman_gain)
        )
    return tf.reduce_sum(tf.stack(log_terms))


def _mvn_log_prob_zero_mean(value: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    chol = tf.linalg.cholesky(covariance)
    solve = tf.linalg.cholesky_solve(chol, tf.reshape(value, [-1, 1]))[:, 0]
    dim = tf.cast(tf.shape(value)[0], tf.float64)
    log_det = 2.0 * tf.reduce_sum(tf.math.log(tf.linalg.diag_part(chol)))
    return -0.5 * (
        dim * tf.math.log(tf.constant(2.0 * 3.141592653589793, dtype=tf.float64))
        + log_det
        + tf.reduce_sum(value * solve)
    )


def _symmetrize(matrix: tf.Tensor) -> tf.Tensor:
    return 0.5 * (matrix + tf.linalg.matrix_transpose(matrix))


def _resource_budgets(
    filter_config: highdim.FixedBranchFilterConfig,
) -> dict[str, int]:
    fit_config = filter_config.fit_config
    return {
        "row_budget": int(fit_config.row_budget) if fit_config is not None else 0,
        "column_budget": int(fit_config.column_budget) if fit_config is not None else 0,
        "dense_matrix_byte_budget": (
            int(fit_config.dense_matrix_byte_budget) if fit_config is not None else 0
        ),
        "normal_matrix_byte_budget": (
            int(fit_config.normal_matrix_byte_budget) if fit_config is not None else 0
        ),
        "retained_storage_byte_budget": int(filter_config.retained_storage_byte_budget),
    }


def _manifest(
    *,
    command: str,
    filter_config: highdim.FixedBranchFilterConfig,
    result: highdim.FixedBranchFilterResult,
    replay: highdim.FixedBranchFilterResult,
    wall_time_seconds: float,
    exact_reference_error: float,
    grid: dict[str, object],
    fit_residual: object,
    normalizer_diagnostics: object,
) -> highdim.StressRunManifest:
    replay_ok = (
        result.branch_identity.hash.value == replay.branch_identity.hash.value
        and abs(float((result.log_likelihood - replay.log_likelihood).numpy())) == 0.0
    )
    return highdim.StressRunManifest(
        {
            "git_commit": "test-runtime",
            "command": command,
            "environment": "pytest CPU smoke",
            "cpu_gpu_status": "CPU_ONLY_CUDA_VISIBLE_DEVICES=-1_expected",
            "random_seeds": (str(filter_config.deterministic_seed),),
            "dtype": "tf.float64",
            "model_equations": (
                "x0 ~ N(m0,P0)",
                "x_t = A x_{t-1} + b + eta_t, eta_t ~ N(0,Q)",
                "y_t = H x_t + c + eps_t, eps_t ~ N(0,R)",
            ),
            "dimension_rank_degree_horizon_grid": grid,
            "resource_budgets": _resource_budgets(filter_config),
            "expected_memory_model": "dense_design_bytes=n_rows*n_cols*8; normal_bytes=n_cols*n_cols*8",
            "measured_peak_memory": "not_available_in_pytest_smoke",
            "wall_time_seconds": float(wall_time_seconds),
            "exact_reference_error": float(exact_reference_error),
            "fit_residual": fit_residual,
            "holdout_residual": None,
            "normalizer_diagnostics": normalizer_diagnostics,
            "branch_hash": result.branch_identity.hash.value,
            "deterministic_replay_status": "PASS" if replay_ok else "FAIL",
            "decision_status": highdim.StressRunStatus.PASS_EXACT_REFERENCE.value,
            "termination_reason": "finite_exact_reference_smoke",
            "stop_condition_triggered": "none",
            "what_is_not_concluded": (
                "DSGE readiness",
                "HMC readiness",
                "GPU readiness",
                "end-to-end score API readiness",
                "large-scale scalability",
            ),
        }
    )


def test_scaling_smoke_lgssm_runs_tiny_grid_with_finite_diagnostics():
    manifests = []
    for state_dim in (1, 2):
        model = _lgssm(state_dim)
        for horizon in (1, 2, 3):
            observations = _observations(horizon)
            config = _filter_config(
                state_dim=state_dim,
                seed=f"phase6-lgssm-d{state_dim}-h{horizon}",
            )
            start = time.perf_counter()
            result = highdim.FixedBranchSquaredTTFilter(config).log_likelihood(
                model,
                _theta0(),
                observations,
            )
            wall_time = time.perf_counter() - start
            replay = highdim.FixedBranchSquaredTTFilter(config).log_likelihood(
                model,
                _theta0(),
                observations,
            )
            reference = _kalman_reference_log_likelihood(model, observations)
            exact_error = abs(float((result.log_likelihood - reference).numpy()))
            manifest = _manifest(
                command="pytest -q tests/highdim/test_scaling_smoke.py",
                filter_config=config,
                result=result,
                replay=replay,
                wall_time_seconds=wall_time,
                exact_reference_error=exact_error,
                grid={
                    "model": "LGSSM",
                    "state_dim": state_dim,
                    "parameter_dim": 0,
                    "horizon": horizon,
                    "rank": None,
                    "max_degree": None,
                },
                fit_residual=None,
                normalizer_diagnostics=tuple(
                    float(step.retained_filter.normalizer.numpy()) for step in result.steps
                ),
            )
            manifests.append(manifest)

            assert result.status is highdim.HighDimStatus.OK
            assert manifest.decision_status is highdim.StressRunStatus.PASS_EXACT_REFERENCE
            assert manifest.fields["deterministic_replay_status"] == "PASS"
            assert exact_error < 2e-12
            assert all(
                tf.math.is_finite(step.log_normalizer)
                for step in result.steps
            )

    assert len(manifests) == 6


def test_scaling_smoke_fixed_tt_artifact_replay_has_resource_manifest():
    model = _lgssm(1)
    observations = _observations(2)
    config = _tt_filter_config(seed="phase6-scalar-tt-artifact")
    start = time.perf_counter()
    result = highdim.FixedBranchSquaredTTFilter(config).log_likelihood(
        model,
        _theta0(),
        observations,
    )
    wall_time = time.perf_counter() - start
    replay = highdim.FixedBranchSquaredTTFilter(config).log_likelihood(
        model,
        _theta0(),
        observations,
    )
    reference = _kalman_reference_log_likelihood(model, observations)
    fit_residuals = tuple(
        float(step.fit_result.fit_residual.numpy())
        for step in result.steps
        if step.fit_result is not None
    )
    density_normalizers = tuple(
        float(step.diagnostics["tt_density_normalizer"].numpy())
        for step in result.steps
    )

    manifest = _manifest(
        command="pytest -q tests/highdim/test_scaling_smoke.py",
        filter_config=config,
        result=result,
        replay=replay,
        wall_time_seconds=wall_time,
        exact_reference_error=abs(float((result.log_likelihood - reference).numpy())),
        grid={
            "model": "scalar_LGSSM_with_squared_TT_artifacts",
            "state_dim": 1,
            "parameter_dim": 0,
            "horizon": 2,
            "rank": (1, 1),
            "max_degree": 4,
        },
        fit_residual=fit_residuals,
        normalizer_diagnostics=density_normalizers,
    )

    assert result.diagnostics["tt_artifacts_present"] is True
    assert manifest.fields["deterministic_replay_status"] == "PASS"
    assert manifest.fields["resource_budgets"]["row_budget"] == 256
    assert manifest.fields["resource_budgets"]["normal_matrix_byte_budget"] == 10_000
    assert max(fit_residuals) < 5e-2
    assert all(value > 0.0 for value in density_normalizers)


def test_scaling_smoke_blocks_when_phase0_to_phase5_regression_flag_is_set():
    assert (
        highdim.stress_ladder_blocked_by_phase_regression(True)
        is highdim.StressRunStatus.BLOCKED_BY_PHASE_REGRESSION
    )
    assert (
        highdim.stress_ladder_blocked_by_phase_regression(False)
        is highdim.StressRunStatus.PASS_DIAGNOSTIC_ONLY
    )


def test_scaling_manifest_requires_resource_and_replay_fields():
    complete = {
        "git_commit": "test",
        "command": "pytest",
        "environment": "unit",
        "cpu_gpu_status": "CPU_ONLY",
        "random_seeds": ("seed",),
        "dtype": "tf.float64",
        "model_equations": ("equation",),
        "dimension_rank_degree_horizon_grid": {"state_dim": 1},
        "resource_budgets": {
            "row_budget": 1,
            "column_budget": 1,
            "dense_matrix_byte_budget": 8,
            "normal_matrix_byte_budget": 8,
            "retained_storage_byte_budget": 8,
        },
        "expected_memory_model": "test",
        "measured_peak_memory": "not_available",
        "wall_time_seconds": 0.0,
        "exact_reference_error": 0.0,
        "fit_residual": None,
        "holdout_residual": None,
        "normalizer_diagnostics": None,
        "branch_hash": "abc",
        "deterministic_replay_status": "PASS",
        "decision_status": highdim.StressRunStatus.PASS_DIAGNOSTIC_ONLY.value,
        "termination_reason": "unit",
        "stop_condition_triggered": "none",
        "what_is_not_concluded": ("production readiness",),
    }

    assert highdim.StressRunManifest(complete).decision_status is highdim.StressRunStatus.PASS_DIAGNOSTIC_ONLY
    missing = dict(complete)
    missing.pop("resource_budgets")
    with pytest.raises(ValueError, match="resource_budgets"):
        highdim.StressRunManifest(missing)
    bad_replay = dict(complete)
    bad_replay["deterministic_replay_status"] = ""
    with pytest.raises(ValueError, match="deterministic_replay_status"):
        highdim.StressRunManifest(bad_replay)


def test_stress_status_separates_tuning_approximation_resource_failures():
    assert (
        highdim.classify_stress_failure(highdim.HighDimStatus.COMPLEXITY_GATE, "row_budget")
        is highdim.StressRunStatus.FAIL_RESOURCE
    )
    assert (
        highdim.classify_stress_failure(highdim.HighDimStatus.CONDITION_NUMBER_VETO, "condition")
        is highdim.StressRunStatus.FAIL_TUNING
    )
    assert (
        highdim.classify_stress_failure(highdim.HighDimStatus.HOLDOUT_RESIDUAL_VETO, "holdout")
        is highdim.StressRunStatus.FAIL_APPROXIMATION
    )
    assert (
        highdim.classify_stress_failure(highdim.HighDimStatus.NONFINITE_VALUE, "nan")
        is highdim.StressRunStatus.FAIL_NUMERICAL_VETO
    )
    assert (
        highdim.classify_stress_failure(highdim.HighDimStatus.INVALID_BRANCH_MISMATCH, "hash")
        is highdim.StressRunStatus.FAIL_IMPLEMENTATION
    )
