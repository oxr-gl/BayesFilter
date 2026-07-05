from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import pytest

from bayesfilter.ssm import (
    BayesianSSMProblem,
    FilterProgramDescriptor,
    InvalidFilterRegistryContract,
    ParameterChart,
    ParameterPrior,
    SSMDataSignature,
    SSMStaticShape,
    SSMTargetContract,
    build_filter_program_registry,
    stable_filter_descriptor_signature,
    stable_filter_program_signature,
    validate_ssm_target_contract,
)


def _problem(**overrides):
    values = {
        "problem_id": "toy-nonlinear-ssm",
        "static_shape": SSMStaticShape(
            horizon=4,
            state_dim=2,
            observation_dim=1,
            innovation_dim=1,
            parameter_dim=3,
        ),
        "data_signature": SSMDataSignature(
            dataset_id="toy-nonlinear-data",
            observation_shape=(4, 1),
            data_hash="sha256:data-v1",
        ),
        "target_coordinate_convention": "unconstrained",
        "model_manifest": {
            "model_id": "toy-nonlinear-model",
            "model_hash": "sha256:model-v1",
            "capabilities": ("transition_mean", "observation_mean"),
        },
    }
    values.update(overrides)
    return BayesianSSMProblem(**values)


def _chart():
    return ParameterChart(
        parameter_names=("rho", "sigma", "beta"),
        unconstrained_dim=3,
        constrained_shape=(3,),
        transform_manifest={
            "transform_id": "identity-chart",
            "transform_hash": "sha256:chart-v1",
        },
        log_jacobian_convention="not_included",
    )


def _prior():
    return ParameterPrior(
        prior_manifest={
            "prior_id": "toy-gaussian-prior",
            "prior_hash": "sha256:prior-v1",
        },
        support_policy="unbounded",
        log_density_authority="graph_native",
    )


def _descriptor(**overrides):
    values = {
        "filter_id": "toy-deterministic-filter",
        "required_model_capabilities": ("transition_mean", "observation_mean"),
        "deterministic_target_policy": "deterministic",
        "approximation_semantics": "deterministic_approximation",
        "implementation_backend": "tensorflow",
        "filter_hash": "sha256:filter-v1",
        "manifest_extra": {"family": "toy"},
    }
    values.update(overrides)
    return FilterProgramDescriptor(**values)


def test_filter_registry_exports_are_public_and_lazy() -> None:
    import bayesfilter.ssm as ssm

    expected = {
        "FilterProgramDescriptor",
        "FilterProgramRegistry",
        "FilterRegistryDecision",
        "InvalidFilterRegistryContract",
        "build_filter_program_registry",
        "stable_filter_descriptor_signature",
    }

    assert expected.issubset(set(ssm.__all__))
    assert all(hasattr(ssm, name) for name in expected)


def test_filter_registry_accepts_capability_match_and_preserves_filter_program_signature() -> None:
    descriptor = _descriptor()
    registry = build_filter_program_registry([descriptor])

    decision = registry.bind_filter_program(
        filter_id="toy-deterministic-filter",
        problem=_problem(),
    )
    repeated = registry.bind_filter_program(
        filter_id="toy-deterministic-filter",
        problem=_problem(),
    )

    assert decision.decision == "accepted"
    assert decision.missing_model_capabilities == ()
    assert decision.descriptor_signature == stable_filter_descriptor_signature(descriptor)
    assert stable_filter_program_signature(decision.filter_program) == stable_filter_program_signature(
        repeated.filter_program
    )
    assert decision.filter_program.filter_manifest["descriptor_signature"] == (
        stable_filter_descriptor_signature(descriptor)
    )


def test_filter_registry_output_feeds_ssm_target_contract_validation() -> None:
    registry = build_filter_program_registry([_descriptor()])
    decision = registry.bind_filter_program(
        filter_id="toy-deterministic-filter",
        problem=_problem(),
    )
    contract = SSMTargetContract(
        problem=_problem(),
        chart=_chart(),
        prior=_prior(),
        filter_program=decision.filter_program,
    )

    assert validate_ssm_target_contract(
        contract,
        require_filter_hmc_target_ready=True,
    ) is contract


def test_filter_registry_rejects_missing_model_capability() -> None:
    registry = build_filter_program_registry(
        [
            _descriptor(
                filter_id="toy-ukf",
                required_model_capabilities=("transition_jacobian",),
                filter_hash="sha256:ukf-v1",
            )
        ]
    )

    with pytest.raises(InvalidFilterRegistryContract, match="missing required"):
        registry.bind_filter_program(filter_id="toy-ukf", problem=_problem())


def test_filter_registry_rejects_stochastic_filter_without_deterministic_artifact_state() -> None:
    registry = build_filter_program_registry(
        [
            _descriptor(
                filter_id="toy-particle-filter",
                deterministic_target_policy="stochastic_not_hmc_ready",
                approximation_semantics="fixed_randomness_approximation",
                filter_hash="sha256:pf-v1",
            )
        ]
    )

    with pytest.raises(InvalidFilterRegistryContract, match="stochastic filter"):
        registry.bind_filter_program(
            filter_id="toy-particle-filter",
            problem=_problem(),
        )


def test_filter_registry_can_accept_fixed_randomness_when_explicitly_allowed() -> None:
    registry = build_filter_program_registry(
        [
            _descriptor(
                filter_id="toy-fixed-particle-filter",
                deterministic_target_policy="fixed_randomness",
                approximation_semantics="fixed_randomness_approximation",
                filter_hash="sha256:fixed-pf-v1",
                manifest_extra={"deterministic_artifact_state": "sha256:particles-v1"},
            )
        ]
    )

    decision = registry.bind_filter_program(
        filter_id="toy-fixed-particle-filter",
        problem=_problem(),
        allow_fixed_randomness=True,
    )

    assert decision.filter_program.hmc_target_ready is True
    with pytest.raises(InvalidFilterRegistryContract, match="fixed-randomness"):
        registry.bind_filter_program(
            filter_id="toy-fixed-particle-filter",
            problem=_problem(),
            allow_fixed_randomness=False,
        )


def test_filter_registry_rejects_duplicate_descriptor_and_process_local_identity() -> None:
    with pytest.raises(InvalidFilterRegistryContract, match="unique"):
        build_filter_program_registry([_descriptor(), _descriptor()])

    with pytest.raises(InvalidFilterRegistryContract, match="process-local"):
        _descriptor(manifest_extra={"source": f"object at 0x{id(object()):x}"})


def test_filter_registry_rejects_unknown_filter_id_and_empty_capability_set() -> None:
    registry = build_filter_program_registry([_descriptor()])

    with pytest.raises(InvalidFilterRegistryContract, match="unknown filter_id"):
        registry.bind_filter_program(filter_id="missing", problem=_problem())

    with pytest.raises(InvalidFilterRegistryContract, match="nonempty"):
        _descriptor(required_model_capabilities=())
