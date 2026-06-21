from __future__ import annotations

import json
from pathlib import Path

import pytest
import tensorflow as tf
import tensorflow_probability as tfp

import bayesfilter
import bayesfilter.highdim as highdim


DTYPE = tf.float64
MANIFEST_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p47-score-hmc-readiness-manifest-2026-06-08.json")
REGISTRY_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p47-target-registry-2026-06-08.json")
_STD_NORMAL = tfp.distributions.Normal(loc=tf.constant(0.0, dtype=DTYPE), scale=tf.constant(1.0, dtype=DTYPE))


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _rows() -> dict[str, dict[str, object]]:
    return {row["target_id"]: row for row in _manifest()["rows"]}


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


def _observations(dim: int) -> tf.Tensor:
    values = tf.constant([[0.12, -0.08, 0.05], [-0.07, 0.11, -0.04]], dtype=DTYPE)
    return values[:, : int(dim)]


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _tt_config(seed: str) -> highdim.FixedBranchFilterConfig:
    product_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 48)],
        _convention(),
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
        measure_convention=_convention(),
        deterministic_seed=seed,
        product_basis=product_basis,
        initial_cores=(highdim.TTCore(tf.ones([1, product_basis.bases[0].basis_dim, 1], dtype=DTYPE)),),
        fit_quadrature_order=141,
    )


def _zhaocui_value(theta: tf.Tensor, observations: tf.Tensor, sigma: tf.Tensor, *, seed: str) -> tf.Tensor:
    gamma, beta = _physical_from_theta(theta)
    return highdim.independent_panel_sv_mixture_zhaocui_tt_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        config=_tt_config(seed),
        branch_seed_prefix=f"p47-m6-score-api-{seed}",
    ).log_likelihood


def _zhaocui_score(theta: tf.Tensor, observations: tf.Tensor, sigma: tf.Tensor, *, seed: str) -> tf.Tensor:
    gamma, beta = _physical_from_theta(theta)
    derivative_config = highdim.FixedBranchDerivativeConfig(parameter_indices=tuple(range(int(theta.shape[0]))))
    return highdim.independent_panel_sv_mixture_zhaocui_tt_score(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        config=_tt_config(seed),
        derivative_config=derivative_config,
        branch_seed_prefix=f"p47-m6-score-api-analytic-{seed}",
        fixture_id=f"p47.m6.score.analytic.{seed}",
    ).score


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
    directions = tf.concat([eye, ramp[tf.newaxis, :], alternating[tf.newaxis, :], reverse_ramp[tf.newaxis, :]], axis=0)
    if int(directions.shape[0]) < 5:
        directions = tf.concat([directions, tf.ones([1, size], dtype=DTYPE) / tf.sqrt(tf.cast(size, DTYPE))], axis=0)
    return directions


def _relative_error(candidate: tf.Tensor, reference: tf.Tensor) -> tf.Tensor:
    return tf.linalg.norm(candidate - reference) / tf.maximum(tf.constant(1.0, dtype=DTYPE), tf.linalg.norm(reference))


def test_p47_m6_manifest_and_registry_keep_evidence_classes_separate() -> None:
    manifest = _manifest()
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    rows = _rows()
    registry_rows = {row["target_id"]: row for row in registry["rows"]}

    assert manifest["claim_scope"] == "evidence_class_readiness_table_not_production_hmc"
    assert manifest["pass_token"] == "PASS_P47_M6_SCORE_HMC_READINESS"
    assert "no production HMC readiness" in manifest["nonclaims"]
    assert "lower-rung rows are not production" in manifest["nonclaims"]
    assert rows["generalized_sv_lower_rung_ksc_mixture_target"]["p42_tiers_passed"] == [
        "TIER_1_LOCAL_VALUE_AND_DIRECTIONAL_SCORE"
    ]
    assert rows["spatial_sir_lower_rung_reference_filtering"]["api_status"] == "blocked_missing_score_evidence"
    assert rows["predator_prey_lower_rung_reference_filtering"]["api_status"] == "blocked_missing_score_evidence"
    assert rows["spatial_sir_production_filtering"]["api_status"] == "blocked_missing_production_filtering_token"
    assert rows["predator_prey_production_filtering"]["api_status"] == "blocked_missing_production_filtering_token"
    assert registry_rows["score_api_hmc_readiness_by_evidence_class"]["claim_class"] == "API_HMC_BY_EVIDENCE_CLASS"


def test_p47_m6_score_readiness_manifest_contract_rejects_overclaim() -> None:
    passed = highdim.ScoreReadinessRow(
        target_id="generalized_sv_lower_rung_ksc_mixture_target",
        evidence_class="lower_rung",
        upstream_tokens=("PASS_P47_M3_GENERALIZED_SV_EQUALITY",),
        p42_tiers_passed=("TIER_1_LOCAL_VALUE_AND_DIRECTIONAL_SCORE",),
        api_status="passed_experimental_subpackage_score_contract",
        hmc_status="blocked_tier2_tier3_not_run",
        promoted_claim="lower-rung experimental score API contract for the declared KSC mixture SV target",
        forbidden_claims=("production score API", "production HMC readiness"),
        m1_route_label="documented-deviation fixed-design substitute",
    )
    blocked = highdim.ScoreReadinessRow(
        target_id="spatial_sir_lower_rung_reference_filtering",
        evidence_class="lower_rung",
        upstream_tokens=("PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY",),
        p42_tiers_passed=(),
        api_status="blocked_missing_score_evidence",
        hmc_status="blocked_missing_score_evidence",
        promoted_claim="no score or HMC readiness claim; filtering row remains lower-rung value/state evidence",
        forbidden_claims=("production score API", "production HMC readiness"),
        m1_route_label="documented-deviation fixed-design substitute",
    )
    manifest = highdim.ScoreReadinessManifest(
        phase="P47-M6",
        rows=(passed, blocked),
        pass_token="PASS_P47_M6_SCORE_HMC_READINESS",
        nonclaims=(
            "no production HMC readiness",
            "no production score API",
            "lower-rung rows are not production",
        ),
    )

    assert highdim.score_readiness_branch_hash(manifest).value
    with pytest.raises(ValueError, match="lower-rung rows cannot promote production claims"):
        highdim.ScoreReadinessRow(
            target_id="bad_lower_rung",
            evidence_class="lower_rung",
            upstream_tokens=("PASS_P47_M3_GENERALIZED_SV_EQUALITY",),
            p42_tiers_passed=("TIER_1_LOCAL_VALUE_AND_DIRECTIONAL_SCORE",),
            api_status="passed_experimental_subpackage_score_contract",
            hmc_status="blocked_tier2_tier3_not_run",
            promoted_claim="production score API",
            forbidden_claims=("production HMC readiness",),
            m1_route_label="documented-deviation fixed-design substitute",
        )
    with pytest.raises(ValueError, match="passed API score rows require P42 Tier 1 evidence"):
        highdim.ScoreReadinessRow(
            target_id="bad_missing_tier1",
            evidence_class="lower_rung",
            upstream_tokens=("PASS_P47_M3_GENERALIZED_SV_EQUALITY",),
            p42_tiers_passed=(),
            api_status="passed_experimental_subpackage_score_contract",
            hmc_status="blocked_tier2_tier3_not_run",
            promoted_claim="lower-rung experimental score API contract",
            forbidden_claims=("production HMC readiness",),
            m1_route_label="documented-deviation fixed-design substitute",
        )
    with pytest.raises(ValueError, match="HMC readiness cannot be promoted"):
        highdim.ScoreReadinessRow(
            target_id="bad_hmc_claim",
            evidence_class="lower_rung",
            upstream_tokens=("PASS_P47_M3_GENERALIZED_SV_EQUALITY",),
            p42_tiers_passed=("TIER_1_LOCAL_VALUE_AND_DIRECTIONAL_SCORE",),
            api_status="passed_experimental_subpackage_score_contract",
            hmc_status="not_requested",
            promoted_claim="lower-rung HMC readiness",
            forbidden_claims=("production HMC readiness",),
            m1_route_label="documented-deviation fixed-design substitute",
        )


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p47_m6_generalized_sv_experimental_score_api_matches_dense_tier1(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _physical_parameters(dim)
    theta = _theta_from_physical(gamma, beta)

    dense = highdim.evaluate_experimental_score_api(
        target_id="generalized_sv_lower_rung_ksc_mixture_target_dense_reference",
        evidence_class="lower_rung",
        m1_route_label="documented-deviation fixed-design substitute",
        parameterization="theta=(Phi^{-1}(gamma_j), log(beta_j))_{j=1:d}",
        theta=theta,
        value_fn=lambda current_theta: _dense_mixture_panel_value(current_theta, observations, sigma),
        diagnostics={"reference_route": "dense_quadrature"},
    )
    zhaocui_value = _zhaocui_value(
        theta,
        observations,
        sigma,
        seed=f"dim-{dim}",
    )
    zhaocui_score = _zhaocui_score(
        theta,
        observations,
        sigma,
        seed=f"dim-{dim}",
    )
    diff = zhaocui_score - dense.score
    directional = tf.linalg.matvec(_directions(int(diff.shape[0])), diff)

    assert dense.status is highdim.HighDimStatus.OK
    tf.debugging.assert_near(zhaocui_value, dense.log_likelihood, atol=2e-2, rtol=8e-3)
    tf.debugging.assert_near(zhaocui_score, dense.score, atol=5e-2, rtol=5e-2)
    tf.debugging.assert_less(_relative_error(zhaocui_score, dense.score), tf.constant(5e-2, dtype=DTYPE))
    tf.debugging.assert_near(directional, tf.zeros_like(directional), atol=5e-2, rtol=5e-2)
    assert int(directional.shape[0]) >= 5


def test_p47_m6_no_top_level_public_score_api_export() -> None:
    forbidden = {
        "ExperimentalScoreAPIResult",
        "ScoreReadinessManifest",
        "ScoreReadinessRow",
        "evaluate_experimental_score_api",
        "score_readiness_branch_hash",
    }

    assert forbidden.isdisjoint(set(bayesfilter.__all__))
    assert all(not hasattr(bayesfilter, name) for name in forbidden)
    assert forbidden.issubset(set(highdim.__all__))
