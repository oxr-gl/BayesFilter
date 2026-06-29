from __future__ import annotations

from pathlib import Path

import bayesfilter
import bayesfilter.highdim as highdim


_HIGH_DIM_TOP_LEVEL_FORBIDDEN = {
    "TFFixedBranchSquaredTTFilterConfig",
    "TFFixedBranchSquaredTTFilterResult",
    "TFFixedBranchSquaredTTScoreResult",
    "tf_fixed_branch_squared_tt_log_likelihood",
    "tf_fixed_branch_squared_tt_score",
    "FixedBranchSquaredTTFilter",
    "FixedBranchFilterConfig",
    "FixedBranchScoreResult",
    "P30FixedBranchGradientTableManifest",
    "StressRunManifest",
    "StressRunStatus",
}

_CANDIDATE_STABLE_SYMBOLS = (
    "TFFixedBranchSquaredTTFilterConfig",
    "TFFixedBranchSquaredTTFilterResult",
    "TFFixedBranchSquaredTTScoreResult",
    "tf_fixed_branch_squared_tt_log_likelihood",
    "tf_fixed_branch_squared_tt_score",
)

_PHASE7_LEDGER = Path(
    "docs/plans/"
    "bayesfilter-highdim-nonlinear-filtering-p35-phase7-public-api-decision-result-2026-06-05.md"
)


def test_existing_v1_public_api_symbols_preserved():
    expected = {
        "TFLinearGaussianStateSpace",
        "TFLinearGaussianStateSpaceDerivatives",
        "tf_linear_gaussian_log_likelihood",
        "tf_kalman_log_likelihood",
        "tf_masked_kalman_log_likelihood",
        "tf_qr_linear_gaussian_log_likelihood",
        "tf_qr_sqrt_kalman_log_likelihood",
        "tf_qr_sqrt_masked_kalman_log_likelihood",
        "tf_qr_linear_gaussian_score_hessian",
        "tf_qr_sqrt_kalman_score_hessian",
        "tf_qr_sqrt_masked_kalman_score_hessian",
        "tf_svd_linear_gaussian_log_likelihood",
        "tf_svd_kalman_log_likelihood",
        "tf_svd_masked_kalman_log_likelihood",
        "TFStructuralStateSpace",
        "structural_block_metadata",
        "structural_filter_diagnostics",
        "structural_filter_metadata",
        "pointwise_deterministic_residuals",
        "affine_structural_to_linear_gaussian_tf",
        "make_affine_structural_tf",
        "tf_svd_sigma_point_log_likelihood",
        "tf_svd_sigma_point_log_likelihood_with_rule",
        "tf_svd_sigma_point_filter",
        "tf_svd_sigma_point_placement",
        "tf_svd_sigma_point_score_with_rule",
        "tf_svd_cubature_score",
        "tf_principal_sqrt_ukf_score",
        "tf_svd_ukf_score",
        "tf_unit_sigma_point_rule",
        "tf_cut4g_sigma_point_rule",
        "tf_svd_cut4_log_likelihood",
        "tf_svd_cut4_filter",
        "tf_svd_cut4_score",
        "TFStructuralFirstDerivatives",
    }

    assert expected.issubset(set(bayesfilter.__all__))
    assert all(hasattr(bayesfilter, name) for name in expected)


def test_no_highdim_top_level_symbols_before_phase7_option_c():
    top_level = set(bayesfilter.__all__)
    leaked = sorted(_HIGH_DIM_TOP_LEVEL_FORBIDDEN.intersection(top_level))

    assert leaked == []
    assert all(not hasattr(bayesfilter, name) for name in _HIGH_DIM_TOP_LEVEL_FORBIDDEN)


def test_experimental_subpackage_import_is_explicit_only():
    assert hasattr(highdim, "FixedBranchSquaredTTFilter")
    assert hasattr(highdim, "StressRunManifest")
    assert hasattr(highdim, "P30FixedBranchGradientTableManifest")
    assert "FixedBranchSquaredTTFilter" in highdim.__all__
    assert "StressRunManifest" in highdim.__all__
    assert "P30FixedBranchGradientTableManifest" in highdim.__all__
    assert "tf_fixed_branch_squared_tt_score" not in highdim.__all__
    assert "tf_fixed_branch_squared_tt_log_likelihood" not in highdim.__all__


def test_stable_public_symbols_include_fixed_branch_scope_language():
    missing_scope = [
        name
        for name in _CANDIDATE_STABLE_SYMBOLS
        if "fixed_branch" not in name.lower() and "fixedbranch" not in name.lower()
    ]

    assert missing_scope == []


def test_public_docs_do_not_claim_adaptive_derivative():
    text = _PHASE7_LEDGER.read_text(encoding="utf-8")
    required_non_claims = (
        "no stable top-level highdim public API",
        "no score API readiness",
        "no DSGE/HMC/GPU readiness",
        "no adaptive-branch derivative support",
        "no default-method recommendation",
    )
    forbidden_claims = (
        "adaptive derivative support is validated",
        "exact nonlinear likelihood is validated",
        "DSGE readiness is validated",
        "HMC readiness is validated",
        "GPU readiness is validated",
        "score API readiness is validated",
    )

    assert "decision_status: `EXPERIMENTAL_SUBPACKAGE_ONLY`" in text
    assert all(phrase in text for phrase in required_non_claims)
    assert all(phrase not in text for phrase in forbidden_claims)
