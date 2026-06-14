from __future__ import annotations

import json
from pathlib import Path

import pytest
import tensorflow as tf
import tensorflow_probability as tfp

import bayesfilter.highdim as highdim


DTYPE = tf.float64
REGISTRY_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p47-target-registry-2026-06-08.json")
M2_MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-paper-scale-readiness-manifest-2026-06-08.json"
)

_STD_NORMAL = tfp.distributions.Normal(
    loc=tf.constant(0.0, dtype=DTYPE),
    scale=tf.constant(1.0, dtype=DTYPE),
)


def _observations(dim: int) -> tf.Tensor:
    values = tf.constant(
        [
            [0.12, -0.08, 0.05],
            [-0.07, 0.11, -0.04],
        ],
        dtype=DTYPE,
    )
    return values[:, : int(dim)]


def _physical_parameters(dim: int) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    gamma = tf.constant([0.60, 0.52, 0.47], dtype=DTYPE)[: int(dim)]
    beta = tf.constant([0.40, 0.35, 0.45], dtype=DTYPE)[: int(dim)]
    sigma = tf.constant([1.00, 0.85, 0.75], dtype=DTYPE)[: int(dim)]
    return gamma, beta, sigma


def _theta_from_physical(gamma: tf.Tensor, beta: tf.Tensor) -> tf.Tensor:
    return tf.reshape(tf.stack([_STD_NORMAL.quantile(gamma), tf.math.log(beta)], axis=1), [-1])


def _physical_from_theta(theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    theta_matrix = tf.reshape(tf.convert_to_tensor(theta, dtype=DTYPE), [-1, 2])
    return _STD_NORMAL.cdf(theta_matrix[:, 0]), tf.exp(theta_matrix[:, 1])


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _tt_config(seed: str = "p47-generalized-sv") -> highdim.FixedBranchFilterConfig:
    convention = _convention()
    product_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 48)],
        convention,
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=(1, 1),
            ridge=1e-12,
            max_sweeps=2,
            sweep_order=(0,),
            row_budget=512,
            column_budget=128,
            dense_matrix_byte_budget=200_000,
            normal_matrix_byte_budget=100_000,
            condition_number_warning=1e10,
            condition_number_veto=1e14,
            holdout_tolerance=5e-4,
        ),
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.constant([0.0], dtype=DTYPE),
                matrix=tf.constant([[8.0]], dtype=DTYPE),
            ),
        ),
        measure_convention=convention,
        deterministic_seed=seed,
        product_basis=product_basis,
        initial_cores=(
            highdim.TTCore(tf.ones([1, product_basis.bases[0].basis_dim, 1], dtype=DTYPE)),
        ),
        fit_quadrature_order=141,
    )


def _kalman_value(theta: tf.Tensor, observations: tf.Tensor, sigma: tf.Tensor) -> tf.Tensor:
    gamma, beta = _physical_from_theta(theta)
    return highdim.independent_panel_sv_mixture_kalman_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    ).log_likelihood


def _cut4_value(theta: tf.Tensor, observations: tf.Tensor, sigma: tf.Tensor) -> tf.Tensor:
    gamma, beta = _physical_from_theta(theta)
    return highdim.independent_panel_sv_mixture_cut4_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    ).log_likelihood


def _zhaocui_value(theta: tf.Tensor, observations: tf.Tensor, sigma: tf.Tensor, *, seed: str) -> tf.Tensor:
    gamma, beta = _physical_from_theta(theta)
    return highdim.independent_panel_sv_mixture_zhaocui_tt_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        config=_tt_config(seed),
        branch_seed_prefix=f"p47-ksc-mixture-zhaocui-{seed}",
    ).log_likelihood


def _value_and_score(value_fn, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    theta = tf.convert_to_tensor(theta, dtype=DTYPE)
    with tf.GradientTape() as tape:
        tape.watch(theta)
        value = value_fn(theta)
    score = tape.gradient(value, theta)
    if score is None:
        raise AssertionError("GradientTape returned None")
    return value, score


def _relative_error(candidate: tf.Tensor, reference: tf.Tensor) -> tf.Tensor:
    return tf.linalg.norm(candidate - reference) / tf.maximum(
        tf.constant(1.0, dtype=DTYPE),
        tf.linalg.norm(reference),
    )


def _directions(size: int) -> tf.Tensor:
    eye = tf.eye(size, dtype=DTYPE)
    ramp = tf.cast(tf.range(1, size + 1), DTYPE)
    ramp = ramp / tf.linalg.norm(ramp)
    alternating = tf.where(
        tf.math.floormod(tf.range(size), 2) == 0,
        tf.ones([size], dtype=DTYPE),
        -tf.ones([size], dtype=DTYPE),
    )
    alternating = alternating / tf.linalg.norm(alternating)
    reverse_ramp = tf.reverse(ramp, axis=[0])
    directions = tf.concat(
        [eye, ramp[tf.newaxis, :], alternating[tf.newaxis, :], reverse_ramp[tf.newaxis, :]],
        axis=0,
    )
    if int(directions.shape[0]) < 5:
        directions = tf.concat(
            [
                directions,
                tf.ones([1, size], dtype=DTYPE) / tf.sqrt(tf.cast(size, DTYPE)),
            ],
            axis=0,
        )
    return directions


def _assert_directional_residuals(candidate_score: tf.Tensor, reference_score: tf.Tensor, *, atol: float) -> None:
    diff = candidate_score - reference_score
    directional = tf.linalg.matvec(_directions(int(diff.shape[0])), diff)
    tf.debugging.assert_near(directional, tf.zeros_like(directional), atol=atol, rtol=atol)
    assert int(directional.shape[0]) >= 5


def test_p47_m3_registry_and_m2_manifest_allow_only_lower_rung_generalized_sv() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    m2_manifest = json.loads(M2_MANIFEST_PATH.read_text(encoding="utf-8"))
    rows = {row["target_id"]: row for row in registry["rows"]}
    m2_rows = {row["target_id"]: row for row in m2_manifest["candidate_rows"]}

    row = rows["generalized_sv_same_target_equality"]
    assert row["evidence_class"] == "lower_rung_value_gradient_equality"
    assert row["m1_route_label"] == "documented-deviation fixed-design substitute"
    assert "PASS_P47_M3_GENERALIZED_SV_EQUALITY" in row["pass_tokens"]
    assert "PASS_P47_M6_SCORE_HMC_READINESS" in row["forbidden_tokens"]
    assert "PASS_P47_M3_GENERALIZED_SV_EQUALITY" not in m2_manifest["claim_boundary"]["forbidden_tokens"]
    assert m2_rows["generalized_sv_same_target_equality"]["readiness_state"].startswith("eligible")


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p47_m3_cut4_matches_kalman_on_same_ksc_mixture_target_value_and_score(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _physical_parameters(dim)
    theta = _theta_from_physical(gamma, beta)

    kalman_value, kalman_score = _value_and_score(
        lambda current_theta: _kalman_value(current_theta, observations, sigma),
        theta,
    )
    cut4_value, cut4_score = _value_and_score(
        lambda current_theta: _cut4_value(current_theta, observations, sigma),
        theta,
    )

    tf.debugging.assert_near(cut4_value, kalman_value, atol=2e-6, rtol=2e-6)
    tf.debugging.assert_near(cut4_score, kalman_score, atol=2e-8, rtol=2e-8)
    tf.debugging.assert_less(_relative_error(cut4_score, kalman_score), tf.constant(1e-8, dtype=DTYPE))
    _assert_directional_residuals(cut4_score, kalman_score, atol=2e-8)


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p47_m3_zhaocui_matches_dense_on_same_ksc_mixture_target_value_and_score(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _physical_parameters(dim)
    theta = _theta_from_physical(gamma, beta)

    dense_value, dense_score = _value_and_score(
        lambda current_theta: _dense_mixture_panel_value(current_theta, observations, sigma),
        theta,
    )
    tt_value, tt_score = _value_and_score(
        lambda current_theta: _zhaocui_value(
            current_theta,
            observations,
            sigma,
            seed=f"dim-{dim}",
        ),
        theta,
    )

    tf.debugging.assert_near(tt_value, dense_value, atol=2e-2, rtol=8e-3)
    tf.debugging.assert_near(tt_score, dense_score, atol=5e-2, rtol=5e-2)
    tf.debugging.assert_less(_relative_error(tt_score, dense_score), tf.constant(5e-2, dtype=DTYPE))
    _assert_directional_residuals(tt_score, dense_score, atol=5e-2)


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p47_m3_cut4_and_zhaocui_direct_gap_is_bounded_on_ksc_target(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _physical_parameters(dim)
    theta = _theta_from_physical(gamma, beta)

    dense_value, dense_score = _value_and_score(
        lambda current_theta: _dense_mixture_panel_value(current_theta, observations, sigma),
        theta,
    )
    cut4_value, cut4_score = _value_and_score(
        lambda current_theta: _cut4_value(current_theta, observations, sigma),
        theta,
    )
    tt_value, tt_score = _value_and_score(
        lambda current_theta: _zhaocui_value(
            current_theta,
            observations,
            sigma,
            seed=f"direct-dim-{dim}",
        ),
        theta,
    )

    tf.debugging.assert_near(cut4_value, dense_value, atol=2e-3, rtol=2e-3)
    tf.debugging.assert_near(cut4_score, dense_score, atol=5e-3, rtol=5e-3)
    tf.debugging.assert_near(cut4_value, tt_value, atol=2e-3, rtol=2e-3)
    tf.debugging.assert_near(cut4_score, tt_score, atol=5e-3, rtol=5e-3)
    _assert_directional_residuals(cut4_score, dense_score, atol=5e-3)
    _assert_directional_residuals(cut4_score, tt_score, atol=5e-3)


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p47_m3_cut4_and_zhaocui_are_same_declared_ksc_target_but_not_native_sv(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _physical_parameters(dim)
    cut4 = highdim.independent_panel_sv_mixture_cut4_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    )
    zhaocui = highdim.independent_panel_sv_mixture_zhaocui_tt_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        config=_tt_config(seed=f"diagnostics-dim-{dim}"),
        branch_seed_prefix=f"p47-ksc-mixture-zhaocui-diagnostics-{dim}",
    )

    assert cut4.diagnostics["target_scope"] == zhaocui.diagnostics["target_scope"]
    assert zhaocui.diagnostics["m1_route_label"] == "documented-deviation fixed-design substitute"
    assert "not exact native SV likelihood" in cut4.diagnostics["non_claims"]
    assert "not exact native SV likelihood" in zhaocui.diagnostics["non_claims"]
    assert "not native generalized SV/CNS estimator" in zhaocui.diagnostics["non_claims"]
    assert "not adaptive MATLAB TT-cross/SIRT reproduction" in zhaocui.diagnostics["non_claims"]


def _dense_mixture_panel_value(theta: tf.Tensor, observations: tf.Tensor, sigma: tf.Tensor) -> tf.Tensor:
    gamma, beta = _physical_from_theta(theta)
    values = []
    for axis in range(int(observations.shape[1])):
        model = highdim.StochasticVolatilitySSM(sigma=sigma[axis])
        axis_theta = model.unconstrained_from_physical(gamma=gamma[axis], beta=beta[axis])
        values.append(
            highdim.scalar_sv_mixture_dense_reference(
                model,
                axis_theta,
                observations[:, axis : axis + 1],
                order=401,
                radius=8.0,
            ).log_likelihood
        )
    return tf.reduce_sum(tf.stack(values))
