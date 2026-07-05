from __future__ import annotations

import json
from pathlib import Path

from bayesfilter.ssm import (
    BayesianSSMProblem,
    FilterProgram,
    ParameterChart,
    ParameterPrior,
    SSMDataSignature,
    SSMStaticShape,
    SSMTargetContract,
    stable_ssm_target_signature,
    validate_ssm_target_contract,
)


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-2026-07-04.json"
)


def _jsonable(value):
    return json.loads(json.dumps(value, sort_keys=True))


def _load_manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _contract_from_manifest() -> SSMTargetContract:
    payload = _load_manifest()["target_contract_manifest"]
    problem = payload["problem"]
    chart = payload["chart"]
    prior = payload["prior"]
    filter_program = payload["filter_program"]
    return SSMTargetContract(
        problem=BayesianSSMProblem(
            problem_id=problem["problem_id"],
            static_shape=SSMStaticShape(**problem["static_shape"]),
            data_signature=SSMDataSignature(**problem["data_signature"]),
            target_coordinate_convention=problem["target_coordinate_convention"],
            model_manifest=problem["model_manifest"],
        ),
        chart=ParameterChart(
            parameter_names=tuple(chart["parameter_names"]),
            unconstrained_dim=chart["unconstrained_dim"],
            constrained_shape=tuple(chart["constrained_shape"]),
            transform_manifest=chart["transform_manifest"],
            log_jacobian_convention=chart["log_jacobian_convention"],
        ),
        prior=ParameterPrior(
            prior_manifest=prior["prior_manifest"],
            support_policy=prior["support_policy"],
            log_density_authority=prior["log_density_authority"],
        ),
        filter_program=FilterProgram(
            filter_id=filter_program["filter_id"],
            required_model_capabilities=tuple(
                filter_program["required_model_capabilities"]
            ),
            deterministic_target_policy=filter_program["deterministic_target_policy"],
            approximation_semantics=filter_program["approximation_semantics"],
            filter_manifest=filter_program["filter_manifest"],
        ),
        frozen_transport=None,
    )


def test_rotemberg_manifest_instantiates_contract_and_validates() -> None:
    manifest = _load_manifest()
    contract = _contract_from_manifest()
    validated = validate_ssm_target_contract(
        contract,
        require_filter_hmc_target_ready=True,
    )
    payload = manifest["target_contract_manifest"]
    expected_payload = dict(payload)
    expected_payload["frozen_transport"] = None
    expected_payload.pop("status", None)
    signature = stable_ssm_target_signature(contract)

    assert manifest["status"] == "PHASE2_MANIFEST_DRAFT_READY_FOR_PHASE3_VALIDATION"
    assert payload["status"] == "draft_not_canonical_signature"
    assert validated is contract
    assert contract.frozen_transport is None
    assert contract.problem.static_shape.state_dim == 6
    assert contract.problem.model_manifest["structural_state_dim"] == 4
    assert _jsonable(contract.manifest_payload()) == _jsonable(expected_payload)
    assert stable_ssm_target_signature(_contract_from_manifest()) == signature
    assert len(signature) == 64
    assert all(ch in "0123456789abcdef" for ch in signature)


def test_rotemberg_manifest_keeps_transport_binding_absent() -> None:
    manifest = _load_manifest()

    assert "frozen_transport" not in manifest["target_contract_manifest"]
