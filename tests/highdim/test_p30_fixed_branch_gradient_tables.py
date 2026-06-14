from __future__ import annotations

import pytest
import tensorflow as tf
import tensorflow_probability as tfp

import bayesfilter.highdim as highdim


def _branch_hash() -> str:
    return highdim.fixed_branch_compatibility_hash(
        {
            "fixture": "p37-m6-lgssm-exact-score",
            "basis_hash": "exact_scalar",
            "ranks": (),
            "sweep_order": (),
            "solver_backend": "tensorflow",
        }
    )


def _one_step_log_evidence(prior_mean: float) -> tf.Tensor:
    y = tf.constant(0.2, dtype=tf.float64)
    variance = tf.constant(1.0 + 0.09, dtype=tf.float64)
    return tfp.distributions.Normal(
        tf.constant(prior_mean, dtype=tf.float64),
        tf.sqrt(variance),
    ).log_prob(y)


def _finite_difference_table(
    *,
    branch_hash: str | None = None,
    analytic_gradient: tf.Tensor | None = None,
    perturb_score: float = 0.0,
) -> highdim.FiniteDifferenceTable:
    base_hash = _branch_hash() if branch_hash is None else branch_hash
    _log_evidence, score = highdim.scalar_one_step_lgssm_prior_mean_score()
    analytic = score if analytic_gradient is None else analytic_gradient
    rows = []
    for h in (1e-2, 1e-3, 1e-4, 1e-5):
        plus = _one_step_log_evidence(0.0 + h)
        minus = _one_step_log_evidence(0.0 - h)
        if perturb_score:
            analytic = score + tf.constant(perturb_score, dtype=tf.float64)
        rows.append(
            highdim.make_finite_difference_row(
                parameter_index=0,
                h=h,
                value_plus=plus,
                value_minus=minus,
                branch_hash_plus=base_hash,
                branch_hash_minus=base_hash,
                branch_hash_base=base_hash,
                analytic_gradient=analytic,
            )
        )
    return highdim.FiniteDifferenceTable(tuple(rows))


def _non_claims() -> tuple[str, ...]:
    return (
        "no adaptive derivative claim",
        "no stable score API claim",
        "no HMC readiness claim",
        "no DSGE readiness claim",
        "no GPU production claim",
        "no general nonlinear derivative claim",
    )


def _manifest(**overrides: object) -> highdim.P30FixedBranchGradientTableManifest:
    values = {
        "phase_id": "P37-M6",
        "model_row": "lgssm_exact_scalar_prior_mean",
        "value_result_artifact": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p30-model-suite-phase1-lgssm-exact-reference-result-2026-06-05.md"
        ),
        "value_prerequisite_status": "PASS_M1",
        "perturbation_coordinate": "prior_mean",
        "parameterization": "physical scalar prior mean",
        "finite_difference_h": (1e-2, 1e-3, 1e-4, 1e-5),
        "tolerance_policy": {
            "abs_error_tolerance": 1e-8,
            "stable_window_policy": "adjacent errors below tolerance with decrease or roundoff plateau",
        },
        "branch_policy": "fixed_branch_compatibility_hash",
        "finite_difference_table": _finite_difference_table(),
        "stable_window_status": "PASS_DECREASING_OR_ROUNDOFF_PLATEAU",
        "row_decision": "DERIVATIVE_PASSED",
        "non_claims": _non_claims(),
    }
    values.update(overrides)
    return highdim.P30FixedBranchGradientTableManifest(**values)


def test_p30_fixed_branch_gradient_table_accepts_lgssm_exact_score_fixture():
    manifest = _manifest()
    rows = manifest.finite_difference_table.valid_rows()

    assert manifest.phase_id == "P37-M6"
    assert manifest.row_decision == "DERIVATIVE_PASSED"
    assert manifest.valid_row_count() == 4
    assert all(row.row_status is highdim.FiniteDifferenceRowStatus.VALID for row in rows)
    assert float(manifest.finite_difference_table.max_abs_error().numpy()) < 1e-8
    assert "score API" in " ".join(manifest.non_claims)


def test_p30_fixed_branch_gradient_table_rejects_pass_without_value_prerequisite():
    with pytest.raises(ValueError, match="stable_window_status does not match"):
        _manifest(value_prerequisite_status="BLOCKED_VALUE_ROW")


def test_p30_fixed_branch_gradient_table_rejects_branch_mismatch_pass():
    rows = []
    table = _finite_difference_table()
    for index, row in enumerate(table.rows):
        rows.append(
            highdim.make_finite_difference_row(
                parameter_index=row.parameter_index,
                h=float(row.h.numpy()),
                value_plus=row.value_plus,
                value_minus=row.value_minus,
                branch_hash_plus="a" * 64 if index == 0 else row.branch_hash_plus,
                branch_hash_minus=row.branch_hash_minus,
                branch_hash_base=row.branch_hash_base,
                analytic_gradient=row.analytic_gradient,
            )
        )
    with pytest.raises(ValueError, match="stable_window_status does not match"):
        _manifest(finite_difference_table=highdim.FiniteDifferenceTable(tuple(rows)))


def test_p30_fixed_branch_gradient_table_rejects_misstated_h_ladder():
    with pytest.raises(ValueError, match="finite_difference_h must match"):
        _manifest(finite_difference_h=(1e-2, 1e-3))


def test_p30_fixed_branch_gradient_table_rejects_inconsistent_stable_window_status():
    with pytest.raises(ValueError, match="stable_window_status does not match"):
        _manifest(stable_window_status="FAIL_NO_STABLE_WINDOW")

    with pytest.raises(ValueError, match="stable_window_status is not an allowed"):
        _manifest(stable_window_status="PASS_BY_ASSERTION")


def test_p30_fixed_branch_gradient_table_rejects_unstable_window_pass():
    with pytest.raises(ValueError, match="stable_window_status does not match"):
        _manifest(finite_difference_table=_finite_difference_table(perturb_score=0.1))


def test_p30_fixed_branch_gradient_table_rejects_blocked_status_for_valid_unstable_rows():
    with pytest.raises(ValueError, match="stable_window_status does not match"):
        _manifest(
            finite_difference_table=_finite_difference_table(perturb_score=0.1),
            stable_window_status="BLOCKED_VALUE_OR_BRANCH_CONTRACT",
            row_decision="DERIVATIVE_BLOCKED",
        )


def test_p30_fixed_branch_gradient_table_accepts_failed_stable_window_status():
    manifest = _manifest(
        finite_difference_table=_finite_difference_table(perturb_score=0.1),
        stable_window_status="FAIL_NO_STABLE_WINDOW",
        row_decision="DERIVATIVE_BLOCKED",
    )

    assert manifest.row_decision == "DERIVATIVE_BLOCKED"
    assert manifest.stable_window_status == "FAIL_NO_STABLE_WINDOW"


def test_p30_fixed_branch_gradient_table_allows_blocked_non_lgssm_row():
    manifest = _manifest(
        model_row="stochastic_volatility_synthetic",
        value_prerequisite_status="BLOCKED_DERIVATIVE_PREREQUISITE",
        finite_difference_h=(),
        finite_difference_table=highdim.FiniteDifferenceTable(()),
        stable_window_status="BLOCKED_VALUE_OR_BRANCH_CONTRACT",
        row_decision="DERIVATIVE_BLOCKED",
    )

    assert manifest.row_decision == "DERIVATIVE_BLOCKED"
    assert manifest.valid_row_count() == 0


def test_p30_fixed_branch_gradient_table_rejects_missing_nonclaim():
    with pytest.raises(ValueError, match="non_claims must include score API"):
        _manifest(non_claims=("no adaptive derivative claim",))


def test_p30_fixed_branch_gradient_table_public_symbol_remains_subpackage_scoped():
    assert hasattr(highdim, "P30FixedBranchGradientTableManifest")
    assert "P30FixedBranchGradientTableManifest" in highdim.__all__
