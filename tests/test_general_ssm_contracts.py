from __future__ import annotations

import importlib

import pytest

from bayesfilter.ssm import (
    BayesianSSMProblem,
    FilterProgram,
    FrozenTransportBinding,
    InvalidSSMContract,
    ParameterChart,
    ParameterPrior,
    SSMDataSignature,
    SSMStaticShape,
    SSMTargetContract,
    stable_filter_program_signature,
    stable_frozen_transport_signature,
    stable_parameter_chart_signature,
    stable_prior_signature,
    stable_problem_signature,
    stable_ssm_target_signature,
    validate_ssm_target_contract,
)


EXPECTED_SSM_EXPORTS = {
    "ApproximationSemantics",
    "BatchRankPolicy",
    "BatchValueScoreFn",
    "BayesianSSMProblem",
    "DeterministicTargetPolicy",
    "FilterProgram",
    "FilterProgramDescriptor",
    "FilterProgramRegistry",
    "FilterRegistryDecision",
    "FrozenTransportBinding",
    "GenericSSMPosteriorAdapter",
    "InvalidFilterRegistryContract",
    "InvalidSSMContract",
    "InvalidSSMTargetBuilderContract",
    "LogJacobianConvention",
    "ParameterChart",
    "ParameterPrior",
    "PriorLogDensityAuthority",
    "PriorSupportPolicy",
    "SSMDataSignature",
    "SSMStaticShape",
    "SSMTargetContract",
    "SSMTargetBuilderMetadata",
    "TARGET_BUILDER_NONCLAIMS",
    "TargetCoordinateConvention",
    "build_filter_program_registry",
    "build_ssm_posterior_adapter",
    "stable_filter_descriptor_signature",
    "stable_filter_program_signature",
    "stable_frozen_transport_signature",
    "stable_parameter_chart_signature",
    "stable_ssm_posterior_adapter_signature",
    "stable_prior_signature",
    "stable_problem_signature",
    "stable_ssm_target_signature",
    "validate_ssm_target_contract",
}


def _static_shape(**overrides):
    values = {
        "horizon": 4,
        "state_dim": 2,
        "observation_dim": 1,
        "innovation_dim": 1,
        "parameter_dim": 3,
    }
    values.update(overrides)
    return SSMStaticShape(**values)


def _data_signature(**overrides):
    values = {
        "dataset_id": "toy-nonlinear-data",
        "observation_shape": (4, 1),
        "mask_shape": None,
        "data_hash": "sha256:data-v1",
    }
    values.update(overrides)
    return SSMDataSignature(**values)


def _problem(**overrides):
    values = {
        "problem_id": "toy-nonlinear-ssm",
        "static_shape": _static_shape(),
        "data_signature": _data_signature(),
        "target_coordinate_convention": "unconstrained",
        "model_manifest": {
            "model_id": "toy-nonlinear-model",
            "model_hash": "sha256:model-v1",
            "capabilities": ("transition_mean", "observation_mean"),
        },
    }
    values.update(overrides)
    return BayesianSSMProblem(**values)


def _chart(**overrides):
    values = {
        "parameter_names": ("rho", "sigma", "beta"),
        "unconstrained_dim": 3,
        "constrained_shape": (3,),
        "transform_manifest": {
            "transform_id": "identity-chart",
            "transform_hash": "sha256:chart-v1",
        },
        "log_jacobian_convention": "not_included",
    }
    values.update(overrides)
    return ParameterChart(**values)


def _prior(**overrides):
    values = {
        "prior_manifest": {
            "prior_id": "toy-gaussian-prior",
            "prior_hash": "sha256:prior-v1",
        },
        "support_policy": "unbounded",
        "log_density_authority": "graph_native",
    }
    values.update(overrides)
    return ParameterPrior(**values)


def _filter_program(**overrides):
    values = {
        "filter_id": "toy-ekf",
        "required_model_capabilities": ("transition_mean", "observation_mean"),
        "deterministic_target_policy": "deterministic",
        "approximation_semantics": "deterministic_approximation",
        "filter_manifest": {
            "filter_id": "toy-ekf",
            "filter_hash": "sha256:filter-v1",
            "backend": "tensorflow",
        },
    }
    values.update(overrides)
    return FilterProgram(**values)


def _target_without_transport(**overrides):
    values = {
        "problem": _problem(),
        "chart": _chart(),
        "prior": _prior(),
        "filter_program": _filter_program(),
        "frozen_transport": None,
    }
    values.update(overrides)
    return SSMTargetContract(**values)


def _transport_for(contract: SSMTargetContract, **overrides):
    target_signature = stable_ssm_target_signature(contract)
    values = {
        "transport_id": "toy-frozen-neutra",
        "dimension": 3,
        "target_signature": target_signature,
        "log_jacobian_available": True,
        "transport_manifest": {
            "transport_id": "toy-frozen-neutra",
            "transport_hash": "sha256:transport-v1",
            "target_signature": target_signature,
        },
    }
    values.update(overrides)
    return FrozenTransportBinding(**values)


def test_ssm_public_namespace_export_allowlist() -> None:
    module = importlib.import_module("bayesfilter.ssm")

    assert set(module.__all__) == EXPECTED_SSM_EXPORTS
    assert all(hasattr(module, name) for name in EXPECTED_SSM_EXPORTS)


def test_core_import_smoke_includes_ssm_without_tensorflow_import_requirement() -> None:
    bayesfilter = importlib.import_module("bayesfilter")
    inference = importlib.import_module("bayesfilter.inference")
    ssm = importlib.import_module("bayesfilter.ssm")

    assert bayesfilter is not None
    assert inference is not None
    assert ssm is not None


def test_problem_identity_positive_and_stable_signature() -> None:
    left = _problem()
    right = _problem()
    changed = _problem(problem_id="toy-nonlinear-ssm-v2")

    assert stable_problem_signature(left) == stable_problem_signature(right)
    assert stable_problem_signature(left) != stable_problem_signature(changed)


def test_problem_identity_rejects_missing_dimension_and_process_local_identity() -> None:
    with pytest.raises(InvalidSSMContract, match="state_dim must be positive"):
        _static_shape(state_dim=0)

    with pytest.raises(InvalidSSMContract, match="process-local"):
        _problem(
            model_manifest={
                "model_id": f"object at 0x{id(object()):x}",
                "model_hash": "sha256:model-v1",
            }
        )


def test_parameter_chart_positive_and_stable_signature() -> None:
    left = _chart()
    right = _chart()
    changed = _chart(
        transform_manifest={
            "transform_id": "identity-chart",
            "transform_hash": "sha256:chart-v2",
        }
    )

    assert stable_parameter_chart_signature(left) == stable_parameter_chart_signature(right)
    assert stable_parameter_chart_signature(left) != stable_parameter_chart_signature(changed)


def test_parameter_chart_rejects_duplicate_names_and_missing_transform_hash() -> None:
    with pytest.raises(InvalidSSMContract, match="parameter_names must be unique"):
        _chart(parameter_names=("rho", "rho", "beta"))

    with pytest.raises(InvalidSSMContract, match="transform_manifest missing required key"):
        _chart(transform_manifest={"transform_id": "identity-chart"})


def test_parameter_prior_positive_and_stable_signature() -> None:
    left = _prior()
    right = _prior()
    changed = _prior(
        prior_manifest={
            "prior_id": "toy-gaussian-prior",
            "prior_hash": "sha256:prior-v2",
        }
    )

    assert stable_prior_signature(left) == stable_prior_signature(right)
    assert stable_prior_signature(left) != stable_prior_signature(changed)


def test_parameter_prior_rejects_missing_manifest_and_unknown_authority() -> None:
    with pytest.raises(InvalidSSMContract, match="prior_manifest missing required key"):
        _prior(prior_manifest={"prior_id": "toy-gaussian-prior"})

    with pytest.raises(InvalidSSMContract, match="unknown prior log_density_authority"):
        _prior(log_density_authority="fallback")  # type: ignore[arg-type]


def test_filter_program_positive_and_stable_signature() -> None:
    left = _filter_program()
    right = _filter_program()
    changed = _filter_program(
        filter_manifest={
            "filter_id": "toy-ekf",
            "filter_hash": "sha256:filter-v2",
        }
    )

    assert stable_filter_program_signature(left) == stable_filter_program_signature(right)
    assert stable_filter_program_signature(left) != stable_filter_program_signature(changed)
    assert left.hmc_target_ready is True


def test_filter_program_rejects_missing_capabilities_and_unknown_target_policy() -> None:
    with pytest.raises(InvalidSSMContract, match="required_model_capabilities"):
        _filter_program(required_model_capabilities=())

    with pytest.raises(InvalidSSMContract, match="unknown deterministic_target_policy"):
        _filter_program(deterministic_target_policy="random")  # type: ignore[arg-type]


def test_frozen_transport_positive_and_stable_signature() -> None:
    base = _target_without_transport()
    left = _transport_for(base)
    right = _transport_for(base)
    changed = _transport_for(
        base,
        transport_manifest={
            "transport_id": "toy-frozen-neutra",
            "transport_hash": "sha256:transport-v2",
            "target_signature": stable_ssm_target_signature(base),
        },
    )

    assert stable_frozen_transport_signature(left) == stable_frozen_transport_signature(right)
    assert stable_frozen_transport_signature(left) != stable_frozen_transport_signature(changed)


def test_frozen_transport_rejects_missing_binding_and_dimension_mismatch() -> None:
    base = _target_without_transport()

    with pytest.raises(InvalidSSMContract, match="transport_manifest missing required key"):
        _transport_for(
            base,
            transport_manifest={
                "transport_id": "toy-frozen-neutra",
                "transport_hash": "sha256:transport-v1",
            },
        )

    with pytest.raises(InvalidSSMContract, match="dimension must match"):
        SSMTargetContract(
            problem=base.problem,
            chart=base.chart,
            prior=base.prior,
            filter_program=base.filter_program,
            frozen_transport=_transport_for(base, dimension=2),
        )


def test_ssm_target_contract_validates_full_binding_and_optional_transport_gate() -> None:
    base = _target_without_transport()
    transport = _transport_for(base)
    transported = SSMTargetContract(
        problem=base.problem,
        chart=base.chart,
        prior=base.prior,
        filter_program=base.filter_program,
        frozen_transport=transport,
    )

    assert validate_ssm_target_contract(transported, require_frozen_transport=True) is transported
    assert stable_ssm_target_signature(base) != stable_ssm_target_signature(transported)


def test_ssm_target_contract_rejects_missing_transport_binding_and_nonready_filter() -> None:
    base = _target_without_transport()

    with pytest.raises(InvalidSSMContract, match="frozen transport binding is required"):
        validate_ssm_target_contract(base, require_frozen_transport=True)

    nonready = _target_without_transport(
        filter_program=_filter_program(
            deterministic_target_policy="stochastic_not_hmc_ready",
            approximation_semantics="fixed_randomness_approximation",
        )
    )
    with pytest.raises(InvalidSSMContract, match="filter program must be deterministic"):
        validate_ssm_target_contract(nonready, require_filter_hmc_target_ready=True)
