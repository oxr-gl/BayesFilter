from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim


def _fixture_manifest(**overrides: object) -> highdim.P30ModelSuiteFixtureManifest:
    values = {
        "version": "p37.m0.fixture.v1",
        "model_id": highdim.P30ModelSuiteModelID.STOCHASTIC_VOLATILITY_SYNTHETIC,
        "source_equations": ("eq:p27-sv1", "eq:p27-sv2", "eq:p27-sv3"),
        "paper_anchor": "Zhao--Cui stochastic-volatility benchmark",
        "matlab_anchor": "eg2_sv/mainscript.m",
        "parameter_values": {"gamma": 0.6, "beta": 0.4, "sigma": 1.0},
        "prior": {"gamma": "declared in phase row", "beta": "declared in phase row"},
        "state_dimension": 1,
        "parameter_dimension": 2,
        "horizon": 3,
        "basis": {"family": "legendre", "ell": 9},
        "rank": (1, 2, 1),
        "sweeps": 1,
        "seed": "p37-m0-sv",
        "dtype": "tf.float64",
        "reference_method": "tiny dense reference before long horizon",
        "expected_metrics": ("path_rmse", "coverage", "ess_quantiles"),
        "vetoes": ("nonfinite_likelihood", "missing_dimension_convention"),
        "non_claims": ("not long-horizon validation", "not BayesFilter evidence yet"),
        "clean_room_status": "P30-derived fixture contract, MATLAB audit reference only",
        "dimension_convention": "x_0 included in this tiny fixture row",
    }
    values.update(overrides)
    return highdim.P30ModelSuiteFixtureManifest(**values)


def _result_manifest(**overrides: object) -> highdim.P30ModelSuiteResultManifest:
    values = {
        "version": "p37.m0.result.v1",
        "fixture_version": "p37.m0.fixture.v1",
        "model_id": highdim.P30ModelSuiteModelID.STOCHASTIC_VOLATILITY_SYNTHETIC,
        "source_governance_status": highdim.ModelSuiteTraceabilityStatus.REFERENCE_ONLY,
        "bayesfilter_evidence_anchors": (),
        "accuracy_metrics": {"path_rmse": "not_run"},
        "resource_metrics": {"wall_time_seconds": "not_run"},
        "finite_diagnostics": {"finite_values": "not_run"},
        "branch_replay_status": "not_applicable",
        "failure_classification": "planning_contract_only",
        "clean_room_status": "P30-derived result schema, no MATLAB code copied",
        "non_claims": ("not BayesFilter evidence", "not posterior accuracy"),
    }
    values.update(overrides)
    return highdim.P30ModelSuiteResultManifest(**values)


def test_p30_registry_contains_required_model_families_with_source_anchors():
    registry = highdim.p30_model_suite_registry()

    assert set(registry) == {
        "lgssm_exact",
        "stochastic_volatility_synthetic",
        "stochastic_volatility_real_optional",
        "spatial_sir",
        "predator_prey",
        "bayesfilter_generic_stress",
    }
    for row in registry.values():
        assert row.source_equations
        assert row.p30_anchor
        assert row.paper_anchor
        assert row.matlab_anchor
        assert row.reference_method
        assert row.dimension_convention
        assert row.non_claims


def test_reference_only_models_are_not_bayesfilter_evidence():
    registry = highdim.p30_model_suite_registry()

    for model_id in (
        "stochastic_volatility_real_optional",
    ):
        row = registry[model_id]
        assert row.status is highdim.ModelSuiteTraceabilityStatus.REFERENCE_ONLY
        assert row.bayesfilter_code_anchor == "none"
        assert row.bayesfilter_test_anchor == "none"
        assert any("not BayesFilter evidence" in claim for claim in row.non_claims)


def test_sv_synthetic_registry_records_scalar_dense_extension_boundary():
    row = highdim.p30_model_suite_registry()["stochastic_volatility_synthetic"]

    assert row.status is highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION
    assert row.bayesfilter_code_anchor == "bayesfilter/highdim/models.py; bayesfilter/highdim/filtering.py"
    assert row.bayesfilter_test_anchor == "tests/highdim/test_p30_stochastic_volatility.py"
    assert any("not TT posterior accuracy" in claim for claim in row.non_claims)
    assert any("no Zhao--Cui T=1000 reproduction" in claim for claim in row.non_claims)


def test_spatial_sir_registry_records_first_gate_extension_boundary():
    row = highdim.p30_model_suite_registry()["spatial_sir"]

    assert row.status is highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION
    assert row.implementation_status == "first_gate_model_contract_only"
    assert row.test_status == "rk4_observation_likelihood_simulation_rmse_diagnostics"
    assert row.bayesfilter_code_anchor == "bayesfilter/highdim/models.py"
    assert row.bayesfilter_test_anchor == "tests/highdim/test_p30_spatial_sir.py"
    assert "eq:p27-sir10" in row.source_equations
    assert any("not production TT/SIRT SIR filtering" in claim for claim in row.non_claims)
    assert any("no partial-observation scalability claim" in claim for claim in row.non_claims)


def test_predator_prey_registry_records_first_gate_extension_boundary():
    row = highdim.p30_model_suite_registry()["predator_prey"]

    assert row.status is highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION
    assert row.implementation_status == "first_gate_model_contract_and_comparison_schema_only"
    assert row.test_status == "rk4_prior_likelihood_simulation_rmse_manifest_schema"
    assert row.bayesfilter_code_anchor == "bayesfilter/highdim/models.py; bayesfilter/highdim/validation.py"
    assert row.bayesfilter_test_anchor == (
        "tests/highdim/test_p30_predator_prey.py; tests/highdim/test_p30_model_suite_contracts.py"
    )
    assert "eq:p27-pp8" in row.source_equations
    assert any("no nonlinear preconditioning usefulness claim" in claim for claim in row.non_claims)
    assert any("no matched linear/nonlinear comparison success claim" in claim for claim in row.non_claims)
    assert any("no paper-scale predator-prey result" in claim for claim in row.non_claims)


def test_generic_stress_registry_records_m5_extension_boundary():
    row = highdim.p30_model_suite_registry()["bayesfilter_generic_stress"]

    assert row.status is highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION
    assert row.implementation_status == "p37_m5_first_gate_stress_schema_and_tiny_cpu_smoke"
    assert row.test_status == "m5_manifest_schema_one_axis_guardrail_and_tiny_cpu_smoke"
    assert "tests/highdim/test_scaling_smoke.py" in row.bayesfilter_test_anchor
    assert "tests/highdim/test_p30_stress_ladders.py" in row.bayesfilter_test_anchor
    assert any("not paper-model reproduction" in claim for claim in row.non_claims)
    assert any("no correctness claim from stress rows" in claim for claim in row.non_claims)
    assert any("no GPU/HMC/DSGE readiness claim" in claim for claim in row.non_claims)


def test_lgssm_registry_preserves_partial_reproduction_nonclaim():
    row = highdim.p30_model_suite_registry()["lgssm_exact"]

    assert row.status is highdim.ModelSuiteTraceabilityStatus.SOURCE_MATCHED
    assert "test_filtering_kalman_exact.py" in row.bayesfilter_test_anchor
    assert any("not full Zhao--Cui reproduction grid" in claim for claim in row.non_claims)


def test_fixture_manifest_requires_p30_equations_and_dimension_convention():
    with pytest.raises(ValueError, match="source_equations"):
        _fixture_manifest(source_equations=())

    with pytest.raises(ValueError, match="dimension_convention"):
        _fixture_manifest(dimension_convention=" ")


def test_fixture_manifest_requires_float64_and_positive_rank():
    with pytest.raises(ValueError, match="dtype"):
        _fixture_manifest(dtype="float32")

    with pytest.raises(ValueError, match="rank"):
        _fixture_manifest(rank=(1, 0, 1))


def test_fixture_manifest_freezes_mapping_fields():
    manifest = _fixture_manifest()

    with pytest.raises(TypeError):
        manifest.parameter_values["gamma"] = 0.7
    with pytest.raises(TypeError):
        manifest.basis["ell"] = 17


def test_result_manifest_requires_clean_room_status_and_non_claims():
    with pytest.raises(ValueError, match="clean_room_status"):
        _result_manifest(clean_room_status="")

    with pytest.raises(ValueError, match="non_claims"):
        _result_manifest(non_claims=())


def test_promoted_result_requires_bayesfilter_evidence_anchor():
    with pytest.raises(ValueError, match="BayesFilter evidence anchors"):
        _result_manifest(
            source_governance_status=highdim.ModelSuiteTraceabilityStatus.SOURCE_MATCHED,
            bayesfilter_evidence_anchors=(),
        )


def test_reference_only_result_can_record_no_bayesfilter_evidence():
    manifest = _result_manifest()

    assert manifest.source_governance_status is highdim.ModelSuiteTraceabilityStatus.REFERENCE_ONLY
    assert manifest.bayesfilter_evidence_anchors == ()
    assert "not BayesFilter evidence" in manifest.non_claims


def test_model_suite_symbols_are_subpackage_scoped():
    assert "P30ModelSuiteFixtureManifest" in highdim.__all__
    assert "p30_model_suite_registry" in highdim.__all__
