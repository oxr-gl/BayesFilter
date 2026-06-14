from __future__ import annotations

import tensorflow as tf

import bayesfilter.highdim as highdim


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _product_basis(degrees: tuple[int, ...]) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree)
            for degree in degrees
        ],
        _convention(),
    )


def _grid2() -> tf.Tensor:
    return tf.constant(
        [
            [-0.75, -0.50],
            [-0.75, 0.25],
            [-0.25, -0.50],
            [-0.25, 0.25],
            [0.25, -0.50],
            [0.25, 0.25],
            [0.75, -0.50],
            [0.75, 0.25],
        ],
        dtype=tf.float64,
    )


def _config(
    ranks: tuple[int, ...],
    sweep_order: tuple[int, ...] | None = None,
    ridge: float = 1e-12,
    max_sweeps: int = 1,
    holdout_tolerance: float = 1e-10,
    condition_number_veto: float = 1e14,
    row_budget: int = 10_000,
    column_budget: int = 1_000,
    dense_matrix_byte_budget: int = 10_000_000,
    normal_matrix_byte_budget: int = 10_000_000,
) -> highdim.FixedTTFitConfig:
    dimension = len(ranks) - 1
    return highdim.FixedTTFitConfig(
        ranks=ranks,
        ridge=ridge,
        max_sweeps=max_sweeps,
        sweep_order=sweep_order or tuple(range(dimension)),
        row_budget=row_budget,
        column_budget=column_budget,
        dense_matrix_byte_budget=dense_matrix_byte_budget,
        normal_matrix_byte_budget=normal_matrix_byte_budget,
        condition_number_warning=1e10,
        condition_number_veto=condition_number_veto,
        holdout_tolerance=holdout_tolerance,
    )


def _rank_one_truth(product: highdim.ProductBasis) -> highdim.FunctionalTT:
    return highdim.FunctionalTT(
        [
            highdim.TTCore(tf.constant([[[0.75], [0.25]]], dtype=tf.float64)),
            highdim.TTCore(tf.constant([[[1.25], [-0.125]]], dtype=tf.float64)),
        ],
        product,
        _convention(),
    )


def _rank_two_truth(product: highdim.ProductBasis) -> highdim.FunctionalTT:
    return highdim.FunctionalTT(
        [
            highdim.TTCore(
                tf.constant(
                    [
                        [[1.0, 0.0], [0.0, 1.0]],
                    ],
                    dtype=tf.float64,
                )
            ),
            highdim.TTCore(
                tf.constant(
                    [
                        [[0.75], [0.20]],
                        [[-0.35], [0.60]],
                    ],
                    dtype=tf.float64,
                )
            ),
        ],
        product,
        _convention(),
    )


def _samples_from_truth(
    truth: highdim.FunctionalTT,
    points: tf.Tensor,
) -> highdim.FixedTTFitSampleBatch:
    return highdim.FixedTTFitSampleBatch(
        points=points,
        target_values=truth.evaluate(points),
        weights=tf.ones([int(points.shape[0])], dtype=tf.float64),
    )


def test_fixed_fit_rank_one_separable_target_exact():
    product = _product_basis((1, 1))
    truth = _rank_one_truth(product)
    points = _grid2()
    samples = _samples_from_truth(truth, points)
    initial_cores = (
        highdim.TTCore(tf.constant([[[0.1], [0.2]]], dtype=tf.float64)),
        truth.cores[1],
    )

    result = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 1, 1), max_sweeps=2),
        initial_cores,
        branch_seed="rank-one",
        measure_convention=_convention(),
    )

    assert result.status is highdim.HighDimStatus.OK
    tf.debugging.assert_near(result.fitted_tt.evaluate(points), samples.target_values, atol=1e-10)
    tf.debugging.assert_near(result.fit_residual, tf.constant(0.0, dtype=tf.float64), atol=1e-10)


def test_fixed_fit_known_rank_two_bivariate_target():
    product = _product_basis((1, 1))
    truth = _rank_two_truth(product)
    points = _grid2()
    samples = _samples_from_truth(truth, points)
    initial_cores = (
        highdim.TTCore(
            tf.constant(
                [
                    [[0.5, 0.1], [0.1, 0.5]],
                ],
                dtype=tf.float64,
            )
        ),
        truth.cores[1],
    )

    result = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 2, 1), max_sweeps=2),
        initial_cores,
        branch_seed="rank-two",
        measure_convention=_convention(),
    )

    assert result.status is highdim.HighDimStatus.OK
    tf.debugging.assert_near(result.fitted_tt.evaluate(points), samples.target_values, atol=1e-10)
    tf.debugging.assert_near(result.fit_residual, tf.constant(0.0, dtype=tf.float64), atol=1e-10)


def test_environment_recomputed_after_each_core_update():
    product = _product_basis((1, 1))
    truth = _rank_one_truth(product)
    samples = _samples_from_truth(truth, _grid2())
    result = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 1, 1), max_sweeps=1),
        [
            highdim.TTCore(tf.constant([[[0.1], [0.2]]], dtype=tf.float64)),
            truth.cores[1],
        ],
        branch_seed="environment",
        measure_convention=_convention(),
    )

    hashes = result.diagnostics["environment_rebuild_hashes"]
    assert result.diagnostics["environment_rebuild_count"] == 2
    assert hashes[0] != hashes[1]


def test_design_matrix_shape_and_vectorization_order():
    product = _product_basis((1, 1))
    points = tf.constant([[-0.5, 0.25], [0.75, -0.25]], dtype=tf.float64)
    cores = (
        highdim.TTCore(tf.ones([1, 2, 2], dtype=tf.float64)),
        highdim.TTCore(
            tf.constant(
                [
                    [[2.0], [3.0]],
                    [[5.0], [7.0]],
                ],
                dtype=tf.float64,
            )
        ),
    )
    samples = highdim.FixedTTFitSampleBatch(
        points=points,
        target_values=tf.ones([2], dtype=tf.float64),
        weights=tf.ones([2], dtype=tf.float64),
    )
    system = highdim.FixedTTFitter().build_core_update_system(
        product,
        points,
        samples.target_values,
        samples.weights,
        cores,
        core_index=0,
        config=_config((1, 2, 1)),
    )

    psi0 = product.evaluate_axis(0, points[:, 0])
    psi1 = product.evaluate_axis(1, points[:, 1])
    right0 = 2.0 * psi1[:, 0] + 3.0 * psi1[:, 1]
    right1 = 5.0 * psi1[:, 0] + 7.0 * psi1[:, 1]
    expected = tf.stack(
        [
            psi0[:, 0] * right0,
            psi0[:, 0] * right1,
            psi0[:, 1] * right0,
            psi0[:, 1] * right1,
        ],
        axis=1,
    )

    assert system.design_matrix.shape == (2, 4)
    tf.debugging.assert_near(system.design_matrix, expected, atol=1e-12)


def test_normal_equation_solution_matches_direct_dense_reference():
    product = _product_basis((1, 1))
    truth = _rank_two_truth(product)
    points = _grid2()
    samples = _samples_from_truth(truth, points)
    initial_cores = (truth.cores[0], truth.cores[1])
    config = _config((1, 2, 1), max_sweeps=1)
    system = highdim.FixedTTFitter().build_core_update_system(
        product,
        points,
        samples.target_values,
        samples.weights,
        initial_cores,
        core_index=1,
        config=config,
    )
    direct_solution = tf.linalg.solve(
        system.normal_matrix,
        tf.reshape(system.rhs, [-1, 1]),
    )[:, 0]
    result = highdim.FixedTTFitter().fit(
        product,
        samples,
        config,
        initial_cores,
        branch_seed="normal-equation",
        measure_convention=_convention(),
    )

    fitted_core1 = tf.reshape(result.fitted_tt.cores[1].values, [-1])
    tf.debugging.assert_near(fitted_core1, direct_solution, atol=1e-12)


def test_deterministic_replay_same_manifest_same_values():
    product = _product_basis((1, 1))
    truth = _rank_one_truth(product)
    samples = _samples_from_truth(truth, _grid2())
    config = _config((1, 1, 1), max_sweeps=2)
    initial_cores = (
        highdim.TTCore(tf.constant([[[0.1], [0.2]]], dtype=tf.float64)),
        truth.cores[1],
    )

    first = highdim.FixedTTFitter().fit(
        product,
        samples,
        config,
        initial_cores,
        branch_seed=17,
        measure_convention=_convention(),
    )
    second = highdim.FixedTTFitter().fit(
        product,
        samples,
        config,
        initial_cores,
        branch_seed=17,
        measure_convention=_convention(),
    )

    assert first.branch_hash == second.branch_hash
    tf.debugging.assert_near(
        first.fitted_tt.evaluate(samples.points),
        second.fitted_tt.evaluate(samples.points),
        atol=0.0,
    )
    reloaded = highdim.FunctionalTT(
        second.fitted_tt.cores,
        product,
        _convention(),
        branch_identity=second.branch_identity,
    )
    tf.debugging.assert_near(reloaded.evaluate(samples.points), second.fitted_tt.evaluate(samples.points))


def test_branch_manifest_contains_required_fixed_fit_fields():
    product = _product_basis((1, 1))
    truth = _rank_one_truth(product)
    samples = _samples_from_truth(truth, _grid2())
    result = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 1, 1), max_sweeps=1),
        [
            highdim.TTCore(tf.constant([[[0.1], [0.2]]], dtype=tf.float64)),
            truth.cores[1],
        ],
        branch_seed="manifest",
        measure_convention=_convention(),
    )

    payload = result.branch_identity.manifest.payload
    expected_top_level = {
        "product_basis",
        "measure_convention",
        "samples",
        "sample_hashes",
        "ranks",
        "ridge",
        "dtype",
        "sweep_order",
        "max_sweeps",
        "initial_core_hash",
        "initialization_rule",
        "per_core_update_statuses",
        "environment_rebuild_hashes",
        "stabilization_choices",
        "complexity_budgets",
        "solver_backend",
        "deterministic_seed",
        "termination_reason",
        "stop_condition_triggered",
    }
    assert expected_top_level.issubset(set(payload))
    assert {
        "sample_points_hash",
        "target_values_hash",
        "weights_hash",
        "holdout_hash",
    }.issubset(set(payload["sample_hashes"]))
    assert payload["per_core_update_statuses"][0]["condition_number"] is not None


def test_branch_hash_changes_for_samples_ridge_ranks_sweep_order():
    product = _product_basis((1, 1))
    truth = _rank_one_truth(product)
    samples = _samples_from_truth(truth, _grid2())
    changed_samples = highdim.FixedTTFitSampleBatch(
        points=samples.points + tf.constant([[0.01, 0.0]], dtype=tf.float64),
        target_values=truth.evaluate(samples.points + tf.constant([[0.01, 0.0]], dtype=tf.float64)),
        weights=samples.weights,
    )
    base_initial = (
        highdim.TTCore(tf.constant([[[0.1], [0.2]]], dtype=tf.float64)),
        truth.cores[1],
    )
    base = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 1, 1), max_sweeps=1),
        base_initial,
        branch_seed="hash",
        measure_convention=_convention(),
    )
    changed_sample_result = highdim.FixedTTFitter().fit(
        product,
        changed_samples,
        _config((1, 1, 1), max_sweeps=1),
        base_initial,
        branch_seed="hash",
        measure_convention=_convention(),
    )
    changed_ridge_result = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 1, 1), ridge=1e-8, max_sweeps=1),
        base_initial,
        branch_seed="hash",
        measure_convention=_convention(),
    )
    changed_order_result = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 1, 1), sweep_order=(1, 0), max_sweeps=1),
        base_initial,
        branch_seed="hash",
        measure_convention=_convention(),
    )
    rank_two_truth = _rank_two_truth(product)
    rank_changed_result = highdim.FixedTTFitter().fit(
        product,
        _samples_from_truth(rank_two_truth, _grid2()),
        _config((1, 2, 1), max_sweeps=1),
        rank_two_truth.cores,
        branch_seed="hash",
        measure_convention=_convention(),
    )

    hashes = {
        base.branch_hash.value,
        changed_sample_result.branch_hash.value,
        changed_ridge_result.branch_hash.value,
        changed_order_result.branch_hash.value,
        rank_changed_result.branch_hash.value,
    }
    assert len(hashes) == 5


def test_trivariate_coupled_example_reports_coordinate_order_sensitivity():
    product = _product_basis((1, 1, 1))
    cores = [
        highdim.TTCore(tf.constant([[[1.0, 0.0], [0.0, 1.0]]], dtype=tf.float64)),
        highdim.TTCore(
            tf.constant(
                [
                    [[1.0, 0.2], [0.3, 0.4]],
                    [[-0.2, 0.7], [0.5, -0.1]],
                ],
                dtype=tf.float64,
            )
        ),
        highdim.TTCore(tf.constant([[[0.8], [0.1]], [[-0.4], [0.6]]], dtype=tf.float64)),
    ]
    truth = highdim.FunctionalTT(cores, product, _convention())
    points = tf.constant(
        [
            [-0.75, -0.50, -0.25],
            [-0.75, 0.25, 0.75],
            [-0.25, -0.50, 0.75],
            [-0.25, 0.25, -0.25],
            [0.25, -0.50, -0.25],
            [0.25, 0.25, 0.75],
            [0.75, -0.50, 0.75],
            [0.75, 0.25, -0.25],
        ],
        dtype=tf.float64,
    )
    samples = _samples_from_truth(truth, points)
    forward = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 2, 2, 1), sweep_order=(0, 1, 2), max_sweeps=1),
        cores,
        branch_seed="coord-order",
        measure_convention=_convention(),
    )
    reverse = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 2, 2, 1), sweep_order=(2, 1, 0), max_sweeps=1),
        cores,
        branch_seed="coord-order",
        measure_convention=_convention(),
    )

    assert forward.diagnostics["coordinate_order"] == (0, 1, 2)
    assert reverse.diagnostics["coordinate_order"] == (0, 1, 2)
    assert forward.diagnostics["sweep_order"] == (0, 1, 2)
    assert reverse.diagnostics["sweep_order"] == (2, 1, 0)
    assert forward.diagnostics["coordinate_order_sensitivity_reported"] is True
    assert forward.branch_hash != reverse.branch_hash


def test_holdout_residual_veto_for_under_ranked_target():
    product = _product_basis((1, 1))
    rank_two_truth = _rank_two_truth(product)
    training = tf.constant([[-0.75, -0.75], [-0.25, 0.25], [0.25, -0.25], [0.75, 0.75]], dtype=tf.float64)
    holdout = tf.constant([[-0.75, 0.75], [-0.25, -0.25], [0.25, 0.25], [0.75, -0.75]], dtype=tf.float64)
    samples = highdim.FixedTTFitSampleBatch(
        points=training,
        target_values=rank_two_truth.evaluate(training),
        weights=tf.ones([4], dtype=tf.float64),
        holdout_points=holdout,
        holdout_values=rank_two_truth.evaluate(holdout),
        holdout_weights=tf.ones([4], dtype=tf.float64),
    )

    result = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 1, 1), max_sweeps=2, holdout_tolerance=1e-14),
        [
            highdim.TTCore(tf.constant([[[1.0], [0.1]]], dtype=tf.float64)),
            highdim.TTCore(tf.constant([[[1.0], [0.1]]], dtype=tf.float64)),
        ],
        branch_seed="holdout",
        measure_convention=_convention(),
    )

    assert result.status is highdim.HighDimStatus.HOLDOUT_RESIDUAL_VETO
    assert result.stop_condition_triggered == highdim.HighDimStatus.HOLDOUT_RESIDUAL_VETO.value
    assert result.holdout_residual > 1e-14


def test_fixed_fit_complexity_gate_is_covered_in_fit_file():
    product = _product_basis((1, 1))
    samples = highdim.FixedTTFitSampleBatch(
        points=tf.constant([[-0.5, -0.5], [0.5, 0.5]], dtype=tf.float64),
        target_values=tf.ones([2], dtype=tf.float64),
        weights=tf.ones([2], dtype=tf.float64),
    )

    result = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 2, 1), row_budget=1),
        [
            highdim.TTCore(tf.ones([1, 2, 2], dtype=tf.float64)),
            highdim.TTCore(tf.ones([2, 2, 1], dtype=tf.float64)),
        ],
        branch_seed="fit-file-complexity",
        measure_convention=_convention(),
    )

    assert result.status is highdim.HighDimStatus.COMPLEXITY_GATE
    assert result.stop_condition_triggered == highdim.HighDimStatus.COMPLEXITY_GATE.value


def test_fixed_fit_condition_number_veto_is_covered_in_fit_file():
    product = _product_basis((1,))
    samples = highdim.FixedTTFitSampleBatch(
        points=tf.constant([[0.0], [0.0]], dtype=tf.float64),
        target_values=tf.ones([2], dtype=tf.float64),
        weights=tf.ones([2], dtype=tf.float64),
    )

    result = highdim.FixedTTFitter().fit(
        product,
        samples,
        _config((1, 1), ridge=0.0, condition_number_veto=10.0),
        [highdim.TTCore(tf.ones([1, 2, 1], dtype=tf.float64))],
        branch_seed="fit-file-condition",
        measure_convention=_convention(),
    )

    assert result.status is highdim.HighDimStatus.CONDITION_NUMBER_VETO
    assert result.stop_condition_triggered == highdim.HighDimStatus.CONDITION_NUMBER_VETO.value
